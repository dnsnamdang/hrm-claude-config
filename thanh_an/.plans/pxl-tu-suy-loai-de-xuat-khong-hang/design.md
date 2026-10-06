# Design — PXL tự suy loại khi đề xuất KH chưa có hàng hóa

@khoipv — Bắt đầu 01/10/2026

- **Bug:** đề xuất nhóm "Cung ứng khách hàng" chỉ chọn khách hàng (chưa chọn hàng) vẫn gửi được (có nội dung/file).
  BE suy loại theo dòng hàng trong HĐ (`SupplyProposalService::resolveType`) → không có dòng → khách lẻ (3).
  PXL copy nguyên `proposal->type` → mặc định "Cung ứng khách lẻ", popup chỉ lấy danh mục, không lấy được hàng HĐ.
- **Hướng (user chốt 01/10/2026):** PXL tự suy loại theo hàng hóa chọn, giống màn đề xuất.
- **Phạm vi áp dụng:** đề xuất `type = 3` (khách lẻ) VÀ không có dòng hàng nào → `SupplyProposal::handlingResolvesType()`.
  Đề xuất có hàng / nội bộ / loại bám HĐ giữ nguyên luật cũ (PXL copy loại đề xuất).
- **BE:**
  - `SupplyHandlingService::store()/update()`: loại PXL = loại HĐ của dòng hàng trong HĐ đầu tiên (đọc lại `contracts.type`),
    không có → khách lẻ. Trạng thái gửi tính theo loại vừa suy.
  - `DetailSupplyHandlingResource`: thêm cờ `type_from_goods` cho màn sửa.
- **FE (`supply_handlings/add.vue`):**
  - Pool gửi `group=1` + `customer_id` → hàng của mọi HĐ còn hiệu lực của khách + danh mục.
  - Popup không truyền `type` (hiện loại HĐ, ô lọc HĐ); 1 phiếu vẫn khóa 1 HĐ (`lockedContractId`).
  - `resolvedType` suy từ dòng hàng → cập nhật `formSubmit.type` (cột bảng, header "Loại", product-info).
    Rời khách lẻ → xóa `don_gia` các dòng.
- **Không đổi:** loại của chính phiếu đề xuất (vẫn 3).
