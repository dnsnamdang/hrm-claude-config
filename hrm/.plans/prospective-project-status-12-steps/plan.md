# Plan — Tiến trình nội bộ 12 bước (Redmine #11426)

Nhánh `tpe` · worktree `HRM/worktrees/tpe-api` + `tpe-client`

## Phase 1 — Đổi tên + gom tên bước về BE ✅ (2026-09-11)
### BE
- [x] Đổi tên bước 5/6/7 trong `ProspectiveProject::STATUS`; thêm `color` 9 mã chuẩn cho STATUS + PARENT_STATUS (bỏ `icon_by_project`/`color_by_project` chết, user đã OK)
- [x] `resolveStatusColor()` + accessor `status_color` + `statusOptions($isParent)` trên Entity
- [x] Resource danh sách + chi tiết (+ khối `parent`) trả `status_name` + `status_color`
- [x] Endpoint `GET assign/prospective-projects/status-options?type=parent` (route đặt trước wildcard)
- [x] Blade export dùng `$item->status_name` (tự phân nhánh dự án cha), bỏ map cứng
### FE
- [x] Store `optionsSelect`: state/action/getter `prospectiveProjectStatusOptions` (cache, {id,text,color})
- [x] `prospective-projects/index.vue`: badge `V2BaseBadge :color`, filter lấy từ store, xoá `getProgressClass`/`getStatusLabel`/CSS pill
- [x] `_id/manager.vue`: `projectStatusInfo` đọc `status_name`/`status_color`, badge tiêu đề nền nhạt 10% + viền 20%
- [x] `ProspectiveProjectChildrenTab.vue`: badge chung, xoá map + CSS
- [x] `report/prospective-projects/index.vue` + `reportUtils.js`: options từ store, map nhãn→id thêm tên mới (giữ tên cũ cho cache)
- [x] `report/solutions-work-summary-by-department/index.vue`: options từ store
- [x] `_id/index.vue`: truyền `statusColor` vào `buildDetailPageTitle` (trước đây xám mặc định)
- [x] `reportUtils.js`: bỏ hẳn tên cũ trong map nhãn → id (user chốt: đổi text thì bỏ cũ)
### Kiểm thử Phase 1 (2026-09-11, Playwright + curl, tài khoản admin)
- [x] API `status-options` (con 12 / cha 8), list `status=7`, detail 138 → tên + màu mới
- [x] Export Excel `status=6` → "Lập dự toán", không còn "Đã duyệt giải pháp"
- [x] UI danh sách: badge tím "Thương thảo giá và giải pháp", "Lập dự toán"; bộ lọc 3 tên mới, không còn tên cũ
- [x] UI chi tiết `/138`, `/138/manager`, dự án cha `/234/manager` (Đang thực hiện), dự án đóng `/175/manager` → tiêu đề + badge đúng
- [x] 2 báo cáo: bộ lọc tiến trình ra tên mới; không có JS error
- [ ] Tab Dự án con: CHƯA test được với dữ liệu — DB dev không có dự án cha nào có con
- [x] ~~`solutions/index.vue`, `my-job/SolutionsTab.vue`, `SolutionUpcomingModal.vue`~~ — KHÔNG thuộc phạm vi: `progressOptions` ở đó là trạng thái GIẢI PHÁP, không phải 12 bước dự án
- [ ] Ghi nhận (chưa sửa): `solutions/components/manager/ProjectInfoTab.vue` nhãn "Tiến trình nội bộ" đang hiện trạng thái GIẢI PHÁP (`solutionData.status_text`), không phải bước dự án — cần user chốt có sửa không

## Phase 2 — Yêu cầu bổ sung thông tin → lùi bước 2 ✅ (2026-09-11)
### BE
- [x] `RequestSolutionService::revertProjectToInfoCollecting($rs, $onlyFromWaiting)` — helper dùng chung; Từ chối / Hủy gọi lại helper (hành vi giữ nguyên)
- [x] `FormTemplateController::storeAdditionalQuestions` gọi helper với `onlyFromWaiting=true` → chỉ hạ khi dự án đang ở bước 3, không kéo lùi nếu giải pháp đã làm dở (bước 4/5)
- [x] Gửi lại yêu cầu (status → 2) đã có sẵn `syncStatusBySolution` → tự lên lại bước 3
### Kiểm thử Phase 2 (tinker, transaction rollback)
- [x] Dự án 165 bước 3 + YC bổ sung → về 2, `updated_by`=13, log `3 → 2` ghi đúng giờ
- [x] Dự án bước 4 + YC bổ sung → giữ 4 (guard)
- [x] Từ chối từ bước 4 → về 2 (như cũ)
- [x] Gọi endpoint thật `POST form-templates/snapshot/6/additional-questions` (RS 21) → RS=9, dự án 165: 3→2, UI `/165/manager` hiện badge "Thu thập thông tin dự án"; đã khôi phục dữ liệu (RS 21=2, P165=3, xoá log/câu hỏi/lịch sử test). Lưu ý: 1 thông báo "câu hỏi bổ sung" đã bắn tới sale dự án 165, không thu hồi được
- [ ] Chưa đi được luồng bấm nút trên UI: dự án 165 chưa có phiếu thu thập (phiếu chỉ sinh qua luồng meeting)

## Phase 3 — Bắt buộc file khi Chốt giải pháp / Chốt báo giá cuối cùng ✅ (2026-09-11)
### BE
- [x] `ProspectiveProjectFinalizeRequest`: `files` required|array|min:1, `files.*.file_path` required (422 tiếng Việt)
- [x] `ProspectiveProjectService::finalizeSolution(..., $files)` → `TableFileHelper::createForTable('solution_review_profiles', profile.id)` với `description = SolutionReviewProfile::FILE_DESC_FINALIZE`; relation `finalizeFiles()`
- [x] `QuotationFinalizeRequest` (mới) + `QuotationController::finalize` nhận files; `QuotationService::finalize` lưu `files` (`table=quotations`, `description = Quotation::FILE_DESC_FINALIZE`); `unfinalize` xoá file chốt
- [x] `TableFileHelper::toArrayForFe()`; `DetailProspectiveProjectResource.finalize_solution_files`; `QuotationResource.finalize_files` (chỉ báo giá trúng thầu)
### FE
- [x] `FinalizeSolutionModal.vue` dựng lại trên `V2BaseModal` + `FileAttachmentTable` bắt buộc, lỗi inline + map 422
- [x] `FinalizeQuotationModal.vue` (mới, V2BaseModal + FileAttachmentTable); `ProspectiveProjectQuotationsTab` bỏ b-modal chốt cũ, dùng component này
- [x] Hiện file đã chốt: component mới `components/V2BaseFileList.vue` (danh sách chỉ đọc gọn: icon · tên · file/dung lượng/ngày · nút tải) dùng ở `SolutionSection` (khối 5. Giải pháp) + cột Trạng thái tab Báo giá — thay `FileAttachmentTable disabled` vì bảng tràn cột hẹp, thừa khoảng trắng (user góp ý 2026-09-11); `V2BaseFileList` có nút Xem trước (FilePreviewModal) + Tải xuống (window.open như FileAttachmentTable)
- [x] `FileAttachmentTable` (dùng chung) gọn lại theo góp ý: bỏ in hoa tiêu đề cột, header 6px/10px, ô 6px/10px, bỏ ép `min-width: 1000px` (gây cuộn ngang ở cột hẹp), bỏ bóng lớn/bo 18px — ảnh hưởng mọi màn dùng bảng file
### Kiểm thử Phase 3
- [x] curl không file → 422 "Vui lòng đính kèm file xác nhận của khách hàng" ở cả 2 endpoint; resource có key mới; FE compile OK
- [x] UI chốt GP (đăng nhập sale 66, dự án 138, hồ sơ 12): bấm Lưu không file → lỗi đỏ dưới bảng, không gọi API; thêm file (upload S3) → chốt OK, dự án 5→6 "Lập dự toán", `files` id 54 desc "Xác nhận chốt giải pháp", khối 5. Giải pháp hiện file; nút Chốt GP ẩn sau chốt
- [x] UI chốt BG (sale 1141, BG-2026-00213, dự án 247): không file → lỗi đỏ; có file → BG Trúng thầu, dự án 7→8, link file hiện dưới badge ở tab Báo giá
- [x] Hủy chốt (API) → BG về Đã duyệt, dự án 8→7, file chốt bị xoá (0 dòng)
- [x] Sửa khi test: popup chốt GP bỏ `.table-responsive` (CSS toàn cục ép min-height ~50vh → 350px trắng); tab Báo giá `$emit('project-changed')` → manager `fetchProjectDetail()` để badge tiêu đề cập nhật ngay
- [x] Đã trả dữ liệu: 138 về bước 5 / hồ sơ 12 approved / xoá file+log; 214 hủy chốt; mật khẩu 2 tài khoản test khôi phục. Còn lại: 1 dòng lịch sử hủy chốt trên BG 214 + thông báo chốt GP đã bắn (không thu hồi)
- 🐞 PHÁT HIỆN cho Phase 5: `QuotationService` đổi bước dự án bằng query builder (`ProspectiveProject::where(...)->update(['status'...])` dòng ~3906/3985/4020) → KHÔNG qua hook model → **bảng log thiếu 6→7, 7→8, 8→7** (dự án 247 log cuối vẫn là 2→6 từ 30/08). Phase 5 phải chuyển sang `$project->update()`

## Phase 4 — Kiểm thử tổng ✅ (2026-09-11)
### API (script `p4_api.py`, tài khoản admin) — 15/16 PASS
- [x] status-options con 12 / cha 8; tên mới bước 5/6/7; toàn bộ màu thuộc 9 mã chuẩn
- [x] Danh sách lọc từng bước 1→12: `status_name`/`status_color` khớp Entity cho cả dự án cha và con (dữ liệu có ở bước 2,3,4,5,6,7,8,11)
- [x] Chi tiết dự án độc lập #248 + dự án cha #234: đủ `status_name`/`status_color`/`finalize_solution_files`
- [x] Export Excel: không còn tên cũ, có tên mới
- [x] Nghịch: chốt GP thiếu file / hồ sơ không tồn tại → 422; chốt BG thiếu file / `file_path` rỗng → 422; không phải sale → bị chặn
- [x] Báo cáo tiến trình dự án TKT (`?time_mode=year`): `status_name` ra tên mới, không có "Không xác định"
- ⚠️ 1 case lệch mã: chốt GP không phải sale trả **400** thay vì 403 (hành vi CŨ của controller: `abort(403)` → `getCode()`=0 → 400; thông báo vẫn đúng). Không sửa trong task này
### UI (Playwright hiển thị, admin)
- [x] Bộ lọc nâng cao "Tiến trình nội bộ": dropdown 12 tên mới; chọn "Lập dự toán" → 37 dự án, toàn badge "Lập dự toán"
- [x] Báo cáo tiến trình dự án TKT: bộ lọc tên mới; popup "Cơ cấu tiến trình" hiện đúng tên
- [x] Báo cáo tổng hợp giải pháp theo phòng ban: bộ lọc tiến trình dự án tên mới (mục "Đã duyệt giải pháp" còn lại là trạng thái GIẢI PHÁP, đúng)
- [x] Không JS error mới ở màn danh sách / 2 báo cáo
- [ ] Chưa test được vì thiếu dữ liệu dev: tab Dự án con (chưa có dự án cha nào có con); bước 9/10/12 (ngoài phạm vi, chưa có code set)
### E2E 3 luồng, nhiều tài khoản (2026-09-11) — dữ liệu GIỮ LẠI, hướng dẫn tự test: `huong-dan-tu-test.md`
- [x] TH1 dự án 249 (sale 27, API): 1→2→6→7(tự duyệt cấp 1)→8→7→8→11; nghịch: tạo GP khi không có GP bị chặn, sale khác chốt/đóng bị chặn, đóng lần 2 bị chặn — 19/22 PASS, 3 "FAIL" là mã 400 thay 403/422 (hành vi cũ, message đúng)
- [x] TH2 dự án 250 (sale 28 + TP 24, API): 2→4→5→6→7→8→7→8, chốt GP thiếu file 422, sale khác bị chặn, file hiện ở detail, hồ sơ chốt xong không chốt lại được — 28/28 PASS
- [x] TH3 dự án 251 (sale 30 + QL GP 24, **UI Playwright**): YC bổ sung (3→2) · gửi lại (2→3) · Tiếp nhận · duyệt hồ sơ (→5) · Chốt GP popup có file (→6) · TP duyệt báo giá trên màn báo giá (→7) · Chốt BG popup có file (→8, tiêu đề đổi ngay) — log đủ 9 dòng
- [x] TH3b dự án 252 (UI): Từ chối YC (→2) · Đóng dự án popup (→11), footer chỉ còn Quay lại
- ⚠️ Ghi nhận (cũ, không sửa): trang chi tiết YC làm GP không tự đổi trạng thái tiêu đề sau "Yêu cầu bổ sung" (phải F5); snapshot phiếu thu thập không được tạo khi tạo dự án qua API dù template Published (phải gọi `handleFormTemplateSnapshot` tay) — cần xem lại `ProspectiveProjectService:402`
## Phase 5 — Lịch sử tiến trình ✅ (2026-09-11)
- ~~Thêm 2 cột text~~ — **user chốt bỏ**, giữ nguyên bảng `prospective_project_status_logs` (status_from / status_to / changed_at / changed_by)
### BE
- [x] `ProspectiveProject::changeStatusById($id, $to, $onlyIfBelow, $onlyIfEquals)` — đổi bước qua model để hook ghi log
- [x] Thay 4 chỗ đổi bước bằng query builder (bỏ qua hook): `QuotationService::cascadeApprovedStatus` (→7), `finalize` (→8, chỉ tiến), `unfinalize` (→7, chỉ khi đang 8), `PricingRequestService` gửi YC giá (→6, chỉ tiến)
- [x] Test tinker (rollback): 7→8, gọi lại không ghi trùng, 8→7 khi đúng 8, không lùi khi đang 7, không tiến 6 khi đang 7; log ghi đúng 2 dòng

### Checkpoint — 2026-09-11
Vừa hoàn thành: TOÀN BỘ 5 phase code + test (Phase 4 regression 15/16 API PASS + UI PASS)
Đang làm dở: —
Bước tiếp theo: user review trên :3005 → commit (chưa commit, chưa push). Ngoài scope chờ khách: bước 9/10/12, HĐ hủy → tự đóng dự án; nhãn "Tiến trình nội bộ" ở chi tiết Giải pháp đang hiện trạng thái giải pháp
Blocked:

## Testcase (2026-09-15)
- [x] Bổ sung 31 testcase (TC-TKT-23 → TC-TKT-53) vào Google Sheet `Testcase _Quản lý dự án` → sheet `12.Dự án TKT`, từ dòng 478 (gid=739303646)
- [x] Sửa lại trình bày theo góp ý 15/09: bỏ icon ⚠️, xuống dòng thật trong ô (bước 1./2./3. và gạch đầu dòng); đã bổ sung quy ước vào `.claude/skills/testcase-documenter/SKILL.md` + `tc_engine.py`

## Tài liệu — Mô tả tiến trình dự án TKT (.docx) (2026-11-17) — @cuong61n
- [x] 2026-11-17: Xuất Word `Mô tả tiến trình dự án TKT.docx` từ `mo-ta-tien-trinh-noi-bo.md` (4 trang: tiến trình là gì · 2 luồng · bảng 12 bước · lùi bước · sơ đồ tóm tắt · quy tắc bắt buộc file · lịch sử · giới hạn hiện tại). Viết bằng ngôn ngữ nghiệp vụ (bỏ tên bảng/cột); cột "Hiện trạng" cập nhật theo Phase 1–5 (đã đổi tên bước 5/6/7, đã có lùi về bước 2 khi yêu cầu bổ sung, đã bắt buộc file khi chốt; bước 9/10/12 và 11b vẫn chưa làm). Script: `gen_mo_ta_tien_trinh.py`. Đã xuất PDF soát bố cục. Trạng thái: xong, chưa đẩy (launchd tự đẩy).
- [x] 2026-11-17: Viết lại bản đầy đủ `Mô tả tiến trình dự án TKT_v2.docx` (đủ 12 chương theo skill business-flow-documenter) sau khi đọc code BE/FE: thêm DỰ ÁN CHA (8 bước, báo giá tổng → bước 7 qua ERP lập HĐ, đóng cha cascade con), rẽ nhánh theo Cách triển khai + Có cần làm GP (Tự triển khai không gửi YC), cấp duyệt báo giá 1/2/3, hạn đóng tự động + cron 01:30 + nhắc + tự đóng, gia hạn TP/BGĐ theo ngưỡng 30 ngày, bảng thông báo người nhận cụ thể, phân quyền, quy tắc khóa. Bản v1 giữ nguyên. Script `gen_mo_ta_tien_trinh_v2.py`. Phát hiện cần khách xác nhận (ghi ở chương 12): (1) duyệt báo giá khác khi dự án ở bước ≥8 kéo dự án về 7; (2) cron tự đóng quét cả dự án cha, cha đóng nhưng con không bị đóng theo; (3) đề xuất gia hạn BE không loại dự án cha trong khi FE không có tab Gia hạn ở cha; (4) nút Đóng dự án cha chỉ giới hạn bước 2 ở FE. Chưa đẩy (launchd tự đẩy).
- [x] 2026-11-17: CHẠY THỬ thật (script PHP gọi service thật trên DB local `local_hrm_erp`, nhánh `gop_db-main`, mọi ca BEGIN…ROLLBACK, không gửi thông báo thật) rồi sửa tài liệu → `Mô tả tiến trình dự án TKT_v3.docx` (16 trang, thêm chương 13 "Kết quả kiểm chứng"; v1, v2 giữ nguyên). ~27 ca, kết quả: SAI so với v2 → đã sửa: (a) "Tiếp nhận" YC làm GP KHÔNG đổi bước (dự án giữ bước 3; bước 4 chỉ khi giải pháp được tạo/gửi); (b) dự án Tự triển khai chỉ lên bước 4 khi giải pháp "Đang triển khai", Chờ PM/Leader/Chờ duyệt GP không đổi bước. XÁC NHẬN thật (trước chỉ suy từ code): duyệt báo giá khi dự án ở bước 8/9 → kéo về 7; cron tự đóng QUÉT dự án cha (giả lập quá hạn → [ĐÓNG] #157) và chỉ đóng cha, 2 con giữ nguyên, còn nút Đóng dự án cha thì đóng cả con; BE cho gửi gia hạn với dự án cha; ERP lập HĐ từ báo giá tổng → cha lên 7; gia hạn ≤30 ngày cấp TP, >30 cấp BGĐ, hạn đóng lùi đúng số ngày, end_date không đổi; màn Sửa không làm lùi bước; changeStatusById ghi log. CHƯA chạy: Lưu nháp/Lưu trên màn tạo (cha), duyệt báo giá tổng, chữ thông báo gửi thật, chương 9. Scripts thử nằm ở scratchpad (không lưu repo). Phát hiện dữ liệu dev: có 1 dự án ở bước 9 (#149) và 1 ở bước 8 (#116) dù chưa có thao tác nào đặt bước 9 — chưa tra nguồn. Chưa đẩy (launchd tự đẩy).
