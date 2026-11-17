# Định nghĩa loại phiếu — nhóm Tài chính / Kho (Trung tâm phê duyệt) — @cuong61n

Ngày 16/11/2026. Nhánh `gop_db-main`, DB local `local_hrm_erp`. Mỗi loại = 1 `Definitions/Finance/*Definition.php` + test `tests/Feature/ApprovalCenter/Finance/*Test.php` + trait `SyncsApprovalInbox` trên model nguồn. Mọi gate đọc lại từ code đang chạy (không chỉ từ `01-tai-chinh.md`); chỗ nào báo cáo gốc lệch code thì ghi ở mục "Sửa so với báo cáo gốc".

## 1. Quy ước chung của nhóm (đọc trước)

- **Quyền tính theo CÔNG TY ĐANG LÀM** (`current_company_role`) ⇒ mỗi người duyệt = cặp (employees.id, công ty c nơi họ giữ mã) — `FinanceApprovalSupport::permissionApprovers()`.
- **"Cùng công ty" của entity (`sameCompanyAsCurrent`, `currentCompanyId()`) là CÔNG TY GỐC `employee_infos.company_id`**, KHÔNG phải công ty đang làm. Người kiêm nhiệm có mã ở công ty B nhưng công ty gốc A duyệt được phiếu công ty A khi đang đứng ở B (Definition mô phỏng đúng: `sameHomeCompanyApprovers()`).
- 4 kiểu "quản lý" (không chuẩn hoá chung, mỗi Definition dùng ĐÚNG kiểu của màn gốc):
  - K1 chỉ pivot theo công ty gốc (Đề nghị thanh toán TP) — `pivotManagers()`.
  - K2 pivot (mọi dòng, department NULL tính 0) + phòng mình ngồi, không cờ `all_department` — `k2Departments()` (Gia hạn / Xuất giữ / Điều chuyển hàng giữ).
  - K3 `manageDepartmentIdsOf` (CÓ cờ `all_department`) + phòng mình ngồi — `k3Departments()` (chỉ Gia hạn hàng mượn).
  - K4 `currentManagedDepartmentIds` (pivot theo công ty gốc, giữ NULL, so `in_array` LỎNG) — `k4Departments()` (Xuất bán hàng mượn TP).
- Trait dùng chung `Definitions/Finance/Concerns/FinanceApprovalSupport.php`, `ThreeLevelApprovalSupport.php` (3 màn Hàng giữ TP→BGĐ→KT). Tên file không kết thúc `Definition.php` nên Registry không nạp.
- Màu trạng thái: nơi Entity có `STATUSES[].color` thì dùng đúng màu đó; nơi không có (Đề nghị thanh toán / thu / Phiếu thu / chi / Xuất bán hàng mượn / Yêu cầu nhập hàng / Hạch toán bổ sung / Điều chỉnh công nợ) dùng `#D97706` (mã "chờ duyệt" trong 9 mã chuẩn) vì Entity không có accessor màu.
- Không loại nào chặn người lập tự duyệt ⇒ `excludeOwn()` = false (mặc định) ở tất cả.

## 2. Bảng từng loại

