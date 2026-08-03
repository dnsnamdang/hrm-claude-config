# Đổi tên "Loại chiết khấu" → "Loại giảm giá" — Design

> Phụ trách: @dnsnamdang · Branch: `tpe-develop-assign`
> Liên quan: danh mục `discount_types` (feature gốc `Bomlist-Quotation` Phase 29).

## Mục tiêu

Đổi **tên hiển thị** của danh mục `Danh mục → Loại chiết khấu` thành **"Loại giảm giá"** trên toàn bộ UI (menu, tiêu đề màn, nhãn form/bảng, thông báo) và đổi **tiền tố mã tự sinh** từ `CK-YYYY-XXXXX` sang `GG-YYYY-XXXXX`.

## Phạm vi

### Làm
- Đổi nhãn submenu menu điều hướng: "Loại chiết khấu" → "Loại giảm giá".
- Đổi tiêu đề: danh sách, bộ lọc, và modal Thêm/Sửa/Xem chi tiết.
- Đổi nhãn form/bảng: "Mã loại CK", "Tên loại CK *", "Tên loại chiết khấu" → "... giảm giá".
- Đổi mọi chuỗi user-facing chứa "loại chiết khấu"/"loại CK" trong 2 màn catalog → "loại giảm giá".
- Đổi tiền tố sinh mã BE: `CK-` → `GG-` (`DiscountType::getNextCode()`).

### KHÔNG làm (giữ nguyên)
- **KHÔNG** đổi tên quyền `Quản lý danh mục loại chiết khấu` (permission string trong seeder + `menu-sidebar.isShow` + BE check) — đổi sẽ vỡ phân quyền.
- **KHÔNG** đổi mã của các bản ghi cũ (giữ `CK-...` như dữ liệu lịch sử) — chỉ bản ghi MỚI dùng `GG-`.
- **KHÔNG** đổi các nhãn "chiết khấu" thuộc chức năng chiết khấu trên báo giá (Tổng chiết khấu, phương thức chiết khấu, phân bổ...) — ngoài phạm vi.
- **KHÔNG** đổi route `/assign/discount-types`, tên bảng `discount_types`, API, cột DB.

## Quyết định
| Vấn đề | Quyết định |
|---|---|
| Mã bản ghi cũ | Giữ nguyên `CK-...` (chỉ đổi rule sinh mã mới) |
| Permission name | Giữ nguyên (không phải nhãn hiển thị) |
| Route / bảng / API | Giữ nguyên |
| Chiết khấu trên báo giá | Ngoài phạm vi, không đụng |

## File đụng
- BE: `Modules/Assign/Entities/DiscountType.php` (getNextCode prefix).
- FE: `components/menu-sidebar.js`, `pages/assign/discount-types/index.vue`, `components/modal/discount-type-modal.vue`.
