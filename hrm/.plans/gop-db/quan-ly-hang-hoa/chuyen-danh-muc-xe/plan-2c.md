# Plan Phase 2c (A7-2c) — Biển số xe · Lái xe ngoài · Danh mục xe · Nhiên liệu

> Căn cứ: `khao-sat-2c.md` (chốt Q1–Q4 ngày 14/10/2026) + khuôn 2b (`design.md`, `plan.md` cùng thư mục).
> Trạng thái: ✅ **XONG + ĐÃ PUSH 14/10**: hrm-api `8f5990cca`, hrm-client `cf5efd2ea`, ERP `ca5fa294de`. Quyền dời sang **1720–1727** (review C1). Report: `2c-t1-report.md`, `2c-t2-report.md`, `2c-t3-report.md`, `2c-fix1-report.md`; review `2c-review-t1-t3.md`, `2c-review-t2.md`.

## Phạm vi
- **hrm-api + hrm-client** worktree `wt-chuyen-doi-hang-hoa`: nhánh con `feat/cdhh-2c-xe` checkout từ `feat/chuyen-doi-hang-hoa`; xong merge về nhánh chung (LOCAL, không push).
- **ERP** worktree `wt-erp-2d1`: nhánh con `feat/cdhh-2c-xe-erp` từ `feat/2d1-erp-khong-loi`; xong merge LOCAL.
- **DB `hrm_erp_giacty`**: KHÔNG migration (4 bảng đã có `status`). Chỉ chèn 8 quyền mới bằng câu lệnh riêng (không chạy cả seeder) + role tạm cho e2e_assign để kiểm, gỡ khi xong.

## Đợt T1 — HRM BE (hrm-api)
1. **Biển số xe** `license-plates` (`license_plates`): nền `BaseCatalog*`, `hasCodeField=false` (Service + Request). `name` required max 90, unique **trong bản ghi đang hoạt động**; `note` ≤255. Chặn Mở khoá tạo trùng. `childrenCount` = xe đang tham chiếu (`vehicles`) + `delivery_trips` + `other_delivery_trips` + `assign_business_employee_details` + `assign_request_employee_details` + `payment_profile_employee_details` + `payment_business_request_employee_details` (cột `license_plate_id`).
2. **Lái xe ngoài** `external-drivers` (`drives`): `BaseCatalog*`, các trường name ≤255 · phone ≤12 · birth_year đúng 4 chữ số · id_card ≤20 · driver_license ≤20, đều bắt buộc. `childrenCount` = `vehicle_drivers` + 4 bảng chuyến (`delivery_trips`, `other_delivery_trips`, `activity_has_*delivery_trips*`) + 2 bảng đề nghị TT (`*delivery_payment_requests`).
3. **Nhiên liệu** `fuels`: `BaseCatalog*`, `name` required ≤90 unique đang hoạt động, `price` số ≥0 bắt buộc. `childrenCount` = `vehicles`.
4. **Danh mục xe** `vehicles`: service + controller riêng (không phải danh mục 1 cấp): list (lọc Biển số · Chủ xe · Hãng · Loại · Model · Tải trọng · Dòng xe · Trạng thái · Người tạo), show, store/update (luật ERP §2 khảo sát + Loại ∈ Hãng, Model ∈ Loại; biển số không trùng xe ĐANG hoạt động khác), lock/unlock, destroy (chặn khi có chuyến/hạch toán). Bảng nối `vehicle_drivers` / `vehicle_company_drivers` sync theo `driver_type`. Ô chọn: biển số đang hoạt động · NCC (`suppliers`) · công ty + bộ phận · lái xe ngoài · nhân viên (`employee_infos.id`).
5. 6 điểm đăng ký (khuôn 2b §3): routes, `CatalogHistoryService::TABLES`, `ExportColumnRegistry`, quyền, menu, `entity-type`.
6. **Quyền** 8 cái, id **1699–1706** (gop_db đang tới 1698 — kiểm lại max + `uniq -d` ngay trước commit), `group='Danh mục hàng hóa'`, `type=9`: Xem/Quản lý danh mục biển số xe · lái xe ngoài · xe · nhiên liệu.
7. PHPUnit: CRUD + unique theo active + chặn xoá có tham chiếu + gate 2 chiều (có quyền / không quyền 403) + Danh mục xe kiểm cha–con và sync bảng nối.

