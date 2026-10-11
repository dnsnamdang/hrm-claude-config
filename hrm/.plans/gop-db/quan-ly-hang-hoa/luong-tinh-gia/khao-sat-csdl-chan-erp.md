# Phase 7 — Khảo sát CSDL + chặn ERP cho luồng tính giá (11/10/2026)

> Khảo sát CHỈ ĐỌC: chỉ chạy `SHOW` / `SELECT`, không sửa source, không ghi DB.
> - DB: `hrm_erp_giacty` (DB gộp local, kết nối theo `wt-chuyen-doi-hang-hoa/hrm-api/.env`). Dữ liệu chụp tới khoảng **15/09/2026**: YCHG mới nhất tạo 15/09 09:37, PTG mới nhất 14/09 17:23.
> - ERP: worktree `wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi`, HEAD `027fb570a2` (đã có G6).
> - Đọc kèm: `ton.md` (Q1–Q20), `khao-sat-be-erp.md`, `mockup-ghi-chu.md` (mockup T0 đã duyệt 11/10).
> - ⚠️ Số liệu ở đây là của DB local. Trước go-live phải chạy lại các câu SQL ở mục 4.4 trên production.

---

## 0. Tóm tắt

| Việc | Kết luận |
|---|---|
| 15 bảng | Đủ 15 bảng. Tất cả là InnoDB utf8mb4, khoá chính bigint, **không có `deleted_at`** (xoá cứng). FK trỏ về `employees` / `companies` / `departments` / `units` / `products` / `costs` / `price_types`. DB gộp chỉ có **một** bảng `employees`, và `auth()->id()` của HRM chính là `employees.id` (`TpEmployee` → `$table = 'employees'`), nên HRM ghi `created_by` không vướng FK |
| Thêm mới | **1 bảng** `price_asking_request_groups` + cột `group_id` ở 3 bảng (dòng hàng YCHG, YCTG, log) + cột chụp chính sách ở dòng PTG + cột nối PTG với Duyệt giá bán (G5) |
| Sửa kiểu | `price_asking_request_products.unit_id`, `unit_name` chuyển sang NULL được (YCHG không chọn ĐVT, Q9) |
| Trạng thái mới | Phần đầu YCHG thêm **10 = Đang hỏi giá**. YCTG thêm **5 = Không duyệt, 6 = Chờ duyệt giá**; giá trị 1 giữ nghĩa, đổi nhãn thành "Đang tính giá". PTG thêm **5 = Chờ duyệt giá, 6 = Giá bị từ chối**. Không đè lên giá trị cũ nào |
| Phiếu cũ | Đề xuất **backfill 1 nhóm cho mỗi phiếu** (4.029 nhóm), lấy theo hãng ghi ở **phần đầu phiếu**, không lấy theo hãng hiện tại của hàng. Trạng thái phần đầu phiếu cũ để nguyên, HRM đổi sang nhãn mới lúc đọc |
| Chặn ERP | Thêm 3 đích vào `ProductMovedToHrm::TARGETS`, gắn middleware cho **41 route** (4 nhóm + `product.getDataForPriceAsking`), giữ nguyên tên route. Sửa 5 link menu. 3 thẻ dashboard: đề xuất **bỏ** |
| Cron 01:00 | **Không phải sửa.** Cron chỉ đọc `product_expected_prices` (status=2, flag≠1). HRM ghi giá qua G4/G5 vẫn giữ đúng quy ước này |
| Phiếu đang dở | 137 YCHG đang chạy (1: 73 · 2: 1 · 5: 41 · 7: 22), 28 YCTG (27 nháp/bị trả + 1 đã nhận), 1 PTG nháp, 376 YCHG nháp. Đề xuất: dọn ở ERP trước ngày chuyển, phần còn lại xử lý tiếp ở HRM. Riêng **30 phiếu hỏi chéo công ty** cần chốt cách xử lý |

---

## 1. Hiện trạng 15 bảng (`SHOW CREATE TABLE`)

Quy ước chung của cả 15 bảng:
- `id bigint unsigned AUTO_INCREMENT`, `created_at`/`updated_at` timestamp NULL.
- Mọi bảng con trỏ cha bằng `parent_id` (riêng log dùng `price_asking_request_id`).
- Tên FK viết tắt kiểu `pcpp_pc`, `pcrpc_pcr`.

### 1.1 Yêu cầu hỏi giá (YCHG)

**`price_asking_requests`** — 4.029 dòng, AUTO_INCREMENT 4288

| Cột | Kiểu | Ghi chú |
|---|---|---|
| code | varchar(255) NOT NULL | `PYCHG-xxxxx` |
| note | varchar(255) NULL | ghi chú của người lập |
| comment | varchar(255) NULL | ghi chú của PTKD (duyệt / không duyệt) |
| approver_comment | text NULL | ghi chú của XNK |
| cancel_reason | text NULL | lý do XNK huỷ duyệt |
| approver_id | bigint unsigned NULL, FK employees | PTKD |
| xnk_approver_id | bigint unsigned NULL, FK employees **ON DELETE SET NULL** | XNK |
| approved_time | datetime NULL | |
| xnk_approved_time | timestamp NULL | |
| status | int NOT NULL | 1..9 (xem 4.1) |
| company_id | bigint unsigned NOT NULL, FK companies | công ty phiếu = công ty người lập |
| department_id | bigint unsigned NOT NULL, FK departments | |
| part_id | bigint unsigned NULL | không có FK |
| created_by | NOT NULL FK employees · updated_by NULL FK employees | |
| received_time | datetime NULL | lúc gửi |
| brand_id, manufacture_id | bigint (**signed**) NULL, không FK | 18 / 20 dòng NULL |
| send_company_id | bigint NULL, không FK | 18 dòng NULL |

Index: chỉ có index của các FK (approver_id, company_id, department_id, created_by, updated_by, xnk_approver_id). **Không có index trên `status`, `created_at`, `brand_id`/`manufacture_id`**.

**`price_asking_request_products`** — 6.729 dòng. Gồm parent_id (FK), product_id (FK products), `product_name`, `code`, **`unit_id` NOT NULL FK units**, **`unit_name` NOT NULL**. Không có SL, không có giá, không có ghi chú. Index trên parent_id, product_id, unit_id.

**`price_asking_request_approve_histories`** — 19.304 dòng. Gồm `price_asking_request_id` bigint (signed, **không FK, không index**), `created_by` bigint (không FK), `note` text, `type` varchar(255) NOT NULL. `type` là chuỗi tiếng Việt, đếm được: Lập phiếu yêu cầu hỏi giá 4.580 · PTKD duyệt 3.700 · XNK duyệt 3.419 · Lập yêu cầu tính giá 3.158 · Duyệt tính giá 3.120 · PTKD không duyệt 881 · XNK không duyệt 241 · Huỷ duyệt 205.

### 1.2 Yêu cầu tính giá (YCTG)

**`price_calculate_requests`** — 3.147 dòng

| Cột | Kiểu | Ghi chú |
|---|---|---|
| code | varchar NOT NULL | `PYCTG-xxxxx` |
| currency | **varchar(255)** NOT NULL | lưu **id** của `currencies` dưới dạng chuỗi |
| exchange_rate | double(16,2) NOT NULL DEFAULT 1 | |
| note, comment | varchar(255) NULL | `comment` = lý do Kế toán mua hàng trả lại |
| price_asking_request_id | NOT NULL FK price_asking_requests | |
| approver_id (FK employees), approved_time | NULL | |
| status | int NOT NULL | 1..4 |
| company_id / department_id (NOT NULL FK) / part_id | | **chép từ YCHG**: 3.147/3.147 dòng có `company_id` bằng YCHG |
| brand_id, manufacture_id | bigint NULL, không FK | 2 dòng NULL (cả 2 đều nháp) |
| created_by / updated_by | FK employees | 3.130/3.147 dòng `created_by` = `xnk_approver_id` của YCHG |

**`price_calculate_request_products`** — 5.342 dòng. Gồm parent_id FK, product_id FK, product_name, code, unit_id FK (NOT NULL), unit_name, `supplier_price` decimal(16,2) NULL, `supplier_price_exchange` double(16,2), `import_tax` double(8,2), `amount_exchange_after_tax` double(16,2), `chosen` tinyint NOT NULL (1: 5.240 · 0: 102).

**`price_calculate_request_product_costs`** — 5.077 dòng. Gồm parent_id FK → request_products, `price_calculate_request_id` FK, `cost_id` FK costs, cost_name, `value` decimal(10,2) NULL (ngoại tệ), `rate` double(8,2), `value_exchange` double(16,2).

### 1.3 Phiếu tính giá (PTG)

**`price_calculates`** — 3.120 dòng. Gồm code, `currency` varchar, `exchange_rate` decimal(16,2) NOT NULL, `note` varchar(255), `price_calculate_request_id` NOT NULL FK (chỉ có index, **không UNIQUE**), `status` int, company/department/part, created_by/updated_by, brand_id/manufacture_id (không dòng nào NULL).

**`price_calculate_products`** — 4.908 dòng. Gồm parent_id FK, product_id FK, product_name, code, unit_id FK, unit_name, `supplier_price` decimal NOT NULL, `other_cost` decimal NOT NULL, `cost_price` decimal(16,2) DEFAULT 0 (giá nhập kho), `chosen` (1: 4.907 · 0: 1), `import_tax`, `supplier_price_exchange`, `amount_exchange_after_tax`, **`note` text** (đã có sẵn, 32 dòng có nội dung).

**`price_calculate_product_costs`** — 4.789 dòng. Cấu trúc như `request_product_costs`, nhưng FK trỏ `price_calculate_products` + `price_calculates`.

**`price_calculate_product_prices`** — 27.874 dòng. Gồm `price_type_id` FK price_types, parent_id FK, `price_calculate_id` FK, **`price_calculate_request_product_id` NOT NULL FK**, **`price_asking_request_product_id` NOT NULL FK**, `price` decimal(16,2), `coefficient` decimal(5,2), `sale_max_percent` decimal(5,2).

**`price_calculate_product_expected_prices`** — 4.192 dòng. Gồm parent_id FK → product_prices, price_calculate_id FK, price, coefficient, sale_max_percent, `effect_date` date.

### 1.4 Kết quả tính giá (KQ)

**`price_calculate_results`** — 3.119 dòng. Gồm `price_asking_request_id`, `price_calculate_request_id`, `price_calculate_id` (cả 3 NOT NULL FK, **không UNIQUE**), `requester_id` FK employees, created_by/updated_by. Không có mã phiếu. Kiểm tra: không YCHG nào có quá 1 KQ, không KQ nào thiếu dòng hàng.

**`price_calculate_result_products`** — 4.906 dòng. Gồm parent_id FK, product_id FK, product_name, code, unit_id FK, unit_name. **Không có `note`.**

**`price_calculate_result_product_prices`** — 27.863 dòng. Gồm price_type_id FK, parent_id FK, price / coefficient / sale_max_percent (đều NOT NULL).

**`price_calculate_result_product_expected_prices`** — 4.191 dòng. Gồm parent_id FK, price, coefficient, sale_max_percent, effect_date (đều NOT NULL).

### 1.5 Ràng buộc ảnh hưởng tới thiết kế

- `price_calculate_product_prices` bắt buộc nối được về **dòng YCTG** và **dòng YCHG**. Khi YCHG chỉ lưu 1 dòng cho mỗi mã hàng (không có ĐVT), các dòng giá theo từng ĐVT vẫn trỏ về được dòng hàng đó (quan hệ n–1). Không cần sửa bảng.
- `price_asking_request_products.unit_id` / `unit_name` đang NOT NULL. Đây là chỗ duy nhất xung đột với Q9.
- Chưa có UNIQUE nào đảm bảo "1 YCTG – 1 PTG" hay "1 PTG – 1 KQ". Dữ liệu hiện tại không có dòng trùng, nên **thêm UNIQUE được ngay**.
- `product_approves` (G5) **không có cột nào trỏ về chứng từ nguồn**. Dòng `pa`/`pap` còn bị **xoá cứng sau khi duyệt hoặc từ chối** (`ProductPriceApprovalService.php:454-455, 575-576`). Vì vậy PTG không có cách biết giá của mình đã được duyệt hay chưa, nếu không thêm cột nối (xem 2.6).

