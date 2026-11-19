# Yêu cầu bổ sung HĐ bán (nhận 10/11/2026) — đối chiếu với code HRM

Nguồn: **yêu cầu của khách hàng** (user xác nhận 10/11), user dán vào session 10/11. Chưa có hạn chót; đề xuất chia 5 đợt, bắt đầu đợt 1 (bắt buộc nhập + điều kiện chuyển duyệt). Đối chiếu bằng đọc code worktree `wt-hop-dong-ban` (nhánh `gop_db-xuat-hang-cha-con`)
+ cột DB rehearsal. "Chưa kiểm xong" = mới đọc tới chỗ gọi, chưa lần tới gốc.

| # | Yêu cầu | Hiện có | Thiếu |
|---|---|---|---|
| 1 | Ghi chú nội bộ từng mã hàng (thêm/sửa/xem/duyệt HĐ gốc + phụ lục) | Cột `hrm_contract_product_prices.note`, form hiện icon ghi chú (`edit.vue:399`) | Chưa rõ `note` là ghi chú nội bộ hay ghi chú in ra bản in — chưa kiểm xong; màn duyệt chưa kiểm |
| 2 | Ngày ký theo popup Xác nhận KH đã ký | `sign_date`, `customer_signed_at` | Kiểm hiển thị |
| 3 | Ngày hiệu lực khi thoả điều kiện | `effective_date`, `recomputeEffectiveDates` (Phase 24 Q15) | — |
| 4 | Điều kiện hiệu lực bắt buộc khi gửi duyệt (Ký / Cọc lần đầu / Bảo lãnh duyệt) | `effective_condition` 1/2/3 | Đang `nullable` ở Request — chưa bắt buộc khi gửi duyệt |
| 4a | Bảo lãnh: sau KH ký có nút "Xác nhận bảo lãnh được duyệt", bắt buộc file + ngày hiệu lực | Chỉ có ô `guarantee_approved_date` trong form | Thiếu nút/popup riêng + file đính kèm |
| 5 | Thời gian thực hiện: số ngày + 4 điều kiện; điều kiện 2–4 thì KD nhập ngày tương ứng | `execution_deadline_days`, `execution_deadline_base` 1–4, `execution_base_date` | `nullable` — chưa bắt buộc; ngày mốc hiện nhập trong form, yêu cầu là nhập SAU (khi KH bàn giao) — cần nút/popup cập nhật ngày mốc |
| 6 | Chưa đủ mốc tính thời gian thực hiện ⇒ xuất hàng / xuất giữ cảnh báo + chuyển duyệt TP → BGĐ | `can_export` hiện CHẶN hẳn khi thiếu ngày hiệu lực / thời hạn | Thiếu luồng "cho xuất nhưng phải duyệt TP→BGĐ" ở YCXH và xuất giữ |
| 7 | Ngày hết hiệu lực = mốc + số ngày | `execution_end_date` (`ContractService:1584`) | Kiểm tên hiển thị |
| 8 | Cảnh báo giao hàng: số ngày cảnh báo trước | — | Thiếu cột + job cảnh báo PM |
| 9 | Tiến độ thanh toán chi tiết (lần 1 theo ngày ký; trung gian: duyệt TK / giao hàng / lắp đặt / chạy thử — nhập ngày + biên bản, cảnh báo KT; lần cuối: nghiệm thu) | `hrm_contract_process_payments` (milestone text, payment_condition_id, offset_days, deadline) | Thiếu loại mốc chuẩn hoá, ngày + biên bản theo mốc, cảnh báo thu tiền / công nợ quá hạn |
| 10 | Kế hoạch giao hàng: hàng nào giao khi nào, ngày đích danh hoặc khoảng | — (Phase 11 để ngoài phạm vi, Redmine #11252) | Thiếu bảng + UI |
| 11 | Cấu hình cảnh báo HĐ sắp hết hiệu lực cho NVKD | — | Thiếu cấu hình + job |
| 12 | Mẫu in: nhận diện HĐ sửa mẫu / tuân thủ mẫu; tách sửa mẫu in khỏi duyệt HĐ | Phase 27: cờ Pháp chế theo chữ (`need_legal_approval`) | Ghi chú "bàn với a Nam" — cần chốt hướng |
| 13 | Phụ lục điều chỉnh điều khoản | HĐ bán HRM chưa có phụ lục (chỉ thấy `addition_annex` ở màn Phiếu chờ giao việc, nguồn ERP) | Thiếu cả tính năng phụ lục |
| 14 | Điều kiện chuyển duyệt I–IX | `composeBgdReasons`: over_limit (vượt trội > hạn mức phòng), regulation (cờ quy chế phòng), under_net, regulation_changed | Xem bảng dưới |

### 14 — điều kiện chuyển duyệt

| Mục | Yêu cầu | Hiện có |
|---|---|---|
| I | Doanh số vượt trội khác 0 | Chỉ khi % vượt trội > hạn mức phòng (`max_extra_price_percent`) — LỆCH. ERP cũng theo hạn mức phòng (`FirmContractService:1499`) |
| II | Sửa khác quy chế (thưởng năng suất, tỷ lệ chia thưởng, tỷ lệ phòng, M14 ≠ 10%, sửa 15 → 14) | `regulation_changed` (Phase 26) — cần đối chiếu đủ 4 ý |
| III | Chi phí dự phòng ≠ 0 | Chưa thấy |
| IV | Mục 13 còn lại sau đàm phán theo định mức hoa hồng phòng (> −5%) | Chưa thấy |
| V | Bán dưới giá net (13 < 0) VÀ thưởng NVKD (12) ≠ 0; áp HĐ gốc, phụ lục, HĐ dịch vụ, HĐ dự án | `under_net`: `marketCosts != 0 && drbv < 0` — chưa kiểm xong có đúng là mục 12/13 |
| VI | Checkbox phòng ban "Trưởng phòng không được duyệt HĐ" | `regulation` (changeApprover) — chưa kiểm xong có phải đúng checkbox này |
| VII | Giá trị HĐ > 500tr (theo cài đặt quy chế) | Chưa thấy |
| VIII | Nhóm KH không ràng buộc PCTT | Chưa thấy |
| IX | Quá hạn mức công nợ NV / KH | Chưa thấy |

## Quyết định / câu hỏi đợt 1

- [x] I (10/11): **giữ theo hạn mức phòng** (`max_extra_price_percent`), không đổi thành "vượt trội khác 0".
  ⚠ Đính chính: hạn mức = 0 hiện nghĩa là KHÔNG xét (HRM `if ($limit && $limit > 0)`, ERP `ContractService::overMaxExtraPricePercent` cũng bỏ qua khi 0)
  ⇒ đặt 0 KHÔNG ra "khác 0" như đã nói. Rehearsal: 102/103 phòng đang 0, 1 phòng 10%. Đang hỏi lại user.
- [x] I (10/11, chốt lại): **đổi nghĩa** — hạn mức = 0 ⇒ có vượt trội (≠ 0) là chuyển BGĐ; để TRỐNG (NULL) ⇒ không xét. Lệch ERP có chủ đích.
  Phát hiện kèm: HRM KHÔNG có ô sửa `max_extra_price_percent` (chỉ ERP `DepartmentsController` sửa được, lưu `?? 0` ⇒ không lưu được trống;
  sửa phòng ở ERP sẽ biến NULL thành 0). Cột DB nullable default 0. ⇒ hỏi tiếp: nơi cấu hình + xử lý 102 phòng đang 0.
- [x] I — nơi cấu hình (10/11 user): màn HRM **Khai Quy chế – Cấu hình**, nhóm "Theo phòng ban" → tab **Quy chế khác** (`id: 'khac'`,
  FE `components/regulation-config/data.js`, BE `Modules/MasterData/Support/RegulationTabRegistry.php:321` — ghi thẳng cột `departments`,
  có hẹn ngày hiệu lực + lịch sử). Thêm field `max_extra_price_percent` vào tab này (để trống được = không xét).
  Ghi chú: tab này đã có `max_value_contract` "Giá trị HĐ tối đa TP duyệt" — HĐ bán HRM CHƯA dùng ⇒ liên quan trực tiếp điều kiện VII (> 500tr).
  Rủi ro còn: màn Phòng ban ERP lưu `?? 0` ⇒ sửa phòng bên ERP biến trống thành 0.
- [x] I — user 10/11 "ok" chốt đề xuất dưới. User 10/11: "cấu hình phải rõ ràng, không bắt user đoán để trống là không xét" ⇒ BỎ ý "để trống = không xét".
  Đề xuất (chờ chốt): ô chọn tường minh "Chuyển BGĐ khi có DS vượt trội" (Không xét / Có vượt trội là chuyển / Vượt hạn mức %) + ô hạn mức %
  chỉ hiện khi chọn mức 3. Cột mới `departments.extra_price_approval_mode` (migration bảng dùng chung, ERP không đọc);
  dữ liệu cũ: hạn mức 0 ⇒ Không xét, > 0 ⇒ Vượt hạn mức (giữ nguyên hành vi sau deploy). ERP lưu 0 không ảnh hưởng chế độ ⇒ hết rủi ro ERP.
- [ ] II — đối chiếu 10/11 (`ContractSupportAccountingService::previewDiffersFromRegulation`): hiện xét 5 tỷ lệ phòng chính
  (`month_percent, after_commission_percent, month_employee/part_lead/department_lead_percent`) + 14.1 lệch số tự tính
  (14.1 tự tính = min(mục 15, % công ty × giá HHDV) — khớp "M14 10% giá công bố, phần dư nằm ở 15"; sửa 15 → 14 = đổi 14.1 ⇒ đã bắt).
  ĐÃ CÓ: II.1 thưởng năng suất, II.3 vế M14 ≠ 10%, II.4. CHƯA: II.2 tỷ lệ phân chia thưởng thực hiện HĐ (21.1.x) và
  II.3 tỷ lệ chia giữa các phòng (%DS mục 19) — Phase 26 5.3a cố ý cho đổi 2 nhóm này vẫn Duyệt (theo ERP). Đang hỏi user.
  - [x] 10/11 user: **THÊM** 21.1.x và mục 19 vào điều kiện chuyển BGĐ (lệch ERP có chủ đích, sửa ghi chú 5.3a Phase 26).
- [x] III (10/11): mục 16 `redundancy_cost` ≠ 0 ⇒ chuyển BGĐ. Rõ nghĩa, làm theo yêu cầu.
- [x] IV: lưới "Quy chế thưởng" theo phòng (tab `hoahong`, bảng ERP `regulations`) đã có khoảng điều kiện so với giá net
  (`condition_compare_value_start/end`) + ô tích "Chuyển duyệt Ban giám đốc" (`change_approver`); HĐ khớp dòng có tích ⇒ lý do `regulation`
  (đã có). ⇒ IV ĐÃ CÓ qua cấu hình. User xác nhận 10/11 — không code.
- [x] V: đã có `under_net` = thưởng NVKD (mục 12 = `sales_bonus`) ≠ 0 VÀ mục 13 (`discount_rate_before_vat`) < 0. Đúng yêu cầu cho HĐ bán.
  Vế "phụ lục, HĐ dịch vụ, HĐ dự án" ngoài phạm vi HĐ bán HRM (phụ lục chưa có).
- [ ] VI: cột `departments.department_lead_disapprove_contract`, ERP nhãn "Trưởng phòng không được duyệt hợp đồng" (`FirmContract::candisApprove`,
  `zt_accounting` ẩn Duyệt). HRM HĐ bán CHƯA dùng, màn cấu hình HRM chưa có ô ⇒ thêm ô vào tab Quy chế khác + lý do BGĐ.
- [ ] VII: `departments.max_value_contract` (đã có ô "Giá trị HĐ tối đa TP duyệt" ở tab Quy chế khác). ERP `FirmContract:1143`: TP chỉ duyệt được khi
  0/trống hoặc ≥ `total_after_vat`. HRM HĐ bán CHƯA dùng ⇒ thêm lý do BGĐ. (Lưu ý "trống/0 = không giới hạn" — trái ý user về cấu hình rõ ràng.)
- [x] VIII: PCTT = phân chia thị trường. ERP cấu hình công ty `configs.customer_groups` "Nhóm khách hàng không ràng buộc HĐ thị trường"
  (`FirmQuotationService::marketDivisionCustomerContract`; HRM màn cấu hình tab "Tổ chức bán hàng & thị trường" đã nối). Thêm lý do BGĐ:
  KH thuộc nhóm đó. Theo đúng chữ khách: chỉ nhóm KH, KHÔNG gồm "Phòng ban không ràng buộc thị trường" (`department_groups`).
- [ ] IX: hạn mức công nợ KH = `declare_limit_debts.limit_debt_export` (HRM đã dùng ở `ProductExportOverLimitService`: công nợ KH trên HĐ người lập
  + giá trị phiếu > hạn mức ⇒ YCXH qua TP → BGĐ; 0 = không xét). Hạn mức công nợ NV: ERP có `departments.over_limit_approval_employee`
  (dùng ở ProductExportRequest:1173) — CHƯA KIỂM XONG nghĩa/đơn vị. Đang hỏi user cách so khi duyệt HĐ.

### IX — khảo sát ERP cách tính công nợ + validate (10/11, user: "công nợ = số đã hạch toán vào tài khoản, không cộng giá trị HĐ")
- **Công thức (ERP `ProductExportRequestsController::getDebtCustomerByEmployee` :1024, `getDebtEmployee` :2165, `AccountDetail::getDebtEmployee` :2322):**
  `SUM(account_details.money_value_exchange) type=1 (Nợ) − type=2 (Có)` trên các TK con của **131** (`accounts.identify_number_parent = 131`),
  chỉ bút toán gắn HĐ (morph `contractable` ∈ HĐ hãng / HĐ dịch vụ / HĐ đầu kỳ [/ HĐ HRM ở bản HRM]).
  - Công nợ KH: lọc thêm `customer_id` và HĐ do **chính NV lập** (`contractable.created_by`) ⇒ là "công nợ của KH trên HĐ của NV đó", không phải toàn bộ KH.
  - Công nợ NV: mọi KH, HĐ do NV lập.
  - Không lọc công ty, không lọc ngày (bản AccountDetail có tham số ngày tuỳ chọn).
- **Hạn mức:** KH = `declare_limit_debts.limit_debt_export` theo (KH, công ty) — màn Khai báo hạn mức công nợ; 0/trống = không xét.
  NV = `employees.limit_export_debt`, thiếu thì `companies.limit_export_debt_employee` (HRM: tab cấu hình công ty "Hạn mức công nợ xuất hàng NV").
- **Validate hiện có:** chỉ ở YCXH (+ phiếu mượn bán): gửi duyệt ⇒ công nợ KH + giá trị phiếu > hạn mức ⇒ TP → BGĐ. Vế NV **bị comment** ở ERP (:2122–2136),
  không chạy. Duyệt HĐ ERP **không** xét công nợ.
- HRM `ProductExportOverLimitService::customerDebtByEmployee` port đúng công thức (lọc `account_details.created_by` thay vì người lập HĐ — CHƯA KIỂM XONG có khác nhau không).
- Áp cho duyệt HĐ (theo ý user): công nợ đã hạch toán (không cộng giá trị HĐ) > hạn mức ⇒ chuyển BGĐ. Câu hỏi còn: phạm vi công nợ KH.
- [x] IX phạm vi (10/11 user): **giống ERP** — công nợ KH trên các HĐ do người lập HĐ này lập. Rehearsal: `account_details.created_by` = người lập HĐ
  ở 100% bút toán 131 (HĐ hãng 69.948/69.948, HĐ dịch vụ 11.167/11.167) ⇒ lọc `account_details.created_by` của HRM tương đương. HĐ HRM chưa có
  bút toán trên rehearsal — CHƯA KIỂM bút toán HĐ HRM có ghi created_by = người lập HĐ không.
- [ ] IX vế NV (mặc định theo chữ khách, chưa hỏi): công nợ NV (mọi KH, HĐ do NV lập) > hạn mức NV (`employees.limit_export_debt`, thiếu thì
  `companies.limit_export_debt_employee`) ⇒ chuyển BGĐ. ERP comment vế này ở YCXH.

**Đợt 1 ⇒ Phase 31:** `design-phase31-dieu-kien-duyet.md` + `mockup-dieu-kien-duyet.html` (10/11). Chờ user duyệt design.

**Đợt 2 ⇒ Phase 32:** `design-phase32-moc-bao-lanh-xuat-hang.md` + `mockup-moc-bao-lanh-xuat-hang.html` (11/11). 3 câu chốt: nút xác nhận bảo lãnh (người lập, KH đã ký, ngày + file bắt buộc); nút cập nhật ngày mốc (người lập, sửa được, biên bản không bắt buộc); YCXH 20/21 khi HĐ thiếu mốc ⇒ TP → BGĐ theo quyền duyệt HĐ; xuất giữ để đợt sau. ĐÃ CODE 11/11 (nhánh gop_db-hd-dieu-kien-duyet, chưa commit).

- [x] I (11/11 chiều, ĐÍNH CHÍNH): ERP định mức "0.00" VẪN xét (decimal truthy) ⇒ có vượt trội là chuyển BGĐ. HRM theo ERP: migration 000004 (0.00 ⇒ chế độ 1) + lưu tab khác ghi số theo chế độ. Không còn là lệch ERP. VI giữ phòng của HĐ (lệch có chủ đích). Chi tiết design-phase31 mục 7.

## Đợt 3 — khảo sát 11/11 (mục 8, 9, 10, 11)

**Đã có (Phase 5e, 16/10):** `hrm_contract_process_payments` (payment_type Tạm ứng/Đặt cọc/Thanh toán, milestone chữ tự do, amount / amount_percent,
`payment_condition_id`, `offset_days`, `deadline` nhập tay — KHÔNG tự tính), danh mục `payment_conditions` 8 mốc: Kể từ ngày ký · Kể từ ngày HĐ có hiệu lực ·
Phê duyệt thiết kế · Giao hàng lần 1 / lần 2 có chữ ký KH · Lắp đặt có chữ ký KH · Chạy thử có chữ ký KH · Bàn giao nghiệm thu. Lệch tổng chỉ cảnh báo.
Rehearsal: 4 dòng (2 HĐ), chưa dòng nào có điều kiện. **Chưa có:** ngày mốc thực tế + biên bản theo từng mốc, hạn thu tự tính, cảnh báo thu tiền / công nợ quá hạn,
kế hoạch giao hàng (mục 10, Redmine #11252 để ngoài Phase 11), cảnh báo giao hàng (mục 8), cấu hình + job cảnh báo HĐ sắp hết hiệu lực (mục 11).
Khuôn có sẵn để dùng lại: nút + popup "ngày + biên bản" (Phase 32 `ContractExecutionBaseModal`, lịch sử meta cũ→mới), lệnh lịch `assign:activate-signed-contracts`.

**Yêu cầu khách (nguyên văn tóm):** Lần 1 = N ngày kể từ ngày ký · Lần trung gian (2/3/4) = Phê duyệt TK / Giao hàng có chữ ký KH / Lắp đặt / Chạy thử —
phải nhập ngày + biên bản, có cảnh báo kỹ thuật cập nhật biên bản; TK/lắp đặt/chạy thử: HĐ chọn "bao nhiêu ngày kể từ ngày hiệu lực"; Giao hàng: theo kế hoạch giao hàng ·
Lần cuối = Bàn giao nghiệm thu · Thanh toán 1 lần thì chọn 1 option bất kỳ. Kế hoạch giao hàng: hàng nào giao khi nào, ngày đích danh hoặc từ ngày…đến ngày.
Cảnh báo giao hàng: số ngày cảnh báo trước. Cấu hình cảnh báo HĐ sắp hết hiệu lực cho NVKD.

Câu hỏi tồn: đang hỏi user lần lượt (xem plan.md).

**Đợt 3 (12/11):** (d) Phase 33 cảnh báo HĐ sắp hết hiệu lực — đã deploy hrm_crm · (b)+(c) Phase 34 kế hoạch giao hàng + cảnh báo giao hàng — đã deploy hrm_crm ·
(a) Phase 35 tiến độ thanh toán chi tiết + cảnh báo thu tiền — đã deploy hrm_crm. Còn: đợt 4 phụ lục (mục 13 — 18/11 đang brainstorm, khảo sát ERP ở plan.md mục "Đợt 4"), đợt 5 mẫu in (mục 12, bàn với a Nam).
