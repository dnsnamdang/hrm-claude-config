# Task 9 — Report: Tab Mẫu in (PrintTab)

## STATUS: DONE

## File thay đổi
- `hrm-thanhan-client/pages/supply/purchase_contracts/components/PrintTab.vue` — thay placeholder bằng bản xem trước hợp đồng khổ A4 + nút In.

## Đã làm
- **Computed-driven (Vue reactivity)** — KHÔNG dùng innerHTML/DOM như demo. Toàn bộ nội dung dựng bằng template + computed; mở tab tự cập nhật theo `form`/`products` (không cần hook `shown.bs.tab`).
- Đọc dữ liệu từ prop `form.main_company_*` / `form.supplier_*` (KEY BE). Mã hàng hiển thị `product_hh_code`; tên = `product_name (+ product_trade_name)`.
- Bố cục A4 (`id="print-sheet"`): Quốc hiệu → Tên HĐ (fallback theo loại nếu trống) → Số HĐ → Căn cứ + "Hôm nay, {vnDate(sign_time)}, chúng tôi gồm:" → BÊN MUA (Bên A) → BÊN BÁN (Bên B) → điều khoản `v-html="form.condition"` → dòng hiệu lực `vnDate(end_time)` → bảng DANH MỤC HÀNG HÓA → Bằng chữ (docSo) → chữ ký 2 bên.
- **Party rows** (port `printParty`): Địa chỉ / MST / Điện thoại / Số TK (`bank_no` tại `bank_name`) / Đại diện (`representative` — Chức vụ: `title`), lọc bỏ dòng rỗng.
- **Tên bên**: ưu tiên snapshot `*_name`, fallback tra `companies`/`suppliers` theo `main_company_id`/`supplier_id`.
- **Bảng theo loại HĐ**: Thương mại (type=2) có cột SL mua / Thành tiền / Ghi chú + dòng Tổng cộng + "Bằng chữ". Nguyên tắc (type=1) ẩn các cột đó (chỉ Mã/Tên/Quy cách/ĐVT/Hãng/Đơn giá) + dòng ghi chú "Đơn giá đã gồm VAT...".
- Thành tiền = `price × order_qty`; Tổng = Σ thành tiền; Bằng chữ dùng `docSo` từ `@/utils/numberToWords`.
- Toolbar: nút "In mẫu" (`b-button`) → `window.print()`.

## Cách xử lý @media print (concern chính của brief)
Dùng **1 khối `<style>` KHÔNG scoped** (không có scoped) cho toàn bộ CSS bản in.
- Lý do: block `body *{ visibility:hidden }` + `#print-sheet, #print-sheet *{ visibility:visible }` cần selector toàn cục — với `<style scoped>` Vue gắn attribute `[data-v-xxx]` nên `body *` không match, và nội dung `v-html` (điều khoản) cũng không nhận style scoped. Non-scoped giải quyết cả 2.
- **Chống rò rỉ ra toàn app**: mọi selector trình bày đều namespace dưới `.print-tab` / `.print-tab .print-sheet`; phần `@media print` chỉ target `#print-sheet` (id duy nhất) và chỉ kích hoạt khi in. Rủi ro va chạm CSS toàn cục ở mức thấp.

## Verify
- `node --check` phần `<script>` (đã strip import): PASS.
- KHÔNG chạy nuxt build (theo ràng buộc).

## Concern / lưu ý
1. **id `print-sheet` là toàn cục** — nếu sau này có nhiều instance PrintTab render đồng thời trên cùng 1 trang (hiếm, vì form chỉ có 1) thì id trùng. Hiện tại chỉ 1 form/trang nên an toàn.
2. `vnDate` đã làm robust: cắt 10 ký tự đầu (`slice(0,10)`) rồi split `-`, phòng khi BE trả `YYYY-MM-DD HH:mm:ss`. base-date-picker mặc định `value-type=YYYY-MM-DD` nên trường hợp thường là chuỗi ngày thuần.
3. Điều khoản render qua `v-html` — dữ liệu là rich-text nội bộ (seed/CKEditor), không phải input người ngoài; đã thêm comment `eslint-disable` cho rule `vue/no-v-html`.
4. Chưa chạy được trên trình duyệt thật trong task này (không build); nên kiểm thị giác + thử In khi chạy client dev.
