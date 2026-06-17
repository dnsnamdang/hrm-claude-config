# Plan — Ghi chú + Lưu-sau-duyệt cho tab Điều khoản thanh toán

**Phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-09-contract-payment-terms-note-approve-design.md`
**Plan chi tiết:** `docs/superpowers/plans/2026-06-09-contract-payment-terms-note-approve.md`

> Khung tổng quát (chi tiết từng step xem plan chi tiết ở trên):

## Phase 1 — Backend: ghi chú trong flow thường
- [x] Migration thêm cột `payment_terms_note` (text, nullable) vào `contracts` — đã migrate thành công
- [x] Thêm `payment_terms_note` vào `$fillable` của model `Contract`
- [x] Thêm rule `payment_terms_note` vào `StoreContractRequest`
- [x] Đảm bảo create/update lưu `payment_terms_note` (mass-assignment qua `fill`)
- [x] Trả `payment_terms_note` trong `ContractDetailResource`

## Phase 2 — Backend: lưu khi đã duyệt
- [x] Service `updatePaymentTermsAfterApprove` (guard status=3, tái dùng `syncPaymentTerms` + lưu note)
- [x] Controller method
- [x] Route `POST contracts/{contract}/updatePaymentTermsAfterApprove` — route:list xác nhận đăng ký OK

## Phase 3 — Frontend
- [x] `PaymentTermsTab.vue`: prop `note` + `canEditAfterApprove`, ô textarea ghi chú, computed `isLocked`
- [x] `GeneralComponent.vue`: bind note + canEditAfterApprove, nút Lưu trong tab, change-tracking, gọi API

## Phase 4 — Kiểm thử (chờ verify thủ công qua UI)
- [ ] Add/Edit: nhập & lưu ghi chú
- [ ] HĐ đã duyệt: mở khóa, sửa bảng + note, bấm Lưu → cập nhật đúng
- [ ] Nút Lưu disable khi không có thay đổi; ẩn khi chưa duyệt

---

### Checkpoint — 2026-06-09
Vừa hoàn thành: Toàn bộ code Phase 1-3 (7 file BE + 2 file FE), cả 3 phase đã qua review spec + chất lượng (APPROVED). Migration đã chạy, route đã đăng ký.
Đang làm dở: (không)
Bước tiếp theo: Verify thủ công Phase 4 qua UI — màn `contract/contract/add` (nhập ghi chú) và màn chi tiết HĐ đã duyệt (status=3) test nút Lưu. Sau đó user tự commit cả 2 repo.
Blocked:
