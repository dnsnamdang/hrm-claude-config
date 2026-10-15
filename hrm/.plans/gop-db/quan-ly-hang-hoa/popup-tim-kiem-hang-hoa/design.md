# Phase 4 — Popup chọn hàng hoá dùng chung ERP + HRM

- Spec: `docs/superpowers/specs/gop-db/2026-10-13-popup-chon-hang-hoa-dung-chung-design.md` (13/10 — chờ user duyệt spec)
- Mockup đã duyệt 13/10: `mockup-popup-tim-hang.html` · Khảo sát: `khao-sat.md`
- Chốt 13/10: phương án A (khuôn popup Xây dựng catalog); mặc định chỉ hàng đã xếp catalog; 1 cột Tồn bán được công ty chứng từ;
  2 cờ trên Tính chất; báo giá DV = phụ tùng của máy + công tắc mở rộng; không lùi `product_type` (quy đổi = chặn go-live);
  cấu hình cột lưu server; ERP thay ruột 2 partial chính (126 include).
- Spec user duyệt 13/10. Plan: `plan.md` (Phần A bản đồ chung + Phần B task chi tiết 4.1–4.2) — chờ user duyệt plan + "Làm". Chưa đụng source.

## Quyết định đã chốt — cấu hình cột (15/10/2026)
- Popup "Cấu hình cột hiển thị" dùng bộ chung `columnCustomizationMixin` + `ColumnCustomizationModal` (`columnScreenKey = 'product_picker'`).
- Cột khoá: **STT · Mã hàng · Tên hàng hoá**. Khoá Tên là NGOẠI LỆ có chủ đích so với chuẩn list-page mục 5 (chỉ khoá STT / Mã / Hành động):
  bấm tên = chọn nhanh 1 hàng, và Tên là cột co giãn duy nhất lấp phần bề rộng còn lại.
- STT vẽ cứng ở template (cạnh ô tick); khai `index` trong `allColumns` chỉ để popup liệt kê đủ bộ cột (`visibleColumns` lọc bỏ).
- Panel cây catalog 280px (đổi từ 330px, 15/10 — cả HRM lẫn ERP).
- Bảng hàng hoá (15/10, N135 → N136): khung bảng gọn popup (table-sm, 3px 6px, thead dính) + màu/viền theo mẫu MISA (header phẳng #d8e7e1, gạch dưới #7cc7ae, nền dòng #fbfbfc, kẻ dọc chấm, hover #e6f5ef, tick #ddf1e9); Tên + cột chữ dài 1 dòng "…" — tên đủ ở đầu popover Đặc điểm, cột chữ dài tooltip đen `v-overflow-tooltip`; **mặc định 20 dòng** (ngoại lệ có chủ đích so với chuẩn popup chọn = 10), lựa chọn 10/20/50/100. Cả HRM + ERP.
