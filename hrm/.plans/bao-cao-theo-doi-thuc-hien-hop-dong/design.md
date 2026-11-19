# Báo cáo theo dõi thực hiện hợp đồng — port ERP → HRM (+ HĐ HRM)

Ngày: 10/11/2026. Nhánh: `develop` (hrm-api + hrm-client). Nguồn ERP: `ERP/TanPhatDev/app/Services/Reports/MonitorContractImplementService.php`, `ReportController@monitorContractImplement*` (dòng 5864-6005), view `reports/monitor_contract_implement.blade.php`.
Recon chi tiết (công thức từng cột, dòng code ERP): `recon.md` cùng thư mục.

## 1. Mục đích

Kinh doanh và quản lý theo dõi từng hợp đồng bán: giá trị HĐ, doanh số đã xuất trong kỳ (theo HĐ và theo tiêu chuẩn), tiền thực thu trong kỳ, tổng DSTC của HĐ và công nợ. HRM đã có HĐ bán riêng (`hrm_contracts`) nên màn HRM phải theo dõi được cả HĐ HRM, không chỉ HĐ cũ của ERP.

## 2. Quyết định đã chốt (user 10/11/2026)

1. **Gộp chung 1 bảng**: 3 nguồn — HĐ hãng (`firm_contracts`), HĐ dịch vụ (`wr_service_contracts`), HĐ HRM (`hrm_contracts`) — mỗi HĐ 1 dòng, cùng bộ cột.
2. **Màn giống hệt ERP**: cột, bộ lọc, In, Xuất Excel, phân quyền 4 cấp theo mã `sale.bao_cao_theo_doi_thuc_hien_hop_dong.view`. Chỉ thêm HĐ HRM.
3. **Sửa ở HRM các lỗi ERP** (ERP giữ nguyên; số HRM lệch ERP đúng ở các chỗ này, phải ghi danh sách lệch để QA đối chiếu):
   - HĐ cha có phụ lục bổ sung: các số lấy từ sổ cái (`revenue_contract`, `income_money`, `income`, `incomed`) phải SUM cả HĐ cha lẫn phụ lục (ERP lấy 1 dòng bất kỳ).
   - Khách có nhiều hãng xe: không được nhân bản giá trị; cột Hãng hiện đủ các hãng (nối chuỗi).
   - Dòng tổng phòng / NV tính trên toàn bộ dữ liệu lọc, không chỉ trang đang xem.
   - HĐ dịch vụ: chuỗi `ServiceAccounting` gõ dính (ERP SVC:836) → Có `App\Model\Sale\ServiceAccounting` phải được trừ khỏi Phải thu.
4. **DSTC "Thực xuất" của HĐ HRM tính trực tiếp từ chứng từ** (phiếu xuất + bán mượn − nhập trả lại) × `standard_price` dòng HĐ. KHÔNG đọc `hrm_contract_product_prices.exported_qty` (cột này không tăng khi PXK loại 21 hoàn tất) và KHÔNG sửa luồng xuất.
5. **Dịch vụ trong HĐ HRM = 0** ở mọi cột DSTC (`hrm_contract_service_items` không có giá tiêu chuẩn).
6. **Tỉnh/TP và Hãng của HĐ HRM lấy theo khách hàng**: tỉnh = `customers.province_id`, hãng = hãng xe của khách (`customer_has_vehicle_manufacts`), bộ lọc Tỉnh / Hãng chạy chung cho cả 3 nguồn.

## 3. Mục tiêu / không làm

- Làm: API + màn danh sách báo cáo + In + Xuất Excel, nối menu `sale-hub.js:265` (dòng placeholder "Theo dõi thực hiện hợp đồng").
- Không làm: sửa ERP; sửa luồng xuất kho HRM; thêm giá tiêu chuẩn cho dịch vụ; thêm tỉnh giao hàng cho báo giá HRM.
- Không được: số liệu 2 nguồn cũ lệch ERP ở chỗ KHÔNG nằm trong mục 2.3 — ngoài các lỗi đã chốt sửa, HRM phải ra đúng số ERP.

## 4. Hành vi (bám ERP, xem `recon.md` §1)

**HĐ lên báo cáo**: HĐ có ít nhất một dòng `account_details` TK 1311 (`account_id = 22`) với `invoiceable_date_accounting` trong kỳ. Không lọc trạng thái.
- Firm: `type NOT IN (3,6,10,7,9)`, `created_at > 2023-07-01`, phụ lục bổ sung gộp vào HĐ cha, ĐHNT (type 8) đứng riêng; Giá trị HĐ trừ phụ lục giảm đã duyệt.
- WR: `type != 4`, `created_at > 2023-07-01`, gộp theo `parent_id`, trừ PL giảm.
- HRM: không có type/phụ lục → mỗi HĐ 1 dòng, Giá trị HĐ = `total_after_vat`. Morph class `Modules\Assign\Entities\Contract\Contract`.

**Cột** (firm/wr y ERP trừ chỗ đã chốt sửa; HRM như sau):
| Cột | HĐ HRM |
|---|---|
| Hợp đồng | `hrm_contracts.code`, link màn chi tiết HĐ HRM |
| Khách hàng | `customers` theo `customer_id` (live, như ERP) |
| Tỉnh/TP, Hãng | theo khách hàng (mục 2.6) |
| Giá trị HĐ | `total_after_vat` |
| DS thực xuất – Theo HĐ | công thức sổ cái biến thể **firm**: Σ(Có−Nợ) 511x + 5212 + 5213, + 5211 với work CKHH/CKDV, trong kỳ |
| DS thực xuất – Tiêu chuẩn | trong kỳ (`created_at` phiếu): PXK HĐ HRM hoàn tất + bán mượn hoàn tất − nhập trả lại hoàn tất, × `standard_price`; + dự phòng; dịch vụ 0 |
| Số tiền thực thu trong kỳ | biến thể **firm**: Có (DeclareDebtBeginning, BillAdjustDept, BillIncome, BillIncomeReport) − Nợ (BillPayment, BillPaymentAuthorization) |
| Tổng DSTC – Tiêu chuẩn | Σ `qty_needed × standard_price` dòng hàng + dự phòng (công thức firm, `firm_support_accounting` contractable HĐ HRM); định mức giảm giá còn lại = 0 (HĐ HRM đều sau 01/11/2025) |
| Tổng DSTC – Thực xuất | như DS tiêu chuẩn nhưng **toàn thời gian** (mục 2.4) |
| Công nợ Phải thu / Đã thu / Còn nợ | công thức firm, **lũy kế toàn thời gian** như ERP |

**Nhóm**: phòng của HĐ → người lập HĐ → HĐ; dòng TỔNG CỘNG đầu bảng. Phân trang theo HĐ (30/trang như ERP).

**Bộ lọc**: Công ty / Phòng / Bộ phận / Nhân viên (người lập HĐ) / Khách hàng / Mã HĐ (khớp chính xác) / Từ ngày–Đến ngày (bắt buộc, trừ khi có Mã HĐ) / Tỉnh (nhiều) / Hãng xe (nhiều).

**Phân quyền** (màn không gate, như ERP): mã `sale.bao_cao_theo_doi_thuc_hien_hop_dong.view` (Catalog `sale.php:805`) thêm `'hrm'` vào `platforms`. Mọi cấp đều OR "HĐ do mình lập" (`created_by`):
- Tổng công ty: không lọc. Công ty: `company_id` = công ty đang chọn (`current_company_role`, chuẩn HRM như báo cáo thu nhập bán hàng). Phòng ban: `department_id ∈ listManageDepartmentIds()`. Bộ phận: `part_id ∈` bộ phận của mình ∪ bộ phận quản lý (như đã chốt 09/11 cho báo cáo thu nhập). Không quyền: HĐ mình lập.

## 5. Quyết định của Claude (user kiểm khi đọc)

- Lọc chỉ bằng Mã HĐ (bỏ trống ngày) — ERP hỏng: HRM bỏ điều kiện kỳ khi không có ngày.
- WR thực thu không trừ phiếu chi và doanh thu Theo HĐ chỉ đếm 5 loại chứng từ: **giữ như ERP** (không chắc là lỗi, không nằm trong danh sách đã chốt sửa).
- Công nợ không trừ nhập trả lại (`ProductImport` Có 1311) — **giữ như ERP** cho cả 3 nguồn.
- PXK HĐ HRM tính DSTC: chỉ **loại 21** (hàng cha mang `standard_price`); loại 20 (xuất sản xuất hàng con) không tính vì dòng con không có giá tiêu chuẩn. Khớp dòng HĐ qua `product_export_request_tab_products.contract_product_id`, không khớp theo `product_id` (tránh trùng khi 1 SP ở nhiều dòng).
- Xuất Excel điền cả Tỉnh/Hãng ở dòng HĐ (ERP để trống), ô số là số thật `#,##0`.
- Phạm vi công ty theo công ty đang chọn (HRM), không theo công ty hồ sơ (ERP).
- HĐ không có `department_id`: như ERP, không hiện trong bảng nhưng vẫn cộng vào TỔNG CỘNG.
- Dự phòng thiếu dòng `firm_support_accounting` hoặc mẫu số 0: HRM tính dự phòng = 0 (Tổng DSTC vẫn ra số dòng hàng); ERP ra NULL làm trống cả ô. `firm_support_accounting` khớp thêm `contractable_type` (ERP chỉ khớp id, có thể khớp chéo loại HĐ).
- Dòng tổng phòng / NV trên mỗi trang = tổng của cả phòng / NV đó trên toàn bộ dữ liệu đã lọc (hệ quả của mục 2.3).

## 6. Để người làm tự quyết

Cấu trúc service (gợi ý `Modules/Finance/Services/MonitorContractImplement/*`, bám `SalesIncome/*` + `CustomerDebtScope`), cách union 3 nguồn, tối ưu query (báo cáo nặng — đo thời gian, so ERP), cách chia trang xuất Excel theo quy tắc > 2s của CLAUDE.md, link HĐ firm/wr (màn HRM nếu đã port, không thì ERP_URL).

## 7. Kiểm thử / nghiệm thu

- Đối số 2 nguồn cũ với ERP trên `erp_hrm_check` cho vài kỳ; mọi chỗ lệch phải giải thích được bằng mục 2.3.
- HĐ HRM: dữ liệu local mỏng (2 HĐ, chưa có bút toán xuất) → test feature dựng dữ liệu cho từng cột.
- FE kiểm bằng Playwright (lọc, phân trang, In, Xuất Excel).
