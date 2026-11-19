# Check: HĐ đã duyệt của Trần Thị Loan không có nút Kết xuất (`/contract/contract`) — @khoipv

Bắt đầu 19/11/2026. Chỉ soát logic, không sửa code.

## Task
- [x] Tìm điều kiện hiện nút: FE `pages/contract/contract/index.vue:374` `v-if="item.can_render_supply"` → BE `Contract::canRenderSupply()` (`Modules/Category/Entities/Contract/Contract.php:363`)
- [x] Liệt kê điều kiện (cả 6 phải đúng):
  1. `status` ∈ {3 Đã duyệt, 11 Không duyệt kết xuất} (9/10 không hiện)
  2. `record_type = 2` (Hợp đồng; BB thương thảo = 1, PL giảm giá = 3 không hiện)
  3. `supply_rendered_at IS NULL` (đã từng kết xuất → ẩn)
  4. `created_by` = người đang đăng nhập (chỉ người lập; HĐ được bàn giao thì `created_by` đổi sang người nhận — `ContractService.php:970`)
  5. `contract_sign_time` không rỗng
  6. Hôm nay ≥ ngày ký (so theo ngày)
  - Không xét quyền (permission) nào.
- [x] DB local (`thanhan_stag_07052026`): Loan = employee 151, không có HĐ nào → không đối chiếu được, cần chạy SQL trên DB demo
- [x] Đăng nhập API demo bằng TK Loan (employee 151), kéo `GET category/contracts?request_type=contract` (674 HĐ, 648 HĐ trạng thái đã duyệt/đã kết xuất)
  - Loan thấy toàn bộ 674 HĐ, nhưng chỉ lập 29 HĐ (25 Đã duyệt, 3 Đã kết xuất, 1 Đang tạo)
  - **22 HĐ** của Loan có `can_render_supply = true` → nút Kết xuất CÓ hiện
  - 3 HĐ ngày ký 23/11/2026 (sau hôm nay 19/11): HD-655, HD-649, HD-640 → ẩn đúng logic "chưa tới ngày ký", 23/11 sẽ tự hiện
  - 3 HĐ đã kết xuất (HD-625, HD-623, HD-473) → ẩn đúng
  - ~620 HĐ đã duyệt còn lại do người khác lập → Loan không thấy nút (chỉ người lập mới kết xuất)
  - Kết luận: không phải bug, code chạy đúng điều kiện

### Checkpoint — 19/11/2026
Vừa hoàn thành: đối chiếu dữ liệu demo
Đang làm dở: —
Bước tiếp theo: chờ user xác nhận HĐ cụ thể đang thắc mắc (nếu khác các nhóm trên)
Blocked:
