# Danh sách cần hạch toán chi phí vận chuyển nhanh — Tóm tắt

**Người phụ trách:** @junfoke — 2026-11-02
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-02-hach-toan-cpvc-nhanh-design.md` · **Plan:** `plan.md`

## Mục tiêu

Kế toán lọc các khoản chi phí giao nhanh (KH chịu, trên HĐ mua) đã nhập kho, tick rồi Tạo phiếu kế toán (Nợ 35241 / Có 811)
ngay trên HRM — không sang ERP.

## Phạm vi (user chốt 02/11/2026)

- Màn danh sách Tài chính › Nhập hàng (lọc, phạm vi 4 cấp, tick + Tạo phiếu kế toán, Xuất Excel, nhận `?status=0`).
- Sửa nguồn giao nhanh của phiếu kế toán cho giống ERP: loại tiền theo HĐ mua (21/22 dòng thật là ngoại tệ), nhân viên chịu
  phí, popup hợp đồng chỉ HĐ bán của NV đó.
- Không làm: cập nhật trạng thái/diễn giải từng dòng (ERP không có nút), số đếm dashboard, màn HĐ mua.

## Quyết định chính

1. Giữ truy vấn / gom nhóm ERP; chỉ sửa: Đến ngày lọc hết ngày, khử trùng hàng hoá khi nhiều phiếu nhập.
2. Hủy phiếu KT không gỡ dòng giao nhanh (giữ như hiện tại).
3. BE chặn khi tạo phiếu: 403 thiếu quyền "Hạch toán chi phí vận chuyển nhanh", 409 dòng đã hạch toán.
4. 1 mục menu duy nhất.
