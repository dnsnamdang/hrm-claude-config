# #10791 — Cảnh báo đơn giá thay đổi khi sửa báo giá

Chi tiết điều tra + test: xem `plan.md` cùng thư mục.

## Quyết định đã chốt

### Chữ 2 nút trên popup cảnh báo — "Đồng ý" / "Từ chối" (chốt 2026-09-17)

| | |
|---|---|
| Spec (Redmine #10791, AC4/AC5) | gọi tên nút nguyên văn **"Đồng ý"** và **"Từ chối"** |
| Skill `button-convention` | nút xác nhận trong modal là **"Xác nhận"**; **"Đồng ý"** nằm trong cột *KHÔNG dùng* |
| Đã làm trước đó | "Cập nhật giá" / "Giữ giá cũ" |
| **Chốt** | **theo spec** — user quyết, vì QA nghiệm thu đúng từng chữ ở AC4/AC5 |

Đây là **ngoại lệ có chủ đích** so với bảng text chuẩn, chỉ áp cho popup này. Popup xác nhận khác
vẫn dùng "Xác nhận" / "Hủy" — đừng lấy chỗ này làm tiền lệ.

Chỗ sửa: `pages/assign/quotations/_id/edit.vue` — `textAccept` / `textClose` trong `$confirm()` của
`repriceErpRows`, có comment trỏ ngược về quyết định này.
