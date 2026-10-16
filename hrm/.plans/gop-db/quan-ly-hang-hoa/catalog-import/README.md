# Nhập cây phân loại + catalog, bỏ Nhóm hàng hoá — ĐỌC TRƯỚC (cập nhật 16/10/2026)

**Trạng thái: TẠM DỪNG theo yêu cầu user (16/10).** Chưa viết code, chưa chạy gì vào DB cho cả 3 việc dưới.

| Việc | File | Đang chờ |
|---|---|---|
| 1. Import cây catalog kinh doanh (Lĩnh vực › Chương › Mục › Tiểu mục) | `khao-sat.md` | user để sau việc 2–3; còn hỏi C2–C5 |
| 2. Nhập cây phân loại 4 cấp (Tính chất › Nhóm CN › Nhóm SP › Loại SP) + gán Loại SP cho hàng | `nhom-hang-sang-loai-sp.md` | nghiệp vụ sửa file theo `can-sua-cay-phan-loai-1610.xlsx` |
| 3. Bỏ Nhóm hàng hoá (`groups`) | `de-xuat-bo-nhom-hang-hoa.md` (đề xuất) + `phu-luc-kiem-ke-nhom-hang.md` (kiểm kê file:line HRM/ERP + số DB) | user trả lời Q1–Q5 (§6 đề xuất) — câu đang hỏi: Q1 bỏ nhóm CÙNG đợt go-live hay đợt riêng |

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
