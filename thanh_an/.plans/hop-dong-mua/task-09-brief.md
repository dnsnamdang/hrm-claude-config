# Task 9 — FE: Tab Mẫu in (PrintTab)

Implementer FE (Nuxt 2 / Vue 2 / Bootstrap-Vue) tại `D:\laragon\www\dns\hrm-thanhan-client`.

Task 7/8 đã xong (form + tab hàng hóa). Task này thay nội dung `PrintTab.vue` (đang là placeholder mỏng).

## Đọc trước (BẮT BUỘC)

1. `D:\laragon\www\dns\.plans\hop-dong-mua\fe-form-contract.md` — §2 (form fields), §3 (line object keys).
2. `D:\laragon\www\dns\demos\demo-lap-hop-dong-mua.html` — port: `renderPrint`, `printParty`, `printGoodsTable`, `vnDate`, và CSS `.print-sheet`, `.print-toolbar`, `@media print` (đưa vào `<style scoped>` hoặc style thường + scope theo id vùng in).
3. `pages/supply/purchase_contracts/components/PurchaseContractForm.vue` — prop truyền vào PrintTab: `:form`, `:products`, `:companies`, `:suppliers`.

## File
- Thay nội dung: `pages/supply/purchase_contracts/components/PrintTab.vue`

## Yêu cầu

- Prop: `form` (Object), `products` (Array), `companies` (Array), `suppliers` (Array).
- Là **computed-driven** (Vue reactivity) — KHÔNG dùng innerHTML/DOM thao tác như demo. Dựng template Vue phản ánh dữ liệu `form`/`products`; mở tab là tự cập nhật theo reactivity (không cần hook shown.bs.tab).
- Bản xem trước khổ A4 (id vùng in ví dụ `print-sheet`), gồm:
  - Quốc hiệu (CHXHCN Việt Nam / Độc lập - Tự do - Hạnh phúc).
  - Tên HĐ (form.name, fallback theo loại), Số HĐ (form.number).
  - Căn cứ + "Hôm nay, ngày ... tháng ... năm ..." (port `vnDate(form.sign_time)`).
  - **BÊN MUA (Bên A):** tên = `form.main_company_name` (hoặc tên công ty đã chọn từ `companies` theo main_company_id); các dòng Địa chỉ/MST/Điện thoại/Số TK (bank_no tại bank_name)/Đại diện (main_company_representative — Chức vụ main_company_title). Port `printParty` nhưng đọc từ `form.main_company_*`.
  - **BÊN BÁN (Bên B):** tương tự đọc từ `form.supplier_*`.
  - Điều khoản HĐ: render `form.condition` (HTML rich-text) — dùng `v-html="form.condition"`.
  - Hiệu lực đến `vnDate(form.end_time)`.
  - **Bảng DANH MỤC HÀNG HÓA:** port `printGoodsTable`. Cột theo loại HĐ: Thương mại có SL mua/Thành tiền/Ghi chú; Nguyên tắc ẩn các cột đó (chỉ Mã/Tên/Quy cách/ĐVT/Hãng/Đơn giá). Mã hàng hiển thị `product_hh_code`. Thành tiền = price×order_qty. Dòng Tổng cộng (chỉ Thương mại) + "Bằng chữ" (docSo từ `@/utils/numberToWords`).
  - Chữ ký 2 bên (Đại diện Bên A/B + tên đại diện).
- Toolbar: nút "In mẫu" → `window.print()`.
- CSS `@media print`: chỉ hiện vùng `#print-sheet` (port từ demo: ẩn mọi thứ, chỉ `#print-sheet` visible, reset vị trí/khổ). Lưu ý `<style scoped>` + `@media print` với `visibility` toàn cục có thể cần style KHÔNG scoped cho phần `body *` — cân nhắc dùng 1 `<style>` thường (không scoped) cho block @media print, hoặc kỹ thuật tương đương đảm bảo chỉ in vùng hợp đồng. (Đối chiếu cách các trang khác trong client làm in nếu có; ưu tiên giải pháp chạy thật.)

## Verify
- SFC hợp lệ; import đúng. node --check phần script nếu có thể.
- KHÔNG chạy nuxt build.

## Report
Ghi `D:\laragon\www\dns\.plans\hop-dong-mua\task-09-report.md`. STATUS + file + cách xử lý @media print (scoped hay không) + concern.
