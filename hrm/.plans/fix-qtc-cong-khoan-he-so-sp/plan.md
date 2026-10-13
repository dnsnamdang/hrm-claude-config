# Fix: QTC không tính được "công khoán đề xuất theo hệ số SP" khi total coefficient = 0

## Bug (user báo 3 hợp đồng)
Bảng "II. Quyết toán theo phiếu giao việc" — cột "Công khoán đề xuất theo hệ số SP" = 0, dù điền tay công khoán đề xuất.
- HĐ_TPE_HN_KD2_26_0037_testQTC2
- HĐ_TPE_HN_KD2_26_0031_testycldbg2 (công khoán duyệt KQ = 0)
- HĐ_TPE_HN_KD2_26_0013_checkcolapdat2 (tổng công khoán ĐM = 0)

## Nguyên nhân gốc (chung cả 3)
`hrm-client/pages/assign/settlement_contract/components/SettlementCalcMixin.js` — `initSettlementDefaults`:
`total = Σ(work_coefficient × coefficient_reality)`; `ratio = total>0 ? (wc×cr)/total : 0`.
Khi `total = 0` (nhân viên chưa có công thực tế coefficient_reality=0) → ratio = 0 cho tất cả → mọi phân bổ (công khoán theo hệ số SP, công HC...) = 0.

## Quyết định (user chốt: Cách A)
Khi `total = 0`: chia theo `work_coefficient`; nếu `Σ work_coefficient` cũng = 0 thì chia đều 1/n. Bù phần lẻ vào người cuối để tổng tỉ lệ = 1 (qua validate 100%). Nhánh thường (total>0) giữ nguyên.

## Tasks
- [x] Trace gốc: total=0 → ratio=0 (SettlementCalcMixin.js initSettlementDefaults)
- [x] Sửa `initSettlementDefaults`: fallback work_coefficient → chia đều, bù phần lẻ người cuối
- [ ] User verify 3 HĐ: công khoán theo hệ số SP hiện số, tổng tỉ lệ = 100%; HĐ có công thực tế không đổi

## Ghi chú
- Chỉ đụng `initSettlementDefaults` (khởi tạo tỉ lệ). `calcProducts`/`calcWorkRequest` dùng lại `rate_request_by_pro` nên tự hưởng fallback.
- Branch `tpe` (hrm-client). Chưa commit.
