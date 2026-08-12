# Cảnh báo "Thông tin chưa lưu" cho màn danh mục (đợt 1)

**Người phụ trách:** @junfoke
**Nhánh:** `gop_db`
**Ticket:** [ERP => HRM] - Danh mục - Chưa hiển thị popup xác nhận khi thoát màn hình khi chỉnh sửa dữ liệu

## Mục tiêu

Khi user đã sửa dữ liệu nhưng chưa lưu và bấm Thoát/Đóng/× → hiện popup
`Thông tin chưa lưu` / `Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?` (Thoát / Ở lại).

## Phạm vi đợt 1 — 15 màn danh mục của 2 phân hệ mới

| # | Màn | Kiểu form | File form |
|---|---|---|---|
| 1 | Cấp dịch vụ bảo dưỡng | modal | `components/modal/customer-care/level-modal.vue` |
| 2 | Ghi chú kiểm tra bảo dưỡng | modal | `components/modal/customer-care/note-maintenance-modal.vue` |
| 3 | Dịch vụ sửa chữa & chi phí khác | modal | `components/modal/customer-care/cost-modal.vue` |
| 4 | Tiền tệ | modal | `components/modal/finance/currency-modal.vue` |
| 5 | Loại tài khoản | modal | `components/modal/finance/type-account-modal.vue` |
| 6 | Tài khoản ngân hàng | modal | `pages/finance/account-banks/AccountBankModal.vue` |
| 7 | Mã phí | modal | `pages/finance/cost-debts/CostDebtModal.vue` |
| 8 | Nguồn vốn | modal | `pages/finance/source-capitals/SourceCapitalModal.vue` |
| 9 | Vụ việc | modal | `pages/finance/works/WorkModal.vue` |
| 10 | Cập nhật nhanh giá dịch vụ | form trong trang | `pages/customer-care/service-price-config/index.vue` |
| 11 | Danh mục lỗi thiết bị | trang create/edit | `pages/customer-care/device-errors/{create,_id/edit}.vue` |
| 12 | Dịch vụ sửa chữa (gói) | trang create/edit | `pages/customer-care/services/{create,_id/edit}.vue` |
| 13 | Hệ thống tài khoản | trang add/edit | `pages/finance/accounts/{add,_id/edit}.vue` |
| 14 | Đề nghị điều chuyển hàng hoá | trang create/edit | `pages/finance/product-transfer-requests/{create,_id/edit}.vue` |
| 15 | Serial thiết bị | — | **Không có form Thêm/Sửa** (màn chỉ xem) → ngoài phạm vi |

## Quyết định kỹ thuật

- **KHÔNG sửa `utils/mixins/unsavedChangesMixin.js`** (hàm dùng chung, 4 màn đang phụ thuộc).
  Mixin đó chỉ bắt `beforeRouteLeave` + `beforeunload` → không chặn được việc đóng modal.
- Tạo **file mixin MỚI** `utils/mixins/unsavedModalMixin.js` dành riêng cho form trong modal.
  Chặn tại sự kiện `hide` của `b-modal` (`bvEvt.preventDefault()`), hỏi xác nhận rồi mới đóng.
  → Phương án hợp nhất 2 mixin sẽ chốt lại sau (anh Nam xác nhận sau).
- Màn form dạng trang (10–14) dùng thẳng `unsavedChangesMixin` có sẵn.
- Giữ nguyên triết lý chống báo nhầm của mixin cũ: chỉ tính là bẩn khi thay đổi xảy ra
  trong ~500ms sau thao tác chuột/phím; dữ liệu do API tự điền → dời mốc so sánh.

### Thay đổi bắt buộc trên mỗi modal

`b-modal` phải tách 3 sự kiện (trước đây gộp hết vào `closeModal`/`reset`):

| Sự kiện | Việc |
|---|---|
| `@shown` | `markFormPristine()` — chốt mốc so sánh sau khi parent nạp xong dữ liệu |
| `@hide` | `onUnsavedModalHide` — guard, có thể `preventDefault()` |
| `@hidden` | reset dữ liệu + `$emit('closeModal')` (việc mà `closeModal` cũ làm trong `setTimeout`) |

Lý do: nếu vẫn reset dữ liệu ở `@hide`, khi guard chặn lại thì form đã bị xoá trắng.

## Ngoài phạm vi (đợt sau)

- ~147 form dạng trang của các phân hệ cũ (decision, assign, training, human, timesheet).
- ~180 form dạng modal của các phân hệ cũ.