| doc_type | màn (FE) | cấp → gate | ghi chú nổi bật |
|---|---|---|---|
| `bill_payment_request` | /finance/bill-payment-requests/{id} | st2 TP: `finance.de_nghi_thanh_toan_truong_phong.approve` + K1 + cùng công ty gốc · st3 KT công nợ · st4 KT trưởng · st5 BGĐ (mỗi cấp 1 mã, cùng công ty gốc) | st6 "Chờ tạo phiếu chi" KHÔNG đưa vào (không có nút Duyệt). Tiền = cột của cấp TRƯỚC như danh sách gốc. |
| `bill_income_request` | /finance/bill-income-requests/{id} | st2: `finance.ke_toan_thanh_toan.manage`, KHÔNG kiểm công ty | truth = `canReject()` (nút Không duyệt) — nút Tạo phiếu thu chặt hơn 1 vế "chưa có phiếu thu". |
| `addition_accounting_request` | /finance/addition-accounting-requests/{id} | st2: loại≠7 `ke_toan_thanh_toan.manage`+cùng công ty gốc; loại 7: công ty gốc ∈ công ty phòng hỗ trợ, Từ chối cần `ke_toan_thanh_toan.manage`, Lập phiếu cần `accounting.ke_toan.manage` | truth = `canReject() \|\| canCreateAccountingBill()`. |
| `bill_adjust_dept_request` | /finance/bill-adjust-dept-requests/{id} | st2: `ke_toan_thanh_toan.manage` + `company_id` phiếu = công ty gốc | danh sách gốc lọc theo công ty NGƯỜI LẬP (lệch), nút lọc theo `company_id` phiếu — Definition theo nút. |
| `borrow_extend_request` | /finance/borrow-extend-requests/{id} | st4 TP (K3) → st5 BGĐ → st2 KT kho (`accounting.ke_toan_kho.manage`); cùng công ty gốc | truth = `canApproveAnyLevel()`. |
| `prepick_extend_request` | /finance/prepick-extend-requests/{id} | st5 TP (K2, phòng phiếu) → st4 BGĐ → st2 KT (3 mã `finance.hang_giu_*.approve`) | |
| `product_prepick_request` | /finance/product-prepick-requests/{id} | st6 TP (K2, phòng phiếu) → st4 BGĐ → st2 KT (nút Lập phiếu xuất giữ / Từ chối) | truth = `canReject()`; st5 "Đang xuất giữ" rời hộp chờ. |
| `prepick_transfer_request` | /finance/prepick-transfer-requests/{id} | như trên nhưng TP xét phòng của NGƯỜI NHẬN (`to_employee`) | từ chối → st3 "Không duyệt". |
| `prepick_cancel_request` | /finance/prepick-cancel-requests/{id} | st2: `finance.giu_hang.manage`, KHÔNG kiểm công ty | ~584 người giữ mã ⇒ nhiều dòng người duyệt/phiếu. |
| `borrow_sell_request` | /finance/borrow-sell-requests/{id} | st10 TP (K4) → st11 BGĐ → st2 KT kho; KHÔNG cấp nào kiểm công ty phiếu | truth = `canDeny()`. |
| `product_import_request` | /finance/product-import-requests/{id} | st12 TP / st10 BKS / st11 BGĐ chỉ cần mã; st2 KT kho `accounting.ke_toan_kho.manage` (+ ngoại lệ định danh) | KHÔNG kiểm phòng / công ty ở mọi cấp. Loại 6 chỉ người tạo; loại 7 thêm người tạo YC xuất nguồn (mọi công ty đang làm, không cần mã); nhập thẳng dùng `canProductImport`. |
| `bill_income` (Phiếu thu) | /finance/bill-incomes/{id} | st2: `finance.phieu_thu.approve`, không kiểm công ty | tiền = `sum_money` (VND). |
| `bill_payment` (Phiếu chi) | /finance/bill-payments/{id} | st5 KT trưởng `finance.phieu_chi_ke_toan_truong.approve` → st2 Thủ quỹ `finance.phieu_chi_thu_quy.approve`; cùng công ty gốc | tiền = `sum_payment_money_approve_exchange` (VND). |
| `bonus_end_year_settlement` | /finance/bonus-end-year-settlements/{id} | st2 BGĐ: tên quyền cũ "BGĐ duyệt quyết toán thưởng năm" (alias), không kiểm công ty | Quyết toán thưởng năng suất QUÝ không có bước chờ ⇒ bỏ. |
| `buy_service_request` | /finance/buy-service-requests/{id} (sourceSubsystem `sale`) | st2 TP chỉ mã `sale.yeu_cau_mua_dich_vu_truong_phong.approve` (không phòng, không công ty) → st3 KS `sale.gia_mua_dich_vu_ban_kiem_soat.approve` + cùng công ty gốc | danh sách gốc lọc phòng K2 (hẹp hơn gate) — theo gate. |
| `self_inventory` | /warehouse/self-inventories/{id} | st2: `warehouse.ket_qua_kiem_ke.approve`, không kiểm công ty | |
| `position_inventory_result` | /warehouse/position-inventory-results/{id} | st2: cùng mã trên; chỉ `type = 1` | phiếu KẾ HOẠCH (type 0) không có bước duyệt. |
| `inventory_audit_report` | /finance/inventory-audit-reports/{id} | st1: `warehouse.bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.approve`, không kiểm công ty | chỉ có Duyệt. |

## 3. Loại KHÔNG đưa vào + lý do

