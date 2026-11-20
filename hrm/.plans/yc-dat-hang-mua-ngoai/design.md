# YC đặt hàng mua ngoài — port ERP → HRM (phía KD khởi tạo)

Spec đầy đủ: `docs/superpowers/specs/2026-11-20-yc-dat-hang-mua-ngoai-design.md`

## Tóm tắt
- HRM: KD lập / sửa / lưu nháp / gửi duyệt / xoá nháp phiếu (status 3 → 6), ghi thẳng bảng ERP `inland_order_requests*` (DB chung). Danh sách + chi tiết chỉ xem mọi status, link "Mở trên ERP".
- ERP: chặn create/store/edit/update/delete/deleteFile bằng `ProductMovedToHrm`; giữ TP duyệt, Kiểm soát (giá NCC + buyer), buyer lập HĐ, huỷ, duyệt lại giá, báo cáo.

## Quyết định đã chốt (20/11/2026)
1. Ranh giới A — HRM chỉ khâu khởi tạo (3, 6).
2. KD theo dõi mọi phiếu trên HRM (cách 1), sau gửi chỉ xem + link ERP.
3. Giá NCC hiện trên HRM khi status 1/4/5.
4. Port gốc (API + Nuxt, logic 1:1 ERP), không gọi API ERP.
