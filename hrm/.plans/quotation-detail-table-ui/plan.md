# Plan — Chỉnh UI bảng chi tiết màn Tạo báo giá

Màn: Quản lý Báo giá → Tạo báo giá (`pages/assign/quotations/_id/edit.vue`, dùng chung cho create.vue).

## Phase 1 — Điều chỉnh cột + thanh cuộn ngang + header

### FE
- [x] AC1: Đặt độ rộng 3 cột "Thành tiền nhập", "Thành tiền bán", "Thành tiền sau VAT" = 130px (bằng cột "Giá nhập"); bỏ `white-space:nowrap` để text tự xuống dòng
- [x] AC2: Thêm thanh cuộn ngang phía trên bảng (`products-scroll-top` + spacer), đồng bộ 2 chiều với vùng cuộn dưới (`products-scroll`); spacer width = table.scrollWidth, cập nhật qua ResizeObserver
- [x] Header căn giữa (`text-align:center !important` để đè `.text-right` Bootstrap) + phân cách cột (`border-right`) + cho phép wrap
- [x] Wiring: `setupTopScrollbar`/`teardownTopScrollbar`/`syncTopScrollbarWidth`/`onTopScrollbarScroll`/`onBodyScrollbarScroll` trong mounted/beforeDestroy

## Phase 2 — Nới rộng cột tiền cho dễ đọc (2026-07-08)

### FE
- [x] Bỏ `white-space:normal; word-break:break-word` trong `.sticky-head th` (rule này làm header bẻ dọc từng ký tự khi cột hẹp/bảng rỗng) → header bẻ theo ranh giới từ, đọc được
- [x] Đổi 5 cột tiền (Giá nhập, Thành tiền nhập, Giá bán, Thành tiền bán, Thành tiền sau VAT) từ `width:130px` → `min-width:150px; white-space:nowrap`; Tiền VAT `min-width:130px; nowrap` → header luôn 1 dòng, đủ rộng, các cột tiền chính bằng nhau (150px)
- [x] Verify Playwright: header các cột tiền 150px, nowrap, đọc rõ; cột ngắn (Thao tác...) bẻ theo từ không còn dọc từng ký tự

### Checkpoint — 2026-07-08
Vừa hoàn thành: toàn bộ Phase 1 (AC1 + AC2 + header căn giữa/phân cách) — CODE DONE + VERIFIED (Playwright)
Verify (màn /assign/quotations/create, login qua API token, viewport 760px ép tràn):
- AC1: 4 cột Giá nhập / TT nhập / TT bán / TT sau VAT offsetWidth bằng nhau (~30-32px khi bảng rỗng); trước đây 130/150/150/170
- AC2: bảng tràn (scrollWidth 1088 > client 675) → thanh cuộn trên hiện; kéo top→body và body→top đồng bộ 2 chiều; spacer tự cập nhật qua ResizeObserver
- Header: allHeaderCentered=true (text-align center đè .text-right), border-right 1px phân cách; ảnh xác nhận trực quan
Đang làm dở: không
Bước tiếp theo: user verify browser với dữ liệu thật (chọn dự án + thêm hàng để thấy cột 130px đầy đủ)
Blocked:
