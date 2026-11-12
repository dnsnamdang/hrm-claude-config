# Đối số ERP ↔ HRM — Báo cáo theo dõi thực hiện hợp đồng

Ngày: 10/11/2026. Nhánh HRM: `feat/monitor-contract-implement` (worktree `hrm-api-mci`). DB: `erp_hrm_check` (local, chung cho ERP và HRM; `ERP/TanPhatDev/.env` trỏ `127.0.0.1/erp_hrm_check` đã kiểm trước khi chạy).

## 1. Cách đối số

- **ERP**: `App\Services\Reports\MonitorContractImplementService::getData()` với quyền Tổng công ty (`is_all_company = true`), đăng nhập NV id 13, chỉ truyền `date_from`/`date_to`.
- **HRM**: `MonitorContractReportService::rows()` với phạm vi `ALL`, cùng kỳ (`start_date`/`end_date`), lấy nguồn `firm` + `wr`.
- Khoá so: (loại HĐ, id HĐ gốc). So 9 cột số (Giá trị HĐ, DS theo HĐ, DS tiêu chuẩn, Thực thu, Tổng DSTC tiêu chuẩn, Tổng DSTC thực xuất, Phải thu, Đã thu, Còn nợ), sai số cho phép 0,5 đ. So thêm mã HĐ, khách hàng, công ty, phòng, người lập, tỉnh, hãng (hãng ERP phải nằm trong chuỗi hãng HRM).
- **Xếp lý do tự động, không đoán**: lấy chính subquery dòng chi tiết của ERP (`firm_final` / `final`, mỗi dòng = HĐ cha hoặc 1 PLBS), rồi:
  1. Tái lập số ERP từ các dòng đó (SUM bỏ dòng có dự phòng/định mức NULL, × số hãng xe của KH) → khớp 100% số ERP ở cả 3 kỳ (xác nhận đã hiểu đúng cách ERP ra số).
  2. Dựng "ERP đã sửa" theo design §2.3/§5 (1 dòng/HĐ con, không nhân hãng xe, dự phòng NULL → 0, sổ cái SUM cha + PLBS). Mỗi ô lệch chỉ được coi là "giải thích được" nếu số HRM **bằng đúng** số "ERP đã sửa".
- Script tạm (không commit): scratchpad `mci-parity/` (`erp_dump.php`, `hrm_dump.php`, `erp_raw.php`, `compare.py`, `verify.py`).

## 2. Kết quả

| Kỳ | Nguồn | Số HĐ ERP | Số HĐ HRM | Khớp cả 9 cột | Lệch (đã giải thích) | Lệch không giải thích |
|---|---|---|---|---|---|---|
| Tháng 07/2026 | firm | 1.796 | 1.796 | 1.774 | 22 | 0 |
| Tháng 07/2026 | wr | 314 | 314 | 270 | 44 | 0 |
| Quý II/2026 | firm | 6.229 | 6.229 | 6.127 | 102 | 0 |
| Quý II/2026 | wr | 798 | 798 | 750 | 48 | 0 |
| Tháng 03/2026 | firm | 2.515 | 2.515 | 2.474 | 41 | 0 |
| Tháng 03/2026 | wr | 295 | 295 | 249 | 46 | 0 |

- Tập HĐ lên báo cáo trùng khớp 100% ở cả 3 kỳ (không HĐ nào chỉ có ở một bên).
- Mã HĐ, khách hàng, công ty, phòng, người lập, tỉnh, hãng: **không lệch** HĐ nào.
- Nguồn HĐ HRM (`hrm`): 0 HĐ trong 3 kỳ (dữ liệu local chưa có bút toán 1311 của HĐ HRM trong kỳ), nên chỉ được kiểm bằng test feature.
- Kỳ chọn: 07/2026 là tháng gần nhất có sổ cái (08–09/2026 chỉ có 1 dòng/tháng); Quý II/2026; 03/2026 có 148 HĐ cha có PLBS và có wr 3948 (2 dòng HTHT).

TỔNG CỘNG (đ) — chênh lệch đều do các lý do ở mục 3:

| Cột | 07/2026 ERP | 07/2026 HRM | Quý II ERP | Quý II HRM | 03/2026 ERP | 03/2026 HRM |
|---|---|---|---|---|---|---|
| Giá trị HĐ | 192.630.489.293 | 190.139.010.331 | 1.940.401.270.423 | 1.927.689.841.616 | 1.246.328.132.579 | 1.238.331.278.160 |
| DS theo HĐ | 44.995.857.743 | 45.064.263.443 | 354.401.877.637 | 354.401.877.637 | 127.206.051.031 | 127.249.128.224 |
| DS tiêu chuẩn | 48.308.411.030 | 46.824.407.922 | 358.816.166.251 | 356.336.492.313 | 123.685.012.575 | 122.363.387.815 |
| Thực thu | 33.285.749.365 | 33.420.007.625 | 455.597.294.786 | 455.597.294.786 | 64.035.529.079 | 64.143.620.652 |
| Tổng DSTC tiêu chuẩn | 196.739.866.604 | 194.411.045.033 | 1.920.423.094.135 | 1.908.490.736.220 | 1.225.640.445.108 | 1.217.732.817.161 |
| Tổng DSTC thực xuất | 140.365.075.908 | 138.073.940.823 | 1.593.440.429.537 | 1.582.355.708.837 | 1.184.401.354.830 | 1.176.529.432.281 |
| Phải thu | 147.438.511.550 | 147.736.373.467 | 1.642.628.246.181 | 1.642.629.315.381 | 1.213.723.528.910 | 1.214.088.410.480 |
| Đã thu | 105.678.138.549 | 105.901.468.351 | 1.247.695.334.798 | 1.247.696.403.998 | 507.072.298.455 | 507.412.360.930 |
| Còn nợ | 41.760.373.001 | 41.834.905.116 | 394.932.911.383 | 394.932.911.383 | 706.651.230.455 | 706.676.049.550 |

## 3. Lý do lệch (chỉ 4 loại, đều nằm trong design §2.3/§5)

| Nhãn | Ý nghĩa | Cột bị ảnh hưởng | Chiều lệch |
|---|---|---|---|
| **Nhiều hãng xe** | KH có N hãng xe (`customer_has_vehicle_manufacts`): ERP join 1-n trước `SUM` nên nhân ×N. HRM không nhân, cột Hãng nối đủ các hãng (§2.3). | Giá trị HĐ, DS tiêu chuẩn, Tổng DSTC 2 cột | ERP = HRM × N (N = 2, 3, 4) |
| **Sổ cái PLBS** | HĐ cha có PLBS: ERP `GROUP BY` HĐ cha nhưng không `SUM` các cột sổ cái → lấy 1 dòng bất kỳ (hay rơi vào dòng PLBS không có bút toán → trống ô; hoặc dòng cha khi PLBS cũng có bút toán riêng, vd wr 456). HRM SUM cha + PLBS (§2.3). | DS theo HĐ, Thực thu, Phải thu, Đã thu, Còn nợ | ERP trống / nhỏ hơn |
| **Dự phòng NULL** | Dòng HĐ / PLBS không có `firm_support_accounting` hoặc mẫu số `before_vat_product + before_vat_repair_service = 0` → ERP ra NULL; `SUM` bỏ **cả dòng** đó (PLBS không được cộng vào Tổng DSTC), hoặc trống ô nếu HĐ chỉ có 1 dòng. HRM tính dự phòng = 0 và chi phí thị trường = 0 trong định mức giảm giá còn lại (§5). | 3 cột DSTC | ERP trống / nhỏ hơn |
| **2 dòng HTHT** | HĐ có 2 dòng `wr_support_accounting`: ERP join nhân đôi dòng; HRM lấy dòng mới nhất (đã biết: wr 3948). | Giá trị HĐ, 3 cột DSTC | ERP = HRM × 2 |

Một số ca đáng xem khi QA:
- **firm 21072** `HĐ_TPSG_KV4_26_0183_02062026` (Quý II): Tổng DSTC tiêu chuẩn ERP 133.515.000, HRM 795.264.941 — PLBS 24469 (giá trị 709.776.000) không có HTHT nên ERP bỏ cả PLBS khỏi Tổng DSTC.
- **firm 418** `HĐ_TPSG_KV4_25_0006_VFSGQL13 LAN2`: PLBS 4132 có HTHT với mẫu số 0 → ERP bỏ 1.090.000 (3.815.000 DSTC − 2.725.000 định mức).
- **firm 1720 / 2476 / 16636**: HĐ không PLBS, không có HTHT → ERP trống ô Tổng DSTC tiêu chuẩn. Riêng 1720 (tạo trước 01/11/2025) HRM ra 1.162.500 = 1.200.000 DSTC − 37.500 định mức giảm giá còn lại (chi phí thị trường coi là 0), không phải 1.200.000.
- **wr 456** `HDDV_TPE_HN_KDTM_25_0007_SÀI ĐÒNG` (Quý II): PLBS 588 có bút toán riêng; Phải thu/Đã thu ERP 2.035.368 (chỉ dòng cha), HRM 3.104.568 (cha + PLBS 1.069.200).
- **wr 3948** `HDDV_TPE_HN_KD2_26_0057_705R` (03/2026): ERP ×2 do 2 dòng HTHT.

## 4. Chưa đối số được bằng dữ liệu local

- Typo `ServiceAccounting` của HĐ dịch vụ (§2.3): `account_details` không có dòng `ServiceAccounting` nào gắn `WrServiceContract` → không phát sinh lệch; dựa vào test feature.
- Lọc chỉ Mã HĐ, không ngày (§5): ERP hỏng ở trường hợp này nên không có số ERP để so.
- HĐ HRM: không có HĐ HRM nào trong 3 kỳ.
- Dòng tổng phòng / NV (§2.3): HRM tính trên toàn bộ dữ liệu lọc, ERP chỉ theo trang → không so theo dòng tổng, chỉ so dòng HĐ và TỔNG CỘNG.

## 5. Bảng HĐ lệch (mọi ô lệch, đã xếp lý do)

Số làm tròn đến đồng. "(trống)" = ERP NULL, màn ERP để trống ô. Mỗi dòng là 1 ô lệch.

### Tháng 07/2026 (01/07–31/07/2026)

| Nguồn | Mã HĐ (id) | Cột | ERP | HRM | Lý do |
|---|---|---|---|---|---|
| firm | HĐ_TPSG_KV4_25_0006_VFSGQL13 LAN2 (418) | Tổng DSTC tiêu chuẩn | 936.831.753 | 937.921.753 | Dự phòng NULL |
| firm | HĐ_TPSG_KV4_25_0006_VFSGQL13 LAN2 (418) | Tổng DSTC thực xuất | 924.205.978 | 925.295.978 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Giá trị HĐ | 4.226.904 | 2.113.452 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Tổng DSTC tiêu chuẩn | 4.448.668 | 2.224.334 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Tổng DSTC thực xuất | 4.448.668 | 2.224.334 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Giá trị HĐ | 3.122.323.200 | 1.561.161.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Tổng DSTC tiêu chuẩn | 2.715.524.000 | 1.357.762.000 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | DS tiêu chuẩn | 2.715.524.000 | 1.357.762.000 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Tổng DSTC thực xuất | 2.715.524.000 | 1.357.762.000 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Giá trị HĐ | 303.600.000 | 75.900.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Tổng DSTC tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Tổng DSTC thực xuất | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Giá trị HĐ | 199.152.000 | 49.788.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Tổng DSTC tiêu chuẩn | 232.344.000 | 58.086.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Tổng DSTC thực xuất | 232.344.000 | 58.086.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | Giá trị HĐ | 29.203.200 | 14.601.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | Tổng DSTC tiêu chuẩn | 30.825.600 | 15.412.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | DS tiêu chuẩn | -30.825.600 | -15.412.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | Giá trị HĐ | 20.606.400 | 6.868.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | Tổng DSTC tiêu chuẩn | 19.828.800 | 6.609.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | DS tiêu chuẩn | -19.828.800 | -6.609.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Giá trị HĐ | 959.472 | 479.736 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Tổng DSTC tiêu chuẩn | 1.146.617 | 573.308 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | DS tiêu chuẩn | 844.217 | 422.108 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Tổng DSTC thực xuất | 1.146.617 | 573.308 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Giá trị HĐ | 303.600.000 | 75.900.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Tổng DSTC tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Tổng DSTC thực xuất | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Giá trị HĐ | 17.690.400 | 5.896.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Tổng DSTC tiêu chuẩn | 19.391.400 | 6.463.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Tổng DSTC thực xuất | 19.391.400 | 6.463.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Giá trị HĐ | 104.652.000 | 34.884.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Tổng DSTC tiêu chuẩn | 117.762.000 | 39.254.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Tổng DSTC thực xuất | 117.762.000 | 39.254.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Giá trị HĐ | 28.944.000 | 14.472.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Tổng DSTC tiêu chuẩn | 30.183.600 | 15.091.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | DS tiêu chuẩn | 2.956.800 | 1.478.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Tổng DSTC thực xuất | 28.671.600 | 14.335.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0878_TP-KIACB (23060) | Giá trị HĐ | 24.056.000 | 12.028.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0878_TP-KIACB (23060) | Tổng DSTC tiêu chuẩn | 24.532.800 | 12.266.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0878_TP-KIACB (23060) | DS tiêu chuẩn | 20.383.200 | 10.191.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0878_TP-KIACB (23060) | Tổng DSTC thực xuất | 20.383.200 | 10.191.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0673_01.726 (23389) | Giá trị HĐ | 105.840.000 | 52.920.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0673_01.726 (23389) | Tổng DSTC tiêu chuẩn | 102.600.000 | 51.300.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0673_01.726 (23389) | DS tiêu chuẩn | 102.600.000 | 51.300.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0673_01.726 (23389) | Tổng DSTC thực xuất | 102.600.000 | 51.300.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0676_02072026 (23453) | Giá trị HĐ | 6.237.000 | 2.079.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0676_02072026 (23453) | Tổng DSTC tiêu chuẩn | 7.711.200 | 2.570.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0676_02072026 (23453) | DS tiêu chuẩn | 7.711.200 | 2.570.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0676_02072026 (23453) | Tổng DSTC thực xuất | 7.711.200 | 2.570.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDTM_26_0856_TPE-VFDN-001 (23484) | Tổng DSTC tiêu chuẩn | 512.734.060 | 521.158.060 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0703_MLC (23848) | Giá trị HĐ | 1.944.000 | 648.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0703_MLC (23848) | Tổng DSTC tiêu chuẩn | 2.268.000 | 756.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0703_MLC (23848) | DS tiêu chuẩn | 2.268.000 | 756.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0703_MLC (23848) | Tổng DSTC thực xuất | 2.268.000 | 756.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0243_14072026 (24090) | Giá trị HĐ | 63.582.624 | 15.895.656 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0243_14072026 (24090) | Tổng DSTC tiêu chuẩn | 64.482.624 | 16.120.656 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0243_14072026 (24090) | DS tiêu chuẩn | 64.482.624 | 16.120.656 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0243_14072026 (24090) | Tổng DSTC thực xuất | 64.482.624 | 16.120.656 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0974_KIAMAZDATB_1607 (24267) | Giá trị HĐ | 5.508.000 | 2.754.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0974_KIAMAZDATB_1607 (24267) | Tổng DSTC tiêu chuẩn | 7.000.000 | 3.500.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0974_KIAMAZDATB_1607 (24267) | DS tiêu chuẩn | 7.000.000 | 3.500.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0974_KIAMAZDATB_1607 (24267) | Tổng DSTC thực xuất | 7.000.000 | 3.500.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0997_TPE-VFNTL (24553) | Giá trị HĐ | 604.800 | 302.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0997_TPE-VFNTL (24553) | Tổng DSTC tiêu chuẩn | 744.800 | 372.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0997_TPE-VFNTL (24553) | DS tiêu chuẩn | 744.800 | 372.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0997_TPE-VFNTL (24553) | Tổng DSTC thực xuất | 744.800 | 372.400 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0321_24072026 (24769) | Tổng DSTC tiêu chuẩn | 201.275.555 | 202.146.705 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_26_1016_TPE-HAVP (24798) | Giá trị HĐ | 3.348.000 | 1.674.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_1016_TPE-HAVP (24798) | Tổng DSTC tiêu chuẩn | 3.906.000 | 1.953.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_1016_TPE-HAVP (24798) | DS tiêu chuẩn | 3.906.000 | 1.953.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_1016_TPE-HAVP (24798) | Tổng DSTC thực xuất | 3.906.000 | 1.953.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Giá trị HĐ | 26.463.316 | 8.821.105 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Tổng DSTC tiêu chuẩn | 28.927.387 | 9.642.462 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Tổng DSTC thực xuất | 28.927.387 | 9.642.462 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Thực thu | (trống) | 7.741.105 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Phải thu | (trống) | 7.741.105 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Đã thu | (trống) | 7.741.105 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Thực thu | (trống) | 50.176.307 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Phải thu | (trống) | 111.721.918 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Đã thu | (trống) | 104.706.398 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Còn nợ | (trống) | 7.015.520 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0093_MECHOAKIEM.CA (4224) | Thực thu | (trống) | 27.567.648 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0093_MECHOAKIEM.CA (4224) | Phải thu | (trống) | 27.567.648 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0093_MECHOAKIEM.CA (4224) | Đã thu | (trống) | 27.567.648 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0112_VINFASTBACGIANG (4424) | DS theo HĐ | (trống) | 3.715.500 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0112_VINFASTBACGIANG (4424) | Thực thu | (trống) | 7.414.740 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0112_VINFASTBACGIANG (4424) | Phải thu | (trống) | 7.414.740 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0112_VINFASTBACGIANG (4424) | Đã thu | (trống) | 7.414.740 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0131_FORDHAIPHONG.CA (4658) | Thực thu | (trống) | 15.357.384 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0131_FORDHAIPHONG.CA (4658) | Phải thu | (trống) | 12.657.384 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0131_FORDHAIPHONG.CA (4658) | Đã thu | (trống) | 15.357.384 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0131_FORDHAIPHONG.CA (4658) | Còn nợ | (trống) | -2.700.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0154_CSKH-BONGSAY (5223) | Thực thu | (trống) | 2.507.760 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0154_CSKH-BONGSAY (5223) | Phải thu | (trống) | 2.507.760 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0154_CSKH-BONGSAY (5223) | Đã thu | (trống) | 2.507.760 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0076_DV110526_PA (5243) | DS theo HĐ | (trống) | 20.639.250 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0076_DV110526_PA (5243) | Phải thu | (trống) | 24.914.790 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0076_DV110526_PA (5243) | Đã thu | (trống) | 22.127.499 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0076_DV110526_PA (5243) | Còn nợ | (trống) | 2.787.291 | Sổ cái PLBS |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Giá trị HĐ | 5.140.800 | 1.285.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Tổng DSTC tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Tổng DSTC thực xuất | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Giá trị HĐ | 5.140.800 | 1.285.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Tổng DSTC tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Tổng DSTC thực xuất | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Giá trị HĐ | 6.998.400 | 3.499.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Tổng DSTC tiêu chuẩn | 8.618.400 | 4.309.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Tổng DSTC thực xuất | 8.618.400 | 4.309.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0196_HY.HONDA.DVSC (5789) | DS theo HĐ | (trống) | 2.249.100 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0196_HY.HONDA.DVSC (5789) | Phải thu | (trống) | 8.358.228 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0196_HY.HONDA.DVSC (5789) | Còn nợ | (trống) | 8.358.228 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0198_MAZDALVL_0606 (5792) | Thực thu | (trống) | 2.911.140 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0198_MAZDALVL_0606 (5792) | Phải thu | (trống) | 2.911.140 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0198_MAZDALVL_0606 (5792) | Đã thu | (trống) | 2.911.140 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0198_MITSHUBISHITUYENQUANG (5814) | DS theo HĐ | (trống) | 481.950 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0198_MITSHUBISHITUYENQUANG (5814) | Phải thu | (trống) | 1.541.106 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0198_MITSHUBISHITUYENQUANG (5814) | Đã thu | (trống) | 1.541.106 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Giá trị HĐ | 7.299.936 | 3.649.968 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Tổng DSTC tiêu chuẩn | 16.581.600 | 8.290.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | DS tiêu chuẩn | 1.915.200 | 957.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Tổng DSTC thực xuất | 9.097.200 | 4.548.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0204_HYUNDAIPVD_1006 (5856) | Thực thu | (trống) | 5.399.752 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0204_HYUNDAIPVD_1006 (5856) | Phải thu | (trống) | 5.691.352 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0204_HYUNDAIPVD_1006 (5856) | Đã thu | (trống) | 5.399.752 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0204_HYUNDAIPVD_1006 (5856) | Còn nợ | (trống) | 291.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0106_PA_DV10062026 (5870) | DS theo HĐ | (trống) | 16.494.900 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0106_PA_DV10062026 (5870) | Phải thu | (trống) | 19.369.692 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0106_PA_DV10062026 (5870) | Đã thu | (trống) | 10.872.846 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0106_PA_DV10062026 (5870) | Còn nợ | (trống) | 8.496.846 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0203_CSKH-BMWTHAOLAPMNK (5878) | Giá trị HĐ | 4.597.560 | 2.298.780 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0203_CSKH-BMWTHAOLAPMNK (5878) | Tổng DSTC tiêu chuẩn | 3.581.424 | 1.790.712 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0203_CSKH-BMWTHAOLAPMNK (5878) | DS tiêu chuẩn | 3.581.424 | 1.790.712 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0203_CSKH-BMWTHAOLAPMNK (5878) | Tổng DSTC thực xuất | 3.581.424 | 1.790.712 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Giá trị HĐ | 1.802.088 | 901.044 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Tổng DSTC tiêu chuẩn | 2.341.332 | 1.170.666 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Tổng DSTC thực xuất | 2.341.332 | 1.170.666 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0111_42 (5936) | DS theo HĐ | (trống) | 1.245.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0111_42 (5936) | Thực thu | (trống) | 2.316.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0111_42 (5936) | Phải thu | (trống) | 2.404.080 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0111_42 (5936) | Đã thu | (trống) | 2.316.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0111_42 (5936) | Còn nợ | (trống) | 87.480 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Giá trị HĐ | 14.164.632 | 7.082.316 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Tổng DSTC tiêu chuẩn | 14.971.032 | 7.485.516 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Tổng DSTC thực xuất | 11.947.032 | 5.973.516 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0214_SCCAUKICHPHU (6016) | Thực thu | (trống) | 2.668.140 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0214_SCCAUKICHPHU (6016) | Phải thu | (trống) | 4.806.540 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0214_SCCAUKICHPHU (6016) | Đã thu | (trống) | 2.668.140 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0214_SCCAUKICHPHU (6016) | Còn nợ | (trống) | 2.138.400 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0120_MERĐNTTB (6042) | DS theo HĐ | (trống) | 4.429.900 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0120_MERĐNTTB (6042) | Phải thu | (trống) | 4.784.292 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0120_MERĐNTTB (6042) | Còn nợ | (trống) | 4.784.292 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0219_HYUNDAIVY_2006 (6071) | DS theo HĐ | (trống) | 571.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0219_HYUNDAIVY_2006 (6071) | Thực thu | (trống) | 1.200.204 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0219_HYUNDAIVY_2006 (6071) | Phải thu | (trống) | 1.200.204 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0219_HYUNDAIVY_2006 (6071) | Đã thu | (trống) | 1.200.204 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Giá trị HĐ | 3.485.894 | 1.742.947 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Tổng DSTC tiêu chuẩn | 3.386.074 | 1.693.037 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Tổng DSTC thực xuất | 3.386.074 | 1.693.037 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Giá trị HĐ | 8.856.000 | 4.428.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Tổng DSTC tiêu chuẩn | 10.313.352 | 5.156.676 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | DS tiêu chuẩn | 976.752 | 488.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Tổng DSTC thực xuất | 10.313.352 | 5.156.676 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0214_TOYOTAYB.CA (6126) | Thực thu | (trống) | 8.705.880 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0214_TOYOTAYB.CA (6126) | Phải thu | (trống) | 8.705.880 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0214_TOYOTAYB.CA (6126) | Đã thu | (trống) | 8.705.880 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0217_CSKH-BMWGPSUAMAYNENCRS20 (6132) | Giá trị HĐ | 10.322.640 | 5.161.320 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0217_CSKH-BMWGPSUAMAYNENCRS20 (6132) | Tổng DSTC tiêu chuẩn | 16.515.360 | 8.257.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0217_CSKH-BMWGPSUAMAYNENCRS20 (6132) | DS tiêu chuẩn | 13.669.920 | 6.834.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0217_CSKH-BMWGPSUAMAYNENCRS20 (6132) | Tổng DSTC thực xuất | 13.669.920 | 6.834.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0127_MITSULBSCCK (6160) | Phải thu | (trống) | 2.240.698 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0127_MITSULBSCCK (6160) | Còn nợ | (trống) | 2.240.698 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0216_SC.CN-GL3000A (6174) | DS theo HĐ | (trống) | 4.636.500 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0216_SC.CN-GL3000A (6174) | Phải thu | (trống) | 6.708.420 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0216_SC.CN-GL3000A (6174) | Còn nợ | (trống) | 6.708.420 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0219_FORDBACGIANG (6200) | Giá trị HĐ | 1.180.008 | 590.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0219_FORDBACGIANG (6200) | Tổng DSTC tiêu chuẩn | 6.961.752 | 3.480.876 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0219_FORDBACGIANG (6200) | DS tiêu chuẩn | 1.575.252 | 787.626 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0219_FORDBACGIANG (6200) | Tổng DSTC thực xuất | 1.575.252 | 787.626 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0129_MSULBTAXL (6263) | DS theo HĐ | (trống) | 6.201.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0129_MSULBTAXL (6263) | Phải thu | (trống) | 7.484.400 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0129_MSULBTAXL (6263) | Còn nợ | (trống) | 7.484.400 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0229_CSKH-TOYOTA20ATHAYCAPBACNHUA (6342) | DS theo HĐ | (trống) | 1.917.500 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0229_CSKH-TOYOTA20ATHAYCAPBACNHUA (6342) | Phải thu | (trống) | 5.634.900 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0229_CSKH-TOYOTA20ATHAYCAPBACNHUA (6342) | Còn nợ | (trống) | 5.634.900 | Sổ cái PLBS |
| wr | HDDV_TPSG_SG_CSKH_26_0262_09594 (6353) | Giá trị HĐ | 1.825.202 | 912.601 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0262_09594 (6353) | Tổng DSTC tiêu chuẩn | 1.808.802 | 904.401 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0262_09594 (6353) | DS tiêu chuẩn | 1.808.802 | 904.401 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0262_09594 (6353) | Tổng DSTC thực xuất | 1.808.802 | 904.401 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0231_CSKH-ATACH88ADAOTIEN (6374) | DS theo HĐ | (trống) | 321.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0231_CSKH-ATACH88ADAOTIEN (6374) | Phải thu | (trống) | 5.304.204 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0231_CSKH-ATACH88ADAOTIEN (6374) | Còn nợ | (trống) | 5.304.204 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0234_HD-CAUNANG7X (6449) | Giá trị HĐ | 4.982.040 | 2.491.020 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0234_HD-CAUNANG7X (6449) | Tổng DSTC tiêu chuẩn | 4.883.760 | 2.441.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0234_HD-CAUNANG7X (6449) | DS tiêu chuẩn | 4.883.760 | 2.441.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0234_HD-CAUNANG7X (6449) | Tổng DSTC thực xuất | 4.883.760 | 2.441.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0137_TYTHTSCMGN (6453) | DS theo HĐ | (trống) | 1.221.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0137_TYTHTSCMGN (6453) | Phải thu | (trống) | 7.151.004 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0137_TYTHTSCMGN (6453) | Còn nợ | (trống) | 7.151.004 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0254_SUBARUHN_1107 (6454) | DS theo HĐ | (trống) | 1.857.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0254_SUBARUHN_1107 (6454) | Phải thu | (trống) | 2.378.776 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0254_SUBARUHN_1107 (6454) | Còn nợ | (trống) | 2.378.776 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0256_HADO01 (6492) | Giá trị HĐ | 7.109.208 | 3.554.604 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0256_HADO01 (6492) | Tổng DSTC tiêu chuẩn | 8.461.152 | 4.230.576 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0256_HADO01 (6492) | DS tiêu chuẩn | 8.461.152 | 4.230.576 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0256_HADO01 (6492) | Tổng DSTC thực xuất | 8.461.152 | 4.230.576 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0238_MYB (6501) | Giá trị HĐ | 9.878.663 | 3.292.888 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0238_MYB (6501) | Tổng DSTC tiêu chuẩn | 11.553.690 | 3.851.230 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0238_MYB (6501) | DS tiêu chuẩn | 3.368.490 | 1.122.830 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0238_MYB (6501) | Tổng DSTC thực xuất | 3.368.490 | 1.122.830 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0239_HD-SC-AC1000 (6535) | DS theo HĐ | (trống) | 829.700 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0239_HD-SC-AC1000 (6535) | Thực thu | (trống) | 291.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0239_HD-SC-AC1000 (6535) | Phải thu | (trống) | 3.919.644 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0239_HD-SC-AC1000 (6535) | Đã thu | (trống) | 291.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0239_HD-SC-AC1000 (6535) | Còn nợ | (trống) | 3.628.044 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | Giá trị HĐ | 1.802.088 | 901.044 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | Tổng DSTC tiêu chuẩn | 3.318.084 | 1.659.042 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | DS tiêu chuẩn | 1.934.352 | 967.176 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | Tổng DSTC thực xuất | 1.934.352 | 967.176 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | DS theo HĐ | (trống) | 321.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | Phải thu | (trống) | 735.804 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0269_VFTC_1707 (6595) | Còn nợ | (trống) | 735.804 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0270_KIEMTRA (6601) | Giá trị HĐ | 9.253.440 | 4.626.720 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0270_KIEMTRA (6601) | Tổng DSTC tiêu chuẩn | 13.023.360 | 6.511.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0270_KIEMTRA (6601) | DS tiêu chuẩn | 13.023.360 | 6.511.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0270_KIEMTRA (6601) | Tổng DSTC thực xuất | 13.023.360 | 6.511.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0271_SCC40 (6603) | DS theo HĐ | (trống) | 1.272.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0271_SCC40 (6603) | Phải thu | (trống) | 2.006.208 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0271_SCC40 (6603) | Còn nợ | (trống) | 2.006.208 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0255_OTOSO8-LOCKHI (6657) | Giá trị HĐ | 3.978.504 | 1.989.252 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0255_OTOSO8-LOCKHI (6657) | Tổng DSTC tiêu chuẩn | 4.960.368 | 2.480.184 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0255_OTOSO8-LOCKHI (6657) | DS tiêu chuẩn | 4.960.368 | 2.480.184 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0255_OTOSO8-LOCKHI (6657) | Tổng DSTC thực xuất | 4.960.368 | 2.480.184 | Nhiều hãng xe |

### Quý II/2026 (01/04–30/06/2026)

| Nguồn | Mã HĐ (id) | Cột | ERP | HRM | Lý do |
|---|---|---|---|---|---|
| firm | HĐ_TPE_HN_KD1_25_0011_FordBắcGiang (168) | Giá trị HĐ | 51.506.400 | 25.753.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0011_FordBắcGiang (168) | Tổng DSTC tiêu chuẩn | 56.760.000 | 28.380.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0011_FordBắcGiang (168) | Tổng DSTC thực xuất | 49.560.000 | 24.780.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0006_VFSGQL13 LAN2 (418) | Tổng DSTC tiêu chuẩn | 936.831.753 | 937.921.753 | Dự phòng NULL |
| firm | HĐ_TPSG_KV4_25_0006_VFSGQL13 LAN2 (418) | Tổng DSTC thực xuất | 924.205.978 | 925.295.978 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_25_0040_0031_T11 (1861) | Giá trị HĐ | 25.523.100 | 8.507.700 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0040_0031_T11 (1861) | Tổng DSTC tiêu chuẩn | 28.221.270 | 9.407.090 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0040_0031_T11 (1861) | Tổng DSTC thực xuất | 28.221.270 | 9.407.090 | Nhiều hãng xe |
| firm | HĐ_TPE_TBVLCN_25_0145_PO 3200248701 (2476) | Tổng DSTC tiêu chuẩn | (trống) | 363.600.000 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Giá trị HĐ | 4.226.904 | 2.113.452 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Tổng DSTC tiêu chuẩn | 4.448.668 | 2.224.334 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0135_LCF (4483) | Tổng DSTC thực xuất | 4.448.668 | 2.224.334 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_25_0152_21-01 (4492) | Giá trị HĐ | 3.976.560 | 1.988.280 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_25_0152_21-01 (4492) | Tổng DSTC tiêu chuẩn | 3.918.600 | 1.959.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0357_43 (7223) | Giá trị HĐ | 22.896.000 | 11.448.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0357_43 (7223) | Tổng DSTC tiêu chuẩn | 23.712.000 | 11.856.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Giá trị HĐ | 297.433.176 | 148.716.588 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Tổng DSTC tiêu chuẩn | 307.285.975 | 153.642.988 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Tổng DSTC thực xuất | 249.580.135 | 124.790.068 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV3_25_0130_TPSG - VFAG (8079) | Tổng DSTC tiêu chuẩn | 1.317.372.257 | 1.322.348.429 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Giá trị HĐ | 783.357.075 | 261.119.025 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Tổng DSTC tiêu chuẩn | 864.929.908 | 288.309.969 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | DS tiêu chuẩn | 15.725.868 | 5.241.956 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Tổng DSTC thực xuất | 739.860.873 | 246.620.291 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Giá trị HĐ | 6.944.030.464 | 1.736.007.616 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Tổng DSTC tiêu chuẩn | 7.213.017.536 | 1.803.254.384 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | DS tiêu chuẩn | 277.646.344 | 69.411.586 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Tổng DSTC thực xuất | 6.961.142.200 | 1.740.285.550 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Giá trị HĐ | 693.532.800 | 173.383.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Tổng DSTC tiêu chuẩn | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Tổng DSTC thực xuất | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV3_25_0164_112 TPSG - CARPLA (9021) | Tổng DSTC tiêu chuẩn | 363.448.522 | 369.007.522 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD3_25_0388_01 (9535) | Tổng DSTC tiêu chuẩn | 322.595.787 | 323.214.237 | Dự phòng NULL |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Giá trị HĐ | 693.532.800 | 173.383.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Tổng DSTC tiêu chuẩn | 661.715.864 | 165.428.966 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Tổng DSTC thực xuất | 661.715.864 | 165.428.966 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Giá trị HĐ | 290.785.176 | 145.392.588 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Tổng DSTC tiêu chuẩn | 296.527.073 | 148.263.537 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | DS tiêu chuẩn | 50.913.120 | 25.456.560 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Tổng DSTC thực xuất | 296.527.073 | 148.263.537 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0010_LCF (11462) | Giá trị HĐ | 38.278.656 | 19.139.328 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0010_LCF (11462) | Tổng DSTC tiêu chuẩn | 40.961.856 | 20.480.928 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0010_LCF (11462) | Tổng DSTC thực xuất | 40.961.856 | 20.480.928 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Giá trị HĐ | 282.717.300 | 94.239.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Tổng DSTC tiêu chuẩn | 345.279.417 | 115.093.139 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | DS tiêu chuẩn | 29.311.950 | 9.770.650 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Tổng DSTC thực xuất | 305.116.767 | 101.705.589 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Giá trị HĐ | 26.211.600 | 13.105.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Tổng DSTC tiêu chuẩn | 27.827.800 | 13.913.900 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Tổng DSTC thực xuất | 21.063.000 | 10.531.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Giá trị HĐ | 24.775.200 | 12.387.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Tổng DSTC tiêu chuẩn | 29.845.200 | 14.922.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Tổng DSTC thực xuất | 29.446.200 | 14.723.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Giá trị HĐ | 722.520 | 240.840 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Tổng DSTC tiêu chuẩn | 653.940 | 217.980 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Tổng DSTC thực xuất | 653.940 | 217.980 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0013_CSKH-KHAUCB (13024) | Giá trị HĐ | 2.209.680 | 1.104.840 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0013_CSKH-KHAUCB (13024) | Tổng DSTC tiêu chuẩn | 2.772.000 | 1.386.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0013_CSKH-KHAUCB (13024) | DS tiêu chuẩn | -2.772.000 | -1.386.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0180_26KMNB2 (13426) | Giá trị HĐ | 12.735.360 | 6.367.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0180_26KMNB2 (13426) | Tổng DSTC tiêu chuẩn | 15.683.360 | 7.841.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0180_26KMNB2 (13426) | Tổng DSTC thực xuất | 15.683.360 | 7.841.680 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0066_2402 (13926) | Giá trị HĐ | 5.896.800 | 1.965.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0066_2402 (13926) | Tổng DSTC tiêu chuẩn | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0066_2402 (13926) | Tổng DSTC thực xuất | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Giá trị HĐ | 15.508.800 | 7.754.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Tổng DSTC tiêu chuẩn | 15.966.800 | 7.983.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Tổng DSTC thực xuất | 15.966.800 | 7.983.400 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Giá trị HĐ | 37.584.000 | 18.792.000 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Tổng DSTC tiêu chuẩn | 33.736.400 | 16.868.200 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Tổng DSTC thực xuất | 33.736.400 | 16.868.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Giá trị HĐ | 6.771.600 | 2.257.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Tổng DSTC tiêu chuẩn | 5.956.500 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Tổng DSTC thực xuất | 5.956.500 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Giá trị HĐ | 2.916.000 | 972.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Tổng DSTC tiêu chuẩn | 3.207.900 | 1.069.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Tổng DSTC thực xuất | 3.207.900 | 1.069.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Giá trị HĐ | 453.600 | 151.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Tổng DSTC tiêu chuẩn | 571.200 | 190.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Tổng DSTC thực xuất | 571.200 | 190.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Giá trị HĐ | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Tổng DSTC tiêu chuẩn | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Tổng DSTC thực xuất | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Giá trị HĐ | 39.744.000 | 19.872.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Tổng DSTC tiêu chuẩn | 34.960.000 | 17.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Tổng DSTC thực xuất | 34.960.000 | 17.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Giá trị HĐ | 12.776.400 | 6.388.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Tổng DSTC tiêu chuẩn | 13.041.600 | 6.520.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Tổng DSTC thực xuất | 13.041.600 | 6.520.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | Giá trị HĐ | 260.928 | 130.464 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | Tổng DSTC tiêu chuẩn | 338.240 | 169.120 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | DS tiêu chuẩn | -338.240 | -169.120 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | Giá trị HĐ | 65.599.200 | 32.799.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | Tổng DSTC tiêu chuẩn | 57.281.200 | 28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | DS tiêu chuẩn | -57.281.200 | -28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0237_KHANHVAN (15217) | Giá trị HĐ | 138.495.717 | 46.165.239 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0237_KHANHVAN (15217) | Tổng DSTC tiêu chuẩn | 146.055.108 | 48.685.036 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0237_KHANHVAN (15217) | DS tiêu chuẩn | 146.055.108 | 48.685.036 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0237_KHANHVAN (15217) | Tổng DSTC thực xuất | 146.055.108 | 48.685.036 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Giá trị HĐ | 1.296.000 | 432.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Tổng DSTC tiêu chuẩn | 1.224.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Tổng DSTC thực xuất | 1.224.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Giá trị HĐ | 122.709.600 | 61.354.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Tổng DSTC tiêu chuẩn | 111.586.000 | 55.793.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Tổng DSTC thực xuất | 111.586.000 | 55.793.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Giá trị HĐ | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Tổng DSTC tiêu chuẩn | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Tổng DSTC thực xuất | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Giá trị HĐ | 3.122.323.200 | 1.561.161.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Tổng DSTC tiêu chuẩn | 2.715.524.000 | 1.357.762.000 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0262_FordBacGiang (15475) | Tổng DSTC thực xuất | 2.715.524.000 | 1.357.762.000 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Giá trị HĐ | 3.240.000 | 1.620.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Tổng DSTC tiêu chuẩn | 3.420.000 | 1.710.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Tổng DSTC thực xuất | 3.420.000 | 1.710.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Giá trị HĐ | 9.180.000 | 4.590.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Tổng DSTC tiêu chuẩn | 10.210.800 | 5.105.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Tổng DSTC thực xuất | 10.210.800 | 5.105.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Giá trị HĐ | 3.412.800 | 1.706.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Tổng DSTC tiêu chuẩn | 3.844.400 | 1.922.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Tổng DSTC thực xuất | 3.844.400 | 1.922.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | Giá trị HĐ | 19.250.000 | 9.625.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | Tổng DSTC tiêu chuẩn | 19.530.000 | 9.765.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | DS tiêu chuẩn | -19.530.000 | -9.765.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Giá trị HĐ | 9.374.400 | 4.687.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Tổng DSTC tiêu chuẩn | 10.936.800 | 5.468.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Tổng DSTC thực xuất | 10.936.800 | 5.468.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0382_TPE-HDHN (15926) | Giá trị HĐ | 2.416.461.616 | 1.208.230.808 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0382_TPE-HDHN (15926) | Tổng DSTC tiêu chuẩn | 2.651.593.464 | 1.325.796.732 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0382_TPE-HDHN (15926) | DS tiêu chuẩn | 42.582.800 | 21.291.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0382_TPE-HDHN (15926) | Tổng DSTC thực xuất | 42.582.800 | 21.291.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Giá trị HĐ | 66.960.000 | 33.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Tổng DSTC tiêu chuẩn | 58.900.000 | 29.450.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Tổng DSTC thực xuất | 58.900.000 | 29.450.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Giá trị HĐ | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Tổng DSTC tiêu chuẩn | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Tổng DSTC thực xuất | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0412_KL (16323) | Giá trị HĐ | 10.152.000 | 5.076.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0412_KL (16323) | Tổng DSTC tiêu chuẩn | 11.924.400 | 5.962.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0412_KL (16323) | DS tiêu chuẩn | 11.924.400 | 5.962.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0412_KL (16323) | Tổng DSTC thực xuất | 11.924.400 | 5.962.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0420_TPE-HA (16417) | Giá trị HĐ | 127.245.600 | 63.622.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0420_TPE-HA (16417) | Tổng DSTC tiêu chuẩn | 165.230.200 | 82.615.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0420_TPE-HA (16417) | DS tiêu chuẩn | 146.557.000 | 73.278.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0420_TPE-HA (16417) | Tổng DSTC thực xuất | 146.557.000 | 73.278.500 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0275_031 (16450) | Giá trị HĐ | 312.786.212 | 156.393.106 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0275_031 (16450) | Tổng DSTC tiêu chuẩn | 327.318.066 | 163.659.033 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0275_031 (16450) | DS tiêu chuẩn | 323.649.506 | 161.824.753 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0275_031 (16450) | Tổng DSTC thực xuất | 323.649.506 | 161.824.753 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0132_0204 (16558) | Giá trị HĐ | 2.948.400 | 982.800 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0132_0204 (16558) | Tổng DSTC tiêu chuẩn | 3.231.900 | 1.077.300 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0132_0204 (16558) | DS tiêu chuẩn | 3.231.900 | 1.077.300 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0132_0204 (16558) | Tổng DSTC thực xuất | 3.231.900 | 1.077.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0437_2.4 (16633) | Giá trị HĐ | 7.689.600 | 1.922.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0437_2.4 (16633) | Tổng DSTC tiêu chuẩn | 9.469.600 | 2.367.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0437_2.4 (16633) | DS tiêu chuẩn | 9.469.600 | 2.367.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0437_2.4 (16633) | Tổng DSTC thực xuất | 9.469.600 | 2.367.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0316_02.426 (16636) | Tổng DSTC tiêu chuẩn | (trống) | 5.886.000 | Dự phòng NULL |
| firm | HĐ_TPE_HN_CSKH_26_0051_CSKH-HYUNDAI22AVAMLD (16749) | Giá trị HĐ | 2.531.088 | 1.265.544 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0051_CSKH-HYUNDAI22AVAMLD (16749) | Tổng DSTC tiêu chuẩn | 3.175.200 | 1.587.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0051_CSKH-HYUNDAI22AVAMLD (16749) | DS tiêu chuẩn | 3.175.200 | 1.587.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0051_CSKH-HYUNDAI22AVAMLD (16749) | Tổng DSTC thực xuất | 3.175.200 | 1.587.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0327_HD-VATTUMD (16780) | Giá trị HĐ | 118.160.316 | 59.080.158 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0327_HD-VATTUMD (16780) | Tổng DSTC tiêu chuẩn | 126.351.867 | 63.175.934 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0327_HD-VATTUMD (16780) | DS tiêu chuẩn | 81.178.067 | 40.589.034 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0327_HD-VATTUMD (16780) | Tổng DSTC thực xuất | 81.178.067 | 40.589.034 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0052_CSKH-HONDA38AP300 (16795) | Giá trị HĐ | 40.014.000 | 20.007.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0052_CSKH-HONDA38AP300 (16795) | Tổng DSTC tiêu chuẩn | 44.460.000 | 22.230.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0052_CSKH-HONDA38AP300 (16795) | DS tiêu chuẩn | 44.460.000 | 22.230.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0052_CSKH-HONDA38AP300 (16795) | Tổng DSTC thực xuất | 44.460.000 | 22.230.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0334_TH.XTP (16846) | Giá trị HĐ | 47.952.000 | 15.984.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0334_TH.XTP (16846) | Tổng DSTC tiêu chuẩn | 47.952.000 | 15.984.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0334_TH.XTP (16846) | DS tiêu chuẩn | 47.952.000 | 15.984.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0334_TH.XTP (16846) | Tổng DSTC thực xuất | 47.952.000 | 15.984.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0095_070426 (16937) | Giá trị HĐ | 4.179.600 | 1.393.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0095_070426 (16937) | Tổng DSTC tiêu chuẩn | 4.876.200 | 1.625.400 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0095_070426 (16937) | DS tiêu chuẩn | 4.876.200 | 1.625.400 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0095_070426 (16937) | Tổng DSTC thực xuất | 4.876.200 | 1.625.400 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0147_08042026 (17112) | Giá trị HĐ | 5.248.800 | 1.749.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0147_08042026 (17112) | Tổng DSTC tiêu chuẩn | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0147_08042026 (17112) | DS tiêu chuẩn | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0147_08042026 (17112) | Tổng DSTC thực xuất | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0107_1004-BMW-PMH (17236) | Giá trị HĐ | 693.532.800 | 173.383.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0107_1004-BMW-PMH (17236) | Tổng DSTC tiêu chuẩn | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0107_1004-BMW-PMH (17236) | DS tiêu chuẩn | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0107_1004-BMW-PMH (17236) | Tổng DSTC thực xuất | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0486_TPE-HA (17600) | Giá trị HĐ | 8.947.584 | 4.473.792 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0486_TPE-HA (17600) | Tổng DSTC tiêu chuẩn | 9.509.784 | 4.754.892 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0486_TPE-HA (17600) | DS tiêu chuẩn | 9.509.784 | 4.754.892 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0486_TPE-HA (17600) | Tổng DSTC thực xuất | 9.509.784 | 4.754.892 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0379_VFTH (17977) | Giá trị HĐ | 6.555.600 | 2.185.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0379_VFTH (17977) | Tổng DSTC tiêu chuẩn | 8.160.000 | 2.720.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0379_VFTH (17977) | DS tiêu chuẩn | 8.160.000 | 2.720.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0379_VFTH (17977) | Tổng DSTC thực xuất | 8.160.000 | 2.720.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0218_H23.04.26 (18247) | Giá trị HĐ | 24.948.000 | 8.316.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0218_H23.04.26 (18247) | Tổng DSTC tiêu chuẩn | 21.945.000 | 7.315.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0404_KHANHVAN (18284) | Giá trị HĐ | 6.237.000 | 2.079.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0404_KHANHVAN (18284) | Tổng DSTC tiêu chuẩn | 6.327.720 | 2.109.240 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0404_KHANHVAN (18284) | DS tiêu chuẩn | 6.327.720 | 2.109.240 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0404_KHANHVAN (18284) | Tổng DSTC thực xuất | 6.327.720 | 2.109.240 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0066_CSKH-BITCARDAURA32 (18401) | Giá trị HĐ | 4.224.096 | 2.112.048 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0066_CSKH-BITCARDAURA32 (18401) | Tổng DSTC tiêu chuẩn | 4.960.200 | 2.480.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0066_CSKH-BITCARDAURA32 (18401) | DS tiêu chuẩn | 4.960.200 | 2.480.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_CSKH_26_0066_CSKH-BITCARDAURA32 (18401) | Tổng DSTC thực xuất | 4.960.200 | 2.480.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0428_04.526 (18654) | Giá trị HĐ | 4.514.400 | 2.257.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0428_04.526 (18654) | Tổng DSTC tiêu chuẩn | 3.971.000 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0428_04.526 (18654) | DS tiêu chuẩn | 3.971.000 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0428_04.526 (18654) | Tổng DSTC thực xuất | 3.971.000 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0430_THACOLS (18669) | Giá trị HĐ | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0430_THACOLS (18669) | Tổng DSTC tiêu chuẩn | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0430_THACOLS (18669) | DS tiêu chuẩn | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0430_THACOLS (18669) | Tổng DSTC thực xuất | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0185_0405 (18710) | Giá trị HĐ | 5.896.800 | 1.965.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0185_0405 (18710) | Tổng DSTC tiêu chuẩn | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0185_0405 (18710) | DS tiêu chuẩn | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0185_0405 (18710) | Tổng DSTC thực xuất | 6.463.800 | 2.154.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0435_020.526 (18746) | Giá trị HĐ | 22.275.856 | 11.137.928 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0435_020.526 (18746) | Tổng DSTC tiêu chuẩn | 25.775.352 | 12.887.676 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0435_020.526 (18746) | DS tiêu chuẩn | 25.775.352 | 12.887.676 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0435_020.526 (18746) | Tổng DSTC thực xuất | 25.775.352 | 12.887.676 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0584_12.26.kd2 (18882) | Giá trị HĐ | 10.044.000 | 5.022.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0584_12.26.kd2 (18882) | Tổng DSTC tiêu chuẩn | 8.645.000 | 4.322.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0584_12.26.kd2 (18882) | DS tiêu chuẩn | 8.645.000 | 4.322.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0584_12.26.kd2 (18882) | Tổng DSTC thực xuất | 8.645.000 | 4.322.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0448_TRONGTHIEN (18955) | Giá trị HĐ | 656.640 | 328.320 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0448_TRONGTHIEN (18955) | Tổng DSTC tiêu chuẩn | 851.200 | 425.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0448_TRONGTHIEN (18955) | DS tiêu chuẩn | 851.200 | 425.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0448_TRONGTHIEN (18955) | Tổng DSTC thực xuất | 851.200 | 425.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Giá trị HĐ | 303.600.000 | 75.900.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Tổng DSTC tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | DS tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0134_070520261 (18994) | Tổng DSTC thực xuất | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0602_VT8-TPE (19062) | Giá trị HĐ | 13.608.000 | 6.804.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0602_VT8-TPE (19062) | Tổng DSTC tiêu chuẩn | 12.821.200 | 6.410.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0602_VT8-TPE (19062) | DS tiêu chuẩn | 12.821.200 | 6.410.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0602_VT8-TPE (19062) | Tổng DSTC thực xuất | 12.821.200 | 6.410.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0611_TPE-HA (19129) | Giá trị HĐ | 4.320.000 | 2.160.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0611_TPE-HA (19129) | Tổng DSTC tiêu chuẩn | 5.320.000 | 2.660.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0611_TPE-HA (19129) | DS tiêu chuẩn | 5.320.000 | 2.660.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0611_TPE-HA (19129) | Tổng DSTC thực xuất | 5.320.000 | 2.660.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0613_KIAMAZDATB_1105 (19147) | Giá trị HĐ | 820.800 | 410.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0613_KIAMAZDATB_1105 (19147) | Tổng DSTC tiêu chuẩn | 816.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0613_KIAMAZDATB_1105 (19147) | DS tiêu chuẩn | 816.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0613_KIAMAZDATB_1105 (19147) | Tổng DSTC thực xuất | 816.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Giá trị HĐ | 199.152.000 | 49.788.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Tổng DSTC tiêu chuẩn | 232.344.000 | 58.086.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | DS tiêu chuẩn | 232.344.000 | 58.086.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0142_1205 - BMW-PMH-CABINET (19238) | Tổng DSTC thực xuất | 232.344.000 | 58.086.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0247_H12.05 (19250) | Giá trị HĐ | 42.670.800 | 14.223.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0247_H12.05 (19250) | Tổng DSTC tiêu chuẩn | 51.764.400 | 17.254.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0474_VINAHOABINH (19373) | Giá trị HĐ | 4.527.360 | 2.263.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0474_VINAHOABINH (19373) | Tổng DSTC tiêu chuẩn | 5.281.920 | 2.640.960 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0474_VINAHOABINH (19373) | DS tiêu chuẩn | 5.281.920 | 2.640.960 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0474_VINAHOABINH (19373) | Tổng DSTC thực xuất | 5.281.920 | 2.640.960 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0641_VPNHL (19471) | Giá trị HĐ | 6.335.064 | 3.167.532 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0641_VPNHL (19471) | Tổng DSTC tiêu chuẩn | 6.505.964 | 3.252.982 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0641_VPNHL (19471) | DS tiêu chuẩn | 5.960.664 | 2.980.332 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0641_VPNHL (19471) | Tổng DSTC thực xuất | 5.960.664 | 2.980.332 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0483_HYUNDAITUYENQUANG (19479) | Giá trị HĐ | 293.266.720 | 146.633.360 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0483_HYUNDAITUYENQUANG (19479) | Tổng DSTC tiêu chuẩn | 272.197.320 | 136.098.660 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0483_HYUNDAITUYENQUANG (19479) | DS tiêu chuẩn | 272.197.320 | 136.098.660 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0483_HYUNDAITUYENQUANG (19479) | Tổng DSTC thực xuất | 272.197.320 | 136.098.660 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0153_kv4-18052026 (19535) | Giá trị HĐ | 62.380.800 | 15.595.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0153_kv4-18052026 (19535) | Tổng DSTC tiêu chuẩn | 62.380.800 | 15.595.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0153_kv4-18052026 (19535) | DS tiêu chuẩn | 62.380.800 | 15.595.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0153_kv4-18052026 (19535) | Tổng DSTC thực xuất | 62.380.800 | 15.595.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | Giá trị HĐ | 29.203.200 | 14.601.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | Tổng DSTC tiêu chuẩn | 30.825.600 | 15.412.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0661_VT08-TPE 02 (19833) | DS tiêu chuẩn | 30.825.600 | 15.412.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0398_Q25-05 (20364) | Giá trị HĐ | 14.688.000 | 7.344.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0398_Q25-05 (20364) | Tổng DSTC tiêu chuẩn | 15.177.600 | 7.588.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0398_Q25-05 (20364) | DS tiêu chuẩn | 15.177.600 | 7.588.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0398_Q25-05 (20364) | Tổng DSTC thực xuất | 15.177.600 | 7.588.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | Giá trị HĐ | 20.606.400 | 6.868.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | Tổng DSTC tiêu chuẩn | 19.828.800 | 6.609.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0522_TH.VFXTP (20560) | DS tiêu chuẩn | 19.828.800 | 6.609.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0725_KL (20807) | Giá trị HĐ | 18.406.440 | 9.203.220 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0725_KL (20807) | Tổng DSTC tiêu chuẩn | 20.086.800 | 10.043.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0725_KL (20807) | DS tiêu chuẩn | 20.086.800 | 10.043.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0725_KL (20807) | Tổng DSTC thực xuất | 20.086.800 | 10.043.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0744_DC01 XTP-TPE (21032) | Giá trị HĐ | 42.670.800 | 14.223.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0744_DC01 XTP-TPE (21032) | Tổng DSTC tiêu chuẩn | 52.153.200 | 17.384.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0744_DC01 XTP-TPE (21032) | DS tiêu chuẩn | 52.153.200 | 17.384.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0744_DC01 XTP-TPE (21032) | Tổng DSTC thực xuất | 52.153.200 | 17.384.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0746_DC03 (21043) | Giá trị HĐ | 88.919.200 | 44.459.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0746_DC03 (21043) | Tổng DSTC tiêu chuẩn | 77.421.200 | 38.710.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0746_DC03 (21043) | DS tiêu chuẩn | 57.281.200 | 28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0746_DC03 (21043) | Tổng DSTC thực xuất | 57.281.200 | 28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0183_02062026 (21072) | Tổng DSTC tiêu chuẩn | 133.515.000 | 795.264.941 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Giá trị HĐ | 959.472 | 479.736 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Tổng DSTC tiêu chuẩn | 1.146.617 | 573.308 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | DS tiêu chuẩn | 302.400 | 151.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0749_TPE-HA (21116) | Tổng DSTC thực xuất | 1.146.617 | 573.308 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Giá trị HĐ | 303.600.000 | 75.900.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Tổng DSTC tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | DS tiêu chuẩn | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_26_0186_0406-BMW-TC-CABINET (21185) | Tổng DSTC thực xuất | 298.080.000 | 74.520.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0566_LCF (21354) | Giá trị HĐ | 16.480.800 | 8.240.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0566_LCF (21354) | Tổng DSTC tiêu chuẩn | 16.695.360 | 8.347.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0566_LCF (21354) | DS tiêu chuẩn | 16.695.360 | 8.347.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0566_LCF (21354) | Tổng DSTC thực xuất | 16.695.360 | 8.347.680 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0768_KL (21480) | Giá trị HĐ | 11.302.416 | 5.651.208 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0768_KL (21480) | Tổng DSTC tiêu chuẩn | 14.651.280 | 7.325.640 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0768_KL (21480) | DS tiêu chuẩn | 14.651.280 | 7.325.640 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0768_KL (21480) | Tổng DSTC thực xuất | 14.651.280 | 7.325.640 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0775_TP-NLX (21549) | Giá trị HĐ | 180.364 | 90.182 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0775_TP-NLX (21549) | Tổng DSTC tiêu chuẩn | 232.050 | 116.025 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0775_TP-NLX (21549) | DS tiêu chuẩn | 232.050 | 116.025 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0775_TP-NLX (21549) | Tổng DSTC thực xuất | 232.050 | 116.025 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0456_Q10-06 (21658) | Giá trị HĐ | 12.960.000 | 6.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0456_Q10-06 (21658) | Tổng DSTC tiêu chuẩn | 13.680.000 | 6.840.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0456_Q10-06 (21658) | DS tiêu chuẩn | 13.680.000 | 6.840.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0456_Q10-06 (21658) | Tổng DSTC thực xuất | 13.680.000 | 6.840.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0461_Q15-06 (22010) | Giá trị HĐ | 4.860.000 | 2.430.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0461_Q15-06 (22010) | Tổng DSTC tiêu chuẩn | 5.985.000 | 2.992.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0461_Q15-06 (22010) | DS tiêu chuẩn | 5.985.000 | 2.992.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0461_Q15-06 (22010) | Tổng DSTC thực xuất | 5.985.000 | 2.992.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Giá trị HĐ | 17.690.400 | 5.896.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Tổng DSTC tiêu chuẩn | 19.391.400 | 6.463.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | DS tiêu chuẩn | 19.391.400 | 6.463.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0814_160626 (22138) | Tổng DSTC thực xuất | 19.391.400 | 6.463.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Giá trị HĐ | 104.652.000 | 34.884.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Tổng DSTC tiêu chuẩn | 117.762.000 | 39.254.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | DS tiêu chuẩn | 117.762.000 | 39.254.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0608_TH.VFXTP (22158) | Tổng DSTC thực xuất | 117.762.000 | 39.254.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0336_10082003 (22381) | Giá trị HĐ | 381.240 | 190.620 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0336_10082003 (22381) | Tổng DSTC tiêu chuẩn | 469.490 | 234.745 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0336_10082003 (22381) | DS tiêu chuẩn | 469.490 | 234.745 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0336_10082003 (22381) | Tổng DSTC thực xuất | 469.490 | 234.745 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Giá trị HĐ | 28.944.000 | 14.472.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Tổng DSTC tiêu chuẩn | 30.183.600 | 15.091.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | DS tiêu chuẩn | 25.714.800 | 12.857.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0627_LCF (22483) | Tổng DSTC thực xuất | 28.671.600 | 14.335.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0636_LCF (22590) | Giá trị HĐ | 6.723.864 | 3.361.932 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0636_LCF (22590) | Tổng DSTC tiêu chuẩn | 7.214.508 | 3.607.254 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0636_LCF (22590) | DS tiêu chuẩn | 1.094.436 | 547.218 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0636_LCF (22590) | Tổng DSTC thực xuất | 1.094.436 | 547.218 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0851_03.KD2 (22704) | Giá trị HĐ | 11.232.000 | 5.616.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0851_03.KD2 (22704) | Tổng DSTC tiêu chuẩn | 12.096.000 | 6.048.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0851_03.KD2 (22704) | DS tiêu chuẩn | 12.096.000 | 6.048.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0851_03.KD2 (22704) | Tổng DSTC thực xuất | 12.096.000 | 6.048.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0001_THACOTRONGTHIEN (21) | Giá trị HĐ | 18.722.880 | 9.361.440 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0001_THACOTRONGTHIEN (21) | Tổng DSTC tiêu chuẩn | 23.310.720 | 11.655.360 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0001_THACOTRONGTHIEN (21) | Tổng DSTC thực xuất | 15.649.920 | 7.824.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_25_0007_SÀI ĐÒNG (456) | Phải thu | 2.035.368 | 3.104.568 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_25_0007_SÀI ĐÒNG (456) | Đã thu | 2.035.368 | 3.104.568 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Giá trị HĐ | 12.975.012 | 4.325.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Tổng DSTC tiêu chuẩn | 15.803.478 | 5.267.826 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Tổng DSTC thực xuất | 15.803.478 | 5.267.826 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Giá trị HĐ | 4.492.079 | 2.246.039 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Tổng DSTC tiêu chuẩn | 5.534.928 | 2.767.464 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Tổng DSTC thực xuất | 5.534.928 | 2.767.464 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Giá trị HĐ | 8.380.800 | 2.095.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Tổng DSTC tiêu chuẩn | 12.035.200 | 3.008.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Tổng DSTC thực xuất | 8.835.200 | 2.208.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Giá trị HĐ | 26.463.316 | 8.821.105 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Tổng DSTC tiêu chuẩn | 28.927.387 | 9.642.462 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | DS tiêu chuẩn | 28.927.387 | 9.642.462 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDTM_26_0021_SZKTHSCBP (3747) | Tổng DSTC thực xuất | 28.927.387 | 9.642.462 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | Giá trị HĐ | 2.496.679 | 1.248.340 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | Tổng DSTC tiêu chuẩn | 3.203.928 | 1.601.964 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | DS tiêu chuẩn | -144.396 | -72.198 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0068_CSKH-DUCHUNGHC (3825) | Giá trị HĐ | 24.101.280 | 12.050.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0068_CSKH-DUCHUNGHC (3825) | Tổng DSTC tiêu chuẩn | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Giá trị HĐ | 24.101.280 | 12.050.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Tổng DSTC tiêu chuẩn | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | DS tiêu chuẩn | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Tổng DSTC thực xuất | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Giá trị HĐ | 8.858.808 | 4.429.404 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Tổng DSTC tiêu chuẩn | 11.082.960 | 5.541.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Tổng DSTC thực xuất | 11.082.960 | 5.541.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Giá trị HĐ | 1.846.800 | 923.400 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Tổng DSTC tiêu chuẩn | 2.599.200 | 1.299.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Tổng DSTC thực xuất | 2.599.200 | 1.299.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0084_FORDBACGIANG (4035) | Giá trị HĐ | 6.330.960 | 3.165.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0084_FORDBACGIANG (4035) | Tổng DSTC tiêu chuẩn | 7.086.240 | 3.543.120 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0084_FORDBACGIANG (4035) | DS tiêu chuẩn | 7.086.240 | 3.543.120 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0084_FORDBACGIANG (4035) | Tổng DSTC thực xuất | 7.086.240 | 3.543.120 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0088_16032026 (4092) | Giá trị HĐ | 6.737.040 | 3.368.520 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0088_16032026 (4092) | Tổng DSTC tiêu chuẩn | 9.961.760 | 4.980.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0088_16032026 (4092) | DS tiêu chuẩn | 9.961.760 | 4.980.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0088_16032026 (4092) | Tổng DSTC thực xuất | 9.961.760 | 4.980.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Giá trị HĐ | 11.798.935 | 5.899.468 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Tổng DSTC tiêu chuẩn | 17.577.592 | 8.788.796 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | DS tiêu chuẩn | 4.883.760 | 2.441.880 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Tổng DSTC thực xuất | 12.411.340 | 6.205.670 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0077_KIAMAZDATB_1703 (4138) | Giá trị HĐ | 1.311.120 | 655.560 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0077_KIAMAZDATB_1703 (4138) | Tổng DSTC tiêu chuẩn | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0077_KIAMAZDATB_1703 (4138) | DS tiêu chuẩn | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0077_KIAMAZDATB_1703 (4138) | Tổng DSTC thực xuất | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDXM_26_0009_DV-TT-18.03 (4164) | Giá trị HĐ | 1.382.400 | 691.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDXM_26_0009_DV-TT-18.03 (4164) | Tổng DSTC tiêu chuẩn | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDXM_26_0009_DV-TT-18.03 (4164) | DS tiêu chuẩn | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KDXM_26_0009_DV-TT-18.03 (4164) | Tổng DSTC thực xuất | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Giá trị HĐ | 2.686.975 | 1.343.488 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Tổng DSTC tiêu chuẩn | 2.903.900 | 1.451.950 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Tổng DSTC thực xuất | 2.295.900 | 1.147.950 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0088_BDCRS20 (4206) | Giá trị HĐ | 7.074.000 | 3.537.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0088_BDCRS20 (4206) | Tổng DSTC tiêu chuẩn | 9.310.000 | 4.655.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0088_BDCRS20 (4206) | DS tiêu chuẩn | 4.522.000 | 2.261.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0088_BDCRS20 (4206) | Tổng DSTC thực xuất | 4.522.000 | 2.261.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0111_FORDBG (4419) | Giá trị HĐ | 4.875.163 | 2.437.582 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0111_FORDBG (4419) | Tổng DSTC tiêu chuẩn | 6.168.348 | 3.084.174 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0111_FORDBG (4419) | DS tiêu chuẩn | 6.058.908 | 3.029.454 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0111_FORDBG (4419) | Tổng DSTC thực xuất | 6.058.908 | 3.029.454 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0104_2.4.2 (4463) | Giá trị HĐ | 6.053.616 | 1.513.404 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0104_2.4.2 (4463) | Tổng DSTC tiêu chuẩn | 8.519.904 | 2.129.976 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0104_2.4.2 (4463) | DS tiêu chuẩn | 5.236.704 | 1.309.176 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0104_2.4.2 (4463) | Tổng DSTC thực xuất | 5.236.704 | 1.309.176 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0122_FORDBACGIANG (4505) | Tổng DSTC tiêu chuẩn | 10.852.002 | 5.426.001 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0123_FORDBACGIANG (4506) | Giá trị HĐ | 19.135.440 | 9.567.720 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0123_FORDBACGIANG (4506) | Tổng DSTC tiêu chuẩn | 23.283.360 | 11.641.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0123_FORDBACGIANG (4506) | DS tiêu chuẩn | 23.283.360 | 11.641.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0123_FORDBACGIANG (4506) | Tổng DSTC thực xuất | 23.283.360 | 11.641.680 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0121_CSKH-MIG (4756) | Giá trị HĐ | 4.936.680 | 2.468.340 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0121_CSKH-MIG (4756) | Tổng DSTC tiêu chuẩn | 5.731.920 | 2.865.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0121_CSKH-MIG (4756) | DS tiêu chuẩn | 5.731.920 | 2.865.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0121_CSKH-MIG (4756) | Tổng DSTC thực xuất | 5.731.920 | 2.865.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0129_THAYBANPHIM (4844) | Giá trị HĐ | 7.174.008 | 3.587.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0129_THAYBANPHIM (4844) | Tổng DSTC tiêu chuẩn | 8.158.752 | 4.079.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0129_THAYBANPHIM (4844) | DS tiêu chuẩn | 8.158.752 | 4.079.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0129_THAYBANPHIM (4844) | Tổng DSTC thực xuất | 8.158.752 | 4.079.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0127_CSKH-BANHCOC (4861) | Giá trị HĐ | 571.536 | 285.768 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0127_CSKH-BANHCOC (4861) | Tổng DSTC tiêu chuẩn | 1.213.992 | 606.996 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0133_SCMACH (4867) | Giá trị HĐ | 2.721.600 | 1.360.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0133_SCMACH (4867) | Tổng DSTC tiêu chuẩn | 3.830.400 | 1.915.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0133_SCMACH (4867) | DS tiêu chuẩn | 3.830.400 | 1.915.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0133_SCMACH (4867) | Tổng DSTC thực xuất | 3.830.400 | 1.915.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0146_TH.VFXTP.SCCAUNANG (4870) | Giá trị HĐ | 27.250.214 | 9.083.405 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0146_TH.VFXTP.SCCAUNANG (4870) | Tổng DSTC tiêu chuẩn | 28.131.980 | 9.377.327 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0146_TH.VFXTP.SCCAUNANG (4870) | DS tiêu chuẩn | 17.613.212 | 5.871.071 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0146_TH.VFXTP.SCCAUNANG (4870) | Tổng DSTC thực xuất | 17.613.212 | 5.871.071 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0135_CSKH-RANGT21200 (4931) | Giá trị HĐ | 1.069.200 | 534.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0135_CSKH-RANGT21200 (4931) | Tổng DSTC tiêu chuẩn | 1.341.000 | 670.500 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0135_CSKH-RANGT21200 (4931) | DS tiêu chuẩn | 793.800 | 396.900 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0135_CSKH-RANGT21200 (4931) | Tổng DSTC thực xuất | 793.800 | 396.900 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0166_TH.VFXTP.DVSC (5212) | Giá trị HĐ | 27.705.240 | 9.235.080 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0166_TH.VFXTP.DVSC (5212) | Tổng DSTC tiêu chuẩn | 34.432.560 | 11.477.520 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0166_TH.VFXTP.DVSC (5212) | DS tiêu chuẩn | 34.432.560 | 11.477.520 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0166_TH.VFXTP.DVSC (5212) | Tổng DSTC thực xuất | 34.432.560 | 11.477.520 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0170_FORDBACGIANG (5291) | Giá trị HĐ | 24.840.000 | 12.420.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0170_FORDBACGIANG (5291) | Tổng DSTC tiêu chuẩn | 29.704.752 | 14.852.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0170_FORDBACGIANG (5291) | DS tiêu chuẩn | 29.704.752 | 14.852.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0170_FORDBACGIANG (5291) | Tổng DSTC thực xuất | 29.704.752 | 14.852.376 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0175_TPV (5353) | Tổng DSTC tiêu chuẩn | 2.913.876 | 3.543.876 | Dự phòng NULL |
| wr | HDDV_TPE_HN_KD2_26_0160_5182026 (5356) | Giá trị HĐ | 23.911.200 | 11.955.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0160_5182026 (5356) | Tổng DSTC tiêu chuẩn | 29.611.800 | 14.805.900 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0174_CSKH-DUCHUNGLOCGA (5465) | Giá trị HĐ | 4.471.200 | 2.235.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0174_CSKH-DUCHUNGLOCGA (5465) | Tổng DSTC tiêu chuẩn | 7.703.064 | 3.851.532 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0174_CSKH-DUCHUNGLOCGA (5465) | DS tiêu chuẩn | 5.749.560 | 2.874.780 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0174_CSKH-DUCHUNGLOCGA (5465) | Tổng DSTC thực xuất | 5.749.560 | 2.874.780 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0175_CSKH-HYUNDAI22APROLINE650 (5474) | Giá trị HĐ | 2.462.400 | 1.231.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0175_CSKH-HYUNDAI22APROLINE650 (5474) | Tổng DSTC tiêu chuẩn | 1.641.600 | 820.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0175_CSKH-HYUNDAI22APROLINE650 (5474) | DS tiêu chuẩn | 1.641.600 | 820.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0175_CSKH-HYUNDAI22APROLINE650 (5474) | Tổng DSTC thực xuất | 1.641.600 | 820.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0169_HDDV KMNB (5487) | Giá trị HĐ | 2.692.008 | 1.346.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0169_HDDV KMNB (5487) | Tổng DSTC tiêu chuẩn | 3.610.152 | 1.805.076 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0169_HDDV KMNB (5487) | DS tiêu chuẩn | 3.610.152 | 1.805.076 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0169_HDDV KMNB (5487) | Tổng DSTC thực xuất | 3.610.152 | 1.805.076 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0173_KIAMAZDATB_2305 (5510) | Giá trị HĐ | 6.202.008 | 3.101.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0173_KIAMAZDATB_2305 (5510) | Tổng DSTC tiêu chuẩn | 6.961.752 | 3.480.876 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0173_KIAMAZDATB_2305 (5510) | DS tiêu chuẩn | 6.961.752 | 3.480.876 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0173_KIAMAZDATB_2305 (5510) | Tổng DSTC thực xuất | 6.961.752 | 3.480.876 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0174_MANHINH (5516) | Giá trị HĐ | 14.249.520 | 7.124.760 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0174_MANHINH (5516) | Tổng DSTC tiêu chuẩn | 18.129.420 | 9.064.710 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0188_H TPE.BGDV.2026006445 (5678) | Giá trị HĐ | 1.382.400 | 691.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0188_H TPE.BGDV.2026006445 (5678) | Tổng DSTC tiêu chuẩn | 1.085.280 | 542.640 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Giá trị HĐ | 5.140.800 | 1.285.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Tổng DSTC tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | DS tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0205_08591 (5704) | Tổng DSTC thực xuất | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Giá trị HĐ | 5.140.800 | 1.285.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Tổng DSTC tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | DS tiêu chuẩn | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0206_08712 (5705) | Tổng DSTC thực xuất | 7.235.200 | 1.808.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0192_BITCARLB.CA (5716) | Giá trị HĐ | 4.419.684 | 2.209.842 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0192_BITCARLB.CA (5716) | Tổng DSTC tiêu chuẩn | 6.220.296 | 3.110.148 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0192_BITCARLB.CA (5716) | DS tiêu chuẩn | 6.220.296 | 3.110.148 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0192_BITCARLB.CA (5716) | Tổng DSTC thực xuất | 6.220.296 | 3.110.148 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Giá trị HĐ | 6.998.400 | 3.499.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Tổng DSTC tiêu chuẩn | 8.618.400 | 4.309.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | DS tiêu chuẩn | 8.618.400 | 4.309.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0210_8596 (5737) | Tổng DSTC thực xuất | 8.618.400 | 4.309.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Giá trị HĐ | 7.299.936 | 3.649.968 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Tổng DSTC tiêu chuẩn | 16.581.600 | 8.290.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | DS tiêu chuẩn | 7.182.000 | 3.591.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0199_CSKH-BMWNGOCHOI (5832) | Tổng DSTC thực xuất | 9.097.200 | 4.548.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Giá trị HĐ | 1.802.088 | 901.044 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Tổng DSTC tiêu chuẩn | 2.341.332 | 1.170.666 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | DS tiêu chuẩn | 2.341.332 | 1.170.666 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0208_VFNWYL_1106 (5901) | Tổng DSTC thực xuất | 2.341.332 | 1.170.666 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0206_CSKH-THACOAUTU37APULI (5905) | Giá trị HĐ | 12.707.280 | 6.353.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0206_CSKH-THACOAUTU37APULI (5905) | Tổng DSTC tiêu chuẩn | 10.840.320 | 5.420.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0206_CSKH-THACOAUTU37APULI (5905) | DS tiêu chuẩn | 10.840.320 | 5.420.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0206_CSKH-THACOAUTU37APULI (5905) | Tổng DSTC thực xuất | 10.840.320 | 5.420.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Giá trị HĐ | 14.164.632 | 7.082.316 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Tổng DSTC tiêu chuẩn | 14.971.032 | 7.485.516 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | DS tiêu chuẩn | 11.947.032 | 5.973.516 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0112_42 (5947) | Tổng DSTC thực xuất | 11.947.032 | 5.973.516 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Giá trị HĐ | 3.485.894 | 1.742.947 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Tổng DSTC tiêu chuẩn | 3.386.074 | 1.693.037 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | DS tiêu chuẩn | 3.386.074 | 1.693.037 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0215_CSKH-HYUNDAI22KT3D (6087) | Tổng DSTC thực xuất | 3.386.074 | 1.693.037 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Giá trị HĐ | 8.856.000 | 4.428.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Tổng DSTC tiêu chuẩn | 10.313.352 | 5.156.676 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | DS tiêu chuẩn | 9.336.600 | 4.668.300 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0213_FORDBACGIANG (6124) | Tổng DSTC thực xuất | 10.313.352 | 5.156.676 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0095_NT (1720) | Tổng DSTC tiêu chuẩn | (trống) | 1.162.500 | Dự phòng NULL (thiếu HTHT: HRM giữ định mức giảm giá còn lại với chi phí thị trường = 0) |

### Tháng 03/2026 (01/03–31/03/2026)

| Nguồn | Mã HĐ (id) | Cột | ERP | HRM | Lý do |
|---|---|---|---|---|---|
| firm | HĐ_TPE_TBVLCN_25_0145_PO 3200248701 (2476) | Tổng DSTC tiêu chuẩn | (trống) | 363.600.000 | Dự phòng NULL |
| firm | HĐ_TPSG_KV1_25_0053_250925 Carpla (4968) | Giá trị HĐ | 411.979.644 | 137.326.548 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_25_0053_250925 Carpla (4968) | Tổng DSTC tiêu chuẩn | 417.899.030 | 139.299.677 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_25_0053_250925 Carpla (4968) | Tổng DSTC thực xuất | 414.791.291 | 138.263.764 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Giá trị HĐ | 297.433.176 | 148.716.588 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Tổng DSTC tiêu chuẩn | 307.285.975 | 153.642.988 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | DS tiêu chuẩn | -12.247.200 | -6.123.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0415_1711KD2.TP-HA (8019) | Tổng DSTC thực xuất | 249.580.135 | 124.790.068 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV3_25_0130_TPSG - VFAG (8079) | Tổng DSTC tiêu chuẩn | 1.317.372.257 | 1.322.348.429 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Giá trị HĐ | 783.357.075 | 261.119.025 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Tổng DSTC tiêu chuẩn | 864.929.908 | 288.309.969 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | DS tiêu chuẩn | 7.193.563 | 2.397.854 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0429_223.CARPLADN (8268) | Tổng DSTC thực xuất | 739.860.873 | 246.620.291 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Giá trị HĐ | 6.944.030.464 | 1.736.007.616 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Tổng DSTC tiêu chuẩn | 7.213.017.536 | 1.803.254.384 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | DS tiêu chuẩn | 96.427.746 | 24.106.936 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_25_0405_026.1125 (8770) | Tổng DSTC thực xuất | 6.961.142.200 | 1.740.285.550 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Giá trị HĐ | 693.532.800 | 173.383.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Tổng DSTC tiêu chuẩn | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | DS tiêu chuẩn | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0173_2811-SALA (8996) | Tổng DSTC thực xuất | 659.188.000 | 164.797.000 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV3_25_0164_112 TPSG - CARPLA (9021) | Tổng DSTC tiêu chuẩn | 363.448.522 | 369.007.522 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_25_0530_512 (9445) | Giá trị HĐ | 6.890.400 | 3.445.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0530_512 (9445) | Tổng DSTC tiêu chuẩn | 8.614.200 | 4.307.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0530_512 (9445) | Tổng DSTC thực xuất | 8.614.200 | 4.307.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_25_0388_01 (9535) | Tổng DSTC tiêu chuẩn | 322.595.787 | 323.214.237 | Dự phòng NULL |
| firm | HĐ_TPE_HN_KD2_25_0573_1512 (10003) | Giá trị HĐ | 4.676.400 | 2.338.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0573_1512 (10003) | Tổng DSTC tiêu chuẩn | 5.758.900 | 2.879.450 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_25_0573_1512 (10003) | Tổng DSTC thực xuất | 5.758.900 | 2.879.450 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Giá trị HĐ | 693.532.800 | 173.383.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Tổng DSTC tiêu chuẩn | 661.715.864 | 165.428.966 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | DS tiêu chuẩn | 661.715.864 | 165.428.966 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV4_25_0209_24122025 (10614) | Tổng DSTC thực xuất | 661.715.864 | 165.428.966 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Giá trị HĐ | 290.785.176 | 145.392.588 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Tổng DSTC tiêu chuẩn | 296.527.073 | 148.263.537 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | DS tiêu chuẩn | 5.532.800 | 2.766.400 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPSG_KV2_26_0003_05012026_HDMB_STPE_HAIAU (11369) | Tổng DSTC thực xuất | 296.527.073 | 148.263.537 | Nhiều hãng xe + Dự phòng NULL |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Giá trị HĐ | 282.717.300 | 94.239.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Tổng DSTC tiêu chuẩn | 345.279.417 | 115.093.139 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | DS tiêu chuẩn | 39.035.865 | 13.011.955 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0024_BLC (11671) | Tổng DSTC thực xuất | 305.116.767 | 101.705.589 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Giá trị HĐ | 26.211.600 | 13.105.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Tổng DSTC tiêu chuẩn | 27.827.800 | 13.913.900 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD3_26_0022_BMWGPBSTB (11697) | Tổng DSTC thực xuất | 21.063.000 | 10.531.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Giá trị HĐ | 24.775.200 | 12.387.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Tổng DSTC tiêu chuẩn | 29.845.200 | 14.922.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0028_HD-LOCTRAN (11743) | Tổng DSTC thực xuất | 29.446.200 | 14.723.100 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Giá trị HĐ | 722.520 | 240.840 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Tổng DSTC tiêu chuẩn | 653.940 | 217.980 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0074_230120261 (12447) | Tổng DSTC thực xuất | 653.940 | 217.980 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0089_KHANHVAN (12681) | Giá trị HĐ | 11.747.592 | 3.915.864 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0089_KHANHVAN (12681) | Tổng DSTC tiêu chuẩn | 11.747.592 | 3.915.864 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0089_KHANHVAN (12681) | Tổng DSTC thực xuất | 11.747.592 | 3.915.864 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Giá trị HĐ | 15.508.800 | 7.754.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Tổng DSTC tiêu chuẩn | 15.966.800 | 7.983.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0155_BWMLongBien (14049) | Tổng DSTC thực xuất | 15.966.800 | 7.983.400 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Giá trị HĐ | 37.584.000 | 18.792.000 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Tổng DSTC tiêu chuẩn | 33.736.400 | 16.868.200 | Nhiều hãng xe |
| firm | HĐ_TPV_MT_KD_26_0154_018 (14053) | Tổng DSTC thực xuất | 33.736.400 | 16.868.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Giá trị HĐ | 6.771.600 | 2.257.200 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Tổng DSTC tiêu chuẩn | 5.956.500 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | DS tiêu chuẩn | 5.956.500 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPSG_KV1_26_0050_303026 (14544) | Tổng DSTC thực xuất | 5.956.500 | 1.985.500 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Giá trị HĐ | 2.916.000 | 972.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Tổng DSTC tiêu chuẩn | 3.207.900 | 1.069.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | DS tiêu chuẩn | 3.207.900 | 1.069.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0279_GeelyDn (14629) | Tổng DSTC thực xuất | 3.207.900 | 1.069.300 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Giá trị HĐ | 453.600 | 151.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Tổng DSTC tiêu chuẩn | 571.200 | 190.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | DS tiêu chuẩn | 571.200 | 190.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0280_GeelyDN2 (14643) | Tổng DSTC thực xuất | 571.200 | 190.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0290_TPE-HA (14813) | Giá trị HĐ | 6.240.000 | 3.120.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0290_TPE-HA (14813) | Tổng DSTC tiêu chuẩn | 5.928.000 | 2.964.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0290_TPE-HA (14813) | DS tiêu chuẩn | 5.928.000 | 2.964.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0290_TPE-HA (14813) | Tổng DSTC thực xuất | 5.928.000 | 2.964.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0224_NHATTAN (15060) | Giá trị HĐ | 8.748.000 | 2.916.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0224_NHATTAN (15060) | Tổng DSTC tiêu chuẩn | 8.748.000 | 2.916.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0224_NHATTAN (15060) | DS tiêu chuẩn | 4.536.000 | 1.512.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0224_NHATTAN (15060) | Tổng DSTC thực xuất | 4.536.000 | 1.512.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Giá trị HĐ | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Tổng DSTC tiêu chuẩn | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | DS tiêu chuẩn | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0313_BoSungL2 (15128) | Tổng DSTC thực xuất | 9.169.200 | 3.056.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Giá trị HĐ | 39.744.000 | 19.872.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Tổng DSTC tiêu chuẩn | 34.960.000 | 17.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | DS tiêu chuẩn | 34.960.000 | 17.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0314_BMWGPMRX (15136) | Tổng DSTC thực xuất | 34.960.000 | 17.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Giá trị HĐ | 12.776.400 | 6.388.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Tổng DSTC tiêu chuẩn | 13.041.600 | 6.520.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | DS tiêu chuẩn | 13.041.600 | 6.520.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0316_BMWGPBD (15138) | Tổng DSTC thực xuất | 13.041.600 | 6.520.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | Giá trị HĐ | 260.928 | 130.464 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | Tổng DSTC tiêu chuẩn | 338.240 | 169.120 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0233_FordBacGiang (15165) | DS tiêu chuẩn | 338.240 | 169.120 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | Giá trị HĐ | 65.599.200 | 32.799.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | Tổng DSTC tiêu chuẩn | 57.281.200 | 28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0121_H13.03.26 (15206) | DS tiêu chuẩn | 57.281.200 | 28.640.600 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0239_13032026 (15243) | Giá trị HĐ | 5.572.800 | 2.786.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0239_13032026 (15243) | Tổng DSTC tiêu chuẩn | 6.501.600 | 3.250.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0239_13032026 (15243) | DS tiêu chuẩn | 6.501.600 | 3.250.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0239_13032026 (15243) | Tổng DSTC thực xuất | 6.501.600 | 3.250.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Giá trị HĐ | 1.296.000 | 432.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Tổng DSTC tiêu chuẩn | 1.224.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | DS tiêu chuẩn | 1.224.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0240_13032026 (15255) | Tổng DSTC thực xuất | 1.224.000 | 408.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Giá trị HĐ | 122.709.600 | 61.354.800 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Tổng DSTC tiêu chuẩn | 111.586.000 | 55.793.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | DS tiêu chuẩn | 111.586.000 | 55.793.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0323_098.KD2.26 (15273) | Tổng DSTC thực xuất | 111.586.000 | 55.793.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Giá trị HĐ | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Tổng DSTC tiêu chuẩn | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | DS tiêu chuẩn | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0253_THACOLS (15370) | Tổng DSTC thực xuất | 11.988.000 | 3.996.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Giá trị HĐ | 3.240.000 | 1.620.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Tổng DSTC tiêu chuẩn | 3.420.000 | 1.710.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | DS tiêu chuẩn | 3.420.000 | 1.710.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0263_LCF (15492) | Tổng DSTC thực xuất | 3.420.000 | 1.710.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Giá trị HĐ | 9.180.000 | 4.590.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Tổng DSTC tiêu chuẩn | 10.210.800 | 5.105.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | DS tiêu chuẩn | 10.210.800 | 5.105.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0351_241 (15581) | Tổng DSTC thực xuất | 10.210.800 | 5.105.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Giá trị HĐ | 3.412.800 | 1.706.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Tổng DSTC tiêu chuẩn | 3.844.400 | 1.922.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | DS tiêu chuẩn | 3.844.400 | 1.922.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD1_26_0265_HD-AN010092 (15595) | Tổng DSTC thực xuất | 3.844.400 | 1.922.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | Giá trị HĐ | 19.250.000 | 9.625.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | Tổng DSTC tiêu chuẩn | 19.530.000 | 9.765.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0362_04.26.kd2 (15656) | DS tiêu chuẩn | 19.530.000 | 9.765.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Giá trị HĐ | 9.374.400 | 4.687.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Tổng DSTC tiêu chuẩn | 10.936.800 | 5.468.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | DS tiêu chuẩn | 10.936.800 | 5.468.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0366_242 (15750) | Tổng DSTC thực xuất | 10.936.800 | 5.468.400 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Giá trị HĐ | 66.960.000 | 33.480.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Tổng DSTC tiêu chuẩn | 58.900.000 | 29.450.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | DS tiêu chuẩn | 58.900.000 | 29.450.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KD2_26_0407_VSMMNH-TPE (16221) | Tổng DSTC thực xuất | 58.900.000 | 29.450.000 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Giá trị HĐ | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Tổng DSTC tiêu chuẩn | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | DS tiêu chuẩn | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| firm | HĐ_TPE_HN_KDXM_26_0153_1 (16270) | Tổng DSTC thực xuất | 5.486.400 | 2.743.200 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_25_0013_HDAIHTINHSCMAQ (531) | Phải thu | (trống) | 5.729.400 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_25_0013_HDAIHTINHSCMAQ (531) | Đã thu | (trống) | 2.268.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_25_0013_HDAIHTINHSCMAQ (531) | Còn nợ | (trống) | 3.461.400 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0080_MITSUVHHN_2210 (1525) | DS theo HĐ | (trống) | 18.668.333 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0080_MITSUVHHN_2210 (1525) | Phải thu | (trống) | 22.933.800 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0080_MITSUVHHN_2210 (1525) | Đã thu | (trống) | 22.933.800 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_25_0056_HDAITHOSCCN (1617) | Thực thu | (trống) | 2.608.168 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_25_0056_HDAITHOSCCN (1617) | Phải thu | (trống) | 2.608.168 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_25_0056_HDAITHOSCCN (1617) | Đã thu | (trống) | 2.608.168 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0060_NT (1648) | Thực thu | (trống) | 1.912.507 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0060_NT (1648) | Phải thu | (trống) | 1.998.907 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0060_NT (1648) | Đã thu | (trống) | 1.998.907 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0087_MGVP_3110 (1697) | Thực thu | (trống) | 1.927.476 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0087_MGVP_3110 (1697) | Phải thu | (trống) | 1.927.476 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_25_0087_MGVP_3110 (1697) | Đã thu | (trống) | 1.927.476 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0081_HDDV-TV (1917) | Thực thu | (trống) | 7.338.125 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0081_HDDV-TV (1917) | Phải thu | (trống) | 7.338.125 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0081_HDDV-TV (1917) | Đã thu | (trống) | 7.338.125 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_25_0057_MERHNSCTB (2552) | Thực thu | (trống) | 10.138.068 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_25_0057_MERHNSCTB (2552) | Phải thu | (trống) | 10.852.164 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_25_0057_MERHNSCTB (2552) | Đã thu | (trống) | 10.138.068 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KDTM_25_0057_MERHNSCTB (2552) | Còn nợ | (trống) | 714.096 | Sổ cái PLBS |
| wr | HDDV_TPSG_SG_CSKH_25_0206_04054 (2583) | Giá trị HĐ | 2.581.202 | 1.290.601 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_25_0206_04054 (2583) | Tổng DSTC tiêu chuẩn | 3.248.802 | 1.624.401 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_25_0206_04054 (2583) | DS tiêu chuẩn | 3.248.802 | 1.624.401 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_25_0206_04054 (2583) | Tổng DSTC thực xuất | 3.248.802 | 1.624.401 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Giá trị HĐ | 129.253.298 | 64.626.649 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Tổng DSTC tiêu chuẩn | 133.636.594 | 66.818.297 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Tổng DSTC thực xuất | 133.636.594 | 66.818.297 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Thực thu | (trống) | 59.262.937 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Phải thu | (trống) | 65.192.137 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_25_0139_SUZUKI (2806) | Đã thu | (trống) | 65.192.137 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_25_0186_CSKH-VELONGBIEN (2854) | Thực thu | (trống) | 6.016.564 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_25_0186_CSKH-VELONGBIEN (2854) | Phải thu | (trống) | 14.621.888 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_25_0186_CSKH-VELONGBIEN (2854) | Đã thu | (trống) | 14.330.288 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_25_0186_CSKH-VELONGBIEN (2854) | Còn nợ | (trống) | 291.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0001_BITCARLB.CA (2908) | Giá trị HĐ | 1.763.208 | 881.604 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0001_BITCARLB.CA (2908) | Tổng DSTC tiêu chuẩn | 2.293.452 | 1.146.726 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0001_BITCARLB.CA (2908) | Tổng DSTC thực xuất | 2.293.452 | 1.146.726 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0005_HDDV (2946) | Giá trị HĐ | 13.072.817 | 6.536.408 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0005_HDDV (2946) | Tổng DSTC tiêu chuẩn | 10.190.779 | 5.095.390 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0005_HDDV (2946) | Tổng DSTC thực xuất | 10.190.779 | 5.095.390 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0002_BMWGPBDPS (2997) | Giá trị HĐ | 27.689.040 | 13.844.520 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0002_BMWGPBDPS (2997) | Tổng DSTC tiêu chuẩn | 36.948.540 | 18.474.270 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0002_BMWGPBDPS (2997) | Tổng DSTC thực xuất | 36.948.540 | 18.474.270 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0011_SCCAU01 (3113) | Thực thu | (trống) | 231.336 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0011_SCCAU01 (3113) | Phải thu | (trống) | 4.999.288 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0011_SCCAU01 (3113) | Đã thu | (trống) | 4.999.288 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0013_VPN (3147) | Giá trị HĐ | 9.157.968 | 4.578.984 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0013_VPN (3147) | Tổng DSTC tiêu chuẩn | 11.674.152 | 5.837.076 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0013_VPN (3147) | Tổng DSTC thực xuất | 11.674.152 | 5.837.076 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0023_DVKTTB.SU-HP (3205) | Giá trị HĐ | 2.938.226 | 1.469.113 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0023_DVKTTB.SU-HP (3205) | Tổng DSTC tiêu chuẩn | 3.223.282 | 1.611.641 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0023_DVKTTB.SU-HP (3205) | Tổng DSTC thực xuất | 3.223.282 | 1.611.641 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0016_03 (3216) | Giá trị HĐ | 7.534.944 | 3.767.472 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0016_03 (3216) | Tổng DSTC tiêu chuẩn | 12.513.744 | 6.256.872 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0016_03 (3216) | Tổng DSTC thực xuất | 11.145.744 | 5.572.872 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0023_HĐDV KIAMAZDA (3281) | Giá trị HĐ | 22.244.544 | 11.122.272 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0023_HĐDV KIAMAZDA (3281) | Tổng DSTC tiêu chuẩn | 31.342.080 | 15.671.040 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0023_HĐDV KIAMAZDA (3281) | DS tiêu chuẩn | 20.052.480 | 10.026.240 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0023_HĐDV KIAMAZDA (3281) | Tổng DSTC thực xuất | 31.342.080 | 15.671.040 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0028_TH.VFXTP (3294) | Giá trị HĐ | 14.861.880 | 4.953.960 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0028_TH.VFXTP (3294) | Tổng DSTC tiêu chuẩn | 16.864.260 | 5.621.420 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0028_TH.VFXTP (3294) | Tổng DSTC thực xuất | 16.864.260 | 5.621.420 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Giá trị HĐ | 12.975.012 | 4.325.004 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Tổng DSTC tiêu chuẩn | 15.803.478 | 5.267.826 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0029_TH.XTP.DVSC.MAYHAN (3296) | Tổng DSTC thực xuất | 15.803.478 | 5.267.826 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0038_05160 (3343) | Giá trị HĐ | 2.570.400 | 642.600 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0038_05160 (3343) | Tổng DSTC tiêu chuẩn | 3.617.600 | 904.400 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0038_05160 (3343) | Tổng DSTC thực xuất | 3.617.600 | 904.400 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0037_KIABACNINH (3388) | Thực thu | (trống) | 4.014.295 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0037_KIABACNINH (3388) | Phải thu | (trống) | 4.014.295 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0037_KIABACNINH (3388) | Đã thu | (trống) | 4.014.295 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Giá trị HĐ | 18.656.795 | 6.218.932 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Tổng DSTC tiêu chuẩn | 30.837.897 | 10.279.299 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Tổng DSTC thực xuất | 8.674.728 | 2.891.576 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Thực thu | (trống) | 3.351.532 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Phải thu | (trống) | 5.344.132 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Đã thu | (trống) | 3.351.532 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0042_KHANHVAN (3444) | Còn nợ | (trống) | 1.992.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Giá trị HĐ | 4.492.079 | 2.246.039 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Tổng DSTC tiêu chuẩn | 5.534.928 | 2.767.464 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | DS tiêu chuẩn | 5.534.928 | 2.767.464 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0042_KMNB26 (3485) | Tổng DSTC thực xuất | 5.534.928 | 2.767.464 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD3_26_0018_HDAIBDPS (3578) | DS theo HĐ | (trống) | 9.421.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0018_HDAIBDPS (3578) | Thực thu | (trống) | 5.299.560 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0018_HDAIBDPS (3578) | Phải thu | (trống) | 15.046.200 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0018_HDAIBDPS (3578) | Đã thu | (trống) | 15.046.200 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0047_VINPN (3633) | Giá trị HĐ | 1.296.000 | 648.000 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0048_SCCAUNANG01 (3660) | DS theo HĐ | (trống) | 1.406.800 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0048_SCCAUNANG01 (3660) | Phải thu | (trống) | 2.713.932 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0048_SCCAUNANG01 (3660) | Đã thu | (trống) | 2.713.932 | Sổ cái PLBS |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Giá trị HĐ | 8.380.800 | 2.095.200 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Tổng DSTC tiêu chuẩn | 12.035.200 | 3.008.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | DS tiêu chuẩn | 8.835.200 | 2.208.800 | Nhiều hãng xe |
| wr | HDDV_TPSG_SG_CSKH_26_0066_05703 (3692) | Tổng DSTC thực xuất | 8.835.200 | 2.208.800 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0056_SC.GDHS-MITSU1.HP (3750) | DS theo HĐ | (trống) | 1.172.600 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0056_SC.GDHS-MITSU1.HP (3750) | Phải thu | (trống) | 1.373.328 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0056_SC.GDHS-MITSU1.HP (3750) | Đã thu | (trống) | 1.373.328 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | Giá trị HĐ | 2.496.679 | 1.248.340 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | Tổng DSTC tiêu chuẩn | 3.203.928 | 1.601.964 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0058_28022026 (3802) | DS tiêu chuẩn | 144.396 | 72.198 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0068_CSKH-DUCHUNGHC (3825) | Giá trị HĐ | 24.101.280 | 12.050.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0068_CSKH-DUCHUNGHC (3825) | Tổng DSTC tiêu chuẩn | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0066_2SLANGSON (3862) | DS theo HĐ | (trống) | 885.560 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0066_2SLANGSON (3862) | Thực thu | (trống) | 1.491.005 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0066_2SLANGSON (3862) | Phải thu | (trống) | 1.491.005 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0066_2SLANGSON (3862) | Đã thu | (trống) | 1.491.005 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0069_HDDV- AD (3868) | DS theo HĐ | (trống) | 791.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0069_HDDV- AD (3868) | Phải thu | (trống) | 2.915.244 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0069_HDDV- AD (3868) | Đã thu | (trống) | 2.915.244 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Giá trị HĐ | 24.101.280 | 12.050.640 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Tổng DSTC tiêu chuẩn | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0071_06.326 (3903) | Tổng DSTC thực xuất | 26.320.320 | 13.160.160 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Giá trị HĐ | 8.858.808 | 4.429.404 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Tổng DSTC tiêu chuẩn | 11.082.960 | 5.541.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | DS tiêu chuẩn | 11.082.960 | 5.541.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0073_09032026 (3929) | Tổng DSTC thực xuất | 11.082.960 | 5.541.480 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0057_705R (3948) | Giá trị HĐ | 4.572.288 | 2.286.144 | 2 dòng HTHT |
| wr | HDDV_TPE_HN_KD2_26_0057_705R (3948) | Tổng DSTC tiêu chuẩn | 5.752.782 | 2.876.391 | 2 dòng HTHT |
| wr | HDDV_TPE_HN_KD2_26_0057_705R (3948) | DS tiêu chuẩn | 5.752.782 | 2.876.391 | 2 dòng HTHT |
| wr | HDDV_TPE_HN_KD2_26_0057_705R (3948) | Tổng DSTC thực xuất | 5.752.782 | 2.876.391 | 2 dòng HTHT |
| wr | HDDV_TPE_HN_KD3_26_0033_HDAILBIENSCPS (3951) | DS theo HĐ | (trống) | 7.268.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0033_HDAILBIENSCPS (3951) | Phải thu | (trống) | 8.659.440 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0033_HDAILBIENSCPS (3951) | Đã thu | (trống) | 8.659.440 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Giá trị HĐ | 1.846.800 | 923.400 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Tổng DSTC tiêu chuẩn | 2.599.200 | 1.299.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | DS tiêu chuẩn | 2.599.200 | 1.299.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0064_SCHOPDK (4005) | Tổng DSTC thực xuất | 2.599.200 | 1.299.600 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0086_CSKH-PHUCTHANHCBDORONG (4083) | DS theo HĐ | (trống) | 1.621.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0086_CSKH-PHUCTHANHCBDORONG (4083) | Phải thu | (trống) | 4.181.004 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0086_CSKH-PHUCTHANHCBDORONG (4083) | Đã thu | (trống) | 1.751.004 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0086_CSKH-PHUCTHANHCBDORONG (4083) | Còn nợ | (trống) | 2.430.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Phải thu | (trống) | 111.721.918 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Đã thu | (trống) | 104.706.398 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0076_DVVOLVO LONG BIÊN (4131) | Còn nợ | (trống) | 7.015.520 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Giá trị HĐ | 11.798.935 | 5.899.468 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Tổng DSTC tiêu chuẩn | 17.577.592 | 8.788.796 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | DS tiêu chuẩn | 7.527.580 | 3.763.790 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Tổng DSTC thực xuất | 12.411.340 | 6.205.670 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Phải thu | (trống) | 5.899.468 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_CSKH_26_0090_CSKH-HYUDAI22APHOT351T (4134) | Đã thu | (trống) | 5.899.468 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0040_TYTHTBDTB (4139) | Phải thu | (trống) | 42.944.310 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0040_TYTHTBDTB (4139) | Đã thu | (trống) | 42.944.310 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0085_SCDAYHOI (4177) | DS theo HĐ | (trống) | 1.842.300 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0085_SCDAYHOI (4177) | Phải thu | (trống) | 3.077.019 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0085_SCDAYHOI (4177) | Đã thu | (trống) | 1.989.684 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0085_SCDAYHOI (4177) | Còn nợ | (trống) | 1.087.335 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Giá trị HĐ | 2.686.975 | 1.343.488 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Tổng DSTC tiêu chuẩn | 2.903.900 | 1.451.950 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | DS tiêu chuẩn | 2.295.900 | 1.147.950 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD2_26_0087_KIAMAZDATB_2003 (4198) | Tổng DSTC thực xuất | 2.295.900 | 1.147.950 | Nhiều hãng xe |
| wr | HDDV_TPE_HN_KD1_26_0091_HD-SCDV-203 (4199) | Phải thu | (trống) | 7.826.544 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD1_26_0091_HD-SCDV-203 (4199) | Còn nợ | (trống) | 7.826.544 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0045_04 (4203) | Thực thu | (trống) | 4.500.000 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0045_04 (4203) | Phải thu | (trống) | 9.472.378 | Sổ cái PLBS |
| wr | HDDV_TPE_HN_KD3_26_0045_04 (4203) | Đã thu | (trống) | 9.472.378 | Sổ cái PLBS |

## 6. Chạy lại sau vòng sửa cuối (10/11/2026)

Sau khi sửa I-1 (lọc một lần ở bước chọn HĐ gốc, PLBS quy về gốc) và `map('intval')`, đã dump lại HRM cho 03/2026, 07/2026, Quý II/2026 (ERP giữ nguyên) rồi chạy lại compare/verify: **số liệu không đổi** so với bảng ở mục 2 (tập HĐ trùng 100%, số HĐ khớp / lệch giải thích được như cũ, 0 lệch không giải thích; riêng firm 1720 vẫn là ca "Dự phòng NULL" đã nêu ở mục 3).
- Ca mới "chỉ PLBS có bút toán 1311 trong kỳ, dòng gốc cộng thêm số của HĐ cha" (design §2.3a, nhãn "Sổ cái PLBS"): **0 ca** ở cả 3 kỳ trên dữ liệu local, nên chỉ được kiểm bằng test feature, chưa đối số với ERP.
