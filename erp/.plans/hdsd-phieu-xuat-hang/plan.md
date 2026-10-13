# Plan — HDSD màn Phiếu xuất hàng (ERP)

**Mục tiêu:** Tài liệu HDSD Word cho màn Phiếu xuất hàng (PXH), làm tương tự HDSD Phiếu xuất kho / Đề nghị xuất kho.

## Trạng thái: HOÀN THÀNH

- [x] Bước 1 — Khảo sát source (controller/model/views/routes/permissions) qua 3 agent song song → report ở scratchpad.
- [x] Bước 4 — Dựng generator `gen_hdsd_pxh_erp.py` (mirror generator PXK, dùng `finish_macos`).
- [x] Chạy generator → `ERP/HDSD_luongchinh/HDSD_PhieuXuatHang.docx`
      (10 Heading 1, 15 bảng, purge 7 media mồ côi, không sót tiêu đề khung).
- [x] Ghi `design.md` + `plan.md`.

## Không làm (theo chốt của user, giống YCXH/YCNH/DNXK/PXK)
- Bước 2 (chụp ảnh thật) & Bước 3 (đi sâu form bằng Playwright): BỎ — dùng box "[Vị trí chèn ảnh]".

## Tái dựng
```bash
/usr/local/bin/python3 ERP/.plans/hdsd-phieu-xuat-hang/gen_hdsd_pxh_erp.py
```
