# Plan: Cột "Phụ lục liên quan" — Danh sách hợp đồng

> Người phụ trách: @khoipv | Ngày: 2026-06-02
> Spec: `docs/superpowers/specs/2026-06-02-contract-list-related-annex-column-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-06-02-contract-related-annex-column.md`

## Phase 1 — Backend

- [x] Thêm relation `annexes()` (hasMany ContractAnnex) vào `Contract.php`
- [x] Thêm `'annexes'` vào mảng `with([...])` trong `ContractService::index()`
- [x] Thêm field `annexes` (id/code/annex_type/status) vào `ContractResource::toArray()`

## Phase 2 — Frontend

- [x] Khai báo `ANNEX_TYPE_ROUTE_MAP` đầu `<script>` của `contract/index.vue`
- [x] Thêm field `{ key: 'annexes', label: 'Phụ lục liên quan', isVisible: true, tdClass: 'min-w-200' }` (trước `actions`)
- [x] Thêm cell slot `cell(annexes)` render mỗi mã một dòng bằng `b-link`
- [x] Thêm method `getAnnexDetailRoute(annex)` build URL `/contract/{route}/{id}`
- [x] Click mã phụ lục mở sang tab mới (`target="_blank"` trên `b-link`)

## Phase 3 — Verify

- [ ] Hợp đồng nhiều phụ lục khác loại → mỗi mã link đúng route theo loại
- [ ] Phụ lục mọi trạng thái đều hiển thị
- [ ] Hợp đồng không phụ lục → ô trống
- [ ] Tuỳ chỉnh cột: ẩn/hiện cột hoạt động; user cấu hình cũ vẫn thấy cột mới
- [ ] Xuất Excel KHÔNG có cột phụ lục
- [ ] Phân trang/đổi filter cột vẫn render đúng
