# Phase 2d — Chuyển 3 danh mục cây catalog sang HRM (Chương · Mục · Tiểu mục)

> Mở 04/10/2026. Nguồn quyết định: `../man-danh-muc-hang-hoa/design.md` §30 (cây 4 cấp), §33w (đổi tên
> Mục / Tiểu mục), §35h H2–H4 (làm 2d trước, ẩn data cũ, `scope_id` nullable).
> Plan: `plan.md` cùng thư mục.

## 1. Vì sao làm trước màn hàng hoá

Form hàng hoá bắt buộc ≥ 1 nhánh catalog đủ 4 cấp (§33b, C5-a). Cây catalog dưới gốc mới **đang rỗng**
(§30d: data cũ bỏ, khai lại) ⇒ chưa có 3 màn này thì không lưu được hàng hoá nào (H2).

## 2. Cây

| Cấp | Tên hiển thị | Bảng | Cột cha | Ghi chú |
|---|---|---|---|---|
| 1 | Lĩnh vực Công ty kinh doanh | `internal_business_scopes` (HRM, 8 dòng, trạng thái **1/2**) | — | màn có sẵn `/assign/internal-business-scopes` |
| 2 | **Chương** | `chapters` (ERP, trạng thái **1/0**) | `internal_business_scope_id` **(cột mới)** | `scope_id` cũ trỏ `scopes` ERP |
| 3 | **Mục** | `job_groups` (ERP, 1/0) | `chapter_id` | tên bảng giữ nguyên (§33w) |
| 4 | **Tiểu mục** | `job_clusters` (ERP, 1/0) | `group_id` → `job_groups` | ⚠️ `group_id` KHÔNG trỏ `groups` |

Cả 3 bảng ERP: không có `code`, không có `description`; `created_by` NOT NULL FK `employees`.

## 3. Quyết định

| # | Chốt | Nguồn |
|---|---|---|
| D1 | Thêm `chapters.internal_business_scope_id` (nullable, FK `internal_business_scopes`) | §30b-1, H3 |
| D2 | Bỏ NOT NULL của `chapters.scope_id` (giữ FK). Chương mới: `scope_id = NULL` | H4 |
| D3 | **Ẩn data cũ khỏi HRM, không xoá**: Chương chỉ hiện khi có `internal_business_scope_id`; Mục chỉ hiện khi Chương cha hiện; Tiểu mục chỉ hiện khi Mục cha hiện. Áp bằng **global scope trên entity HRM** ⇒ danh sách, `getAll`, mở chi tiết theo id (404), rule cha đều tự loại data cũ | H3 |
| D4 | Theo khuôn **danh mục Xe** (Phase 2b): `BaseCatalog*` + trạng thái 1/0 + unique tên **theo cha, chỉ so bản ghi đang hoạt động** + chặn mở khoá sinh trùng tên + cờ `children_exists` chống N+1 | khảo sát 04/10 |
| D5 | Tên tối đa **64** ký tự — đúng rule ERP (`ChaptersController:54-59`), vì màn ERP cũ còn sống và vẫn sửa được các dòng này | ERP |
| D6 | Khoá: chỉ khoá được khi **không còn con đang hoạt động** (ngữ nghĩa cây Phase 0, `activeChildrenCount` thật). Mở khoá: chỉ khi cha đang hoạt động. Xoá: chỉ khi không có con nào (xoá cứng — bản ghi mới chưa ai dùng) | khuôn nền |
| D7 | Lĩnh vực Công ty kinh doanh: thêm Chương vào điều kiện **xoá** (có Chương ⇒ không xoá) và **khoá** (có Chương đang hoạt động ⇒ không khoá) — 3 đường: `isCanDelete`, `isCanLockUpdate`, `InternalBusinessScopeController@delete` | khuôn nền |
| D8 | 6 quyền **1670–1675** (`Xem/Quản lý danh mục chương · mục · tiểu mục`), type 9, group `Danh mục hàng hóa` | §30b-3 |
| D9 | Menu Danh mục chung: nhóm mới **"Catalog kinh doanh"** (`subItems`): Chương → Mục → Tiểu mục. Mục *Lĩnh vực Công ty kinh doanh* giữ chỗ cũ | §30b-7 |
| D10 | Không làm Import đợt này (giống Xe) — chưa có yêu cầu | — |
| D11 | Slug = tên bảng: `chapters` · `job-groups` · `job-clusters` (bài học `vehicle-life`) | Phase 2b |

## 4. Ngoài phạm vi

Xoá data cũ + `product_group_classifies` + sửa `Product::searchByFilter` (§30d bước 3, §30e) ·
gỡ 3 màn ERP · bảng `product_business_catalogs` và việc đếm hàng hoá làm "con" của Tiểu mục (làm ở
màn hàng hoá — khi đó bổ sung vào `childrenCount()` của Tiểu mục).

## 5. Rủi ro đã biết

- Màn ERP Chương/Nhóm CV/Cụm CV **còn sống** ⇒ người dùng ERP vẫn thấy + sửa được dòng mới (dòng mới
  `scope_id = NULL` ⇒ ERP nhóm theo lĩnh vực sẽ không hiện chúng dưới lĩnh vực nào). Chấp nhận tới khi gỡ màn ERP.
- ERP "xoá" = `status = 0` và danh sách ERP ẩn `status = 0` ⇒ khoá ở HRM = biến mất bên ERP. Chấp nhận.
