# Hỗ trợ SQL dữ liệu prod (không sửa code) (@junfoke)

## Ngày 10/11/2026 (@junfoke)
- [x] 10/11/2026 — Hỗ trợ xuất danh sách toàn bộ hàng hoá cổng ETEK POWER (`erp.etekpower.com.vn`, DB cũ trước gộp, nhánh `master`): viết SQL theo cột chức năng Xuất Excel danh sách hàng hoá, đổi mã loại/trạng thái/người tạo sang tên, kèm `p.*`. Chạy thử local (`gop_db_rbac`), chưa chạy trên DB Power.
- [x] 10/11/2026 — Hỗ trợ cập nhật mẫu in mới nhất (mẫu 147) cho 2 HĐ `HĐ_TPE_HN_KDXM_26_0575_XMHD` (30925) và `HĐ_TPE_HN_KDXM_26_0577_XMTN` (30971): SQL có sao lưu `bk_20261110_firm_contracts_mau_in` + câu hoàn tác, chạy thử local rồi user chạy prod (`giong_mau = 1` cả 2). Kinh doanh cần nhập lại phần đã sửa tay (ngày lập, GUQ 045/2026/GUQ-TPETEK, số ngày giao/bàn giao, điều khoản riêng).

## Ngày 13/11/2026 (@junfoke)
- [x] 13/11/2026 — Hỗ trợ đổi ngày trên mẫu in phụ lục `HĐ_TPE_HN_KDTM_26_1225_TPE-VH_PLG1` (`/admin/sale/firm-contracts-annexes/30500`) về 13/11/2026: phụ lục nằm ở `firm_contracts` (id 30500, `parent_contract_id` 28231), không phải `contract_annexes` (2 lượt SQL đầu đoán sai bảng, ra rỗng). Ngày trong HTML lưu `05 th&aacute;ng 12` + dấu cách không ngắt (C2A0) + `năm 2024` ⇒ REPLACE bằng biến `@old/@new` có `UNHEX('C2A0')`, sao lưu `firm_contracts_bk_30500_20261113`. User chạy prod: `so_lan = 1` → UPDATE → ngày cũ 0 / ngày mới 1. Bảng sao lưu còn trên prod.
- [x] 13/11/2026 — Hỗ trợ đổi người tạo phiếu duyệt KQ `TPE.PDKQ.2026020028` từ Nguyễn Thị Thu Huyền (`employees.id` 867) sang anh Quách Xuân Phương - phòng KTCN (`employees.id` 364, không phải `employee_infos.id` 344): `UPDATE wr_assign_tasks SET created_by = 364 WHERE id = 20028 AND code = … AND created_by = 867`. User kiểm SELECT trước = 867 rồi chạy. Sau đổi chỉ anh Phương vào được màn sửa phiếu.
