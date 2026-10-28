# Nhập cây phân loại + catalog, bỏ Nhóm hàng hoá — ĐỌC TRƯỚC (cập nhật 16/10/2026)

**Trạng thái: TẠM DỪNG theo yêu cầu user (16/10).** Chưa viết code, chưa chạy gì vào DB cho cả 3 việc dưới.

| Việc | File | Đang chờ |
|---|---|---|
| 1. Import cây catalog kinh doanh (Lĩnh vực › Chương › Mục › Tiểu mục) | `khao-sat.md` | user để sau việc 2–3; còn hỏi C2–C5 |
| 2. Nhập cây phân loại 4 cấp (Tính chất › Nhóm CN › Nhóm SP › Loại SP) + gán Loại SP cho hàng | `nhom-hang-sang-loai-sp.md` | nghiệp vụ sửa file theo `can-sua-cay-phan-loai-1610.xlsx` |
| 3. Bỏ Nhóm hàng hoá (`groups`) | `de-xuat-bo-nhom-hang-hoa.md` (đề xuất) + `phu-luc-kiem-ke-nhom-hang.md` (kiểm kê file:line HRM/ERP + số DB) | user trả lời Q1–Q5 (§6 đề xuất) — câu đang hỏi: Q1 bỏ nhóm CÙNG đợt go-live hay đợt riêng (17/10 hỏi lại, đề xuất "Chia 2" — user tạm nghỉ trước khi trả lời) |

## File nguồn (của user, KHÔNG nằm trong repo)
- `/private/var/folders/…/Zalo Temp/TempDownloads/Cây danh mục catalogue.xlsx` — cây catalog (việc 1)
- `~/Desktop/Copy of Quan hệ HH.xlsx` — 1.691 cặp Loại SP ↔ mã nhóm cũ (`groups.id`)
- `~/Desktop/Copy of ERP_final ngày 16-10-le.xlsx` — 33 sheet; dùng: `CâyERP`, `Cấp 1-2/2-3/3-4`, `Mã cấp 1/3/4`, `NewERP Green Power` (9.382 hàng), `Hang_hoa_ma_nhom_cu`
Bản chép 16/10 của cả 3 file: `nguon/` (cạnh README) — đọc bằng bản này nếu file gốc bị dọn.

## Đã chốt với user (16/10)
- Catalog: **KHÔNG truncate**, giữ dữ liệu cũ ⇒ seeder tìm-hoặc-tạo theo (tên, cha).
- Nhóm hàng sẽ đổi sang Loại SP, rồi **bỏ hẳn** Nhóm hàng.
- Cấp cha của Loại SP lấy từ file cây 4 cấp; tên trùng nhiều cha ⇒ nghiệp vụ sửa file (đã xuất danh sách).
- Đã giải thích "đường 4 cấp không khớp cây" (373 dòng: 338 chỉ lệch Tính chất — Nhóm CN "Thiết bị đo - kiểm tra" dưới 2 Tính chất).
  Đề xuất chưa chốt: coi CâyERP là chuẩn, tra cha theo Loại SP của dòng hàng.

## Số liệu then chốt
- Cây file: 8 Tính chất · 48 Nhóm CN · 270 Nhóm SP · 957 Loại SP; 50 tên trùng nhiều cha (theo đường đầy đủ).
- DB cây phân loại rỗng (1 dòng rác `product_natures` `TCHH.GJGH` "hjjhjh"); `name`, `code` UNIQUE toàn bảng; mã `<PREFIX>.<4 ký tự>` (TCHH./NCN./NSP./LSP.).
- Hàng: 45.890 (28.378 đang dùng); sheet hàng khớp 7.984 mã; **20.398 hàng đang dùng ngoài file**; theo nhóm 1–1 chỉ gán được 9.628 hàng.
- Nhóm ↔ Loại nhiều–nhiều (277 nhóm ↔ >1 loại) ⇒ không thay group_id 1–1.

## Trước khi làm tiếp
Đụng source (seeder, migration, chạy vào DB) phải xin phép riêng với phạm vi cụ thể. Hỏi tồn lần lượt từng câu.

## Rà soát lại từ file "ERP FINAL ngày 16-10-le.xlsx" (16/10, bản user gửi lại — thay cho can-sua-cay-phan-loai-1610.xlsx)
- Nguồn: `nguon/v2-1610/`. Kết quả: `ra-soat-ERP-FINAL-1610.xlsx` (sinh lại: `python3 -I ra_soat_erp_final.py <file> <groups.tsv> <out>`).
- NewERP: 32 tên cấp con nằm dưới >1 cha (2 Nhóm CN · 12 Nhóm SP · 18 Loại SP) → 191 dòng hàng lệch cha đa số.
- Hang_hoa_ma_nhom_cu: 277 nhóm cũ → >1 Loại; 351 Loại → >1 nhóm cũ; 307/893 nhóm DB chưa có Loại (202 nhóm còn 2.045 hàng đang dùng); 1 Loại trỏ nhóm 2579 không có DB; 1.394 dòng (7990–9401) chưa có ID nhóm cũ — hàng mới (6/1.227 mã có trên DB).

## Rà soát file "ERP_final ngày 17-10.xlsx" (18/10, chỉ sheet `NewERP Green Power` theo user)
- Nguồn: `nguon/v3-1710/`. Kết quả: `ra-soat-ERP-1710.xlsx` (sinh lại: `python3 -I ra_soat_1710.py <file17> <file16> <groups.tsv> <products.tsv> <out>`; 2 tsv dump từ `hrm_erp_giacty`).
- Bố cục đổi: bỏ cột "Mã Fast"; cột G = Mã hàng, cột I = ID nhóm hàng cũ (thay sheet `Hang_hoa_ma_nhom_cu`).
- Cây: 6 Tính chất · 48 Nhóm CN · 282 Nhóm SP · 968 Loại SP (16/10: 6 · 48 · 270 · 962). **0 tên cấp con nhiều cha** (16/10: 32 — đã sửa hết), 0 dòng thiếu cấp, 0 tên trùng khi so không dấu/không hoa thường (collation `utf8mb4_unicode_ci`, `name` UNIQUE từng bảng) ⇒ **cây nhập được**. 69 ô có khoảng trắng thừa (tự cắt khi nhập). Tên dài nhất 53 ký tự (cột 255).
- DB giacty: cây rỗng (`product_function_groups`/`product_families`/`product_types` 0; `product_natures` 1 dòng rác `TCHH.GJGH`).
- Mã: 9.207 mã, 7 mã lặp (cùng Loại — vô hại), 167 dòng không mã; 7.984 khớp DB (7.980 đang dùng); ID nhóm ghi trong file khớp 100% `group_id` DB.
- Độ phủ 28.378 hàng đang dùng: a. theo mã 7.980 · b. nhóm cũ 1–1 Loại 3.846 · c. nhóm cũ nhiều Loại 14.507 · d. nhóm chưa có Loại 2.045 (202 nhóm). 278 nhóm ↔ >1 Loại; 1 ID nhóm không có DB; 1.393 dòng trống ID nhóm (hàng mới).

## File import cây 4 cấp (19/10) — `import-cay-1710/` (bản chép `~/Desktop/import-cay-1710/`)
- User chốt: nhập qua **chức năng Import Excel có sẵn của 4 màn** (không seeder, không sửa code). Mẫu barcode Tính chất: Máy móc/Dây chuyền/Phần mềm = 1 · Dụng cụ - đồ nghề = 2 · Vật tư - linh kiện - phụ kiện = 4 · Phụ tùng ô tô - xe máy = 4. Serial 968 Loại = Không bắt buộc. Số ngày tồn lâu để trống (làm cùng việc nhóm hàng, sau).
- Mã sinh tuần tự theo đường sắp chữ cái: TCHH.0001–0006 · NCN.0001–0048 · NSP.0001–0282 · LSP.0001–0968. Bảng tra đủ đường: `0_Bang_tra_cay_4_cap.xlsx`.
- Thứ tự import: 1 → 2 → 3 → 4a → 4b (giới hạn 500 dòng/lần ⇒ Loại tách 2 file). Sinh lại: `python3 -I sinh_file_import_cay.py <file17> import-cay-1710`.
- Bẫy khuôn file: header phải có ĐỦ mọi cột `importColumns` (kể cả "Diễn giải" không bắt buộc), sheet `Data`, cột đầu STT — thiếu 1 cột là "File không đúng mẫu" (lần sinh đầu dính).
- Đã kiểm 19/10 trên màn local (3031/8031, giacty), chặn POST `/import`, chỉ Load + Validate: file 1 **6/6 hợp lệ**; file 2/3/4a/4b mỗi dòng đúng 1 lỗi "mã cha không tồn tại" (48/282/500/468 — đúng vì cấp cha chưa import), 0 lỗi khác. DB không đổi (1·0·0·0).
- Sau import: tick `is_auto_parts` cho Tính chất "Phụ tùng - linh kiện ô tô - xe máy" (B1); xoá/khoá dòng rác `TCHH.GJGH` "hjjhjh".
- **19/10 ĐÃ IMPORT vào DB local `hrm_erp_giacty`** (user "làm"), qua màn Import Excel local 3031/8031, tài khoản e2e (NV 1180 ⇒ created_by/changed_by = 1180): 6/48/282/468+500 thành công, 0 lỗi. Đối chiếu DB: 968/968 đường 4 cấp khớp bảng tra (mã + tên + cha), mẫu barcode đúng, 968 Loại Serial = Không bắt buộc, tất cả Hoạt động, `catalog_histories` có đủ 6/48/282/968 dòng "create". 19/10 (user "làm luôn", qua màn): đã XOÁ dòng rác `TCHH.GJGH` "hjjhjh" + tick "Là phụ tùng ô tô" cho TCHH.0005 (B1 xong trên local). VPS test / prod: chưa import.
