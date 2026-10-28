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

## Phase 4 — Fix Redmine #11816 (26/10/2026)
- [x] R1. Bộ lọc: thêm Kho, Mã hàng hóa, Tên hàng hóa, Công ty – Phòng ban (khuôn màn anh em #11814). Mã/Tên hàng: kế hoạch tổng không có
      bảng hàng → lọc theo hàng trong các Phiếu kiểm kê lập từ kế hoạch (`self_inventories.self_inventory_request_all_id` → `self_inventory_products`)
- [x] R2. Tiêu đề: bỏ chữ "Danh sách" → "Kế hoạch tổng kiểm kê hàng hóa" (tab trình duyệt + tiêu đề bảng)
- [x] R3. Bỏ sort cột Người tạo (FE + SORT_MAP BE)
- [x] R4. Nội dung yêu cầu dài: kẹp 2 dòng (`text-wrap clamp-2`) + hover xem đủ

### Checkpoint — 2026-10-26 (#11816)
Vừa hoàn thành: R1–R4. BE `SelfInventoryRequestAllService` (applyFilters + filterOptions warehouses/is_all_company, bỏ `creator` khỏi SORT_MAP),
Controller index trả `meta.is_all_company`. FE `index.vue` khuôn màn anh em (V2BaseCompanyDepartmentFilter slot #field-org, ô Kho/Mã/Tên hàng).
Kiểm: parse vue-template-compiler + babel OK; php -l OK; smoke HTTP kernel (transaction rollback) — mỗi ô lọc khớp 1 / lệch 0, sort creator bị bỏ qua.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm bộ lọc + cột Nội dung yêu cầu dài (CHƯA bấm thật). CHƯA commit.
Blocked:

## Phase 5 — Fix Redmine #11818 (26/10/2026) — theo skill form-validate
- [x] V1. Câu lỗi bỏ tên trường đứng trước, theo `locales/vi.json` ("Bắt buộc phải nhập", "Không hợp lệ", "Vui lòng nhập tối đa 255 ký tự.") — cả FE lẫn `messages()` BE
- [x] V2. Lưu nháp chỉ bắt Ngày kiểm kê từ/đến; Lưu và duyệt bắt đủ. `required` rẽ theo `isSending()` ở FormRequest, rule định dạng/nghiệp vụ luôn bật
- [x] V3. FE bỏ tự kiểm `required` (để BE trả 422 đủ ô cùng lúc), chỉ giữ kiểm định dạng (≤ 255 ký tự); 422 → toast câu chung

### Checkpoint — 2026-10-26 (#11818)
Vừa hoàn thành: V1–V3. `SelfInventoryRequestAllStoreRequest` thêm `isSending()` (status 1), câu lỗi theo vi.json; form FE `validateFormat()` thay
`validateAll()`, 422 → toast câu chung. Smoke HTTP kernel (rollback): nháp trống → 2 lỗi ngày; duyệt trống → 6 lỗi; ngày ngược / note 256 ký tự
bị chặn cả ở nháp; nháp chỉ có ngày → 200. DB không đổi.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm form Tạo/Sửa (CHƯA bấm thật). Đã commit + push `develop` (api 5dbe9650b, client 0df13b4ef).
Blocked:

## Phase 6 — Fix Redmine #11820 (26/10/2026)
- [x] E1. Xuất Excel danh sách: bỏ tô nền dòng tên cột (giữ in đậm + viền) — khuôn #11823 màn Phiếu kiểm kê

### Checkpoint — 2026-10-26 (#11820)
Vừa hoàn thành: E1 (`components/export-excel.js`, bỏ `cell.fill` dòng tiêu đề cột). Parse babel OK.
Đang làm dở: —
Bước tiếp theo: user bấm Xuất Excel kiểm file (CHƯA mở file thật). Đã commit + push `develop` (api 5dbe9650b, client 0df13b4ef).
Blocked:
