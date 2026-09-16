# Import / Export cho các màn Danh mục đã chuyển ERP → HRM

**Người phụ trách:** @junfoke — 2026-09-10
**Nhánh:** `feat/catalog-import-export` (tách từ `gop_db`)
**Spec đầy đủ:** [docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md](../../../docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md)
**Plan:** [plan.md](plan.md)

---

## Mục tiêu

Người dùng khai báo danh mục hàng loạt bằng file Excel thay vì gõ tay từng bản ghi, và lấy dữ
liệu danh mục ra file theo đúng bộ lọc đang xem.

## Scope

- **Thêm Import — 13 màn**: finance (currencies, account-banks, works, cost-debts,
  source-capitals), human (nations, areas, provinces, wards, banks), customer-care (levels,
  note-maintenances, costs)
- **Thêm Export — 9 màn**: finance (account-banks, works, cost-debts, source-capitals), human
  (nations, areas, provinces, wards, banks)
- **Ngoài scope**: 9 màn Giao việc + finance/accounts + finance/type-accounts (đã đủ cả hai,
  không đụng) · customer-care/serials (màn chỉ đọc) · customer-care/services +
  customer-care/device-errors (trang tạo có bảng chi tiết, file phẳng không chở được)

## Quyết định đã chốt

| # | Quyết định |
| --- | --- |
| Q1 | Import **chỉ thêm mới**. Trùng → dòng đó báo "Đã tồn tại", dòng hợp lệ vẫn được tạo. Không upsert, không all-or-nothing |
| Q2 | File mẫu **sinh động tại FE** từ chính `importColumns` — header file mẫu và bộ nhận diện header của trình đọc dùng một nguồn duy nhất. Cột lấy theo các trường ở màn Tạo mới |
| Q3 | Nâng `FinanceImportMixin.js` → **`CatalogImportMixin.js`** dùng chung (user đã duyệt sửa file dùng chung) |
| Q4 | 9 màn đã có Import **giữ nguyên file mẫu .xlsx tĩnh**, không chuyển sang sinh động |
| Q5 | Nút Import gate **giống hệt nút "Tạo mới" của chính màn đó**; không đủ quyền thì **ẩn nút**, không disable. 5 màn Nhân sự (địa lý + ngân hàng) hiện không gate quyền nào → Import cũng không gate |
| Q6 | Ràng buộc cha tra theo **mã**, không tìm thấy thì báo lỗi dòng. **Không tự tạo bản ghi cha** |
| Q7 | Export màn **Phường/xã dựng ở FE bằng ExcelJS theo lô** (đã đếm: 13.465 dòng); 8 màn còn lại dùng `DynamicExport` ở BE |
| Q8 | Ngân hàng **không import logo** (màn Tạo mới có ô tải ảnh, file Excel không chở được) |
| Q9 | Vụ việc / Mã phí có **ô Mã do người dùng nhập, unique** (`WorkRequest.php:19`) → file mẫu CÓ cột Mã, chống trùng theo mã |
| Q10 | Hàm ghi của import gọi lại **method tạo sẵn có của service** (`createWork()`, `createSourceCapital()`…) chứ không `Model::create()` thẳng, để `logCatalogCreate()` vẫn chạy và Lịch sử thay đổi không bị thủng |

## ⚠️ GOTCHA

- `wards` có **13.465 dòng** — đừng đi đường export ở BE cho màn Phường/xã, sẽ timeout trên
  server đúng như vụ `customer-care/serials` trước đây.
- `FinanceImportMixin.js` đang chạy thật ở `finance/accounts` + `finance/type-accounts`. Đổi tên
  xong phải **test lại 2 màn đó ngay trong Phase 1** trước khi đi tiếp.
- Khoá chống trùng ghi trong spec là **đề xuất theo màn Tạo mới** — phải đối chiếu lại ràng buộc
  `unique` thật trong migration khi làm từng màn (Task 3 Step 7 có sẵn lệnh).
- Đừng đọc nhầm comment `Bắt buộc nhập Mã vụ việc do BE quyết` trong `WorkModal.vue` — câu đó nói
  **ràng buộc bắt buộc nhập do BE áp** (trả 422), KHÔNG phải BE tự sinh mã.
- `currentEmployeeId()` chỉ có ở service extends `FinanceService` (Currency, Account, TypeAccount).
  `WorkService` / `CostDebtService` / `SourceCapitalService` dùng thẳng `auth()->id()`.

## Phase

1. Khung dùng chung (`CatalogImportMixin` + `buildImportTemplate`) + hồi quy 2 màn Tài chính
2. Tài chính — 5 màn Import, 4 màn Export
3. Địa lý + Ngân hàng — 5 màn Import + Export (gồm Export FE cho Phường/xã)
4. CSKH — 3 màn Import
