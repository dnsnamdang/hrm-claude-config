# Phân công báo giá: giới hạn theo nhóm nghiệp vụ mình quản lý

**Người phụ trách:** @khoipv · **Ngày:** 18/09/2026
**Spec chi tiết:** `docs/superpowers/specs/2026-09-18-phan-cong-bao-gia-theo-nhom-design.md`

## Mục tiêu
Người có quyền `Phân công báo giá` chỉ phân công được dự toán do **nhân viên trong nhóm nghiệp vụ mình quản lý** tạo.
Không quản lý ai → chỉ phân công được **dự toán do chính mình tạo**.

## Quy tắc
```php
in_array($this->created_by, listManageEmployeeIdsByGroup()) || $this->created_by == auth()->user()->id
```
Không quản lý nhóm nào → mảng rỗng → chỉ còn dự toán của chính mình.

## Scope
| Điểm | Xử lý |
|---|---|
| `Project::canAssign()` | Bật lại ràng buộc nhóm (logic cũ đang bị comment) |
| `Project::canRejectAssignment()` | Áp cùng phạm vi |
| API `PUT /projects/{project}/assign-employee` | Thêm chặn server-side — trước đây **không kiểm tra quyền gì** |
| Thông báo "cần phân công" (store + update) | Gửi cho quản lý nhóm của người tạo; không có → gửi chính người tạo nếu họ có quyền |
| Dashboard đếm "dự toán cần phân bổ" (3 chỗ) | Lọc cùng điều kiện |
| Command nhắc sắp quá hạn | Gửi theo từng dự toán cho quản lý nhóm của người tạo |

## Quyết định lớn
- Viết điều kiện **inline** đúng style `Quotation::canApprove()` sẵn có, không tách helper/cache riêng (theo góp ý của @khoipv).
- Không đụng quyền XEM dự toán / báo giá và các luồng duyệt khác (TP duyệt, BGĐ duyệt, Duyệt bàn giao báo giá).

## Tác động
Thông báo "cần phân công": trước gửi cho **21 người** có quyền → nay **2-3 quản lý nhóm** của người tạo.
