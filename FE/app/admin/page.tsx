"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, Share2, Activity } from "lucide-react"
import Link from "next/link"
import { useEffect, useState } from "react"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type StatsData = {
    total_nodes: number
    total_relationships: number
    status: string
}

export default function AdminDashboard() {
    const [stats, setStats] = useState<StatsData | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchStats() {
            try {
                const response = await fetch(`${API_BASE_URL}/api/admin/stats`)
                if (response.ok) {
                    const data = await response.json()
                    setStats(data)
                }
            } catch (error) {
                console.error("Failed to fetch stats:", error)
            } finally {
                setLoading(false)
            }
        }
        fetchStats()
    }, [])

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-zinc-400 mt-2">Tổng quan về Cơ sở tri thức (Knowledge Graph).</p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
                <Card className="bg-zinc-800 border-zinc-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-zinc-200">Total Nodes</CardTitle>
                        <Database className="h-4 w-4 text-emerald-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">
                            {loading ? "..." : (stats?.total_nodes ?? "--")}
                        </div>
                        <p className="text-xs text-zinc-400">Entities & Concepts</p>
                    </CardContent>
                </Card>
                <Card className="bg-zinc-800 border-zinc-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-zinc-200">Relationships</CardTitle>
                        <Share2 className="h-4 w-4 text-blue-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">
                            {loading ? "..." : (stats?.total_relationships ?? "--")}
                        </div>
                        <p className="text-xs text-zinc-400">Total connections</p>
                    </CardContent>
                </Card>
                <Card className="bg-zinc-800 border-zinc-700">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-zinc-200">System Status</CardTitle>
                        <Activity className="h-4 w-4 text-green-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">
                            {loading ? "..." : (stats?.status === "connected" ? "Online" : "Offline")}
                        </div>
                        <p className="text-xs text-zinc-400">Neo4j Connection</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4 bg-zinc-800 border-zinc-700">
                    <CardHeader>
                        <CardTitle className="text-white">Quick Actions</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <Link href="/admin/nodes" className="block w-full p-4 border border-zinc-600 rounded-lg hover:bg-zinc-700 transition-colors">
                            <div className="font-semibold text-emerald-400">Manage Nodes</div>
                            <div className="text-sm text-zinc-400">Create, edit, or delete knowledge nodes.</div>
                        </Link>
                        {/* Add more actions */}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
