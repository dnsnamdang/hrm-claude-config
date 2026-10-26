# Giá 0 = "chưa tính giá" + cảnh báo khi chọn hàng ở Báo giá — Thiết kế

**Ngày:** 2026-10-23 · **Repo:** hrm-api, hrm-client, ERP TanPhatDev (nhánh `gop_db`)
**Trạng thái:** đã chốt nội dung, CHƯA được phép code (chờ user cho phép rõ ràng + phạm vi).

## Mục đích
Thay quy ước cũ "giá Bán lẻ 1 đ = chưa có giá" bằng giá **0**. Không có mặt hàng nào thực sự bán giá 0.
Người dùng phải nhập được 0 ở các luồng cập nhật giá. Khi sale chọn một hàng chưa tính giá vào báo giá,
hệ thống phải hỏi lại trước khi thêm.

## Chốt với user (23/10/2026)
1. Giá 0 thay quy ước 1 đ. **Dữ liệu 1 đ cũ để nguyên**, không chạy lệnh đổi 1 đ → 0.
2. Mở giá 0 **chỉ cho các ô giá bán**. Giá NCC và tỷ giá vẫn phải > 0.
3. Nhập giá 0 thì **bỏ qua luật sàn** "không thấp hơn giá công ty quản lý" (`OwnerPriceFloor`).
4. Cảnh báo bật khi giá **≤ 1 đ HOẶC hàng chưa có dòng giá** (null).
5. Câu cảnh báo: **"Hàng chưa tính giá bán, xác nhận vẫn chọn mã hàng này?"**
6. Chọn nhiều hàng mà có mã chưa tính giá: hiện 1 cảnh báo liệt kê các mã đó. Bấm **Không** thì bỏ riêng
   các mã chưa tính giá, **vẫn thêm phần còn lại**.
7. Phạm vi cảnh báo:
   - HRM: Báo giá `/assign/quotations` · Báo giá dịch vụ CSKH `/customer-care/wr-quotations`
   - ERP: Báo giá firm · Báo giá dự án · Báo giá dịch vụ sale · Báo giá dịch vụ CSKH
   - KHÔNG làm: Hợp đồng (dòng hàng kế thừa từ báo giá, không có popup chọn), Báo giá mẫu ERP,
     Báo giá thanh lý ERP, Báo giá thường ERP

## Phần A — Cho nhập giá bán 0

| Luồng | Hiện trạng | Việc cần làm |
|---|---|---|
| Phiếu tính giá HRM `/finance/price-calculates` | Gửi duyệt / Lưu & duyệt chặn `<= 0` ở 5 loại giá bán | FE `PriceCalculateForm.vue:~498` + BE `PriceCalculateWriter.php:~683` (`prices.{type}.price`) đổi thành `< 0`. GIỮ chặn ở giá NCC (`:617`, mixin `priceInputRowsMixin.js:130`) và tỷ giá |
| Cập nhật giá bán `/finance/product-prices` | `min:0`, đã nhận 0 | Chỉ phần sàn giá (dưới) |
| Duyệt giá bán `/finance/product-price-approvals` | chỉ chặn `< 0` | Chỉ phần sàn giá |
| Yêu cầu tính giá | chỉ có giá NCC | Không đổi |
| ERP | mọi đường ghi giá đã khoá, chuyển sang HRM | Không đổi |

**Sàn giá công ty quản lý:** `OwnerPriceFloor` (dùng ở `ProductPriceUpdateService`, `ProductPriceApprovalService`,
`PriceCalculateWriter`). Giá mới = 0 thì bỏ qua kiểm sàn. Giá mới > 0 thì giữ luật cũ. Luật sẵn có
"giá công ty quản lý ≤ 1 đ coi như chưa có giá ⇒ bỏ sàn" giữ nguyên.

## Phần B — Cảnh báo khi chọn hàng chưa tính giá

**Điều kiện "chưa tính giá"** (một chỗ định nghĩa mỗi stack): `price == null || price <= 1`. Giá xét là
**giá theo loại giá của chính phiếu báo giá**, đúng con số popup đang hiện (`row.price` / `units[].price`).

**HRM**
- Báo giá: chèn bước kiểm vào `QuotationProductSearchModal` (`applySelection` / `onPickerQuickPick`), chỉ bật khi
  modal mở từ màn báo giá (prop mới, mặc định tắt). BOM, phiếu kho và Hỏi giá dùng chung modal nhưng không đổi.
- Báo giá dịch vụ CSKH: chèn vào `WrQuotationForm.vue` `onPickProducts` (giá lấy từ `line-info` `sell_price`).
- Dùng `this.$confirm(...)` (`base-confirm-modal`) theo chuẩn HRM, không dùng `msgBoxConfirm`.

**ERP**
- Điểm chung: `cfg.onPick` trong `searchProductQuotationJs.blade.php:~66`, thêm cờ cấu hình bật cảnh báo.
  Chỉ 4 màn trong phạm vi được bật cờ; thanh lý và báo giá thường để tắt. Dùng `swal` như các màn báo giá ERP.
- Chọn nhiều: `chooseProducts(ids)` chỉ nhận id, nên phải lấy giá từ dòng tìm kiếm (`row.price`) hoặc từ `/items`
  trước khi gọi `addProduct`.

**Popup chọn hàng HRM:** nhãn "Chưa có giá" hiện đang chỉ bật khi không có dòng giá (`has_price = price > 0`).
Nới thành ≤ 1 đ cho khớp điều kiện cảnh báo (*mình tự chọn*).

## Không làm
- Không đổi dữ liệu 1 đ cũ. Không đổi luật Khôi phục hàng khoá (`ProductRestoreRule` đã coi Bán lẻ ≤ 1 đ là chưa có giá).
- Không đổi giá NCC, tỷ giá. Không đổi Hợp đồng, Báo giá mẫu, thanh lý, báo giá thường ERP.
- Không đổi cảnh báo 0 đ lúc Gửi duyệt báo giá HRM (`baogia-warning-zero-price`, đã có).

## Kiểm thử
- PHPUnit: PTG nhận giá bán 0, vẫn chặn giá NCC 0; sàn giá bỏ qua khi 0 ở cả 3 service; `OwnerPriceFloorApiTest`, `PriceCalculateApiTest`.
- Playwright (bắt buộc vì có FE): mỗi màn trong phạm vi chọn 1 mã ≤ 1 đ, 1 mã chưa có giá, 1 mã có giá; chọn nhiều
  rồi bấm Không ⇒ đo số dòng thêm vào bảng; màn ngoài phạm vi (BOM, báo giá thường ERP) không có cảnh báo.
