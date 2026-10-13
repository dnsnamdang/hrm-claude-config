# Plan — HDSD màn Yêu cầu nhập hàng (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Yêu cầu nhập hàng, làm tương tự HDSD Yêu cầu xuất hàng.

## Trạng thái: HOÀN THÀNH

- [x] Bước 1 — Khảo sát source (controller/model/views/routes/permissions/menu) qua các agent song song.
- [x] Bước 4 — Dựng generator `gen_hdsd_ycnh_erp.py` (mirror generator YCXH, dùng `finish_macos`).
- [x] Chạy generator → `ERP/HDSD_luongchinh/HDSD_YeuCauNhapHang.docx`
      (11 Heading 1, 17 bảng, không sót tiêu đề khung, purge media OK).
- [x] Ghi `design.md` + `plan.md`.

## Không làm (theo chốt của user)
- Bước 2 (chụp ảnh thật) & Bước 3 (đi sâu form bằng Playwright): BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-yeu-cau-nhap-hang/gen_hdsd_ycnh_erp.py
```
