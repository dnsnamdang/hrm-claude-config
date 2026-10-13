# Plan — Fix rò phiếu chéo công ty (yêu cầu đặt hàng)

## Tasks
- [x] Thêm `->where('send_company_id', $item->company_id)` vào vòng tính `$ids` trong `RootOrderRequest::searchByFilter()` (~dòng 332)
- [x] `php -l` sạch
- [x] Verify prod (read-only): đếm lại phiếu status=3 Lê Trung Tiến (id 290) thấy — kỳ vọng giảm 75 → 4 (chỉ cty 4)
- [x] Kiểm 3 nhánh (all/for-approved/else) vẫn dùng `$ids` đúng
- [ ] Chờ user test browser + xác nhận trước khi commit

### Checkpoint — 2026-07-24
Vừa hoàn thành: chẩn đoán prod xác nhận rò chéo công ty (B); tạo plan.
Bước tiếp theo: sửa dòng 332 + verify đếm trước/sau.
Blocked: —
