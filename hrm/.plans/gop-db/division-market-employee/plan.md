# Plan — Phiếu phân chia thị trường theo nhân viên (#11695)

> @junfoke · nhánh `task_11695` · design: `design.md` · spec: `docs/superpowers/specs/gop-db/2026-10-16-division-market-employee-design.md`

## Phase 0 — Chuẩn bị nhánh
- [x] Tạo `task_11695` từ `task_11694` (cả 2 repo)
- [x] Merge `origin/gop_db` vào `task_11694` — sửa 4 quyền #11694 sang `$this->perm`, `V2BaseSegmented` lấy bản gop_db
- [x] Merge `task_11694` vào `task_11695` (fast-forward)
- [x] Phân tích demo + code ERP, chốt 5 quyết định với user

## Phase 1 — BE
- [x] Migration thêm cột (`employee_id`, `division_part_id`, `business_area_id`) + index 5 bảng
- [x] Migration tách 14 phiếu cũ theo nhân viên
- [x] 5 entity + trạng thái / quyền / phạm vi xem / canX / mã phiếu
- [x] Service: danh sách + lọc + sort, phạm vi NV, options form, chi tiết cây, lưu (validate phạm vi, hãng, SL tối đa), gửi / thu hồi / duyệt / từ chối / hủy duyệt, xoá, lịch sử
- [x] Controller + request + list resource + route + blade in + export rows
- [x] 5 quyền seeder (`$this->perm`), `CatalogHistoryService` (bảng + nhãn `sent` / `recalled`), `ExportColumnRegistry`
- [x] Chặn Hủy duyệt / Xoá phiếu phòng ban khi còn phiếu NV Chờ duyệt / Đã duyệt
- [x] Test API (sau khi user cho chạy migrate + permission:sync)

## Phase 2 — FE
- [x] Danh sách (bộ lọc, cột, hành động theo trạng thái, xuất Excel)
- [x] Form Tạo / Sửa / Chi tiết (cây Tỉnh/TP → khu vực, popup chọn khu vực trong phạm vi, popup phường/xã chỉ xem, nhãn SL tối đa)
- [x] Popup Từ chối (lý do bắt buộc), Lịch sử, In
- [x] Menu "Theo nhân viên"
- [x] Verify Playwright

### Checkpoint — 2026-10-16
Vừa hoàn thành: BE + FE #11695. DB local đã migrate 2 file (--path), tách 14 phiếu cũ → 135 phiếu (mỗi phiếu 1 NV), permission:sync, gán 5 quyền mới cho role 18. Test API: lưu, chặn SL tối đa, hãng ngoài phạm vi, NV khác phòng, 423 khi chờ duyệt/đã duyệt, gửi/thu hồi/duyệt/từ chối/hủy duyệt, chặn hủy duyệt phiếu phòng ban, lọc/sort/xuất Excel/in/lịch sử. Playwright: danh sách, sửa + thêm khu vực + lưu, chi tiết, gửi duyệt, từ chối (lý do hiện ở form), tạo mới với NV chưa thuộc bộ phận.
Đang làm dở: —
Bước tiếp theo: user review UI; commit task_11695 (chưa commit); đưa skill sửa vào PR hrm-claude-config.
Blocked:
Ghi chú: dữ liệu test còn trong DB local — phiếu NV 140 (Đang tạo, NV 237), 141 (Đang tạo, đã từ chối 1 lần, NV 235).

## Phase 3 — E2E
- [x] Dựng bộ e2e `e2e/` (ngang hàng hrm-client; workspace chưa có) — Playwright 1.61 alpha (cùng bản MCP, dùng lại Chromium 1226), Node 24 nvm
- [x] `tests/division-market-employees.spec.ts` — 15 kịch bản + setup đăng nhập: 16/16 đạt (15 phút trên dev server `php -S` + Nuxt dev)

### Checkpoint — 2026-10-16 (e2e)
Vừa hoàn thành: e2e #11695 chạy xanh 16/16; test tự dọn phiếu NV phòng 50 trước/sau (đã xoá luôn phiếu test tay 140, 141).
Đang làm dở: —
Bước tiếp theo: user review; commit task_11695.
Blocked:
Lệnh chạy: `cd e2e && PATH="/c/Users/Legion/AppData/Local/nvm/v24.6.0:$PATH" E2E_BASE_URL=http://127.0.0.1:3005 E2E_API_URL=http://127.0.0.1:8002 npx playwright test`
