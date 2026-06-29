# Thanh lý hợp đồng — Design (tóm tắt)

**Phụ trách:** @khoipv
**Ngày:** 2026-06-22
**Trạng thái:** Prototype HTML (chưa nối BE)

## Mục tiêu
Dựng **prototype HTML tĩnh** cho màn **Biên bản thanh lý hợp đồng** — tổng hợp lại toàn bộ
các biên bản nghiệm thu (BBNT) đã có của 1 hợp đồng + đối chiếu thanh toán. Dùng lại ngôn ngữ
thị giác và tập dữ liệu mẫu của `bbnt_demo (2).html`.

## Quyết định lớn (chốt khi brainstorming 2026-06-22)
| Vấn đề | Quyết định |
|---|---|
| Bản chất | Chỉ **prototype HTML/UI** (giống bbnt_demo), chưa nối BE/DB |
| 3 bảng TẬP 1/2/3 | Trình bày dạng **tab** chuyển qua lại |
| Nhập tay | **Có** ô nhập: Giá trị thanh toán (TẬP 1), Ngày thanh lý, Kết luận. Phần còn lại read-only tự gom |
| Chữ ký | **Không** có khối chữ ký |
| Dữ liệu | Dùng lại `DATA` (HD001–HD005) của demo BBNT để số khớp nhau |

## Bố cục
1. Header thương hiệu "Biên bản thanh lý hợp đồng"
2. Bước 1: chọn KH → HĐ (selector cascade)
3. Tóm tắt HĐ + KPI (giá trị HĐ / đã NT lũy kế / còn lại / tiến độ %)
4. Danh sách lần nghiệm thu (BBNT): Lần · Loại · Ngày · Giá trị + dòng tổng %
5. Cấu hình thanh lý: Số BB (auto) · Ngày thanh lý (nhập) · Căn cứ
6. 3 tab:
   - TẬP 1 — Tổng hợp hóa đơn (Giá trị thanh toán nhập tay → Còn chưa TT auto)
   - TẬP 2 — Chi tiết từng hóa đơn (block read-only + cộng theo HĐ)
   - TẬP 3 — Tổng hợp hàng hóa (SL HĐ vs Số thực hiện + chênh lệch, gom nhóm theo Phần)
7. Kết luận + banner đối chiếu (đã TT đủ? / đã NT đủ?)
8. Actions: Lưu · Tải Excel · In (ghost, chưa nối)

## Nhất quán số liệu
Phân bổ `slNt` (lũy kế đã NT) của từng mặt hàng vào các hóa đơn → TẬP 2 subtotal = Giá trị thực hiện
TẬP 1 = tổng = "đã NT lũy kế" ở KPI. TẬP 3 Số thực hiện = `slNt`.

## Spec chi tiết
`docs/superpowers/specs/2026-06-22-contract-liquidation-demo-design.md`
