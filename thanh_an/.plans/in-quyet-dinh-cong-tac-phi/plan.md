# In QUYẾT ĐỊNH cử đi công tác — Plan tổng quát

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-15-in-quyet-dinh-cong-tac-phi-design.md`
**Plan chi tiết:** `docs/superpowers/plans/2026-06-15-in-quyet-dinh-cong-tac-phi.md`

## Phase 1 — FE (print.vue)
- [x] Task 1: Thêm computed `companyName` + `tripPlaces`; dọn `detail_tmp` + khối padding `form`
- [x] Task 2: Viết lại template `.print-data` thành layout QUYẾT ĐỊNH (header 2 cột, căn cứ, Điều 1/2/3, footer 2 cột)
- [x] Task 3: CSS 2 cột header/footer
- [x] Task 4: Dọn code chết (`formatTime`, `moment`) + dọn thêm sau review: bỏ request `static-data` thừa, flag `isShow*`, import `vue2-datepicker`/`TP_URL` không dùng

## Kiểm thử (cần user xác nhận trên trình duyệt)
- [ ] Mở `/timesheet/jobassignment/2059/print` — layout đúng, không lỗi Console
- [ ] Ctrl+P xem print preview — ẩn nút, 2 cột canh đúng, tiếng Việt có dấu
- [ ] Thử phiếu nhiều nhân viên — Điều 1 liệt kê đủ

## Phase 2 — Chuyển sang popup (theo mẫu hrm-client/assign/form-templates)
- [x] Tạo component dùng chung `components/modal/JobAssignmentDecisionPrintModal.vue` (b-modal + nội dung QUYẾT ĐỊNH + nút In/Đóng, `open(id)`, `getPrintStyles()`, `handlePrint()` mở cửa sổ mới in)
- [x] index.vue: dropdown In → `@click="$refs.printModal.open(item.id)"` + nhúng modal + import/register
- [x] waiting-approve.vue: tương tự
- [x] Giữ lại file page `_id/print.vue` (theo yêu cầu user, route /print vẫn truy cập được)
- Điều chỉnh format: thời gian lấy từ `intend_start_at`/`intend_end_at` (sớm nhất/muộn nhất), hiển thị `HH:mm DD/MM/YYYY`

## Checkpoint — 2026-06-15
Vừa hoàn thành: Chuyển màn in QUYẾT ĐỊNH từ page sang popup dùng chung cho 2 trang danh sách (index + waiting-approve).
Đang làm dở: (không)
Bước tiếp theo: User mở danh sách phiếu giao việc → dropdown "In" → kiểm tra popup hiển thị + nút In mở cửa sổ in.
Blocked: Không chạy được Nuxt app trong môi trường này → cần user kiểm tra trực quan.
