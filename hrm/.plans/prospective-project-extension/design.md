# Gia hạn dự án TKT + tự đóng theo giai đoạn (Redmine #11153)

Người phụ trách: @cuong61n · Nhánh `tpe` (worktree `HRM/worktrees/tpe-api` :8005 + `tpe-client` :3005)

## Mục tiêu
1. Nút **Gia hạn** ở màn chi tiết dự án TKT → popup nhập số ngày + lý do → đề xuất đi qua phê duyệt 2 cấp.
2. **Cấu hình thời gian đóng dự án tự động** theo giai đoạn (9 giai đoạn) + tham số chung.
3. **Cron tự đóng** dự án quá hạn, có thông báo nhắc trước N ngày cho NVKD chính.

## Quyết định đã chốt (assumption, cần khách xác nhận — xem mục cuối)
- **4 tham số chung** (S, M, N, X) là cột mới trên `general_regulations` (1 bản ghi / công ty), sửa ở màn Cấu hình chung → tab "Quản lý dự án" → sub-tab mới "Đóng dự án tự động":
  - `project_no_quotation_close_months` = **S**: chưa có báo giá duyệt thì hạn = ngày tạo + S tháng (mặc định 3)
  - `project_close_warning_days` = **N**: nhắc NVKD chính trước hạn N ngày (mặc định 7)
  - `project_auto_close_days` = **M**: quá hạn thêm M ngày thì hệ thống tự đóng (mặc định 0 = đóng ngay khi quá hạn)
  - `project_extension_tp_max_days` = **X**: ngưỡng ngày Trưởng phòng được duyệt (mặc định 30)
- **Cấu hình theo giai đoạn**: bảng `project_phase_close_configs` (1 dòng / giai đoạn, `close_months` null = KHÔNG tự đóng). Giá trị mặc định seed theo spec: GD1 12 · GD2 10 · GD3 8 · GD4 6 · GD5 4 · GD9 4 · GD6 3 · GD7 1 · GD8 không áp dụng.
- **Công thức hạn đóng** (`prospective_projects.auto_close_date`):
  - Chưa có báo giá `Đã duyệt`/`Trúng thầu` → `created_at + S tháng`
  - Đã có → `approved_at của báo giá duyệt GẦN NHẤT + close_months của giai đoạn hiện tại`
  - Giai đoạn không cấu hình → `auto_close_date = null` (không bao giờ tự đóng)
  - Cộng thêm `extended_days` (tổng ngày đã được duyệt gia hạn)
  - Tính lại tại: tạo/sửa dự án, duyệt báo giá, duyệt gia hạn, và mỗi lần cron chạy (idempotent, chống lệch nếu quên hook).
- **Phạm vi duyệt** (chốt 2026-09-11, copy nguyên khuôn duyệt báo giá): Trưởng phòng chỉ duyệt đề xuất của **phòng ban mình quản lý**, Ban giám đốc chỉ duyệt trong **công ty mình**. Quyền thôi chưa đủ.
- **Phê duyệt 2 cấp** (copy khuôn duyệt báo giá): `days <= X` → chỉ TP duyệt là xong; `days > X` → TP duyệt rồi chuyển BGĐ duyệt tiếp. 2 quyền mới: `Trưởng phòng duyệt gia hạn dự án TKT`, `Ban giám đốc duyệt gia hạn dự án TKT`.
- **Duyệt xong** (chốt 2026-09-11): CHỈ `extended_days += days` → hạn đóng lùi ra đúng bấy nhiêu ngày; xoá cờ đã nhắc; ghi lịch sử dự án. **KHÔNG đụng `end_date`** của dự án — đó là trường sale tự nhập theo hợp đồng/kế hoạch, spec #11153 không yêu cầu sửa. 2 cột `old_end_date`/`new_end_date` trên bảng đề xuất lưu mốc HẠN ĐÓNG trước/sau (giữ tên cột, Resource trả ra `old_auto_close_date`/`new_auto_close_date`).
- **MỌI giai đoạn đều đếm từ ngày duyệt báo giá gần nhất** (chốt 2026-09-12). Spec nêu riêng giai đoạn Đấu thầu "tính từ thời điểm nộp thầu", nhưng DB không có cột ngày nộp thầu và user quyết định KHÔNG thêm — dùng chung một mốc cho cả 9 giai đoạn. Hệ quả: giai đoạn Đấu thầu bắt đầu đếm sớm hơn ý spec đúng bằng khoảng cách từ ngày duyệt báo giá tới ngày nộp thầu; bù bằng cách tăng số tháng cấu hình của giai đoạn đó nếu thực tế cần.
- **Hạn đóng tính LẠI TỪ ĐẦU mỗi lần, không cộng dồn** (chốt 2026-09-11): `mốc gốc + số tháng cấu hình + tổng ngày đã gia hạn`. Hệ quả đã xác nhận với user: **sửa cấu hình số tháng thì hạn của cả dự án CŨ cũng dịch theo** (test thật: đổi S 3→4 tháng, dự án 257 từ 31/12/2026 → 31/01/2027, số ngày đã gia hạn vẫn giữ). KHÔNG chọn phương án "đóng băng hạn tại thời điểm vào giai đoạn".
- **Điều kiện hiện nút Gia hạn**: là NVKD chính · dự án chưa đóng · trạng thái KHÔNG thuộc {9 Thực hiện hợp đồng, 10 Nghiệm thu và thanh lý, 11 Đóng} · chưa quá hạn đóng · chưa có đề xuất đang chờ duyệt.
- **Lý do tự đóng**: thêm bản ghi danh mục `Hệ thống tự đóng do quá thời gian thực hiện`.

## Ngoài phạm vi
- Dự án cha: dùng chung logic, không tự đóng cascade xuống con (cron chỉ đóng đúng dự án quá hạn).

## Câu hỏi cần khách chốt (đang chạy theo giả định, chưa có xác nhận)

> Câu hỏi 3 về "ngày nộp thầu" ĐÃ CHỐT 2026-09-12: mọi giai đoạn dùng chung mốc ngày duyệt báo giá gần nhất, không thêm cột mới.

| # | Vấn đề | Đang làm theo giả định nào | Nếu khách chốt khác thì sửa ở đâu |
|---|---|---|---|
| 1 | **Tiền tố thông báo** | Dùng `[DATKT]` cho mọi thông báo của dự án TKT (`[DATKT] Chờ duyệt: <b>Tên dự án</b>. Xin gia hạn 45 ngày.`). Skill `notification-convention` yêu cầu đối tượng chưa có prefix thì đề xuất 3–5 ký tự rồi **hỏi user xác nhận** | `ProspectiveProjectExtensionService::buildTitle()` và `AutoCloseProspectiveProjectsCommand::notifyMainSale()` |
| 2 | **Giá trị mặc định 4 tham số** | S = 3 tháng (chưa có báo giá) · N = 7 ngày (nhắc trước hạn) · M = 0 ngày (quá hạn là đóng ngay) · X = 30 ngày (ngưỡng Trưởng phòng). Spec chỉ nêu S = 3 tháng, ba tham số còn lại spec để trống | Sửa trực tiếp ở màn Cấu hình chung → Quản lý dự án → Đóng dự án tự động (không phải sửa code). Mặc định cho công ty mới nằm ở `ProjectCloseConfigService::GENERAL_FIELDS` + migration `2026_09_11_000002` |

Chốt xong điểm nào thì ghi lại ngay vào mục "Quyết định đã chốt" ở trên để lần sau không hỏi lại.

## Tài liệu
- Plan: `plan.md` · Spec chi tiết: `docs/superpowers/specs/2026-09-11-prospective-project-extension-design.md`
