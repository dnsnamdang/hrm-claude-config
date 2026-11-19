# Phase 33 — Cảnh báo HĐ sắp hết hiệu lực (HĐ bán HRM)

Nguồn: **yêu cầu khách hàng** 10/11/2026 mục 11 ("Bổ sung cấu hình cảnh báo HĐ sắp hết hiệu lực >> Cảnh báo cho NVKD nắm được").
Đợt 3 phần (d) — làm trước (b)+(c) kế hoạch / cảnh báo giao hàng và (a) tiến độ thanh toán (user chốt thứ tự 11/11).

## 1. Đã chốt (11/11)

| # | Câu | Chốt |
|---|---|---|
| D1 | Ngày hết hiệu lực | `execution_end_date` (Ngày kết thúc thực hiện = ngày mốc + số ngày thực hiện, đúng định nghĩa khách) |
| D2 | Nhắc khi nào | 1 lần khi **còn đúng N ngày** + 1 lần **đúng ngày hết hiệu lực**. Không nhắc lặp hằng ngày |
| D3 | Ai nhận | **Người lập HĐ** |
| D4 | Cấu hình N | **Theo công ty**, ô bắt buộc, số nguyên ≥ 1, **mặc định 30** (không có quy ước "0 = không nhắc") |

## 2. Hiện có (Phase 24, không đổi)

Lệnh lịch `assign:activate-signed-contracts` (00:20) ⇒ `ContractService::expireIfOverdue`: Có hiệu lực (6) / Đang thực hiện (19) mà
`execution_end_date < hôm nay` ⇒ **Hết hiệu lực (20)** + báo người lập `[HDB] Cập nhật: <mã>. Hết hiệu lực — quá thời hạn thực hiện (…)`.
⇒ Phase 33 chỉ thêm phần **nhắc trước**; dòng thời gian của 1 HĐ: còn N ngày (nhắc) → ngày hết hạn (nhắc) → hôm sau tự Hết hiệu lực (báo như cũ).

## 3. Thiết kế

- **Cấu hình:** Khai Quy chế – Cấu hình → Theo công ty → tab **Báo giá – Hợp đồng**, ô "Số ngày cảnh báo HĐ sắp hết hiệu lực" (ngày).
  `RegulationTabRegistry` `baogia` thêm field `store=company`, `integer`, bắt buộc, `min:1`; đi chung pipeline hẹn ngày + lịch sử của tab.
  **Migration** `companies.contract_expiry_warning_days` smallint unsigned NOT NULL default 30 (bảng dùng chung ERP; ERP không đọc).
  FE `data.js` thêm ô vào nhóm Hợp đồng của tab (nhãn khớp 1-1 registry).
- **Lệnh lịch mới** `assign:warn-expiring-contracts`, **08:00** hằng ngày (giờ làm việc, không bắn push nửa đêm), `withoutOverlapping`.
  `ContractService::warnExpiringContracts(?Carbon $today)`: theo từng công ty lấy N; HĐ trạng thái 6 / 19, có `execution_end_date`,
  `execution_end_date = hôm nay + N` ⇒ nhắc "còn N ngày"; `= hôm nay` ⇒ nhắc "hôm nay". HĐ không có ngày kết thúc (thiếu mốc / số ngày) ⇒ bỏ qua.
  Lần chạy trùng trong ngày: dựa `withoutOverlapping` + so đúng ngày (không thêm bảng nhật ký). Ngày lệnh không chạy ⇒ mất lần nhắc đó (chấp nhận).
- **Thông báo** (skill notification-convention, khuôn `ContractNotificationService::send`, prefix `HDB`):
  `[HDB] Sắp đến hạn: <b>HĐ_…</b>. Hết hiệu lực 15/12/2026 (còn 30 ngày)` · ngày hết hạn: `… Hết hiệu lực hôm nay (15/12/2026)`.
  Người nhận: `created_by`. Deep-link `/assign/contracts/{id}`. Type `contract_expiring`.

## 4. Kiểm

- PHPUnit: đúng N ngày ⇒ nhắc; N±1 ⇒ không; đúng ngày ⇒ nhắc "hôm nay"; trạng thái khác 6/19 ⇒ không; thiếu ngày kết thúc ⇒ không;
  2 công ty N khác nhau; registry validate bắt buộc / min:1; migration default 30. Stub gửi thông báo (đếm, không bắn FCM thật — memory rehearsal-gui-push-that).
- Playwright: tab Báo giá – Hợp đồng hiện ô mới, bỏ trống / 0 ⇒ lỗi dưới ô (chặn ghi bằng route), số đọc đúng từ API.

## 5. Nhánh

Nhánh riêng tách origin/gop_db theo mặc định — đề xuất **làm tiếp trên `gop_db-hd-dieu-kien-duyet`** (cùng chuỗi yêu cầu KH 10/11, đã merge tester) để
merge sang `gop_db-xuat-hang-cha-con` cho tester như Phase 31–32.

## 6. Ghi chú cho các phần sau của đợt 3 (khảo sát 11/11)

`companies` (ERP) đã có 2 cột cảnh báo — KHÔNG phải cảnh báo hết hiệu lực nên Phase 33 vẫn thêm cột mới:
- `warning_due_date` "Thời gian hiển thị cảnh báo thu nợ đến hạn" (ERP `WarningDebtDueDateService`, đã có ở tab Công nợ HRM) ⇒ xem lại khi làm (a) cảnh báo thu tiền.
- `warning_product_delivery` "Số ngày vượt quá thời gian cần giao" (ERP `WarningProductDeliveryService`, báo cáo đơn hàng) ⇒ xem lại khi làm (c) cảnh báo giao hàng.
