# Xuất Excel danh sách nhân sự — chia nhỏ theo trang (chưa có số Redmine) — @cuong61n

Màn `/human/employee_info`, nút "Xuất danh sách". Nhánh `gop_db` (worktree `gop_db-api` + `gop_db-client`).

## Vấn đề
- Xuất Excel danh sách nhân sự không ra file: BE gom cả bảng (không phân trang) rồi dựng file bằng `FromView` trong 1 request (`getEmployeeByField`).
- Đã chốt hướng chia nhỏ như khuôn skill list-page mục 14c (`export-rows` + `utils/export/listExportFile.js`).

## Phase 1 — Chia nhỏ xuất file
### BE
- [x] 2026-11-04 Tách đoạn map dòng nhân sự thành `buildEmployeeExportItem()` — bản BE cũ `getEmployeeByField` và API mới dùng chung, bản cũ giữ nguyên để đối chiếu
- [x] 2026-11-04 Thêm `GET human/employee-infos/export-rows` (`EmployeeInfoController::exportRows`): trả `{headings, widths, rows, total, page, limit}`, 2.000 dòng/lượt, trần 5.000; dùng chung bộ lọc + phân quyền với `getEmployeeInfos()`; nạp sẵn tài khoản ngân hàng cả trang (tránh N+1); chữ `<br>`/`&amp;` đổi về chữ thường cho ô Excel
- [x] 2026-11-04 Cột đúng thứ tự file cũ (blade `employee_info_report`), 44 trường; trường "Ảnh" (45) không đi đường này
### FE
- [x] 2026-11-04 `export-list-employee-modal.vue`: không tick "Ảnh" → gọi `exportListFile` (tải tuần tự từng trang, dòng tiến độ, khoá nút OK khi đang xuất); tick "Ảnh" → giữ đường BE cũ vì ảnh nằm S3, trình duyệt không tải được (CORS)
### Kiểm tra
- [x] 2026-11-04 Gọi controller trong tinker (TK namdangit): đang làm 604 dòng × 45 cột 0,35s; nghỉ việc 600 dòng 0,25s; không còn `<br>`/`&amp;` trong ô
- [x] 2026-11-04 Thử trên trình duyệt local (:3002): không ảnh ra file đủ 604 dòng × 45 cột; đã kiểm phân trang không trùng (limit 50/7, STT liên tục 1–604, mã NV không trùng)
- [x] 2026-11-04 Đã commit + đẩy nhánh `gop_db` (469f70b81 / 7aeb5c532) và deploy prod bằng `~/build_tpe.sh`

## Phase 2 — Xuất kèm cột Ảnh
Nguyên nhân: đường BE cũ tải ~604 ảnh S3 TUẦN TỰ (~0,25s/ảnh ≈ 150s) trong 1 request nên quá thời gian chờ; ít nhân sự thì kịp.
### BE
- [x] 2026-11-04 `export-rows` nhận field 45: thêm cột 2 "Ảnh", trả kèm `images` (base64 JPEG thu nhỏ ~90px) + `image_column`; `fetchAvatarThumbnails()` tải song song bằng curl_multi 20 ảnh/lượt, nền trắng cho PNG trong suốt; ảnh lỗi → null
### FE
- [x] 2026-11-04 `listExportFile.js`: `fetchExportRows` gom `images`, tham số `pageLimit`; `buildXlsxBlob` chèn ảnh vào đúng ô (dòng cao 72pt). Modal nhân sự: tick Ảnh cũng đi đường chia trang, 100 dòng/lượt
### Kiểm tra
- [x] 2026-11-04 Local 604 người: 70s ra file 2,1MB, 577 ảnh chèn đúng dòng, mã NV không trùng. 28 người không có ảnh vì link S3 trả 403 (dữ liệu, đường cũ cũng không tải được)
- [ ] Chưa commit/push, chưa deploy prod (chờ user bảo)

