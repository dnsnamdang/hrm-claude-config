# Plan T2 — Nền CSDL luồng tính giá (Phase 7) — 11/10/2026 (chốt T2-Q1, T2-Q2)

> Nguồn: `design.md` §2.3, §3.1, §3.3, §4, §12 (T2) · `khao-sat-csdl-chan-erp.md` §1, §2, §4 · `ton.md` D2, D4, D9.
> ⛔ Plan KHÔNG phải lệnh code — xin "làm" riêng kèm phạm vi (repo · nhánh · file · migration/seed/backfill vào DB nào).
> Môi trường: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t2-nen-csdl-tinh-gia` từ `feat/chuyen-doi-hang-hoa`; DB dev `hrm_erp_giacty`.

## 0. Hiện trạng đo trong code (11/10)

- HRM **chưa có model nào** cho 15 bảng luồng (grep `price_asking|price_calculate` chỉ ra `ProductUsageGuard` + `Cost`). `Modules/Sale` là module rỗng (chỉ khung, chưa có Entities/Migrations/Tests).
- PHPUnit chỉ quét `tests/Unit` + `tests/Feature` theo `phpunit.xml`, nhưng test module chạy bằng đường dẫn (`vendor/bin/phpunit Modules/MasterData`) — G1–G6, T1 đều nằm ở `Modules/MasterData/Tests/Feature`.
- Toàn bộ code giá (G4/G5 `Services/ProductPrice`, T1 `Services/InternalPricePolicy`) nằm trong **`Modules/MasterData`**, dù menu ở Tài chính / Bán hàng.
- Id quyền **1662–1669 trống** ở nhánh chung + DB giacty (đã dùng tới 1661, 1670–1675; giacty có thêm 1676–1678 của nhánh CSKH). Chưa kiểm `origin/gop_db` (git đang vướng Xcode license) — kiểm lại ngay trước merge (R5).
- `ProductCompany` (`Entities/Product/ProductCompany.php:23-40`): 4 hằng 1–4 + `STATUS_TEXT` + `STATUS_COLOR`; chưa có 5.

## 1. Câu cần chốt trước khi code (hỏi lần lượt)

- ✅ **T2-Q1 Module đặt code luồng** — user chốt 11/10: **`Modules/MasterData`** (cùng G4/G5/T1; T5 tách lõi ghi giá dùng chung; PHPUnit chung). Menu vẫn ở Bán hàng / Tài chính như design §7. Thay đề xuất Sale + Finance của design §6. Thư mục: `Entities/PriceCalculation/`, `Services/PriceCalculation/`, `Console/`.
- ✅ **T2-Q2 Hàng mới sau khi gửi YCHG (mã 2/5) hiện ở màn nào** — user chốt 11/10: **giữ ở màn "Hàng hoá nhập thông tin"** (lọc 1, 2, 5 + badge); có giá (3) thì sang màn Đang KD. ⇒ thêm S8, S9.

## 2. Task

### 2.1 Migration (khuôn G1: guard `hasTable/hasColumn`, cột mới NULL được, có `down()`)
- [x] M1 tạo `price_asking_request_groups` (design §3.1, khảo sát §2.1): UNIQUE(price_asking_request_id, brand_id, manufacture_id), index (company_id, status), (xnk_employee_id, status).
- [x] M2 `price_asking_requests`: index (company_id, status).
- [x] M3 `price_asking_request_products`: + `group_id` FK + index; `unit_id`, `unit_name` ⇒ NULL được (giữ FK) — Cách A khảo sát §2.3.
- [x] M4 `price_asking_request_approve_histories`: + `group_id` NULL + index; + index `price_asking_request_id`.
- [x] M5 `price_calculate_requests`: + `group_id` UNIQUE; + `rejected_by`, `rejected_at`.
- [x] M6 `price_calculates`: UNIQUE(price_calculate_request_id) — migration tự kiểm trùng trước, có trùng thì dừng kèm danh sách id.
- [x] M7 `price_calculate_products`: + 8 cột chụp chính sách (khảo sát §2.5) + `approval_status`, `approval_comment`, `approval_decided_at`.
- [x] M8 `price_calculate_results`: UNIQUE(price_calculate_id) (kiểm trùng như M6).
- [x] M9 `product_approves`: + `price_calculate_id` NULL + index.

### 2.2 Model / entity (connection mặc định, KHÔNG `mysql2`; bảng ERP ⇒ `extends Model` + service tự gán audit, ghi lý do trên class — CLAUDE.md HRM)
- [x] 15 model bảng cũ + `PriceAskingRequestGroup`; quan hệ cha–con; hằng trạng thái + nhãn + màu (design §2.1, 9 mã màu chuẩn); scope "Đang hỏi giá" đọc `IN (1,5,7,10)` cho phần đầu phiếu cũ.

### 2.3 Trạng thái hàng × công ty mã 5 (D4)
- [x] `ProductCompany::STATUS_PRICING = 5` + nhãn "Đang tính giá" + màu `#2563EB`.
- [x] Sửa mọi chỗ đọc theo danh sách rà (mục 3) — xử như mã 2.
- [x] FE: S5 (danh sách lọc thêm 5) + S9 (màn Nhập thông tin hiện 1/2/5).
- [x] BE: S2 (🐞 guard G4), S4, S8; test S6, S7 + ca màn Nhập thông tin trả mã 2/5.

### 2.4 Quyền (D9)
- [x] `PriceCalculationPermissionSeeder` riêng, idempotent, khuôn `ProductPricePermissionSeeder`: 1662 / 1663 / 1664, type 8, group "Hàng hoá"; thêm cùng dòng vào `PermissionsTableSeeder` (giữ đồng bộ như 1656–1658). Chèn vào giacty bằng seeder riêng — KHÔNG chạy seeder chính.

### 2.5 Lệnh
- [x] `price-asking:backfill-groups` (`--dry-run`, chạy lại ghi 0) theo khảo sát §2.8.
- [x] `price-asking:close-stale --before=2026-06-01` (`--dry-run`) — CHỈ chạy dry-run (chạy thật hỏi riêng): nhóm dở ⇒ 6 Huỷ duyệt, `close_reason` "Chuyển hệ thống", có log; nháp giữ.

### 2.6 Kiểm
- [x] PHPUnit mới: migration up→down→up; backfill (ca 20 phiếu thiếu hãng, 4 phiếu đổi hãng, 6 phiếu st1 có YCTG nháp ⇒ 7, 21 YCTG bị trả 3 ⇒ 5, chạy lại ghi 0); close-stale; seeder idempotent; mã 5 ở từng chỗ đọc đã sửa.
- [x] PHPUnit MasterData toàn bộ xanh (hiện 359).
- [x] Dry-run trên giacty khớp số khảo sát §2.8/§4 (4.029 nhóm · 6.729 dòng · 3.147 YCTG) — số có thể lệch do giacty sao từ hrm_erp 10/10, ghi số thật.
- [x] Chạy thật trên giacty (sao lưu 15 bảng trước), chạy lại ghi 0.
- [x] FE (nếu có sửa): Playwright đo nhãn/màu trạng thái 5 ở màn hàng hoá.

## 3. Rà `pcc.status` (D4) — kết quả 11/10 (hrm-api + hrm-client + ERP `wt-erp-2d1`)

**Chưa có chỗ nào GHI mã 2** (luồng 1→2 chưa từng code) — mã 2 hiện chỉ được đọc. Hầu hết bộ lọc là `= 3` (chỉ đang KD), `<> 4` / `isLocked`, `= 1`, NULL/NOT NULL ⇒ mã 5 tự rơi đúng chỗ mã 2 đang rơi. Phải sửa:

| # | Chỗ | Vì sao | Sửa |
|---|---|---|---|
| S1 | `ProductCompany.php:23-41` | thiếu hằng / nhãn / màu cho 5 | `STATUS_PRICING = 5`, "Đang tính giá", `#2563EB` |
| S2 | 🐞 `ProductPriceUpdateService.php:154-170` `assertTradingAt` (gọi ở :91, :110) | `switch` không có `default` ⇒ **mã 5 lọt qua như Đang KD, màn Cập nhật giá G4 sửa được giá** | thêm `case 5` (câu riêng "Hàng đang tính giá" — dùng lại `MSG_WAITING_PRICE` được) + `default` chặn mọi mã ≠ 3 |
| S3 | `ProductListResource.php:55-59`, `ProductDetailResource.php:28,42-44` | badge trống khi map thiếu 5 | tự hết sau S1 (đã `?? null`) — kiểm |
| S4 | `ProductLifecycleService.php:285-293` `statusPayload` | đọc map không `??` | thêm `??` cho chắc |
| S5 | FE `utils/product-list-screens.js:198-205` | danh sách lọc trạng thái gõ cứng 1/2/3 (+4) — dùng ở màn Dữ liệu công ty + popup Catalog | thêm 5 "Đang tính giá" |
| S6 | `Tests/Feature/ProductCompanyFoundationTest.php:58-62` | bất biến "status chỉ ∈ 1–4" ⇒ đỏ khi có dòng 5 | thêm 5 vào tập hợp lệ |
| S8 | `ProductService.php:203-205` `SCREEN_ENTERING` | lọc `= 1` ⇒ hàng 2/5 biến khỏi màn (T2-Q2) | `IN (1, 2, 5)`; thao tác giữ gate cũ (xoá chỉ mã 1 — `deletableAt`) |
| S9 | FE màn `pages/master-data/products/entering.vue` (qua `ProductListPage`) | cần ô lọc trạng thái 1/2/5 + cột badge nếu màn chưa có | kiểm màn, bổ sung theo khuôn màn Dữ liệu công ty; Playwright đo |
| S7 | Ca test mới | `ProductPriceScreenApiTest` (:173, :343), `ProductLifecycleApiTest` (:876) đang có ca mã 2 | thêm ca mã 5 tương ứng |

