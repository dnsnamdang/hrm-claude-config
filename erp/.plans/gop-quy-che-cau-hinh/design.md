# Gộp Quy chế – Cấu hình về 1 màn "Khai quy chế – cấu hình – chi tiết"

> **Trạng thái:** Thiết kế GIAO DIỆN (UI). Logic/endpoint/DB migration **chưa** nằm trong scope — làm sau.
> **Dự án:** ERP TanPhatDev (Laravel · Blade + AngularJS 1.3.9 · Bootstrap 4). Ngày: 2026-09-08.
> **Mockup:** Artifact `88e82524-…` (file `regulation-config-mockup.html` kèm session).

---

## 1. Mục tiêu & phạm vi

Gộp toàn bộ **cấu hình** + **quy chế công ty** + **quy chế kinh doanh theo phòng ban** đang nằm rải rác ở nhiều màn về **1 màn duy nhất** "Khai báo quy chế – cấu hình". Đây là bản thiết kế **giao diện + kiến trúc thông tin (IA)**; phần logic (đọc/ghi, migrate, endpoint mới, bảng lịch sử còn thiếu) để giai đoạn sau.

### Quyết định nền tảng (chốt 2026-09-08)

1. **KHÔNG còn tầng "Toàn hệ thống".** Mọi cấu hình trước đây khai chung toàn hệ thống (`configs` single-row) **đều chuyển thành khai theo công ty**. Mỗi công ty tự khai cấu hình của mình, không dùng chung.
2. **Công ty lấy theo tài khoản đăng nhập** — **không có dropdown chọn công ty**. Màn hiển thị công ty hiện tại dạng nhãn chỉ-đọc để người dùng biết đang cấu hình cho công ty nào.
3. Còn **2 phạm vi**: ① **Theo công ty** (của mình) · ② **Theo phòng ban – bộ phận**.
4. **"Chặn quá hạn" (`due_configs`) KHÔNG đưa vào màn này** — giữ nguyên màn riêng hiện có, không nhúng.

**Trong scope (thiết kế UI):**
- Mô hình 2 phạm vi + thanh ngữ cảnh (công ty theo login + chọn phòng ban/bộ phận cho ②).
- Bố cục màn (master–detail + lịch sử).
- Danh sách nhóm cấu hình theo từng phạm vi + field từng nhóm.
- 3 kiểu vùng chi tiết (form · grid+modal · bậc thang) + quy ước chung.
- Điều hướng vào màn + nguyên tắc di trú màn cũ.

**Ngoài scope (để giai đoạn logic):**
- Endpoint mới, service, DB migration, bảng lịch sử cho phần trước-đây-global.
- **Migrate dữ liệu global `configs` → per-company** (nhân bản giá trị hiện tại cho từng công ty).
- Migrate/tạo mới điều khoản thanh toán theo công ty.
- Redirect/gỡ bỏ các màn cũ.

---

## 2. Hiện trạng — bản đồ nơi lưu (khảo sát code)

Trước đây dữ liệu nằm ở **3 tầng**; theo mô hình mới, **tầng global gộp xuống company**:

| Tầng (cũ) | Nơi lưu hiện tại | Xử lý theo mô hình mới |
|---|---|---|
| **Toàn hệ thống** (1 dòng chung) | `configs` (single-row) · `contract_rows` · `service_price_config` | **Chuyển thành per-company** (migrate giá trị global → mỗi công ty) — việc của giai đoạn logic |
| **Theo công ty** | cột trên `companies` · JSON `companies.config_settlement_period` · bảng con price/product types | Giữ nguyên, **nhận thêm các field vốn là global** |
| **Theo phòng ban / bộ phận** | `regulations` (polymorphic `objectable`) · cột `departments.*` / `parts.*` · `regulation_histories` | Giữ nguyên |
| ~~Chặn quá hạn~~ | `due_configs` / `company_due_configs` | **Không thuộc màn này** — giữ màn riêng |

**Field vốn trùng 2 nơi (global + company)** giờ **chỉ còn 1 nơi (company)** → hết vấn đề "field nào thắng lúc runtime": SL nhân viên tối đa/phòng, KM hỗ trợ VC, hàng cập nhật giá, hệ số giá vốn dịch vụ…

