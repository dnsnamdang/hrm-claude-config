# Phase 2c (A7-2c) — 3 danh mục Xe công ty còn lại — khảo sát 14/10/2026 (chỉ đọc)

> ERP `wt-erp-2d1` (`feat/2d1-erp-khong-loi`) · HRM worktree `wt-chuyen-doi-hang-hoa` (`feat/chuyen-doi-hang-hoa` @ api `3b7dd0f1a`) · DB `hrm_erp_giacty`.
> Chưa đụng source. Dòng xe + Tải trọng đã làm ở 2b (22/09) ⇒ 2c còn 3 màn + (tuỳ chốt) Nhiên liệu.

## 1. Ba màn, đo thật
| Màn ERP | Route ERP | Controller (dòng) | Bảng | Hoạt động / khoá | Gate ERP |
|---|---|---|---|---|---|
| Danh mục biển số xe | `licensePlate.*` (`/license-plates`) | `Common\LicensePlatesController` (179) | `license_plates` (id name note status …) | 161 / 2 | **không** |
| Danh mục lái xe ngoài | `drives.*` (`/drives`) | `Common\DrivesController` (207) | **`drives`** (id name phone birth_year id_card driver_license status …) | 69 / 3 | **không** |
| Danh mục xe | `vehicle.*` (`/vehicles`, 5 blade, có trang create/edit riêng) | `Common\VehiclesController` (314) | `vehicles` + 2 bảng nối `vehicle_drivers` (110) · `vehicle_company_drivers` (74) | 134 / 3 | **không** |
| (Nhiên liệu — ô bắt buộc của Danh mục xe) | `fuel.*` (menu "Vận chuyển - Bốc xếp") | `Common\FuelController` (172) | `fuels` (id name **price** status) | 4 / 0, sửa lần cuối 07/2023 | `Quản lý loại nhiên liệu` |

⚠️ Đính chính `design.md`: bảng lái xe ngoài là **`drives`** (72 dòng); `vehicle_drivers` (110) là bảng NỐI xe ↔ lái xe ngoài.

Mức dùng: biển số tạo mới gần nhất 07/08/2026 (16 dòng từ 2026) · xe 07/08/2026 (17) · lái xe 09/06/2026 (5).

## 2. Hành vi ERP cần giữ / lưu ý
- **Xoá = set `status=0`** ở cả 3 màn (như 2b) ⇒ HRM "Khoá".
- **Biển số**: `name` required max 90, **unique toàn bảng kể cả bản ghi đã xoá** (cùng lỗi 2b) · note max 255. Dữ liệu: 0 trùng.
- **Lái xe ngoài**: name/phone(≤12)/birth_year(4 ký tự)/id_card(≤20)/driver_license(≤20) đều bắt buộc; không kiểm trùng (1 CCCD trùng giữa 2 lái xe đang hoạt động). `store` không gán `status` (sống nhờ default).
- **Danh mục xe**: 7 ô chọn bắt buộc — Biển số (không trùng với xe đang hoạt động; dữ liệu có **1 biển gắn 2 xe** đang hoạt động) · Hãng xe · Loại xe · Model xe (2b) · Tải trọng · Dòng xe (2b) · Nhiên liệu. Chủ xe: "Xe Tân Phát" ⇒ Công ty + Bộ phận; ngược lại ⇒ **NCC** (`owner` → `suppliers`). Loại tài xế: 1 = lái xe ngoài (chọn nhiều từ `drives`), 2 = tài xế công ty (chọn nhiều nhân viên, lưu `employee_infos.id`). Hiện có: 109 xe NCC + lái ngoài · 24 xe công ty + tài xế công ty · 1 xe NCC + tài xế công ty.
- ERP KHÔNG kiểm Loại xe thuộc Hãng xe, Model thuộc Loại xe (2b đã thêm kiểm ở danh mục).
- `vehicle.getRoadInfo` (tra tuyến cho vận chuyển) nằm chung controller — **giữ ở ERP**.

