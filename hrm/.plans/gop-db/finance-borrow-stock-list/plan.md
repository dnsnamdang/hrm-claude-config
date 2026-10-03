# Danh sách hàng mượn + Hàng sắp hết hạn mượn — plan

Thiết kế: [`./design.md`](./design.md) · Nhánh dự kiến: `feat/finance-borrow-stock-list`

---

## Phase 0 — Khảo sát & chốt hướng ✅ (2026-09-23)

- [x] Tìm màn ERP: `warehouseInfo.borrowIndex` + `warehouseInfo.expiringBorrow`
- [x] Đọc blade `warehouse/warehouses/borrowIndex.blade.php` — 13 cột 2 tầng, 8 ô lọc, 3 trạng thái
- [x] Đọc `WarehouseInfosController::borrowSearchData()` — 1 truy vấn phục vụ 4 màn qua `?type=`
- [x] Đối chiếu `expiringBorrow` với `borrowIndex` — cùng cột, bỏ 2 ô lọc, thêm bó ngày + `created_by`
- [x] Tra vị trí menu ERP: đúng 2 chỗ (`topmenubar:852-853` và `:1056-1057`)
- [x] Xác nhận HRM **đã có sẵn 2 nhãn menu chờ** ở đúng 2 chỗ đó
- [x] Xác nhận **không cần tạo quyền mới** — 3 quyền `Xem phiếu hàng mượn theo …` đã có
      (`web` 100890-892 / `api` 1565-1567), 3 màn hàng mượn khác đang dùng
- [x] Xác nhận tiền lệ: cặp màn hàng giữ (`prepick-stocks` + `prepick-expiring`) đã port xong
- [x] Chốt với user: siết quyền theo cấp · dòng mở rộng ▸ · làm 2 màn, bỏ 2 biến thể Kế toán kho

## Phase 1 — BE truy vấn ✅ (2026-09-23)

