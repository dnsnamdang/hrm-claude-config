# Report — Đổi luật chép giá giữa các công ty (15/10/2026)

Brief: `cum-gia-1510-brief.md`. Repo `wt-chuyen-doi-hang-hoa/hrm-api`. Không ghi DB, không tạo/DROP database, không push, không stash,
không viết lệnh dọn.

## 1. Commit

| Commit | Nhánh | Nội dung |
|---|---|---|
| `0a598827e` | `feat/cdhh-cum-gia` (từ `feat/chuyen-doi-hang-hoa` @ `4bdcf760e`) | feat(gia-cty): đổi luật chép giá 15/10 — nhóm chia sẻ 1·3·4, công ty tự quản 2·7 |
| **`5ab7ab2ac`** | `feat/chuyen-doi-hang-hoa` | Merge `--no-ff` LOCAL. Soát marker xung đột (`git grep` `<<<<<<<`/`>>>>>>>`/`=======`) trong `config` + `Modules/MasterData`: 0. Chưa push |

## 2. File đã sửa (hrm-api, đều LF như gốc)

| File | Thay đổi |
|---|---|
| `config/price.php` | Bỏ `cluster_company_ids` [1,2,3,4]. Thêm `shared_price_company_ids` **[1,3,4]** + `self_managed_company_ids` **[2,7]**, comment tiếng Việt theo chốt 15/10 |
| `Modules/MasterData/Services/ProductPrice/CompanyPriceBackfill.php` | Constructor nhận nhóm chia sẻ. B5 chỉ chạy khi chủ ∈ {1,3,4}, công ty nhận = nhóm \ {chủ}. B0 `pcu_foreign` coi pcu hợp lệ khi chủ VÀ nhận cùng thuộc nhóm. B1–B4 không đổi (mọi chủ) |
| `Modules/MasterData/Console/BackfillCompanyPricesCommand.php` | Đọc 2 khoá config. Dòng đầu in "nhóm chia sẻ: 1, 3, 4 · tự quản: 2, 7". Bảng luôn có cột Cty 1·2·3·4·7 (+ cột công ty khác nếu có số). `--company` giữ nguyên |
| `Modules/MasterData/Services/ProductPrice/CompanyPriceComparator.php` | Constructor (nhóm chia sẻ, tự quản). Hàng được so: chủ ∈ 2 danh sách. Cặp cần có giá: (hàng × chủ) + (hàng × R) khi chủ và R cùng ∈ nhóm chia sẻ. Cặp ngoài luật: không so, không đếm — trừ cặp HRM sinh (N71) vẫn kiểm BB1 |
| `Modules/MasterData/Console/CompareCompanyPricesCommand.php` | Đọc 2 khoá config, mặc định so 1·2·3·4·7, dòng "Số cặp" ghi rõ luật |
| `Modules/MasterData/Tests/Feature/CompanyPriceBackfillTest.php` | Sửa cho luật mới (chi tiết mục 3) |

Tài liệu: `gia-theo-cong-ty/runbook-trien-khai.md` (ghi chú đầu file, mục 3.0 luật mới + bảng 3a mới, bảng 3a cũ thu gọn và ghi
"luật cũ 1-2-3-4", mục 4/5 + 2 nhật ký ghi "luật cũ"), `quan-ly-hang-hoa/deploy-dev-server.md` bước 5 (ý nghĩa nhóm + cảnh báo DB dev
đã backfill luật cũ), `gia-theo-cong-ty/design.md` (P2/P2b, P2c, P12, BB8, §3.1, §3.2 B5, §3.4, §3.5 ghi "Đổi 15/10" + mục nhật ký
"Đổi 15/10/2026").

## 3. Test

**`CompanyPriceBackfillTest` 12/12 OK (254 assertion) · cả bộ `Modules/MasterData` 557/557 OK (5.115 assertion, 3 phút 23 giây)** —
đúng mốc 557. Chạy trên `hrm_erp_giacty` trong transaction, rollback sau mỗi ca (cách chạy cũ của bộ này).

Bộ hàng giả mới:
- H1 (Cty 1) có `pcc(H1,3)` = 1.05, `pcc(H1,4)` = 1, `pcc(H1,2)` = 1.07 (HP có dòng hệ số ERP cũ). Kết quả: chép sang 3 (giá × 1.05, làm
  tròn nghìn) và 4 (giá bằng, T4 lẻ nghìn). **KHÔNG sang 2/7**: không upp/pcu, dòng `pcc(H1,2)` giữ `status` NULL + hệ số 1.07.
- H2 (Cty 4, thiếu loại 5): bù 0 rồi chép sang 1, 3. Không có dòng hệ số ⇒ giá bằng (assert từng loại).
- **H7 (Cty 2) / H8 (Cty 7)**: chỉ có `pcc` chủ status 3 + upp/pcu của chủ, không sang 1/3/4.
- Dry-run = chạy thật. Lệnh in bảng có tiêu đề `Cty 1 | Cty 2 | Cty 3 | Cty 4 | Cty 7 | Tổng`.
- `--company`: lọc [1,2] thì H1 không chép (2 là công ty tự quản, 3/4 ngoài lọc). H7 qua B4 ở Cty 2. Sau đó lọc [3,4] thì chép tiếp.
  Lọc [7] chỉ đụng H8.
- Idempotent: chạy lần 2 ghi 0 dòng.
- So khớp: 8 cặp, 0 lệch. `compare([2])` chỉ so 1 cặp (H7). Sửa 1 giá Cty 3 thì báo đúng 1 lệch. N71: cặp HP "lấy về" bằng HRM
  (ngoài luật) vẫn kiểm BB1, `chu_chua_kinh_doanh` 3 → 2.
- N72: điền 4 ô quản trị cho dòng nhận 3/4. Dòng HP không bị đụng.
- Mẫu dữ liệu thật trên DB đích: 0 lệch, dry-run 0 dòng.

## 4. Đo dry-run (chỉ đọc)

DB có sẵn dữ liệu trước backfill: **`hrm_erp`** (có M1/M2, `upp.company_id` NULL 264.646, pcu 0, pcc có status 0). Lệnh chạy bằng
`DB_DATABASE=hrm_erp php artisan product-price:backfill-company --dry-run`, đã kiểm `getDatabaseName()` = `hrm_erp`. Đếm lại sau khi
chạy: NULL 264.646 / pcu 0 / pcc status 0, tức không ghi gì. Thời gian 5,6 giây.

| Việc | Cty 1 | Cty 2 | Cty 3 | Cty 4 | Cty 7 | Tổng |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 0 · 0 · 0 · 0 | | | | | |
| upp.assign | 258.270 | 18 | 138 | 6.220 | 0 | 264.646 |
| pcu.owner | 45.477 | 3 | 23 | 1.057 | 0 | 46.560 |
| upp.fill | 5.765 | 0 | 0 | 108 | 0 | 5.873 |
| pcc.owner ins + upd | 27.370 | 3 | 14 | 980 + 4 | 0 | 28.371 |
| pcu.copy | 1.007 | 0 | 28.821 | 27.860 | 0 | 57.688 |
| upp.copy | 6.042 | 0 | 172.926 | 167.160 | 0 | 346.128 |
| pep.copy | 32 | 0 | 2.007 | 1.975 | 0 | 4.014 |
| pcc.recv ins + upd | 998 | 0 | 27.972 + 382 | 27.361 + 23 | 0 | 56.736 |
| **TỔNG GHI** | 344.961 | **24** | 232.283 | 232.748 | 0 | **810.016** |

Đối chứng: code cũ chạy dry-run trên cùng DB, cùng ngày được TỔNG 1.042.371. Bảng 10/10 ghi 1.042.374; chênh 3 dòng `pep` vì số này
phụ thuộc ngày chạy. Luật mới bớt **232.355** dòng: toàn bộ phần chép vào Cty 2, cộng 3 mã HP (3 ĐVT) không còn chép ra 1/3/4.

So khớp (chỉ đọc) trên `hrm_erp_giacty` (DB này đã backfill bằng luật cũ) với code mới: **85.107 cặp, 0 lệch**, T4 229, §3.3 17.619.
Số cặp này = 28.368 mã chủ thuộc 1/3/4 × 3 công ty + 3 cặp chủ HP, tức là bằng đúng số `pcc` có status sau backfill theo luật mới.

## 5. Điểm cần user biết

1. **Hàng có chủ ngoài 2 danh sách (5/6/8).** Giữ hành vi cũ của hàng ngoài cụm: vẫn qua B1–B4 (gán chủ dòng giá, pcu chủ, bù loại,
   pcc chủ status 3), không chép, không nhận. Không thể bỏ B1 vì M3 cần mọi dòng giá có `company_id`. Lệnh so khớp không so các hàng
   này. Đo 15/10: **0 mã** có chủ 5/6/7/8, nên hiện tại nhánh này không có dữ liệu thật đi qua.
2. **Hàng `company_id` NULL.** Như cũ: tiền tố `SG-` thì gán Cty 4 (1 mã, status 0). Không xác định được chủ thì B0 `owner_unknown`
   dừng cả lệnh.
3. **Công ty tự quản 2/7 và công ty 5/6/8 đi cùng một đường backfill** (B1–B4, không B5). Danh sách tự quản chỉ khác ở 2 chỗ: lệnh
   so khớp kiểm cặp chủ của 2/7, và bảng in luôn có cột Cty 2, Cty 7.
4. **`hrm_erp_giacty` chưa dọn (việc treo, user "dọn sau").** HP đang giữ hàng chép của 1/3/4, và 1/3/4 đang giữ 3 mã HP. Chạy lại
   lệnh mới ra 0 dòng vì không tự dọn. So khớp ra 0 lệch vì bỏ qua cặp ngoài luật. Vì vậy **dữ liệu trên giacty / VPS test sẽ không
   phản ánh luật mới tới khi dọn**. Nếu VPS test backfill lại từ đầu trên DB chưa backfill thì sẽ ra đúng luật mới.
5. **ERP `wt-erp-2d1/app/Console/Commands/PriceSnapshotCommand.php`** (dòng 75, 80, 84) còn gõ cứng `[1, 2, 3, 4]` khi lấy mẫu hàng
   cho snapshot §3.7. Ngoài phạm vi, chưa sửa.
6. Đầu migration `2026_10_09_000003` còn chữ "công ty nhận trong cụm". Không sửa vì migration đã chạy, chỉ là chú thích.

## 6. Lỗi / rủi ro mới

- **N128** — Sau khi đổi luật, HP mất toàn bộ hàng của 1/3/4. Hôm nay, qua ERP `getData`, HP đang bán mọi hàng của cụm: đo `hrm_erp`
  có **398 mã** đang bán của công ty khác mà HP có dòng hệ số riêng (`pcc` company 2). Sau chuyển đổi, popup HP chỉ còn 3 mã của HP.
  Cần chốt 2 việc:
  - (a) Chứng từ HP đang dở dang có hàng 1/3/4 sẽ xử lý giá thế nào. Đọc theo công ty thì HP không có dòng giá cho các mã này.
  - (b) HP lấy lại hàng nào thì đi đường "lấy về" (2-C2) và tự tính giá.

  Chưa đo số chứng từ dở dang của HP. Mức độ: cần user chốt trước khi lên production. ETEK Green không bị ảnh hưởng vì luật cũ đã để
  Cty 7 khởi đầu trống.
