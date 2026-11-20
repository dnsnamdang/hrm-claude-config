# SDD ledger — plan: HRM/.plans/agent-chat/agent/cong-viec-theo-nhan-vien/plan.md
Executor: inline (user "làm" 19/11, không chọn cách ⇒ cách 1 đề xuất). Nhánh gop_db-agent-cong-viec-theo-nhan-vien (api base 729a7ced6 · client base b37aa3b41), đã bỏ upstream để không lỡ push gop_db.
Ruling: không commit theo task (memory "user tự báo commit") — task-start/task-done scripts dựa commit nên ghi ledger tay; review cuối dùng `git diff 729a7ced6` — sai thì chỉ mất tiện truy vết từng task.
Pre-flight: T3←T1 collect(...,$openOnly)+allowedEmployeeIds public: khớp. T3←T2 employeeIds()/period(): khớp. T4←T2,T3: khớp. T5←T4 block work_rank{id,label,department,value,qua_han,ask}: khớp. T4 chi tiết dùng ViecTongHopCuaToiTool::card (public static): có sẵn.
Task 1: complete (chưa commit; tests: OpenOnlyCollectTest 3/3 RED→GREEN; tests/Unit/EmployeeWork* 45/45 OK; tests/Feature/EmployeeWorkPerformance 4 OK + 16 ERROR có sẵn — mọi lỗi là fixture `insert roles` thiếu company_id ⇒ FK roles_company_id_foreign, xảy ra trước khi gọi code)
Task 1: Ruling: chấp nhận 16 lỗi fixture có sẵn, không sửa test cũ (ngoài luồng, ghi danh sách) — thay đổi ở nhánh mặc định là `->when(false, …)` không tác dụng — nếu sai: hồi quy báo cáo không bị test feature bắt, đã giảm rủi ro bằng unit EmployeeWork* xanh.
Ngoài luồng: tests/Feature/EmployeeWorkPerformance/{ReportApi,MeetingCanView,NoPartGroup,WorkingEmployee}Test chèn roles thiếu company_id ⇒ 16 ca lỗi FK trên db_gop_6_11.
Task 2: complete (chưa commit; tests: CongViecTheoNhanVienScopeTest 8/8, RED = class not found → GREEN)
Task 2: Ruling: thêm test + hành vi "không nêu pham_vi ⇒ phạm vi rộng nhất được xem" (allowedEmployeeIds không lọc phòng) — giống luật 15 các công cụ báo cáo; spec chỉ nêu 4 giá trị — sai thì câu "ai quá hạn nhiều nhất" của trưởng phòng sẽ hiện mọi phòng họ quản lý thay vì phòng mình.
Task 2: Ruling: test cấp quyền bằng vai trò TẠM có company_id=1 (không dùng vai trò sẵn có) + xoá cấp sẵn của mã này cho NV — vì roles.company_id có FK và 157 không có vai trò sẵn phù hợp — sai thì chỉ ảnh hưởng test.
Task 2: Ruling: người ngoài phạm vi ⇒ PermissionNeed generic "Nhân viên này không thuộc phạm vi bạn được xem." (không lộ số) — sai thì câu từ chối hơi khác khuôn.
Task 3: complete (chưa commit; tests: CongViecTheoNhanVienStatsTest 6/6, RED = class not found → GREEN; hiệu năng công ty 1 đang tồn < 25 query, < 3s)
Task 3: Ruling: `tong` = Tổng đầu việc của báo cáo (gồm Dừng/Huỷ) để khớp báo cáo; chi tiết không nêu nhóm ⇒ bỏ Dừng/Huỷ — sai thì "tổng việc" lệch kỳ vọng người hỏi vài việc huỷ.
Task 3: Ruling: rank() trả thêm `con_lai` (số người có chỉ số chưa hiện) — cần cho câu "còn N người" như các thẻ khác; không đổi interface đã có.
Task 4: complete (chưa commit; tests: CongViecTheoNhanVienTest 8/8 RED=class not found → GREEN; Personal/Payroll/ScopedToolsTest xanh sau khi cập nhật số công cụ 49/51 + matrix 50)
Task 4: Ruling: trần mô tả công cụ là 600 ký tự (PersonalToolsTest áp cho MỌI công cụ), không phải 1000 như spec — viết gọn mô tả mới (594), viec_qua_han (597), viec_cua_nhan_vien — sai thì không có hại, chỉ là mô tả ngắn hơn.
Task 4: Ruling: hỏi thật thấy "Liệt kê việc quá hạn của X" bị chọn viec_cua_nhan_vien (ví dụ trong mô tả là "việc của anh Nam") ⇒ đổi mô tả công cụ cũ thành "NHIỆM VỤ (tasks only)" + ví dụ "nhiệm vụ của anh Nam", luật 21 thêm "viec_cua_nhan_vien CHỈ khi nói rõ nhiệm vụ" — hỏi lại: việc ⇒ công cụ mới (385), nhiệm vụ ⇒ công cụ cũ.
Task 4: Bộ Agent PHPUnit hết bộ nhớ ở 1G — CÓ SẴN: chạy trên worktree tạm origin/gop_db cũng chết 1G ⇒ chạy 2G.
Task 5: complete (chưa commit; Playwright :3070 NV13 "Top 10 người đang có nhiều việc đang làm nhất": 10 dòng work_rank, chồng lấn 0, scrollWidth=clientWidth 702, tràn dòng 0, "n quá hạn" rgb(220,38,38) ×10, link báo cáo đúng, cursor pointer; bấm dòng 1 ⇒ câu "Việc đang làm của DNS Admin" + thẻ tasks 2 dòng, dòng thẻ cũ is-off 10/10; console 37 lỗi đều ERR_CONNECTION_REFUSED socket/ảnh). Thẻ rank cũ: diff chỉ thêm 64 dòng, 0 dòng xoá; không có dữ liệu tháng 10 để hiện thẻ.
Task 6: work_parity.php NV13 tháng 10 + tháng 11/2026: 408 NV, lệch 0. hoi_that 12 câu + 3 câu sau sửa: 10/12 đúng công cụ + nêu kỳ; "ai đi công tác nhiều nhất" ⇒ thong_ke_cong_tac (giữ); "tôi đang có bao nhiêu việc quá hạn" ⇒ viec_qua_han toi (hành vi cũ, giữ).
PHÁT HIỆN chờ user: chế độ "đang tồn" bị PHIẾU CÔNG TÁC cũ chi phối — 7,738 phiếu qua ngày chưa duyệt kết quả (5,970 ở "Đã duyệt", từ 04/2024) ⇒ top quá hạn toàn CSKH 290–385 phiếu/người.
Final review (opus, read-only, tái hiện bằng tinker): 0 Critical, 2 Important, 6 Minor; 5 điểm Review Focus đều đạt.
Final: fixed I1 hỏi người có xep_theo bỏ người số 0 — test_hoi_nguoi_co_xep_theo_giu_nguoi_so_0 RED→GREEN (rank keepZero cho toi/nguoi)
Final: fixed I2 thiếu pham_vi mà có nhan_vien_ids/phong_ban_id ⇒ trả cả phạm vi — test_thieu_pham_vi_suy_tu_tham_so RED→GREEN (phamVi suy từ tham số) + luật 21 thêm hướng dẫn phòng
Final: fixed (nâng từ Minor 3) chỉ có tu_ngay ⇒ 1 ngày — test_chi_co_tu_ngay_thi_den_hom_nay RED→GREEN (đến hôm nay)
Final: fixed (nâng từ Minor 4) bấm tên hỏi tiếp mất kỳ — test_bam_ten_hoi_tiep_giu_ky RED→GREEN (ask kèm kỳ khi che_do=ky)
Final: minor (deferred): openOnlyFilter() chen giữa docblock và thân makePair() — docblock mồ côi
Final: minor (deferred): hạn Vấn đề chỉ có deadline so giá trị thô, báo cáo coi cả ngày (local 0 bản ghi)
Final: minor (deferred): thẻ work_rank hiện số hạng cả khi so sánh / 1 người (metric null)
Final: minor (deferred): đang tồn với người đã nghỉ trả nguoi [] không câu báo
Final: Ruling (declined list): pham_vi=toi gom việc của mình ở mọi công ty — việc của bản thân, giữ — sai thì người làm 2 công ty thấy cả việc công ty kia khi hỏi "của tôi".
19/11 user "tạm loại phiếu công tác khỏi danh sách công việc" + "làm": LOAI bỏ phieu_cong_tac, ghi_chu_loai trong data, luật 21 nêu 1 lần + đi công tác ⇒ thong_ke_cong_tac; test_hang_so + test_khong_tinh_phieu_cong_tac RED→GREEN; work_parity so với báo cáo types=meeting,task,issue,job: tháng 10 + 11, 408 NV, lệch 0; hoi_that 5 câu đúng.
Deploy: 19/11 ĐÃ DEPLOY PROD TPE api a519d1282 · client fb4f109b4 (Nothing to migrate, site 200).
