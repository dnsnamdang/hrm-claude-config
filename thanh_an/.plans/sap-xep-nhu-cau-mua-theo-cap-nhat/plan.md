# Plan — Sắp xếp mặc định "mới nhất lên đầu" (Báo cáo tổng hợp nhu cầu mua hàng)

**Phụ trách:** @khoipv
**Màn:** `supply/reports/purchase-demand`
**Ngày:** 2026-09-08

## Mục tiêu (bản chốt cuối)
Vào màn là **mã hàng vừa được đẩy sang báo cáo gần nhất nằm trên đầu**, không cần thao tác gì.
**Không có checkbox** — sắp xếp là hành vi mặc định.

## Lịch sử quyết định
1. Ban đầu: thêm checkbox "Cập nhật gần nhất" để bật/tắt sắp xếp (đã code + verify).
2. Phát hiện khi @khoipv hỏi thứ tự mặc định: query **không có `ORDER BY`** → thứ tự do MySQL tự
   quyết (tình cờ ra `shp.id` tăng dần = **cũ nhất lên đầu**, và không có gì bảo đảm).
3. **@khoipv chốt:** bỏ checkbox, cho mới nhất lên đầu làm mặc định luôn.

## Mốc thời gian dùng để sắp xếp
`MAX(COALESCE(sh.approved_at, sh.created_at))` của các PXL gộp vào mã hàng đó.

- Dòng chỉ vào báo cáo khi PXL `status = 5` (đã duyệt) → mốc đúng là **thời điểm duyệt**.
- Nhưng cột `status` **default 5**: phiếu lập thẳng không đi qua luồng duyệt nên `approved_at` NULL
  (thực tế staging: **6/8 phiếu NULL**). Dùng riêng `approved_at` sẽ đẩy 6/8 phiếu xuống cuối vô nghĩa
  → `COALESCE` sang `created_at` (với phiếu lập thẳng thì đó chính là lúc vào báo cáo).
- MAX vì 1 dòng báo cáo gộp nhiều PXL (gộp theo `product_id`).

## Task

### BE — `Modules/Supply/Services/SupplyReportService.php::purchaseDemand()`
- [x] Select thêm `sh.approved_at as handling_approved_at` + `sh.created_at as handling_created_at`
- [x] Thêm field `pushed_at` vào mỗi row, giữ MAX `COALESCE(approved_at, created_at)` khi gộp
- [x] `usort($allRows, ...)` giảm dần theo `pushed_at` ngay sau khi gom nhóm
- [x] Tie-break theo `product_id` (usort PHP 7.4 **không stable** → không tie-break là thứ tự dao động)
- [x] Đặt sort **trước** các bộ lọc group/ncc/hd_mua — `array_filter` giữ thứ tự nên lọc xong vẫn đúng

### FE — `pages/supply/reports/purchase-demand/index.vue`
- [x] Gỡ checkbox "Cập nhật gần nhất" khỏi khối bộ lọc
- [x] Gỡ biến `sortRecentFirst` khỏi `data` và khỏi `resetFilter()`
- [x] `displayRows` trả về nguyên bản (chỉ lọc "Chỉ mã chưa có HĐ mua"), giữ thứ tự BE đã sắp
- [x] Excel không cần đụng — dùng chung `displayRows`

## Checkpoint — 2026-09-08

**Vừa hoàn thành:** Toàn bộ. BE sắp xếp mặc định, FE sạch checkbox.

**Verify trên DB thật `thanhan_stag_07052026` (14 dòng báo cáo) — 5/5 PASS:**
1. Thứ tự giảm dần, mới nhất lên đầu — PASS
2. Đối chiếu `pushed_at` với `MAX(COALESCE(approved_at, created_at))` từng mã — **0 sai**
3. 0 dòng thiếu mốc thời gian
4. Chạy lại 3 lần ra **cùng một thứ tự** (chứng minh tie-break xử đúng chỗ usort không stable)
5. Lọc `type=1` (11 dòng) vẫn giảm dần — bộ lọc không phá thứ tự

Kết quả: `HC-HH-020/021/022` (2026-08-26 09:25:38) lên đầu → `HC-SH-003`, `HC-HH-024`
(2026-07-13 15:16:36) xuống cuối. Trước đây `VT-XN-001` đứng #1 nay xuống #6 vì mốc thật của nó
là 2026-08-01 10:29:40 (mã này nằm ở nhiều PXL, lấy MAX).

Lint: `php -l` sạch · `node --check` sạch · `vue-template-compiler` 0 error.

**Bước tiếp theo:** @khoipv build lại client + hard refresh, mở màn xem thứ tự bằng mắt.

**Blocked:** Chưa test trình duyệt thật — session không có tài khoản đăng nhập.
