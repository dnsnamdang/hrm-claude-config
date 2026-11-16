# Báo cáo thưởng theo hợp đồng — port ERP → HRM (+ HĐ HRM)

Ngày: 14/11/2026 · Trạng thái: chờ user duyệt · Nhánh: `develop` (hrm-api + hrm-client), làm trong worktree.

## 1. Mục đích

Đưa màn ERP "Báo cáo thưởng theo hợp đồng" (menu Báo cáo thu nhập) sang HRM. Màn chỉ đọc: với mỗi hợp đồng, xem tiền thưởng đã ghi sổ (TK 3351) của từng nhân viên trong kỳ, kèm doanh số tiêu chuẩn. Màn HRM phải ra cùng số với ERP trên DB gộp, và tự nhận hợp đồng bán mới của HRM (`hrm_contracts`) khi HĐ này bắt đầu có bút toán thưởng.

## 2. Quyết định đã chốt (user 14/11/2026)

1. **Gộp cả `hrm_contracts`**: 3 nguồn là HĐ hãng (`firm_contracts`), HĐ dịch vụ (`wr_service_contracts`) và HĐ HRM, hiện trong cùng 1 bảng.
2. **HĐ HRM gộp sẵn, tự lên khi có số**: dùng chung câu truy vấn sổ 3351 với morph `Modules\Assign\Entities\Contract\Contract`.
   - Hiện chưa có bút toán nào của HĐ HRM (prod `hrm_erp_gop`: `hrm_contracts` 0 dòng; dev 2 dòng; không có `account_details` nào mang `contractable_type LIKE 'Modules%'`), nên trên thực tế chưa có dòng nào hiện ra.
   - Doanh số tiêu chuẩn của HĐ HRM = 0.
3. **Phạm vi quyền bám ERP 1:1** (14/11): cấp Công ty theo công ty hồ sơ, cấp Bộ phận chỉ bộ phận của mình. Khác 2 báo cáo HRM đã port, đây là cố ý.
4. **Bám ERP 1:1, chỗ lệch thì ghi chú**:
   - Số liệu, cột, bộ lọc, sắp xếp, In, Excel giống ERP.
   - Lỗi rõ ràng thì sửa ở HRM, ERP giữ nguyên, và ghi vào §6 để QA đối chiếu.
   - Các điểm "lạ nhưng có thể là ý đồ" giữ như ERP.

## 3. Mục tiêu / Không làm / Phản mục tiêu

**Làm**
- API, màn báo cáo, In, Xuất Excel.
- Nối menu vào placeholder "Thưởng theo hợp đồng" ở `hrm-client/components/subsystem-menu/sale-hub.js:266` (nhóm "Thưởng - Thu nhập").

**Không làm**
- Không sửa ERP.
- Không port popup chi tiết theo nhân viên: ERP có hàm `showDetail` (view `:381`, gọi `report.getDetailByEmployee`) nhưng bảng không có chỗ nào gọi hàm này, tức là code chết.
- Không thêm cột hay bộ lọc ngoài ERP.
- Không tạo bút toán thưởng cho HĐ HRM.

**Phản mục tiêu** (chạy được vẫn là hỏng)
- Số HĐ hãng / HĐ DV lệch ERP ở chỗ không nằm trong §6.
- Người không đủ quyền thấy thưởng của người khác, ở bảng, dòng tổng, In hay Excel.
- HĐ hãng và HĐ DV trùng id bị gộp hoặc lẫn nhân viên của nhau.

## 4. Nguồn ERP

Repo `ERP/TanPhatDev`:
- Routes `web.php:3243-3246`: `/bonus-contract-report`, `/searchData`, `/print`, `/export`. Menu ở `topmenubar.blade.php:742`.
- Controller `ReportController.php:2164-2215`:
  - In: mẫu `report_templates.id = 310` (`ReportTemplate::BAO_CAO_THUONG_THEO_HOP_DONG`), view `print_landscape`, các biến `CHI_TIET` / `NGAY` / `THANG` / `NAM` / `HEADER`.
  - Excel: `BonusBusinessContractReportServiceExport` (FromView), `TITLE` "Báo cáo thưởng theo hợp đồng", `COLSPAN` 10, tên file `bao_cao_thuong_theo_hop_dong.xlsx`.
- Service `app/Services/Reports/BonusBusinessContractReportService.php`: `bonusContractReportSearchData`, `getBonusContract`, `getBonusContractFirmEmpl`, `getBonusContractServiceEmpl`, `filterDate`, `printListData`. Các hàm còn lại không dùng.
- View `resources/views/reports/bonus_contract_report.blade.php`.

## 5. Hành vi (bám ERP)

### Số liệu

Nguồn là `account_details` của TK **3351**. Bỏ các dòng có `invoiceable_type` thuộc BillPayment, BillPaymentAuthorization hoặc ClosingEntry. Mỗi cột = Σ Có (`type = 2`) − Σ Nợ (`type = 1`) theo work:

| Cột | work code |
|---|---|
| Thưởng thực hiện hợp đồng (`diff_employee`) | `TTHHD` |
| Thưởng năng suất tháng (`commission_month`) | `TNST` |
| Thưởng năng suất quý (`commission_quarter`) | `TNSQ` |
| Tiền vận chuyển còn lại (`commission_transport`) | `TVC` |

- Tổng cộng = 4 cột cộng lại.
- Id work tra theo `works.code`, không hard-code.

### Dòng hợp đồng

- Gom theo (`contractable_id`, `contractable_type`, `contractable_code`), như ERP: mã HĐ in ra là `account_details.contractable_code`, không phải mã trên bảng HĐ.
- Bỏ HĐ có cả 4 cột = 0.
- Join **INNER** vào bảng HĐ và `departments` theo `department_id` của HĐ. HĐ không có phòng bị loại khỏi cả bảng lẫn dòng tổng, như ERP.

| Nguồn | Khách hàng | Doanh số tiêu chuẩn (dòng HĐ) | Link |
|---|---|---|---|
| HĐ hãng | mã `customers.code` (live, qua `customer_id`) - tên `firm_contracts.customer_name` (snapshot) | Σ `firm_settlement_contract_detail.commission_sale` với `type = 2`, `contractable_type` = HĐ hãng, không lọc ngày | chi tiết HĐ hãng |
| HĐ DV | `wr_service_contracts.customer_code` - `customer_name` (snapshot) | 0 | chi tiết HĐ DV |
| HĐ HRM | `hrm_contracts.customer_code` - `customer_name` (snapshot, cùng kiểu HĐ DV) | 0 | chi tiết HĐ HRM |

- Lọc Khách hàng theo `customer_id` của HĐ.
- Cột Phòng ban = tên phòng của HĐ.

### Dòng nhân viên dưới mỗi HĐ

- Gom theo `account_details.employee_id` trong đúng HĐ đó, cùng điều kiện, cùng bộ lọc ngày / quyền / tổ chức / NV với dòng HĐ. Bỏ NV có cả 4 cột = 0.
- Hiện `mã - họ tên` và **mã phòng - tên phòng hiện tại** của NV (`employees` → `employee_infos.department_id` → `departments`).
  - Join INNER, nên NV không có phòng không hiện ra, nhưng tiền của NV đó vẫn nằm trong dòng HĐ.
- Doanh số tiêu chuẩn:
  - HĐ hãng: Σ `firm_support_accounting_employees.commission_sale_percent` × (DSTC dòng HĐ) / 100.
    - Chỉ khi `firm_contracts.status = DA_QUYET_TOAN`, `is_main = 1`, contractable là HĐ hãng.
    - Không có thì 0.
  - HĐ DV, HĐ HRM: 0.
- Sắp xếp dòng NV:
  - Theo cùng cột / chiều sắp xếp người dùng chọn.
  - Mặc định mã NV tăng dần.
  - Sau đó theo `employee_id` tăng dần.

### Bảng

- Cột: STT · Hợp đồng · Khách hàng · Phòng ban · 4 cột thưởng · Tổng cộng · Doanh số tiêu chuẩn.
- Dòng HĐ in đậm, STT `n`. Dòng NV đánh số `n.m`.
- Dòng TỔNG CỘNG nằm đầu bảng, cộng trên **toàn bộ HĐ đã lọc**, không chỉ trang đang xem (ERP đã làm vậy).
- Phân trang theo HĐ, 10 HĐ/trang như ERP.
- Sắp xếp được theo 6 cột số. Mặc định Mã HĐ (`contractable_code`) giảm dần, sau đó theo `contractable_id` tăng dần. Sắp xếp chạy trên cả 3 nguồn gộp.

### Bộ lọc

- Từ ngày, Đến ngày: **bắt buộc**, thiếu thì không cho lọc. Áp lên `invoiceable_date_accounting`.
- Công ty, Phòng ban, Bộ phận: lọc theo cột tổ chức trên bút toán.
- Nhân viên: lọc `account_details.employee_id`, nên dòng HĐ chỉ còn số của NV đó.
- Khách hàng.
- Mã HĐ: tìm gần đúng (LIKE).
- Nút Lọc, Làm mới, In, Xuất Excel.

### Phân quyền

- Màn không gate (như ERP), dùng mã `accounting.bao_cao_thuong_theo_hop_dong.view`. Catalog `hrm-api/app/Support/Permissions/Catalog/accounting.php:613`, scopes 1-4: thêm `'hrm'` vào `platforms`, deploy chạy `permission:catalog-sync`.
- Phạm vi lọc trên bút toán (như ERP). Mọi cấp đều OR thêm điều kiện `account_details.employee_id = tôi`:

| Cấp | Điều kiện |
|---|---|
| Tổng công ty | không lọc |
| Công ty | `account_details.company_id` = công ty **hồ sơ** của người xem (`employee_infos.company_id`, như ERP — user chốt 14/11) |
| Phòng ban | `account_details.department_id` ∈ phòng mình quản lý (`employee_manage_departments` lọc theo công ty hồ sơ, như ERP) |
| Bộ phận | `account_details.part_id` = bộ phận của mình (`employee_infos.part_id`, như ERP — user chốt 14/11) |
| Không quyền | chỉ bút toán của chính mình |

- Ô lọc Công ty / Phòng / Bộ phận hiện theo cờ `is_all_company` / `is_company` / `is_department` / `is_part` do API trả về.
- In và Excel đi qua cùng phạm vi đó.

### In / Excel

- **In**: dùng lại mẫu `report_templates.id = 310`, khổ ngang. HEADER lấy theo công ty hồ sơ của người in, như ERP.
- **Excel**:
  - Tiêu đề "Báo cáo thưởng theo hợp đồng", kèm khoảng ngày.
  - Cột như bảng, dòng HĐ in đậm.
  - Ô số là số thật `#,##0`.
  - Tên file `bao_cao_thuong_theo_hop_dong.xlsx`.
  - Xuất toàn bộ HĐ đã lọc, không phân trang. Nếu > 2s thì chia trang theo quy tắc CLAUDE.md.

## 6. Danh sách lệch / quyết định của Claude (user kiểm khi đọc)

Giữ như ERP:
- DSTC dòng NV của HĐ hãng chỉ có khi HĐ đã quyết toán. Dòng HĐ thì lấy từ chi tiết quyết toán `type = 2` mà không xét trạng thái. Hai con số có thể không khớp nhau.
- HĐ không có phòng, và NV không có phòng, bị bỏ khỏi bảng (INNER JOIN). Tiền của NV không phòng vẫn cộng vào dòng HĐ.
- Mã HĐ lấy từ `account_details.contractable_code`, gom cả theo mã. Nếu một HĐ có bút toán mang 2 mã khác nhau thì ra 2 dòng.
- Khách hàng HĐ hãng: mã live, tên snapshot.
- Phạm vi theo cột tổ chức trên **bút toán**, không theo công ty của HĐ hay phòng hiện tại của NV.
- Lọc Nhân viên làm dòng HĐ chỉ còn số của NV đó.
- Phòng của dòng NV là phòng hiện tại, không phải phòng lúc ghi sổ.

