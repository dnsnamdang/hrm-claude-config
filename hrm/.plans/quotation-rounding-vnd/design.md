# Làm tròn báo giá theo tiền tệ — Design (tóm tắt)

> Phụ trách: @dnsnamdang · Branch: `tpe-develop-assign` · FE-only
> Màn: Quản lý dự án TKT → Quản lý báo giá — Tạo mới / Cập nhật (báo giá độc lập type=2 + từ BOM type=1).

## Mục tiêu
Trường "Làm tròn" + toàn bộ giá trị tiền tự động theo Loại tiền tệ của báo giá:
- **VNĐ**: khoá **"Số nguyên (0)"**, dropdown disabled, tooltip "Đồng VNĐ mặc định làm tròn đến số nguyên".
- **Tiền không phần lẻ** (JPY/KRW…): mặc định "Số nguyên (0)" nhưng **vẫn cho đổi**.
- **Tiền có phần lẻ** (USD/EUR…): mặc định "Mặc định (tối đa 2 số lẻ)", chọn tự do.

## Hiện trạng nền
- `roundingMode` (data) ↔ `quotations.rounding_mode` (tinyint nullable -3..2; null=2 số lẻ). Migration `2026_06_10_000001` đã có.
- `roundingPrecision` = `roundingMode!=null ? parseInt : 2` → điều khiển `formatMoney` (thành tiền/thuế/tổng) + roll-up + precision ô nhập. Làm tròn ở **FE**; BE chỉ lưu `rounding_mode`.
- Currency màn edit **read-only** (set lúc tạo theo dự án; chỉ đổi được khi tạo mới — xem feature `quotation-currency-editable`).

## Các phase & quyết định
| Phase | Nội dung |
|---|---|
| **P1** | VNĐ → ép `roundingMode='0'` + disable dropdown + tooltip. Khác → null (2 số lẻ), enabled. Tái dùng `roundingPrecision` cho tính toán (KHÔNG đụng công thức). Init theo currency ở loadDetail/selectProject/initCreateMode + watcher `currencyCode`. |
| **P2** | Fix ô NHẬP chưa làm tròn: thêm prop `precision` cho `V2BaseCurrencyInput` (Assign-only) — làm tròn theo precision, precision=0 chặn nhập thập phân, reformat khi đổi tiền. Wire `:precision="roundingPrecision"` vào 16 ô TIỀN (₫); KHÔNG áp ô % (VAT/CK%). |
| **P3** | **BUGFIX nhận diện VNĐ**: mã VNĐ trong ERP `currencies` là **'VNĐ'** (ký tự đ), rate=1 — KHÔNG phải 'VND'. `isVndCurrency` chuẩn hoá `toUpperCase().replace(/Đ/g,'D') === 'VND'` (edit.vue + index.vue view). Print đã tự xử lý 'VNĐ'. |
| **P4** | Tinh chỉnh non-VNĐ: (1) đổi giữa 2 ngoại tệ CÓ phần lẻ (USD↔EUR) → **giữ** lựa chọn làm tròn; (2) tiền KHÔNG phần lẻ (`zeroDecimalCurrencyCodes=['JPY','KRW','KWR']`) → mặc định "Số nguyên (0)" nhưng vẫn cho đổi. Thêm `isZeroDecimalCurrency` + `currencyDefaultRounding`. |

## Ma trận hành vi cuối
| Loại tiền | Mặc định làm tròn | Select | Ô nhập | Đổi tiền giữ lựa chọn? |
|---|---|---|---|---|
| VNĐ | Số nguyên (0) | **khoá** | số nguyên | luôn 0 |
| JPY/KRW | Số nguyên (0) | mở | số nguyên | về 0 khi chọn |
| USD/EUR… | 2 số lẻ | mở | 2 số lẻ | USD↔EUR giữ; từ VNĐ/JPY sang → 2 số lẻ |

## Phạm vi & file
- **FE-only**, không migration/permission/BE (BE đã lưu `rounding_mode`, `between:-3,2` gồm 0).
- `pages/assign/quotations/_id/edit.vue` (create.vue `extends`): `isVndCurrency`/`isZeroDecimalCurrency`/`currencyDefaultRounding`/`roundingPrecision`, watcher `currencyCode`, init ở loadDetail/selectProject/initCreateMode/handleChangeCurrency, template disable+tooltip+precision.
- `components/V2BaseCurrencyInput.vue` (Assign-only): prop `precision` + format/parse/onInput.
- `pages/assign/quotations/_id/index.vue` (view): `isVndCurrency` chuẩn hoá + dòng tỷ giá.

## Chờ E2E (user)
Build FE → VNĐ khoá 0 + ô tiền số nguyên + ẩn tỷ giá; JPY mặc định 0 (đổi được); USD 2 số lẻ + tỷ giá; USD↔EUR giữ lựa chọn làm tròn; thành tiền/thuế/tổng khớp.