## 3. Ai đọc 3 bảng này
- **ERP vận chuyển** (giữ nguyên, đọc thẳng bảng): chuyến giao hàng `delivery_trips` (3.058 chuyến / 69 xe, mới nhất 15/09/2026), chuyến khác `other_delivery_trips` (395), hạch toán chuyến, đề nghị thanh toán vận chuyển, công thức vận chuyển Tân Phát, báo giá vận chuyển, bảng giá vận chuyển hiệu lực, báo cáo chuyến, phân vùng thị trường (`Division*`).
- **HRM Công tác** (`Modules/Assign`): `TpLicensePlate` / `TpVehicle` / `TpFuel` — chọn biển số xe công ty (`vehicles.is_tanphat=1`) ở Phân công / Hồ sơ thanh toán công tác (307 dòng, mới nhất 31/07/2026); `RoadController` đọc xe + nhiên liệu. ⚠️ Lọc biển số xe công ty **không kiểm `vehicles.status`** (xe đã xoá vẫn hiện) ⇒ ngoài luồng **N102**.
- Màn HRM: chưa có màn nào cho 3 bảng (đã có 6 màn nhóm "Xe" ở Danh mục chung: Hãng xe · Loại xe · Model xe · Đời xe · Dòng xe · Tải trọng).

## 4. Hiện trạng ERP sau 2b
4 màn 2b + Dòng xe + Tải trọng **vẫn ghi song song ở ERP** (menu "Xe" còn đủ 9 mục, route chưa chặn). Chưa có quyết định chặn ghi danh mục xe ở ERP.

## 5. Tự chốt (kỹ thuật, theo khuôn 2b)
- Dùng chung bảng ERP, giữ id, không di trú; nền `BaseCatalog*` cho Biển số + Lái xe ngoài; Danh mục xe là màn form riêng (nhiều ô chọn + 2 bảng nối) nhưng vẫn list-page + popup/trang form theo khuôn HRM.
- Unique biển số **chỉ so bản ghi đang hoạt động**; chặn Mở khoá tạo trùng (như B3 của 2b).
- Xoá thật chỉ khi không có tham chiếu (chuyến giao hàng, chuyến khác, hạch toán, đề nghị TT, công tác, bảng nối…); Khoá luôn được.
- Danh mục xe kiểm thêm Loại xe ∈ Hãng xe, Model ∈ Loại xe (như 2b).
- Tài xế công ty: ô chọn nhân viên trả `employee_infos.id` (HRM `employees.employee_info_id`).
- 1 biển gắn 2 xe đang hoạt động: không dọn dữ liệu; rule chỉ chặn khi lưu xe khác biển đó.
- Quyền: 3 cặp Xem / Quản lý (lấy max id ngay trước commit; kiểm `uniq -d`), nhóm Danh mục xe.

## 6. Câu hỏi tồn (hỏi lần lượt)
| # | Câu | Chốt |
|---|---|---|
| Q1 | Có gồm màn **Nhiên liệu** (`fuels`, 4 dòng, có giá) không | ✅ **Có** — thêm màn Nhiên liệu (tên + giá) + 1 cặp quyền (14/10) |
| Q2 | Sau 2c, màn danh mục xe ở **ERP** (9 màn menu "Xe" + Nhiên liệu) xử lý thế nào | ✅ **Chặn ghi + menu trỏ HRM cho cả 10 màn** (6 màn 2b + 4 màn 2c) — giữ route đọc mà vận chuyển dùng (`getRoadInfo`, searchData nếu có chỗ gọi) (14/10) |
| Q3 | Menu HRM đặt ở đâu | ✅ **Nhóm "Xe" ở Danh mục chung** (cạnh 6 màn 2b, nhóm thành 10 mục) (14/10) |
| Q4 | Gate quyền HRM (ERP hiện không gate 3 màn) | ✅ **4 cặp Xem / Quản lý = 8 quyền** (khuôn 2b); deploy phải gán quyền cho người đang dùng (14/10) |
