# Design — Port màn "Hợp đồng vận chuyển" (DeliveryContract) ERP → HRM

> **Phân hệ:** Vận chuyển (Module Transport). **Nguồn:** `ERP/TanPhatDev` (Laravel 6, guard web, AngularJS+Blade) — READ ONLY.
> **Đích:** `HRM/hrm-api` (Laravel 8, guard api, LOCAL) + `HRM/hrm-client` (Nuxt 2/Vue 2, V2Base).
> **Nhánh:** `develop` (gop_db), DB gộp `erp_hrm_check`.
> **Khảo sát gốc:** `scratchpad/erp-delivery-contract-survey.md` (11 mục, đã đọc trọn).

---

## 1. Mục đích & vị trí trong chuỗi

Hợp đồng vận chuyển là **mắt cuối** của chuỗi giá vận chuyển đã port:

**Báo giá VC (DeliveryQuotation) → THGVC (DeliveryCostSummary) → BGHLVC (PriceListValidDelivery) → Hợp đồng vận chuyển (DeliveryContract)**

Khi duyệt THGVC sẽ sinh/cập nhật BGHLVC ([[hrm-bghlvc-port-readonly-done]], [[hrm-thgvc-port-done]]). Hợp đồng vận chuyển được **lập từ một BGHLVC** (chọn qua dropdown), chốt cứng (snapshot) thông tin NCC/tài khoản/giá, rồi gửi duyệt. Sau khi làm xong màn này, bước kế tiếp (ngoài phạm vi design này) là **"nối logic các màn lại với nhau"** — trong đó nút "Lập hợp đồng vận chuyển" đang là placeholder ở màn THGVC chi tiết + danh sách sẽ được đấu nối.

> **Nguyên tắc port (CLAUDE.md + skill `erp-to-hrm-screen`):** bám ERP 1:1 về **hành vi** (cột, lọc, hành động, ai-làm-gì, trạng thái); bám HRM về **hình thức** (V2Base, màu, thứ tự nút, thông báo). Port trung thành hành vi "lạ" của ERP KHÔNG phải lỗi; đưa vào sai lệch hành vi mới MỚI là lỗi. **Adaptation HRM bắt buộc đè chỉ dẫn ngược** (gate fail-closed ở BE, chặn khóa ở BE, số quốc tế, ngày dd/mm/yyyy, file qua bảng `files`, thông báo theo template HRM).

---

## 2. Quyết định đã chốt (user chốt 2026-10-29: "theo đề xuất, port trung thành ERP trước, lỗi sửa sau")

| # | Quyết định | Chốt |
|---|---|---|
| **A** | **Nguồn lập HĐ = BGHLVC** (PriceListValidDelivery), như code ERP đang chạy thật. KHÔNG lập trực tiếp từ THGVC. Việc đấu nút "Lập HĐ" ở THGVC là bước "nối logic các màn" sau này. | ✅ |
| **B** | **HĐ chính = HEADER-ONLY** (B1): không lưu ma trận xe/tải/tuyến khi tạo/sửa (giữ nguyên hành vi `syncDetails`/`warehouses` comment của ERP). Ma trận giá thật nằm ở **Phụ lục** + **Import Excel**. **Bổ sung chống crash**: mọi đường đọc chi tiết (export/print/`details_table`) phải trả rỗng an toàn khi HĐ không có vehicles/payloads/roads. | ✅ |
| **C** | **Tạo bộ quyền MỚI guard `api`** nhóm "Hợp đồng vận chuyển", **3 mức Xem** (tổng cty / cty / phòng ban) y như THGVC. **Lọc theo company_id** (sửa bẫy ERP không lọc → xem chéo cty). Quyền **Duyệt dùng lại "Duyệt giá vận chuyển"** đã có (ERP cũng dùng chung chuỗi này). | ✅ |
| **D** | **Giữ closeContract**: 1 NCC + trùng kho → tự đóng (status=4) các HĐ cũ trùng kho khi duyệt/đổi kho. Điều kiện theo loại xe (ERP đã comment) KHÔNG thêm. | ✅ |
| **E** | **Giữ cơ chế Phụ lục**: phụ lục duyệt → ghi đè/bổ sung bảng giá Final của HĐ gốc + cập nhật `final_min_extra_km`. | ✅ |
| **F** | **Giữ Import Excel** ma trận cho Phụ lục. Khuôn import chuẩn HRM (`import-excel` skill). Khớp theo **id/mã** thay vì tên (sửa bẫy ERP khớp fuzzy theo tên) — nếu không có mã trong file thì fallback theo tên như ERP. | ✅ |
| **G** | **Bỏ rác ERP khi port**: route `create2` (chết), cột di sản `delivery_cost_summary_id`/`delivery_cost_summary_quotation_id` (không ghi), `checkCloseContract` (logic chết tham chiếu cột di sản → viết lại theo supplier_id hoặc bỏ). | ✅ |

