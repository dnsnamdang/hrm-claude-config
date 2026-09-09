# Kế hoạch — Port màn "Yêu cầu gia hạn hàng giữ" ERP → HRM

Thiết kế: [design.md](design.md) · Nhánh `feat/finance-prepick-extend-request` · @junfoke

Quy ước: mỗi Phase xong thì ghi Checkpoint (vừa xong / đang dở / bước tiếp / blocked / verify).
Đọc lại mục "Bẫy đã biết" ở cuối trước mỗi Phase.

---

## Phase 0 — Chuẩn bị ✅ (2026-08-22)

- [x] Tạo nhánh `feat/finance-prepick-extend-request` trên cả `hrm-api` và `hrm-client`
      (cắt từ `gop_db`, cả 2 repo lúc đó sạch — 0 file thay đổi).
- [x] Sao lưu 4 bảng → `bak_*_20260822`, số dòng khớp gốc. **Giữ tới khi user test xong.**
- [x] Ghi lại số liệu gốc (xem Checkpoint).
- [x] Không cần kéo dữ liệu: local đủ bảng gia hạn (khác màn ĐCHG — local thiếu bảng cha).
- [x] Đọc lại skill `erp-to-hrm-screen`.

**User chốt thêm 2026-08-22:** bản in giữ **khổ ngang**; đính kèm bám mẫu
`BillPaymentAttachmentService` (`CmcS3Helper`, thư mục S3 `prepick_extend_request`, ≤ 13 MB).

### Checkpoint — Phase 0

```text
Vừa hoàn thành: tạo 2 nhánh + sao lưu 4 bảng.
Đang làm dở: không.
Bước tiếp theo: Phase 1 — Entities + migration bảng lịch sử.
Blocked: không.
Verify (số dòng gốc = số dòng bản sao):
  prepick_extend_requests        1.421
  prepick_extend_request_details 31.437
  prepick_details                53.832
  prepick_logs                   110.744
Lệnh dọn khi test xong:
  DROP TABLE bak_prepick_extend_requests_20260822;
  DROP TABLE bak_prepick_extend_request_details_20260822;
  DROP TABLE bak_prepick_details_20260822;
  DROP TABLE bak_prepick_logs_20260822;
```

## Phase 1 — BE: Entities + migration lịch sử ✅ (2026-08-22)

