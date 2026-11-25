# #11924 — Chặn khóa hàng hóa khi còn phiếu/HĐ đang trong tiến trình

> Thiết kế (brainstorming) — chờ user duyệt trước khi lên plan & code.
> Vé: http://quanly.dnsmedia.vn/issues/11924 (project "ERP - Yêu cầu sửa lỗi (TPE gửi)").

## 1. Ý đồ & vì sao

TPE yêu cầu: khi **khóa (lock) một hàng hóa** trong Danh mục hàng hóa, phải **chặn** nếu hàng còn
nằm trong **bất kỳ phiếu đang trong tiến trình** thuộc 3 luồng (mua / nhập / xuất) **hoặc** một
**hợp đồng** liên quan còn hiệu lực & chưa xuất hết. Mục tiêu nghiệp vụ: không cho "khóa" một hàng
vẫn đang được giao dịch dở (tránh kẹt chứng từ đang chạy).

Thông báo (theo vé):
- Luồng mua: **"Hàng đang trong tiến trình mua"**
- Luồng nhập: **"Hàng đang trong tiến trình nhập"** (vé gõ "tiền trình nhâp" — lấy câu đúng chính tả)
- Luồng xuất: **"Hàng đang trong tiến trình xuất"**
- Hợp đồng: **(đề xuất)** "Hàng đang trong hợp đồng chưa xuất hết" — *vé không ghi rõ câu, cần chốt*.

## 2. Màn này nằm ở HRM (không phải ERP)

Vé filed ở project ERP nhưng màn DM hàng hóa + chức năng khóa **đã dời sang HRM**:
- ERP: route products bị comment + gắn middleware `productMovedToHrm`; `ProductsController` không còn hàm lock.
- HRM: `Modules/MasterData/Services/Product/ProductLifecycleService::lock()` là implementation đang chạy.
→ **Fix ở HRM.** (Giống tiền lệ vé firm-warranty: TPE quen filed ở ERP cho cả màn đã port.)

## 3. Chỗ sửa & kiến trúc đề xuất

`ProductLifecycleService::lock()` (hiện ở `Modules/MasterData/Services/Product/ProductLifecycleService.php`,
~dòng 312–331) hiện chỉ chặn: đã khóa (423) / trạng thái ≠ Đang kinh doanh (422). **Chưa có** guard tiến trình.

**Approaches đã cân nhắc (cách build):**
- **(A) — ĐỀ XUẤT:** Tạo service dùng chung mới `ProductInProgressService` (theo chủ đề nghiệp vụ,
  đúng quy tắc Bước 3b của skill erp-to-hrm-screen). Nó phơi ra:
  - `firstBlockingFlow(int $productId, int $companyId): ?string` — trả `'buy'|'import'|'export'|'contract'|null`,
    kiểm theo thứ tự mua → nhập → xuất → HĐ, dừng ở luồng đầu tiên vướng (vé chỉ cần 1 câu).
  - Mỗi luồng 1 method `exists*InProgress()` dùng `EXISTS` (không đếm, không kéo dữ liệu), company-scoped.
  `lock()` gọi `firstBlockingFlow()`, có kết quả thì `fail(<message theo luồng>)` (422, theo đúng pattern
  `fail()` hiện có — business state, không phải 423 lock-record).
  *Lợi:* các màn khác (xóa cứng, chuyển kinh doanh, QA) tái dùng được; 1 nơi duy nhất giữ định nghĩa "đang tiến trình".
- **(B) nhét inline trong `lock()`:** nhanh hơn nhưng vi phạm quy tắc "hàm nghiệp vụ dùng chung", và
  logic quét ~10 bảng sẽ phình `lock()`. **Loại.**

**Hiệu năng:** mỗi luồng là 1 (hoặc vài) truy vấn `EXISTS` có `product_id` + `company_id` + lọc status;
dừng sớm ở luồng đầu tiên vướng. Kiểm/`EXISTS` thay vì `count`. Kiểm index `product_id` trên các bảng chi tiết.

## 4. Bản đồ dữ liệu (đã khảo sát 4 luồng, trích file:line ở phần ghi chú)

**Phạm vi:** quét theo **công ty đang làm việc** (`current_company_role`) — hàng khóa theo từng công ty,
nên chỉ chặn bởi chứng từ của chính công ty đó (giống `PriceAskingProductReader` dùng `a.company_id`).
Cần xác minh cột `company_id` tồn tại trên từng bảng header khi implement (task plan).

Cột "Độ chắc": ✅ đã trace tới hằng số/field; ⚠️ đề xuất ruling, cần chốt hoặc trace tiếp khi implement.

### 4.1 Luồng MUA — message "Hàng đang trong tiến trình mua"

| Phiếu | Bảng chi tiết → header | Map trạng thái | KẾT THÚC | Chặn khi status ∈ | Nguồn |
|---|---|---|---|---|---|
| Hỏi giá (YCHG) | `price_asking_request_products` → `price_asking_requests` | — | — | **Tái dùng** `PriceAskingProductReader::hasOpenRequest()` (open = WAITING_PTKD + ASKING_STATUSES + DRAFT, nhóm chưa CLOSED) | ✅ `PriceAskingProductReader:412` |
| YC đặt hàng trong nước | `inland_order_request_products` → `inland_order_requests` | 0 Đã hủy·1 Đã duyệt·2 Chờ duyệt·3 Đang tạo·4 Đang lập HĐ·5 Đã lập HĐ·6 Chờ TP duyệt | {0, 5 (đã chuyển HĐ→ check ở §4.4)} | {1,2,3,4,6} | `inland_order_requests/index.blade:74` |
| PDH (root) | `root_order_request_products` → `root_order_requests` | 0 Đã hủy·1 Đã duyệt·2 Chờ duyệt·3 Đang tạo·6 Chờ TP duyệt | {0, 1 (đã duyệt→chuyển `order_request2`)} | {2,3,6} | `root_order_requests/index.blade:66` |
| (legacy) Tiếp nhận/tổng hợp | `order_request_product2` → `order_request2` | DA_HUY=0·DA_TONG_HOP=4 (→chuyển inland) | {0,4} | phần còn lại | ⚠️ *cần xác minh gop_db còn loại này + map — task plan* |

### 4.2 Luồng NHẬP — message "Hàng đang trong tiến trình nhập"

> ⚠️ KHÔNG mượn bộ lọc của `IncomingStockService` (nó là "hàng đang về": loại cả đang tạo/chờ duyệt +
> ràng `type`/`created_at`). Blocking cần tập "chưa kết thúc" rộng hơn.
> **Nguyên tắc chốt (ruling #3): KẾT THÚC = {Đã hạch toán, Đã hủy, Đã nhập kho hoàn tất, Không duyệt}.**

Map trạng thái lấy từ blade ERP gốc (file:line ở cột cuối). "Chặn khi status ∈" = tập đang tiến trình.

| Phiếu | Bảng chi tiết → header | Map trạng thái | KẾT THÚC (không chặn) | Chặn khi status ∈ | Nguồn |
|---|---|---|---|---|---|
| YCNH | `product_import_request_details` → `product_import_requests` | 1 Đã đề nghị·2 Chờ duyệt·3 Đang tạo·4 Đang nhập kho·5 Đã hạch toán·6 Đã hủy·7 Đang lập ĐN·8 Đã nhập kho·9 Đang hạch toán·10-12 Chờ duyệt cấp | {5,6,8} | {1,2,3,4,7,9,10,11,12} | `product_import_requests/index.blade:85-96` |
| ĐNNK | `warehouse_import_request_details` → `warehouse_import_requests` | 1 Đang nhập kho·2 Chờ duyệt·3 Đang tạo·4 Đã hạch toán·5 Đã hủy·6 Đã nhập kho·7 Đang hạch toán | {4,5,6} | {1,2,3,7} | `warehouse_import_requests/index.blade:84-90` |
| PNK | `warehouse_import_lots` → `warehouse_imports` | DA_HACH_TOAN=1·KHONG_DUYET=4·DA_HUY=8 (const HRM) | {1,4,8} | phần còn lại {2,3,5,6,7} | const HRM `WarehouseImport` |
| Phiếu nhập hàng | `product_import_details` → `product_imports` | 1 Đã hoàn thành·3 Đang tạo | {1} | {3} | `product_imports/all.blade:85` |
| Tổng hợp chi phí NK | `order_import_request_products` → `order_import_requests` | 1 Đã duyệt·2 Chờ duyệt·3 Đang tạo (+ "Không duyệt") | {1, không duyệt} | {2,3} | `order_import_requests/index.blade:67` |
| Nhập hàng ĐC kiểm kê | `inventory_discrepancy_handling_import_products` → `inventory_discrepancy_handling_imports` | DANG_TAO=1·DA_GUI_NCC=2·KHONG_DUYET=3·CHO_DUYET=4·DA_DUYET=5 | {3,5} | {1,2,4} | const `InventoryDiscrepancyHandlingImport:78-82` |

### 4.3 Luồng XUẤT — message "Hàng đang trong tiến trình xuất"

> **Nguyên tắc chốt: KẾT THÚC = {Đã hạch toán, Đã hủy, Đã xuất kho hoàn tất, Không duyệt}; PXH KHÔNG tính (ruling #2).**
> ⚠️ **ĐNXK: KHÔNG dùng `status != 3` của `PrepickStockService`** — ở đây `status=3` = **"Đang tạo"** (nháp),
> loại nó sẽ bỏ sót phiếu nháp cần chặn. Dùng terminal theo status như dưới.

| Phiếu | Bảng chi tiết → header | Map trạng thái | KẾT THÚC | Chặn khi status ∈ | Nguồn |
|---|---|---|---|---|---|
| YCXH | `product_export_request_details` → `product_export_requests` | 1 Đã đề nghị·2 Chờ duyệt·3 Đang tạo·4 Đang xuất kho·5 Đã hạch toán·6 Đã hủy·7 Đang lập ĐN·8 Đã xuất kho·9 Đang hạch toán (+quyết toán) | {5,6,8,13 quyết toán} | `STATUS_PROCESING` (model) | `product_export_requests/forManager.blade:101` |
| ĐNXK | `warehouse_export_request_details` → `warehouse_export_requests` | 1 Đang xuất kho·2 Chờ duyệt·3 Đang tạo·4 Đã hạch toán·5 Đã hủy·6 Đã xuất kho·7 Đang hạch toán | {4,5,6} (+ `is_complete=1`) | {1,2,3,7} | `warehouse_export_requests/index.blade:84-90` |
| PXK | `warehouse_export_lots` → `warehouse_exports` | 1 Đã hạch toán·2 Chờ duyệt·3 Đang tạo·4 Không duyệt·5 Đã nhập lại·6 Đã xuất lại·7 Đang hạch toán | {1,4,5,6} | {2,3,7} | `warehouse_exports/index.blade:86` |
| PXH | ~ | ~ | **KHÔNG TÍNH** (ruling #2) | — | — |
| YC chuyển hàng | `product_transfer_request_products` → `product_transfer_requests` | 1 Đã tiếp nhận·2 Chờ duyệt·3 Đang tạo·4 Đang ĐN·14 Đã ĐN·5 Đang xuất kho·6 Đã xuất kho·7 Đang VC·8/9 Đang nhập kho·10 Đã nhập kho·11 Đã nhập hàng·12 Đã phân bổ·13 Đã hủy | {10,11,12,13} | {1,2,3,4,5,6,7,8,9,14} | `ProductTransferRequest::STATUSES:22-93` |
| PXH ĐC kiểm kê | `inventory_export_details` → `inventory_exports` | 1 Đã hoàn thành·3 Đang tạo | {1} | {3} | const `InventoryExport` |

### 4.4 HỢP ĐỒNG — message "Hàng đang trong hợp đồng chưa xuất hết" (đề xuất)

Điều kiện: tồn tại dòng HĐ có `product_id = X`, header **có hiệu lực** VÀ `quantity - exported_qty > 0`.

| Loại | Bảng chi tiết → header | "Có hiệu lực" | Độ chắc |
|---|---|---|---|
| HĐ vật tư (type=1) | `contract_products` / `root_contract_products` → `contracts` (type=1) | status IN {CO_HIEU_LUC=6, DANG_XUAT_HANG=8} | ✅ |
| HDDV | `service_contract_item_products` → `service_contracts` | status=CO_HIEU_LUC=6 | ✅ |
| HDDA | `project_contract_tab_products` → `project_contracts` | status=CO_HIEU_LUC=6 | ✅ |
| HĐNT (nguyên tắc, type=3) | `contract_products` → `contracts` (type=3) | **status=DA_DUYET=1** (khác 4 loại kia!) | ✅ |
| PLBS (type=6) | `contract_products` → `contracts` (type=6, `parent_contract_id`) | status=CO_HIEU_LUC=6 | ✅ |

"Chưa xuất hết" = `quantity - exported_qty > 0` (cột `exported_qty` trên bảng chi tiết tương ứng).
`exporting_qty` (đang xuất dở) là accessor tính động — **không** dùng trong điều kiện khóa (chỉ cần "đã xuất hết").

## 5. Quyết định ĐÃ CHỐT (user chốt 2026-11-25)

1. **"Đang trong tiến trình" = phiếu chưa kết thúc.** Em tự tra terminal từ gốc → **nguyên tắc đồng nhất:**
   KẾT THÚC mọi phiếu = {Hủy, Không duyệt, Đã hạch toán, Đã nhập/xuất kho hoàn tất, Đã quyết toán}.
   Mọi status khác = đang tiến trình → chặn. (Đã áp vào bảng §4.2/§4.3, không còn ⚠️.)
2. **PXH (đã xuất, `product_exports`) KHÔNG tính** vào chặn — hàng đã rời kho.
3. **"Đã hạch toán" = kết thúc → không chặn** (áp cho YCNH=5, ĐNNK=4, PXK=1, và mọi phiếu có trạng thái này).
4. **Phạm vi hợp đồng: CHỈ 5 HĐ ERP** đúng vé (vật tư type1 · HDDV · HDDA · HĐNT type3 · PLBS type6).
   KHÔNG quét HĐ HRM-native (`firm_contract`/`wr_service_contract`/`hrm_contract`).
5. **Ranh giới "đã chuyển tiếp"** (luồng mua): DA_DUYET(root=4)/DA_LAP_HOP_DONG(inland=5)/DA_TONG_HOP(or2=4)
   = đã kết thúc ở luồng mua (đã chuyển sang phiếu/HĐ sau, mà phiếu/HĐ sau vẫn bị check riêng) → tránh chặn trùng.
6. **Câu thông báo HĐ** (vé không ghi): "Hàng đang trong hợp đồng chưa xuất hết" (đề xuất — user chưa phản đối).

> Thứ tự kiểm & 1 câu báo: `firstBlockingFlow()` kiểm mua → nhập → xuất → HĐ, **dừng ở luồng đầu tiên vướng**,
> trả đúng 1 câu theo luồng đó (ruling: chỉ báo luồng đầu hit).

## 6. Non-goals
- Không đổi FE màn DM hàng hóa (nút Khóa đã có; chặn trả 422 hiện toast sẵn).
- Không đụng các service đang chạy (`IncomingStockService`, `PrepickStockService`) — chỉ đọc tham chiếu, không sửa.
- Không mở rộng sang xóa cứng / chuyển kinh doanh (dù service mới có thể tái dùng sau).

## 7. Việc còn lại trước khi code
- **User duyệt design** (HARD-GATE) — các mục §5 đã chốt, status map đã trace tới gốc blade/const (hết ⚠️
  trừ 1 dòng legacy `order_request2`).
- Khi lên plan, mỗi phiếu thành 1 task kiểm chứng trước khi query:
  - Xác minh cột `company_id` tồn tại trên từng bảng header (scope theo `CurrentCompany::id()`).
  - Kiểm index `product_id` trên các bảng chi tiết (tránh full-scan khi EXISTS).
  - Xác minh `order_request2` (legacy tiếp nhận/tổng hợp) còn dữ liệu trong DB gộp không + map trạng thái;
    không còn thì bỏ khỏi luồng mua.
  - Xác minh tên cột `exported_qty` / `quantity` trên từng bảng chi tiết HĐ (§4.4) và `STATUS_PROCESING`
    của `ProductExportRequest`.
