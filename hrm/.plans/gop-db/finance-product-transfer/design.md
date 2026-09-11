# Design — Port màn **Phiếu điều chuyển hàng** (ERP → HRM)

**Người phụ trách:** @junfoke — 2026-09-04
**Nhánh:** `feat/finance-product-transfer` (hrm-api + hrm-client, tách từ `gop_db`)
**Khảo sát chi tiết:** [khao-sat.md](./khao-sat.md) — đọc trước, tài liệu này chỉ tóm tắt quyết định.

---

## 1. Mục tiêu

Đưa màn ERP **Kho → Điều chuyển → Phiếu điều chuyển hàng** (`Warehouse\ProductTransfersController`,
bảng `product_transfers`, mã `PDCH-`) sang HRM tại **Tài chính → Điều chuyển → Phiếu điều chuyển hàng**
(`/finance/product-transfers`), dùng chung bảng trên DB gộp (309 phiếu đã có, không migration bảng chính).

**Nghiệp vụ giữ nguyên ERP:** chuyển hàng giữa 2 **kho kế toán** trong cùng 1 **kho vật lý**.
2 trạng thái — *Đang tạo* → *Đã hạch toán*; hạch toán là trừ/cộng `accounting_stocks`, ghi
`accounting_stock_logs` (giá vốn FIFO) và bút toán Nợ 156 / Có 156. Hạch toán rồi khoá vĩnh viễn.

---

## 2. Quyết định đã chốt với user (2026-09-04)

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Nhãn menu trùng với màn *Phiếu yêu cầu chuyển hàng* | **Đã xử lý xong**: trả màn cũ về nhóm *Xuất hàng* đúng tên ERP; mục *Phiếu điều chuyển hàng* ở nhóm *Điều chuyển* để dành cho màn này |
| 2 | 13 lỗi/bất thường của ERP | **Sửa theo chuẩn HRM** — bảng §3 |
| 3 | Tách 2 method FIFO khỏi `WarehouseExportAccountingService` | **Duyệt**, điều kiện: *không ảnh hưởng màn đang chạy và màn port sau* → §4 |
| 4 | Lịch sử thao tác (ERP **không có**) | **CÓ** — làm mới theo skill `entity-history`, §5 |
| 5 | Huỷ phiếu / đảo bút toán | **KHÔNG** — ERP không có thì thôi |

---

## 3. Sửa theo chuẩn HRM — 13 điểm

**Nhóm A — bảo mật & đúng đắn dữ liệu (bắt buộc sửa):**

| ERP | HRM |
|---|---|
| Phạm vi quyền chỉ áp khi `?type=all`; vào URL trần thấy phiếu mọi công ty | Áp phạm vi quyền **vô điều kiện** trong `searchByFilter`, không phụ thuộc tham số |
| `store`/`update` không gate quyền (chỉ màn `create` chặn `can('Kế toán kho')`) | Gate ở **cả** `store`/`update`/`destroy` bằng `canCreate()`/`canEdit()` trên Entity (KHÔNG dùng middleware `checkPermission` — guard `web` vs `api`, §6) |
| `status` nhận thẳng từ request, không validate | `required|integer|in:1,2` trong FormRequest |
| `export_price` không reset giữa các vòng lặp → dòng `qty = 0` ăn giá dòng trước | Khởi tạo lại mỗi dòng, `qty = 0` → `export_price = 0` |
| `$product->data` (accessor hỏng trên `gop_db`) | Tự chọn field cần, không dùng accessor |

**Nhóm B — trải nghiệm & rule team:**

| ERP | HRM |
|---|---|
| Bộ lọc **Kho**, **Mã hàng hoá**, **Tên hàng hoá**, **khoảng ngày** khai trên UI nhưng BE bỏ qua | **Làm cho chạy thật** — BE xử lý đủ; verify bằng tab Network |
| Bộ lọc **Người duyệt** | **Bỏ hẳn** — màn này không có khái niệm người duyệt, giữ lại là ô lọc chết |
| Setter `qty` tự kẹp về `in_stock` | **Báo đỏ**, không tự sửa giá trị người nhập ([[feedback_validate_khong_tu_sua_gia_tri_nhap]]) |
| `qty` rule `min:1` (chặn cả số lẻ dù cột `decimal(12,2)`) | `gt:0` — cho số lẻ |
| Dropdown kho kế toán lúc mở Sửa/Xem nạp **toàn bộ kho mọi công ty, cả kho đã khoá** | Luôn lọc `company_id` + `status = 1` + `warehouse_id`; kho đã khoá đang gắn với phiếu vẫn hiện (🔒) |
| Xoá phiếu không dọn file S3; `delete()` trả redirect kiểu web | Dọn file đính kèm; trả JSON |
| Badge *Đang tạo* = `danger` (ĐỎ) | **XÁM** — nháp/đang tạo theo bảng màu SRS |

