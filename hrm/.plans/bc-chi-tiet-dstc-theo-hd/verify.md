# Đối chiếu số — Báo cáo chi tiết doanh số tiêu chuẩn theo 1 hợp đồng

Ngày soát: 10/11/2026 · DB local `erp_hrm_check` (cả ERP `TanPhatDev` và `hrm-api` cùng trỏ `127.0.0.1:3306/erp_hrm_check`)
Code: hrm-api `feat/revenue-standard-contract` @ `8cc84cc4e`, hrm-client @ `a5e6aa55d`.

## 1. Đối chiếu HRM với ERP (HĐ hãng + HĐ DV)

### Cách làm
- **ERP**: nạp app ERP chỉ-đọc bằng script, gọi đúng 4 hàm mà `ReportController::revenueStandardContractSearchData`
  gọi (`getDataContract`, `getDataAdditionAnnex`, `getDataAnnex`, `getDataContractReturn`). Mảng quyền truyền vào
  service không dùng tới khi lấy dữ liệu nên kết quả giống hệt API `report/revenue_standard_contract/searchData`.
  - Tổng từng khối lấy bằng hàm ERP `RevenueStandardContractService::getTotalRevenue*`, có trừ dòng "Chi phí dự phòng".
  - Tổng cộng tính như blade `getSumRevenue*`: gốc + PL bổ sung − PL giảm − trả lại.
- **HRM**: gọi `RevenueStandardContractService::build()` với header tra như `resolve()`. Không qua lớp phạm vi,
  vì DB local chưa seed mã quyền nên gọi HTTP sẽ ra 500.
  - Tổng khối lấy từ `RevenueStandardContractPrintTable::blockTotals`, tổng cộng từ `grandTotals`.
    Màn hình và Excel dùng cùng quy tắc này.
- **Phạm vi**: **TOÀN BỘ 21.605 mã HĐ gốc** trên DB local, gồm 15.653 HĐ hãng (`firm_contracts` không có
  `parent_contract_id`) và 5.952 HĐ DV (`wr_service_contracts` không có `parent_id`).
- **So sánh**: so từng dòng của 4 khối, đủ mọi khoá (`object_id … object_type`, gồm `revenue_contract`,
  `revenue_net`, `revenue_standard`), số làm tròn 4 chữ số. Tổng khối và tổng cộng so với sai số 0,01.

### Kết quả
| Hạng mục | Số lượng |
|---|---|
| Mã HĐ đối chiếu | 21.605 |
| Dòng đối chiếu (4 khối) | 143.400 |
| Khối PL bổ sung | 1.106 |
| Khối PL giảm | 1.121 |
| HĐ có khối nhập trả lại | 879 |
| HĐ có tổng DSTC ≠ 0 | 17.656 |
| ERP lỗi 500 | 0 |
| **Lệch (dòng / tổng khối / tổng cộng)** | **0** |

Ví dụ một số mã đã nằm trong tập: `HĐ_TPE_HN_KDTM_25_0009_0408`, `HĐ_TPE_HN_KD2_26_0635_OTOVIVA-TPE`,
`HĐ_TPE_HN_KD1_25_0011_FORDBẮCGIANG-PL`, `HDDV_TPE_HN_KDTM_25_0010_VFGLAMSCCN`, `HDDV_TPE_HN_KD3_25_0041_BMWTLTB`.

Các task trước đã đối chiếu riêng từng nguồn:
- Task 2: 55 mã gốc / PL, 0 lệch.
- Task 3: 1.072 mã trả lại, 0 lệch, và thêm 1 bộ dữ liệu tạm cho nhánh spa trả lại HĐ DV (đã xoá).

### HTHT trùng id giữa HĐ hãng và HĐ mới
2 HĐ hãng có id trùng với id HĐ mới HRM:
- id 13 `HĐ_TPSG_SG_PTTT_25_0001_040825.ĐH.TPSG.SHAT`
- id 15 `HĐ_TPE_TBVLCN_25_0002_NT-04.08.2025`

Mỗi HĐ có 2 dòng `firm_support_accounting` (1 dòng `FirmContract`, 1 dòng HĐ mới):
- **ERP** không lọc `contractable_type`. Trên DB local ERP vẫn ra đúng, chỉ vì dòng `FirmContract` có id nhỏ hơn
  nên `first()` lấy trúng nó.
- **HRM** lọc theo loại nên luôn đúng.

Hiện 2 bên khớp số. Nếu sau này dòng HĐ mới đứng trước, ERP sẽ lấy nhầm, còn HRM vẫn đúng.

