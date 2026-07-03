# Plan: Playwright E2E cho HRM

> Spec: `docs/superpowers/specs/2026-06-26-playwright-e2e-design.md`
> Design: `.plans/playwright-e2e/design.md`
> **Plan chi tiết (task-by-task, có code):** `docs/superpowers/plans/2026-06-26-playwright-e2e.md`
>
> Khung phase tổng quan bên dưới — chi tiết từng task ở file plan trên.

## Phase 0 — Bootstrap
- [ ] Tạo cấu trúc `HRM/e2e/` + `.nvmrc` (Node 18)
- [ ] `package.json` + cài `@playwright/test`, `dotenv`, `playwright install chromium`
- [ ] `playwright.config.ts` (projects setup + chromium storageState)
- [ ] `tsconfig.json`, `.env.sample`, `.gitignore`
- [ ] `auth/login.setup.ts` (login UI → storageState)
- [ ] `tests/smoke/login.spec.ts`
- [ ] Chạy `npx playwright test` xanh + mở report

## Phase 1 — POM nền + module Human (pilot)
- [ ] `pages/BasePage.ts`, `pages/LoginPage.ts`, `pages/EmployeePage.ts`
- [ ] `tests/human/employee.spec.ts`: danh sách / tìm kiếm / tạo / sửa / (xóa)
- [ ] Chốt chiến lược dữ liệu test (hậu tố ngẫu nhiên + cleanup)

## Phase 2 — Mở rộng (sau)
- [ ] Module tiếp theo theo khuôn P1

## Phase 3 — CI (tùy chọn, sau)
- [ ] GitHub Actions chạy playwright test

## Tài liệu
- [ ] `e2e/README.md` — hướng dẫn sử dụng dev (cài Node 18, chạy, viết test, debug, report)
