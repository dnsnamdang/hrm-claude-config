# Fix: logic lấy Doanh thu (phiếu hạch toán bổ sung - Phối hợp kinh doanh, type=7)

## Yêu cầu (spec ảnh)
Doanh thu = **Tổng PS CÓ TK 1362 − Tổng PS NỢ TK 1362**, gắn công ty ("Gửi tới công ty"),
**mã đối ứng với TK 511, 5212, 5213** trên hạch toán của quyết toán HĐ.

## Hiện trạng (cũ)
`SettlemenHandleAdditionalAccountingService::handleAccounting`:
- Chỉ lấy 1362 **một chiều** (Có, type=2), đối ứng **5111** (một mã lá), cộng `money_value_exchange`.
- Không trừ chiều Nợ; không gồm 511 (nhóm)/5212/5213.

## Ngữ nghĩa xác minh (prod)
- `type=1` = Nợ (debt), `type=2` = Có (has) — từ `AccountDetail`.
- Chart of accounts: `511` = TK cha (con 5111,5112,5113,5114,5117,5118 = doanh thu); `5212`/`5213` = con của 521 (hàng bán trả lại / giảm giá).

## Fix
- [x] `matchRevenueRef`: entry 1362 có ref `identify_number` bắt đầu bằng **`511`** / **`5212`** / **`5213`** → khớp **CẢ NHÓM CHA-CON** mọi cấp (chuẩn phân cấp TT200), không cần query `Account`.
- [x] Doanh thu NET theo phòng = Σ(1362 Có) − Σ(1362 Nợ) (lọc theo ref) — `$revenueByDept[$dept]`.
- [x] Tổng công ty = Σ `$revenueByDept` các phòng thuộc công ty `$ck`.
- [x] Phân bổ NV (work 15 "Doanh thu hàng hóa") dùng `$deptRevenue = $revenueByDept[$dk]` (net) thay vì 1 entry Có.
- [x] `php -l` sạch.
- [ ] User đối chiếu số doanh thu trên phiếu type=7 sinh mới (vd tương tự 1732).

## Giả định cần xác nhận
- "511" hiểu là **cả nhóm 511 (5111..5118)** (vì entries post ở mã lá, 511 là cha). 5212/5213 lấy đúng 2 mã lá. Nếu ý là chỉ đúng `5111` như cũ thì báo mình chỉnh lại.

## File
- `app/Services/Sale/Firm/Settlement/SettlemenHandleAdditionalAccountingService.php`

## Lưu ý
- Chỉ ảnh hưởng phiếu type=7 **sinh MỚI** (khi kế toán duyệt quyết toán HĐ). Phiếu cũ (như 1732) không đổi.
- Giá vốn (dòng gạch trong spec) chưa đụng — user chỉ yêu cầu sửa doanh thu.
