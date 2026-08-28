# Danh sách phải kiểm BẰNG MẮT cuối Phase 6 (user làm)

Bối cảnh: DB local `hrm_tpe` chỉ có **1 lĩnh vực kinh doanh nội bộ có nhóm ngành con**, chứa **22 nhóm ngành** → bảng sẽ là 1 nhóm 22 dòng. Muốn thấy hiệu ứng gom nhóm nhiều lĩnh vực thì phải gán bớt vài nhóm ngành sang lĩnh vực khác trước khi xem.

## Tab Biên bản (Task 6.5)

1. Đường kẻ `group-break` giữa 2 nhóm lĩnh vực: nhìn ra **1 đường đậm gọn** hay bị **2 đường chồng sát** (1px xám nhạt của `border-bottom` + 2px xám đậm của `border-top`)? Nếu chồng → sửa 1 dòng CSS trong `MeetingInvestmentSurvey.vue`.
2. Cột Lĩnh vực: nhóm 1 hàng (nhãn cùng hàng input) vs nhóm nhiều hàng (nhãn lửng trên, các hàng dưới trống) — căn dọc có ổn không.
3. Không có nhãn lĩnh vực lặp bất thường ở các dòng giữa nhóm.
4. Dòng ảo (nhóm ngành đã bị xoá khỏi danh mục nhưng meeting còn lưu): hiện đúng tên gốc, checkbox khoá không cho tích lại.
5. Bảng 5 cột không lẻ hàng; tích 1 dòng → 2 ô Mức đầu tư/Thời gian bật lên; bỏ tích → trắng lại và khoá.

## Bản in biên bản (Task 6.6)

6. `rowspan` khi bảng bị **ngắt trang** giữa một nhóm lĩnh vực — review tĩnh không kiểm được, phải in thử meeting có nhiều nhóm ngành.
7. Bảng 5 cột không tràn lề ngang; ô Lĩnh vực gộp dọc căn giữa nhìn ổn.

## File Excel biên bản (Task 6.7)

8. Mở file Excel thật: 5 cột đúng, cột D là **số** (SUM chạy được), `#,##0`, mức đầu tư = 0 hiện "0" chứ không trống.
9. Cột B lặp tên lĩnh vực ở mọi dòng → lọc/pivot trong Excel chạy đúng.
10. Thử đặt tên lĩnh vực/nhóm ngành bắt đầu bằng `=` → mở Excel xem `safeText()` có chặn được không (chống formula injection).

## E2E (Task 6.8)

11. Chạy thật bộ `e2e/tests/assign/meeting-investment-survey.spec.ts` với FE + API cùng chạy.
