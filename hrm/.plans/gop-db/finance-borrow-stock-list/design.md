# Danh sách hàng mượn + Hàng sắp hết hạn mượn (ERP → HRM) — design

- **Người phụ trách:** @junfoke — 2026-09-23
- **Trạng thái**: KHẢO SÁT XONG, chưa viết code — xem `./plan.md`
- **Phạm vi**: **2 màn** báo cáo tra cứu, **CHỈ ĐỌC** (không thêm/sửa/xóa)
  - `Danh sách hàng mượn` — ERP `warehouseInfo.borrowIndex`
  - `Hàng sắp hết hạn mượn` — ERP `warehouseInfo.accountingExpiringBorrow` (**bản KẾ TOÁN**,
    không phải bản cá nhân `expiringBorrow` — xem mục 11)
- **Phân hệ đích**: Tài chính (`Modules/Finance`) — mọi màn hàng mượn khác đã nằm ở đây
- **Tiền lệ bám sát**: cặp màn SONG SINH bên hàng giữ đã port xong —
  [Danh sách hàng giữ](../finance-prepick-stock-list/design.md) +
  [Hàng sắp hết hạn giữ](../finance-prepick-expiring/design.md).
  ERP dùng **cùng một controller, cùng một truy vấn** cho cả 2 cặp, chỉ khác bảng nguồn.

---

## Mục tiêu

Người dùng tra được **ai đang mượn hàng gì, hạn trả bao giờ, còn nợ bao nhiêu** mà không phải mở
từng phiếu xuất mượn; và người mượn tự thấy hàng của mình **sắp đến hạn trả**.

## Bảng dữ liệu (dùng chung ERP — KHÔNG tạo bảng mới, KHÔNG migration)

Màn này **không có bảng riêng**. Nó là một góc nhìn của phiếu xuất mượn:

| Bảng | Vai trò |
|---|---|
| `product_export_requests` (`per`) | phiếu mượn — lọc `type = 3 (XUAT_MUON)` + `borrow_status = 2 (DA_MUON)` |
| `product_export_request_details` | dòng hàng — điều kiện còn nợ `base_exported_qty > borrow_returned_qty` |
| `warehouse_export_requests` (`wer`) | nối sang kho |
| `warehouses` (`w`) | tên/mã kho |
| `configs.warning_day` | số ngày cảnh báo, dùng cho màn "sắp hết hạn" |

⚠️ Một phiếu **đã trả hết** thì biến mất khỏi danh sách (điều kiện `whereExists` ở ERP), chứ không
hiện với số còn lại = 0.

## Hiện trạng ERP

### Cấu trúc bảng 2 tầng

| Tầng | Cột |
|---|---|
| Cha — 1 phiếu (7 cột) | Người mượn · Phòng ban · **Yêu cầu** (mã phiếu, link `product_export_requests/{id}/show`) · Kho · Ngày mượn · Ngày hẹn trả · Trạng thái |
| Con — 1 mặt hàng (6 cột) | Tên hàng · Mã hàng · SL mượn · Đã trả · Còn lại · Đơn vị |

ERP dựng bằng `rowspan` (ô cha kéo dọc qua các dòng con).

### Trạng thái hạn mượn (tính runtime, KHÔNG lưu DB)

So `product_export_requests.return_date` với hôm nay:

| Trạng thái | Điều kiện | Màu ERP | Màu HRM |
|---|---|---|---|
| Trong hạn | hẹn trả **>** hôm nay | `bg-success` | xanh |
| Đến hạn | hẹn trả **=** hôm nay | `bg-warning` | vàng |
| Hết hạn | hẹn trả **<** hôm nay | `bg-danger` | đỏ |

Màu ERP ở đây đã đúng nhóm SRS — **không phải sửa** như trường hợp "Đang tạo" của các màn chứng từ.

### Bộ lọc ERP

| Ô lọc | Danh sách hàng mượn | Sắp hết hạn | BE lọc theo |
|---|---|---|---|
| Kho | ✔ | ✔ | `wer.warehouse_id` |
| Phòng ban | ✔ | ✖ | `per.created_by IN Department::getMembers()` |
| Nhân viên | ✔ (dây chuyền theo Phòng ban) | ✖ | `per.created_by` |
| Model | ✔ | ✔ | `details.model_name LIKE` |
| Thương hiệu | ✔ | ✔ | `details.brand_id` |
| Tên hàng | ✔ | ✔ | `details.product_name LIKE` |
| Mã hàng | ✔ | ✔ | `details.code LIKE` |
| Trạng thái | ✔ | ✔ | so `return_date` với hôm nay |

Màn "sắp hết hạn" bỏ 2 ô Phòng ban / Nhân viên — ERP bản kế toán cũng không có 2 ô này.

Nguồn dữ liệu cho 2 ô **Phòng ban / Nhân viên** xem mục 8 bảng dưới — HRM lấy từ BE, không
lọc danh sách nhân sự toàn hệ thống ở client như ERP.

### Cùng một endpoint phục vụ 4 màn

`warehouseInfo.borrowSearchData` nhận `?type=`:

| `type` | Màn | Bó thêm |
|---|---|---|
| (rỗng) | Danh sách hàng mượn | — |
| `expiring` | Hàng sắp hết hạn mượn **(bản cá nhân, phân hệ Thông báo)** | `return_date <= hôm nay + warning_day` **và** `created_by = mình` |
| `accounting_expiring` | Hàng sắp hết hạn mượn **(bản KẾ TOÁN — HRM port bản này)** | chỉ `return_date <= hôm nay + warning_day`, KHÔNG bó người |
| `accounting_expired` | (Kế toán kho) đã quá hạn | `return_date < hôm nay` |

Biến thể `accounting_expired` (đã quá hạn) **không làm đợt này**. Bản cá nhân `expiring`
cũng không port thành màn riêng — xem mục 11.

## Các điểm bất nhất của ERP và cách xử lý

| # | ERP | Xử lý ở HRM |
|---|---|---|
| 1 | **Không có quyền nào cả** — nhóm route `warehouse_infos` không gắn middleware, controller không kiểm gì ⇒ ai đăng nhập cũng thấy hàng mượn của TOÀN công ty | **Siết lại**: gate vào màn + phạm vi 3 cấp (mục Phân quyền). User chốt 23/09/2026 |
| 2 | Sắp xếp `per.created_at ASC` — phiếu cũ nhất lên đầu | Đổi **giảm dần** theo SRS; ghi vào bảng "sửa có chủ ý" |
| 3 | Phân trang cứng 20 dòng, không đổi được | Theo chuẩn HRM: mặc định 10, chọn 5/10/20/50/100 |
| 4 | Bảng `rowspan`, in nhiều trang hay vỡ ô gộp | Dòng mở rộng ▸ như màn hàng giữ (user chốt 23/09/2026) |
| 5 | Lọc theo hàng hoá chạy 2 lượt truy vấn (`pluck('parent_id')` rồi `whereIn`) — danh sách phiếu lớn thì mảng id khổng lồ | Đổi sang `whereExists` một lượt, cùng kiểu đang lọc "còn nợ" |
| 6 | Ô "Model" là select nhưng ERP lọc bằng `LIKE model_name` (chuỗi), không theo id | Giữ đúng nghiệp vụ; FE dùng `V2BaseSelectRemote` trả về **tên model** |
| 7 | Cột "Yêu cầu" link sang màn ERP `product_export_requests/{id}/show` | **Điểm cắt** — mở tab ERP bằng `openErp()` (như màn YCMDV), chưa port màn đó |
| 8 | Ô **Nhân viên** lọc mảng `ALL_EMPLOYEES` (toàn hệ thống) phía client theo `department_id` ⇒ dropdown đầy **lựa chọn chết**, chọn người chưa từng mượn là bảng trống; không cắt theo quyền | Lấy từ `/meta` của BE — chỉ người THỰC SỰ đang có hàng mượn, đã cắt theo phạm vi quyền; FE thu hẹp tiếp theo Công ty/Phòng ban. Copy `prepick-stocks/index.vue::employeeOptions` |
| 9 | ERP có **2 màn sắp hết hạn** dùng chung truy vấn: bản cá nhân `expiringBorrow` (phân hệ Thông báo, bó `created_by = mình`) và bản kế toán `accountingExpiringBorrow` (Kế toán kho → Mượn hàng, KHÔNG bó người) | Port **bản kế toán**; phạm vi để `applyViewScope()` lo. Không port riêng bản cá nhân vì người không có quyền phạm vi nào đã tự bị bó về phiếu của mình — xem mục 11 |
| 10 | **Ô lọc Kho lọc SAI KHO.** Dropdown đổ từ `accounting_warehouses` (55 dòng) nhưng query lọc `wer.warehouse_id` trỏ sang `warehouses` (23 dòng). Id trùng nhau nhưng là kho KHÁC: `warehouses` id=2 = "LN – Liên Ninh", `accounting_warehouses` id=2 = "LN02 – Liên Ninh - Hàng khuyến mại" ⇒ chọn một kho, lọc ra kho khác, mà cột Kho lại in tên theo `warehouses` | Lấy dropdown từ **`warehouses`**, đúng bảng đang join, và chỉ những kho THỰC SỰ có phiếu mượn trong phạm vi user (đo 23/09: 7 kho, không phải 55) |

## Thiết kế bản HRM

### Route & menu

| Màn | Route FE | Mục menu ĐÃ CÓ SẴN (chỉ thiếu `link`) |
|---|---|---|
| Danh sách hàng mượn | `/finance/borrow-stocks` | `finance.js:187` (nhóm **Mượn hàng**) + `lookup.js:49` (nhóm **Thông báo**) |
| Hàng sắp hết hạn mượn | `/finance/borrow-expiring` | `finance.js:188` + `lookup.js:50` |

ERP đặt mỗi màn ở **đúng 2 chỗ** (`topmenubar.blade.php:852-853` phân hệ Thông báo và `:1056-1057`
phân hệ Kế toán kho → nhóm Mượn hàng) ⇒ HRM khai đủ 2 chỗ, **không thêm chỗ thứ ba**.

### Phân quyền

**KHÔNG tạo quyền mới** — 3 quyền phạm vi của luồng hàng mượn đã có sẵn và đang được 3 màn khác
dùng (`BorrowExportRequest`, `BorrowSellRequest`, `BorrowExport`):

| Quyền | id `web` | id `api` |
|---|---|---|
| Xem phiếu hàng mượn theo tổng công ty | 100890 | 1565 |
| Xem phiếu hàng mượn theo công ty | 100891 | 1566 |
| Xem phiếu hàng mượn theo phòng ban | 100892 | 1567 |

**KHÔNG cần seeder cấp quyền.** `ChecksEmployeePermission` tra quyền **theo TÊN, gộp mọi guard** (`pluck` hết id trùng tên rồi `whereIn`), nên bản `web` đang gán cho 3 role của ERP là đủ. Đã đo 23/09/2026: NV #34 (có quyền tổng công ty qua role ERP) thấy **74/74** phiếu, NV #101 (không quyền) thấy **4** phiếu của chính mình — khớp SQL thuần.

Phạm vi dữ liệu (fail-closed, xét theo thứ tự) — đúng khuôn màn hàng giữ:

| Điều kiện | Thấy gì |
|---|---|
| Super admin (role 18) **hoặc** `… theo tổng công ty` | mọi công ty |
| `… theo công ty` | phiếu của người cùng công ty mình |
| `… theo phòng ban` | `per.created_by IN` thành viên phòng mình quản lý **hoặc** chính mình |
| Không quyền nào | chỉ `per.created_by = mình` |

⚠️ Khác biệt **"theo phòng ban"** của HRM (cộng thêm phòng mình đang ngồi) là quy ước chung toàn
phân hệ, user đã chốt giữ nguyên 23/09/2026 — xem
[YCMDV design](../buy-service-request/design.md). Áp y như vậy ở đây, không xử lý riêng.

Màn **Hàng sắp hết hạn mượn** giữ đúng ERP: luôn bó `created_by = mình`, quyền phạm vi không nới
thêm (nó là màn "hàng CỦA TÔI sắp đến hạn").

### Cấu trúc BE

| File | Việc |
|---|---|
| `Modules/Finance/Services/BorrowStockReportService.php` | **mới** — truy vấn dùng chung cho cả 2 màn + export + print. Khuôn: `PrepickStockReportService` |
| `Modules/Finance/Http/Controllers/V1/BorrowStockController.php` | **mới** — `index` · `filter-options` · `export` · `print` |
| `Modules/Finance/Services/PrepickConfigService.php` | **dùng lại** — docblock đã ghi sẵn `warning_day` dùng cho "hàng giữ / hàng **mượn**" |
| `Modules/Finance/Entities/ProductImportRequest/ProductExportRequest.php` | **dùng lại** hằng `XUAT_MUON` / `DA_MUON` — đã port |
| `app/ExcelExport/ExportColumnRegistry.php` | thêm khoá `borrow_stocks` |
| `Modules/Finance/Routes/api.php` | thêm nhóm route |

⚠️ **KHÔNG đụng `BorrowStockService`** (đã có, tính *tồn hàng mượn đang treo ở luồng khác*). Màn
này chỉ cần phép trừ thẳng `base_exported_qty - borrow_returned_qty`. Hai thứ khác nhau — đặt tên
service mới là `BorrowStockReportService` cho khỏi nhầm, đúng cách hàng giữ đã tách
`PrepickStockService` (tồn) vs `PrepickStockReportService` (báo cáo).

