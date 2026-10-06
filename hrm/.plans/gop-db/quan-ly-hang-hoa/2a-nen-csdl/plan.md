# Đợt 2-A — Nền CSDL màn hàng hoá: plan

> 04/10/2026 · @namdangit · khảo sát + chốt: `khao-sat.md` (K0–K4).
> ✅ User cho phép code (04/10) + cho chạy 3 migration vào `hrm_erp` (04/10).

## 0. Mục tiêu & ranh giới

Dựng phần CSDL cho các đợt 2-B/2-C mà **không làm đổi hành vi ERP đang chạy**:
- KHÔNG sinh dòng mới ở `product_company_coefficients` (K1 — backfill trạng thái hoãn tới phase gỡ hệ số giá).
- KHÔNG xoá cột chung trên `products` (`min_stock_qty`, `guarantee`, `guarantee_type`) — bước cuối §24c-1.
- KHÔNG làm A5 (`product_company_units`, tách giá vốn) — để phase giá.
- 4 migration lỡ chạy của nhánh cũ: chỉ có ở DB local ⇒ bỏ qua (user 04/10).

## 1. Phạm vi xin phép

| | |
|---|---|
| Repo | **chỉ `hrm-api`** (hrm-client không đụng) |
| Nhánh | `feat/p2a-nen-csdl` checkout từ `feat/chuyen-doi-hang-hoa`; xong merge về nhánh chung (K4). ⛔ không đụng `gop_db` |
| File mới | 3 migration `Modules/MasterData/Database/Migrations/2026_10_0X_*` · 2 Entity `Modules/MasterData/Entities/Product/` · 1 test `Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php` |
| Bảng đụng | `product_company_coefficients` (+5 cột) · `product_suppliers` (+1 cột, 1.741 dòng nhận giá trị mặc định 1) · tạo `product_business_catalogs` |
| DB | chạy 3 migration vào **DB local `hrm_erp`** — hỏi riêng trước khi chạy |

## 2. Task

### [x] T1. Migration — `product_company_coefficients` thêm trạng thái + 4 cột quản trị (A1, §24b)

```
status              tinyint unsigned NULL   -- NULL = dòng chỉ có hệ số (dữ liệu cũ); 1 Đang nhập thông tin · 2 Chờ tính giá · 3 Đang kinh doanh
business_policy_id  bigint unsigned NULL    FK business_policies(id)
min_stock_qty       decimal(12,2) NULL      -- cùng kiểu products.min_stock_qty
guarantee           int NULL                -- cùng kiểu products.guarantee
guarantee_type      varchar(255) NULL       -- cùng kiểu products.guarantee_type
created_by, updated_by  bigint unsigned NULL
INDEX (company_id, status)
```
- `coefficient` GIỮ NOT NULL (K2: dòng HRM sinh ra ghi 1). UNIQUE(product_id, company_id) **đã có sẵn** — không tạo lại.
- `down()`: drop FK + index + cột. Guard `Schema::hasColumn` để chạy lại an toàn.
- Mã trạng thái (1/2/3) là đề xuất — nêu cùng lúc xin phép.

### [x] T2. Migration — `product_suppliers.company_id` (K3)

```
company_id  bigint unsigned NOT NULL DEFAULT 1   FK companies(id)   INDEX
```
- 1.741 dòng cũ nhận 1 qua DEFAULT (user chốt: toàn bộ về Cty 1, kể cả 44 dòng hàng Cty 4).
- DEFAULT 1 giữ cho `->suppliers()->sync()` của ERP vẫn chạy (không biết `company_id`).
- ⚠️ Hệ quả đã biết: ERP lưu hàng là xoá NCC của MỌI công ty rồi ghi lại về Cty 1 — chấp nhận tới khi 2-D chặn form hàng ERP.
- Không thêm UNIQUE (§24c-1).

### [x] T3. Migration — tạo `product_business_catalogs` (A6)

```
id
product_id      FK products(id)
company_id      FK companies(id)
job_cluster_id  FK job_clusters(id)        -- chỉ lưu Tiểu mục; 3 cấp trên join ngược (A7 đã thoả: job_clusters.group_id NOT NULL)
created_by      bigint unsigned NULL
timestamps
UNIQUE (product_id, company_id, job_cluster_id)
INDEX (company_id, job_cluster_id)
```

### [x] T4. Entity

- `Entities/Product/ProductCompany.php` → bảng `product_company_coefficients` (connection mặc định, KHÔNG mysql2), docblock ghi rõ tên bảng lệch nội dung (§24b) + hệ số giá sẽ bỏ (K0); hằng `STATUS_*`; quan hệ `product`, `company`, `businessPolicy`.
- `Entities/Product/ProductBusinessCatalog.php` → quan hệ `product`, `company`, `jobCluster`.
- Không đụng `Human/Entities/TpProductCompanyCoefficient.php` (đang đọc mysql2 — việc của luồng cắt mysql2).

### [x] T5. Test PHPUnit `ProductCompanyFoundationTest`

- 3 bảng/cột tồn tại đúng kiểu, nullable, default (`product_suppliers.company_id` = 1 khi insert không truyền).
- UNIQUE 3 cột của `product_business_catalogs` chặn trùng.
- Bất biến ERP: số dòng `product_company_coefficients` **không đổi** sau migrate (1.105); mọi dòng cũ `status IS NULL`, `coefficient` giữ nguyên.
- `down()` trả schema về như cũ.

### [x] T6. Kiểm sau khi chạy vào DB local (khi được phép)

- `SHOW CREATE TABLE` 3 bảng khớp T1–T3.
- `SELECT COUNT(*), SUM(company_id=1) FROM product_suppliers` = 1.741 / 1.741.
- Giá popup ERP không đổi: so 20 mã mẫu có giá lẻ nghìn trước/sau (truy vấn `SearchController` CASE WHEN) — phải trùng khớp.
- Không có FE ⇒ không cần Playwright.

## 3. Việc chuyển sang đợt khác (đã ghi)

- 2-D: chặn thêm route lưu **Hãng sản xuất ERP** (`Sale/ManufacturesController:274`) — K2.
- Phase gỡ hệ số giá: backfill trạng thái hàng cũ + 3 câu (chi nhánh 1.100 dòng · status 2/5 · `deleted_at`) — khảo sát mục 3.

## Nhật ký kiểm (04/10/2026)

| Kiểm | Kết quả |
|---|---|
| RED trước khi có code | 5/5 ca fail (thiếu cột/bảng/class) |
| Migrate `--path` đúng 3 file (DB còn >20 migration người khác đang chờ — KHÔNG chạy) | 3/3 Migrated |
| PHPUnit `ProductCompanyFoundationTest` | **OK 5 tests, 30 assertions**; dòng thử dọn sạch (`product_suppliers` 1.741, `product_business_catalogs` 0) |
| Bảng hệ số trước/sau | 1.105 dòng · tổng hệ số 1130.4340 — không đổi |
| `product_suppliers.company_id` | 1.741/1.741 = 1 |
| Giá popup (công thức `SearchController` CASE WHEN), 20 mã × Cty 1/2/3 × mọi loại giá | **231/231 dòng trùng khớp** trước/sau |
| `down()` | ⚠️ chưa chạy thử rollback trên DB dùng chung |
| Bẫy gặp | MySQL 8 trả tên cột `information_schema` CHỮ HOA ⇒ `$row->is_nullable` undefined; phải đặt bí danh `AS is_nullable` |

### Checkpoint — 2026-10-04
Vừa hoàn thành: T1–T6, commit `15610ea2a` trên `feat/p2a-nen-csdl`, đã fast-forward vào nhánh chung `feat/chuyen-doi-hang-hoa` + push (04/10).
Đang làm dở: không.
Bước tiếp theo: mở đợt 2-B (Đọc: API + FE 4 màn) — khảo sát + plan, nhánh con từ `feat/chuyen-doi-hang-hoa`.
Blocked:
