# Phiếu chờ duyệt tập trung (ERP) — Design

> Dự án: ERP TanPhatDev. Nhánh: `master` (tạo feature branch khi bắt đầu code). Phụ trách: @namdangit.
> Trạng thái: **THIẾT KẾ XONG — chưa code** (2026-08-12).
> Inventory đầy đủ ~130 luồng + checklist gắn code: xem `plan.md`.

---

## 1. Mục tiêu

Gom tất cả "phiếu chờ duyệt" của mọi luồng nghiệp vụ ERP về **1 màn hình tổng hợp**, **lọc theo loại phiếu**.
Hiện mỗi luồng có màn chờ duyệt riêng (`.forApprover`/`.forApproved`/`?type=waiting`), người dùng phải đi từng chỗ.

**Làm cho ERP trước** (ERP cần dùng ngay). Sau khi gộp DB (`gop_db`) hoàn tất, các luồng HRM ghi chung vào cùng bảng registry → không phải làm lại kiến trúc.

## 2. Hiện trạng (kết quả khảo sát)

- **KHÔNG có engine duyệt / bảng workflow chung.** Mỗi Model tự khai trạng thái trên chính bảng nghiệp vụ, quy ước phổ biến `status`: `CHO_DUYET=2`, `DA_DUYET/CO_HIEU_LUC=3`, `TU_CHOI=4` (mẫu `FirmContract.php:97-110`). Một số luồng thêm `approver_id`, `approved_by`, `approved_at`, `first_approver_id`, `department_approve_time`.
- **"Người duyệt hiện tại" xác định động**, 3 cách: (a) theo quyền `$user->can('Duyệt ...')` — phổ biến nhất; (b) theo cột `approver_id` đích danh (HĐ bán, báo giá dự án); (c) theo role/phân công (hàng giữ/mượn nhiều cấp).
- **Đã có sẵn màn gộp dạng đếm**: `HomeController@approveList` (`app/Http/Controllers/HomeController.php:496`, ~2145 dòng, ~130 khối `if can(...)`) + `home.blade.php:148` (AngularJS `ng-repeat`). Mỗi item hiện chỉ trả `['group','name','link','count']` → **đếm + link tới màn danh sách**, chưa duyệt tại chỗ, chưa lọc theo loại, không liệt kê từng phiếu.
- **Mọi luồng đều có route `.show` (GET `/{id}`)** mở thẳng 1 phiếu — đã verify `firmContract.show`, `settlementContract.show`, `bill_payment_request.show`, `productExportRequest.show`, `ProjectQuotation.show`, `warrantyRepairRequest.show`, `inlandBuyContractNew.show`... → deep-link mở thẳng phiếu khả thi toàn hệ thống.
- Chặn duyệt khi có NV quá hạn công nợ: middleware `checkDueConfigsManager` / `CheckDueConfigs` (giữ nguyên, không đụng).
- Lịch sử duyệt chi tiết từng cấp: chỉ vài luồng có (`contract_approver_histories`, `price_asking_request_approve_histories`, bên HRM có `decision_history_approves`...). Registry KHÔNG nhân bản log này.

## 3. Quyết định thiết kế (đã chốt qua brainstorming)

| # | Quyết định | Chi tiết |
|---|---|---|
| 1 | **Hộp duyệt cá nhân** | Chỉ hiện phiếu mà người đăng nhập có quyền/trách nhiệm duyệt (không phải bảng giám sát toàn hệ thống). |
| 2 | **Deep-link mở thẳng phiếu** | Màn gộp = liệt kê + lọc; bấm phiếu → gọi route `<luồng>.show` (GET `/{id}`) mở **thẳng đúng phiếu** đó, không dừng ở màn danh sách. Không duyệt inline (giai đoạn 1). Đã verify: mọi luồng đều có route `.show` dạng `/{id}`. |
| 3 | **Registry tập trung (push)** | 1 bảng chung `approval_inbox`; mỗi luồng đẩy phiếu vào khi chờ duyệt; màn gộp chỉ đọc 1 bảng. |
| 4 | **Xác định người duyệt theo QUYỀN + PHẠM VI** | Registry lưu `required_permission` + `company_id`/`department_id`/`part_id`. Lọc: user CÓ quyền đó VÀ khớp phạm vi. |
| 5 | **Không xóa bản ghi** | Luồng nhiều cấp → `advance()` đổi quyền/cấp trên CÙNG 1 dòng; kết thúc → `resolve()` đổi `status`. Giữ lịch sử trong cùng bảng. |
| 6 | **Giai đoạn hiện tại** | Chỉ khảo sát + thiết kế + plan. Chưa code. |

## 4. Kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│  ~130 luồng nghiệp vụ ERP (24 nhóm)                          │
│  Khi phiếu chuyển sang CHỜ DUYỆT / duyệt 1 cấp / kết thúc    │
│        │ push()        │ advance()        │ resolve()         │
│        ▼               ▼                  ▼                   │
│              ApprovalInboxService (ERP)                      │
│                        │                                     │
│                        ▼                                     │
│              ┌───────────────────────┐                       │
│              │  bảng approval_inbox  │  ← 1 dòng / 1 phiếu    │
│              └───────────────────────┘                       │
│                        ▲ đọc (lọc theo quyền + phạm vi)      │
│                        │                                     │
│   Màn gộp: Blade + AngularJS + Yajra DataTable (server-side) │
│   → mỗi dòng có nút "Duyệt" link sang màn duyệt gốc          │
└─────────────────────────────────────────────────────────────┘
   (Sau khi gộp DB xong: HRM cũng push vào cùng bảng này)
```

## 5. Schema bảng `approval_inbox`

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | bigint PK | |
| `source_system` | varchar(10) | `erp` \| `hrm` (chuẩn bị cho gộp) |
| `doc_type` | varchar(64) index | Mã loại phiếu để **lọc** (vd `firm_contract`, `project_quotation`, `bill_payment_request`). |
| `doc_type_label` | varchar(255) | Tên hiển thị ("Hợp đồng bán hàng", "Báo giá dự án"). |
| `group_code` | varchar(64) index | 1 trong 24 nhóm (mượn nhóm của `approveList`). |
| `source_table` | varchar(64) | Bảng gốc (vd `firm_contracts`). |
| `source_id` | bigint index | Id bản ghi gốc. |
| `code` | varchar(64) | Mã phiếu. |
| `title` | varchar(500) | Tiêu đề/nội dung tóm tắt. |
| `requester_id` | bigint null | Người tạo phiếu (`created_by`). |
| `requester_name` | varchar(255) null | Cache tên người tạo (tránh join). |
| `document_date` | date null | Ngày phiếu. |
| `required_permission` | varchar(255) index | **Tên quyền cần để duyệt ở cấp hiện tại.** |
| `alt_permissions` | json null | Các quyền thay thế cùng duyệt được cấp hiện tại (nhiều quyền OR). |
| `company_id` | bigint null index | Phạm vi công ty. |
| `department_id` | bigint null index | Phạm vi phòng ban. |
| `part_id` | bigint null index | Phạm vi bộ phận. |
| `approver_id` | bigint null index | Đích danh nếu luồng có sẵn (bổ trợ cho quyền). |
| `current_level` | tinyint default 1 | Cấp duyệt hiện tại (luồng nhiều cấp). |
| `level_started_at` | datetime null | Thời điểm phiếu VÀO cấp hiện tại (để tính TG duyệt theo từng cấp). Cập nhật mỗi lần `push`/`advance`/tái kích hoạt. |
| `round` | tinyint default 1 | Vòng gửi duyệt hiện tại (tăng mỗi lần bị từ chối rồi gửi lại). |
| `amount` | decimal(20,2) null | Giá trị tiền (hiển thị/sắp xếp). |
| `approve_route` | varchar(255) null | Tên route **mở thẳng phiếu** — dạng `<luồng>.show` (GET `/{id}`). |
| `approve_params` | json null | Tham số build link — tối thiểu là `id` (=`source_id`); kèm param phụ nếu route cần. |
| `status` | tinyint index | `1=pending`, `2=approved`, `3=rejected`, `4=canceled`. |
| `resolved_at` | datetime null | Khi kết thúc. |
| `resolved_by` | bigint null | Người thao tác cuối. |
| `created_at`/`updated_at` | timestamps | |
| `created_by`/`updated_by` | bigint null | Audit. |

- **Unique idempotent**: `(source_system, source_table, source_id)` — mỗi phiếu tối đa 1 dòng, tránh push trùng.
- Index tổng hợp lọc cá nhân: `(status, required_permission, company_id)`.

## 6. Lọc "phiếu cần tôi duyệt"

**Quy tắc (đã sửa để khớp `canTranferApprove` của luồng — Task 9i):** phiếu **đã chỉ định người duyệt** (`approver_id` set, vd sau "chuyển duyệt" lên BGĐ) → **CHỈ** hiện cho đúng người đó; phiếu **chưa chỉ định** (`approver_id` null) → theo **quyền + phạm vi công ty**.

```sql
WHERE status = 1 -- pending
  AND (
    -- (1) Phiếu đã chỉ định approver → CHỈ đúng người đó (khớp canTranferApprove: approver_id == auth)
    ( approver_id IS NOT NULL AND approver_id = <user.id> )
    OR
    -- (2) Phiếu chưa chỉ định → theo quyền + phạm vi công ty
    ( approver_id IS NULL
      AND required_permission ∈ <quyền của user>
      AND ( company_id IS NULL OR company_id = <user.company_id> ) )
  )
```

> LƯU Ý (design tension đã biết): nhánh (2) dùng `required_permission` + `company_id` làm **proxy** cho gating thật của luồng. Với firm_contract cấp TP, gating thật là "dept-manager của phòng HĐ (EmployeeManageDepartment) HOẶC Super Admin" — registry chưa mã hóa dept-manager nên non-super-admin có quyền "Duyệt hợp đồng" nhưng KHÔNG quản phòng đó vẫn thấy phiếu (edge, defer). Cấp BGĐ (đã chỉ định) thì khớp chính xác qua nhánh (1).

> Quy tắc khớp phạm vi bám theo cách `approveList` đang lọc (173 chỗ dùng `company_id/department_id`): đa số lọc theo `company_id` của user; một số theo phòng ban; vài quyền có biến thể "Xem theo tổng công ty / công ty / phòng ban / bộ phận" (vd hạch toán CP vận chuyển nhanh) → map thành mức phạm vi khi push.

## 7. Cơ chế push — `ApprovalInboxService`

3 thao tác chuẩn, gắn vào từng luồng (đặt cạnh chỗ đổi `status`):

| Hàm | Gọi khi | Hành vi |
|---|---|---|
| `push($entry)` | Phiếu chuyển sang **chờ duyệt** (tạo mới gửi duyệt, hoặc chuyển duyệt cấp đầu) | `updateOrCreate` theo unique key → 1 dòng `status=pending`, set `required_permission`+phạm vi cấp đầu. |
| `advance($src, $newPermission, $newLevel, $altPerms=[])` | Duyệt xong 1 cấp mà **còn cấp sau** | CÙNG dòng: đổi `required_permission`/`alt_permissions`/`current_level` sang cấp kế. Vẫn `pending`. |
| `resolve($src, $status, $userId, $reason=null)` | Duyệt xong **cấp cuối** / từ chối / hủy | Đổi `status` (approved/rejected/canceled) + `resolved_at`/`resolved_by`; ghi log bước cuối kèm `note=$reason` (**lý do từ chối** nếu có). **Không xóa dòng.** |

- `$src` = `(source_table, source_id[, source_system])`.
- **Backfill**: command `approval-inbox:backfill {group?}` quét trạng thái pending hiện tại của từng luồng (tái dùng chính điều kiện lọc trong `approveList`) → nạp registry lần đầu, idempotent theo unique key.
- **Nguồn tham chiếu vàng**: mỗi khối `if can(...)` trong `approveList` đã mã hoá sẵn (quyền, phạm vi, count query, link) cho từng luồng → copy trực tiếp sang push/backfill.

## 8. Màn gộp (Blade + AngularJS + Yajra DataTable)

- Route mới (vd `approvalInbox.index` + `approvalInbox.searchData`), controller mới `ApprovalInboxController` (không phình `HomeController`).
- **DataTable server-side** (pattern chuẩn ERP): cột Loại phiếu · Mã · Tiêu đề · Người tạo · Ngày · Số tiền · Nhóm · nút **"Duyệt"** = `route(approve_route, approve_params)` → mở thẳng phiếu (route `<luồng>.show`), `target=_blank` tuỳ chọn.
- **Map `doc_type` → route `.show`**: mỗi loại phiếu gắn sẵn tên route `.show` của luồng (suy từ prefix route trong `approveList`, vd `firmContract.index` → `firmContract.show`). Vài loại dùng chung 1 controller (HĐ nguyên tắc/dự án đều `firmContract.show`) → vẫn đúng vì cùng bảng.
- **Bộ lọc**: theo `doc_type` (loại phiếu — select2), `group_code` (nhóm), người tạo, khoảng ngày, tìm kiếm mã/tiêu đề. Dùng `initSearchColumn`/`mergeSearch`/`saveSearch` sẵn có.
- **Badge đếm** tổng số phiếu chờ (tái dùng số từ registry) hiển thị ở menu/notification.
- `home.blade.php` (widget đếm cũ) giữ nguyên hoặc trỏ dữ liệu từ registry ở phase sau — không bắt buộc phá.

## 9. Edge cases & lưu ý

- **Phiếu bị chỉnh sửa / rút lại**: luồng phải gọi `resolve(...canceled)` khi phiếu bị huỷ/soạn lại để dòng biến mất khỏi hộp.
- **Đổi phạm vi/nhân sự phê duyệt**: vì lọc theo quyền (không cache user), khi phân quyền đổi thì hộp tự đúng — không cần cập nhật registry (trừ `approver_id` đích danh).
- **Item KHÔNG phải phiếu duyệt** trong `approveList` (cảnh báo/nhắc: "Tài khoản chưa phân quyền", "Hàng mượn/giữ hết hạn", "Cảnh báo phân công NV", "Thông báo hoàn thiện hồ sơ", "Phiếu chờ giao việc"...) → **loại khỏi registry** (không phải approval); giữ ở widget cảnh báo riêng nếu cần.
- **Nhiều quyền duyệt cùng 1 cấp** (vd đề nghị thanh toán: TP / KT công nợ / KT trưởng / BGĐ ở các bước) → mô hình `current_level` + `required_permission`/`alt_permissions` theo từng bước; mỗi lần duyệt gọi `advance` sang bước kế.
- **`checkDueConfigsManager`**: middleware chặn duyệt vẫn nằm ở màn gốc — không cần tái hiện ở màn gộp (chỉ liệt kê).
- **Idempotent** tránh nhân đôi khi vừa backfill vừa có push mới.
- **Nhiều vòng duyệt (Gửi → Từ chối → Gửi lại)**: KHÔNG tạo dòng registry mới. `resolve(rejected)` đưa dòng về `rejected` (phiếu về người tạo, hết pending). Khi **gửi lại** → `push()` **tái kích hoạt CHÍNH dòng đó**: `status=pending`, `round++`, `level=1`, `level_started_at=now`, xóa `resolved_*`. Mỗi lượt duyệt/từ chối ở mỗi bước & mỗi vòng ghi 1 dòng `approval_inbox_logs` (kèm `round`). TG duyệt tính theo từng bước/vòng; khoảng giữa từ chối → gửi lại KHÔNG tính (phiếu ở người tạo). "Đang chờ" chỉ tính khi đang `pending`.

## 10b. Bảng log bước duyệt `approval_inbox_logs` (phục vụ báo cáo theo từng cấp)

Registry chỉ giữ trạng thái hiện tại; để báo cáo **TG duyệt theo từng cấp** + **ai duyệt/từ chối ở bước nào** cần 1 bảng log ghi mỗi lần chuyển bước:

| Cột | Ý nghĩa |
|---|---|
| `inbox_id` | FK → `approval_inbox.id` |
| `round` | Vòng gửi duyệt của bước (tinyint) |
| `level` | Cấp của bước (tinyint) |
| `required_permission` | Quyền cần ở bước đó |
| `actor_id` | **Người thực sự thao tác** (duyệt/từ chối) ở bước này (`resolved_by` của bước) |
| `action` | `approve` \| `reject` \| `cancel` |
| `started_at` | Thời điểm phiếu vào bước (= `level_started_at` khi bắt đầu bước) |
| `ended_at` | Thời điểm thao tác xong bước |
| `note` | Lý do (nếu có) |
| `created_at` | timestamp |

- Ghi 1 dòng mỗi lần `advance()` (kết thúc bước hiện tại, mở bước sau) và `resolve()` (kết thúc bước cuối).
- **TG duyệt của 1 người ở 1 phiếu** = `ended_at − started_at` của dòng có `actor_id` = người đó.
- Backfill: chỉ dựng được log cho phiếu còn dữ liệu mốc thời gian ở luồng gốc (một số luồng có sẵn `contract_approver_histories`... có thể map; luồng không có thì log bắt đầu từ khi bật tính năng).

## 11. Báo cáo phê duyệt (màn phụ)

Mục tiêu: nắm tình hình phê duyệt **theo thời gian** và **theo người duyệt**. Route riêng (vd `approvalInbox.report`). Mockup: `mockup-report.html`.

- **Bộ lọc**: Kỳ (Tháng/Quý/Năm/Tùy chọn) + Từ–Đến ngày · Công ty · Nhóm/Loại phiếu · Người duyệt · Kết quả · Xuất Excel.
- **KPI**: Tổng đã xử lý · Đã duyệt (tỉ lệ) · Từ chối · Đang chờ (TỔNG hệ thống) · **TG duyệt trung bình** · Quá hạn (>N ngày) · **Tỉ lệ đúng hạn** (design trước, làm sau — ngưỡng cấu hình, vd ≤24h).
- **Biểu đồ**: (1) phiếu duyệt/từ chối theo thời gian (ngày/tuần/tháng); (2) phân bố theo nhóm nghiệp vụ.
- **Bảng hiệu suất theo người duyệt**: Người duyệt (+phòng) · Cấp/Vai trò · Đã duyệt · Từ chối · Tỉ lệ duyệt · **TG duyệt TB (theo từng cấp)** · Phiếu lâu nhất (TG xử lý) · dòng Tổng cộng.
- **Khối "Chi tiết phiếu đã xử lý"** (drill-down cuối trang, có Xuất Excel): Loại phiếu · Mã (link `.show`) · Người yêu cầu · **Người duyệt** · Cấp · Ngày gửi · Ngày duyệt · TG duyệt · Kết quả · **Lý do từ chối**.
- **Lý do từ chối lấy ra báo cáo chung được**: lấy từ `approval_inbox_logs.note` (ghi khi `resolve(rejected, …, $reason)`). Với luồng có sẵn cột/bảng lý do riêng (`reason_of_approver`, `contract_approver_histories.note`…) → truyền chính giá trị đó vào `resolve()`. Hiển thị dưới badge "Từ chối" trong bảng chi tiết + cột riêng khi Xuất Excel; phiếu nhiều vòng thì mỗi vòng từ chối có lý do riêng theo `round`.
- **Quyết định đã chốt**:
  - **TG duyệt TB tính THEO TỪNG CẤP** (thời gian mỗi người giữ phiếu ở bước của họ = `ended_at − started_at` trong `approval_inbox_logs`), KHÔNG phải tổng thời gian toàn phiếu.
  - **KHÔNG có cột "đang chờ theo từng người"**: phiếu chờ lọc theo QUYỀN → nhiều người cùng có quyền duyệt 1 phiếu, không quy được về 1 người. "Đang chờ" chỉ là **KPI tổng** toàn hệ thống. Bảng theo người chỉ phản ánh **việc đã thực sự làm** (approve/reject) lấy từ `actor_id`.
  - **Không** làm chiều phân tích theo Phòng ban / theo Loại phiếu (chốt bỏ).
- Nguồn số liệu: `approval_inbox` (đang chờ/tổng) + `approval_inbox_logs` (đã duyệt/từ chối/thời gian theo cấp).
- **Đơn vị đếm (đã chốt): theo LƯỢT XỬ LÝ** (mỗi log = 1 lượt). Phiếu nhiều vòng (từ chối rồi duyệt lại) tính nhiều lượt: +1 "Từ chối" cho người duyệt vòng bị từ chối, +1 "Đã duyệt" cho người duyệt vòng sau. KHÔNG đếm theo phiếu distinct.

## 10. Lộ trình phase (tổng quan — chi tiết ở plan.md)

- **Phase 0** — Khảo sát + Thiết kế (đang làm). ✅
- **Phase 1** — Khung: migration `approval_inbox` + `ApprovalInboxService` + `ApprovalInboxController` + màn DataTable + backfill command. (chưa code)
- **Phase 2+** — Gắn từng nhóm luồng (mỗi nhóm: hook push/advance/resolve + backfill + verify). Thứ tự đề xuất theo mức dùng: Hợp đồng → Báo giá → Kế toán kho/Xuất nhập → Thu chi/Quyết toán → Đặt mua hàng → Bảo hành → Kế hoạch/Vận chuyển/Kiểm kê. (chưa code)
- **Phase cuối (sau gộp DB)** — HRM push vào cùng registry (`source_system='hrm'`). (ngoài phạm vi hiện tại)

---

## Cập nhật trạng thái — 2026-08-14 (sau Phase 3/4/5)

### Đã hoàn thành
- **Khung + màn** (Phase 1-2): registry `approval_inbox` + `approval_inbox_logs`; service `push()/advance()/resolve()` (config-driven qua `config/approval_inbox.php`); màn danh sách + màn báo cáo (mockup đã port).
- **Phase 3** — backfill-display 10 loại có data đầu tiên (firm_contract, project_quotation, product_export/import_request, settlement_contract, inland_buy_contract, bill_payment_request, bill_income, purchase_invoice, bill_payment).
- **Phase 4** — live hook 10 loại đầu (push khi gửi duyệt / advance khi chuyển cấp / resolve khi duyệt cuối-từ chối-huỷ; bọc try/catch, không phá luồng thật).
- **Phân trang** server-side (page-size 20/50/100/200, STT liên tục) — fix cắt 200 phiếu.
- **Siết scope quyền** — `config/approval_inbox.php` `permission_scopes` (16 quyền cấp phòng = department; còn lại company; cơ chế part sẵn). `pendingBuilderForUser` so `department_id`/`part_id` phiếu với phòng/bộ phận user **QUẢN LÝ** (`employee_manage_departments`/`employee_manage_parts`). Super Admin bypass=company. Giữ nhánh approver_id đích danh.
- **Thời gian gửi / KPI** — cột `submitted_at` DATETIME cố định (live hook = now() lúc push đầu; backfill = created_at nguồn; advance/re-push KHÔNG đổi). Cột màn "Thời gian gửi" (ngày-giờ) + filter dùng submitted_at. KPI: từng cấp = logs (level_started_at→ended_at); tổng = submitted_at→resolved_at.
- **Phase 5** — backfill-display 39 loại còn lại (9 batch theo nhóm, điều tra gate thật từng loại). **Tổng: 49 loại config, ~1344 phiếu registry** (màn Super Admin company 1: 49 loại / 21 nhóm / 934 phiếu).

### Còn lại
1. **Live hook cho 39 loại Phase 5** (như Phase 4) — hiện mới backfill-display; duyệt/từ chối ở màn gốc chưa tự cập nhật registry (chạy lại `approval-inbox:backfill` để đồng bộ, hoặc bật backfill định kỳ làm lưới an toàn).
2. **Gap push-condition luồng multi-level** — push chỉ khi phiếu ở status gốc; phiếu nộp thẳng cấp cao chưa push live (backfill vẫn bắt). Cân nhắc backfill định kỳ hoặc hardening.
3. **Nhóm B — 30 luồng pending=0** — thêm khi phát sinh data.
4. **Report KPI** dùng submitted_at→resolved_at + logs — để triển khai bên màn báo cáo.
5. **Concern scope đã ghi ledger**: gate thủ kho (pivot `warehouse_stockers`) → company over-inclusive; vài luồng company_id=null (hạch toán bổ sung type7, mua DV) do gate cross-company; bug có sẵn `dd($e)` trong `BillPaymentRequestController@update` (chưa sửa, cần xác nhận).

> Chi tiết per-loại (bảng/group/route/mapping status→quyền/concern) xem ledger `.superpowers/sdd/phieu-cho-duyet-tap-trung/progress.md` + các `task-*-report.md`. Khảo sát luồng: `missing-flows-survey.md`, `phase3-flow-data.md`. Scope quyền: `permission-scope-survey.md`.
