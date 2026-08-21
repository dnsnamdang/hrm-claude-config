# Plan — customer-manager

@manhcuong · 2026-06-10

Màn quản lý KH HRM (`/assign/customers/:id/manager`) tương đương ERP, full edit, 6 tab, 3 phase.
Spec: `docs/superpowers/specs/2026-06-10-customer-manager-design.md`

---

## Phase 1 — Thông tin chung + Liên hệ + Thông tin khác

### BE (Modules/Assign)
- [x] BE1: Model ERP mysql2 `TpCustomerGallery` (customer_galleries) + `TpCustomerVideo` (customer_videos)
- [x] BE2: `CustomerService::show` load thêm galleries[] + videos[] + attachments[] (parseAttachments tách cột)
- [x] BE3: `CustomerService::updateMedia($id, request)` — galleries delete-all+insert, videos upsert theo id, attachments giữ cũ (attachment_paths[]) + upload mới S3 (transaction mysql2)
- [x] BE4: Upload S3 dùng `App\Helper\CmcS3Helper` (putFile/putFiles); uploadCustomerImage + deleteAttachmentFile
- [x] BE5: CustomerController (updateMedia/uploadImage/deleteFile) + route `POST /{id}/media`, `POST /upload-image`, `POST /{id}/delete-file` (đặt upload-image TRƯỚC /{id})
- [x] BE6: CustomerDetailResource bổ sung galleries/videos/attachments
- [x] BE7: php -l PASS (6 file)

### FE (hrm-client)
- [x] FE1: Trang `pages/assign/customers/_id/manager/index.vue` — CustomerForm tabbed
- [x] FE2: Tách bằng `tabbed` prop + `<component :is>` (b-tabs/b-tab khi tabbed, div khi phẳng) — KHÔNG nhân đôi code, giữ chung 1 state + 1 save. Di chuyển block "Địa chỉ giao hàng" vào Tab Thông tin chung.
- [x] FE3: Tab1 "Thông tin chung" = SECTION 1+2+3 + Địa chỉ giao hàng (save tổng qua V2Footer có sẵn)
- [x] FE4: Tab2 "Thông tin liên hệ" = SECTION 4 contacts (ẩn khi !isOrganization)
- [x] FE5: `OtherInfoTab.vue` (Tab "Thông tin khác") — ảnh upload S3 + tài liệu PDF + video + nút Lưu (media); 3 store action mới
- [x] FE6: Row action "Quản lý" (ri-settings-3-line) ở danh sách → `/:id/manager`
- [x] Tab placeholder: Báo giá/Hợp đồng (Phase 2), Danh sách trang thiết bị (Phase 3)

### Verify
- [x] V1: php -l PASS (BE) + vue-template-compiler + @babel/parser PASS (3 SFC + store/actions.js). KHÔNG có eslint/esbuild bin tại đây.
- [ ] V2: user verify browser P1 (mở `/assign/customers/:id/manager`, kiểm tra 6 tab + lưu Thông tin khác)

---

## Phase 2 — Báo giá + Hợp đồng
### BE
- [x] P2-BE1: `CustomerManagerService::documents($id,$kind,$req)` đọc ERP 4 bảng (firm_quotations, wr_service_quotations type=1, firm_contracts, wr_service_contracts type=1); join employees→employee_infos→departments lấy người tạo + phòng ban; filter start_date/end_date/employee_id/department_id; sum total_after_vat + paginate
- [x] P2-BE2: `departments()` list phòng ban ERP
- [x] P2-BE3: CustomerManagerController (documents, departments) + route `GET /{id}/documents`, `GET /manager/departments`
### FE
- [x] P2-FE1: `DocumentTable.vue` (filter ngày/NV/phòng ban + bảng + phân trang b-pagination + dòng tổng)
- [x] P2-FE2: `QuotationsTab.vue` (2 bảng: hàng hóa firm_quotation + dịch vụ wr_quotation) + `ContractsTab.vue` (2 bảng contract, có cột Ngày hiệu lực)
- [x] P2-FE3: gắn vào CustomerForm tab (lazy) thay placeholder
### Lưu ý P2
- Đơn giản hóa phân quyền: lọc theo customer_id + filter (không replicate cascade quyền Xem-tất-cả/công-ty/phòng của ERP). Đủ cho màn xem chứng từ của 1 KH.

