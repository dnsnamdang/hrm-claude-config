# STATUS.md

## Đang làm
- Bomlist-Quotation → @dnsnamdang → .plans/Bomlist-Quotation/plan-phase11.md
  Trạng thái: Phase 11 đang test UI — đã sửa 9 bug + 1 cleanup từ test session 6. Bao gồm: bỏ giá bán khỏi BOM (cả UI table + popup + import/export + DB drop cột quoted_price), loose version match khi chọn BOM con, validate tên BOM khi nháp, preview BOM thực tế trong modal hồ sơ trình duyệt (alert có link mã+tên), fix prop tab Hồ sơ + button Yêu cầu XD giá, BOM resolve dùng status=Đã duyệt + log debug.
  Checkpoint: 2026-04-17 (session 8-12) — Nhiều vòng test + fix UI/UX + phân quyền:
  - Form tạo/show YCBG: compact table key-value, file upload fix (S3 string URL), link BOM, popup detail
  - Màn show/edit báo giá: info table compact, topbar title+status, bg trắng, collapsible info, sticky header products, font-weight 300, tỷ suất LN từng dòng+tổng, footer pricing compact responsive, V2BaseButton chuẩn, popup YCBG + lịch sử
  - Bỏ deadline khỏi báo giá, thêm Giải pháp+Hạng mục, bỏ text "Giá tính theo", lưu nháp skip validate, đổi currency cảnh báo + reactive code/exchangeRate, cấp duyệt client-side realtime
  - Validate required 4 field (hiệu lực/giao hàng/bảo hành/tiền tệ), validate giá >0 khi submit, highlight cell đỏ
  - Cấp 3 rõ 2 bước: footer "C3 — TP & BGĐ", popup submit flow 2 step visual
  - Danh sách báo giá: 12 cột (tiền tệ/tổng/người tạo/ngày tạo/cấp duyệt/người duyệt/ngày duyệt), column customization, bộ filter đầy đủ (cấp tổ chức cascading + GP→Version + trạng thái + người duyệt), button lịch sử
  - Phân quyền: 7 permissions group "Báo giá" (4 cấp xem + XD giá + TP duyệt + BGĐ duyệt), can_view_import_price (KD không xem giá nhập/tỷ suất chi tiết, xem tỷ suất tổng)
  - Notification mobile: APP_NAME_MOBILE="Thông báo từ ERP TPE", strip_tags HTML body
  - Layout: padding giảm (custom-assign.scss), pt-2→pt-1, PageTitleMixin cho 15 trang Assign thiếu, bỏ PageHeader cũ trong BomBuilderEditor, bỏ select tiền tệ khỏi BOM list
  Bước tiếp: User test tiếp flow end-to-end.

## Tạm dừng

- notify-task-report → @dnsnamdang → .plans/notify-task-report/plan.md
  Trạng thái: 26/26 task done. Fix $fillable + UI daily-report. FCM blocked bởi HTTP trên dev server
  Checkpoint: 2026-04-09 — Phase 11 done. Cần HTTPS trên dev server để FCM hoạt động

## Hoàn thành

- solution-add-module-deploying → @manhcuong → .plans/solution-add-module-deploying/plan.md
  Hoàn thành: 2026-04-07. 3/3 task. PM thêm hạng mục khi đang triển khai + auto-approve
- solution-save-and-approve → @manhcuong → .plans/solution-save-and-approve/plan.md
  Hoàn thành: 2026-04-07. 2/2 task. Button "Lưu và duyệt" khi has_modules=false
- solution-version-report → @manhcuong → .plans/solution-version-report/plan.md
  Hoàn thành: 2026-04-07. 15/15 task + 53 test cases. Báo cáo QLDA_BC_10 theo version