Hành vi giữ nguyên như mã 2 (không sửa, tự chốt theo D4): sửa thông tin hàng được (`editableAt`, `assertOwner`) · không lấy về / không khoá / không xoá · không hiện ở màn Đang KD (= 3), màn Cập nhật giá, xem trước chính sách (= 3) · popup Catalog tab Thêm có (≠ 4) · tính là "đang dùng" (NOT NULL) · có bộ giá theo công ty (`companiesWithStatus` NOT NULL).
ERP: không chỗ nào xử riêng mã 2; popup chọn hàng lọc `= 3` ⇒ 5 bị loại như 2; cron 14:30 không đọc status ⇒ **ERP không phải sửa**.
Để ý cho T5: `ProductPriceApprovalService::markOwnerTrading` (:380-384, :469-481) ép mọi mã ⇒ 3 khi duyệt hàng `products.status = 2` — đúng ý (giá đã áp), ghi nhận.


## 4. Kết quả (11/10/2026 — user cho "làm")

- Nhánh `feat/t2-nen-csdl-tinh-gia` (2 repo). api: `e41e536e0` mã 5 · `e7e4cbd00` quyền · `303bf43bb` lệnh · `a34237155` migration + model
  (commit bổ sung — lần đầu sót do glob đường dẫn trong zsh, đã merge lại) ⇒ merge LOCAL nhánh chung `a078e77f3` + `ee6928c96`.
  client: `b4226d038` ⇒ merge LOCAL `fd7a87d4d`. CHƯA push.
- DB `hrm_erp_giacty`: sao lưu 18 bảng trước (`wt-chuyen-doi-hang-hoa/backup-t2-20261011-1424/t2-tables.sql`, 26MB) · 9 migration (batch 436–437) ·
  up→down→up đạt, sau down schema 8 bảng KHỚP bản sao lưu · 🐞 M3 down lỗi MySQL 1832 (MODIFY cột có FK sang NOT NULL) ⇒ gỡ/gắn FK
  `unit_id` (như G1 M3) · seeder 1662–1664 (chạy 2 lần, lần 2 chèn 0; chưa gán role).
- Backfill thật = dry-run: **4.029 nhóm · 6.729 dòng hàng · 3.147 YCTG · 10.029 log · 21 YCTG 3⇒5 · 20 phiếu lấy hãng dòng đầu · 6 st1⇒7**;
  trạng thái nhóm NULL 548 · 1: 67 · 4: 3.119 · 5: 41 · 6: 155 · 7: 28 · 9: 71 (khớp khảo sát §2.8/§4); XNK: người duyệt 3.530 · phân công công ty
  gửi tới 435 · công ty phiếu 26 · **không xác định 38**. Chạy lại ghi 0. Log thiếu 114 so với tổng 5 loại = log mồ côi (phiếu đã xoá ở ERP).
- close-stale dry-run: **45 nhóm / 45 phiếu** (1: 10 · 5: 13 · 7: 22 — khớp 14/13/18 của khảo sát, 4 phiếu st1 có YCTG sang 7); 22 nhóm có YCTG,
  1 có PTG nháp. CHƯA chạy thật.
- PHPUnit MasterData **372/372** (trước 359): +7 backfill/close-stale, +5 seeder, ca mã 5 ở G4 (kèm mã lạ ⇒ default chặn), khoá, màn Nhập thông tin.
  Danh sách trắng giá thêm 4 model giá của chứng từ (khớp mẫu `ProductExpectedPrice` do tên class).
- Playwright MCP (Nuxt 3031 + API 8031, e2e_assign; tạm đổi 3 dòng pcc công ty 1 sang 1/2/5 rồi trả nguyên status + updated_at):
  màn Nhập thông tin hiện 3 hàng, badge đúng chữ/màu (5 `#2563EB`, nền rgba .1); ô lọc Trạng thái đứng đầu, 3 lựa chọn; chọn "Đang tính giá" ⇒
  1 request `company_status=5`, 1 hàng; bộ lọc 4·4·3 cùng bề ngang ở 1440 + 1280, không cuộn ngang; màn Dữ liệu công ty có "Đang tính giá".
- e2e (chưa chạy): `products-read.api.spec.ts` ca 3b · `products-read-ui.spec.ts` ca ô lọc Trạng thái màn entering.
- Tự chốt khi code (ghi để duyệt): close-stale — phần đầu phiếu khi mọi nhóm đóng = 4 nếu có nhóm Đã tính giá, không thì **6 Huỷ duyệt** (mã cũ);
  YCTG/PTG nháp của nhóm 7 bị đóng GIỮ NGUYÊN ⇒ T4/T5 phải chặn thao tác khi nhóm đã đóng. ✅ **User duyệt 11/10**: đóng nhóm, giữ chứng từ (22 nhóm có YCTG: 17 YCTG Không duyệt · 4 nháp · 1 kèm PTG nháp) — **ràng buộc cho T4/T5: nhóm đã đóng (4/6/9) ⇒ BE 423 mọi thao tác ghi trên YCTG/PTG của nhóm, FE ẩn nút, màn hiện "Nhóm đã huỷ duyệt"; chỉ còn xem.** Không thêm trạng thái Huỷ cho YCTG/PTG. Backfill: nhóm 9 ⇒ `close_reason` = ghi chú XNK;
  nhóm 6 ⇒ `cancel_reason`; `closed_by` = XNK đã duyệt. Phân công XNK bám ERP (dòng `employee_date_to IS NULL` mới nhất theo `created_at`).

- ✅ **close-stale CHẠY THẬT trên giacty 11/10 (user yêu cầu, để đánh giá)** — sao lưu trước `backup-t2-20261011-1424/truoc-close-stale.sql`
  (3 bảng groups / requests / approve_histories). Đóng 45 nhóm (1: 10 · 5: 13 · 7: 22) ⇒ 6 "Chuyển hệ thống"; 45 phiếu ⇒ 6 Huỷ duyệt (không phiếu nào
  có nhóm Đã tính giá); 45 log "Huỷ duyệt" (id > 19304, `created_by` = 0 — chạy bằng lệnh, không có người); 21 YCTG + 1 PTG nháp giữ nguyên;
  0 nhóm mở trước mốc; nhóm sau mốc không đụng (1: 57 · 5: 28 · 7: 6). Chạy lại ghi 0. Phần đầu phiếu sau chạy: 1: 59 · 5: 28 · 7: 4 · 6: 200.
  Điểm tự chốt "mọi nhóm đóng ⇒ 4 nếu có nhóm có giá, không thì 6" — ✅ user duyệt 11/10.

### Checkpoint — 2026-10-11 (wrap up)
Vừa hoàn thành: T2 xong — code + DB giacty (migrate, seed 1662–1664, backfill 4.029 nhóm, close-stale THẬT 45 nhóm) + PHPUnit 372/372 + Playwright;
merge LOCAL nhánh chung api `ee6928c96`, client `fd7a87d4d` (chưa push); tài liệu đã push hrm-claude-config `26189ed`.
Đang làm dở: không.
Bước tiếp theo: user đánh giá kết quả close-stale (log `created_by` = 0) · push code khi user báo · plan T3 YCHG.
Blocked: —

### Sau wrap up — 11/10/2026 (user chốt)
- Log close-stale: user chốt **created_by = 13** ⇒ đã UPDATE trên giacty: 45 log (id 19684–19728) `created_by` 0 ⇒ 13; 45 nhóm "Chuyển hệ thống" `closed_by`/`updated_by` NULL ⇒ 13. Production: xem T3-Q6.
- Code nhánh chung: **giữ local**, chưa push. Role tạm `T1_UAT_NAMDANG` (107124): **giữ** để user tự test.
