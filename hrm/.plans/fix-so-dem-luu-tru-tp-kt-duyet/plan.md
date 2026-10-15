# Plan — Fix số đêm lưu trú TP/KT duyệt bị reset về 0

Nhánh: `tpe` (client). Fix nhỏ, chỉ FE. Màn: Đề nghị thanh toán (DNTT) — tab Lưu trú.

## Bug
Khi TP/KT duyệt sửa số công (ĐM công) khác số ban đầu → hàm `calcStayTab()` trong
`BusinessTravelExpensesTab.vue` chạy và **reset cứng `number_night_tp_approve` / `number_night_kt_approve`
của từng dòng stay_reals về 0** (dòng 363, 365). Trong khi dòng "Tổng cộng" set theo `số ngày − 1`
(dòng 359–360) → per-row hiển thị 0, lệch với tổng.

## Yêu cầu (đã chốt với user)
- Sửa hiển thị số đêm lưu trú TP/KT duyệt của từng dòng **luôn theo số đề xuất** (`number_night_request`),
  KHÔNG reset về 0. (User chọn: "Luôn bằng số đề xuất".)
- Validate số đêm lưu trú giữ nguyên (`StayTab.validateNumber` đã chặn tổng số đêm > số ngày − 1),
  không cần đổi — vẫn chặn khi vượt trần và surface qua `getError()`.

## Tasks
- [x] Điều tra: root cause = calcStayTab reset per-row night về 0
- [x] Chốt behavior với user: luôn mirror số đề xuất
- [x] FE `BusinessTravelExpensesTab.vue::calcStayTab()`: đổi `= 0` → `= Number(val.number_night_request) || 0` cho TP & KT
- [ ] Test tay: TP duyệt sửa số công → ô số đêm TP duyệt hiện theo đề xuất; KT tương tự; đề xuất (creator) không đổi behavior
