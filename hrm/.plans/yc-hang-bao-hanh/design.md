# Thiết kế: Port màn Phiếu yêu cầu hãng bảo hành (FirmWarrantyRequest) ERP → HRM

- **Ngày:** 2026-11-20
- **Tác giả:** namdangit (qua Claude)
- **Trạng thái:** D1/D2/D3 ĐÃ CHỐT (20/11) — chờ duyệt tài liệu để sang bước lập plan
- **Nhánh:** HRM `develop`, ERP `develop_02`. gop_db chỉ khi user yêu cầu.
- **Màn tham chiếu (khuôn copy):** `finance/delivery-cost-asking-requests` (YC hỏi giá vận chuyển) và `finance/*` (YC đặt hàng mua ngoài) — 2 bản port cùng mẫu tuần này.

---

## 1. Quyết định đã chốt (20/11/2026)

| # | Quyết định | ✅ CHỐT | Hệ quả cho plan |
|---|---|---|---|
| **D1** | Phạm vi danh sách trên HRM | **Chỉ hiện phiếu của chính người lập** (`created_by = mình`) | KHÔNG gate quyền, KHÔNG `checkPermission`, KHÔNG `columnCustomizationMixin`, KHÔNG đụng Catalog quyền. BE Service lọc `created_by = auth()->id()`. Menu HRM khai KHÔNG `codes`. (KD cấp trên muốn xem phiếu nhân viên thì vào ERP.) |
| **D2** | Khóa màn Tạo/Sửa bên ERP | **Giữ ERP mở song song** | KHÔNG sửa ERP create/edit, KHÔNG redirect. Màn ERP vẫn lập được trong giai đoạn chuyển. |
| **D3** | Chuông kết quả ERP→HRM | **CÓ — báo khi XNK "Không duyệt" (status 5)** | +1 đoạn Guzzle bên ERP tại `unApprove`, gọi `POST {hrm_url_BE}/api/v1/finance/firm-warranty-requests/{id}/notify-result` (khuôn `WrApproveResultsController::notifyHrmImportResult`). HRM thêm route `notify-result` + giao chuông cho người lập. |
| **D4** (21/11/2026) | Validate Lưu nháp | **Validate ĐẦY ĐỦ, KHÔNG nới nháp** (đảo lại ý ban đầu ở §7) — khớp ERP + sibling `DeliveryCostAskingRequestStoreRequest` | Store/Update cùng 1 bộ rule cho status 1 và 2; chỉ guard "Chưa phân công người phụ trách…" áp khi status = 2. |

---

## 2. Ý định & lý do (Intent / Why)

Chuyển **khâu KD khởi tạo** Phiếu yêu cầu hãng bảo hành sang nền tảng HRM; **khâu mua hàng của XNK vẫn ở ERP**. Đây là bước tiếp theo của chủ trương "KD làm trên HRM, XNK/mua hàng ở ERP" — đã làm cho *YC hỏi giá vận chuyển* và *YC đặt hàng mua ngoài*. Mục tiêu: KD lập/sửa/gửi phiếu trong HRM (giao diện HRM thống nhất), dữ liệu **ghi thẳng vào bảng ERP** để màn XNK bên ERP dùng nguyên, không đổi luồng nghiệp vụ downstream.

**Chuỗi nghiệp vụ (không đổi):** `FirmWarrantyRequest (KD lập)` → nút *"Lập thư yêu cầu"* → `FirmWarranty (XNK gửi hãng)` → `FirmWarrantyConfirm (xác nhận BH)`. **Chỉ màn đầu** chuyển sang HRM; 2 màn sau ở lại ERP.

## 3. Goals / Non-goals / Anti-goals

**Goals**
- KD lập, lưu nháp, Lưu & gửi, sửa lại (phiếu nháp hoặc bị "Không duyệt"), xóa nháp, in phiếu — trên HRM.
- Ghi thẳng 4 bảng ERP (`firm_warranty_requests` + 3 bảng con) trên cùng DB (kiến trúc gộp), set đúng `status` 1/2.
- Khi gửi duyệt: báo chuông cho **người mua XNK được phân công** (theo `AssignHistory`), link mở phiếu bên ERP.
- Màn HRM trông như các màn HRM khác (V2Base, mixin, badge BE-driven, nút chuẩn `button-convention`).

