# Plan — ĐHNT chỉ validate giá với hàng SL > 0

## Tasks
- [x] Xác định root cause: lời gọi `getPriceByUnitAndType()` (ném `PriceNotFoundForCompany`) không chặn theo SL.
- [x] `PrincipleOrderStoreRequest::rules()` — thêm `if (qty <= 0) continue;` đầu vòng lặp product, bỏ guard qty trùng ở cuối.
- [x] `PrincipleOrderService` (save loop ~line 286) — tách nhánh: qty>0 dùng `getPriceByUnitAndType`, else `priceOrNull() ?? 0`.
- [x] `ZTPrincipleOrderStoreRequest::rules()` — áp cùng fix (skip qty≤0).
- [x] `ZTPrincipleOrderService` (save loop ~line 285) — áp cùng fix + import `ProductPriceService`.
- [x] `php -l` cả 4 file — sạch.
- [ ] (Chờ user) Test thực tế trên ERP: tạo ĐHNT có 1 dòng hàng chưa có giá tại cty + SL=0 → Lưu nháp thành công, không còn tooltip "chưa có giá".
- [x] Commit + push `gop_db`: `def03b04dc` (rebase origin/gop_db sạch) — 2026-11-03.
- [ ] (Chờ user) Test thực tế trên ERP sau khi deploy.

## Ghi chú
- `validateDifferenceListPrice()` đã gate `qty > 0` sẵn — không đụng.
- Biến thể zt (nha khoa) sửa kèm cho nhất quán; nếu luồng nha khoa cố ý bắt buộc giá thì báo để revert phần zt.

### Checkpoint — 2026-11-03
Vừa hoàn thành: Fix 4 file (2 FormRequest + 2 Service), lint sạch, viết design.md + plan.md.
Đang làm dở: (không)
Bước tiếp theo: User test trên ERP rồi quyết định commit.
Blocked: (không)
