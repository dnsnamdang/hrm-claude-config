# YC tính giá / Phiếu tính giá — tab Chi phí: gõ đơn giá bị nhảy số (17/11/2026)

Nguyên nhân: HRM chỉ lưu TỈ LỆ (2 số lẻ) rồi tính ngược đơn giá = giá NCC × tỉ lệ / 100 → gõ 25,500,000 thành 26.98% → hiện lại 25,496,100.
ERP (PriceCalculateRequestProductCost.blade.php) giữ nguyên `_value` người gõ, tỉ lệ chỉ để hiển thị.

Worktree: `HRM/wt-cost-api`, `HRM/wt-cost-client` (nhánh `fix/yctg-chi-phi-don-gia` từ origin/develop).

- [x] FE mixin `priceInputRowsMixin`: chi phí giữ `value`; gõ đơn giá → giữ value, tỉ lệ làm tròn 2 số; gõ tỉ lệ → bỏ value, đơn giá = giá NCC × tỉ lệ; đổi giá NCC → chi phí có value giữ đơn giá, tính lại tỉ lệ
- [x] FE gửi `value` kèm `rate` (YCTG form + PTG form), nạp `value` khi mở phiếu sửa
- [x] BE YCTG writer: nhận `value` nếu có (0 ≤ value ≤ giá NCC), tỉ lệ suy ra; không có thì như cũ
- [x] BE PTG writer compute/validate + skeletonRows (YCTG → PTG chép cả value)
- [x] Test BE: 2 test mới + sửa n198 (dòng nháp giữ đơn giá đã lưu); YCTG 12/12, PTG 20/20 (n198 sửa xong chạy lại xanh)
- [ ] Thử tay trên giao diện
- [x] Push develop: api 01255efd6 / client 6b8269046; gop_db: api e5465d9b6 / client 823561986 (17/11)

### Checkpoint — 17/11/2026
Vừa hoàn thành: code + test BE, giả lập mixin FE bằng node
Đang làm dở: —
Bước tiếp theo: QA thử trên develop/gop_db