**Adaptation HRM bắt buộc (đè ERP, áp cho cả màn này):**
- `catch (\Exception $e)` / `\Throwable` (ERP thiếu `\` là bug Laravel 6 — HRM không chép).
- File đính kèm qua bảng **`files`** chung (`table='delivery_contracts'` + `table_id`), KHÔNG cột `attachments` chuỗi, KHÔNG S3-unlink-local.
- Số hiển thị chuẩn quốc tế `1,234,567.89` mọi nơi (bảng, form, in, Excel). Ngày `dd/mm/yyyy`.
- Badge màu + chữ do BE trả (`status_color` + `status_text`). Dùng 9 mã màu chuẩn HRM.
- Thông báo theo template `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}` + deep-link ID (skill `notification-convention`).
- Bản ghi khóa/sai trạng thái: chặn ở BE (423/422), FE ẩn nút (v-if).
- Mã tự sinh theo pattern HRM: giữ tiền tố ERP **`HĐVC-`** cho HĐ, **`...:PL-NN`** cho phụ lục (để khớp dữ liệu/in cũ), sinh qua `getNextCode()`-style.

---

## 3. Mô hình trạng thái (giữ y ERP)

| status | Hằng (đặt khi port) | Nhãn | Màu HRM |
|---|---|---|---|
| 0 | `DA_HUY` | Đã hủy | `#DC2626` (từ chối/khóa) |
| 1 | `DA_DUYET` | Đã duyệt | `#16A34A` (hoàn thành) |
| 2 | `CHO_DUYET` | Chờ duyệt | `#D97706` (chờ duyệt) |
| 3 | `DANG_TAO` | Đang tạo | `#64748B` (nháp) |
| 4 | `DONG` | Đóng | `#6B7280` (đã đóng) |

`type`: 1 = `HOP_DONG`, 2 = `PHU_LUC`.

**Luồng:** store→3 (nháp) / 2 (gửi duyệt ngay). send→2. approve(1)→ sinh Final* + closeContract + notify người tạo. approve(3)=từ chối (bắt buộc `approver_comment`)→ về 3 + notify. delete→0 (chỉ status=3 + chính chủ). closeContract tự đặt status=4 cho HĐ khác trùng kho cùng NCC.

> ERP không khai hằng status trong model (magic number). HRM khai hằng rõ ràng trên Entity.
> ERP filter list thiếu option "4 Đóng" → **HRM bổ sung** đủ 5 trạng thái vào ô lọc.

---

## 4. Database — ánh xạ bảng (GHI THẲNG bảng sẵn có nếu đã tồn tại trong DB gộp)

Kiểm tra trong `erp_hrm_check` xem các bảng `delivery_contract*` đã có chưa (ERP đã tạo từ migration 2020-2021). **Nếu đã có → dùng lại, chỉ thêm cột nếu thiếu** (quy tắc gop_db). Nếu chưa có → migration tạo mới theo cấu trúc ERP + convention HRM (company_id/department_id/part_id, created_by/updated_by, timestamps).

