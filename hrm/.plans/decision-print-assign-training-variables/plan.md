# Plan — Biến mẫu in + in N bản cho QĐ cử đi đào tạo

@manhcuong · Design: `.plans/decision-print-assign-training-variables/design.md` · Spec: `docs/superpowers/specs/2026-07-15-decision-print-assign-training-variables-design.md`

## Phase 1 — Hạ tầng ngày

### BE
- [x] `Helper.php`: thêm `parseVNDateTime($value)` — parse `d/m/Y H:i:s` / `d/m/Y H:i` / `d/m/Y` bằng `createFromFormat`, trả `null` nếu rỗng/rác, passthrough nếu đã là Carbon
- [x] Verify tinker: `21/12/2025 08:00`→`21/12/2025`; `05/12/2025 08:00`→`05/12/2025` (KHÔNG đảo thành 12/05); `null`/`'abc'`→`null`

## Phase 2 — Metadata biến

### BE
- [x] `PrintTemplateVariable.php` block `TYPE_ASSIGN_TRAINING` (681-687): thêm 14 biến chung (`MON_HOC`, `HINH_THUC_DT`, `DON_VI_DT`, `DIA_DIEM_DT`, `NOI_DUNG_DT`, `SO_THANG_CAM_KET_LV`, `THOI_GIAN_CU_DI_DT_TU`/`_DEN` is_date, 6 biến tiền)
- [x] Cùng block: thêm 21 biến theo học viên (`TEN_HOC_VIEN`, `PHONG_BAN_HV`, `SO_HDLD_HV`, `DIEN_THOAI`, quản lý trực tiếp x2, `BO_PHAN`, `CHUC_DANH`, `CHUC_VU`, `CAP_BAC`, `NGAY_SINH` is_date, `NGAY_CAP_CMTND` is_date, `GIOI_TINH`, `CMTND`, `NOI_CAP_CMTND`, `QUE_QUAN`, `DAN_TOC`, `QUOC_TICH`, `DIA_CHI_THUONG_TRU`, `NOI_CU_TRU`, `CHUYEN_NGANH`, `TRINH_DO_HOC_VAN`)
- [x] Verify tinker picker: 44 dòng, 4 is_date nở `_CHU`/`_SO` + ẩn gốc, `NGAY_KY_CHU`/`_SO` có sẵn từ biến chung

## Phase 3 — Value-fill + in N bản

### BE
- [x] `AssignTrainingController`: tách `fillCourseVariables(&$common, $at)` — 14 biến chung, tiền qua `formatCurrency`, `NOI_DUNG_DT` qua `nl2br`, 2 biến thời gian qua `parseVNDateTime` + `fillDateVariants(..., 'keep')`
- [x] `AssignTrainingController`: thêm `loadStudentEmployeeInfos($students)` — eager-load `employeeManager.info`, `employeeManagerWorkingPosition`, `workPosition.ranks`, `part`, `role`, `employee_educations`; `withoutGlobalScopes()` (CompanyActiveScope)
- [x] `AssignTrainingController`: thêm `fillStudentVariables(&$result, $student, $info)` — 4 biến snapshot + `SO_HDLD_HV` fallback live `DecisionLaborContract` status=2 + 17 biến live null-safe (`$info ? ... : ''`)
- [x] `AssignTrainingController::print()`: viết lại 2 tầng — `$common` fill 1 lần, lặp students `$result = $common` (copy) → `fillReport` mỗi HV → `implode('<div class="page-break active"></div>')`; 0 HV → in 1 bản biến rỗng
- [x] Verify `php -l` sạch 3 file BE

## Phase 4 — FE ngắt trang

### FE
- [x] `pages/decision/assign-training/_id/print.vue`: CSS `/deep/ .page-break.active` — `border-top: 2px dashed`, `margin: 24px 0`, `page-break-before: always`. KHÔNG sửa `print-content.js` (plugin dùng chung)

## Phase 5 — Verify

- [x] Tinker `print()` AT#3: ra 3 bản, đúng 2 dấu `page-break active`, tên HV khác nhau không nhiễm chéo
- [x] Tinker AT#3: `SO_HDLD_HV` fallback live ra `317/`, `318/`, `330/2025/HĐLĐ-TPE`; tiền `1,300,000` / `3,900,000`; `THOI_GIAN_CU_DI_DT_TU_SO` = `21/12/2025`
- [x] Tinker AT#1 (1 HV): ra 1 bản, 0 page-break
- [x] Khôi phục `print_template` gốc sau test
- [x] Playwright màn `/decision/assign-training/3/print`: hiện 3 bản + đường ngắt, 0 lỗi console

## Phase 6 — Đổi QUOC_TICH → DAN_TOC (phát sinh sau verify)

### BE
- [x] Xác minh HSNS không có trường quốc tịch NV: `national` nhãn form = "Dân tộc"; `nationality` chỉ ở `employee_relationships` (người thân); 93 cột `employee_infos` không có cột quốc tịch
- [x] `PrintTemplateVariable.php`: bỏ `QUOC_TICH`, thêm `DAN_TOC` + comment giải thích
- [x] `AssignTrainingController::fillStudentVariables`: `QUOC_TICH` → `DAN_TOC`
- [x] Verify: php -l sạch; picker có DAN_TOC + không còn QUOC_TICH; runtime AT#3 `DAN_TOC = Kinh`

## Phase 7 — Test end-to-end với mẫu in thật (user yêu cầu)

- [x] Soạn mẫu demo "1 bản = 1 người" dùng biến mới → `mau-in-goi-y.html` (giữ bố cục QĐ gốc: bảng tiêu đề, Điều 1/2/3, nơi nhận)
- [x] Áp mẫu demo tạm vào Decision AT#3 (backup trước) → in thật → chụp `ket-qua-in-thu.png`: 3 bản, mỗi bản 1 HV, mọi biến đổ đúng (SO_HDLD_HV 317//318//330/, tiền 1,300,000 / 3,900,000, MON_HOC, SO_THANG_CAM_KET_LV=36, NGAY_KY_CHU "ngày 20 tháng 12 năm 2025"), 0 lỗi console
- [x] Khôi phục mẫu gốc AT#3 (10101 ký tự, khớp bit-for-bit, không còn dấu vết demo)
- [x] Xác minh HV 1384 Trần Hạnh Minh in QL trực tiếp RỖNG là do `direct_manager_id = NULL` (vấn đề DATA, không phải code) — null-safe hoạt động đúng, không vỡ

## Phase 8 — Test CỬA SỔ IN THẬT bằng Playwright (user hỏi lại)

- [x] Nhận ra gap: Phase 5/7 mới test màn XEM TRƯỚC (DOM + CSS), CHƯA test cửa sổ in thật do `$printContent()` mở
- [x] Test cửa sổ in: `ctx.expect_page()` bắt popup → 2 thẻ `.page-break.active` có mặt, computed `page-break-before: always` / `break-before: page`
- [x] Xuất PDF thật (`emulate_media("print")` + `.pdf(format="A4")`) → 3 trang A4
- [x] ĐỐI CHỨNG LẦN 1 (mẫu gốc 10101 ký tự): xoá page-break vẫn 3 trang → **KHÔNG chứng minh được gì** (nội dung tự tràn 3 trang), khẳng định "3 trang = ngắt trang OK" là NGỤY BIỆN
- [x] ĐỐI CHỨNG LẦN 2 (mẫu cực ngắn `<p>BAN IN CUA: {{TEN_HOC_VIEN}}</p>`): CÓ page-break = **3 trang**, xoá page-break = **1 trang** → ngắt trang A4 giữa các học viên HOẠT ĐỘNG THẬT (chứng minh dứt khoát)
- [x] Khôi phục mẫu gốc AT#3 (10101 ký tự, không dấu vết, 3 học viên nguyên vẹn)

## Phase 9 — Thêm lại QUOC_TICH hardcode 'Việt Nam' (user chốt)

### BE
- [x] `PrintTemplateVariable.php`: thêm `QUOC_TICH` ('Quốc tịch (mặc định Việt Nam)') cạnh `DAN_TOC` + comment cảnh báo NV nước ngoài
- [x] `AssignTrainingController::fillStudentVariables`: `$result['QUOC_TICH'] = 'Việt Nam'` (hardcode, không đọc DB)
- [x] Verify: php -l sạch; picker 65 biến có cả DAN_TOC + QUOC_TICH, không key trùng; runtime AT#3 cả 3 bản `DAN_TOC = Kinh` + `QUOC_TICH = Việt Nam`; template gốc khôi phục

### Checkpoint — 2026-07-15
Vừa hoàn thành: Toàn bộ Phase 1-5. 4 file sửa (3 BE + 1 FE), verify pass hết.
Đang làm dở: (không)
Bước tiếp theo: User soạn lại mẫu in theo hướng "1 bản = 1 người" (dùng {{TEN_HOC_VIEN}}... thay danh sách gõ tay) + hard-refresh in thử browser. CHỜ user chốt vấn đề QUOC_TICH (cột `national` lưu DÂN TỘC "Kinh" x947/"Tày" x5/"Nùng" x3, employee_infos KHÔNG có cột quốc tịch).
Blocked: (không)
