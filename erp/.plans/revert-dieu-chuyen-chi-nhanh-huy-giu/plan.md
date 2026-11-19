# Plan — Revert điều chuyển chi nhánh (hủy giữ trước) + chặn tại YCXH

## Tasks

### Phần D — Xác minh (xong)
- [x] D1: Xác nhận direct/non-direct cùng qua `ProductExport::updateWarehouse`, switch = `can_export_from_prepick`.
- [x] D2: Commit `4ba07a032e` → GIỮ (còn đúng cho direct type 7, vô hại non-direct).

### Phần A — Revert xuất-theo-giữ (chỉ non-direct)
- [x] A1: `WarehouseExportRequest::getCanExportFromPrepickAttribute()` — nhánh type 7 thêm
      `&& optional($this->product_export_request)->is_export_direct`.
- [x] A2: Verify nhánh non-direct type 7 ở `validateProducts` — sau A1 `can_export_from_prepick=false`
      → rơi nhánh `else` (:772) "Chỉ xuất từ sl tồn" (`in_stock - in_promotion_stock`, `in_stock` KHÔNG gồm giữ);
      `$employee_id` (:695) vô hại vì nhánh else bỏ qua prepick_qty. Đúng logic cũ.
- [x] A3: FE `formJs.blade.php` — `employee_id` param ở `updateStock` (:45) ĐÃ gate sẵn
      `(form.type==7 && form.is_export_direct)` → non-direct không gửi employee → stock hiện TỒN.
      Không có getter `can_export_prepick` riêng.

### Phần B — Bỏ guard 1 YCXH : 1 KD cho non-direct
- [x] B1: `ProductExportRequestsController.php` store — guard `count(created_by)>1` chỉ chạy khi `is_export_direct`.
- [x] B2: `ProductExportRequestsController.php` update — y hệt B1.
- [x] B3: FE `formJs.blade.php` — `updateStock` (:22) + `chooseProductTransferRequest` (:219) chỉ chặn khi
      `is_export_direct`. `checkWithCreator` (:239) là DEAD CODE (không gọi đâu) → để nguyên.

### Phần C — Chặn hủy giữ tại YCXH (chỉ non-direct)
- [x] C1: store — khi `!is_export_direct`: gọi helper mới `validateTransferHoldReleased($ycchIds, $export_company_id)`
      quét YCCH → gom product theo KD → `PrepickDetail(product_id, employee_id=KD, company_id=export_company_id, qty>0)`
      > 0 → `responseErrors('...', ['product_transfer_requests' => $msgs])` gom theo KD.
- [x] C2: update — y hệt C1 (cùng helper).
- [x] C3: FE `form.blade.php` khối YCCH — đổi `errors['product_transfer_requests'][0]` → `ng-repeat` hiện HẾT dòng lỗi.

### Verify
- [x] V1: `php -l` sạch 4 file sửa.
- [x] V2: 3 chỗ FE mirror khớp (BE A1 + FE employee_id :45 + same-creator guards). Cột "Đang giữ" chỉ display, không phải switch.
- [x] V3: SELECT read-only trên PROD — schema đủ (prepick_details.product_id/employee_id/company_id/qty,
      ptr_products.parent_id/product_id, ptr.created_by, per.export_company_id/is_export_direct); ca YCXH#42524
      (non-direct, KD 331, product 48334, cty nguồn 1) → giữ=0, query enforcement chạy đúng.

### Test tự động trên DB local erp_new (2026-10-03)
- [x] T-switch: `can_export_from_prepick` trên WER#36298 type7 — is_export_direct=1→true (xuất giữ),
      =0→false, =null→false (test RAM, không save).
- [x] T-enforce: gọi method thật `validateTransferHoldReleased` qua reflection —
      ca còn giữ (YCCH#7966, Hồ Ngọc Tiến giữ 1 SP, cty4)→CHẶN đúng câu;
      cùng YCCH khác cty nguồn→CHO QUA; nhiều YCCH nhiều KD cùng cty→CHẶN gom 10 dòng;
      ids rỗng→CHO QUA; company_id null→CHO QUA.
- [x] T-fix: phát hiện Employee KHÔNG có cột `name` → sửa helper dùng `full_name` (accessor). php -l lại OK.
- [x] T-browser: FE Angular qua Playwright trên local erp_new (http://127.0.0.1:8001) — ca CHẶN non-direct:
      type=7, "Gửi đến công ty"=cty4, "Nhập về kho", chọn YCCH PYCCH-TESTREVERT (KD Đào Thị Thúy giữ 5
      "Tay cân lực 1/2 inch" tại cty nguồn 4), "Nhân viên vận chuyển" → bấm Lưu.
      Kết quả: POST `/admin/warehouse/product_export_requests` trả HTTP 200 `success:false`,
      `errors.product_transfer_requests[0]` = "Kinh doanh Đào Thị Thúy đang giữ 5 Tay cân lực 1/2 inch
      tại công ty nguồn. Cần hủy giữ trước khi lập yêu cầu xuất điều chuyển."; FE render inline đỏ
      (`.invalid-feedback.d-block.ng-scope`, ng-repeat C3). KHÔNG redirect, KHÔNG ghi DB (verify
      product_export_requests type7 hôm nay rỗng + YCCH 7969 product_export_request_id=null).
      Đã dọn fixture (prepick_details 65021, ptr 7969, ptr_products 37730). Screenshot:
      TanPhatDev/hold-block-inline-error.png.
- [x] T-deduct: trừ TỒN đúng không (gọi THẬT `updateWarehouse()` trên WER#36298 type7 non-direct,
      trong transaction rollback — KHÔNG ghi DB). Trừ kho KHÔNG mutate bảng tồn: `in_stock`/`prepick_qty`
      suy ra bằng `in_stock -= (export_total_qty - export_prepick_qty - export_hold_qty)` và
      `prepick_qty -= export_prepick_qty` (ProductInfo.php:1498-1522, mirror Product/ProductTemplate).
      Fixture tạm: NV 429 (người YC điều chuyển) giữ 5 x SP45028 @cty nguồn 1.
      • NON-DIRECT (đã revert): `can_export_from_prepick=false` → export_prepick_qty=0, export_hold_qty=0,
        export_total_qty=1 → **trừ TỒN=1, trừ GIỮ=0** (giữ 5 còn nguyên dù có giữ) ✓ đúng logic cũ.
      • DIRECT (giữ nguyên): `can_export_from_prepick=true` → export_prepick_qty=1 → **trừ GIỮ=1, trừ TỒN=0** ✓.
      Rollback sạch: fixture biến mất, werd#91963 giữ nguyên (prepick=0,total=1).
      Script: scratchpad/test_trutonotrudung.php.

### Phần E — DỜI validate hủy giữ: YCXH → ĐNXK (user chốt 2026-10-06)
Lý do: ĐNXK (`WarehouseExportRequest` = đề nghị xuất kho) do **kế toán công ty nguồn** lập, họ đi hủy
giữ luôn ở bước đó. Chặn ở YCXH (KD lập) là sai người. Quyết định: **gỡ HẲN ở YCXH, chỉ chặn ở ĐNXK**;
chặn **mọi lần lưu ĐNXK** (nháp status 3 lẫn gửi status 2). Chỉ áp non-direct type 7 (giữ nguyên Phần C logic).

- [x] E1: Tách `validateTransferHoldReleased()` ra service `app/Services/Warehouse/TransferHoldValidator.php`
      `::validate($ycchIds, $sourceCompanyId): array` (static, logic query GIỮ NGUYÊN 100%; câu lỗi cuối đổi
      "...lập yêu cầu xuất điều chuyển" → "...lập đề nghị xuất kho"). Docblock ghi "Nơi đang dùng".
- [x] E2: `ProductExportRequestsController` — GỠ method + 2 khối gọi (store + update). Nhánh `is_export_direct`
      (guard 1 KD) gộp vào `if (type==7 && is_export_direct)`. Gỡ 2 import thừa `ProductTransferRequestProduct`,
      `PrepickDetail` (chỉ còn dùng trong method đã gỡ). Employee/Product/ProductTransferRequest vẫn dùng → giữ.
- [x] E3: `WarehouseExportRequestsController` — thêm `use ...TransferHoldValidator;`. store(): sau `validateWarehouse`
      trước `acquireReserveLock`, parent = `ProductExportRequest::find(product_export_request_id)`; nếu
      `type==7 && !is_export_direct` → validate, còn giữ → `success=false` + `errors.transfer_hold` + message chung.
      update(): y hệt, parent = `$object->product_export_request`. ĐẶT NGOÀI transaction → early return sạch.
- [x] E4: FE `form.blade.php` ĐNXK — thêm block `ng-if="errors.transfer_hold.length"` ng-repeat (đầu card-block).
      create + edit đã set `$scope.errors` sẵn → không sửa JS. **KHÔNG gỡ** span `errors.product_transfer_requests`
      ở form YCXH: vẫn phục vụ rule `required|array|min:1` của YCXH (ctrl :427, :985) — không phải dead code.
- [x] E5: `php -l` sạch cả 3 file PHP (service + 2 controller).

### Checkpoint — 2026-10-06 (dời validate hủy giữ YCXH → ĐNXK)
Vừa hoàn thành: E1–E5. User chốt: gỡ HẲN ở YCXH, chỉ chặn ĐNXK, chặn mọi lần lưu (nháp + gửi).
File sửa: `app/Services/Warehouse/TransferHoldValidator.php` (MỚI);
`app/Http/Controllers/Warehouse/ProductExportRequestsController.php` (gỡ method + 2 khối + 2 import);
`app/Http/Controllers/Warehouse/WarehouseExportRequestsController.php` (use + store + update);
`resources/views/warehouse/warehouse_export_requests/form.blade.php` (block lỗi FE).
Đang làm dở: (không).
Bước tiếp theo: user test môi trường có giữ thật — lập YCXH điều chuyển qua kho khi KD còn giữ (KHÔNG còn bị
chặn ở YCXH) → kế toán công ty nguồn lập ĐNXK từ YCXH đó → PHẢI bị chặn "Cần hủy giữ..."; hủy giữ xong lập lại OK.
Xuất thẳng (is_export_direct): không áp chặn, vẫn guard 1 KD ở YCXH.
Blocked: DB trỏ PROD hrm_erp_gop → chỉ sửa code, CHƯA test submit được. CHƯA commit/push (chờ yêu cầu).


## Checkpoint — 2026-10-03 (hoàn tất implement + test BE local)
Vừa hoàn thành: TOÀN BỘ A1–A3, B1–B3, C1–C3, V1–V3.
File sửa: `app/Model/Warehouse/WarehouseExportRequest.php` (A1);
`app/Http/Controllers/Warehouse/ProductExportRequestsController.php` (imports + helper validateTransferHoldReleased + guard store/update);
`resources/views/warehouse/product_export_requests/formJs.blade.php` (B3);
`resources/views/warehouse/product_export_requests/form.blade.php` (C3).
Đang làm dở: (không).
Bước tiếp theo: user review + test trên môi trường có giữ thật (tạo YCXH điều chuyển qua kho khi KD còn giữ → phải bị chặn; tích xuất thẳng → vẫn xuất theo giữ + chặn 1:1).
Blocked: không submit/test data được (DB trỏ PROD hrm_erp_gop) — chỉ sửa code + SELECT. CHƯA commit/push (chờ yêu cầu).

---

## ĐẢO NGƯỢC đợt revert — về phiên bản 2 (2026-10-07)

User chốt: "cứ revert về phiên bản 2" = quay lại logic feature cũ
(tự trừ giữ + 1 YCXH gồm YCCH cùng 1 KD), hoàn tác trọn đợt revert A–E.

- [x] Kiểm khả thi: `git revert` khô 3 commit (b688b47c30, 6a3f428475,
      c96524b68e) → SẠCH, 0 xung đột. Giữa feature cuối (4ba07a032e 16/09)
      và revert đầu (c96524b68e 03/10) chỉ có merge master + fix HĐ hãng,
      không đụng logic trừ-giữ → revert không va chạm, fix HĐ hãng giữ nguyên.
- [x] Revert gộp 3 commit thành 1: **2db1d389d4** (8 file, +11/-141,
      xoá TransferHoldValidator.php).
- [x] php -l 3 file PHP sạch.
- [x] Xác nhận state = phiên bản 2:
      - WarehouseExportRequest:620 bật can_export_from_prepick cho type 7
        KHÔNG kèm is_export_direct → tự trừ giữ.
      - ProductExportRequestsController:709 guard "cùng 1 người tạo" vô điều
        kiện cho type 7 → 1 YCXH 1 KD.
- [ ] CHƯA push (chờ user yêu cầu). CHƯA test trình duyệt.

### Checkpoint — 2026-10-07 (đảo ngược revert)
Vừa hoàn thành: revert trọn đợt revert A–E về phiên bản 2, commit 2db1d389d4 trên gop_db.
Đang làm dở: để trống.
Bước tiếp theo (chờ user): test trình duyệt luồng YCXH→YCCH→ĐNXK điều chuyển CN; push khi user yêu cầu.
Blocked: để trống.
