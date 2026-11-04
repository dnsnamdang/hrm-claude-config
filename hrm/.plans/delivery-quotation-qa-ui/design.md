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
