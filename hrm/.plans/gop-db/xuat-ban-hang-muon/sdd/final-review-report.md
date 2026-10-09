# Final review report — xuat-ban-hang-muon Phase 2 (BorrowSell / PXBHM-)

Reviewer cuối cùng toàn nhánh. Đã đọc: brief, plan `2026-09-07-...-phase2.md`, 3 gói diff (BE committed 3582 dòng, BE uncommitted objectable, FE worktree), và đối chiếu code ERP gốc (`BorrowSell.php`, `BorrowSellsController.php`, `FirmContractBorrowSellService.php`, `FirmContractExportService.php`).

## Tổng kết theo severity

- **Blocker: 0**
- **High: 0**
- **Medium: 1**
- **Low: 3**

**Verdict tổng: SHIP-with-nits.** Không có finding chặn. Nghiệp vụ hạch toán, quyền, transaction, atomic increment đều đúng và port trung thành ERP. 1 điểm Medium là divergence side-effect rollup (không ảnh hưởng cân bằng bút toán / tồn khả bán), nên xác nhận chủ ý trước khi merge.

---

## Đã verify là ĐÚNG (không phải finding)

Ghi lại để chốt các điểm rủi ro cao nhất trong brief đã được kiểm và đạt:

1. **export_price nhất quán store() ↔ 2 nhánh giá vốn (CONFIRMED).** HRM `BorrowSellService::store()` (be-committed dòng 2012/2028) tính `export_price = Σ(detailQty × unit_coefficient × borrowDetail.export_price) / Σ detailQty` — GIỐNG HỆT ERP `BorrowSellsController::store` dòng 240/252. ERP rẽ nhánh y như HRM: Firm → `FirmContractBorrowSellService::costAccounting` (dòng 203: `export_price × qty`, KHÔNG coef) → Có **157**; WrService → `getDataCreateDept` (dòng 600: `export_price × qty × unit_coefficient`) → Có **1561**. HRM `costAccounting` (dòng 1638) và `costAccountingWrService` (dòng 1742) khớp verbatim. Port trung thành 1-1, đúng Global Constraint 7.

2. **Trait extraction KHÔNG đổi hành vi xuất hàng thường (CONFIRMED — Global Constraint 2).** Trait thêm guard `if ($contractCompanyId !== null && deptCompany(...) !== $contractCompanyId) continue;`. Với normal export, `ProductExportPostingService` luôn truyền `company_id` non-null → điều kiện rút gọn về nguyên bản → bút toán không đổi. Nhánh Firm borrow-sell truyền `$contract->company_id` (lọc theo công ty) khớp ERP `FirmContractExportService::monthlyAndQuarterlyCommissionAccounting`/`riskFundAccounting` (dòng 190-192, 282-284 CÓ lọc `department_root->company_id != firm_contract->company_id`). Nhánh WrService truyền `null` (không lọc) khớp ERP `getDataCreateDept` (không có lọc company). `vatExtraCostAccounting` giữ tên = TNCN. Đúng.

3. **Cân bằng Nợ=Có mọi nhánh (CONFIRMED qua test).** Các test `BorrowSellPostingFirmTest`, `BorrowSellPostingWrServiceTest`, `BorrowSellDeliveryTripAccountingTest`, `ProductExportPostingRegressionTest` đều assert `Σ Nợ == Σ Có`. Từng block bút toán đều dựng cặp Nợ/Có cùng `value`.

4. **BE rethrow ValidationException (CONFIRMED — Global Constraint 5).** `BorrowSellService::store()` throw `ValidationException` tại 5 điểm (dòng 1910, 1918, 2005, 2046) và KHÔNG bọc try/catch chung. Controller `store()` (dòng 1224-1237) chỉ gate 403 rồi gọi service, KHÔNG catch → exception nổi lên handler → 422.

5. **Atomic increment (CONFIRMED — memory lost-update).** `updateWarehouse` dùng `DB::table(...)->increment('borrow_returned_qty'/'returned_by_sell'/'exported_qty', ...)` (dòng 2108, 2121, 2124) thay vì `+= rồi save()`. Đúng bài học sự cố BorrowSell 2026-09-04.

6. **Transaction bao trọn + duyệt cha (CONFIRMED).** Toàn bộ tạo phiếu + updateWarehouse + postDeliveryTripAccounting + postAccounting + set parent `DA_DUYET` nằm trong 1 `DB::transaction` (dòng 1923-2082); posting trả `[ok,err]`, fail → throw RuntimeException → rollback.

7. **FE qty-only + fail-closed (CONFIRMED — Global Constraint 3,4).** `BorrowSellForm.vue::buildPayload` chỉ gửi `{borrow_sell_request_id, products:[{objectable_id, objectable_type, details:[{product_export_request_detail_id, qty}]}]}`, không field tiền. Cờ quyền (`is_can_view`, `is_can_create_borrow_sell`) đọc từ BE, không hardcode `= true`. Import từ `../api` đúng (không nhầm Phase 1).

8. **Bỏ nhánh KM + suy loại HĐ từ contractable_type (CONFIRMED — Global Constraint 6).** `store()` chặn `type !== HANG_THUONG` (dòng 1917); `getDataAccounting` rẽ nhánh theo `contractable_type` (CONTRACT_FIRM/CONTRACT_WR_SERVICE), không đọc cột `type`.

---

## FINDINGS

### [Medium] F1 — updateWarehouse bỏ sót side-effect rollup so với ERP (nested WrService exported_qty + Firm tab warehouse_exported_qty/need_repair)

- **File:** `Modules/Finance/Services/BorrowSell/BorrowSellService.php::updateWarehouse` (be-committed dòng 2093-2137).
- **Đối chiếu ERP:** `App\Model\Warehouse\BorrowSell::updateWarehouse` (dòng 410-509).
- **Mô tả:**
  - **WrService — thiếu cộng cấp 2.** ERP dòng 416-421: sau khi cộng `$p->objectable->exported_qty` (cấp 1 = `wr_service_contract_items`), nếu `contractable_type == WrServiceContract` thì cộng THÊM `$contract_item->objectable->exported_qty += $p->qty` (cấp 2 = morphTo `objectable` của WrServiceContractItem, ví dụ merchandise/product-item). HRM chỉ increment cấp 1 (`wr_service_contract_items.exported_qty`, dòng 2108), KHÔNG cộng cấp 2 lồng.
  - **Firm — thiếu warehouse_exported_qty + need_repair.** ERP vòng lặp tabs (dòng 481-483) cộng `firm_contract_tab_products.exported_qty` + `warehouse_exported_qty` + set `need_repair`. HRM cộng `firm_contract_tab_products.exported_qty` (qua objectable, đúng) nhưng KHÔNG đụng `warehouse_exported_qty` và `need_repair`.
- **Failure scenario:** Sau khi lập phiếu xuất bán từ HĐ dịch vụ, cột `exported_qty` của bản ghi objectable cấp 2 (rollup dòng HĐ dịch vụ) bị under-count; báo cáo/màn hình theo dõi "đã xuất" cấp HĐ dịch vụ hiển thị thiếu. Tương tự HĐ hãng: `warehouse_exported_qty`/`need_repair` trên `firm_contract_tab_products` không phản ánh lần xuất bán (liên quan flow YCLD/lắp đặt — xem memory `erp-ycld-need-repair-sync`).
- **Giới hạn tác động:** KHÔNG ảnh hưởng (a) cân bằng bút toán, (b) guard tồn khả bán — vì `availableSellQty` tính từ `product_export_request_details.base_exported_qty`/`borrow_returned_qty` (dòng 1998-2003), KHÔNG đọc các cột rollup này. Nên không gây over-sell. Chỉ lệch số liệu rollup cấp hợp đồng.
- **Verdict:** **PLAUSIBLE.** Có thể là scope-cut chủ ý (Ruling T7-6 bỏ tabs, T7-7 bỏ need_check_exported), nhưng cấp-2 WrService KHÔNG dính tới tabs/KM nên nhiều khả năng là sót thật. **Đề nghị:** xác nhận với chủ nghiệp vụ xem rollup `exported_qty` cấp HĐ (WrService nested) và `warehouse_exported_qty`/`need_repair` (Firm tab) có được dùng ở màn/loại báo cáo nào không; nếu có → bổ sung increment tương ứng.

### [Low] F2 — StoreBorrowSellRequest::authorize() comment sai lệch (tham chiếu middleware không tồn tại)

- **File:** `Modules/Finance/Http/Requests/BorrowSell/StoreBorrowSellRequest.php` (be-committed ~dòng 1260+), comment `authorize()`.
- **Mô tả:** `authorize()` return `true` với comment nói "gate ở middleware `checkPermission:Kế toán kho` (route)". Thực tế `Routes/api.php` KHÔNG gắn middleware này (có comment giải thích spatie miss do model_type='App\Employee'); gate 403 nằm ở `BorrowSellController::store` qua `BorrowSell::userCanCreate()`.
- **Failure scenario:** Không có lỗi runtime — gate vẫn hoạt động ở controller. Chỉ gây hiểu nhầm khi bảo trì (dev tưởng middleware bảo vệ route).
- **Verdict:** **CONFIRMED.** Cosmetic. Đề nghị sửa comment cho đúng ("gate 403 ở BorrowSellController::store qua userCanCreate()").

### [Low] F3 — Tab Hạch toán (BorrowSellDetailResource) TÍNH LẠI bút toán live thay vì đọc account_details đã post

- **File:** `Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php` — key `accounting`/`accounting_error` gọi `app(BorrowSellPostingService::class)->getDataAccounting($this->resource)` tại read-time.
- **Mô tả:** Khi mở chi tiết phiếu, tab Hạch toán dựng lại bút toán từ HĐ/HTHT hiện tại, KHÔNG đọc từ `account_details` đã ghi lúc store(). Đây là quyết định đã chốt (Ruling T9-accounting-in-detail).
- **Failure scenario:** Nếu cấu hình `support_accounting`/HĐ đổi SAU khi phiếu đã post, tab Hạch toán hiển thị số khác với sổ `account_details` thực tế. Ngoài ra nếu `getDataAccounting` trả lỗi (thiếu HTHT/trưởng phòng) sau này → tab hiển thị `accounting_error` dù phiếu đã post thành công.
- **Verdict:** **CONFIRMED (design choice).** Ghi nhận, không chặn. Nếu cần "sổ đúng như đã hạch toán" thì nên đọc `account_details`; hiện tại chấp nhận theo ruling.

### [Low] F4 — postAccounting/postDeliveryTripAccounting catch \Throwable có thể nuốt ValidationException từ saveAccountDetail

- **File:** `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php::postAccounting` (dòng 1473-1485), `postDeliveryTripAccounting` (dòng ~1794-1845).
- **Mô tả:** Block `catch (\Throwable $e) { return [false, msg]; }` bắt MỌI exception khi ghi sổ. Nếu `AccountDetail::saveAccountDetail` (hoặc downstream) ném `ValidationException`, nó bị chuyển thành `[false, msg]` → `store()` throw `RuntimeException` → client nhận 500 thay vì 422.
- **Failure scenario:** Rất hiếm — saveAccountDetail thường không validate input người dùng. Chỉ xảy ra nếu downstream posting có validate. Không ảnh hưởng cân bằng (vẫn rollback đúng).
- **Verdict:** **PLAUSIBLE (biên hiếm).** Chấp nhận được: đây là ghi sổ nội bộ, không phải validate payload người dùng (payload đã validate ở StoreBorrowSellRequest + service trước khi tới đây). Không cần sửa; nếu muốn nghiêm ngặt thì `catch` loại trừ `ValidationException`.

---

## Ghi chú phạm vi

- KHÔNG báo bug Phase 1 `type_name` mislabel (`BorrowSellRequestDetailResource $typeNames`) — ngoài scope theo Global Constraint 8. (Có tồn tại trong diff nhưng bỏ qua đúng yêu cầu.)
- gop_db: không phát hiện dùng `mysql2`/`DB_CONNECTION_SECOND`; lookup org qua `DB::table`, bảng trùng ưu tiên bản ERP — đúng Global Constraint 9.
- Route: `GET /{id}/print-data` đăng ký trước `GET /{id}`; không xung đột (khác số segment). `POST /` không gắn middleware checkPermission (chủ ý, gate ở controller). Đúng thiết kế quyền đã chốt.

**Kết luận: SHIP-with-nits — merge được sau khi xác nhận F1 (Medium) là chủ ý hay cần bổ sung increment rollup.**
