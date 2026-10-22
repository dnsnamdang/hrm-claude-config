# Gói dữ liệu go-live 20/10/2026 — cây phân loại + bỏ Nhóm hàng hoá (phần DỮ LIỆU)

Chuẩn bị 20/10 15:50–16:30. Chạy trong cửa sổ go-live, **SAU** runbook chính (`../../deploy-dev-server.md` Lối B /
`../../gia-theo-cong-ty/runbook-trien-khai.md`: sao lưu → code → migration → quyền). Chưa chạy gì lên prod.

## Thứ tự (cập nhật 20/10 17:30 — user: cả 3 bước chạy bằng SQL, không import Excel)
Chạy bằng MySQL client / tool DB trên DB prod, **SAU** migration + quyền + backfill giá theo công ty. Mỗi file tự in số kiểm; lệch xa ⇒ DỪNG.
| # | File | Việc | Số kỳ vọng (bản sao giacty) | Thời gian |
|---|---|---|---|---|
| D1 | `cay-4-cap/cay_4_cap_2010.sql` | Cây phân loại 4 cấp + lịch sử; TCHH.0005 "Là phụ tùng ô tô" | K0 = 0·0·0·0 · tạo 6/48/282/968 · K1 rỗng · K2 = 0·0·0·0 | 0,2 giây |
| D2 | xoá dòng rác Tính chất nếu K0 in ra (vd `TCHH.GJGH`) — trên màn Tính chất | — | — | — |
| D3 | `golive_bo_nhom_2010.sql` | Gán Loại (a+b), VAT, tồn lâu 180, thuộc tính | xem bảng D3 dưới | 1,6 giây |
| D4 | — | Gửi `ds-hang-vat-trong.xlsx` cho nghiệp vụ | 17 hàng | — |
| D5 | `catalog-dich-vu-o-to/catalog_dich_vu_o_to_2010.sql` | Catalog Dịch vụ ô tô cho công ty 1·2·3·4 | xem bảng D5 dưới | 0,2 giây |
Đã chạy thử **cả chuỗi D1 → D3 → D5** trên DB nháp mô phỏng prod (4 bảng cây rỗng, `products.product_type_id` NULL, bảng khác chép giacty) — ra đúng mọi số; chạy lại từng file lần 2 = 0 dòng; DB nháp đã DROP.
Cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất để 0 như lúc import (runbook B11 — nghiệp vụ tick trên màn nếu cần).
Bản Excel cũ `../import-cay-1710/` giữ làm dự phòng (nhập qua màn Import cho ra đúng cùng mã), KHÔNG chạy cả hai.

### D0. Kiểm trước (prod) — chỉ đọc
```sql
SELECT 'natures' t, COUNT(*) FROM product_natures UNION ALL SELECT 'fgroups', COUNT(*) FROM product_function_groups
UNION ALL SELECT 'families', COUNT(*) FROM product_families UNION ALL SELECT 'types', COUNT(*) FROM product_types;
-- Kỳ vọng ~0 (giacty: 1 dòng rác natures). Có dữ liệu thật ⇒ DỪNG: mã TCHH./NCN./NSP./LSP. và tên có thể trùng (name UNIQUE) ⇒ import báo lỗi.
SELECT code, name FROM product_natures;   -- dòng rác (vd TCHH.GJGH "hjjhjh") ⇒ xoá trên màn sau D1
SELECT COUNT(*) FROM products WHERE product_type_id IS NOT NULL;   -- giacty 0
```

### (Dự phòng — chỉ khi nhập cây bằng Excel thay cho D1) kiểm sau nhập: 6 · 48 · 282 · 968 dòng; `SELECT COUNT(*) FROM product_types WHERE code LIKE 'LSP.%'` = 968.
Import giới hạn 500 dòng/lần ⇒ Loại tách 4a (500) + 4b (468). File 2/3/4 báo "mã cha không tồn tại" nghĩa là chưa nhập cấp cha.

### D3. Số kỳ vọng (đo trên giacty — prod lệch nhẹ là bình thường, lệch xa ⇒ DỪNG)
| Bước | Nội dung | giacty |
|---|---|---|
| B0 | Loại `LSP.%` | 968 (≠ ⇒ DỪNG, D1 chưa đủ) |
| B1 | bảng phụ map_ma / map_nhom; câu "mã Loại không có trên DB" | 9.207 / 309; **rỗng** |
| B2 | gán Loại theo mã hàng file 17/10 | 7.984 dòng (7.980 đang dùng) |
| B3 | gán Loại theo nhóm cũ 1–1 | 7.895 dòng (3.846 đang dùng) |
| | hàng đang dùng có Loại sau | **11.826** / 28.378 |
| B4 | VAT (i) từ thuế suất riêng / (ii) từ nhóm VAT > 0 | 0 / 350; còn NULL đang dùng **17** (nhóm VAT 0 ⇒ danh sách) |
| B5 | `long_stock_days` = 180 cho Loại | 968 |
| B6 | thuộc tính Loại (nhóm 1–1, gộp hợp) | **957** cặp / 234 Loại |
Thời gian chạy trên bản sao: 1,7 giây. Chạy lại lần 2 = 0 dòng đổi (an toàn khi lỡ chạy 2 lần).

### Lui
Cuối file SQL (đang để comment): trả `products.product_type_id / vat_percent / vat_percent_tax_rate_id`, `product_types.long_stock_days`,
xoá `product_type_attributes` mới — đã thử trên bản sao: lệch 0 so với trước. Bảng phụ `zz_golive2010_*` DROP sau nghiệm thu.

## Đã kiểm 20/10
- Sinh: `python3 -I sinh_sql_bo_nhom.py "../nguon/v3-1710/Copy of ERP_final ngày 17-10.xlsx" ../import-cay-1710/0_Bang_tra_cay_4_cap.xlsx <dump tsv> .`
  (file 17/10 user gửi lại 20/10 = cùng MD5 bản `nguon/v3-1710`). Mã Loại tra theo `0_Bang_tra_cay_4_cap.xlsx` (mã do file import sinh ⇒ prod ra đúng mã).
- Chạy thật trên DB nháp `zz_golive2010_thu` (7 bảng chép từ giacty, đã DROP): số khớp mô phỏng; lần 2 = 0; LUI = 0 lệch.

## KHÔNG có trong gói (cần CODE — chưa làm, chưa xin phép)
- **Nhóm máy → Loại** (1.592 liên kết): cần ERP picker lọc Loại OR Nhóm (6 chỗ `Common/SearchController`) + HRM form ô "Dùng cho Loại máy". Chuyển dữ liệu mà chưa có code ⇒ picker ERP mất phụ tùng ⇒ để đợt code.
- ERP đọc tồn lâu theo Loại (5 chỗ), INNER → LEFT JOIN ~30 báo cáo, bỏ dự phòng VAT nhóm (3 chỗ). Dữ liệu B4/B5 chạy trước an toàn: ERP vẫn đọc nhóm như cũ.

## D5. Catalog kinh doanh "Dịch vụ ô tô" (file user gửi 20/10 16:23 — `Danh mục catalouge-DỊch vụ ô tô_final.xlsx`, bản chép trong thư mục)
User 20/10: KHÔNG làm file Excel import ⇒ 1 file SQL chạy thẳng. Công ty gắn: **1 Tân Phát · 2 Hải Phòng · 3 Vinh · 4 Sài Gòn** (user đổi 20/10, trước đó chỉ công ty 1) — mỗi công ty 1 bộ liên kết riêng.
- `@scope_code` = `LVCTKD.0007` (mã "Dịch vụ ô tô" trên giacty). **Prod khác mã ⇒ sửa dòng `SET @scope_code`**; câu C0 phải ra đúng "Dịch vụ ô tô", status 1, `scope_id` không NULL.
- Tìm-hoặc-tạo theo (tên, cha): chương/mục/tiểu mục đã có thì dùng lại; bản ghi mới ghi `catalog_histories` "create" như màn Import. Không đụng 65 chương cũ ERP (không có lĩnh vực).
- Gắn hàng: luật như popup "Xây dựng catalog" (hàng còn dùng, có dòng tại TỪNG công ty, không hàng tạm / ngừng KD, nhánh hoạt động); trùng bỏ qua.

| Kiểm | giacty (bản sao) |
|---|---|
| file | 14 Chương · 77 Mục · 243 Tiểu mục · 822 dòng mã × Tiểu mục (724 mã; 87 mã ở >1 Tiểu mục) |
| tạo mới | 14 / 77 / 243 + 334 dòng lịch sử |
| "đường không ra Tiểu mục hoạt động" | rỗng |
| mã không gắn được (C5) | 27 mã × 4 công ty = 108 dòng, đều "không có mã trên DB / đã xoá" (SGCB-SGGD…, TMV-PC5E4-33001-…, HOSE 6605-B38 39MM …) ⇒ gửi nghiệp vụ |
| gắn | **3.180** liên kết mới = 795 × 4 (cty 1: 21 → 816 · cty 2/3/4: 0 → 795; 697 hàng mỗi công ty) |
| thời gian | 0,2 giây; lần 2 = 0 dòng; LUI (theo mốc id) ⇒ 5 bảng về đúng số trước |
Sinh lại: `python3 -I sinh_catalog.py nguon-catalog-dich-vu-o-to-final.xlsx <mã lĩnh vực> .`
⚠️ Bài học khi thử: `SET NAMES utf8mb4` trần cho biến `@...` collation `utf8mb4_0900_ai_ci` ⇒ lỗi 1267 "Illegal mix of collations" khi so cột `unicode_ci` — 2 file SQL đã đặt `SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci`. Chạy bằng tool khác (DBeaver/Workbench) phải giữ dòng này.

## ⚠️ 20/10 ~20:15 — ĐÃ CHẠY TẬP TRÊN BẢN SAO PROD `hrm_erp_20_10` ⇒ THỨ TỰ + SỐ CHUẨN Ở `../../TRIEN-KHAI-PROD-2010.md` (bước 3.6, 8.x, 9)
Thêm 2 file: `0_kq_tinh_gia_trung_2010.sql` (TRƯỚC migration) · `8_dong_phieu_hoi_cheo_2010.sql` (sau backfill nhóm; `@nguoi_chay` bắt buộc).
Đổi: file cây 4 cấp nay THAY cây cũ prod (có chốt chặn + sao lưu); bỏ 2 cột `declare_*` không còn trên prod; catalog BẮT BUỘC `@nguoi_chay`.
Bảng số giacty ở trên chỉ để tham khảo — số prod: 11.959 hàng có Loại · VAT chép 1.290 · 17 VAT trống · catalog +14 Tiểu mục, 814 liên kết/công ty.
Danh sách gửi nghiệp vụ (từ bản sao prod): `ds-gui-nghiep-vu-prod-2010.xlsx` (thay `ds-hang-vat-trong.xlsx` — bản giacty).
