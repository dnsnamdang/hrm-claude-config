# YCHG — Bắt buộc nhập ảnh ở popup "Thêm hàng tạm"

**Chốt:** 03/11/2026 · **Nhánh:** `develop` (hrm-client + hrm-api) · **Trạng thái:** DONE (FE+BE+test+Playwright), CHƯA commit

## Yêu cầu

Màn **Yêu cầu hỏi giá (YCHG)** → popup **Thêm hàng tạm** → trường **Hình ảnh** ("Chọn ảnh") phải **BẮT BUỘC** nhập. Trước đây hàng tạm KHÔNG bắt ảnh.

## Quyết định đã chốt

1. **Phạm vi: CHỈ popup "Thêm hàng tạm" màn YCHG** (đường tạo/sửa trực tiếp qua `TempProductController` → `TempProductRequest`), cả tạo lẫn sửa.
   - **KHÔNG ép** ở bước **PTKD duyệt** hàng tạm (`PriceAskingTempProductRequest`, màn khác) — giữ hành vi cũ. Lý do: user chỉ yêu cầu ở popup YCHG; thu hẹp blast radius.
   - Cơ chế tách: thêm method `enforcesGallery()` trong `TempProductRequest` (trả `true`), subclass PTKD override `false`.
2. **Ngoại lệ giữ ảnh cũ (mirror `ProductRequest`):** sửa hàng tạm cũ chỉ có `avatar`, chưa có thư viện ảnh (`product_galleries`), không gửi ảnh mới ⇒ `keepsLegacyAvatar()` cho qua, không ép gửi lại. (Khớp FE: có `avatar` coi như đã có ảnh.)
3. **Validate ở CẢ FE lẫn BE** (quy tắc HRM 06/10/2026).
4. **Message dùng câu chuẩn**, không tự viết lại:
   - BE: `galleries.required`/`.min` kế thừa `ProductRequest::messages()` = "Vui lòng tải lên ít nhất 1 hình ảnh."
   - FE: "Bắt buộc phải tải ảnh lên".

## Thay đổi

### BE (hrm-api)
- `Modules/MasterData/Http/Requests/Product/TempProductRequest.php`
  - `rules()`: thêm `galleries => 'required|array|min:1|max:10'` khi `enforcesGallery() && !keepsLegacyAvatar()`.
  - Thêm method `enforcesGallery(): bool` (mặc định `true`).
- `Modules/MasterData/Http/Requests/Product/ProductRequest.php`
  - `keepsLegacyAvatar()` đổi `private` → `protected` (chỉ nới visibility để subclass dùng lại, không đổi hành vi).
- `Modules/MasterData/Http/Requests/Product/PriceAskingTempProductRequest.php`
  - Override `enforcesGallery(): bool` = `false` (PTKD duyệt không ép lại ảnh).

### FE (hrm-client) — đã làm phiên trước
- `pages/assign/quotations/components/QuotationProductSearchModal.vue`
  - `<ProductFormGallery :required="isYchg" ...>` (bắt buộc khi là chế độ YCHG).
  - `validateYchg()`: ảnh trống + không `avatar` ⇒ lỗi "Bắt buộc phải tải ảnh lên".
  - `clearFilledErrors()`: xoá lỗi ảnh khi đã có ảnh hoặc avatar.
  - (`applyTempServerErrors()` đã sẵn map key `galleries`/`galleries.N` của BE → hiển thị dưới khối ảnh.)

## Test

- `Modules/MasterData/Tests/Feature/TempProductApiTest.php`
  - Thêm `galleries` vào `payload()`; thêm 2 test: `thieu_anh_hang_tam_bao_422` (tạo không ảnh → 422), `sua_hang_tam_con_avatar_cu_khong_bat_gui_anh_lai` (sửa legacy-avatar → 200).
- Vá fixture (thêm `galleries` cho đường tạo/sửa YCHG): `TempProductScreenTest::payload()`, `PriceAskingTempProductTest::form()` ($base, cho đường sửa trực tiếp `TEMP_URL`).
- **Kết quả:** TempProductApiTest 20/20 · PriceAskingTempProductTest 16/16 · TempProductScreenTest 12/12 · TempProductVisibilityTest 7/7 · ProductCopyApiTest 28/28 — **tất cả xanh**.

## Playwright

`http://127.0.0.1:3000/sale/price-asking-requests/add` → Thêm hàng tạm → Lưu (trống): trường **Hình ảnh** có dấu `*`, báo đỏ "Bắt buộc phải tải ảnh lên", popup không đóng, không gọi API, toast "Vui lòng kiểm tra lại dữ liệu nhập". ✓
