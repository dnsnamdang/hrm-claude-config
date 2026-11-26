# YC chuyển hàng — hiện tồn kho công ty khác (cross-company)

> Redmine #10783 — "[Khởi tạo] Yêu cầu chuyển hàng: NV TPE chọn kho nhưng không hiển thị tồn của kho SG"
> Fix ở **CẢ 2 bên** (ERP + HRM đã port). Tài liệu HRM tương ứng: `HRM/.plans/yc-chuyen-hang-ton-cross-company/`.

## Ý định (why)

Màn **Yêu cầu chuyển hàng** (`admin/warehouse/product_transfer_requests`) cho phép NV chọn kho để xem
tồn rồi lập yêu cầu chuyển hàng từ kho đó về. Nghiệp vụ này vốn là để lấy hàng **từ kho công ty khác**,
nên **phải hiển thị tồn của kho công ty khác**. Hiện tại chọn kho khác công ty thì cột "SL tồn" hiện "-"
dù BC "tồn kho có thể bán theo công ty" cho thấy có tồn.

## Nguyên nhân gốc (đã kiểm tới gốc + dữ liệu thật)

Dropdown "Xem tồn" liệt kê **mọi kho, không lọc công ty** (`Warehouse::getByGroupAll()`), nhưng query tồn
`ProductStockService::getStockQty()` lại **ép `accounting_warehouses.company_id = công ty người đăng nhập`**
(`$user->info->company_id`, dòng 34-36). Khi kho được chọn thuộc công ty khác:
- `$accounting_warehouse_ids` rỗng
- `Product::getAccountingStockDetail()` (dòng 2563-2568) fallback về **toàn bộ kho công ty login**
- → tính tồn cho sai công ty → `in_stock = 0` → FE hiện "-".

**Dữ liệu thật (DB local `erp_hrm_check`):** kho `SG-CSKH` (`warehouses.id=5`) → `accounting_warehouses.id=10`,
`company_id=4` (TNHH TB Tân Phát Sài Gòn). Mã `MLER-AM101663CMUX` (`products.id=7318`) tồn thật tại acc_wh 10.
NV TPE = công ty 1 → bị ép lọc công ty 1 → rớt kho 5.

BC "tồn có thể bán theo công ty" **không lỗi** vì lọc theo công ty NGƯỜI DÙNG CHỌN (`company_id`/`user_company_id`),
không ép công ty login.

## Phạm vi & cách tiếp cận (đã chốt với user — hướng "sửa HẸP")

`getStockQty` + `getAccountingStockDetail` là **hàm dùng chung ~40 màn** (báo giá, đơn hàng, ĐNXK, prepick...).
Form YC chuyển hàng dùng chung endpoint `warehouseInfo.stockOfProducts` → không được đổi hành vi chung.

**Giải pháp:** thêm **cờ opt-in** `stock_by_selected_warehouse` mà **chỉ form YC chuyển hàng gửi**:
- Khi cờ bật + có kho được chọn → `getStockQty` bỏ lọc `company_id = login`, và truyền `company_id`
  của **kho được chọn** vào `params` của `getAccountingStockDetail`.
- `getAccountingStockDetail` **KHÔNG sửa** — đã honor `params['company_id']` (dòng 2553, 2556) cho tồn/
  prepick/hold/khuyến mại.
- 40 màn khác **không gửi cờ → đi đúng nhánh cũ, byte-identical**, không ảnh hưởng.

Kho cùng công ty với user: cờ bật vẫn ra kết quả y hệt (company suy ra = công ty user). Chỉ khác ở kho
chéo công ty → đúng như BC.

## Quyết định đã chốt
- Hiện tồn kho công ty khác trên YC chuyển hàng là **đúng nghiệp vụ** (user xác nhận).
- Sửa **hẹp** bằng cờ opt-in, **không** đổi hành vi hàm tồn dùng chung cho màn khác (user chốt).
- Không đụng `getAccountingStockDetail`.

## Không làm (non-goals)
- Không đổi lọc công ty mặc định của `getStockQty`/`getAccountingStockDetail` cho các màn khác.
- Không đổi dropdown "Xem tồn" (vẫn liệt kê mọi kho như ERP gốc).
- Không commit/push (chờ yêu cầu).
