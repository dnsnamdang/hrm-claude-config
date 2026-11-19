# QA UI màn "DM mẫu báo giá vận chuyển" (BGVC) — Design

Màn `DeliveryQuotation` (prefix `BGVC-`), port từ ERP `/admin/delivery_quotations`.
FE: `hrm-client/pages/transport/delivery-quotations/`. BE: `hrm-api/Modules/Transport/.../DeliveryQuotation`.

Chi tiết từng việc QA xem `plan.md`. File này chỉ ghi các **quyết định** cần nhớ về sau.

## Quyết định đã chốt

### QĐ1 — Nút "Lưu nháp" vs "Lưu và tiếp tục" (Item 10, user chốt 2026-11-03)

**Bối cảnh:** spec (ảnh QA mục 1) ghi "Thêm nút Lưu nháp và Lưu tiếp tục: **cả 2 chỉ cần validate
ngày hiệu lực**". Nhưng skill `button-convention` + `form-validate` quy định "Lưu và tiếp tục" là
một kiểu LƯU ĐẦY ĐỦ (chỉ khác "Lưu" ở chỗ ở lại form tạo tiếp), không phải kiểu nháp.

**Chốt theo SKILL (SKILL thắng SPEC về hình thức — CLAUDE.md):**

| Nút | Validate | Sau khi lưu |
| --- | --- | --- |
| **Lưu nháp** (`is_draft=1`) | CHỈ ngày hiệu lực bắt buộc; nới `required` xe/trọng tải/tuyến/km_actual. Rule ĐỊNH DẠNG vẫn chặn. | Về màn danh sách |
| **Lưu** (`is_draft=0`) | ĐỦ mọi trường bắt buộc | Về màn danh sách |
| **Lưu và tiếp tục** (`is_draft=0`) | ĐỦ mọi trường bắt buộc (= như "Lưu") | Ở lại form, reset để tạo bản mới |

- "Lưu và tiếp tục" chỉ hiện ở **Tạo mới** (sửa thì bản ghi đã tồn tại, không có "tiếp tục tạo mới").
- Mọi kiểu lưu đều set/giữ trạng thái **DANG_TAO (3)** — `store()` luôn set, `update()` không đổi
  status → yêu cầu "sau khi lưu → đang tạo" thỏa sẵn, không cần code thêm.
- Rule định dạng (date / numeric / exists / max) **luôn bật ở BE** cho mọi kiểu lưu — nháp lọt dữ
  liệu sai định dạng là sai nằm vĩnh viễn trong DB (form-validate mục 1).

**Bẫy đã xử lý:** bảng con `delivery_quotation_vehicles.vehicle_category_id`,
`..._payloads.vehicle_payload_id`, `..._roads.road_id` đều **NOT NULL**, mà
`syncDetails/syncPayloads/syncRoads` tạo dòng con KHÔNG tự lọc null. Nháp gửi mảng mặc định của FE
(1 xe `vehicle_category_id=null`, 1 tuyến `road_id=null`) sẽ nổ ràng buộc khoá ngoại. →
`DeliveryQuotationService::sanitizeDetails()` lọc bỏ mọi dòng con chưa đủ khoá ngoại TRƯỚC khi
`syncDetails` (no-op với bản lưu đầy đủ vì validate đã bắt đủ).

### QĐ2 — Trạng thái, Người/Ngày cập nhật, Lịch sử (Item 14–16, 2026-11-04)

**Trạng thái — chữ + màu do BE quyết** (`DeliveryQuotation::STATUS_META` / `statusMetaOf()`, Resource trả
`status_text` + `status_color`, FE chỉ `V2BaseBadge`):

| status | Chữ | Màu (nhóm chuẩn) |
| --- | --- | --- |
| 3 `DANG_TAO` | Đang tạo | `#64748B` (nháp) |
| 1 `DA_TONG_HOP` | Đã lập tổng hợp giá | `#16A34A` (hoàn thành) |
| khác | Không xác định | `#6B7280` |

Status 1 được set khi lập **Tổng hợp giá vận chuyển đề xuất (THGVC)** từ mẫu báo giá
(`DeliveryCostSummaryService::store`) — đồng thời ghi 1 dòng lịch sử "Thay đổi trạng thái".

**Lịch sử — dùng hạ tầng chung `catalog_histories`** (trait `LogsCatalogHistory` +
`CatalogHistoryService`), KHÔNG tạo bảng log riêng:
- Phạm vi ghi: 5 trường đầu phiếu (`date_valid_from`, `date_valid_to`, `km_actual`, `price_list_valid_id`,
  `note`) + 2 khoá ẢO dạng bảng `vehicle_rows` (Dòng xe – tải trọng) / `road_rows` (Tuyến đường, gồm Km)
  — cây con xóa-tạo-lại mỗi lần lưu nên khoá dòng là khoá tự nhiên (`vehicle_category_id`, `road_id`), DTO
  diff ra thêm mới / đã xóa / sửa thông tin. Ghi ở store / update (không đổi gì thì KHÔNG ghi) / destroy
  + đổi trạng thái.
- Khai ở `CatalogHistoryService::TABLES` (KHÔNG phải `GATED_TABLES`) → đọc qua endpoint chung
  `GET catalog-histories/delivery_quotations/{id}`: mẫu báo giá không chứa giá, danh sách không scope dữ
  liệu theo người xem → **không cần quyền mới / endpoint riêng có gate**.
- FE: danh sách = row action "Lịch sử" mở `CatalogHistoryModal`; chi tiết = khối `SystemInfoSection`
  cuối form (`endpoint-base="catalog-histories"`). Bản ghi cũ trước 04/11/2026 không có log (không backfill).

**Ngày giờ:** cột Ngày tạo / Ngày cập nhật hiển thị `d/m/Y H:i` (BE format sẵn).

### QĐ3 — Phạm vi dropdown "Áp dụng cho bảng giá hiệu lực" + dòng "Giá cước vượt trội" (Item 17–18, 2026-11-04)

**Phạm vi bảng giá = công ty của NGƯỜI ĐĂNG NHẬP** (bám ERP `DeliveryQuotationController::create/edit/copy`:
`PriceListValidDelivery::where('company_id', auth()->user()->info->company_id)`). Trước đây HRM trả cả 7 bảng
của mọi công ty, ERP chỉ 3.
- Một hàm duy nhất `DeliveryQuotationLookupController::scopeCurrentCompany()`, dùng chung cho dropdown
  (`priceLists`), lấy dữ liệu bảng giá (`priceListData`) và rule `exists` của Store/UpdateRequest
  (defense-in-depth: gọi thẳng API với id bảng giá công ty khác → 422).
- Không xác định được công ty → `whereRaw('1 = 0')`, KHÔNG `company_id IS NULL`.
- **Sửa / Chi tiết giữ bảng giá phiếu đang dùng** kể cả khi thuộc công ty khác (phiếu cũ): FE gửi
  `include_ids`, UpdateRequest cho qua đúng id phiếu đang lưu; đổi sang bảng giá công ty khác vẫn bị chặn.
- **Nhân bản**: bảng giá nguồn không nằm trong phạm vi → xoá trống, người dùng chọn lại.

**"Giá cước vượt trội"**: dòng thứ 3 trong `thead` của ma trận (Số km = `-`, mỗi cột tải trọng 1 ô khoá
`—`), chỉ để HIỂN THỊ, KHÔNG lưu dữ liệu — giống ERP (input `disabled`, không có cột trong DB). File
Excel xuất đã có dòng này từ trước.

### QĐ4 — Ô giá trang trí trong ma trận dùng markup TĨNH, KHÔNG V2Base (Item 20, user chốt 2026-11-06)

**Vấn đề:** CLAUDE.md quy định "ô chỉ để ĐỌC vẫn dùng V2Base* + disabled". Nhưng ma trận giá có N ô
trang trí = số tuyến × số cột (loại xe × trọng tải); 50 tuyến × ~14 cột ≈ 700+ ô. Mỗi `V2BaseInput`
gắn mixin vee-validate → đăng ký 1 field validate, 700+ instance làm màn treo khi gõ/bấm.

**Quyết định (user "Đồng ý dùng ô tĩnh"):** 2 vị trí ô giá THUẦN TRANG TRÍ — hàng "Giá cước vượt trội"
và thân ma trận — đổi sang `<div class="cell-placeholder">—</div>` (SCSS giả khung ô disabled). Các ô
này KHÔNG `v-model`, KHÔNG gửi BE, KHÔNG cần validate (ma trận rỗng để NCC điền trên file Excel xuất ra)
nên bỏ V2Base không mất gì. NGOẠI LỆ hẹp của quy tắc V2Base, chỉ áp cho ô trang trí số-lượng-lớn ở màn
này; mọi ô THỰC (Số Km `v-model`, ô Tuyến mở picker, select loại xe / trọng tải) GIỮ nguyên V2Base.
