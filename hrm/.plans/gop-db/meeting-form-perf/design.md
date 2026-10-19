# Design (ĐỀ XUẤT — chưa duyệt) — Giảm request khi mở màn Sửa / Chi tiết meeting

Phụ trách: @dnsnamdang · Nhánh `gop_db` (hrm-client là chính, hrm-api một phần) · Ngày khảo sát: 19/10/2026
Liên quan: `.plans/gop-db/meeting-form-redesign` (việc tồn "gộp ~25 API") · app di động chờ web xong (`.plans/app-meeting-mobile`)

> ⏸ **HOÃN 19/10/2026** — user: "lưu lại làm sau, tôi xử lý UI trước". Khi quay lại: hỏi phép Phase A (phạm vi ở mục 4) rồi mới code.
>
> Chưa được phép code. Mọi phase phải hỏi riêng kèm phạm vi, chờ câu "làm".

## 1. Số đo (Playwright, Chrome headless 1440, local `artisan serve` 4 worker, tài khoản e2e, F5)

| Màn | Request | Dung lượng | Chi tiết meeting về lúc | Request cuối xong lúc |
|---|---|---|---|---|
| Sửa — meeting 6356 (không dự án) | **29** | 2,2 MB | **14,1 s** (gửi lúc 4,2 s) | 17,3 s |
| Chi tiết — meeting 832 (1 dự án) | **39** | 3,7 MB | **13,2 s** (gửi lúc 3,8 s) | 21,9 s |
| Sửa meeting 832 (không có quyền sửa → tự chuyển `/show`) | ~60 | — | nạp HẾT 1 lượt rồi nạp lại lượt 2 | > 22 s |

Gọi riêng lẻ (curl, không tranh chấp): chi tiết meeting **0,39 s** · mọi API danh mục 0,2–0,53 s.
⇒ **Không API nào chậm — chậm vì DỒN SỐ LƯỢNG.** Chi tiết meeting xếp hàng sau ~20 request danh mục nên tốn ~10 s chờ.
(Production nhiều worker hơn nhưng trình duyệt vẫn chỉ mở 6 kết nối/host, nên vẫn xếp hàng.)

Script đo: scratchpad session 19/10 `measure-meeting-edit.js <id> hard|nav edit|show` (đọc storageState `e2e/.auth/user.json`).

## 2. Nguyên nhân (đối chiếu code + số đo)

| # | Nguyên nhân | Chỗ | Request |
|---|---|---|---|
| N1 | Chi tiết meeting gọi ở `mounted()` của PAGE → chạy SAU mounted của mọi component con → xếp cuối hàng | `_id/edit.vue:30` (show.vue tương tự) | đẩy chi tiết từ 0,4 s → ~10 s |
| N2 | Tab ẩn dùng `v-show` → dựng + nạp danh mục ngay cả khi chưa mở | `MeetingForm.vue:109/120/129/139` | ~15 |
| N3 | `PopupStaff` dựng 2 lần (Nhân sự + Biên bản), mỗi lần 3 request, cache store không kịp chặn (cùng tick) | `PopupStaff.vue:659-661` | 6 (3 trùng; `all-working-positions` 246 KB × 2) |
| N4 | `CreateTaskModal` nạp danh mục ở `created()` dù popup đóng — chuỗi tuần tự 3 bước | `CreateTaskModal.vue:1915-1917` (qua MeetingReport + TaskListTab) | 3–6 |
| N5 | `ImportResultModal` trong tab Nhiệm vụ nạp `prospective-projects/getAll?per_page=10000` **1,2 MB** | `ImportResultModal.vue:1454` | 1 (nặng nhất) |
| N6 | 5 danh mục dự án nạp dù meeting KHÔNG có dự án (tab còn ẩn bởi `hasProjects`) | `MeetingProject.vue:477-481` | 5 (applications 389 KB, industries 218 KB) |
| N7 | `meeting_types/getAll` gọi 3–5 lần (MeetingForm + GeneralInfo + include_ids sau khi chi tiết về) | `MeetingForm.vue:1285`, `GeneralInfo.vue:1312/1159` | 2–4 thừa |
| N8 | 2 request lấy về KHÔNG dùng: `getListCustomer?q=` (`filteredCustomers` không ai đọc), `meeting/rooms/bookable` (`bookableRooms` chỉ gán) | `GeneralInfo.vue:1298/1923` | 2 |
| N9 | Màn Sửa nạp đủ rồi mới biết `can_edit=false` → chuyển `/show` nạp lại lượt 2 | `_id/edit.vue:55` | gấp đôi |
| N10 | `solutions/getAll?per_page=10000`, `tasks/getAll?per_page=10000` tải cả bảng | `GeneralInfo.vue:1247`, `CreateTaskModal.vue:2508` | 2 |
| N11 | BE `getDataForShow` chạy `DB::table()->first()` theo từng dự án trong vòng lặp (N+1) | `MeetingService.php` ~972-1012 | — |
| N12 | Danh sách nhiệm vụ của meeting gọi 3 lần ở màn Chi tiết | `TaskListTab` | 2 thừa |

