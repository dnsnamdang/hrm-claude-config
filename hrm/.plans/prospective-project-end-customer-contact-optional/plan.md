# Plan — Bỏ bắt buộc "Người liên hệ" của KH thụ hưởng cuối

**Người phụ trách:** @khoipv

## Phase 1 — Bỏ require (FE + BE)

### FE
- [x] `CustomerBlock.vue`: thêm prop `requiredContact` (default `true`)
- [x] `CustomerBlock.vue`: label "Người liên hệ" đổi `:required="requiredCustomer"` → `:required="requiredContact"`
- [x] `CustomerInfoSection.vue`: block `benefit` truyền `:required-contact="false"`

### BE
- [x] `ProspectiveProjectRequest.php`: bỏ rule require `customer_benefit_contact_name` + `customer_benefit_contact_phone`
- [x] `ProspectiveProjectRequest.php`: xóa method dead code `benefitCustomerRequiresContact()`

### Kiểm thử (Playwright, DB hrm_production_18072026)
- [x] FE: tick KH thương mại dịch vụ → Người liên hệ KH cuối KHÔNG còn dấu `*` (KH trực tiếp vẫn có `*`) — verify qua DOM
- [x] BE: probe status=2 (lưu chính thức), intermediary=true, KH cuối doanh nghiệp, bỏ trống liên hệ → KHÔNG có lỗi require `customer_benefit_contact_name/phone`
- [x] BE đối chứng: KH trực tiếp doanh nghiệp bỏ trống liên hệ → VẪN có lỗi `customer_contact_name/phone` (không ảnh hưởng)
- [x] BE: `customer_benefit_scope_id/scope_group_id` vẫn required (các field KH cuối khác không bị đụng)

### Checkpoint — 2026-07-18
Vừa hoàn thành: sửa FE+BE + đã test bằng Playwright, cả 3 case đạt. Lưu ý: status=1 là NHÁP (bỏ require), lưu chính thức là status=2.
Đang làm dở: (không)
Bước tiếp theo: user tự thử luồng đầy đủ trên UI nếu muốn; sẵn sàng "wrap up".
Blocked:
Ghi chú: probe status=1 vô tình tạo bản ghi rác id=122 (name='probe') → đã xóa cùng status_log con, verify DB sạch.