| Bảng | Vai trò | Ghi chú port |
|---|---|---|
| `delivery_contracts` | HĐ + Phụ lục (type 1/2) | Giữ cột snapshot. **Bỏ dùng** `delivery_cost_summary_id`, `delivery_cost_summary_quotation_id` (di sản). Thêm `company_id`/`department_id`/`part_id` nếu thiếu (để lọc scope). `created_by`/`updated_by` = `auth()->id()` (employees.id). |
| `delivery_contract_vehicles` | tầng xe (vehicle_category_id) | chỉ ghi khi Phụ lục/Import |
| `delivery_contract_vehicle_payloads` | tầng trọng tải (vehicle_payload_id, extra_price) | |
| `delivery_contract_vehicle_payload_roads` | tầng tuyến (road_id, km, cost) | denormalize vehicle_category_id/vehicle_payload_id |
| `final_delivery_contract_vehicle_payload_roads` | snapshot giá "chốt" sau duyệt | KHÔNG có parent_id; phụ lục ghi đè Final của HĐ gốc |
| `delivery_contract_has_warehouses` | pivot kho xuất phát | gán qua updateWarehouse sau duyệt |
| `files` (dùng chung) | file đính kèm | `table='delivery_contracts'`, `table_id` |

**Cột snapshot chốt cứng lúc tạo (giữ y ERP, đừng join live):** `company_account_number/name`, `company_bank_name/branch`, `supplier_address`, `supplier_account_number`, `supplier_bank`, `identity_card_number/date/place`, `tax_code`, `deputy_id/name/role`, `min_extra_km`, `final_min_extra_km`, `template`.

**Bẫy bảng:** `supplier_id` trỏ bảng **`customers`** (Supplier model = customers + is_supplier), KHÔNG bảng `suppliers`. Validate `exists:customers,id`.

---

## 5. Backend (hrm-api/Modules/Transport)

### 5.1 Entities
- `DeliveryContract` (extends BaseModel) — hằng status/type, quan hệ: `supplier()` (Supplier=customers), `approver()`, `warehouses()` (belongsToMany pivot), `vehicles()`, `roads()` (hasManyThrough xuống roads), `annexes()`/`parent_contract()`, `files()`, `finalRoads()`, `company()`. Accessor `warehouses_name`. Method nghiệp vụ: `canEdit/canAnnex/canAnnexEdit/canUpdateWarehouse/canDelete/canApprove` (giữ logic ERP: chính chủ + trạng thái; canApprove = quyền "Duyệt giá vận chuyển" + status=2). `getNextCode()`.
- `DeliveryContractVehicle`, `DeliveryContractVehiclePayload`, `DeliveryContractVehiclePayloadRoad`, `FinalDeliveryContractVehiclePayloadRoad`, `DeliveryContractHasWarehouse` (hoặc dùng pivot thuần).
- `syncDetails($vehicles, $roads)` port y ERP (xóa cũ → tạo lại 4 tầng, roads dùng chung theo index, cost theo ô, extra_price theo payload).

### 5.2 Service `DeliveryContractService` (CORE)
- `createFromPriceList` / `store` / `update` (HĐ header-only: snapshot account + NCC theo loại cá nhân/tổ chức; **KHÔNG** syncDetails/warehouses).
- `annexStore` / `annexUpdate` (Phụ lục: validate đầy đủ ma trận, copy snapshot từ parent, sync kho = kho parent, `syncDetails` thật).
- `send` (status 2 + notify người có quyền "Duyệt giá vận chuyển" theo company người tạo).
- `approve` (status 1: set approver, `closeContract`, sinh Final*; status 3: từ chối + comment; notify người tạo).
- `closeContract` (D: đóng HĐ khác cùng supplier + trùng kho).
- `updateWarehouse` (gán kho sau duyệt + closeContract).
- `importExcel` (F: parse ma trận cho phụ lục, khớp theo id/mã, khuôn `import-excel`).
- `destroy` (status=3 + chính chủ → status=0).
- `exportRows` / `printData` / `printListData` (**chống crash khi HĐ rỗng chi tiết** — trả mảng/bảng rỗng an toàn).
- Phạm vi dữ liệu (`scoped()`): lọc theo quyền 3 mức + **company_id** (sửa bẫy ERP). Người xem phiếu đã đóng dấu duyệt/từ chối vẫn thấy; super-admin/quyền tổng cty không bó company_id.

### 5.3 Controller `DeliveryContractController` (V1)
Route (bỏ `create2`): index(của tôi) / all(tất cả) / show / store / update / annexStore / annexUpdate / getDataForAnnex / send / approve / destroy / updateWarehouse / importExcel / exportList / printData / printListData / searchData(nếu cần) / form-options. Gate bằng `checkPermission` + re-check `isCurrentEmployeeHasPermission` cho endpoint nhạy cảm. Chặn khóa/sai trạng thái ở đầu hàm (423/422) — nếu dùng FormRequest thì guard ở middleware route (khuôn `CheckCustomerNotLocked`).

### 5.4 FormRequest (chỉ `rules()`, KHÔNG `messages()`)
`StoreRequest`, `UpdateRequest`, `AnnexStoreRequest`, `AnnexUpdateRequest`, `ApproveRequest` (khai đủ id các tầng nếu `validated()` dùng — **bẫy đã trả giá ở THGVC Task 14**), `UpdateWarehouseRequest`, `ImportRequest`. Rethrow `ValidationException`.

### 5.5 Transformer
`DeliveryContractListResource` (status_text/color, supplier/kho/người duyệt/ngày, cờ `is_can_*`), `DeliveryContractDetailResource` (header + ma trận nếu có + Final + kho + files + cờ hành động). Eager load chống N+1.

### 5.6 Permission seeder (guard api, nhóm "Hợp đồng vận chuyển", `type` = phân hệ Vận chuyển)
Khai `$this->perm([...])` (KHÔNG id/guard_name). Dự kiến: **Xem (3 mức: tổng cty/cty/phòng ban)**, Thêm, Sửa, Xóa, Lập phụ lục, Cập nhật kho, In, Xuất Excel, Import. **Duyệt = dùng lại "Duyệt giá vận chuyển"** (không tạo mới). Xác nhận bộ quyền chi tiết trong plan. Verify `permission:sync --dry-run`.

---

## 6. Frontend (hrm-client/pages/transport/delivery-contracts)

- `index.vue` — DS "của tôi" (created_by=self, mọi trạng thái). 4 mixin chuẩn list-page. Cột: STT, Mã (nuxt-link; phụ lục hiện dòng "Phụ lục cho HĐ <mã gốc>"), NCC, Kho, Người duyệt, Ngày duyệt, Người tạo, Ngày tạo, Trạng thái, Hành động. Lọc: Mã, NCC, Kho, Người tạo, Người duyệt, Trạng thái (đủ 5 option). Hành động/điều kiện: Tạo phụ lục (canAnnex), Sửa (canEdit/canAnnexEdit), Xóa (canDelete), Cập nhật kho (canUpdateWarehouse), In/In bảng kê/Xuất (luôn hiện). Nút ẩn hẳn khi không đủ điều kiện (v-if).
- `all.vue` (hoặc `index.vue?type=all`) — DS "tất cả" (status!=3), cho người duyệt. Phân hệ chính (menu `all`) quyết định type quyền + scope.
- `create.vue` / `_id/edit.vue` + `ContractForm.vue` — form HĐ header-only: NCC, min_extra_km, chọn BGHLVC (edit thì disable), nhánh cá nhân (CMT/ngày/nơi cấp) / tổ chức (MST/người đại diện/chức vụ), tài khoản công ty, ghi chú, file (V2BaseFile/FileAttachmentTable), mẫu in theo loại NCC. V2Base-only.
- `annex/create.vue` + `_id/edit.vue` + `AnnexForm.vue` + `ImportModal.vue` — phụ lục có ma trận xe/tải/tuyến đầy đủ + import Excel. Chọn HĐ gốc (modal, canAnnex). Sửa chỉ khi status=3.
- `_id/index.vue` — chi tiết: header + tab ma trận (nếu có) + Final + kho + files. Footer `V2Footer` + `#custom-actions`: Duyệt (is_can_approve), Sửa, Xóa, Lập phụ lục, Cập nhật kho, In, In bảng kê, Xuất Excel — **khớp hành động & điều kiện với danh sách**. Modal Duyệt (base-confirm-modal / V2BaseModal), modal Cập nhật kho, modal Import.
- In: theo skill `print-page` — nút In mở **popup xem trước** (BE trả `print-data`/`print-list-data` dựng HTML từ mẫu ReportTemplate ERP: `HOP_DONG_VAN_CHUYEN` / `..._TO_CHUC` / `PHU_LUC_...` / `BANG_KE_GIA_CUOC_VAN_CHUYEN`). Logo theo `company_id` ghi trên chứng từ.
- Menu: `components/subsystem-menu/transport.js` — thêm mục "Hợp đồng vận chuyển" (isShow = mảng 3 quyền Xem).
- Tiêu đề chi tiết: `Chi tiết hợp đồng vận chuyển: <mã>`. Sau thao tác → `markFormSaved()` + về danh sách.

