# Thiết kế: Port màn "Tổng hợp giá vận chuyển đề xuất" (ERP → HRM)

> Tài liệu thiết kế cho builder. Ngôn ngữ làm việc: tiếng Việt. Bước sau: `superpowers:writing-plans`.

## 1. Mục đích & bối cảnh (why)

Màn **"Tổng hợp giá vận chuyển đề xuất"** (ERP: model `DeliveryCostSummary`, mã **THGVC-**,
controller `app/Http/Controllers/Common/DeliveryCostSummaryController.php` 16 action) là **bước
SINH ra "Bảng giá hiệu lực vận chuyển" (BGHLVC)**. Khi port BGHLVC sang HRM (đã xong, chỉ-đọc +
gia hạn) ta cố ý gác phần sinh này lại — giờ port nốt để đóng trọn luồng.

Luồng nghiệp vụ ERP (4 màn liên tiếp):

```
Báo giá vận chuyển (DeliveryQuotation, BGVC-)   ← ĐÃ CÓ trong HRM (CRUD đầy đủ)
        │  (nút "Tổng hợp" ở chi tiết)
        ▼
Tổng hợp giá VC đề xuất (DeliveryCostSummary, THGVC-)   ← MÀN NÀY, chưa có trong HRM
        │  import báo giá nhiều NCC → đề xuất giá = MIN → gửi → DUYỆT
        ▼
Bảng giá hiệu lực VC (PriceListValidDelivery, BGHLVC)   ← ĐÃ CÓ (đọc); cần BỔ SUNG phần GHI
        │  (mỗi báo giá NCC đã duyệt → "Lập hợp đồng vận chuyển")
        ▼
Hợp đồng vận chuyển (deliveryContract)   ← CHƯA port → nút hiện "Tính năng chưa phát triển"
```

## 2. Scope

### Goals (làm trọn — "tất cả những gì ERP xử lý trong màn này")
- **Danh sách** THGVC: lọc (code, trạng thái, người tạo, người duyệt, NCC, công ty), phân trang,
  cột Hành động bám chi tiết.
- **Tạo** THGVC từ một **Báo giá vận chuyển** nguồn (vào qua `?delivery_quotation_id=...`): kế thừa
  nguyên khung **tuyến × loại xe × trọng tải** + km + công ty + hiệu lực từ/đến từ báo giá gốc.
  Người dùng nhập **Ghi chú** + **file đính kèm PDF**.
- **Import báo giá của từng NCC** bằng Excel (mỗi NCC một file, khớp đúng thứ tự xe → trọng tải →
  tuyến của báo giá gốc; đọc `extra_price` + `cost` từng ô). Mỗi NCC thành một **tab** trong ma trận.
- **Đề xuất giá tự động = GIÁ NHỎ NHẤT (khác 0)** trong tất cả báo giá NCC cho từng ô (giá cước vượt
  trội + cost từng tuyến×trọng tải). Prefill vào giá duyệt.
- **Sửa tay** trong modal: giá cước vượt trội (`updateExtraPrice`) và cost theo tuyến
  (`updatePayLoadRoads`).
- **Workflow trạng thái**: Đang tạo (3) → Chờ duyệt (2) → Đã duyệt (1). *(Đang lập HĐ (5) / Đã lập
  HĐ (4) giữ hằng số + nhãn để hiển thị, nhưng HRM chưa chuyển sang được vì màn Hợp đồng VC chưa
  port.)*
- **Lưu nháp / Gửi duyệt / Duyệt / Không duyệt** (kèm comment người duyệt). Chỉ sửa/xóa khi Đang
  tạo và là người tạo.
- **Khi DUYỆT (status=1) → SINH/CẬP NHẬT BGHLVC**: nếu báo giá nguồn đã gắn `price_list_valid_id`
  → `update` bảng giá hiệu lực hiện có (merge xe/trọng tải/tuyến); chưa gắn → **check trùng khoảng
  thời gian theo công ty người duyệt** rồi `create` mới. Cost/extra_price ghi theo **giá duyệt**
  (`approve_cost` / `approve_extra_price`) gửi lên lúc duyệt. Sau đó copy từng NCC + file đính kèm
  sang `PriceListValidDeliveryQuotation`.
- **Xuất Excel** bản tổng hợp (ma trận, có letterhead công ty).
- **Thông báo** (notification) khi gửi duyệt / duyệt / không duyệt — theo chuẩn HRM.
- **Đính kèm / xóa file**.
- **Quyền** mới (guard `api`) khai qua seeder đồng bộ.
- **Bổ sung phần GHI cho `PriceListValidDeliveryService`** trong HRM (hiện chỉ có đọc) —
  `create()` / `update()` port từ ERP `app/Services/PriceListValidDelivery/PriceListValidDeliveryService.php`.
- **Điểm vào**: thêm hành động **"Tổng hợp"** ở màn chi tiết Báo giá vận chuyển (đã có trong HRM),
  điều kiện giống ERP (`canSummaryCost()` → báo giá ở trạng thái cho phép).

### Non-goals (ngoài màn này)
- **Port màn Hợp đồng vận chuyển** (`deliveryContract`). Nút **"Lập hợp đồng vận chuyển"** ở báo giá
  NCC đã duyệt vẫn **hiển thị** nhưng bấm vào báo **"Tính năng chưa phát triển"** (chốt với user:
  khi nào port màn HĐ VC thì ghép vào). Không dựng route cụt.
- Thay đổi màn Báo giá vận chuyển ngoài việc thêm hành động "Tổng hợp".
- Thay đổi màn BGHLVC ngoài việc thêm phần GHI vào service.

### Anti-goals (coi là thất bại dù chạy được)
- Duyệt nhưng **không** sinh/cập nhật đúng BGHLVC, hoặc sinh sai cost (lấy nhầm giá NCC thay vì giá
  duyệt), hoặc tạo trùng bảng giá cùng khoảng thời gian/công ty.
- Import Excel NCC lệch khung (đọc nhầm ô vì không khớp thứ tự xe/trọng tải/tuyến của báo giá gốc)
  mà vẫn lưu.
- Ma trận dồn cột khi dữ liệu không đều (phải căn theo khung gốc, ô thiếu để trống — bài học BGHLVC).
- Đề xuất "min" tính cả số 0 (phải bỏ 0; nếu mọi NCC = 0 thì 0).
- Quyền fail-open: lộ THGVC công ty khác / cho duyệt khi không có quyền.

## 3. Ràng buộc (constraints)

- **Phụ thuộc đã sẵn trong HRM**: `DeliveryQuotation` (Transport module, CRUD đầy đủ, có trang chi
  tiết `pages/transport/delivery-quotations/_id`), 5 entity `PriceListValidDelivery*`
  (`Modules/Finance/Entities/Delivery/`), danh mục `VehicleCategory` / `VehiclePayload` / `Road` /
  `Province` (MasterData/Human), bảng `files`, `customers` (Supplier).
- **Phụ thuộc CHƯA có**: 5 bảng `delivery_cost_summary*` (ERP có migration 2021_04; DB gộp
  `erp_hrm_check` — kiểm tra bảng đã tồn tại chưa, nếu có thì GHI THẲNG, thiếu cột thì thêm; theo
  quy ước gộp DB không tạo bảng mới trùng). Phần GHI của `PriceListValidDeliveryService`.
- **Quy ước HRM bắt buộc** (CLAUDE.md + skills):
  - Quyền mới guard `api`, khai qua **`permission-seeder`** (không migration/SQL tay), **không**
    dùng lại quyền ERP guard `web`. BE re-check endpoint nhạy cảm bằng
    `isCurrentEmployeeHasPermission('<Tên quyền>')`, cờ FE init `false` (fail-closed).
  - FE màn mới chỉ dùng **V2Base\***; Select trong modal → `V2BaseSelectInModal`; nút ẩn (v-if)
    khi không dùng được; bảng tràn bọc `V2BaseTableScroll`; `.text-muted` đỏ → dùng `#6b7280`.
  - Số **quốc tế** `1,234,567.89` (FE `toLocaleString('en-US')`, CẤM `'vi-VN'`; BE `number_format`
    mặc định). Ngày `dd/mm/yyyy`.
  - Model `extends Model` → set tay `created_by`/`updated_by = auth()->id()` khi ghi;
    `auth()->id()` = `employees.id`.
  - Bản ghi bị khóa chặn ở BE (423). FormRequest chỉ `rules()`, không `messages()` cho rule chung.
  - **Import Excel** theo skill `import-excel`; **Export Excel** theo skill `export-excel` (ô số = số
    thô + `data-format`, letterhead qua `WithDrawings`/trait). **Thông báo** theo
    `notification-convention`.
  - Hành động xong → quay về màn danh sách; tiêu đề chi tiết `Chi tiết <đối tượng>: <mã>`; hành động
    ở màn chi tiết KHỚP màn danh sách.
