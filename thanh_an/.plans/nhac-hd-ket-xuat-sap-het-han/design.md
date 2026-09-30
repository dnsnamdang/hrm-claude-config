# Thông báo HĐ đã kết xuất sang cung ứng sắp hết hạn — Tóm tắt thiết kế

@khoipv — 24/09/2026

Spec đầy đủ: [docs/superpowers/specs/2026-09-24-nhac-hd-ket-xuat-sap-het-han-design.md](../../docs/superpowers/specs/2026-09-24-nhac-hd-ket-xuat-sap-het-han-design.md)

## Mục tiêu

Nhắc nhân sự phòng Cung ứng khi hợp đồng **đã kết xuất sang cung ứng** sắp hết hạn mà
**chưa đề xuất đủ hàng**, chia người nhận **theo địa bàn khách hàng**.

## Scope

| File | Loại |
|---|---|
| `app/Console/Commands/NotifySupplyContractExpiration.php` | Mới |
| `app/Console/Kernel.php` | +1 dòng lên lịch |

Không migration · không sửa FE · không đụng hàm dùng chung.

## Quyết định lớn

1. **Ánh xạ địa bàn → phòng là hằng trong code:** `1 (Miền Bắc) => [88]`,
   `3 (Miền Nam) => [103, 106]`. Miền Trung (2) và KH trống địa bàn **cố ý bỏ qua** — hệ thống
   không có phòng Cung ứng Miền Trung.
2. **"Chưa xử lý xong" = chưa đề xuất đủ hàng**, dùng lại nguyên
   `SupplyProposalService::fullyProposedContractIds()`. HĐ đã đề xuất đủ mà phiếu còn đang xử lý
   thì không nhắc.
3. **Người nhận = toàn bộ NV của phòng** (`employee_infos.department_id`, `status ∈ {1, 2}`),
   không lọc theo quyền.
4. **4 mốc nhắc: 30 / 15 / 7 / 1 ngày**, so bằng đúng ngày (không phải `<=`) → mỗi HĐ tối đa
   4 thông báo trong đời.
5. **Giờ gửi 08:30** hằng ngày (`Asia/Ho_Chi_Minh`) — không trùng 2 cron nhắc hạn sẵn có
   (07:00 và 10:00).
6. **Địa bàn lấy sống** từ `category_customers.customer_area_id`, không dùng cột chụp
   `contracts.customer_area_name`.
7. **Phải dùng `sendToAllContractNotification()`** — `sendToAllNotification()` đụng `auth()`
   nên fatal trong console.

## Cảnh báo

- DB dev `thanhan_stag_07052026` còn phòng ban cũ, **không có `103`/`106`** → trên dev chỉ test
  được nhánh Miền Bắc.
- Phát hiện ngoài lề: `quotations:notify-expiration` chưa từng chạy được (sai tên command +
  typo `whewre`). Chưa sửa, chờ user quyết.
