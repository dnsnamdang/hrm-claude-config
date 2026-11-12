# Phiếu yêu cầu xuất tách / xuất ghép (ERP → HRM) (@junfoke)

## Ngày 11/11/2026 (@junfoke)
- [x] 11/11/2026 — Khảo sát chuẩn bị port 2 màn ERP "Phiếu yêu cầu xuất tách" (YCXT) + "Phiếu yêu cầu xuất ghép" (YCXG): giống nhau ~90% (cùng endpoint, 3 bảng, luồng duyệt, phân quyền, dựa trên công thức hàng `recipe_products`) ⇒ đề xuất dựng 1 khung chung. Luồng: Lưu (Đang tạo) / Lưu & Gửi (Chờ duyệt, kiểm tồn không giữ hàng); kế toán kho (`accounting.ke_toan_kho.manage`) duyệt bằng "Tạo đề nghị xuất kho" (ghép có Xuất thẳng → "Tạo phiếu xuất hàng") hoặc "Không duyệt"; mã trạng thái 2 màn lệch nhau (tách 8–9, ghép 8–10). HRM: chưa có code, menu Tài chính › "Tách - ghép" + hub Bán hàng đang mở ERP, 2 mã quyền xem có trong Catalog (chỉ ERP). DB local: 89 phiếu tách, 855 phiếu ghép.
- Lỗi ERP thấy trong code: không endpoint nào kiểm quyền; menu "YC xuất ghép chờ duyệt" truyền sai tham số `for-approve`; 2 màn lọc chờ duyệt khác nhau (kho vs công ty); quyền mở xem không khớp danh sách; trạng thái treo khi hủy / từ chối đề nghị xuất kho loại tách; bộ lọc trạng thái thiếu; nút In ẩn + code in hỏng; validate lỏng. Nghi lỗi HRM: `ProductExportController.php:471` đọc mã phiếu ghép từ `warehouse_export_requests` thay vì `join_export_requests` (chưa kiểm).
- [x] Chờ user chốt phạm vi → đã chốt 12/11 (mục dưới).

## Ngày 12/11/2026 (@junfoke) — user chốt phạm vi
- Rà chuỗi phía sau bên HRM: ĐNXK HRM chỉ tạo từ YCXH; ĐNXK / PXK / Phiếu xuất hàng HRM **vẫn xử lý được phiếu loại 9/10 do ERP tạo** nhưng **không cập nhật trạng thái** `split/join_export_requests` (ERP có ~12 chỗ), và Phiếu xuất hàng **không tự sinh phiếu nhập tách/ghép** (ERP `ProductExport.php:1527,1597`) ⇒ chuỗi đứt, lỗi có sẵn. Phiếu nhập hàng loại 8/10 HRM đã chặn. Xác nhận bug `ProductExportController.php:471,482` đọc nhầm bảng `warehouse_export_requests`.
- Chốt:
  - **Port ĐỦ cả chuỗi**: 2 màn + ĐNXK tạo từ tách/ghép + đồng bộ trạng thái ở ĐNXK/PXK/Phiếu xuất hàng/Phiếu nhập + tự sinh phiếu nhập tách/ghép + xuất thẳng (ghép).
  - Quyền **tạo giữ như ERP** (ai đăng nhập cũng tạo); xem theo 2 mã có sẵn; duyệt/không duyệt = `accounting.ke_toan_kho.manage`.
  - **Sửa lỗi ERP** (theo chuẩn HRM trong bản port).
  - **Sửa kèm** bug Phiếu xuất hàng đọc nhầm bảng.
  - **Làm bản in** (ERP đang ẩn/hỏng) theo khuôn bản in HRM.
- [x] Viết design + spec (chia phase). User bảo "làm dần đi" → làm luôn Phase 1.

## Phase 1 — 2 màn tách / ghép (12/11/2026)
Nhánh `feat/yc-xuat-tach-ghep` (api + client), tách từ `origin/gop_db`, không track, CHƯA commit. Từ 12/11 chiều chuyển về
thư mục chính `hrm-api` / `hrm-client` (đã gỡ worktree `.worktrees/yc-xuat-tach-ghep`).
### BE
- [x] Worktree + nhánh (2 repo)
- [x] Entity 6 bảng (`Entities/SplitJoinExport/`) + trait chung `SplitJoinExportRequestCommon` (quyền, phạm vi, lọc, sort)
- [x] `SplitJoinExportRequestService`: đọc / form-options / công thức / tồn (+ tồn nhập thẳng) / lưu / xóa / không duyệt / Excel / in
- [x] Lịch sử (`GATED_TABLES` + endpoint `/{id}/histories`) + thông báo (Kế toán kho cùng công ty / người tạo)
- [x] FormRequest + controller cha/2 con + route (`finance/split-export-requests`, `finance/join-export-requests`); Catalog thêm `hrm` 2 mã xem
- [x] Bản in `prints/split-join-export-request.blade.php`
- [x] Verify bằng script (rollback): lưu nháp / sửa + gửi / sửa phiếu đã gửi bị chặn / không duyệt / lịch sử / in / xóa / vượt tồn / kho lạ / hàng không công thức — cả tách lẫn ghép; tài khoản thường không thấy, không duyệt được
### FE
- [x] Khung chung `components/finance/split-join-export/` (kinds, List, Form, RejectModal, export-excel) + 8 trang
- [x] Menu finance.js + sale-hub.js (`erpPath` → `link ?type=all`)
- [x] Verify trình duyệt (3100/8100): danh sách, chi tiết, In, tạo phiếu ghép (thêm hàng, tồn đỏ, BE trả lỗi đúng dòng)
- [ ] Thử tay: lưu thật 1 phiếu → sửa → gửi → Từ chối → Xóa trên giao diện; Xuất Excel; Xuất thẳng
- [ ] Commit (chờ user)
### Deploy
- `permission:catalog-sync` (2 mã xem thêm `hrm`). Không migration.

## Phase 2 — ĐNXK tạo từ phiếu tách / ghép (12/11/2026)
Cùng nhánh `feat/yc-xuat-tach-ghep`, CHƯA commit. Spec mục 7.
### BE
- [x] `Finance/Services/SplitJoinWarehouseExportService` (nguồn tách/ghép của ĐNXK): cửa vào (Chờ duyệt + Kế toán kho + cùng công ty, ghép xuất thẳng chặn), dòng hàng từ phiếu nguồn (tách nguyên dòng, ghép gộp NVL), tồn `in_stock − in_promotion` theo kho kế toán công ty, kiểm tồn gộp đơn vị gốc, đồng bộ trạng thái + lịch sử phiếu nguồn
- [x] `Assign/WarehouseExportRequestService`: `createFromSplitJoin`, nhánh loại 9/10 trong `updateDraft` + `cancel` (vá E9: hủy ĐNXK → phiếu nguồn 6 Đã hủy cả tách lẫn ghép); gửi thủ kho ghi `export_total_qty` (giữ tồn)
- [x] API `finance/{split|join}-export-requests/{id}/warehouse-export-data` + `POST /{id}/warehouse-export-requests` (checkPermission Kế toán kho); `stock-of-products` nhận `split/join_export_request_id`; `editData` kho theo công ty + id nguồn
- [x] Entity ĐNXK thêm quan hệ `splitExportRequest` / `joinExportRequest`; Resource + Excel ĐNXK trả phiếu nguồn hợp nhất `source_code/source_url/source_label`, Người yêu cầu = người tạo phiếu tách/ghép
- [x] Thông báo người tạo phiếu nguồn: "Đã duyệt" (lập ĐNXK) / "Đã hủy" (hủy ĐNXK) — gửi sau commit
- [x] `approve_link` → màn HRM (`link`); ghép Xuất thẳng vẫn mở ERP tới Phase 4
- [x] Tồn phiếu TÁCH (Phase 1) đổi sang `in_stock − in_promotion` cho khớp số ĐNXK kiểm
- [x] Verify script rollback cả tách lẫn ghép: chặn phiếu nháp / lập lần 2 / kho lạ / vượt tồn; nháp→nguồn 1, gửi→7 + giữ tồn, hủy→6; lịch sử; editData/show; approve_link
### FE
- [x] `warehouse-export-requests/create.vue` nhận `?split_export_request_id=` / `?join_export_request_id=`: dòng khoá (không chọn bớt, không sửa SL), kho đổi được, nhãn Mã YCXT/YCXG, Quay lại → phiếu nguồn
- [x] `_id/edit.vue` nhánh loại 9/10; `_id/index.vue` + `index.vue` link phiếu nguồn theo `source_url`
- [x] Form tách/ghép: nút Tạo đề nghị xuất kho → `$router.push` màn HRM
- [x] Verify trình duyệt YCXT-00093: Tạo ĐNXK → Lưu nháp → chi tiết → Sửa → Gửi thủ kho → danh sách link nguồn; phiếu nguồn "Đã đề nghị" + thông báo. Dữ liệu thử đã hoàn nguyên.
- [ ] Commit (chờ user)
### Còn để Phase 3
- Thủ kho lập PXK từ ĐNXK (duyệt ĐNXK) → phiếu nguồn 4 Đang xuất kho (`WarehouseExportService::approveExportRequest` đang bỏ nhánh tách/ghép).

- [x] Commit Phase 1+2: api `cf58fbf8b`, client `80ae6a8dc` (12/11, chưa push). Code chuyển từ worktree về thư mục chính.

## Phase 3 — Phiếu xuất kho (PXK) đồng bộ phiếu tách / ghép (12/11/2026)
Chỉ BE (màn PXK không hiển thị phiếu nguồn). Spec mục 8.
- [x] `SplitJoinWarehouseExportService::syncFromWarehouseExport()`: lập PXK → nguồn 4 Đang xuất kho (+ báo người tạo), gửi PXK → 5 Đã xuất kho, hủy PXK nháp → 6 Đã hủy; lịch sử; thông báo `DB::afterCommit`
- [x] `WarehouseExportService`: gọi ở `createFromExportRequest` / `send` / `cancel`; ghép (ĐNXK loại 9) phải xuất ĐÚNG SL đề nghị (`assertJoinFullQty`, cả lô tạm lẫn lô chính thức)
- [x] Verify script rollback (tách 5599 / ghép 4465, kho 2): lập→4, gửi→5 (ĐNXK 6), hủy→6 (ĐNXK 5), ghép xuất thiếu bị chặn; lịch sử nguồn đủ dòng
- [x] Commit Phase 3
### Còn để Phase 4
- Lập Phiếu xuất hàng từ PXK (`WarehouseExport::approve()` ERP): tách → 8 Chờ nhập hàng, ghép → 5; tự sinh phiếu nhập tách/ghép; xuất thẳng ghép; vá E10.

- [x] Commit Phase 3: api `97a53bd0f`

## Phase 4 — Phiếu xuất hàng (khảo sát 12/11/2026, chờ user chốt cách chia)
ERP `ProductExport::updateWarehouse()` :1478-1640 + `WarehouseExport::approve()` :1252-1310. HRM `ProductExportService::createFromWarehouseExport`
chưa có nhánh loại 9/10 (PXH loại 9/10 lập ở HRM hiện không sinh gì, phiếu nguồn kẹt "Đã xuất kho"). Đề xuất chia:
- 4a — PXH từ PXK tách/ghép: ghi `split_/join_export_request_id` lên PXH; tách → cập nhật `exported_qty` dòng + NVL, tự sinh
  YC nhập kho NHAP_TACH (`warehouse_import_requests`, gửi luôn), nguồn → 8 Chờ nhập hàng; ghép → tự sinh Phiếu nhập kho NHAP_GHEP
  (`warehouse_imports`, lô ở vị trí `join_split_position` của kho, cộng tồn), nguồn → 9 Chờ nhập hàng; vá E10 (`ProductExportController:471,482`).
- 4b — Ghép Xuất thẳng: lập PXH thẳng từ phiếu ghép + tự sinh Phiếu nhập hàng kế toán NHAP_GHEP nhập thẳng + bút toán
  (`AccountDetail`), nguồn → 10 Hoàn thành. Nặng nhất (đụng kế toán).

User chốt 12/11: làm 4a trước, commit, rồi 4b.

### Phase 4a — PXH từ PXK tách/ghép (12/11/2026)
- [x] `ProductExportService::createFromWarehouseExport`: ghi `split_/join_export_request_id` lên PXH; lập PXH → nguồn tách 8 Chờ nhập hàng / ghép 5 (`syncFromWarehouseExport('pxh_created')` + báo người tạo "Đã xuất kho"); hoàn tất → `SplitJoinImportService`
- [x] `Finance/Services/SplitJoinImportService` (mới): tách → `exported_qty` dòng + NVL, tự sinh ĐNNK "Nhập tách" (`WarehouseImportRequestService::createFromSplitExport`, gửi thủ kho); ghép → tự sinh PNK "Nhập ghép" ở vị trí tách/ghép của kho + cộng tồn (`PhysicalStockWriter::importLot`), nguồn → 9 Chờ nhập hàng (1 lần / phiếu ghép); kho chưa khai vị trí tách/ghép → 422
- [x] `ProductExportPostingService`: bút toán giá vốn loại 9/10 (Nợ account_debt / Có từng account_has, work) — trước đây HRM chặn "Loại phiếu xuất 9 không hỗ trợ hạch toán!"; vá lỗi ERP nhánh tách dùng nhầm `$total` cũ; 9/10 không gắn contractable
- [x] E10: `ProductExportController` đọc phiếu ghép từ `join_export_requests` (+ link màn HRM), người yêu cầu loại 9/10 = người tạo phiếu tách/ghép
- [x] Verify script rollback trọn chuỗi nguồn → ĐNXK → PXK lập+gửi → PXH hoàn tất: tách 5599 (bút toán cân, exported_qty, ĐNNK PDNNK loại 10 đúng 2 NVL), ghép 4465 (PNK loại 8, lô ở vị trí 4639, tồn +1, nguồn 9, bút toán cân)
- [x] Commit 4a
### Còn lại
- 4b: ghép Xuất thẳng (PXH thẳng từ phiếu ghép + phiếu nhập kế toán NHAP_GHEP nhập thẳng + bút toán, nguồn → 10).
- Phase 5: duyệt nhập (ĐNNK tách → PNK; PNK ghép duyệt) hoàn thành phiếu nguồn (ERP `ProductImportsController.php:816,822,1445`); kiểm màn ĐNNK/PNK HRM với loại 8/10 không có YCNH nguồn.

- [x] Commit 4a: api `5911b1959`. User đồng ý làm Phase 5 trước 4b (4b cần phiếu nhập kế toán Nhập ghép = phần Phase 5 mở).

## Phase 5 — Phiếu nhập hàng Nhập ghép (8) / Nhập tách (10) (12/11/2026)
### BE
- [x] `ProductImportService`: `resolveSourcePir` trả null cho PNK 8/10 (không YCNH; KHÔNG model rỗng vì markParentUsed save()); popup chọn PNK nhận 8/10; `buildDetailsFromSource` cho dòng YCNH rỗng + giá 8/10; `getWarehouseImportSource` null-safe + điền sẵn TK Có / Vụ việc từ PXH nguồn (ERP create.blade:118-121); 8/10 vào `$editableTypes`, `buildDetailsByType`, `resolveAccountingService`; `fillEditableHeader` lưu TK Có / Vụ việc; `handleCompleted` → nguồn Hoàn thành
- [x] `SplitJoinProductImportAccountingService` (mới): Nợ TK từng kho kế toán = supplier_price × import_qty / Có account_has (work_id)
- [x] `SplitJoinImportService`: `importPrices` (ghép = BẢO TOÀN giá trị NVL đã xuất — ERP không nhân SL công thức; tách = giá nhập gần nhất như ERP), `accountPrefill`, `onProductImportCompleted` (ghép → 10, tách → 9 + lịch sử + báo người tạo; ERP sửa→duyệt quên loại tách)
- [x] FormRequest store/update: 8/10 không cần `product_import_request_detail_id`; hoàn tất bắt buộc TK Có, Vụ việc, TK Nợ từng kho
- [x] Verify script rollback trọn chuỗi tới PNH (ghép: giá trị nhập 3,284,445 = giá trị xuất; tách: ĐNNK → PNK → PNH, nguồn 9); thiếu TK Có bị chặn; nháp → sửa → hoàn tất; thủ kho mở được form lập PNK từ ĐNNK tách (createData)
### FE
- [x] `importTypeConfig` thêm 8 (giá chỉ đọc) / 10 (giá sửa được); `ProductImportForm` ô TK Có + Vụ việc (header) + TK Nợ dưới ô kho kế toán (loại 8/10), nạp danh mục qua `arrange-form-options`, lỗi BE về đúng ô, đưa vào unsaved snapshot
- [ ] Xem trên trình duyệt — CHƯA làm: profile Playwright `playwright-a` đang bị phiên khác giữ; DB local không có PNK 8/10 chờ duyệt (định giả lập API nguồn bằng route)
- [x] Commit Phase 5
- [x] 12/11/2026 — User chốt "giữ logic ERP nhiều nhất, chỉ khác khi ERP sai rành rành": giá nhập phiếu tách giữ như ERP (giá nhập gần nhất, cho sửa); bỏ 2 chỗ khác ERP không phải lỗi — thông báo khi phiếu tách/ghép sang Hoàn thành, và bắt buộc ô Vụ việc trên PNH 8/10 (TK Có / TK Nợ vẫn bắt buộc). Danh sách chỗ còn khác ERP (đều là lỗi ERP) ghi ở mục 11 spec. Commit api `63fa9ced0`, client `df66361e8` (chưa push).

### Checkpoint — 12/11/2026 16:40
Vừa hoàn thành: Phase 5 (BE + FE, verify script; chưa xem trình duyệt form PNH 8/10).
Đang làm dở: —
Bước tiếp theo: xem form PNH 8/10 trên trình duyệt khi rảnh Playwright → 4b (ghép Xuất thẳng: màn PXH thẳng từ phiếu ghép + tự sinh PNH Nhập ghép nhập thẳng, dùng lại SplitJoinProductImportAccountingService).
Blocked:
