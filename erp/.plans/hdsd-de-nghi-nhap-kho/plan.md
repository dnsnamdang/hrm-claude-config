# Plan — HDSD màn Đề nghị nhập kho (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Đề nghị nhập kho (PDNNK), làm tương tự HDSD Yêu cầu nhập hàng / Phiếu xuất hàng.

## Trạng thái: HOÀN THÀNH

- [x] Bước 1 — Khảo sát source (controller/model/views/routes/permissions) qua 3 agent song song (BE/Model/FE) → report ở scratchpad.
- [x] Bước 4 — Dựng generator `gen_hdsd_dnnk_erp.py` (mirror generator PXH, dùng `finish_macos`).
- [x] Chạy generator → `ERP/HDSD_luongchinh/HDSD_DeNghiNhapKho.docx`
      (10 Heading 1, 19 bảng, purge 7 media mồ côi, không sót tiêu đề khung).
- [x] Ghi `design.md` + `plan.md`.

## Không làm (theo chốt của user, giống YCXH/YCNH/DNXK/PXK/PXH)
- Bước 2 (chụp ảnh thật) & Bước 3 (đi sâu form bằng Playwright): BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-de-nghi-nhap-kho/gen_hdsd_dnnk_erp.py
```