---

## 7. Đấu nối THGVC (ghi nhận, THỰC THI Ở BƯỚC SAU — ngoài phạm vi plan port này trừ khi user chốt gộp)

Nút "Lập hợp đồng vận chuyển" (placeholder toast "Tính năng chưa phát triển") ở `pages/transport/delivery-cost-summaries/_id/index.vue:208` + row-action ở list. Khi "nối logic các màn": nút điều hướng sang `create.vue` của HĐ, HĐ chọn BGHLVC (BGHLVC sinh từ chính THGVC khi duyệt). Cờ `is_can_create_contract` đã có sẵn ở Resource THGVC. (THGVC M1 — giữ/bỏ row-action trên LIST — vẫn mở, không chặn việc này.)

---

## 8. Bẫy phải né khi port (từ khảo sát §11)

1. `supplier_id` → bảng `customers`, không phải `suppliers`.
2. Cột snapshot chốt cứng — giữ y, đừng join live.
3. Cột di sản THGVC + `checkCloseContract` chết — **bỏ/viết lại theo supplier_id** (G).
4. `create2` chết — bỏ (G).
5. `syncDetails`/`warehouses` comment ở store/update (B1 giữ) → **nhưng export/print/`details_table` phải chống crash khi rỗng**.
6. Import khớp theo tên — HRM đổi sang id/mã (F).
7. `catch (Exception)` thiếu `\` — HRM dùng `\Exception`/`\Throwable`.
8. List/search không lọc company_id — HRM **lọc** (C).
9. `deleteFile` unlink local dù S3 — HRM dùng bảng `files` chung + xóa đúng cơ chế HRM.
10. Final* không có parent_id; phụ lục ghi đè Final của HĐ gốc — giữ (E).
11. canApprove không check cùng công ty — giữ hành vi ERP (ai có quyền "Duyệt giá vận chuyển" đều duyệt được); scope xem thì có lọc company_id (C).

---

## 9. Hạng mục & cách chạy

Feature lớn → `superpowers:writing-plans` sinh `plan.md` (tasks nhỏ, test từng task), thi công qua **Subagent-Driven Development** (như THGVC 16 task). Verify Playwright thật + đối chiếu ERP + đối chiếu ngang 2-3 màn HRM đã QA trước khi bàn giao. KHÔNG commit/push trừ khi user yêu cầu.

**Mở (không chặn):** bộ quyền chi tiết chốt ở đầu plan; cấu trúc bảng thực tế trong `erp_hrm_check` (đã có cột nào) kiểm bằng `SHOW COLUMNS` trước Task DB.