- **Kỹ thuật**: hrm-api Laravel 8 / PHP 7.4 / `nwidart/laravel-modules` / guard `api` / spatie
  permission. hrm-client Nuxt 2.14 / Vue 2 / Node 14 / Bootstrap-Vue / vee-validate v2.
- **Git**: làm trên `develop` (họ gop_db). AI **không** commit/push trừ khi user yêu cầu trực tiếp.
  hrm-api giữ local.

## 4. Các quyết định "how" đã chốt (của tôi, trừ khi ghi là của user)

1. **Module & vị trí**: đặt trong `Modules/Transport` (bám BGHLVC + DeliveryQuotation). Entities 5
   bảng THGVC → `Modules/Transport/Entities/DeliveryCostSummary/` (bám pattern
   `Entities/DeliveryQuotation`). Controller `V1/DeliveryCostSummary`, Service
   `Services/DeliveryCostSummary`, Transformers, Requests, Exports, ExcelImports tương ứng.
2. **Phần GHI BGHLVC**: port `create()` / `update()` của ERP
   `PriceListValidDeliveryService` vào **chính service đọc hiện có** của HRM
   (`Modules/Transport/Services/PriceListValidDelivery/PriceListValidDeliveryService.php`) — giữ 1
   service như ERP. Entity `PriceListValidDelivery*` chuyển từ chỉ-đọc sang có ghi: set tay
   `created_by`/`updated_by`.
3. **Điểm vào "Tổng hợp"**: thêm action ở chi tiết Báo giá VC (HRM), điều kiện bám `canSummaryCost()`
   của ERP. (Cần kiểm trạng thái báo giá HRM đã có cờ tương ứng chưa — mục Builder.)
4. **Đề xuất min**: tính ở **client (Vue computed)** bám `getMinCost()`/`getMinExtraPrice()` của ERP
   (gom giá cùng ô mọi NCC, bỏ 0, lấy `Math.min`). Prefill `approve_*`; người duyệt sửa đè ở màn
   duyệt; giá duyệt gửi lên BE khi `approve(status=1)`.
5. **Ma trận & khung xe/trọng tải**: khung (loại xe × trọng tải × tuyến) **KHÔNG dựng lúc `store`** —
   bám đúng ERP: `store` chỉ lưu `delivery_quotation_id` + ghi chú + file + trạng thái; khung
   xe/trọng tải/tuyến của từng NCC **dựng lúc IMPORT** (`quotationImport`) theo đúng khung báo giá
   gốc. Ma trận hiển thị căn ô theo **khung HEADER gốc** (vehicles.id → payloads.id → roads), ô
   thiếu để trống, không dồn cột (bài học RF#1 của BGHLVC). Mỗi NCC một tab; dòng "Giá cước vượt
   trội" + các dòng tuyến.
6. **Import Excel NCC**: port `QuotationImport` (validate thứ tự xe dòng 8 / trọng tải dòng 9 /
   extra dòng 10 / tuyến từ dòng 11, khớp báo giá gốc) theo skill `import-excel`. Lệch khung → báo
   lỗi, không lưu.
7. **Quyền** (guard `api`, seeder), bám bộ ERP:
   - `Duyệt giá vận chuyển` (duyệt) — dùng trong `canApprove()` + gate route approve.
   - `Xem tổng hợp giá vận chuyển đề xuất theo tổng công ty` / `... theo công ty` / `... theo phòng
     ban` (lọc phạm vi danh sách + `canView()`).
   - Sửa/Xóa/Lập HĐ: không quyền riêng, check `created_by == auth()->id()` + trạng thái (như ERP).
   - `type` = phân hệ Vận chuyển (BGHLVC dùng 22). Menu `isShow` = có một trong 3 quyền "Xem...".
8. **Workflow & notification**: trạng thái + nút bám ERP; thông báo gửi/duyệt/không-duyệt theo
   `notification-convention` (thay cơ chế Redis của ERP).
9. **Export Excel**: port `DeliveryCostSummaryExcel` theo skill `export-excel`. **Không có bản in**
   riêng (ERP màn này chỉ Export Excel, không print).
10. **Nút "Lập hợp đồng vận chuyển"**: hiển thị ở báo giá NCC đã duyệt, bấm → toast/thông báo
    **"Tính năng chưa phát triển"** (quyết định của **user**).
11. **Sinh BGHLVC khi duyệt**: bám đúng nhánh ERP `approve()` — có `price_list_valid_id` → `update`;
    chưa có → check overlap `date_valid_from/to` theo `company_id` người duyệt → `create`; rồi copy
    NCC + file sang `PriceListValidDeliveryQuotation`. Toàn bộ trong 1 transaction.
12. **File đính kèm CẤP PHIẾU THGVC**: dùng **bảng `files` chung** (`table`/`table_id`) + component
    `V2BaseFile`, **KHÔNG** bê cột `delivery_cost_summaries.attachments` (chuỗi CSV qua `CmcS3Helper`)
    của ERP. Lý do: đây là màn HRM mới, quy ước HRM + entity anh em (`PriceListValidDeliveryQuotation`)
    đều dùng bảng `files`; cột CSV đúng kiểu HRM đã thay thế. `deleteFile` thao tác trên bảng `files`.
    *(File cấp NCC thì ERP vốn đã dùng bảng `files` → giữ nguyên, bước duyệt copy sang
    `PriceListValidDeliveryQuotation`.)*
13. **File mẫu import NCC**: **KHÔNG** thêm action "tải mẫu" riêng (ERP không có, và `QuotationImport`
    đọc ma trận theo vị trí cố định khớp khung báo giá gốc — không phải khuôn 1-hàng-tiêu-đề của skill
    `import-excel` nên `buildImportTemplate()` không dùng được). **Bản xuất Excel tổng hợp chính là
    khung để NCC điền** (đúng thứ tự xe/trọng tải/tuyến). Import lệch khung → báo lỗi, không lưu.

## 5. Dữ liệu (5 bảng THGVC)

```
delivery_cost_summaries
  └─ delivery_cost_summary_quotations                 (1 dòng / NCC: supplier_id, file đính kèm)
       └─ delivery_cost_summary_quotation_vehicles
            └─ ..._quotation_vehicle_payloads          (extra_price theo NCC)
                 └─ ..._quotation_vehicle_payload_roads (cost theo NCC × tuyến)
```
Khung gốc (vehicles/payloads/roads) copy từ `DeliveryQuotation` khi tạo. Báo giá gốc giữ
`price_list_valid_id` (nếu đã gắn với một BGHLVC) → quyết định create vs update khi duyệt.

## 6. Để lại cho builder (plan sẽ chốt)
- Chữ ký chính xác các action controller, Service, Resource, FormRequest, route (static trước
  `/{id}`).
- Nơi lưu `approve_cost`/`approve_extra_price` (persist trên detail THGVC hay chỉ gửi lúc duyệt) —
  bám ERP `approve()` + `PriceListValidDeliveryService::create/update`.
- Chi tiết UI ma trận + 2 modal sửa giá dựng bằng V2Base.
- Xác nhận 5 bảng `delivery_cost_summary*` đã có trong DB gộp hay cần thêm (kiểm bằng
  `information_schema`).

> **Đã chốt qua builder-check (không còn mở):** nhánh create-vs-update BGHLVC là CÓ THẬT (HRM BGVC
> đã set/đọc `price_list_valid_id` đầy đủ) · cờ gate nút "Tổng hợp" ĐÃ CÓ
> (`DeliveryQuotation::canSummaryCost()` trong HRM, `status==1 || created_by==me`).

## 7. Quyết định đã chốt với user
- **Phạm vi công ty khi DUYỆT = Hướng A (bám ERP)** — user chốt 2026-10-28. `canApprove()` chỉ
  kiểm quyền `Duyệt giá vận chuyển` + trạng thái = Chờ duyệt, **KHÔNG** chặn công ty. BGHLVC sinh
  ra vẫn đóng dấu + check overlap theo công ty người duyệt (bám ERP 1:1). Khớp các lần chốt trước
  của user: xem/duyệt theo quyền, không chặn chéo công ty.
```
