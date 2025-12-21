"use client"

import * as React from "react"
import Link from "next/link"
import { Send, Bot, User, Cpu, Share2, Home, Settings } from "lucide-react"

import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"

// --- Types ---

type Message = {
    id: string
    role: "user" | "bot"
    content: string
    timestamp: string
}

type GraphNode = {
    id: string
    label: string
    type: string
    x?: string
    y?: string
    color?: string
}

type ReasoningStep = {
    id: string
    title: string
    description: string
    relatedNodes: string[]
}

type GraphEdge = {
    id: string
    source: string  // Changed from 'from' to match BE
    target: string  // Changed from 'to' to match BE  
    label?: string
}

type APIResponse = {
    answer: string
    success: boolean
    reasoning_steps: ReasoningStep[]
    kg_nodes: GraphNode[]
    kg_edges: GraphEdge[]
    intent: string
    entity: string
    confidence: number
    best_reasoner: string | null
    error: string | null
}

const INITIAL_MESSAGES: Message[] = [
    {
        id: "1",
        role: "bot",
        content: "Xin chào! Tôi là trợ lý tra cứu Luật Bảo vệ Môi trường. Hãy đặt câu hỏi và tôi sẽ trả lời cùng quá trình suy luận.",
        timestamp: "",  // Empty to avoid hydration mismatch, will show no timestamp for welcome message
    },
]

// API endpoint configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
const API_ENDPOINT = `${API_BASE_URL}/api/v1/env-law/chat-with-reasoning`

// API call function
async function fetchChatResponse(question: string): Promise<APIResponse> {
    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, stream: false }),
    })

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
    }

    return response.json()
}

