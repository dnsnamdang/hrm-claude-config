# Popup Tuỳ chỉnh cột — thêm Chọn tất cả / Bỏ chọn hết (giống popup Xuất Excel)

## FE (hrm-client, nhánh gop_db)
- [x] `components/modal/column-customization-modal.vue`: 2 nút Chọn tất cả / Bỏ chọn hết (không đụng cột khoá/bắt buộc), dòng "Đang chọn x/y cột", rộng 720px, lề + icon ☰ xám như export-fields-modal
- [x] Sửa lỗi chữ chạm đường kẻ (bỏ rule `label { top: 10px }` cũ)

## Tài liệu (Drive, 06/10/2026)
- [x] HDSD: 41 file — thay ảnh cửa sổ + chèn bước/câu 2 nút, đẩy theo ID (giữ link)
- [x] SRS: 39 file — thay ảnh + bảng giao diện (+Chọn tất cả, Bỏ chọn hết, Số cột đang chọn) + bảng event
- [x] SRS "Danh mục dịch vụ sửa chữa và chi phí khác" (Google Doc gốc) — sửa trực tiếp qua Playwright, ảnh thay sau khi đăng nhập Google
- [x] SRS_Các quy tắc chung_VN_1.0 mục "Tùy chỉnh cột" — thêm 2 dòng qua Playwright
- [x] `_catalog_docs_lib/hdsd_gon.py`: phần Tùy chỉnh cột sinh thêm Bước 3 Chọn tất cả / Bỏ chọn hết

Script dùng lại: `scripts/` (cap.py chụp popup · edit.py sửa HDSD · srs_edit.py sửa SRS · push.py đẩy theo ID có chặn ModTime)
