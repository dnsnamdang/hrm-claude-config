# Hỗ trợ nhập phân số cho hệ số quy đổi đơn vị — Tóm tắt

## Mục tiêu
Cho phép user nhập hệ số quy đổi (conversion_factor) dạng phân số (VD: "1/3", "2/5") thay vì chỉ số thập phân. Đổi kiểu dữ liệu DB từ `float` sang `string`.

## Scope
- Đổi column `conversion_factor` trong `product_package_informations` sang `string(50)`
- Tạo helper `parseConversionFactor()` để parse "1/3" → 0.333333
- Cập nhật tất cả các điểm tính toán sử dụng conversion_factor: parse trước khi tính
- Cập nhật FE input từ `type="number"` → `type="text"` + validate format
- Giữ nguyên `product_unit_prices.coefficient` là `float` (lưu giá trị đã parse)

## Quyết định lớn
- **Lưu nguyên chuỗi user nhập** ("1/3") trong DB → khi edit hiển thị lại đúng
- **Mọi phép tính số học** đều gọi helper parse trước
- **Data cũ** (float) tự động tương thích vì helper parse cũng handle số thập phân thường

## Spec chi tiết
Xem: `docs/superpowers/specs/2026-04-16-fraction-conversion-factor-design.md`
