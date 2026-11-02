# Đồng bộ khổ giấy: soạn mẫu in = xem trước = bản in — @junfoke

Repo `TanPhatDev`, nhánh `gop_db`. Khởi nguồn: KD báo 2 HĐ bán 30518, 30563 (`firm-contracts/{id}/print`) in ra khối chữ ký
"ĐẠI DIỆN BÊN BÁN" rớt dòng, trong DM mẫu in nhìn không lỗi.

## Nguyên nhân
1. Khung soạn CKEditor rộng 210mm (~794px), trang in thật chỉ 168–180mm; mẫu chữ ký dùng 2 ô cố định 438px + 397px + 20 dấu cách.
2. HĐ in từ **bản sao mẫu lưu trong HĐ** (`firm_contracts.template`), không đọc lại DM mẫu in. Bản sao 2 HĐ đã bị sửa: toàn bài 22px
   (mẫu gốc 141 "HĐ mua bán vật tư (Phòng Dầu)" là 16px), thêm nội dung Điều 8.1.

## Khổ chuẩn chung
A4, lề trên 15 / phải 10 / dưới 15 / trái 20mm → vùng chữ 180mm dọc, 267mm ngang. Đổi lề phải sửa cùng lúc
`public/css/print-page.css` và `public/css/yield-css/editor.css`.

## Ngày 02/11/2026 (@junfoke)
- [x] 02/11/2026 — Hỗ trợ check lỗi prod mẫu in HĐ 30518, 30563: gửi SQL (có sao lưu `firm_contracts_bk_sig_20261102`) đổi khối chữ ký sang bảng 100%, 2 ô 50% căn giữa.
- [x] 02/11/2026 — Theo user "đồng bộ mọi màn về 1 tỉ lệ": thêm `print-page.css`; khung soạn mẫu in (59 màn: DM mẫu in, mẫu báo cáo, form HĐ/phụ lục) = 180mm, dùng chung CSS bản in; `print` (217 màn), `print_quota`, `print_landscape` (206 màn, 267mm), `printMulti` (về khổ chuẩn); Ctrl+P trên trang xem trước = nút In; khung soạn có nút "Khổ ngang"; màn sửa mẫu báo cáo xem trước đúng khổ. Đo khớp phần tử trên local (2 HĐ, 2 màn ngang, 12 mẫu). Commit `f28117b631`.
- [x] 02/11/2026 — Theo user: bỏ nét chấm mờ tự thêm cho bảng `no-border` trong khung soạn (dễ tưởng lỗi), tăng version `editor.css` trong `app.directive.js` — `d01b68eed4`.
- [x] 02/11/2026 — Giải thích user: mẫu 141 không lỗi, lỗi chỉ ở bản sao trong 2 HĐ (22px + sửa nội dung) → Điều 7.1 in 4 dòng vs soạn 3 dòng là do so 2 nội dung khác nhau.
- [x] 02/11/2026 — SQL thống kê cỡ chữ HĐ vs mẫu gốc (xác định mẫu 141) + SQL đưa 22px → 16px, giữ dòng "5.1. Phạt vi phạm hợp đồng:" 22px như mẫu (sao lưu `firm_contracts_bk_font_20261102`).
- [x] 02/11/2026 — Fix hộ QA: HĐ 30563 tên "Công ty Con Đường Xanh" (chỗ 20px duy nhất) to hơn Tân Phát → SQL đổi về 16px (sao lưu `firm_contracts_bk_cdx_20261102`), user kiểm trước ra 1 chỗ.