export default function ChatbotPage() {
    const [messages, setMessages] = React.useState<Message[]>(INITIAL_MESSAGES)
    const [inputValue, setInputValue] = React.useState("")
    const [isThinking, setIsThinking] = React.useState(false)

    // Track the reasoning data for the *latest* bot response
    const [currentReasoning, setCurrentReasoning] = React.useState<{ steps: ReasoningStep[], nodes: GraphNode[], edges: GraphEdge[] } | null>(null)

    const handleSendMessage = () => {
        if (!inputValue.trim()) return

        const newMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: inputValue,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }

        setMessages((prev) => [...prev, newMessage])
        setInputValue("")
        setIsThinking(true)
        setCurrentReasoning(null) // Hide old graph while thinking

        // Call the real API
        const questionText = inputValue.trim()

        fetchChatResponse(questionText)
            .then((apiResponse) => {
                setIsThinking(false)

                if (apiResponse.success) {
                    // Use the reasoning data from the API response
                    setCurrentReasoning({
                        steps: apiResponse.reasoning_steps,
                        nodes: apiResponse.kg_nodes,
                        edges: apiResponse.kg_edges
                    })

                    const botResponse: Message = {
                        id: (Date.now() + 1).toString(),
                        role: "bot",
                        content: apiResponse.answer || "Không có câu trả lời.",
                        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    }
                    setMessages((prev) => [...prev, botResponse])
                } else {
                    // Handle error from API
                    const errorResponse: Message = {
                        id: (Date.now() + 1).toString(),
                        role: "bot",
                        content: `Lỗi: ${apiResponse.error || "Không thể xử lý câu hỏi."}`,
                        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    }
                    setMessages((prev) => [...prev, errorResponse])
                }
            })
            .catch((error) => {
                setIsThinking(false)
                console.error("API Error:", error)

                const errorResponse: Message = {
                    id: (Date.now() + 1).toString(),
                    role: "bot",
                    content: `Lỗi kết nối: ${error.message}. Vui lòng kiểm tra Backend đã chạy chưa.`,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                }
                setMessages((prev) => [...prev, errorResponse])
            })
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleSendMessage()
        }
    }

    return (
        <div className="h-screen w-full flex flex-col overflow-hidden">
            <header className="h-14 border-b border-white/10 flex items-center px-6 bg-zinc-900 sticky top-0 z-10">
                <Link href="/" className="mr-4 text-zinc-400 hover:text-white transition-colors" title="Về trang chủ">
                    <Home className="h-5 w-5" />
                </Link>
                <div className="flex items-center gap-2 font-semibold text-2xl text-white">
                    <Bot className="h-8 w-8 text-emerald-400" />
                    <span>Chatbot Luật Môi Trường</span>
                </div>
                <div className="ml-auto flex items-center gap-2">
                    <Link href="/admin">
                        <Button variant="ghost" size="icon" className="text-zinc-400 hover:text-white" title="Quản trị Tri thức">
                            <Settings className="h-5 w-5" />
                        </Button>
                    </Link>
                    <Badge variant="outline" className="text-zinc-400 border-zinc-700 font-normal">
                        v2.0 - Knowledge Graph
                    </Badge>
                </div>
            </header>

            <div className="flex w-full flex-1 overflow-hidden">
                {/* Left Panel: Chat Interface */}
                <div className="w-[60%] border-r border-white/20 flex flex-col relative h-full">
                    {/* Background for left panel only */}
                    <div className="absolute inset-0 z-0 bg-gradient-to-br from-zinc-900 via-zinc-950 to-black"></div>

                    {/* Chat Messages Area - Scrollable */}
                    <div className="flex-1 overflow-hidden relative z-10">
                        <ScrollArea className="h-full">
                            <div className="flex flex-col gap-4 max-w-3xl mx-auto p-4 pb-8">
                                {messages.map((message) => (
                                    <div
                                        key={message.id}
                                        className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"
                                            }`}
                                    >
                                        {message.role === "bot" && (
                                            <Avatar className="h-8 w-8 border flex-shrink-0">
                                                <AvatarImage src="/bot-avatar.png" alt="Bot" />
                                                <AvatarFallback><Bot className="h-4 w-4" /></AvatarFallback>
                                            </Avatar>
                                        )}

                                        <div
                                            className={`rounded-2xl px-4 py-2.5 max-w-[80%] text-sm ${message.role === "user"
                                                ? "bg-emerald-600 text-white rounded-br-none"
                                                : "bg-white/10 text-zinc-100 rounded-bl-none backdrop-blur-sm"
                                                }`}
                                        >
                                            <p className="whitespace-pre-wrap">{message.content}</p>
                                            <span className="text-[10px] opacity-70 mt-1 block w-full text-right">
                                                {message.timestamp}
                                            </span>
                                        </div>

                                        {message.role === "user" && (
                                            <Avatar className="h-8 w-8 border flex-shrink-0">
                                                <AvatarImage src="/user-avatar.png" alt="User" />
                                                <AvatarFallback><User className="h-4 w-4" /></AvatarFallback>
                                            </Avatar>
                                        )}
                                    </div>
                                ))}
                                {isThinking && (
                                    <div className="flex gap-3 justify-start items-center ml-2">
                                        <Avatar className="h-8 w-8 border">
                                            <AvatarFallback><Bot className="h-4 w-4" /></AvatarFallback>
                                        </Avatar>
                                        <div className="text-xs text-zinc-400 animate-pulse">Thinking...</div>
                                    </div>
                                )}
                            </div>
                        </ScrollArea>
                    </div>

                    {/* Input Area - Fixed at bottom */}
                    <div className="relative z-10 p-4 border-t border-white/20 bg-zinc-900/95 backdrop-blur-md flex-shrink-0">
                        <div className="max-w-3xl mx-auto flex gap-2">
                            <Input
                                placeholder="Nhập câu hỏi của bạn..."
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyDown={handleKeyDown}
                                className="flex-1 bg-white/10 border-white/20 text-white placeholder:text-zinc-400 focus-visible:ring-emerald-500"
                            />
                            <Button onClick={handleSendMessage} size="icon" className="bg-emerald-600 hover:bg-emerald-700">
                                <Send className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </div>

                {/* Right Panel: Knowledge Graph & Reasoning */}
                <div className="w-[40%] bg-white pb-8">
                    <div className="h-full flex flex-col p-4 gap-4">

                        {/* 1. Reasoning Steps */}
                        {/* 1. Reasoning Steps */}
                        {/* 1. Reasoning Steps */}
                        <Card className="flex-1 flex flex-col shadow-2xl border-zinc-200 bg-white">
                            <CardHeader className="pb-3 border-b border-zinc-200">
                                <CardTitle className="text-base flex items-center gap-2 text-zinc-900">
                                    <Cpu className="h-4 w-4 text-blue-600" />
                                    Reasoning Process
                                </CardTitle>
                                <CardDescription className="text-zinc-600">Logical steps taken to answer</CardDescription>
                            </CardHeader>
                            <ScrollArea className="flex-1">
                                <CardContent className="p-4">
                                    {currentReasoning ? (
                                        <Accordion type="single" collapsible defaultValue="item-0" className="w-full">
                                            {currentReasoning.steps.map((step, index) => (
                                                <AccordionItem key={step.id} value={`item-${index}`}>
                                                    <AccordionTrigger className="text-sm font-medium py-2">
                                                        <div className="flex items-center gap-2 text-left">
                                                            <Badge variant="secondary" className="h-5 w-5 p-0 flex items-center justify-center rounded-full text-xs">
                                                                {index + 1}
                                                            </Badge>
                                                            {step.title}
                                                        </div>
                                                    </AccordionTrigger>
                                                    <AccordionContent>
                                                        <div className="pl-7 text-sm text-zinc-700">
                                                            <p className="mb-2">{step.description}</p>
                                                            <div className="flex flex-wrap gap-1">
                                                                {step.relatedNodes.map(node => (
                                                                    <Badge key={node} variant="outline" className="text-[10px] px-1 py-0 h-5 border-zinc-300 text-zinc-700">
                                                                        {node}
                                                                    </Badge>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </AccordionContent>
                                                </AccordionItem>
                                            ))}
                                        </Accordion>
                                    ) : (
                                        <div className="h-full flex flex-col items-center justify-center text-zinc-400 text-sm gap-2 min-h-[200px]">
                                            <Cpu className="h-8 w-8" />
                                            <span>Waiting for query...</span>
                                        </div>
                                    )}
                                </CardContent>
                            </ScrollArea>
                        </Card>

                        {/* 2. Knowledge Graph Visualization (Mock) */}
                        {/* 2. Knowledge Graph Visualization (Mock) */}
                        {/* 2. Knowledge Graph Visualization (Mock) */}
                        <Card className="h-1/2 flex flex-col shadow-2xl border-zinc-200 bg-white">
                            <CardHeader className="pb-3 border-b border-zinc-200">
                                <CardTitle className="text-base flex items-center gap-2 text-zinc-900">
                                    <Share2 className="h-4 w-4 text-indigo-600" />
                                    Knowledge Graph
                                </CardTitle>
                            </CardHeader>
                            <div className="flex-1 bg-zinc-50 relative overflow-hidden flex items-center justify-center p-4">
                                {currentReasoning ? (
                                    <div className="relative w-full h-full">
                                        {/* Render Dynamic Edges (First, to be behind nodes) */}
                                        <svg className="absolute inset-0 pointer-events-none w-full h-full opacity-40 text-zinc-400">
                                            {currentReasoning.edges && currentReasoning.edges.map(edge => {
                                                // Find nodes by matching label (since BE uses label text, not ID)
                                                const fromNode = currentReasoning.nodes.find(n =>
                                                    n.label === edge.source || n.id === edge.source || n.label.includes(edge.source)
                                                )
                                                const toNode = currentReasoning.nodes.find(n =>
                                                    n.label === edge.target || n.id === edge.target || n.label.includes(edge.target)
                                                )
                                                if (!fromNode || !toNode) return null

                                                return (
                                                    <line
                                                        key={edge.id}
                                                        x1={fromNode.x}
                                                        y1={fromNode.y}
                                                        x2={toNode.x}
                                                        y2={toNode.y}
                                                        stroke="#9ca3af"
                                                        strokeWidth="2"
                                                    />
                                                )
                                            })}
                                        </svg>

                                        {/* Render Dynamic Nodes (Second, to sit on top of lines) */}
                                        {currentReasoning.nodes.map((node) => {
                                            // Helper to get color code
                                            const getNodeColor = (type: string) => {
                                                const colors: Record<string, string> = {
                                                    "DoiTuong": "#2563eb", // Blue 600
                                                    "CoQuan": "#9333ea",   // Purple 600
                                                    "QuyenNghiaVu": "#16a34a", // Green 600
                                                    "HanhVi": "#dc2626",   // Red 600
                                                    "CheTai": "#ea580c",   // Orange 600
                                                    "KhaiNiem": "#0891b2", // Cyan 600
                                                    "DieuLuat": "#d97706", // Amber 600
                                                    "entity": "#4f46e5",   // Indigo 600
                                                    "concept": "#059669",  // Emerald 600
                                                }
                                                return colors[type] || "#52525b" // Zinc 600
                                            }

                                            return (
                                                <div
                                                    key={node.id}
                                                    className="absolute"
                                                    style={{ top: node.y, left: node.x, transform: 'translate(-50%, -50%)' }}
                                                >
                                                    <div
                                                        className="px-3 py-1.5 rounded-full text-white text-sm font-medium shadow-lg hover:scale-110 transition-transform cursor-default whitespace-nowrap z-10"
                                                        style={{ backgroundColor: getNodeColor(node.type) }}
                                                        title={node.type}
                                                    >
                                                        {node.label}
                                                    </div>
                                                </div>
                                            )
                                        })}

                                        <div className="absolute bottom-4 right-4 text-[10px] text-muted-foreground bg-background/80 px-2 py-1 rounded">
                                            Knowledge Graph (Live)
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex flex-col items-center justify-center text-zinc-400 text-sm gap-2">
                                        <Share2 className="h-8 w-8" />
                                        <span>Chưa có dữ liệu</span>
                                    </div>
                                )}
                            </div>
                        </Card>

                    </div>
                </div>
            </div>
        </div>

    )
}