- [x] `BorrowStockReportService` — khung + docblock (ghi rõ khác `BorrowStockService` thế nào)
- [x] `baseQuery()`: `product_export_requests` + join kho, lọc `XUAT_MUON` / `DA_MUON` / còn nợ
- [x] `applyViewScope()` — 4 nhánh quyền, fail-closed, khớp 1-1 `BorrowExportRequest::applyViewScope()`
- [x] `applyFilters()` — 8 ô lọc, đổi 4 chỗ `pluck+whereIn` của ERP sang `whereExists` (#5)
- [x] `applyExpiringWindow()` — dùng lại `PrepickConfigService::warningDay()`
- [x] Trạng thái hạn mượn tính bằng `CASE` + `CURDATE()`; bộ lọc Trạng thái so bằng CHÍNH biểu
      thức đó nên màn và bộ lọc không thể lệch
- [x] Sắp xếp giảm dần theo ngày tạo (khác ERP — đã ghi vào bảng "sửa có chủ ý")
- [x] `search()` — bảng 2 tầng, mặt hàng nạp 1 truy vấn cho cả trang (không N+1)
- [x] `filterMeta()` — kho / nhân viên / thương hiệu, **chỉ giá trị thực sự có trong phạm vi user**
- [x] Nhãn nhân viên dựng bằng `employeeOptionLabel()` → `Tên - Mã phòng - Mã NV` (CLAUDE.md)
- [x] **Đo thật trên `gop_db`**: NV #34 (quyền tổng công ty) thấy 74 phiếu · NV #101 (không quyền)
      thấy 4 phiếu của mình · chưa đăng nhập thấy 0 — cả 3 khớp SQL thuần
- [x] Phát hiện + vá **lỗi ERP #10**: ô lọc Kho của ERP đổ từ `accounting_warehouses` nhưng lọc
      trên `warehouses` ⇒ chọn kho này lọc ra kho khác

## Phase 2 — BE controller & route ✅ (2026-09-23)

- [x] `BorrowStockController`: `index` · `meta` (export/print để Phase 5)
- [x] `BorrowExpiringController extends BorrowStockController` — chỉ override `scoped()` để
      **merge cờ `expiring_only` ở BE**, không đọc cờ FE gửi lên (đúng cách `PrepickExpiringController`)
- [x] 4 route `finance/borrow-stocks` + `finance/borrow-expiring`, toàn route tĩnh, không có `/{id}`
- [x] ~~Seeder cấp quyền~~ — **KHÔNG CẦN**: trait tra quyền theo TÊN gộp mọi guard, bản `web` của
      ERP đang gán cho 3 role là đủ (đã đo)
- [x] ~~Resource/Transformer riêng~~ — **KHÔNG CẦN**: service đã trả mảng thuần kèm `status_name`
      / `status_type` và ngày `dd/mm/yyyy`; bọc thêm Resource chỉ để map lại đúng các khoá đó là thừa
- [x] Đo qua controller: chưa đăng nhập **403** · NV #101 **4** phiếu · NV #34 **74** phiếu ·
      `meta` trả 7 kho / 35 NV / 32 thương hiệu / 3 trạng thái

## Phase 3 — FE màn Danh sách hàng mượn ✅ (2026-09-23)

- [x] `pages/finance/borrow-stocks/index.vue` — khung copy từ `prepick-stocks/index.vue`
- [x] 5 mixin: `PageTitleMixin` · `filterStateMixin` · `DedupeLoadMixin` ·
      `columnCustomizationMixin` · `reportPrintPreviewMixin`
- [x] `localStorageKey` / `columnScreenKey` riêng (`finance_borrow_stocks`)
- [x] `V2BaseSmartFilterPanel` + `floating`, 8 ô lọc, khối tổ chức khai đủ 4 key
- [x] ~~`show-quick-search=false` — ERP không có ô tìm nhanh…~~ **QUYẾT ĐỊNH SAI, đã sửa 24/09/2026**
      (user báo): tắt cờ này làm mất ô tìm nhanh VÀ dồn nút Tìm kiếm / Làm mới vào khối nâng cao —
      lệch chuẩn mọi màn danh sách. Lấy giao diện theo ERP là trái nguyên tắc gốc. Đã thêm param
      `keyword` ở BE (mã phiếu · người mượn · tên/mã hàng còn nợ) + bật ô tìm nhanh ở FE, sửa thẳng
      trên `gop_db`. Skill `list-page` + `erp-to-hrm-screen` đã bổ sung quy tắc cấm tắt.
- [x] Bảng dòng mở rộng ▸ (tầng 2 = mặt hàng). Mặt hàng nằm sẵn trong response nên mở/thu là việc
      THUẦN FE, không gọi thêm API — nhẹ hơn màn hàng giữ (bên đó lazy load từng hàng hoá)
- [x] Badge trạng thái qua `V2BaseBadge` + `statusBadgeVariant.js`, text/màu đều do BE trả
- [x] Cột "Yêu cầu" mở tab ERP (`openErp` dạng `<a target="_blank">`) — màn chi tiết phiếu chưa port
- [x] 4 cột số để TRỐNG ở dòng phiếu: một phiếu gồm nhiều đơn vị khác nhau (Cái / Can 6KG /
      Xô 18L), cộng tổng là con số vô nghĩa
- [x] Gắn `link` vào 2 mục menu có sẵn (`finance.js` nhóm Mượn hàng + `lookup.js` nhóm Thông báo)

## Phase 4 — FE màn Hàng sắp hết hạn mượn ✅ (2026-09-23)

- [x] `pages/finance/borrow-expiring/index.vue` — **`extends` màn Danh sách hàng mượn**, chỉ ghi đè
      `title` / `apiPrefix` / 3 khoá lưu / `filterFields`. **47 dòng thay vì chép ~500 dòng.**
      (Cặp màn hàng giữ đang là 2 bản chép 957 + 974 dòng — sửa gì cũng phải nhớ sửa 2 nơi.)
- [x] 6 ô lọc — bỏ khối tổ chức và ô Nhân viên (màn luôn chỉ phiếu của chính mình)
- [x] Khoá riêng `finance_borrow_expiring` + id popup xuất file riêng
- [x] Gắn `link` vào 2 mục menu có sẵn

## Phase 5 — Xuất Excel & Bản in ✅ (2026-09-23)

- [x] BE `exportRows()` — dòng PHẲNG (1 dòng = 1 mặt hàng còn nợ), 14 cột, đi qua đúng
      `applyViewScope()` + `applyFilters()` của màn
- [x] BE `flatQuery()` dùng CHUNG cho Xuất Excel và Bản in ⇒ 2 chỗ không thể lệch số dòng
- [x] BE `printListData()` + `buildPrintTable()` — bảng gom 3 cấp Phòng ban → Người mượn → Mặt
      hàng, **đúng bố cục ERP** (khác bảng 2 tầng trên màn; kế toán đối chiếu bản in theo phòng ban)
- [x] Dùng mẫu in của ERP trong DB: `report_templates` **243** (danh sách) và **245** (sắp hết hạn)
      — ERP có mẫu RIÊNG cho từng màn, không dùng chung. Thêm 2 hằng vào `ErpReportTemplate`
- [x] `PRINT_LINE_LIMIT = 10000` (ERP không chặn gì → dữ liệu lớn là trình duyệt đơ)
- [x] 4 route `/export` + `/print` cho cả 2 màn
- [x] FE `components/export-excel.js` — 14 cột, dùng chung 2 màn, `ExportFieldsModal` chọn trường
      trước (KHÔNG xuất thẳng), thứ tự cột theo thứ tự user tick
- [x] FE nút In + Xuất Excel + `ReportPrintPreviewModal` (khổ ngang)
- [x] **Đo thật**: export ra **193 dòng phẳng** / 14 cột · print ra **190.737 ký tự**, 249 `<tr>`,
      không còn biến `{...}` nào chưa thay

## Phase 6 — Đối chiếu ngược ERP + verify ✅ (2026-09-23)

- [x] Đủ 13 cột ERP · 8 ô lọc · 3 trạng thái
- [x] Bộ grep tự kiểm của skill `erp-to-hrm-screen` — sạch cả 9 mục
- [x] Đo phạm vi quyền qua controller: chưa đăng nhập 403 · NV #101 4 phiếu · NV #34 74 phiếu
- [x] **Verify trên trình duyệt + XEM ẢNH** (DNS Admin, quyền tổng công ty):
  - Danh sách ra **74 phiếu**, 12 cột, ngày `dd/mm/yyyy`, badge "Hết hạn" đỏ, mã phiếu là link
    sang cổng ERP (`qttt.tanphat.com/.../product_export_requests/35595/show`)
  - Mở/thu ▸ chạy, dòng mặt hàng ra đủ SL mượn / Đã trả / Còn lại / Đơn vị
  - 9 ô lọc hiện đủ, nhãn floating, cùng chiều cao
  - **Lọc Kho = "LN - Liên Ninh" → 74 còn 20 phiếu, bảng chỉ còn đúng kho đó** (SQL thuần: 20 ✓)
  - "Làm mới" về lại 74
  - **In**: letterhead Tân Phát + "BÁO CÁO DANH SÁCH HÀNG MƯỢN" + bảng gom 3 cấp, Tổng cộng 193
  - **Xuất Excel**: popup 14/14 trường → file `danh_sach_hang_muon.xlsx`, 195 dòng × 15 cột, ô số
    là **number** + `numFmt #,##0.##` (không dính "number stored as text")
  - Màn **Hàng sắp hết hạn mượn**: tiêu đề / API / 6 ô lọc / khoá lưu / id popup đều riêng, trạng
    thái rỗng in "Không có dữ liệu phù hợp bộ lọc."
  - Console: **0 lỗi**. 2 cảnh báo là của build toàn dự án (postcss `flex-end`, export thiếu ở
    `Sidebar.vue`), không liên quan màn này
- [x] **2 lỗi tự tìm ra khi verify và đã sửa** — xem mục dưới
- [x] **Verify nốt bằng dữ liệu demo bơm vào DB local** (user cho phép sửa DB):
  - Màn **Hàng sắp hết hạn mượn** ra đúng **6 phiếu** của DNS Admin — trước đó 0 dòng nên chưa
    khẳng định được màn chạy
  - **Đủ CẢ 3 badge trên cùng một màn**: Trong hạn (xanh) · Đến hạn (vàng) · Hết hạn (đỏ),
    đúng bảng màu SRS
  - Lọc Trạng thái = **Trong hạn** → 2 phiếu, hạn trả 28/09 ✓ · = **Đến hạn** → 2 phiếu,
    hạn trả 23/09 ✓
  - Cửa sổ `warning_day = 7` chạy đúng: phiếu hạn 28/09 lọt, và phiếu đã quá hạn (03/08) vẫn hiện
    ở màn Sắp hết hạn — **đúng ERP** (điều kiện `<=` bao gồm cả quá khứ), không phải lỗi

## 2 lỗi phát hiện khi verify trình duyệt (23/09/2026)

**1. Cột "Yêu cầu" ở dòng mặt hàng in nhầm MÃ HÀNG.** Service trả khoá `code` cho mặt hàng, trùng
tên với `code` = mã phiếu của tầng 1 ⇒ `V2BaseDataTable` lấy `item.code` làm nội dung mặc định cho
ô cột "Yêu cầu". Sửa: đổi tên khoá thành `product_code`.
⚠️ Bài học: **dòng cha và dòng con trong bảng cây KHÔNG được trùng tên khoá** với bất kỳ `column.key`
nào — bảng tự điền nội dung mặc định, không báo lỗi gì.

**2. Bộ lọc ghi được giá trị nhưng bảng KHÔNG tải lại.** Deep watcher của Vue 2 đưa `newVal` và
`oldVal` là **CÙNG MỘT object** khi bộ lọc bị sửa tại chỗ ⇒ so `newVal[k] !== oldVal[k]` lúc nào
cũng bằng nhau, `changed` luôn rỗng, không bao giờ gọi `loadData()`. Chọn ô lọc xong bảng y nguyên
mà console sạch trơn. Sửa: so với bản sao SÂU tự giữ (`oldFilters`), đúng cách `prepick-stocks` làm.
⚠️ Bài học: đây là lỗi **chỉ bấm thật mới thấy** — grep tự kiểm và compile đều sạch.

## Phase 7 — Tài liệu ✅ (2026-09-23)

- [x] `design.md` + `plan.md` (file này)
- [x] Cập nhật `.plans/gop-db/STATUS.md`
- [x] Spec đầy đủ `docs/superpowers/specs/gop-db/2026-09-23-finance-borrow-stock-list-design.md`
- [x] Ghi memory phần học được (`project_kho_nhap_xuat.md`)

## Dữ liệu demo đã BƠM VÀO DB LOCAL (23/09/2026) — nhớ khôi phục

Dump `gop_db` gốc không kiểm được 2/3 badge và màn "Sắp hết hạn": mọi phiếu mượn có hạn trả
22/04–04/08/2026 (đã quá hạn hết), và tài khoản test DNS Admin (`employees.id = 13`) chưa tự lập
phiếu mượn nào. **User cho phép sửa DB local để test (23/09/2026)** → đã sửa 6 phiếu:

| Phiếu | Đổi gì | Để test |
|---|---|---|
| PYCXH-35595, PYCXH-35567 | `created_by` → 13, `return_date` → 28/09/2026 | badge **Trong hạn** (xanh) |
| PYCXH-35542, PYCXH-35539 | `created_by` → 13, `return_date` → 23/09/2026 | badge **Đến hạn** (vàng) |
| PYCXH-35519, PYCXH-35518 | `created_by` → 13 (giữ hạn trả 03/08) | badge **Hết hạn** (đỏ) |

Cả 6 đều `created_by = 13` nên màn **Hàng sắp hết hạn mượn** của DNS Admin ra đúng 6 dòng
(`configs.warning_day = 7` ⇒ cửa sổ tới 30/09, cả 6 đều lọt).

⚠️ **Giá trị gốc đã sao lưu trong bảng `_bak_borrow_test_20260923`.** Chạy
[`./khoi-phuc-du-lieu-test.sql`](./khoi-phuc-du-lieu-test.sql) để trả lại nguyên trạng.
**Phải khôi phục trước khi chạy harness đối chiếu phạm vi quyền HRM vs ERP**, nếu không 6 phiếu
này lệch chủ và làm sai kết quả đối chiếu.

## Quyết định đã chốt (23/09/2026)

1. ✅ **Ô "Nhân viên" lấy từ `/meta` của BE, KHÔNG lọc `ALL_EMPLOYEES` phía client như ERP.**
   Copy nguyên cách màn hàng giữ đã làm (`prepick-stocks/index.vue::employeeOptions`):
   - BE chỉ trả **người THỰC SỰ đang có hàng mượn**, đã cắt theo phạm vi quyền của user
   - FE thu hẹp tiếp theo Công ty / Phòng ban đang chọn
   - `V2BaseCompanyDepartmentFilter` tự xoá `employee_id` khi đổi công ty/phòng ban nên không sót
     giá trị cũ ngoài danh sách

   Cách của ERP (lọc mảng `ALL_EMPLOYEES` toàn hệ thống theo `department_id`) cho ra dropdown đầy
   **lựa chọn chết** — chọn người chưa từng mượn gì thì bảng trống trơn — và không cắt theo quyền.

2. ✅ **Màn "Hàng sắp hết hạn mượn" giữ đúng ERP**: luôn bó `created_by = mình`, kể cả người có
   quyền "theo tổng công ty". Đây là màn *"hàng CỦA TÔI sắp đến hạn trả"*, không phải màn quản lý.
   Ai cần nhìn toàn công ty thì dùng màn `Danh sách hàng mượn` + lọc Trạng thái = Đến hạn/Hết hạn.

---

## Phase 8 — Sửa lỗi port nhầm biến thể (24/09/2026)

User đẩy lên dev rồi đối chiếu `erp-crm/.../accountingExpiringBorrow` với
`hrm-crm/finance/borrow-expiring` → **HRM thiếu rất nhiều dữ liệu**.

- [x] Truy nguyên: ERP có **2 màn** sắp hết hạn mượn ở **2 phân hệ**, dùng chung truy vấn, khác
      đúng một điều kiện — `expiringBorrow` (Thông báo, bó `created_by = mình`) và
      `accountingExpiringBorrow` (Kế toán kho → Mượn hàng, không bó người)
- [x] Mục menu HRM ở `finance.js` nhóm Mượn hàng ứng với **bản kế toán**, bản port đầu làm nhầm
      bản cá nhân ⇒ đo trên `gop_db`: **74 → 6 phiếu**
- [x] Bỏ `created_by = auth()->id()` khỏi `applyExpiringWindow()`; phạm vi để `applyViewScope()` lo
- [x] Sửa docblock service + `BorrowExpiringController` — ghi rõ port bản KẾ TOÁN và vì sao
- [x] Đo lại qua controller: DNS Admin (tổng công ty) **74** ✓ · NV #101 (không quyền) **2** ✓
- [x] Cập nhật design.md (mục 11) + spec + STATUS + memory
- [x] **User đẩy bản sửa lên dev rồi đối chiếu lại 2 cổng** — xác nhận KHỚP (24/09/2026)

## Checkpoint — 2026-09-23

- **Vừa hoàn thành**: Phase 0-7 — BE + FE 2 màn + xuất Excel + bản in + menu + tài liệu, **đã
  verify trên trình duyệt và xem ảnh**. Tìm và sửa 2 lỗi chỉ lộ khi bấm thật.
- **Đang làm dở**: không có.
- **Bước tiếp theo**: user nghiệm thu. Sau đó merge 2 nhánh `feat/finance-borrow-stock-list` về
  `gop_db` (user làm phần git).
- **Blocked**: không. Còn 2 việc phải làm **trên cổng dev** vì dữ liệu local không đủ:
  kiểm badge "Trong hạn" / "Đến hạn", và kiểm màn Sắp hết hạn bằng tài khoản CÓ lập phiếu mượn.
  Chưa commit, chưa push.
