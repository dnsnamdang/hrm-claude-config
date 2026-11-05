# Hỗ trợ: nhà thuốc không xuất được HĐĐT Viettel — SIGNATURE_NOT_FOUND (không có số Redmine) — @cuong61n

Yêu cầu từ hỗ trợ (Tuấn Kiệt), 05/11/2026: GPP `tienphong1909` (Nhà thuốc Tiên Phong 68 — Đường Tuệ Tĩnh,
Quảng Ninh) bấm xuất hoá đơn điện tử thì báo `SIGNATURE_NOT_FOUND` + "Không thể tạo hoá đơn điện tử".

## Task

- [x] (05/11/2026) Điều tra trên prod GPP
  - Nghiệp vụ: lỗi nằm ở **phía Viettel SInvoice**, không phải lỗi phần mềm. Tài khoản Viettel của nhà thuốc
    đăng nhập được nhưng Viettel không tìm thấy chữ ký số để ký hoá đơn → cần nhà thuốc liên hệ Viettel
    kiểm tra/gia hạn/đăng ký lại chứng thư số (HSM/SmartCA) và gán cho mẫu 2/001, ký hiệu C26MTP.
  - Kỹ thuật: user 4196 → cơ sở 5386 (MST 022197001729), `einvoice_provider=viettel`, mẫu `2/001`, ký hiệu
    `C26MTP`. Bảng `e_invoice` chỉ có 1 HĐĐT thành công (C26MTP1, có mã CQT, 02/04/2026) → cấu hình
    tài khoản/mẫu/ký hiệu đúng, trước đây ký được. Ngày 04/11/2026 có 11 lần gọi `createInvoice` (api-01: 5,
    api-02: 6), không lần nào tạo được bản ghi. Mã `SIGNATURE_NOT_FOUND` không có trong code SPHACY —
    `EInvoiceService::syncInvoiceToViettel` trả nguyên `description` của Viettel ra FE.
  - Đã kiểm: DB prod (users, drugstores, e_invoice), laravel.log 2 server API. Không gọi thử createInvoice
    lên Viettel để tránh phát hành hoá đơn thật.
  - Trạng thái: đã trả lời hỗ trợ, chờ nhà thuốc làm việc với Viettel. Không sửa code/dữ liệu.
