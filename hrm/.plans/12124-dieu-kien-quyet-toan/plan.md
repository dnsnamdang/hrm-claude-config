# #12124 Điều kiện quyết toán (Quy chế bán hàng → tab Báo giá – Hợp đồng)

Redmine: http://quanly.dnsmedia.vn/issues/12124 · nhánh `feat/12124-dieu-kien-quyet-toan` (HRM api/client từ develop, ERP từ develop_02)

## Quyết định (tự chốt, báo user)
- Lưu `companies.settlement_debt_condition` tinyint mặc định 1 (migration ở HRM) — theo CÔNG TY của hợp đồng.
- 1 = Hoàn thành công nợ (logic cũ) · 2 = Số dư công nợ = 0: thêm kiểm số dư TK 1311 (gồm TK con) Nợ − Có, làm tròn đồng, đúng = 0 (trả thừa cũng chặn).
- Áp mọi loại HĐ: HĐ thường/dự án (SettlementContractService), HĐ hãng (FirmSettlement), HĐ DV BH-SC (WrSettlement) + danh sách chờ quyết toán. Biên bản thanh lý dùng chung canCreate của Firm/Wr nên cũng bị chặn.
- Không sửa hàm dùng chung `checkDebtIsOverByAccountNumber`.

## Task
- [x] ERP helper `app/Helpers/SettlementDebtCondition.php` + gắn 3 service quyết toán + UpdateContractWaitingSettlementService
- [x] HRM migration + registry field select + inline options + rule `in:1,2`
- [x] HRM client data.js tab baogia `csel('Điều kiện quyết toán', …)`
- [x] Test HRM regulation (TabRegistry/ScalarTabs/Schema/History/SaveRouting) OK
- [x] Kiểm UI Playwright (select 2 lựa chọn hiện ở tab Báo giá – Hợp đồng; giá trị 3 → 422 "Không hợp lệ"; helper ERP chặn đúng trên DB local)
- [x] Commit/push (chờ user)

### Checkpoint — 2026-11-12
Đã push develop: HRM api 1c86810e6 / client 773801cae; ERP develop_02 deb6bc2af6. Chưa gop_db. Deploy cần chạy migration companies.settlement_debt_condition.
