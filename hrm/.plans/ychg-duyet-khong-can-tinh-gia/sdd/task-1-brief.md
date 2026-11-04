# Task 1 — Trạng thái dòng `9` + maps + audit reader

Repo: `hrm-api` (Laravel 8 / PHP 7.4, `Modules/MasterData`). Work on branch `develop`.

## Global Constraints (bind every task)
- Dữ liệu nhạy cảm (giá vốn/giá nhập) gate server-side, không chỉ ẩn FE.
- Badge màu + text do BE quyết (`company_status_text`/`company_status_color`); dùng đúng bộ mã màu chuẩn HRM (9 mã), KHÔNG chế mã mới.
- Số en-US. Không đổi luồng dòng Đồng ý (1/7) và Từ chối (8).

## Files
- Modify: `Modules/MasterData/Entities/Product/ProductCompany.php` (hằng trạng thái ~dòng 23-33, STATUS_TEXT ~39-48, STATUS_COLOR ~50-59)
- Test: `Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php` — nếu file này đã tồn tại thì THÊM test vào đó; nếu đã có file test đơn vị khác cho entity này (grep `ProductCompany` trong `Modules/MasterData/Tests`), thêm vào file sẵn có thay vì tạo trùng. Nếu không có, tạo file này (DatabaseTransactions không bắt buộc — test này thuần hằng số, không chạm DB).

## Interfaces — Produces (các task sau phụ thuộc)
- `ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE = 9`
- `ProductCompany::isTemp(9) === true`
- `STATUS_TEXT[9]`, `STATUS_COLOR[9]` tồn tại và không rỗng.

## Bối cảnh trạng thái hiện có (ĐỌC để khớp phong cách, đừng đổi)
- 1=Đang nhập thông tin, 2=Chờ tính giá (STATUS_WAITING_PRICE), 3=STATUS_TRADING (Đang kinh doanh), 4=Ngừng KD, 5=STATUS_PRICING, 6=STATUS_TEMP (hàng tạm chờ), 7=STATUS_TEMP_APPROVED (đồng ý), 8=STATUS_TEMP_REJECTED (từ chối).
- `TEMP_STATUSES = [6,7,8]`, `PRICING_FLOW_STATUSES = [2,5]`.
- `STATUS_COLOR` hiện có: TRADING→`#16A34A`, TEMP→`#6D5A9E`, TEMP_APPROVED→`#7C3AED`, TEMP_REJECTED→`#DC2626`.
- `isTemp(?int $status): bool` = `in_array($status, self::TEMP_STATUSES, true)`.

## Steps (TDD)

**Step 1 — Viết test** (thêm vào file test entity):
```php
public function test_no_price_status_is_temp_and_has_badge(): void
{
    $this->assertSame(9, ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE);
    $this->assertTrue(ProductCompany::isTemp(ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE));
    $this->assertArrayHasKey(9, ProductCompany::STATUS_TEXT);
    $this->assertArrayHasKey(9, ProductCompany::STATUS_COLOR);
    $this->assertNotSame('', trim((string) ProductCompany::STATUS_TEXT[9]));
}
```

**Step 2 — Chạy test, xác nhận FAIL** (`Undefined constant` / key thiếu).
`php artisan test Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php` (hoặc file bạn chọn).

**Step 3 — Thêm hằng + maps**:
- `const STATUS_TEMP_APPROVED_NO_PRICE = 9;` (sau hằng status 8).
- Thêm `9` vào `TEMP_STATUSES` → `[6,7,8,9]`.
  - Lý do: dòng `9` TRƯỚC khi Duyệt phiếu vẫn là hàng tạm chưa kinh doanh — phải ẩn khỏi catalog/picker như 6/7/8; `isTemp(9)=true` cho phép PTKD mở lại form đổi quyết định và hiện controls hàng tạm. Sau promote → `3` tự hết ẩn.
- `STATUS_TEXT[9] = 'Duyệt không cần tính giá'`.
- `STATUS_COLOR[9] = '#7C3AED'` (dùng lại mã nhóm "chốt" của TEMP_APPROVED — thuộc 9 mã chuẩn; KHÔNG tạo mã mới).
- Nếu có `STATUS_TEXT`/màu ở nơi khác (vd `INFO_STATUS_TEXT` dòng ~69) KHÔNG cần thêm 9 trừ khi reader đòi.

**Step 4 — AUDIT mọi reader của `product_company_coefficients.status`** (BẮT BUỘC — đây là Review Focus số 1):
- Grep trong `Modules/`: `product_company_coefficients`, `company_status`, `STATUS_TEXT`, `STATUS_COLOR`, `TEMP_STATUSES`, `PRICING_FLOW_STATUSES`, `isTemp`, `excludeTempOnly`.
- Với MỖI reader: xác nhận `9` được map đúng (badge có text/màu) và không rơi vào nhánh "không xác định"/badge trống. Đặc biệt kiểm: màn "Trạng thái HH công ty quản lý" (Kho dữ liệu), list sản phẩm, các filter trạng thái.
- Nếu một reader cần loại/giữ `9` riêng (vd filter "Đang kinh doanh" KHÔNG được lẫn `9`) thì sửa tại reader đó.
- Nếu phát hiện `9` đã bị dùng cho ý nghĩa khác ở đâu đó → đổi hằng mới sang giá trị trống kế tiếp (ví dụ `9` thực đã dùng thì lấy số chưa dùng), cập nhật test + brief-note trong report.
- Ghi DANH SÁCH reader đã kiểm + kết luận vào report.

**Step 5 — Chạy test, xác nhận PASS.**

**Step 6 — Commit** (trên `develop`):
`feat(ychg): add product status 9 (approved-no-price) + badge maps`
Kết thúc message bằng dòng: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Ghi report đầy đủ vào file report (đường dẫn trong dispatch). Trả về CHỈ: status (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED), commit hash(es), 1 dòng tóm tắt test, và concerns (nếu có — nhất là kết quả audit nếu phát hiện reader cần sửa). KHÔNG dispatch subagent nào khác.
