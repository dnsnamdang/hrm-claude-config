# Hỗ trợ SQL dữ liệu prod (không sửa code) (@junfoke)

## Ngày 10/11/2026 (@junfoke)
- [x] 10/11/2026 — Hỗ trợ xuất danh sách toàn bộ hàng hoá cổng ETEK POWER (`erp.etekpower.com.vn`, DB cũ trước gộp, nhánh `master`): viết SQL theo cột chức năng Xuất Excel danh sách hàng hoá, đổi mã loại/trạng thái/người tạo sang tên, kèm `p.*`. Chạy thử local (`gop_db_rbac`), chưa chạy trên DB Power.
- [x] 10/11/2026 — Hỗ trợ cập nhật mẫu in mới nhất (mẫu 147) cho 2 HĐ `HĐ_TPE_HN_KDXM_26_0575_XMHD` (30925) và `HĐ_TPE_HN_KDXM_26_0577_XMTN` (30971): SQL có sao lưu `bk_20261110_firm_contracts_mau_in` + câu hoàn tác, chạy thử local rồi user chạy prod (`giong_mau = 1` cả 2). Kinh doanh cần nhập lại phần đã sửa tay (ngày lập, GUQ 045/2026/GUQ-TPETEK, số ngày giao/bàn giao, điều khoản riêng).
