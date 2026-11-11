# Hỗ trợ: không xem được preview HĐĐT Mắt Bão — timeout tải PDF (không có số Redmine) — @cuong61n

Yêu cầu từ hỗ trợ, 11/11/2026 13:54: GPP `sphthienkim6258` (HKD Nhà thuốc Tây Thiên Kim, MST 074188000702) bấm
xem preview hoá đơn ĐT Mắt Bão ở màn Danh sách hoá đơn bán hàng thì báo "Không lấy được PDF preview Mắt Bão.
Vui lòng kiểm tra laravel.log".

## Task

- [x] (11/11/2026) Điều tra trên prod GPP
  - Nghiệp vụ: lỗi tạm thời bên Mắt Bão — server render PDF phản hồi quá chậm lúc 13:43–13:47. Cấu hình mẫu số/ký hiệu
    của cơ sở đúng (tạo nháp thành công). Khách bấm lại sau ít phút là xem được, không cần sửa dữ liệu.
  - Kỹ thuật: api-02 có 3 dòng `Mắt Bão preview: Lỗi download PDF` (13:43:40, 13:44:16, 13:47:43), cùng MST,
    `cURL error 28` sau 30s. `MatBaoEInvoiceService.php:920` đặt timeout tải PDF = 30s. Thử lại link PDF từ api-02
    lúc ~14:08: HTTP 200, 338 KB, ~6,6s → Mắt Bão hết chậm. Khác vụ 23/10 (error 308 mẫu số ký hiệu).
  - Đã kiểm: laravel.log 2 server API, curl tải PDF từ server. Không sửa code/dữ liệu.
  - Trạng thái: đã trả lời, chờ khách thử lại. Gợi ý (chưa làm): tăng timeout tải PDF/retry 1 lần, trả lỗi rõ cho FE.
