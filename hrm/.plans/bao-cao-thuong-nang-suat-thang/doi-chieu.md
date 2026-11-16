# Đối chiếu ERP trước / sau vá — Báo cáo thưởng năng suất tháng

Nguồn: `CommissionMonthReportService` (worktree ERP, nhánh `feature/bao-cao-thuong-nang-suat-thang`), DB local `erp_hrm_check` (chỉ SELECT), người xem NV 13 (phạm vi Tổng công ty), không lọc phòng/KH.
Đơn vị: đồng. "Trước" = code base 09ac07a86e; "Sau" = code đã vá.

## 1. Tổng cộng

| Kỳ | Chỉ tiêu | Trước | Sau |
|---|---|---:|---:|
| 05/2026 | Thưởng NS tháng | 394,210,939 | 341,125,135 |
| 05/2026 | DS tiêu chuẩn | 36,532,121,526 | 34,163,026,695 |
| Cả năm 2026 | Thưởng NS tháng | 2,955,689,001 | 2,518,065,158 |
| Cả năm 2026 | DS tiêu chuẩn | 269,936,685,493 | 251,086,807,978 |
| Cả năm 2025 (có HĐ 13, 15) | Thưởng NS tháng | 1,954,651,549 | 1,572,992,714 |
| Cả năm 2025 | DS tiêu chuẩn | 182,285,459,297 | 157,586,409,606 |

Thời gian chạy (ERP, 1 lần): 05/2026 26,3s → 2,4s; năm 2026 229,8s → 9,2s; năm 2025 102s → 6,3s (do hết nhân dòng + bỏ quét lọc O(N²)).

## 2. Mục 6A.1 — Phòng có nhiều bộ phận (NV lặp theo số bộ phận)

| Kỳ | Phòng | NV trước | NV sau | Thưởng trước | Thưởng sau | DSTC trước | DSTC sau |
|---|---|---:|---:|---:|---:|---:|---:|
| 05/2026 | 47 (6 bộ phận) | 96 | **16** | 46,019,496 | 7,669,916 | 4,545,158,015 | 769,236,087 |
| 05/2026 | 50 (2 bộ phận) | 6 | 3 | 8,677,180 | 4,338,590 | 504,535,545 | 461,236,419 |
| 05/2026 | 67 (4 bộ phận) | 8 | 2 | 13,863,512 | 3,465,878 | 14,004,565 | 350,114,131 |
| 2026 | 47 | 108 | 18 | 484,465,668 | 80,744,278 | 45,562,895,881 | 8,092,524,459 |

Thưởng sau = thưởng trước ÷ số bộ phận (47: 46,019,496 / 6 = 7,669,916).

## 3. Mục 6A.3 — Join `*_support_accounting` thiếu `contractable_type` (HĐ nhân đôi)

| HĐ | Kỳ | Dòng trước | Dòng sau | Thưởng trước | Thưởng sau | DSTC trước | DSTC sau |
|---|---|---:|---:|---:|---:|---:|---:|
| HĐ hãng 13 | 2025 | 4 | 2 | 40,102 | 20,051 | 4,010,160 | 2,005,080 |
| HĐ hãng 15 | 2025 | 4 | 2 | 49,560 | 24,780 | 4,956,000 | 2,478,000 |
| HĐ DV 3948 | 2026 | 4 | 2 | 57,528 | 28,764 | 28,764 | 2,876,391 |

HĐ 13, 15 không có sổ trong 2026 (sổ nằm ở 09-12/2025) nên đối chiếu ở kỳ 2025. HĐ DV 3948: DSTC tăng ×100 do mục 6A.5 (dưới).

## 4. Mục 6A.5 — Công thức DSTC (chia tỷ lệ → nhân tỷ lệ/100)

Cũ: `tnst_NV / tnst_tổng × (commission_sale / ti_le)`. Mới: `tnst_NV / tnst_tổng × commission_sale × ti_le / 100`.

Ví dụ giả lập (HĐ hãng chưa QT, commission_sale = 1,000,000, tnst NV 10 / tổng 40):

