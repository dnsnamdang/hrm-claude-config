# Thư mục Demo (prototype HTML)

> Gom toàn bộ file demo/prototype HTML standalone của dự án. Mỗi file mở trực tiếp bằng trình duyệt (không cần server), dùng để chốt UX/nghiệp vụ trước khi build thật.

## Danh sách file

| File | Mô tả | Spec liên quan |
|------|-------|----------------|
| `demo-tao-de-xuat-cung-ung-hang-hoa.html` | Tạo đề xuất cung ứng hàng hóa — 2 loại (Theo khách hàng · Theo nội bộ), wizard 2 bước, popup chọn hàng (bảng + chọn-all), phân biệt Trong/Ngoài HĐ, cảnh báo vượt SL theo HĐ (không chặn), đính kèm File lưu trữ. | `docs/superpowers/specs/2026-06-25-purchase-proposal-demo-design.md` |
| `demo-bc-vong-doi-du-toan-hop-dong.html` | Báo cáo vòng đời Dự toán → Hợp đồng. (Chuyển về từ `hrm-thanhan-client/pages/sale/report-project-contract/`) | — |
| `demo-xuat-excel-gia-hang-hoa.html` | Chọn trường + loại giá khi xuất Excel màn Quản lý giá hàng hóa | — |
| `demo-lap-hop-dong-mua.html` | Lập hợp đồng mua với NCC (đảo vai Bên Mua/Bên Bán), 2 loại HĐ Nguyên tắc/Thương mại (ẩn-hiện cột SL/Thành tiền + tổng giá trị), hàng hóa chia nhóm, điều khoản rich-text điền sẵn, 5 tab như form HĐ bán. | `docs/superpowers/specs/2026-07-13-lap-hop-dong-mua-design.md` |
| `demo-tao-don-mua-hang.html` | Tạo mới Đơn mua hàng (phân hệ Cung ứng) — mô hình giống HĐ mua nhưng không phải hợp đồng: 1 form duy nhất, 2 tab TT chung (NCC + dư nợ theo công ty) / Hàng hóa; 1 popup Chọn hàng hóa hợp nhất có lọc Nguồn (Theo phiếu đề xuất: 1 dòng = 1 phiếu PDNMH × 1 mã · Không theo phiếu: hàng danh mục); bảng 1 mã gộp nhiều phiếu (input SL mua từng phiếu, SL đề xuất Σ, SL mua 2 chiều, cảnh báo đỏ/vàng không chặn), dòng danh mục hiện "Mua ngoài phiếu đề xuất", "Cung ứng nội bộ" khi không có KH, cột Ghi chú nhập tay, đơn giá có VAT + cột %VAT, khối tổng Thành tiền trước VAT / VAT / Thành tiền sau VAT realtime (như màn contract/contract/add). | `docs/superpowers/specs/2026-07-23-demo-don-mua-hang-design.md` |

## Quy ước

- Đặt tên: `demo-<ten-man-hinh>.html` (tiếng Việt không dấu, gạch ngang).
- Mọi file demo mới của dự án để trong thư mục này.
