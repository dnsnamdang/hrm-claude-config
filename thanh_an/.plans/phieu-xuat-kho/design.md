# Design (tóm tắt) — Phiếu xuất kho (bản thật BE + FE)

> @khoipv · 26/11/2026 · Spec đầy đủ: [2026-11-26-phieu-xuat-kho-design.md](../../docs/superpowers/specs/2026-11-26-phieu-xuat-kho-design.md) · Demo: `demos/demo-phieu-xuat-kho.html`

## Mục tiêu
Nối tiếp ĐNXK thật (đang dừng ở **Chờ xuất kho**): thủ kho lập **Phiếu xuất kho** chọn lô / seri (FEFO) → duyệt → trừ tồn thật, ghi thẻ kho, cộng SL đã xuất về ĐNXK (→ Đang xuất kho / Đã xuất kho).

## Phạm vi
- **Có**: danh sách V2, tạo / sửa (chọn ĐNXK trong form, lô → seri, quét seri, thu gọn), chi tiết (Hàng hóa / Thẻ kho / Lịch sử), duyệt, in 02-VT; ĐNXK thêm tab PXK, nút Lập PXK / Mở nháp, **Đóng phần còn lại**.
- **Không**: Gửi bộ phận giao hàng (kho → KH), hàng KH gửi, bỏ duyệt / hủy PXK, giá vốn.

## Quyết định lớn
| | |
|---|---|
| Trạng thái | 1 Nháp (giữ tạm SL lô) → 2 Đã xuất kho (khóa). Tối đa 1 PXK nháp / ĐNXK |
| Ai làm | (đổi 27/11) Lập / sửa: quyền **537 Quản lý phiếu xuất kho** (mọi kho, không cần thủ kho). Duyệt: quyền **538 Duyệt phiếu xuất kho**. Xóa: Nháp + 537 + người lập. Đóng phần còn lại ĐNXK: 537 |
| Phân quyền xem | 3 cấp như ĐNXK (quyền seeder id 534–536); (27/11) bỏ "thủ kho luôn thấy phiếu kho mình" |
| ĐVT (PA 1) | SL lô nhập theo **ĐVT cơ bản**, cho 3 số lẻ (lô có seri bắt số nguyên); BE ÷ hệ số → `exported_qty` dòng ĐNXK (chia theo id tăng dần) |
| Lô được chọn | Cùng kho + hàng; tồn chung hoặc giữ cho đúng HĐ của ĐNXK; **phải dùng hết lô giữ HĐ trước tồn chung**; hết hạn hiện nhưng khóa; FEFO |
| Seri | **1 seri = 1 ĐVT cơ bản**; seri chọn ≤ SL lô; phần không seri ≤ số không seri còn của lô. PNK sửa: số seri ≤ SL × hệ số |
| HĐ | Duyệt PXK **cộng dồn** `contract_products.exported_qty` (quy ĐVT, hàng gốc nếu đổi hàng); import Excel SL đã xuất bị chặn khi HĐ đã có PXK |
| Người nhận / SĐT | Theo đúng rule ĐNXK |
| Ngày xuất | ≥ ngày tạo ĐNXK, ≤ hôm nay; thẻ kho ghi theo ngày xuất |
| Duyệt | 1 transaction, lockForUpdate tồn / seri / ĐNXK, kiểm lại toàn bộ; ghi `stock_ledgers` doc_type `PXK`, seri status 2 |

## Bảng mới
`warehouse_exports`, `warehouse_export_items`, `warehouse_export_lots`, `warehouse_export_serials`, `warehouse_export_logs` (chỉ index). Thêm cột đóng phần còn lại vào `warehouse_export_requests`, cột `warehouse_exports` vào `column_customizations`.

## Ảnh hưởng
ĐNXK (cờ mới, tab, Đóng phần còn lại, chặn Thu hồi / Trả lại khi có PXK nháp). SL thực hiện / còn lại HĐ (màn HĐ, đề xuất cung ứng) đổi theo `exported_qty`. Sửa dùng chung: rule seri PNK, import Payroll SL đã xuất. Báo cáo tồn không sửa.
