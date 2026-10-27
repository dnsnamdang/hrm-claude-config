# Kiểm kê theo hàng hóa (Phiếu kiểm kê) — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-20-kiem-ke-theo-hang-hoa-design.md`
> Khuôn: màn anh em **Kiểm kê theo vị trí** (`Modules/Finance/*PositionInventoryResult*`, `pages/warehouse/position-inventory-results`)
> + màn cha **Kế hoạch kiểm kê theo hàng hóa** (`*SelfInventoryRequest*`, `pages/finance/self-inventory-requests`).

## Phase 0 — Khảo sát
- [x] Đọc controller/model/blade/JS class ERP `self_inventories` (danh sách, form, chi tiết, quyền, trạng thái, luồng) + dữ liệu thật
- [x] Chốt với user 20/10 (spec mục 3): điều chuyển → HRM, nhập/xuất → ERP; 3 quyền tên y ERP type 21; popup kế hoạch y ERP; làm hết phần phụ như ERP

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 3 quyền trong `PermissionsTableSeeder` (type 21, group "Kiểm kê theo hàng hóa") + `permission:sync --dry-run`
- [x] B2. Entities `SelfInventory/*` (phiếu + 9 bảng con): STATUSES màu SRS, quyền, `scopedQuery` (type all / wait-approve), cờ (`canEdit/canUpdateResult/canApprove/canHandle/canTransfer/canInventoryImport/Export`), `needTransfer/needImport/needExport/handleCompleted`, `generateCode` `<cty>.KKK-NNNNN`
- [x] B3. Hàm tồn dùng chung: port `Product::getDataForInventory` (vị trí + lô có tồn, lọc công ty thuê) + `lotStockOfProducts` (Làm mới số liệu) — grep trước, đặt service theo chủ đề tồn vật lý
- [x] B4. `SelfInventoryService` (list/filter/sort/export-rows/print-list/filter-options/detail)
- [x] B5. `SelfInventoryWriteService`: form-options (kho, công ty thuê theo kho, NV + chức vụ), popup kế hoạch (union y ERP), plan-data, product-data, lot-stocks, store/update (validate, phiếu treo → popup, chặn hàng trùng kế hoạch tổng, kế hoạch → Đã lập kiểm kê), destroy, saveResult (+ Hàng thừa khác, file kết quả S3, thông báo Kế toán kho), approve/reject (thông báo), lịch sử
- [x] B6. FormRequest + Controller + routes `/self-inventories` + đăng ký `catalog_histories` (GATED)
- [x] B7. In (mẫu 292 phiếu / 291 danh sách, letterhead công ty phiếu) + Xuất Excel phiếu
- [x] B8. Nối màn khác: Kế hoạch theo hàng hóa nút Lập phiếu → HRM (gỡ `ERP_RESULT_CREATE_PATH`); Phiếu điều chuyển vị trí nhận `self_inventory_id` (source + store + cập nhật trạng thái phiếu KK) — test lại 2 màn đó
- [x] B9. Smoke test HTTP kernel toàn luồng + dọn dữ liệu test theo id

### Checkpoint — 2026-10-20 (Phase 1 BE xong)
Vừa hoàn thành: B1–B9 — 3 quyền seeder (dry-run OK, chưa sync thật); Entities `SelfInventory/*` (+ `SelfInventoryRequestAll` chỉ đọc);
`PhysicalStockReader` (port `getDataForInventory` + `lotStockOfProducts`); `SelfInventoryService` / `WriteService` / `AttachmentService` /
`PrintService` + `SelfInventoryExport` + blade; FormRequest Store / SaveResult; controller + 23 route `/self-inventories`;
`catalog_histories` GATED `self_inventories`; màn Kế hoạch: `erp_result_path` → `result_create_path` (HRM); Phiếu điều chuyển vị trí:
`GET /position-transfers/source-self/{id}` + store/update nhận `self_inventory_id`. Smoke HTTP kernel trong transaction rollback: 84/84 PASS
(Super admin 77 + NV thường 7). API contract thực tế: spec mục 8.
Đang làm dở: —
Bước tiếp theo: Phase 2 FE (F1–F6); FE màn Kế hoạch đổi `erp_result_path` → `result_create_path`, màn Phiếu điều chuyển đọc `?self_inventory_id=`.
Blocked:

## Fix 20/10 — user chốt lại 2 điểm "y ERP" sau Phase 1
- [x] Gỡ chặn phiếu nhập/xuất treo khi Lưu & gửi (ERP `checkPending` không bao giờ chặn) — `SelfInventoryController::blockedResponse`, bỏ `PENDING_MESSAGE` + `SelfInventoryWriteService::pendingVouchers()`
- [x] Thêm hàng trả MỌI lô `qty != 0` trong vị trí (công ty thuê chỉ để chọn vị trí) — `PhysicalStockReader::inventoryProducts`; kiểm tinker: SP 35182 kho 4 lọc TPE vẫn ra lô TPSG

## Phase 2 — FE (`pages/warehouse/self-inventories`)
- [x] F1. Danh sách `index.vue` (+ `?type=wait-approve`), row-actions, export-excel, In danh sách, Lịch sử
- [x] F2. Form dùng chung: thông tin chung + popup chọn kế hoạch, kho + công ty thuê (đổi thì xoá hàng, hỏi xác nhận), bảng hàng rowspan + ĐVT tách dòng, Làm mới số liệu, hội đồng, Hàng thừa khác, file kết quả, popup phiếu treo
- [x] F3. create / _id/edit / _id/index: footer theo cờ (Lưu / Lưu & gửi / Gửi duyệt / Duyệt / Không duyệt / 3 nút Xử lý / In / Xuất), 404
- [x] F4. Menu: Kho › Kiểm kho "Kiểm kê theo hàng hóa" → link; Tài chính › Kiểm kê thêm "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả"
- [x] F5. Màn Kế hoạch: Lập phiếu → HRM; màn Phiếu điều chuyển vị trí: tạo từ `?self_inventory_id=`
- [x] F6. Checklist skill erp-to-hrm-screen (grep) + compile

### Checkpoint — 2026-10-20 (Phase 2 FE xong, chưa mở trình duyệt)
Vừa hoàn thành: F1–F6 — `pages/warehouse/self-inventories/` (index + create + _id/edit + _id/index, components: SelfInventoryForm,
PlanPickerModal, row-actions, export-excel, product-tree). Dùng lại KHÔNG sửa: `position-inventory-results/components/result-units.js`
(ĐVT tách dòng) + `ApproveNoteModal.vue`, `AttachmentSection` (api-base), `SystemInfoSection`, `CatalogHistoryModal`.
Không dùng `PendingVouchersModal` (BE đã gỡ chặn phiếu treo 20/10). Menu: Kho › Kiểm kho "Kiểm kê theo hàng hóa" có link;
Tài chính › Kiểm kê thêm "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả" (`?type=wait-approve`, trang có watcher query).
Màn Kế hoạch: Lập phiếu → `result_create_path` (HRM, cùng tab). Phiếu điều chuyển vị trí: `?self_inventory_id=` →
`/source-self/{id}`, gửi `self_inventory_id`; list/chi tiết nguồn `self_inventory` link HRM.
Grep checklist skill sạch; parse vue-template-compiler + @babel/parser 16 file OK; nuxt dev :3000 trả 200, chunk không lỗi build.
Đang làm dở: —
Bước tiếp theo: V1 — user mở trình duyệt kiểm toàn luồng (tạo tay / từ KH theo HH / từ KH tổng, Làm mới số liệu, đổi ĐVT,
Gửi duyệt + Hàng thừa khác + file, Duyệt / Không duyệt, Tạo phiếu điều chuyển).
Blocked:

## Phase 3 — Kiểm chứng
- [x] V1a. Playwright toàn luồng 20/10 (DNS Admin, trình duyệt riêng headless): danh sách/sort/số dòng/lọc nâng cao, validate trống,
  tạo tay (kho → tự điền công ty thuê, chọn hàng, hội đồng → chức vụ tự chọn), sửa + đổi ĐVT Can (tồn lô quy đổi 161),
  Lưu và gửi, nhập Thực kiểm + Hàng thừa khác + file PNG, Gửi duyệt, `?type=wait-approve`, Không duyệt → gửi lại → Duyệt,
  nút xuất kho → ERP tab mới, In, Xuất Excel, Lịch sử; lập từ KH theo HH (KH → Đã lập), Tạo phiếu điều chuyển vị trí (nháp,
  `tmp_position_transfer_details` có `self_inventory_result_id`, phiếu KK → Đang xử lý); nút Lập phiếu ở màn Kế hoạch.
  Dọn theo id: phiếu 874/875, PĐCVT 948, lịch sử 1226–1240, 1 thông báo, KH 6 trả status 1 — DB về đúng mốc.
  Chưa test được: KH tổng kiểm kê (bảng `self_inventory_request_alls` local rỗng), bấm "Điều chuyển" thật (đụng tồn kho), NV thường.
