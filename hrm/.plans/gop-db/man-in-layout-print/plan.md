# Màn in cũ → popup xem trước — @namdangit

Thiết kế + quyết định: [design.md](design.md)

## Phase 0 — Vá tạm lòi menu + lỗi biến (08/10/2026)

- [x] Thêm `layout: 'print'` vào 105 màn in (chưa commit — sẽ bị thay dần bởi popup, file nào xoá thì thôi)
- [x] Biến `TRINH_DO_HOC_VAN` in trống (HĐLĐ 733 prod): HĐ lập lúc hồ sơ chưa có trình độ → lưu trống;
      thêm `academicLevelName()` lấy bù từ hồ sơ cho TRINH_DO_HOC_VAN/BANG_CAP/TRINH_DO (api `77506e50d`)

## Phase 1 — Hạ tầng + in CHI TIẾT Quyết định

### FE
- [x] `utils/print/decisionPrintStyle.js`: `buildDecisionPrintCss(root, { lineHeight, compactTable, forPrint })` + lề
      (mặc định 20/20/20/30mm + giãn dòng 1.6 = đúng bản in cũ; HĐLĐ 20/15/20/25 + 1.4; phụ lục 1.4 + compactTable)
- [x] `utils/print/decisionPrintTargets.js`: bảng khoá màn → endpoint/tiêu đề (tên menu)/CSS/lề (24 bản in)
- [x] `ReportPrintPreviewModal`: thêm `contentCss` / `pageMargin` / slot (mặc định như cũ — đã kiểm 13px/10px, 12mm 10mm)
- [x] `plugins/print-preview.js`: `this.$printPreview({ decision, id } | { url | html, title, ... })`, đăng ký nuxt.config (client)
- [x] 23 nút "In" ở màn danh sách + `ActionButtonComponent` → `$printPreview` (sửa luôn link Quy chế lương trỏ sai → 404)
- [x] Xoá 24 file `pages/decision/**/_id/print*.vue` (mẫu HTML từ BE)
- [x] Verify Playwright (dev 3005/8002): 17/17 bản in có dữ liệu local — 0 thuộc tính lệch giữa xem trước và iframe in
      (HĐLĐ 1.269 phần tử, cao 3.682px = 3.682px); nút In dựng iframe đúng @page; đóng popup dọn sạch modal + style.
      6 bản chưa có dữ liệu local để đo: thưởng lương T13, tăng lương thâm niên, ký HĐLĐ, nghỉ hưu, tạm hoãn (+ thoả thuận), HĐ đào tạo
- [ ] Cập nhật skill `print-page` mục 0 (màn Quyết định nay là popup qua `$printPreview`) — chờ user đồng ý sửa skill chung

## Phase 2 — In DANH SÁCH (53 màn)

- [x] `utils/print/listPrintHtml.js`: dựng HTML bảng (letterhead công ty người in + tiêu đề + bảng + vùng ký),
      escape ô, lỗi 1 ô chỉ làm trống ô đó; trần `LIST_PRINT_LIMIT` = 2.000 dòng (vượt = chặn in, nhắc thu hẹp lọc)
- [x] `utils/print/list-targets/{decision,training,misc}.js` + `index.js`: khai báo 53 màn (khoá = route in cũ),
      cột/tiêu đề/hàm trạng thái SINH TỰ ĐỘNG từ template `print.vue` cũ (chép nguyên văn), sửa tay 2 ô + 3 lỗi chính tả tiêu đề
- [x] Plugin nhận `{ listRoute: computedPrintUrl }` — bộ lọc chuyển nguyên từ query; khổ ngang, preset mẫu ERP
- [x] 52 nút "In" ở màn danh sách: `:to="computedPrintUrl" target="_blank"` → `@click="$printPreview({ listRoute: computedPrintUrl })"`
- [x] Xoá 53 file `print.vue` / `waiting-approve-print.vue`
- [x] Verify: đối chiếu từng ô bản cũ (iframe trang /print) với popup mới — 53/53 khớp tiêu đề cột + mọi ô.
      Bản cũ cắt ngầm: Phiếu đề xuất công việc 200/486 dòng, Ngân hàng câu hỏi 1.000/1.687 — bản mới in đủ.
      Nhánh vượt trần (giả lập total 5.000): hiện nhắc, ẩn bản xem trước + nút In.

## Phase 3 — Báo cáo/phiếu tự dựng (33 trang) — nhúng iframe

- [x] `layouts/print.vue`: chế độ nhúng `?embed=1` — ẩn thanh nút của trang, phơi `window.__hrmPrintPage()`
- [x] `ReportPrintPreviewModal`: prop `src` (iframe, khung 1200px) — bỏ slot dự định ở Phase 1 (không dùng)
- [x] Plugin `{ page }`; 41 chỗ mở (`:to`, `window.open`, `$router.push`) → `$printPreview({ page | url })`
- [x] Biên bản họp (3 tab Cuộc họp) → `{ url: assign/meeting/{id}/print }` như 8 báo cáo, xoá `assign/meeting/_id/print.vue`
- [x] `assign/meeting/_id/survey-print.vue` thiếu `layout: 'print'` (lòi menu) → bổ sung
- [x] Verify (script Playwright headless riêng — profile-a đang bị phiên khác giữ): 26 trang có dữ liệu — trang nhúng lên,
      không lòi menu, thanh nút ẩn, bấm In của popup gọi đúng hàm in sẵn có (`window.open`+`print` / `window.print`),
      màn cha không chuyển trang. 6 trang không có dữ liệu local: đề nghị thanh toán, thưởng T13 (2), ĐN xuất bán
      hàng mượn, phiếu KS phòng, khảo sát đào tạo.
- [ ] (Không làm) `training/report/training-status-by-personnel/print` — nút In ở màn gốc đang bị comment, không ai mở được
- [ ] Cập nhật skill `print-page` mục 0/8 theo `$printPreview` — chờ user đồng ý sửa skill chung

### Checkpoint — 2026-10-08 (Phase 3)
Vừa hoàn thành: Phase 1-3 — mọi nút In cũ mở tab `/print` đều chuyển sang popup `$printPreview`; đã verify; CHƯA commit.
Đang làm dở: không.
Bước tiếp theo: user duyệt báo cáo → commit client (api đã có `77506e50d`); hỏi cập nhật skill print-page.
Blocked:

### Checkpoint — 2026-10-09 (merge)
Vừa hoàn thành: nhánh `gop_db-man-in-popup` (`412ebe490`, kèm sửa nút "In quyết định" màn QĐ chờ duyệt) đã merge
develop để test (user test đạt) → merge vào `gop_db` (`681ca5ea7`) và push. Rà 6 commit mới của gop_db: không đụng phần in.
Đang làm dở: không.
Bước tiếp theo: (tuỳ user) cập nhật skill print-page theo `$printPreview`; sửa comment cũ ở `finance/borrow-sells/_id/index.vue`
("mở trang in ở tab mới"); đưa api `77506e50d` sang develop nếu cần.
Blocked:
