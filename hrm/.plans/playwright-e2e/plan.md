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

---

## Diễn biến thực tế (session pivot)

Feature khởi đầu là "Playwright cho HRM" nhưng trong quá trình làm đã **mở rộng thành chuẩn team + pilot ở nhatlinh**:

- ✅ **Chuẩn team**: tạo skill `playwright-setup` (Claude Code tự setup đúng chuẩn) đặt trong 4 project của `hrm-claude-config` (hrm, nhatlinh, erp, thanh_an) + guide người-đọc `websites/playwright-e2e-setup-guide.md`. Chốt: e2e/ riêng · Node 20 local · `@playwright/test` · storageState · POM · không webServer auto.
- ✅ **Pilot nhatlinh** (`nhatlinh/e2e/`): migrate script cũ (global playwright) → `@playwright/test` + POM (TypeScript). Chạy thật: **6 pass / 5 fail** — 5 fail KHÔNG do setup (3 API fail vì tồn kho E2E_PROD=0 → API chạy đúng; 2 UI kho fail do selector). Suite kho là WIP của user, không đụng.
- ⏳ **HRM e2e/ (Phase 0-1 gốc): CHƯA làm** — chưa dựng `HRM/e2e/`. Nếu cần, chạy skill `playwright-setup` để scaffold theo chuẩn, pilot module Human.

### Checkpoint — 2026-07-01
Vừa hoàn thành: Chuẩn team hoá Playwright (skill 4 project + guide) + pilot nhatlinh chạy được (6 pass). Xác minh setup nhatlinh OK bằng cách chạy suite thật.
Đang làm dở: Không có — đã chốt "setup Playwright OK". 5 test kho fail là WIP của user (data tồn kho + selector), không thuộc phần setup, không tự sửa.
Bước tiếp theo: (a) User tự commit/push skill lên hrm-claude-config (đã chọn tự làm git); (b) khi cần, scaffold `HRM/e2e/` bằng skill playwright-setup (pilot Human).
Blocked: (không)
