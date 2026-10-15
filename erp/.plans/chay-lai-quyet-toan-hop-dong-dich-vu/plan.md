# Chạy lại quyết toán hợp đồng dịch vụ (WrServiceContract)

## Mục tiêu
Thêm chức năng "Chạy lại quyết toán HĐ dịch vụ" ở màn admin/run_support_accounting/form,
song song với "Quyết toán HD hãng" đã có.

## Bối cảnh / root cause
- "Quyết toán HD hãng" = flag settlement_contract → RunSetlementContract → FirmSettlementContractAccountingService
  (có cờ $re_run + null-safe nên chạy lại được).
- RunSetlementContract có nhánh WrServiceContract nhưng HỎNG: (1) không import WrSettlementContractAccountingService,
  (2) truyền null request trong khi WR service đọc thẳng $request->receive_percent (không fallback).
- WR ghi chi tiết vào WrSettlementContractDetail (wr_detail), KHÔNG phải firm_detail.

## Đã làm (branch master)
- [x] WrSettlementContractAccountingService::processAccounting: $request nullable + optional() + fallback %.
      getSettlementInfo tự tính receive_percent khi truyền null → re-run đúng. CREATE flow giữ nguyên.
      (cả storeSettlementTab null-safe). php -l sạch.
- [x] Job mới RunWrSettlementContract: xóa employees/departments/wr_detail + tabs + AccountDetail → processAccounting($set, null).
      setUser cho queue. Scope contractable_type = WrServiceContract. php -l sạch.
- [x] Controller RunSupportAccountingController: import + nhánh settlement_wr_contract == 'true' → dispatch job.
- [x] View form_run_support_accounting: checkbox "Quyết toán HĐ dịch vụ" (ng-model form.settlement_wr_contract).
- [ ] User test: nhập số HĐ dịch vụ vào "Số hợp đồng", tick "Quyết toán HĐ dịch vụ", RUN → so số quyết toán + hạch toán.

## Không đụng
- RunSetlementContract (giữ nguyên, không sửa bug WR cũ ở đó — job mới thay thế cho HĐ dịch vụ).

## Branch: master
