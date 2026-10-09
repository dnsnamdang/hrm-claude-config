# Chặn nhập kết quả (WrImportResult) khi PCT chưa duyệt — Cách 1b (không backfill)

## Bug
Cho tạo phiếu nhập KQ dù PCT (phiếu công tác - HRM) đang tạo/chưa duyệt.

## Root cause
`has_assign_business` (HRM ghi sang ERP qua mysql2) trước đây nhị phân, HRM set =1 ngay lúc TẠO PCT
(không phải lúc duyệt). ERP canImportResult đọc như boolean → PCT đang tạo vẫn cho nhập KQ.

## Giải pháp 1b — GIỮ nghĩa giá trị 1 cho dữ liệu cũ (không cần backfill)
has_assign_business: 0 = chưa có PCT | **1 = PCT đã duyệt (giữ nghĩa cũ)** | **2 = PCT chưa duyệt (mới)**
- Dữ liệu cũ =1 → vẫn cho nhập KQ, KHÔNG bị chặn nhầm, KHÔNG cần chạy script prod.
- Từ deploy: HRM set 2 lúc tạo PCT, set 1 lúc duyệt → bug fixed cho luồng mới.

## Đánh đổi (đã chấp nhận)
PCT cũ đang-tạo hiện =1 → không phân biệt được với đã-duyệt → vẫn lọt (không sửa hồi tố nhóm cũ).
Bù lại: không chặn nhầm + không đụng data prod.

## ERP đã sửa (branch master, php -l sạch)
- [x] WrAssignTask: PCT_KHONG_CO=0, PCT_DA_DUYET=1, PCT_CHUA_DUYET=2.
- [x] canImportResult: has_assign_business == PCT_DA_DUYET(1).
- [x] canDelete: == PCT_KHONG_CO(0).
- [x] WrImportResultsController store()+storeApp(): gate BE chặn nếu != PCT_DA_DUYET(1).
- [ ] User test sau deploy HRM.

## HRM: xem HRM/.plans/pct-duyet-set-has-assign-business-2
## Branch: master
