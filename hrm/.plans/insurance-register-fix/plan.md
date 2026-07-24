# Plan — Fix màn Đăng ký bảo hiểm (/decision/insurance/add)

## Phase 1 — Fix crash khi thiếu Chức vụ/Phòng ban/Công ty (Bug A)
- [x] FE: `FormComponent.vue` mounted() null-guard `currentWorkingPosition/currentDepartment/currentCompany/currentEmployeeInfo` trước khi đọc `.code`/`.name`
- [x] Verify local: NV work_position=null (uyendtt.hr) vào màn không crash, form render đầy đủ (console 0 error)

## Phase 2 — Fix "Chế độ được hưởng" không đổi thông tin đăng ký (Bug B)
- [x] FE: `SingleEmployeeInsurance.vue` `onProgramRewardConditionChange` khớp program-relation theo `text` (fallback `insurance_package_detail_id == $event.id`) — vì id reward (14) ≠ detail_id (13) trong package program relations
- [x] Verify local: chọn 4B → "Chương trình đăng ký"=4B/phí 1.647.566; 3B → 3B/phí 2.613.489; đổi qua lại đúng (UI click thật + state)

## Phase 3 — Fix "Công ty chi trả" sai khi đổi Chế độ được hưởng (Bug C)
- [x] FE: `SingleEmployeeInsurance.vue` `onProgramRewardConditionChange` gán `program_relation_fee = $event.price` ĐỒNG BỘ + reactive (`this.$set`), bỏ `$nextTick` — để `calcTotalFee` tính công ty chi trả đúng ngay trong render (không dùng giá chế độ cũ)
- [x] Verify local (UI click thật): chọn 3B → Công ty chi trả = 2.613.489, NV = 0; 4B → 1.647.566, NV = 0 (không có gói bổ sung)

## Phase 4 — Fix BE store crash khi NV thiếu Chức vụ/Phòng ban (Bug D)
- [x] BE: `InsuranceService::store` + `update` null-guard `$department/$company/$workingPosition` trước khi đọc `->code/->name` (fix cả 2 method); `?? ''` cũ sai precedence không bảo vệ null
- [x] Verify local (UI thật): uyendtt.hr (work_position=null) bấm "Lưu và gửi duyệt" → confirm popup → POST 200, tạo phiếu PDKBH_00002, working_position_name = '' (test record còn trong DB local)

## Phase 5 — (ĐÃ HỦY / REVERT) Đổi cách chọn mức "Chế độ được hưởng"
- [x] Từng thử đổi getRewardCondition sang "lấy mức thâm niên cao nhất" → user quyết định GIỮ NGUYÊN logic ban đầu (ưu tiên quy chế khớp ĐẦU TIÊN theo id)
- [x] Đã REVERT: `getRewardCondition` trở lại foreach return-first; gỡ helper `getSeniorityThreshold`. Verify: EG-041→4B (reg13), EG-007→4B+3B (reg10)
- Ghi chú: NV thâm niên ≥60 vẫn chỉ thấy gói của quy chế mốc thấp nhất khớp (theo yêu cầu). Nếu sau này cần đổi → xem lại Bug E trong git history session này.

## Phase 6 — Note thứ tự điều kiện khi tạo quy chế bảo hiểm
- [x] FE: thêm note info-box ở `AddInsuranceModal.vue` (đầu modal, dưới "Loại bảo hiểm", `v-if="!isShow"`): NV thỏa nhiều điều kiện → hệ thống áp dụng điều kiện KHỚP ĐẦU TIÊN (thứ tự từ trên xuống mỗi chức vụ); sắp điều kiện ưu tiên cao lên trước
- [x] Verify local: mở "Chế độ bảo hiểm theo cấp bậc" → Tạo mới → note hiện rõ (ảnh)
- [x] FE: thêm note tương tự ở `Insurance.vue` (đầu tab "Chế độ bảo hiểm theo cấp bậc" trên màn tạo/sửa quyết định, `v-if="!isShow"`) — verify hiện đúng trên màn general/add

## Ghi chú
- Component tương tự (`insurance-out-companies`, `reports/insurance-register`) KHÔNG dính 2 lỗi này (grep sạch).
- Bug B gốc là data: quy chế bảo hiểm trỏ tới `insurance_package_detail` (id 14) khác row với package program relations (id 13) dù trùng tên → khớp theo tên là fix FE an toàn không đụng BE/data.

### Checkpoint — 2026-07-10
Vừa hoàn thành: Fix + verify local cả Bug A (crash null Chức vụ) và Bug B (map Chế độ được hưởng).
Đang làm dở: (không)
Bước tiếp theo: user verify trên browser; cân nhắc chuẩn hoá BE `get-reward-condition` trả đúng khóa map (tùy chọn).
Blocked:
