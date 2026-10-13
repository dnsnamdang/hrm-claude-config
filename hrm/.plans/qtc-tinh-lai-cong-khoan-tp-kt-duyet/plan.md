# QTC: tính lại công khoán theo hệ số SP theo công khoán TP/KT duyệt

## Bug
Khi TP (và KT) duyệt công khoán khác công khoán đề xuất → "công khoán theo hệ số SP" (bảng II theo phiếu + bảng III theo người) không tính lại, vẫn theo đề xuất.

## Nguyên nhân
`SettlementCalcMixin.js`:
- `calcProducts` chỉ tính `assign.work_request_by_pro` (= Σ công khoán ĐỀ XUẤT × hệ số SP). Không tính bản TP/KT duyệt.
- `calcWorkRequest` dòng 159/164: `work_tp_approve_by_pro` & `work_kt_approve_by_pro` đều nhân `assign.work_request_by_pro` (đề xuất) → không đổi theo duyệt.

## Fix (cả TP và KT)
- [x] `calcProducts`: thêm `work_tp_approve_by_pro`/`work_kt_approve_by_pro` cấp product + gom lên cấp phiếu `assign.work_tp_approve_by_pro`, `assign.work_kt_approve_by_pro`
- [x] `calcWorkRequest`: dùng `assign.work_tp_approve_by_pro` / `assign.work_kt_approve_by_pro` (thay `assign.work_request_by_pro`)
- [ ] User verify: đổi công khoán TP duyệt → công khoán theo hệ số SP (bảng III) tính lại theo TP duyệt; tương tự KT

## Ghi chú
FE-only, branch `tpe` (hrm-client). Chưa commit tới khi user duyệt.
