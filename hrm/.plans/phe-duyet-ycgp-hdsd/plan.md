# Plan — HDSD màn "Phê duyệt → Yêu cầu giải pháp"

Người phụ trách: @dnsnamdang
Output: `HDSD_luongchinh/HDSD_PheDuyet_YeuCauGiaiPhap.docx`
Ảnh nguồn: `hdsd_ycgp_pending_shots/` (12 ảnh)
Tài khoản chụp: namdangit@gmail.com (DNS ADMIN update) — https://dev-hrm.eteksofts.com/assign/request-solution/pending

## Phase 1: Khảo sát code
- [x] FE: pending.vue, _id/index.vue, RequestSolutionForm.vue, RequestTab.vue, RequestSolutionReceiveModal.vue, formTabInput.vue, FormPreview.vue (phần isAddForm), menu-sidebar.js
- [x] BE: routes api.php, RequestSolutionController, RequestSolutionService (pending/receive/calculateNeedReceiveDate/calculateWarningDate), Entity RequestSolution (STATUSES, isCanReceive, generateCode), RequestSolutionResource (getDeadlineStatus), RequestSolutionReceiveRequest, FormTemplateController::storeAdditionalQuestions
- [x] Luồng ngược: NotifyRequestSolutionDeadlineCommand (cron cảnh báo), SolutionService (updateRequestSolution/destroy), PermissionsTableSeeder (quyền 1012), export blade request_solutions_pending

## Phase 2: Chụp ảnh thật (Playwright MCP, 1440x900)
- [x] 01 tổng quan, 02 bộ lọc nâng cao, 03 popup Tiếp nhận, 04 dropdown chọn PM
- [x] 05 chi tiết tab Thông tin yêu cầu (fullPage), 06 tab Phiếu thu thập, 07 ô nhập câu hỏi, 08 câu hỏi chờ gửi
- [x] 09 Lịch sử thay đổi phiếu, 10 tab Dự án TKT (fullPage), 11 tab Meetings, 12 menu Phê duyệt
- [x] Không thực thi thao tác ghi dữ liệu: popup Tiếp nhận đóng bằng Đóng; câu hỏi bổ sung không bấm gửi

## Phase 3: Dựng Word
- [x] Generator scratchpad `gen_ycgp_pending.py` (dùng hdsd_p5_work/hdsd_lib.py, khung HDSD_DanhMuc/HDSD_VaiTroDuAn.docx)
- [x] TỔNG QUAN (thuật ngữ, giới thiệu, quyền + phạm vi theo implementation_type)
- [x] P1 vì sao cần màn này + vòng đời trạng thái + công thức hạn tiếp nhận
- [x] P2 truy cập & bố cục | P3 lọc | P4 17 cột + nhãn hạn + 3 nút hàng
- [x] P5 chi tiết 4 tab | P6 popup Tiếp nhận (bảng từng trường + mặc định + lỗi) | P7 Yêu cầu bổ sung
- [x] P8 Xuất Excel | P9 thông báo tự động | P10 sau tiếp nhận | P11 FAQ
- [x] Build + verify: 14 Heading 1, 12 hình + 12 caption, 16 bảng, updateFields=true, broken=0, ~1.4MB

### Checkpoint — 27/07/2026
Vừa hoàn thành: HDSD_PheDuyet_YeuCauGiaiPhap.docx (11 phần + tổng quan).
Đang làm dở: không
Bước tiếp theo: user review nội dung.
Blocked:

## Ghi chú phát hiện khi đọc code (không sửa, chỉ báo)
- `RequestSolutionService::receive()` khai `close_solution_date` 2 lần trong cùng mảng → giá trị người dùng chọn ở ô "Ngày dự kiến xong GP (v1)" bị ghi đè bằng `now()`. Tài liệu đã ghi rõ hiện trạng này.
- Popup Tiếp nhận: nhãn "Ngày cần nhận GP nội bộ" đang bind `customer_need_gp_date`, nhãn "Ngày cần tiếp nhận YC" đang bind `internal_need_gp_date` (hoán vị so với tên nhãn).
- `pending.vue` còn code Duyệt/Từ chối bị comment; `canReceive(item)` luôn return true (lọc thật nằm ở BE).