### Cấu trúc FE

| File | Việc |
|---|---|
| `pages/finance/borrow-stocks/index.vue` | màn chính |
| `pages/finance/borrow-expiring/index.vue` | màn sắp hết hạn (2 màn RIÊNG, đúng cách hàng giữ làm — không dùng `?type=`) |
| `pages/finance/borrow-stocks/components/export-excel.js` | bộ cột xuất Excel, dùng chung cho cả 2 màn |

Bảng dùng `V2BaseDataTable` với **dòng mở rộng ▸**: tầng 1 = phiếu mượn, bấm ▸ ở cột STT xổ ra
các mặt hàng. Copy pattern từ `pages/finance/prepick-stocks/index.vue`.

### Xuất Excel & Bản in

- Xuất: `ExportFieldsModal` chọn cột trước → `ExportColumnRegistry` + `DynamicExport` (4 mắt xích)
- In: `ReportPrintPreviewModal` + `reportPrintPreviewMixin`, chặn 2000 dòng bằng `LimitsPrintListRows`
- Cả 2 đi qua **đúng bộ lọc đang áp dụng** trên màn

## 11. Port NHẦM biến thể — lỗi đã sửa 24/09/2026

**Triệu chứng:** user đối chiếu trên dev thấy màn HRM `/finance/borrow-expiring` **thiếu rất nhiều
dữ liệu** so với ERP `accountingExpiringBorrow`.

**Nguyên nhân:** ERP có **HAI màn** "hàng sắp hết hạn mượn", dùng chung một truy vấn, khác nhau
đúng một điều kiện — và nằm ở **hai phân hệ khác nhau**:

| ERP | Vị trí menu | Bó thêm | Đo trên `gop_db` |
|---|---|---|---|
| `expiringBorrow` | phân hệ **Thông báo** (`topmenubar:853`) | `created_by = chính mình` | 6 phiếu (DNS Admin) |
| `accountingExpiringBorrow` | Kế toán kho → **Mượn hàng** (`topmenubar:1057`) | không bó người | **74 phiếu** |

Mục menu của HRM ở `finance.js` nhóm **Mượn hàng** ứng với **bản kế toán**, nhưng bản port đầu lại
implement bản cá nhân ⇒ hụt 74 → 6.

**Đã sửa:** bỏ `created_by = auth()->id()` khỏi `applyExpiringWindow()`. Phạm vi người xem để
`applyViewScope()` lo như màn Danh sách. Đo lại sau khi sửa: DNS Admin (tổng công ty) **74 phiếu**
✓ · NV #101 (không quyền) **2 phiếu** của chính mình ✓.

**Không port riêng bản cá nhân** — `applyViewScope()` đã tự bó về phiếu của chính mình với người
không có quyền phạm vi nào, nên một màn phục vụ được cả hai nhóm. Màn "Hàng sắp hết hạn giữ"
(`PrepickExpiringController`) cũng chốt đúng cách này và ghi rõ trong docblock.

⚠️ **Bài học:** skill `erp-to-hrm-screen` đã cảnh báo *"một màn có thể nằm ở NHIỀU nhóm menu, giữ
nguyên tham số trên link — copy link mà bỏ tham số là hỏng ý nghĩa mục menu"*. Ở đây còn nặng hơn:
không phải cùng một route khác tham số, mà là **hai route khác hẳn nhau**. Khi màn ERP xuất hiện ở
2 phân hệ, phải mở **cả hai** controller ra đọc, đừng cho rằng chúng giống nhau.

## Không làm trong đợt này

- 2 biến thể Kế toán kho (`accounting_expiring`, `accounting_expired`)
- Màn chi tiết phiếu xuất mượn (`product_export_requests/{id}/show`) — vẫn mở sang ERP
- Lịch sử thay đổi: **màn chỉ đọc, không sinh log** → không có khối lịch sử

## Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| Siết quyền làm người đang dùng ERP mất dữ liệu quen thuộc | Đối chiếu số dòng HRM vs ERP theo từng nhân sự trước khi giao, như đã làm ở YCMDV |
| Dòng mở rộng + xuất Excel: file phẳng 13 cột, lặp phần cha | Theo đúng cách màn hàng giữ đang xuất |
| `Department::getMembers()` của ERP chưa có bản HRM tương đương | Dùng `ChecksEmployeePermission::departmentMemberIds()` đã có |
