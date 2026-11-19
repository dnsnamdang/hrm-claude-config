# Design: Port "Hợp đồng bán đầu kỳ" ERP → HRM

- Ngày: 2026-11-04 · User "bỏ qua" phần hỏi → các lựa chọn dưới đây là **quyết định của Claude**, đánh dấu (C).
- Hướng: bám nghiệp vụ ERP 1:1, giao diện theo khuôn HRM (V2Base*).
- Worktree: `HRM/.worktrees/hrm-api-hdbdk` + `HRM/.worktrees/hrm-client-hdbdk`, nhánh `feature/hd-ban-dau-ky` (từ `origin/develop` a982cb60a / 1e675af2e).

## 1. Nguồn ERP (`ERP/TanPhatDev`)
- Route `opening-contracts` (`routes/web.php` 4956–4970), `Accounting/OpeningContractController`, model `App\Model\Accounting\OpeningContract`, request Create/Update, `ExcelImports/OpeningContractImport`, `ExcelExports/OpeningContractExcel`, view `resources/views/accounting/opening_contracts/*`.
- Menu ERP: Kinh doanh → Đơn hàng - hợp đồng → "Hợp đồng bán đầu kỳ" `?type=all`, **không gate quyền**.
- Bảng `opening_contracts` (đã có trên DB gộp, 2.228 dòng): `id, code (text), sign_day (date), customer_id, note (varchar nullable), created_by, updated_by, created_at, updated_at`. Không có company_id/department_id/part_id → phạm vi theo **đơn vị của người tạo** (employees → employee_infos).
- Đang bị tham chiếu: `declare_debt_beginning` (deptable_type = `App\Model\Accounting\OpeningContract`, 1.711 dòng), `account_details` (contractable_type cùng chuỗi, 4.409 dòng), `bill_income_request_details`… → **chuỗi morph giữ nguyên chuỗi class ERP**.

## 2. Bảng nghiệp vụ

| Mục | ERP | HRM |
|---|---|---|
| Danh sách | sort `created_at desc` | giữ; sort được: code, sign_day, created_at, updated_at |
| Cột | STT · Số hợp đồng · Ngày ký · Khách hàng (`code - fullname`) · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật · Hành động | giữ đủ; thêm Ghi chú (ẩn mặc định). Số hợp đồng là `nuxt-link` → chi tiết |
| Lọc | code (text), customer (select-ajax), created_by (nhân viên, gồm nghỉ việc), khoảng Ngày ký, company/department/part (của người tạo) | giữ; tìm nhanh = `Tìm theo số hợp đồng`; khối Công ty → Phòng ban → Bộ phận; Ngày ký `variant: range`. Ô Công ty chỉ hiện khi `meta.is_all_company` |
| Phạm vi (`type=all`) | tổng công ty → tất cả · công ty → thành viên cty mình · phòng ban → thành viên phòng mình · bộ phận → thành viên bộ phận mình · không quyền → của mình | giữ đúng thứ tự ưu tiên. Super Admin = tổng công ty. Đơn vị của người đăng nhập null → fail-closed (chỉ của mình) |
| Nhánh `type≠all` (chỉ của mình) | có nhưng menu không dùng | **không port** (C) — màn luôn chạy nhánh `all` |
| Xem chi tiết (`canView`) | Super Admin · người tạo · tổng công ty · công ty/phòng ban/bộ phận và người tạo là thành viên | giữ 1:1; không xem được → 404 → FE `/pages/extras/404` |
| Tạo | ai cũng tạo được | giữ (không gate quyền) |
| Sửa | ai thấy dòng đều thấy nút; chặn khi đã có `declare_debt_beginning` trỏ tới: "Không được sửa do đã khai báo công nợ đầu kỳ" | `is_can_edit = canView && !đã khai báo công nợ đầu kỳ` (C: thêm điều kiện canView cho route update — ERP không kiểm, đây là lỗ) ; BE chặn ở update (409/422 kèm câu ERP) |
| Xoá | chặn khi có `declare_debt_beginning` ("Không được xóa do đã khai báo công nợ đầu kỳ") hoặc `account_details` contractable ("Không được xóa do đã có hạch toán HĐ bán đầu kỳ"); xoá cứng | `is_can_delete = canView && !có khai báo && !có hạch toán`; BE kiểm lại với đúng 2 câu ERP; xoá cứng |
| Validate | code required + **unique trong công ty** (whereIn created_by = thành viên cty người tạo; update dùng cty của người tạo HĐ, ignore id); sign_day required; customer_id required\|exists | giữ; message unique nghiệp vụ "Đã tồn tại trong công ty" (lang file không có câu này); required/exists dùng lang mặc định |
| Form | Số hợp đồng*, Ngày ký*, Ghi chú; Khách hàng* (popup chọn) + Địa chỉ, SĐT (chỉ đọc) | giữ; khối "Thông tin chung" + "Thông tin khách hàng" (`V2BaseFormSection`); popup chọn KH dùng lại khuôn có sẵn (vd `pages/finance/addition-accounting-requests/components/CustomerSearchModal.vue` hoặc `V2BaseSelectRemote` gọi `assign/customers/search`) |
| Import | xlsx/xls, từ dòng 2; cột A Số HĐ · B Ngày ký (d/m/Y) · C Mã KH · D Tên KH · E Địa chỉ · F SĐT; bỏ dòng trống; A–D bắt buộc; **mã HĐ không được trùng toàn hệ thống**; ngày ký không ở tương lai; KH tìm theo code + status=1; địa chỉ/SĐT nhập thì phải khớp; 1 dòng lỗi → không nhập gì, trả `error_details`; OK: "Import thành công N bản ghi" | giữ nghiệp vụ; UI `V2BaseImportModal` + file mẫu `buildImportTemplate()` (cột A = STT, giữ thứ tự cột ERP sau đó). Nhãn sửa "nhà cung cấp" → "khách hàng" (C: ERP chép nhầm từ import HĐ mua) |
| Xuất Excel | `exportList` `danh_sach_hop_dong_ban_dau_ky.xlsx` | `GET export-rows` + `listExportFile` (FE dựng file), `ExportFieldsModal` |
| In danh sách | template `ReportTemplate::DANH_SACH_HOP_DONG_BAN_DAU_KY` = id **467**, header = công ty người đăng nhập | `ReportPrintPreviewModal` với template 467 — đây là bản in DANH SÁCH, không phải chứng từ → header theo công ty người đăng nhập như ERP (C) |
| Lịch sử | không có | bắt buộc HRM: `catalog_histories` (tạo/sửa/xoá; field code, sign_day, customer, note) + `CatalogHistoryModal` ở danh sách, `SystemInfoSection endpoint-base="catalog-histories"` ở chi tiết |

## 3. Quyết định đã chốt (C)
1. **Phân hệ chính: Bán hàng** (`permissionType` 23). Route FE `/sale/opening-contracts`; mục menu có sẵn `sale-hub.js` nhóm Bán hàng → Khác → "Hợp đồng bán đầu kỳ" đổi thành `{ n, link }`, **không `isShow`** (ERP không gate menu).
2. **4 quyền mới guard api, type 23, group "Hợp đồng bán đầu kỳ"** (tên khác ERP để tránh trùng tên guard web):
   - `Xem tất cả hợp đồng bán đầu kỳ của tổng công ty`
   - `Xem tất cả hợp đồng bán đầu kỳ của công ty`
   - `Xem tất cả hợp đồng bán đầu kỳ của phòng ban`
   - `Xem tất cả hợp đồng bán đầu kỳ của bộ phận`
   Không thêm quyền Thêm/Sửa/Xoá/Import (ERP không có). Không tự gán cho role.
3. BE nằm ở `Modules/Finance` (entity `Entities/Contract/OpeningContract` đã có, đang CHỈ ĐỌC `$guarded=['*']`) → mở ghi: `$fillable` (code, sign_day, customer_id, note, created_by, updated_by), bật timestamps, gán `created_by/updated_by = auth()->id()` ở service (không đổi base class vì entity đang được nhiều service đọc). Phần đọc hiện có giữ nguyên.
4. Mã HĐ: unique form = trong công ty người tạo; import = toàn hệ thống — lệch nhau nhưng **giữ như ERP**.
5. Edit/delete cùng điều kiện ở danh sách và chi tiết (cờ BE `is_can_edit`/`is_can_delete`).
6. `hrm-client/utils/contract-link.js`: `OpeningContract` → `/sale/opening-contracts/${id}`.
7. **#12055 (06/11/2026)**: import chỉ còn 3 cột bắt buộc (Số hợp đồng, Ngày ký, Mã khách hàng), mỗi trường báo lỗi riêng; không còn đọc/so sánh tên KH, địa chỉ, SĐT. Mục này thay phần import 6 cột kiểu ERP ở trên.
8. **#12054 (06/11/2026)**: user chốt Lịch sử ghi chú nhiều dòng hiện Trước/Sau 2 cột, sửa ở `SystemInfoSection` nên áp cho mọi màn có Lịch sử.

## 4. API (prefix `api/v1/finance/opening-contracts`)
| Method | Path | Ghi chú |
|---|---|---|
| GET | `/` | list phân trang; query: keyword(code), code, customer_id, created_by, sign_day_from, sign_day_to, company_id, department_id, part_id, sort_by, sort_direction, page, per_page; `meta.is_all_company` |
| GET | `/export-rows` | như list, trả JSON theo trang (2.000/lượt, trần 5.000) |
| GET | `/print-data` | dữ liệu in danh sách (rows + header công ty) |
| POST | `/import/validate` + `/import` | (hoặc 1 endpoint theo khuôn import màn mẫu) — validate toàn bộ, lỗi → không ghi |
| POST | `/` | tạo |
| GET | `/{id}` | chi tiết (404 khi !canView) |
| PUT | `/{id}` | sửa |
| DELETE | `/{id}` | xoá |

Resource: id, code, sign_day (Y-m-d) + sign_day_text (d/m/Y), customer {id, code, fullname, address, mobile}, customer_text (`code - fullname`), note, created_by_name, created_at_text (d/m/Y H:i), updated_by_name, updated_at_text, is_can_edit, is_can_delete.

## 4b. Lệch so với bản design ban đầu khi triển khai (C)
- In danh sách: endpoint `GET /print` (không phải `/print-data`), template 467 khổ ngang.
- Import: `POST /import/validate` + `POST /import`, payload key `items`.
- Form: 1 khối `V2BaseFormCard` "THÔNG TIN CHUNG" + `CreatorInfoLine`; Khách hàng = `V2BaseSelectRemote` gọi
  `assign/customers/search` (gõ ≥ 2 ký tự); Địa chỉ / SĐT chỉ đọc luôn hiện, tự điền khi chọn khách (#12053).
- Sửa/xoá: chặn bằng middleware route `CheckOpeningContractEditable` (chạy trước FormRequest).

## 4c. Việc sót ở màn khác — ĐÃ SỬA (user đồng ý 04/11)
- `pages/finance/product-export-requests/components/ContractCostModal.vue:204`: link `opening_contract` đổi từ ERP sang `/sale/opening-contracts/{id}` (`to:`).
- Màn BPSQ `pages/finance/bill-productivity-settlement-quarters/index.vue`: lỗi sort (truyền `:sortBy="filters.sort_by"` tên BE trong khi key cột là
  `dateAccounting`/`createdAt` → không sang desc) → thêm computed `tableSortBy` map ngược.

## 5. Không làm
- Không port `getDataForBillIncomeRequest/PaymentRequest/AdjustDeptRequest` (HRM đã có ở service khác).
- Không xoá màn ERP.
