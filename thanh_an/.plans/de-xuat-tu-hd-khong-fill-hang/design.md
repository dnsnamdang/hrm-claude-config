# Design — Phiếu đề xuất từ HĐ kết xuất không tự fill hàng

- **Mục tiêu:** người lập tự chọn hàng cần đề xuất thay vì nhận sẵn toàn bộ hàng còn lại của HĐ rồi phải xóa bớt.
- **Scope:** chỉ FE `pages/supply/supply_proposals/add.vue` (luồng `?contract_id=`).
- **Giữ nguyên:** loại đề xuất, khách hàng, HĐ nguồn vẫn điền sẵn + khóa; API prefill vẫn chặn HĐ đã đề xuất đủ.
- **Popup:** `sourceContractId` = HĐ nguồn → ẩn hẳn hàng HĐ khác, bộ lọc HĐ chỉ còn HĐ nguồn + "Ngoài hợp đồng" (đã có từ 23/09/2026).
- **Hệ quả:** hàng chọn từ popup vào phiếu với SL = 0 như lập tay (không còn điền sẵn SL còn được đề xuất). Nếu chỉ chọn hàng ngoài HĐ → phiếu thành khách lẻ, không lưu contract_id (giống khi xóa hết hàng HĐ trước đây).
