# Plan — HDSD màn Phiếu nhập hàng (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Phiếu nhập hàng (PNH), làm tương tự HDSD Phiếu nhập kho / Đề nghị nhập kho.

## Trạng thái: HOÀN THÀNH

- [x] Bước 1 — Khảo sát source (controller/model/views/routes/permissions) qua 3 agent song song (BE/Model/FE); report trả inline (agent read-only).
- [x] Bước 4 — Dựng generator `gen_hdsd_pnh_erp.py` (mirror generator PNK, dùng `finish_macos`).
- [x] Chạy generator → `ERP/HDSD_luongchinh/HDSD_PhieuNhapHang.docx`
      (12 Heading 1, 19 bảng, purge 7 media mồ côi, không sót tiêu đề khung).
- [x] Ghi `design.md` + `plan.md`.

## Không làm (theo chốt của user, giống YCXH/YCNH/DNXK/PXK/PXH/DNNK/PNK)
- Bước 2 (chụp ảnh thật) & Bước 3 (đi sâu form bằng Playwright): BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-nhap-hang/gen_hdsd_pnh_erp.py
```
