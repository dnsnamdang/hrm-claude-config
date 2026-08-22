# Port các bản sửa lỗi component dùng chung từ `gop_db` sang `tpe-develop-assign`

**Người phụ trách:** @dnsnamdang · **Nhánh:** `feature/port-shared-fixes` (từ `origin/tpe-develop-assign`, repo `hrm-client`)

## Mục tiêu

`gop_db` đã sửa nhiều lỗi ở component dùng chung mà `tpe-develop-assign` chưa có. Đưa các bản
sửa đó sang, **không kéo theo tính năng riêng của bản gộp DB**.

Tổng khối lượng chênh lệch ở component/util dùng chung: ~4.900 dòng / 52 file → phải chia đợt,
không port một lượt.

## Nguyên tắc chọn

1. Chỉ lấy file mà `gop_db` **sửa lỗi / chuẩn hoá UI**, không lấy file mang tính năng mới của
   phân hệ chỉ có ở `gop_db` (Finance, CSKH, Danh mục chung…).
2. Trước khi lấy nguyên file: kiểm tra **prop bị bỏ** và **event bị bỏ** — có là không port nguyên,
   phải ghép tay từng hunk.
3. File nào `gop_db` sửa vì **đặc thù DB gộp** (vd `customer_groups` bên gộp không có cột `code`)
   thì KHÔNG bê nguyên, phải viết lại cho tpe.
4. `gop_db` cũng có lỗi — không port mù. Đã phát hiện `V2BaseRejectApproveModal.vue` bên `gop_db`
   có typo `::rows="3"` (2 dấu hai chấm); bản tpe đang đúng, giữ nguyên.

## Đợt 1 — Select & ô nhập liệu (ĐÃ LÀM)

Đúng nhóm gây ra hiện tượng user thấy ở màn `/assign/customers/{id}/edit`.

Theo `.claude/skills/select-and-input-state/SKILL.md`: một kiểu khoá duy nhất cho mọi ô nhập
(nền `#f1f5f9`, chữ `#475569`, không `opacity`), chip chọn nhiều một khuôn duy nhất, focus không
viền xanh, ô tự dựng bằng `<div>` phải tự chặn thao tác khi khoá.

Đã kiểm: 0 prop bị bỏ, 0 event bị bỏ, 0 default đổi → lấy nguyên file an toàn.

## Các đợt sau — chờ chốt phạm vi

- **Lịch sử màn chi tiết** (`SystemInfoSection.vue` + BE `SystemLogService` / `SystemLogController`)
  — cần cả FE và BE, xem plan.md.
- **V2Base khác**: DataTable, FilterPanel, Pagination, TitleSubInfo, Button, Footer, Import*.
- **Modal**: base-confirm-modal, column-customization-modal, V2BaseModal (mới) + 5 modal sửa
  `rows="3"` → `:rows="3"`.
- **Mixin/util mới**: unsavedModalMixin, unsavedChildFormMixin, formValidateMixin,
  columnCustomizationMixin, exportFieldsMixin, DedupeLoadMixin, number-input, statusBadgeVariant.
