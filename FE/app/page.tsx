import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import Link from "next/link"
import { ArrowRight, BookOpen, Users } from "lucide-react"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Hero Section */}
      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center relative px-6 py-24 text-center overflow-hidden">
        {/* Background Image & Overlay */}
        <div className="absolute inset-0 z-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/hero-bg.png" alt="Background" className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-black/60"></div>
        </div>

        <div className="max-w-4xl space-y-6 relative z-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 backdrop-blur px-3 py-1 text-sm text-zinc-200 shadow-sm">
            <BookOpen className="h-4 w-4" />
            <span>Đồ án môn học: Biểu diễn Tri thức</span>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-6xl text-white">
            Chatbot Tra Cứu <span className="text-emerald-400">Luật Môi Trường</span>
          </h1>
          <p className="text-xl text-zinc-300 max-w-2xl mx-auto">
            Hệ thống hỗ trợ tra cứu nhanh chóng, chính xác các quy định pháp luật về môi trường, giúp nâng cao nhận thức và tuân thủ pháp luật.
          </p>
          <div className="pt-8 flex flex-col sm:flex-row gap-12 justify-center items-center">
            <Link href="/chatbot">
              <Button size="lg" className="rounded-full h-14 px-8 text-lg gap-2 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-1 bg-white text-black hover:bg-zinc-200 border-none">
                Truy cập Chatbot
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <Link href="/admin">
              <Button size="lg" variant="outline" className="rounded-full h-14 px-8 text-lg gap-2 border-white/30 bg-black/20 text-white hover:bg-white/10 backdrop-blur">
                Quản lý Tri thức
                <Users className="h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Environmental Context Section */}
      <section className="relative py-16 px-6 border-t border-zinc-800 text-white overflow-hidden">
        {/* Background Image & Overlay */}
        <div className="absolute inset-0 z-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/context-bg.png" alt="Context Background" className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-black/70"></div>
        </div>

        <div className="max-w-4xl mx-auto space-y-16 relative z-10">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white">Bối cảnh & Tầm quan trọng</h2>
            <p className="text-zinc-300 mt-2">Tại sao chúng ta cần quan tâm đến Luật Bảo vệ Môi trường?</p>
          </div>

          {/* Feature 1 - Left Aligned */}
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="md:w-1/2">
              <div className="rounded-xl overflow-hidden shadow-xl border-4 border-zinc-800">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/env-1.png" alt="Quốc hội thông qua Luật" className="w-full h-auto object-cover hover:scale-105 transition-transform duration-500" />
              </div>
            </div>
            <div className="md:w-1/2 space-y-4 text-center md:text-left">
              <h3 className="text-2xl font-semibold text-emerald-500">Cơ sở Pháp lý Vững chắc</h3>
              <p className="text-zinc-300 leading-relaxed">
                Quốc hội Việt Nam đã thông qua <strong>Luật Bảo vệ Môi trường 2020</strong>, đánh dấu bước ngoặt lớn trong công tác quản lý nhà nước,
                đặt mục tiêu phát triển bền vững và bảo vệ sức khỏe cộng đồng lên hàng đầu.
              </p>
            </div>
          </div>

          {/* Feature 2 - Right Aligned (Alternating) */}
          <div className="flex flex-col md:flex-row-reverse items-center gap-8">
            <div className="md:w-1/2">
              <div className="rounded-xl overflow-hidden shadow-xl border-4 border-white dark:border-zinc-800">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/env-2.png" alt="Thực trạng ô nhiễm" className="w-full h-auto object-cover hover:scale-105 transition-transform duration-500" />
              </div>
            </div>
            <div className="md:w-1/2 space-y-4 text-center md:text-left">
              <h3 className="text-2xl font-semibold text-emerald-500">Thách thức từ Thực tiễn</h3>
              <p className="text-zinc-300 leading-relaxed">
                Tình trạng khai thác tài nguyên bừa bãi và ô nhiễm môi trường đang diễn ra phức tạp.
                Việc nắm vững các quy định pháp luật là "tấm khiên" để mỗi cá nhân và doanh nghiệp tránh vi phạm và bảo vệ hệ sinh thái.
              </p>
            </div>
          </div>

          {/* Feature 3 - Left Aligned */}
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="md:w-1/2">
              <div className="rounded-xl overflow-hidden shadow-xl border-4 border-white dark:border-zinc-800">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src="/env-3.png" alt="Bảo vệ hành tinh" className="w-full h-auto object-cover hover:scale-105 transition-transform duration-500" />
              </div>
            </div>
            <div className="md:w-1/2 space-y-4 text-center md:text-left">
              <h3 className="text-2xl font-semibold text-emerald-500">Trách nhiệm Chung</h3>
              <p className="text-zinc-300 leading-relaxed">
                Bảo vệ môi trường không chỉ là nghĩa vụ pháp lý mà còn là trách nhiệm đạo đức.
                Cùng nhau, chúng ta gìn giữ màu xanh cho thế hệ tương lai thông qua hiểu biết và hành động đúng đắn.
              </p>
            </div>
          </div>

        </div>
      </section>

      {/* Team Section */}
      <section className="bg-background py-16 px-6 border-t">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold flex items-center justify-center gap-2">
              <Users className="h-8 w-8 text-primary" />
              Thành viên Thực hiện
            </h2>
            <p className="text-muted-foreground mt-2">Đội ngũ phát triển dự án</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Member 1 */}
            <Card className="text-center border-none shadow-md hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4">
                  <Avatar className="h-40 w-40 border-4 border-primary/10">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src="/member-1.png" alt="Lê Quang Long" className="h-full w-full object-cover" />
                    <AvatarFallback className="text-2xl bg-primary/5 text-primary">L</AvatarFallback>
                  </Avatar>
                </div>
                <CardTitle className="text-xl">Lê Quang Long</CardTitle>
              </CardHeader>
            </Card>

            {/* Member 2 */}
            <Card className="text-center border-none shadow-md hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4">
                  <Avatar className="h-40 w-40 border-4 border-primary/10">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src="/member-2.png" alt="Đỗ Tấn Lưc" className="h-full w-full object-cover" />
                    <AvatarFallback className="text-2xl bg-primary/5 text-primary">L</AvatarFallback>
                  </Avatar>
                </div>
                <CardTitle className="text-xl">Đỗ Tấn Lưc</CardTitle>
              </CardHeader>
            </Card>

            {/* Member 3 */}
            <Card className="text-center border-none shadow-md hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto mb-4">
                  <Avatar className="h-40 w-40 border-4 border-primary/10">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src="/member-3.png" alt="Nguyễn Anh Minh" className="h-full w-full object-cover" />
                    <AvatarFallback className="text-2xl bg-primary/5 text-primary">M</AvatarFallback>
                  </Avatar>
                </div>
                <CardTitle className="text-xl">Nguyễn Anh Minh</CardTitle>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 text-center text-sm text-muted-foreground border-t bg-zinc-50 dark:bg-zinc-900">
        © 2024 Environmental Law Lookup Project. All rights reserved.
      </footer>
    </div>
  )
}
