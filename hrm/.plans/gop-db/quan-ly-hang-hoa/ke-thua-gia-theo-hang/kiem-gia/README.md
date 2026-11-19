# Kiểm giá cũ / giá mới khi đổi cài đặt Giá bán theo hãng sx

> Soạn 30/10/2026 · @namdangit. KHÔNG phải source code, không ghi DB: 1 câu SELECT chạy trên prod + 1 script Python chạy ở máy dev.
> Cần đợt 2 đã deploy (SQL đọc bảng `inherited_price_factors`).

| File | Việc |
|---|---|
| `chup-gia.sql` | Chụp bộ giá (chỉ đọc) của công ty kế thừa: mọi mã **Đang KD** do công ty khác tạo × ĐVT × loại giá — 6 cột chép (giá, hệ số giá, ĐMGG, 3 cờ sửa tay) + dòng nguồn + trạng thái kế thừa + hệ số k lúc chụp |
| `so-gia.py` | Ghép bản TRƯỚC + bản SAU ⇒ Excel: tab **Tổng hợp** + **mỗi công ty 1 tab** (giá cũ / mới / chênh / giá nguồn / kỳ vọng / Kết quả) |

## 1. Chép SQL lên VPS (1 lần)
```bash
scp -P 2225 HRM/.plans/gop-db/quan-ly-hang-hoa/ke-thua-gia-theo-hang/kiem-gia/chup-gia.sql erp_tpe@124.158.4.24:~/
```

## 2. Chụp TRƯỚC — ngay trước khi bấm Lưu cài đặt
Đổi `TPHP` thành các công ty sắp đổi cài đặt (ngăn bằng phẩy, không dấu cách, vd `TPHP,TPSG,TPV`):
```bash
sed "s/^SET @cty = .*/SET @cty = 'TPHP';/" ~/chup-gia.sql \
  | mysql -h 192.168.122.103 -u hrm_tpe -p -B hrm_erp_gop | gzip > ~/gia-truoc-$(date +%Y%m%d-%H%M).tsv.gz
```
- `-B` bắt buộc (tách tab + có dòng tiêu đề), KHÔNG thêm `-N`.
- Đo local: 2 công ty × ~30.000 mã = 362.000 dòng, ~18 s, 78 MB (gzip ~8 MB).

## 3. Lưu cài đặt trên màn → chờ dải "Đang áp" tắt (chuông `[GIA] Cập nhật`)

## 4. Chụp SAU — cùng lệnh, cùng danh sách công ty
```bash
sed "s/^SET @cty = .*/SET @cty = 'TPHP';/" ~/chup-gia.sql \
  | mysql -h 192.168.122.103 -u hrm_tpe -p -B hrm_erp_gop | gzip > ~/gia-sau-$(date +%Y%m%d-%H%M).tsv.gz
```
Giữ khoảng TRƯỚC → SAU càng ngắn càng tốt: ai sửa giá ở công ty nguồn / công ty đích trong lúc đó cũng hiện thành "đổi".

## 5. Kéo về máy dev, ra Excel
```bash
scp -P 2225 'erp_tpe@124.158.4.24:~/gia-*.tsv.gz' .
python3 HRM/.plans/gop-db/quan-ly-hang-hoa/ke-thua-gia-theo-hang/kiem-gia/so-gia.py \
  gia-truoc-<giờ>.tsv.gz gia-sau-<giờ>.tsv.gz -o so-gia-TPHP.xlsx
#   in: "TPHP: N dòng · đổi giá X dòng / Y mã · lệch Z · ghi W dòng" — exit 1 khi có dòng lệch
```
- Cần `openpyxl` (`pip3 install openpyxl`).
- Mặc định tab công ty chỉ ghi dòng **đáng xem**: giá trị đổi, lệch kỳ vọng, đổi Kế thừa ⇄ Tự xây dựng giá hoặc đổi hệ số k.
  `--tat-ca` ghi mọi dòng (đo local 362.000 dòng ⇒ ~3 phút, file 34 MB — Excel mở chậm; chỉ dùng khi cần rà toàn bộ).

## Đọc file
- **Tổng hợp:** cách cài trước/sau, số dòng giá, dòng chuyển sang kế thừa / tự tính, dòng + mã đổi giá, **dòng LỆCH** (ô đỏ).
- **Tab công ty** — cột Kết quả:
  - `Khớp — đổi giá…` / `Khớp — không đổi`: hàng kế thừa, giá mới = kỳ vọng.
  - `LỆCH kỳ vọng: giá, hệ số giá…` (nền đỏ) hoặc `LỆCH: thiếu dòng giá ở công ty nguồn` ⇒ gửi file cho dev, **không sửa tay giá**.
  - `Tự xây dựng giá — đổi … (không do cài đặt?)`: hàng không kế thừa mà giá đổi — thường do có người sửa giá trong lúc chụp.
  - `Chỉ có ở bản TRƯỚC/SAU`: hàng vào/thôi Đang KD giữa 2 lần chụp.
- **Kỳ vọng** = giá công ty nguồn ở bản SAU × hệ số k (mã › hãng › 1), làm tròn 1,000 đ, không thấp hơn giá nguồn, giá ≤ 1 đ giữ
  nguyên; hệ số giá × k (2 số lẻ, trần 999.99); ĐMGG + cờ sửa tay chép nguyên — cùng luật `InheritedPriceSync::scaledPriceSql` /
  `scaledCoefficientSql`. Đổi luật ở code thì sửa cả `chup-gia.sql` (luật kế thừa) và `so-gia.py` (`expected()`).
- Bổ sung, không thay: `php artisan product-price:compare-inherited` vẫn là phép so chính (có cả giá hiệu lực chờ áp — file Excel
  này KHÔNG so giá hiệu lực).

## Đã thử (30/10, DB local `hrm_erp_21_10_prod`)
- TRƯỚC = SAU ⇒ 0 đổi, 0 lệch, exit 0.
- SAU giả lập: 1 hãng TPHP chuyển kế thừa × 1.2 (6 dòng), 1 dòng cố tình +5 đ ⇒ "đổi giá 6 dòng / 1 mã · lệch 1", dòng lệch nền đỏ
  "LỆCH kỳ vọng: giá" (26,648,005 vs kỳ vọng 26,648,000 = 22,207,000 × 1.2 làm tròn), 5 dòng còn lại "Khớp — đổi giá", exit 1.
