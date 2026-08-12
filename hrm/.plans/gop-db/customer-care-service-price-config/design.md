# Design — Cập nhật nhanh giá dịch vụ (CSKH)

**Người phụ trách:** @junfoke — 2026-08-06
**Nhánh:** `gop_db`
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-08-06-customer-care-service-price-config-design.md`

## Mục tiêu

Chuyển màn **Cập nhật nhanh giá dịch vụ** từ ERP sang HRM, phân hệ **CSKH**
(`/customer-care/service-price-config`). Màn danh mục thứ 6 của phân hệ.

## Scope

**Có:** 1 form 2 trường (Hệ số giá bán dịch vụ, Định mức đàm phán giá %) lưu vào
`service_price_config` (1 dòng duy nhất) + **cập nhật hàng loạt** 207 gói bảo dưỡng / 242 cấp dịch
vụ; 2 route `GET|PUT /v1/customer-care/service-price-config`; popup xác nhận trước khi lưu;
migration đưa quyền ERP 100320 về phân hệ CSKH; điền link menu.

**Không:** đổi công thức tính `base_price`, đổi schema, bỏ hành vi ghi đè hàng loạt, đụng màn
Danh mục gói bảo dưỡng.

## Quyết định chính

1. **Quyền: thêm bản ghi HRM guard `api` TRÙNG TÊN quyền ERP** (id 1130,
   `Cập nhật nhanh giá dịch vụ`, group `Danh mục dịch vụ bảo dưỡng`, type 24) và gate route bằng
   **`erpPermission`** (khớp theo TÊN, không quan tâm guard) → ai có quyền ở ERP **hoặc** ở HRM đều
   dùng được màn.
   Phương án ban đầu — giữ id 100320 và chỉ đổi `type` — **đã thử rồi rollback**: quyền đó có
   `guard_name = web`, mà FE chỉ nạp quyền guard `api` nên middleware đá về 404, và middleware BE
   `checkPermission` cũng luôn 403. Xem mục Gotcha.
2. **Thêm popup xác nhận** nêu rõ số gói bị ảnh hưởng (ERP bấm Lưu là chạy luôn) — số lấy từ API.
3. **Giữ nguyên hành vi ghi đè hàng loạt** của ERP: mọi gói đều bị áp lại hệ số và định mức, kể cả
   gói đã chỉnh riêng.
4. Dùng lại entity `Service` / `ServiceLevel` đã port ở màn Danh mục gói bảo dưỡng.

## Gotcha

- **Bảng `service_price_config` chỉ có 1 dòng**, ERP hardcode `find(1)` → HRM dùng `firstOrNew`.
- `base_price` **chỉ** tính lại khi hệ số thực sự đổi; `coefficient_cost_price_service` và
  `sale_max_percent` thì **luôn** ghi đè cho mọi gói.
- Gói không resolve được `work_price` của công ty: ERP ghi `base_price = 0`, HRM **bỏ qua gói đó**
  và báo lại số gói bị bỏ qua.
- 4 lỗi ERP đã sửa khi port: `catch (Exception)` bắt nhầm `League\Flysystem\Exception`; `dd()` trong
  catch; `find(1)` không guard null; ghi giá về 0 khi thiếu công ty.
- **Quyền ERP dùng guard `web`, HRM dùng guard `api`** — đây là bẫy lớn nhất của màn này:
  `store.state.permissions` ở FE **chỉ chứa quyền guard api** (573 quyền, không có cả
  `Xem khách hàng` id 100057 đã đổi type từ đợt trước) → mục menu gate bằng tên quyền ERP sẽ luôn
  bị `middleware/checkPermission.js` đá về `/pages/extras/404`. Middleware BE `checkPermission`
  cũng đọc qua Spatie guard `api` nên luôn 403.
  → Muốn dùng quyền ERP ở BE thì phải gate bằng **`erpPermission`**; muốn FE thấy quyền thì phải có
  **bản ghi guard `api`** (trùng tên là hợp lệ, spatie chỉ unique theo `name + guard_name`).
- Không đụng bản ghi ERP 100320 (giữ `web` / `type = NULL` / group `Kế toán làm giá`) để màn ERP
  và 4 dòng phân quyền hiện có chạy y nguyên.
- `$nuxt.$loading` chưa sẵn sàng lúc `mounted()` → phải gọi `$loading?.start?.()`.
- Sao lưu cột bị ghi đè **trước** lần gọi API ghi đầu tiên: màn này ghi đè 207 gói ngay lần lưu
  đầu, sao lưu sau là mất dữ liệu gốc.
