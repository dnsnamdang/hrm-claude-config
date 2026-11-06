# Plan — Danh sách loại phiếu hạch toán (@khoipv)

## Phase 1 — Port màn danh sách

### BE
- [x] Entity `Modules/Finance/Entities/ListBillAccounting.php` (`$table`, hằng `TYPES` chép ERP)
- [x] Service `ListBillAccountingService::index()` — keyword (name), type, sort name/type, mặc định id asc như ERP
- [x] Resource `ListBillAccountingResource` (type_name, accounting_text)
- [x] Controller `ListBillAccountingController` index / types / export (DynamicExport)
- [x] Route `v1/finance/list-bill-accountings` (không middleware quyền)
- [x] `ExportColumnRegistry` khoá `list_bill_accountings`
- [x] Smoke test API

### FE
- [x] `pages/admin/list-bill-accountings/index.vue` (khuôn `pages/finance/currencies/index.vue`)
- [x] Menu `components/subsystem-menu/admin.js` — nhóm dưới "Danh mục mẫu in"
- [x] Compile check

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE (entity/service/resource/controller/route/export) + FE (index.vue + menu admin.js). Smoke test API 5/5 = 200 (list, lọc type+keyword, sort type_name desc, types, export 82KB). Compile FE pass, grep checklist sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm /admin/list-bill-accountings (menu Quản trị hệ thống, dưới Danh mục mẫu in).
Blocked:

## Fix — Cột "Hạch toán riêng" hiện số 0 (15/10, user báo)
- [x] Nguyên nhân: slot `cell-accounting` chỉ có 1 thẻ `<i v-if>` → dòng accounting=0 slot rỗng, V2BaseDataTable rơi về nội dung mặc định in `0`
- [x] Bọc `<span class="field-line">` luôn render; verify render SSR cũ ra `0` / mới ra ô trống, compile sạch
- [ ] User F5 kiểm trên trình duyệt

## Fix — Xuất Excel: logo to hơn bảng (15/10, user báo)
- [x] Nguyên nhân: xuất qua `DynamicExport` (blade chèn logo cỡ gốc) — bảng 4 cột hẹp hơn ảnh
- [x] Chuyển sang khuôn chung `utils/export/listExportFile.js` (logo trải bằng bề rộng bảng): BE `GET /export-rows` (`ListBillAccountingService::exportRows()`), bỏ `/export` + mục `ExportColumnRegistry[list_bill_accountings]`; FE `runExport` → `exportListFile`
- [x] Verify: php -l, smoke test export-rows (lọc type / theo fields / phân trang), compile FE
- [ ] User xuất thử trên trình duyệt xem logo

## Fix — Xuất Excel: bỏ nút lọc ở hàng tiêu đề (15/10, user yêu cầu)
- [x] Hàm chung `listExportFile.js`: thêm tuỳ chọn `autoFilter` (mặc định true → màn khác không đổi)
- [x] Màn này truyền `autoFilter: false`; verify dựng file thật: mặc định có `<autoFilter>`, false thì không
- [ ] User xuất thử trên trình duyệt


## Dời menu sang Bán hàng (15/10)
- [x] Gỡ mục khỏi `components/subsystem-menu/admin.js`, thêm vào `sale-hub.js` › Quy chế - Thiết lập › Thiết lập (route giữ `/admin/...`)
- [ ] User mở trình duyệt kiểm sidebar Bán hàng

## Tài liệu SRS / HDSD / Testcase (06/11/2026) @khoipv
- [x] Đọc code màn (FE `pages/admin/list-bill-accountings/index.vue` — file duy nhất; BE `Modules/Finance` ListBillAccounting*): màn CHỈ XEM — không Thêm / Sửa / Xóa / Khóa / Lịch sử / Xem chi tiết / Import; bộ lọc gọn 2 ô (không có Tìm kiếm nâng cao / Cài đặt bộ lọc); không gắn quyền, không giới hạn phạm vi
- [x] Grep màn đọc ngược (hrm-api, hrm-client, ERP, cột `*bill_accounting*` trong DB gộp): không màn HRM nào đọc; chỉ màn gốc ERP đọc cùng bảng → Phần 5 1 dòng "Hệ thống ERP"
- [x] Chụp ảnh dev-hrm (`dslpht_shots/_capture/capture.js`, chặn mọi yêu cầu ghi — 0 yêu cầu ghi): 8 ảnh màn + 16 icon, dữ liệu thật 105 loại phiếu, không giả dữ liệu
- [x] `gen_srs.py` → `SRS - Danh sách loại phiếu hạch toán.docx`: 4 chức năng (Xem DS, Tìm kiếm và lọc, Tùy chỉnh cột, Xuất Excel — UC), BR-01..09, Phần 5 bảng 4 cột, Mục lục trang riêng căn giữa; selfcheck khớp mẫu; metrics ui=12.8 ev=4.8 evch=1003 intro=1767
- [x] `gen_hdsd.py` → `HDSD_Danh sach loai phieu hach toan.docx`: 9 trang, 4 phần (Truy cập và tìm kiếm, Sắp xếp và phân trang, Xuất Excel, Tùy chỉnh cột)
- [x] `gen_testcase.py` → `testcase.xlsx` (loai danh_muc): 84 TC, 6 nhóm, P0 41.7%, check_tc 0 lỗi
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx`: Testcase 89 có TC / 235 N/A; SRS 79 có mục / 84 N/A

### Checkpoint — 2026-11-06
Vừa hoàn thành: bộ tài liệu SRS + HDSD + Testcase + Đối chiếu checklist màn Danh sách loại phiếu hạch toán (chuẩn 04/11)
Đang làm dở: —
Bước tiếp theo: user mở 4 file kiểm tra, quyết định đẩy Drive
Blocked:
