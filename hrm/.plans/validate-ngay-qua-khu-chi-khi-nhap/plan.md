# Plan — Chỉ chặn ngày quá khứ khi bản ghi còn ở trạng thái Nháp

Bug: duyệt GP bị chặn bởi validate "Ngày cần xong GP phải >= ngày hiện tại" dù ngày đó nhập từ lúc còn nháp.
Quy tắc chốt: chỉ áp `after_or_equal:today` khi bản ghi trong DB còn ở trạng thái nháp (hoặc đang tạo mới); qua nháp rồi thì giữ nguyên ngày cũ. Copy pattern có sẵn `TaskUpdateRequest::currentTaskIsDraft()`.

## BE (hrm-api)
- [x] `Solution/SolutionRequest.php`: thêm `currentSolutionIsDraft()`, áp cho `internal_need_gp_date` + `modules.*.due_date`
- [x] `ProspectiveProject/ProspectiveProjectRequest.php`: thêm `currentProjectIsDraft()`, áp cho start_date / end_date / customer_need_solution_date / internal_solution_close_date
- [x] `Meeting/MeetingUpdateApiRequest.php`: `reports.*.expected_deadline` chỉ chặn khi meeting còn status 1 (đồng bộ với start_date đã có sẵn)
- [x] `JobRequestController@update`: deadline / time_start_request chỉ chặn khi phiếu còn `JobRequest::DANG_TAO`
- [x] `AssignJobController@update`: deadline / time_start_request chỉ chặn khi phiếu còn `AssignJob::DANG_TAO`

## FE (hrm-client)
- [x] `ProgressFinanceSection.vue`: thêm prop `allowPastDates`; `prospective-projects/_id/edit.vue` truyền theo status gốc
- [x] `meeting/GeneralInfo.vue` + `meeting/MeetingReport.vue`: đổi `disabled-date` inline sang method `disablePastDates` (bỏ chặn khi meeting đã qua status 1)

## Không đổi (cố ý)
Các màn tạo mới bản ghi con ngay lúc thao tác vẫn chặn ngày quá khứ: tạo phiên bản mới GP/hạng mục (`CreateNewVersionRequest`), thêm thành viên (`AddMemberRequest`), hồ sơ nghiệm thu (`StoreReviewProfileRequest`), màn Thêm mới dự án/GP/họp.

### Checkpoint — 2026-08-19
Vừa hoàn thành: toàn bộ task BE + FE ở trên, đã `php -l` sạch.
Đang làm dở: chưa test UI thực tế.
Bước tiếp theo: user xác nhận có cần chạy Playwright kiểm thử luồng duyệt GP không.
Blocked:

## Kết quả test (2026-08-19)

Cách test BE: đẩy request qua HTTP kernel thật (routes + middleware + FormRequest + controller) bằng
token JWT của đúng người có quyền, bọc `DB::beginTransaction()` … `rollBack()` nên **không đổi dữ liệu dev**.
Mỗi nhóm đều chạy 2 lượt: code cũ (git stash) và code mới, để chứng minh đúng chỗ lỗi.

| # | Ca kiểm thử | Code cũ | Code mới |
|---|---|---|---|
| 1-3 | GP #29 (Chờ PM duyệt, ngày cần xong GP 08/08 = quá khứ): PM duyệt / lưu / đổi ngày quá khứ khác | 422 chặn | 200 ✔ |
| 4-5 | GP #29: bỏ trống ngày · ngày sai định dạng | 422 | 422 (vẫn chặn) ✔ |
| 6-7 | GP #7 CÒN NHÁP, ngày quá khứ: lưu nháp · gửi duyệt | 422 | 422 (vẫn chặn) ✔ |
| 8-10 | GP #7 nháp: ngày tương lai · = hôm nay · = hôm qua | 200/200/422 | 200/200/422 ✔ |
| 12-13 | modules.*.due_date quá khứ / tương lai trên GP đã qua nháp | – | qua validate cả 2 ✔ |
| 16-17 | Dự án #199 (status 2, start_date 18/08 quá khứ): lưu nguyên trạng · đẩy hết ngày về quá khứ | 422 chặn | 200 ✔ |
| 18-19 | Dự án #199: end < start · close > need (ràng buộc chéo) | 422 | 422 (vẫn chặn) ✔ |
| 20-23 | Dự án #126 CÒN NHÁP: lưu nháp / gửi duyệt ngày quá khứ · ngày tương lai · = hôm nay | 422/422/200/200 | 422/422/200/200 ✔ |
| 24-26 | YCCV #486 (Chờ duyệt, deadline 24/07 quá khứ): TP duyệt · deadline sai định dạng · thiếu deadline | 422 chặn | 200/422/422 ✔ |
| 27-28 | YCCV #486 hạ về nháp: deadline quá khứ · tương lai | – | 422/200 ✔ |
| 29-31 | Giao việc #355 (Đã duyệt, deadline 27/07 quá khứ): sửa · hạ về nháp quá khứ · hạ về nháp tương lai | 422 chặn | 200/422/200 ✔ |
| 36-39 | Họp #54 (Chốt lịch, đã diễn ra): hạn biên bản quá khứ · tương lai · họp Lên lịch hạn quá khứ · hạn sai định dạng | 400 chặn (ca 36) | qua/qua/400/400 ✔ |

FE (Playwright, đăng nhập thật vào :3000):
- Sửa dự án #199 (đã qua nháp): lịch **0/42 ô bị khoá** → chọn được ngày quá khứ; bấm **Lưu** → thành công, ngày giữ nguyên, `updated_by` ghi đúng.
- Sửa dự án #126 (còn nháp): lịch mở tháng 07 → **42/42 ô bị khoá** ✔
- Thêm mới dự án: **23 ô quá khứ bị khoá** ✔
- Tạo họp mới: **23 ô quá khứ bị khoá** ✔
- Gọi thẳng `disablePastDates` của `GeneralInfo` + `MeetingReport` trong bundle đang chạy: tạo mới/status 1 → chặn quá khứ; status 2/3 → không chặn ✔
- 4 file .vue compile sạch bằng `vue-template-compiler`.

Không kiểm được (thiếu dữ liệu/quyền, đã kiểm bù ở tầng khác):
- GP nháp + hạng mục: mọi GP nháp trong DB đều thuộc dự án "Tự triển khai" nên rule `modules.*` bị bỏ qua sẵn từ trước → đã kiểm ở tầng rule (nháp chặn, đã qua nháp cho qua).
- Duyệt GP trên UI: tài khoản admin không phải PM của GP nào → đã kiểm đủ ở tầng HTTP với đúng tài khoản PM.
