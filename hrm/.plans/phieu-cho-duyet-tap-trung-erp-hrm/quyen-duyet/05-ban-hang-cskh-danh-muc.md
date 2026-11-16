# Quyền duyệt — nhóm Bán hàng · CSKH · Vận chuyển · Danh mục dùng chung (MasterData) — @cuong61n

Ngày 16/11/2026. Chỉ đọc code `hrm-api` + `hrm-client` nhánh `gop_db-main` (working tree), KHÔNG chạy lệnh ghi, KHÔNG truy vấn DB. Đường dẫn BE tính từ `hrm-api/Modules/`, FE tính từ `hrm-client/`. "Chưa xác minh" = chỉ suy từ code, chưa đối chiếu dữ liệu thật. Hạ tầng quyền / "quản lý phòng" dùng chung xem `00-ha-tang-quyen.md` (đừng chép lại ở đây).

Viết tắt: **Q(x)** = mã quyền x (tên cũ ghi kèm khi code còn gọi bằng tên cũ — tra qua `permission_aliases`); **QL(P)** = "người quản lý phòng P" (3 biến thể, xem 00-ha-tang §1.6); **cùng cty** = công ty của phiếu = công ty đang làm của người duyệt.

---

## 0. Kết luận nhanh

1. **Khe `model_type` KHÔNG còn.** `PermissionChecker` nạp quyền từ `employee_has_roles` "bỏ qua model_type" và chỉ xét Vai trò có `roles.company_id` = công ty đang làm (`hrm-api/app/Support/Permissions/PermissionChecker.php:9-17, 246-281`). Mọi cửa (`checkPermission`, `isCurrentEmployeeHasPermission`, `WarrantyRepairPermission::has`, trait `ChecksEmployeePermission`) đều quy về đó (`app/Http/Middleware/CheckPermission.php:32`, `CustomerCare/Support/WarrantyRepairPermission.php:62-65`, `Finance/Entities/Concerns/ChecksEmployeePermission.php:19-24`). ⇒ Nhận định "CustomerCare khoá với mọi người (0 người HRM-type giữ quyền)" của `inventory-hrm.md:16-26, 377-381` **đã lỗi thời**; "Tạo phiếu giao việc chỉ có guard web" cũng sai (catalog đã có `['api','Tạo phiếu giao việc']`, `app/Support/Permissions/Catalog/customer_care.php:557-559`).
2. **Không còn Super Admin vượt quyền** ở cả CustomerCare/Transport/MasterData/Finance-Bán hàng (grep `isSuperAdmin|hasRole('Super|role_id 18` chỉ còn trong comment/test). Docblock nhiều nơi còn ghi "Super admin" (vd `WrServiceContract.php` docblock `getIsCanApproveAttribute`, `WrImportResultService.php:38`) nhưng **code không có nhánh đó**.
3. **Điều kiện "quản lý" chỉ có ở 3 luồng**: HĐ dịch vụ SC-BD-BT (`approver_id` HOẶC QL phòng, **loại trừ nhau**), KH nhân viên (QL phòng/cùng phòng + quyền), và các nhóm "XNK phân công hiện hành" của YCHG (người đích danh theo thương hiệu × hãng × công ty, không phải quản lý). Tất cả luồng còn lại chỉ là **quyền + cùng công ty**.
4. **Không có luồng nào trong nhóm này có nhiều cấp duyệt "chạy hết" trên HRM**, trừ: PNKQ (2 bước: mở form duyệt rồi lưu), Chuyến xe khác (Duyệt → Hạch toán), YCHG→nhóm→YCTG→PTG→Duyệt giá bán (chuỗi 5 chứng từ khác nhau), KH nhân viên (TP → "Gửi BGĐ", BGĐ duyệt KHÔNG có màn HRM). Nên "một người giữ nhiều cấp" trong nhóm này chủ yếu là **một người có nhiều quyền rời nhau** (xem mục E).
5. **Fail-open / lệch gate phát hiện** (chi tiết từng mục): Biên bản bàn giao sơ bộ (`approver_id` chỉ để thông báo, ai cũng duyệt được — A8); PNKQ `?type=wait_approve_result` không có quyền thì KHÔNG bó phạm vi (A2); Chuyến xe khác phải có thêm quyền "Thủ kho" mới duyệt được nhưng menu "Chờ duyệt" chỉ gate "Duyệt chuyến xe khác" (B1); THGVC / HĐ vận chuyển duyệt xuyên công ty (B2, B3); YCHG "Chờ PTKD duyệt" không hiện cho PTKD nếu thiếu quyền Xem (C1).
6. **Menu Bán hàng › Phê Duyệt hiện đã có thêm màn so với `danh-gia-tung-phieu.md` §6**: "HĐ chờ duyệt" (SC-BD-BT) và 4 mục "Kế hoạch & chỉ tiêu" (KH bán hàng / KH PTTT / Giao chỉ tiêu phòng ban / NV) — `hrm-client/components/subsystem-menu/sale-hub.js:344-364`. Mục §6 tài liệu nền ghi "KH bán hàng, KH phát triển thị trường chưa có màn" là **sai**; xem mục D.

---

## A. CUSTOMERCARE (`Modules/CustomerCare`, FE `pages/customer-care`)

### A1. Hợp đồng dịch vụ SC-BD-BT — Duyệt / Không duyệt (C4 trong tài liệu nền)

**(a) Các cấp** (`Entities/WrServiceContract/WrServiceContract.php:81-89`)

| Mã status | Chữ BE trả | Chuyển sang |
|---|---|---|
| 1 `HD_CREATING` | Đang tạo | 2 khi người lập bấm Gửi duyệt (`Services/WrServiceContractService.php:582-588` chỉ nhận 1 hoặc 2 từ form; `Http/Requests/WrServiceContract/WrServiceContractRequest.php:29, 43`) |
| **2 `HD_WAITING`** | **Chờ duyệt** | 3 (Duyệt) hoặc 11 (Không duyệt) — `WrServiceContractService.php:1569-1596` |
| 3 `HD_EFFECTIVE` | Có hiệu lực | Huỷ duyệt → 11; Đóng → 10 |
| 11 `HD_REJECTED` | Không duyệt | người lập sửa rồi gửi lại (`getIsCanEditAttribute`, entity tr.358-371) |

Chỉ **1 cấp duyệt** (Chờ duyệt). Phụ lục (type 3/4) không có route duyệt trên HRM: `contractOrFail` ép `type = 1` (`Http/Controllers/V1/WrServiceContractController.php:472-475`) ⇒ phụ lục chờ duyệt (1 phiếu theo `inventory-hrm.md:389`) **chỉ duyệt được trên ERP**.

**(b) Ai duyệt cấp "Chờ duyệt"** — `getIsCanApproveAttribute` (`WrServiceContract.php:388-402`):

```
status = 2 (Chờ duyệt) VÀ type = 1
 NẾU approver_id có giá trị  →  CHỈ người đó (approver_id = auth id)
 NGƯỢC LẠI                   →  department_id của HĐ ∈ phòng người đăng nhập QUẢN LÝ
```

- **Không cần mã quyền nào**, không xét công ty, không xét `company_id` của HĐ (so `department_id` — id phòng duy nhất toàn hệ thống nên tương đương).
- **`approver_id` và QL phòng KHÔNG phải "HOẶC"** (khác `danh-gia-tung-phieu.md:73` "approver_id hoặc quản lý phòng"): khi đã có `approver_id` thì **quản lý phòng bị loại**. Điều này khác docblock của chính hàm ("Super Admin · người được chọn duyệt · hoặc người QUẢN LÝ phòng", `WrServiceContract.php` ngay trên hàm) — code không có Super Admin và có `return` sớm theo `approver_id`.
- "QL phòng" ở đây = `WarrantyRepairHandleRequest::managedDepartmentIds` (`Entities/WarrantyRepairHandleRequest/WarrantyRepairHandleRequest.php:266-276`): chỉ `pluck department_id` các dòng `employee_manage_departments` của công ty gốc `auth()->user()->info->company_id` — **KHÔNG tính cờ `all_department`, KHÔNG cộng phòng của chính mình, KHÔNG dùng công ty đang làm** (biến thể V3 mục 00-ha-tang §1.6; chưa chạy thử trên người kiêm nhiệm).
- HRM **không có chỗ nào ghi `approver_id` trước khi duyệt** (grep `approver_id` ở `WrServiceContractService.php` chỉ có lọc `:124-125` và gán lúc duyệt/không duyệt `:1572, :1587`; `WrServiceContractRequest` không có trường này) ⇒ HĐ lập từ HRM luôn đi nhánh QL phòng. HĐ lập từ ERP có thể mang `approver_id` (ERP form có ô Người duyệt): **chưa xác minh** phía ERP.

**(c) Kiểm ở đâu / ai THẤY**
- BE chốt thật ở `WrServiceContractController::approve/reject` (`:331-368`): `if (!$model->is_can_approve) → 423`. Không fail-open. `reject` thêm lý do bắt buộc (`:353-361`).
- FE chỉ đọc cờ BE: `pages/customer-care/wr-service-contracts/index.vue:630, 637`; `components/WrServiceContractForm.vue:664, 669`.
- **Danh sách "chờ duyệt" lệch người duyệt**: `?type=for-approve` = `status = 2` ∩ phạm vi XEM (`WrServiceContractService.php:206-215, 228-254`): tổng công ty / "ẩn giá" ⇒ tất cả; công ty ⇒ cùng cty hoặc mình lập; phòng ban ⇒ phòng QL hoặc mình lập; không quyền Xem ⇒ chỉ phiếu mình lập. Người được `approver_id` chỉ định **nhưng không có quyền Xem HĐ** sẽ không thấy phiếu trong danh sách chờ (mở link trực tiếp vẫn duyệt được vì BE chỉ kiểm `is_can_approve`; `canView` chỉ dùng ở màn chi tiết). Người xem được cả công ty nhưng không phải QL/approver thấy phiếu mà không có nút.
- Mã Xem: `customer_care.hop_dong_dich_vu_sc_bh.view` (phạm vi 2/3/4) + `sale.hop_dong_an_gia.view` (xem tất cả) — `WrServiceContract.php:115, 124`.

**(d) Người tạo tự duyệt?** KHÔNG bị chặn. Nếu người lập là QL của `department_id` HĐ (hoặc là `approver_id`) thì tự duyệt được: `is_can_approve` không so `created_by`.

**(e) Một người nhiều cấp**: chỉ có 1 cấp; "lập + duyệt" cùng người được phép (xem d). Cũng người này có thể Huỷ duyệt/Đóng (`is_can_un_approve` `:408-418` = QL phòng, KHÔNG xét `approver_id`; `is_can_close` `:425-436` = người lập HOẶC QL phòng).

**(f) Đặc thù**: `dueConfig` chỉ gắn cho lập/sửa (`Routes/api.php:369, 373`), KHÔNG gắn cho approve/reject. Thông báo cho người duyệt: không rõ ai nhận (chưa xác minh `WrServiceContractNotifier`).

**(g) Cho bảng gom**: kiểu gate = **(c) người đích danh `approver_id` NẾU có, ngược lại (b) QL phòng `department_id`** — một điều kiện **rẽ nhánh theo dữ liệu từng dòng**, KHÔNG phải HOẶC. Không có cột quyền. Definition cần: `assignee_column = approver_id` + `fallback_manager_department_column = department_id` + `manager_variant = V3` + `scope_to_view = false` (người duyệt không cần quyền Xem). Biểu diễn bằng 1 cột gate đơn giản: **KHÔNG** (cần cờ "nếu cột đích danh NULL thì dùng QL phòng").

### A2. Phiếu nhập kết quả (PNKQ) — Duyệt kết quả (menu CSKH › Giao việc)

**(a) Các cấp** (`Entities/WrImportResult/WrImportResult.php:28-33, 45-51`)

| Status | Chữ BE | Ghi chú |
|---|---|---|
| 1 | Đang tạo | người lập |
| **2** | **Chờ duyệt kết quả** | người duyệt bấm "Duyệt kết quả" → mở form duyệt, tạo phiếu duyệt kết quả (PDKQ, bản ghi `wr_assign_tasks.parent_id = phiếu giao việc`) |
| **5** | **Đang duyệt kết quả** | PDKQ nháp (status PDKQ 3) — chỉ người tạo PDKQ tiếp tục / không duyệt |
| 3 | Đã duyệt kết quả | khi PDKQ Chờ hạch toán (1) hoặc Đã hạch toán (2) — `Services/WrApproveResultStoreService.php:422-470` |
| 4 | Chờ BKS duyệt kết quả | **không có đường chuyển nào trong HRM** (grep `CHO_BKS_DUYET` chỉ có hằng + nhãn; `WrApproveResultStoreService::applyStatus` không đặt) — đường ERP, chưa xác minh |
| 6 | Không duyệt kết quả | `WrImportResultService::reject` |

**(b) Ai duyệt (cấp 2 → Duyệt)** — `canApproveResult` (`Services/WrImportResultService.php:574-582`): `status = 2` VÀ **Q(Duyệt phiếu nhập kết quả = `customer_care.phieu_nhap_ket_qua.approve`, tên cũ cùng chữ)** VÀ `viewer.company_id` có giá trị VÀ `result.company_id = viewer.company_id`. `viewer.perm_approve` = `isCurrentEmployeeHasPermission(PERM_APPROVE)` (`:1563`, hằng `:63`). **Không có điều kiện quản lý.** `company_id` phiếu = công ty của người LẬP (gán lúc lưu; chưa xác minh dòng gán) — quyền xét ở công ty ĐANG LÀM của người duyệt.

Cấp 5 (Đang duyệt): `canEditApproveResult` (`:603-606`) = `PDKQ.status = 3 (KQ_DANG_TAO)` VÀ `PDKQ.created_by = auth id` ⇒ **người đích danh = người đã mở form duyệt lần đầu**, KHÔNG xét lại quyền duyệt (kiểm `canEditApproveResult` ở `WrApproveResultStoreService.php:324`, `WrApproveResultSourceService.php:73`).

Từ chối: `canRejectResult` (`:615-632`): PNKQ 2 hoặc 5 + Q(duyệt) + cùng cty; riêng PNKQ 5 thêm `PDKQ.created_by = mình`.

**(c) Kiểm ở đâu**: route **không** gắn `checkPermission` có chủ ý (comment `Routes/api.php:428-430`); chốt ở service: `approveData` (`WrApproveResultSourceService.php:61, 73`), `store` (`WrApproveResultStoreService.php:244` → 403), `update` (`:324`), `reject` (`WrImportResultService.php` hàm `reject`, kiểm `canRejectResult` → 403). Có `dueConfig:Duyệt kết quả công việc,manager` ở `approveStore/approveUpdate` (`Routes/api.php:432-435`) — **chặn trưởng phòng còn nhân viên quá hạn** (HTTP 423, `Finance/Http/Middleware/CheckDueConfig.php`). BE chốt thật; FE đọc cờ (`pages/customer-care/wr-import-results/index.vue:647-665`; form `WrImportResultForm.vue:366`).
- **Danh sách / ai THẤY**: menu chỉ có `?type=all` (`hrm-client/components/subsystem-menu/customer-care.js:132`; comment `:124` ghi lối `wait_approve_result` "chỉ có trên dashboard → không khai"). `?type=wait_approve_result`: có Q(duyệt) ⇒ `status = 2` ∩ cùng cty (`WrImportResultService.php:340-343`); **không có Q(duyệt) ⇒ KHÔNG bó phạm vi** (comment `:347-348` "lỗi ERP, giữ" — user chốt 02/11/2026) ⇒ người không quyền gọi `?type=wait_approve_result` thấy **mọi PNKQ mọi trạng thái mọi công ty**. `?type=all`: phạm vi 3 quyền Xem (`customer_care.phieu_nhap_ket_qua.view` 2/3/4); không có quyền Xem ⇒ chỉ phiếu mình (`:306-329`) — **người duyệt không có quyền Xem vẫn không thấy phiếu "all"** (nhưng `canView` cho vào chi tiết qua `canApproveResult`, `:544-564`).

**(d) Người tạo tự duyệt?** Không chặn: `canApproveResult` không so `created_by` PNKQ.

**(e) Một người nhiều cấp**: cùng người lập PNKQ, mở form duyệt (tạo PDKQ), lưu nháp rồi duyệt tiếp — được. Người A mở form lưu nháp (PNKQ → 5) rồi **người B (cũng có quyền duyệt) không tiếp tục được** (chỉ A), dù B có thể "Không duyệt" ⇒ chỉ A (`:628-631`) — vậy B không có cách giải phóng phiếu ngoài A/Admin DB.

**(f)** Nhóm 3 trạng thái PDKQ quyết kết quả: lưu nháp (PNKQ→5), "Duyệt HĐ" / "Duyệt lắp đặt-GVK-ép" (PNKQ→3). Duyệt cùng lúc đồng bộ serial, hợp đồng, yêu cầu lắp đặt (`WrApproveResultStoreService.php:422-470`).

**(g) Cho bảng gom**: cấp 2 = **(a) quyền + cùng cty**, không phạm vi quản lý ⇒ **biểu diễn được bằng gate quyền đơn giản**. Cấp 5 = **(c) đích danh theo bảng con** (`wr_assign_tasks` con, `created_by`) — cần join/subquery; coi PNKQ 5 là "phiếu đang chờ chính tôi tiếp tục", KHÔNG phải hàng đợi của nhóm. Nên chỉ đưa PNKQ status 2 vào bảng gom.

### A3. Yêu cầu đi kiểm tra sửa chữa - bảo hành (C1) — Phòng tiếp nhận từ chối / chuyển phòng

**(a) Cấp**: `Entities/WarrantyRepairRequest/WarrantyRepairRequest.php:32-40`: 1 Đang tạo · **2 Chờ xử lý** (STATUS_WAITING_HANDLE) · 3 Đang xử lý · … Từ chối = về 1 kèm lý do (`Services/WarrantyRepairRequestService.php:884-905`). Chỉ 1 cấp (phòng tiếp nhận).

