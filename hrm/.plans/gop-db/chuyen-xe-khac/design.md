# Chuyến xe khác — Tóm tắt

**Người phụ trách:** @junfoke — 2026-10-27
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-10-27-chuyen-xe-khac-design.md` · **Plan:** `plan.md`

## Mục tiêu

Chuyển màn **Chuyến xe khác** (ERP Kho › Vận chuyển - Bốc xếp) sang phân hệ **Vận chuyển** của HRM — màn nhập liệu đầu
tiên của nhóm chuyến xe (Chuyến xe chở hàng làm sau vì tạo từ popup trong Phiếu xuất / nhập kho).

## Phạm vi (user chốt 27/10/2026)

- Trọn luồng: danh sách (+ lối vào "chờ duyệt", "chờ hạch toán"), Thêm / Sửa / Chi tiết (3 kiểu: Gửi hàng · Tuyến cố
  định · Tuyến không có sẵn, khối Chi tiết phân bổ cước theo nhân viên + phiếu xuất/nhập kho), Duyệt xe xuất phát →
  Kết thúc chuyến xe → Duyệt / Không duyệt, Không duyệt của kế toán, Xoá, In phiếu / In danh sách, Xuất Excel.
- **Phiếu hạch toán chuyến xe khác giữ ở ERP** (nút Hạch toán mở ERP tab mới). Duyệt KHÔNG sinh bút toán.

## Quyết định chính

1. BE chặn đúng điều kiện hiện nút của ERP (ERP chỉ ẩn nút, API để ngỏ).
2. Sửa các lỗi hiển thị / dữ liệu của ERP (BSX hiện id, Ngày duyệt sai cột, thiếu trạng thái Chờ duyệt, xoá bỏ sót dòng
   con, so tổng cước số thực, mẫu in sai ô, in danh sách nhầm mẫu…) — không đổi công thức cước.
3. Trần cước khi đi 2 chiều = cước công thức ×2 + vượt trội; nhập vượt thì báo đỏ (ERP tự cắt về 1 chiều).
4. Quyền tên y ERP, kiểm bằng trait `ChecksEmployeePermission`: Thủ kho (vào màn), Xem chuyến xe theo tổng công ty /
   công ty / phòng ban, Duyệt chuyến xe khác, Hạch toán chuyến xe khác, Hạch toán vận chuyển (người nhận thông báo).
5. Khuôn HRM: Phiếu yêu cầu vận chuyển (`pages/finance/delivery-requests`) + Phiếu nhập kho điều chỉnh kiểm kê.
