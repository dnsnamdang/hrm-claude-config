# HDSD màn "Báo cáo hạn mức công nợ nhân viên" (ERP, nhánh gop_db)

- **Output:** `HDSD_BaoCaoHanMucCongNoNhanVien.docx` (10 trang).
- **Generator:** `gen_hdsd.py` — khuôn chi tiết `HdsdBuilder`, bám file mẫu `HDSD_YeuCauXuatHang.docx` (user chỉ định 15/10/2026).
- Không chèn ảnh → các ô "[Vị trí chèn ảnh] …".
- Hành vi nghi lỗi KHÔNG ghi vào HDSD — xem testcase `../bao-cao-han-muc-cong-no-nhan-vien/`.

Dựng lại (Windows, cần Word): `python gen_hdsd.py`
