# Plan — Loại meeting: gán phiếu tổng hợp kết quả (Redmine #11130)

> @junfoke — Nhánh `task_11130` (tách từ `tpe`), cả 2 repo.
> Design: `.plans/meeting-type-result-form/design.md`

## Phase 1 — BE: cấu hình phiếu trên Loại meeting

- [x] 1.1 Migration `add_result_form_to_meeting_types_table`: `has_result_form`, `form_template_id`
- [x] 1.2 `MeetingType`: fillable + quan hệ `formTemplate()`
- [x] 1.3 Request lưu Loại meeting: `form_template_id` bắt buộc khi bật công tắc, phải là mẫu phiếu Published
- [x] 1.4 Service/Resource Loại meeting: lưu + trả 2 trường mới

## Phase 2 — BE: phiếu trong biên bản meeting

- [x] 2.1 API chi tiết meeting trả `result_form` (mẫu phiếu theo Loại meeting + đáp án đã lưu)
- [x] 2.2 Endpoint lưu đáp án phiếu theo meeting (`FormAnswerService`, type = `meeting`)
- [x] 2.3 Chặn Hoàn thành biên bản khi còn câu bắt buộc chưa trả lời (422, nêu rõ câu nào)

## Phase 3 — FE

- [x] 3.1 Danh mục Loại meeting: công tắc + ô chọn mẫu phiếu
- [x] 3.2 Biên bản meeting: phân vùng "Phiếu tổng hợp kết quả meeting" ở đầu, render động
- [x] 3.3 Chặn Hoàn thành + hiện lỗi inline tại câu bắt buộc còn trống

## Phase 4 — Verify

- [x] 4.1 Cấu hình Loại meeting: bật/tắt, chọn mẫu, lưu, mở lại
- [x] 4.2 Biên bản của loại meeting có phiếu: render đúng bộ câu hỏi, lưu đáp án, mở lại còn nguyên
- [x] 4.3 Thiếu câu bắt buộc → không Hoàn thành được (kiểm cả BE lẫn FE)
- [x] 4.4 Loại meeting KHÔNG gán phiếu → biên bản không đổi
- [x] 4.5 Phiếu khảo sát đầu tư cũ + báo cáo CSKH tiềm năng không bị ảnh hưởng

### Checkpoint — 2026-09-11
Vừa hoàn thành: tách nhánh, khảo sát engine phiếu động, chốt 2 quyết định kiến trúc với user
Đang làm dở: Phase 1
Bước tiếp theo: migration + entity + request cho Loại meeting
Blocked:

### Verify (2026-09-11, FE :3005 → API :8002 → DB `hrm_prod_30_3_26`)

| Ca | Kết quả |
| --- | --- |
| Modal Loại meeting: công tắc "Gán phiếu tổng hợp kết quả meeting" | ✔ hiện; bật lên mới hiện ô chọn mẫu phiếu + dòng giải thích |
| Ô chọn mẫu phiếu chỉ liệt kê mẫu đã Phát hành | ✔ |
| Lưu Loại meeting có gán phiếu | ✔ DB: `has_result_form = 1`, `form_template_id = 7` |
| API chi tiết meeting trả `result_form` | ✔ kèm tên mẫu + đáp án đã lưu |
| Biên bản: phân vùng "Phiếu tổng hợp kết quả meeting" ở đầu | ✔ render đúng bộ câu hỏi của mẫu |
| Nhập đáp án → Lưu biên bản | ✔ DB `form_answers` (type = `meeting`, type_id = 54) + 3 dòng chi tiết đúng nội dung |
| Mở lại biên bản | ✔ 3 đáp án hiện lại nguyên vẹn |
| FE chặn Hoàn thành: chưa trả lời gì | ✔ báo thiếu câu 1 (câu 2 đang ẩn theo rẽ nhánh nên không đòi) |
| FE: trả lời câu 1 = "Có" | ✔ câu 2 trở thành bắt buộc, báo thiếu đúng câu 2 |
| FE: trả lời đủ | ✔ hết báo thiếu |
| BE chặn Hoàn thành (gọi thẳng API) | ✔ thiếu → lỗi `result_form_answers`; đủ → hết lỗi |
| BE rẽ nhánh: câu 1 = "Không" | ✔ KHÔNG đòi câu 2 |
| Loại meeting không gán phiếu | ✔ biên bản không đổi (phân vùng ẩn) |
| Phiếu khảo sát đầu tư cũ | ✔ giữ nguyên, chạy song song, không đụng |

**Lỗi tìm ra trong lúc verify và đã sửa:**
1. `MeetingService` gọi `$meeting->meetingType` nhưng quan hệ trên entity đặt tên snake_case
   (`meeting_type()`) → API luôn trả `result_form = null`.
2. FE tra đáp án theo `q.local_id`, nhưng Resource mẫu phiếu trả khoá là **`localId`** (camelCase) —
   FormPreview cũng emit theo khoá này → đáp án không khớp câu hỏi, luật bắt buộc báo sai.

**Ẩn/hiện câu hỏi động theo rẽ nhánh — ĐÃ LÀM (bổ sung 2026-09-11, commit 78330aa5b).**
Lần verify đầu phát hiện `FormPreview` vẽ mọi câu hỏi, không ẩn câu theo `visibility` → thiếu đúng vế
spec "Câu 2 chỉ hiển thị khi Câu 1 là Có". Cách chữa: lọc câu chưa tới lượt NGAY TRƯỚC khi truyền
`sections` cho FormPreview (computed `visibleResultFormSections`), KHÔNG sửa FormPreview vì component
đó dùng chung với Phiếu thu thập thông tin của dự án TKT. Hàm `isResultQuestionVisible()` dùng chung
cho cả việc vẽ lẫn việc kiểm câu bắt buộc để 2 chỗ không lệch nhau.

| Ca (kiểm lại sau khi sửa) | Kết quả |
| --- | --- |
| Chưa trả lời câu 1 | ✔ câu 2 ẨN, câu 1 + câu 3 hiện |
| Câu 1 = "Không" | ✔ câu 2 vẫn ẨN, không bị đòi bắt buộc |
| Câu 1 = "Có" | ✔ câu 2 HIỆN và trở thành bắt buộc |

Ảnh: `hrm-client/11130-phieu-trong-bien-ban.png`, `hrm-client/11130-re-nhanh-cau-2-hien.png`.

**Dữ liệu test còn lại trong DB local** (không xoá được qua API vì đang ở trạng thái đã chốt / đang
được dùng): meeting id 54 `TPE.MET.KH.26.0050`, loại meeting id 17 "Loại meeting test #11130",
`form_answers` id 3. Mẫu phiếu test đã xoá.

**Migration đã chạy trên DB local để môi trường khớp nhánh `tpe`** (DB snapshot cũ hơn code):
`add_is_customer_meeting_to_meetings_table`, `add_sort_order_to_meeting_employees_table`,
`add_report_deadline_columns_to_meetings_table`, `add_code_to_meeting_types_table`,
`create_meeting_investment_demands_table`, `switch_meeting_investment_demands_to_internal_scopes`,
`create_meeting_investment_scopes_table`, `add_type_to_meeting_attachments_table`,
`add_tracking_columns_to_meeting_investment_demands_table`, `create_meeting_report_executors_table`,
`backfill_meeting_report_executors`, `change_note_conclusion_to_longtext_on_meetings_table`.
Vẫn còn ~12 migration khác chưa chạy (không liên quan meeting).

### Checkpoint — 2026-09-11
Vừa hoàn thành: cả 3 phase code + verify trên UI thật; sửa 2 lỗi phát hiện khi verify
Đang làm dở: không
Bước tiếp theo: commit 2 repo; cân nhắc task riêng cho việc FormPreview chưa ẩn câu theo rẽ nhánh
Blocked: không

## Phase 5 — Tài liệu

- [x] 5.1 Sinh testcase Excel cho tính năng (`gen_testcase.py` + `testcase.xlsx`, 67 TC / 39 P0)

### Checkpoint — 2026-09-12
Vừa hoàn thành: testcase.xlsx (67 TC, 8 section nghiệp vụ + 7 TC phân quyền) dựng bằng engine chung
của skill testcase-documenter, nội dung bám đúng code nhánh `task_11130` (nhãn, thông báo lỗi, luật
rẽ nhánh, quyền trong seeder)
Đang làm dở: không
Bước tiếp theo: chuyển QA chạy testcase; nếu cần thì bổ sung SRS
Blocked: không

## Phase 6 — BỎ phần cấu hình trên Loại meeting (mô tả task cập nhật 15/09/2026)

> TPE sửa mô tả #11130: mục "1. Cấu hình Loại meeting" đánh dấu **(BỎ)**; mục "2. Biên bản meeting"
> ghi **(GIỮ LẠI - FIX CODE SẴN VỚI LOẠI MEETING - Họp tìm hiểu về giới thiệu sản phẩm)**.
> Tức là quay về đúng phiếu khảo sát CỨNG đã có sẵn (`MeetingInvestmentSurvey`), không cấu hình
> bộ câu hỏi theo Loại meeting nữa. Phản hồi QA "Chưa thấy form nhập câu hỏi" khép lại theo hướng này.

- [x] 6.1 Nhánh **`task_11130_tpe` (tách từ `tpe`)** ở cả 2 repo — bản đầu lỡ tách từ `tpe-develop-assign`, xem ghi chú cuối file
- [x] 6.2 BE: revert toàn bộ code #11130 (MeetingType, MeetingTypeRequest/Service, MeetingService,
      MeetingController, MeetingUpdateApiRequest, 3 Resource/Transformer)
- [x] 6.3 BE: migration `2026_09_15_000001_drop_result_form_from_meeting_types_table` bỏ 2 cột
      `has_result_form` / `form_template_id` (giữ nguyên file migration cũ để bảng `migrations` không lệch)
- [x] 6.4 FE: revert modal Loại meeting (công tắc + ô chọn mẫu phiếu) và phân vùng phiếu động ở Biên bản
- [x] 6.5 Verify: Loại meeting không còn công tắc; biên bản loại "Họp tìm hiểu & Giới thiệu sản phẩm"
      vẫn hiện khảo sát cứng + chặn Hoàn thành khi thiếu câu bắt buộc
- [ ] 6.6 Chạy migration 6.3 trên các môi trường đã deploy (local/test/prod) — chờ user quyết

**Giữ nguyên, KHÔNG đụng tới:** `MeetingInvestmentSurvey.vue`, `meeting_investment_demands`,
`meeting_investment_scopes`, validate `has_investment_demand` / `investment_demands` trong
`MeetingUpdateApiRequest` — đây chính là phần spec yêu cầu giữ lại.

**Dữ liệu tồn đọng:** đáp án đã lưu ở `form_answers` với `type = meeting` (bản test) không bị xoá,
chỉ còn mồ côi. Testcase `testcase.xlsx` sinh cho bản cũ nay không còn đúng phần cấu hình.

### Checkpoint — 2026-09-15
Vừa hoàn thành: revert code #11130 ở cả 2 repo + migration bỏ 2 cột
Đang làm dở: verify trên UI
Bước tiếp theo: kiểm Loại meeting + Biên bản trên :3005, rồi phản hồi Redmine
Blocked: chưa chốt có chạy migration bỏ cột trên môi trường đã deploy hay không

### Verify Phase 6 — 2026-09-15 (FE :3005 → API :8002, DB `hrm_prod_30_3_26`)

| Ca | Kết quả |
| --- | --- |
| Modal Thêm loại meeting | ✔ chỉ còn Tên / Trạng thái / Mô tả / Có khách hàng — hết công tắc gán phiếu |
| Biên bản meeting id 54 (loại từng gán phiếu) | ✔ không còn phân vùng "Phiếu tổng hợp kết quả meeting", không lỗi JS mới |
| Biên bản loại `HOP_TIM_HIEU_GIOI_THIEU_SP` | ✔ vẫn hiện "1/ Khảo sát nhu cầu khách hàng" như trước |

**Phát hiện ngoài lề, có thể chính là lý do QA "chưa thấy":** DB đang có **2 loại meeting trùng
tên** "Họp tìm hiểu & Giới thiệu sản phẩm" — id 14 (`code = NULL`, bản cũ) và id 18
(`code = HOP_TIM_HIEU_GIOI_THIEU_SP`, do `SystemMeetingTypesSeeder` tạo). Khối Khảo sát chỉ bật
theo `code`, nên meeting chọn nhầm bản id 14 thì KHÔNG có khảo sát nào hiện. Seeder khoá theo
`code` nên không nhận ra bản trùng tên cũ. Cần rà dữ liệu ở môi trường test/prod: hoặc backfill
`code` cho bản cũ, hoặc khoá bản cũ để user không chọn nhầm.

### Đổi nhánh nền — 2026-09-15 (quan trọng)

Bản sửa lần đầu tách từ `tpe-develop-assign` là SAI nền: merge nhánh đó vào `tpe` thì Git
fast-forward, kéo nguyên cả dòng `tpe-develop-assign` (task_11377, #11386, #11390, fix quyền…)
vào `tpe`. Đã `reset --hard` trả `tpe` về đúng `origin/tpe` ở cả 2 repo (lúc đó CHƯA push) và
làm lại trên nhánh `task_11130_tpe` tách từ `tpe`:

| Repo | Nhánh | Commit |
| --- | --- | --- |
| hrm-api | `task_11130_tpe` (nền `ea65e953a`) | `28323306a` |
| hrm-client | `task_11130_tpe` (nền `656cfd5bc`) | `9fce02599` |

2 nhánh cũ `task_11130_bo_cau_hinh` giữ lại làm dự phòng, KHÔNG merge.

**Đính chính so với nhận định sáng nay:** `origin/tpe` của hrm-client nay ĐÃ có FE #11130
(bản pull mới hơn lần kiểm đầu), nên cả 2 repo đều phải gỡ, không còn chuyện lệch nhánh FE/BE.
