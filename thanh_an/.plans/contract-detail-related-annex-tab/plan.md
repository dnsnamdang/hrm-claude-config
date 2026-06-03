# Plan: Tab "Phụ lục liên quan" — Chi tiết hợp đồng

> @khoipv — Spec: `docs/superpowers/specs/2026-06-03-contract-detail-related-annex-tab-design.md`
> Plan chi tiết (step-by-step): `docs/superpowers/plans/2026-06-03-contract-detail-related-annex-tab.md`

## Task (tổng quát)

### Phase 1 — Backend
- [x] Thêm field `annexes` (+ `annex_type_label`) vào `ContractDetailResource.php` (dòng 17 import, 256-262 field)

### Phase 2 — Frontend
- [x] Thêm template bảng phụ lục vào tab rỗng `GeneralComponent.vue:1112-1152`
- [x] Import + đăng ký `BaseStatusColor`, thêm `ANNEX_TYPE_ROUTE_MAP`, `statusColorMap`
- [x] Thêm method `getAnnexDetailRoute`, `getAnnexStatusText`
- [x] Click mã phụ lục mở **tab mới** (`target="_blank" rel="noopener"`)

### Phase 3 — Kiểm thử (user thực hiện trên trình duyệt)
- [ ] Mở chi tiết hợp đồng có phụ lục → bảng hiển thị đúng, click mã → đúng trang chi tiết
- [ ] Hợp đồng không phụ lục → hiển thị "Chưa có phụ lục liên quan"

---

### Checkpoint — 2026-06-03
Vừa hoàn thành: Code BE + FE xong, đã qua review spec + chất lượng (đều approved). Tích hợp BE↔FE khớp 5 key.
Đang làm dở: (không)
Bước tiếp theo: User chạy server, kiểm thử thủ công Phase 3 trên trình duyệt; sau đó tự commit.
Blocked: (không)
