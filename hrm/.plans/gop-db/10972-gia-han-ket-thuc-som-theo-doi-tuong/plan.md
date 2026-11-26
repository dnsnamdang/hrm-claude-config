# Plan — #10972 Gia hạn / kết thúc sớm theo Đối tượng

Design: `design.md` cùng thư mục · Spec: `docs/superpowers/specs/gop-db/2026-11-26-10972-gia-han-ket-thuc-som-theo-doi-tuong-design.md`

## Phase 1 — BE (hrm-api)
- [x] Migration `Modules/Assign/Database/Migrations/2026_11_26_000001_add_target_type_to_extend_end_soon_requests.php` (đã chạy local)
- [x] `ExtendEndSoonRequest`: hằng số TYPE_*, TARGET_*, accessor type_text / target_type_text
- [x] `AssignRequest::employeeToTime()`; canExtendTime / canEndSoon theo ngày của người đăng nhập; syncEmployee giữ ngày riêng
- [x] `ExtendEndSoonRequestService`: applyApproved, findPending, pendingMessage
- [x] Controller: normalizeTarget, chặn trùng theo người tạo, approve qua service, export 2 cột, eager-load index
- [x] FormRequest: target_type bắt buộc khi ≥ 2 nhân sự; "Chỉ mình tôi" so ngày hiệu lực của chính người tạo
- [x] Transformer + Criteria (lọc target_type, NULL = Tất cả); getForExtendEndSoon trả employee_count, my_to_time
- [x] getDetail trả effective_to_time từng nhân viên
- [x] Ngày riêng ở: listAssignBussiness, validateAssignBusiness, validateVsAssignBusiness, calculateFormData + buildTimesheets, SettlementContractController
- [x] Sửa isLastDay
- [x] Kết thúc sớm riêng theo đoàn khi đoàn kết thúc sớm hơn

## Phase 2 — FE (hrm-client)
- [x] `utils/assign/extendEndSoonRequest.js` (hằng số dùng chung)
- [x] ExtendEndSoonForm: ô Đối tượng + validateTarget; create/edit gọi validateTarget
- [x] Danh sách: cột + lọc Loại phiếu, Đối tượng; fieldsExport
- [x] AssignBusinessForm: cột "Ngày gia hạn/kết thúc" giữa Có chiều về / Ghi chú (employeeDetailColspan)

## Phase 3 — Kiểm
- [x] Tinker (transaction + rollback): luồng duyệt 6 ca, chấm công, trùng lịch, syncEmployee, thanh toán, ca kết thúc sớm theo đoàn, isLastDay
- [x] Playwright (26/11): màn tạo 2 nhân sự báo đỏ khi trống → chọn Chỉ mình tôi → Lưu và gửi duyệt; danh sách 2 cột + lọc Đối tượng (1 + 1880 = 1881); duyệt ⇒ PCT giữ 28/11, NV 13 ngày riêng 30/11; chi tiết PCT cột giữa Có chiều về/Ghi chú, NV 2 tuyến gộp đúng; PCT 1 nhân sự khoá Chỉ mình tôi
- [x] Sửa lỗi Playwright bắt được: `getDetail` closure thiếu `use ($obj)` ⇒ 400 Undefined variable

## Checkpoint — 2026-11-26 (kiểm giao diện xong)
Vừa hoàn thành: BE + FE + kiểm Playwright đủ 3 màn; dữ liệu test PCT-14818 đã trả về gốc.
Đang làm dở: —
Đã push 26/11: `task_10972` (api 164db9d4d · client b32866181) + cherry-pick lên develop (api 8adbbf6d5 · client 4cfead048).
Bước tiếp theo: deploy dev chạy migration `2026_11_26_000001`, QA test; lên gop_db khi user bảo.
Blocked:
