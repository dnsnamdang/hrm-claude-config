# Plan — HDSD màn Đề nghị xuất kho (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Đề nghị xuất kho (PDNXK), làm tương tự HDSD Yêu cầu xuất hàng / Yêu cầu nhập hàng.

## Trạng thái: HOÀN THÀNH

- [x] Bước 1 — Khảo sát source (controller/model/views/routes/permissions) qua 3 agent song song → report ở scratchpad.
- [x] Bước 4 — Dựng generator `gen_hdsd_dnxk_erp.py` (mirror generator YCNH, dùng `finish_macos`).
- [x] Chạy generator → `ERP/HDSD_luongchinh/HDSD_DeNghiXuatKho.docx`
      (11 Heading 1, 16 bảng, purge 7 media mồ côi, không sót tiêu đề khung).
- [x] Ghi `design.md` + `plan.md`.

## Không làm (theo chốt của user, giống YCXH/YCNH)
- Bước 2 (chụp ảnh thật) & Bước 3 (đi sâu form bằng Playwright): BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-de-nghi-xuat-kho/gen_hdsd_dnxk_erp.py
```
