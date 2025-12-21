# Giải thích Cấu trúc Dự án Next.js & Shadcn UI

Tài liệu này giải thích chi tiết về cấu trúc thư mục và các tệp tin quan trọng trong dự án Next.js vừa được khởi tạo.

## 1. Cấu trúc Thư mục Chính

### `app/`
Đây là nơi chứa toàn bộ code của ứng dụng (App Router).
- **`layout.tsx`**: Layout chính của ứng dụng, chứa cấu hình font chữ (Geist), metadata (SEO), và thẻ `<body>`. Mọi trang (`page.tsx`) đều được render bên trong layout này.
- **`page.tsx`**: Trang chủ của ứng dụng (Home page). Đây là nơi chúng ta đã viết code demo cho Shadcn UI.
- **`globals.css`**: File CSS toàn cục. Chứa các biến CSS cho Shadcn UI (màu sắc, radius) và các directives của Tailwind CSS (`@theme`).

### `components/`
Thư mục chứa các React components.
- **`components/ui/`**: Chứa các component của Shadcn UI được cài đặt (ví dụ: `button.tsx`, `input.tsx`, `card.tsx`). Bạn có thể chỉnh sửa trực tiếp code của các component này nếu muốn tùy biến sâu hơn. Đây là điểm khác biệt của Shadcn so với các thư viện component khác (bạn sở hữu code).

### `lib/`
Chứa các tiện ích (utilities) dùng chung.
- **`lib/utils.ts`**: File này chứa hàm `cn` (classname). Hàm này giúp kết hợp các class của Tailwind một cách thông minh, xử lý xung đột class (sử dụng `clsx` và `tailwind-merge`). Rất quan trọng khi sử dụng Shadcn UI.

### `public/`
Chứa các file tĩnh (static files) như hình ảnh, fonts, icons.

### `node_modules/`
Thư mục chứa các thư viện đã cài đặt (do npm quản lý). Không nên chỉnh sửa file trong này.

## 2. Các File Cấu hình Quan trọng

### `components.json`
File cấu hình riêng của Shadcn UI. Nó quy định nơi lưu trữ components, utils, và các thiết lập về style (style "new-york", base color "neutral").

### `package.json`
File quản lý dự án npm.
- **scripts**: Các lệnh để chạy dự án (`npm run dev`, `npm run build`).
- **dependencies**: Danh sách các thư viện đang sử dụng (react, next, lucide-react, tailwindcss...).

### `next.config.ts`
File cấu hình cho Next.js server và build process.

### `tsconfig.json`
File cấu hình TypeScript, quy định các rule kiểm tra code và alias (ví dụ `@/*` trỏ về thư mục gốc).

### `postcss.config.mjs`
Cấu hình PostCSS, được Tailwind CSS sử dụng để xử lý CSS.

## 3. Cách thức hoạt động
1. **Next.js App Router**: Hệ thống routing dựa trên file system.
2. **Tailwind CSS**: Framework CSS ưu tiên tiện ích (utility-first), giúp style nhanh chóng ngay trong class HTML.
3. **Shadcn UI**: Cung cấp các component được xây dựng sẵn, đẹp mắt, dễ tiếp cận (accessible), và có thể tùy chỉnh dễ dàng. Code của component nằm ngay trong dự án của bạn (`components/ui`).

## 4. Ví dụ luồng hoạt động (Demo Page)
Trong `app/page.tsx`:
- Import các component từ `@/components/ui/...`.
- Sử dụng `<Card>` để tạo khung.
- Sử dụng `<Input>` và `<Button>` để tạo form.
- Class Tailwind (ví dụ `flex`, `min-h-screen`) được dùng để căn chỉnh bố cục trang.
