# Plan — Dashboard Timesheet: Tổng NS cộng tác viên & Tổng NS chính thức

Phụ trách: @khoipv

## Mục tiêu
Thêm 2 card vào màn `timesheet/dashboard` (HCNS):
- **Tổng nhân sự cộng tác viên** = NV thuộc phòng ban có `cooperation_type IN (1=KD, 2=NV)`.
- **Tổng nhân sự chính thức** = `Tổng nhân sự` − `Tổng NS cộng tác viên`.

Tính theo đúng công ty đang chọn, dùng chính tập NV mà dashboard đang tính (`$employee_id_department`) ⇒ tự khớp: chính thức + CTV = Tổng nhân sự. Style 2 card y hệt card "Nhân sự đi làm / Tổng nhân sự".

## Tasks
- [x] BE: import `Department` vào `Modules/Timesheet/Services/DashboadService.php`
- [x] BE: trong `hcns()` tính `$tong_nv_ctv` (join departments theo cooperation_type) + trả về 2 key `tong_nv_ctv`, `tong_nv_chinh_thuc`
- [x] FE: thêm 2 card hiển thị `data.tong_nv_chinh_thuc` và `data.tong_nv_ctv` trong `components/dashboad/HcnsDashboad.vue`

### Checkpoint — 2026-06-09
Vừa hoàn thành: cả 3 task (BE + FE).
Đang làm dở: (không)
Bước tiếp theo: user test trên dashboard, đối chiếu số với báo cáo human/personnel.
Blocked:
