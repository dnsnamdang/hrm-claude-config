# Plan — Khai báo đầu kỳ công nợ (KH + NCC)

> Phụ trách: @junfoke · Tạo 2026-10-01
> Design: `.plans/gop-db/finance-declare-debt-beginning/design.md`

## Phase 0 — Khảo sát + chốt

- [x] Khảo sát ERP 2 màn (controller, model, view, import, export, quyền, nơi đọc dữ liệu)
- [x] Soi dữ liệu gop_db: 1.746 / 1.141 dòng, TK 1311 / 3311, `configs.debt_calculation_date`
- [x] User chốt 8 điểm (xem design.md)

## Phase 1 — BE (gộp cả KH + NCC vì 2 màn dùng chung lõi)

- [x] `Services/DeclareDebt/DeclareDebtContractRegistry` — bảng tra 11 class HĐ ERP → bảng
- [x] `Services/DeclareDebt/DeclareDebtPostingService` — ghi / sửa / xoá `account_details`, cờ phát sinh
- [x] `Entities/Contract/Concerns/DeclareDebtCommon` — phạm vi xem 4 cấp + quyền (trait)
- [x] Entity `DeclareDebtBeginning` (bỏ chỉ-đọc, BaseModel) + `DeclareDebtSupplierBeginning` (mới)
- [x] `AbstractDeclareDebtService` + 2 service con (lọc, lưu, sửa, xoá, lịch sử, import, xuất, in)
- [x] `DeclareDebtRequest` / `DeclareDebtSupplierRequest`, `DeclareDebtResource`
- [x] `AbstractDeclareDebtController` + 2 controller, 24 route (`foreach` 2 prefix)
- [x] `CatalogHistoryService::TABLES` + `ExportColumnRegistry` thêm 2 màn
- [x] Seeder quyền id 1615-1622 (guard api trùng tên ERP) + insert DB local
- [x] Kiểm bằng API thật: list/lọc/sort, form-options, objects, contracts, show, store (lỗi + trùng),
      update, lịch sử, delete (sổ xoá theo), import validate, export-rows, print — cả 2 màn
- [x] Đối chiếu dòng `account_details` sinh ra với dòng ERP cũ: khớp từng cột

## Phase 2+3 — FE (gộp 2 màn: component DÙNG CHUNG + cấu hình)

- [x] `utils/finance/declareDebtConfigs.js` — cấu hình KH / NCC (cột import, trường xuất, endpoint…)
- [x] `components/finance/declare-debt/` DeclareDebtList · DeclareDebtForm · DeclareDebtContractPicker ·
      ContractCodeLink (dùng `utils/contract-link.js`)
- [x] 8 trang mỏng `pages/finance/declare-debt-{,supplier-}beginnings/` index · add · _id/edit · _id/index
- [x] Menu `finance.js`: 2 mục nhóm "Khai báo đầu kỳ" + mục "Công nợ đầu kỳ theo KH - HĐ" (nhóm Kế toán
      công nợ — ERP đặt màn KH ở 2 chỗ)
- [x] Import (buildImportTemplate, payload `rows`) · Xuất (ExportFieldsModal + listExportFile) · In
      (mẫu ERP, chặn 2.000 dòng) · Lịch sử 2 nơi (CatalogHistoryModal + SystemInfoSection)

## Phase 4 — Kiểm tra

- [x] Playwright: danh sách KH/NCC, bộ lọc nâng cao (bấm Loại dư → 1.175 dòng khớp DB), Thêm mới
      (lỗi chưa chọn KH, popup chọn HĐ, dòng "Đã khai báo" không thêm được, lỗi 422 theo dòng, lưu
      thành công), Chi tiết + Lịch sử, Sửa + cảnh báo chưa lưu, In danh sách, popup Xuất, NCC ngoại tệ
- [x] Đối chiếu `account_details` sinh từ giao diện (KH + NCC USD) — khớp ERP
- [x] Grep tự kiểm skill (HTML thô, vi-VN, Người lập, action.key, Tất cả) — sạch
- [x] Dọn dữ liệu test + quyền cấp tạm trên DB local
- [ ] Chưa bấm thật: tải file Excel (trình duyệt MCP đóng giữa chừng — đã kiểm `export-rows` qua API),
      luồng Import trên giao diện (đã kiểm validate qua API)

## Phase 5 — Tài liệu cho tester

- [x] 2026-10-02 testcase bám luồng ERP, mỗi TC có dòng "Đối chiếu ERP" khi HRM khác ERP —
      `gen_testcase.py` sinh `testcase HRM - Khai bao dau ky cong no.xlsx` (74 TC, P0 54%) và
      `testcase HRM - Khai bao dau ky cong no nha cung cap.xlsx` (79 TC, P0 53%)
- [x] 2026-10-02 testcase THUẦN ERP (thao tác, nhãn, thông báo của ERP) — `gen_testcase_erp.py` sinh
      `testcase ERP - Khai bao dau ky cong no.xlsx` (52 TC) và `testcase ERP - Khai bao dau ky cong no nha cung cap.xlsx` (53 TC)

### Checkpoint — 2026-10-01 11:30
Vừa hoàn thành: BE + FE 2 màn, kiểm API + Playwright
Đang làm dở: —
Bước tiếp theo: user nghiệm thu; chạy SQL quyền 1615-1622 trên server; bấm thử Import + tải Excel
Blocked:
