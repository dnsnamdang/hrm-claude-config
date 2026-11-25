# Design (tóm tắt) — Phiếu đề nghị xuất kho (bản thật)

> @khoipv · 25/11/2026 · Spec chi tiết: [2026-11-25-phieu-de-nghi-xuat-kho-design.md](../../docs/superpowers/specs/2026-11-25-phieu-de-nghi-xuat-kho-design.md)
> Demo: `demos/demo-phieu-de-nghi-xuat-kho.html`

## Mục tiêu
Người có quyền lập ĐNXK từ HĐ bán (chỉ loại Xuất bán), chọn hàng theo ô Xuất bán của PXL đã duyệt, gửi kho; thủ kho tiếp nhận (đợt này chỉ Trả lại). Xuất kho / trừ tồn làm ở màn PXK riêng đợt sau.

## Quyết định lớn
- Dừng ở Chờ xuất kho; luồng Nháp → Chờ xuất kho → Bị trả lại → gửi lại; người lập Thu hồi được khi Chờ xuất kho.
- Quyền mới: `Quản lý phiếu đề nghị xuất kho` + 3 quyền xem danh sách theo tổng cty / cty / nhóm nghiệp vụ; thủ kho thấy phiếu đã gửi tới kho mình.
- Xóa: người lập + Nháp / Bị trả lại; bỏ nút Hủy.
- Chọn HĐ: Đã duyệt (3) / Đã kết xuất (9) + Ngày KT ≥ hôm nay.
- SL còn lại HĐ = (Tồn kho→Xuất bán + Mua thêm→Xuất bán − phần NCC giao thẳng KH) − đã đề nghị phiếu khác; vượt → chặn cả nháp.
- Tồn xuất được = giữ cho HĐ + tồn chung − chờ xuất phiếu khác (quy ĐVT cơ bản); vượt → chỉ nháp.
- Lưu theo dòng PXL, FE gộp theo (hàng, ĐVT, giá); hàng đổi tách dòng, SL hàng gốc cho sửa.

## Bảng mới
`warehouse_export_requests`, `warehouse_export_request_products`, `warehouse_export_request_logs` (không khóa ngoại).