**Non-goals**
- KHÔNG port màn `FirmWarranty` / `FirmWarrantyConfirm` (phần XNK) — giữ nguyên ERP.
- KHÔNG đổi luồng duyệt/gửi hãng/xác nhận bảo hành.
- KHÔNG port method `approve()` của ERP controller (xác định là **code chết**: tham chiếu hằng `DA_DUYET` và `firmWarrantyRequestService` không tồn tại, không JS nào gọi).

**Anti-goals (coi là thất bại dù chạy được)**
- Tạo bảng HRM mới rồi đồng bộ sang ERP (lệch dữ liệu với màn XNK đang chạy).
- Viết lại nghiệp vụ tồn/giá/hợp đồng trong HRM (trùng mã, dễ sai).
- Bê UI AngularJS của ERP sang (sai chuẩn HRM).
- Gán cờ quyền literal `true`, hoặc để lộ phiếu chéo người/công ty ngoài phạm vi đã chốt.

## 4. Ràng buộc (Constraints)

- **DB gộp:** Model HRM trỏ thẳng `$table` vào bảng ERP, KHÔNG khai `$connection` riêng (y như `DeliveryCostAskingRequest`). Dữ liệu dùng chung sau `gop_db`.
- **Bảng ERP "nói dối" — kiểm tới gốc:** `supplier` = bảng `customers`; nhiều cột `*_name` là snapshot. Port phải đọc code ERP tới nơi tính giá trị, không suy từ nhãn (CLAUDE.md "kiểm tới tận gốc").
- **Skill thắng spec về UI:** chữ nút/màu/icon/thứ tự theo `button-convention`, `list-page`, `modal-popup`, `form-validate`, `erp-to-hrm-screen`. Thông báo lấy nguyên văn bộ QLDA / `notification-convention`.
- **Mọi element form dùng `V2Base*`** (không HTML thô); select trong modal dùng `V2BaseSelectInModal`; số theo chuẩn quốc tế `1,234.56`.
- **Tài liệu** chỉ ở `HRM/docs`, `HRM/.plans` (symlink); KHÔNG để trong repo code.
- **Không commit/push** khi user chưa yêu cầu.

## 5. Các hướng đã cân nhắc (Approaches)

1. **(CHỌN) Ghi thẳng bảng ERP + XNK xử lý ở ERP + chuông 2 chiều** — bám khuôn `delivery-cost-asking-requests`. HRM lo lập/sửa/nháp/gửi/xóa/in; ERP giữ danh sách XNK, "Không duyệt", "Lập thư yêu cầu", downstream.
   *Vì sao chọn:* khớp 2 bản port tuần này, không lệch dữ liệu, không trùng nghiệp vụ.
2. **(LOẠI) HRM giữ bảng riêng rồi đồng bộ ERP** — lệch dữ liệu với màn XNK đang chạy thật, phải viết tầng sync hai chiều.
3. **(LOẠI) Viết lại toàn bộ nghiệp vụ trong HRM (kể cả FirmWarranty)** — ngoài scope ("XNK vẫn ở ERP"), trùng mã, rủi ro cao.

→ **Chỉ Hướng 1 hợp lý.**

## 6. Dữ liệu — 4 bảng ERP (ghi thẳng)

Giữ nguyên tên bảng/cột ERP. Model HRM `extends BaseModel`, `$table` trỏ ERP, không `$connection`.

- **`firm_warranty_requests`** — phiếu. Cột chính: `code` (`PYCHBH-xxxxx`), `status`, `brand_id`+`brand_name`(snapshot), `manufacture_id`+`manufacture_name`(snapshot), `send_company_id` (công ty gửi hãng), `approver_id` (người mua XNK — **không nhập từ form**, suy từ `AssignHistory`), `approved_time`, `approver_comment`, `created_by`, `company_id`/`department_id`/`part_id` (của người lập — BaseModel hook gán), `note`.
- **`firm_warranty_request_products`** — dòng hàng cần bảo hành. `product_id`+snapshot(`product_name/code/model_id/model_name/all_barcodes/unit_id/unit_name`), `serial`, `content`(bắt buộc), `note`, `customer_id`+snapshot(`customer_name/code`), `contractable_id/contractable_type`(**đa hình**: `FirmContract` | `WrServiceContract`)+`contractable_code`(snapshot), `handover_date`, `attachment` (chuỗi URL S3 nối `", "`), `in_stock` (0/1).
- **`firm_warranty_request_product_items`** — bảo hành **bằng hàng**: `firm_warranty_request_product_id`, `product_id`+snapshot, `qty`.
- **`firm_warranty_request_product_costs`** — bảo hành **bằng tiền**: `firm_warranty_request_product_id`, `cost_name`, `amount`.

**Sync:** khi lưu, **xóa sạch dòng con rồi tạo lại** (port `syncProducts` của ERP). Code sinh: tạo với code tạm `TMP-uniqid` (cột NOT NULL) → lấy `id` → set `PYCHBH-` + `str_pad(id,5,'0')` → save lại.

**Trạng thái (giữ số ERP):** 1 Đang tạo · 2 Chờ duyệt · 3 Đang gửi NCC · 4 Đã gửi NCC · 5 Không duyệt · 6 Đã xác nhận BH · 7 Hoàn thành. **HRM chỉ set 1 hoặc 2**; 3–7 do luồng ERP cập nhật. Badge: BE trả `status_text` + `status_color` (map vào 9 màu chuẩn: nháp `#64748B`, chờ duyệt `#D97706`, từ chối `#DC2626`, đang/đã gửi `#2563EB`/`#0EA5E9`, hoàn thành `#16A34A`).

## 7. Backend HRM (`Modules/Finance`)

Đặt trong **module Finance** để gom cùng 2 bản port KD-request trước (quyết định cấu trúc của tôi; đổi được nếu bạn muốn `Modules/Purchase`).

- **Entities:** `FirmWarrantyRequest` + 3 model con, trỏ `$table` ERP.
- **Controller:** `V1/FirmWarrantyRequestController` (`extends ApiController`), route group `/v1/finance/firm-warranty-requests`, `auth:api`.
  - Gate theo **D1**: Đề xuất own-only → KHÔNG `checkPermission`, Service lọc `created_by = auth()->id()`, `findEditable/findForCurrentUser` chặn 403/404/422. (Nếu chọn scope: gắn `checkPermission:purchase.phieu_yeu_cau_hang_bao_hanh.view` + `CurrentPermission::scope(...)`.)
- **WriteService** (`DB::transaction`): `store/update` (ghi phiếu + `syncProducts` + `sendIfNeeded`), `destroy` (xóa con + phiếu). `canEdit/canDelete` = **chủ phiếu** (`created_by === auth()->id()`) **và** status ∈ {1 Đang tạo, 5 Không duyệt} — port đúng ERP. FormRequest resolve **thủ công sau guard** (`app(...)->validated()`) để tránh bẫy "validate trước guard".
- **Validate** (port inline ERP, không khai `messages()` cho rule phổ biến):
  - `brand_id`/`manufacture_id`/`send_company_id` required+exists; `note` max 255.
  - `products` required|array|min:1; mỗi dòng: `product_id` exists, `content` required, `unit_id` exists, hàng **cùng thương hiệu** với phiếu.
  - `customer_id` **required_if `in_stock=0`**; `contractable_id` **required_unless `customer_id=null`**.
  - `items.*.qty` numeric|min:1; `costs.*.amount` numeric|min:1, `costs.*.cost_name` required.
  - Chặn trùng `product_id + serial` trong cùng phiếu.
  - Khi `status=2`: bắt buộc đã có `AssignHistory.buy_employee_id` cho (send_company+brand+manufacture); chưa có → "Chưa phân công người phụ trách thương hiệu, hãng sản xuất".
  - ~~**Lưu nháp (status 1) nới `required`** theo chuẩn HRM (giữ rule định dạng), ví dụ chỉ bắt `brand_id`. ⚠️ **Chủ ý lệch ERP:** ERP chạy ĐỦ rule kể cả status 1 (không nới); HRM nới theo convention `form-validate` + 2 bản sibling tuần này — ghi vào design để QA khỏi báo nhầm.~~ → **ĐÃ ĐẢO 21/11 (D4): không nới nháp, validate đầy đủ như ERP.**
- **Lookups cần port (BE):**
  - **Công ty gửi** (`send_company_id`): đổ **toàn bộ công ty** qua khuôn `Company::getForSelect()` (ERP `formJs` dòng 8) — **KHÔNG bó theo công ty người lập**, chỉ `required`. (Ai *xem* được phiếu do D1 quyết, không liên quan ô này.)
  - `getDeputy(manufacture_id)` → gọi `manufactures/{id}/getDeputy`, chỉ để **hiển thị** ô readonly "Người nhận đơn/Người mua" (thông tin phụ trách của hãng). **Đây KHÔNG phải đích chuông.**
  - **Người mua XNK nhận chuông** = **đúng 1 người** = `AssignHistory` theo (`send_company_id`+`brand_id`+`manufactures_id`), `whereNull('employee_date_to')`, `orderBy('created_at','desc')->first()->buy_employee_id` (ERP controller:186-190). Không có → chặn gửi "Chưa phân công người phụ trách thương hiệu, hãng sản xuất".
  - **`approver_id` KHÔNG ghi lúc tạo/sửa** — ERP comment dòng gán (controller:200), chỉ set trong `approve()` là code chết; màn XNK bên ERP tự recompute từ `AssignHistory`. → HRM để `approver_id` null, mirror đúng.
  - Picker **hàng** (lọc theo `manufacture_id`/brand), **khách hàng**, **hợp đồng** (đa hình FirmContract/WrServiceContract) + **`checkData`** (xác minh hàng thuộc hợp đồng, lấy `handover_date`).
- **In:** endpoint `/{id}/print-data` trả `{template}` HTML, qua `reportPrintPreviewMixin` (port `print_data`/`product_table` của ERP). **In danh sách** + **Xuất Excel**: xem D-phụ mục 11.
- **Resource:** List + Detail; eager-load tránh N+1; trả `status_text`/`status_color`, cờ `can_edit`/`can_delete`.

## 8. Frontend HRM (`pages/finance/firm-warranty-requests`)

5 file bám khuôn sibling: `index.vue`, `create.vue`, `_id/index.vue`, `_id/edit.vue`, `components/FirmWarrantyRequestForm.vue`, `api.js`.

- **Mixin:** `PageTitleMixin`, `filterStateMixin`, `DedupeLoadMixin`, `reportPrintPreviewMixin` (list); `unsavedChangesMixin` (form). Thêm `columnCustomizationMixin` **chỉ khi D1 = scope**.
- **Danh sách — cột mặc định:** STT · **Số phiếu** (`nuxt-link`) · Thương hiệu · Hãng sản xuất · **Người tạo** · **Ngày tạo** · Ngày duyệt · Người duyệt (XNK) · **Trạng thái** (badge) · Hành động. (Nhãn "Người tạo"/"Ngày tạo", KHÔNG "Người lập/Ngày lập".) Sort mặc định giảm dần theo ngày tạo.
- **Lọc:** tìm nhanh `Tìm theo số phiếu, mã/tên hàng, model, code đặt hàng`; nâng cao (floating): Thương hiệu, Hãng SX, Phòng (nếu scope), Khách hàng (ajax), Người duyệt (ajax), Trạng thái, khoảng Ngày tạo.
- **Hành động dòng:** In (luôn) · Sửa (`v-if can_edit`) · Xóa (`v-if can_delete`). Footer chi tiết khớp đúng danh sách (In/Sửa/Xóa, cùng điều kiện).
- **Form (header):** Thương hiệu (bắt buộc; đổi → xóa toàn bộ dòng hàng) · Hãng SX (bắt buộc) · Công ty gửi (`send_company_id`, bắt buộc) · Người nhận đơn/Người mua (readonly, tự fill từ `getDeputy`) · Người yêu cầu/Phòng (readonly, user hiện tại) · Ghi chú.
- **Form (bảng dòng hàng):** mỗi dòng: Hàng cần bảo hành (popup `V2ProductPickerModal`, cùng thương hiệu) · Serial · **Nội dung bảo hành** (bắt buộc) · `in_stock` (checkbox) · Khách hàng (`ChooseErpCustomerModal`) · Hợp đồng (bám `DeclareDebtContractPicker` — chọn loại HĐ + checkData) · Đính kèm (`V2BaseFile`) · sub-bảng **Bảo hành bằng hàng** (items: picker hàng + qty) · sub-bảng **Bảo hành bằng tiền** (costs: `cost_name` + `amount`).
- **Nút footer form** (`V2Footer` slot `#custom-actions`): **Lưu nháp** (`secondary`, `ri-save-3-line`, status=1) · **Gửi duyệt** (`primary`, `ri-send-plane-line`, status=2). KHÔNG nút Duyệt (duyệt ở ERP). Lưu xong → `markFormSaved()` + về danh sách.
- **Bắt buộc HRM:** Xuất Excel danh sách, Cấu hình cột (nếu scope), cảnh báo thoát khi chưa lưu, validate realtime vee-validate + BE 422, bảng tràn ngang cuộn 2 đầu.

## 9. Chuông (notifications)

- **HRM → ERP (khi Gửi duyệt, status 2):** ghi thẳng bảng `notifications` theo **khuôn adapter ERP** (`notifiable_type='App\Employee'`, `type='App\Notifications\SystemNotification'`, `data.url` trỏ ERP `.../firm_warranty_requests/{id}/show`). **Người nhận = đúng 1 người** = `AssignHistory.buy_employee_id` mới nhất còn hiệu lực (xem mục 7) — khác delivery-cost (bản kia gửi cho mọi holder `purchase.mua_hang.manage`); warranty gửi đúng 1 người phụ trách thương hiệu/hãng. Nội dung theo `notification-convention` + `NotificationMeta::build()`.
- **ERP → HRM (D3 = CÓ, đã chốt):** khi XNK `unApprove` (status 5), ERP gọi `POST {hrm_url_BE}/api/v1/finance/firm-warranty-requests/{id}/notify-result` (Guzzle, Bearer JWT SSO, timeout 5s, lỗi chỉ `Log::warning`) — khuôn `WrApproveResultsController::notifyHrmImportResult`. HRM route `notify-result`: chỉ approver phiếu / holder `purchase.mua_hang.manage` gọi được (403 kể cả id sai); phiếu phải ở status 5 (nếu không 422); chuông về **người lập** qua `EmployeeInfoService::sendNotification(employee_info_id, …)`, deep-link HRM `/finance/firm-warranty-requests/{id}`.

## 10. Quyền & Menu

- **Mã quyền:** `purchase.phieu_yeu_cau_hang_bao_hanh.view` **đã tồn tại** (`Catalog/purchase.php:786`, `platforms=['erp']`, `scopes=[1,2,3,4]`).
  - D1 = own-only → **không cần đụng** (màn không gate).
  - D1 = scope → thêm `'hrm'` vào `platforms`, `permission:catalog-sync`, admin cấp ở `/admin/roles`.
- **Menu:** thay placeholder chuỗi trần `'YC hãng bảo hành'` tại `components/subsystem-menu/sale-hub.js:187` thành `{ n: 'YC hãng bảo hành', link: '/finance/firm-warranty-requests' }` (own-only: bỏ `codes`; scope: thêm `codes: ['purchase.phieu_yeu_cau_hang_bao_hanh.view']`). Giữ cạnh 2 bản port tuần này.

## 11. Quyết định phụ (builder tự xử theo đề xuất, nêu để minh bạch)

- **Module** = `Modules/Finance` (gom cùng sibling). Đổi sang `Modules/Purchase` nếu muốn theo phân hệ quyền.
- **Route/path** = `finance/firm-warranty-requests` (khớp sibling).
- **In danh sách + Xuất Excel 1 phiếu:** ERP có cả (`FirmWarrantyRequestExcel`, template `DANH_SACH_...`). Port: **In danh sách** + **Xuất Excel danh sách** (bắt buộc HRM) theo `export-excel`/`print-page`; "Xuất Excel 1 phiếu" của ERP là tùy, tôi **tạm bỏ** nếu không QA yêu cầu.
- **Cột `canView` scope DEPARTMENT/PART** của ERP đang là bug "luôn false" (comment giữ nguyên). Nếu D1=scope, port **sửa đúng** 2 nhánh này.
- **Người ký/duyệt in phiếu** dùng **Chức danh HRM** (`titles`), KHÔNG dùng `roles` của ERP (CLAUDE.md #11932).

## 12. Để lại cho builder

- Rà `V2ProductPickerModal` / `ChooseErpCustomerModal` / `DeclareDebtContractPicker` khớp tới đâu với nhu cầu (đa hình HĐ + checkData) — tách/điều chỉnh component dùng chung, hỏi trước khi sửa component đang chạy.
- Viết e2e Playwright (lập nháp → gửi → sửa lại → xóa nháp) trước khi báo xong; verify LIVE trên `http://127.0.0.1:3000`.
- Đối chiếu ngược ERP (nhánh `develop_02` đang chạy) + đối chiếu ngang 2–3 màn HRM đã QA (bước 5/5b skill `erp-to-hrm-screen`).
- Kế hoạch triển khai chi tiết: `superpowers:writing-plans` → `HRM/.plans/firm-warranty-request-port/plan.md`.
