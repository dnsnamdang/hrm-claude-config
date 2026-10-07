# Update style các báo cáo cũ — tổng quan

**Nhánh:** `gop_db` (code ở nhánh checkout ra từ `gop_db`) · **Phụ trách:** @namdangit · Mở: 04/10/2026
**Khuôn:** skill `HRM/.claude/skills/report-styles` (mẫu = Báo cáo tổng hợp CSKH tiềm năng, `template/` commit `ae11073e9`)

## Mục tiêu

Chuyển lần lượt các báo cáo cũ của hrm-client sang 1 khuôn chung: bộ lọc nổi có In/Excel trên đầu → khối tổng hợp
`.rsum` → bảng cây `rsum-tb` (dòng TỔNG, ô chọn cấp bung, tiêu đề dính, cuộn ngang 2 thanh) → popup
`V2BaseReportModal`. Mỗi báo cáo là 1 folder con (mockup → design → plan → hỏi "làm" → code), chỉ tạo khi bắt đầu.

## Quy trình mỗi báo cáo (theo skill report-styles mục 5)

1. Liệt kê hiện trạng (bộ lọc, biểu đồ, cột, popup, In/Excel, cách BE phân trang).
2. Hỏi user các điểm NGHIỆP VỤ, lần lượt từng câu; điểm thuần UI thì tự chốt theo khuôn và ghi vào đầu mockup.
3. Mockup từ DOM + CSS thật → user duyệt.
4. design.md + plan.md → hỏi "làm" (repo · nhánh · file · có đụng BE/DB không) → code → kiểm Playwright.

## Theo dõi

| # | Báo cáo | Route | Folder | Trạng thái |
|---|---|---|---|---|
| 1 | Thời gian meeting theo dự án | `/assign/report/meeting-by-projects` | `meeting-by-projects/` | ĐÃ MERGE gop_db 05/10 (api 8de764f79, client 2f04d1dfb) |
| 2 | Thời gian meeting theo nhân viên | `/assign/report/meeting-by-employees` | `meeting-by-employees/` | ĐÃ MERGE gop_db 05/10 (api 9696baa26, client 6c0b509de) + bổ sung lọc trạng thái / popup loại / popup NV tham gia (api 60aa9bfa0, client 81b715269); e2e chưa chạy |
| 3 | Kế hoạch & kết quả làm việc theo nhân viên | `/assign/report/employee-work-performance` | `employee-work-performance/` | ĐÃ MERGE gop_db 06/10 (api 45b8a2b2f, client 88c9f3f01); SRS xong |

## Báo cáo 3 — employee-work-performance: quyết định đã chốt (05–06/10/2026)

Spec: `docs/superpowers/specs/gop-db/2026-10-06-update-style-bao-cao-ke-hoach-ket-qua-lam-viec-design.md`

- Phân trang ở BE theo nhóm Phòng ban (10/20/50/100, mặc định 20); summary + dòng TỔNG tính trên toàn bộ; trang vượt → trang cuối.
- Làm luôn 3 điểm logic: reportSeq/reportParams (chống response cũ đè mới, In/Excel theo bộ lọc đang hiển thị); Excel popup
  tải từ server (`drill/export`); ô Công ty theo `filter-options` + `can_change_company` (luôn false — không có cấp tổng công ty).
- Bộ lọc: Kỳ đứng đầu, Loại công việc đứng cuối dùng `CheckboxMultiSelect` (col 6, chip 1 dòng); "Chỉ hiện nhân viên có việc"
  ở dòng tiêu đề khối tổng hợp cạnh nút Thu gọn.
- Bỏ "Chỉ tính việc chủ trì" (chỉ meeting có chủ trì; ai có tên trong danh sách thực hiện đều tính) và bỏ hẳn cột Vai trò +
  KPI tỷ lệ việc chủ trì; BE bỏ qua `host_only`.
- Phiếu công tác / Phiếu giao việc: popup chỉ 2 loại này thì ẩn cột Tên công việc (lẫn loại: "—"), cả bản in / Excel; mã phiếu
  bấm mở panel; panel có khối "Thông tin phiếu" tải khi mở qua `GET …/item` (chỉ phiếu có người trong phạm vi quyền).
- Ô chọn cấp trong tiêu đề cột: KHÔNG ép `height="18px"` (lỗi của khuôn report-styles — cỡ xs cao 26px); các báo cáo khác +
  skill vẫn dính, chờ user quyết.
- Theme Sale: bỏ vạch `::before` đầu tiêu đề bộ lọc / tiêu đề card cho TOÀN theme (commit riêng client de8779fb9).
- 06/10 chiều (user chốt): Meeting trong popup đầu việc mở panel meeting DÙNG CHUNG (`ReportMeetingDetailDrawer`, Xem biên
  bản); `Meeting::canView` nới theo phạm vi NV của báo cáo (1612–1614, dùng chung `applyEmployeeScope`).
- NV ĐÃ NGHỈ: giữ nếu có số liệu trong kỳ, không có thì bỏ (chỉ báo cáo này dựng dòng từ danh mục NV); ô chọn NV giữ nguyên.
- NV chưa gán bộ phận: phòng CÓ chia → nhóm "Không thuộc bộ phận" ngang cấp bộ phận, đứng cuối; phòng KHÔNG chia → bỏ cấp.
  Áp 4 báo cáo Giao việc (kế hoạch & kết quả, phát triển thị trường – KH, kết quả dự án TKT, kết quả CSKH tiềm năng).
- Tên hiển thị loại việc: Task → "Nhiệm vụ", Issue → "Vấn đề" (báo cáo + my-todo); mã loại giữ nguyên.


## 07/10/2026 — đợt 3: ô chọn cấp · tiêu đề 1 dòng · "phòng có chia bộ phận" theo danh mục (user chốt + lệnh "Làm")

Phạm vi: hrm-api + hrm-client nhánh `gop_db` (sửa thẳng), không migration / seeder / quyền. CHƯA commit.

- [x] Ô chọn cấp: bỏ ép `height` (18px ở potential-customer-tracking, service-demand; 22px ở meeting-by-projects,
      meeting-by-employees) — đo trước: chữ tràn đáy 7px / 3px; sau: cả 6 màn 26px, tràn -1px. Sửa luôn skill
      `report-styles` (SKILL.md + template TrackingTable.vue).
- [x] Tiêu đề cột LUÔN 1 dòng (user: "không chấp nhận xếp thành 2 hàng"): soát 8 báo cáo ở 1366px, chỉ service-demand
      vi phạm (4 tiêu đề 2 dòng + ô chọn cấp rớt hàng 2 vì bảng ép vừa khít 1083px). Sửa: `th` nowrap, nhãn + ô chọn cấp
      `flex-wrap: nowrap`, bảng `min-width: 1480px` + `V2BaseTableScroll` (2 thanh), cột Meeting 140→165px, Ngày hoàn
      thành 110→160px. Đo sau: 9/9 tiêu đề 1 dòng, cao 42px, ở 1366 và 1920; trang không cuộn ngang. Luật ghi vào skill.
- [x] "Phòng có chia bộ phận" xét THEO DANH MỤC `parts` (chỉ bộ phận đang hoạt động, status = 1): helper
      `Part::departmentIdsWithActiveParts()`; áp 5 service — CustomerMarketDevelopment, ProspectiveProjectResultReport,
      EmployeeWorkTreeBuilder (caller truyền tập phòng, builder vẫn không đụng DB), PotentialCustomerTracking,
      PotentialCustomerCare (level `keepWhen`). Phòng có trong danh mục mà dữ liệu không ai gán → giữ cấp, cả phòng vào
      "Không thuộc bộ phận"; phòng chỉ có bộ phận đã khoá → bỏ cấp. Dữ liệu có gán bộ phận thì vẫn hiện cấp như cũ.
- [x] "Không thuộc bộ phận" luôn cuối danh sách bộ phận trong phòng: đã đúng ở cả 5 (đo API thật: 7/7 phòng EWP, 4/4 CMD).
- [x] Test: PHPUnit `PartCatalogDepartmentsTest` + ca danh mục ở 5 test NoPart/Tree/PartBudget + ca popup nhóm "Không thuộc
      bộ phận" (đi MỌI node cây so số popup) cho TKT và Kết quả CSKH tiềm năng. Fixture `tests/Unit/PartCatalogFixture.php`
      (transaction, DB local không đổi — đã kiểm 0 dòng sót). RED trên code cũ: 5 ca đỏ; GREEN: 16 bộ liên quan xanh.
- [x] E2E (biên dịch được, CHƯA chạy): helper `e2e/utils/levelSelect.ts` gắn vào 4 spec; service-demand ca 1/1b đổi từ
      "không cuộn ngang" sang "tiêu đề 1 dòng + cuộn ngang trong bảng".
- [ ] User kiểm trên app · commit/push khi user yêu cầu · chạy e2e khi user yêu cầu.

Còn lại: popup chi tiết (drill) cột "Bộ phận" vẫn ẩn/hiện theo dữ liệu (`has_part`), chưa theo danh mục.
