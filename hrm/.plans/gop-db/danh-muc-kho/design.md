# Danh mục kho (7 màn ERP → HRM) — Design (tóm tắt)

**Người phụ trách:** @junfoke — 2026-10-19

> Nhánh `feat/chuyen-doi-hang-hoa` (cả 2 repo — user chỉ định 19/10; code làm trên `feat/warehouse-catalogs` rồi chuyển sang)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-19-danh-muc-kho-design.md`
> Plan: `.plans/gop-db/danh-muc-kho/plan.md`

## Mục tiêu

Chuyển nhóm menu ERP **Danh mục → Kho** sang HRM, phân hệ **Danh mục chung**, nhóm menu mới **"Kho"**
(theo sheet quy hoạch: Danh mục | Kho | Danh mục …).

## Phạm vi (user chốt 19/10/2026)

- **Port 7 màn ERP đang hiện trên menu**: Kho vật lý, Kho kế toán, Nhà kho, Dãy, Khoang, Vị trí, Kiện.
- **Bỏ Nhóm kho** (menu ERP đã bị comment, 2 dòng dữ liệu từ 2023).
- **Bỏ đồng bộ CRM** (`services.mate.use_crm`) khi tạo/sửa kho vật lý.
- **Quyền**: 1 quyền duy nhất **"Quản lý kho"** (guard `api`, type 9 Danh mục chung) cho cả 7 màn — xem + ghi.

## Thứ tự làm

| Phase | Màn | Ghi chú |
| --- | --- | --- |
| 1 | **Nhà kho** | Mở đường: quyền, nhóm menu Kho, khuôn "danh mục có cha là kho" + sinh con hàng loạt |
| 2 | Dãy | Sinh khoang × vị trí |
| 3 | Khoang | |
| 4 | Vị trí | 2 loại vị trí, xuất Excel, nhiều điều kiện chặn xoá |
| 5 | Kho vật lý | Rủi ro cao nhất, sinh nhà + vị trí tách ghép |
| 6 | Kho kế toán | |
| 7 | Kiện | Độc lập |

## Quyết định chính

1. **Khung**: dựng trên khung danh mục dùng chung của `Modules/MasterData`
   (`BaseCatalogController/Service/Model/Request/Resource` + FE `vehicleCatalogScreenMixin` /
   `vehicleCatalogModalMixin`) — form là **popup**, có Khóa/Mở khóa, Lịch sử, Xuất Excel, Cấu hình cột.
2. **Trạng thái**: bảng ERP `houses`/`rows`/`spaces`/`positions` không có cột trạng thái → thêm cột
   `status` (1 Hoạt động / 0 Khóa, mặc định 1) bằng migration chỉ-thêm-cột, như tiền lệ `bank_branches`,
   `vehicle_life`. ERP không đọc cột này (bản ghi khoá ở HRM vẫn chọn được bên ERP — ghi nhận, như Đời xe).
3. **Phạm vi dữ liệu** (user chốt): giữ như ERP — người thường chỉ thấy bản ghi thuộc kho vật lý có
   `warehouses.company_id` = công ty mình; **Super admin** thấy mọi công ty và có thêm ô lọc Công ty.
4. **Xoá**: xoá cứng, chỉ khi đang Hoạt động và chưa được dùng (khuôn H2). Kho vật lý / kho kế toán (xoá mềm
   status = 2 bên ERP) chốt ở phase 5-6.
5. **Giữ nghiệp vụ ERP**: mã/tên unique trong phạm vi cha; tạo bản ghi cha sinh con hàng loạt
   ("Dãy i"/"D{i}"…). Sửa lỗi ERP: số lượng sinh validate `integer|between:1,999` (ERP đo độ dài chuỗi).
