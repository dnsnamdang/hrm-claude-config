# Design (tóm tắt) — Biến mẫu in + in N bản cho QĐ cử đi đào tạo

- **Người phụ trách**: @manhcuong
- **Ngày**: 2026-07-15
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-15-decision-print-assign-training-variables-design.md`
- **Màn**: https://dev-hrm.eteksofts.com/decision/assign-training

## Mục tiêu

QĐ cử đi đào tạo là loại **1 QĐ — nhiều học viên**. Hiện in ra đúng 1 bản với 5 biến. Cần:

1. **In N bản** — mỗi học viên 1 bản, nội dung giống nhau, ngắt trang A4 giữa các bản.
2. **+36 biến mẫu in** cho nhóm `Decision::TYPE_ASSIGN_TRAINING`.

## Quyết định lớn

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Nơi lặp N bản | **BE ghép sẵn** — fill template N lần, nối bằng `<div class="page-break active"></div>`. Plugin in FE (`print-content.js:50-53`) đã hỗ trợ sẵn class này. Response giữ shape `{ template }`. |
| 2 | Nguồn dữ liệu HV | **Snapshot khi có, live khi không** — `name`/`department`/`telephone` snapshot; HSNS còn lại live từ `EmployeeInfo`. |
| 3 | Format tiền | `formatCurrency()` → `5,000,000`. Không "đồng", không bằng chữ. |
| 4 | Thời gian ĐT | `_CHU` + `_SO`, bỏ giờ. |
| 5 | `DIEN_THOAI` | Snapshot `students.telephone` — đã verify = `employee_infos.telephone` (ĐT cty). |
| 6 | `CAP_BAC` | `workingPosition->ranks()->first()->name` (giống `StudentResource`). |
| 7 | `NOI_CAP_CMTD` | Bỏ (lỗi gõ). Chỉ `NOI_CAP_CMTND`. |
| 8 | `SO_HDLD_HV` | Snapshot **?: fallback live** — snapshot NULL 4/4 trên data thật. |
| 9 | `QUOC_TICH` / `DAN_TOC` | **Cả 2**: `DAN_TOC` = `national`; `QUOC_TICH` hardcode `'Việt Nam'` (HSNS không lưu quốc tịch — xem phát hiện 3). |

## Phát hiện quan trọng

**1. `NGAY_KY` / `NGAY_HIEU_LUC` đã có sẵn 2 định dạng → NGOÀI SCOPE.**
Nằm trong `DECISION_COMMON_VARIABLES` (`PrintTemplateVariable.php:321-322`, `is_date => true`) + `setValuePrintDecision` đã gọi `fillDateVariants` (dòng 476-477). Feature `decision-date-format-variants` đã làm. Chỉ verify.

**2. Bẫy `from_time`/`to_time` — KHÔNG phải cột date.**
Migration `2024_12_26_095658` đổi date→**string** `'d/m/Y H:i'`. `fillDateVariants` dùng `Carbon::parse` (hiểu `/` kiểu Mỹ):

| Input | Kết quả | Hậu quả |
|---|---|---|
| `21/12/2025 08:00` | `InvalidFormatException` | print() → HTTP 400, **màn in vỡ** |
| `05/12/2025 08:00` | `12/05/2025` | **âm thầm đảo ngày↔tháng** |

→ Bắt buộc thêm `Helper::parseVNDateTime()` parse tường minh bằng `createFromFormat`.

**3. HSNS KHÔNG có trường quốc tịch của nhân viên.**
`employee_infos.national` được form gắn nhãn **"Dân tộc"** (`EmployeeInfoForm.vue:190-193`; Kinh ×947, Tày ×5, Nùng ×3). Cột `nationality` chỉ có ở `employee_relationships` = quốc tịch **người thân**. → User chốt: `DAN_TOC` = `national` (đúng nghĩa) + `QUOC_TICH` **hardcode 'Việt Nam'** (không nguồn dữ liệu; sai nếu có NV nước ngoài → khi đó phải thêm cột vào HSNS). Nợ ngoài scope: 4 loại QĐ khác vẫn map `QUOC_TICH` = `national` → in 'Kinh'.

## Phạm vi

**4 file, không migration / permission / git.**

| File | Việc |
|---|---|
| `hrm-api/Modules/Human/Helper/Helper.php` | +`parseVNDateTime()` (hàm mới) |
| `hrm-api/Modules/Human/Entities/PrintTemplateVariable.php` | +35 metadata vào block `TYPE_ASSIGN_TRAINING` (681-687) |
| `hrm-api/.../V1/AssignTrainingController.php` | `print()` 2 tầng + 3 helper method |
| `hrm-client/pages/decision/assign-training/_id/print.vue` | CSS `.page-break.active` |

## Biến bổ sung (36)

- **Chung — 14** (bảng `assign_trainings`): `MON_HOC`, `HINH_THUC_DT`, `DON_VI_DT`, `DIA_DIEM_DT`, `NOI_DUNG_DT`, `SO_THANG_CAM_KET_LV`, `THOI_GIAN_CU_DI_DT_TU`/`_DEN` (is_date), 6 biến tiền (`KINH_PHI_DT_1_NGUOI`, `TONG_KINH_PHI_DT`, `CTY_HO_TRO_1_NGUOI`, `TONG_CTY_HO_TRO`, `NV_CHI_TRA_1_NGUOI`, `TONG_NV_CHI_TRA`).
- **Theo HV — 22**: `TEN_HOC_VIEN`, `PHONG_BAN_HV`, `SO_HDLD_HV`, `DIEN_THOAI`, `NGUOI_QUAN_LY_TRUC_TIEP` + `CHUC_VU_...`, `BO_PHAN`, `CHUC_DANH`, `CHUC_VU`, `CAP_BAC`, `NGAY_SINH` (is_date), `NGAY_CAP_CMTND` (is_date), `GIOI_TINH`, `CMTND`, `NOI_CAP_CMTND`, `QUE_QUAN`, `DAN_TOC`, `QUOC_TICH`, `DIA_CHI_THUONG_TRU`, `NOI_CU_TRU`, `CHUYEN_NGANH`, `TRINH_DO_HOC_VAN`.

4 biến `is_date` → picker nở `_CHU`/`_SO` → **44 dòng** nhóm riêng + biến chung QĐ.

## Downstream

- Mẫu in đã lưu **không vỡ** (5 biến cũ giữ nguyên), nhưng **QĐ nhiều HV nay in N bản** — mẫu cũ nếu tự liệt kê danh sách HV trong 1 bản sẽ lặp N lần → cần soạn lại mẫu theo hướng "1 bản = 1 người".

## Data test

`AssignTraining#3` (3 HV: 1352, 1353, 1384 — `009/2026/QĐĐT-TPE`, template 10101 ký tự), `AssignTraining#1` (1 HV: 637) để test N=1.
