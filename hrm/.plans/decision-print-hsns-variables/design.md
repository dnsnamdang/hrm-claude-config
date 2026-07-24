# decision-print-hsns-variables — Tóm tắt

**Mục tiêu:** Bổ sung biến mẫu in còn thiếu cho nhiều loại QĐ, phần lớn lấy từ HSNS (EmployeeInfo), kèm 3 biến ngày mới 2 định dạng (`NGAY_SINH`, `NGAY_CAP_CMTND`, `THOI_GIAN_HDLD_HIEN_TAI`). Dùng lại hạ tầng feature `decision-date-format-variants` (is_date + fillDateVariants + expandDateVariables).

**Scope theo nhóm:**
- **A** (Bổ nhiệm/Điều chuyển/Điều chỉnh lương/Nghỉ hưu/Kỷ luật): +13 biến HSNS (NGAY_SINH, NGAY_CAP_CMTND [ngày], GIOI_TINH, CMTND, NOI_CAP_CMTND, DIA_CHI_THUONG_TRU, NOI_CU_TRU, QUE_QUAN, QUOC_TICH, CHUYEN_NGANH, TRINH_DO_HOC_VAN, DIEN_THOAI, MAIL).
- **B** (Bổ nhiệm/Điều chuyển/Điều chỉnh lương): +CAP_BAC_TRUOC_TD/SAU_TD (old_rank_name/new_rank_name).
- **C** (Chấm dứt + Tạm hoãn HĐLĐ): +9 biến thiếu (GIOI_TINH, NOI_CAP_CMTND, NGAY_CAP_CMTND[ngày], DIA_CHI_THUONG_TRU, CHUYEN_NGANH, QUE_QUAN, QUOC_TICH, DIEN_THOAI, THOI_GIAN_HDLD_HIEN_TAI[ngày]). Suspend 2 khối.
- **D** (QĐ ký HĐLĐ + Phụ lục HĐLĐ): +THOI_GIAN_HDLD_HIEN_TAI[ngày].

**Chốt:** loại gộp TERMINATION_AND_SUSPEND → BỎ QUA (không có print()). THOI_GIAN_HDLD_HIEN_TAI = start_date HĐLĐ liên kết (labor_contract_id → DecisionLaborContract). Biến mới lấy HSNS live. Không migration/permission/git.

**Field dễ sai:** QUE_QUAN=home_town, QUOC_TICH=national, NOI_CU_TRU=full_address (tạm trú), DIA_CHI_THUONG_TRU=full_address_residence (thường trú), CHUYEN_NGANH=employee_educations->last()->specialty, TRINH_DO_HOC_VAN=listAcademicLevels[academic_level], DIEN_THOAI=personal_telephone?:telephone, MAIL=email?:personal_email, CAP_BAC=old_rank_name/new_rank_name.

**Spec chi tiết:** `docs/superpowers/specs/2026-07-14-decision-print-hsns-variables-design.md`
