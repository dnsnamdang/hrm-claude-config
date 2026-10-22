# Cập nhật danh mục 4 cấp cho hàng ETEK GREEN — 21/10/2026

Nguồn: `nguon-UPDATE-hang-green.xlsx` (bản chép file user gửi 21/10 "Copy of UPDATE hàng green.xlsx", sheet Thành phẩm, 855 dòng).
Đối chiếu trên `hrm_erp_21_10` = dump prod `hrm_erp_gop` 21/10 20:25 (app prod đang down).

| File | Nội dung |
|---|---|
| `tong-ket-danh-muc-green-2110.xlsx` | Tổng kết: luật · danh mục mới · hàng gán Loại · lệch cây so với file · dòng bỏ qua · mã giữ nguyên |
| `danh_muc_green_2110.sql` | Chạy thẳng bằng MySQL client — chốt chặn @ok, chạy lại = 0 dòng, khối LUI cuối file |
| `sinh/` | Script sinh (export TSV từ DB → `resolve2.py` → `sinh_sql.py` / `sinh_xlsx.py`) |

## Luật đã chốt với user 21/10 (câu 1–8)
1. So tên coi `,` và `-` là một; danh mục mới đặt tên kiểu gạch ngang.
2. Loại SP đã có trên DB ⇒ lấy 4 cấp đang có trên DB (user đổi từ "bỏ qua 86 dòng" sang luật này). Nhóm SP/Nhóm CN đã có ⇒ dùng cha DB.
3. Bỏ qua: model chưa có (16) · Loại = "0" (5) · danh mục MỚI file đặt dưới >1 cha (22 dòng: Mặt bích, Ống ruột gà, Kẹp đỡ ống, Bình - Bồn - Bể).
4. Mã đã có Loại ⇒ giữ (8). Gán cả mã đã xoá status 0 (20).
5. Loại mới: tồn lâu 180, VAT/mẫu tem trống, không serial, không thuộc tính; người tạo 13 DNS Admin.
6. Lịch sử "create" ở catalog_histories cho danh mục mới; gán Loại cho hàng không ghi lịch sử hàng hoá.

## Số (bản sao prod 21/10)
Tạo 17 Nhóm SP (NSP.0283–0299) + 95 Loại SP (LSP.0969–1063); không tạo Tính chất/Nhóm CN. Gán Loại 827 mã (620 Loại có sẵn · 207 Loại mới; 20 mã đã xoá); 127 mã cây lệch so với file.

## Trạng thái
- 21/10 22:xx: chạy thử trên local `hrm_erp_21_10` (user cho phép): lần 1 khớp mọi số · lần 2 = 0 dòng · LUI về đúng từng số (ck CRC32 products khớp) · chạy lại lần cuối ⇒ local ĐÃ cập nhật (bảng zz_green2110_* còn trên local).
- 22/10 ~00:05: ĐÃ CHẠY TRÊN PROD `hrm_erp_gop` (user chạy, VPS): ok=1 · gán 827 · lệch 0/0/0 · 299 · 1063 · 112 — khớp local. (Bỏ phương án ghi đè cả DB: prod có chấm công/đăng ký cơm ghi sau 20:25.) Sau nghiệm thu DROP 4 bảng zz_green2110_*.
- Chia sẻ hàng ETEK GREEN + DTTDETEK nhận hàng: ĐÃ CHẠY PROD 22/10 05:xx — xem `../../gia-theo-cong-ty/chia-se-green-2110.md`.