**Giữ nguyên (là nghiệp vụ ERP, không phải lỗi):**

- TK nợ / TK có cứng `156` trên form, bản in và bút toán — đúng bản chất chuyển kho nội bộ.
- Không port nút *"Tạo phiếu điều chuyển hàng"* từ màn `warehouseTransfer`: link chết (cột
  `warehouse_transfer_id` đã bị migration 2023-10-30 xoá), màn đó cũng không còn trong menu ERP.

**Chuẩn UI HRM áp thêm** (ERP không có): `V2BaseSmartFilterPanel` + `filterFields`, Cấu hình cột,
`filterStateMixin` nhớ bộ lọc, `ExportFieldsModal` khi xuất Excel, `V2Footer` cho nút màn chi tiết/form,
`unsavedChangesMixin`, nút không dùng được thì **ẩn** chứ không xám, ô rỗng **để trống** (không `—`),
số theo **chuẩn quốc tế `1,234,567.89`**.

> ⚠️ Skill `erp-to-hrm-screen` (checklist mục C, dòng 204-205) vẫn ghi rule CŨ: "Tiền: `.` ngăn nghìn,
> `,` ngăn thập phân" và "Ô rỗng in `—`". Hai rule này **đã bị user thay** (26/08 số quốc tế,
> 22/08 ô rỗng để trống) và `export-excel` / `print-page` / `list-page` đã cập nhật — riêng skill này
> còn sót. Màn này theo rule MỚI. Cần sửa skill (xem plan Task 0.2).

---

## 4. Hàm dùng chung

### 4a. `AccountingStockService` — dùng lại NGUYÊN TRẠNG, không sửa

`in_acc_warehouse` mà ERP thêm chỉ là `SUM(qty)` thô của kho kế toán đang chọn, **không** bị trừ
pending → service riêng của màn tự query 1 dòng rồi tự ghép
`in_stock = min(khả dụng công ty, in_acc_warehouse, in_warehouse)`.
4 màn đang gọi service không bị đụng vào. (Chi tiết: khảo sát §5 ghi chú (a).)

### 4b. Tách FIFO — điều kiện "không ảnh hưởng màn khác"

Tách 2 method private `fifoValue()` + `layerQtyPrice()` từ
`Modules/Assign/Services/WarehouseExportAccountingService` sang service dùng chung mới
**`Modules/Assign/Services/StockValueFifoService`** (đặt tên theo *chủ đề nghiệp vụ*, không theo tên màn
— skill `erp-to-hrm-screen` bước 3b).

Cam kết không ảnh hưởng, thực hiện bằng 4 ràng buộc:

1. **Cắt nguyên khối, không viết lại**: bê y nguyên thân 2 method, chỉ đổi `private` → `public` và
   chuyển 4 hằng FQN đi cùng. Không đổi tham số, không đổi kiểu trả về, không "tiện tay tối ưu".
2. `WarehouseExportAccountingService` giữ nguyên 2 method cũ dưới dạng **wrapper 1 dòng** gọi sang
   service mới → mọi caller hiện tại (`ProductExportService.php:245`) không phải sửa dòng nào.
3. **Test hồi quy màn Phiếu xuất hàng trước/sau khi tách**: chạy cùng 1 phiếu, so `export_price` từng
   dòng + `value_before`/`value_after` của log — phải khớp tuyệt đối.
4. Docblock service mới liệt kê **"Nơi đang dùng"** để màn port sau biết gọi lại thay vì chép.

`calculateExportPrice()` **không** tách: nó bám bảng `product_export_detail_accounting` (phân bổ kho
của phiếu xuất hàng), màn này không có bảng đó nên tự tính từ log của chính nó như ERP.

---

## 5. Lịch sử thao tác (mới, ERP không có)

Theo skill `entity-history` — bảng `product_transfer_history`, biến thể **subset-diff**, hiển thị
đủ **2 nơi**: popup ở màn danh sách + mục *Lịch sử* ở màn chi tiết.

Trả lời sẵn 4 câu hỏi §0 của skill (anh xem lại giúp, thấy lệch thì em sửa):

| Câu hỏi | Chốt |
|---|---|
| Track trường nào | Đúng các trường trên màn: kho vật lý, kho xuất, kho nhập, ghi chú, file đính kèm, và **bảng con chi tiết hàng hoá** (dùng *khoá dạng bảng* §3 của skill) |
| Ai được xem | Không permission riêng — vào được màn thì xem được |
| Action nào | `create` · `update` · `status` (hạch toán). Xoá không ghi (phiếu biến mất thì log vô nghĩa) |
| Bảng con dạng danh sách | **Có** — `product_transfer_details` |

Snapshot lưu **giá trị hiển thị** (tên kho, tên hàng) chứ không lưu id. Bộ lọc *Loại hoạt động* giữ
đúng 3 nhóm cố định; ô *Người thực hiện* lấy qua `App\Services\HistoryPerformerOptions`.

---

## 6. Phân quyền

Dùng lại **đúng permission ERP**, không tạo mới: `100682` *Xem phiếu điều chuyển hàng theo - tổng công ty*,
`100683` *… - công ty*, `100080` *Kế toán kho* (quyền lập phiếu). Cả 3 ở guard **`web`**.

⚠️ Middleware `checkPermission` của HRM resolve qua spatie `getAllPermissions()` nên **bỏ sót quyền
gán từ ERP** (`model_type = 'App\Employee'`) → user có quyền thật vẫn 403. Màn *Phiếu yêu cầu chuyển hàng*
đã đụng và xử lý bằng cách **không gắn middleware**, chặn bằng `canView()/canEdit()/canCreate()` tự
query pivot trên Entity. Màn này làm y hệt. ([[project_erp_permission_guard_web_vs_api]])

Phạm vi danh sách: quyền tổng công ty → tất cả · quyền công ty → cùng `company_id` · không quyền →
chỉ phiếu mình lập. Phiếu *Đang tạo* chỉ người lập thấy.

---

## 7. Phạm vi giao hàng

**BE** (`Modules/Finance`): 2 Entity + `ProductTransferService` + `ProductTransferAccountingService`
(hạch toán) + `ProductTransferHistoryService` + Controller + FormRequest + 2 Resource + ~13 route
+ 1 migration bảng lịch sử. Dùng lại: `AccountingStockService`, `StockValueFifoService` (mới tách),
`AccountDetail`, `ErpReportTemplate` (mẫu in 388/387), popup tìm hàng
`GET /v1/customer-care/services/search-products`.

**FE** (`hrm-client/pages/finance/product-transfers/`): `index.vue` · `create.vue` · `_id/index.vue`
· `_id/edit.vue` · `_id/print.vue` · `components/ProductTransferForm.vue` +
`ProductTransferHistoryModal.vue` + gắn link vào mục menu đã để sẵn.

**Không làm:** huỷ phiếu / đảo bút toán · nút tạo từ `warehouseTransfer` · sửa `AccountingStockService`.

---

## 8. Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| Màn **ghi tồn kho + ghi sổ kế toán thật** — sai là hỏng số liệu | Test trên DB local, đối chiếu `accounting_stocks` / `accounting_stock_logs` / `account_details` trước-sau với ERP chạy cùng phiếu |
| Tách FIFO làm lệch giá vốn màn Phiếu xuất hàng | 4 ràng buộc §4b, có bước test hồi quy bắt buộc |
| Sửa bộ lọc chết → kết quả khác ERP, QA tưởng lỗi | Ghi rõ trong tài liệu test case: đây là **sửa có chủ đích**, kèm đối chiếu ERP |
| `formValidateMixin` không có `setFieldError` | `$set` vào `formErrors` ([[project_formvalidatemixin_no_setfielderror]]) |

---

## 9. Liên kết

- Kế hoạch task: [plan.md](./plan.md)
- Khảo sát ERP: [khao-sat.md](./khao-sat.md)
- Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-04-finance-product-transfer-design.md` *(viết ở Phase 1)*