- **Duyệt giá bán hàng hoá** (`product_approves`, MasterData) — HOÃN, chưa làm. Chưa có Eloquent model (toàn bộ ghi bằng `DB::table`), "phiếu chờ" = SỰ TỒN TẠI dòng và bị XOÁ khi duyệt / từ chối ⇒ cần ≥ 10 điểm `scheduleSync` rải ở `ProductPriceApprovalSubmitter`, `ProductPriceSetWriter`, `InheritedPriceSync`, `ProductLifecycleService`, `ProductPriceWriter`, `ManufacturePriceModeService`, `PriceCalculateWriter`… + dựng model trong phạm vi nhóm khác (MasterData). Gate bản thân đơn giản (mã `finance.gia_ban_hang_hoa.approve` + `company_id` = công ty đang làm). Bảng local rỗng ⇒ không có dữ liệu thật để đối soát. Cần điều phối quyết định cho sửa MasterData.
- **Điều chuyển kho** (`warehouse_transfers`) — BỎ: gate đọc bảng `warehouse_accountants` (RỖNG 0 dòng ở DB gộp, `PrepickCancelRequestService` đã ghi nhận bảng này chết; bảng sống là `accounting_warehouse_accountants`) VÀ còn đòi phiếu nằm trong `scopedQuery` bằng 4 tên quyền xem cũ ⇒ hiện không ai duyệt được, 0 phiếu. Đó là lỗi code gốc, ghi ở mục 5.
- **Chỉ tiêu kinh doanh** (phòng ban / nhân viên) và **Phân chia thị trường theo nhân viên** — đã có `Definitions/Sale/BusinessTarget*Definition.php`, `DivisionMarketEmployeeDefinition.php` do nhóm Bán hàng làm; KHÔNG làm lại để khỏi trùng. **Phân chia thị trường theo phòng ban** không có trạng thái chờ (1 Đang tạo → 2 Đã duyệt) ⇒ không đưa vào.
- **Quyết toán thưởng năng suất quý** — không có bước chờ duyệt (người lập có mã "Tạo/Duyệt" lưu là duyệt luôn).
- **Đề nghị nhập kho (`warehouse_import_requests`, thủ kho), Yêu cầu vận chuyển, Chuyển hàng nhập thẳng, Yêu cầu chuyển hàng, Yêu cầu xuất mượn, YCXH vượt hạn mức, Kế hoạch NV, Hạch toán mua dịch vụ** — không nằm trong danh sách ưu tiên của đợt này, chưa làm (xem `01-tai-chinh.md` mục 14–19 để làm tiếp; gate đã khảo sát).

## 4. Điểm ghi bằng query builder đã xử lý (`ApprovalInboxService::scheduleSync`)

| File | Chỗ | doc_type |
|---|---|---|
| `Modules/Finance/Services/BillIncomeWriteService.php` `markRequestCreatedAndNotify()` | `BillIncomeRequest::query()->update(status 3)` | `bill_income_request` |
| `Modules/Finance/Services/BillAdjustDeptSourceService.php` `onBillCreated()` | `AdditionAccountingRequest ... update(status 4)` | `addition_accounting_request` |
| cùng file `onBillDeleted()` | `AdditionAccountingRequest ... update(status 2)` (trả lại chờ) | `addition_accounting_request` |
| cùng file `changeAdjustRequestStatus()` | `BillAdjustDeptRequest ... update(status)` | `bill_adjust_dept_request` |
| `Modules/Finance/Services/ProductImportService.php` (2 chỗ: `DANG_HACH_TOAN`, `closeSourceImportRequest` → `DA_HACH_TOAN`) | `DB::table('product_import_requests')->update` | `product_import_request` |

Đã rà (đều Eloquent `save()` nên trait tự đồng bộ): Đề nghị thanh toán, Gia hạn hàng mượn, 3 màn Hàng giữ, Hủy giữ, Xuất bán hàng mượn, Phiếu thu/chi, Quyết toán thưởng năm, Mua dịch vụ, Kiểm kê (2), Biên bản. Các `update()` còn lại của đề nghị thanh toán / thu tiền (→ st7/8/9, → st4/5) chỉ chạy khi phiếu đã rời hộp chờ nên không cần.
Model `ProductImportRequest` không khai `$fillable` và hook `creating`/`updating` cần người đăng nhập (ghi lịch sử bằng `auth()->id()`, gán đè cấp tổ chức) ⇒ `seedTest()` của loại này đăng nhập thay người lập.

## 5. Lỗi / lệch của code gốc phát hiện (CHỈ ghi, không sửa)

