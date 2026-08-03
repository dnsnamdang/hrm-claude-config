# Plan — Manager gia hạn/kết thúc sớm phiếu công tác theo quyền

> Spec chi tiết: `docs/superpowers/specs/2026-06-24-business-trip-manager-extend-design.md`
> Phụ trách: @manhcuong

## Phase 1 — Backend

- [x] Service `BusinessTripAssignService::finishExtend`: nhánh manager (đọc `employee_info_id`), lookup BusinessTripEmployee where employee_id=target & assign_id, check `listManageEmployeeInfoIds(false,null,true)`; giữ nguyên nhánh self
- [x] Tách message chặn trùng request theo nhánh (self / manager)
- [x] FormRequest `BusinessTripManagerFinishExtendRequest` (id|exists, employee_info_id|exists:employee_infos, date|date, type|in:1,2)
- [x] Controller `managerFinish` (type=1) + `managerExtend` (type=2): gate `isCurrentEmployeeHasPermission('Gia hạn, kết thúc sớm phiếu công tác')` → 403; notification approver
- [x] Routes `POST .../manager/finish` + `.../manager/extend` (auth:api, KHÔNG checkPermission)
- [x] `php -l` sạch 4 file BE

## Phase 2 — Frontend

- [x] `index.vue`: helper `canManagerExtend()` + nút row `fa-calendar-plus` v-if quyền + `openManagerExtend(item)`
- [x] Component `manager-finish-trip-modal.vue`: @show fetch chi tiết phiếu → dropdown Nhân sự; Loại/Thời gian/Ghi chú; validate inline (is-invalid + invalid-feedback + touched)
- [x] Store action `managerFinishExtendTrip` (map type→manager/finish|manager/extend, body {id, employee_info_id, date, note, type})
- [x] Wire submit → toast + reload danh sách; lỗi hiện message BE
- [x] Verify browser (Playwright, tài khoản namdangit) — PASS

## Checkpoint — 2026-06-24 (VERIFIED)
Vừa hoàn thành: Code BE + FE, review từng task PASS + final whole-branch READY TO MERGE + VERIFY browser bằng Playwright (tài khoản namdangit, DB hrm_prod_local).
Kết quả verify end-to-end:
- Nút "Gia hạn/Kết thúc sớm" (icon lịch xanh) hiện đúng mỗi dòng màn Quản lý phiếu đi công tác (có quyền 315).
- Modal nạp đúng danh sách NS trong phiếu (dropdown value=employee_info_id), Loại/Thời gian*/Ghi chú, validate inline.
- Gia hạn (POST manager/extend) → 200, tạo request type=2 status=1 (chờ duyệt). Toast "Gia hạn thành công".
- Kết thúc sớm (POST manager/finish) → 200, message "Yêu cầu kết thúc công tác thành công".
- Chặn trùng → 422 "Nhân sự này đã có yêu cầu kết thúc/gia hạn công tác đang chờ duyệt" (đúng nhánh manager), FE hiện toast đỏ.
- Request manager tạo hiện đúng ở màn duyệt finish-extend (Cáp Văn Chiến).
- Đã dọn sạch 2 record test (req 471, 472) khỏi DB thật.
Chưa verify trực tiếp qua UI (do namdangit là admin all_department): nhánh 403 không-quyền + 422 NS-ngoài-phạm-vi — đã xác nhận bằng code review + dùng chung listManageEmployeeInfoIds với màn DS.
Bước tiếp theo: (không) — sẵn sàng merge khi cần.
Blocked: (không)

### Cập nhật UI — 2026-06-24
Theo yêu cầu user: đổi 2 select (Nhân sự + Loại) trong manager-finish-trip-modal.vue từ `b-form-select` sang component `BaseSelect2Modal` (@/components/BaseSelect2Modal.vue) — options dạng `{ id, text }`, prepend placeholder "-- Chọn nhân sự --". Bỏ param `response` thừa ở .then. Verify Playwright lại: 2 select2 render đúng trong modal, dropdown nạp NS qua Select2, submit gia hạn end-to-end OK (200), không console error; đã dọn record test.
