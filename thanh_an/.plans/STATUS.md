# Trạng thái Features

> Cập nhật khi: tạo feature mới, wrap up, chuyển feature, hoặc merge xong.
> Không xóa entry trong "Hoàn thành".

## Đang làm

- **Báo cáo tổng hợp nhu cầu mua hàng (màn thứ 3 phân hệ Cung ứng)** — Báo cáo tổng hợp nhu cầu mua hàng dựa trên demo `bao_cao_nhu_cau_mua.html`: mỗi khối = 1 mã hàng, đối chiếu tồn kho khả dụng / tồn thầu (HĐ bán) / HĐ mua NCC còn hiệu lực / đề xuất đi mua (sinh từ Phiếu xử lý cung ứng) → quyết định mua. Build đủ khung, chỉ "SL đề xuất mua" là dữ liệu thật (gom `alloc_mua`, phiếu status=5), cột tồn kho/tồn thầu/HĐ mua giữ chỗ `—` chờ module; +1 quyền mới (id 517), không phân quyền cấp, Excel FE, KHÔNG migration. BE: `SupplyReportService::purchaseDemand` + `SupplyReportController` + route `GET supply/reports/purchase-demand`. FE: menu + `pages/supply/reports/purchase-demand/index.vue` (KPI/filter/bảng rowspan/popup/tooltip/Excel). Nhóm hàng lấy `products.product_group_id→product_groups.name`; người đề xuất lấy theo `Employee.id` (khớp `getEmployeeCreateNameAttribute`); filter options từ tập gốc (không tự thu hẹp). **Code xong 9 task (review + sửa 4 điểm), CHỜ user verify UI E2E** (cần seed quyền 517 + có PXL status=5 có dòng Mua hàng). (@namdangit) — 2026-07-13, ĐANG LÀM (code xong, chờ verify UI)
  - Spec: `docs/superpowers/specs/2026-07-13-bao-cao-nhu-cau-mua-design.md`
  - Design tóm tắt + Plan: `.plans/bao-cao-nhu-cau-mua/design.md` · `plan.md`

- **Xử lý cung ứng — build thật (màn thứ 2 phân hệ Cung ứng)** — Màn cho user quyền "Xử lý cung ứng hàng hóa": inbox đề xuất → Từ chối / Tạo phiếu xử lý. **Refactor đề xuất sang mô hình phản hồi**: 1 đề xuất → nhiều phiếu xử lý + nhiều từ chối; trạng thái suy ra (Chờ tiếp nhận/Đang xử lý/Đã từ chối); reject → bảng `supply_proposal_rejections` (bỏ set status terminal). BE: 3 bảng mới (`supply_handlings` + `_products` 9 cột phân bổ + `supply_proposal_rejections`), quyền 515 "Duyệt phiếu xử lý cung ứng", API supply-handlings CRUD + approve/reject-approve + supply-proposals/inbox; PXL loại KH=Đã lập(5), nội bộ=Chờ duyệt(3)→BGĐ duyệt→5/7. FE: menu +2 (inbox + danh sách PXL), form phiếu xử lý (bảng phân bổ theo loại + tabs tổng hợp read-only: đề nghị xuất kho/mua/xuất gửi/trả vay + tham chiếu HĐ + validate vượt đặt đơn/HĐ + duyệt), bổ sung khối "Phản hồi xử lý" ở đề xuất. Lưu phân bổ + tab tổng hợp (chưa sinh chứng từ thật). **Code xong 9 task (mỗi task đã review, nhiều opus + đối chiếu BE thật), CHỜ user verify UI E2E.** (@namdangit) — 2026-07-08, ĐANG LÀM (code xong, chờ verify UI)
  - Spec: `docs/superpowers/specs/2026-07-08-xu-ly-cung-ung-design.md`
  - Design tóm tắt + Plan: `.plans/xu-ly-cung-ung/design.md` · `plan.md`

- **Phiếu đề xuất cung ứng — build thật (màn đầu tiên phân hệ Cung ứng)** — Xây màn đầu tiên phân hệ Cung ứng. Module BE mới `Modules/Supply` (3 bảng `supply_proposals`/`_products`/`_files`, không FK; 3 quyền id 512/513/514 group "Cung ứng" type 7; API `/api/v1/supply/supply-proposals` CRUD + send + reject + customers + goods-pool; auto mã `DXCU-YYYY-####`; trạng thái 1 Nháp/3 Đã gửi/7 Từ chối/9 Đã xử lý; gửi → thông báo nhóm "Xử lý cung ứng" qua `notifications`). FE: wire phân hệ `/supply` (MenuSupply + layouts/default + dashboard + tile), danh sách + form add/edit/show 3 khối (thông tin chung + nội dung/file + bảng hàng hóa với popup chọn hàng Trong/Ngoài HĐ + tab tham chiếu HĐ) + modal từ chối. Không phân quyền cấp; xóa được Nháp+Từ chối của mình. UI theo convention PM (Bootstrap-Vue), demo chỉ tham chiếu luồng. **Code xong 11 task (mỗi task đã review, nhiều task opus + đối chiếu BE thật), CHỜ user verify UI E2E.** (@namdangit) — 2026-07-08, ĐANG LÀM (code xong, chờ verify UI)
  - Spec: `docs/superpowers/specs/2026-07-08-de-xuat-cung-ung-design.md`
  - Plan chi tiết (11 task): `docs/superpowers/plans/2026-07-08-de-xuat-cung-ung.md`
  - Design tóm tắt + Plan: `.plans/de-xuat-cung-ung/design.md` · `plan.md`

## Tạm dừng

_(chưa có)_

## Hoàn thành (3 entry gần nhất)
- **Import Excel — Vật tư, phụ kiện thay thế sửa chữa (tab Thông tin bổ sung, màn Danh mục hàng hóa)** — Bổ sung 2 nút "Tải file mẫu" + "Import Excel" cho section "Vật tư, phụ kiện thay thế sửa chữa" trong tab Thông tin bổ sung màn `category/product`. Khớp hàng hóa theo Mã nội bộ (status=2), tái dùng endpoint `importExcel` (thêm nhánh `type='replacement-attachment'`), all-or-nothing khi có dòng lỗi, gộp theo object_id; lưu DB khi Lưu cả form. Task 1-5 (subagent-driven, mỗi task review + final review opus sạch Critical). BE: mới `ProductReplacementAttachmentImport` (verify DB thật: gộp quantity=5, `name` lấy từ `product_name`) + nhánh `type='replacement-attachment'` trong `OtherIncomeController@importExcel` (all-or-nothing, php -l + route PASS). FE: mới modal `import-excel-modal-replacement-attachment.vue` (feedback đủ: dòng lỗi/success=false/rỗng, `<Required/>`) + file mẫu `static/vat_tu_thay_the_mau.xlsx` + sửa `AdditionalInfo.vue` (2 nút + handler gộp theo object_id, template compile OK). Fix từ review: bỏ `.csv` accept, xử lý phản hồi im lặng. Không migration, không phân quyền cấp. (@namdangit) — 2026-07-22, HOÀN THÀNH (user xác nhận xong 2026-07-23)
  - Spec: `docs/superpowers/specs/2026-07-22-import-excel-vat-tu-thay-the-design.md`
  - Plan chi tiết (6 task): `docs/superpowers/plans/2026-07-22-import-excel-vat-tu-thay-the.md`
  - Design tóm tắt + Plan tổng quát: `.plans/import-excel-vat-tu-thay-the/design.md` · `plan.md`

- **Fix: HĐ Nguyên tắc bị tính giá trị hợp đồng** — HĐ loại Nguyên tắc (type=5) là HĐ khung, giá trị phải = 0, nhưng HĐ 371 hiện 4.181.000 do 7 dòng nhóm I lọt `qty=1` (nguồn từ báo giá BG-472). Root cause: BE `syncGroups` dùng `qty ?? 0` (no-op khi qty≠null) + FE bê qty từ báo giá/import. Fix 3 điểm: BE `ContractService::syncGroups` hard-set qty=0 & amount=0 cho type 5; FE `GeneralComponent::onQuotationChange` set qty:0; FE `ProductComponent::handleImportSuccess` normalize qty/amount=0. Code xong 3 task, php -l BE PASS. Không migration. (@namdangit) — 2026-07-22, HOÀN THÀNH (user xác nhận xong 2026-07-23)
  - Plan: `.plans/fix-contract-nguyen-tac-qty/plan.md`

- **Hợp đồng mua (build thật — màn thứ 4 phân hệ Cung ứng)** — Dựng thật màn "Hợp đồng mua" (mua hàng NCC) trong module Supply từ demo `demos/demo-lap-hop-dong-mua.html`: 4 màn (danh sách + thêm mới + xem/sửa + duyệt). Full-stack BE+FE. Nguồn hàng lấy từ Báo cáo nhu cầu mua hàng (popup chọn hàng). Luồng duyệt GIỐNG HĐ bán (status 1 nháp/2 chờ duyệt/3 duyệt/4 từ chối/5 hủy, 1 endpoint store, sendNotification). Phân quyền KHÔNG phân cấp. 2 loại HĐ: Nguyên tắc (chỉ đơn giá) / Thương mại (SL+thành tiền+tổng). Bên B (NCC) info lưu snapshot header (bảng suppliers chỉ có name/code). Tái dùng mô hình HĐ bán: payment_terms 4 loại (100PCT/TIME/VALUE/ROLLING), theo đợt, auto code. Trừ nhu cầu bên báo cáo: ĐỂ SAU (chừa con trỏ nguồn). **CODE XONG Task 1-10 (subagent-driven, mỗi task review, toàn bộ Opus).** BE: 4 bảng (đã migrate) + 4 entity + Request + Service (generateCode HDM-YYYY-####, getList không phân cấp, store/update sync products/payment_terms/progress, approve/reject, sendNotification quyền Duyệt) + 2 transformer (status_color=text_type) + controller 11 endpoint + routes + 3 quyền id 518/519/520 (đã seed). FE: menu + danh sách + form add/edit (PurchaseContractForm+GeneralTab+ProductsTab+GoodsPickerModal+PrintTab, CKEditor điều khoản, docSo bằng chữ, cảnh báo SL over/under, gộp hàng theo mã in-place) + trang xem/duyệt. **BE LIVE-VERIFY PASS** (route:list 11 endpoint; smoke store→total đúng 84.150.000; goods-pool 6 demand+3169 catalog). **Task 11 browser E2E: CHỜ user bật Nuxt dev + tài khoản test.** (@namdangit) — 2026-07-20, HOÀN THÀNH (user xác nhận xong)
  - Spec: `docs/superpowers/specs/2026-07-20-hop-dong-mua-design.md`
  - Plan chi tiết (11 task): `docs/superpowers/plans/2026-07-20-hop-dong-mua.md`
  - Design tóm tắt + Plan + Ledger: `.plans/hop-dong-mua/design.md` · `plan.md` · `progress-ledger.md`

- **Giữ nguyên tên file gốc khi upload** — Tên file đính kèm bị đổi khác lúc upload (phát hiện ở `timesheet/request-payment-working-fee/add`, thực chất lỗi TOÀN HỆ THỐNG). Root cause `CmcS3Helper::putFile()`: `Str::slug` cả tên lẫn extension (`.pdf`→`-pdf`, mất dấu tiếng Việt) + nối `-{timestamp}-{random4}`. Sửa: giữ nguyên 100% tên gốc, chuyển phần chống trùng sang path thư mục `{folder}/{timestamp}-{random}/{Tên gốc}.pdf`. FE: `fileNameFromUrl()` copy-paste ở 27 file → gom về `utils/helpers.js` có `decodeURIComponent` (URL S3 nay percent-encoded); 13/27 bản là code chết đã xóa. Verify tĩnh PASS (parse 27/27 .vue, php -l, unit test 6 case gồm URL format cũ). Tồn: `putFileProduct()` cùng bug, chưa sửa. (@khoipv) — 2026-07-16, HOÀN THÀNH (user xác nhận xong 2026-07-17)
  - Plan: `.plans/upload-file-giu-ten-goc/plan.md`

- **Demo "Lập hợp đồng mua" (prototype)** — File demo HTML standalone form tạo HĐ mua với NCC — bản **đảo vai** của form HĐ bán (`contract/contract/add`): công ty mình = Bên Mua (Bên A), NCC = Bên Bán (Bên B). 5 tab như HĐ bán (Thông tin chung + Hàng hóa + Điều khoản thanh toán + Mẫu in + Đính kèm). **2 loại HĐ**: Nguyên tắc (chỉ đơn giá, không SL/thành tiền/tổng) · Thương mại (hiện cột SL + Thành tiền + Tổng giá trị HĐ) — toggle ẩn/hiện cột bằng CSS `body.mode-thuongmai`. Hàng hóa **chia nhóm** (nghiệp vụ), thêm/xóa nhóm+dòng, tính thành tiền/tổng realtime. **Điều khoản = 1 ô rich-text** (giống `ConditionComponent`) điền sẵn 8 điều rút gọn từ mẫu HĐNT 143. Bên A chọn từ dropdown công ty → auto điền; Bên B chọn NCC → auto điền (data mẫu Thành An + Hồng Anh/Roche từ mẫu thực tế). UI Bootstrap 4 + b-tabs mô phỏng client. **E2E Playwright PASS** (2 tab, toggle loại, tính tổng 120.8tr, nút Lưu alert đúng loại). Output: `demos/demo-lap-hop-dong-mua.html` + index README. **Cập nhật 2026-07-14 (Task 11):** đảo logic — 1 mã hàng phục vụ nhiều phiếu đề xuất/KH nay **GỘP về 1 dòng** (mô hình `purposes[]`, ô "Mục đích mua" ghép nhiều phiếu, SL đề xuất/đặt mua cộng dồn); modal Chọn hàng hóa thêm mã đã có → cộng dồn không tạo dòng trùng. Verify Playwright PASS (CEA 1 dòng SL 14/13, tổng 185.150.000). (@khoipv) — 2026-07-13, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-13-lap-hop-dong-mua-design.md`
  - Plan chi tiết (11 task): `docs/superpowers/plans/2026-07-13-lap-hop-dong-mua.md`

- **BC bảo lãnh — chế độ xem theo cập nhật mới nhất** — Màn `contract/reports/guarantee_contract`: checkbox "Xem theo cập nhật mới nhất" trong bộ lọc → bảng chuyển dạng PHẲNG từng dòng bảo lãnh sort theo lần lưu tab bảo lãnh (dự thầu/thực hiện HĐ) gần nhất, không gom KH (cùng KH tách nhiều hàng); cột mới "Thời gian cập nhật" (sau Tên KH, chỉ chế độ mới); Excel theo chế độ đang xem. Cơ chế: lưu tab bảo lãnh là xóa-tạo-lại → `updated_at` = lần lưu cuối, KHÔNG migration. BE: param `view_mode=latest_update` trên `GET category/reports/guarantees` — `ReportService` bỏ groupBy + sort updated_at DESC/id DESC, resource phẳng mới `ReportGuaranteeFlatResource`, response mặc định nguyên vẹn, filter + phân quyền 3 cấp dùng chung closure. FE: 1 file `index.vue` (checkbox + buildRequestParams/buildFlatRows + template v-if + columnCount computed 25/26 sửa luôn bug lệch 24 + colspan Tổng + Excel splice cột 4/dịch numFmt indices). Thực thi subagent-driven 7 task mỗi task có review + final review Opus READY TO COMMIT. **E2E PASS** (save tab bảo lãnh HD-162/2026 → lên đầu 17:03; chế độ cũ không regression; Excel 2 chế độ parse đúng 26/25 cột; log BE sạch). Minor tồn: race hiếm khi toggle lúc request in-flight; N+1 find theo pattern cũ. CHƯA commit. (@khoipv) — 2026-07-09, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat-design.md`
  - Plan chi tiết (7 task): `docs/superpowers/plans/2026-07-09-bc-bao-lanh-xem-theo-cap-nhat.md`
  - Design tóm tắt + Plan + Ledger: `.plans/bc-bao-lanh-xem-theo-cap-nhat/design.md` · `plan.md` · `progress-ledger.md`

- **Đẩy trả báo giá / gói thầu về phòng trước** — Màn `contract/quotation_render` + `contract/bid_package_render`: nút "Đẩy trả" (quyền `Phân công hợp đồng` HOẶC `Lập hợp đồng`, bắt buộc nhập lý do). Báo giá 9→1 (group null, dự toán →6 'Kế hoạch'); gói thầu 4→2 (group null, dự toán →11 'Thầu', BG nguồn 18→8 'Thầu' khi project_type=1, TODO multi-quotation). 3 cột mới `return_reason/returned_by/returned_at` trên 2 bảng (migration ĐÃ CHẠY, không FK); banner đỏ ở chi tiết, tự clear khi gửi duyệt lại (BG→2, GT→3); lịch sử `HistoryApproved*` giữ vĩnh viễn; notification cho người tạo BG / NV thực hiện GT. Phân công NV phụ trách HĐ giữ nguyên. BE: `canReturnRender()` 2 entity + 2 route PUT `return-render` + controller/service (GT dùng gán trực tiếp + save vì `group_process` không fillable) + 4 resource. FE: nút+modal 2 màn render, banner 2 trang chi tiết. Thực thi subagent-driven 7 task, mỗi task có review. **E2E PASS** (BG-331 + GT-336, edge: 400 sai status/không quyền, 422 reason trống, log sạch). Minor tồn: reason chưa escape trong title HTML notification (pattern giống rejectBid); 3 cột return client-writable qua PUT update chung. CHƯA commit (đã stage). (@khoipv) — 2026-07-09, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-09-day-tra-bao-gia-goi-thau-design.md`
  - Plan chi tiết (7 task): `docs/superpowers/plans/2026-07-09-day-tra-bao-gia-goi-thau.md`
  - Design tóm tắt + Plan tổng quát: `.plans/day-tra-bao-gia-goi-thau/design.md` · `plan.md`

- **Gói thầu gộp nhiều báo giá (cùng KH)** — Cho phép 1 gói thầu tạo từ NHIỀU báo giá cùng khách hàng (hiện khóa 1 gói thầu ↔ 1 báo giá qua `bid_packages.quotation_id`). Chốt: khác dự toán được, KHÔNG có báo giá chính (ngang hàng), chọn multi trong form thêm gói thầu; tính "nhiều báo giá" chỉ ở khâu gói thầu — thầu→HĐ giữ logic cũ, đường ngoài thầu (báo giá→HĐ) giữ 1-1. Mô hình: bảng nối mới `bid_package_quotations` (không FK, không is_primary), `bid_packages.quotation_id/project_id`=NULL khi gộp; HĐ từ gói thầu gộp `quotation_id`=NULL nối qua `bid_package_id`. **Đánh giá lại 2026-07-08 (quét code 3 agent)**: vòng đời phải lặp N ở 6 điểm; sửa 3 kết luận sai nhóm "không sửa"; thêm dashboard/filter/reverse-resource; chốt đủ 8 quyết định (append tách nhóm + badge; price_type khác → trống + cảnh báo; backfill CÓ; ContractAssignEmployee.quotation_id=NULL; sửa 🟠 1 đợt). **ĐÃ CODE XONG BE+FE 2026-07-08**: 2 migration ĐÃ CHẠY (bảng nối backfill 81/81 + cột truy nguồn `quotation_id` trên bid_package_groups/products); Service 6 điểm vòng đời + syncQuotations/sourceQuotations; 4 Resource; related-data 3 màn; 6 report + dashboard + filter; FE modal multi-select + chips + badge + append. **Verify UI PASS các nhánh chính** (tạo gộp GT-354/355: 2 BG 7→11→8, 2 DT →11; xóa revert 7/10; chặn khác KH; related-data 3 chiều; danh sách N mã; fix kèm: thêm `customer_id` vào QuotationResource). E2E còn lại (phân công HĐ / kết xuất / hủy / HĐ từ gói gộp / report với data gộp) đã hoàn tất. (@khoipv) — 2026-07-07, code 2026-07-08, HOÀN THÀNH 2026-07-09
  - Spec: `docs/superpowers/specs/2026-07-07-bid-package-multi-quotation-design.md`
  - Design + Plan: `.plans/bid-package-multi-quotation/design.md` · `plan.md`

- **Phụ lục thay đổi điều khoản thanh toán** — Loại phụ lục HĐ thứ 7 (`annex_type='change_payment_terms'`), nhân bản slice `contract_annex_time`. Lập/duyệt/in chứng từ đổi bộ điều khoản thanh toán (bảng 4 điều khoản `contract_payment_terms` + `payment_terms_note`) của HĐ đã duyệt. Khi duyệt: ghi đè điều khoản live + note + nhúng snapshot version mới + `ContractChange`. Giữ nút sửa inline sẵn có. Có In bảng động Cũ→Mới. Form 1 bảng mới (prefill hiện tại, tái dùng `PaymentTermsTab.vue`). Chỉ HĐ status=3. Không migration, tái dùng quyền "Lập/Duyệt hợp đồng". Không đụng `syncPaymentTerms` gốc. BE mới: Service+Controller+Request+DetailResource+routes; sửa `ANNEX_TYPE_LABELS`. FE mới bộ trang `contract_annex_payment_terms/`; sửa 3× ROUTE_MAP + API_MAP + option approve.vue + menu. Fix bổ sung: `mt-3` header–tabs; fix crash chi tiết (`formSubmit.contract={}`); `ContractDetailResource` đọc `payment_terms`/`payment_terms_note` từ snapshot v0 (fallback live); đăng ký 4 biến mẫu in (`NGAY_LAP`, `BANG_DIEU_KHOAN`, `GHI_CHU_CU`, `GHI_CHU_MOI`); chặn tạo phụ lục khi HĐ đang có phụ lục dở (filter `exclude_in_progress_annex` cho cả 8 màn). (@khoipv) — 2026-07-07, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-07-contract-annex-payment-terms-design.md`
  - Design + Plan: `.plans/contract-annex-payment-terms/design.md` · `plan.md`

- **Thông báo dự toán chờ phân công sắp hết hạn** — Màn Dự toán (`sale/project`): Console Command mới `projects:notify-assignment-due` chạy dailyAt 07:00, quét dự toán status=2 (Chờ phân công) còn ≤2 ngày làm việc là tới `expected_time` → gửi thông báo cho tất cả người có quyền `'Phân công báo giá'` (dùng `listEmployeeInfoByPermission` + `sendToAllContractNotification`, `Carbon::diffInWeekdays` trừ T7/CN). Không gửi cuối tuần/quá hạn. Chỉ BE, không FE/migration. (@khoipv) — 2026-07-06, HOÀN THÀNH
  - Spec: `docs/superpowers/specs/2026-07-06-notify-project-assignment-due-design.md`
  - Design + Plan: `.plans/notify-project-assignment-due/design.md` · `plan.md`

- **Giữ lọc màn bid_package/dashboard + contract/dashboard (tham chiếu plan/dashboard)** — Cơ chế giữ lọc dashboard nằm trong 3 card dùng chung (`FilterPieChartCard/LineChartCard/ColumnChartCard`), lưu localStorage qua `utils/dashboard-chart-filter.js` theo prop `module`. `BidPackageDashboard.vue` & `ContractDashboard.vue` đã có `module` nên đã lưu, nhưng thiếu/sai prop mapping so với `PlanDashboard.vue` (chuẩn) → khôi phục lọc không map lại được id. Fix FE 2 file: Pie đổi `region-mapping`→`area-mapping`; Column thêm `status-options`/`status-mapping`/`area-mapping`. (@khoipv) — 2026-07-06, HOÀN THÀNH (verify UI PASS)
  - Plan: `.plans/bid-package-dashboard-giu-loc/plan.md`

- **Khách hàng sử dụng cuối cùng — chọn nhiều (BG/HĐ/Gói thầu)** — Trường "Khách hàng sử dụng cuối cùng" từ chọn 1 → chọn nhiều ở cả 3 module (`quotations`, `contracts`, `bid_packages`). Lưu cột JSON `customer_last_used` (mảng `[{id,name}]`) làm nguồn chính; giữ cột cũ `customer_last_used_name` = tên nối `", "` (list/report/export không phải sửa) + `customer_last_used_id` = id phần tử đầu. UI chip/tag, tái dùng `CustomerModal` single-pick append + dedupe theo id. Auto từ dự toán: `addProject` đẩy khách hàng chính vào mảng (xóa được). BE dùng **mutator** trên Entity tự đồng bộ 2 cột cũ (khỏi sửa service store/update). (@junfoke) — 2026-07-08, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-07-khach-hang-cuoi-cung-chon-nhieu-design.md`
  - Design tóm tắt + Plan: `.plans/khach-hang-cuoi-cung-chon-nhieu/design.md` · `plan.md`

- **Giữ bộ lọc khi rời trang — 4 phân hệ (Danh mục/Kinh doanh/Kế hoạch/Quản lý thầu)** — Rà soát toàn bộ màn danh sách, chuẩn hoá giữ bộ lọc + trang phân trang khi vào chi tiết rồi back (tham chiếu `plan/quotation`, mixin `searchMixinPlugin.js`). Phạm vi: 8 màn (sale/assign-kpi, sale/register-kpi, sale/report-project-contract, sale/detail-report, plan/detail-report, bid_package/detail-report, category/customer_handover, customer_handover/waiting-approve) + fix trùng `localStorageKey` của plan/project & bid_package/project. Bỏ ~24 danh mục con Category (CRUD modal, không rời trang). Chỉ FE. (@khoipv) — 2026-07-04, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-04-giu-loc-danh-sach-design.md`
  - Design + Plan: `.plans/giu-loc-danh-sach/design.md` · `plan.md`

- **Thêm cột "Ghi chú báo giá" + "Ghi chú thầu" + đổi tên "Ghi chú hợp đồng" — màn hợp đồng** — Màn `contract/contract/add` (dùng chung edit/detail qua `GeneralComponent`): thêm 2 cột read-only `note_quotation` ("Ghi chú báo giá", lấy từ note báo giá) + `note_bid_package` ("Ghi chú thầu", lấy từ `bid_package_products.note`), đổi label cột `note` hiện tại → "Ghi chú hợp đồng" (giữ sửa được). BE: migration `contract_products` thêm 2 cột (text, không FK, ĐÃ CHẠY) + `ContractProduct::$fillable`. FE: `ProductComponent.vue` (columns + template read-only + width + export Excel + import preserve), `GeneralComponent.vue` (`addNegotiation` map ghi chú theo `data.type`: thầu→note_bid_package, báo giá→note_quotation, note HĐ để trống). Quyết định chờ user xác nhận: để trống "Ghi chú hợp đồng" khi tạo từ nguồn. (@khoipv) — 2026-07-03, HOÀN THÀNH (verify UI PASS)
  - Plan: `.plans/contract-quotation-bid-note-columns/plan.md`

- **Thêm cột "Ghi chú báo giá" + đổi tên "Ghi chú thầu" — màn gói thầu** — Màn `bid_package/bid_package/add`: thêm cột mới `note_quotation` (label "Ghi chú báo giá", read-only, lấy từ trường note bên báo giá, lưu DB) + đổi label cột `note` hiện tại thành "Ghi chú thầu" (tạo từ báo giá thì để trống). BE: migration thêm cột `note_quotation` (không FK) + fillable. FE: `ProductComponent.vue` (fields + template + export Excel), `GeneralComponent.vue` (`addQuotation` map note→note_quotation, note=''). (@khoipv) — 2026-07-03, HOÀN THÀNH (verify UI PASS)
  - Plan: `.plans/bid-package-quotation-note-column/plan.md`
- **Báo cáo bán hàng theo mặt hàng** — Báo cáo dạng cây 3 cấp gom theo mặt hàng (Hàng hoá › Khách hàng › Luồng bán hàng) theo mẫu `bc_banhang_theo_mathang.html`, UI đồng bộ `sale/report-project-contract`. 4 giai đoạn BG→Thầu→HĐ→Thực xuất (Thực xuất để trống). 1 quyền `Xem báo cáo bán hàng theo mặt hàng`, không lọc theo cấp, loại HĐ hủy. BE: `ProjectController@saleProductReport` (`category/projects/reports/sale-product`) dựng cây + show-once BG/Thầu, dùng snapshot `contract_products`; đã verify tinker (707 MH, KPI đúng). FE: trang `pages/contract/reports/sale-product/index.vue` (KPI, filter, cây collapse, drill-down mở thẳng chi tiết DT/BG/GT/HĐ, xuất Excel). Menu gắn `isShow`. (@khoipv) — 2026-07-02, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-02-bc-ban-hang-theo-mat-hang-design.md`
  - Plan chi tiết (7 task): `docs/superpowers/plans/2026-07-02-bc-ban-hang-theo-mat-hang.md`
  - Design tóm tắt + Plan tổng quát: `.plans/bc-ban-hang-theo-mat-hang/design.md` · `plan.md`
- **Thanh lý HĐ — Giá trị thực tế & chặn thanh lý** — Thêm ô "Giá trị thực tế" (bắt buộc) vào biên bản thanh lý (`contract/contract_liquidation`, Bước 2). So sánh với số tiền đã nghiệm thu lũy kế (`summary.total_performed`): chưa có BBNT đã duyệt (`bbnt_list.length=0`) → bỏ qua; đã có ≥1 BBNT → nếu `total_performed < actual_value` thì chặn lập/lưu (strict less-than). Lưu cột mới `actual_value`, hiển thị lại ở chi tiết/duyệt. Chặn ở mọi nút lưu (nháp + gửi/duyệt), enforce cả FE + BE (guard trong Service). Bổ sung: chặn cả khi DUYỆT (Controller approve bọc try/catch + Service guard tươi + FE chặn sớm). Giữ cho phép actual_value=0. (@khoipv) — 2026-07-01, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-07-01-contract-liquidation-actual-value-design.md`
  - Design tóm tắt + Plan: `.plans/contract-liquidation-actual-value/design.md` · `plan.md`

- **BBNT lấy đơn giá theo product_id + unit_id** — Sửa lỗi BBNT lấy nhầm đơn giá khi cùng 1 mặt hàng nằm trong HĐ ở nhiều ĐVT/giá khác nhau (vd product 26: Hộp @1.500.000 và mL @30.000) → màn chi tiết hiển thị MAX(price)=1.5tr cho cả dòng mL, còn tổng đã lưu tính theo 30k → chi tiết ≠ danh sách (report 23 lệch 5.880.000). Khóa giá/SL theo `product_id+unit_id`: BE `productQtyMap` groupBy product+unit, thêm `productPriceByUnit`+`resolvePriceName` (fallback product_id), `saveItems`/`saveInvoiceBlocks` lưu `unit_id`, resource trả `unit_id`; **migration thêm cột `unit_id`** (không FK, đã chạy). FE: `AcceptanceReportForm` tra meta theo pid|unit; `ProductGrid`/`FormByMonth`/`FormByInvoiceDetail` prefill khớp pid|unit (fallback pid) + gửi `unit_id` + consumedBefore theo unit. (@khoipv) — 2026-06-30, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-06-30-acceptance-report-price-by-unit-design.md`
  - Design tóm tắt + Plan: `.plans/acceptance-report-price-by-unit/design.md` · `plan.md`

- **Cho phép trùng hàng hóa — NT theo tháng (BBNT)** — Loại "Theo tháng" (`FormByMonth.vue`) cho chọn lặp lại cùng mặt hàng (cùng hàng ở nhiều hóa đơn khác nhau). FE: bỏ loại trừ ở popup + bỏ dedup khi push → mỗi confirm thêm dòng mới; mỗi dòng có `uid` riêng (đổi `:key`); "Còn lại"/"Đã NT" **trừ dần theo dòng** (`consumedBefore`/`rowEffNt`/`rowRemain`/`isOver`, giống FormByInvoiceDetail). **Trùng theo cặp (mặt hàng + số hóa đơn)** chỉ trong cùng biên bản: 2 hàng khác nhau dùng chung 1 số HĐ OK, chỉ chặn cùng hàng+cùng số HĐ lặp (`dupPairSet`/`isDupRow`/`dupMsg`/`hasDupError`); cross-report giữ khóa theo số HĐ. BE: `assertNoDuplicateInvoiceNumbers` đổi dupSelf sang cặp cho `TYPE_THANG` (+ helper `duplicateProductInvoiceNos`), cross-report & loại khác giữ nguyên. (@khoipv) — 2026-06-30, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-06-30-acceptance-report-month-duplicate-goods-design.md`
  - Design tóm tắt + Plan: `.plans/acceptance-report-month-duplicate-goods/design.md` · `plan.md`

- **Tự gắn hàng hóa từ HĐ liên quan vào danh sách KPI — màn HĐ add/edit** — Khi `has_kpi == 1` VÀ đã chọn "Hợp đồng liên quan" → tự động lấy hàng hóa thường (`groups`) của HĐ liên quan, giữ nguyên cấu trúc nhóm, giá/SL theo HĐ liên quan, **thêm vào cuối** `group_kpis`. Đổi HĐ liên quan nhiều lần → cộng dồn. Bỏ chọn HĐ liên quan / tắt KPI → tự gỡ nhóm đã gắn (cờ `from_related_contract`), giữ nhóm tự thêm. Thuần FE, tái dùng `GET category/contracts/{id}`, không sửa BE. Sửa `GeneralComponent.vue` (dùng `@input` thay watch — BaseSelect2 chỉ emit input khi user thao tác, tránh kích hoạt khi edit nạp dữ liệu). (@khoipv) — 2026-06-30, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-06-30-contract-kpi-autofill-from-related-design.md`
  - Design tóm tắt + Plan: `.plans/contract-kpi-autofill-from-related/design.md` · `plan.md`

- **Bôi đỏ tiêu đề tab có lỗi validate — màn HĐ add/edit** — Khi submit thiếu trường bắt buộc (BE trả 422), bôi đỏ tiêu đề tab chứa lỗi để user biết tab nào cần sửa. Sửa `pages/contract/contract/components/GeneralComponent.vue` (dùng chung add + edit): thêm 4 computed (`hasErrorInGeneralTab`, `hasErrorInProgressTab`, `hasErrorInGuaranteeTab`, `hasErrorInPaymentTab`), bổ sung `group_kpis` vào `hasErrorInProductTab` có sẵn; đổi title 4 tab (Thông tin chung, Tiến độ thực hiện, Bảo lãnh, Điều khoản thanh toán) sang slot `#title` + `text-danger`. Chỉ FE. (@khoipv) — 2026-06-30, HOÀN THÀNH (verify UI PASS)
  - Plan: `.plans/contract-add-tab-error-highlight/plan.md`

- **Chọn trường & loại giá khi xuất Excel — màn Quản lý giá hàng hóa** — Bổ sung modal cho màn `category/product_unit_price`: bấm "Xuất excel" mở modal 2 mục (Chọn trường thông tin: 10 trường / Chọn loại giá: Giá vốn + price_types động), mỗi mục Select2 multiple + "Chọn tất cả", mặc định tích hết, validate ≥1 mỗi mục. `generateWorkbook` dựng cột động theo lựa chọn, vẫn xuất FE bằng ExcelJS, tôn trọng bộ lọc hiện tại. Chỉ FE, không đổi BE. (@khoipv) — 2026-06-29, HOÀN THÀNH (verify UI PASS)
  - Spec: `docs/superpowers/specs/2026-06-29-product-unit-price-export-fields-design.md`
  - Plan chi tiết (5 task): `docs/superpowers/plans/2026-06-29-product-unit-price-export-fields.md`
  - Design tóm tắt + Plan tổng quát: `.plans/product-unit-price-export-fields/design.md` · `plan.md`
- **Demo "Tạo đề xuất nhập hàng" (prototype)** — File demo HTML standalone cho màn tạo đề xuất nhập hàng, 3 loại (① Theo HĐ bán đã duyệt — BGĐ duyệt; ② Mua khác — lý do mua; ③ Mua hàng tồn kho NK/PPL — nước NK + kho đích + hạn dùng). Theo style `bbnt_demo (2).html`: wizard 3 bước, modal chọn hàng từ danh mục, cảnh báo (không chặn) khi L1 vượt SL còn lại. **Không nhập giá, không chọn NCC**; footer theo số mặt hàng + tổng SL. Output: `demos/demo-tao-de-xuat-nhap-hang.html`. (@khoipv) — 2026-06-26
  - Spec: `docs/superpowers/specs/2026-06-25-purchase-proposal-demo-design.md`
  - Design tóm tắt + Plan: `.plans/purchase-proposal-demo/design.md` · `plan.md`

- **Lọc Hãng/nước SX — màn detail-report** — Thêm bộ lọc "Hãng, nước sản xuất" (dropdown chọn 1) vào màn `plan/detail-report`. Lọc báo giá có dòng hàng thuộc hãng/nước được chọn qua `whereExists` trên `quotation_tab_products.producer_country`. Dropdown lấy danh mục `producer_countries` (thêm param `all` bỏ lọc created_by). Export Excel tự hưởng filter. Không migration. (@khoipv) — 2026-06-26
  - Spec: `docs/superpowers/specs/2026-06-25-detail-report-producer-country-filter-design.md`
  - Design tóm tắt + Plan: `.plans/detail-report-producer-country-filter/design.md` · `plan.md`

- **Thanh lý hợp đồng — build thật (BE + FE)** — Xây màn Biên bản thanh lý hợp đồng: chứng từ lưu DB có duyệt (CRUD giống BBNT), 1 thanh lý/HĐ, gom BBNT đã duyệt → 3 tab (Tổng hợp hóa đơn có nhập tay thanh toán + Chi tiết hóa đơn + Tổng hợp hàng hóa), snapshot khi lưu. 4 bảng (không khóa ngoại), 2 quyền mới (id 509/510), HĐ không đổi trạng thái. BE: migration + 4 entity + service (buildAggregation + CRUD) + request + controller (transaction) + 2 resource + routes (9). FE: helpers + menu + list + approve + form + Summary + Tabs. Đồng bộ UI theo BBNT (Phase 4–5), chặn trùng số hóa đơn (Phase 6), bổ sung cột hàng hóa, cập nhật bổ sung ngày+file (Phase 7), validate ngày thanh lý + base components (Phase 9). Excel/In để sau. (@khoipv) — 2026-06-25, verify UI PASS
  - Spec build: `docs/superpowers/specs/2026-06-24-contract-liquidation-design.md`
  - Plan chi tiết (11 task): `docs/superpowers/plans/2026-06-24-contract-liquidation.md`
  - Spec prototype: `docs/superpowers/specs/2026-06-22-contract-liquidation-demo-design.md`
  - Design tóm tắt + Plan tổng quát: `.plans/contract-liquidation/design.md` · `plan.md`

- **Từ chối lập gói thầu** — Bổ sung chức năng từ chối lập gói thầu trên màn `bid_package/quotation` (báo giá đã gửi thầu, status=7). Quyền "Lập gói thầu" mới được từ chối, bắt buộc nhập lý do; báo giá → status 20, dự toán → status 19 (cùng nhãn "Từ chối lập gói thầu"). Không migration (tái dùng `reason_deny`). (@khoipv) — 2026-06-23, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-23-bid-package-quotation-reject-design.md`
  - Plan chi tiết: `docs/superpowers/plans/2026-06-23-bid-package-quotation-reject.md`
  - Design tóm tắt: `.plans/bid-package-quotation-reject/design.md`
  - Plan tổng quát: `.plans/bid-package-quotation-reject/plan.md`

- **Biên bản nghiệm thu (BBNT) — đợt 2: cập nhật theo demo (2)** — Khớp màn thêm/sửa BBNT với `bbnt_demo (2).html`: (1) Bước 1 thêm dropdown Khách hàng (cascade KH→HĐ→Loại) + tiêu đề/hint "chỉ HĐ do bạn lập"; (2) ContractSummary thêm địa bàn (`customer_area_name`) + "lần nghiệm thu kế tiếp"; (3) Form Theo tháng thêm sub-tab "Tổng hợp (gộp hàng nhiều HĐ)"; (4) Form cthd **bỏ** tab Tổng hợp. BE: `selectableContracts` select thêm customer_id/customer_name (không migrate). FE 6 file. (@khoipv) — 2026-06-19, verify UI PASS
  - Spec gốc: `docs/superpowers/specs/2026-06-16-acceptance-report-add-design.md`
  - Spec đợt 2: `docs/superpowers/specs/2026-06-19-acceptance-report-add-demo2-changes-design.md`
  - Plan: `.plans/acceptance-report-add/plan.md` (Phase 10)

- **BBNT — bổ sung nhỏ (Phase 11 + 12)** — (11) Thêm hiển thị "Tổng hóa đơn" (read-only) lên header mỗi block loại "chi tiết từng hóa đơn". (12) Chức năng "Cập nhật bổ sung": sửa Ngày biên bản + bảng File lưu trữ (Tên tài liệu/File/Ghi chú) ở **mọi trạng thái** qua endpoint riêng `updateSupplement` (pattern "Tiến độ thực hiện" màn HĐ), chỉ owner/người có quyền duyệt; bảng mới `acceptance_report_files` (không khóa ngoại) + component `SupplementUpdate.vue`. (@khoipv) — 2026-06-22, verify UI PASS
  - Spec 11: `docs/superpowers/specs/2026-06-22-acceptance-report-invoice-total-header-design.md`
  - Spec 12: `docs/superpowers/specs/2026-06-22-acceptance-report-supplement-update-design.md`
  - Plan 12 chi tiết: `docs/superpowers/plans/2026-06-22-acceptance-report-supplement-update.md`
  - Plan tổng quát: `.plans/acceptance-report-add/plan.md` (Phase 11, 12)

- **Cột "Số hóa đơn" — Nội dung công tác phí** — Thêm cột text `invoice_number` (không bắt buộc) vào bảng Nội dung công tác phí màn `timesheet/request-payment-working-fee`, sau cột "Nội dung", cả người tạo & người duyệt sửa được. BE: migration + 3 chỗ create trong service + resource. FE: `RequestPaymentWorkingFeeForm.vue` (header + input + default + colspan). (@khoipv) — 2026-06-18, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-18-working-fee-invoice-number-column-design.md`
  - Plan: `.plans/working-fee-invoice-number-column/plan.md`

- **In phiếu đề nghị thanh toán công tác phí** — Trang in mới `_id/print.vue` theo mẫu "GIẤY ĐỀ NGHỊ THANH TOÁN": header 2 cột (công ty/tỉnh theo người tạo) → người đề nghị → lặp từng phiếu công tác (bảng đủ cột đề xuất + duyệt + số hóa đơn) → bảng tổng hợp → lý do trễ hạn → khối ký. BE: thêm block `requester` vào `DetailRequestPaymentWorkingFeeResource`. FE: **modal popup** `components/modal/RequestPaymentWorkingFeePrintModal.vue` (giống `BusinessTripDecisionPrintModal`), mở từ dropdown danh sách; nút In dùng window.open + print. (@khoipv) — 2026-06-18, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-18-request-payment-working-fee-print-design.md`
  - Plan: `.plans/request-payment-working-fee-print/plan.md`

- **Biên bản nghiệm thu (BBNT) — màn thêm mới + Backend CRUD** — FE `pages/contract/acceptance_report/add.vue` wizard 3 bước, đủ 5 loại NT, UI lai, chia nhiều component con. BE đầy đủ (Modules/Category): 3 bảng + entities + service CRUD + meta (lần kế tiếp/loại được phép/lũy kế) + duyệt/từ chối + auto code. Quy tắc khóa loại **tonghd-sticky**. FE đã nối API thật (meta + submit + khóa loại). Đã có đủ **danh sách + thêm + chi tiết + sửa + duyệt/từ chối/xóa** (wizard tách `AcceptanceReportForm` dùng chung create/edit/show, prefill + readonly). type & hien_trang lưu integer. Migrate + route:list OK. (@khoipv) — 2026-06-18, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-16-acceptance-report-add-design.md`
  - Plan: `.plans/acceptance-report-add/plan.md`
- **In QUYẾT ĐỊNH cử đi công tác (Business Trip)** — Đổi bản in màn `timesheet/business_trip_assigns/:id/print` từ "GIẤY ĐI ĐƯỜNG" sang "QUYẾT ĐỊNH cử người lao động đi công tác" (copy mẫu từ `jobassignment/_id/print.vue`). 1 QĐ liệt kê tất cả NV. BE thêm field `employee_account_id`; FE viết lại template+script `print.vue`. (@khoipv) — 2026-06-16, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-16-business-trip-print-design.md`
  - Plan: `docs/superpowers/plans/2026-06-16-business-trip-print.md`
  - Plan tổng quát: `.plans/business-trip-print/plan.md`

- **In phiếu giao việc** — Đổi bản in màn `timesheet/jobassignment/:id/print` từ "GIẤY ĐI ĐƯỜNG" sang "QUYẾT ĐỊNH cử người lao động đi công tác" theo mẫu Word (chỉ trang 1). 1 bản QĐ liệt kê tất cả NV, header 2 cột text, Điều 1 dạng đoạn văn, không số QĐ. Chỉ sửa FE `print.vue`. (@khoipv) — 2026-06-15, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-15-in-quyet-dinh-cong-tac-phi-design.md`
  - Plan: `docs/superpowers/plans/2026-06-15-in-quyet-dinh-cong-tac-phi.md`
  - Plan tổng quát: `.plans/in-quyet-dinh-cong-tac-phi/plan.md`

- **Duyệt HĐ "Không thực hiện" → Hủy hợp đồng** — TP bấm Duyệt HĐ có `result=2` → HĐ chuyển trạng thái mới "Hủy hợp đồng" (Contract `HUY=5`) + đẩy dự toán/báo giá/gói thầu sang trạng thái mới "Hủy hợp đồng" (const mới mỗi entity) + ghi lịch sử kèm lý do. Tái dùng nút Duyệt, không snapshot. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-10-contract-cancel-not-executed-on-approve-design.md`
  - Plan: `.plans/contract-cancel-not-executed-on-approve/plan.md`

- **Bỏ validate khi hợp đồng "Không thực hiện"** — Khi tạo/sửa HĐ (từ gói thầu/báo giá) chọn `result = 2` (Không thực hiện) → bỏ TẤT CẢ validate, chỉ bắt buộc `reason`. Áp dụng FE + BE, tạo mới + cập nhật. `result = 1`/trống → validate đầy đủ như cũ. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-10-contract-not-executed-skip-validate-design.md`
  - Plan: `.plans/contract-not-executed-skip-validate/plan.md`

- **Ghi chú + Lưu-sau-duyệt tab Điều khoản thanh toán** — Thêm 1 ô ghi chú chung cho tab Điều khoản thanh toán (cột `payment_terms_note` trên `contracts`) + nút Lưu mở khóa & lưu cả bảng + ghi chú khi HĐ đã duyệt (endpoint mới `updatePaymentTermsAfterApprove`, tái dùng `syncPaymentTerms`). Chỉ form `contract/contract`. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-09-contract-payment-terms-note-approve-design.md`
  - Plan: `.plans/contract-payment-terms-note-approve/plan.md`

- **Bắt buộc field khi gửi duyệt gói thầu lên TP** — Bắt buộc `bid_opening_time`, `bid_closing_time`, `execution_time` (numeric>0), `execution_time_unit` khi nhân viên bấm "Gửi duyệt" (status=3) trong `StoreBidPackageRequest`. Lưu nháp/Lưu và gửi vẫn để trống được. (@khoipv) — 2026-06-08
  - Spec: `docs/superpowers/specs/2026-06-08-bid-package-send-approve-required-fields-design.md`
  - Plan: `.plans/bid-package-send-approve-required-fields/plan.md`

- **Đồng bộ thông tin hợp đồng gốc xuống phụ lục** — Sửa số HĐ / ngày ký / ngày kết thúc / thời gian thực hiện ở hợp đồng gốc (màn 203, sau duyệt) → đồng bộ 4 trường vào TẤT CẢ snapshot `ContractVersion` để mọi phụ lục hiển thị giá trị mới. BE sửa `updateDataAfterApprove` (bọc transaction); FE gửi thêm `time_progress`. (@khoipv) — 2026-06-08
  - Spec: `docs/superpowers/specs/2026-06-08-dong-bo-thong-tin-hop-dong-xuong-phu-luc-design.md`
  - Plan: `.plans/dong-bo-thong-tin-hop-dong-xuong-phu-luc/plan.md`

- **Tab "Phụ lục liên quan" — Chi tiết hợp đồng** — Điền tab rỗng trong màn chi tiết/sửa HĐ bằng bảng phụ lục (STT, Mã PL, Loại PL, Trạng thái); mã PL click → chi tiết đúng loại, trạng thái badge màu. BE: thêm `annexes` + `annex_type_label` vào `ContractDetailResource`. (@khoipv) — 2026-06-03
  - Spec: `docs/superpowers/specs/2026-06-03-contract-detail-related-annex-tab-design.md`
  - Plan: `.plans/contract-detail-related-annex-tab/plan.md`

- **Cột "Phụ lục liên quan" — Danh sách hợp đồng** — Thêm cột hiển thị mọi mã phụ lục của hợp đồng (mỗi mã 1 dòng, mọi trạng thái), click → chi tiết phụ lục đúng loại qua `ANNEX_TYPE_ROUTE_MAP`. BE: relation `Contract::annexes` + eager load + expose ở `ContractResource`. (@khoipv) — 2026-06-03
  - Spec: `docs/superpowers/specs/2026-06-02-contract-list-related-annex-column-design.md`
  - Plan: `.plans/contract-related-annex-column/plan.md`

- **Popup DT gom hàng hóa 4 phân hệ + quy đổi ĐVT** — Enhancement cho report-project-contract: popup chi tiết DT hiển thị tất cả HH từ DT/BG/Thầu/HĐ, thêm 3 cột SL quy đổi về ĐVT chính (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-29-lifecycle-detail-aggregate-products-design.md`
  - Plan: `.plans/report-project-contract/plan.md`

- **Sửa BCCT báo giá — mỗi báo giá 1 dòng** — Đổi plan/detail-report từ mỗi hàng hóa 1 dòng sang mỗi báo giá 1 dòng + popup chi tiết sản phẩm (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-28-detail-report-quotation-summary-design.md`
  - Plan: `.plans/detail-report-quotation-summary/plan.md`

- **Báo cáo chi tiết hợp đồng** — Báo cáo tổng hợp sản phẩm từ nhiều hợp đồng (27 cột, 8 filters, phân quyền 3 cấp, export Excel) (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-06-detail-report-contract-design.md`
  - Plan: `.plans/detail-report-contract/plan.md`

- **Tab Dữ liệu liên quan trên báo giá** — Thay tab input thủ công bằng tab read-only tự động lấy chứng từ liên quan (Dự toán/Thầu/Hợp đồng) qua endpoint BE mới `GET /quotations/{id}/related-data` + component `QuotationRelatedDataComponent.vue` (@khoipv) — 2026-05-25
  - Spec: `docs/superpowers/specs/2026-05-25-quotation-related-data-design.md`
  - Plan: `.plans/quotation-related-data/plan.md`

- **BC Tổng hợp Vòng đời DT → HĐ** — Báo cáo tổng hợp 1 dòng/DT, grouped headers 4 giai đoạn (DT/BG/GT/HĐ), KPI cards, popup drill-down, export Excel, phân quyền 3 cấp dùng lại bộ "Xem báo cáo chi tiết dự toán theo ..." (ID 504-506) (@khoipv) — 2026-05-27
  - Spec: `docs/superpowers/specs/2026-05-25-report-project-contract-design.md`
  - Plan: `.plans/report-project-contract/plan.md`

- **Tab Thuế TNCN lưu cả bảng 1 lần** — Thay pattern edit per-row bằng 1 nút Lưu chung dưới bảng trong tab Thuế TNCN của màn employee_info/edit, BE thêm endpoint bulk (@manhcuong) — 2026-05-26
  - Spec: `docs/superpowers/specs/2026-05-26-employee-tax-bulk-save-design.md`
  - Plan: `.plans/employee-tax-bulk-save/plan.md`

- **Tính Thuế TNCN trong bảng lương** — Áp biểu lũy tiến 7 bậc + đa-đoạn tax_type theo khoảng ngày + 3 cột giảm trừ INFO trên bảng lương. Config global (1 row dùng chung mọi company). Quy ước nội bộ KHÁC TT 111: (1) BHXH giảm trừ = NLĐ+NSDLĐ (32%) thay vì chỉ NLĐ; (2) đoạn 10%/20% dùng `probation_salary` (@manhcuong) — 2026-05-13, Phase 1-10 xong + verified, chờ E2E qua UI bảng lương thật
  - Spec: `docs/superpowers/specs/2026-05-13-personal-income-tax-design.md`
  - Plan: `.plans/personal-income-tax/plan.md`

- **Tab Dữ liệu liên quan trên dự toán** — Hiển thị chứng từ nghiệp vụ liên quan (Kế hoạch/Thầu/Hợp đồng) với mã chứng từ (link) + người thực hiện, endpoint BE mới + implement FE component (@khoipv) — 2026-05-25
  - Spec: `docs/superpowers/specs/2026-05-25-project-related-data-design.md`
  - Plan: `.plans/project-related-data/plan.md`

- **Mẫu in riêng cho hợp đồng lao động** — Mỗi HĐLĐ lưu bản mẫu in riêng (longText) thay vì FK dùng chung. FE 2 tab + CKEditor. Migration backfill data cũ. (@khoipv) — 2026-05-23
  - Spec: `docs/superpowers/specs/2026-05-22-employment-contract-print-template-design.md`
  - Plan: `.plans/employment-contract-print-template/plan.md`

- **Bộ lọc ngân hàng thực hiện** — Thêm filter "Ngân hàng thực hiện" vào danh sách hợp đồng, lọc qua `whereHas('guarantees')` theo `bank_guarantee_id` (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-contract-bank-guarantee-filter-design.md`
  - Plan: `.plans/contract-bank-guarantee-filter/plan.md`

- **Bộ lọc kết quả thầu** — Thêm filter "Kết quả thầu" (Trúng/Trượt/Chưa có) vào màn danh sách gói thầu, lọc theo trường `result` trong bảng `bid_packages` (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-bid-package-result-filter-design.md`
  - Plan: `.plans/bid-package-result-filter/plan.md`

- **Thêm cột Sale phụ trách vào danh sách khách hàng** — Hiển thị tên Sale (dept 83) + mảng hàng hoá phụ trách từ tab Phân công phụ trách, eager load trong query list (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-sale-person-charge-column-design.md`
  - Plan: `.plans/sale-person-charge-column/plan.md`

- **Danh sách phụ lục chờ duyệt** — Trang gộp 6 loại phụ lục HĐ chờ duyệt vào 1 danh sách (API gộp BE + trang FE approve.vue) (@khoipv) — 2026-05-21
  - Spec: `docs/superpowers/specs/2026-05-21-contract-annex-approve-list-design.md`
  - Plan: `.plans/contract-annex-approve/plan.md`

- **Mở rộng mối quan hệ gia đình** — Thêm Ông, Bà, Khác (text tự do) vào dropdown mối quan hệ trong Thông tin gia đình, áp dụng 4 màn employee_info (@khoipv) — 2026-05-21
  - Spec: `docs/superpowers/specs/2026-05-21-family-relation-extend-design.md`
  - Plan: `.plans/family-relation-extend/plan.md`

- **Đính kèm file cho người thân** — Bổ sung chức năng upload/xóa file đính kèm (tối đa 5 file) cho từng thành viên gia đình trong Thông tin nhân sự, hỗ trợ cả flow yêu cầu cập nhật (@khoipv) — 2026-05-20
  - Spec: `docs/superpowers/specs/2026-05-20-family-attachment-design.md`
  - Plan: `.plans/family-attachment/plan.md`

- **Từ chối phân công dự toán** — Thêm chức năng từ chối phân công trên màn dự toán, nhập lý do, chuyển status = 17 (Hủy dự toán), trạng thái cuối cùng (@khoipv) — 2026-05-20
  - Spec: `docs/superpowers/specs/2026-05-20-reject-assignment-design.md`
  - Plan: `.plans/reject-assignment/plan.md`

- **Thêm cột KH sử dụng cuối cùng vào BCCT báo giá** — Thêm cột `customer_last_used_name` vào màn plan/detail-report (web + Excel) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-19-detail-report-customer-last-used-design.md`
  - Plan: `.plans/detail-report-customer-last-used/plan.md`

- **Hạn mức công nợ theo từng KH** — Chuyển hạn mức công nợ từ nhóm KH xuống từng khách hàng, xóa 2 cột khỏi customer_groups, thêm vào category_customers, dọn FE/BE (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`
  - Plan: `.plans/customer-group-credit-limit/plan.md`

- **Điều khoản thanh toán trên hợp đồng** — Thêm bảng điều khoản thanh toán (4 loại: 100% trước giao, giới hạn thời gian, giới hạn giá trị, gối đầu đơn hàng) vào tab "Cài đặt công nợ thanh toán" trong form HĐ (section 3 mock cảnh báo công nợ) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-18-contract-payment-terms-design.md`
  - Plan: `.plans/contract-payment-terms/plan.md`

- **Phiếu xác định & quy tắc xử lý vi phạm công nợ** — Cấu hình loại phiếu được tính là công nợ + hành động khi điều khoản bị vi phạm (mục 4 của mock cảnh báo công nợ) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-18-debt-violation-rules-design.md`
  - Plan: `.plans/debt-violation-rules/plan.md`

- **Hạn mức công nợ nhóm KH** — ~~Thêm 2 trường vào nhóm KH~~ → Đã thay thế bởi "Hạn mức công nợ theo từng KH" (2026-05-19) — chuyển hạn mức xuống cấp từng khách hàng (@khoipv) — 2026-05-18
  - Spec cũ: `docs/superpowers/specs/2026-05-18-customer-group-credit-limit-design.md`
  - Spec mới: `docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`

- **Giá bán HĐ trước** — Populate cột Giá bán HĐ trước bằng đơn giá bán từ HĐ gần nhất cùng KH, fallback cùng tỉnh. Áp dụng cho báo giá, gói thầu, hợp đồng. (@khoipv) — 2026-05-13
  - Plan: `.plans/previous-contract-price/plan.md`

- **Fix quy đổi giá khi thay đổi đơn vị tính** — Sửa lỗi giá không quy đổi theo conversion_factor khi đổi đơn vị ở gói thầu + hợp đồng + phân quyền bảng hàng hóa theo can_handle (@khoipv) — 2026-05-12
  - Plan: `.plans/fix-unit-price-conversion/plan.md`

- **Phụ lục thay đổi số lượng — 2 kiểu bảng** — Hỗ trợ chọn Kiểu A (SL sau đ/c) hoặc Kiểu B (SL điều chỉnh) cho mỗi phụ lục, áp dụng form + bản in (@khoipv) — 2026-05-09
  - Spec: `docs/superpowers/specs/2026-05-08-annex-quantity-table-type-design.md`
  - Plan: `.plans/annex-quantity-table-type/plan.md`

- **Thêm hàng hóa vào phụ lục thay đổi số lượng** — Cho phép thêm sản phẩm mới từ danh mục hệ thống vào phụ lục thay đổi số lượng, tạo nhóm mới/chọn nhóm cũ, nhân bản (@khoipv) — 2026-05-08
  - Spec: `docs/superpowers/specs/2026-05-08-annex-quantity-add-product-design.md`
  - Plan: `.plans/annex-quantity-add-product/plan.md`

- **Danh mục kho** — FE + BE hoàn chỉnh: menu, danh sách, modal CRUD cho Kho Vật Lý + Kho Kế Toán, 4 migrations, full API (@namdangit) — 2026-05-13
  - Spec: `docs/superpowers/specs/2026-05-13-danh-muc-kho-design.md`
  - Plan: `.plans/danh-muc-kho/plan.md`

- **Báo cáo chi tiết thầu** — Báo cáo chi tiết gói thầu (27 cột, 9 filters, phân quyền 3 cấp, export Excel, link HĐ) (@khoipv) — 2026-05-06
  - Spec: `docs/superpowers/specs/2026-05-06-detail-report-bid-package-design.md`
  - Plan: `.plans/detail-report-bid-package/plan.md`

- **Báo cáo chi tiết báo giá** — Trang báo cáo tổng hợp sản phẩm từ nhiều báo giá + export ExcelJS + phân quyền 3 cấp (@khoipv) — 2026-05-06
  - Spec: `docs/superpowers/specs/2026-05-05-detail-report-quotation-design.md`
  - Plan: `.plans/detail-report-quotation/plan.md`

- **Quotation Flow for Contract Types** — Sửa flow dự toán loại Cho/Tặng, Đặt/Mượn, Nguyên tắc để đi qua báo giá trước khi sang hợp đồng (@khoipv) — 2026-04-25
  - Spec: `docs/superpowers/specs/2026-04-24-quotation-flow-for-contract-types-design.md`
  - Plan: `.plans/quotation-flow-for-contract-types/plan.md`

- **Editable Price Cost** — Cho phép sửa cột Giá vốn trong bảng sản phẩm báo giá (@khoipv) — 2026-04-23
  - Spec: `docs/superpowers/specs/2026-04-23-editable-price-cost-design.md`
  - Plan: `.plans/editable-price-cost/plan.md`
