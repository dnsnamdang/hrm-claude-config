# Báo cáo chi tiết doanh số tiêu chuẩn theo 1 hợp đồng — port ERP → HRM

Ngày: 2026-11-10 · Nhánh: `develop` (hrm-api + hrm-client)

## 1. Mục đích

Kế toán / quản lý bán hàng gõ **1 mã hợp đồng** và xem từng dòng hàng hoá, dịch vụ đóng góp bao nhiêu
vào **doanh số tiêu chuẩn (DSTC)**: giá bán, giá net, 2 hệ số quy đổi, đơn giá DSTC, doanh số HĐ, doanh số net, DSTC.
Đây là màn đối chiếu số DSTC đi vào thu nhập bán hàng / thưởng. Màn bên ERP đã có, giờ chuyển sang HRM,
và **phải nhận thêm hợp đồng mới của HRM (`hrm_contracts`)**, loại mà ERP chưa biết.

## 2. Nguồn ERP (bám 1:1 với HĐ hãng và HĐ DV bảo hành)

| Thành phần | Vị trí ERP (`ERP/TanPhatDev`) |
|---|---|
| Route | `routes/web.php:3454-3457` `report/revenue_standard_contract` (+ `/searchData`, `/print`, `/export`) |
| Controller | `app/Http/Controllers/ReportController.php:6197-6300` |
| Service | `app/Services/Reports/RevenueStandardContractService.php` (1073 dòng) |
| View | `resources/views/reports/revenue_standard_contract.blade.php` |
| Mẫu in | `report_templates.id = 358` (`ReportTemplate::BAO_CAO_CHI_TIET_DOANH_SO_TIEU_CHUAN_THEO_HOP_DONG`), in ngang, biến `CHI_TIET`, `HOP_DONG`, `HEADER` |
| Menu | Báo cáo → "Báo cáo chi tiết doanh số tiêu chuẩn theo 1 hợp đồng" |

**Bố cục:** 1 ô nhập mã HĐ + nút Lọc / Làm mới / In / Xuất Excel. Kết quả trả về 4 khối,
mỗi khối là danh sách dòng có cùng cột:

STT · Tên hàng/Dịch vụ · Mã hàng · ĐVT · Tính chất hàng hoá · Đơn giá bán · Đơn giá net ·
Hệ số quy đổi giá bán · Hệ số quy đổi tính chất HH · Đơn giá tính DSTC · SL ·
Doanh số theo HĐ · Doanh số net · DSTC. Dòng cuối là Tổng cộng 3 cột doanh số.

1. **Hợp đồng gốc** (`getDataContract`): dòng hàng (`root_quantity > 0`, giá = `LEAST(price, allocated_price)`)
   và dòng chi phí/dịch vụ (`revenue_calculation = 1`), cộng thêm 2 dòng **"Giảm vượt định mức"** (= `min(discount_rate_before_vat, 0)`)
   và **"Chi phí dự phòng"** (= `redundancy_cost`) lấy từ bản Hỗ trợ hạch toán (`createDataSpa`).
2. **Phụ lục bổ sung** (`getDataAdditionAnnex`): mỗi PL bổ sung (`type = PL_BO_SUNG`, cha = HĐ gõ vào) là một khối giống HĐ gốc.
3. **Phụ lục giảm** (`getDataAnnex`): mỗi PL giảm là một khối, 2 dòng spa tính lại theo tỉ lệ của HĐ cha.
4. **Nhập trả lại** (`getDataContractReturn`): dòng hàng theo `min(qty, returned_qty)` mang số âm, 2 dòng spa theo tỉ lệ.

HĐ hãng (`firm_contracts` + `firm_contract_tab_products` + `firm_contract_costs`) và HĐ DV bảo hành
(`wr_service_contracts` + 6 bảng dòng) **port giữ nguyên công thức**. HRM đã chung DB nên đọc thẳng các bảng ERP này,
giống cách port Bảng tổng hợp thu nhập bán hàng (`Modules/Finance/Services/SalesIncome/*`).

## 3. Hợp đồng mới HRM (`hrm_contracts`): quyết định đã chốt

| # | Vấn đề | Chốt |
|---|---|---|
| Q1 | HĐ mới hiện ra sao | **Bố cục giống HĐ hãng ERP** (cùng cột, cùng khối) |
| Q2 | Dòng dịch vụ (`hrm_contract_service_items`) chưa lưu đơn giá DSTC | **Giống màn Hỗ trợ hạch toán**: DSTC = giá báo × SL (`ContractSupportAccountingService.php:116`, `:395` dùng `standard_price ?? quoted_price`) để 2 màn khớp số |
| Q3 | Nhập trả lại | Hiện **số âm** trừ vào tổng như HĐ hãng. **Nguồn SL = cộng `product_export_request_tab_products.returned_qty` theo `emplement_contract_id`** (Q5) |
| Q4 | Phạm vi quyền | **Chặn theo phạm vi** (khác ERP, xem §4) |
| Q5 | Nguồn SL trả lại HĐ mới | **Cộng từ dòng phiếu ĐNXK**, vì `hrm_contract_product_prices.returned_qty` hiện chưa được luồng kho HRM ghi (`HandoverContractSourceService.php:22`); luồng nhập trả ghi vào `product_export_request_tab_products` (`ProductImportService.php:1407-1424`) |
| Q6 | Cơ sở phạm vi phòng/bộ phận | **Phòng/bộ phận lưu trên HĐ** (`company_id`/`department_id`/`part_id`), xem §4 |

Dữ liệu HĐ mới:

- **Dòng hàng** `hrm_contract_product_prices` (`contract_id`) đã lưu snapshot `net_price`, `standard_price`,
  `sale_max_percent`, `quoted_price`, `unit_price_after_discount`, `extra_price`, `qty_needed`, `returned_qty`
  (công thức tại `Modules/Assign/Services/ContractService.php:1443-1460`:
  `standard_price = min(round(sau giảm + vượt trội), net) × G × H`).
  - Doanh số HĐ = SL × giá sau giảm (tương ứng `LEAST(price, allocated_price)` của ERP). **Builder chọn cột đúng nghĩa và ghi rõ trong code.**
  - Doanh số net = SL × `net_price`; DSTC = SL × `standard_price`.
  - **2 cột hệ số** chưa lưu trên dòng. Hiển thị bằng cách **tính lại khi xem**:
    G = hệ số loại giá của HĐ (cùng nguồn `$priceTypeCoef` trong ContractService),
    H = hệ số tính chất hàng hoá theo cây `product_natures` (`ProductNatureDstcCoefficient::forProducts`).
    Hệ số chỉ để hiển thị; DSTC luôn lấy `standard_price` đã lưu, không tính lại.
  - Cột "Tính chất hàng hoá" hiện tên nút `product_natures` (không dùng enum cũ `products.product_type`).
  - Dòng cha/con BOM (`parent_id`, `show_children`): **builder xem HĐ mới lưu giá ở dòng nào rồi chỉ lấy dòng mang giá**, để không cộng trùng.
- **Dòng dịch vụ** `hrm_contract_service_items`: giá = `unit_price_after_discount`, net/DSTC theo Q2, hệ số để trống.
  **Lấy đúng tập dòng mà màn Hỗ trợ hạch toán đang cộng** (`ContractSupportAccountingService.php:105-117`, `:395`),
  kể cả dòng chi phí không có cờ tính doanh số, để 2 màn khớp số. *(Quyết định của Claude, theo Q2; khác ERP vốn lọc `revenue_calculation = 1`.)*
- **2 dòng spa**: bản HTHT của HĐ mới nằm ở bảng chung `firm_support_accounting` với
  `contractable_type = Modules\Assign\Entities\Contract\Contract` (`Modules/Assign/Entities/Contract/SupportAccounting.php`).
  Lấy `discount_rate_before_vat`, `redundancy_cost` như ERP.
- **Phụ lục**: HĐ mới không có phụ lục, nên 2 khối PL rỗng.
- **Nhập trả lại** (Q5): SL trả = Σ `product_export_request_tab_products.returned_qty` của các phiếu ĐNXK gắn HĐ
  (`emplement_contract_id` = id HĐ mới; builder xác nhận cột phân biệt loại HĐ để không lẫn id HĐ hãng),
  ghép về dòng `hrm_contract_product_prices` theo hàng (`product_id` ↔ `erp_product_id`) + `unit_id`.
  Dòng hiện SL = `min(qty_needed, SL trả)` với đơn giá của dòng HĐ. Hàng bộ cha/con: ghép vào dòng mang giá (như mục dòng hàng).
  2 dòng spa theo đúng **dạng** công thức nhánh HĐ hãng ERP (`RevenueStandardContractService.php:178-235`).
  Trường thay thế lấy theo **đúng các trường màn Hỗ trợ hạch toán HĐ mới đang dùng** cho cùng khái niệm
  (vd `total_market_costs` ↔ `sales_bonus` ở `ContractSupportAccountingService.php:154-158`; giá sau phân bổ ↔
  `unit_price_after_discount` / `allocated_discount_amount`). Builder ghi bảng ánh xạ trong code.
  *(Quyết định của Claude; ERP không có số để đối chiếu, nên anh cần soát số trả lại của 1 HĐ mới thật khi nghiệm thu.)*

**Bẫy phải xử lý:**

- ERP `getDataSupportAccounting` join `fsa.contractable_id = fc.id` **không lọc `contractable_type`**.
  Chỉ HĐ hãng và HĐ mới dùng chung bảng `firm_support_accounting`, nên id HĐ mới có thể trùng id HĐ hãng và lấy nhầm HTHT.
  **Bản HRM lọc `contractable_type` ở bảng `firm_support_accounting`** (HĐ DV đọc bảng riêng `wr_support_accounting`, giữ như ERP).
- Tra theo mã:
  - **HĐ hãng + HĐ DV giữ nguyên hành vi ERP.** `getData($code)` gộp dòng của cả 2 loại theo mã, HTHT lấy `firm ?? wr`.
    Như vậy số HRM = số ERP kể cả trường hợp hiếm là mã trùng ở 2 bảng.
  - **HĐ mới** chỉ dùng khi mã không có ở HĐ hãng/HĐ DV. Mã trùng giữa HĐ mới và HĐ ERP thì ưu tiên HĐ ERP, ghi log cảnh báo.
    *(Quyết định của Claude.)*
  - Không tìm thấy thì báo "Không tìm thấy hợp đồng".

## 4. Phân quyền

- Mã quyền: `sale.bao_cao_chi_tiet_doanh_so_tieu_chuan_theo_1_hop_dong.view`, đã có ở
  `hrm-api/app/Support/Permissions/Catalog/sale.php:789`, scopes `[1,2,3,4]`. **Đổi `platforms` thành `['erp','hrm']`.**
  Không seeder, không migration quyền.
- Kiểm bằng `CurrentPermission::scope(code)`. `null` = không có quyền thì vào màn bị chặn (403).
- **Khác ERP (cố ý):** ERP đọc scope nhưng không dùng. HRM **chặn theo phạm vi**, xét theo
  **`company_id` / `department_id` / `part_id` lưu trên HĐ gõ vào** (Q6; cả 3 bảng HĐ đều có 3 cột này):
  - 4 Tập đoàn: mọi HĐ.
  - 3 Công ty: `company_id` HĐ = công ty hiện tại.
  - 2 Phòng ban: `department_id` HĐ thuộc các phòng mình quản lý (`listManageDepartmentIds()`, cùng nghĩa với `SalesIncomeScope`).
  - 1 Bộ phận: `part_id` HĐ thuộc các bộ phận mình quản lý, **gồm bộ phận của chính mình** (như fix `e08285357`).
  - Luôn xem được HĐ do mình lập (`created_by`).
  - HĐ ngoài phạm vi thì báo "Bạn không có quyền xem hợp đồng này" (403), không lộ số liệu.
  - Tái dùng cách lấy danh sách phòng/bộ phận quản lý của `SalesIncomeScope`. Cột so khác: ở đây là cột tổ chức trên HĐ,
    không phải NV hưởng thu nhập.
- Phạm vi xét trên **HĐ gõ vào**. Phụ lục và trả lại đi theo HĐ cha.

## 5. HRM: chỗ đặt

- **API** (hrm-api, module Finance, cạnh SalesIncome):
  `GET /sale/revenue-standard-contract?contract_code=` → JSON `{contract, addition_annexs, annexs, returns}` giống ERP;
  `/print` → HTML từ mẫu 358; `/export` → Excel giống ERP.
- **Client** (hrm-client): `pages/sale/revenue-standard-contract/index.vue`, menu cạnh "Bảng tổng hợp thu nhập từ bán hàng"
  trong `components/subsystem-menu/sale-hub.js` (và `finance.js` nếu thu nhập bán hàng có ở đó).
  Theo pattern V2Base / `docs/shared.md`, giao diện cùng kiểu màn thu nhập bán hàng.
- Bộ lọc: ô nhập mã HĐ (gõ tay như ERP; **builder được phép** thêm gợi ý mã nếu đã có component sẵn).

## 6. Mục tiêu / không làm / thất bại

- **Mục tiêu:** cùng 1 HĐ hãng/DV thì số HRM = số ERP từng dòng. HĐ mới hiện đủ dòng, DSTC dòng hàng = `standard_price × SL`,
  khớp màn Hỗ trợ hạch toán của HĐ đó.
- **Không làm:** không sửa ERP; không thêm cột hệ số vào `hrm_contract_*`; không làm DSTC chuẩn cho dịch vụ HĐ mới;
  không đổi công thức ERP (kể cả chỗ khó hiểu như `market_cost` chia tỉ lệ ở nhánh trả lại).
- **Coi là hỏng dù chạy được:** số HĐ hãng lệch ERP; lấy nhầm HTHT do trùng id; người phạm vi thấp xem được HĐ công ty khác.

## 7. Kiểm thử

- Feature test hrm-api (DatabaseTransactions, DB local; gán quyền theo kiểu trait `GrantsSalesIncomeScope`):
  1 HĐ hãng, 1 HĐ DV, 1 HĐ mới có dòng ĐNXK `returned_qty > 0`; 4 mức phạm vi + không quyền + HĐ tự lập;
  trùng id HTHT giữa HĐ hãng và HĐ mới; mã trùng giữa HĐ ERP và HĐ mới.
- Đối chiếu tay: chọn 1 HĐ hãng thật trên DB local, so JSON HRM với `revenueStandardContractSearchData` ERP.

## 8. Để builder tự quyết

Cấu trúc class / tách service; tên route cụ thể; chọn đúng cột "giá HĐ" cho dòng HĐ mới; xử lý dòng BOM cha/con;
gợi ý mã HĐ; định dạng file Excel (bám ERP).
