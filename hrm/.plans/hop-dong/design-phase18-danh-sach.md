# Phase 18 — Cập nhật màn Danh sách hợp đồng: quyền phân cấp + bộ lọc

> Khảo sát 27/10/2026 trên nhánh `gop_db-hop-dong-ban`. Trạng thái: **ĐỀ XUẤT — chờ user duyệt**, chưa code.
> Chuẩn áp: skill `list-page` (mục đầu: bộ 4 quyền theo cấp; bộ lọc bắt đầu Công ty › Phòng ban › Bộ phận;
> `V2BaseSmartFilterPanel` + `floating`; khoảng ngày gộp 1 ô; người dùng hệ thống là select, không vào ô tìm nhanh).
> Nguồn nghiệp vụ ERP: `app/Datatables/Sale/Firm/FirmContractDatatable.php` (nhánh `type=all`) +
> `resources/views/sale/firm/contracts/index.blade.php` (search_columns).

## 1. Hiện trạng quyền

| Nơi | Hiện tại |
|---|---|
| Seeder (`PermissionsTableSeeder` dòng ~1246) | `Xem danh sách Hợp đồng theo tổng công ty` · `… theo công ty` · `… theo phòng ban` · `… theo bộ phận` (type 23, nhóm `Hợp đồng`) |
| BE `ContractController::scopedContractQuery()` | `checkPermissionListWithColumn(…, 4 quyền trên, true)` — dùng chung cho `index` + `export` |
| FE `pages/assign/contracts/index.vue:551` | 4 cờ `is_all_company / is_company / is_department / is_part` → chỉ để điều khiển ô Công ty–Phòng ban |
| Menu `sale-hub.js:58` | Không gate quyền (ai cũng vào; không có quyền xem theo cấp thì chỉ thấy HĐ mình tạo) |

**Lệch chuẩn:**
1. Tên quyền không theo khuôn `Xem tất cả [màn]` / `Xem [màn] theo công ty|phòng ban|bộ phận`.
2. Quyền "tổng công ty" trả **mọi** HĐ, kể cả **Đang tạo của người khác**. Chuẩn: "Xem tất cả" bỏ trạng thái Đang tạo.
3. Ba cấp dưới cũng thấy HĐ Đang tạo của người khác trong phạm vi. ERP ẩn ở **mọi cấp** (chỉ thấy Đang tạo của chính mình).
4. Bảng `hrm_contracts` chỉ có index `id`, `quotation_id`, `code` — thiếu index cho các cột lọc theo cấp / bộ lọc (`company_id`, `department_id`, `part_id`, `created_by`, `status`, `customer_id`, `sign_date`).

## 2. Đề xuất quyền

| Tên mới (đổi tên qua `RENAMED`, giữ gán cho vai trò) | Tên cũ | Phạm vi |
|---|---|---|
| Xem tất cả Hợp đồng | Xem danh sách Hợp đồng theo tổng công ty | mọi HĐ, trừ Đang tạo của người khác |
| Xem Hợp đồng theo công ty | Xem danh sách Hợp đồng theo công ty | `company_id` = công ty đang làm |
| Xem Hợp đồng theo phòng ban | Xem danh sách Hợp đồng theo phòng ban | phòng ban mình quản lý |
| Xem Hợp đồng theo bộ phận | Xem danh sách Hợp đồng theo bộ phận | bộ phận mình quản lý |
| (không quyền) | — | chỉ HĐ mình tạo |

Cả 4 cấp: luôn thấy HĐ mình tạo; HĐ **Đang tạo** của người khác bị ẩn (câu hỏi Q1).
Đụng: seeder (đổi tên + `RENAMED`), `ContractController::scopedContractQuery`, FE `index.vue` (4 cờ). Thêm migration index.

## 3. Hiện trạng bộ lọc
Ô tìm nhanh: mã HĐ, tên khách hàng. Nâng cao: Công ty–Phòng ban–Bộ phận–**Người lập** (4 ô) · Khách hàng · Trạng thái (liệt kê đủ 10 trạng thái enum ERP, HRM chỉ dùng 4) · Ngày ký (khoảng).

## 4. Đề xuất bộ lọc (user duyệt từng dòng)

| # | Ô lọc | Kiểu | Nguồn | Đề xuất |
|---|---|---|---|---|
| 0 | Ô tìm nhanh: mã HĐ, số HĐ, mã báo giá, mã KH, tên KH, MST KH | text (Enter) | ERP có mã HĐ; còn lại mới | ✅ |
| 1 | Công ty – Phòng ban – Bộ phận – **Người tạo** | cụm 4 ô (giữ) | ERP có | ✅ đổi nhãn "Người lập" → "Người tạo" |
| 2 | Khách hàng | select tìm từ xa (giữ) | ERP có | ✅ |
| 3 | Trạng thái | **chọn nhiều**, chỉ 4 trạng thái HRM dùng (Đang tạo · Chờ duyệt · Có hiệu lực · Đã thanh lý) | ERP có | ✅ |
| 4 | Ngày ký | khoảng (giữ) | — | ✅ |
| 5 | Ngày hiệu lực | khoảng | mới | ✅ |
| 6 | Ngày hết hạn | khoảng | mới | ✅ |
| 7 | Ngày tạo | khoảng | ERP có (lọc theo `created_at`) | ✅ |
| 8 | Bảng giá | select | ERP có | ✅ |
| 9 | Người duyệt | select nhân viên | ERP có | ✅ |
| 10 | Hàng hoá (mã / tên / model) | text (Enter), 1 ô | ERP có 3 ô riêng | ✅ gộp 1 ô |
| 11 | Giá trị hợp đồng (sau VAT) | khoảng số tiền | mới | ⚪ tuỳ chọn |
| 12 | Ngày kết thúc thực hiện | khoảng | mới | ⚪ tuỳ chọn |
| 13 | Lắp đặt (Có / Không) | select | mới | ⚪ tuỳ chọn |
| 14 | Phòng thực hiện (chính / hỗ trợ) | select phòng ban | mới | ⚪ tuỳ chọn |

Không đề xuất: Dự án TKT (báo giá đã bỏ gắn dự án từ 13/10), SĐT khách (ERP có — HRM chưa có cột, dùng ô tìm nhanh qua mã/tên KH).
Mọi ô theo `V2BaseSmartFilterPanel` + `floating`; ô chọn → tìm luôn, ô gõ → Enter.

## 5. Quyết định đã chốt (27/10/2026)
- **Q1:** HĐ **Đang tạo** của người khác **ẩn ở cả 4 cấp** (khớp ERP). Mọi cấp vẫn thấy HĐ mình tạo ở mọi trạng thái.
- **Q2:** Tên quyền dùng **"Hợp đồng bán hàng"**: `Xem tất cả Hợp đồng bán hàng` · `Xem Hợp đồng bán hàng theo công ty` ·
  `Xem Hợp đồng bán hàng theo phòng ban` · `Xem Hợp đồng bán hàng theo bộ phận` (đổi tên từ 4 tên cũ qua `RENAMED`).
- **Q3:** Làm **đủ 15 dòng** ở mục 4 (cả 11 dòng ✅ lẫn 4 dòng tuỳ chọn: Giá trị HĐ, Ngày kết thúc thực hiện, Lắp đặt, Phòng thực hiện).
- Trạng thái đề xuất: đã chốt nội dung, **chưa được phép code** (chờ câu cho phép riêng).