---

## 2. Đề xuất thay đổi CSDL tối thiểu

Nguyên tắc:
- Migration đặt ở HRM, theo khuôn G1: có guard `Schema::hasColumn` / `hasTable`, đặt trong `Modules/<module>/Database/Migrations`.
- Không đổi nghĩa giá trị cũ, không xoá cột cũ.
- Cột mới đều NULL được, để dòng ERP cũ vẫn hợp lệ.

### 2.1 Bảng mới `price_asking_request_groups` (nhóm Thương hiệu – Hãng của YCHG)

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| id | bigint unsigned PK | |
| price_asking_request_id | bigint unsigned NOT NULL, FK price_asking_requests | |
| company_id | bigint unsigned NOT NULL, FK companies | chép từ phiếu, để lọc hàng chờ của XNK cho nhanh |
| brand_id, manufacture_id | bigint unsigned NOT NULL | **chụp lúc lưu**: hàng có đổi hãng về sau thì nhóm vẫn giữ |
| sort_order | int | STT La Mã |
| xnk_employee_id | bigint unsigned NULL, FK employees | **chụp** người mua phụ trách (`assign_histories.buy_employee_id`, `employee_date_to IS NULL`, theo thương hiệu × hãng × công ty phiếu) lúc gửi. Bàn giao công việc thì cập nhật cột này (K7) |
| status | tinyint NULL | NULL = chưa tới tay XNK (phiếu đang tạo / chờ PTKD / bị PTKD trả). Các giá trị khác ở 2.4 |
| xnk_note | text NULL | ghi chú XNK khi duyệt |
| xnk_approved_by, xnk_approved_at | NULL | XNK duyệt nhóm |
| close_reason | text NULL | lý do "Không có giá" / "Huỷ duyệt" (bắt buộc) |
| closed_by, closed_at | NULL | |
| priced_at | datetime NULL | lúc giá được áp, nhóm thành Đã tính giá |
| created_by/updated_by + timestamps | | khuôn BaseModel |

- Index: `UNIQUE(price_asking_request_id, brand_id, manufacture_id)`, `(xnk_employee_id, status)` cho hàng chờ của XNK, `(company_id, status)`.
- Thêm cột **`group_id`** (bigint unsigned NULL, FK groups, có index) vào:
  - `price_asking_request_products`: dòng hàng thuộc nhóm nào, chụp lúc lưu.
  - `price_calculate_requests`: YCTG của nhóm. Thêm **UNIQUE(group_id)** để đảm bảo 1 nhóm – 1 YCTG. MySQL cho phép nhiều NULL trong UNIQUE, nên dòng cũ chưa backfill vẫn hợp lệ.
  - `price_asking_request_approve_histories`: log thao tác theo nhóm (XNK duyệt / Không có giá / Huỷ duyệt / Lập YCTG / áp giá). Log của cả phiếu (lập phiếu, PTKD) để `group_id` NULL. Thêm luôn index `price_asking_request_id`, hiện bảng chưa có.
- Thời điểm sinh nhóm: tính lại mỗi lần lưu khi phiếu ở trạng thái Đang tạo / Không duyệt. Cố định từ lúc gửi đi.

### 2.2 Phần đầu YCHG (`price_asking_requests`) với phiếu mới

| Cột | Phiếu mới (HRM) | Hệ quả |
|---|---|---|
| brand_id, manufacture_id | **để NULL**. Nhóm là nguồn duy nhất | HRM không đọc 2 cột này, trừ lúc backfill. ERP chỉ đọc ở thẻ dashboard XNK, mà thẻ đó đề xuất bỏ (3.4) |
| send_company_id | **để NULL** (Q3 bỏ ô "Gửi tới công ty") | Phiếu cũ giữ nguyên giá trị |
| approver_comment, xnk_approver_id, xnk_approved_time, cancel_reason | phiếu mới không dùng, đã chuyển xuống nhóm | backfill chép xuống nhóm. Phần đầu phiếu cũ giữ nguyên |
| comment, approver_id, approved_time | vẫn dùng cho PTKD (duyệt cả phiếu, Q19) | |
| company_id | lấy **công ty đang làm việc** của người lập (§23c `company_role`), không lấy `info->company_id` như ERP `boot()` | |
| status | thêm **10 = Đang hỏi giá** | xem 2.4 |

### 2.3 Dòng hàng YCHG: bỏ chọn ĐVT (Q9)

Có 2 cách:

| Cách | Làm gì | Hệ quả |
|---|---|---|
| **A (đề xuất)** | `ALTER ... MODIFY unit_id bigint unsigned NULL, unit_name varchar(255) NULL` (giữ FK) | Phiếu mới lưu NULL, nghĩa là "mọi ĐVT". Phiếu cũ vẫn hiện ĐVT đã hỏi. ERP còn đọc `unit_name` ở màn show / bản in, nhưng các màn đó đã bị chặn |
| B | Không đổi kiểu cột, phiếu mới ghi ĐVT cơ sở (`product_units.is_base=1`) | Không cần DDL, nhưng dữ liệu sai nghĩa: tưởng chỉ hỏi ĐVT cơ sở. 124/6.729 dòng cũ là hàng nhiều ĐVT |

Số liệu: 45.300 hàng có 1 ĐVT, 508 hàng có 2, 80 hàng có 3, 1 hàng có 4. YCTG/PTG luôn bung đủ ĐVT: mỗi ĐVT 1 dòng `*_products`, `chosen` luôn = 1.

### 2.4 Mã trạng thái (không đè giá trị cũ)

**YCHG — phần đầu phiếu** (ERP đang dùng 1–9):

