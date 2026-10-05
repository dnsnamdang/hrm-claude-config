# Design — Cảnh báo & tự động đóng nhu cầu theo Lĩnh vực (Redmine #11377)

> Feature: `demand-expiry-config` · @junfoke · Nhánh `task_11377`
> **Tách từ `task_11386`** (không phải từ `tpe`): #11377 dùng lại trạng thái `DA_DONG` và màn
> Danh sách nhu cầu đã làm ở #11386. Khi merge phải đưa `task_11386` vào trước.
> Liên quan: `.plans/customer-demand-list/` (#11386)

## Mục tiêu

Nhu cầu khách hàng có **thời hạn xử lý**: quá hạn mà chưa lập Dự án TKT thì hệ thống tự đóng, và
báo trước cho người phụ trách M ngày.

## Công thức

```
T   = thời điểm cuộc họp phát sinh nhu cầu chuyển sang "Hoàn thành"
N   = Thời gian hiệu lực nhu cầu (ngày) — khai theo từng Lĩnh vực công ty kinh doanh
M   = Thời gian cảnh báo trước khi đóng (ngày) — tham số CHUNG, mặc định 3

Cảnh báo tại  T + N - M   (chỉ khi N > M)
Tự đóng tại   T + N
```

Phạm vi quét: nhu cầu **Đang theo dõi** và **chưa gắn Dự án TKT**.

## Quyết định (user chốt 14/09/2026)

1. **Nhu cầu ĐANG MỞ áp mốc hạn mới.** Nhu cầu ĐÃ ĐÓNG để nguyên, không mở lại, không tính lại.
2. `N` mặc định **0 = không có thời hạn** cho toàn bộ lĩnh vực đang có. Bật code lên không nhu cầu
   nào bị đóng cho tới khi khách nhập N thật.
3. Trạng thái đích là **"Đóng"** (`DA_DONG`) — tên khách chốt cùng ngày, xem `customer-demand-list/design.md`.

## Đo trên dữ liệu prod thật (`hrm_prod_09_26`, ngày 14/09/2026)

| Kiểm tra | Kết quả |
| --- | --- |
| Nhóm ngành đã trỏ về Lĩnh vực | 35/35 — không cần migration ánh xạ |
| Nhu cầu có `internal_business_scope_id` | 115/115 |
| Nhu cầu đang mở | 99 (95 cái có cuộc họp đã Hoàn thành) |
| Lĩnh vực đang có nhu cầu mở | 4 / 8 (Dịch vụ ô tô 82, Giáo dục đào tạo 8, Công nghiệp 6, Năng lượng và hạ tầng 3) |

**Tác động nếu bật với T = giờ kết thúc cuộc họp, M = 3:**

| N | Đóng ngay | Bắn cảnh báo ngay |
| --- | --- | --- |
| 7 ngày | **25** | 62 |
| ≥ 15 ngày | 0 | 0 |

→ Khuyến nghị khách đặt **N ≥ 15**. Dữ liệu prod rất mới (cuộc họp 04/09 → 12/09/2026).

## Vấn đề lớn nhất và cách xử lý

Hệ thống **không lưu thời điểm cuộc họp chuyển sang Hoàn thành**: `meetings` chỉ có `status` /
`end_date` / `updated_at`, và **không có bảng lịch sử meeting**. Không có T thì không tính được hạn.

Xử lý: thêm cột `meetings.completed_at`, ghi từ nay khi chuyển trạng thái; backfill dữ liệu cũ bằng
`end_date` (giờ kết thúc cuộc họp). KHÔNG dùng `updated_at` — mỗi lần sửa biên bản là nó đổi, hạn
sẽ nhảy lung tung.

## Lệch spec — bám cái nào

| Điểm | Spec #11377 | Chọn |
| --- | --- | --- |
| Nút Tạo Dự án TKT khi nhu cầu đã đóng | "làm mờ kèm tooltip **hoặc** ẩn hoàn toàn" | **Ẩn hẳn** — đúng vế thứ hai spec cho phép và đúng quy ước project |
| Badge "Đã đóng" | "Đã đóng" | **"Đóng"** — tên khách chốt 14/09 |