**(b) Ai**: `canHandleRequest` = `status = 2` VÀ chưa có phiếu xử lý VÀ **Q(`customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm`, tên cũ "Xử lý yêu cầu sửa chữa")** VÀ `department_reception_id = phòng của người đăng nhập` (`employee_infos.department_id`, KHÔNG phải QL phòng) — tr.289-312; `canReject`/`canTransferDepartmentReception` dùng chung (tr.330-338). Không so công ty (phòng tiếp nhận quyết định).

**(c) Kiểm ở đâu**: route `reject` / `transfer-department` gắn `checkPermission:…confirm` (`Routes/api.php:271-274`) + controller dùng `findOrFail` rồi service gọi `canReject()` (`WarrantyRepairRequestService.php:887`; `transferDepartmentReception` tr.~915 cũng gọi `canTransferDepartmentReception`) ⇒ BE chốt. FE `pages/customer-care/warranty-repair-requests/index.vue:591-604`.
- Ai THẤY phiếu chờ xử lý: `?type=all` (phạm vi Xem `…yeu_cau_di_kiem….view` 2/3/4) **HOẶC** người có `confirm` thì thấy mọi phiếu `department_reception_id = phòng mình` (`Services/WarrantyRepairRequestService.php:373-376`; `Entity canView` tr.276-280) ⇒ **khớp ai duyệt được**. Không có menu "chờ xử lý" riêng (menu `?type=all`).

**(d)** Người tạo tự xử lý? Chỉ khi chính người tạo cũng ở phòng tiếp nhận + có quyền confirm — không chặn.
**(e)** 1 người = người lập + phòng tiếp nhận: được.
**(g)**: gate = **(a) quyền + (e) phòng tiếp nhận = phòng của người xem** (`department_reception_id = employee_infos.department_id`) — không phải QL phòng. Biểu diễn được bằng gate `{perm: confirm, recipient_department_column: department_reception_id}`; cần thêm kiểu "phòng của tôi" bên cạnh "phòng tôi quản lý".

### A4. Phiếu xử lý yêu cầu (C2) — "Không duyệt" bởi người lập Phiếu cung cấp thông tin

**(a)** `Entities/WarrantyRepairHandleRequest/WarrantyRepairHandleRequest.php:34-39`: **2 Chờ CCTT** (STATUS_AWAIT_INFORMATION; 4 "Chờ CCTT bổ sung" **không** được tính là chờ); Không duyệt → 1 Đang tạo (`Services/WarrantyRepairHandleRequestService.php:643-661`).
**(b)** `canCreateRepairInformation` (tr.204-208) = `status = 2` VÀ Q(`customer_care.phieu_cung_cap_thong_tin.create`, "Tạo phiếu cung cấp thông tin"); `canReject` = cùng điều kiện (tr.211-214). **Không phòng, không công ty, không quản lý** (docblock ngay trên hàm nhấn "KHÁC chứng từ 1: KHÔNG ràng buộc phòng ban").
**(c)** BE: route gắn `checkPermission:…create` (`Routes/api.php:305-306`) + controller `canReject()` (`Http/Controllers/V1/WarrantyRepairHandleRequestController.php:308-336`). Ai thấy: phạm vi Xem `…phieu_xu_ly_yeu_cau….view` (tr.74, `canView` tr.225-263) + `index` có thể gồm lối riêng theo quyền tạo CCTT — chưa đọc hết `applyScope` của màn này; **chưa xác minh** người có quyền tạo CCTT nhưng không có quyền Xem có thấy phiếu "Chờ CCTT" không.
**(d)** Không chặn người lập phiếu xử lý tự "Không duyệt". **(e)** n/a.
**(g)**: **quyền đơn thuần** (không phạm vi) — gate đơn giản; nhưng "ai thấy" phụ thuộc phạm vi Xem ⇒ nếu bảng gom coi quyền create là điều kiện thấy thì phải khai thêm `visible_by = perm create` (không phải view).

### A5. Phiếu cung cấp thông tin (C3, "wr-information-requests") — Từ chối tiếp nhận

**(a)** `Entities/WrServiceQuotation/WrServiceQuotation.php:45-53`: **2 Chờ làm báo giá** (`STATUS_WAITING_QUOTATION`) ⇒ 9 Không duyệt (`Services/WrServiceQuotationService.php:1388`). Bước nghiệp vụ là **làm báo giá**, "Từ chối tiếp nhận" là phụ.
**(b)** `canReject = canCreateQuotation` (tr.431-434, 390-428): `type = 0` + `status = 2` + có dòng sửa chữa (thiết bị / mở rộng / chi phí > 0) + mỗi thiết bị ≤ 1 lỗi + **`warrantyRepairRequest.created_by = auth id`** (người lập PHIẾU YÊU CẦU gốc, tr.427). Không dùng quyền (comment `Routes/api.php:336-338`: cố ý không gắn quyền).
**(c)** BE: controller `canReject()` (`Http/Controllers/V1/WrServiceQuotationController.php:201-224`). Ai thấy: `?type=waiting_create_quotation` (menu `sale-hub.js:94-96`) = chính phiếu mình là người lập YC gốc. Khớp.
**(d)** Người lập CCTT không phải người duyệt trừ khi trùng người lập YC gốc.
**(e)** Một người lập YC + lập CCTT: tự "từ chối tiếp nhận" được.
**(g)**: gate **(c) đích danh theo bảng cha** (`wr_service_quotations.warranty_repair_request_id → warranty_repair_requests.created_by`); điều kiện nghiệp vụ (có dòng sửa chữa, ≤ 1 lỗi/thiết bị) chạy bằng code/query con. **Không phải hàng đợi duyệt** (4.686 phiếu "chờ làm báo giá" theo `inventory-hrm.md:381`) ⇒ nên loại khỏi bảng gom như `danh-gia-tung-phieu.md §5`. Cột "đích danh qua bảng cha" cần cho Definition (không phải cột trên chính bảng).

### A6. Hợp đồng dịch vụ — Phòng tiếp nhận từ chối tiếp nhận / người lập đổi phòng (C5)

**(a)** Không có cấp riêng: HĐ `status = 3 Có hiệu lực` + `department_reception_id` + chưa có phiếu giao việc (trừ phiếu huỷ 9). "Từ chối tiếp nhận" không đổi status mà đặt `department_reception_id = NULL` (`Services/WrServiceContractService.php:1653-1668`).
**(b)** `is_can_reject_reception` (`WrServiceContract.php:464-479`): `status = 3` + `department_reception_id` có + chưa có PGV + **Q(`customer_care.phieu_giao_viec.create`, tên cũ "Tạo phiếu giao việc")** + `department_reception_id = phòng của người đăng nhập`. Đổi phòng: `is_can_change_reception` (`:443-455`) = **người lập HĐ** + status 3 + chưa có PGV. Không công ty, không QL.
**(c)** BE `WrServiceContractController::rejectReception` kiểm `is_can_reject_reception` (`:445-455`) → 423. FE `index.vue:658, 665`; `WrServiceContractForm.vue:693, 702`. Không có màn "chờ tiếp nhận" riêng (menu không có) ⇒ **không có danh sách để gom**; muốn gom phải tự dựng truy vấn (HĐ type 1, status 3, phòng tiếp nhận = phòng mình, NOT EXISTS PGV).
**(d)(e)** Người lập tự đổi phòng; người trong phòng tiếp nhận từ chối — hai vai khác nhau, 1 người có thể giữ cả hai.
**(g)**: **chưa phải duyệt** theo nghĩa phiếu chờ duyệt (đây là hàng đợi tiếp nhận công việc, 243 HĐ theo `inventory-hrm.md`). Kiểu gate = quyền + "phòng của tôi" như A3. **Khuyến nghị loại khỏi bảng gom** (hoặc gắn nhãn "tiếp nhận").

### A7. Yêu cầu giao việc khác — Phòng tiếp nhận từ chối

`Services/AssignOtherRequestService.php:352-358` (`canAssignTask`): status **"Chờ giao việc"** (`CHO_GIAO_VIEC`) + `department_reception_id = phòng của người xem`; **KHÔNG cần quyền**; BE kiểm ở `reject` (`:479-…`, 403 nếu khác phòng, 409 nếu sai trạng thái). Route không gắn `checkPermission` (comment `Routes/api.php:471-473`). Không công ty. Thuộc hàng đợi tiếp nhận (như A6) — **không phải duyệt**. Gate bảng gom = `{department_reception_id = phòng của tôi}` thuần, không quyền.

### A8. Biên bản bàn giao sơ bộ (`handover-records`) — **không có trong tài liệu nền**