1. Phần lớn luồng không kiểm công ty của phiếu (Y1): Đề nghị thu tiền (duyệt + không duyệt), Hủy giữ, Xuất bán hàng mượn (cả 3 cấp), Yêu cầu nhập hàng (cả 4 cấp), Phiếu thu, Quyết toán thưởng năm, Kiểm kê (2), Biên bản, Mua dịch vụ cấp TP — người giữ mã ở công ty nào cũng duyệt phiếu công ty khác.
2. Đề nghị thu tiền: `changeStatus` (Không duyệt) chỉ kiểm `isAccountant()` + `status==2`, docblock service nói gọi `canReject()` nhưng controller không gọi ⇒ không kiểm công ty; màn "Chờ duyệt" gốc lại lọc công ty.
3. `ChecksEmployeePermission::currentCompanyId()` = công ty GỐC, còn quyền = công ty ĐANG LÀM ⇒ lệch với người kiêm nhiệm (mô phỏng đúng ở mọi Definition dùng `sameHomeCompanyApprovers`).
4. Hàng giữ / Gia hạn / Điều chuyển (K2): người KHÔNG phải quản lý nhưng ngồi đúng phòng của phiếu và có mã TP vẫn duyệt được, kể cả phiếu do chính mình lập. Cờ `all_department` bị bỏ sót ở 8/9 luồng TP (chỉ Gia hạn hàng mượn K3 tính).
5. Xuất bán hàng mượn (K4): `in_array` lỏng ⇒ phiếu `department_id = NULL` khớp dòng cờ "tất cả phòng ban" (department NULL) của TP; `waiting_approve` gốc trả mọi phiếu chờ KT kho cùng công ty cho BẤT KỲ AI (không kiểm quyền).
6. Yêu cầu nhập hàng: TP cấp 12 không kiểm phòng; loại 7 cho người tạo YC xuất nguồn duyệt không cần mã ở mọi công ty; thông báo TP (`tpApproverIdsForDepartment`) lọc phòng trong khi gate duyệt không lọc.
7. Điều chuyển kho: gate đọc `warehouse_accountants` rỗng ⇒ không ai duyệt được (nghi hỏng sau khi gộp DB).
8. Phiếu thu / Phiếu chi / Quyết toán thưởng năm / Kiểm kê vị trí: màn gốc không có danh sách "chờ tôi duyệt" — người duyệt chỉ thấy phiếu qua quyền xem theo cấp (Y5); Trung tâm phê duyệt vá đúng chỗ thiếu này.
9. Đề nghị thanh toán: `canApproveAtCurrentStatus()` trả true cả ở st6 ("Chờ tạo phiếu chi") nhưng FE/danh sách loại st6 khỏi `is_can_approve` (không có nút Duyệt) — Definition theo FE.
10. Đề nghị thanh toán: số tiền hiện ở danh sách = cột của CẤP TRƯỚC (BGĐ không thấy số KT trưởng vừa chỉnh) — đã nêu ở `cot-gia-tri.md`, Definition giữ nguyên để khớp danh sách, cần user chốt.
11. Báo cáo gốc `01-tai-chinh.md` §3: nói "Lập phiếu kế toán" mở sang cổng ERP — code hiện tại đã mở màn HRM `/finance/bill-adjust-depts/create` ⇒ Yêu cầu hạch toán bổ sung CÓ bước duyệt thật trên HRM (đã đưa vào).

## 6. Số liệu local (phiếu đang chờ thật trong DB `local_hrm_erp`, 16/11/2026)

Đề nghị thanh toán 40 · Đề nghị thu tiền 4 · Hạch toán bổ sung 45 · Điều chỉnh công nợ 49 · Gia hạn hàng mượn 3 · Gia hạn hàng giữ 3 · Xuất giữ 8 · Điều chuyển hàng giữ 4 · Hủy giữ 0 · Xuất bán hàng mượn 1 · Yêu cầu nhập hàng 35 · Phiếu thu 8 · Phiếu chi 2 · Quyết toán thưởng năm 0 · Mua dịch vụ 0 · Kiểm kê hàng hoá 0 · Kiểm kê vị trí 0 · Biên bản 0 (0 ⇒ chỉ có phiếu thử trong test / seed).

## 7. Cách kiểm lại

- `cd hrm-api && vendor/bin/phpunit tests/Feature/ApprovalCenter/Finance` (83 test, ~1 phút).
- `php artisan approval-center:seed-test <doc_type> --count=6` → `php artisan approval-inbox:verify <doc_type>` → `approval-center:clean-test` (cẩn thận: lệnh clean xoá cả phiếu thử của nhóm khác trong manifest).
- Test dùng `FinanceTestData::grantRole()` (Vai trò thử trong giao dịch, tự rollback) + `roleLessEmployee()` + `addManagerRow()` để dựng tổ hợp "chỉ có mã A / ngồi phòng / quản lý phòng khác / cờ tất cả phòng" mà dữ liệu thật không phủ hết — đây là chỗ đột biến bị bắt (xem kết quả đột biến trong báo cáo cuối).
