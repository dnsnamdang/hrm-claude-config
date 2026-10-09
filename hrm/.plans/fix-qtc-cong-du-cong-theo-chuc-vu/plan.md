# Fix: người đủ-công-theo-chức-vụ không hiện công trong phiếu QTC

## Bối cảnh / Bug
- Màn: Quyết toán công (settlement_contract) — bảng "IV. Bảng quyết toán công khoán theo hợp đồng".
- User báo: NV Trịnh Thị Lợi (chức vụ nằm trong cấu hình "Chức vụ luôn được tính đủ công hành chính (PCT kỹ thuật)", type=1) khi lập QTC **không hiện công** để quyết toán.
- Nguyên nhân gốc: `SettlementContractController::getDataForSettlementContract` (dòng 307-312) tính `coefficient_reality = sum(timesheet_detail_assigns.hour)/8` theo từng task. Người đủ-công-theo-chức-vụ **không chấm giờ theo task** → sum(hour)=0 → coefficient_reality=0 → FE (`SettlementCalcMixin.js:15-17`) ratio=0 → công QTC=0 = không hiện.
- Đoạn ép đủ công ở `TimesheetSummaryService.php:1128-1138` chỉ set `labour_day` cho bảng chấm công, KHÔNG áp vào coefficient QTC.

## Quyết định nghiệp vụ (user chốt — Cách 1)
- Với NV có chức vụ trong cấu hình đủ-công (type=1) mà coefficient theo giờ task = 0:
  → lấy `coefficient_reality = SUM(timesheet_summaries.labour_day)` của NV đó trong khoảng `from_time`→`to_time` của phiếu công tác (= số ngày đủ công trong kỳ).
- Người chấm công bình thường: giữ nguyên = tổng giờ thực tế trên task ÷ 8.

## Tasks
- [x] Trace root cause (BE getDataForSettlementContract + FE SettlementCalcMixin + TimesheetSummaryService đủ-công)
- [x] Xác nhận nguồn: `timesheet_summaries` có `employee_info_id`, `day`, `labour_day` (labour_day đã được đủ-công override set đầy đủ; ngày không đủ công = 0)
- [x] BE: `SettlementContractController::getDataForSettlementContract` — thêm fallback Cách 1 cho NV đủ-công (dòng ~307-312) + helper `getAlwaysFullTimeWorkingPositionIds()` (cache theo company)
- [x] BE: import `AssignConfig` + `TimesheetSummary`
- [x] `php -l` sạch
- [x] User verify (một phần): fix create đúng — NV 1214 (Trịnh Thị Lợi) chức vụ 26 ∈ config type=1, SUM(labour_day)=3.00

## Bổ sung 2026-08-05: công HC=0 khi SHOW/EDIT phiếu đã lưu
Bug: NV đủ-công có chấm công (công=1) nhưng bảng III QTC hiển thị "Tổng công HC thực tế" (coefficient_reality) = 0.
Nguyên nhân: `SettlementContractTransformer` (show/edit) đọc coefficient_reality ĐÃ LƯU (=0), không recompute → fix create-flow không cứu phiếu cũ.
Fix:
- [x] Tạo helper dùng chung `Modules/Assign/Services/SettlementFullTimeCoefficientResolver.php` (resolve coefficient_reality từ labour_day khi =0 + chức vụ ∈ config type=1)
- [x] Refactor `getDataForSettlementContract` (create) dùng helper (bỏ private method cũ)
- [x] Áp helper vào `SettlementContractTransformer` map assign_tasks.employees (show/edit) — dùng from_time/to_time đã lưu trên settlement_contract_assign_tasks
- [x] php -l 3 file sạch
- [ ] Deploy lên server test + user verify cả phiếu mới lẫn phiếu cũ hiện đúng công HC

## Ghi chú
- Gate chặt: chỉ override khi coefficient theo giờ = 0 VÀ `employee_work_position_id` ∈ cấu hình type=1 → không đụng NV thường / NV đủ-công có chấm giờ.
- Field chức vụ: `employee_infos.employee_work_position_id` (đúng field mà logic đủ-công đang dùng).
- Branch: `tpe` (cả API + Client). Chưa commit tới khi user xác nhận.
