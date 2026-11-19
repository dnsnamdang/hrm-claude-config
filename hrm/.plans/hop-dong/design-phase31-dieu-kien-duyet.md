# Phase 31 — Bắt buộc nhập khi gửi duyệt + điều kiện chuyển duyệt BGĐ (HĐ bán HRM)

Nguồn: **yêu cầu khách hàng** (10/11/2026), phân tích + từng quyết định ở `yeu-cau-bo-sung-10-11-gap.md`. Đây là đợt 1/5.
Mockup: `mockup-dieu-kien-duyet.html`.

## 1. Mục tiêu

- HĐ gửi duyệt phải có đủ điều kiện hiệu lực và thời gian thực hiện.
- Bộ điều kiện bắt HĐ lên BGĐ theo đúng 9 điều kiện khách đưa (I–IX). Cấu hình theo phòng nằm ở màn **Khai Quy chế – Cấu hình**,
  mỗi ô tự nói rõ nghĩa — không có giá trị "để trống / 0 = không xét" bắt user đoán (yêu cầu user 10/11).

**Không làm (đợt sau):** nhập ngày mốc thực hiện sau khi KH bàn giao (đợt 2), nút xác nhận bảo lãnh (đợt 2), xuất hàng khi chưa đủ mốc (đợt 2),
tiến độ thanh toán / kế hoạch giao hàng / cảnh báo (đợt 3), phụ lục (đợt 4), mẫu in (đợt 5). Vế V/IX cho phụ lục, HĐ dịch vụ, HĐ dự án.

## 2. Bắt buộc khi gửi duyệt (mục 4, 5)

- `ContractService::submit` thêm `assertExecutionTermsFilled`: thiếu `effective_condition`, `execution_deadline_days` (> 0),
  `execution_deadline_base` ⇒ 422, mỗi khoá một câu `Bắt buộc phải nhập`. Lưu nháp (Tạo / Sửa) giữ `nullable`.
- `execution_base_date` KHÔNG bắt khi gửi duyệt (đợt 2 cho nhập sau, khi sự kiện xảy ra).
- **Bỏ mặc định (chốt 11/11)**: `effective_condition` / `execution_deadline_base` vốn NOT NULL default 1 từ 14/08/2026 (commit `ac8cf78f4`, không ghi lý do;
  BE + FE còn tự điền 1) ⇒ kiểm bắt buộc vô tác dụng. Migration `2026_11_11_000002` đổi 2 cột nullable không default (không sửa dữ liệu),
  bỏ tự điền ở BE/FE/Resource; chưa chọn thì không tính Ngày hiệu lực / Ngày kết thúc thực hiện (không đoán theo ngày ký).
- FE: map 422 vào đúng 3 ô (khuôn form-validate: inline dưới ô, toast chung, cuộn tới lỗi đầu). Các ô nằm ở tab Thông tin chung.
  Gửi duyệt từ màn chi tiết (không ở form) — **chốt 11/11**: báo chính xác ô nào thiếu (tên từng ô, lấy từ 422)
  rồi chuyển sang màn Sửa; màn Sửa mở ra đã hiện sẵn lỗi dưới đúng 3 ô + cuộn tới ô đầu (lỗi chuyển sang qua store,
  không đặt lên URL). Nút Gửi duyệt KHÔNG khoá trước.

## 3. Cấu hình — tab "Quy chế khác" (theo phòng)

Tab đang có 3 ô (Quỹ rủi ro, % Hưởng lợi nhuận, Giá trị HĐ tối đa TP duyệt). Bố trí lại thành 2 khối, mỗi hàng đủ 12 cột:

**Khối "Quỹ & lợi nhuận"** — Quỹ rủi ro (%), % Hưởng lợi nhuận (giữ nguyên).

**Khối "Duyệt hợp đồng bán"**

| Ô | Kiểu | Giá trị | Cột `departments` |
|---|---|---|---|
| Chuyển BGĐ khi có DS vượt trội | chọn 1 | Không xét · Có vượt trội là chuyển · Vượt hạn mức | `extra_price_approval_mode` (MỚI, tinyint 0/1/2) |
| Hạn mức DS vượt trội | số % (0 < x ≤ 100), chỉ hiện + bắt buộc khi "Vượt hạn mức" | | `max_extra_price_percent` (có) |
| Giá trị HĐ TP được duyệt | chọn 1 | Không giới hạn · Có giới hạn | `max_value_contract_mode` (MỚI, tinyint 0/1) |
| Giá trị HĐ tối đa | số đồng > 0, chỉ hiện + bắt buộc khi "Có giới hạn" | | `max_value_contract` (có) |
| Trưởng phòng không được duyệt HĐ | ô tích | | `department_lead_disapprove_contract` (có, ERP dùng) |