**(a)** `Entities/HandoverRecord/HandoverRecord.php:23-26, 34-38`: 1 Đang tạo · **2 Chờ duyệt** · 3 Đã duyệt · 4 Từ chối. 1 cấp.
**(b)** **KHÔNG kiểm người duyệt.** `canApprove` = `status = 2` (`Services/HandoverRecordService.php:185-188`); `approve()` ghi nhận không kiểm gì ngoài trạng thái (docblock `:481-483`: "Không kiểm người duyệt (y ERP không quyền — user chốt)"). Route không `checkPermission` (`Routes/api.php:489-495`; comment "ERP màn này không có quyền, user chốt giữ y ERP 04/11/2026"). Biểu mẫu bắt buộc chọn `approver_id` (`Http/Requests/HandoverRecordRequest.php:48`) nhưng **chỉ để gửi thông báo "Chờ duyệt"** (`Services/HandoverRecordNotifier.php:29`) — **bất kỳ người đăng nhập nào** gọi `PUT handover-records/{id}/approve` đều duyệt được.
**(c)** FE hiện nút theo `is_can_approve` = chỉ trạng thái (`pages/customer-care/handover-records/index.vue:353`, `_id/index.vue`, `HandoverRecordForm.vue:194-248`) ⇒ **mọi người đều thấy nút Duyệt trên mọi biên bản Chờ duyệt**. Danh sách không bó phạm vi ("ERP không bó phạm vi, ai cũng thấy mọi biên bản", `HandoverRecordService.php:~98-100`).
**(d)** Người lập tự duyệt được. **(e)** n/a.
**(g)**: **gate nguyên tắc** là `approver_id` (người đích danh) nhưng **BE không cưỡng chế**. Khi gom, nếu chỉ hiện cho `approver_id` thì sẽ **HẸP hơn** thực tế BE cho phép — cần user chốt: giữ y ERP (ai cũng duyệt) hay siết `approver_id`. Biểu diễn: gate **(c) đích danh cột `approver_id`**. Đây là phát hiện mới, tài liệu nền không có.

### A9. Báo giá dịch vụ / Biên bản giao nhận hàng hoá (Sale) — KHÔNG phải luồng duyệt

- Báo giá dịch vụ (`wr-quotations`): trạng thái "Duyệt" (2) tự đặt khi người lập bấm "Lưu và duyệt" (`WrServiceQuotation.php:85`, `Services/WrQuotationService.php:325`) — tự duyệt, không có người duyệt khác.
- Biên bản giao nhận hàng hoá (`Modules/Sale`, `handover-product-records`): "Lưu và duyệt" của chính người lập (`Modules/Sale/Services/HandoverProductRecordStoreService.php:15`); route không `checkPermission` (`Modules/Sale/Routes/api.php:20-24`). Không có hàng đợi duyệt của người khác ⇒ **loại khỏi bảng gom**.

---

## B. VẬN CHUYỂN (`Modules/Transport`, FE `pages/transport`) — **chưa có trong tài liệu nền**, ngoài "Chuyến xe khác"

### B1. Chuyến xe khác

**(a) Các cấp** (`Entities/OtherDeliveryTrip/OtherDeliveryTrip.php:32-47`): 2 Đang tạo → 4 Đang chạy → **5 Chờ duyệt** → **1 Chờ hạch toán** (sau duyệt) → 7 Đang hạch toán / 3 Đã hạch toán (làm bên ERP); 6 Không duyệt (từ chối của kế toán). "Không duyệt" ở bước Chờ duyệt (5) trả về **2 Đang tạo** (`Services/OtherDeliveryTrip/OtherDeliveryTripWriteService.php:181-187`), không phải 6. Hai bước chờ:

| Cấp | Mã status | Chữ BE | Người thực hiện |
|---|---|---|---|
| Duyệt | 5 | Chờ duyệt | Q("Duyệt chuyến xe khác" = `warehouse.chuyen_xe_khac.approve`) **VÀ** Q("Thủ kho" = `warehouse.thu_kho.manage`) |
| Hạch toán / Không duyệt (kế toán) | 1 | Chờ hạch toán | Q("Hạch toán chuyến xe khác") (nút Hạch toán + Không duyệt); xem hàng đợi: Q("Hạch toán chuyến xe khác") HOẶC Q("Hạch toán vận chuyển") |

**(b)** `canApprove` (`OtherDeliveryTrip.php:230-233`) = `status = 5` + Q(Duyệt chuyến xe khác). Nhưng MỌI endpoint đi qua `run()` kiểm **Q(Thủ kho)** trước (`Http/Controllers/V1/OtherDeliveryTrip/OtherDeliveryTripController.php:50-54`) rồi `withViewable` kiểm `canView()` (`:68-77`) — `canView` (tr.172-199): mình tạo → được; `status = 5` ∩ cùng cty ∩ Q(duyệt) → được; phiếu Đang tạo của người khác → không; còn lại theo 3 quyền Xem chuyến xe (tổng cty / cty / QL phòng + phòng mình). ⇒ **Duyệt = Thủ kho + Duyệt chuyến xe khác + (thấy phiếu)**. Không điều kiện QL; công ty: nếu chỉ dựa nhánh `status=5` thì phải cùng cty; người có quyền Xem tổng công ty duyệt được phiếu mọi cty (vì `canApprove` không so công ty).
**(c)** BE chốt: `approve/rejectApprove` → `canApprove()` 403 (`:254-277`); `deny` → `canDeny()` (= `canAccounting`) (`:280-290`). FE: nút trong form `components/OtherDeliveryTripForm.vue:551-564` đọc `detail.can_approve/can_deny/can_accounting`. **Danh sách `index.vue` không có hành động Duyệt ở hàng** (grep `can_approve` không có) ⇒ lệch quy tắc "danh sách = chi tiết" (CLAUDE.md), chỉ ghi nhận.
- **Hàng đợi "chờ duyệt"**: `?type=waitingApprove` = `status = 5` ∩ cùng cty, **chỉ khi có Q(duyệt)** — không có thì `1 = 0` (`OtherDeliveryTrip.php:132-146`). **Menu** `Chuyến xe khác chờ duyệt` gate `isShow: ['Duyệt chuyến xe khác']` (`hrm-client/components/subsystem-menu/transport.js:33`) — **thiếu "Thủ kho"**: người có quyền duyệt nhưng không có Thủ kho thấy menu nhưng mọi API trả 403 ("Bạn không có quyền truy cập màn chuyến xe khác").
**(d)** Người tạo tự duyệt: **không chặn** (`canApprove` không so `created_by`). Cũng không chặn người "Kết thúc chuyến" tự duyệt (`canFinish` ai xem được đều kết thúc — comment `:216-217`).
**(e)** Một người: lập → xuất phát → kết thúc → duyệt → hạch toán nếu giữ đủ quyền. Các quyền rời nhau (Thủ kho + Duyệt + Hạch toán) có thể ở một người.
**(f)** Thông báo: lúc Kết thúc ⇒ báo người có Q(duyệt) cùng cty chuyến (`WriteService.php:157-161`, `notifyPermission`); lúc Duyệt ⇒ báo người có Q("Hạch toán vận chuyển") (tên **khác** quyền thực hiện "Hạch toán chuyến xe khác" — comment entity `:59-61`).
**(g) Cho bảng gom**: cấp Chờ duyệt = **(a) Hai mã quyền đồng thời (AND)** `[Thủ kho, Duyệt chuyến xe khác]` + cùng cty. Cột gate đơn lẻ không đủ — cần `required_perms: [..., ...]` (AND). Cấp Chờ hạch toán: gate nhận HOẶC (2 quyền cho "thấy") nhưng AND/đơn (1 quyền) cho "thao tác" ⇒ **cột "thấy" ≠ cột "duyệt được"**: Definition phải tách `visible_perms` (OR) khỏi `act_perms`.

### B2. Tổng hợp giá vận chuyển đề xuất (THGVC)

**(a)** `Entities/DeliveryCostSummary/DeliveryCostSummary.php:29-33`: 3 Đang tạo → **2 Chờ duyệt** → 1 Đã duyệt (hoặc về 3 khi Không duyệt: `ApproveRequest` nhận `status ∈ {1,3}`, `Http/Requests/DeliveryCostSummary/ApproveRequest.php:24-25`) → 5 Đang lập HĐ → 4 Đã lập HĐ.
**(b)** `canApprove` = Q("Duyệt giá vận chuyển" = `warehouse.gia_van_chuyen.approve`) + `status = 2` (`DeliveryCostSummary.php:122-125`). **Không so công ty, không QL** — docstring `ApproveRequest.php:10` "KHÔNG chặn công ty".
**(c)** BE: route gắn `checkPermission:warehouse.gia_van_chuyen.approve` (`Routes/api.php:139-140`) + `ApproveRequest::authorize()` gọi `canApprove()` (`:15-24`) ⇒ BE chốt. **Hàng đợi** `?type=approve` = `status = 2` ∩ người LẬP cùng công ty với người duyệt, chỉ khi có Q(duyệt) (`Services/DeliveryCostSummary/DeliveryCostSummaryService.php:280-283`) ⇒ thấy phiếu chỉ cùng cty nhưng duyệt được cả phiếu cty khác (nếu biết id) — **lệch có chủ ý** (docstring). FE `delivery-cost-summaries/index.vue:231-253` dùng `hasAPermission` (fail-closed), `_id/index.vue:65-70`.
**(d)** Người tạo tự duyệt: không chặn. **(e)** n/a (1 cấp). **(f)** Duyệt ghi giá DUYỆT vào từng dòng + sinh BGHLVC (`DeliveryCostSummaryService.php:412-454`).
**(g)** Gate **(a) quyền + cùng cty của người lập** (khi xem hàng đợi) / **quyền thuần** (khi thao tác). Đơn giản; Definition `perm = warehouse.gia_van_chuyen.approve`, `company_scope = creator_company`.

