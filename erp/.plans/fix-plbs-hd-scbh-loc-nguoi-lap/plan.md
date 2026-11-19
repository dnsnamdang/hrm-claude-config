# Phụ lục bổ sung HĐ SC - BH: thêm lọc Người lập

Không Redmine · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Xử lý: màn Phụ lục bổ sung HĐ SC - BH (`warranty_repair_contract_addition_annexs`) chưa có lọc theo người lập → thêm ô "Người lập" sau "Người duyệt hợp đồng", chọn nhân viên giống ô "Người lập hợp đồng" màn HĐ SC - BH; BE đã có sẵn điều kiện lọc (`WrServiceContract.php:983`), áp cả danh sách + Xuất Excel. 1 file `index.blade.php`. Commit `ba66eec24b` — đã lên gop_db + develop_02.

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Hỗ trợ: DS HĐ SC-BH (`warranty_repair_contracts?type=all`) người không lập HĐ vẫn thấy action Tạo phiếu YC xuất hàng / PL bổ sung / PL giảm / Quyết toán → không phải lỗi: 4 hàm `canProductExport/canAdditionAnnex/canAnnex/canSettlementContract` (`WrServiceContract.php`) cho người lập **hoặc Super Admin**; tài khoản trong ảnh (`huyenntt.qttt`) có Super Admin. Chưa sửa, chờ user quyết có bỏ ngoại lệ Super Admin không.
