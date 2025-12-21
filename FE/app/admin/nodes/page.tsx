"use client"

import * as React from "react"
import { Plus, Search, Pencil, Trash2, Loader2, Save } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    SheetFooter,
    SheetClose,
} from "@/components/ui/sheet"
import { Separator } from "@/components/ui/separator"

// --- Types ---
type KnowledgeType = "DoiTuong" | "HanhVi" | "CheTai" | "KhaiNiem" | "DieuLuat" | "CoQuan" | "QuyenNghiaVu"

type NodeData = {
    id: string
    name: string
    type: string
    description?: string
    source?: string
    properties: Record<string, any>
}

// --- API ---
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function searchNodes(query: string): Promise<NodeData[]> {
    const res = await fetch(`${API_BASE_URL}/api/v1/admin/nodes/search?q=${encodeURIComponent(query)}`)
    if (!res.ok) throw new Error("Failed to fetch nodes")
    return res.json()
}

async function createNode(data: any): Promise<NodeData> {
    const res = await fetch(`${API_BASE_URL}/api/v1/admin/nodes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error("Failed to create node")
    return res.json()
}

async function updateNode(id: string, data: any): Promise<NodeData> {
    const res = await fetch(`${API_BASE_URL}/api/v1/admin/nodes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    if (!res.ok) throw new Error("Failed to update node")
    return res.json()
}

async function deleteNode(id: string): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/api/v1/admin/nodes/${id}`, {
        method: "DELETE"
    })
    if (!res.ok) throw new Error("Failed to delete node")
}

// --- Page Component ---
export default function AdminNodesPage() {
    const [nodes, setNodes] = React.useState<NodeData[]>([])
    const [query, setQuery] = React.useState("")
    const [loading, setLoading] = React.useState(false)
    const [isSheetOpen, setIsSheetOpen] = React.useState(false)
    const [editingNode, setEditingNode] = React.useState<NodeData | null>(null)

    // Form Stats
    const [formData, setFormData] = React.useState({
        name: "",
        type: "KhaiNiem",
        description: "",
        source: "",
        extraProps: "{}"
    })

    const fetchNodes = React.useCallback(async () => {
        setLoading(true)
        try {
            const data = await searchNodes(query)
            setNodes(data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }, [query])

    // Initial load
    React.useEffect(() => {
        fetchNodes()
    }, [fetchNodes])

    const handleEdit = (node: NodeData) => {
        setEditingNode(node)
        setFormData({
            name: node.name,
            type: node.type,
            description: node.description || "",
            source: node.source || "",
            extraProps: JSON.stringify(node.properties, null, 2)
        })
        setIsSheetOpen(true)
    }

    const handleCreate = () => {
        setEditingNode(null)
        setFormData({
            name: "",
            type: "KhaiNiem",
            description: "",
            source: "",
            extraProps: "{}"
        })
        setIsSheetOpen(true)
    }

    const handleSubmit = async () => {
        setLoading(true)
        try {
            const props = JSON.parse(formData.extraProps || "{}")
            // Merge form fields into props - use noi_dung for description
            props.ten = formData.name
            props.noi_dung = formData.description  // Use noi_dung instead of mo_ta
            props.mo_ta = formData.description     // Also set mo_ta for compatibility
            props.dieu_khoan = formData.source

            // Backend expects:
            // labels: [Type]
            // properties: {...}

            if (editingNode) {
                const result = await updateNode(editingNode.id, { properties: props })
                console.log("Update result:", result)
            } else {
                const result = await createNode({
                    labels: [formData.type],
                    properties: props
                })
                console.log("Create result:", result)
            }

            setIsSheetOpen(false)
            await fetchNodes() // Refresh list
        } catch (err) {
            console.error("Submit error:", err)
            alert(`Error: ${err}`)
        } finally {
            setLoading(false)
        }
    }

    const handleDelete = async (id: string) => {
        if (!confirm("Bạn có chắc chắn muốn xóa node này không?")) return
        setLoading(true)
        try {
            console.log("Deleting node:", id)
            await deleteNode(id)
            console.log("Delete successful")
            await fetchNodes()  // Wait for refresh
        } catch (err) {
            console.error("Delete error:", err)
            alert(`Lỗi khi xóa: ${err}`)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-white">Nodes Management</h1>
                    <p className="text-zinc-400">View and manage knowledge graph entities.</p>
                </div>
                <Button onClick={handleCreate} className="bg-emerald-600 hover:bg-emerald-700">
                    <Plus className="mr-2 h-4 w-4" /> Add Node
                </Button>
            </div>

            {/* Search Bar */}
            <div className="flex items-center gap-2 bg-zinc-800 p-2 rounded-lg border border-zinc-700">
                <Search className="h-5 w-5 text-zinc-400 ml-2" />
                <Input
                    placeholder="Search nodes by name..."
                    className="bg-transparent border-none text-white focus-visible:ring-0"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && fetchNodes()}
                />
                <Button variant="secondary" onClick={fetchNodes}>Search</Button>
            </div>

            {/* Table */}
            <div className="border border-zinc-700 rounded-lg overflow-hidden">
                <table className="w-full text-sm text-left text-zinc-300">
                    <thead className="text-xs uppercase bg-zinc-800 text-zinc-400">
                        <tr>
                            <th className="px-6 py-4 font-medium">Name</th>
                            <th className="px-6 py-4 font-medium">Type</th>
                            <th className="px-6 py-4 font-medium">Description</th>
                            <th className="px-6 py-4 font-medium">Source</th>
                            <th className="px-6 py-4 font-medium text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-zinc-700 bg-zinc-900">
                        {loading ? (
                            <tr><td colSpan={5} className="p-8 text-center"><Loader2 className="animate-spin h-6 w-6 mx-auto" /></td></tr>
                        ) : nodes.length === 0 ? (
                            <tr><td colSpan={5} className="p-8 text-center text-zinc-500">No nodes found. try searching using keywords.</td></tr>
                        ) : (
                            nodes.map((node) => (
                                <tr key={node.id} className="hover:bg-zinc-800/50 transition-colors">
                                    <td className="px-6 py-4 font-medium text-white">{node.name}</td>
                                    <td className="px-6 py-4">
                                        <Badge variant="outline" className="bg-zinc-800 border-zinc-600">
                                            {node.type}
                                        </Badge>
                                    </td>
                                    <td className="px-6 py-4 max-w-xs truncate" title={node.description}>
                                        {node.description || <span className="text-zinc-600 italic">--</span>}
                                    </td>
                                    <td className="px-6 py-4">{node.source || <span className="text-zinc-600 italic">--</span>}</td>
                                    <td className="px-6 py-4 text-right space-x-2">
                                        <Button size="icon" variant="ghost" className="h-8 w-8 text-zinc-400 hover:text-white" onClick={() => handleEdit(node)}>
                                            <Pencil className="h-4 w-4" />
                                        </Button>
                                        <Button size="icon" variant="ghost" className="h-8 w-8 text-red-400 hover:text-red-300 hover:bg-red-900/20" onClick={() => handleDelete(node.id)}>
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Edit/Create Sheet */}
            <Sheet open={isSheetOpen} onOpenChange={setIsSheetOpen}>
                <SheetContent className="bg-zinc-900 border-l border-zinc-700 text-zinc-100 sm:max-w-md overflow-y-auto">
                    <SheetHeader>
                        <SheetTitle className="text-white">{editingNode ? "Edit Node" : "Create Node"}</SheetTitle>
                        <SheetDescription>
                            Make changes to the knowledge node here. Click save when you're done.
                        </SheetDescription>
                    </SheetHeader>
                    <div className="grid gap-4 py-8">
                        <div className="grid gap-2">
                            <label className="text-sm font-medium">Name</label>
                            <Input
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="bg-zinc-800 border-zinc-700"
                            />
                        </div>
                        <div className="grid gap-2">
                            <label className="text-sm font-medium">Type (Label)</label>
                            <select
                                className="flex h-10 w-full rounded-md border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white"
                                value={formData.type}
                                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                                disabled={!!editingNode} // Neo4j labels are hard to change simply
                            >
                                <option value="KhaiNiem">KhaiNiem</option>
                                <option value="DoiTuong">DoiTuong</option>
                                <option value="HanhVi">HanhVi</option>
                                <option value="CheTai">CheTai</option>
                                <option value="DieuLuat">DieuLuat</option>
                                <option value="CoQuan">CoQuan</option>
                                <option value="QuyenNghiaVu">QuyenNghiaVu</option>
                            </select>
                        </div>
                        <div className="grid gap-2">
                            <label className="text-sm font-medium">Description</label>
                            <textarea
                                className="flex min-h-[80px] w-full rounded-md border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white"
                                value={formData.description}
                                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            />
                        </div>
                        <div className="grid gap-2">
                            <label className="text-sm font-medium">Source / Reference</label>
                            <Input
                                value={formData.source}
                                onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                                className="bg-zinc-800 border-zinc-700"
                            />
                        </div>
                        <Separator className="bg-zinc-700 my-2" />
                        <div className="grid gap-2">
                            <label className="text-sm font-medium">Raw Properties (JSON)</label>
                            <textarea
                                className="flex min-h-[150px] w-full rounded-md border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm font-mono text-zinc-300"
                                value={formData.extraProps}
                                onChange={(e) => setFormData({ ...formData, extraProps: e.target.value })}
                            />
                        </div>
                    </div>
                    <SheetFooter>
                        <SheetClose asChild>
                            <Button variant="outline" className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">Cancel</Button>
                        </SheetClose>
                        <Button onClick={handleSubmit} className="bg-emerald-600 hover:bg-emerald-700">
                            <Save className="mr-2 h-4 w-4" /> Save Changes
                        </Button>
                    </SheetFooter>
                </SheetContent>
            </Sheet>
        </div>
    )
}