### Khác biệt đã chấp nhận (không phải lỗi)
1. Chỗ ERP nổ 500 (chia cho 0 khi base HTHT = 0, hoặc PL giảm có HĐ cha chưa có HTHT) thì HRM hiện 0.
   Trên dữ liệu local không có HĐ nào rơi vào trường hợp này: 0 lỗi ERP trên 21.605 mã.
   Task 3 đã kiểm bằng dữ liệu tạm.
2. Giữ nguyên lỗi ERP để số khớp:
   - Trả lại HĐ hãng đọc `$product->qty`, cột này không tồn tại → tiền trả lại trong spa = 0, `market_cost` chỉ là
     một tỉ lệ.
   - PL giảm HĐ hãng đọc `root_qty` → định mức hàng / giảm giá hàng = 0.
3. Dòng trả lại kiểu ERP lấy nguyên `returned_qty`, không chặn theo SL HĐ (đúng như ERP).
4. HĐ mới HRM không có bản ERP để so. Phần trả lại dùng quy tắc riêng: hàng bộ tính theo bộ đủ, spa trả lại
   chia tỉ lệ theo tiền trả. Xem mục 3.

## 2. HĐ mới HRM với màn "Hỗ trợ hạch toán" (HTHT)

### Cách làm
Gọi `HrmContractSource` qua `RevenueStandardContractService::build()`, rồi so với
`ContractSupportAccountingService::computePreview()` (số của màn HTHT) trên cùng HĐ.

### Kết quả
| HĐ | Dòng | DSTC báo cáo | HTHT `standard_sale` | Khớp |
|---|---|---|---|---|
| `HĐ_TPE_HN_KDTM_26_0001_HTHT-TEST` (id 15, dữ liệu thật) | 3 dòng hàng cha (dòng con BOM `CON-TEST` bị bỏ đúng) | 52.516.352 | 52.516.352 | ✔ |
| `HĐ_TPE_HN_KDTM_26_0001_HTHT-TEST` + 2 dòng dịch vụ tạm (xem ghi chú) | hàng 52.516.352 + dịch vụ 3.300.000 | 55.816.352 | 55.816.352 | ✔ |
| `HĐ_TPE_CTV_NV_26_0001_abc` (id 13, dữ liệu thật) | 4 dòng hàng, chưa có giá tiêu chuẩn | 0 | 0 | ✔ |

Ghi chú:
- Trên DB local không HĐ mới nào có dòng dịch vụ. Để kiểm phần dịch vụ, đã thêm tạm 2 dòng
  `hrm_contract_service_items` (mã `ZZRSC-DV1`: chi phí tính doanh số, SL 2 × 1.500.000; mã `ZZRSC-CP1`: chi phí không
  tính doanh số, 300.000) **trong 1 transaction rồi rollback**. Sau đó đã kiểm: còn 0 dòng `ZZRSC`.
  - Báo cáo cộng cả 2 dòng giống HTHT: HTHT cộng mọi dòng dịch vụ vào DSTC.
- 2 dòng spa của HĐ 15 đọc HTHT đã lưu (lọc đúng loại HĐ mới):
  - "Giảm vượt định mức" = min(3.564.330, 0) = 0.
  - "Chi phí dự phòng" = 0.
  - Khớp `firm_support_accounting` id 21654.

## 3. Số trả lại HĐ mới cần anh soát khi nghiệm thu

ERP không có loại HĐ này nên không có số để đối chiếu. Phần trả lại HĐ mới theo quy tắc mới:
- SL trả cộng từ dòng ĐNXK.
- Hàng bộ chỉ tính bộ đủ.
- Spa trả lại chia tỉ lệ theo tiền trả.

HĐ mới có trả lại trên DB local:
- `HĐ_TPE_CTV_NV_26_0001_abc` (id 13): trả 2 dòng, mỗi dòng SL 1.
  - `TATE-TBTE-05`: 610.000
  - `TATE-TBTE-03`: 260.000
  - Tổng trả lại theo giá HĐ: 870.000. DSTC trả lại = 0 vì HĐ này chưa có giá tiêu chuẩn. Spa trả lại = 0 vì HTHT
    có dự phòng 0.
  - HĐ này chưa thử được trường hợp có DSTC ≠ 0 và hàng bộ. Khi nghiệm thu, anh soát thêm trên 1 HĐ thật có giá
    tiêu chuẩn và có trả hàng bộ.

## Script
Script để ở scratchpad phiên làm việc, không commit:
- `t7/erp_full.php`, `t7/hrm_full.php`: dump 2 bên.
- `t7/cmp_full.py`: so sánh.
- `t7/step2.php`: so với HTHT.
