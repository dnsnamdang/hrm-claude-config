# Báo cáo tổng hợp chăm sóc khách hàng tiềm năng — design (tóm tắt)

> @namdangit · Tạo: 2026-10-04 · Trạng thái: **HOÀN THÀNH — merge + push gop_db, đã deploy VPS (04/10/2026)**
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-04-bao-cao-tong-hop-cskh-tiem-nang-design.md`
> Mockup: `mockup.html` (cùng thư mục, mở bằng file://) — dựng từ DOM + CSS thật của app
> Nhánh: `gop_db-bao-cao-tong-hop-cskh-tiem-nang` (api + client, từ `origin/gop_db`) · worktree `websites/wt-bao-cao-tong-hop-cskh/`
> ⛔ Không merge vào `gop_db` — xong chỉ push nhánh feature.

## Mục tiêu

Ảnh chụp **tại thời điểm xem**: mỗi Sales đang theo dõi những **nhu cầu làm dự án** nào (còn Đang theo dõi) và
những **dự án TKT** nào (tiến trình 2 → 9), với khách nào, lần chăm sóc gần nhất là khi nào, nhu cầu nào sắp hết hạn.

## Quyết định đã chốt

| # | Chốt |
|---|---|
| 1 | Không có bộ lọc Kỳ — số liệu tại lúc xem |
| 2 | Nhu cầu: `meeting_investment_demands.status = 1`; Sales = `COALESCE(owner_employee_id, meetings.host_employee_id)` |
| 3 | Dự án: `prospective_projects.status` 2 → 9; Sales = `main_sale_employee_id` |
| 4 | Phòng / công ty = nơi Sales đang làm việc (gom cây + quyền); không có Sales → "Chưa xác định" cuối cây |
| 5 | Cây Phòng ▸ Sales ▸ Khách hàng ▸ lá (nhu cầu trước, dự án sau), cột Loại |
| 6 | 2 cột giá trị riêng: nhu cầu `expected_amount` · dự án `expected_contract_amount` |
| 7 | Hạn theo dõi = `dueDate()`; ≤ M ngày → cam; không có hạn chỉ hiện ở dòng, không có ô tổng hợp riêng |
| 8 | Lần chăm sóc gần nhất (dòng KH) = meeting Hoàn thành mới nhất, ai chủ trì cũng được → popup lịch sử có sẵn |
| 9 | 3 quyền mới id **1676–1678** (tổng công ty / công ty / phòng ban), `type = 29` (phân hệ CSKH trước bán); không quyền → việc của mình |
| 10 | Khối tổng hợp ẩn chỉ tiêu = 0 |
| 11 | Ô lọc: Công ty · Phòng ban · Sales phụ trách · Khách hàng / Loại · **Tiến trình dự án** · Lĩnh vực · Hạn theo dõi |
| 12 | Khuôn UI: `/sale/prepick-tracking` + `V2BaseReportModal`; menu CSKH trước bán › Báo cáo thị trường |
| 13 | Người có quyền báo cáo xem được chi tiết meeting CÓ nhu cầu trong phạm vi quyền — nới `Meeting::canView()` (khuôn báo cáo dịch vụ #24) |
| 14 | 4 nhóm quyền báo cáo thị trường (1179–1181 · 1187–1189 · 1660–1661 · 1676–1678) chuyển `type` 4 → 29 để hiện đúng ở phân hệ CSKH trước bán trên màn Phân quyền |

## Phạm vi kỹ thuật

- **Không** bảng/cột mới, **không** migration, **không** cron, **không** thông báo.
- BE: 1 service + 1 controller + 6 route + Excel/In + 3 quyền trong seeder + nới `Meeting::canView()`.
- FE: 1 màn (index + 3 component) + 1 dòng menu.
