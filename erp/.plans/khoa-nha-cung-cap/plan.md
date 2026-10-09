# Cho khóa nhà cung cấp (thay vì xóa cứng bị chặn)

## Hiện trạng
Nút 'Xóa' NCC set status=0 (=Khóa, soft) nhưng bị Supplier::canDelete()=false chặn hoàn toàn. status: 1=Hoạt động, 0=Khóa. getForSelect... đều where(status,1) nên NCC khóa tự ẩn khỏi chọn.

## Quyết định (user)
1. Điều kiện: cho khóa TỰ DO khi đang hoạt động (status==1). Không kiểm tra phát sinh.
2. Đổi nhãn Xóa -> Khóa (nút + thông báo).
3. Mở khóa: chờ user xác nhận.

## Tasks
- [ ] Supplier::canDelete() -> return status==1
- [ ] Đổi nhãn nút + message (Xóa->Khóa)
- [ ] php -l + user test

## Branch: master

## Cập nhật: thêm Mở khóa (user chọn b)
- Route GET suppliers/{id}/unlock (quyền "Sửa nhà cung cấp") + SuppliersController@unlock (status 0->1).
- Nút list theo status: hoạt động->Khóa (class lock, fa-lock); khóa->Mở khóa (class unlock, fa-unlock). Confirm a.unlock có sẵn.
- php -l sạch, route đăng ký OK. Chưa commit (master). Chờ user test.

### Checkpoint — 2026-07-01
Vừa hoàn thành: Khóa/Mở khóa NCC — canDelete()=status==1; nút Khóa/Mở khóa theo trạng thái; route+method unlock.
Bước tiếp theo: user test list NCC (khóa/mở khóa) → commit.