## Phase 3 — Danh sách trang thiết bị
### BE
- [x] P3-BE1: 3 model Tp (TpEquipmentOld=equipments_old, TpExternalEquipment=external_equipments, TpSerial=serials)
- [x] P3-BE2: `CustomerManagerService` equipment: equipmentList (nhóm Thiết bị cũ + NCC khác, join products/brands/product_models/suppliers, kèm serials), buildOld/ExternalRows, serialRowsFor, equipmentDetail
- [x] P3-BE3: CRUD thiết bị: addOld/updateOld/deleteOld + addExternal/updateExternal/deleteExternal (chặn trùng, chặn xóa nếu serial đã dùng trong 9 bảng luồng, chèn serial khi thêm)
- [x] P3-BE4: Serial: addSerial, updateSerial, changeSerial (parent_id + status cũ=2), deleteSerial (chặn theo luồng), serialUsedInFlow, checkSerial
- [x] P3-BE5: suppliers() + searchProducts() (modal)
- [x] P3-BE6: Controller endpoints + routes (equipment list/detail, old/external CRUD, serial CRUD, suppliers, search-products) — đặt /serial/* và /manager/* trước /{id}
### FE
- [x] P3-FE1: `EquipmentTab.vue` — filter (NCC thiết bị tp/ncck + mã/tên), nút Thêm thiết bị cũ/NCC, bảng nhóm (Tên/Thương hiệu/Model/Mã/SL/Serial/NCC/Hành động)
- [x] P3-FE2: 4 modal (theo skill modal-popup): Thêm/Sửa thiết bị (cũ + NCC, product picker inline an toàn trong modal, serial khi thêm), Danh sách serial, Sửa/Đổi serial, Thêm serial
- [x] P3-FE3: gắn vào CustomerForm tab (lazy)
### Defer P3 (ghi rõ — ngoài phạm vi, dữ liệu hệ thống phức tạp)
- KHÔNG gồm hàng "Tân Phát (xuất kho)" từ ProductExportRequest (read-only, coupling sâu report ERP)
- KHÔNG gồm "Thêm serial cho phiếu xuất" (addSerialToInvoiceable), "Tăng số lượng" (updateProductCustomer), "Tình trạng sử dụng" (submitUsageStatus), attachment ảnh cho serial, device_errors/tạo dịch vụ
- → Quản lý đầy đủ: Thiết bị cũ + NCC khác + serial (thêm/sửa/đổi/xóa)

---

## Phase 4 — Parity ERP (bổ sung cho giống màn ERP 100%)
Nguồn: rà soát 3 agent đối chiếu ERP `customercare/customermanager/show_.blade.php` 6 tab (2026-06-16). User chọn làm TẤT CẢ nhóm A + B + C + D. Làm theo đợt an toàn→phức tạp.

### Đợt 1 — Nhóm A (gap thật, rẻ, độc lập) — CODE DONE 2026-06-16
- [x] A1: Cột NVKD + Phòng ban người liên hệ — KHÔNG phải cột; suy ra từ firm_quotations + wr_service_quotations gắn customer_contact_id → NV tạo + phòng ban (dedupe). BE `CustomerService::getErpContactSalesMap` + gắn vào getErpContactsWithAccountsById; FE CustomerForm hiển thị read-only trong contact block.
- [~] A2: BỎ — cột `external_equipments.product_equivalent_id` đã bị ERP DROP (migration 2023_04_10 v4), ERP không lưu field này → không phải gap thật, HRM bỏ đúng.
- [x] A3: Tăng số lượng thiết bị — BE `CustomerManagerService::addQuantity` + controller `addQuantity` + route POST `/{id}/equipment/add-quantity`; FE EquipmentTab nút "Tăng SL" + modal.
- [x] A4: Filter Nhóm hàng hóa — ERP dropdown hỏng (nạp customer_groups, không wire). BE làm bản chạy thật: `productGroups()` từ bảng `groups` + filter `products.group_id` ở buildOld/ExternalRows; route GET `/manager/product-groups`; FE dropdown + fetch group_id.
- [x] A5: Nhãn Loại hình tổ chức — sửa CustomerForm loại 4 "Doanh nghiệp FDI" → "Tổ chức phi chính phủ" khớp ERP.
- Verify: php -l PASS 4 file BE; vtc + @babel parser PASS EquipmentTab.vue + CustomerForm.vue.

### Đợt 1b — Validate serial đúng ERP — CODE DONE 2026-06-16
Đối chiếu validate vs ERP (SerialController + 3 Request thiết bị). Phát hiện: ERP update()/change() có gọi checkExistSerial nhưng BỎ QUA kết quả (dead code) → ERP thực tế KHÔNG chặn theo luồng khi sửa/đổi serial → HRM update/change đã khớp. Gap thật ở "Thêm serial".
- [x] addSerial: trước đây trùng thì bỏ qua âm thầm + báo "thành công", không giới hạn SL. Sửa: required + unique TOÀN BẢNG serials (ERP unique:serials,serial) + chặn trùng trong list + tổng (đang có + mới) ≤ SL thiết bị. Helper normalizeSerialNames/validateNewSerials/equipmentQtyFor/countSerialsFor. Trả ok=false → controller 422 → FE toast.
- [x] addOldEquipment + addExternalEquipment: thay check `qty<count` bằng validateNewSerials (bắt thêm trùng + unique toàn bảng).
- [x] FE submitAddSerial: rỗng → toast "Vui lòng nhập serial" (không đóng âm thầm) + chặn trùng client-side.
- [x] SỬA THEO CHUẨN VALIDATE (CLAUDE.md): addSerial THROW ValidationException keyed `serials.{i}` (required/unique/trùng-list) + key chung `serials` (vượt SL) → Laravel render 422 {message,errors}. equipmentAction rethrow ValidationException (không nuốt thành 500). FE: V2BaseError dưới TỪNG ô serial (serialLineError(idx)) + lỗi chung dưới list (addSerialGeneralError); required validate client-side trước (inline ngay); @input clear lỗi ô. KHÔNG dùng toast cho lỗi field.
- Verify: php -l PASS; vtc+babel PASS; SMOKE DB ERP thật: errors() trả đúng key/field — serials.1=>Vui lòng nhập serial, serials.0=>Serial đã tồn tại (unique toàn bảng), serials.1=>Serial bị trùng trong danh sách, serials=>vượt SL.

### Đợt 2 — C2 + C4 (báo giá/hợp đồng, rẻ) — CODE DONE 2026-06-16
- [x] C2: Lọc bỏ chứng từ nháp — DOC_MAP thêm cờ `draft` cho wr_quotation/wr_contract; documents() ẩn status=DANG_TAO(1) trừ created_by = currentUserId(). STATUS_DANG_TAO=1.
- [x] C4: Filter Công ty — documents() filter `ei.company_id`; service `companies()` + controller + route GET `/manager/companies`; FE DocumentTable prop `companies` + dropdown (chỉ hiện khi có data) + param company_id; QuotationsTab/ContractsTab nạp companies, truyền cho bảng firm.
- Verify: php -l PASS 3 file BE; vtc+babel PASS DocumentTable/QuotationsTab/ContractsTab.

### Đợt 3 — Nhóm B (UX nâng cao, HRM đã đủ data)
- [~] B1: Địa chỉ giao hàng + Người liên hệ qua modal lưu tức thời — BỎ: HRM nhập inline lưu chung đã đủ data (cùng bảng), chỉ khác UX, không phải gap chức năng.
- [ ] B2: Cấp Quận/Huyện cho KH nước ngoài (nation_id != 1) — BE đã sẵn (districts() + lưu district_id); chỉ thiếu FE. NHƯNG sửa CustomerForm (component DÙNG CHUNG add/edit, đã CHỦ ĐỘNG bỏ district) → cần xác nhận trước.
- [ ] B3: Nút tạo nhanh Đường/Thôn/Xóm (hamlet) — cần endpoint createHamlet + modal, cũng sửa CustomerForm dùng chung → cần xác nhận.
- [x] B4: Gallery ảnh kéo-thả sắp xếp thứ tự — DONE: vuedraggable bọc gallery trong OtherInfoTab (BE updateMedia đã lưu position theo thứ tự mảng); CSS cursor move + ghost; hint "Kéo để sắp xếp". Parse PASS.
- [ ] B5: Ảnh đính kèm cho serial — cột serials.attachment có sẵn; cần upload S3 trong modal serial. Ưu tiên thấp (agent đánh giá).

### Đợt 4 — C1 + C3 + Nhóm D (coupling sâu, effort lớn)
- [x] C1: Phân quyền cascade báo giá/hợp đồng — DONE 2026-06-16. PERM_MAP per kind; applyDocumentPermissionScope trong buildDocumentsQuery (áp cả documents() lẫn export). firm (4 cấp): all→ei.company_id→phòng QUẢN LÝ (employee_manage_departments)→bộ phận QUẢN LÝ (employee_manage_parts)→created_by. wr (3 cấp): all→d.company_id→d.department_id(của user)→created_by. Lấy org user qua employee_infos theo auth()->user()->employee_info_id; quyền qua ErpPermissionHelper::userCan. Mặc định không quyền → chỉ của mình (an toàn). Verify DB ERP thật login 4 user: ALL 217=217, CÔNG TY 206=206, PHÒNG(quản lý dept42) 59=59, CHỈ MÌNH 0=0 — khớp raw tuyệt đối.
- [x] C3: Nút In + Xuất Excel báo giá/hợp đồng — DONE 2026-06-16. BE: tách buildDocumentsQuery dùng chung + documentsExportData (lấy tất cả) + DOC_LABELS; Export class CustomerDocumentsExport (FromView) + blade exports/assign/customer_documents (cột khớp ERP: STT/Ngày lập/Số/Tổng TT/[Ngày hiệu lực]/Người tạo/Phòng ban + Tổng cộng); controller exportDocuments → Excel::download; route GET /{id}/documents/export. FE DocumentTable: nút In (lấy all rows → openPrintWindow window.print) + Xuất Excel (apiExportExcel); filterParams() dùng chung. Verify: php -l PASS; xlsx sinh thật 16KB (217 dòng báo giá / 131 HĐ có Ngày hiệu lực); export rows == documents total (draft filter nhất quán); documents() phân trang còn OK sau refactor.
- [x] D1: Nhóm "Tân Phát" thiết bị từ phiếu xuất — DONE 2026-06-16. buildTanPhatRows replicate getReportDetailData (2 nhánh: product_export_request_details status=5 + 6 loại phiếu [1,2,11,13,14,17] need_export+HANG_HOA; borrow_sell_request_products qty>0 + borrow_sells), gộp theo product_id (mergeTanPhatRow cộng dồn SL), read-only. equipmentList thêm nhóm "Tân Phát" đầu. serialRowsFor: Tân Phát='tp', Thiết bị cũ giữ ['tp','tpc'] (ERP lưu serial thiết bị cũ là 'tp' — KHÔNG đổi sang 'tpc' kẻo ẩn 3579 serial). FE: option lọc "Tân Phát" + nhóm read-only (ẩn Tăng SL/Sửa/Xóa, span "—") + serialReadonly (serial Tân Phát chỉ xem). Verify DB ERP thật: KH14272 Tân Phát 252sp = raw distinct 252, qty khớp; KH45 Thiết bị cũ serial không mất. php -l + parse PASS.
  Defer trong D1: cột handover/invoiceable, ngày bàn giao (thuộc D5).
- [x] D2: addSerialToInvoiceable — DONE 2026-06-16. buildTanPhatRows lộ invoice_id/invoice_type (phiếu đại diện MAX id, ưu tiên product_export). Service addSerialToInvoiceable: validate (required + unique toàn bảng TRỪ serial đã trên chính invoiceable + chống trùng list, throw ValidationException inline) + insert product_type='tp' gắn invoiceable_id/type. Controller + route POST /{id}/serial-invoiceable. FE: nút "Thêm serial cho phiếu xuất" trong serial modal Tân Phát + nhánh submitAddSerial. Verify DB ERP thật (rollback): thêm unique → tp+invoiceable_id=3847+ProductExportRequest; trùng toàn bảng → "Hệ thống đã tồn tại serial này" (khớp ERP).
- [~] D3: Tạo dịch vụ/bảo hành từ thiết bị — NGOÀI PHẠM VI màn này. addOldEquipmentService gom DeviceError/DeviceErrorProduct/wr_service_* → bắc cầu sang module Bảo hành/Dịch vụ mà HRM Assign KHÔNG có. Không phải gap hiển thị của màn quản lý; cần port module Dịch vụ riêng nếu muốn.
- [~] D4: device_errors + units — KHÔNG hiển thị trên markup tab thiết bị ERP (chỉ data nền cho D3) → không có gì để parity → bỏ. (Cùng đó: cột Hình ảnh sp + usage_status đã bị ERP comment `{{-- --}}` → HRM không hiện là đúng.)
- [x] D5: Cột serial mở rộng + In/Xuất Excel tab thiết bị — DONE 2026-06-16. serialRowsFor join invoiceable (product_export_requests/borrow_sell_requests → COALESCE code = Phiếu YCXH) + warranty (firm_contract guarantee + handover created_at → ngày nghiệm thu/bảo hành/hết BH, best-effort nhánh firm_contract như ERP). FE serial modal +5 cột (Hình ảnh/Ngày nghiệm thu/Thời gian BH/Hết BH/Phiếu YCXH) + formatDate. In/Xuất Excel tab thiết bị (CustomerEquipmentExport + blade + route /{id}/equipment/export + FE nút In dùng this.groups + Excel apiExportExcel). Verify: invoiceable_code serial 3317→PYCXH-12414 khớp raw; xlsx 252 rows 25KB; route OK. Lưu ý data thật: attachment=0, warranty firm_contract=0 toàn hệ (ERP cũng trống) → cột shape khớp, Phiếu YCXH có data thật.

---
## Checkpoint
### Checkpoint — 2026-06-16 (SỬA ĐÚNG: tab Thiết bị nhóm theo NHÓM HÀNG HÓA)
User báo ERP hiện tên nhóm "Cầu nâng 2 trụ..." còn HRM hiện "Tân Phát". Truy nguồn: tab thiết bị gọi `customerCareReport.getProductDataCustomerCare` (KHÔNG phải getListProductOfCustomer). `getProductForReport` nhóm bằng `Group::whereIn(product group_ids)` → **rowGroups = NHÓM HÀNG HÓA (groups.name)**, KHÔNG phải Tân Phát/NCC. Tân Phát/NCC chỉ là CỘT + filter nguồn.
Sửa: equipmentList GỘP nguồn (tp=Tân Phát+thiết bị cũ, ncck=external) rồi NHÓM theo products.group_id→groups.name (productGroupMap), sort theo tên; fallback "Chưa phân nhóm" cho product không group. type_text giữ Tân Phát/NCC khác (cột NCC). Verify: KH41360→1 nhóm "Cầu nâng 2 trụ thủy lực có cổng" (khớp ERP), KH45→13 nhóm hàng hóa, KH14272→165 nhóm; export có cột Nhóm; filter group_id OK. php -l+parse PASS.
(Trước đó hiểu nhầm "2 nhóm theo NCC" — đã thay bằng nhóm hàng hóa đúng ERP.)

### Checkpoint — 2026-06-16 (Sửa cấu trúc tab Thiết bị — bản nhầm, xem checkpoint trên)
User báo tab "Danh sách trang thiết bị" hiển thị khác ERP. Đối chiếu markup ERP (#products): ERP CHỈ 2 nhóm "Tân Phát" (gồm hàng xuất kho + Thiết bị cũ, đều product_type_name='Tân Phát') + "NCC khác" — HRM trước tách 3 nhóm. Đã sửa:
- BE equipmentList: gộp buildTanPhatRows + buildOldRows vào 1 nhóm "Tân Phát"; filter type_supplier 'tp'(Tân Phát)/'ncck'. buildOldRows type_text+supplier='Tân Phát'; buildExternal type_text='NCC khác'.
- FE: filter 2 option (Tân Phát/NCC khác), label "Nhà cung cấp thiết bị"; cột "Serial thiết bị làm dịch vụ"; dòng "Tổng cộng: X thiết bị"; STT lồng "gIdx.idx" + group header có số nhóm. Thiết bị cũ vẫn Sửa/Xóa (readonly=false), hàng xuất kho read-only.
- Verify: KH45 2 nhóm Tân Phát(14 external_old)+NCC khác(1); KH14272 Tân Phát(252)+NCC(0); KH41360 Tân Phát(1 thiết bị cũ, NCC label 'Tân Phát', sửa được)+NCC(0). php -l + parse PASS.

### Checkpoint — 2026-06-16 (Phase 4 HOÀN TẤT mọi gap hiển thị — D1/D2/D5 + Nhóm D chốt)
Vừa xong: D5 (cột serial mở rộng + In/Excel tab thiết bị), D2 (addSerialToInvoiceable), chốt D3/D4.
- D1 Tân Phát group (252sp=raw), D2 serial cho phiếu xuất (validate khớp ERP, rollback OK), D5 invoiceable_code (serial 3317→PYCXH-12414) + warranty best-effort + In/Excel (xlsx 25KB).
- D3 NGOÀI PHẠM VI (bắc cầu module Dịch vụ/Bảo hành HRM không có); D4 KHÔNG có UI ở ERP (commented) → bỏ đúng.
- FINAL integration smoke 11/11 PASS: 3 nhóm thiết bị, invoice_id, 2 export xlsx sinh thật, 6 route mới đăng ký. php -l + vtc/babel PASS toàn bộ (6 BE + 6 SFC).
KẾT LUẬN: mọi gap HIỂN THỊ/CHỨC NĂNG của màn quản lý KH đã parity ERP. Còn lại đều là (a) bridge module khác (D3), (b) ERP không hiển thị (D4, usage_status, ảnh sp), (c) sửa CustomerForm dùng chung cần duyệt (B2/B3), (d) ưu tiên thấp (B5 ảnh serial — data thật=0).
Bước tiếp: user verify browser toàn bộ + quyết B2/B3 (nếu cần KH nước ngoài) / D3 (nếu port module Dịch vụ).
Blocked: không.

### Checkpoint — 2026-06-16 (Phase 4 Đợt 3 B4 + C3 CODE DONE)
Vừa xong: parity test HRM↔ERP (A1/A4/C2/A3 khớp 5/5 dựng lại query ERP). B4 (gallery kéo-thả vuedraggable). C3 (In + Xuất Excel báo giá/hợp đồng — Export FromView + blade + route + FE In/Excel).
Verify: php -l + vtc/babel PASS toàn bộ; xlsx sinh thật (Excel::raw 16KB); export rows == documents total; documents() phân trang OK sau refactor buildDocumentsQuery.
Còn lại Phase 4: C1 (cascade quyền), Nhóm D (Tân Phát/phiếu xuất/dịch vụ — coupling sâu); B2/B3 (sửa CustomerForm dùng chung — cần user duyệt); B5 (ảnh serial — ưu tiên thấp).
Bước tiếp: user verify browser (In mở cửa sổ in, Xuất Excel tải file; cho phép popup) + quyết C1/D.
Blocked: không.

### Checkpoint — 2026-06-16 (Phase 4 Đợt 1 + Đợt 2 CODE DONE)
Branch: cả hrm-api + hrm-client đã checkout `test` (code 6 tab gốc nằm ở đây). Stash 1 thay đổi hideList ở tpe-develop-assign.
Vừa xong: rà soát parity ERP (3 agent) → Đợt 1 (A1/A3/A4/A5, A2 bỏ vì non-gap) + Đợt 2 (C2/C4).
- A1: NVKD/Phòng ban liên hệ (suy ra từ báo giá). A3: tăng SL thiết bị. A4: filter nhóm hàng (bản chạy thật, ERP gốc hỏng). A5: nhãn loại hình. C2: ẩn nháp dịch vụ. C4: filter công ty.
- Verify: php -l PASS toàn bộ BE; vtc+@babel parser PASS 6 SFC.
- SMOKE TEST DB ERP THẬT (dev_erp, read-only + A3 rollback) — PASS 2026-06-16: A1 contact 24035/KH33601 nvkd=7 NV + phongban=5 phòng (join+dedupe đúng); A3 addQuantity 1→4 rollback OK; A4 productGroups=878, lọc group_id=2129→1 sp; C2 documents wr_quotation KH33601=21 dòng (draft filter chạy); C4 companies=8. Tất cả cột ERP tồn tại (products.group_id, employee_infos.company_id, wr_*.status, *.customer_contact_id, employees.employee_info_id).
- CHUẨN HÓA V2Base (2026-06-16): thay raw `<input type="date">` → `V2BaseDatePicker` (DocumentTable 2 ô, EquipmentTab ngày xuất); ô tìm sản phẩm/NCC raw `<input>` → `V2BaseInput` (giữ search bằng @input + @click.native vì V2BaseInput không emit focus). File `type=file` ẩn ở OtherInfoTab giữ nguyên. vtc+babel PASS. Quy ước lưu memory feedback_v2base_elements.
- CÒN LẠI: user verify UI browser (xem checklist dưới).
Phát hiện đáng lưu ý (đổi tính toán scope): A2 = cột ERP đã drop (không gap); A4 dropdown ERP gốc nạp sai + không wire (hỏng); B1 = HRM inline đã đủ data, chỉ khác UX.
Đang làm dở: không.
Bước tiếp: chờ user quyết Đợt 3 (Nhóm B — UX nâng cao, giá trị thấp) và Đợt 4 (C1 cascade quyền + C3 In/Excel + Nhóm D Tân Phát/phiếu xuất/dịch vụ — effort lớn, coupling sâu module Kho+Dịch vụ ERP). Khuyến nghị: D nên tách đợt riêng, làm khi port luồng kho/dịch vụ.
Blocked: không có eslint/esbuild bin (dùng vtc+babel thay). Test DB ERP thật cần user chạy hrm-api.

### Checkpoint — 2026-06-10 (brainstorm done)
Vừa xong: khảo sát toàn bộ màn ERP (3 agent) + chốt scope (3 phase, full edit, route mới, tách Tab1/2, Tab6 đầy đủ). Spec + design + plan đã fill.
Bước tiếp: user duyệt design → bắt đầu code Phase 1 (BE trước: model gallery/video + show + media save).
Blocked: chưa có (FE build cần node_modules — verify cuối qua user).

### Checkpoint — 2026-06-10 (Phase 1 CODE DONE)
Vừa xong: Phase 1 đầy đủ BE (7/7) + FE (6/6).
- BE: 2 model Tp gallery/video; show() +galleries/videos/attachments; updateMedia/uploadCustomerImage/deleteAttachmentFile (CmcS3Helper, transaction mysql2); 3 route (upload-image đặt trước /{id} tránh nuốt route); DetailResource +3 field. php -l PASS.
- FE: CustomerForm thêm prop `tabbed` + `<component :is>` (b-tabs khi tabbed / div khi phẳng, DRY chung 1 state+save); di chuyển block Địa chỉ giao hàng vào Tab Thông tin chung; Tab1=chung+cá nhân/tổ chức+giao hàng, Tab2=liên hệ (ẩn khi cá nhân), Tab Thông tin khác=OtherInfoTab (ảnh/tài liệu/video). Placeholder Báo giá/Hợp đồng/Thiết bị. Trang `/:id/manager` + row action "Quản lý". 3 store action media.
- Verify: php -l PASS; vue-template-compiler + @babel/parser PASS cho 3 SFC + actions.js; BTab dùng inject→component:is đăng ký OK; bootstrap-vue/nuxt registered.
Đang làm dở: không.
Bước tiếp: user chạy hrm-client (npm dev) verify browser — mở `/assign/customers/:id/manager`: kiểm 6 tab hiển thị; Tab Thông tin chung/Liên hệ lưu (V2Footer); Tab Thông tin khác upload ảnh + tài liệu PDF + video → Lưu; kiểm add/edit cũ (`/add`, `/:id/edit`) KHÔNG bị ảnh hưởng (form phẳng), lưu ý Địa chỉ giao hàng giờ nằm trên mục Người liên hệ ở trang edit.
Blocked: không có eslint/esbuild bin để lint sâu (đã dùng vtc + babel parser thay thế).

### Checkpoint — 2026-06-10 (Phase 2 + Phase 3 CODE DONE)
Vừa xong: toàn bộ 6 tab.
- Phase 2 (Báo giá + Hợp đồng): CustomerManagerService.documents đọc ERP 4 bảng + join NV/phòng ban, filter ngày/NV/phòng ban, sum + phân trang; CustomerManagerController.documents/departments; routes. FE DocumentTable + QuotationsTab + ContractsTab gắn vào tab (lazy).
- Phase 3 (Thiết bị): 3 model Tp (equipments_old/external_equipments/serials); equipmentList (nhóm Thiết bị cũ + NCC khác, join products/brands/models/suppliers, kèm serials) + CRUD thiết bị (chặn trùng, chặn xóa theo 9 bảng luồng) + serial CRUD (thêm/sửa/đổi parent_id/xóa) + suppliers/search-products. Controller + routes (serial/* + manager/* đặt trước /{id}). FE EquipmentTab + 4 modal (product picker inline).
- Defer P3: hàng Tân Phát từ phiếu xuất, addSerialToInvoiceable, updateProductCustomer (tăng SL), submitUsageStatus, serial attachment, device_errors.
- Verify: php -l PASS toàn bộ BE; 8 class mới autoload OK (class_exists); vue-template-compiler + @babel/parser PASS 8 SFC FE. route:list không chạy được do lỗi có sẵn Module Decision (không liên quan).
Bước tiếp: user chạy hrm-api (migrate không cần — chỉ đọc/ghi ERP) + hrm-client npm dev → verify browser toàn bộ 6 tab.
Blocked: không.

### Checkpoint — 2026-06-10 (TEST với DB ERP thật — PASS, sửa 3 bug)
Đã test BE thật qua tinker (kết nối dev_erp), luồng GHI bọc transaction + rollback (KHÔNG để lại data):
- P1 media: updateMedia → galleries=2/videos=1/attachments=1, show() đọc lại OK.
- P2 documents: KH 33601 → báo giá hàng hóa 217 dòng, sum=117,132,912,101, người tạo "Đặng Ngọc Vinh" + phòng ban "PHÒNG THIẾT BỊ Ô TÔ 2" (join NV/phòng ban OK). 4 loại chứng từ chạy.
- P3 equipment: KH 45 → Thiết bị cũ 14 + NCC khác 1; searchProducts 30 kết quả; CRUD đầy đủ (addOld/updateOld/deleteOld + addExternal/deleteExternal + addSerial/updateSerial/changeSerial/deleteSerial) — ALL OK.
3 BUG phát hiện & đã sửa khi test:
1. FE V2BaseError dùng prop `message` (không phải `error`) → đổi 4 chỗ trong EquipmentTab.
2. NCC (supplier) ở ERP = `customers` có is_supplier (model Supplier $table='customers' + scope), KHÔNG phải bảng `suppliers` (rỗng). Sửa suppliers() đọc customers is_supplier (limit 50 + keyword search) + join supplier_name từ customers; FE đổi chọn NCC sang inline search.
3. serials.created_by + updated_by NOT NULL → currentUserId() resolve ERP employee id (ErpPermissionHelper::erpEmployeeId) + fallback created_by của KH; set cả created_by/updated_by khi insert serial.
Verify cuối: php -l PASS + 8 class autoload OK + vtc/@babel parser PASS 9 file FE. route:list KHÔNG chạy (lỗi sẵn Module Decision, không liên quan).
Còn lại: user verify UI trên browser.

---

## Phase 4 — Fix: ô Số lượng (modal Thêm/Sửa thiết bị) không cho nhập số âm

- [x] FE `EquipmentTab.vue` — chặn gõ/dán số âm ở ô **Số lượng** của modal thiết bị (`min`/`step` + chặn phím `-`,`+`,`e` + lọc lại giá trị khi input)
- [x] FE `EquipmentTab.vue` — tách thông báo lỗi: bỏ trống vs nhập 0 (trước đây cả 2 đều ra "Vui lòng nhập số lượng")
- [x] Verify: parse SFC (vue-template-compiler + @babel/parser) + mô phỏng bộ lọc với các chuỗi gõ/dán

### Checkpoint — 2026-08-11 (Phase 4)
Vừa hoàn thành: ô **Số lượng** trong modal Thêm/Sửa thiết bị (`EquipmentTab.vue`) không cho nhập số âm.

Hiện trạng cũ: `<V2BaseInput v-model="eqForm.qty" type="number">` — không có `min`, `type=number`
vẫn cho gõ `-`, `+`, `e`. Nhập `-5` chỉ bị chặn lúc bấm Lưu, lại báo sai là "Vui lòng nhập số lượng".

Cách sửa (3 lớp, chỉ FE):
1. `min="1" step="1"` — chặn ở nút tăng/giảm + constraint của trình duyệt
2. `@keydown.native="blockNegativeKey"` — chặn phím `-` `+` `e` `E` `.` `,`
3. `@input.native="onQtyInput"` — lọc lại giá trị (chặn đường **dán chuỗi**), lấy **cụm chữ số đầu tiên**

⚠️ 2 điểm dễ sai đã xử lý:
- Đổi `v-model` → `:value` + `@input.native`: cần chạm thẳng DOM input. Nếu chỉ gán lại `eqForm.qty`
  mà giá trị sau lọc trùng giá trị cũ thì Vue không render lại → ô nhập vẫn hiện ký tự vừa gõ.
  Vì vậy `onQtyInput` gán cả `event.target.value`.
- Lọc bằng `replace(/[^0-9]/g,'')` sẽ biến `3.5` thành `35` (lệch 10 lần) → dùng `match(/\d+/)`
  lấy cụm chữ số đầu tiên, `3.5` → `3`.

Verify (trích thẳng 2 hàm từ SFC ra chạy, không chép tay): template compile 0 lỗi, script parse PASS,
render fn có `nativeOn`; `-5`→5, `-0`→0, `3.5`→3, `-12abc`→12, `  -7 `→7; qty rỗng → "Vui lòng nhập
số lượng", qty=0 → "Số lượng phải lớn hơn 0".

⚠️ CÒN NỢ: **BE không validate qty** — `CustomerManagerService::addOldEquipment/updateOldEquipment`
nhận thẳng `$request->get('qty')` vào `TpEquipmentOld`. Gọi API trực tiếp vẫn lưu được số âm.
Chưa sửa vì user chỉ yêu cầu chặn ở ô nhập.

Đang làm dở: không có.
Bước tiếp theo: user chạy `npm run dev` hrm-client → mở `/assign/customers/43707/manager` tab Thiết bị
→ Thêm thiết bị cũ → thử gõ và dán số âm vào ô Số lượng.
Blocked: không có.

---

## Phase 5 — Gỡ khối "Serial (tùy chọn)" khỏi form Thêm thiết bị (parity ERP)

- [x] Đối chiếu ERP: xác nhận ERP đã gỡ khối nhập serial khỏi CẢ 2 modal thêm thiết bị
- [x] FE `EquipmentTab.vue` — xoá block `v-if="!eqIsEdit"` (label "Serial (tùy chọn)" + list input + nút "Thêm serial")
- [x] FE `EquipmentTab.vue` — bỏ `payload.addSerials` trong `submitEquipment()` + bỏ `addSerials: []` trong `emptyEqForm()`
- [x] Verify: vue-template-compiler compile 0 lỗi + @babel/parser PASS + render fn không còn tham chiếu `addSerials`
- [ ] User verify trình duyệt: `/assign/customers/43711/manager` → tab Thiết bị → Thêm thiết bị NCC khác / Thêm thiết bị cũ

### Checkpoint — 2026-08-12 (Phase 5)
Vừa hoàn thành: gỡ khối nhập serial ở form Thêm thiết bị (cả "thiết bị cũ" và "thiết bị NCC khác" — dùng chung 1 modal).

**Vì sao HRM có mà ERP không có** (điều tra trong repo `D:\laragon\www\erp`):
- Commit `0f76240` (11/04/2024, "cập nhật lại các file luồng sửa serial") **comment toàn bộ** khối
  `<tr ng-repeat="addSerial in addSerials">` + nút "Thêm serial" trong CẢ 2 modal `#externalEquipment`
  và `#oldEquipment` (`resources/views/customercare/customermanager/show_.blade.php`), đồng thời comment
  dòng `data.addSerials = $scope.addSerials` trong `submitExternalEquipment` (`handleJs.blade.php:144-149`).
- Commit `bf391cb` (17/04/2024) xoá hẳn đoạn comment đó.
- ⚠️ **BE ERP không được dọn theo**: `CustomerManagerController::addExternalEquipment()` (dòng 647-720) vẫn
  còn nguyên `foreach ($request->addSerials ...)` + validate "Số lượng serial không được vượt quá số lượng
  của thiết bị" (dòng 665) → **code chết**. Khi port sang HRM, phía HRM lấy BE ERP làm chuẩn parity nên
  dựng lại UI cho nhánh chết này (Phase 3, task P3-FE2 "serial khi thêm").
- Bản port cũng đã méo sẵn: ERP bản cũ khối serial có thêm cột **Vị trí (`space`)** + **file ảnh đính kèm**,
  HRM chỉ port mỗi ô `serial`.
- ⇒ Mô hình đúng của ERP hiện tại: tạo thiết bị trước, serial nhập sau qua modal riêng
  ("Thêm serial cho thiết bị cũ/ncc khác" `show_.blade.php:2615`, "Thêm serial cho phiếu xuất" dòng 2671).
  HRM đã có đủ 2 modal này → không mất chức năng gì.

BE HRM (`CustomerManagerService::addOldEquipment/addExternalEquipment` đọc `addSerials`) **giữ nguyên**,
không ai gọi nữa — đúng như ERP đang để. Xoá được nếu sau này dọn code.

Verify: template compile 0 lỗi, script parse PASS, render fn không còn `addSerials`, template không còn
"Serial (tùy chọn)".

⚠️ CÒN NỢ (phát hiện khi điều tra, CHƯA sửa vì ngoài scope yêu cầu):
`serialRowsFor()` (`CustomerManagerService.php:675`) lọc `->where('s.product_id', $productId)`. Với thiết bị
NCC khác tick **"Hàng công ty không bán"** thì `product_id = NULL` → SQL thành `s.product_id = NULL` →
không bao giờ khớp ⇒ serial của loại hàng này luôn hiện **Xem (0)** dù đã lưu trong bảng `serials`
(serial mồ côi, còn chiếm chỗ khiến lần sau nhập lại báo "đã tồn tại"). Fix: dùng `whereNull('s.product_id')`
khi `$productId` rỗng, kết hợp điều kiện `product_no_sale_name` đã có sẵn.

Đang làm dở: không có.
Bước tiếp theo: user mở `/assign/customers/43711/manager` tab Thiết bị, kiểm tra 2 popup thêm thiết bị
không còn ô Serial, và luồng thêm serial qua "Xem (n)" → "Thêm serial" vẫn chạy.
Blocked: không có.

---

## Phase 6 — Chuyển 2 ô picker trong modal thiết bị sang `V2BaseSelectRemote`

- [x] FE `EquipmentTab.vue` — ô **Nhà cung cấp** (chỉ có ở popup NCC khác): bỏ dropdown tự chế → `V2BaseSelectRemote` + `fetchSuppliers(keyword)`
- [x] FE `EquipmentTab.vue` — ô **Trang thiết bị** (dùng chung 2 popup): bỏ dropdown tự chế → `V2BaseSelectRemote` + `fetchProducts(keyword)`
- [x] FE — xoá state chết `productKeyword/productResults/supplierKeyword/supplierResults` + CSS `.product-dropdown/.product-item`
- [x] Verify: template compile 0 lỗi, script parse PASS, 2 ô `V2BaseSelectRemote`, không còn tham chiếu state cũ
- [ ] User verify trình duyệt

### Checkpoint — 2026-08-12 (Phase 6)
Vừa hoàn thành: 2 ô picker trong modal Thêm/Sửa thiết bị dùng đúng component chuẩn.

**Hiện trạng cũ**: cả 2 ô là `V2BaseInput` + `<div class="product-dropdown">` tự dựng tay
(Phase 3, 16/06/2026). Trong CÙNG modal thì ô "Tình trạng thiết bị" lại dùng `V2BaseSelectInModal`
→ 2 kiểu UI lệch nhau.

**Vì sao lúc đó không dùng `V2BaseSelectInModal`**: component này chỉ nhận `options` TĨNH, search
client-side. NCC có **~6900 bản ghi** (`CustomerManagerService.php:726`, BE `limit(50)` theo keyword),
sản phẩm cũng `limit(30)` → không nạp hết vào options được.
**Nhưng** repo đã có sẵn `components/V2BaseSelectRemote.vue` (select2 + ajax, tự set
`dropdownParent = .modal-content` để không bị focus-trap của b-modal cướp focus), tạo **23/04/2026** —
trước màn này 2 tháng. Component cha `CustomerForm.vue` (bọc chính `EquipmentTab`) đã dùng nó.
⇒ Đây là thiếu sót lúc port, không phải giới hạn kỹ thuật.

**Lợi ích thu được** (đều là khiếm khuyết của bản tự chế): debounce 300ms thay vì gọi API mỗi ký tự ·
select2 huỷ request cũ nên hết race-condition gõ nhanh · click ra ngoài / Esc đóng dropdown · điều hướng
bằng phím ↑↓ Enter · nút × xoá lựa chọn (`allowClear`) · giá trị đã chọn hiện TRONG ô (trước đây chỉ nằm ở
`placeholder` + dòng "Đã chọn: …" nên mở form Sửa nhìn như chưa chọn gì).

⚠️ Ô **Trang thiết bị** dùng chung 2 popup → popup "Thêm mới thiết bị cũ" cũng đổi theo (đúng ý đồ).
Nhánh tick "Hàng công ty không bán" giữ nguyên `V2BaseInput` nhập tay, không đụng.

2 điểm dễ sai đã xử lý:
- Option text hiển thị "MÃ - Tên" (giống dropdown cũ) nhưng `eqForm.product_name` phải là tên THUẦN →
  thêm cache `productSearchCache` để tra ngược theo id trong `onSelectProduct`, không cắt chuỗi.
- `initialOption` để hiện sẵn nhãn khi mở form **Sửa** — không có nó thì select2 chỉ có value, hiện ô rỗng.

BE **không sửa gì**: `assign/customers/manager/suppliers?keyword=` và `.../search-products?keyword=`
đã đúng dạng `[{id, name, code}]` mà `fetchFn` cần.

Verify: vue-template-compiler compile 0 lỗi · @babel/parser PASS · template có đúng 2 `<V2BaseSelectRemote>` ·
0 tham chiếu còn sót tới `productKeyword/productResults/supplierKeyword/supplierResults/onProductSearch/
onSupplierSearch/selectProduct/selectSupplier` · CSS `.product-dropdown`/`.product-item` đã xoá.

Đang làm dở: không có.
Bước tiếp theo: user mở `/assign/customers/43711/manager` tab Thiết bị → Thêm thiết bị NCC khác:
gõ tìm NCC + sản phẩm, chọn, bấm ×, mở Sửa xem có hiện sẵn tên NCC/sản phẩm không.
Blocked: không có.

---

## Phase 7 — Ảnh letterhead đầu trang IN (tab Báo giá / Hợp đồng / Trang thiết bị)

- [x] BE `CustomerManagerService::companyHeader()` — `companies.header` của công ty người đang in, ghép `ERP_URL` thành URL TUYỆT ĐỐI, trả `''` nếu thiếu
- [x] BE `CustomerManagerController::printHeader()` + route `GET assign/customers/manager/print-header`
- [x] FE `utils/assign/customer-print-header.js` — `loadCustomerPrintHeader(store)` (nhớ kết quả, gọi API 1 lần) + `printHeaderImgTag(url)`
- [x] FE `DocumentTable.vue` (dùng cho CẢ tab Báo giá + Hợp đồng, 4 instance) — nạp header lúc mounted, chèn `<img>` đầu `<body>` trước `<h3>`
- [x] FE `EquipmentTab.vue` — tương tự cho `printList()`
- [x] Verify: `php -l` 3 file BE · route resolve đúng controller · smoke tinker ra URL thật · SFC compile/parse PASS · chạy thật `printHeaderImgTag`
- [ ] User verify trình duyệt (xem lưu ý môi trường bên dưới)

### Checkpoint — 2026-08-12 (Phase 7)
Vừa hoàn thành: 3 bản in của màn Quản lý KH có ảnh letterhead đầu trang, cùng nguồn dữ liệu với
bản in "Yêu cầu chuyển hàng" (`ProductTransferRequestService::buildPrintData` → `HEADER`).

**Nguồn ảnh**: `companies.header` của **công ty NGƯỜI ĐANG IN** (`auth()->user()->info->company_id`).
Khác phiếu Yêu cầu chuyển hàng (lấy theo công ty NGƯỜI TẠO PHIẾU) vì 3 tab này là **báo cáo danh sách**,
không gắn với chứng từ của công ty nào. Cùng khuôn `AccountService::companyHeader()`.

⚠️ **Bắt buộc URL TUYỆT ĐỐI** (skill print-page mục 4): `companies.header` lưu đường dẫn tương đối
`/uploads/xxx.png` trên server ERP. Cửa sổ in mở bằng `window.open('')` có base `about:blank` → đường dẫn
tương đối vừa 404 (mất ảnh) vừa làm `onload` không nổ ⇒ **không tự bật hộp thoại in**. Nên BE ghép `ERP_URL`.

⚠️ **Không được `await` trước `window.open`** — trình duyệt chặn popup. Vì vậy header **nạp sẵn lúc mounted**
vào `printHeaderUrl`, hàm in giữ nguyên đồng bộ. Util nhớ kết quả (module-scope promise) vì 3 tab dựng tới
**5 instance** bảng (Báo giá 2 + Hợp đồng 2 + Thiết bị 1) — nếu mỗi cái tự gọi thì dư 5 request cùng giá trị.

Chống vỡ: ảnh 404/bị xóa → `onerror="this.style.display='none'"` (không dính icon ảnh vỡ, `onload` vẫn nổ
nên vẫn tự bật hộp thoại in). Công ty chưa có ảnh / chưa cấu hình `ERP_URL` → trả `''` → không chèn thẻ
`<img>`, bản in ra y như trước.

Verify: `php -l` PASS 3 file · route resolve `GET api/v1/assign/customers/manager/print-header` →
`CustomerManagerController@printHeader` · tinker (auth TpEmployee 13, company 1) trả
`http://erp.test:8080/uploads/1751696586ts-hn.png` · 2 SFC compile 0 lỗi + script parse PASS ·
chạy thật `printHeaderImgTag`: có URL → thẻ img đúng, rỗng → chuỗi rỗng, `"` trong URL được escape.

🖥️ **Lưu ý môi trường (không phải lỗi code)**: máy local có `ERP_URL=http://erp.test:8080` nhưng
`erp/public/uploads/` **rỗng** → ảnh 404 và bị ẩn, in ra không thấy letterhead. Bản in Yêu cầu chuyển hàng
cũng vậy trên máy này. Muốn thấy ảnh khi test local: copy file vào `erp/public/uploads/` hoặc trỏ `ERP_URL`
sang ERP thật.

Đang làm dở: không có.
Bước tiếp theo: user mở `/assign/customers/43711/manager` → tab Báo giá / Hợp đồng / Trang thiết bị → bấm In.
Blocked: không có.

---

## Phase 8 — Parity ERP: thiếu ô "Hàng công ty tương đương" khi tick "Hàng công ty không bán"

User báo: popup **Thêm mới thiết bị NCC khác**, khi tick "Hàng công ty không bán" thì các trường
khác với popup ERP. Đối chiếu `erp/resources/views/customercare/customermanager/show.blade.php:1074-1196`
(modal `#externalEquipment`): ERP có thêm trường **"Hàng công ty tương đương" (\*)** — picker sản phẩm,
chỉ hiện khi tick, và **ghi thẳng vào `product_id`** (`show.blade.php:1407-1411` `addProductEquiValent`),
BE ERP bắt buộc `product_id => required|exists:products,id` kể cả khi đã tick
(`AddExternalEquipmentRequest.php:32`). HRM thiếu ô này → lưu ra `product_id = NULL`,
`product_name = ''` (cột NOT NULL nhưng MySQL không bật STRICT nên nuốt thành rỗng).
Hệ quả: check trùng theo `product_id` mất tác dụng, thiết bị rơi vào nhóm "Chưa phân nhóm"
(nhóm theo `products.group_id`), serial gắn theo `product_id` cũng lệch.
Dữ liệu thật xác nhận ý đồ ERP: 2.600 dòng `external_equipments`, 1.300 dòng hàng không bán
nhưng chỉ 27 dòng `product_id` rỗng.

Phạm vi user chốt: **thêm ô còn thiếu + siết validate BE**. KHÔNG xếp lại thứ tự trường,
KHÔNG sửa nhãn (giữ "(\*)" ở Nhà cung cấp và chữ "(tháng)" ở Thời gian sử dụng), KHÔNG đụng dữ liệu cũ.

- [x] P8-FE1: `EquipmentTab.vue` — thêm ô **Hàng công ty tương đương (\*)**, hiện khi
      `eqModalType === 'external_equipment' && eqForm.product_no_sale`, đặt full-width ngay dưới ô
      "Trang thiết bị" (giữ layout 2 cột hiện có). Ghi vào `eqForm.product_id`.
- [x] P8-FE1b: cách chọn = **popup tìm hàng hóa** như ERP (user chốt, sau khi bản đầu dùng `V2BaseSelectRemote`):
      ô chỉ đọc + nút kính lúp → **dùng lại `pages/customer-care/services/components/ProductSearchModal.vue`**
      của màn Gói bảo dưỡng, prop `addOnRowClick` (click 1 dòng là chọn). KHÔNG sửa gì trong component đó.
      Đặt popup NGOÀI `b-modal` thiết bị + thêm `no-enforce-focus` cho `b-modal` (focus-trap của b-modal
      cướp focus ô tìm kiếm — tiền lệ `pages/human/districts/components/DistrictModel.vue:2`)
- [x] P8-FE1c: ô hiển thị hàng tương đương dùng **V2Base** (user yêu cầu): `V2BaseInput` (`readonly` + `hasSuffix`,
      click mở popup) — bỏ `input-group` + `<input>`/`<button>` thuần Bootstrap.
      Nút kính lúp: làm rồi nhưng **user yêu cầu bỏ** → chỉ còn ô, bấm vào ô là mở popup. Style scoped `.eq-picker-input ::v-deep .v2-input { cursor: pointer }` (UA stylesheet ép
      `cursor: text` cho input nên phải nhắm thẳng `.v2-input`, không thể trông vào kế thừa từ wrapper)
- [x] P8-FE2: `validateEquipment()` — khi đã tick thì bắt buộc `product_id`, lỗi inline `V2BaseError`
- [x] P8-FE3: `openEdit()` + `emptyEqForm()` + `onSelectProduct()` — thêm `equivalent_product_name`
      để preload đúng nhãn picker khi mở form Sửa
- [x] P8-BE1: `CustomerManagerService::buildExternalRows()` — trả thêm `equivalent_product_name`
      (tên thật join từ `products`; key `product_name` đang bị ghi đè bằng `product_no_sale_name`)
- [x] P8-BE2: `addExternalEquipment()` + `updateExternalEquipment()` — validate như ERP:
      `product_id` required + exists, `product_no_sale_name` required khi tick, `qty` required|integer|min:1;
      ném `ValidationException` (wrapper `equipmentAction()` đã rethrow sẵn → 422 chuẩn)
- [x] P8-V: Verify — `php -l`, compile SFC, gọi service qua tinker trên KH thật (có rollback)

### Checkpoint — 2026-08-13 (Phase 8)
Vừa hoàn thành: bổ sung ô "Hàng công ty tương đương" (parity ERP) + siết validate BE cho thiết bị NCC khác.
- FE `EquipmentTab.vue`: ô mới `V2BaseSelectRemote` v-model `eqForm.product_id`, hiện khi `external_equipment` + đã tick;
  `equivalent_product_name` thêm vào `emptyEqForm/openEdit/onSelectProduct` (2 ô picker dùng chung `product_id` nên
  chọn ở ô nào cũng cập nhật nhãn ô kia); `validateEquipment()` chặn thiếu hàng tương đương khi đã tick.
- BE `CustomerManagerService`: `validateExternalEquipment()` dùng chung cho add + update
  (product_id required|integer|exists, product_no_sale_name required khi tick, qty required|integer|min:1),
  message tiếng Việt đổi theo trạng thái tick; `buildExternalRows()` trả thêm `equivalent_product_name`.
⚠️ Bẫy đã dính và đã sửa: rule `exists:<db>.products,id` — Laravel đọc "a.b" là **connection**.table
  chứ không phải database.table → phải để trần `exists:products,id` (products nằm trên connection mặc định).
Verify (chạy thật trên DB `gop_db`): php -l PASS · SFC compile 0 lỗi + script parse PASS ·
  tinker 6 case add (tick thiếu product_id → "Vui lòng chọn hàng công ty tương đương"; không tick thiếu →
  "Vui lòng chọn trang thiết bị"; product_id ma → "không tồn tại"; qty=0 → chặn; hợp lệ → tạo được, rollback) ·
  2 case update (thiếu product_id → 422; hợp lệ → ok, rollback, bản ghi NGUYÊN VẸN) ·
  `buildExternalRows` KH7620: product_name='Máy cân bằng động HM30BU' vs
  equivalent_product_name='Máy cân bằng động ngang gối cứng HM4BU' → đúng 2 tên khác nhau, chứng minh cần field riêng.
Đang làm dở: không có.
Bước tiếp theo: user mở `/assign/customers/<id>/manager` → tab Trang thiết bị → "Thêm thiết bị NCC khác" →
  tick "Hàng công ty không bán" → kiểm tra ô "Hàng công ty tương đương" + thử lưu khi bỏ trống.
Blocked: không có (tài khoản dev 0 quyền nên không tự bấm UI được — route gắn `erpPermission:Sửa khách hàng`).

### Checkpoint — 2026-08-13 (Phase 8 — đổi sang popup tìm hàng hóa)
Vừa hoàn thành: user chỉ ra ERP dùng **popup tìm kiếm hàng hóa** (`#searchProductEquivalent`) cho ô này,
không phải dropdown. Đã đổi ô "Hàng công ty tương đương" sang ô chỉ đọc + nút kính lúp mở popup.
**Tái dùng `ProductSearchModal.vue` của màn Gói bảo dưỡng** (user chỉ định) — 17 bộ lọc + phân trang
+ 12 cột, gọi `customer-care/services/search-products` + `product-catalogs` (2 route CHỈ có `auth:api`,
không gắn `checkPermission` → dùng được từ màn khách hàng). Component đó **không bị sửa 1 dòng nào**
(`git diff --name-only` chỉ có EquipmentTab.vue).
Quyết định giữ nguyên: ô **Trang thiết bị** (khi KHÔNG tick) vẫn là `V2BaseSelectRemote` theo Phase 6 —
user chốt chỉ đổi riêng ô Hàng tương đương, chấp nhận 2 kiểu chọn trong cùng modal.
⚠️ Bẫy đã xử lý: `b-modal` bẫy focus (focusin → kéo về .modal-content) sẽ làm không gõ được vào ô tìm
kiếm của popup con → thêm `no-enforce-focus`, và render popup NGOÀI `b-modal`.
📌 Còn lệch (chấp nhận, do tái dùng nguyên trạng): popup giữ tiêu đề "Chọn hàng hóa áp dụng",
cột checkbox và nút "Thêm N hàng hoá" của chế độ chọn nhiều — ô này chỉ lấy phần tử đầu.
Muốn bỏ thì phải thêm prop vào component dùng chung ⇒ cần hỏi trước theo quy tắc dự án.
Verify: 2 SFC compile 0 lỗi + script parse PASS · route `customer-care/services/{search-products,product-catalogs,search-models}`
tồn tại, middleware group chỉ `auth:api`, 3 method có trong `ServiceController`.
(`php artisan route:list` không chạy được do lỗi SẴN CÓ của `PermissionHelper.php:23` khi chạy CLI — không liên quan thay đổi này.)
Đang làm dở: không có.
Bước tiếp theo: user test trình duyệt — tick "Hàng công ty không bán" → bấm kính lúp → popup tìm hàng hóa
mở đè lên modal thiết bị, gõ tìm được, click 1 dòng → tên hàng điền vào ô → lưu.
Blocked: không có.