## 3. ⚠️ Ràng buộc — KHÔNG được chuyển tab sang `v-if` (mở mới dựng)

Lúc Lưu, `MeetingForm` đọc payload từ component tab:
- `MeetingForm.vue:778` `formData.projects = this.$refs.meetingProject.getProjectData()`
- `MeetingForm.vue:790 / 1073` đọc khảo sát qua `this.$refs.meetingReport.$refs.investmentSurvey`

Từ đợt U1 (14/10), BE **xoá liên kết dự án không có trong payload**. Tab Dự án TKT chưa dựng ⇒ thiếu `projects` ⇒ Lưu
là **xoá âm thầm dự án đã gắn**. ⇒ Giữ `v-show` (tab vẫn dựng), chỉ **hoãn phần NẠP DANH MỤC** tới khi tab được mở / popup được bật.

## 4. Đề xuất theo phase (thứ tự = lợi lớn, rủi ro thấp trước)

### Phase A — FE màn meeting (chỉ file của màn meeting, không đụng component dùng chung)
1. **Gọi chi tiết TRƯỚC** (N1, N9): page `edit.vue` / `show.vue` gọi chi tiết ở `created()` và chỉ render `MeetingForm` khi đã có dữ liệu
   (`v-if="loaded"`). Kéo theo: `can_edit=false` chuyển `/show` TRƯỚC khi con nào dựng → hết nạp đôi; `include_ids` loại meeting có ngay từ lần gọi đầu.
2. **Loại meeting nạp 1 lần** ở `MeetingForm`, truyền xuống `GeneralInfo` qua prop (N7).
3. **Bỏ 2 request không dùng** (N8) — grep chắc chắn không ai đọc trước khi gỡ.
4. **Tab Dự án TKT**: 5 danh mục chỉ nạp khi `form.projects.length > 0` VÀ tab được mở lần đầu (N6). Kiểm `getProjectData()` không cần danh mục.
5. **Tab Biên bản**: khảo sát đầu tư (`investment-scopes`) giữ nguyên (cần cho validate Hoàn thành) — chỉ đổi điều kiện tính `isProductIntroType` dùng `meeting_type_code` của chi tiết thay vì chờ danh sách loại.

Ước tính sau Phase A (màn Sửa, F5): 4 khung chung + chi tiết + ~8 danh mục còn lại (PopupStaff/CreateTaskModal chưa sửa) — chi tiết về ~0,5 s sau khung chung thay vì ~10 s.

### Phase B — Component dùng chung (PHẢI hỏi riêng, ảnh hưởng màn khác)
6. `PopupStaff`: nạp `getDataStaff` + 2 danh mục khi `show` modal (đã có `onModalShow`) thay vì `mounted` (N3).
7. `CreateTaskModal`: chuyển `loadSelectOptions` + `tasks/getAll` từ `created()` sang lúc mở popup (đã có `onShown`/`loadInitialOptions`) (N4).
8. `ImportResultModal`: nạp danh sách dự án khi mở popup (N5).
9. `TaskListTab`: chặn gọi danh sách 3 lần (N12).
   ⇒ Cần rà mọi màn đang dùng 4 component này (tasks/index, my-job, solutions…) + Playwright từng màn.

### Phase C — BE / tìm phía server (tuỳ chọn)
10. `solutions/getAll?per_page=10000`, `tasks/getAll?per_page=10000` → ô chọn tìm phía server (`V2BaseSelectRemote`, như đã làm ô Dự án TKT) (N10).
11. Bỏ N+1 trong `getDataForShow` (nạp sẵn applications / customer_scope_groups / customer_scopes 1 lần) (N11).
12. Bật lại cache store cho scopes / industries / applications / customer-scopes / priority-levels — **cần tra vì sao bị comment** (có thể cố ý để danh mục khoá/mở hiện đúng) trước khi bật.

Không đề xuất endpoint gộp `form-options`: sau A + B chỉ còn vài request, gộp thêm lợi ít mà tạo endpoint phải bảo trì song song.

## 5. Kiểm chứng khi làm
- Đo lại bằng script: số request, dung lượng, mốc chi tiết về — so với bảng mục 1 (6356 Sửa, 832 Chi tiết, 832 Sửa→show).
- Ca hồi quy bắt buộc: Lưu meeting có dự án mà KHÔNG mở tab Dự án TKT → dự án vẫn còn (đọc DB / chi tiết).
- Lưu / Hoàn thành có khảo sát đầu tư mà không mở tab Biên bản → khảo sát không mất, validate vẫn chặn đúng.
- e2e: meeting-target, meeting-participants, meeting-host, meeting-investment-survey, tab-navigation (+ màn dùng component Phase B).

## Câu hỏi cần chốt
(xem plan.md / hỏi user lần lượt)
