# Plan — quotation-print-template-fix

Người phụ trách: @manhcuong

## Phase 1 — Hiệu chỉnh mẫu in báo giá (FE only)

### FE
- [x] Bỏ cột "Thành tiền nhập" + tổng tiền nhập khỏi bảng tổng hợp trong QuotationPrintPreview.vue
- [x] Fix "Hiệu lực báo giá" rỗng: đổi `item.validity_days` → `'Đến ngày ' + formatDate(item.validity_date)` (DB đã rename cột 2026-05-28)
- [x] "Đại diện kinh doanh/ Email" hiển thị "[Họ tên] / [Email]" (bỏ mã NV) — map fullname từ list_employee_infos + email từ store.employees, thêm prop salesEmployeeEmail; chữ ký cuối trang chỉ hiện họ tên
- [x] Fix "Thông số kỹ thuật" dính liền: stripHtml giữ xuống dòng (<br>, đóng thẻ block → \n) + class cell-spec white-space: pre-line (cả preview + CSS cửa sổ in)
- [x] Áp dụng tên/email ở cả 2 màn gọi print: pages/assign/quotations/index.vue + _id/index.vue

### Verify (Playwright headless, BG-2026-00001, local FE:3000/BE:8000)
- [x] AC1: bảng tổng hợp không còn cột "Thành tiền nhập" (cả 2 luồng in: danh sách + chi tiết)
- [x] AC2: "Hiệu lực báo giá: Đến ngày 03/08/2026" (validity_date DB = 2026-08-03)
- [x] AC3: "DNS Admin / namdangit@gmail.com" (trước fix: "HN_QTTT - DNS Admin", không email); chữ ký cuối trang = "DNS Admin"
- [x] AC4: thông số kỹ thuật xuống dòng theo <br>/block gốc, computed white-space = pre-line

- [x] (Bổ sung) Chữ ký "ĐẠI DIỆN KINH DOANH": tên căn giữa theo cụm thay vì lệch phải — .print-signature flex justify-end + .signature-inner text-center (cả preview + CSS cửa sổ in). Verify Playwright: 3 dòng cùng tâm.

### Checkpoint — 2026-07-04
Vừa hoàn thành: toàn bộ Phase 1 + verify Playwright 2 luồng in (danh sách + chi tiết) PASS 4/4 AC + fix căn giữa chữ ký.
Đang làm dở: (không)
Bước tiếp theo: user verify bằng mắt trên browser + in thử PDF thật.
Blocked: (không)

## Phase 2 — Fix ô "Đơn vị tính" rỗng cho hàng ERP khi in

Nguyên nhân: ERP search API trả `unit_name` nhưng `unit_id=null` cho sản phẩm cha; HRM chỉ lưu `unit_id` và resolve tên qua relation `tpUnit` → null → ô đơn vị rỗng. Sản phẩm ERP có đơn vị base trong `dev_erp.product_units` (is_base=1) nên tra ngược được `unit_id`.

### BE
- [x] Thêm `TpProductUnitPrice::getBaseUnitIds(array $erpIds): array` (mirror getCostPrices, trả [product_id => unit_id] where is_base=1)
- [x] Enrich `unit_id` trong `ErpProductSearchService::search()`: sản phẩm nào `unit_id=null` + có `erp_product_id` → tra base unit từ ERP, gán vào unit_id
- [x] Seeder `BackfillQuotationProductUnitIdSeeder`: set unit_id where NULL + erp_product_id NOT NULL
- [x] FIX seeder cho production: DB chính và ERP ở HOST KHÁC NHAU (hrm_production@192.168.122.103 vs erp_new@erp.eteksofts.com:33061) → bỏ JOIN chéo, tra base unit qua connection mysql2 (TpProductUnitPrice::getBaseUnitIds) rồi update DB chính theo id. Verify local: reset dòng 284→null, chạy seeder→điền lại unit_id=39

### Verify
- [x] Search hàng ERP (COGI-ERCOHC4502) trả unit_id=39 (trước fix: null), unit_name='Bộ'
- [x] Chạy seeder: 144 dòng cập nhật; BG-2026-00008/00010 các dòng cha có unit_id (39=Bộ, 75=Xô 18L, 40=Cái)
- [x] DetailQuotationResource(quotation 10) trả unit_name='Bộ'/'Xô 18L' cho dòng cha ERP
- [x] UI (Playwright headed, BG-2026-00010): popup Xem trước — dòng cha ERP hiện Đơn vị tính = "Bộ", "Xô 18L"

### Checkpoint — 2026-07-09
Vừa hoàn thành: fix ô Đơn vị tính rỗng cho hàng ERP — enrich unit_id ở ErpProductSearchService + seeder backfill (144 dòng). Verify: search trả unit_id, resource trả unit_name.
Đang làm dở: (không)
Bước tiếp theo: user mở lại popup In trên browser xác nhận bằng mắt.
Blocked: 1 dòng ERP mồ côi (erp_product_id=47928 không có trong dev_erp.products) không tra được base unit — chấp nhận rỗng.

## Phase 3 — Fix cột Model/Thương hiệu/Xuất xứ rỗng khi TẠO báo giá từ BOM

Nguyên nhân: `loadBomProducts()` (edit.vue) map sản phẩm từ BOM chỉ set `model_id/brand_id/origin_id` + `unit_name`, THIẾU `model_name/brand_name/origin_name`. Bảng chi tiết bind `parent.model_name`... → hiện "—". (Báo giá đã lưu không lỗi vì DetailQuotationResource resolve tên qua relation.)

### FE
- [x] edit.vue `loadBomProducts().mapProduct`: thêm `model_name/brand_name/origin_name` từ `p` (BOM detail resource đã trả sẵn)

### Verify
- [x] DetailBomListResource(bom 3) trả model_name='GC-4.0PROA', brand_name='KOISU', origin_name='China'
- [x] UI (Playwright headed, create?project_id=19 → BOM-2026-00003): bảng chi tiết hiện Model/Thương hiệu/Xuất xứ đúng (GC-4.0PROA/KOISU/China, ST-IW1640/SUMAKE/Taiwan, con 22-DPM/DAISEN/Japan)

### Checkpoint — 2026-07-09 (Phase 3)
Vừa hoàn thành: fix FE loadBomProducts bổ sung 3 field name. Nuxt hot-reload, không cần restart.
Bước tiếp theo: user tạo báo giá từ BOM xác nhận bằng mắt.
Blocked: (không)
