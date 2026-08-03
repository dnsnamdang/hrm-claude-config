# Giữ bộ lọc khi rời trang — Danh mục / Kinh doanh / Kế hoạch / Quản lý thầu

**Phụ trách:** @khoipv · **Ngày:** 2026-07-04

## Mục tiêu
Rà soát toàn bộ màn danh sách 4 phân hệ, chuẩn hoá cơ chế **giữ nguyên bộ lọc + trang phân trang** khi user vào chi tiết (hoặc trang khác trong luồng) rồi quay lại. Tham chiếu màn chuẩn: `plan/quotation`.

## Cơ chế
Tái sử dụng mixin có sẵn `@/utils/mixins/searchMixinPlugin.js` (`loadFilterState`, `saveFilterState`, `savePaginationState`, `clearFilterState`, `beforeRouteLeave`). Không sửa file mixin dùng chung, không đụng 9 màn đang chạy tốt (trừ fix trùng key).

- `localStorageKey`: khoá lưu riêng từng màn.
- `pathsToKeep`: khi rời sang path nằm trong danh sách này → **giữ** lọc; ngoài danh sách → `beforeRouteLeave` **xóa** lọc.

## Phạm vi (chốt với user): 8 màn + fix trùng key

| # | Màn | localStorageKey | pathsToKeep |
|---|---|---|---|
| 1 | sale/assign-kpi | `sale-assign-kpi` | `/sale/assign-kpi`, `/sale/register-kpi` |
| 2 | sale/register-kpi | `sale-register-kpi` | `/sale/register-kpi`, `/sale/assign-kpi` |
| 3 | sale/report-project-contract | `sale-report-project-contract` | `/sale/report-project-contract`, `/plan/quotation` |
| 4 | sale/detail-report | `sale-detail-report` | `/sale/detail-report`, `/bid_package/bid_package`, `/contract/contract`, `/plan/project`, `/plan/quotation` |
| 5 | plan/detail-report | `plan-detail-report` | `/plan/detail-report`, `/plan/quotation` |
| 6 | bid_package/detail-report | `bid-package-detail-report` | `/bid_package/detail-report`, `/bid_package/bid_package`, `/contract/contract` |
| 7 | category/customer_handover | `category-customer-handover` | `/category/customer_handover` |
| 8 | category/customer_handover/waiting-approve | `category-customer-handover-waiting` | `/category/customer_handover` |

**Fix trùng key:** `plan/project` và `bid_package/project` đang cùng `sale-project-plan`.
- `plan/project` → `plan-project`
- `bid_package/project` → `bid-package-project`
- `sale/project` giữ `sale-project`.

## Loại khỏi phạm vi
~24 danh mục con của Category (banks, unit, origin, model, cost...): sửa bằng **modal**, không có trang chi tiết riêng → pattern chuẩn (xóa lọc khi rời menu) không mang lợi ích thực tế. Bỏ qua.

## Cạm bẫy kỹ thuật
Màn có `watch.formFilter` với `immediate: true` (assign-kpi, register-kpi): watcher chạy trước `mounted`. Nếu đặt `saveFilterState()` trong watcher, nó ghi đè state đã lưu bằng giá trị mặc định trước khi mounted kịp load → mất tác dụng. **Xử lý:** bỏ `immediate: true`, load state ở đầu `mounted`, gọi `getData()` tường minh cuối `mounted`.

Chi tiết đầy đủ: `docs/superpowers/specs/2026-07-04-giu-loc-danh-sach-design.md`
