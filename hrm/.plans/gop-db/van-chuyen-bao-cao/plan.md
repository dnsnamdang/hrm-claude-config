# Vận chuyển - Bốc xếp — 9 báo cáo (đợt 1) — Plan

> Nhánh `feat/van-chuyen-bao-cao` (cả 2 repo, từ `develop`, 23/10/2026). Khuôn giao diện: skill `report-styles` (rsum);
> nghiệp vụ / quyền / menu: skill `erp-to-hrm-screen`.

## Thứ tự (user chốt 23/10)

1. 3 báo cáo bốc xếp: theo NCC · theo nhân viên · chi tiết theo nhân viên  — XONG 23/10 (chưa commit)
2. 5 báo cáo vận chuyển theo lái xe / hiệu quả gộp / chi tiết chuyến xe (nguồn `account_details`)
   — cặp theo lái xe XONG 24/10 (đã commit); hiệu quả gộp ×2 + chi tiết chuyến xe XONG 26/10 (chưa commit) → đợt 1 XONG
3. Thêm link "BC chi phí vận chuyển theo NV kinh doanh" (đã port `/sale/transport-cost-by-staff`) vào menu Vận chuyển

## Báo cáo bốc xếp — nghiệp vụ (ERP `ArrangeGoodController::reportArrangeGood*` + `ProductImportExportArrangeDeliveryExecutor`)

- Nguồn: `product_import_export_arrange_deliveries` (1 lượt bốc xếp của Phiếu nhập hàng / Phiếu xuất hàng, HRM đã ghi từ
  2 màn đó) + `product_import_export_arrange_delivery_executors` (người bốc xếp, `employee_price`).
- Theo NCC: lượt `rent_type = 2` (Thuê ngoài) có NCC; Số tiền = `total_money × (1 + vat%)`. Theo NV: tiền `employee_price`.
- Ngày hạch toán = `account_details.invoiceable_date_accounting` của Phiếu nhập/xuất hàng (class ERP `App\Model\Warehouse\
  ProductExport|ProductImport`).
- Quyền (tên y ERP, guard api, type 22 = Vận chuyển): "Xem báo cáo bốc xếp theo tổng công ty" (mọi công ty) / "… theo công ty"
  (NCC: công ty phiếu; NV: công ty nhân viên) / không quyền = của mình (NCC: phiếu mình lập; NV: lượt mình bốc xếp).
- **User chốt 23/10:** khuôn rsum; tổng tiền NCC cộng SAU VAT (ERP cộng trước VAT, lệch dòng); cả 3 báo cáo lọc theo
  NGÀY HẠCH TOÁN (ERP BC tổng theo NV lọc ngày tạo).
- Sửa lỗi ERP thêm: ô Nhân viên của BC theo NV không ăn (FE gửi `accounting_obj_id`); ô Công ty của BC theo NCC không ăn;
  N+1 truy vấn từng phiếu.

## Thiết kế

- BE `Modules/Finance/Services/ArrangeReport/{ArrangeReportService, ArrangeReportPrintService}`, controller
  `ArrangeReportController`, route `finance/arrange-reports/{supplier|employee}` (+ `/filter-options`, `/item-list`,
  `/export`, `/item-list/export`, `/print-list-data`). Dữ liệu nhỏ (≈ 400 lượt thuê ngoài, ≈ 2.900 dòng người bốc xếp) →
  lọc ở SQL, gom cây ở PHP.
- FE `pages/transport/arrange-reports/{by-supplier, by-employee, by-employee-detail}` + `components/` dùng chung (copy
  `template/` của skill, tiền tố `arr-`). Cây: NCC ▸ lượt · NV (1 cấp) · NV ▸ lượt.
- Menu: **phân hệ Vận chuyển của HRM** (user chốt 23/10, sau 1 lần đặt nhầm sang Kho) — bật phân hệ theo chuẩn hub như Kho
  (`subsystems.js` bỏ hidden/erpGhost, `HUB_SUBSYSTEMS`, Tổng quan `SubsystemHubOverview`); `transport.js` 4 nhóm theo
  mega-menu ERP: Chuyến xe · Báo cáo bốc xếp · Vận chuyển với NCC · Báo cáo vận chuyển (15 màn). ERP không gate quyền ở menu.

## Kết quả 3 báo cáo bốc xếp (23/10)

- [x] BE service + print service + Excel (2 dạng) + controller + route + 2 quyền (type 21) — PHPUnit `ArrangeReportApiTest` 6/6
- [x] FE 3 trang + component dùng chung, menu Kho › Vận chuyển - Bốc xếp (15 mục, 3 link + link BC NV kinh doanh)
- [x] Playwright: theo NCC (cây, popup drill, In danh sách qua chọn cột → bản in), theo NV (1 cấp), chi tiết theo NV (cây)
- ⚠ DB local: `supplier_id` của lượt bốc xếp trỏ id khách hàng ERP cũ, `gop_db.customers` local chưa có (5/5 NCC) → hiện
  "NCC #id". Cần kiểm trên DB dev/prod thật.
- 23/10 user báo ô NCC HRM chỉ hiện id: đổi ô "Nhà cung cấp" về y ERP — ô GÕ TÌM trên toàn bảng `customers`
  (port `Customer::searchCustomerByKeywords($kw, all=true)`, API `finance/arrange-reports/supplier/search-suppliers`),
  chọn nhiều; bỏ danh sách NCC cố định rút từ dữ liệu (tôi tự đổi, user nhắc KHÔNG tự sửa logic khi chuyển đổi).
- ERP dev lỗi `code of non-object` cùng gốc (NCC không có trong `customers`) — bản chặn vỡ commit `9903085e85` trên `develop_02`.

## 2 báo cáo chi phí vận chuyển theo lái xe (24/10/2026, chưa commit)

- ERP `ReportController::transportByDriver*` / `detailTransportByDriver*` + `AccountDetail::transportByDriverSearchData` …
  (AccountDetail.php:4386-4780). Nguồn `account_details` mã công việc CLX/XXE/CPK/VCD/CTP của phiếu hạch toán chuyến xe chở
  hàng / chuyến xe khác; 1 dòng = 1 phiếu hạch toán × 1 lái xe.
- **User chốt 24/10:** Cộng KHÔNG gồm Công tác phí (y ERP); % chênh lệch dòng lái xe / TỔNG = chênh lệch ÷ định mức (màn BC
  tổng ERP cộng dồn % ở dòng tổng là sai); thêm cột đếm "Số chuyến" bấm ra popup.
- Quyền tên y ERP, type 22, nhóm "Báo cáo vận chuyển": "Xem báo cáo vận chuyển theo công ty theo tổng công ty" / "… theo
  công ty" (công ty của lái xe); không quyền = bút toán mình lập (`created_by`).
- BE `Modules/Finance/Services/DriverCostReport/{DriverCostReportService, DriverCostReportPrintService}`, controller
  `DriverCostReportController`, route `finance/driver-cost-reports` (+ filter-options, item-list, export, item-list/export,
  print-list-data), Excel `DriverCostReportExport` (kế thừa `ArrangeReportExport`), dùng lại 4 blade in/Excel của báo cáo bốc
  xếp qua tham số `printer`. Ô Kỳ tách trait `Services/Concerns/ResolvesReportPeriod` (dùng chung với bốc xếp).
  PHPUnit `DriverCostReportApiTest` 5/5 + `ArrangeReportApiTest` 6/6.
- FE `pages/transport/driver-cost-reports/{summary, detail}` + `components/`. BC tổng: 1 cấp, tên lái xe mở BC chi tiết tab
  mới (giữ kỳ + công ty). BC chi tiết: Lái xe ▸ chuyến, đọc bộ lọc ban đầu từ query. Link phiếu hạch toán / chuyến xe mở ERP.
- Số liệu gop_db khớp SQL theo công thức ERP (tiền + km từng lái xe). KM thực chạy âm lớn do dữ liệu nhập sai km (ERP cũng vậy).

## 3 báo cáo còn lại (26/10/2026, chưa commit)

- **BC hiệu quả gộp xe vận tải** `/transport/trip-gross-reports/by-vehicle` + **BC chi tiết hiệu quả gộp theo chuyến xe**
  `/transport/trip-gross-reports/detail` — ERP `detailEffectiveTransportByDriver*` / `detailEffectiveByDriver*`. 1 chuyến = 1
  phiếu hạch toán đã hạch toán; Cước = `cost_need_allocation`, Chi phí lái xe = CLX+XXE+CPK+VCD của phiếu, Lãi gộp = hiệu.
  **User chốt 26/10:** gộp 1 dòng / biển số (ERP tách 2 loại chuyến → trùng dòng); cây Biển số ▸ chuyến; kỳ theo ngày hạch toán
  (ERP ngày cập nhật — trùng 100% gop_db); chi phí CỘNG cả bút toán không gắn lái xe (1.605 bút toán xăng ~125tr — ERP #6 có,
  #7 không). Chọn phiếu theo quyền / ô Lái xe, cộng mọi bút toán của phiếu. Đối chiếu năm 2026: 1.203 chuyến, 13 xe, Cước
  662.727.172, Chi phí 431.531.553 = SQL theo công thức ERP.
- **BC chi tiết chuyến xe** `/transport/trip-detail-report` — ERP `detailTripReport*`. Cây chuyến ▸ phiếu xuất/nhập; kỳ theo ngày
  tạo chuyến (y ERP); thêm khối tổng hợp + dòng TỔNG + cột "Số phiếu". **User chốt 26/10:** NVKD chuyến xe khác = người lập yêu
  cầu xuất/nhập (ERP đọc `activity_has_other_delivery_trip_accounting.employee_id` TINYINT → 399/530 dòng thành id 127).
  Quyền 5 tên y ERP (tổng công ty / công ty / phòng ban NVKD / mình lập — theo công ty / phòng / người lập CHUYẾN).
- BE: `Services/DriverCostReport/{TripAccountingQuery (truy vấn chuyến dùng chung), TripGrossReportService, TripDetailReportService,
  TransportReportPrintService (lớp cha in), *PrintService}`, `Controllers/V1/{TransportReportController (lớp cha), TripGross…,
  TripDetail…}`, route `finance/trip-gross-reports`, `finance/trip-detail-reports`. PHPUnit `TripReportsApiTest` 3/3 (tổng 14/14).
- FE: bộ dùng chung `pages/transport/components/{TransportReportPage, TransportReportTable, TransportReportSummary,
  TransportItemModal, configs/tripGross.js, configs/tripDetail.js}` — 3 trang chỉ truyền config. 2 BC theo lái xe GIỮ bộ
  component riêng (đã giao), có thể chuyển sang bộ chung sau.

## Ngày 28/10/2026 (@junfoke)
- [x] 28/10/2026 — Commit 5 báo cáo vận chuyển (2 BC chi phí vận chuyển theo lái xe + BC hiệu quả gộp xe vận tải, BC chi tiết hiệu quả gộp theo chuyến xe, BC chi tiết chuyến xe) và merge develop vào `feat/van-chuyen-bao-cao`: api `38e0313af` / `6e4e56904`, client `9629666cd` / `a833a0993`.

## Ngày 29/10/2026 (@junfoke)
- [x] 29/10/2026 — Lỗi #11910, #11911, #11916 (3 BC dùng chung component: hiệu quả gộp theo xe, chi tiết hiệu quả gộp, chi tiết chuyến xe): popup bỏ dòng "Bạn đang xem", ô tìm có nút x, mặc định 10 dòng, tiêu đề cột số canh phải + tooltip tiêu đề, ô 0 ở dòng chi tiết để trống, dấu ✓ đậm, ô tìm chi tiết chuyến bỏ phiếu/chuyến, giãn khối tổng hợp; Excel tiêu đề cột xuống dòng + nới cột; bản in chỉ thu chữ khi thật sự tràn (≤18 cột giữ 10px). Client `bc52f6154`, api `946cdb516` — đã lên origin/develop.
- [x] 29/10/2026 — Xác nhận nguyên nhân bằng SQL prod (phiếu hạch toán TPE_HTCXK_00417/00418 ↔ chuyến TPE_CXK_00437/00436), ghi vào memory.
- [x] 29/10/2026 — Xuất testcase BC chi tiết hiệu quả gộp theo chuyến xe: 111 TC (P0 41%) — kiểm số theo luồng phát sinh 15 TC, đối chiếu ERP - HRM 14 TC, đối chiếu nội bộ HRM 5 TC, 11 điểm khác ERP đã chốt. File `testcase/testcase - BC chi tiet hieu qua gop theo chuyen xe.xlsx`.
