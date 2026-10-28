# Gộp mã còn mang phạm vi trong tên (U9) — bảng đối chiếu, bước 1

CSV: `gop-ma-pham-vi.csv` (27 dòng). Số vai trò/người đọc từ `hrm_erp_rbac_rehearsal` (chỉ SELECT); "goi: N" = số chỗ gọi quyền (permission:scan).

## Tổng
- 27 mã khớp dấu hiệu phạm vi (design nói ~25: 17 Xem, 5 Thao tác, 3 Duyệt; thực tế 18 Xem, 6 Thao tác, 3 Duyệt).
- Theo loai: `khong_phai_pham_vi` 18 (đều là Xem) · `can_user_quyet` 9 (6 thao tác + 3 duyệt) · `gop` 0.
- Số nhóm đích: 5 (chi tiêu tạo, chi tiêu duyệt, thị trường tạo, thị trường duyệt, giá bán tạo) + 18 mã Xem giữ nguyên.

## Điều bất ngờ
1. **18 mã Xem đã gộp rồi từ GĐ1**: đều đã có `scopes` (1-4 hoặc 2-4) và `legacy` theo cấp. Chữ "theo nhân viên / theo phòng ban / theo công ty" trong tên là chiều nhóm của báo cáo (báo cáo X theo nhân viên), không phải phạm vi dữ liệu. Không cần gộp, chỉ giữ nguyên.
2. **9 mã còn lại GĐ1 đã cố ý để riêng** (quy ước 5 trong Catalog: "cấp nghiệp vụ, không phải phạm vi"). U9 lại muốn gộp. Hai quyết định đang mâu thuẫn nên cần user chọn.
3. Quyền nhân viên/phòng ban của chỉ tiêu và thị trường là hai loại phiếu khác nhau (Company vs Department controller); gộp nghĩa là một mã dùng phạm vi để phân biệt cấp giao.
4. Nhiều người dính: `presale.gia_ban_theo_phong.create` có 174 người.

## Câu cần user quyết (can_user_quyet)
Mỗi câu có 3 phương án chung: **1** = gộp, phòng ban/công ty ⇒ phạm vi 3 (công ty), nhân viên/phòng ⇒ phạm vi 2 (phòng ban); **2** = gộp đúng chữ U9: biến thể "theo nhân viên" ⇒ phạm vi null, "theo phòng ban" ⇒ 2; **3** = giữ tách như GĐ1 (không gộp).

- **Q1 Chỉ tiêu kinh doanh** (4 mã: `sale.chi_tieu_kinh_doanh_phong_ban|nhan_vien` × `create|approve` → `sale.chi_tieu_kinh_doanh.create|approve`, scopes 2,3): gộp phiếu giao chỉ tiêu theo phòng ban và theo nhân viên thành một mã Tạo và một mã Duyệt? 1 / 2 / 3.
- **Q2 Phân chia thị trường** (3 mã: `sale.phan_chia_thi_truong_phong_ban.create`, `..._nhan_vien.create`, `..._nhan_vien.approve` → `sale.phan_chia_thi_truong.create|approve`): gộp hai loại phiếu thị trường thành một mã Tạo, và đổi mã Duyệt (chỉ có bản nhân viên) cho khớp? 1 / 2 / 3.
- **Q3 Xây dựng giá bán** (2 mã: `presale.gia_ban_theo_cong_ty.create`, `presale.gia_ban_theo_phong.create` → `presale.gia_ban.create`, scopes 2,3): gộp "theo công ty" (3) và "theo phòng" (2) thành một mã? Lưu ý GĐ1 ghi đây là cấp triển khai (liên phòng vs theo phòng) nên rủi ro đổi nghĩa cao hơn. 1 / 3 (phương án 2 không áp dụng vì không có biến thể nhân viên).

Gộp theo 1 hoặc 2: vai trò giữ cả hai biến thể nhận phạm vi cao nhất (như GĐ1).
