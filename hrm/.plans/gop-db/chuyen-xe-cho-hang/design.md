# Chuyến xe chở hàng — Tóm tắt

**Người phụ trách:** @junfoke — 2026-10-31
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-10-31-chuyen-xe-cho-hang-design.md` · **Plan:** `plan.md`

## Mục tiêu

Chạy trọn luồng **Chuyến xe chở hàng** trên HRM (phân hệ Vận chuyển), người dùng không phải sang ERP — trừ phiếu hạch
toán chuyến xe (giữ ERP, nút Hạch toán mở tab ERP).

## Phạm vi (user chốt 31/10/2026)

- **A.** Màn Chuyến xe chở hàng: danh sách (+ lối vào "chờ hạch toán"), popup Tạo / Sửa, Duyệt xe xuất phát → Kết thúc →
  Không duyệt (kế toán, có lý do) → Kết thúc lại, chi tiết, In / Excel, Lịch sử. Form duyệt 3 kiểu: Xe Tân Phát · Xe ngoài ·
  Gửi hàng.
- **B.** Phiếu xuất kho HRM gắn chuyến (Hình thức vận chuyển = Công ty vận chuyển: chuyến, tuyến, km chốt, ghi chú) + popup
  tạo nhanh chuyến ở form PXK và PNK. Logic chuyến của PNK tách ra service dùng chung.
- Không làm: phiếu hạch toán, tab Bốc xếp của PXK, chọn chuyến ở bước lấy hàng.

## Quyết định chính

1. **Giữ nguyên cách tính ERP** — "chỉ chuyển đổi nền tảng": đi 2 chiều không ×2 cước; Chuyến xe khác cũng đưa về như ERP.
2. Chỉ khác ERP ở cách hiện: vượt trần báo đỏ; chia cước dòng cuối nhận phần lẻ.
3. BE chặn đúng điều kiện nút ERP (403 / 409); lối "chờ hạch toán" gate quyền **Hạch toán chuyến xe chở hàng** (ERP gate quyền
   không tồn tại).
4. Sửa lỗi hiển thị / crash của ERP (in, Excel, link phiếu nhập, thiếu bảng giá) — spec mục 7.
