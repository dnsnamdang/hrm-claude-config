# Plan — Thêm cột Mã nhân viên vào báo cáo vận chuyển & bốc xếp

@junfoke · Repo `TanPhatDev` (bản B, nguồn chính)

## Mục tiêu
Thêm cột **Mã NV** (nguồn `employee_infos.code`) đứng trước cột tên, ở **cả màn web lẫn Excel/In**, cho 6 báo cáo. Mục đích: công thức bảng lương VLOOKUP theo mã, tránh nhầm khi trùng tên.

Quyết định đã chốt với user:
- Cột riêng "Mã NV" (không ghép vào tên).
- Làm cả màn + Excel.
- Báo cáo 4 (Chi tiết chuyến xe): **chỉ thêm Mã NVKD**, giữ nguyên cột Lái xe (lái xe lưu text tự nhập, có thể là lái xe ngoài → không có mã) → phương án (a).

## Nhãn cột
- BC1, BC2: **Mã lái xe** · BC3: **Mã NVKD** · BC4: **Mã NVKD** · BC5, BC6: **Mã NV**

## Tasks

### BC1 — Tổng hợp CP vận chuyển theo lái xe
- [x] Query `AccountDetail::transportByDriverSearchData`: `employee_code` vào 2 subquery (sub/sub1) + query gộp ngoài (select + groupBy)
- [x] Màn `reports/transport_by_driver.blade.php`: th "Mã lái xe" + td `d.employee_code`
- [x] Excel `reports/exports/transport_by_driver_export.blade.php`

### BC2 — Chi tiết CP vận chuyển theo lái xe
- [x] Query `detailTransportByDriverSearchData` (cùng pattern sub/sub1 + gộp ngoài — sửa chung replace_all với BC1)
- [x] Màn `reports/detail_transport_by_driver.blade.php`: cột "Mã lái xe", dòng nhóm hiện mã, dòng chuyến để trống
- [x] Excel `reports/exports/detail_transport_by_driver_export.blade.php`

### BC3 — CP vận chuyển theo NVKD
- [x] Query `transportByStaffEmployeeSearchData`: `em_info.code as e_code` (2 subquery + select gộp ngoài)
- [x] Màn `reports/detail_transport_by_staff.blade.php`: cột "Mã NVKD" (`v.e_code`)
- [x] Excel `ExcelExports/DetailTransportByStaffExcel.php` (HTML string, cả detail()+basic(); dời cột format số G→H)

### BC4 — Chi tiết chuyến xe (chỉ Mã NVKD)
- [x] Query `detailTripEmployeeReportSearchData` + `detailOtherTripEmployeeReportSearchData`: propagate `employee_code`/`i_employee_code` qua các tầng subquery
- [x] Màn `reports/detail_trip.blade.php`: cột con "Mã NVKD" trong nhóm Chi tiết
- [x] Excel `reports/exports/detail_trip_report_export.blade.php`

### BC5 — Cấu hàng bốc xếp theo nhân viên (tổng hợp)
- [x] Query `searchReportArrangeGoodByEmployeeSearchData`: `ei.code as employee_code`
- [x] Màn `common/delivery_arrange/report_by_employee.blade.php`: cột "Mã NV"
- [x] Excel/In `PrintArrangeGoodService::getReportArrangeGoodByEmployeeTable`

### BC6 — Chi tiết cấu hàng bốc xếp theo nhân viên
- [x] Query `searchReportArrangeGoodDetailByEmployeeSearchData`: `ei.code as employee_code`
- [x] Màn `common/delivery_arrange/report_detail_employee.blade.php`: cột "Mã NV"
- [x] Excel/In `PrintArrangeGoodService::getReportArrangeGoodByDetailEmployeeTable`

## BỔ SUNG — BC4 thêm cột "Mã lái xe" (khách yêu cầu, đổi quyết định (a)→có mã lái xe)

Trước chốt (a): BC4 không có mã lái xe. Nay khách cần. Cách "hợp lý" (nhánh `local_tri`):
- **Mã lái xe = 1 cột**, giá trị: lái xe NỘI BỘ → **mã HRM** (qua `company_driver_id` = employee_infos.id); lái xe NGOÀI (bảng `drives`, driver_type=1) → **CCCD** (`drives.id_card`); còn lại trống.
- Query (`detailTripReportSearchData` 2 subquery union): kéo `drives.id_card` xuyên subquery xe → `driver_ext_cccd` (type1 CASE driver_type=1, type2 NULL, đồng bộ union). `company_driver_id` đã có sẵn.
- Controller + mail job: gộp `company_driver_id` vào `$hrmCodeMap`; `$item->driver_code = HRM[company_driver_id] ?? driver_ext_cccd ?? ''`.
- Blade màn `detail_trip.blade.php` + export `detail_trip_report_export.blade.php`: thêm cột "Mã lái xe" cạnh "Lái xe".
- `php -l` sạch; verify: nội bộ Đồng Xuân Thạch → HRM `52010682`. Lái xe ngoài: snapshot local 0 chuyến nên chưa thấy data, nhưng cột `driver_ext_cccd` tạo đúng + `drives.id_card` có sẵn.
- [ ] User deploy + test dev (đặc biệt ca có lái xe ngoài → hiện CCCD).

## FIX SAU DEPLOY — Mã phải khớp HRM (không phải mã ERP)

User phản hồi: mã lái xe/NVKD hiển thị mã ERP cũ (`NV.xxx`), KHÔNG khớp mã nhân viên mới trong HSNS/HRM (vd Nguyễn Hồng Thắng HRM=`12210312`, ERP=`NV.00524`).

**Link chính thức ERP↔HRM** (đang dùng ở màn chức vụ `EmployeesController@...`): `ERP employees.employee_info_id = HRM employee_infos.id` (cùng khoá). KHÔNG khớp CCCD. HRM ở **server khác** → map bằng PHP qua connection `hrm` (không join cross-DB).

Đã làm (nhánh `local_tri`):
- [x] Helper `app/Services/HrmEmployeeService.php`: `codesByInfoIds($ids)` [info_id=>hrm_code] qua connection hrm; `attach($rows)` gán mã vào object rows.
- [x] Query 6 báo cáo (`AccountDetail`, `ProductImportExportArrangeDeliveryExecutor`): đổi lộ `employee_info_id` (thay vì `em_info.code`). BC4 propagate `employee_info_id`/`i_employee_info_id` qua subquery lồng.
- [x] Controller map mã HRM vào field blade dùng (`employee_code`/`e_code`/`i_employee_code`): BC1/BC2 `attach($data->items()/$data)`; BC3 map `e_code` vào mảng NV; BC4 map `employee_code`+`i_employee_code` vào sub; BC5/BC6 `attach`. Cả search + export.
- [x] 4 mail job (path >ngưỡng, gửi Excel qua mail) map tương tự.
- [x] `php -l` sạch tất cả; verify tinker: BC5 Nguyễn Hồng Thắng info_id 524 → HRM `12210312` (khớp HSNS), BC1 Đồng Xuân Thạch → 52010682, BC4 NVKD Vũ Bá Hoàng → NV.00389 (HRM giữ mã NV cho người này).
- [ ] User test browser trên dev sau khi deploy local_tri + đối chiếu Excel/In.

### Verify (đợt đầu — mã ERP, đã bị thay bằng mã HRM ở trên)
- [x] `php -l` 4 file PHP sửa — sạch
- [x] Rà FE: các class map (`TransportByDriverReport`, `TransportByStaffReport`, `DetailTransportByStaffReport`, `DetailTripSubReport`) copy toàn bộ key → mã NV không bị rớt; BC5/BC6 gán thẳng `response.data.data`
- [x] Verify query bằng dữ liệu thật (bản B local, DB erp_dev_30_01_26, login emp 13): cả 6 query chạy không lỗi, trả đúng `employee_code`/`e_code` — BC1/BC2 NV.01105, BC4 NV.00389, BC5/BC6 NV.00528; BC3 & BC4-other 0 dòng nhưng SQL không ném lỗi (không dính ONLY_FULL_GROUP_BY). Script test đã xoá.
- [x] Verify trực quan Playwright (bản B :8001, emp 13): BC1 màn (STT|NV.01105|Đồng Xuân Thạch), BC2 màn (dòng nhóm NV.01105), BC4 màn (Mã NVKD = NV.00389), BC5 màn (NV.00528|Lê Văn Chiến|578,050) — header + data đúng. Excel/In verify qua render HTML: BC5/BC6 service có "Mã NV"+NV.00528, BC1 export blade có "Mã lái xe"+NV.01105, BC3 export blade có "Mã NVKD". BC3 màn 0 dòng trong snapshot (không có dữ liệu vận chuyển theo NVKD) nhưng header + SQL OK.
→ **READY để đẩy lên dev.**

### Checkpoint — 2026-08-26
Vừa hoàn thành: Thêm cột Mã NV vào 6 báo cáo (4 vận chuyển + 2 bốc xếp), cả màn web lẫn Excel/In. php -l sạch, data-flow FE verify.
Đang làm dở: (không)
Bước tiếp theo: User chạy thử trên bản B local (`php artisan serve :8001`) đối chiếu cột mã + xuất Excel/In.
Blocked: (không)