- [x] Fix 20/10 (user): Ghi chú cùng hàng Công ty thuê kho — `SelfInventoryForm.vue` col-md-8 (Thêm) / col-md-4 (Sửa, Chi tiết)
- [x] Fix 20/10 (user): Lịch sử dòng SỬA kết quả kiểm kê chỉ in tên hàng + trường đổi — `SelfInventoryWriteService::loadVirtualRows`
  dòng kết quả `__brief` → `true` (bỏ phụ chú Vị trí / Lô / ĐVT). Log đã ghi trước giữ nguyên hiển thị cũ.
- [ ] V1b. Chờ user chốt: bảng hàng ở bước nhập kết quả rộng ~1.780px > khung 1.336px → cột Thực kiểm / Chênh lệch / Ghi chú khuất phải
- [ ] V1c. Chờ user chốt: phiếu rác id 97 (status 0, không mã) hiện badge "0" ở danh sách

## Rà sau Phase 2 (20/10)
- [x] Nhãn 2 nút Xử lý theo ERP: "Tạo phiếu nhập kho điều chuyển" / "Tạo phiếu xuất kho điều chuyển" (subagent đặt "điều chỉnh")
- [x] Grep checklist + fail-open trên `pages/warehouse/self-inventories`: sạch
- Giữ: "Duyệt kết quả" (đồng bộ màn anh em + popup dùng chung); khối file tiêu đề "File đính kèm" (component chung); cột Kế hoạch KK ở danh sách là chữ (ERP danh sách không có cột này); Hàng thừa khác dùng `position-inventory-results/structure` + `master-data/units/getAll` (route không gate quyền)

## Phase 4 — Fix Redmine #11814 (QA 21/10)
- [x] R4. Tạo phiếu từ kế hoạch: Ngày kiểm kê / Kho / Công ty thuê kho đã `disabled` nhưng nền trắng (cùng gốc R3 bên Kế hoạch) → `::v-deep` trong `SelfInventoryForm.vue`
- [x] R5. Tạo phiếu từ kế hoạch báo đỏ "Hàng hóa không còn tồn…" — hàng hết tồn thật (KH 3 local: 16/222, tồn thực tế + kế toán = 0; ERP thì vỡ form). User chốt 22/10: giữ bỏ hàng, đổi toast đỏ → cảnh báo vàng, câu gọn tối đa 5 mã (`warnNoStock`)

### Checkpoint — 2026-10-22 (#11814)
Vừa hoàn thành: R4 (ô khoá xám bằng ::v-deep trong SelfInventoryForm) + R5 (cảnh báo vàng hàng hết tồn). Kèm R1–R3 bên plan Kế hoạch kiểm kê theo hàng hóa.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm (chưa bấm thật); hỏi user có sửa gốc ở V2BaseInput (component dùng chung) để ô disabled xám ở mọi màn không.
Blocked:

## Phase 5 — Fix Redmine #11817 (QA 21/10)
- [x] R6. Tạo phiếu: bấm × ở ô ĐVT kiểm kê → ô trống nhưng dữ liệu vẫn giữ ĐVT cũ (`onUnitInput` bỏ qua giá trị rỗng) nên "Lưu và gửi" lọt, không báo lỗi → cho xoá thật (`unit_id = null`) + `validateAll()` bắt từng dòng ĐVT kiểm kê trống, lỗi inline tại ô (khoá `products.i.positions.j.details.k.results.m.unit_id`, câu khớp BE)
- [x] R7. Chọn kế hoạch #03 báo đỏ "Hàng hóa không còn tồn…" — trùng R5 (#11814), đã sửa ở local (cảnh báo vàng, tối đa 5 mã), chưa lên dev

### Checkpoint — 2026-10-22 (#11817)
Vừa hoàn thành: R6 — `SelfInventoryForm.vue` `onUnitInput` cho xoá ĐVT thật (bỏ cơ chế vẽ lại ĐVT cũ + `unitClearAt`), `validateAll()` bắt ĐVT kiểm kê trống từng dòng → viền đỏ + câu lỗi dưới ô. BE đã có sẵn `results.*.unit_id required`. Parse template + script OK. R7 trùng R5.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm: × ô ĐVT → Lưu / Lưu và gửi báo lỗi tại ô; chọn lại ĐVT → hết lỗi, quy đổi tách dòng vẫn đúng.
Blocked:

## Phase 6 — Fix Redmine #11819 (QA 23/10)
- [x] R8. Danh sách: bỏ sort cột Người tạo / Người duyệt / Trạng thái (list-page "Cột nào được sort": chỉ mã/tên, tiền, ngày)
- [x] R9. Cập nhật kết quả: tiêu đề Hàng hóa / Hàng thừa khác / Hội đồng kiểm kê có (*) như tab ERP (trước chỉ hiện ở Thêm/Sửa)
- [x] R10. Duyệt kết quả: thiếu khối Hàng thừa khác khi phiếu không có hàng thừa → luôn hiện khi `show_result_columns` (bảng trống "Không có dữ liệu", như tab ERP)

### Checkpoint — 2026-10-23 (#11819)
Vừa hoàn thành: R8 `index.vue` bỏ `sortable` cột Trạng thái / Người tạo / Người duyệt (còn sort: Số phiếu, Ngày kiểm kê, Ngày tạo, Ngày duyệt).
R9 `SelfInventoryForm.vue` computed `showRequiredMark` (= Thêm/Sửa hoặc đang nhập kết quả) cho (*) khối Hàng hóa / Hội đồng; Hàng thừa khác có (*) khi nhập kết quả — chỉ dấu, không thêm luật validate.
R10 khối Hàng thừa khác hiện mọi lúc `show_result_columns` (duyệt / đã duyệt không có dòng → "Không có dữ liệu"). Parse template + script OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm 3 điểm trên dev.
Blocked:

## Phase 7 — Fix Redmine #11825 (câu lỗi theo skill form-validate)
- [x] R11. Lỗi "Hàng hóa – Hàng hóa đã lập phiếu kiểm kê." có tiền tố tên trường (cả toast lẫn dưới dòng) → bỏ tiền tố, chỉ còn "Hàng hóa đã lập phiếu kiểm kê." (skill form-validate §3, chốt #11791)
- [x] R12. Áp skill cho cả màn: bỏ tiền tố "<Tên trường> –" mọi câu lỗi FE (`SelfInventoryForm.vue`) + BE (StoreRequest, SaveResultRequest, WriteService, Controller); bỏ trống → "Bắt buộc phải nhập", quá dài → "Vui lòng nhập tối đa N ký tự.", sai → "Không hợp lệ"
- [x] R13. Toast khi BE trả 422 lỗi theo ô → câu chung "Vui lòng kiểm tra lại thông tin đã nhập.", không nhét câu lỗi của ô lên toast

### Checkpoint — 2026-10-23 (#11825)
Vừa hoàn thành: R11–R13. BE bỏ tiền tố ở StoreRequest / SaveResultRequest / WriteService / Controller (endpoint `product-data` chỉ báo qua toast nên giữ câu tự nói rõ "Vui lòng chọn kho." …; "Kế hoạch kiểm kê không tồn tại.", "Tồn theo lô phải lớn hơn 0." viết thành câu). FE `SelfInventoryForm.vue`: câu lỗi tự kiểm theo vi.json, toast 422 = "Vui lòng kiểm tra lại thông tin đã nhập." (save + runDetailAction), `productRowError` hiện thêm mọi lỗi con của dòng chưa có ô riêng, thêm dòng lỗi dưới ô Kế hoạch kiểm kê. Smoke: POST rỗng → 422 đủ khoá, câu không tiền tố; `duplicateErrors` → "Hàng hóa đã lập phiếu kiểm kê.". Template + script parse OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm lại case #11825 (kế hoạch tổng id=8, hàng đã lập phiếu).
Blocked:

## Phase 8 — Fix Redmine #11826 (QA 23/10, màn Chi tiết phiếu)
- [x] R14. Hàng thừa khác: nút xoá vị trí (dòng vị trí thứ 2 trở đi) đang là dấu "−" → đổi sang biểu tượng thùng rác như nút Xóa dòng
- [x] R15. Tiêu đề Hàng hóa / Hàng thừa khác / Hội đồng kiểm kê có (*) khi nhập kết quả — đã làm ở R9 (#11819), chưa lên dev → chỉ kiểm lại
- [x] R16. Thông tin chung: bỏ ô Số phiếu (mã đã hiện trên thanh tiêu đề) → Ghi chú luôn `col-md-8`

### Checkpoint — 2026-10-23 (#11826)
Vừa hoàn thành: R14 `SelfInventoryForm.vue` nút "Xóa vị trí" ở Hàng thừa khác `ri-subtract-line` → `ri-delete-bin-line` (vẫn `danger`). R15 đã có từ R9 — ảnh QA chụp trên dev chưa có bản #11819. R16 bỏ ô Số phiếu ở Thông tin chung (Sửa + Chi tiết; mã vẫn trên thanh tiêu đề), Ghi chú luôn `col-md-8`. Template + script parse OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm phiếu 1074 (nhập kết quả, thêm 2 vị trí ở Hàng thừa khác); deploy kèm #11819.
Blocked:

## Phase 9 — Fix Redmine #11822 (QA 21/10, màn Tạo phiếu)
- [x] R17. Ô Công ty thuê kho (chưa chọn kho): thêm placeholder "Chọn công ty thuê kho" + bỏ tooltip "Chọn kho trước…"
- [x] R18. Câu lỗi validate theo skill form-validate: bỏ tiền tố tên trường (đã làm ở #11825) + FE KHÔNG tự chặn `required` — chỉ chặn định dạng (Ghi chú ≤ 255), required / trùng để BE trả 422 rồi hiện dưới từng ô
- [x] R19. Bảng Hàng hóa cuộn dọc: dòng lộ qua khe phía trên tiêu đề dính → phủ kín
- [x] R20. Bỏ chú thích "TPE - 87" dưới SL tồn kho
- [x] R21. Đổi kho / công ty thuê kho khi đã có hàng: chưa bấm Đồng ý mà ô đã đổi (công ty thuê kho bị clear) → giữ nguyên giá trị cũ tới khi Đồng ý
- [x] R22. Popup Thêm hàng hóa chỉ lọc tồn theo kho, không theo công ty thuê kho → thêm tham số `stock_company_ids[]` vào ProductPickerService (user đồng ý 23/10), màn truyền công ty thuê kho đang chọn

### Checkpoint — 2026-10-23 (#11822)
Vừa hoàn thành: R17–R22. FE `SelfInventoryForm.vue`: placeholder ô Công ty thuê kho + bỏ tooltip "Chọn kho trước"; `validateAll()` → `validateFormat()` chỉ chặn Ghi chú > 255, bắt buộc / trùng thành viên / ĐVT trống để BE 422 (đủ ô 1 lần, câu không tiền tố); tiêu đề bảng dính ở từng `th` + `border-collapse: separate`; bỏ dòng "TPE - 87" dưới SL tồn kho; `confirmClearProducts` vẽ lại giá trị cũ ngay, chỉ đổi khi Đồng ý; popup Thêm hàng hóa truyền `stock_company_ids`. BE `ProductPickerRequest` + `ProductPickerService` thêm `stock_company_ids[]` (cùng điều kiện `PhysicalStockReader::inventoryProducts`).
Smoke (kho 2, công ty 3): popup 4812 → 136 hàng; product-data trên 100 hàng đã lọc: no_stock 0 (chưa lọc: 98/100 hết tồn — đúng lỗi QA). POST phiếu rỗng → 422 warehouses / company_rentals / products / members.0.* cùng lúc. Template + script parse OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm 6 điểm (đặc biệt R19 tiêu đề dính khi cuộn bảng dài, R21 đổi kho → Hủy / Đồng ý).
Blocked:

## Phase 10 — Fix Redmine #11823 (QA 21/10, màn Danh sách)
- [x] R23. Ô lọc Kho: công tắc 🔒 xem được cả kho đã khoá (khuôn `LockableFilterSelect` như danh mục kho #11782); BE `filterOptions` trả kho kèm `is_locked` (bỏ kho ERP đã xoá status 2)
- [x] R24. ERP chỉ thấy phiếu theo công ty, HRM thấy hết. Gốc: `SelfInventory` kiểm quyền qua trait `ChecksEmployeePermission` (bỏ qua `role_has_permissions.company_id`, role 18 = xem hết) trong khi ERP `Employee::can()/hasRole()` lọc theo công ty đang chọn. User chốt 23/10 hướng 1: CHỈ màn này — `isAllCompany` / `canViewCompany` / `hasPermission` → hàm chung `isCurrentEmployeeHasPermission()` (theo `current_company_role`), bỏ lối tắt role 18. Không sửa ERP, không sửa trait chung (103 file)
- [x] R25. Cột Kế hoạch kiểm kê thành link sang chi tiết kế hoạch (theo hàng hóa / tổng) — BE trả `plan_path`
- [x] R26. Bỏ sort Ngày tạo / Ngày duyệt (Người tạo / Người duyệt / Trạng thái đã bỏ ở #11819); sort mặc định trống → icon trung tính, BE vẫn created_at giảm dần
- [x] R27. Thêm cột Ngày cập nhật + Người cập nhật (bảng + Xuất Excel)
- [x] R28. Ngày duyệt kèm giờ (bảng + Excel; bản in đã có giờ)
- [x] R29. Xuất Excel: bỏ màu nền dòng tiêu đề cột
- [x] R30. (Hỏi) Lọc có "Chờ xử lý" / "Đang xử lý" nhưng không thấy phiếu → KHÔNG sửa: 2 trạng thái có thật (Duyệt kết quả có chênh lệch → Chờ xử lý; lập phiếu điều chuyển / nhập-xuất điều chỉnh → Đang xử lý), y ERP; dữ liệu hiện chưa có phiếu nào tới bước đó

### Checkpoint — 2026-10-23 (#11823)
Vừa hoàn thành: R23–R30. BE `SelfInventoryService`: `filterOptions.warehouses` = `WarehouseCatalogScope::warehouseOptions([], true, true)` (mọi công ty, kèm `is_locked`, bỏ status 2); list join `updated_by` → `updated_at_full` / `updater_name`; `plan_path` theo KH theo hàng hóa / KH tổng; `SORT_MAP` chỉ còn `code` + `inventory_date`. FE `index.vue`: slot `#field-warehouse_id` = `LockableFilterSelect` (công tắc cục bộ `showLockedWarehouses`), cột Kế hoạch KK là link, bỏ sort Ngày tạo / Ngày duyệt (sort mặc định trống), cột Ngày duyệt hiện giờ, thêm Ngày cập nhật / Người cập nhật, `exportFieldKeyMap` (created_at / approve_time → *_full). `export-excel.js`: thêm 2 cột, Ngày duyệt kèm giờ, bỏ nền tiêu đề cột.
R24 / R30 không sửa code (phạm vi + trạng thái y ERP) — trả lời QA.
Smoke (tinker, NV 13 Super admin): list 690, có updater/approve giờ/plan_path; kho 19 (1 khoá); sort created_at/approve_time bị bỏ qua → created_at desc; export 690 dòng có updater. Template + script parse OK. Chưa mở trình duyệt.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm: công tắc 🔒 ô Kho, bấm link kế hoạch, Xuất Excel (tiêu đề không nền, đủ 2 cột mới).
Blocked:

### Checkpoint — 2026-10-23 (#11823 R24)
Vừa hoàn thành: R24 `SelfInventory.php` 3 hàm quyền dùng `isCurrentEmployeeHasPermission()`. Smoke (tinker, transaction rollback): DNS Admin công ty 1 → xem hết 690; giả `company_role = 4` → all/company/BKS = false, chỉ 1 phiếu của mình; NV 25 không quyền → 0.
Đang làm dở: —
Bước tiếp theo: deploy dev → QA kiểm lại với tài khoản/công ty thật; lưu ý người có quyền ở công ty khác công ty hiện tại sẽ mất quyền trên màn này (đúng ERP).
Blocked:

## Phase 11 — Fix Redmine #11857 (QA 23/10, màn Danh sách + nhập kết quả)
- [x] R31. "Đặt sort về mặc định": ảnh QA chụp 15:53 23/10, TRƯỚC commit #11823 R26 (16:13) → sort Ngày tạo / Ngày duyệt đã bỏ. Vá nốt: sort cũ (created_at / approve_time…) còn lưu localStorage → khi khôi phục chỉ giữ `code` / `inventory_date`
- [x] R32. (*) tại khối Hàng hóa / Hàng thừa khác / Hội đồng kiểm kê lúc nhập kết quả → đã có từ #11821 (`4c14fd4bf`, 09:23 23/10, đã lên origin/develop); ảnh QA chụp trên hrm-crm (bản build cũ). Không sửa code

### Checkpoint — 2026-10-26 (#11857)
Vừa hoàn thành: R31 (FE `index.vue` `restoreAndLoad`), R32 xác minh
Đang làm dở: —
Bước tiếp theo: deploy → QA kiểm lại trên bản mới
Blocked:
