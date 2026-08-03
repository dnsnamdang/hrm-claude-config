# Design tóm tắt — Demo "Tạo đề xuất cung ứng hàng hóa"

> Phụ trách: @khoipv · Ngày: 2026-06-25 · Loại: **prototype HTML standalone**
> Spec đầy đủ: `docs/superpowers/specs/2026-06-25-purchase-proposal-demo-design.md`

## Mục tiêu
Dựng file demo HTML (1 file, hardcode data) cho màn **Tạo đề xuất cung ứng hàng hóa** với **2 loại**, theo ngôn ngữ thiết kế của `bbnt_demo (2).html`. Chốt UX trước khi build thật.

## 2 loại đề xuất
| Loại | Nguồn hàng | Field thêm | Cấp duyệt |
|------|-----------|-----------|-----------|
| 1. Cung ứng theo khách hàng | Hàng trong HĐ (mọi HĐ đã duyệt của KH) + hàng ngoài HĐ (danh mục) | chọn Khách hàng → popup chọn hàng, phân biệt Trong/Ngoài HĐ | BGĐ duyệt |
| 2. Cung ứng theo nội bộ | Danh mục hàng hóa | Lý do mua (bắt buộc) | Phải xét duyệt |

## Quyết định lớn (brainstorming)
1. **Không nhập giá** → bỏ cột đơn giá/thành tiền; footer theo số mặt hàng + tổng SL.
2. **Không chọn NCC** ở bước đề xuất.
3. **L2** bắt buộc Lý do mua; **L3** thêm thông tin nhập khẩu.
4. **L1** cảnh báo khi SL đề xuất vượt SL còn lại (không chặn lưu).

## Bố cục 3 bước
1. **Chọn loại (select) + thông tin chung + thông tin theo loại** (config strip gộp chung trong Bước 1, đổi theo loại).
2. Bảng chi tiết hàng hóa + footer.
3. **File lưu trữ** (đính kèm tài liệu, theo pattern màn nghiệm thu) + nút Lưu đề xuất.

## Đầu ra
`demos/demo-tao-de-xuat-cung-ung-hang-hoa.html` (thư mục `demos/` gom toàn bộ file demo của dự án).
