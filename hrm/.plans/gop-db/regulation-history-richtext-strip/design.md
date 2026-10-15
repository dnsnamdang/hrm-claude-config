# Quy chế – Lịch sử "Điều khoản báo giá" hiển thị CODE (HTML thô) — Fix

Nhánh `gop_db`. Bug do tester báo trên màn "Khai Quy chế – Cấu hình", tab **Báo giá – Hợp đồng**.

## Triệu chứng
Cột "Nội dung thay đổi" trong bảng **Lịch sử thay đổi** của các trường **Điều khoản báo giá**
hiển thị nguyên thẻ HTML (vd `<p>Giá trên đã bao gồm VAT…</p>`) thay vì chữ sạch.
Ảnh: https://prnt.sc/90cI6hZHUF6C

## Root cause (đã trace)
Các trường soạn thảo (FE dùng `rich()` = editor Quill/CKEditor) lưu **HTML thô** vào
`configs.*` / `companies.*`:
- tab `baogia`: `quotation_footer`, `service_quotation_footer` (store=config)
- tab `dieukhoan`: `quotation_footer_company`, `payment_term_company` (store=company)

Registry khai `type => 'string'`. BE `RegulationConfigService::formatHistoryValue()` với
type=string rơi vào nhánh `return (string) $raw;` → trả nguyên HTML. FE
`RegulationConfigScreen.vue` render cột lịch sử bằng `{{ r[2] }}` (escaped) → thấy code.

Chuỗi lịch sử là 1 dòng tóm tắt gộp nhiều field bằng `; ` và `→`, KHÔNG thể v-html
(trộn markup nhiều field). Biểu diễn đúng của 1 giá trị HTML trong tóm tắt = **văn bản thuần**.

Ảnh hưởng 2 đường dựng nội dung lịch sử:
- `formatDiffList()` (RegulationConfigHistory.diff, store=config) — đường của tab baogia.
- `historyCompanyRegulation()` (company_regulation_histories, store=company) — đường tab dieukhoan.

## Hướng fix (chỉ ở tầng HIỂN THỊ, KHÔNG mutate dữ liệu)
1. Registry: đánh dấu 4 trường rich bằng cờ `'rich' => true` (GIỮ `type => 'string'` để
   validation/lưu không đổi — switch rule ở `ScheduleRegulationVersionRequest` dựa vào `type`).
2. Service: thêm helper `richToPlainText()` (thay mọi thẻ bằng khoảng trắng → decode entity →
   gộp khoảng trắng → trim); `formatHistoryValue()` nhận thêm cờ `$rich`; 2 caller truyền cờ:
   - `formatDiffList`: `!empty($fields[$key]['rich'])`.
   - `historyCompanyRegulation`: tra cờ rich theo field_name (map từ registry, giống `companyFieldType`).

Cột giá trị công ty/config trong DB vẫn giữ HTML (bản in/preview vẫn render đẹp); chỉ dòng
tóm tắt lịch sử được strip. Fix ở display → mọi dòng lịch sử CŨ lẫn MỚI đều sạch ngay.

## Quyết định đã chốt
- KHÔNG đổi `type` sang 'richtext' (sẽ vỡ rule validate → fallback integer, chặn lưu điều khoản).
- KHÔNG strip ở tầng lưu (`buildDiffSnapshot`): sẽ chỉ sạch bản ghi MỚI, dòng cũ vẫn code; và
  đó là mutate biểu diễn đã lưu. Strip ở display an toàn + phủ cả lịch sử cũ.
- Phạm vi: chỉ sửa hiển thị bảng "Lịch sử thay đổi". (Hàng đợi "Phiên bản đã hẹn" đọc
  `diff_snapshot` trực tiếp trên FE — hiện chưa có báo lỗi; theo dõi riêng, không gộp vào fix này.)