| Tỷ lệ NV | DSTC cũ | DSTC mới | Mới / cũ |
|---|---:|---:|---:|
| 100% | 2,500 | 250,000 | ×100 |
| 50% | 5,000 | 125,000 | ×25 |
| Trưởng phòng (=100) | 2,500 | 250,000 | ×100 |
| Thiếu dòng tỷ lệ | **lỗi** "Trying to get property 'commission_sale_percent' of non-object" | 0 | — |
| Tổng TNST HĐ = 0 | 0 | 0 | — |

**Lưu ý:** brief kỳ vọng "NV 50% có DSTC = ¼ số cũ". Số thực tế KHÔNG ra ¼ vì code cũ chia cho tỷ lệ tính bằng đơn vị phần trăm (50), không phải 0,5. Cũ ở tỷ lệ 100 đã bằng `commission_sale / 100`; công thức mới ở 100 ra đúng `commission_sale`. Vì vậy mọi cặp (HĐ chưa QT / HĐ DV) đều tăng ×100 ở tỷ lệ 100 và ×25 ở tỷ lệ 50. Tỷ số giữa NV 50% và NV 100% trên cùng HĐ: cũ 2 : 1 (đảo), mới 1 : 2 (đúng).

Trong DB local ở 3 kỳ trên KHÔNG có cặp (HĐ hãng chưa QT, NV không phải trưởng phòng, tỷ lệ ≠ 100) nào có DSTC ≠ 0 (HĐ hãng gần như đã quyết toán; `wr_support_accounting_employees` 100% là 100%), nên số thật không có "1 NV 50%" để so; đối chiếu bằng ví dụ giả lập ở trên. Tổng DSTC chỉ giảm nhờ bỏ nhân dòng (6A.1/6A.3) và đổi nhánh đã QT (dưới), phần HĐ DV/chưa QT tăng.

## 5. Mục 6A.6 — Nhánh đã quyết toán

Trước: `[0]` của nhóm không sắp thứ tự (lẫn bản nháp `settlement_contract_id` NULL). Sau: chỉ dòng chính thức (`settlement_contract_id` có giá trị), `id` lớn nhất. Ảnh hưởng nằm trong số tổng ở mục 1. Ví dụ đổi: NV 27 / HĐ 1325 năm 2026 DSTC 125,164,816 → 150,647,042 (chưa tách riêng nguyên nhân dòng nháp hay dòng nhiều bản); phần lớn cặp khác không đổi.

## 6. Các mục không đổi số

6A.2 (quyền): user 34 (Tổng công ty, part_id = 20): trước thấy 0 phòng / 0 NV (bị khóa theo bộ phận), sau thấy 20 phòng / 128 NV. 6A.4 (thiếu dòng tỷ lệ → 0, hết `dd`), 6A.7 (popup 403 ngoài phạm vi), 6A.10 (gom theo type + id), 6A.11 (in rỗng không lỗi), 6A.12 (không còn `groupBy` không aggregate) không đổi số liệu báo cáo ở các kỳ trên.

## Đối số HRM ↔ ERP đã vá (Task 10)

Môi trường: DB `erp_hrm_check` (chỉ SELECT), ERP `wt-bonus-month-erp` (kết quả sau vá, `out-sau-*.json` của Task 8), HRM `wt-bonus-month-api` (đã kiểm `ReflectionClass::getFileName()` nằm trong worktree). Phạm vi Tổng công ty: dùng stub `BonusMonthScope` có `level() = 'all'` (không đăng nhập user). Script: `scratchpad/month-parity/compare.php`.

**Kết quả: 0 lệch ở cả 3 kỳ** (dung sai 0,5 cho từng cặp HĐ-NV, cả TNST lẫn DSTC).

### 1. Tổng cộng (ERP sau vá = HRM `search()` = HRM export-rows)

| Kỳ | DSTC ERP | DSTC HRM | TNST ERP | TNST HRM | Lệch |
|---|---:|---:|---:|---:|---:|
| 05/2026 | 34.163.026.695,11 | 34.163.026.695,11 | 341.125.135 | 341.125.135 | 0 |
| Năm 2026 | 251.086.807.978,04 | 251.086.807.978,04 | 2.518.065.158 | 2.518.065.158 | 0 |
| Năm 2025 | 157.586.409.605,64 | 157.586.409.605,64 | 1.572.992.714 | 1.572.992.714 | 0 |

### 2. Điểm kiểm và toàn bộ cặp

| Kỳ | Số cặp (loại HĐ, HĐ, NV) ERP / HRM | Cặp lệch | Phòng lệch | Phòng 47 DSTC / TNST (khớp) |
|---|---|---:|---:|---|
| 05/2026 | 2.756 / 2.756 | 0 | 0 | 769.236.087,46 / 7.669.916 |
| Năm 2026 | 14.563 / 14.563 | 0 | 0 | 8.092.524.458,74 / 80.744.278 |
| Năm 2025 | 11.103 / 11.103 | 0 | 0 | 7.404.514.083,26 / 73.965.036 |

HĐ điểm kiểm (TNST / DSTC cộng mọi NV, ERP = HRM):

| HĐ | 05/2026 | 2026 | 2025 |
|---|---|---|---|
| Firm 13 | 0 / 0 | 0 / 0 | 20.051 / 2.005.080 |
| Firm 15 | 0 / 0 | 0 / 0 | 24.780 / 2.478.000 |
| WR 3948 | 0 / 0 | 28.764 / 2.876.391 | 0 / 0 |

NV hưởng 50% (cặp có dòng `commission_sale_percent = 50`, DSTC khác 0; ERP = HRM ở mọi cặp): 05/2026 có 4 cặp (vd HĐ 18923, NV 28 và NV 505: TNST 67.716, DSTC 7.695.000), 2026 có 24 cặp (vd HĐ 4109 NV 27: 1.711.442 / 194.482.087,62), 2025 có 34 cặp (vd HĐ 5366 NV 39: 1.550.134 / 176.151.580,01).

### 3. HĐ wr 3948 trùng dòng support_accounting

`wr_support_accounting` có 2 dòng (id 1441, 1442, cùng `commission_sale` = 2.876.391); `wr_support_accounting_employees` có 2 dòng cho NV 83 (id 1581, 1582, cùng 100%). ERP lấy `max(sp.id)` (CommissionMonthReportService dòng 378-381, `orderBy('id')->keyBy` ở dòng 451-455); HRM `BonusMonthDstc::loadSupport` sắp `id` tăng dần, dòng sau ghi đè nên cũng ra id lớn nhất. Hai dòng cùng giá trị nên kết quả không phụ thuộc cách chọn; 2026: DSTC 2.876.391 cả hai phía. Firm không có dòng trùng.

### 4. Thời gian HRM (máy local, DB local)

| Kỳ | `search()` lạnh | `search()` nóng | export-rows (cây đầy đủ) | Mục tiêu |
|---|---:|---:|---:|---|
| 05/2026 | 0,85s | 0,52s | 0,72s | < 15s, đạt |
| Năm 2026 | 3,69s | 2,58s | 2,46s | < 15s, đạt |
| Năm 2025 | 3,64s | 2,32s | 2,52s | < 15s, đạt |

"Lạnh" = lần gọi đầu của tiến trình PHP mới; `export-rows` đo `tree(rows())` + `totals()` (cùng đường với controller, phần dữ liệu `expand` do FE dựng nên không thêm truy vấn).

### 5. Trước / sau vá ERP (Task 8) so với HRM

| Kỳ | ERP trước vá DSTC / TNST | ERP sau vá = HRM DSTC / TNST |
|---|---|---|
| 05/2026 | 36.532.121.525,89 / 394.210.939 | 34.163.026.695,11 / 341.125.135 |
| Năm 2026 | 269.936.685.492,70 / 2.955.689.001 | 251.086.807.978,04 / 2.518.065.158 |
| Năm 2025 | 182.285.459.297,02 / 1.954.651.549 | 157.586.409.605,64 / 1.572.992.714 |
