# DS phiếu công tác — thêm cột Nội dung công tác, Vị trí chấm công

- Người phụ trách: @khoipv
- Bắt đầu: 18/11/2026
- Màn: `/timesheet/business_trip_assigns` (client `pages/timesheet/business_trip_assigns/index.vue`, màn CŨ — b-table)
- API: `GET timesheet/business_trip_assigns` → `BusinessTripAssignListResource` — đã trả sẵn `description` + `timesheet_info` (lịch sử chấm công theo NV, mỗi lượt có `place`) ⇒ **không sửa BE**

## Quyết định
- Nội dung công tác = `description` (ô "Nội dung công việc" ở form phiếu). Hiển thị text thuần (không v-html), giữ xuống dòng.
- Vị trí chấm công = gom `place` của mọi lượt chấm công theo phiếu (mọi NV), bỏ trống + bỏ trùng, mỗi vị trí 1 dòng. Phiếu chưa chấm công → ô trống.

## Phase 1 — FE
- [x] Thêm 2 cột vào `fields`: `description` (sau Mã phiếu), `timesheet_places` (sau Người đi công tác)
- [x] Map `timesheet_places` từ `timesheet_info` trong `getData` + `resetSearch` (dùng chung hàm `mapRow`)
- [x] Slot hiển thị riêng cho 2 cột (text thuần, không v-html)
- [ ] User test UI

## Phase 2 — Xuất Excel (FE, ExcelJS như `pages/timesheet/report/business_trip_assign_report_.vue`)
- Gọi lại `GET timesheet/business_trip_assigns` theo bộ lọc hiện tại (`formFilter`), 200 dòng/trang, các trang sau song song tối đa 3 request, giữ thứ tự.
- 1 dòng/phiếu, cột như bảng (trừ Hành động); Vị trí chấm công nhiều vị trí → xuống dòng trong ô.
- [x] Nút "Xuất excel" trên toolbar (không gate quyền), cờ `isExporting` chống bấm 2 lần
- [x] `exportEx` → `fetchAllPagesForExport` → `generateWorkbook` (tiêu đề + header + border, file `danh_sach_phieu_cong_tac_<thời gian>.xlsx`)
- [ ] User test xuất file

## Phase 3 — Xuất Excel chậm (5000 phiếu: mỗi trang 200 phiếu 12–28 s)
Nguyên nhân: `BusinessTripAssignListResource` chạy ~8–10 query / phiếu (BusinessTripEmployee, EmployeeInfo, Timesheet join, canPaymentFeeRequest, isExistPaymentFeeRequest, requestPaymentWorkingFeeRoot, can_approve/can_reject, người tạo/duyệt) + payload 326 kB / 200 phiếu ⇒ 5000 phiếu ≈ hàng chục nghìn query.
### BE
- [x] `BusinessTripAssignService`: tách phần dựng query lọc + phân quyền của `index()` ra `buildListQuery($request)` (chỉ dời code, `index()` giữ nguyên hành vi)
- [x] `exportData($request)`: dùng `buildListQuery` (bỏ eager load), lấy hết theo bộ lọc, gom theo lô: NV đi công tác (1 query), vị trí chấm công (1 query / 1000 phiếu), tên người tạo/duyệt (1 query) — chỉ trả các cột cần xuất
- [x] Controller `export` + route `GET /timesheet/business_trip_assigns/export` (khai TRƯỚC `/{id}`)
### FE
- [x] `exportEx` gọi 1 request `/export` theo bộ lọc, bỏ gọi phân trang; giữ `generateWorkbook`
- [ ] User test tốc độ + file

## Phase 4 — Push
- [x] Commit + push `origin/master`: API `b30bd226`, Client `fedb604b` (phần thêm cột: client `7db875db` user đã commit trước)
- [ ] Deploy API + client cùng lúc (FE gọi route `/export` mới); không có migration

## Phase 5 — Cột "Phương tiện" (danh sách + Excel)
- Nguồn: phương tiện của từng lượt chấm công (`timesheets.vehicle_id` → `vehicles`, `no_company_vehicle`), text theo `Timesheet::vehicleText` ("Biển số (Hãng)" / "Không đi xe công ty"). Gom mọi lượt của phiếu, bỏ trống + bỏ trùng, nối ", " — giống ô "Phương tiện sử dụng" ở chi tiết phiếu (`utils/businessTripVehicle.js`).
### FE
- [x] Thêm field `timesheet_vehicles` "Phương tiện" sau "Vị trí chấm công"; `mapRow` dùng lại `vehicleUsageText(val.timesheet_info)` (API danh sách đã trả `vehicle_text`) ⇒ không sửa BE danh sách
- [x] `generateWorkbook`: thêm cột "Phương tiện" sau "Vị trí chấm công"
### BE
- [x] `exportData`: query timesheet theo lô leftJoin `vehicles`, dựng text bằng `Timesheet::vehicleText`, trả `timesheet_vehicles` (chuỗi nối ", ")
- [x] Kiểm: php -l, so khớp 20 dòng export với ListResource, chạy thử generateWorkbook (+ slot hiển thị text thuần, không v-html)
  - DB staging chỉ 3 lượt chấm công có xe (phiếu #5911, #5913, #5919) → export ra đúng "29A-00435 (Lexus)" / "30A-91200 (Audi)", khớp ListResource; export 5500 phiếu vẫn 18 query ~3,9 s
- [ ] User test

### Checkpoint — 18/11/2026 16:00
Vừa hoàn thành: Phase 5 — cột Phương tiện ở danh sách (FE `mapRow` dùng `vehicleUsageText`) + Excel (BE `exportData` join `vehicles`, trả `timesheet_vehicles`)
Đang làm dở:
Bước tiếp theo: User test; CHƯA commit/push phần Phase 5 (chờ user bảo). Deploy API + client cùng lúc
Blocked:

## Phase 6 — Thanh cuộn ngang bảng danh sách (thông tin bị co quá)
- Nguyên nhân: CSS chung `assets/scss/custom-table.scss` ép `.table-responsive-sm { overflow-x: hidden !important }` + bảng `fixed` độ rộng % ⇒ 14 cột bị ép vừa màn hình. Không sửa CSS chung, chỉ ghi đè trong màn.
- [x] Đổi `thStyle.width` mọi cột sang px (tổng ~2330px; bảng `fixed` tự rộng theo tổng cột, màn rộng hơn thì vẫn full 100%)
- [x] Thêm class `bt-scroll-x` vào div `.table-responsive` đang bọc `b-table`, style scoped `overflow-x: auto !important` cho wrapper bảng
- [x] Kiểm compile template
- [x] Bảng không có border ô → thêm prop `bordered` cho `b-table` (như `_id/approve.vue`, `report/business_trip_assign_day_report.vue`)
- [x] Cố định cột Mã phiếu: `stickyColumn: true` (như `payroll/manpower-allocations`); CSS scoped: nền trắng, hover cùng màu dòng `#efefef`, viền phải bằng box-shadow (viền collapse không đi theo ô sticky)
- [x] Cố định thêm cột STT: STT `left: 0`, Mã phiếu `left: 60px` (class `sticky-code`, = độ rộng cột STT)
- [ ] User test

## Phase 7 — Push (Phase 5 + 6)
- [x] Commit + push `origin/master`: API `8071f0ad` (export thêm Phương tiện), Client `ac02839e` (cột Phương tiện, cuộn ngang, viền, cố định STT + Mã phiếu)
- [ ] Deploy API + client cùng lúc; không có migration