| Mã | Nhãn HRM | Ghi chú |
|---|---|---|
| 3 | Đang tạo | giữ |
| 2 | Chờ PTKD duyệt | giữ |
| 8 | Không duyệt | giữ. Người lập sửa rồi gửi lại |
| **10** | **Đang hỏi giá** | **mới**: PTKD đã duyệt, còn nhóm chưa đóng |
| 4 | Đã tính giá | giữ: mọi nhóm đã đóng, có ít nhất 1 nhóm đã tính giá |
| 9 | Không có giá | giữ mã, đổi nghĩa thành "mọi nhóm đều đóng mà không nhóm nào có giá" |
| 5, 1, 7 | (mã cũ) → hiện **"Đang hỏi giá"** | chỉ có ở phiếu cũ, HRM gộp vào bộ lọc "Đang hỏi giá" (`status IN (1,5,7,10)`) |
| 6 | (mã cũ) "Huỷ duyệt" | chỉ có ở phiếu cũ, coi là đã đóng (xem câu hỏi C3) |

**Nhóm** (bảng mới, nên tự chọn mã). Đề xuất **trùng số với mã YCHG ERP có cùng nghĩa**, để backfill chỉ cần chép mã:

| Mã | Nhãn |
|---|---|
| NULL | chưa tới tay XNK |
| 5 | Chờ XNK duyệt |
| 1 | Chờ lập YCTG |
| 7 | Đang tính giá (đã có YCTG, nháp cũng tính) |
| 4 | Đã tính giá |
| 9 | Không có giá (đóng) |
| 6 | Huỷ duyệt (đóng) |

**YCTG** (ERP dùng 1–4):

| Mã | Nhãn HRM |
|---|---|
| 3 | Đang tạo |
| 2 | Chờ tính giá (giữ nghĩa "đã gửi Kế toán mua hàng") |
| **5** | **Không duyệt** (mới. ERP cũ trả về 3, nên phân biệt được qua `comment`) |
| 1 | **Đang tính giá** (giữ nghĩa "đã có PTG", chỉ đổi nhãn. Dòng cũ duy nhất có mã 1 cũng đang có PTG nháp, khớp nghĩa) |
| **6** | **Chờ duyệt giá** (mới) |
| 4 | Đã tính giá |

Cột thêm: `rejected_by`, `rejected_at`. Lý do không duyệt dùng lại `comment` varchar(255), giống ERP. Nếu cần dài hơn thì thêm `reject_reason text`.

**PTG** (ERP chỉ dùng 1, 3):

| Mã | Nhãn |
|---|---|
| 3 | Đang tạo |
| **5** | **Chờ duyệt giá** (mới) |
| **6** | **Giá bị từ chối** (mới, mở lại cho sửa) |
| 1 | Đã duyệt |

Tránh dùng mã 2 vì YCTG đang dùng mã 2, dễ nhầm.

### 2.5 Chụp chính sách nội bộ vào dòng PTG (Q13) + ghi chú dòng

- **Ghi chú dòng:** `price_calculate_products.note` (text) **đã có**, không cần thêm. Q10: không ghi đè `products.note`. Nếu bản in kết quả hoặc drill trong YCHG cần hiện ghi chú, thêm `note text NULL` vào `price_calculate_result_products` (tuỳ chọn). YCHG / YCTG chỉ có ghi chú ở phần đầu phiếu (`note` đã có).
- **Chụp chính sách**, thêm vào `price_calculate_products`. Tất cả NULL được; NULL hết nghĩa là hàng của chính công ty phiếu, không có giá mua nội bộ:

| Cột | Kiểu | Ý nghĩa (theo `chupCS()` của mockup) |
|---|---|---|
| policy_owner_company_id | bigint unsigned NULL | công ty quản lý hàng lúc chụp |
| policy_manufacture_id | bigint unsigned NULL | hãng dùng tra chính sách |
| policy_base_type | tinyint NULL | 1 = Theo giá vốn · 2 = Theo giá bán. NULL kèm owner khác công ty phiếu nghĩa là "Chưa cấu hình" |
| policy_percent_import_lot, policy_percent_stock | decimal(8,2) NULL | 2 tỉ lệ |
| policy_owner_cost_price | decimal(16,2) NULL | giá vốn của công ty quản lý lúc chụp. **Chỉ trả cho người có quyền 1092** (Q12). BE trả null, FE hiện "—" |
| policy_owner_prices | json NULL | 6 giá bán của công ty quản lý `{price_type_id: price}` lúc chụp |
| policy_captured_at | datetime NULL | chụp lúc lưu PTG; phiếu đã duyệt hiện số đã chụp |

  Có thể dồn cả khối vào 1 cột json `internal_policy_snapshot`. Đề xuất **dùng cột rời**, để BE dễ xoá riêng giá vốn khi người xem không có 1092, không phải lọc trong json.

### 2.6 Nối PTG với Duyệt giá bán G5 (Q5)

Khi công ty bật quy chế duyệt, PTG đẩy giá sang `product_approves`, mỗi (hàng × ĐVT × công ty) 1 yêu cầu. Lúc duyệt hoặc từ chối, G5 xoá dòng `pa`. Cần thêm:
- `product_approves.price_calculate_id` bigint unsigned NULL + index. G5 dựa vào cột này để báo ngược về PTG.
- Ở `price_calculate_products` thêm: `approval_status` tinyint NULL (NULL = không qua duyệt · 1 chờ · 2 đã duyệt · 3 bị từ chối), `approval_comment` text NULL (chép lý do từ chối **trước khi** G5 xoá `pa`), `approval_decided_at`.
- `ProductPriceApprovalService::approve()/reject()` cần gọi lại PTG:
  - Mọi dòng đã duyệt: PTG → 1, YCTG → 4, nhóm → 4, sinh KQ, YCHG kiểm xem đã đủ nhóm chưa.
  - Có dòng bị từ chối: PTG → 6.
  - Đây là thay đổi vào code G5 đã xong, cần ghi vào design.

### 2.7 UNIQUE và index nên thêm (bảng cũ, dữ liệu không trùng)

- `price_calculates.price_calculate_request_id` UNIQUE (1 YCTG – 1 PTG).
- `price_calculate_results.price_calculate_id` UNIQUE.
- `price_asking_requests (company_id, status)`.
- `price_asking_request_approve_histories.price_asking_request_id`.

