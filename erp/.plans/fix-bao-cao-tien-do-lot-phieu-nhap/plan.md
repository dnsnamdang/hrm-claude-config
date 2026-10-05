# Fix: Báo cáo tiến độ đặt hàng theo nhân viên lọt phiếu YCĐH nháp (Đang tạo)

@junfoke · Repo `TanPhatDev` (bản B) · nhánh `master` · ngày 11/09/2026

## Bối cảnh / Bug

QA báo: phiếu **PDH-07554** hiện trong **Báo cáo tiến độ đặt hàng theo nhân viên**
(`/admin/orders/reports/orderReportProcess`) nhưng tìm không ra ở **Danh sách phiếu YC đặt hàng**
(`/admin/orders/root_order_request?_type=all`), kể cả khi lọc đúng mã phiếu.

## Root cause (đã xác nhận bằng data prod)

`root_order_requests` id=7554, `status = 1` (Đang tạo), `created_by = 28` (Bùi Hữu Hanh),
`approver_id` NULL, tạo 09/09/2026 — tức **phiếu nháp chưa gửi duyệt**.

- **Màn danh sách (đúng)**: `RootOrderRequest::searchByFilter()` dòng 361-365 ẩn phiếu
  `status = DANG_TAO` trừ khi người xem chính là người tạo.
- **Màn báo cáo (sai)**: `OrderReportProcessService::filter()` **không có điều kiện status nào**
  (chỉ lọc khi user tự chọn ô "Trạng thái hàng") ⇒ vơ cả phiếu nháp vào báo cáo, lại render link
  bấm sang được phiếu nháp của người khác.

Không liên quan phân quyền, không phải dữ liệu sai, model không dùng SoftDeletes.

## Quyết định

Loại **duy nhất status = 1 (Đang tạo)** khỏi báo cáo — khớp đúng hành vi màn danh sách.
Phiếu **Hủy (5)** vẫn giữ nguyên như hiện tại (user chốt 11/09/2026).

## Tasks

- [x] BE: `OrderReportProcessService::filter()` — thêm `where(status != RootOrderRequest::DANG_TAO)`
  ngay sau block phân quyền, trước các filter tuỳ chọn. Vì `filter()` được gọi từ
  `getManagementBuy()` (nguồn duy nhất của `getData()`) nên áp cho **cả 3 lối ra**: xem trên web,
  In (`printReportOrderReportProcess`), Xuất Excel + job gửi mail (`getTable4Excel`).
- [x] BE: thêm `use App\Model\Order\RootOrderRequest;` vào đầu service.
- [x] FE: `orders/reports/order_report_process/index.blade.php` dòng 458 — bỏ option **Đang tạo**
  khỏi dropdown "Trạng thái hàng" (`collect(...)->reject(...)->values()`), tránh user chọn một
  trạng thái không bao giờ ra dòng nào.
  ⚠️ Không dùng `array_filter(A, fn)` vì Blade `@json()` tách tham số bằng `explode(',')` → biểu
  thức có dấu phẩy top-level sẽ vỡ khi compile.
- [x] Verify: `php -l` service sạch; biểu thức `collect()->reject()->values()` chạy thử ra JSON
  đúng (mảng liên tục, đã bỏ id=1); `git diff --stat` = 5 dòng, CRLF nguyên vẹn.
- [ ] User verify browser: mở lại báo cáo 01/01/2026–10/09/2026 → PDH-07554 phải biến mất;
  dropdown "Trạng thái hàng" không còn "Đang tạo"; các phiếu trạng thái 2-5 vẫn đủ như cũ.
- [ ] User tự branch + commit + deploy.

## Checkpoint — 11/09/2026

Vừa hoàn thành: sửa 2 file (BE service + blade FE), lint sạch, diff tối thiểu.
Đang làm dở: không.
Bước tiếp theo: user test trên browser rồi tự commit.
Blocked: không.