HRM chuẩn hoá (không đổi số):
- Bỏ N+1: ERP chạy 1 câu truy vấn NV cho mỗi HĐ. HRM gom 1 câu cho cả trang (và cho cả tập khi In/Excel). Kết quả không đổi.
- Ghép NV vào HĐ theo (`contractable_type`, `contractable_id`), vì có 3 nguồn trùng id.
- Bỏ lọc `year` / `month` của ERP: màn ERP không có ô nào gửi 2 tham số này.

- Dòng NV ghép theo cả (`contractable_type`, `contractable_id`, `contractable_code`) giống dòng HĐ.
  - ERP chỉ lọc theo `contractable_id`, nên một HĐ có 2 mã sẽ lặp tiền NV ở cả 2 dòng.
  - Đã kiểm `hrm_erp_gop` ngày 14/11: không có HĐ nào có 2 mã trên sổ 3351, nên số không đổi.
- Chỉ port `getBonusContract` + 2 hàm NV (`getBonusContractFirmEmpl` / `getBonusContractServiceEmpl`). Các hàm khác trong service ERP (vd `:199`, chỉ xét 3 cột) không dùng.

- Phạm vi Bộ phận khi NV không có bộ phận: ERP thành `part_id IS NULL`, tức thấy mọi bút toán không bộ phận (rò). HRM thay bằng 0, không khớp bút toán nào, nên chỉ còn thấy bút toán của mình. Đây là lệch cố ý, QA đừng báo lệch ERP. (final review 16/11)
- Ngày lọc ở API bắt buộc định dạng `Y-m-d`. ERP nhận cả chuỗi có giờ rồi so sai và trả rỗng mà không báo.

Lỗi ERP sửa ở HRM: chưa phát hiện. Người làm thấy lỗi rõ ràng khi đối số thì sửa ở HRM và bổ sung vào đây.

## 7. HRM — vị trí và khuôn

- FE: `/sale/bonus-contract-report`.
- Khuôn: bám màn đã port **Báo cáo theo dõi thực hiện HĐ** (`/sale/monitor-contract-implement`, `.plans/bao-cao-theo-doi-thuc-hien-hop-dong/`):
  - Service `Modules/Finance/Services/MonitorContractImplement/*`: Scope, RowShape, link HĐ theo nguồn (`MonitorContractReportService::link()`, nguồn ERP thì dùng `ERP_URL`).
  - FE: `V2BaseSmartFilterPanel`, bảng nhóm, In, Excel.
- Màn song song **Báo cáo thưởng theo nhân viên** (`.plans/bc-thuong-theo-nhan-vien/`, session khác, đang brainstorm) đọc cùng sổ 3351 / cùng work. Nếu màn đó code trước, người làm có thể dùng chung phần truy vấn tổng 3351, nhưng không được chờ nó.
- Skill áp dụng: `erp-to-hrm-screen`, `report-styles`, `list-page`, `print-page`, `export-excel`.

## 8. Để người làm tự quyết

- Tên class, route API theo quy ước module Finance.
- Cách union 3 nguồn.
- Index nếu đo thấy chậm.
- Link HĐ hãng / HĐ DV: dùng màn HRM nếu đã port, nếu chưa thì `ERP_URL`.

## 9. Kiểm thử / nghiệm thu

- Đối số HĐ hãng + HĐ DV với ERP trên cùng DB, ít nhất 2 kỳ: tổng, từng HĐ, từng NV, DSTC. Mọi chỗ lệch phải giải thích được bằng §6.
- HĐ HRM: dựng bút toán 3351 giả trong test feature, kiểm dòng HĐ, dòng NV, link, DSTC = 0.
- Test quyền 4 cấp + không quyền + OR "của mình".
- FE kiểm bằng Playwright: lọc, bắt buộc ngày, phân trang, sắp xếp, In, Xuất Excel.
