# Làm giải pháp — rà soát cho TPE SMART AGENT (12/11/2026, ĐÃ CHỐT 5 câu, CHƯA code)

Khung chung user đặt: lãnh đạo xem **số lượng theo phòng / công ty**, **chi tiết theo phòng / công ty**, **theo nhân viên**,
**theo phân loại**, **theo thời gian**.

## 1. Agent đang có gì
- `giai_phap` (11/11): LIỆT KÊ tối đa 20 dòng yêu cầu làm GP (`request_solutions`, quyền "Xem danh sách yêu cầu làm giải pháp")
  hoặc giải pháp (`solutions`, quyền "Xem danh sách làm giải pháp" + nới PM / leader / thành viên qua `SolutionService::index`).
  Lọc: nhóm trạng thái, quá hạn, phòng TIẾP NHẬN, từ khoá. Trả tổng + 20 dòng.
- `du_an_tkt` (sap_toi_han_gp) có hạn KH cần giải pháp của dự án.
- Chưa có: thống kê đếm / gom nhóm; chi tiết 1 giải pháp (hạng mục, thành viên, việc trễ, giờ công); lọc theo PM / người / thời gian.

## 2. Nguồn có sẵn trong hệ thống (đã đọc code + đếm DB local db_gop_6_11)
| Nguồn | Nội dung | Quyền / phạm vi |
|---|---|---|
| `request_solutions` (33 dòng) | trạng thái 1 Nháp · 2 Chờ tiếp nhận · 9 YC bổ sung · 3 Đã tiếp nhận · 4 Từ chối · 6 Đang thực hiện · 8 Hoàn thành · 5 Huỷ · 10 Đóng · 11 Đã chốt GP; `sent_date`, `customer_need_gp_date`, `customer_need_quote_date`, `internal_need_gp_date`, `responded_deadline_status` (1 đúng hạn 17 · 2 quá hạn 2 · trống 14), phòng/người tiếp nhận, PM, nhóm ngành, lĩnh vực | list: "Xem danh sách yêu cầu làm giải pháp" |
| Báo cáo **"Theo dõi giải pháp theo phòng KD"** `SolutionRequestsByDepartmentReportService` | yêu cầu gom Công ty → Phòng KD (phòng NGƯỜI GỬI) → NV gửi; đếm theo trạng thái; lọc lĩnh vực / nhóm ngành / ứng dụng | "Xem báo cáo theo dõi giải pháp theo phòng KD" — phòng mình quản lý / công ty / tập đoàn; không quyền ⇒ yêu cầu mình gửi |
| `solutions` (43: 27 Đóng · 9 Đang triển khai · 4 Đã duyệt GP · 2 Đã duyệt giá · 1 Chốt GP) | PM (32 PM khác nhau), % tiến độ, version hiện tại, phòng, nhóm ngành/lĩnh vực/ứng dụng, dự án TKT, yêu cầu gốc | list: "Xem danh sách làm giải pháp" + PM/leader/thành viên |
| Báo cáo **"Version giải pháp"** `SolutionVersionsReportService` | Công ty → Phòng GP → Giải pháp → Version: **số việc, giờ dự kiến, giờ thực tế, số nhân sự** mỗi version | "Xem báo cáo version giải pháp" — phòng / công ty / tập đoàn; không quyền ⇒ GP mình tạo |
| API màn quản lý 1 GP `v1/assign/solutions/{id}/manager/*` | hạng mục có việc trễ, người trễ việc, thống kê trạng thái việc, việc/vấn đề/meeting sắp tới, nhân lực, việc chờ duyệt, tiến độ theo hạng mục | ⚠️ KHÔNG tự kiểm quyền xem (lỗ hổng #15 còn mở) ⇒ Agent phải tự chặn: GP phải nằm trong danh sách người hỏi thấy |
| `solution_modules` (7) · `solution_members` (50) · `solution_versions` (44) · tasks gắn GP (19) · `bom_lists` (28) | hạng mục (leader, hạn, %), thành viên + vai trò, version | — |

Dữ liệu local mỏng (43 GP, 33 yêu cầu, 7 hạng mục) ⇒ demo thống kê ít số; chi tiết 1 GP chỉ vài GP có hạng mục.

## 3. Đề xuất công cụ (nháp)
| # | Công cụ | Câu trả lời được | Ghi chú |
|---|---|---|---|
| A | `thong_ke_giai_phap` (MỚI) | "Tháng này phòng KD1 gửi bao nhiêu yêu cầu GP, bao nhiêu quá hạn phản hồi?", "Phòng Kỹ thuật đang làm bao nhiêu GP, theo trạng thái", "PM nào đang ôm nhiều GP nhất", "GP theo nhóm ngành năm nay", "Giải pháp nào tốn nhiều giờ công nhất" | đối tượng yêu cầu / giải pháp; nhóm theo phòng / người / trạng thái / nhóm ngành / tháng; số theo đúng báo cáo có sẵn |
| B | `chi_tiet_giai_phap` (MỚI) | "Giải pháp X đang tới đâu, hạng mục nào trễ, ai trễ việc, còn gì chờ duyệt, tốn bao nhiêu giờ?" | gọi lại service màn quản lý SAU khi kiểm GP nằm trong danh sách người hỏi thấy |
| C | `giai_phap` (SỬA) | "Danh sách GP anh Minh làm PM", "Yêu cầu GP gửi trong tháng 9" | thêm lọc người (PM / người gửi / người tiếp nhận) + khoảng thời gian |
| — | KHÔNG làm | giá BOM / giá vốn / giá đề xuất | nhạy cảm (giá vốn) — giữ nguyên nguyên tắc Agent không trả giá vốn |

## 4. Câu cần chốt (hỏi lần lượt)
1. Quyền cho THỐNG KÊ: theo quyền 2 báo cáo có sẵn hay theo quyền danh sách?
2. "Theo phòng" của yêu cầu GP: phòng KD gửi, phòng tiếp nhận, hay cả hai?
3. "Theo nhân viên" của giải pháp: chỉ PM, hay cả leader hạng mục / thành viên?
4. Mốc thời gian: yêu cầu theo ngày gửi; giải pháp theo ngày tạo hay ngày chốt / đóng?
5. Chi tiết 1 GP gồm những khối nào (hạng mục, việc trễ, chờ duyệt, giờ công, thành viên, meeting sắp tới)?

## 5. Đã chốt (user 12/11, cả 5 câu chọn 1)
1. **Quyền thống kê = quyền 2 báo cáo có sẵn**: yêu cầu ⇒ "Xem báo cáo theo dõi giải pháp theo phòng KD"
   (`presale.bao_cao_theo_doi_giai_phap_theo_phong_kd.view`, phạm vi theo PHÒNG NGƯỜI GỬI: phòng quản lý / công ty / tập đoàn,
   không quyền ⇒ yêu cầu mình gửi); giải pháp ⇒ "Xem báo cáo version giải pháp" (`assign.bao_cao_version_giai_phap.view`,
   phạm vi theo phòng GP `solutions.department_id`, không quyền ⇒ GP mình tạo). Số khớp màn báo cáo.
2. **Yêu cầu gom được theo phòng KD gửi VÀ phòng tiếp nhận; NỚI thêm yêu cầu gửi TỚI phòng mình quản lý**
   (`listManageDepartmentIds()` ∋ `receive_dept`) — kết quả ghi rõ "gồm cả yêu cầu gửi tới phòng bạn quản lý" (báo cáo không có phần này).
3. **Theo nhân viên của giải pháp: PM và thành viên (2 cách gom riêng)**; thành viên = `solution_members` còn hoạt động
   (chưa khoá / chưa hết hạn), leader hạng mục tính như thành viên. Yêu cầu: người gửi + người tiếp nhận.
4. **Thời gian**: yêu cầu theo `sent_date`; giải pháp theo `created_at`; thêm chỉ số "được duyệt trong kỳ" theo
   `solution_versions.approved_at` (1 GP tính 1 lần). KHÔNG dùng `close_solution_date` / `end_date` (là ngày DỰ KIẾN).
5. **Chi tiết 1 GP bản gọn**: tổng quan (trạng thái, version, PM, % tiến độ, hạn KH cần) · hạng mục (leader, hạn, %, số việc trễ)
   · người đang trễ việc · việc chờ duyệt · giờ công dự kiến/thực tế + số thành viên. Chặn TRƯỚC khi gọi API màn quản lý:
   GP phải nằm trong `SolutionService::index` của người hỏi (quyền danh sách / PM / leader / thành viên). Tìm theo mã / tên,
   nhiều kết quả ⇒ hỏi lại chọn. Việc/meeting sắp tới để công cụ việc / lịch họp trả lời.
- C (`giai_phap` sửa): thêm lọc người (PM / người gửi / người tiếp nhận) + khoảng thời gian.
- Không trả giá BOM / giá vốn.

## 6. Đã code (12/11/2026, hrm-api nhánh gop_db-tpe-smart-agent, CHƯA commit)
- MỚI `Support/GiaiPhapScope.php`: phạm vi 2 báo cáo (ép công ty đang làm) + nới yêu cầu gửi tới phòng mình quản lý **chỉ khi có
  quyền báo cáo từ phạm vi phòng** — siết thêm so với câu chốt vì `listManageDepartmentIds()` trả cả 39 phòng cho NV 1345 (không quyền)
  và [44] cho NV 62 (nhân viên) ⇒ không gate là lộ. GP "thật" = không nháp + có ≥1 version không nháp (như báo cáo version; loại 3 GP
  đóng khi version còn nháp).
- MỚI `Tools/ThongKeGiaiPhapTool` (`thong_ke_giai_phap`), `Tools/ChiTietGiaiPhapTool` (`chi_tiet_giai_phap`); SỬA `GiaiPhapTool`
  (nhan_vien_id + vai nguoi_gui/nguoi_nhan/pm/thanh_vien, tu_ngay/den_ngay; mô tả 952 ký tự). Registry 43 công cụ (45 có lương).
- Phát hiện: báo cáo version gọi **người tạo** (`created_by`) là "PM" — lệch `pm_id` ở 12/43 GP local. Agent gom theo `pm_id`
  (cột màn danh sách) và ghi chú trong kết quả. Ngoài luồng, chưa sửa báo cáo.
- Đối chiếu: NV 13 yêu cầu 25 = báo cáo (từng phòng gửi khớp 9/9), tháng 9 = 4 = báo cáo; GP 32 / 334 giờ dự kiến / 6 giờ thực tế =
  báo cáo version (NV 13 + NV 59 phạm vi phòng).
- Test `LamGiaiPhapTest` 5 ca (khớp báo cáo; phía gửi/nhận + nới + quá hạn; gom PM / thành viên / duyệt trong kỳ / giờ; chi tiết + chặn
  ngoài phạm vi; giai_phap lọc người/ngày). PHPUnit Agent 212/212.
- Eval +9 (#191–199, 199 câu): 14/14 công cụ; #195 "Giải pháp Vinfast tới đâu" model hỏi lại đúng nhưng kind = ok (kind ask chỉ khi có
  thẻ pick — FE pick chưa có loại giải pháp) ⇒ đề sửa expect ok; làm thẻ chọn GP sau nếu cần (đụng FE).