**Chưa có màn khai:** điều khoản thanh toán mặc định; cột "% đặt cọc – điều kiện giữ hàng" (xác minh cột chính xác khi làm logic).

**Pattern UI có sẵn tái dùng:**
- `companies/{id}/regulations` — form cấu hình per-company nhiều field.
- `departments/{id}/regulations` — **3 tab quy chế/thưởng** (grid hoa hồng + bậc thang + form) — nền của phạm vi ②.
- `regulationFormModal.blade.php` — modal CRUD 1 quy chế hoa hồng.
- Submit: AJAX + `ResponseTrait` (`responseSuccess`/`responseErrors`) → `toastr`.

---

## 3. Mô hình phạm vi & thanh ngữ cảnh

Thanh ngữ cảnh đầu màn gồm 2 khối:

- **Công ty đang cấu hình** — nhãn **chỉ-đọc** (badge, icon tòa nhà, chú thích *"theo tài khoản đăng nhập"*). Không chọn được.
- **Phạm vi áp dụng** — toggle **2 lựa chọn**:

| # | Phạm vi | Ngữ cảnh cần chọn | Kiểu khai |
|---|---|---|---|
| ① | **Theo công ty** | (không cần — công ty theo login) | 1 bộ giá trị cho công ty |
| ② | **Theo phòng ban – bộ phận** | dropdown **Phòng ban / Bộ phận** (`optgroup` tách 2 cấp) | **giữ nguyên 3 tab quy chế/thưởng ERP** cho đơn vị đã chọn |

**Thanh ngữ cảnh đổi theo phạm vi:** ① chỉ nhãn công ty + toggle + Lưu/Hủy · ② hiện thêm dropdown Phòng ban / Bộ phận. **Chọn đơn vị trước rồi khai** (department-first).

---

## 4. Bố cục màn (master–detail)

```
┌────────────────────────────────────────────────────────────────────┐
│ Khai quy chế – cấu hình   [🏢 Công ty (login)]  [Phạm vi ①②]  Lưu Hủy│
├───────────────┬────────────────────────────────────────────────────┤
│ DANH SÁCH NHÓM│  <Tên nhóm đang chọn>                    [chip PV]  │
│ (nav dọc,     │  ┌──────────────────────────────────────────┐       │
│  badge đếm)   │  │  Vùng khai chi tiết:                     │       │
│ • Nhóm A  (5) │  │   – FORM field (① + "Quy chế khác" ②) HOẶC│      │
│ • Nhóm B  (3) │  │   – GRID hoa hồng+modal / LADDER (②)      │       │
│ • Nhóm C  (4) │  └──────────────────────────────────────────┘       │
├───────────────┴────────────────────────────────────────────────────┤
│ 🕘 Lịch sử thay đổi (theo nhóm + phạm vi đang chọn)      [Xem tất cả]│
└────────────────────────────────────────────────────────────────────┘
```

- **Cột trái**: danh sách nhóm (nav dọc, badge đếm). Nhóm đổi theo phạm vi.
- **Cột phải**: chi tiết nhóm đang chọn (form hoặc grid/bậc thang tùy nhóm).
- **Dưới cùng**: panel **Lịch sử thay đổi** theo nhóm + phạm vi đang chọn.

---

## 5. Danh sách nhóm theo từng phạm vi

### ① Theo công ty (nền `companies` + bảng phụ, **đã gộp toàn bộ field global cũ**)

| Nhóm | Field chính | Nơi lưu (tham khảo) |
|---|---|---|
| **Chung** | Logo, Tiêu đề (theo công ty), Mô tả | `configs.logo/title/description` → chuyển per-company |
| **Báo giá – Hợp đồng** | Số ngày hiệu lực báo giá (+ dự án); thời gian đăng ký KH; % hiệu quả HĐ tối thiểu; % thưởng thực hiện HĐ tối đa; % tối thiểu hưởng DS người lập HĐ; SL nhân viên tối đa/phòng; điều khoản báo giá mặc định (+ dịch vụ); ràng buộc lập HĐ theo thị trường | `configs.quotation_valid_days`/`project_quotation_valid_days`/`customer_register_expiry`/`quotation_footer`/`service_quotation_footer`/`is_equipment…` (→ company) + `companies.minimum_stipulation_effect_contract`/`revenue_calculates_productivity_bonus`/`min_sale_bonus_percent`/`max_employee_on_department` |
| **Kỹ thuật** | Đơn giá công; công khoán; bảng tính công khoán | `companies.work_price`/`work_bond` + `contract_rows` |
| **Giá bán** | Hệ số giá bán DV; hệ số giá bán DV thuê ngoài; hệ số giá vốn DV; hệ số giá TMĐT; định mức đàm phán giá | `companies.coefficient_price_service`/`coefficient_price_service_outsource` + `configs.coefficient_cost_price_service`/`coefficient_ecommerce_price`/`service_price_config` (→ company) |
| **Chiết khấu & hỗ trợ bán hàng** | % chiết khấu dịch vụ; % chiết khấu hàng làm DV; số KM hỗ trợ VC; giá trị đơn hàng hỗ trợ VC | `companies.per_discount_service`/`per_discount_prod_service`/`company_pay_km`/`pay_value_order` |
| **Tổ chức bán hàng & thị trường** | Phân thị trường theo; phòng ban / nhóm KH không ràng buộc thị trường | `companies.market_division_type` + `configs.department_groups`/`customer_groups` (→ company) |
| **Công nợ & tài chính** | Ngày khai báo công nợ đầu kỳ; hạn mức công nợ xuất hàng NV; số dư lẻ tối đa điều chỉnh; số ngày quá hạn tính lãi (bán lẻ/đại lý/DV); cảnh báo thu nợ đến hạn; lãi suất %; thuế vận tải | `companies.limit_export_debt_employee`/`adjust_odd_balance`/`overdue_date_max_*`/`warning_due_date`/`interest_rate` + `configs.debt_calculation_date`/`vat_delivery_trip_percent` (→ company) |
| **Xuất – nhập hàng** | Số ngày cảnh báo mượn/giữ; hạn xuất hàng nhập thẳng; giới hạn giá trị hàng mượn; SL hàng tờ khai HQ; số ngày vượt thời gian giao; % đặt cọc giữ hàng; giá trị giữ hàng khác; số ngày giữ tối đa (HĐDA/hàng gửi/thường); số ngày mượn tối đa | `companies.overdue_date_export_direct`/`borrow_limit_value`/… + `configs.warning_day`/`max_prepick_date*`/`consignment_holding_time`/`max_borrow_date` (→ company); % đặt cọc: cột cần xác minh |
| **Hàng hóa** | Tính chất hàng hóa; hàng không bắt buộc serial; nhãn hiệu áp dụng; hệ số thuế BVMT; quy tắc duyệt giá (cập nhật/cần duyệt/mới/reset) | `configs.product_types`/`serial_product_types`/`environment_tax`/`is_company_price…` (→ company) + `companies.brand_ids` |
| **Kỳ quyết toán** | Kỳ quyết toán theo năm | `companies.config_settlement_period` (JSON) |
| **Điều khoản** *(NOTE)* | Điều khoản báo giá / thanh toán theo công ty | báo giá: từ `configs` → company; **thanh toán chưa có màn** → tạo mới khi làm logic |

> **Không đưa vào màn:** "Chặn quá hạn" (`due_configs`/`company_due_configs`) — giữ màn riêng theo yêu cầu.

### ② Theo phòng ban – bộ phận (nền `regulations` + `departments`/`parts`)

Giữ nguyên **3 tab quy chế/thưởng** của màn `departments/{id}/regulations` — KHÔNG dựng bảng phẳng. Sau khi chọn Phòng ban/Bộ phận, cột trái hiện 3 nhóm = 3 tab ERP. Ánh xạ khái niệm docx → tab thật:

| Nhóm (cột trái) | = Tab ERP | Kiểu vùng chi tiết | Field / Nơi lưu | Ánh xạ docx |
|---|---|---|---|---|
| **Quy chế hoa hồng / năng suất** | Tab 1 "Danh mục quy chế tính hoa hồng" | **GRID nhiều dòng + modal** (§6.B) | `regulations` (polymorphic): áp dụng cho (tính chất hàng) · bảng giá · khoảng giá net · NS tháng % · NS quý % · phân chia HĐ (TP/TBP/NV) · phân chia NS (TP/TBP/NV) · trạng thái | **"Thưởng năng suất tháng, quý"** (user xác nhận = danh mục quy chế hoa hồng) |
| **Thưởng thêm quý (lũy tiến)** | Tab 2 | **Bậc thang + khối tỉ lệ chia lũy tiến** (§6.C) | `departments` cột bậc thang + `rate_reward_progressive_tp/tbp/nv` (Part có cột tương ứng) | **"Thưởng lũy tiến"** |
| **Quy chế khác** *(chỉ Phòng ban)* | Tab 3 | **FORM 3 trường** (§6.A) | `departments.risk_fund` (quỹ rủi ro / thưởng cuối năm) · `departments.profit_percent` (% hưởng LN) · `departments.max_value_contract` (hạn mức HĐ TP duyệt) | **"Quỹ rủi ro" · "% Hưởng lợi nhuận" · "Quy chế duyệt"** |

**Phòng ban vs Bộ phận (theo ERP):** màn Bộ phận (`parts/{id}/regulations`) chỉ có **2 tab** — thiếu tab "Quy chế khác". Vì vậy nhóm **Quy chế khác** đánh dấu `deptOnly` và **tự ẩn** khi đang chọn Bộ phận (banner giải thích). Bộ phận không khai quỹ rủi ro / %LN / hạn mức duyệt.

> **Ghi chú "Thưởng năm":** docx liệt kê "Thưởng năm" như 1 mục riêng, nhưng ERP không có tab độc lập — bản chất là **quỹ rủi ro / thưởng cuối năm** (`departments.risk_fund`) ở Tab 3. Đã gộp vào "Quy chế khác", không tạo nhóm thừa.

---

## 6. Kiểu vùng chi tiết

Ba kiểu: **A. FORM** (① + nhóm "Quy chế khác" của ②); **B. GRID + modal**, **C. LADDER** (② — bê nguyên cấu trúc 3 tab `departments/{id}/regulations`).

### A. FORM
- Render field theo loại: **số** (input + đơn vị %/ngày/đồng), **text**, **rich-text** (điều khoản/mô tả), **toggle/checkbox** (ràng buộc thị trường, cờ hàng hóa), **multi-select** (nhóm KH, phòng ban, tính chất hàng hóa, nhãn hiệu), **upload** (logo), **bảng con** (`contract_rows`, kỳ quyết toán). Gom field trong lưới 2 cột co giãn.
- Ở ② "Quy chế khác": 3 trường số (quỹ rủi ro %, % hưởng LN, hạn mức HĐ được duyệt) + banner "chỉ khai ở cấp Phòng ban".

### B. GRID nhiều dòng + modal (② nhóm "Quy chế hoa hồng / năng suất" = Tab 1 ERP)
- **Bảng danh mục** mỗi dòng = 1 quy chế hoa hồng của đơn vị: STT · Áp dụng cho · Bảng giá · Giá net so sánh · **NS tháng %** · **NS quý %** · Phân chia HĐ (TP/TBP/NV) · Phân chia NS (TP/TBP/NV) · Trạng thái · Thao tác (sửa/xóa).
- Nút **"+ Thêm mới"** / icon sửa mở **modal** (mirror `regulationFormModal.blade.php`), gồm fieldset: **Điều kiện áp dụng** (tính chất hàng, bảng giá, áp dụng từ ngày, trạng thái) · **So sánh giá net** (toán tử + khoảng từ–đến) · **Thưởng NS tháng** · **Thưởng NS quý** · **Phân chia theo HĐ** (TP/TBP/NV) · **Phân chia theo NS** (TP/TBP/NV).
- Phân trang khi nhiều dòng. Map thẳng sang `regulations` khi làm logic.

### C. LADDER — bậc thang + tỉ lệ chia lũy tiến (② nhóm "Thưởng thêm quý" = Tab 2 ERP)
- **Bảng bậc thang** theo *Tổng hoa hồng của phòng*: mỗi bậc = Toán tử-từ · Giá trị-từ · Toán tử-đến · Giá trị-đến · **Tỉ lệ %**. Nút "+ Thêm bậc" / xóa bậc.
- **Khối "Tỉ lệ chia lũy tiến"**: 3 ô % **Trưởng phòng / Trưởng bộ phận / Nhân viên** (map `rate_reward_progressive_tp/tbp/nv`) + hiển thị tổng %.

*(`regulations` polymorphic cả Department lẫn Part; ngữ cảnh cấp đơn vị lấy từ dropdown Phòng ban/Bộ phận, không cần cột chọn cấp trong bảng.)*

---

## 7. Quy ước chung

- **Lưu/Hủy:** nút Lưu cấp màn nhưng **chỉ lưu nhóm đang mở** (tránh ghi đè nhóm khác). Chuyển nhóm/phạm vi/đơn vị khi chưa lưu → **cảnh báo mất dữ liệu**. AJAX + `ResponseTrait` + `toastr`.
- **Validate:** lỗi inline từng field (`is-invalid` + `invalid-feedback`), BE rethrow `ValidationException`; grid hoa hồng validate trong modal; bậc thang chặn khoảng chồng lấp.
- **Lịch sử thay đổi:** panel dưới — Thời gian / Người thực hiện / Nội dung / Phạm vi / Ghi chú. ② có nền `regulation_histories`; ① (company) — nền `company_regulation_historys`; các field vốn global **chưa có bảng lịch sử theo công ty** → bổ sung khi làm logic.
- **Phân quyền (fail-closed):** công ty lấy từ tài khoản đăng nhập → chỉ khai được công ty của mình; ② theo quyền phòng ban/bộ phận hiện có. **Không hard-code `= true`**, ẩn nút Lưu nếu thiếu quyền; BE tự kiểm quyền + kiểm công ty đúng với tài khoản trước khi trả/ghi.
- **Trạng thái rỗng:** ② chưa chọn phòng ban/bộ phận → hiện hướng dẫn "Chọn phòng ban / bộ phận để bắt đầu khai".

---

## 8. Điều hướng & di trú màn cũ

- Thêm menu **"Danh mục chung → Quy chế – Cấu hình"**, route mới đề xuất `admin/regulation-config`.
- Màn mới **kế thừa** dữ liệu/endpoint cũ; **không xóa** các màn cũ (`configs/edit`, `companies/{id}/regulations`, `departments/{id}/regulations`, `parts/{id}/regulations`, `sale/service-config-price`) ngay. Redirect/gỡ để giai đoạn logic.
- **`due_configs/edit` (Chặn quá hạn) giữ nguyên** — không gộp, không đụng.

---

## 9. Điểm để lại cho giai đoạn LOGIC (open questions)

1. **Migrate global → per-company:** nhân bản giá trị `configs` (single-row) hiện tại xuống cột/bảng của **từng công ty**; xác định công ty nào là "nguồn chuẩn" ban đầu.
2. **Field global chưa có chỗ chứa per-company:** một số field global chưa có cột tương ứng trên `companies` → cần thêm cột / bảng phụ per-company khi migrate.
3. **NOTE docx:** tạo mới điều khoản **thanh toán** theo công ty (hiện chưa có màn); điều khoản báo giá chuyển từ global → company.
4. **Bảng lịch sử theo công ty** cho các field vốn global → bổ sung nếu muốn hiển thị lịch sử phạm vi ①.
5. **Cột "% đặt cọc – điều kiện giữ hàng":** xác minh cột chính xác trên `companies`.
6. Route/permission mới cho màn gộp + kiểm ràng buộc "công ty = công ty của tài khoản đăng nhập".
7. Trường hợp tài khoản quản trị nhiều công ty (nếu có) — hiện chốt 1 công ty theo login; xử lý sau nếu phát sinh.

---

## 10. Tài sản kèm theo
- **Mockup HTML** (2 phạm vi, công ty theo login, master–detail, grid hoa hồng + modal, bậc thang, lịch sử) — Artifact `88e82524-…` / file mockup kèm session.
- **Spec tab gốc:** `Gộp quy chế - cấu hình ERP.docx` (bản text ở scratchpad `gop-quy-che-spec.txt`).
