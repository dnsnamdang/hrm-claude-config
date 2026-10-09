# Fix: không gửi duyệt lại được hàng tạm đã bị từ chối

## Bug
Vào hàng tạm bị từ chối → Sửa → 'Gửi Duyệt lại' báo 'Không thể sửa hàng tạm này!'.

## Root cause
`TmpProductsController::updateDraft()` dòng 750 guard bằng `canEdit()` (TmpProduct:73 = chỉ status 3 Đang tạo). Nhưng updateDraft thiết kế xử lý cả gửi-duyệt-lại hàng từ chối (status 0): dòng 796 set PENDING, 798-801 xóa lý do từ chối. Danh sách cũng có nút riêng 'Sửa và gửi duyệt lại' cho status 0 (dòng 157-158). Guard bỏ sót status 0 → chặn nhầm.

## Fix
Đổi guard: cho phép status DRAFT(3) HOẶC REJECTED(0) của chính người tạo. Không sửa canEdit() (tránh nhân đôi nút edit ở list).

## Tasks
- [ ] Sửa guard updateDraft (TmpProductsController ~750) + php -l
- [ ] User test: hàng từ chối → sửa → gửi duyệt lại → về Chờ duyệt, xóa lý do từ chối

## Nhánh: sync_quotation
