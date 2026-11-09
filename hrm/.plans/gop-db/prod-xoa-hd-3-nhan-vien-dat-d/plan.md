# Xoá hợp đồng + QĐ tiếp nhận của 3 nhân viên trên PROD (không có số Redmine) — @cuong61n

Yêu cầu qua chat (09/11/2026, 13:31): xoá hộ **tất cả hợp đồng** (HĐLĐ + HĐ thử việc) của 3 nhân viên
PHÒNG DỰ ÁN TRỌNG ĐIỂM: Sầm Văn Linh (12611198), Nguyễn Thế Huấn (12611199), Nguyễn Quang Tuyến (12611200).
User chốt xoá thêm 3 QĐ tiếp nhận gắn với 3 HĐ thử việc.

## Task

- [x] (09/11/2026) Tra dữ liệu PROD (DB `hrm_erp_gop`, chỉ đọc) — khớp đúng 6 HĐ trong ảnh:
  - Sầm Văn Linh: 598/2026/HĐLĐ-TPE (id 773, HĐLĐ xác định thời hạn) · 594/2026/HĐLĐ-TPE (id 769, thử việc, QĐ 153/2026/QĐTN-TPE id 762)
  - Nguyễn Thế Huấn: 599/2026/HĐLĐ-TPE (id 774) · 593/2026/HĐLĐ-TPE (id 768, thử việc, QĐ 154 id 761)
  - Nguyễn Quang Tuyến: 600/2026/HĐLĐ-TPE (id 775) · 592/2026/HĐLĐ-TPE (id 767, thử việc, QĐ 155 id 760)
- [x] (09/11/2026) Rà phụ thuộc: HĐ chỉ có phụ cấp (24) + nhiệm vụ (6); không phụ lục / gia hạn / chấm dứt / tạm hoãn / điều chuyển / thay đổi lương / nghỉ hưu nào trỏ tới. Quét mọi bảng có `decision_id` → QĐ có accept_personnels (3), phụ cấp (12), lịch sử duyệt (6), đối tượng phòng ban (3), vị trí (3). Duyệt QĐ tiếp nhận không ghi sang hồ sơ nhân viên → không phá hồ sơ
- [x] (09/11/2026) Sao lưu toàn bộ dòng sắp xoá (9 bảng, mysqldump `--no-create-info`) ra `~/Desktop/dns/backup_prod_xoa_hd_20261109.sql` — khôi phục = chạy lại file này
- [x] (09/11/2026) Xoá trong 1 transaction, theo đúng thứ tự service xoá của hệ thống (`DecisionLaborContractService::destroy`, `AcceptPersonnelService::destroy`): 6 HĐ + 24 phụ cấp + 6 nhiệm vụ; 3 QĐ + 3 accept_personnels + 12 phụ cấp + 6 lịch sử duyệt + 3 + 3 dòng đối tượng. Số dòng xoá khớp số đếm trước
- [x] (09/11/2026) Kiểm lại: 3 nhân viên không còn HĐ nào trong `decision_labor_contracts`. Trạng thái: **đã xong trên PROD 09/11/2026**
- [x] (09/11/2026 15:45) **Sự cố do bước xoá trên gây ra**: duyệt QĐ tiếp nhận (id 769) lỗi `1062 Duplicate entry '161/2026/QĐTN-TPE'`.
  Nguyên nhân: mã QĐ (`Decision::getNextCodeApproved`) và số HĐLĐ (`DecisionLaborContractService`, đoạn sinh `HĐLĐ`) sinh bằng **đếm `withTrashed()` + 1**, không lấy số lớn nhất. Xoá trên UI là xoá MỀM (`Decision`, `DecisionLaborContract` dùng SoftDeletes) nên số đếm giữ nguyên; tôi xoá CỨNG → đếm hụt 3 (QĐ) / 6 (HĐ) → sinh lại số đã có.
  Xử lý: nạp lại 3 dòng `decisions` (760–762) + 6 dòng `decision_labor_contracts` (767–769, 773–775) từ file sao lưu, đặt `deleted_at` = 09/11/2026 15:44 (đúng trạng thái như xoá trên UI, vẫn ẩn khỏi danh sách). Lưu ý nạp kèm `SET time_zone='+00:00'` vì mysqldump ghi TIMESTAMP theo UTC (lần nạp đầu bị lùi 7 giờ, đã nạp lại đúng giờ gốc).
  Kết quả: mã QĐ tiếp theo của TPE = 164 (số lớn nhất 163), số HĐLĐ TPE tiếp theo = 603 (số lớn nhất 602). QĐ 769 đã tự quay lại trạng thái cũ (status 3, chưa có mã) → duyệt lại là được. Bảng con (phụ cấp, nhiệm vụ, accept_personnels…) không ảnh hưởng số nên để xoá như cũ.
  Bài học: **trên prod không xoá cứng bản ghi có SoftDeletes / bản ghi được đếm để sinh mã** — xoá thì đặt `deleted_at` giống thao tác UI.