### 2.8 Phiếu cũ: backfill nhóm hay đọc ảo?

| | Backfill (đề xuất) | Đọc ảo |
|---|---|---|
| Làm gì | Lệnh artisan chạy 1 lần lúc go-live, chạy lại được, có `--dry-run`. Sinh **4.029** nhóm (mỗi phiếu 1 nhóm), gán `group_id` cho 6.729 dòng hàng, 3.147 YCTG và log nhóm | Không ghi gì. Phiếu không có nhóm thì dựng 1 nhóm giả từ phần đầu phiếu |
| Ưu | 1 nguồn sự thật. Danh sách "x/n nhóm", hàng chờ của XNK, gate theo nhóm, bộ lọc chỉ cần 1 câu truy vấn. `group_id` của YCTG làm UNIQUE được. 21 phiếu đang dở xử lý tiếp như phiếu mới | Không đụng dữ liệu cũ |
| Nhược | Ghi khoảng 18.000 dòng (nhóm + gán `group_id`) | Mọi truy vấn phải có 2 nhánh (UNION hoặc COALESCE), dễ ra số sai âm thầm (bài học gộp DB). Gate theo nhóm không có id để gắn. Phiếu cũ đang dở không có chỗ ghi trạng thái nhóm |

Quy tắc backfill (đối chiếu dữ liệu thật):

| Trường của nhóm | Lấy từ | Ca đặc biệt |
|---|---|---|
| brand_id / manufacture_id | **phần đầu phiếu** | 20 phiếu NULL (13 nháp, 5 st1, 1 st5, 1 st6): lấy hãng hiện tại của dòng hàng đầu tiên. **4 phiếu có hàng đã đổi hãng sau khi hỏi** (PYCHG-00019, 00241, 00669 nháp; PYCHG-02766 đã tính giá, 8 mã hiện thuộc thương hiệu 207 thay vì 782): vẫn gom 1 nhóm theo phần đầu phiếu, **không tách** |
| status | mã phần đầu phiếu nếu thuộc {5,1,7,4,9,6}; 2/3/8 thì NULL | 6 phiếu st1 đã có YCTG nháp: nhóm = **7** |
| xnk_employee_id | `xnk_approver_id`; nếu NULL thì phân công hiện hành theo `send_company_id`; vẫn không có thì theo `company_id` | xem 4.3 (phiếu chéo công ty) |
| xnk_note / close_reason | `approver_comment` (duyệt hoặc không có giá) / `cancel_reason` (huỷ) | |
| priced_at | `price_calculate_results.created_at` | |
| log | các type XNK duyệt / XNK không duyệt / Huỷ duyệt / Lập yêu cầu tính giá / Duyệt tính giá: gán `group_id` của nhóm duy nhất | |
| YCTG | 21 YCTG st3 có `comment` mà YCHG đang st7 (nghĩa là bị Kế toán trả): **3 → 5** | 2 YCTG st3 có comment nhưng YCHG st1 (từ 2024 / 02/2026): giữ 3 |

Phần đầu phiếu cũ **không ghi lại trạng thái**: HRM đổi 1/5/7 thành "Đang hỏi giá" lúc đọc (đọc ảo ở mức phần đầu phiếu, ít rủi ro vì chỉ 1 bảng). 6 giữ nhãn "Huỷ duyệt" cho phiếu cũ.

---

## 3. Chặn ERP

### 3.1 Middleware `productMovedToHrm` (G6) hoạt động thế nào

`app/Http/Middleware/ProductMovedToHrm.php`, alias ở `app/Http/Kernel.php:78`, gắn **cho từng route** (không gắn cho cả group), đứng trước `checkPermission`:
- Tham số là khoá đích trong `TARGETS`. `buildHrmUrl($target, $id)` = `config('app.hrm_url_FE')` + đường đích. `{id}` lấy từ tham số route `id` (phải là số); không có id thì về `FALLBACK_PATH`.
- GET/HEAD gõ thẳng trên trình duyệt: trả view `errors.moved_to_hrm` (403), có nút "Mở trên HRM". POST, AJAX, expectsJson: trả JSON 403 `{success:false, message, redirect_url}`.
- `PRICE_TARGETS` quyết định câu mô tả trên trang báo (luồng giá hay luồng thông tin hàng).

Cần thêm (tên đường HRM là đề xuất, chốt ở design):

```php
'price-asking'            => '/finance/price-asking-requests/{id}',
'price-asking-list'       => '/finance/price-asking-requests',
'price-calc-request'      => '/finance/price-calculate-requests/{id}',
'price-calc-request-list' => '/finance/price-calculate-requests',
'price-calculate'         => '/finance/price-calculates/{id}',
'price-calculate-list'    => '/finance/price-calculates',
```

- Thêm các khoá này vào `PRICE_TARGETS`, hoặc tạo cờ riêng để trang báo ghi "Hỏi giá / tính giá nay làm trên HRM".
- `FALLBACK_PATH` hiện cố định là danh sách hàng hoá. Cần **mỗi khoá có đích dự phòng riêng** (ví dụ khoá `price-asking` không có id thì về danh sách YCHG). Đây là sửa nhỏ trong `buildHrmUrl`.
- `id` dùng chung được vì HRM đọc cùng bảng, nên `/admin/orders/price_asking_requests/123/show` ⇒ `/finance/price-asking-requests/123`.
- **KQ**: `{id}` của route là id KQ, còn HRM mở KQ trong YCHG (Q20). Có 2 cách:
  - Middleware tra `price_calculate_results.price_asking_request_id` rồi trỏ `…/price-asking-requests/{asking}?group={gid}`. Cần thêm hàm resolver.
  - Trỏ về danh sách YCHG. Đơn giản nhưng mất ngữ cảnh.

### 3.2 Route phải chặn (giữ nguyên tên; `routes/web.php:2246-2295` + `:600`)

| Nhóm | Route (tên) | Khoá đích |
|---|---|---|
| YCHG (16) | `PriceAskingRequest.index`, `.create`, `.searchData` | `price-asking-list` |
| | `.edit`, `.delete`, `.show`, `.print`, `.update`, `.approve`, `.reject`, `.approveXNK`, `.rejectXNK`, `.cancelApprove`, `.getDataForPriceCalculate` (có `{id}`) | `price-asking` |
| | `.store` | `price-asking-list` |
| YCTG (11) | `PriceCalculateRequest.index`, `.create`, `.store`, `.searchData` | `price-calc-request-list` |
| | `.edit`, `.delete`, `.show`, `.print`, `.update`, `.reject`, `.getDataForPriceCalculate` | `price-calc-request` |
| PTG (9) | `PriceCalculate.index`, `.create`, `.store`, `.searchData` | `price-calculate-list` |
| | `.edit`, `.delete`, `.show`, `.print`, `.update` | `price-calculate` |
| KQ (4) | `PriceCalculateResult.index`, `.searchData` | `price-asking-list` |
| | `.show`, `.print` | resolver KQ ⇒ YCHG (hoặc danh sách) |
| Phụ trợ (1) | `product.getDataForPriceAsking` (`:600`, JSON cho form YCHG) | `price-asking-list` |

Tổng **41 route**. Middleware phải đứng **trước** `checkPermission` có sẵn ở `PriceCalculateRequest.create/edit`.

Chặn xong thì các lỗi cũ (xoá PTG không kiểm quyền, in PTG 404, in KQ 500, PTKD duyệt 500) tự hết vì không còn đường vào.

### 3.3 Menu `resources/views/layouts/topmenubar.blade.php`

Làm theo khuôn G6 (dòng 932, 2225): `rtrim(config('app.hrm_url_FE'),'/') . '<đường>'`, `target="_blank" rel="noopener"`, nhãn thêm "(HRM)".

| Dòng | Hiện tại | Đổi thành |
|---|---|---|
| 327 | `route('PriceAskingRequest.index')` "Phiếu Yêu cầu hỏi giá" | `/finance/price-asking-requests` |
| 931 | `route('PriceCalculate.index')?type=all` "Phiếu tính giá hàng hóa" | `/finance/price-calculates` |
| 1534 | `route('PriceAskingRequest.index')` | `/finance/price-asking-requests` |
| 1536 | `route('PriceCalculateRequest.index')` | `/finance/price-calculate-requests` |
| 2383 | `route('PriceAskingRequest.index')?type=approve` "…chờ duyệt" | `/finance/price-asking-requests?…` (tham số lọc "chờ tôi duyệt" chốt theo màn HRM) |

Dòng 1537 đang là comment, không cần đụng.

### 3.4 Ba thẻ dashboard `app/Http/Controllers/HomeController.php:1394-1443`

| Thẻ | Truy vấn hiện tại | Sau khi HRM ghi |
|---|---|---|
| "Yêu cầu hỏi giá chờ duyệt" (quyền ERP `PTKD duyệt…`) | `status=2` + phạm vi xem ERP | Vẫn đếm được (mã 2 giữ nguyên), nhưng phạm vi theo 4 quyền phạm vi ERP mà Q11 đã bỏ, nên **lệch số với HRM** |
| "Yêu cầu hỏi giá cần XNK duyệt" | phần đầu `status=5`, hãng ở phần đầu, `send_company_id` | **Sai hẳn**: phiếu mới không bao giờ có phần đầu = 5 và để NULL hãng / `send_company_id`, nên **luôn ra 0** |
| "Yêu cầu tính giá chờ duyệt" (`Kế toán mua hàng`) | `PriceCalculateRequest::where('status',2)->count()`, không lọc công ty | Mã 2 vẫn đúng nghĩa, nhưng đếm toàn hệ thống |

Ngoài ra, cả 3 thẻ gate bằng **quyền ERP**, còn HRM cấp quyền mới (Q11, id mới). Người có quyền mới không thấy thẻ, người có quyền cũ lại thấy số sai.

Đề xuất **bỏ 3 thẻ khỏi dashboard ERP** (việc chờ xem trên HRM).
- Nếu muốn giữ: làm theo khuôn G6 (link `buildHrmUrl`, giữ số đếm), viết lại thẻ XNK đếm `price_asking_request_groups` (status=5, `xnk_employee_id`=tôi), 2 thẻ còn lại lọc `company_id`. Đã giữ thì phải sửa cùng lúc với chặn route.
- Bỏ thẻ thì bỏ luôn `use PriceAskingRequest/PriceCalculateRequest` nếu không còn chỗ nào dùng.

### 3.5 Các chỗ khác ở ERP đọc bảng

Đã grep `app/ config/ database/seeds/ routes/ resources/views/` (trừ 4 controller, 15 model, view `orders/price_*`):

| Chỗ | Đọc gì | HRM ghi trạng thái mới thì sao |
|---|---|---|
| `Product::checkPriceAsked()` (`app/Product.php:7725`) + bản sao ở `ProductInfo.php:4016`, `ProductTemplate.php:6958` | YCHG phần đầu `status=1` chứa hàng | Phiếu mới không bao giờ có phần đầu = 1, nên trả rỗng. **Vô hại**: chỉ được gọi từ `getDataForPriceAsking` của 4 controller (`ProductsController:3374`, `Product2Controller:1980`, `ProductInfoController:1708`, `ProductTemplatesController:2260`), mà chỉ route của `ProductsController` còn sống và route đó sẽ bị chặn. HRM tự làm cảnh báo "đang có người hỏi giá" theo **nhóm** (status ∈ {5,1,7}) |
| `HomeController` | xem 3.4 | |
| `ProductWriteAuditObserver::WHITELIST_ROUTES` `'PriceCalculate.*'` (`:31`) | | Không vỡ. **Gỡ** sau khi chặn để audit bắt được đường ghi còn sót |
| `database/seeds/UpdateDB.php:763-960` | PTG đã duyệt (`status=1`) | Seeder chạy tay, không chạy lúc runtime. PTG mới vẫn dùng 1 = Đã duyệt nên vẫn đúng nghĩa |
| `partials/classes/sale/ProductPrice.blade.php:91` | chỉ là cờ ngữ cảnh JS | Không liên quan |
| Báo giá / bán hàng / kho / mua hàng | không đọc | Không ảnh hưởng |
| Thông báo cũ trỏ URL ERP | local: 0 dòng `notifications` chứa `price_asking` / `price_calculate` | Production có thể còn. Bấm vào thì ra trang chặn có link HRM |

### 3.6 Cron `product:update_price` (01:00, `app/Console/Kernel.php:47`, `UpdateProductPrice.php`)

- Chỉ đọc `product_expected_prices` có `effect_date = hôm nay`, `status = 2`, `flag != 1 OR NULL`. Ghi `product_unit_prices` theo `unit_price_id` (đã mang `company_id` từ G3), rồi đặt `status = 1`. **Không đọc 15 bảng tính giá.**
- HRM ghi giá hiệu lực qua lớp G4/G5: không qua duyệt thì `status=2, flag=0`; qua duyệt thì chờ với `flag=1`, duyệt xong G5 đặt `status=2, flag=0` (`ProductPriceApprovalService.php:412`). **Khớp quy ước của cron, nên không phải sửa** (giữ K11).
- Lưu ý: cron ghi lịch sử qua `units_for_history` đọc cột cũ. Lỗi này có từ trước, nằm ngoài luồng.

---

## 4. Số liệu tham chiếu + phiếu đang dở

### 4.1 Trạng thái từng bảng (local, tới 15/09/2026)

| YCHG | Nhãn ERP | Số | Tạo từ – tới |
|---|---|---|---|
| 3 | Đang tạo | 376 | 13/01 – 19/08/2026 (chỉ 2 phiếu từ 06/2026) |
| 2 | Chờ PTKD duyệt | 1 | 14/09/2026 |
| 5 | Chờ XNK duyệt | 41 | 28/01 – 15/09 (28 phiếu từ 06/2026) |
| 1 | Chờ XNK hỏi giá | 73 | 08/10/2024 – 14/09/2026 (59 phiếu từ 06/2026) |
| 7 | Chờ tính giá | 22 | 04/02 – 10/08 (18 phiếu trước 06/2026) |
| 4 | Đã tính giá | 3.119 | |
| 8 | Không duyệt | 171 | |
| 9 | Không có giá | 71 | |
| 6 | Huỷ duyệt | 155 | |

- YCTG: 3 Đang tạo **27** · 1 Đã duyệt **1** · 4 Đã tính giá 3.119 · 2 Chờ duyệt **0**.
- PTG: 3 Đang tạo **1** (28/02/2026) · 1 Đã duyệt 3.119.
- KQ: 3.119, bằng đúng số YCHG / YCTG / PTG đã tính giá.

### 4.2 Chuỗi đang dở (YCHG × YCTG × PTG)

| YCHG | YCTG | PTG | Số | Diễn giải |
|---|---|---|---|---|
| 1 | — | — | 67 | XNK đã duyệt, chưa lập YCTG |
| 1 | 3 | — | 6 | YCTG nháp (2 có comment) |
| 5 | — | — | 41 | chờ XNK |
| 7 | 3 | — | 21 | Kế toán **trả** YCTG (đều có comment), YCHG kẹt ở "Chờ tính giá" (lỗi cũ) |
| 7 | 1 | 3 | 1 | PTG nháp từ 28/02 (ca "lưu nháp PTG làm YCTG Đã duyệt") |
| 2 | — | — | 1 | chờ PTKD |
| 3 | — | — | 376 | nháp |
| 6 / 8 / 9 | — | — | 155 / 171 / 71 | ERP cho người lập sửa và gửi lại |

### 4.3 Phiếu hỏi chéo công ty (vướng Q3/Q4 "cả luồng 1 công ty")

`company_id × send_company_id` của toàn bộ phiếu: (1,1) 2.839 · (4,1) 931 · (3,1) 184 · (4,4) 20 · (1,NULL) 17 · (8,1) 12 · (1,2) 11 · …

Trong số phiếu đang dở:

| YCHG | cùng công ty | khác công ty | `send` NULL |
|---|---|---|---|
| 1 | 51 | 17 | 5 |
| 5 | 30 | 11 | 0 |
| 7 | 20 | 2 | 0 |
| 2 | 1 | 0 | 0 |

Có phân công hiện hành theo **công ty phiếu** (quy tắc mới) hay không:

| YCHG | Có phân công | Tổng |
|---|---|---|
| st1 | 51 | 73 |
| st5 | 31 | 41 |
| st7 | 20 | 22 |

Nếu tra theo `send_company_id` thì lần lượt là 68 / 39 / 22.

Hệ quả: với **30 phiếu đang dở hỏi chéo**, XNK và Kế toán thật ra là người của công ty 1. Theo Q11 ("xét quyền trong công ty phiếu") họ không có quyền trong công ty 4, nên phiếu kẹt. Theo Q4, duyệt PTG ghi giá cho công ty phiếu (4), khác với ERP (ghi cho công ty quản lý hàng, thường là 1).

### 4.4 Đề xuất xử lý lúc go-live

1. **T-7 ngày**: xuất danh sách phiếu đang dở (SQL bên dưới chạy trên production), báo PTKD / XNK / Kế toán mua hàng **xử lý xong ở ERP**: duyệt nốt, tính nốt, hoặc huỷ / không có giá. Ưu tiên 30 phiếu chéo công ty và 21 YCTG bị trả.
2. **Ngày chuyển**: chặn ERP (mục 3) và chạy backfill nhóm (2.8) **trong cùng một lần deploy** (K: lên prod một lần, không đường lui).
3. Phiếu **còn dở** sau bước 1:
   - Cùng công ty: xử lý tiếp ở HRM như phiếu 1 nhóm. Nhóm giữ `xnk_employee_id` đã chụp.
   - Chéo công ty: chọn 1 trong 3 cách (câu C1).
   - Phiếu cũ đang dở trước 06/2026 (st1: 14, st5: 13, st7: 18): đề xuất **đóng hàng loạt** (nhóm → 6 Huỷ duyệt, `close_reason` = "Đóng khi chuyển sang HRM", có log) nếu nghiệp vụ đồng ý.