- [x] `Entities/PrepickExtend/PrepickExtendRequest.php` — 5 hằng trạng thái + `STATUSES`
      (**"Đang tạo" = `draft` XÁM**, vá lỗi #8), `WRITABLE_STATUSES`, `SORTABLE_COLUMNS`,
      `searchByFilter()` / `applyAllScope()` / `applyViewScope()` / `orWhereApprovable()` /
      `applyWaitingApproveScope()` / `applyFilters()` / `applySort()`,
      `canEdit/canDelete/canView/canApprove/canBKSApprove/canTPApprove/canApproveAnyLevel`.
- [x] `PrepickExtendRequestDetail.php` — `prepick_detail()` + `baseQty()` (quy ĐV cơ bản).
- [x] `PrepickExtendRequestHistory.php` — **7 action** (3 action duyệt riêng cho 3 cấp, khác màn
      hủy chỉ có 1 "Duyệt": người đọc cần biết phiếu đã qua cấp nào).
- [x] Migration `2026_08_22_000001_create_prepick_extend_request_history_table.php` — **đã chạy**.
      Index đặt tên tay (`per_history_*`) tránh lỗi 1059 quá 64 ký tự.
- [x] Dùng lại `PrepickDetail` / `PrepickLog` ở `Entities/PrepickCancel/`, không tạo bản sao.

**Khác ERP thêm 2 điểm (đã ghi vào design §7):**
- `canView()` bổ sung 3 nhánh quyền XEM theo cấp — ERP chỉ cho người có quyền DUYỆT + người tạo,
  nên người được cấp quyền xem nhìn thấy phiếu ngoài danh sách mà bấm vào ra `not_found`.
- `applyViewScope()` nhánh "theo phòng ban" thêm `orWhere('created_by', mình)` — ERP chỉ
  `whereIn('department_id')` nên người đó **mất phiếu của chính mình** nếu phòng ban mình không
  nằm trong nhóm quản lý.
- Bỏ bộ lọc `warehouse` của ERP (bảng KHÔNG có cột `warehouse_id` — ô lọc chết).
- `product_name` / `product_code` / `contract` / `customer_id` đổi từ `pluck()->whereIn()` sang
  `whereHas()` — ERP kéo cả mảng id của 31.437 dòng chi tiết về PHP.

### Checkpoint — Phase 1

```text
Vừa hoàn thành: 3 entity + migration lịch sử (đã chạy migrate thành công).
Đang làm dở: không.
Bước tiếp theo: Phase 2 — PrepickStockService::moveToExpireDate() + PrepickExtendRequestService.
Blocked: không.
Verify: `php -l` 4 file sạch. Chạy thật trên dữ liệu local qua tinker:
  · PGHHG-01501 · status 4 -> statusMeta = {"name":"Chờ BGĐ duyệt","type":"warning"} · 115 dòng chi tiết
  · dòng 1: need_extend=1, extend_qty=1.00, baseQty=1, lô gốc 2026-07-28 -> hạn mới 2026-08-04
  · searchByFilter — DNS Admin (super): tổng 1.359 (= 1.421 − 62 nháp của người khác, đúng rule
    "nháp chỉ người tạo thấy"), Chờ KT 1, keyword `PGHHG-015` ra 2
  · searchByFilter — NV 285 (không super): tổng 29, Đang tạo 1 (nháp của chính họ), Chờ KT 0
```

## Phase 2 — BE: Service ✅ (2026-08-22)

- [x] **`PrepickStockService::moveToExpireDate()`** — chuyển lô: `lockForUpdate` dòng nguồn, kiểm
      đủ tồn, trừ nguồn + log âm, tìm/tạo dòng đích, cộng đích + log dương. Dòng đích set
      `company_id` theo dòng NGUỒN (vá lỗi #1). Hằng `ERP_PREPICK_EXTEND_DETAIL_TYPE` đã đối chiếu
      DB thật: khớp **59.734** dòng `prepick_logs`.
- [x] `PrepickExtendRequestService` — `searchByFilter`, `meta()`, `maxExpireDate()`,
      `dataToCreate()`, `normalizeLines()` + `buildLine()` + `syncProducts()`,
      `store()`, `update()`, `approve()` (3 cấp, 1 transaction), `applyExtendToStock()`,
      `reject()`, `destroy()`, `needBoardApprove()` (= `checkSwitchApprove` của ERP).
- [x] `PrepickExtendRequestHistoryService` — subset-diff, **khoá bảng con = `prepick_detail_id`**
      (KHÔNG phải `product_id` như màn hủy: cùng 1 hàng hoá có thể nằm ở nhiều lô / nhiều khách /
      nhiều hạn nên `product_id` sẽ gộp nhầm các dòng khác nhau). Đã nối vào store/update/approve/reject.
- [x] `detailData()` + `approvalRows()` cho màn Chi tiết.

**3 lỗi ERP nữa phát hiện khi port (bổ sung vào design §5):**

| # | Lỗi | Ghi chú |
|---:|---|---|
| 11 | `checkSwitchApprove()` đọc `invoiceable_type` namespace **`App\Model\Accounting\*`** | Dữ liệu thật là **`App\Model\IncomeExpenditure\*`** (BillAdjustDept 16.012 · BillIncomeReport 10.499 · BillIncome 7.326) → ERP tính tiền đã thu ra **0 với MỌI hợp đồng**, tức luôn dưới ngưỡng → luôn đẩy lên BGĐ |
| 12 | `products` KHÔNG có cột `base_price` — ERP dùng accessor `firstOrFail()` 2 tầng | Hàng thiếu bảng giá là **500 giữa lúc TP duyệt**. HRM đọc thẳng `product_units.is_base` → `product_unit_prices.price_type_id = 1`, thiếu thì coi như 0 |
| 13 | ⚠️ **ERP `checkSwitchApprove()` HỎNG TRÊN DB GỘP** | Nó gọi `$product->product->data` — accessor nạp cả quan hệ `files`. `gop_db.files` là schema HRM (`table`/`table_id`), ERP tìm `files.fileable_id` → SQL 1054. Đo thật: **33/40 phiếu lỗi**. Nghĩa là sau khi gộp DB, bước **TP duyệt bên cổng ERP đang 500** với hầu hết phiếu |

**Đối chiếu ERP ↔ HRM (`checkSwitchApprove` vs `needBoardApprove`)** — chạy cùng lúc trên `gop_db`,
40 phiếu đầu: HRM chạy được **40/40**, ERP chỉ **7/40** (33 phiếu lỗi #13). Trên 7 phiếu ERP tính
được thì **KHỚP 7/7**, gồm cả 1 ca `true` (PGHHG-00032).

⚠️ Đối chiếu với LỊCH SỬ (`board_of_manager_approver_id` có hay không) là **phép kiểm sai** — hàm
tính theo dữ liệu HIỆN TẠI (tiền đã thu tới hôm nay, ngưỡng % hiện tại, giá hiện tại) còn phiếu cũ
được quyết định theo dữ liệu tại thời điểm duyệt.

### Checkpoint — Phase 2

```text
Vừa hoàn thành: toàn bộ tầng service (tồn giữ, nghiệp vụ, lịch sử).
Đang làm dở: không.
Bước tiếp theo: Phase 3 — Controller + FormRequest + route + đính kèm.
Blocked: không.
Verify — chạy thật trên gop_db:
  · dataToCreate: NV 781 21 lô/7 query/7ms · NV 31 161 lô/7 query/51ms · NV 65 17 lô/6 query/9ms
    (số query CỐ ĐỊNH theo số lô -> hết N+1; ERP bắn 1-2 query mỗi lô)
  · needBoardApprove khớp ERP 7/7 trên tập ERP tính được (ERP lỗi 33/40, xem lỗi #13)
  · detailData PGHHG-00001: 2 dòng hàng, khối duyệt ra ĐỦ 3 cấp (TP/BGĐ/KT) dù CẢ 3 đều
    không nhập ghi chú -> chứng minh vá lỗi #3 (ERP đòi `&& comment` nên khối này RỖNG)
  · LUỒNG GHI TỒN (chạy trong transaction rồi rollback):
      lập PGHHG-01502 (status 3) -> ép status 2 -> approve()
      "Duyệt phiếu thành công", status -> 1, moved = 2 log
      lô cũ 13.00 -> 8.00 · lô mới qty 5.00, hạn 2026-09-13, company_id = 1 KHỚP nguồn (vá lỗi #1)
      prepick_logs +2 (1 âm 1 dương) · lịch sử phiếu 2 dòng: create + kt_approve
      sau rollback: phiếu 1.421 · lô 53.832 · logs 110.744 · lịch sử 0 -> DB nguyên vẹn
```

## Phase 3 — BE: Controller + route + quyền ✅ (2026-08-22)

- [x] `PrepickExtendRequestController` — `index`, `show`, `stock`, `histories`, `store`, `update`,
      `destroy`, `approve`, `reject`, `uploadFiles`. (In / Xuất Excel để Phase 8.)
- [x] `PrepickExtendRequestStoreRequest` + `PrepickExtendRequestRejectRequest` — messages tiếng Việt,
      `prepareForValidation()` decode `products` khi FE gửi multipart.
- [x] `PrepickExtendRequestListResource` — cột ERP + 2 cột cập nhật + 3 cờ `is_can_*`.
- [x] **10 route** trong `Modules/Finance/Routes/api.php`, prefix `finance/prepick-extend-requests`.
      `/stock` + `/upload-files` khai TRƯỚC `/{id}` để không bị route động nuốt.
- [x] Quyền đọc qua `ChecksEmployeePermission`, **không tạo permission mới**.
- [x] Đính kèm: `CmcS3Helper::putFiles(..., 'prepick_extend_request')`, **13 MB**, bộ mime ĐÚNG ERP
      (không nhận `zip` như màn Đề nghị thanh toán). ⚠️ Namespace là `App\Helper\CmcS3Helper`
      (thư mục `Helper` số ít), KHÔNG phải `App\Helpers`.
- [x] Chặn sửa/xoá phiếu không còn `canEdit()` bằng **423 LOCKED**.
- [x] `stock` chặn xem lô của người khác: chỉ cho khi đang thực sự sửa phiếu của họ
      (`request_id` phải trỏ phiếu do đúng người đó lập và mình xem được).

### Checkpoint — Phase 3

```text
Vừa hoàn thành: tầng HTTP đầy đủ (trừ In/Excel).
Đang làm dở: không.
Bước tiếp theo: Phase 4 — FE màn danh sách.
Blocked: không.
Verify — gọi API THẬT qua HTTP (JWT, http://127.0.0.1:8000):
  · GET /            -> total 1.359, meta đủ 4 cờ quyền + 5 statuses ("Đang tạo" = draft XÁM)
                        + max_expire_date 23/09/2026
  · GET /1501        -> "Chờ BGĐ duyệt", 115 dòng, khối duyệt 1 cấp, can_edit false, can_approve true
  · GET /stock       -> admin ra rỗng (đúng: không giữ lô nào sắp hết hạn) + max_expire_date
  · GET /1501/histories -> [] (phiếu cũ, HRM chưa ghi log)
  · POST /           -> tạo PGHHG-01503 "Yêu cầu của bạn đã được lưu..."
  · DELETE /1503     -> "Xóa thành công", tổng phiếu về đúng 1.421
  · PUT /1 (đã duyệt)    -> HTTP 423 + câu báo rõ
  · DELETE /1 (đã duyệt) -> HTTP 423 + câu báo rõ
  · POST /1/approve  -> HTTP 422 {"status":["Phiếu không ở trạng thái chờ duyệt."]}
⚠️ `php artisan route:list` KHÔNG chạy được trên repo này (lỗi có sẵn ở
   RequestUpdateTimeSheetController gọi helper quyền lúc build danh sách route, không liên quan
   feature này) — kiểm route bằng `app('router')->getRoutes()`.
```

## Phase 4 — FE: màn danh sách ✅ (2026-08-22)

- [x] `pages/finance/prepick-extend-requests/index.vue` — 4 mixin
      (`PageTitleMixin`, `filterStateMixin`, `DedupeLoadMixin`, `columnCustomizationMixin`),
      `localStorageKey` / `columnScreenKey` = `finance_prepick_extend_requests`.
- [x] `V2BaseSmartFilterPanel` + `filterFields` 6 ô (Mã phiếu, Người lập, Trạng thái, Người duyệt,
      Tên hàng hóa, Mã hàng hóa) + khoảng ngày + khối Công ty/Phòng ban.
      ⚠️ `initialStateForm` phải khai đủ `company_id` / `department_id` / `part_id` / `employee_id`.
- [x] Cột: STT · Mã phiếu (`nuxt-link`) · Người lập · Ngày lập · Trạng thái (`V2BaseBadge` +
      `statusBadgeVariant`) · Người duyệt · Ngày duyệt · Hành động. Sort mặc định giảm dần ngày tạo.
- [x] Hành động: Sửa · Xóa · Duyệt · Từ chối · In · Lịch sử — hiện/ẩn theo **cờ BE**
      (`is_can_edit` / `is_can_delete` / `is_can_approve`), nút không dùng được thì **ẩn hẳn**.
      ⚠️ `V2BaseRowActions` emit **CHUỖI key** → `switch (action)`.
- [x] Toolbar: Thêm mới → Xuất Excel → Cấu hình cột (bộ dựng file Excel để Phase 8).
- [x] `RejectModal.vue` — chữ **"Từ chối"** (không phải "Không duyệt", theo button-convention),
      bắt buộc nhập lý do, `:interactable` chứ không `disabled`.
- [x] Gắn link menu `components/subsystem-menu/finance.js` (mục trước đó không có link).

### Checkpoint — Phase 4

```text
Vừa hoàn thành: màn danh sách + popup Từ chối + link menu.
Đang làm dở: không.
Bước tiếp theo: Phase 5 — FE form Thêm / Sửa.
Blocked: không.
Verify — BẤM THẬT trên trình duyệt (127.0.0.1:3000), 0 lỗi console:
  · Bảng: 10 cột đúng thứ tự, 10 dòng/trang, mã phiếu là <nuxt-link> /finance/prepick-extend-requests/1501
  · Badge "Chờ BGĐ duyệt" nền rgb(254,249,195) — đúng nhóm warning
  · Cột Hành động dòng "Chờ BGĐ duyệt" hiện ĐÚNG 3 nút: Duyệt (link sang chi tiết) · Từ chối · Lịch sử
    (Sửa/Xóa ẩn vì is_can_edit/is_can_delete = false) -> bấm THẬT: Lịch sử mở modal,
    Từ chối mở popup nhập lý do => KHÔNG dính bẫy `action.key`
  · Bộ lọc bấm thật từng ô, khớp API 100%:
      không lọc 1.359 · status 4 -> 2 · status 1 -> 1.356 · status 5 -> 0
      Người tạo 30 -> 27 · Tên hàng "máy nén" -> 242 · Mã hàng "HK-W" -> 89
      Làm mới -> về 1.359
```

⚠️ **Bài học khi test bộ lọc bằng Playwright**: chờ 2s sau mỗi lần đổi ô lọc là KHÔNG ĐỦ trên dev
(API ~1,2s+ baseline). Số đọc được sẽ **lệch đúng một nhịp** — nhìn y hệt "ô lọc không ăn". Đã suýt
báo nhầm thành bug; chờ **3s** thì mọi ô đều đúng. Đo lại trước khi kết luận.

### Việc phát sinh, để Phase 6 xử lý

- [x] ⚠️ ERP cho kế toán **sửa lại "Hạn giữ mới" ngay lúc duyệt** (`approve()` nhận `products` rồi
      gọi `syncProducts()` trước khi ghi tồn). `PrepickExtendRequestService::approve()` hiện CHƯA
      nhận `products` — mới áp đúng số đã lưu. Vì vậy nút "Duyệt" ở danh sách để `to:` sang màn chi
      tiết (giống ERP) chứ không gọi API thẳng. Bổ sung khi làm màn chi tiết.

## Phase 5 — FE: form Thêm / Sửa ✅ (2026-08-22)

- [x] `create.vue` · `_id/edit.vue` · `components/PrepickExtendRequestForm.vue` dùng chung.
- [~] Bảng chi tiết theo §2.3 design; ô ĐVT **khóa + icon ⓘ** giải thích — mới làm **12/13 cột**.
      ❌ **THIẾU cột "Có thể giữ"** (ERP `product.in_stock`) ở CẢ form lẫn màn chi tiết. Đây KHÔNG
      phải cột "Đang giữ": `in_stock` là **tồn kho khả dụng của hàng hoá**, ERP tính
      `max(0, round((in_stock − in_promotion_stock) / unit_coefficient))` lấy từ 1 API tồn kho
      riêng (`show.blade.php:302`). Xem mục "Việc còn thiếu" cuối Phase 5.
- [x] Checkbox "Cần gia hạn" dùng `V2BaseCheckbox` (prop `label`, **không** truyền slot).
- [x] Ô "Cần gia hạn (SL)" và "Hạn giữ mới": vượt khoảng thì **báo đỏ dưới ô**, TUYỆT ĐỐI không tự
      kéo giá trị về trần; còn lỗi thì **không gọi API**.
- [x] Trần "Hạn giữ mới" = hôm nay + `configs.max_prepick_date`; nhỏ nhất = ngày mai (`after:today`).
- [x] 2 nút lưu: **Lưu nháp** (status 3) + **Gửi duyệt** (status 5) — dựng ở `#custom-actions`.
- [x] `unsavedChangesMixin` + `markFormSaved()`; upload đính kèm + gỡ file.
- [x] Bảng rỗng ở màn Thêm nói RÕ lý do + mốc ngày "sắp hết hạn" (BE trả `warning_date`).
- [x] Màn Sửa vào bằng URL khi phiếu không sửa được -> đá về Chi tiết.

**2 lỗi tự phát hiện khi bấm thật, đã sửa:**

| # | Lỗi | Cách sửa |
|---:|---|---|
| 1 | Lưu ở màn **Sửa** ném **500 `Column 'model_id' cannot be null`** | `detailData()` không trả `model_id`, mà `buildLine()` lại lấy snapshot TỪ PAYLOAD FE. Sửa gốc: thêm `productSnapshots()` — **BE tự dựng snapshot** (tên/mã/model/ĐV cơ bản) từ `products`, KHÔNG tin payload. 5 cột đó đều NOT NULL nên FE quên 1 cột là vỡ câu insert |
| 2 | Lỗi "Chưa tích chọn hàng hóa nào" không tự mất khi user vừa tick | `onNeedExtendChange()` xoá lỗi `products` ngay khi có ≥ 1 dòng được tick, không đợi tới lúc bấm Lưu |

**Gộp bớt request**: `detailData()` trả kèm `max_expire_date` + `warning_date` nên màn Sửa KHÔNG
phải gọi thêm `/stock` chỉ để lấy 2 con số cấu hình.

### ❗ Việc còn thiếu — phát hiện khi user soát plan (2026-08-22)

- [x] **Bổ sung cột "Có thể giữ" (`in_stock`)** — XONG 2026-08-22 theo **phương án A** (user chốt).
      Bảng chi tiết nay đủ **13/13 cột**.
      ERP có 2 cột số lượng cạnh nhau và chúng KHÁC nhau:
      · **Có thể giữ** = tồn kho khả dụng của hàng hoá (kho còn bao nhiêu để giữ tiếp)
      · **Đang giữ** = số đang giữ trên chính lô đó (`prepick_details.qty`) — cột HRM đang có
**Kết quả khảo sát:**

| Nơi | Tình trạng |
|---|---|
| ERP lấy `in_stock` từ đâu | `show.blade.php:283` POST `warehouseInfo.stockOfProducts` → `ProductStockService::getStockQty()` → **`Product::getAccountingStockDetail()`** (app/Product.php:2358-2619). Màn này KHÔNG gửi kho nào cả → `accounting_warehouse_ids` rỗng → ERP fallback "mọi kho kế toán của công ty". FE quy đổi `max(0, round((in_stock − in_promotion_stock) / unit_coefficient))` |
| HRM đã có chưa | **CÓ RỒI** — `ProductTransferRequestService::accountingStockDetail()` (dòng 1011) là bản port RÚT GỌN của đúng hàm ERP đó, trả `in_warehouse` / `in_stock` / `prepick_qty` / `hold_qty`, và có sẵn nhánh fallback khi `accWarehouseIds` rỗng |
| Dùng lại thẳng được không | **KHÔNG.** Hàm đó `private`; còn `stockOfProducts()` (public) thì **bắt buộc `stock_query`** (phải chọn kho/nhóm kho) — màn gia hạn không có ô chọn kho nên không truyền được |

⇒ Muốn dùng lại phải **tách `accountingStockDetail()` ra chỗ dùng chung**. Đó là đụng vào service
của màn Phiếu điều chuyển hàng ĐANG CHẠY → theo CLAUDE.md phải **hỏi ý kiến trước**, nên dừng ở đây.

**2 phương án, chờ user chốt:**

| | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **A** ✅ user chốt | Tách `accountingStockDetail()` sang service tồn kho dùng chung, 2 màn cùng gọi | 1 nguồn sự thật, sau này sửa 1 chỗ | Đụng file màn Chuyển hàng đang chạy → phải test lại màn đó |
| **B** | Viết bản riêng trong `PrepickExtendRequestService` | Không đụng màn nào khác | **Nhân bản ~140 dòng** logic tồn kho, 2 bản chắc chắn lệch nhau theo thời gian |

**Đã làm theo A:**

- [x] Tạo `Modules/Finance/Services/AccountingStockService.php` — chuyển nguyên 170 dòng
      `accountingStockDetail()` ra, đổi `private` → `public function detail()`. Docblock ghi rõ
      "Nơi đang dùng" + phân biệt với `PrepickStockService` (tồn KHO vs tồn HÀNG GIỮ).
- [x] `ProductTransferRequestService` bỏ bản private, nhận service mới qua constructor injection.
      **Đã test lại màn Chuyển hàng**: `GET /product-transfer-requests/stock` vẫn trả đúng
      `in_warehouse 258 · in_stock 258 · prepick_qty 0 · hold_qty 0`.
- [x] `PrepickExtendRequestService::inStockOfProducts()` + endpoint `GET /in-stock`
      (tổng route màn gia hạn: **14**). **Dedupe `product_id`** trước khi tính — 1 hàng hoá nằm ở
      nhiều lô thì ERP tính lại từng lô, HRM tính 1 lần rồi map ra mọi lô.
- [x] FE: thêm cột "Có thể giữ" + icon ⓘ phân biệt với "Đang giữ"; nạp **SAU** khi bảng đã hiện
      (đúng cách ERP làm ở `show.blade.php:283`) nên bảng không phải chờ phép tính tồn kho.
      Lỗi khi nạp thì im lặng để 0, KHÔNG toast — số phụ trợ, hỏng không cản việc lập phiếu.
- [x] Ghi nguyên tắc "hàm nghiệp vụ dùng chung phải tách ra" vào skill `erp-to-hrm-screen`
      (**Bước 3b** mới + 1 dòng trong bảng "Bẫy hay dính") — user yêu cầu 2026-08-22.

**Verify (bấm thật, 0 lỗi console):** màn Thêm của NV 781 ra đủ **13 cột** đúng thứ tự ERP
(… ĐVT · **Có thể giữ** · Đang giữ · Cần gia hạn …), 21 dòng, **11/21 dòng có tồn kho > 0**.
Dòng 1: Có thể giữ = 0 · Đang giữ = 13 → 2 cột đúng là 2 con số khác nhau.

### Checkpoint — Phase 5

```text
Vừa hoàn thành: form Thêm/Sửa + create.vue + _id/edit.vue.
Đang làm dở: không.
Bước tiếp theo: Phase 6 — màn Chi tiết + duyệt 3 cấp (kèm việc còn nợ: approve nhận `products`).
Blocked: không.
Verify — BẤM THẬT trên trình duyệt bằng tài khoản NV 781 (có 21 lô sắp hết hạn), 0 lỗi console:
  · Màn Thêm với tài khoản KHÔNG có lô: bảng rỗng + câu giải thích đúng mốc 31/08/2026
    (= hôm nay + configs.warning_day = 7 ngày)
  · Màn Thêm với NV 781: 12 cột đúng thứ tự, 21 dòng, checkbox V2BaseCheckbox render được
  · Bấm "Gửi duyệt" khi chưa tick dòng nào -> chặn, KHÔNG popup, lỗi "Chưa tích chọn hàng hóa nào"
  · Tick dòng 1 (đang giữ 13) rồi gõ SL = 99 -> ô VẪN GIỮ 99, viền rgb(220,53,69),
    lỗi "Cần gia hạn – Không được vượt số đang giữ (13)"  => KHÔNG tự kéo về trần
  · Bỏ trống Hạn giữ mới -> "Hạn giữ mới – Bắt buộc nhập"
  · Sửa SL = 2 + hạn = 23/09/2026 rồi Lưu nháp -> tạo PGHHG-01504, ĐIỀU HƯỚNG VỀ DANH SÁCH
    DB: 21 dòng (giữ cả dòng không tick như ERP), 1 dòng tick SL 2, hạn 2026-09-23, lịch sử `create`
  · Màn Sửa PGHHG-01504: tiêu đề kèm mã, nạp đúng ghi chú/trạng thái/phòng ban, 21 dòng, 1 dòng tick
  · Sửa SL -> 7 rồi lưu: HTTP 200, DB ghi model_id 14300 · unit_id 39 · code JONN-C-7DW7G100V,
    lịch sử `create, update`
  · Dọn sạch: xoá phiếu test -> DB về đúng 1.421 phiếu / 31.437 chi tiết / tồn + logs KHÔNG đổi
```

✅ **User chốt 2026-08-22**: xoá phiếu thì **GIỮ LẠI lịch sử** ("lỡ sau cần check"). Vậy hành vi
hiện tại là ĐÚNG Ý, không phải thiếu sót — `destroy()` chỉ xoá phiếu + dòng chi tiết, bảng
`prepick_extend_request_history` giữ nguyên. Khớp luôn với `PrepickCancelRequestService::destroy()`.

## Phase 6 — FE: chi tiết + duyệt 3 cấp ✅ (2026-08-22)

- [x] `_id/index.vue` — tiêu đề `Chi tiết yêu cầu gia hạn hàng giữ: <mã>`, **Mã phiếu là ô đầu tiên**.
- [x] Khối duyệt: nút **Duyệt** / **Từ chối** hiện theo cờ BE của đúng cấp đang chờ.
      ⚠️ Dựng ở `#custom-actions`, KHÔNG bật `menu.approve` — `V2Footer` tự chèn popup xác nhận
      chung chung làm validate chạy sau popup (đã đo 22/08/2026).
- [x] Popup Từ chối bắt buộc nhập lý do (mẫu `RejectModal.vue` của màn hủy).
- [x] Khối "Lịch sử duyệt" 3 cấp TP / BGĐ / KT — hiện dòng **chỉ cần có `*_approver_id`**,
      KHÔNG đòi có ghi chú (vá lỗi #3); KT lấy đúng cột `approver_comment` (vá lỗi #4).
- [x] Thao tác xong (Lưu / Duyệt / Từ chối) đều `$router.push` **về danh sách**.
- [x] **BE: `approve()` nay nhận `products`** — người duyệt (MỌI cấp) được tick/bỏ tick dòng và sửa
      "Hạn giữ mới" ngay tại màn duyệt, đúng ERP (`show.blade.php:144` + `approve()` gọi
      `syncProducts()` trước khi ghi tồn). **KHÔNG cho sửa số lượng** — ERP để ô SL chỉ đọc ở màn
      duyệt. Thêm `applyApproverEdits()` validate hạn mới + chặn bỏ tick hết ("phải giữ lại ít nhất
      1 hàng hoá thì mới duyệt được"). Việc còn nợ từ Phase 4 -> ĐÃ XONG.
- [x] Nhãn nút duyệt theo ĐÚNG cấp: **TP duyệt / BGĐ duyệt / KT duyệt** (ERP cũng ghi vậy).
- [x] Khối **Lịch sử thay đổi** (`PrepickHistoryPanel`) mặc định ẩn — gộp luôn Phase 7.

### Checkpoint — Phase 6

```text
Vừa hoàn thành: màn Chi tiết + duyệt 3 cấp + từ chối + 2 khối lịch sử. Phase 7 coi như xong theo.
Đang làm dở: không.
Bước tiếp theo: Phase 8 — In (khổ ngang) + Xuất Excel.
Blocked: không.
Verify — BẤM THẬT trên trình duyệt, 0 lỗi console:
  · Chi tiết PGHHG-01505 (Chờ KT duyệt), tài khoản có quyền duyệt:
      tiêu đề kèm mã · nút [KT duyệt rgb(26,188,156) teal] [Từ chối rgb(220,38,38) đỏ] [Quay lại]
      nhãn nút khớp đúng cấp đang chờ
  · Bấm KT duyệt -> popup DUY NHẤT, câu nêu rõ hậu quả:
      "Duyệt bước Kế toán sẽ CHUYỂN LÔ HÀNG GIỮ sang hạn mới ngay lập tức và không thể hoàn tác."
  · Xác nhận -> điều hướng VỀ DANH SÁCH. Đo DB:
      lô cũ 53798: 13.00 -> 10.00
      lô mới 53834: qty 3.00 · hạn 2026-09-23 · company_id 1 KHỚP nguồn (vá lỗi #1)
                    objectable_type = App\Model\Warehouse\PrepickExtendRequestDetail (đúng chuỗi ERP)
      prepick_logs +2: (53798: 13 -> -3 -> 10) và (53834: 0 -> +3 -> 3)
      phiếu: status 1 · approver_id 13 · approved_time
      lịch sử: create (781) + kt_approve (13)
  · HOÀN NGUYÊN xong: đối chiếu với bản sao bak_*_20260822 -> logs 110.744 = bản sao,
    lô lệch qty = 0, phiếu 1.421, lịch sử 0
```

## Phase 7 — Lịch sử thay đổi ✅ (2026-08-22, làm gộp trong Phase 4 + 6)

- [x] `PrepickHistoryModal.vue` ở màn danh sách (Phase 4) + `PrepickHistoryPanel.vue` ở màn chi
      tiết, mặc định ẩn (Phase 6). Cả 2 dùng chung component của nhóm Giữ hàng nên sắp mới → cũ,
      đủ 3 bộ lọc, dropdown người thực hiện `Mã phòng – Tên NV` là có sẵn.
- [x] Khối **Lịch sử duyệt** (3 bộ cột TP/BGĐ/KT trên chính bản ghi) — hiện dòng chỉ cần có
      `*_approver_id`, KHÔNG đòi ghi chú (vá lỗi #3).

## Phase 8 — In + Xuất Excel ✅ (2026-08-22)

- [x] `_id/print.vue` + `print-list.vue` theo mục 0 của skill `print-page`
      (`layout: 'print'`, nút In canh phải, khung A4). **Khổ ngang** — user đã chốt 2026-08-22.
- [x] Mẫu in dựng trong `Modules/Finance/Resources/views/prints/`, KHÔNG ghi `report_templates`.
- [x] `components/export-excel.js` dựng file bằng ExcelJS; BE trả đủ trường cho popup chọn trường.
- [x] BE: `renderPrint()` · `renderPrintList()` · `exportData()` + 3 endpoint
      (`/{id}/print-data`, `/print-list-data`, `/export`) → tổng **13 route**.
- [x] 2 mẫu blade trong `Modules/Finance/Resources/views/prints/`, KHÔNG ghi `report_templates`.
- [x] Nút In: cột Hành động ở danh sách · toolbar (in cả danh sách) · footer màn Chi tiết
      (nút trắng `secondary` — In là action phụ).

⚠️ **Không eager load `prepick_detail.customer`**: `PrepickDetail` là model DÙNG CHUNG của nhóm Giữ
hàng và KHÔNG khai quan hệ `customer` → `RelationNotFoundException`. Sửa model dùng chung phải hỏi
ý kiến trước (CLAUDE.md) nên `renderPrint()` tự tra khách hàng bằng 1 truy vấn gộp.

### Checkpoint — Phase 8

```text
Vừa hoàn thành: In 1 phiếu + In danh sách + Xuất Excel (BE render, FE hiển thị/dựng file).
Đang làm dở: không.
Bước tiếp theo: Phase 9 — checklist tổng + user test tay + bàn giao.
Blocked: không.
Verify — BẤM THẬT trên trình duyệt:
  · /1501/print: tiêu đề "PHIẾU YÊU CẦU GIA HẠN HÀNG GIỮ" + Số phiếu · 4 bảng ·
    bảng chi tiết đủ 10 cột · bảng "Lịch sử duyệt" in kèm · khối ký 4 người
    Khổ NGANG: tờ giấy rộng 1007px (~297mm) · nền xám rgb(238,238,238) chuẩn chung
    Nút In canh ĐÚNG mép phải giấy (cùng toạ độ x = 1019)
  · /print-list?status=4: "DANH SÁCH PHIẾU YÊU CẦU GIA HẠN HÀNG GIỮ", "Tổng số phiếu: 2"
    khớp bộ lọc · 7 cột · khổ ngang
  · Xuất Excel với 3 trường user tick (Mã phiếu / Người tạo / Trạng thái):
    tải về THẬT `danh_sach_yeu_cau_gia_han_hang_giu.xlsx` (7.101 bytes), 0 lỗi.
    Đọc `sharedStrings.xml`: tiêu đề + STT + đúng 3 cột đã tick + 2 dòng dữ liệu
    (PGHHG-01501 / PGHHG-01500) -> thứ tự cột theo đúng thứ tự tick
  · Popup chọn trường có đủ 11 trường
```

⚠️ **Cột Khách hàng trên bản in RỖNG** — KHÔNG phải lỗi code: `prepick_details.customer_id` của
các lô (948, 7835, 5570, 946…) **không tồn tại trong bảng `customers`** trên DB gộp. Đúng lỗi dữ
liệu đã biết (`customers` thiếu dải id ERP, NCC/KH rỗng ~87%). Đã kiểm bằng SQL đối chiếu.

## Phase 9 — Menu + checklist + verify + bàn giao ✅ (user test tay 2026-08-24: "tạm ổn")

- [x] Gắn link cho mục "Yêu cầu gia hạn hàng giữ" trong `components/subsystem-menu/finance.js`
      (làm ở Phase 4).
- [x] **6 lệnh grep tự kiểm của skill chạy SẠCH** trên cả thư mục feature:
      `status-pill|statusPillClass` · `interactable:|disabledTitle` · `action.key ===` ·
      `V2BaseFilterPanel` · `advanced-filters` — không có kết quả nào.
      2 kết quả còn lại đều là **cố ý, khớp màn đã port**: câu toast `Xuất Excel thành công`
      (bảng QLDA không có mã cho việc xuất file) và `<button class="close">` — nút × của
      `b-modal`, copy y hệt `RejectModal` màn Yêu cầu hủy hàng giữ.
- [~] 6 lệnh grep tự kiểm: **ĐÃ chạy, sạch**. Checklist A→H của skill: **chưa rà đủ từng mục**.
- [~] **Bấm thật bằng Playwright**: đã chạy danh sách / form / chi tiết / in / xuất Excel và luồng KT duyệt (đo tồn rồi hoàn nguyên). **CHƯA test 2 cấp TP và BGĐ** — cần tài khoản có quyền tương ứng. Chi tiết:
      luồng Lưu nháp → Gửi duyệt → TP duyệt → (BGĐ) → KT duyệt, đối chiếu `prepick_details` +
      `prepick_logs` trước/sau bằng SQL.
- [~] Đối chiếu ngược §2 design: mới soát phần **bảng chi tiết** (chính nhờ đó phát hiện thiếu cột
      "Có thể giữ"). Còn phải soát nốt cột màn danh sách + bộ lọc + điều kiện ẩn/hiện từng nút.
- [x] Cập nhật `.plans/gop-db/STATUS.md`.

---

## Phase 10 — Vá QA redmine 11276 / 11277 / 11278 / 11296 (2026-09-04)

- [x] **11276** — cột "Cần gia hạn" mặc định = số **ĐANG GIỮ**, không để 0/trống. Gốc: ERP làm
      việc này trong class JS `PrepickExtendRequestDetail`
      (`if (!this._extend_qty) this._extend_qty = this.qty / this.unit_coefficient`) nên nhìn vào
      DB thấy 0 mà màn ERP vẫn hiện số. Áp ở cả `mapLot()` (màn Thêm) lẫn `loadDetail()` (Chi tiết
      / Duyệt). Payload không đổi: dòng chưa tích vẫn gửi `extend_qty = 0`.
- [x] **11277** — lịch chọn "Hạn giữ mới" bị **mất cột Chủ nhật**. Gốc ở component dùng chung
      `V2BaseDatePicker`: `onOpen()` ghim `left` theo ô input mà không kẹp mép phải màn hình, nên
      ô ở cột sát phải làm popup tràn khỏi viewport. Đã kẹp `left` trong
      `[8px, innerWidth - popupWidth - 8px]`.
- [x] **11278** (phần ghi chú trong ảnh) — màn Chi tiết thiếu nút **Sửa / Xóa** cho phiếu nháp
      trong khi màn Điều chuyển hàng giữ cùng nhóm đã có. Bổ sung 2 nút, gate bằng cờ BE
      `is_can_edit` / `is_can_delete` (BE đã trả sẵn), thao tác xong quay về danh sách.
- [x] **11296** — 404 báo "Không tìm thấy dữ liệu" + trả về danh sách (xem plan màn Hủy hàng giữ).
- [x] **11278** (phần "giá trị vượt ngưỡng") — **KHÔNG PHẢI LỖI, tester báo nhầm**. Đã đối chiếu
      code ERP (xem Checkpoint): ERP không chặn tạo phiếu vượt ngưỡng, và ERP cũng KHÔNG cho
      TP/BGĐ/KT sửa số lượng lúc duyệt. HRM đang khớp. Không sửa gì.

### Checkpoint — Phase 10

```text
Vừa hoàn thành: 11276, 11277, phần nút Sửa/Xóa của 11278, 11296.
Đang làm dở: không.
Bước tiếp theo: user phản hồi lại tester về 11278 (báo nhầm).
Blocked: không.
Verify: compile các file .vue đã sửa.

KẾT LUẬN 11278 — ĐỐI CHIẾU CODE ERP, KHÔNG PHẢI LỖI:
1. "Không tạo được giá trị vượt ngưỡng": ERP `PrepickExtendRequestController::store()` chỉ validate
   `extend_qty` numeric/min:0/max:999999 + `validateProducts()` (qty <= số đang giữ của LÔ) +
   hạn không quá `max_prepick_date`. KHÔNG có ràng buộc nào theo GIÁ TRỊ TIỀN. HRM giống hệt
   (`PrepickExtendRequestService`: qty <= `lot->qty`). Ngưỡng tiền chỉ dùng để RẼ NHÁNH DUYỆT.
   Chạy thật `needBoardApproveByLines()` trên `gop_db`: công ty 1 (ngưỡng 20tr) — 1 x hàng
   1.882.223đ -> không cần BGĐ; 1 x hàng 25.000.000đ -> CẦN BGĐ. Công ty 4 (ngưỡng 5tr), 1 x
   7.500.000đ -> CẦN BGĐ. `basePrice()` đọc thẳng `product_units` + `product_unit_prices` nên
   không dính lỗi accessor `Product->data` của ERP trên DB gộp.
   => Tester không dựng được data đủ tiền (lô của tài khoản test toàn hàng giá 1đ), không phải HRM chặn.
2. "TP/BGĐ/KT duyệt không sửa được giá trị vượt ngưỡng": ERP `prepick_extend_requests/show.blade.php`
   render số lượng bằng `<td><% product.extend_qty %></td>` — CHỮ, không phải input; chỉ
   `new_expire_date` và checkbox `need_extend` sửa được. Màn Điều chuyển (`prepick_transfer2/
   show.blade.php`) còn chặt hơn: `<td><% product.qty %></td>` và checkbox đã bị comment.
   HRM cũng chỉ cho sửa "Hạn giữ mới" -> KHỚP ERP.
```

---

## Bẫy đã biết — đọc lại trước mỗi phase

| Bẫy | Cách tránh |
|---|---|
| Trạng thái đánh số ngược (3 = Đang tạo, 5 = Chờ TP) | Giữ nguyên số ERP; **"Đang tạo" phải XÁM**, ERP đang tô đỏ |
| `prepick_details` không có `unit_id` | Luôn quy đổi `qty × unit_coefficient`; ô ĐVT khóa |
| Dòng `prepick_details` mới thiếu `company_id` | Set theo company của dòng NGUỒN, đừng để hook lấp bằng công ty người duyệt |
| `V2Footer` tự chèn popup cho `menu.approve` / `menu.print` | Dựng nút ở `#custom-actions` |
| `V2BaseRowActions` emit chuỗi key | `switch (action)`, đừng so `action.key` |
| `V2BaseButton` không có prop `disabled` | Ẩn bằng `v-if` / `visible` |
| `V2BaseCheckbox` truyền slot | Chỉ dùng prop `label`, nếu không render khối rỗng |
| `is-invalid` nằm ở `.v2-input__wrapper`, không ở `input` | Selector cuộn-về-ô-lỗi phải bắt wrapper |
| `$request->get()` không đọc JSON body | Dùng `input()` |
| `ApiController` không có `$this->validate()` | Dùng FormRequest |
| Toast tự chế câu mới | Lấy nguyên văn bảng QLDA |
| Ô khóa nhìn như ô trống | Kèm icon ⓘ + tooltip nói rõ vì sao khóa |
| Nút "Làm mới" không nạp lại danh sách | `handleReset` phải tự gọi `loadData()` |
