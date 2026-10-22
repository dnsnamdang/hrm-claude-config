# Kế hoạch tổng kiểm kê hàng hóa — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-20-ke-hoach-tong-kiem-ke-hang-hoa-design.md`

## Phase 0 — Khảo sát
- [x] Khảo sát nghiệp vụ màn ERP `self_inventory_request_alls`
- [x] Chốt 20/10: Nội dung yêu cầu + Thành phần tham gia bắt buộc thật; dùng lại 3 quyền màn anh em; bỏ ô lọc chết; giữ điều kiện Lập phiếu ERP

## Phase 1 — BE
- [x] B1. Entity `SelfInventoryRequestAll` (mở rộng model chỉ-đọc: STATUSES, scopedQuery, cờ, generateCode, DETAIL_PATH)
- [x] B2. `SelfInventoryRequestAllService` (list/filter/sort/export-rows/filter-options/detail/form-options)
- [x] B3. `SelfInventoryRequestAllWriteService` (store/update/destroy, thông báo, lịch sử) + đăng ký `CatalogHistoryService::GATED_TABLES`
- [x] B4. FormRequest + Controller + 12 route `finance/self-inventory-request-alls`
- [x] B5. In (290/289 + letterhead theo công ty phiếu, ký sát phải)
- [x] B6. Màn Phiếu kiểm kê: link kế hoạch tổng ERP → HRM (`SelfInventoryService` planInfo / planRows / planData)
- [x] B7. Smoke test HTTP kernel (rollback) — Super admin 20/20, NV thường 20/20, phạm vi xem đúng; DB sạch (catalog_histories max 1244 như trước)

## Phase 2 — FE (`pages/finance/self-inventory-request-alls`)
- [x] F1. Danh sách index.vue (khuôn màn anh em; khoá `finance_self_inventory_request_alls`)
- [x] F2. Form dùng chung (ngày từ–đến, kho nhiều → công ty thuê kho tự chọn, phòng ban, validate inline, unsaved, Lưu và tiếp tục)
- [x] F3. create / _id/edit / _id/index (+ SystemInfoSection, 404)
- [x] F4. Menu `finance.js` erpPath → link
- [x] F5. Checklist skill (grep sạch) + parse vue-template-compiler/babel OK

### Checkpoint — 2026-10-20 (BE + FE)
Vừa hoàn thành: B1–B7 + F1–F5. Bám màn anh em `self-inventory-requests` ở: bộ lọc floating, toolbar, Cấu hình cột, Xuất Excel ExcelJS,
In danh sách, popup Lịch sử, khối V2BaseFormSection, footer V2Footer #custom-actions, Lưu và tiếp tục, row-actions dùng chung list/detail.
Đang làm dở: —
Bước tiếp theo: mở trình duyệt kiểm (CHƯA bấm thật — nuxt dev local không chạy lúc làm): danh sách + lọc, Tạo (validate đỏ cùng lúc, chọn kho → công ty
thuê kho tự chọn, lịch chặn ngày đến < ngày từ), Sửa, Chi tiết, Xóa, In, Xuất Excel, Lịch sử, nút Lập phiếu → màn Phiếu kiểm kê nạp đúng kế hoạch.
Không cần `permission:sync` (dùng 3 quyền đã có của màn anh em). CHƯA commit.
Blocked:

## Phase 3 — Kiểm chứng Playwright (user yêu cầu 20/10, localhost, DNS Admin)
- [x] V1. Danh sách: nạp, cột đủ, 1 request/lần, lọc Trạng thái (`status=3` → rỗng), Làm mới, In danh sách (mẫu 289), Xuất Excel (popup 9/9 trường → tải file)
- [x] V2. Tạo: bấm Lưu nháp khi trống → 6 ô báo lỗi cùng lúc + QLDA_001; lịch "đến" khoá ngày < "từ"; chọn 2 kho → Công ty thuê kho tự chọn 5 công ty (gộp trùng, khớp DB); Lưu nháp → DB đủ 4 bảng + log
- [x] V3. Sửa: nạp lại đủ (select2 không ghi đè công ty khi mở), bỏ 1 công ty + sửa nội dung → Lưu và duyệt → log "Thay đổi thông tin" + "Thay đổi trạng thái", có thông báo chuông
- [x] V4. Chi tiết: ẩn Sửa/Xóa, có Lập phiếu + In; In (mẫu 290 + letterhead, ký sát phải); khối Lịch sử 3 mốc; Lập phiếu → màn Phiếu kiểm kê nạp đúng kế hoạch (mã, kho, công ty thuê, ghi chú), link kế hoạch = HRM
- [x] V5. Xóa phiếu nháp từ danh sách: popup xác nhận → xoá hẳn + log delete; URL id lạ → trang 404, không toast
- [x] Dọn dữ liệu test theo id: phiếu 8 (+ bảng con), log 1255–1259, 7 thông báo; phiếu 9 đã xoá qua UI. DB về như trước (notifications 3125)
- [ ] ⚠️ Phát hiện (component dùng chung, CHƯA sửa — chờ user): `V2BaseSelect` chọn NHIỀU không bao giờ hiện viền đỏ khi lỗi — rule viền `div.v2-select .select2-container:not(--disabled) .select2-selection--multiple { border … !important }` nặng hơn `.v2-select.is-invalid .select2-selection` (scoped). Dính cả màn Kế hoạch kiểm kê theo hàng hóa + mọi select multiple.
