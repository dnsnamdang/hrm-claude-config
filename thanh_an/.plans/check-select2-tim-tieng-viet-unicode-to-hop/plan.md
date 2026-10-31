# Check: Gõ "Lào cai" ở ô Tỉnh/Thành phố (màn HĐ) — máy này ra, máy kia không ra

> @khoipv — 30/10/2026

## Câu hỏi
Màn `contract/contract`, bộ lọc Tỉnh/Thành phố: qua UltraViewer gõ "Lào cai" thì ra kết quả, nhưng chính người dùng máy đó tự gõ "Lào cai" thì không ra.

## Kết luận (chưa sửa code)
- Ô lọc là `base-select2` (`hrm-thanhan-client/pages/contract/contract/index.vue:33`) → `components/BaseSelect2.vue` bọc `v-select2-component`, **không có matcher riêng** → dùng matcher mặc định của Select2, lọc hoàn toàn ở FE (option tải sẵn từ `category/customer_provinces`, `index.vue:894`).
- Matcher mặc định của Select2 bỏ dấu bằng bảng tra ký tự **dựng sẵn** (à → a). Ký tự **tổ hợp** (a + dấu huyền rời U+0300) không có trong bảng → không bỏ được dấu → chuỗi gõ không khớp tên tỉnh.
- Máy kia gõ tiếng Việt ra **Unicode tổ hợp** (Unikey/EVKey chọn bảng mã "Unicode tổ hợp", hoặc bàn phím Vietnamese cũ của Windows). Gõ qua UltraViewer thì ký tự do bộ gõ của máy mình sinh ra (Unicode dựng sẵn) nên khớp.
- Không phải lỗi dữ liệu / BE.

## Hướng xử lý
- [ ] Ngay: máy kia đổi bảng mã bộ gõ sang **Unicode** (dựng sẵn) → kiểm lại.
- [ ] (Tuỳ chọn, cần user duyệt vì sửa hàm dùng chung) Thêm matcher cho Select2 chuẩn hoá `normalize('NFC')` / bỏ dấu tổ hợp trước khi so sánh — áp dụng toàn cục (BaseSelect2, Select2 dùng trực tiếp).
