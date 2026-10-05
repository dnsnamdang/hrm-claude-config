# Plan — Fix phiếu tính giá hiển thị sai Giá mới

@junfoke — Repo `TanPhatDev`. Xem `design.md`.

## Phase 1 — Điều tra
- [x] Truy vết màn Chi tiết phiếu tính giá → class `PriceCalculateProduct` / `ProductPrice`
- [x] Xác định thủ phạm: `recalcAllPrices()` trong `after()` (commit `542b97637e`, 17/04/2026)
- [x] Gửi user SQL read-only check prod (2 phiếu KT báo + rà toàn bộ phiếu lệch)
- [x] Kết luận: DB đúng, chỉ sai hiển thị; phiếu Đã duyệt không sửa được nên chưa bị ghi đè

## Phase 2 — Fix FE
- [x] `PriceCalculateProduct`: thêm getter `is_saved_record`, chỉ recalc khi bản ghi chưa lưu
- [x] `ProductPrice.shouldUseDatabaseEcommerceValue()`: bản ghi đã lưu → dùng giá DB (giá TMDT)
- [x] Giữ nguyên line ending (LF), diff gọn 11 dòng thêm / 1 dòng sửa

## Phase 3 — Verify local (:8001, DB erp_dev_30_01_26)
- [x] Chi tiết phiếu tính giá PTG-00007: 3,600,000 (đúng DB), công thức 3,660,000
- [x] Chứng minh ngược: gọi tay `recalcAllPrices()` → về 3,660,000
- [x] Sửa phiếu PTG-00002: hiển thị + `submit_data` đều 6,000,000 → lưu lại không đè
- [x] Yêu cầu hỏi giá PYCHG-00013: đúng DB (màn này cũng đang lỗi, fix chung)
- [x] Kết quả tính giá id 6: đúng DB (trước fix hiện 0)
- [x] Tạo mới (useRequest PYCTG-00016): vẫn recalc như cũ → không hồi quy

## Còn lại
- [ ] User test lại trên dev/prod với đúng PTG-03082 & PTG-03086
- [ ] Commit / merge (chưa commit theo quy ước)

## Phase 4 — #11334: Đơn giá tab Tính giá lấy theo Thành tiền sau thuế
- [x] Đọc issue Redmine 11334 + ảnh QA (PTG-03046, thuế NK 25%)
- [x] Xác định cột đang bind `supplier_price_exchange` (trước thuế)
- [x] Hỏi user: Giá nhập kho có cộng theo sau thuế không → **CÓ**
- [x] `form.blade.php:267` cột Đơn giá VNĐ → `amount_exchange_after_tax`
- [x] `PriceCalculateProduct.cost_price` cộng từ `amount_exchange_after_tax`
- [x] Verify local: nhập thuế NK 25% trên PTG-00002 → Đơn giá = Giá nhập kho = 13,888,888.75, bảng cộng khớp, giá mới đã lưu không đổi
- [ ] User test PTG-03046 trên prod sau khi deploy
- [ ] **CHỜ USER CHỐT**: phiếu CŨ có thuế NK > 0 hiển thị Giá nhập kho theo số ĐÃ LƯU hay theo công thức mới (user hoãn 07/09/2026 — "chờ phương án sau"). Hiện chạy theo công thức mới; không ảnh hưởng DB/bán hàng. Xem mục ĐIỂM MỞ trong design.md

## Phase 5 — #11335: Link xem chi tiết Yêu cầu tính giá
- [x] Đọc issue Redmine 11335
- [x] Rà project tìm pattern link chứng từ liên quan → khuôn `firm_warrantys/form.blade.php:16`
- [x] Áp khuôn đó cho ô "Chọn yêu cầu tính giá" + `ng-if` cho màn Tạo mới
- [x] Verify local: link đúng id, target _blank, HTTP 200; màn tạo mới không vỡ
- [ ] User test trên prod (PTG-03086)

### Checkpoint — 2026-09-07
Vừa hoàn thành: fix 2 file FE + verify 5 kịch bản trên local.
Đang làm dở: không.
Bước tiếp theo: user test PTG-03082 / PTG-03086 trên môi trường có data thật rồi commit.
Blocked: không.
