# Tooltip chart cột báo giá — tách Trong thầu / Ngoài thầu — @khoipv

## Bối cảnh
- Màn `plan/dashboard` → `PlanDashboard.vue:423` render `FilterColumnChartCard` (title "Biểu đồ số lượng báo giá theo trạng thái trên từng nhân viên", `module="quotation"`).
- Series là 4 nhóm trạng thái gộp từ BE `CategoryDashboardService::getAllQuotationStatusMapping()`:
  Đang thực hiện / Đang thực hiện đã duyệt / Không thực hiện / **Đã thực hiện**.
- Tooltip hiện tại là tooltip mặc định ApexCharts (`ColumnChart.vue`, `shared: true`) → chỉ hiện `tên nhóm: số lượng`.

## Yêu cầu
Hover cột của 1 nhân viên → tooltip hiện thêm: trong số nhóm **"Đã thực hiện"** có bao nhiêu **Trong thầu**, bao nhiêu **Ngoài thầu**.
Logic đếm cũ giữ nguyên, chỉ bổ sung thông tin.

## Quyết định (đã chốt với user)
- Chỉ tách cho nhóm **"Đã thực hiện"**, các nhóm khác giữ nguyên.
- Nguồn phân loại: `quotations.project_type` — `1 = Trong thầu`, `2 = Ngoài thầu`.
- `project_type` 4/5/6 (HĐ Cho-Tặng, Đặt-Mượn, Nguyên tắc) **bỏ qua** → TT + NT có thể < số cột.
- Layout tooltip:
  ```
  NV.00001 - Nguyễn Văn A
  ─────────────────────────
  ■ Đang thực hiện: 12
  ■ Đang thực hiện đã duyệt: 4
  ■ Không thực hiện: 3
  ■ Đã thực hiện: 8
     Trong thầu: 6 | Ngoài thầu: 2
  ─────────────────────────
  Tổng: 27
  Đã thực hiện — TT: 6 | NT: 2
  ```

## Task
### BE (`hrm-thanhan-api`)
- [x] `Modules/Category/Services/CategoryDashboardService.php` → `getQuotationColumnChart()`: thêm key `bidBreakdown`
      (`statusId`, `statusText`, `in[]`, `out[]` theo đúng thứ tự `categories`), dùng 1 query `groupBy(created_by, project_type)`
- [x] Chỉ trả `bidBreakdown` khi nhóm "Đã thực hiện" nằm trong `filteredStatusMapping` (tôn trọng bộ lọc trạng thái)
- [x] Không đụng `getBidPackageColumnChart` / `getContractColumnChart`

### FE (`hrm-thanhan-client`)
- [x] `components/charts/FilterColumnChartCard.vue`: nhận `bidBreakdown` từ API → `localChartData` → truyền prop xuống `ColumnChart`
- [x] `components/charts/ColumnChart.vue`: thêm prop `bidBreakdown` (default `null`) + custom tooltip
- [x] Opt-in: `bidBreakdown = null` → giữ nguyên tooltip mặc định (BidPackageDashboard / ContractDashboard không đổi)

- [ ] Verify UI trên `plan/dashboard`

## Phạm vi file
- `hrm-thanhan-api/Modules/Category/Services/CategoryDashboardService.php`
- `hrm-thanhan-client/components/charts/FilterColumnChartCard.vue`
- `hrm-thanhan-client/components/charts/ColumnChart.vue`

### Checkpoint — 2026-09-22
Vừa hoàn thành: BE trả `bidBreakdown`, FE truyền prop + custom tooltip trong `ColumnChart.vue`.
Đang làm dở: (không)
Bước tiếp theo: User mở `plan/dashboard` hover cột để verify UI.
Blocked:

**Kết quả chạy thử service (DB thanhan_stag_22092026, 01/2025–12/2026):**
- 25 nhân viên, nhóm "Đã thực hiện" tổng 430
- bidBreakdown: Trong thầu 270 + Ngoài thầu 110 = 380
- Chênh 50 = báo giá `project_type` 4/5/6 (HĐ Cho-Tặng 8, Đặt-Mượn 9, Nguyên tắc 33) — đúng như đã chốt là bỏ qua
