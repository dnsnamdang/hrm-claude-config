# STATUS — ERP Tân Phát

## Đang làm

- [Fix báo cáo Tổng hợp bán hàng: cột SL trả lại](fix-summary-sale-sl-tra-lai/plan.md) — `SummarySaleReportService::getData()` hard-code `returned_qty=0`; thêm nhánh union nhập trả lại (type 4|9) định giá qua `product_export_detail_id`, netting đầy đủ tiền
- [Testcase: Chặn TP duyệt khi NV có hàng quá hạn](chan-tp-duyet-qua-han/plan.md) — testcase.xlsx 36 TC cho luồng `checkDueConfigsManager`/`DueConfigBlockService` (3 loại quá hạn, ~30 phiếu); HRM ở `HRM/.plans/chan-tp-duyet-qua-han/`
- [Lập HĐ ERP từ báo giá HRM](hrm-quotation-to-erp-contract/plan.md) — cross-system, 3 phase. **CODE DONE cả 3 phase (không commit), chờ test E2E.** Lập firm_contract ERP thẳng từ báo giá Assign HRM (status=7 + tmp synced + VND), bỏ firm-quotation. ERP đọc HRM qua connection `hrm`, popup "Báo giá HRM" prefill KH+SP, nới store()/request, schema `hrm_quotation_id` (migration đã chạy); ghi ngược HRM `erp_firm_contract_id` chống trùng; banner+nút deep-link bên HRM. Cặp HRM: `HRM/.plans/hrm-quotation-to-erp-contract/`. Verify: unit_id HRM=units.id ERP (không map); `php -l` toàn bộ sạch; route đăng ký OK.
- [Dashboard: PLBS trong nước chờ duyệt](dashboard-plbs-cho-duyet/plan.md) — thêm 2 ô đếm PLBS tự do (type=5) & theo hãng (type=4) chờ duyệt vào group "Đặt mua hàng trong nước" trong `HomeController::approveList()`, link `_type=for-approved`
- [Dashboard: Yêu cầu xuất tách chờ duyệt](dashboard-split-export-cho-duyet/plan.md) — thêm 1 ô đếm `SplitExportRequest` status=2 vào group "Kế toán kho" trong `HomeController::approveList()`, link `splitExportRequest.all`

## Chờ review / test

- [Fix: tiền VAT vận chuyển không về 0 khi xóa thành tiền](fix-delivery-vat-zero/plan.md) — directive dùng chung `inputGroupPercent` (`app.directive.js:725`) thiếu nhánh `value=0` → tiền VAT kẹt giá trị cũ; thêm early-return zero amount ở chế độ non-reCalc

- [Chặn nhập tồn kho đang về cho hàng đặt công ty](chan-nhap-ton-kho-dang-ve-hang-dat-cong-ty/plan.md) — FE ẩn option type 5 + BE validate `in:1,2,3,6` khi item thuần đặt công ty (root_order_request)

- [BillAdjustDept validate trùng cặp: bỏ qua khi không có HĐ](bill-adjust-dept-validate-trung-cap/plan.md) — `validateDetails()` chỉ check trùng khi dòng có `contractable_id`

- [Bypass duyệt kết quả PNKQ 5598 (HĐ 125)](bypass-duyet-ket-qua-pnkq-5598/plan.md) — bỏ qua check "đủ SL bàn giao" riêng phiếu 5598 (store+update); chấp nhận lệch dữ liệu, HĐ không quyết toán

- [Fix: Invoice2 lập nhiều lần/sửa với hàng chưa lập hết](fix-invoice2-lap-nhieu-lan-hang-chua-lap-het/plan.md) — BE revert `invoice_qty` ở update+delete (3 loại) tránh double-count; FE reconcile hàng bảo hành khi sửa

- [Fix: Invoice2 hàng bảo hành sửa SL & khai hải quan](fix-invoice2-hang-bao-hanh-sua-sl-khai-hai-quan/plan.md) — `invoice2/form.blade.php`: SL→input + bỏ `disabled` customs (BE/JS đã sẵn sàng)

- [Xuất excel chi tiết Phiếu xuất hàng (HĐH)](xuat-excel-chi-tiet-phieu-xuat-hang/plan.md) — code xong Task 1–9 (route/Excel class/controller/blade/2 nút), php -l sạch; chờ chạy thử + đối chiếu file mẫu (Task 10) + chốt 2 điểm: cột VAT bốc xếp (%/số tiền) & điều kiện hiện block vận chuyển
- [Điều kiện quyết toán công: yêu cầu đã quyết toán HĐ](quyet-toan-cong-yeu-cau-quyet-toan-hd/plan.md) — sửa `CheckContractIsDoneController` (firm cần status=10; wr HĐDV cần status=5, PBH giữ cũ); chờ test 4 ca
- [Fix: Số tiền thanh toán reload theo giá trị HĐ](fix-so-tien-thanh-toan-reload-theo-gia-tri-hd/plan.md) — $watch reset `_amount` ở FirmContract + WRInformation; fix typo `total.after_vat` ở WRServiceContractPayment
- [Fix: cảnh báo hàng mượn/giữ hết hạn theo warning_day](fix-canh-bao-hang-muon-giu-warning-day/plan.md) — `HomeController@approveList`: 2 filter dùng `now + warning_day` thay vì `now`
- [Fix: HĐ mới hiện sẵn NV/Phòng QTC](fix-qtc-hien-o-hop-dong-moi/plan.md) — sửa typo `ng-selected` (`=` → `==`) ở `firm/contracts/form.blade.php:325`
- [Fix: bug "chuyển duyệt" khi duyệt hỗ trợ hạch toán](fix-keychanged-support-accounting-chuyen-duyet/plan.md) — sửa `getKeysChanged` (fallback tên cột detail), chờ test tài khoản Đông trên HĐ 20479

## Hoàn thành

_(trống)_
