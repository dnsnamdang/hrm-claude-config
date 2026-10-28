# HDSD màn "Khai báo hạn mức công nợ khách hàng" (ERP, nhánh gop_db)

- **Output:** `HDSD_KhaiBaoHanMucCongNoKhachHang.docx` (12 trang).
- **Generator:** `gen_hdsd.py` — khuôn chi tiết `HdsdBuilder`, bám file mẫu `HDSD_YeuCauXuatHang.docx` (user chỉ định 15/10/2026).
- Không chèn ảnh → các ô "[Vị trí chèn ảnh] …".
- Hành vi nghi lỗi KHÔNG ghi vào HDSD — xem testcase `../khai-bao-han-muc-cong-no-kh/`.

Dựng lại (Windows, cần Word): `python gen_hdsd.py`
