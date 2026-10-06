# Dữ liệu đã tạo — HDSD Quy trình GP luồng sale tự làm (02/10/2026, DB local_hrm_erp)

- Dự án TKT id=151 `CTV_NV.UD.0101.2026.DA001` "Cung cấp và lắp đặt cầu nâng 2 trụ cho xưởng dịch vụ Ô tô Thành An" — Tự triển khai, Có làm GP, KD chính = DNS Admin (id 13), KH id 93 (Ô tô Thành An), liên hệ id 1518. Tạo qua API POST assign/prospective-projects (status=2).
- SQL bổ sung snapshot tên/mã/MST/địa chỉ KH (customer_* và customer_benefit_*) cho dự án 151 (API không tự điền).
- BOM tổng hợp id=25 `BOM-2026-00025` (trạng thái Hoàn thành, 3 dòng hàng chép từ BOM 22) cho giải pháp 956 — tạo qua API POST assign/bom-lists.
- Hồ sơ trình duyệt giải pháp id=13 `HS.TD.CTV_NV.UD.0101.2026.DA001_GP39.1` — tạo qua giao diện, bấm "Lưu & Duyệt" → tự duyệt (approved); GP 956 → Đã duyệt giải pháp, dự án 151 → Đã duyệt giải pháp, BOM 25 → Đã duyệt.
- (Để chụp ảnh cảnh báo "chưa có BOM", tạm đặt BOM 25 về trạng thái Đang tạo rồi trả lại Hoàn thành bằng SQL trước khi trình hồ sơ.)
- Báo giá id=90 `BG-2026-00081` (Đang tạo) — tạo qua giao diện bằng nút Tạo báo giá ở thẻ Hồ sơ của dự án 151 (từ BOM 25).
- Chốt giải pháp cho dự án 151 qua giao diện (chọn hồ sơ 13, ghi chú, đính kèm file Bien_ban_xac_nhan_giai_phap.pdf) → hồ sơ 13 = finalized, GP 956 = Chốt giải pháp (17); dự án 151 giữ Dự toán (6) (đã lên Dự toán khi tạo báo giá).
- Dự án TKT id=154 `CTV_NV.UD.0101.2026.DA002` 'Cung cấp bộ dụng cụ sửa chữa nhanh cho Thần Châu Garage' — Tự triển khai, KHÔNG làm GP (nhánh không làm GP), KH id 210; tạo qua API + SQL bổ sung tên/mã KH.