## Đợt T2 — HRM FE (hrm-client)
- 3 màn danh mục (Biển số, Lái xe ngoài, Nhiên liệu) theo khuôn list-page + popup form của 6 màn xe 2b.
- Màn **Danh mục xe**: list-page + trang/popup form (ô chọn dây chuyền Hãng → Loại → Model; công tắc Xe Tân Phát ⇒ Công ty + Bộ phận / NCC; Loại tài xế ⇒ chọn nhiều lái xe ngoài / nhân viên).
- Menu: nhóm "Xe" ở Danh mục chung thêm 4 mục (`subItems`, đếm link bằng DOM).
- Validate báo đồng thời mọi ô; không dùng `trim` ở ô nhập.

## Đợt T3 — ERP
- `ProductMovedToHrm::TARGETS` thêm 10 khoá: 6 màn 2b (`vehicle-manufacts`, `vehicle-brands`, `vehicle-models`, `vehicle-life`, `vehicle-categories`, `vehicle-payloads`) + `license-plates`, `external-drivers`, `vehicles`, `fuels`.
- Gắn middleware lên route GHI (store/update/delete/create/edit, import model xe) của 10 nhóm route; **giữ** `searchData`, `vehicleManufact.brands`, `vehicle.getRoadInfo` và mọi chỗ đọc của vận chuyển.
- Menu "Xe" + mục Nhiên liệu (menu Vận chuyển - Bốc xếp) đổi sang link HRM `(HRM)` kiểu C-b.

## Kiểm chứng (trước khi báo xong)
1. Số dòng 4 bảng giữ nguyên mốc (license_plates 163 · drives 72 · vehicles 137 · fuels 4; bảng nối 110 / 74), 0 bản ghi rác sau khi thử.
2. Gate quyền 2 chiều (role tạm, xoá cache quyền).
3. Playwright đo DOM: 4 màn đủ cột, lọc bắn đúng param, nút hành động bấm thật, form Danh mục xe dây chuyền + đổi chủ xe/loại tài xế; menu nhóm Xe đủ 10 link.
4. ERP: 10 route ghi trả trang/JSON "đã chuyển sang HRM"; menu trỏ HRM; mở lại 1 chuyến giao hàng + công thức vận chuyển + `getRoadInfo` vẫn chạy.
5. HRM Công tác vẫn chọn được biển số xe công ty (N102 không sửa ở đây).

## Checklist deploy 2c (review I3 — ERP chặn ghi cùng lúc HRM chưa ai có quyền)
- Quyền HRM mới: **1720–1727** (đã dời khỏi 1699–1706 vì `origin/develop` dùng tới 1711). Kiểm lại max id các nhánh ngay trước khi merge prod.
- TRƯỚC khi bật middleware ERP: gán quyền HRM "Quản lý danh mục {biển số xe · lái xe ngoài · xe · nhiên liệu}" (+ cặp Xem) cho role của người đang thao tác. Người sửa 3 bảng từ 2025 (đo trên giacty, `created_by/updated_by` = `employees.id`):
  | NV | Phòng | Biển số | Lái xe | Xe |
  |---|---|---:|---:|---:|
  | Bùi Thị Thơm (311) | Logistic (LN) | 50 | 10 | 49 |
  | Đào Thị Thúy (34) | Quản trị thông tin | 1 | – | 17 |
  | Trịnh Thị Lợi (787) | Quản trị thông tin | – | 2 | 10 |
  | Bùi Thị Thịnh (408) | KT-HC CN Vinh | 3 | – | 6 |
  | Hà Thị Khánh Ly (332) | HCNS CN Hải Phòng | 2 | 2 | 4 |
  | Hồ Chí Dũng (917) | Logistic (PTT) | 3 | 1 | 3 |
  | Trần Hồng Nhung (204) · Lưu Thị Hồng (336) · Bùi Thị Thịnh (1035) | KT tài vụ · Logistic · KD bôi trơn | – | 0–1 | 1 |
- Người có quyền ERP 100134 "Quản lý dòng xe" / 100135 "Quản lý trọng tải xe" / 100138 "Quản lý loại nhiên liệu" ⇒ cấp quyền HRM tương ứng (dòng xe/tải trọng 2b: 1648–1651 theo seeder — xem N104 lệch id DB).
- 6 màn 2b cũng bị ERP chặn ghi trong đợt này ⇒ người đang sửa Hãng/Loại/Model/Đời xe ở ERP cũng phải có quyền HRM 2b.