- Đi chung pipeline của tab (hẹn ngày áp dụng + lịch sử). `RegulationTabRegistry` 'khac' thêm 3 field; field select kiểu `sel` có sẵn ở `data.js`.
- **Migration** (bảng `departments` dùng chung ERP; ERP không đọc 2 cột mới):
  - thêm `extra_price_approval_mode`, `max_value_contract_mode`;
  - đặt sẵn: `max_extra_price_percent > 0` ⇒ mode 2, còn lại 0; `max_value_contract > 0` ⇒ 1, còn lại 0 ⇒ **sau deploy không HĐ nào đổi hành vi**.
- ERP màn Phòng ban vẫn lưu `?? 0` vào 2 cột số — không ảnh hưởng vì chế độ nằm ở cột riêng. Không sửa ERP.
- `department_lead_disapprove_contract`: ERP đã có ô ở màn Phòng ban; HRM thêm ô ở đây, 2 nơi cùng ghi 1 cột.

## 4. Điều kiện chuyển BGĐ

Gom ở `ContractService::composeBgdReasons` (dùng cho cả bước TP từ preview HTHT và bước sau từ HTHT đã lưu). Khoá + câu hiện:

| | Khoá | Điều kiện | Câu hiện |
|---|---|---|---|
| I | `over_limit` (đổi) | mode 1: vượt trội ≠ 0 · mode 2: % vượt trội > hạn mức · mode 0: bỏ qua | `Có doanh số vượt trội` / `Doanh số vượt trội x% vượt hạn mức y% của phòng` |
| II | `regulation_changed` (mở rộng) | thêm: tỷ lệ chia thưởng thực hiện HĐ (21.1.x: `department/part/employee_bonus_contract_percent`) và tỷ lệ chia doanh số giữa các phòng (19, `commission_sale_percent` từng phòng) lệch quy chế | `Đổi tỷ lệ / thưởng so với quy chế` (giữ) |
| III | `redundancy` (mới) | mục 16 `redundancy_cost` ≠ 0 | `Có chi phí dự phòng` |
| IV | `regulation` (giữ) | dòng quy chế khớp có tích "Chuyển duyệt Ban giám đốc" | giữ |
| V | `under_net` (giữ) | thưởng NVKD (12) ≠ 0 và mục 13 < 0 | giữ |
| VI | `lead_cannot_approve` (mới) | phòng có tích "Trưởng phòng không được duyệt HĐ" | `Trưởng phòng của phòng không được duyệt hợp đồng` |
| VII | `over_value` (mới) | mode 1 và `total_after_vat` > `max_value_contract` | `Giá trị HĐ x vượt mức Trưởng phòng được duyệt y` |
| VIII | `free_market_group` (mới) | KH thuộc nhóm trong `configs.customer_groups` (chỉ nhóm KH, không gồm `department_groups`) | `Khách hàng thuộc nhóm không ràng buộc phân chia thị trường` |
| IX | `customer_debt` / `employee_debt` (mới) | công nợ đã hạch toán TK 131 (không cộng giá trị HĐ) > hạn mức. KH: công nợ của KH trên HĐ do người lập HĐ lập, hạn mức `declare_limit_debts.limit_debt_export` (KH × công ty HĐ, ≤ 0 bỏ qua). NV: công nợ mọi KH trên HĐ do người lập HĐ lập, hạn mức `employees.limit_export_debt` → thiếu thì `companies.limit_export_debt_employee` | `Công nợ khách hàng x vượt hạn mức y` / `Công nợ nhân viên lập HĐ x vượt hạn mức y` |

- Công thức công nợ dùng chung với YCXH: tách `ProductExportOverLimitService::customerDebtByEmployee` ra service công nợ dùng chung, thêm `employeeDebt`.
- Phòng xét = phòng của HĐ (`contract.department_id`), như I hiện tại. Công ty xét hạn mức KH = công ty của HĐ.
- Cổng giữ nguyên (Phase 24/26): có lý do + người duyệt không có quyền BGĐ ⇒ ẩn Duyệt, chỉ còn Chuyển duyệt BGĐ. Người có quyền BGĐ Duyệt thẳng.
- Hiển thị: khối cảnh báo đang có (`support-accounting.vue:12`, `_id/index.vue:25`) đổi từ 1 câu nối `;` sang **danh sách gạch đầu dòng** (9 lý do nối 1 dòng không đọc được).
- Ghi lý do vào lịch sử duyệt khi Chuyển duyệt (đang có `bgd_reasons` trong modal Chuyển duyệt — giữ).

## 5. Kiểm

