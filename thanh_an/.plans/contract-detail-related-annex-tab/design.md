# Tab "Phụ lục liên quan" — Chi tiết hợp đồng (@khoipv)

> Tóm tắt. Spec đầy đủ: `docs/superpowers/specs/2026-06-03-contract-detail-related-annex-tab-design.md`

## Mục tiêu
Điền nội dung tab **"Phụ lục liên quan"** (hiện rỗng) trong màn chi tiết/sửa hợp đồng (`GeneralComponent.vue:1112-1115`). Hiển thị bảng phụ lục của hợp đồng: **STT, Mã phụ lục, Loại phụ lục, Trạng thái**.

## Scope
- **BE (1 file):** thêm field `annexes` (kèm `annex_type_label`) vào `ContractDetailResource.php`, dùng relation `annexes()` có sẵn + hằng `ContractAnnexApproveResource::ANNEX_TYPE_LABELS`.
- **FE (1 file):** render `b-table-simple` từ `formSubmit.annexes` trong `GeneralComponent.vue`; mã phụ lục click sang chi tiết qua `ANNEX_TYPE_ROUTE_MAP`; trạng thái badge màu `BaseStatusColor`.

## Quyết định lớn
- Nhãn loại phụ lục lấy từ BE (detail resource), không lặp logic ở FE.
- Mã phụ lục click → chi tiết đúng loại.
- STT + 3 cột; trạng thái badge màu; read-only.

## Tái dùng
- Relation `Contract::annexes()` + `ANNEX_TYPE_ROUTE_MAP` đã tạo ở feature `contract-related-annex-column` (cột phụ lục màn danh sách).
- `BaseStatusColor` + `statusColorMap` + nhãn trạng thái: theo màn `contract_annex_vat/index.vue`.

## Ngoài phạm vi
Không CRUD phụ lục, không filter/sort, không phân quyền cấp, không `is_can_delete`.