4. **376 phiếu nháp** (gần hết trước 06/2026): giữ nguyên. Người lập mở trong HRM thì nhóm được tính lại khi lưu và áp quy tắc mới (chặn nhóm chưa phân công). Có thể xoá hàng loạt phiếu nháp quá 90 ngày (câu C4).
5. 1 PTG nháp (28/02) + YCTG st1 đi kèm: đề xuất xoá PTG nháp (trả YCTG về 2, nhóm về 7), hoặc để Kế toán mở tiếp ở HRM.

SQL kiểm trên production (chỉ đọc):

```sql
SELECT a.status ychg, r.status yctg, c.status ptg, (a.company_id<>a.send_company_id) cheo, COUNT(*)
FROM price_asking_requests a
LEFT JOIN price_calculate_requests r ON r.price_asking_request_id=a.id
LEFT JOIN price_calculates c ON c.price_calculate_request_id=r.id
WHERE a.status NOT IN (4) GROUP BY 1,2,3,4;
SELECT COUNT(*) FROM (SELECT price_calculate_request_id FROM price_calculates GROUP BY 1 HAVING COUNT(*)>1) x; -- phải =0 trước khi thêm UNIQUE
SELECT COUNT(*) FROM (SELECT price_calculate_id FROM price_calculate_results GROUP BY 1 HAVING COUNT(*)>1) x;  -- phải =0
SELECT COUNT(*) FROM price_asking_requests WHERE brand_id IS NULL OR manufacture_id IS NULL;           -- ca backfill đặc biệt
```

---

## 5. Rủi ro

| # | Rủi ro | Giảm thiểu |
|---|---|---|
| R1 | Đọc ảo nhóm (nếu không backfill) làm mọi truy vấn có 2 nhánh và ra số sai âm thầm | Backfill |
| R2 | G5 xoá `pa` sau khi quyết, nên PTG không biết giá đã được duyệt hay bị từ chối | Cột `product_approves.price_calculate_id` + gọi lại từ G5 + chép lý do sang dòng PTG |
| R3 | Duyệt từng phần ở G5 (1 ĐVT duyệt, 1 ĐVT từ chối) không có trạng thái PTG tương ứng | Chốt câu C5 |
| R4 | Đang có yêu cầu G4 chờ duyệt cho cùng (hàng × ĐVT × công ty) lúc PTG gửi duyệt. ERP chặn bằng truy vấn không lọc công ty | HRM chặn hoặc thay thế, có lọc `company_id` (câu C6) |
| R5 | 30 phiếu chéo công ty đang dở bị kẹt quyền, hoặc ghi giá sang công ty khác với ERP | Dọn trước go-live + câu C1 |
| R6 | 3 thẻ dashboard ERP ra số sai (thẻ XNK luôn 0) | Bỏ thẻ, hoặc viết lại cùng lúc với chặn route |
| R7 | Xoá route ERP làm vỡ mọi trang (menu gọi `route()`) | Chỉ gắn middleware, giữ tên route |
| R8 | Thêm UNIQUE trên production mà có dòng trùng thì migration fail | Chạy SQL 4.4 trước. Migration có guard |
| R9 | `price_asking_request_products.unit_id` chuyển sang NULL thì code ERP đọc `unit_name` lỗi | ERP đã chặn các màn đó. HRM hiện "Mọi ĐVT" |
| R10 | Đổi người phụ trách hãng giữa chừng mà `xnk_employee_id` đã chụp thì nhóm kẹt ở người cũ | Bàn giao công việc phải cập nhật cột này (K7), hoặc chọn tra động (câu C2) |
| R11 | `policy_owner_cost_price` lộ giá vốn | BE xoá cột này khi người xem không có 1092, có test cả 2 ca có quyền và không quyền |

---

## 6. Câu hỏi cần user chốt

- **C1 — Phiếu chéo công ty đang dở lúc chuyển (30 phiếu):** (a) bắt dọn xong ở ERP, còn sót thì đóng hàng loạt; (b) cho xử lý tiếp ở HRM theo quy tắc mới (XNK / Kế toán của công ty phiếu, giá ghi cho công ty phiếu); (c) giữ người cũ đã chụp và nới quyền riêng cho phiếu cũ. Đề xuất (a).
- **C2 — Người XNK của nhóm:** chụp lúc gửi (Bàn giao công việc cập nhật), hay tra phân công hiện hành mỗi lần như ERP `isAssignedBuyer`? Đề xuất chụp.
- **C3 — Nhóm đóng (Không có giá / Huỷ duyệt):** người lập có được sửa và gửi lại phiếu không (ERP cho sửa phiếu 6/9)? Hay phải lập phiếu mới? Với phiếu nhiều nhóm thì gửi lại chỉ nhóm đóng hay cả phiếu?
- **C4 — Phiếu cũ:** đồng ý backfill nhóm (4.029 nhóm)? Đóng hàng loạt phiếu đang dở trước 06/2026? Xoá phiếu nháp quá 90 ngày (376 nháp, gần hết trước 06/2026)?
- **C5 — PTG qua G5 duyệt từng phần:** 1 dòng bị từ chối thì cả PTG → "Giá bị từ chối" và các dòng đã duyệt vẫn áp? Hay G5 bắt duyệt / từ chối cả PTG cùng lúc?
- **C6 — Hàng đang có yêu cầu G4 chờ duyệt** cùng (hàng × ĐVT × công ty): PTG chặn gửi duyệt hay thay thế yêu cầu cũ?
- **C7 — 3 thẻ dashboard ERP:** bỏ (đề xuất) hay viết lại trỏ HRM?
- **C8 — Đường dẫn HRM** `/finance/price-asking-requests`, `/finance/price-calculate-requests`, `/finance/price-calculates`: đồng ý vị trí `finance` (cạnh `product-prices`, `product-price-approvals`)? Hay đặt theo cụm menu trong mockup?
- **C9 — ĐVT ở YCHG:** cách A (`unit_id` NULL được, đề xuất) hay cách B (ghi ĐVT cơ sở)?