- PHPUnit: mỗi lý do 1 ca có / không; I đủ 3 mode; VII 2 mode; IX hạn mức 0 bỏ qua; migration đặt sẵn mode đúng.
- Playwright: tab Quy chế khác (ẩn/hiện ô theo chế độ, lưu + hẹn), màn duyệt hiện danh sách lý do, gửi duyệt thiếu ô ⇒ lỗi dưới ô.
- Đo `bgdReasons` thêm 3 truy vấn (nhóm KH, 2 công nợ) — công nợ quét `account_details` (lớn) ⇒ EXPLAIN trước khi chốt.

## 6. Đã chốt (11/11)

- Công nợ IX: KHÔNG thêm index (user chốt 11/11). Đo rehearsal: 2 truy vấn ~48 ms lần đầu, 6 ms khi gọi lại cùng request (nhớ theo request);
  nặng nhất 228 ms (NV lập 1.424 HĐ). Nếu prod chậm thì xem lại index ghép trên account_details (bảng dùng chung ERP).

- Điều kiện VIII giữ đúng yêu cầu KH (user chốt 11/11): nhóm 9 "Khách hàng thương mại" + 30 "Trung tâm đăng kiểm xe cơ giới" (3.607 KH) —
  áp từ đầu 2026 thì ~7% HĐ hãng (1.284/17.621) lên BGĐ; không hỏi lại khách.

- Gửi duyệt từ màn chi tiết khi thiếu ô ⇒ báo chính xác ô thiếu rồi sang màn Sửa (mục 2).
- Công nợ IX: khi code EXPLAIN truy vấn `account_details` trước; chậm thì hỏi user chuyện thêm index. Kiểm luôn bút toán
  HĐ HRM có ghi `account_details.created_by` = người lập HĐ không (rehearsal chưa có bút toán HĐ HRM).

## 7. Đính chính sau khi kiểm ERP bằng chạy thật (11/11, chiều)

Kiểm: ERP local nhánh gop_db (worktree `wt-xuat-hang-cha-con`, cổng 8099, DB rehearsal, chặn mọi lệnh ghi) + tinker gọi thẳng hàm ERP.
- **I — ERP định mức `0.00` VẪN XÉT**: `FirmContractService::overMaxExtraPricePercent` viết `if ($max && …)`, cột decimal trả chuỗi `"0.00"` ⇒ PHP coi là đúng
  ⇒ có vượt trội là bắt chuyển BGĐ (câu "Hợp đồng vượt quá hạn mức Doanh số vượt trội…"). Chỉ NULL mới bỏ qua. Dữ liệu: 76/76 HĐ hãng 2026 có vượt trội
  (phòng 0.00) đều qua chuyển duyệt, HĐ không vượt trội chỉ 9%. ⇒ Mục 3 "ERP lưu `?? 0` không ảnh hưởng" là SAI.
  **Chốt 11/11:** theo ERP — phòng `0.00` ⇒ chế độ 1 "Có vượt trội là chuyển" (migration `2026_11_11_000004`), NULL ⇒ 0, > 0 ⇒ 2. Mục I thôi là "lệch ERP có chủ đích".
- **Đồng bộ số ↔ chế độ khi lưu tab Quy chế khác (chốt 11/11)** — ERP chỉ đọc con số, nên HRM ghi số theo chế độ:
  DS vượt trội: Không xét ⇒ `NULL` · Có vượt trội là chuyển ⇒ `0` · Vượt hạn mức ⇒ số nhập. Giá trị HĐ: Không giới hạn ⇒ `NULL` · Có giới hạn ⇒ số nhập.
  Lỗ còn lại (không sửa ERP): màn Phòng ban ERP lưu `?? 0` ⇒ sửa phòng bên ERP biến NULL thành 0 (= có vượt trội là chuyển ở ERP); `saveRiskFund` cho nhập
  `max_value_contract = 0` ⇒ ERP coi "0.0000" là hạn mức 0 (TP không duyệt được HĐ nào).
- **VI (chốt 11/11): giữ xét phòng của HĐ** — lệch ERP có chủ đích (ERP `candisApprove` xét phòng của chính người duyệt; Phòng Dự án 55 có 3/4 TP thuộc phòng khác).
- Khớp ERP (chạy so cùng dữ liệu): công thức công nợ KH/NV (6 NV, 11 cặp, khớp từng đồng); hạn mức KH (int, không dính "0.00"); hạn mức NV → công ty
  (double 0 ⇒ lấy công ty); VII nguồn phòng = phòng HĐ; VIII cấu hình `configs` 1 dòng/công ty; V = `switch_approve`.
- Lệch nhỏ còn ghi nhận: I ERP lấy phòng NGƯỜI LẬP (40/17.621 HĐ khác phòng HĐ) và mẫu số `total_cost` (HRM: tổng trước VAT).