### B3. Hợp đồng vận chuyển (+ phụ lục)

**(a)** `Entities/DeliveryContract/DeliveryContract.php:40-44`: 3 Đang tạo → **2 Chờ duyệt** (người lập `send`, `Services/DeliveryContract/DeliveryContractService.php:1042-1066`, chính chủ) → 1 Đã duyệt / 3 (Không duyệt = về Đang tạo, bắt buộc ghi chú) (`:1073-1113`); 0 Đã huỷ · 4 Đóng.
**(b)** `canApprove` = Q("Duyệt giá vận chuyển") + `status = 2` (`DeliveryContract.php:332-337`; comment `:331` "KHÔNG bó công ty — duyệt xuyên công ty, y ERP"). Service kiểm lại `isCurrentEmployeeHasPermission + status` (`:1087-1090`). Route `checkPermission:warehouse.gia_van_chuyen.approve` (`Routes/api.php:179-180`).
**(c)** Hàng đợi: không có tab `approve` riêng; danh sách theo phạm vi Xem (`scoped()` `:146-200`): tổng cty ⇒ tất cả; cty ⇒ phiếu của người lập cùng cty **HOẶC `approver_id` = mình**; phòng ban ⇒ cùng phòng người lập HOẶC `approver_id` = mình; không có quyền Xem ⇒ `1 = 0`. ⇒ người chỉ có "Duyệt giá vận chuyển" mà không có quyền Xem **không thấy phiếu** (fail-closed nhưng KHÔNG khớp ai duyệt được); `approver_id` = mình chỉ giúp "thấy" (chưa xác minh `approver_id` được ghi lúc nào ngoài lúc duyệt — `:1092`). FE `delivery-contracts/_id/index.vue:157-161` đọc `detail.is_can_approve`.
**(d)** Người lập tự duyệt: không chặn. **(f)** Thông báo "Chờ duyệt" gửi người có Q(duyệt) cùng cty NGƯỜI LẬP (`:1275-1290`).
**(g)** Giống B2: gate quyền; "ai thấy" khác "ai duyệt".

---

## C. DANH MỤC DÙNG CHUNG — MASTERDATA (`Modules/MasterData`, FE `pages/sale/*` + `pages/finance/product-price-approvals`)

Chuỗi nghiệp vụ gồm **5 chứng từ** nối nhau: YCHG (PTKD duyệt) → nhóm hàng (XNK) → YCTG (KTMH từ chối / lập PTG) → PTG → Duyệt giá bán (`product_approves`). Quyền đều là mã `finance.*` / `sale.*`; công ty đang làm quyết định, KHÔNG có điều kiện QL.

### C1. Yêu cầu hỏi giá (YCHG) — cấp PTKD (M1)

**(a)** `Entities/PriceCalculation/PriceAskingRequest.php:18-28, 30-43`: 3 Đang tạo → **2 Chờ PTKD duyệt** → 10 Đang hỏi giá / 8 Không duyệt; sau đó theo nhóm (C3). Mã 1/5/7 là phiếu cũ ERP hiện "Đang hỏi giá".
**(b)** `canPtkd` (`Services/PriceCalculation/PriceAskingAccess.php:120-123`) = `status = 2` + `company_id` phiếu = công ty đang làm + Q(`finance.yeu_cau_hoi_gia.approve`, tên "PTKD duyệt yêu cầu hỏi giá", catalog `finance.php:893-904`). **Không QL, không phòng.** Hạng dưới: hàng tạm (`tempApprove/tempReject/…`) và `lineDecide` cùng gate PTKD (`PriceAskingRequestWriter.php:519-548, 610-…`).
**(c)** BE chốt 3 lớp: route `checkPermission:finance.yeu_cau_hoi_gia.approve` (`Routes/api.php:421-424, 426-436`) + `assertWritable` (phiếu thấy được + của cty đang làm) + `lockForPtkd` (status, `PriceAskingRequestWriter.php:887-896`). FE `pages/sale/price-asking-requests/index.vue:139, 336` đọc `item.can_process`.
**Ai THẤY — KHÔNG khớp ai duyệt**: `scopeVisible` (`PriceAskingAccess.php:63-76`) = phiếu mình lập ∪ phạm vi XEM 4 cấp (`sale.yeu_cau_hoi_gia.view`, phạm vi 1-4; cấp phòng ban = **phòng QL**, `PriceViewScope.php:24, 128-135`); không có quyền Xem ⇒ chỉ phiếu mình (docblock `PriceAskingAccess.php:15-18`, "kể cả PTKD / XNK — như ERP, user chốt 21/10/2026"). ⇒ PTKD không có quyền Xem **không thấy phiếu Chờ PTKD của người khác**. Phiếu công ty khác thấy được nhờ quyền tổng công ty nhưng **chỉ xem** (403 `MSG_OTHER_COMPANY`).
**(d)** Người lập tự duyệt: **không chặn** (không so `created_by` trong `lockForPtkd`/`canPtkd`). **(e)** Người lập = PTKD = XNK phân công: làm được cả 3 bước một mình (xem C3).
**(f)** `dueConfig:Duyệt hàng tạm` chỉ ở các route duyệt hàng tạm (`Routes/api.php:431-433`) — chặn chính người duyệt còn hàng quá hạn.
**(g)**: **(a) quyền + cùng cty**, gate đơn giản: `{perm: finance.yeu_cau_hoi_gia.approve, company_scope: current}`; "thấy" cần khai thêm `visible_scope_code: sale.yeu_cau_hoi_gia.view` nếu muốn giữ đúng hành vi hiện tại (người duyệt không có Xem thì hôm nay không thấy), hoặc chốt thay đổi chủ ý.

### C2. Hàng tạm trong YCHG (M2)

Cấp: `product_company_coefficients.status` 6 (tạm, chờ PTKD) → 7 Đồng ý / 8 Không duyệt / 9 Duyệt không cần tính giá (`PriceAskingRequestWriter.php:519-548`). Gate = **cùng PTKD** (Q approve + phiếu `status = 2` + công ty phiếu = công ty đang làm). Không phải hàng đợi riêng — xử lý ngay trong form phiếu YCHG. **Không đưa vào bảng gom** (chỉ là chi tiết của C1; `inventory-hrm.md` đếm 1 hàng).

### C3. Nhóm hàng của YCHG — XNK duyệt / báo không có giá / huỷ (M3)

**(a)** `Entities/PriceCalculation/PriceAskingRequestGroup.php:18-24`: **5 Chờ XNK** (STATUS_WAITING_XNK) → 1 Chờ lập YCTG (sau XNK duyệt) → 7 Đã có YCTG → 4 Đã áp giá; 9 Không có giá; 6 Huỷ duyệt (chỉ khi chưa có YCTG); 11 Đã chuyển công ty quản lý. `inventory-hrm.md:398` ghi thêm 583 nhóm status NULL "tính là ở bước XNK" — chưa xác minh trong code mới (`groupXnkId` `PriceAskingAccess.php:142-148` vẫn coi `null` như chờ).
**(b)** `groupActions` (`PriceAskingAccess.php:158-168`): `can_approve`/`can_no_price` = phiếu `ASKING_STATUSES` + cty đang làm + nhóm status 5 + **`isGroupXnk`** (`:151-155`) = Q(`finance.yeu_cau_hoi_gia.update`, tên "XNK xử lý yêu cầu hỏi giá", platform **hrm only**) **VÀ** `XnkAssignmentResolver::resolve(brand_id, manufacture_id, company_id)` = **mình** (`Services/PriceCalculation/XnkAssignmentResolver.php:19-35`: dòng `assign_histories` `employee_date_to IS NULL`, mới nhất, `buy_employee_id`). ⇒ **Người đích danh theo từng nhóm (thương hiệu × hãng × công ty) + quyền**. Super admin không vượt (docblock `:21`).
**(c)** BE chốt: route `checkPermission:finance.yeu_cau_hoi_gia.update` (`Routes/api.php:437-441`) + `lockForXnk` → `isGroupXnk` 403 rồi `groupActions` 409 (`PriceAskingRequestWriter.php:973-988`). FE `index.vue:139, 336` (`can_process`). Ai thấy: như C1 (phạm vi Xem), kèm `can_process` tính theo `groupActions` ⇒ XNK phân công không có quyền Xem **không thấy** phiếu của người khác (docblock `PriceAskingAccess.php:15-18`).
**(d)** Người lập YCHG = XNK phân công: tự duyệt nhóm được (không chặn).
**(e) MỘT NGƯỜI GIỮ NHIỀU CẤP — ví dụ rõ nhất trong nhóm**: một nhân viên vừa lập YCHG, vừa có Q(PTKD duyệt) → PTKD duyệt phiếu mình lập; vừa là XNK phân công hiện hành của nhóm → duyệt nhóm; vừa có Q(Tính giá bán hàng hoá) → lập YCTG/PTG. Không có cơ chế "người duyệt cấp trước ≠ cấp sau" trong code (grep không có so sánh `approver_id`/`xnk_employee_id` giữa các cấp).
**(g)**: gate **(c) đích danh tính ĐỘNG** (không lưu trên phiếu mà tra `assign_histories` theo `brand_id × manufactures_id × company_id` — lưu ý cột `manufactures_id` có "s") **VÀ (a) quyền**. Không biểu diễn được bằng cột đơn giản: cần `resolver` riêng (hoặc ghi `xnk_employee_id` lúc chuyển PTKD→XNK để cố định, nhưng khi đó đổi phân công giữa chừng sẽ lệch hành vi hiện tại). Nên đưa vào bảng gom **theo mức nhóm** (1 dòng/nhóm status 5) chứ không theo mức phiếu.

### C4. Yêu cầu tính giá (YCTG) — KTMH từ chối (M4) và Phiếu tính giá (PTG)

**(a)** YCTG (`Entities/PriceCalculation/PriceCalculateRequest.php:18-23`): 3 Đang tạo · **2 Chờ tính giá** · 1 Đã có PTG · 4 Đã tính giá · 5 KTMH không duyệt · 6 PTG chờ duyệt giá. PTG (`PriceCalculate.php:18-21`): 3 Đang tạo · **5 Chờ duyệt giá** (hàng đợi M5) · 6 Giá bị từ chối · 1 Đã duyệt.
**(b)** KTMH từ chối YCTG: `canReject` (`Services/PriceCalculation/PriceCalculateRequestAccess.php:147-150`) = status 2 + cty phiếu = cty đang làm + Q(`finance.phieu_tinh_gia.create`, "Tính giá bán hàng hoá") + nhóm chưa đóng. Route `checkPermission:finance.phieu_tinh_gia.create` (`Routes/api.php:464`). **Không QL.** Lập PTG: cùng Q (`PriceCalculateAccess.php:20`).
**(c)** Ai thấy: phạm vi Xem `sale.yeu_cau_tinh_gia_ban.view` (YCTG) / `sale.tinh_gia_ban.view` (PTG) 1-4; không có thì chỉ phiếu mình lập, và vào được màn nếu là "actor" (có 1 trong 3 quyền XNK/Tính giá/Xem giá vốn, `PriceCalculateRequestAccess.php:60-68`) ⇒ **lọt danh sách rỗng** nếu thiếu phạm vi. FE `pages/sale/price-calculate-requests/index.vue:244-251`.
**(d)(e)** Người lập YCTG (XNK) ≠ người tính giá (Q phieu_tinh_gia.create) theo thiết kế quyền; **code không cấm một người có cả 2 quyền** làm cả hai.
**(g)**: YCTG chờ tính giá = gate quyền `finance.phieu_tinh_gia.create` + cty; PTG chờ duyệt giá **không có người duyệt riêng** — nó chuyển thành hàng đợi C5 (`product_approves`). Chỉ đưa C5 vào bảng gom, YCTG ("Chờ tính giá") là hàng đợi **công việc**, không phải duyệt.

### C5. Duyệt giá bán hàng hoá (`product_approves`) — (M5)

**(a)** Không có cột status; **có dòng = đang chờ**, xử lý xong xoá cứng (docblock `Services/ProductPrice/ProductPriceApprovalService.php:15-40`). 1 cấp. PTG/hàng tạm sinh dòng.
**(b)** Route group gắn `checkPermission:finance.gia_ban_hang_hoa.approve` (`Routes/api.php:493-503`; catalog `finance.php:848-858`, platform hrm). Phạm vi: `product_approves.company_id` = công ty đang làm (`ProductPriceApprovalService.php:264-272, 476-` / `openApproves` `:831`). **Không QL, không phòng.** Hàng đang khoá ⇒ Duyệt 422, Không duyệt vẫn được (docblock). Người **không có quyền Xem giá vốn** (`master_data.gia_von_hang_hoa.view`) vẫn duyệt được nhưng không thấy giá vốn/hệ số (`:93-95`).
**(c)** BE chốt: route + lọc công ty + khoá hàng (`assertNotLocked`). Hàng đợi **chính là danh sách** (`/finance/product-price-approvals`, menu `finance.js:522, 690`, gate `codes: ['finance.gia_ban_hang_hoa.approve']`) ⇒ **khớp ai thấy = ai duyệt** (đều chỉ cần quyền + công ty).
**(d)** Người lập (đề xuất giá, `product_expected_prices` / PTG) tự duyệt: **không chặn** — chỉ thông báo cho người đề nghị (`ProductPriceApprovalService.php:508-513`); không có so sánh `created_by`/`proposer` với người duyệt.
**(e)** Một người = PTG người lập (Q Tính giá) + Q Duyệt giá bán: tự duyệt phiếu mình tính — không chặn.
**(g)**: **(a) quyền + công ty bộ giá** — biểu diễn được bằng gate đơn giản; nhưng "đối tượng chờ" **không phải 1 bản ghi có status** (có dòng = chờ, duyệt xong xoá) nên bảng gom phải **đồng bộ theo sự kiện tạo/xoá dòng**, không đọc cột status.

### C6. Danh mục MasterData khác — không có luồng duyệt

`MasterData/Routes/api.php` chỉ có `approve/reject` ở 3 cụm: `price-asking-requests`, `price-calculate-requests`, `product-price-approvals`. Các danh mục khác (hàng hoá, đơn vị, thuế, kho, danh mục chung…) chỉ có Khoá/Mở khoá (lifecycle `PUT {id}/lock|unlock`, gate `checkPermission:<build>`), **không có "chờ duyệt"**. `temp-products` (hàng tạm) chỉ lập/sửa/xoá; việc duyệt hàng tạm nằm trong YCHG (C2).

---

## D. MENU BÁN HÀNG › PHÊ DUYỆT — màn đã có trên HRM nhưng lưu ở module Finance

Nguồn menu: `hrm-client/components/subsystem-menu/sale-hub.js:329-366`. Các màn chạy trên `Modules/Finance` (`Routes/api.php:1735-1872`). **Không có trong `danh-gia-tung-phieu.md`** (mục "Chỉ tiêu kinh doanh" và "Phân chia thị trường" có; "KH bán hàng/KH PTTT" ghi sai là chưa có màn).

### D1. Kế hoạch bán hàng / KH phát triển thị trường của nhân viên (`sale-plan-employees`, `market-plan-employees`)

**(a)** `Entities/EmployeePlan/EmployeePlan.php:26-31, 37-44`: 1 Đang tạo → **2 Chờ TP duyệt** → 3 TP đã duyệt → **4 Chờ BGĐ duyệt** → 5 BGĐ đã duyệt; 6 Hủy. Người lập **là trưởng phòng của chính phòng phiếu** ⇒ Gửi duyệt đi **thẳng 4** (`creatorIsHead`, `EmployeePlan.php:363-369`; `Services/EmployeePlan/EmployeePlanService.php:476-488`). **BGĐ duyệt (4→5) KHÔNG có màn HRM** (`sendDirector` docblock "chưa có màn BGĐ duyệt", `:521-523`): chỉ phiếu `form_version = 2` (HRM) mới thao tác trên HRM (`isHrmForm`).
**(b)** Cấp TP: `canApprove` = phiếu HRM + `status = 2` + `isHeadOfPlan` (`EmployeePlan.php:280-283, 322-325`): **không phải người lập** + `department_id` phiếu ∈ `approvableDepartmentIds()` = (nếu có Q(`sale.ke_hoach_ban_hang_nhan_vien.approve` / `sale.ke_hoach_phat_trien_thi_truong_nhan_vien.approve`)) **{các phòng có dòng `employee_manage_departments` của mình (chỉ `whereNotNull(department_id)`, KHÔNG cờ `all_department`) ∪ phòng ngồi của mình}** (`:184-207`). ⇒ **Q(mã duyệt) VÀ (QL phòng phiếu HOẶC cùng phòng)** — nhân viên thường cùng phòng có mã duyệt cũng duyệt được (đúng luật ERP `canDepartmentApprove`, docblock `:20`). Cấp "Gửi BGĐ": `canSendDirector` = status 3 + `isHeadOfPlan` (`:332-335`) = **cùng người** TP vừa duyệt (hoặc người khác thoả điều kiện).
**(c)** BE: route `approve/reject/send-director` gắn `checkPermission:<mã duyệt>` (`Routes/api.php:1869-1871`) + `transition()` kiểm `canApprove`/`canReject`/`canSendDirector` → 403 (`Http/Controllers/V1/EmployeePlanBaseController.php:141-162, 247-251`). **Hàng đợi** `?type=for-approve` (menu `sale-hub.js:360-361`, `codes: [mã duyệt]`) = `applyForApproveScope` (`EmployeePlan.php:257-269`): phòng ∈ approvable + status ∈ {2, 3} + `created_by ≠ mình` + phiếu HRM ⇒ **khớp ai duyệt/gửi BGĐ được**.
**(d)** Người lập tự duyệt: **bị chặn** (`!isOwner` trong `isHeadOfPlan` và `created_by <> me` trong hàng đợi). Nếu người lập là TP của phòng → phiếu bỏ qua cấp TP (chuyển thẳng "Chờ BGĐ").
**(e) Nhiều cấp, một người**: một TP vừa duyệt cấp 2→3 vừa "Gửi BGĐ" 3→4 (hai thao tác liên tiếp, cùng điều kiện) — chủ ý. Người giữ cả "TP" và "lập" thì cấp TP bị bỏ.
**(g)**: Gate **(a) mã quyền duyệt + (b) QL phòng HOẶC cùng phòng**, kèm `exclude_creator = true` và cờ `form_version = 2`. Biểu diễn bằng 1 cột đơn giản: **KHÔNG** — cần `manager_variant = manage_rows_or_own_department` + loại trừ người lập. Cấp 4 "Chờ BGĐ duyệt": **không có người duyệt trên HRM** ⇒ không đưa vào hàng đợi của ai (hoặc khai "duyệt ở ERP").

### D2. Giao chỉ tiêu kinh doanh — phòng ban (`business-target-departments`) và nhân viên (`business-target-employees`)

**(a)** `Entities/BusinessTarget/BusinessTargetCompany.php:30-33` + `Concerns/HasBusinessTargetStatus.php:14-19`: 1 Đang tạo → **2 Chờ duyệt** → 3 Đã duyệt; 5 Hủy; Từ chối / Huỷ duyệt → 1. **1 cấp.**
**(b)** `canApprove` (`Concerns/HasBusinessTargetAccess.php:127-130`) = `status = 2` + `canActAsApprover` (`:112-115`) = Q(`sale.chi_tieu_kinh_doanh_phong_ban.approve` hoặc `…_nhan_vien.approve` cho bản nhân viên, `BusinessTargetForDepartment.php:37-39`) + **cùng cty** (`sameCompanyAsCurrent`). Quyền duyệt **không có phạm vi** (comment `:79` "quyền Duyệt không có phạm vi"). **Không QL phòng.** `canUnApprove` = status 3 + cùng điều kiện (`:137-140`).
**(c)** BE: route `checkPermission:<mã>` + `transition` → `canApprove` (`Http/Controllers/V1/BusinessTargetBaseController.php:55-72`). **Hàng đợi** `?type=for-approve` (`sale-hub.js:362-363`): `applyForApproveScope` = `status = 2` ∩ cty đang làm, chỉ khi có quyền (`Concerns/HasBusinessTargetAccess.php:79-89`) ⇒ **khớp**. Người duyệt cũng thấy phiếu Chờ duyệt của cty trong danh sách chính (`:56-72`).
**(d)** Người lập tự duyệt: **không chặn** (không so `created_by`). **(e)** Một người = lập (Q create) + duyệt (Q approve) cùng cty: được.
**(g)**: **(a) quyền + cùng cty** — gate đơn giản; Definition `perm = …approve`, `company = document.company_id`.

### D3. Phiếu phân chia thị trường — phòng ban / nhân viên

- **Theo phòng ban** (`Entities/DivisionMarket/DivisionMarketDepartment.php:31-38`): chỉ 2 trạng thái **1 Đang tạo → 2 Đã duyệt**; không có "Chờ duyệt" — người có Q("Duyệt phiếu phân chia thị trường theo phòng ban") duyệt **thẳng** phiếu Đang tạo hoặc dùng "Lưu và duyệt" (`canApprove = !isApproved && Q`, `:182-185`; `Http/Controllers/V1/DivisionMarketDepartmentController.php:160, 180, 232-235`). Không công ty. Người ngoài **không thấy** phiếu Đang tạo của người khác nếu không có quyền Xem công ty/tổng công ty (`applyViewScope` `:138-153`). ⇒ **Không phải hàng đợi duyệt**; loại khỏi bảng gom.
- **Theo nhân viên** (`DivisionMarketDepartmentEmployee.php:31-33`): 1 Đang tạo → **3 Chờ duyệt** → 2 Đã duyệt. `canApprove` = `status = 3` + Q("Duyệt phiếu phân chia thị trường theo nhân viên") + **cùng cty** (`allowed`, `:203-211, 235-238`). Người duyệt thấy phiếu Chờ duyệt cùng cty trong danh sách (`applyViewScope` `:152-183`). Route `checkPermission` + `recordNotLocked` (`Routes/api.php:1765-1790`). Người lập (Q create) tự duyệt: **không chặn**. Gate = **quyền + cùng cty** (đơn giản).

### D4. Các mục menu Phê Duyệt CHƯA có màn HRM (đối chiếu `sale-hub.js:329-345`)
Chuỗi trần (chưa là link): HĐ Vật tư-HH-TB (+PL), PL bổ sung/giảm của HĐ SC-BD-BT, HĐ Nguyên tắc, ĐH Nguyên tắc, HĐ Dự án, Biên bản thanh lý chờ duyệt, Quyết toán HĐ chờ duyệt. Có link nhưng thuộc Assign (ngoài phạm vi báo cáo này): Yêu cầu giải pháp chờ duyệt, Báo giá chờ duyệt. Khớp `danh-gia-tung-phieu.md §6`.

---

## E. "MỘT NGƯỜI NHIỀU CẤP" và "tự duyệt" — tổng hợp nhóm này

| Luồng | Tự duyệt (người lập = người duyệt) | Một người giữ nhiều cấp |
|---|---|---|
| A1 HĐ SC-BD-BT | Cho phép (QL phòng của `department_id` HĐ hoặc `approver_id`) | 1 cấp; nhưng nếu `approver_id` có thì QL phòng bị loại (không phải HOẶC) |
| A2 PNKQ | Cho phép | Người mở form duyệt = người duy nhất tiếp tục/ không duyệt khi PNKQ "Đang duyệt" |
| A3 YC kiểm tra | Cho phép (nếu trùng phòng tiếp nhận) | — |
| A4/A5/A6/A7 | A5 cho phép khi trùng người lập YC; A4/A6/A7 cho phép | — |
| A8 BB bàn giao sơ bộ | Cho phép (và mọi người khác cũng duyệt được) | — |
| B1 Chuyến xe khác | Cho phép | Thủ kho + Duyệt + Hạch toán là 3 quyền rời nhau, có thể chung 1 người |
| B2/B3 THGVC / HĐ VC | Cho phép | — |
| C1→C5 chuỗi giá | Cho phép (không so `created_by`) | 1 người = lập YCHG + PTKD + XNK phân công + Tính giá + Duyệt giá bán; code không chặn |
| D1 KH nhân viên | **Chặn** (`!isOwner`; người lập là TP ⇒ nhảy cấp thẳng "Chờ BGĐ") | TP duyệt (2→3) rồi tự "Gửi BGĐ" (3→4) |
| D2/D3 | Cho phép | — |

Không có luồng nào trong nhóm kiểm "người duyệt cấp sau ≠ người duyệt cấp trước" (grep `approver_id`, `xnk_employee_id`, `approved_by` không có so sánh chéo).

---

## F. ĐÁNH GIÁ CHO BẢNG GOM — Definition phải khai gì

Câu hỏi: để biết "người X thấy phiếu này ở cấp hiện tại", Definition cần (1) mã quyền + phạm vi, (2) quản lý phòng nào, (3) người đích danh, (4) kết hợp.

| Luồng / cấp | (1) Mã quyền (+ phạm vi) | (2) QL phòng | (3) Đích danh | (4) Kết hợp | Cột gate đơn giản đủ? |
|---|---|---|---|---|---|
| A1 HĐ SC-BD-BT, Chờ duyệt | Không | QL phòng `department_id` (V3) | `approver_id` | **rẽ nhánh**: có `approver_id` ⇒ chỉ người đó, không ⇒ QL phòng | **Không** |
| A2 PNKQ 2 | `customer_care.phieu_nhap_ket_qua.approve` + cùng cty | — | — | — | Có |
| A2 PNKQ 5 | — | — | người tạo PDKQ con | join bảng con | Không (nên loại) |
| A3 YC kiểm tra, Chờ xử lý | `…yeu_cau_di_kiem_tra….confirm` | — | — | AND phòng tiếp nhận = phòng mình | Một phần ("phòng của tôi" ≠ QL phòng) |
| A4 Phiếu xử lý, Chờ CCTT | `customer_care.phieu_cung_cap_thong_tin.create` | — | — | — | Có |
| A5 CCTT, Chờ báo giá | — | — | `request.created_by` (qua bảng cha) | điều kiện dòng sửa chữa | Không (nên loại) |
| A6/A7 tiếp nhận | A6: `…phieu_giao_viec.create`; A7: không | — | — | AND phòng tiếp nhận = phòng mình | Một phần |
| A8 BB bàn giao sơ bộ | Không (BE không kiểm) | — | `approver_id` (thông báo) | — | Cần user chốt |
| B1 Chuyến xe khác, Chờ duyệt | `warehouse.chuyen_xe_khac.approve` **AND** `warehouse.thu_kho.manage` + cùng cty | — | — | AND nhiều quyền | Không (cần mảng AND) |
| B1 Chờ hạch toán | thấy: `Hạch toán chuyến xe khác` OR `Hạch toán vận chuyển`; làm: chỉ `Hạch toán chuyến xe khác` | — | — | OR (thấy) / đơn (làm) | Không (tách `visible` ≠ `act`) |
| B2 THGVC | `warehouse.gia_van_chuyen.approve` + cùng cty người lập (hàng đợi) | — | — | — | Có |
| B3 HĐ vận chuyển | `warehouse.gia_van_chuyen.approve` (thấy còn cần quyền Xem hoặc `approver_id`) | — | `approver_id` (chỉ để thấy) | — | Một phần |
| C1 YCHG, Chờ PTKD | `finance.yeu_cau_hoi_gia.approve` + cùng cty | — (chỉ khi dùng phạm vi Xem: phòng QL) | — | thấy = phạm vi Xem OR mình lập | Có (thao tác) / Một phần (thấy) |
| C3 Nhóm XNK | `finance.yeu_cau_hoi_gia.update` | — | **XNK phân công hiện hành** (tra `assign_histories`) | AND | Không (cần resolver động) |
| C4 YCTG chờ tính giá | `finance.phieu_tinh_gia.create` + cùng cty | — | — | — | Có (nhưng là việc, không phải duyệt) |
| C5 Duyệt giá bán | `finance.gia_ban_hang_hoa.approve` + công ty bộ giá | — | — | — | Có (đối tượng = dòng tồn tại, không có status) |
| D1 KH nhân viên TP | `sale.ke_hoach_ban_hang_nhan_vien.approve` (hoặc `…phat_trien_thi_truong…`) | QL phòng (rows) **OR** cùng phòng | loại trừ người lập | AND + OR + NOT | Không |
| D2 Chỉ tiêu | `sale.chi_tieu_kinh_doanh_{phong_ban,nhan_vien}.approve` + cùng cty | — | — | — | Có |
| D3 Phân chia thị trường NV | `Duyệt phiếu phân chia thị trường theo nhân viên` + cùng cty | — | — | — | Có |

**Các điểm KHÔNG biểu diễn được bằng "một cột gate đơn giản" và đề xuất**:
1. **Rẽ nhánh theo dữ liệu dòng** (A1): `assignee_column` + `fallback_manager_department_column`. Cần kiểu gate `assignee_or_manager`.
2. **AND nhiều quyền** (B1 Thủ kho + Duyệt): `required_perms[]`.
3. **Tách "thấy" ≠ "duyệt được"** (B1 Chờ hạch toán, B3, C1 người duyệt thiếu quyền Xem): Definition phải có `visible` và `act` riêng, kèm lựa chọn "người duyệt luôn thấy" (đề xuất bảng gom: người có `act` luôn thấy, đổi hành vi hiện tại có chủ ý — cần user chốt).
4. **"Phòng của tôi" (không phải "phòng tôi quản lý")** (A3, A6, A7): thêm `own_department_column`.
5. **Người đích danh động qua bảng khác** (C3 `assign_histories`; A2 PNKQ 5 `wr_assign_tasks.created_by`; A5 `warranty_repair_requests.created_by`): cần `resolver` hoặc snapshot khi chuyển cấp.
6. **Loại trừ người lập** (D1 có, các luồng khác không): cờ `exclude_creator`, mặc định **false** để khớp hành vi hiện tại; D1 bật.
7. **Đối tượng không có cột trạng thái** (C5): đồng bộ theo sự kiện tạo/xoá dòng.
8. **Biến thể "phòng tôi quản lý"**: A1 dùng V3 (không cờ `all_department`, công ty gốc); D1 dùng "rows + phòng ngồi" (cũng không cờ tổng); các luồng khác dùng quyền thuần ⇒ Definition cần `manager_variant` (xem 00-ha-tang §1.6).
9. **Công ty**: nhiều luồng so `company_id` phiếu với công ty đang làm (`PermissionChecker` cũng tính quyền theo công ty đó); B2, B3, B1 (người có Xem tổng công ty) **cố ý không bó** ⇒ Definition cần `company_scope ∈ {document, creator, none}`.

---

## G. Mâu thuẫn với tài liệu nền (cần sửa trong `inventory-hrm.md` / `danh-gia-tung-phieu.md`)

| # | Tài liệu nền | Code hiện tại |
|---|---|---|
| 1 | `inventory-hrm.md:16-26` khe `model_type` làm CustomerCare "khoá với mọi người", MasterData chỉ 9-26 người qua được | Đã đóng: `PermissionChecker` bỏ qua `model_type` (`PermissionChecker.php:15-17`); gate theo Vai trò thuộc công ty (`roles.company_id`) |
| 2 | `inventory-hrm.md:379-381` "0 người giữ `Tạo phiếu giao việc`, chỉ guard web" | Catalog có cả `api` + `web` (`Catalog/customer_care.php:557-559`) |
| 3 | `inventory-hrm.md:20-24` CEP / Super admin vượt quyền ~20 luồng; C1, C4, C5 SA vượt | Không có SA vượt: `ChecksEmployeePermission.php:5-9`; `getIsCanApproveAttribute` không có nhánh SA; `Transport/.../ApproveRequest`, `PriceAskingAccess.php:21` ghi rõ không bypass |
| 4 | `danh-gia-tung-phieu.md:73` / `inventory-hrm.md:386` HĐ SC-BD-BT: "`approver_id` hoặc quản lý phòng" | **XOR theo dữ liệu**: có `approver_id` ⇒ chỉ người đó (`WrServiceContract.php:396-401`) |
| 5 | `inventory-hrm.md:377` C1 MW `Xử lý yêu cầu sửa chữa` (tên cũ) | Route/entity dùng mã `customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm` (`Routes/api.php:271-274`, entity `:85`) — cùng quyền, tên khác |
| 6 | `inventory-hrm.md:403, 407` MD Tên quyền ("XNK xử lý…", "Tính giá bán hàng hoá") dùng MW cũ | Nay là mã `finance.yeu_cau_hoi_gia.update`, `finance.phieu_tinh_gia.create`; không đổi bản chất |
| 7 | `danh-gia-tung-phieu.md §6` "KH bán hàng, KH phát triển thị trường **chưa có màn**" | Có màn (`sale-plan-employees`, `market-plan-employees`), đã gắn menu `sale-hub.js:360-361` — D1 |
| 8 | `danh-gia-tung-phieu.md §4` Chuyến xe khác: "quyền 'Duyệt chuyến xe khác'" | **Thêm** quyền "Thủ kho" bắt buộc (`OtherDeliveryTripController.php:50-54`) |
| 9 | `danh-gia-tung-phieu.md §4` PNKQ "quyền 'Duyệt phiếu nhập kết quả'" | Đúng, **thêm** điều kiện cùng công ty (`WrImportResultService.php:574-582`) và cấp "Đang duyệt" chỉ người tạo PDKQ |
| 10 | Không có | Biên bản bàn giao sơ bộ (A8), Phiếu yêu cầu giao việc khác (A7), THGVC (B2), HĐ vận chuyển (B3), chuỗi giá C3-C5 (chi tiết) chưa có trong 2 tài liệu nền ở mức người duyệt |

---

## H. Chưa xác minh

1. `approver_id` của `wr_service_contracts` do ERP ghi lúc nào (HĐ lập từ ERP) và có phổ biến không — cần SELECT phần `status=2 AND approver_id IS NOT NULL`.
2. Người kiêm nhiệm (làm việc ở công ty phụ): `managedDepartmentIds` (A1) dùng công ty gốc `info->company_id` nên có thể không thấy phòng quản lý ở công ty kiêm nhiệm — chưa chạy thử.
3. `company_id` của PNKQ / `wr_import_results` gán theo công ty người lập hay công ty chứng từ gốc (`WrImportResultStoreService` — chưa đọc dòng gán).
4. `applyScope` đầy đủ của Phiếu xử lý yêu cầu (A4) có lối "thấy theo quyền tạo CCTT" hay không.
5. `WrServiceContractNotifier::notifyApproved/Rejected` và người nhận thông báo "Chờ duyệt" của HĐ SC-BD-BT.
6. Nhóm YCHG `status NULL` (583 nhóm theo `inventory-hrm.md:398`): vẫn tính như bước XNK; chưa thử trên dữ liệu.
7. Nút Duyệt chuyến xe khác/THGVC ở hàng danh sách: chỉ thấy ở form; chưa kiểm FE danh sách THGVC/HĐVC có hành động Duyệt ở hàng hay không (grep `is_can_approve` ở `index.vue` không có).
8. ERP vẫn còn route duyệt cho A1-A6, B1-B3 (tài liệu nền); chưa kiểm phía ERP có khoá kiểu `productMovedToHrm` cho các luồng nào ngoài MasterData.
