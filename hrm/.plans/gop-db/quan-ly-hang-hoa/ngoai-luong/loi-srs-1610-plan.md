# Plan đợt "lỗi SRS 16/10" — N146 · N160 · N162–N191 · N195–N202 (trừ mục đã đóng) — 16/10/2026

> Nguồn: `../viec-con-lai.md` mục A + "Chốt nghiệp vụ 16/10/2026 (tối)"; khảo sát chỉ đọc 16/10 (3 nhóm, file:line bên dưới).
> ⏳ CHƯA được "làm". Không mục nào cần migration / seeder.
> Đã đóng, không làm: N175 · N193 · N194 · N199. N192 (chép giá HP trên VPS test) là việc DB — hỏi riêng, ngoài đợt.

## Nhánh
| Repo | Worktree | Nhánh con | Từ |
|---|---|---|---|
| hrm-api | `wt-chuyen-doi-hang-hoa/hrm-api` | `feat/cdhh-loi-srs-1610` | `feat/chuyen-doi-hang-hoa` (@ `c85a59031`, đã có develop) |
| hrm-client | `wt-chuyen-doi-hang-hoa/hrm-client` | `feat/cdhh-loi-srs-1610` | `feat/chuyen-doi-hang-hoa` |
| ERP | `wt-erp-2d1` | `feat/2d1-loi-srs-1610` (chỉ N160) | `feat/2d1-erp-khong-loi` |

Merge LOCAL về nhánh chung; push khi user cho phép; ⛔ không vào gop_db.

## Lượt 1 — Hàng hoá + thành phần chung
| # | Sửa | Chỗ | Repo |
|---|---|---|---|
| N169(c) | Hàng đang Chờ tính giá bán / Đang tính giá ở **BẤT KỲ công ty nào** (Q1) — thông báo nêu tên công ty đó: BE so `manufacture_id, brand_id, model_id, barcode_id, origin_id` + tập ĐVT (unit_id + hệ số) với DB, khác ⇒ 422 "Hàng đang tính giá, huỷ yêu cầu trước khi đổi"; chặn cả `updateCommon` (hàng tạm). FE computed `pricingLocked` ⇒ disabled các ô | `ProductWriteService.php:128-140, 364-377`; `ProductCompany::PRICING_FLOW_STATUSES`; `ProductFormGeneral.vue:23-28,127,132,137,143-148`, `ProductFormUnitsTable.vue` | api + client |
| N169(b) | Reader trả `has_price` (giữ `retail_price` float); picker + ô ĐVT dòng chứng từ hiện "Chưa có giá" | `ProductPriceReader.php:147`, `ProductPickerService.php:177,237`; `ProductPickerPanel.vue:205-206` | api + client |
| N168 | Bảo hành `step=1` chặn số lẻ · Hệ số thuế BVMT `min=1` · nhãn Loại tài liệu `required` | `ProductFormAdmin.vue:44`, `ProductFormPurchase.vue:77`, `ProductFormTechDocs.vue:14` | client |
| N167 | Tên công ty fallback `store.companies` / `employee_company`; sửa chuỗi "công ty công ty…" | `utils/productLifecycle.js:22-26`; `product-price-approvals/index.vue:470` | client |
| N166 | ⚠️ Chưa xác nhận trong code (nghi `fill()` của Playwright không phát keydown). Bước 1 tái hiện bằng gõ phím thật; chỉ sửa nếu tái hiện được (bắt thêm sự kiện `input` trong mixin — mixin dùng toàn app ⇒ hỏi lại trước khi sửa) | `unsavedChangesMixin.js:48-65`, `ProductForm.vue:306` | client |
| N181 | Đưa dải "chưa xếp catalog" ra ngoài DataTable (không sửa `V2BaseDataTable`, 233 nơi dùng) | `ProductListPage.vue:182,236` | client |
| N146 | Dòng mới YCXH gắn `_price_pending`; `loadUnits` xong (kể cả cache) đặt lại giá theo ĐVT hiện tại | `ProductExportRequestForm.vue:2535-2556`, `ManualLinesTable.vue:240-262` | client |
| N163 | Tách `select2Language` ra util, thêm vào `V2BaseSelectInModal` (175 nơi dùng — chỉ đổi chữ) | `V2BaseSelectInModal.vue:161-167`, `V2BaseSelect.vue:69,102-113` | client |
| N162 | Helper opt-in: `QueryException` ⇒ câu chung + log; thay 15 `catch` của controller YCXH | `ProductExportRequestController.php` (vd :1196, :1595) | api |
| N160 | (Q2) Bỏ bypass `hasRole('Super Admin')` ở `canView` (+ grep các can* khác cùng file); runbook: gán quyền "Xem … theo tổng công ty" cho vai trò cần xem trước deploy | ERP `InlandOrderRequestNew.php:584` | ERP |

## Lượt 2 — Cập nhật giá bán + Duyệt giá bán
| # | Sửa | Chỗ | Repo |
|---|---|---|---|
| N169(a) | `query()` join pcc theo `pa.company_id` ⇒ `is_locked`; `approve()` (lẻ + hàng loạt) gặp hàng `pcc.status=4` ⇒ 422 kèm mã hàng, không duyệt phần nào; FE nhãn "Hàng đang khoá" + tắt nút Duyệt | `ProductPriceApprovalService.php:138-146,256-277,333-380`; `ProductPriceApprovalTable.vue` | api + client |
| N172 | `applyReject`: `*_wait_approve = NULL` (upp, pep, pcu), giữ cờ 2; xoá pep cờ 1 có `price=0 AND coefficient=0` (dòng mới chưa duyệt); `pick` chỉ đọc wait khi cờ = 1 (dữ liệu cờ 2 cũ tự đúng, không migration); dòng "Đề xuất X bị từ chối: <lý do>" đọc từ log `rejected` mới nhất | `ProductPriceApprovalService.php:550-612`; `ProductPriceListService.php:343,362-396`; `ProductPriceTable.vue:49-50`; kiểm `CompanyPriceBackfill` | api + client |
| N173 | API trả `meta.ecom_coefficient` theo công ty; FE bỏ hằng 1,3 | `ProductPriceController.php:44`, `ProductPriceWriter.php:42-50`; `product-prices/index.vue:167` | api + client |
| N170 | `setItems`/`replaceItem` chạy `Calc.ecom` sau `unitFromApi` (dùng hệ số N173) | `product-prices/index.vue:353-366` | client |
| N171 | Sửa tại page: sau `scrollToFirstError` chỉnh `scrollLeft` vùng cuộn bảng, chừa 338px cột dính (không sửa util chung) | `product-prices/index.vue:553-562`, `ProductPriceTable.vue:336-337` | client |
| N174 | `base-confirm-modal` thêm `inputMaxLength`/`inputMaxMessage` opt-in (2000); `handleError` toast `errors.approve_comment` | `base-confirm-modal.vue:144-152`; `product-price-approvals/index.vue:516-583` | client |
| N176 | Dòng giá hiệu lực (`kind==='exp'`) hệ số → giá tròn đồng như màn Cập nhật; dòng hiện hành giữ | `ProductPriceApprovalTable.vue:343-357` | client |
| N177 | (Q3) Route của quyền "Duyệt giá bán hàng hoá": `$hideCost = !canSeeCost()` ⇒ popup Lịch sử ẩn giá vốn khi thiếu "Xem giá vốn hàng hoá" (kể cả có "Cập nhật giá bán hàng hoá"); màn Cập nhật giá bán không đổi | `ProductPriceApprovalController.php:106` | api |
| N178 | Toast Không duyệt hàng loạt thêm "N yêu cầu đã được người khác xử lý" | `product-price-approvals/index.vue:555` | client |
| N179 | Cột Hệ số 72 → ~110px ở cả 2 màn (cập nhật tổng bề rộng, `table-layout: fixed`) | `ProductPriceApprovalTable.vue:223`, `ProductPriceTable.vue:341` | client |

## Lượt 3 — YCHG · YCTG · PTG
| # | Sửa | Chỗ | Repo |
|---|---|---|---|
| N186 | BE `update()` sau `canEdit`: `!send` + status 5 ⇒ 422 "Yêu cầu Không duyệt chỉ được sửa rồi gửi lại"; FE ẩn Lưu nháp, nút gửi "Gửi lại" | `PriceCalculateRequestWriter.php:89,93,175`; `PriceCalculateRequestForm.vue:156-163` | api + client |
| N200 | Lý do sửa giá theo từng dòng (Q4): `$l->note ? code.': '.note : 'Phiếu tính giá '.code`, đưa `$reason` vào vòng lặp | `PriceCalculateWriter.php:259,272-287` | api |
| N190 · N198 | Chế độ chỉ xem + bản in dùng số đã lưu (`value/value_exchange`, `cost_price`…), dòng sửa được vẫn tính lại. N198 đụng bản in PTG — rủi ro trung bình | `priceInputRowsMixin.js:23-28`; `PriceCalculateService.php:304-306,353,376-378`; `PriceCalculateForm.vue:331,344-345,409,418` | api + client |
| N196 | `sellFromApi`: TMĐT không nạp `expected_prices` (không sửa `blockRows` dùng chung) | `PriceCalculateForm.vue:376` | client |
| N195 | `MSG_NO_VIEW` / `MSG_GROUP_CLOSED` riêng PTG; `loadOptions` thêm `X-Silent-Errors` | `PriceCalculateAccess.php:56-59`, `PriceCalculateWriter.php:435`, `PriceCalculateService.php:235`; `price-calculates/index.vue:247` | api + client |
| N191 | YCTG `loadOptions` thêm `X-Silent-Errors`; ô lọc qua `scopeVisible` | `price-calculate-requests/index.vue:261-263`; `PriceCalculateRequestService.php:135` | api + client |
| N185 | Ô lọc Người tạo (+ người duyệt) YCHG qua `scopeVisible` | `PriceAskingRequestService.php:232,256` | api |
| N188 | Hiện lỗi khoá `rows` (V2BaseError trên bảng) | `PriceCalculateRequestForm.vue:438-442` | client |
| N189 | Câu FE đổi thành "Không được lớn hơn 999,999,999,999." | `PriceCalculateRequestForm.vue:390`, `priceInputRowsMixin.js:88`, `PriceCalculateForm.vue:460,483` | client |
| N182 | Form Sửa YCHG Không duyệt hiện "Ghi chú PTKD" (theo mẫu YCTG) | `PriceAskingRequestForm.vue:238-241` | client |
| N180 | Cột Hành động `cellClass: 'text-wrap'` (hoặc icon + title) | `price-asking-requests/index.vue:131,249` | client |
| N197 | Popup Chọn YCTG `size="xl"` | `RequestPickerModal.vue:5` | client |
| N202 | `scrollToFirstError` không focus ô `.mx-datepicker` | `utils/scrollToFirstError.js:67-70` | client |
| N183 | (Q5) Cột + ô lọc "XNK tiếp nhận" theo XNK lưu trên nhóm; khác phân công hiện hành ⇒ dòng phụ "Phân công hiện tại: …" | `PriceAskingRequestService.php:92-99,258`, `PriceAskingAccess.php:104-111`; `price-asking-requests/index.vue` | api + client |
| N184 | (Q6) Đổi nhãn cột + ô lọc thành "PTKD xử lý" | `price-asking-requests/index.vue:230,247` | client |
| N187 | (Q7) Nút "Không duyệt"; lịch sử giữ "KTMH không duyệt"; thông báo từ chối "[YCTG] Không duyệt"; thông báo gửi "Chờ tính giá"; sửa test `PriceCalculateRequestApiTest.php:237` | `PriceCalculateRequestNotifier.php:24,32`; `PriceCalculateRequestForm.vue:181,466-471` | api + client |
| N201 | (Q8) Xoá phiếu người khác ⇒ 403 "Bạn không có quyền xoá phiếu này" (kiểm chủ phiếu trước trạng thái); thêm nút "Xem" cột Hành động | `PriceCalculateWriter.php:182-189`; `price-calculates/index.vue:206-218` | api + client |

## Lượt 4 — e2e / công cụ (không đụng code app)
- N164: chạy lại provision role "E2E Assign Admin" (hoặc bước cấp bổ sung 9 quyền) — **ghi DB giacty, hỏi riêng**.
- N165: sửa 2 spec giả định dữ liệu quyền (`product-price-approvals-ui` A2, `product-prices-ui` P7).
- N155: spec e2e màn Gói bảo dưỡng tự tạo role tạm.

## Kiểm
- PHPUnit: MasterData + Assign + `PriceReaderWhitelistTest` sau mỗi lượt; ca mới cho N169(a), N169(c), N172, N186, N177, N162, N185, N191, N198. ERP PHPUnit cho N160.
- Playwright MCP (worktree 3031/8031) mỗi màn có sửa giao diện: đo DOM trước/sau (N171 toạ độ ô vs cột dính, N179/N180/N197 bề rộng, N181 thanh hàng loạt hiện, N170 TMĐT lúc nạp, N172 dòng bị từ chối). Tái hiện trước khi sửa.
- Cập nhật spec e2e các màn đụng tới; KHÔNG tự chạy e2e (chỉ khi user yêu cầu).
- Role tạm (vd quyền "Duyệt giá bán hàng hoá", "Xem giá vốn hàng hoá") cấp để test ⇒ gỡ + xoá cache khi xong; đếm mốc roles/rhp/ehr.

## Câu hỏi — ĐÃ CHỐT 16/10/2026
Q1 N169(c) bất kỳ công ty · Q2 N160 bỏ bypass · Q3 N177 popup theo "Xem giá vốn hàng hoá" · Q4 N200 ghi chú dòng hàng · Q5 N183 XNK lưu trên nhóm · Q6 N184 nhãn "PTKD xử lý" · Q7 N187 "Không duyệt" + "Chờ tính giá" · Q8 N201 sửa code theo tài liệu.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | như bảng Nhánh |
| DB | giacty chỉ đọc + role tạm để test (gỡ khi xong). Không migration / seeder |
| e2e | sửa spec, không tự chạy |

### Kết quả Lượt 1 — 16/10/2026
Commit trên nhánh con, CHƯA merge về nhánh chung, chưa push. Không migration / seeder / cache:clear.

| # | Trạng thái | Commit | Ghi chú |
|---|---|---|---|
| N169(c) | ✅ | api `28dd1da14` · client `b5a358f60` | BE `ProductWriteService::assertIdentityKeptWhilePricing` (trong transaction sau `lockProduct`, chạy cho cả `update` lẫn `updateCommon`): pcc bất kỳ công ty ∈ {2,5} + đổi Hãng SX/Thương hiệu/Model/Code đặt hàng/Xuất xứ (0/''/null coi như nhau) hoặc có ĐVT mới (dòng không id) ⇒ 422 theo từng ô "Hàng hoá đang tính giá tại <tên công ty>, huỷ yêu cầu tính giá trước khi đổi <ô>.". `ProductFormResource` trả `pricing_lock_message`; FE dải xám (khuôn `product-scope-notice`) + disabled 5 select, ẩn nút "+" model và "Thêm đơn vị" |
| N169(b) | ✅ | api `1a3abe62b`, `5d3297cdd` · client `bd5db99bf`, `f20ac7f67` | `has_price` ở `ProductPriceReader::unitOptions`, picker (dòng: null khi không có loại giá; ĐVT), `ProductExportRequestPickerService::productUnits`. FE: popup ô Giá bán "Chưa có giá" (xám #6b7280, nghiêng); ô ĐVT dòng YCXH "Cái (Chưa có giá)". ⚠️ Các màn chứng từ khác tự dựng option ĐVT (báo giá `quotations/_id/edit.vue`, BOM, mượn hàng, huỷ giữ hàng…) CHƯA ghi chú — không có helper chung, cần chốt có làm tiếp không |
| N168 | ✅ | client `c92273c04` | Trước (HEAD): `step="any"`, `min="0"`, nhãn không `*`. Sau (đo DOM): Bảo hành step=1 min=0; BVMT min=1; "Loại tài liệu" có `*` màu rgb(220,38,38) |
| N167 | ✅ | client `ddd42a3e6` | Tái hiện: tài khoản e2e `company_roles` = 0 phần tử ⇒ `companyName` = "công ty đang làm việc". Sau: "· 28,371 hàng hoá đang kinh doanh tại CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT". Bỏ chữ "công ty" thừa ở popup Duyệt |
| N166 | ✖ Không phải lỗi app | — | Gõ phím thật (keyboard.type) ở form Tạo mới + form Sửa ⇒ có popup "Thông tin chưa lưu"; `fill()` ⇒ không popup (thoát thẳng về /entering). Không sửa mixin. Thêm ca e2e E13b |
| N181 | ✅ | client `816fdbb44` | Tái hiện: dải hiện + tick 1 dòng ⇒ `.product-bulk-bar` không có. Sau: dải ngoài `section.tp-card` (y=184, h=39), tick 1 dòng ⇒ thanh "Đã chọn 1 hàng hoá" hiện (y=294), không chồng. Không sửa V2BaseDataTable |
| N146 | ✅ | client `f20ac7f67` | Tái hiện (màn Tạo YCXH, mô phỏng popup trả giá công ty khác 999 qua `onProductsApply`): ô Đơn giá giữ "999". Sau: "3,200,000" = giá ĐVT công ty phiếu; cờ `_price_pending` gỡ sau khi đặt giá (kể cả ĐVT đã có trong bộ nhớ); payload/snapshot chưa lưu không đổi |
| N163 | ✅ | client `a2ed94eec` | `utils/select2Language.js`; V2BaseSelect đọc từ util, V2BaseSelectInModal thêm `language` (extraSettings vẫn đè được). Tái hiện popup Model: "No results found" ⇒ sau: "Không có dữ liệu"; V2BaseSelect (form hàng hoá) vẫn "Không có dữ liệu" |
| N162 | ✅ | api `f9ecef715` | Trait opt-in `App\Http\Controllers\Api\Traits\SafeErrorMessage::safeErrorMessage()` — QueryException ⇒ "Có lỗi hệ thống khi xử lý dữ liệu, vui lòng thử lại hoặc liên hệ quản trị viên." + log; exception khác giữ câu. Áp 17 khối catch (15 × 400 + 2 × 422) của `ProductExportRequestController` |
| N160 | ✅ | ERP `194c2077b0` | Bỏ `hasRole('Super Admin')` ở `canView`; các `can*` khác cùng file không có bypass. ⚠️ Runbook deploy: gán quyền "Xem phiếu yêu cầu đặt hàng trong nước theo tổng công ty" cho vai trò cần xem hết. Ngoài phạm vi (chưa sửa, cùng kiểu bypass): `InlandOrderSummaryNew.php:893,941`, `InlandOrderNotificationNew.php:299`, `InlandPurchaseInvoice.php:631,656,707`, `InlandBuyContractNewController.php:253`, `InlandOrderNotificationNewController.php:172` |

**Test**
- hrm-api `Modules/MasterData/Tests`: `OK (556 tests, 5390 assertions)` (lượt đầu đỏ 1 ca `ProductPickerSearchTest` do khuôn khoá dòng chưa có `has_price` ⇒ cập nhật ca, `5d3297cdd`)
- hrm-api `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- `PriceReaderWhitelistTest`: `OK (2 tests, 45 assertions)`
- Ca mới: `ProductPricingIdentityLockTest` (4), `ProductPickerItemsTest::n169b_*` (1), `ProductExportRequestSafeErrorTest` (2); ERP `N160InlandOrderRequestNewSuperAdminTest` (4)
- ERP toàn bộ: `OK, but incomplete, skipped, or risky tests! Tests: 207, Assertions: 4395, Skipped: 4.` (lượt đầu đỏ `test_n147…` vì comment mới chứa chữ "theo tổng công ty" trong thân canView ⇒ đổi chữ comment, amend)

**e2e (sửa spec, KHÔNG chạy)**: `products-read-ui` (N181) · `products-form-ui` E13b (N166), E14/E14b (N169c), E15 (N168) · `assign/product-picker-ui` (N169b, chặn route search, không ghi DB) · `product-prices-ui` (N167) · `product-catalog-ui` (N163). `--list` parse được. Chưa có spec YCXH ⇒ N146 chỉ kiểm bằng Playwright MCP.

**Playwright N169(c)** (chặn `/products/50066/edit` gắn `pricing_lock_message`, không ghi DB): trước — 5 select enabled, "Thêm đơn vị" 1, nút "+" model 1, không dải; sau — 5 select `disabled` + `.select2-container--disabled`, "Thêm đơn vị" 0, "+" model 0, ô Tên vẫn sửa, dải màu chữ rgb(55,65,81) nền rgb(245,248,252) cao 39px. Không chặn ⇒ 5 ô mở, nút Thêm đơn vị 1.

**Role**: không tạo role tạm ngoài transaction PHPUnit (tự rollback). Đếm sau cùng roles=130 · role_has_permissions=20967 · employee_has_roles=1718 (bằng nhau trước/sau chạy test). Đăng nhập lại tài khoản e2e_assign qua API 1 lần để lấy token cho Playwright.

### Kết quả Lượt 2 — 16/10/2026
Commit trên nhánh con `feat/cdhh-loi-srs-1610`, CHƯA merge về nhánh chung, chưa push. Không migration / seeder / cache:clear, không role tạm (PHPUnit tự rollback).

| # | Trạng thái | Commit | Ghi chú |
|---|---|---|---|
| N169(a) | ✅ | api `b5f05024c` · client `e3f1fb6b9`, `b79191af4` | `query()` join pcc theo `pa.company_id` ⇒ `is_locked`. `approve()` kiểm 2 lần (trước validate + trong transaction, `lockForUpdate` pcc) ⇒ 422 khoá `locked`: "Hàng hoá đang ngừng kinh doanh, không duyệt được: <mã>. Mở khoá hàng hoá trước khi duyệt hoặc chọn Không duyệt." — cả lô không duyệt phần nào. Khoá ở công ty KHÁC không chặn. FE: dòng "🔒 Hàng đang khoá — mở khoá hàng hoá để duyệt, hoặc Không duyệt", nút Duyệt `disabled`, Không duyệt vẫn bấm; Duyệt hàng loạt có hàng khoá ⇒ toast mã, 0 request |
| N172 | ✅ | api `b5f05024c` · client `123e6d9a8` | `applyReject`: `*_wait_approve = NULL` ở upp / pep / pcu, giữ cờ 2; xoá pep cờ 1 + `price = 0` + `coefficient = 0`. `priceRow`/giá vốn/giá hiệu lực chỉ đọc giá chờ khi cờ = 1 (dữ liệu cờ 2 cũ tự đúng); lịch sử bản đề nghị cũng chỉ xét cờ 1. Unit trả `rejected_proposal` (log `rejected` mới nhất của ĐVT — khớp theo hậu tố " (ĐVT)" của dòng Giá vốn; chỉ khi `pcu.approve_comment` còn — Lưu / Gửi lại / Duyệt đều xoá lý do). FE (ô Tên): "Đề xuất Giá vốn 1,000,000; Bán lẻ 1,500,000, hệ số 1.5, ĐMGG 7% và N mục khác bị từ chối: <lý do>" (đủ trong `title`), thay dòng "Lý do không duyệt". `CompanyPriceBackfill` chép nguyên cột (không đọc ô) ⇒ không đổi |
| N173 | ✅ | api `d46bf314c` · client `b5b4d4855` | `meta.ecom_coefficient` = `ProductPriceWriter::ecomCoefficient(công ty đang làm)`; FE `this.ecom` từ meta (dự phòng 1,3) truyền xuống bảng |
| N170 | ✅ | client `b5b4d4855` | `baseOf()` = `unitFromApi` + `Calc.ecom(hệ số N173)` cho `setItems` + `replaceItem` |
| N171 | ✅ | client `b5b4d4855` | `revealCell()` tại trang: trước `scrollToFirstError`, chỉnh `scrollLeft` `.ppt-scroll` để ô lỗi cách mép cột dính 8px (hoặc kéo vào nếu tràn phải). Util chung không đổi |
| N174 | ✅ | client `b79191af4` | `base-confirm-modal` thêm `inputMaxLength`/`inputMaxMessage` (opt-in, mặc định 0 — 70+ màn không đổi; đếm `Array.from(trim())` khớp `mb_strlen(trim)`). `handleError`: khoá 422 không dạng `{pa}.{pap}.{trường}` ⇒ toast câu BE |
| N176 | ✅ | client `e3f1fb6b9` | dòng `kind==='exp'`: giá = `round(hệ số × giá vốn)`; dòng hiện hành giữ tròn trăm |
| N177 | ✅ | api `fc40bfc02` | `$hideCost = !canSeeCost()`; màn Cập nhật giá bán không đổi |
| N178 | ✅ | client `b79191af4` | "Đã không duyệt N yêu cầu. M yêu cầu đã được người khác xử lý." |
| N179 | ✅ | client `123e6d9a8`, `e3f1fb6b9` | Hệ số 72 ⇒ 110 ở 2 màn; tổng bề rộng tự cộng (đo: Cập nhật 1850 = tổng th; Duyệt 1782 = tổng th). Chữ lỗi "Bắt buộc phải nhập" còn 2 dòng (cao 33.6px, rộng 93px) — hết vỡ từng chữ; muốn 1 dòng cần ~125px |

**Test**
- hrm-api `Modules/MasterData/Tests`: `OK (562 tests, 5479 assertions)`
- hrm-api `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- `PriceReaderWhitelistTest`: `OK (2 tests, 45 assertions)` (đọc `catalog_histories` không phải bảng giá ⇒ không thêm whitelist)
- Ca mới: `ProductPriceApprovalApiTest::n169a_*` (2), `n172_*` (1), `n177_*` (1); `ProductPriceScreenApiTest::n172_*` (1), `n173_*` (1); sửa `o_gia_hien_ban_cho_duyet_…` (cờ 2 ⇒ giá vốn đang áp 800,000)

**Playwright MCP (3031/8031)** — trước ⇒ sau
- N170 (TEWI-AQUA, nạp lần đầu): TMĐT "0" / hệ số "0" ⇒ "443,300,000" / "2.08", không "● Chưa lưu"; chặn meta 1.4 ⇒ "477,400,000" / "2.24" (N173)
- N171: scrollLeft 29 ⇒ ô Giá vốn left 576 < cột dính right 605 (tái hiện đúng 29px); scrollLeft 400 ⇒ left 205 (khuất hẳn). Sau: left 605, chữ lỗi left 613; ô Giá mới Bán lẻ khi scrollLeft 900: 531 ⇒ 613
- N179 Duyệt: th Hệ số 72 ⇒ 110; chữ lỗi cao 67.2px (4 dòng, rộng 55) ⇒ 33.6px (rộng 93); Cập nhật: th 110
- N176: hệ số 2 × giá vốn 1,234,567 dòng hiệu lực "2,469,100" ⇒ "2,469,134"; dòng hiện hành vẫn "2,469,100"
- N169(a) (chặn API): trước không nhãn, nút Duyệt bật ⇒ sau nhãn có, `disabled=true` (Không duyệt `false`), Duyệt hàng loạt 0 request + toast
- N174: lý do 2001 ký tự: popup đóng + toast "The given data was invalid." ⇒ popup mở, giữ 2001 ký tự, lỗi inline; 422 approve_comment ⇒ toast "Không được vượt quá 2000 ký tự"
- N178: "Đã không duyệt 1 yêu cầu." ⇒ "… 1 yêu cầu đã được người khác xử lý."
- N172 (chặn API): dòng "Đề xuất Giá vốn 300,000,000; Bán lẻ 400,000,000, hệ số 1.8 và 1 mục khác bị từ chối: Giá cao hơn đối thủ", cao 48px

**e2e (sửa spec, KHÔNG chạy)**: `product-prices-ui` — P3 đọc `meta.ecom_coefficient` thay 1,3; thêm N170+N173, N171, N172+N179. `product-price-approvals-ui` — A2 đo cột Hệ số 110 (bản có 1092); A4 thêm N174 (2001 ký tự) + N172 (SQL `price_wait_approve` NULL, ô = giá đang áp, dòng "Đề xuất … bị từ chối"); A7 mới (chặn API: N169a, N176, N179, N174 422, N178). `--list` parse được (22 ca / 5 file).

**Role / DB**: không tạo role tạm. Đếm trước = sau: roles 130 · role_has_permissions 20967 · employee_has_roles 1718; product_approves 0 = 0. Không ghi DB qua giao diện (lưu đều bị validate chặn, còn lại chặn response).

### Kết quả Lượt 3 — 17/10/2026
Commit trên nhánh con `feat/cdhh-loi-srs-1610`, CHƯA merge về nhánh chung, chưa push. Không migration / seeder / cache:clear, không role tạm (PHPUnit tự rollback; giao diện kiểm bằng chặn response).

| # | Trạng thái | Commit | Ghi chú |
|---|---|---|---|
| N186 | ✅ | api `db61b27c4` · client `145159f3c` | BE `update()`: status 5 + không gửi ⇒ 422 khoá `status` "Yêu cầu Không duyệt chỉ được sửa rồi gửi lại" (giữ status 5, lý do, log). FE: ẩn Lưu nháp, nút + popup xác nhận "Gửi lại"; 422 `status` ⇒ toast |
| N187 | ✅ | api `db61b27c4` · client `145159f3c` | Nút / popup / toast "Không duyệt" (lịch sử giữ "KTMH không duyệt"); thông báo "[YCTG] Không duyệt: …" và "[YCTG] Chờ tính giá: …". ⚠️ 2 nhóm hành động này ngoài danh sách 14 giá trị của skill notification-convention — theo Q7 user chốt |
| N200 | ✅ | api `b19448eae` | `PriceCalculateWriter::lineReason()` trong vòng lặp: "PTG-x: <ghi chú dòng>" / "Phiếu tính giá PTG-x" — áp thẳng (pcu) và gửi duyệt (product_approves) |
| N190 · N198 | ✅ | api `b19448eae` · client `145159f3c`, `b4f43a318` | BE PTG `show()`/bản in: dòng không sửa được dùng số đã lưu (`storedNumbers`); YCTG BE vốn trả số đã lưu. FE `priceInputRowsMixin`: dòng `_stored` đọc supplier_price_exchange / amount_exchange_after_tax / costs value, value_exchange (+ `costExchange`); PTG giá nhập kho = `cost_price` đã lưu. Dòng sửa được vẫn tính lại |
| N196 | ✅ | client `b4f43a318` | `sellFromApi`: TMĐT `expected = []`; không đụng `blockRows` |
| N195 | ✅ | api `b19448eae` · client `b4f43a318` | `PriceCalculateAccess::MSG_NO_VIEW` "Bạn không có quyền xem phiếu tính giá", `MSG_GROUP_CLOSED` "Nhóm hàng đã đóng, phiếu tính giá chỉ còn xem." (writer lock + `requestForCreate`); filter-options `X-Silent-Errors` |
| N191 | ✅ | api `4295ccbb1` · client `145159f3c` | filterOptions YCTG qua `scopeVisible`; filter-options `X-Silent-Errors` |
| N185 | ✅ | api `4295ccbb1` | filterOptions YCHG qua `scopeVisible` (Người tạo, PTKD; thêm cả Thương hiệu / Hãng / XNK cho cùng kiểu) |
| N183 | ✅ | api `4295ccbb1` · client `de72a3fbf` | `xnk` = XNK lưu trên nhóm (khớp ô lọc), `xnk_current` khi phân công hiện hành khác; "Chờ … duyệt" vẫn theo người đang phân công. Danh sách: dòng phụ "Phân công hiện tại: …"; chi tiết YCHG cũng hiện |
| N184 | ✅ | client `de72a3fbf` | Cột + ô lọc "PTKD xử lý" |
| N188 | ✅ | client `145159f3c` | V2BaseError khoá `rows` ngay trên thanh tab |
| N189 | ✅ | client `145159f3c`, `b4f43a318` | "Không được lớn hơn 999,999,999,999." ở tỉ giá / giá NCC (YCTG + PTG qua mixin) / giá bán PTG |
| N182 | ✅ | client `de72a3fbf` | Form Sửa YCHG status 8 hiện "Ghi chú PTKD: <lý do>" |
| N180 | ✅ | client `de72a3fbf` | Cột Hành động `cellClass: 'text-wrap'` + `.wait-text` xuống dòng |
| N197 | ✅ | client `b4f43a318` | RequestPickerModal `size="xl"` |
| N202 | ✅ | client `49d989301` | `scrollToFirstError`: không focus ô trong `.mx-datepicker` (chỉ cuộn) — util chung, đổi 1 điều kiện |
| N201 | ✅ | api `b19448eae` · client `b4f43a318` | `delete()` kiểm chủ phiếu trước trạng thái ⇒ 403 "Bạn không có quyền xoá phiếu này" (thiếu "Tính giá bán hàng hoá" vẫn chặn ở route); cột Hành động thêm "Xem". ⇒ t5-plan C9 (xoá phiếu người khác 403) và C20 (nút Xem) nay KHỚP code — không sửa tài liệu thiết kế |

**Test**
- hrm-api `Modules/MasterData/Tests`: `OK (571 tests, 5632 assertions)`
- hrm-api `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- `PriceReaderWhitelistTest`: `OK (2 tests, 45 assertions)`
- Ca mới (đỏ trên code cũ — đã chạy lại với Services về HEAD cũ: 8/8 fail): `PriceCalculateRequestApiTest::n186_*`, `n191_*`; `PriceCalculateApiTest::n198_*`, `n195_*`, `n200_*` (2), `n201_*`; `PriceAskingRequestApiTest::n185_*`, `n183_*`; sửa tiêu đề thông báo ở `gui_ktmh_tu_choi_…` (N187)

**Playwright MCP (3031/8031, 1440×900)** — trước ⇒ sau
- N180 (bung 5 phiếu, 4 dòng "Chờ … duyệt"): bảng 1226 / khung 1139, cột Hành động 190px, mép phải 1481 > 1400 ⇒ bảng 1139 = khung, cột 100px, chữ chờ cao 49px
- N184: tiêu đề + nhãn lọc "PTKD duyệt" ⇒ "PTKD xử lý"; N183 (chặn API): dòng phụ "Phân công hiện tại: …" 12px rgb(107,114,128)
- N182 (chặn GET PYCHG-04283 thành status 8): không có lý do ⇒ "Ghi chú PTKD: …" (y 293)
- N190 PYCTG-03162 tab Chi phí: Bảo hiểm 4,021 ⇒ 4,398 (tổng 1,465,975 + 488,658 + 4,398 = 1,959,031 = bản in)
- N187: nút "Từ chối" ⇒ "Không duyệt", popup "Không duyệt yêu cầu tính giá / Lý do không duyệt"
- N186 (chặn GET PYCTG-02786 can_edit): [Lưu nháp, Lưu và gửi duyệt] ⇒ [Gửi lại], popup xác nhận nút "Gửi lại"
- N188 (chặn PUT ⇒ 422 rows): câu lỗi không hiện ở đâu ⇒ hiện trên thanh tab (1 PUT, bị chặn)
- N189: "Không hợp lệ" ×2 ⇒ "Không được lớn hơn 999,999,999,999." ×2, 0 request
- N191 / N195 (chặn 403 danh sách + ô lọc): 2 toast ⇒ 1 toast; PTG câu "phiếu tính giá"
- N201: hành động dòng PTG-03178 [Xem giá bán mới, In] ⇒ [Xem, Xem giá bán mới, In], href `/finance/price-calculates/3178`
- N197 (chặn pending-requests): popup 800, bảng 841 / vùng 726, nút Chọn 1117–1189 > mép 1120 ⇒ popup 1140 (150–1290), bảng 1066 = vùng, nút 1166–1239
- N198 PTG-03178: giá nhập kho 13,108,667 ⇒ 13,108,986 (= đã lưu + đã áp), Bảo hiểm 4,147 ⇒ 4,466; màn Sửa (dòng sửa được) vẫn tính lại 13,108,667. Bản in (API print-data): có 13,108,986 + 2,020,546, không còn 13,108,667 (không bấm nút In)
- N196 PTG-02618: TMĐT 2 dòng "giá sẽ áp dụng" ⇒ 1
- N202 (chặn GET PTG-03178 thành nháp sửa được, thêm giá hiệu lực bỏ trống ngày, Lưu nháp): lịch bật 1, focus trong datepicker ⇒ lịch 0, không focus, câu lỗi trong khung nhìn (top 457); 0 request ghi

**e2e (sửa spec, KHÔNG chạy)** — `HRM/e2e`: `sale/price-calculate-request.spec.ts` P4 "Không duyệt", P4b mới (N186 API 422 + nút Gửi lại, N188, N189), P5 thêm N190, N2 mới (N191); `sale/price-asking-request.spec.ts` P6 mới (N180, N183, N184, N182 — chặn response); `finance/price-calculate.spec.ts` P7 mới (N201, N197, N198, N196, N202 — chặn response), N2 mới (N195). `--list` (node 20) parse được: 27 ca / 6 file.

**Role / DB**: không tạo role tạm. Đếm sau: roles 130 · role_has_permissions 20967 · employee_has_roles 1718 (= mốc). Mọi lệnh ghi trên trình duyệt bị chặn bằng route.fulfill.

**Tồn / ngoài phạm vi**
- N187 lệch skill notification-convention (nhóm hành động "Chờ tính giá", "Không duyệt" không thuộc 14 giá trị) — theo Q7; nếu cần cập nhật skill thì hỏi riêng
- N185 mở rộng thêm Thương hiệu / Hãng / XNK của ô lọc YCHG (cùng gốc lộ nháp) — nếu không muốn thì bỏ 1 dòng

### Kết quả đợt N203/N179 — 17/10/2026
Nhánh `feat/cdhh-chua-co-gia-1710` (api + client), CHƯA merge nhánh chung, chưa push. Không migration / seeder / permission:sync / cache:clear; không ghi DB (PHPUnit tự rollback; Playwright chặn mọi request ghi bằng route.fulfill). Đếm sau cùng roles 130 · role_has_permissions 20967 · employee_has_roles 1718 (không đổi).

| # | Trạng thái | Commit | Ghi chú |
|---|---|---|---|
| N203 helper | ✅ | client `3b4a2ef1f` | `utils/unitOptionLabel.js` — `unitOptionLabel(unit, label?)`: `has_price === false` ⇒ thêm " (Chưa có giá)"; thiếu/null ⇒ giữ nhãn. `ManualLinesTable.vue` (YCXH) dùng helper thay chuỗi tự dựng |
| N203 Báo giá `quotations/_id/edit.vue` | ✅ | client `3b4a2ef1f` · api `730f25a38` | API `erp-product-units` đã có `has_price` từ N169(b) (qua `ProductPriceReader::unitOptions`). FE trước đây KHÔNG gửi `quotation_id` ⇒ BE lấy công ty người đăng nhập; nay gửi `quotation_id` ⇒ giá + `has_price` theo công ty GHI TRÊN báo giá (đổi ĐVT cũng lấy giá đúng công ty báo giá) |
| N203 BOM `BomBuilderEditor.vue` + `BomBuilderTableCard.vue` | ✅ | api `730f25a38` · client `3b4a2ef1f` | `DetailBomListResource` thêm `has_price` vào `unit_options` nhúng (vẫn KHÔNG trả số giá); `erp-product-units` nhận `bom_list_id` ⇒ công ty BOM; FE giữ cờ `has_price` khi lọc bỏ field giá; 2 bảng (2 chỗ option) dùng helper |
| N203 Mượn hàng `BorrowExportRequestForm.vue` | ✅ | api `730f25a38` · client `3b4a2ef1f` | `BorrowExportRequestService::unitsOfProducts` thêm `has_price = price > 0` (giá loại 1, đã kẹp công ty qua `joinPrices`). Nhãn "Thùng (x10) (Chưa có giá)" |
| N203 Giữ hàng `ProductPrepickRequestForm.vue` | ✅ | api `730f25a38` · client `3b4a2ef1f` | Gắn `has_price` ở `ProductPrepickRequestController::productUnits` (KHÔNG sửa `ProductImportRequestService::productUnits` — response màn Yêu cầu nhập hàng giữ nguyên, có ca test chốt). FE map giữ `has_price` |
| N203 `QuotationProductEditModal.vue` / `QuotationProductSearchModal.vue` | ✖ bỏ qua | — | Danh sách ĐVT là DANH MỤC ĐVT chung (`assign/product-projects/get-unit`, hàng tự nhập / hàng tạm YCHG) — không gắn hàng, không có khái niệm giá. Popup chọn hàng đã ghi "Chưa có giá" từ N169(b) |
| N203 `ServiceFormComponent.vue` (Gói bảo dưỡng) | ✖ bỏ qua | — | ĐVT của dòng nội dung kiểm tra lấy từ danh mục ĐVT (`units` + `locked_units`), không theo hàng hoá ⇒ không có giá ĐVT để cảnh báo |
| N179 | ✅ | client `b4ca906ac` | Hệ số 110 ⇒ **140px** (không phải ~125): đo DOM chữ lỗi = icon 14 + khoảng 6 + chữ 103px (12px Roboto) + đệm ô 16 = 139px ⇒ 125 vẫn 2 dòng (đã thử: rộng 108, cao 33.6). Tổng bề rộng tự cộng ở `totalWidth` |
| N165 | ✅ (spec) | e2e (ngoài git) | `product-price-approvals-ui` A2: cả 2 trạng thái quyền "Xem giá vốn hàng hoá" giả lập bằng chặn phản hồi danh sách (không quyền ⇒ xoá 4 trường + `can_view_cost=false`). `product-prices-ui` P7: chọn công ty KHÁC 1 mà vai trò mang quyền "Cập nhật giá bán hàng hoá" của e2e_assign THỰC SỰ gắn (`employee_has_roles.company_id`), không có ⇒ `test.skip` kèm lý do; trả `company_role` cũ trong `finally` (trước đây không trả). ⚠️ Phương án tự gắn tạm vai trò cho công ty 2 bị bộ phân loại quyền chặn (sửa tài nguyên dùng chung) ⇒ trên DB hiện tại P7 sẽ SKIP |
| N155 | ✅ (spec) | e2e (ngoài git) | `tests/customer-care/services-ui.spec.ts` mới: role tạm "E2E N155 tạm - Thêm Sửa gói bảo dưỡng" qua `utils/tempRoleFixture` (company_id = 1 ở 2 pivot, xoá cache quyền), afterAll gỡ + kiểm 0 role. S1 nút Tạo mới + API store 422 (qua cổng quyền); S2 lỗi Tên / 422 Mã + Công ty hiện cùng lúc (chặn POST); S3 form Sửa nhóm theo Loại SP lấy từ hàng (khớp SQL), "Chưa phân loại" cuối, Lưu 1 POST (chặn); N1 gỡ role ⇒ 0 Tạo mới, API store/update 403 |

**Test**
- `PriceReaderWhitelistTest`: `OK (2 tests, 45 assertions)`
- hrm-api `Modules/MasterData/Tests`: `OK (575 tests, 5644 assertions)` (gồm ca mới `UnitHasPriceTest` 4 ca: xuất mượn, giữ hàng + khuôn YCNH không đổi, erp-product-units theo BOM, chi tiết BOM nhúng `has_price` không số giá)
- hrm-api `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- hrm-api `Modules/Finance/Tests`: `Tests: 121, Assertions: 6695, Errors: 1, Failures: 1, Skipped: 1.` — 2 ca đỏ SẴN, không liên quan (đã chạy lại với 2 file Finance trả về bản trước commit: vẫn đỏ y hệt): `BorrowSellStoreTest::test_returning_qty_excludes_parent_request` (FK `created_by = 1` không có trong `employees`), `PrepickTrackingApiTest::test_export_tree_indent_and_bold_per_level`
- e2e (sửa spec, KHÔNG chạy): `npx playwright test --list` (node 20) parse được 29 ca / 8 file gồm `quotation-unit-select` (+ ca N203), `services-ui` (4 ca mới), `product-price-approvals-ui`, `product-prices-ui`

**Playwright MCP (3031/8031, tài khoản e2e_assign, mọi POST/PUT ghi bị chặn)**
- Báo giá 279 (hàng 3921): option ĐVT `["Cái (Chưa có giá)", "Hộp", "Thùng (Chưa có giá)"]` — khớp API (`Cái` 0 / `Hộp` 60,000 / `Thùng` 0); request `{"erp_product_ids":[3921],"quotation_id":279}`; option không disabled
- BOM 23 (sửa, chặn GET chi tiết ép `has_price=false` cho 1 dòng): 119 select ĐVT; dòng ép ra "Bộ (Chưa có giá)", dòng khác "Bộ" / "Xô 18L" / "Cái." không ghi chú; API chi tiết đã có khoá `has_price`
- Xuất mượn / giữ hàng: kiểm qua API (curl) `[('Cái', 0, False), ('Hộp', 60000, True), ('Thùng', 0, False)]` cả 2 route; màn Sửa giữ hàng 2467 không nạp ĐVT với tài khoản e2e (không phải người lập ⇒ chế độ xem) nên chưa đo được DOM 2 màn này
- N179 Duyệt giá (chặn danh sách giả lập, có quyền xem giá vốn): trước — th Hệ số 110, chữ lỗi cao 33.6px (2 dòng, rộng 93); thử 125 — vẫn 33.6px (rộng 108); sau 140 — cao 19px, 1 dòng (getClientRects = 1), rộng 123; bảng 1812 = tổng th 1812 (15 cột)
- N179 Cập nhật giá: th Hệ số 140 = td 140; xoá Hệ số + Lưu ⇒ "Bắt buộc phải nhập" cao 19px, 1 dòng; bảng 1880 = tổng th 1880; 0 request ghi

**Còn mở / ghi chú**
- Giá ĐVT ở xuất mượn + giữ hàng vẫn theo công ty NGƯỜI ĐĂNG NHẬP (controller không truyền công ty phiếu — như trước đợt này); `has_price` nhất quán với giá đang hiện. Sửa phiếu công ty khác ⇒ cùng lệch như giá
- ~~Ô ĐVT báo giá cắt chữ~~ ✅ đã đo + sửa — xem "Bổ sung N203 — ô ĐVT báo giá" bên dưới
- `product-price-approvals-ui` N2 cũng đổi `company_role = 2` — cùng kiểu giả định dữ liệu quyền như P7, ngoài phạm vi N165 đợt này
- P7 sẽ skip trên DB hiện tại cho tới khi có vai trò gắn công ty khác (cần user cho phép spec tự gắn tạm, hoặc dựng dữ liệu)

#### Bổ sung N203 — ô ĐVT báo giá (17/10/2026) · client `b5cd3188d`
- Tái hiện (báo giá 279, 1440px, ĐVT đang chọn "Cái" chưa có giá): select rộng 73px trong td 90px, chỗ cho chữ 51.8px (đệm 9.6 × 2) mà chữ "Cái (Chưa có giá)" rộng 92.2px ⇒ BỊ CẮT (`text-overflow: clip`, không title). Cột KHÔNG giãn (td 90, bảng 2244.98 — select co theo ô)
- Sửa (chỉ màn báo giá `quotations/_id/edit.vue`): option của ĐVT ĐANG CHỌN chỉ hiện tên; các option khác vẫn "(Chưa có giá)"; ĐVT đang chọn chưa có giá ⇒ chấm đỏ 6px (#dc2626, `position: absolute` góc trên phải, nằm trong khung select) + `title` "Cái (Chưa có giá)" trên khối ô
- Sau: chọn "Cái" (chưa giá) — option `["Cái", "Hộp", "Thùng (Chưa có giá)"]`, chữ 17.3px ≤ 51.8px, chấm đỏ 1 (trong khung select), title đúng; đổi sang "Hộp" (có giá) — `["Cái (Chưa có giá)", "Hộp", "Thùng (Chưa có giá)"]`, 0 chấm, title rỗng. Select 73 / td 90 / bảng 2244.98 — không đổi trước/sau. Ghi bị chặn
- e2e `quotation-unit-select` ca N203 cập nhật: chọn ĐVT chưa giá ⇒ ô hiện tên gốc, chữ ≤ chỗ trống, 1 chấm đỏ, title, bề rộng select không đổi (`--list` parse được)

#### Bổ sung N203 — ô ĐVT BOM (17/10/2026) · client `307690f70`
- Tái hiện (BOM 23 sửa, 1440px, chặn GET chi tiết ép `has_price=false` cho ĐVT đang chọn): select `.table-input` cố định 90px trong td 112px, chỗ cho chữ 72px (đệm 8 × 2) mà "Bộ (Chưa có giá)" rộng 94.4px ⇒ BỊ CẮT (`clip`, không title). Cột không giãn (bảng 3270.68)
- Sửa `BomBuilderTableCard.vue` (cả 2 chỗ render select ĐVT trong file), đúng khuôn báo giá: option ĐVT đang chọn chỉ hiện tên, option khác vẫn "(Chưa có giá)"; khối bọc `inline-block` ôm sát select + chấm đỏ 6px #dc2626 absolute góc trên phải + `title`. `BomBuilderEditor.vue` không đổi thêm (đã giữ `has_price`)
- Sau: dòng ép — chữ "Bộ" 15px ≤ 72px, title "Bộ (Chưa có giá)", chấm đỏ nằm TRONG khung select (rgb(220, 38, 38)); select 90 / td 112 / bảng 3270.68 = trước; cao dòng 98 = khi gỡ khối bọc (mô phỏng DOM cũ). Ghi bị chặn
- e2e: không có spec BOM nào kiểm ô ĐVT ⇒ không sửa spec

- Đối chiếu số chấm đỏ (BOM 23, công ty 1): KHÔNG ép ⇒ 3 chấm / 119 ô ĐVT; API chi tiết trả đúng 3 dòng có ĐVT đang chọn `has_price=false` (0 dòng lệch unit_id) và khớp 3 dòng chấm: DMLS-DK150 · Bộ · 0đ, JONN-AI030045 · Bộ · 0đ, SN-T05003-500G · Cái · 0đ (truy vấn chỉ đọc `product_unit_prices` công ty 1 loại 1 = 0.00; SQL đếm dòng cha ERP của BOM có giá ≤ 0 = 3). ÉP 1 dòng vốn có giá (NAHU-NHXZ-04:02 · Bộ · 265,000,000) ⇒ 4 chấm = 3 + 1. Con số "4 chấm" ở lần đo trước = 3 thật + 1 ép — không lệch, không phải lỗi

### Kết quả N205 — 17/10/2026
Nhánh `feat/cdhh-n205-gia-cty-phieu` (api + client), CHƯA merge nhánh chung, chưa push. Không migration / seeder / cache:clear / ghi DB (PHPUnit tự rollback; Playwright chặn mọi request ghi bằng route.fulfill — 0 request ghi).

| Màn | Trạng thái | Commit | Ghi chú |
|---|---|---|---|
| Giữ hàng (yêu cầu xuất giữ) | ✅ | api `784814717` · client `de26eb522` | `ProductPrepickRequestController::productUnits` nhận `product_prepick_request_id` ⇒ giá + `has_price` theo `company_id` của phiếu (`CompanyHelper::pricingCompanyId($doc)`); không gửi ⇒ công ty đang làm. Phiếu không tồn tại / `canView()` false (đúng cổng của `show()`) ⇒ 404 "Không tìm thấy yêu cầu xuất giữ hoặc bạn không có quyền xem." Công ty truyền TƯỜNG MINH vào `ProductImportRequestService::productUnits` ⇒ API ĐVT màn Yêu cầu nhập hàng không đổi. FE `ProductPrepickRequestForm.loadUnits` gửi id khi có `requestId` (màn Sửa) |
| Mượn hàng (yêu cầu xuất hàng mượn) | ✖ không sửa | — | Màn chỉ có TẠO (không route update, form chỉ dùng ở `create.vue`; Chi tiết hiện giá ĐÃ LƯU) ⇒ không có "phiếu đã lưu" để gửi id; giá ĐVT lúc tạo theo công ty đang làm = đúng quy tắc "phiếu chưa lưu". Lưu: BE tự tính lại giá (`productSnapshot` theo `pricingCompanyId($object)`), không tin giá client |

**Lưu phiếu — có tính lại giá theo công ty phiếu không?**
- Mượn hàng: CÓ (`storeProducts` → `productSnapshot($productId, $unitId, …, pricingCompanyId($object))`).
- Giữ hàng: KHÔNG — `normalizeLines` lấy `price` + `total_amount` từ payload FE (`$row['price']`) cho mọi loại; loại 99 giá lấy từ ĐVT, loại gắn hợp đồng giá lấy từ hợp đồng. KHÔNG sửa đợt này (đổi ngữ nghĩa lưu: phiếu nháp cũ mở ra lưu sẽ bị chốt lại theo giá hiện hành; loại hợp đồng cần chốt nguồn giá riêng) ⇒ ghi tồn, cần user quyết.

**Test**
- Ca mới `Modules/MasterData/Tests/Feature/PrepickUnitPriceDocCompanyTest` (5 ca: phiếu công ty B ⇒ giá B dù đang làm C; phiếu công ty A chưa giá ⇒ has_price false; tạo mới ⇒ công ty đang làm; nháp người khác + id không tồn tại ⇒ 404 không lộ giá; API YCNH không đổi). Trên controller cũ: 3/5 đỏ (3 ca mới), 2 ca giữ hành vi xanh.
- hrm-api `Modules/MasterData/Tests`: `OK (580 tests, 5652 assertions)`
- hrm-api `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- hrm-api `Modules/Finance/Tests`: `Tests: 121, Assertions: 6695, Errors: 1, Failures: 1, Skipped: 1.` — đúng 2 ca đỏ sẵn: `BorrowSellStoreTest::test_returning_qty_excludes_parent_request`, `PrepickTrackingApiTest::test_export_tree_indent_and_bold_per_level`
- `PriceReaderWhitelistTest`: `OK (2 tests, 45 assertions)`

**Playwright MCP (3031/8031, 1440×900, tài khoản e2e_assign — đang làm công ty 1)** — màn Sửa PYCXG-02307 (chặn GET chi tiết: giả phiếu Đang tạo, loại 99, `company_id` 4, 1 dòng ENEO-410-V5250 "Chai 1 Lít" 147,000). Giá DB (chỉ đọc): Chai 1 Lít 140,000 (cty 1) / 147,000 (cty 4); Thùng 24 Chai 3,341,000 / 3,508,000
- TRƯỚC (FE về HEAD cũ): request `…/products/41240/units` KHÔNG kèm id, BE thật trả giá cty 1; đổi ĐVT sang Thùng ⇒ Đơn giá **3,341,000**, Thành tiền 6,682,000 (sai — phiếu cty 4)
- SAU, BE thật: request `…/units?product_prepick_request_id=2307` ⇒ **404** (e2e_assign không xem được phiếu thật 2307) ⇒ ô ĐVT 0 option, không lộ giá công ty khác
- SAU, phản hồi ĐVT = đầu ra BE thật đã sửa cho người XEM ĐƯỢC phiếu (tinker chỉ đọc, NV công ty 1 có quyền xem: 147,000 / 3,508,000; không gửi id: 140,000 / 3,341,000): đổi ĐVT sang Thùng ⇒ Đơn giá **3,508,000**, Thành tiền 7,016,000
- 0 request ghi (POST/PUT/DELETE bị chặn)

**e2e**: không có spec nào cho màn Giữ hàng / Mượn hàng ⇒ không sửa spec.

**Tồn / ngoài phạm vi**
- Giữ hàng lưu tin giá client (xem trên) — cần quyết có chốt giá ở BE cho loại 99 không.
- Công ty "phiếu chưa lưu" lệch nguồn: giá đọc `currentEmployeeCompanyId()` = `employee_infos.company_role ?: company_id`, còn `store()` của Mượn hàng / Giữ hàng (và YCXH) ghi `company_id = employee_infos.company_id`. Người có `company_role ≠ company_id` (DB local: 3/1119 nhân sự) thấy giá công ty đang làm nhưng phiếu ghi công ty gốc (Mượn hàng còn tự tính lại giá theo công ty gốc lúc lưu ⇒ giá hiện ≠ giá lưu). Vấn đề chung của cả hệ, không sửa đợt này.
- `BorrowExportRequestService::exportRequestData` trả `units` (giá theo công ty phiếu xuất mượn nguồn) nhưng FE không dùng giá này — không ảnh hưởng.

### Kết quả N207 — 17/10/2026

Nhánh `feat/cdhh-n207-gia-giu-hang` (api + client), CHƯA merge nhánh chung, chưa push. Không migration / seeder / cache:clear / ghi DB (PHPUnit tự rollback; Playwright chặn GET chi tiết + PUT bằng route.fulfill).

| Repo | Commit | Nội dung |
|---|---|---|
| hrm-api | `cf4b83e67` | `ProductPrepickRequestService::store()/update()` → `normalizeLines(..., $priceCompanyId)` BỎ QUA `price` / `total_amount` / tên / mã / model / hãng / tên ĐVT client gửi. Loại 1–5: dòng hợp đồng (`contractLines` đọc 1 lần, dùng chung cho kiểm SL còn lại qua `remainingFromLines`; khoá `lineKey` — loại 5 HĐ hãng theo `product_id`; `contractLines` thêm `orderBy('id')` ⇒ nhiều dòng cùng hàng lấy dòng id nhỏ nhất); hàng không có trong HĐ ⇒ giá 0. Loại 99: giá bán lẻ (price_type_id 1) theo ĐVT qua `ProductPriceReader::pricesByUnit` (cách `resolveManualLineMeta`); `store()` dùng `$docCompanyId` = CHÍNH biến ghi `company_id` phiếu (vẫn `employee_infos.company_id`, không đổi — N208); `update()` dùng `CompanyHelper::pricingCompanyId($object)`. ĐVT không giá ⇒ 0, không chặn. `total_amount` = SL × giá BE ⇒ `needBoardApprove()` loại 99 so ngưỡng bằng tổng thật. Nhãn: dòng HĐ > danh mục hàng hoá; tên ĐVT tra `units` theo `unit_id` |
| hrm-client | `01ef566f7` | `ProductPrepickRequestForm.loadUnits`: màn Sửa (không phải Chi tiết), dòng đã có ĐVT ⇒ đặt Đơn giá = giá hiện hành của ĐVT (công ty phiếu, N205), ĐVT không có trong danh sách ⇒ 0 — đúng số BE sẽ lưu. Chạy trước `markFormPristine()` ⇒ không bẩn form. Sau khi lưu, form quay về danh sách (rule 22/08) / "Lưu và tiếp tục" mở form trống ⇒ mọi chỗ hiện giá sau lưu đều đọc từ BE, không cần nạp lại chi tiết |

**Test** — mới `Modules/Finance/Tests/Feature/PrepickRequestServerPriceTest` (6 ca): (a) loại 99 giá giả ⇒ giá lẻ công ty phiếu C (300,000 / ĐVT phụ 3,300,000) + nhãn tên/mã/ĐVT tra BE; (f) ĐVT không giá ⇒ 0; (d) Sửa phiếu Cty B khi đang làm C ⇒ 200,000; (e) ngưỡng BGĐ loại 99 = tổng BE (600,000 > 100,000 ⇒ true); (b) loại 1 ⇒ giá dòng HĐ 123,456; (c) loại 5 hai dòng cùng hàng khác ĐVT/giá ⇒ dòng đầu 111,000. Trên code cũ: **6/6 đỏ** (lưu đúng giá client 1 / 5 / 7 / 9 / 999999, ngưỡng false).
- `Modules/Finance/Tests`: `Tests: 127, Assertions: 6705, Errors: 1, Failures: 1, Skipped: 1.` — đúng 2 ca đỏ sẵn (`BorrowSellStoreTest::test_returning_qty_excludes_parent_request`, `PrepickTrackingApiTest::test_export_tree_indent_and_bold_per_level`)
- `Modules/Assign/Tests`: `OK, but incomplete, skipped, or risky tests! Tests: 25, Assertions: 3886, Skipped: 1.`
- `Modules/MasterData/Tests` (gồm `PriceReaderWhitelistTest`): `OK (580 tests, 5652 assertions)` — không cần thêm whitelist (đọc giá qua `ProductPriceReader`)

**Playwright MCP (3031/8031, 1440×900, e2e_assign)** — màn Sửa phiếu giả id 999999 (GET chi tiết chặn: loại 99, Đang tạo, dòng SKYO-SB-2P ĐVT "Cái." SL 2 giá ĐÃ LƯU 1đ; API ĐVT thật trả 11,800,000):
- TRƯỚC (FE cũ): Đơn giá **1**, Thành tiền **2**, Tổng **2**; PUT Lưu nháp gửi `price: 1` (BE mới sẽ lưu 11,800,000 ⇒ màn ≠ số lưu)
- SAU: Đơn giá **11,800,000**, Thành tiền **23,600,000**, Tổng **23,600,000**; `isFormDirty()` = false; PUT gửi `price: 11800000`. Thêm dòng N207-B giá đã lưu 999, ĐVT 42 không có trong danh sách ĐVT ⇒ **0 / 0**, payload `price: 0`
- Console: chỉ lỗi có sẵn (ảnh `e2e.png` 404, `visibleExportFields` chưa khai ở `pages/finance/product-prepick-requests/index.vue` — màn danh sách, không đụng)
- e2e: thêm `e2e/tests/finance/product-prepick-request-price.spec.ts` (worktree, ngoài git; mock hoàn toàn, không ghi DB) — CHƯA chạy (chỉ chạy khi user yêu cầu)

**Tồn**
- N208 làm lộ thêm: màn TẠO lấy giá ĐVT theo `company_role ?: company_id` (công ty đang làm) còn BE lưu theo `employee_infos.company_id` ⇒ với người có 2 giá trị khác nhau (3/1119 NV local) giá lúc tạo ≠ giá lưu (BE đúng công ty phiếu, màn sai). Đóng cùng N208.
- Loại 1–5 màn Sửa vẫn hiện giá ĐÃ LƯU (không nạp lại giá HĐ) — giá HĐ đã ký hầu như không đổi; lệch chỉ với nháp cũ lưu giá client khác HĐ. Loại 5: hàng nhiều dòng khác ĐVT vẫn chỉ nhận ĐVT dòng đầu (khuôn kiểm SL ERP, không đổi).
- Ghi chú lịch sử: sửa nháp cũ có giá client ≠ giá hiện hành ⇒ lưu lại sẽ chốt theo giá hiện hành và ghi diff giá vào lịch sử (đúng chốt N207).
