# Task 2 — Report: Tách biến NGÀY thành 2 dòng `_CHU` / `_SO` trong picker biến mẫu in

## STATUS: DONE

File sửa DUY NHẤT: `hrm-api/Modules/Human/Entities/PrintTemplateVariable.php`

---

## BƯỚC 1 — Đánh cờ `'is_date' => true` (tổng 42 dòng)

### DECISION_COMMON_VARIABLES (3)
- NGAY_QUYET_DINH
- NGAY_KY
- NGAY_HIEU_LUC

### DECISION_TYPE_VARIABLES
- **TYPE_ACCEPT_PERSONNEL (4):** THOI_GIAN_TIEP_NHAN_TU, THOI_GIAN_TIEP_NHAN_DEN, NGAY_SINH, NGAY_CAP_CMTND
- **TYPE_RENEW_LABOR_CONTRACT (4):** THOI_GIAN_TIEP_NHAN_TU, THOI_GIAN_TIEP_NHAN_DEN, NGAY_SINH, NGAY_CAP_CMTND
- **TYPE_APPOINT_PERSONNEL (2):** THOI_GIAN_BO_NHIEM_TU, THOI_GIAN_BO_NHIEM_DEN
- **TYPE_TRANSFER_PERSONNEL (2):** THOI_GIAN_DIEU_CHUYEN_TU, THOI_GIAN_DIEU_CHUYEN_DEN
- **TYPE_TERMINATION_LABOR_CONTRACT (2):** THOI_GIAN_BD_CHAM_DUT_HDLD, NGAY_SINH
- **TYPE_SUSPEND_LABOR_CONTRACT (3):** NGAY_SINH, THOI_GIAN_TAM_HOAN_TU, THOI_GIAN_TAM_HOAN_DEN
- **TYPE_RETIREMENT (1):** THOI_GIAN_BAT_DAU_NGHI_HUU
- **TYPE_EMPLOYEE_DISCIPLINE (3):** THOI_GIAN_KY_LUAT, NGAY_SA_THAI, NGAY_XAY_RA
- **TYPE_INCREASE_SENIORITY (3):** NGAY_XET_THAM_NIEN, NGAY_XET_TN, NGAY_XET_TN_GAN_NHAT
- **TYPE_TERMINATION_AND_SUSPEND_LABOR_CONTRACT (3):** THOI_GIAN_BD_CHAM_DUT_HDLD, THOI_GIAN_TAM_HOAN_TU, THOI_GIAN_TAM_HOAN_DEN

### LABOR_CONTRACT_COMMON_VARIABLES (2)
- NGAY_HOP_DONG, NGAY_SINH

### LABOR_CONTRACT_SUB_TYPE_VARIABLES
- **[LABOR_CONTRACT_MAIN] (3):** NGAY_HIEU_LUC, THOI_HAN_HOP_DONG, NGAY_CAP_CMTND
- **[LABOR_CONTRACT_APPENDIX] (1):** NGAY_CAP_CMTND

### PRINT_TEMPLATE_VARIABLES
- **[HOP_DONG_DAO_TAO] (4):** NGAY_KY_HĐLĐ, NGAY_SINH, NGAY_CAP_CCCD, NGAY_HIEU_LUC
- **[BIEN_BAN] (2):** NGAY_HOP, NGAY_XAY_RA

**Tổng: 42 dòng** (khớp `grep -c` = 42).

Đã KHÔNG đánh cờ: THOI_HAN (số tháng, MAIN), THOI_GIAN_DAO_TAO (chuỗi giờ), HAN_DANG_KY, CHU_KY_XET_TN, HE_SO_TN.

Lưu ý các biến trùng tên ở nhiều block xử lý qua context/`replace_all` đúng phạm vi:
- NGAY_SINH/NGAY_CAP_CMTND (ACCEPT + RENEW, block identical) → replace_all.
- THOI_GIAN_BD_CHAM_DUT_HDLD (TERMINATION + TERM&SUSPEND) → replace_all.
- NGAY_CAP_CMTND (MAIN + APPENDIX) → replace_all.
- NGAY_XAY_RA: BIEN_BAN (form có `template_type_id`) và DISCIPLINE (form ngắn) xử lý riêng.
- NGAY_SINH TERMINATION vs SUSPEND: phân biệt bằng context (TERMINATION có TRINH_DO_HOC_VAN, SUSPEND thì NGAY_SINH/NOI_CU_TRU/CCCD liên tiếp).

---

## BƯỚC 2 — Thêm method `expandDateVariables`
Thêm `protected static function expandDateVariables(array $items): array` ngay sau `buildObjectsForGroup`, trước dấu `}` đóng class. Với item `is_date=true` sinh 2 item `_CHU` + `_SO` (kèm mô tả dạng chữ/dạng số), ẩn item gốc; item thường giữ nguyên (unset `is_date`).

## BƯỚC 3 & 4 — 4 điểm gọi expandDateVariables
1. `buildSubTypeVariables` — block THÔNG TIN CHUNG: `'items' => self::expandDateVariables($commonVariables)`.
2. `buildSubTypeVariables` — block sub-type: `'items' => self::expandDateVariables($subTypeVariables)`.
3. `buildObjectsForGroup` — dòng đầu: `$items = self::expandDateVariables(is_array($items) ? $items : $items->all());` (trước `collect($items)->map(...)`).
4. Định nghĩa method (BƯỚC 2) — điểm khai báo dùng chung cho cả 3 call site trên.

(2 call site trong buildSubTypeVariables phục vụ QUYẾT ĐỊNH + HĐLĐ; call site trong buildObjectsForGroup phục vụ BIEN_BAN, HOP_DONG_DAO_TAO, và các loại khác dùng nhánh groupBy.)

---

## VERIFY (output thực tế)
1. `php -l` → `No syntax errors detected in Modules/Human/Entities/PrintTemplateVariable.php`
2. Picker QĐ chấm dứt HĐLĐ → `YYbareOKY` (đúng kỳ vọng: có NGAY_KY_CHU + NGAY_KY_SO, ẩn NGAY_KY gốc, có THOI_GIAN_BD_CHAM_DUT_HDLD_CHU).
3. Picker Biên bản → `YYnondateOK` (đúng kỳ vọng: có NGAY_HOP_CHU + NGAY_HOP_SO, biến thường SO_BIEN_BAN giữ nguyên).

## Concern
- Không có. Chỉ sửa đúng 1 file, không đổi logic build khác, không commit git.
- Lưu ý downstream (ngoài phạm vi Task 2): tên biến trong DB/template người dùng đã lưu vẫn dùng dạng gốc `{{X}}`; việc render 2 định dạng `_CHU`/`_SO` phụ thuộc helper của Task 1 khi thay thế giá trị — đảm bảo phần setValue/replace ở DecisionService (và các service HĐLĐ/biên bản/đào tạo) nhận diện được hậu tố `_CHU`/`_SO`. Đây là Task khác, không thuộc file này.
