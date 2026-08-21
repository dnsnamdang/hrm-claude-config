# Thêm option 100 dòng/trang — các màn đã chuyển sang HRM (gop-db)

> Nhánh: `gop_db` · Phụ trách: @khoipv · Ngày: 2026-08-13

## Mục tiêu

Ô chọn **Số dòng/trang** ở các màn danh sách đã port từ ERP sang HRM (phần gộp DB) phải có thêm
lựa chọn **100**.

## Hiện trạng khảo sát

| Nơi render phân trang | Option đang có | Thiếu 100? |
| --- | --- | --- |
| `components/V2BaseDataTable.vue` (prop `pageSizeOptions`, default) | `[5, 10, 20, 50]` | ✅ thiếu |
| `components/V2BasePagination.vue` (prop `pageSizeOptions`, default) | `[10, 20, 50, 100]` | ❌ đã có |
| 3 modal tìm kiếm gop-db (`ProductSearchModal`, `GroupSearchModal`, `CostSearchModal`) | tự truyền `[20, 50, 100]` | ❌ đã có |

→ **Toàn bộ** màn danh sách gop-db đều lấy option từ **default của `V2BaseDataTable`**;
không màn nào tự truyền `page-size-options` bị thiếu 100. Vậy chỉ có **1 điểm sửa duy nhất**.

## Quyết định (user chốt 2026-08-13)

1. **Sửa thẳng default của component dùng chung** `V2BaseDataTable`, KHÔNG truyền prop riêng cho từng màn.
   - Lý do: 1 dòng thay vì lặp 16 chỗ; màn gop-db làm sau tự có 100 mà không phải nhớ truyền.
   - Chấp nhận: 75 file khác ngoài gop-db cũng có thêm option 100 — chỉ **thêm**, không màn nào mất
     lựa chọn đang có nên không phá vỡ hành vi cũ.
2. **Giữ option 5** → kết quả `[5, 10, 20, 50, 100]`.
   - Không đồng bộ về `[10, 20, 50, 100]` như `V2BasePagination` để tránh user đang để 5 dòng/trang
     bị select không khớp giá trị.

## Phạm vi ảnh hưởng

- **1 file**: `hrm-client/components/V2BaseDataTable.vue:250`
- **Không** đụng BE, không migration, không permission.
- 16 màn gop-db hưởng lợi trực tiếp:
  - `pages/finance/`: account-banks · accounts · cost-debts · currencies · product-transfer-requests ·
    source-capitals · type-accounts · works
  - `pages/customer-care/`: costs · device-errors · levels · note-maintenances · serials · services
  - `pages/assign/customers` · `pages/human/banks`

## Ghi chú

- `V2BaseDataTable` và `V2BasePagination` là **2 component phân trang song song** trong repo, default
  lệch nhau (`[5,10,20,50]` vs `[10,20,50,100]`). Đợt này chỉ vá option, **không gộp** 2 component —
  nếu sau này muốn gộp thì phải rà cả 93 file đang dùng `V2BaseDataTable`.
- BE đã soát thật: `100` đi lọt ở mọi endpoint gop-db, **không phải sửa BE dòng nào**. Trong đó
  3 chỗ có cap `min(100, max(1, …))` (`DeviceErrorController:303`, `ServiceService:484` và `:719`) —
  100 đúng bằng trần nên vẫn chạy. ⚠️ Nếu sau này thêm option `200`/`500` thì 3 chỗ này sẽ âm thầm
  ghim lại 100, phải sửa BE trước.
- `/human/banks` dùng param **`limit`** chứ không phải `per_page` (cả FE lẫn BE) — khớp nhau, không cap.

## Spec chi tiết

`docs/superpowers/specs/gop-db/2026-08-13-pagination-100-rows-design.md`
