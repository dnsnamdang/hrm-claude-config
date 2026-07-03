# Design tóm tắt: Playwright E2E cho HRM

> Phụ trách: @dnsnamdang · Spec đầy đủ: `docs/superpowers/specs/2026-06-26-playwright-e2e-design.md`

## Mục tiêu
Tích hợp Playwright làm bộ kiểm thử E2E cho **hrm-client** (Nuxt 2/Vue 2):
1. Bộ E2E regression tự động (login + CRUD module).
2. Hỗ trợ Claude verify FE khi code (qua Playwright MCP, độc lập suite).

## Quyết định lớn
- **Vị trí**: thư mục `HRM/e2e/` **độc lập**, Node 18+ riêng (`.nvmrc`). Lý do: Playwright cần Node ≥18, app Nuxt chạy Node 14 → tách để không vỡ build (đây cũng là nguyên nhân các lần phải cài lại Playwright trước đây — lệch Node).
- **Ngôn ngữ**: TypeScript.
- **Auth**: `login.setup.ts` login UI 1 lần → lưu `storageState` (`.auth/user.json`), test tái dùng.
- **Pattern**: Page Object Model; selector ưu tiên `getByRole/getByText`, chỉ thêm `data-testid` vào Vue khi cần (hỏi trước).
- **Môi trường**: Local — FE `localhost:3000`, API `127.0.0.1:8000`, user tự chạy `npm run dev` (không dùng `webServer` auto).
- **Pilot Phase 1**: module Human — danh sách & CRUD nhân viên (`pages/human/employee`).

## Phase
- **P0 Bootstrap**: config + login smoke test (chứng minh chạy được).
- **P1 POM + Human**: khuôn mẫu CRUD nhân viên.
- **P2 Mở rộng**: module khác theo khuôn P1.
- **P3 CI** (tùy chọn sau).

## Không làm (YAGNI)
CI ngay, test ERP, visual regression, test API trực tiếp.
