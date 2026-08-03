# Design (tóm tắt) — Tự gắn hàng hóa từ HĐ liên quan vào KPI

**Người phụ trách:** @khoipv · **Ngày:** 2026-06-30 · **Phạm vi:** Frontend (không sửa BE)

## Mục tiêu
Form HĐ (`contract/contract` add + edit): khi `has_kpi == 1` **và** đã chọn **HĐ liên quan** → tự động lấy **hàng hóa thường** (`groups`) của HĐ liên quan, **giữ nguyên cấu trúc nhóm**, **giá/SL theo HĐ liên quan**, **thêm vào cuối** danh sách KPI (`group_kpis`).

## Quyết định lớn
- **Thuần FE**, tái dùng endpoint `GET category/contracts/{id}` để lấy `groups` của HĐ liên quan. Không cần BE mới (BE `syncGroupKpis` dùng `fill()` theo fillable → field thừa bị bỏ qua an toàn).
- **Kích hoạt tự động** qua `watch` `has_kpi` + `related_contract_id`, kèm cờ `kpiAutofillReady` để **không** tự gắn khi trang edit nạp dữ liệu.
- **Đánh dấu** nhóm tự gắn bằng cờ transient `from_related_contract: true` (không lưu DB) để phục vụ "tự gỡ".
- **Append, giữ nhóm cũ.** Đổi HĐ liên quan nhiều lần → **cộng dồn** (đã được xác nhận chấp nhận).
- **Tự gỡ** nhóm `from_related_contract` khi **bỏ chọn HĐ liên quan** hoặc **tắt áp KPI**; giữ nhóm người dùng tự thêm.

## File chạm
- `pages/contract/contract/components/GeneralComponent.vue` (data + watch + 2 method).

## Spec chi tiết
`docs/superpowers/specs/2026-06-30-contract-kpi-autofill-from-related-design.md`
