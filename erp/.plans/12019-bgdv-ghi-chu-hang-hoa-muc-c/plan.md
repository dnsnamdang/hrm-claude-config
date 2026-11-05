# #12019 — Báo giá dịch vụ: ghi chú từng dòng mục C. Hàng hóa (+ chặn chọn trùng hàng)

Redmine #12019 "[Bán hàng] Báo giá dịch vụ: phần C. Hàng hóa cho phép điều ghi chú" · @junfoke · ERP `TanPhatDev` (CSKH › Báo giá dịch vụ)

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Tính năng mới #12019: mỗi dòng mục **C - Loại hàng hóa** có nút "Thêm ghi chú" dưới tên hàng (giống báo giá thường), màn xem hiện "Ghi chú: …"; in ra Mẫu 1, Mẫu 2 (dòng ghi chú dưới tên hàng) và BGDV-02A (cột Ghi chú sẵn có). Migration `2026_11_05_000001_add_note_to_wr_service_quotation_merchandises` (có kiểm cột tồn tại), model `WrServiceQuotationMerchandise` + JS lưu. Nhánh `task_12019` tách `gop_db`, commit `01379ab72f`, merge `develop_02` `147354bfc1` (đã push; dev cần `php artisan migrate`). Chưa merge `gop_db`.
- [x] 05/11/2026 — Hỗ trợ check "thêm 3 hàng giống nhau thành 3 dòng" ở mục C: `addMerchandise` (từ 2022) chưa từng kiểm trùng, báo giá thường thì cộng dồn SL; bản in BGDV-02A gộp dòng cùng tên/model/giá/VAT/ĐVT, Mẫu 1/2 in đủ.
- [x] 05/11/2026 — Theo user: chọn lại mã đã có ở mục C thì **không thêm dòng, báo "Hàng đã được thêm vào báo giá"** — chặn cả bấm tên hàng (`formJS.blade.php`, hàm `merchandiseAdded`) lẫn tick nhiều rồi "Thêm (N)" (`searchProductQuotationJs.blade.php`, đoạn chỉ màn BGDV dùng; mã trùng bị bỏ qua, mã mới vẫn thêm). Kiểm trùng theo mã, tính cả dòng đã lưu; phiếu cũ đã trùng giữ nguyên. Commit `209d1867a2` (gop_db, đã push).
- [ ] `task_12019` đưa vào `gop_db` khi user bảo.
