import Link from "next/link"
import { Bot, Database, Share2, Home, Settings, Activity } from "lucide-react"

export default function AdminLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="flex h-screen w-full bg-zinc-950 text-zinc-100">
            {/* Sidebar */}
            <aside className="w-64 border-r border-white/10 flex flex-col">
                <div className="h-14 flex items-center px-6 border-b border-white/10">
                    <Database className="h-6 w-6 text-emerald-400 mr-2" />
                    <span className="font-bold text-lg">Knowledge Admin</span>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <Link href="/" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-white/5 text-zinc-400 hover:text-white transition-colors">
                        <Home className="h-5 w-5" />
                        Về Trang chủ
                    </Link>
                    <div className="px-3 py-2 text-xs font-semibold text-zinc-500 uppercase mt-2">Dashboard</div>
                    <Link href="/admin" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-white/5 text-zinc-400 hover:text-white transition-colors">
                        <Activity className="h-5 w-5" />
                        Tổng quan
                    </Link>
                    <Link href="/admin/nodes" className="flex items-center gap-3 px-3 py-2 rounded-md bg-white/5 text-white font-medium">
                        <Share2 className="h-5 w-5" />
                        Manage Nodes
                    </Link>
                    {/* Future: Relationships */}
                    <div className="px-3 py-2 text-xs font-semibold text-zinc-500 uppercase mt-4">System</div>
                    <Link href="/chatbot" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-white/5 text-zinc-400 hover:text-white transition-colors">
                        <Bot className="h-5 w-5" />
                        Back to Chatbot
                    </Link>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto bg-zinc-900">
                <div className="p-8 max-w-6xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    )
}
