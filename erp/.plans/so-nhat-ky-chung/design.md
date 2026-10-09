# Sổ Nhật ký chung (S03a-DN TT99/2025 — mở rộng cho ERP)

## Mục tiêu
Màn báo cáo **Sổ Nhật ký chung** trong ERP, đọc **generic từ `account_details`**, có xuất Excel đúng mẫu S03a-DN mở rộng.
**Yêu cầu cốt lõi:** thêm loại phiếu mới phát sinh hạch toán → journal **tự lấy đúng dữ liệu, KHÔNG phải sửa lại**.

## Quyết định đã chốt (brainstorming)
1. Đầu ra: **màn báo cáo web** (DataTable server-side + bộ lọc) **+ nút Xuất Excel** đúng mẫu.
2. Phạm vi: **một công ty / một lần** (mặc định công ty user). Hiển thị đủ cột gồm "Công ty" & "GD nội bộ", **chưa** làm hợp nhất/loại trừ nội bộ (để sau).
3. Bộ lọc: Công ty • Từ–Đến ngày (theo **Ngày ghi sổ**) • PB→BP→NV cascading • *nâng cao:* TK, Đối tượng, Dự án, Hợp đồng, Hàng hóa.
4. Nguyên tắc dữ liệu: **Phương án A — journal 100% generic**. Cột nào phiếu chưa ghi → **để trống**. Muốn đầy đủ hơn → sửa ở **phía phiếu** khi ghi `account_details`, KHÔNG đụng journal.
5. Hiển thị: **web = mã + tên**; **Excel = chỉ mã** (khớp mẫu S03a-DN).

## Kiến trúc
- **Bất biến:** journal chỉ đọc `account_details` + join bảng tham chiếu. **Không** có nhánh `if (phiếu loại X)`.
- Thành phần (theo pattern báo cáo kế toán hiện có — "sổ chi tiết"):
  - `app/Http/Controllers/Accounting/GeneralJournalController.php`: `index`, `searchData` (Yajra), `exportExcel`, aggregate tổng Nợ/Có.
  - `resources/views/accounting/general_journal/index.blade.php`: Blade + AngularJS + DataTable server-side.
  - `app/ExcelExports/GeneralJournalExport.php`: mẫu S03a-DN mở rộng.
  - Route nhóm `admin/accounting/general-journal/*` + quyền `Xem sổ nhật ký chung` (middleware `checkPermission`).
  - Menu: nhóm Kế toán.

## Mapping 21 cột ↔ account_details

| # | Cột journal | Nguồn account_details | Ghi chú |
|---|---|---|---|
| 1 | Ngày ghi sổ | `invoiceable_date_accounting` | Mốc lọc chính |
| 2 | Số CT | `invoiceable_code` | Denormalized, phiếu-agnostic |
| 3 | Ngày CT | = Ngày ghi sổ (không có trường riêng) | Phương án A |
| 4 | Diễn giải | `accounting_note` (thường rỗng) | Để trống nếu rỗng |
| 5 | Đã ghi Sổ Cái | luôn ✓ (account_details = đã post) | |
| 6 | STT dòng | số dòng chạy theo kết quả lọc (tính lúc hiển thị) | |
| 7 | Số hiệu TK | `account_id` → accounts (số hiệu + tên) | |
| 8 | Phát sinh Nợ | `money_value` khi `type=1` (TYPE_DEPT) | |
| 9 | Phát sinh Có | `money_value` khi `type=2` (TYPE_HAS) | |
| 10 | Công ty | `company_id` | |
| 11 | Phòng ban | `department_id` | |
| 12 | Bộ phận | `part_id` | |
| 13 | Nhân viên | `employee_id` | |
| 14 | Khoản mục | `service_accounting_item_id` (đa số rỗng) | |
| 15 | Đối tượng | COALESCE `customer_id`/`supplier_id`/`obj_company_id` | |
| 16 | Dự án | (không có trường) → suy từ ProjectContract nếu có, else trống | |
| 17 | Hợp đồng | `contract_id` / `contractable_code` | |
| 18 | Hàng hóa | `product_id` | |
| 19 | Loại tiền tệ | `currency_id` | |
| 20 | Tỷ giá | `exchange_rate` | |
| 21 | GD nội bộ | Y nếu `obj_company_id` ≠ null, else N | |

Thứ tự: Ngày ghi sổ ↑ → theo bút toán (phiếu nguồn `invoiceable_id`) → Nợ trước Có → id.
**STT dòng** = số dòng chạy liên tục theo kết quả đã lọc/sắp xếp (tính lúc hiển thị, không lưu DB).

## Màn hình
- Bộ lọc như trên; PB→BP→NV cascading (select2-ajax).
- Bảng 21 cột (web: mã + tên).
- Chân bảng: **Cộng phát sinh (theo bộ lọc)** = tổng Nợ / tổng Có trên **toàn bộ tập lọc** (query aggregate riêng), + badge **Cân đối Nợ=Có** ✓/✗.

## Xuất Excel
- `GeneralJournalExport` đúng mẫu S03a-DN mở rộng: tiêu đề, Năm, ĐVT, header 3 nhóm gộp (Chuẩn TT99 / Cơ cấu tổ chức / Chiều phân tích), dòng dữ liệu (chỉ **mã**), dòng "Cộng phát sinh", dòng "Cân đối Nợ=Có". Xuất **đúng bộ lọc đang xem**.

## Phân quyền & hiệu năng
- Quyền `Xem sổ nhật ký chung`. Mặc định công ty user; công ty khác nếu có quyền đa công ty.
- `account_details` ~940k dòng → **cần index** `(company_id, invoiceable_date_accounting)`; DataTable **server-side**; tổng Nợ/Có = query aggregate riêng (không cộng theo trang).

## Điều KHÔNG làm ở bản này (YAGNI)
- Hợp nhất đa công ty + loại trừ GD nội bộ (chỉ hiển thị cột, chưa xử lý).
- Lấp cột khuyết bằng cách join ngược phiếu nguồn (vi phạm "no modify").
- Sổ Cái / các sổ khác (chỉ Nhật ký chung).

## Downstream / mở rộng sau
- Bổ sung denormalize `khoản mục`, `dự án`, `diễn giải`, `ngày CT` ở phía từng phiếu khi ghi `account_details` → journal tự đầy đủ hơn mà không sửa journal.
- Giai đoạn 2: hợp nhất + loại trừ nội bộ (dùng cờ GD nội bộ).

---

## Cập nhật theo demo HTML (bản chốt UI/logic — 2026-07-16)

Nguồn: `~/Documents/demo/so-nhat-ky-chung.html` (+ `assets/journal.js`). Demo là mock hoàn chỉnh của màn; phần dưới **chốt lại** mapping + hành vi cho khớp demo, đọc thực tế `account_details` (erp_new).

### Bảng 20 cột (đúng thứ tự demo) ↔ account_details

| # | Cột (tên theo demo) | Nguồn account_details | % có dữ liệu | Ghi chú |
|---|---|---|---|---|
| 1 | STT dòng | (tính lúc render) | — | số dòng chạy theo tập lọc |
| 2 | Ngày ghi sổ | `invoiceable_date_accounting` | 100% | mốc lọc chính |
| 3 | Số CT | `invoiceable_code` | — | |
| 4 | Ngày CT | **KHÔNG có cột riêng** → = Ngày ghi sổ | — | gap Phương án A; muốn tách phải denormalize ở phiếu |
| 5 | Diễn giải | `accounting_note` (fallback `service_name`) | ~60% | |
| 6 | Số hiệu TK | `account_id` → `accounts` (số hiệu + tên) | 100% | |
| 7 | Phát sinh Nợ | `money_value` khi `type=1` (TYPE_DEPT) | — | |
| 8 | Phát sinh Có | `money_value` khi `type=2` (TYPE_HAS) | — | |
| 9 | Công ty | `company_id` | 100% | |
| 10 | Phòng ban | `department_id` | 100% | |
| 11 | Bộ phận | `part_id` | ~3% | đa số trống |
| 12 | Nhân viên | `employee_id` | ~21% | |
| 13 | **Mã phí** | `cost_debt_id` → `cost_debts` (mã + tên; model `CostDebt`, relation `AccountDetail::cost_debt()` sẵn có) | ~0.6% | filter sẵn `where('cost_debt_id',...)` — tái dùng |
| 14 | Đối tượng | COALESCE `customer_id` / `supplier_id` / `obj_company_id` | ~48% | |
| 15 | **Vụ việc** | `work_id` → `works` (mã + tên) | ~23% | thay "Dự án" ở design cũ |
| 16 | Hợp đồng | `contract_id` / `contractable_code` | 60–69% | |
| 17 | Hàng hóa | `product_id` → products | ~12% | |
| 18 | Loại tiền | `currency_id` | 100% | |
| 19 | Tỷ giá | `exchange_rate` | 100% | |
| 20 | GD nội bộ | `obj_company_id` != null → **Y**, else N | 0.1% | dùng để loại trừ khi hợp nhất (giai đoạn 2) |

> Đổi tên so với design gốc: **Khoản mục → "Mã phí"**, **Dự án → "Vụ việc" (`work_id`)**. Cột "Mã phí" hầu như trống trên dữ liệu thật → hiển thị rỗng (không sai, đúng Phương án A).

### Bộ lọc & hành vi (map demo → BE)

- **Kỳ báo cáo** (Cả năm / Quý I–IV / Tháng 1–12 / Tùy chọn): thuần FE, tự set Từ–Đến ngày; BE chỉ nhận `from`/`to` lọc theo `invoiceable_date_accounting`.
- **TK tổng hợp — match prefix**: chọn `331` phải lấy cả `3311/3312/3331...`. BE lọc theo **số hiệu TK** `accounts.number LIKE '<chọn>%'` (không lọc theo `account_id` đơn lẻ).
- **Cascade Công ty→Phòng ban→Bộ phận→Nhân viên**: lọc `company_id`/`department_id`/`part_id`/`employee_id`; FE select2-ajax phân cấp.
- **Nâng cao**: Mã phí, Đối tượng, Khách hàng, Vụ việc, Hợp đồng, Hàng hóa, Loại tiền, GD nội bộ, Đã ghi Sổ Cái, Số tiền từ–đến.
- **Quick search**: LIKE trên `invoiceable_code` + `accounting_note` + số hiệu TK.
- **Số tiền từ–đến**: so với `money_value` (Nợ hoặc Có của dòng).
- **Số lũy kế kỳ trước chuyển sang** (checkbox, kiểu MISA): 1 query aggregate riêng — tổng Nợ/Có các dòng có `invoiceable_date_accounting < from` **thoả mọi filter khác trừ ngày**; render dòng "Số lũy kế kỳ trước" + "Cộng lũy kế từ đầu năm".
- **Đã ghi Sổ Cái**: `account_details` = đã post → luôn ✓. Filter này để tương thích mẫu; mặc định coi tất cả "Đã ghi" (bỏ điều kiện chưa-ghi vì ERP không có khái niệm unposted trong account_details).
- **Cài đặt trường lọc (mặc định/mở rộng)**: thuần FE (localStorage theo user), không đụng BE.

### Chân bảng / tổng
- **Cộng phát sinh (theo bộ lọc)**: tổng Nợ / tổng Có toàn tập lọc (query aggregate riêng, KHÔNG cộng theo trang).
- **Badge Cân đối**: `CÂN ĐỐI` nếu ΣNợ=ΣCó, else `LỆCH <số>`.
- Dòng tổng hiển thị **cả đầu bảng lẫn tfoot** (sticky) như demo.

### In & Excel
- **In sổ S03a-DN**: layout đúng demo (`printSheetHTML`) — 9 cột chuẩn TT99 (Ngày ghi sổ, Số hiệu/Ngày CT, Diễn giải, Đã ghi Sổ Cái ✓, STT dòng, Số hiệu TK đối ứng, Nợ, Có) + hàng "Cộng phát sinh" + khối chữ ký. Hàng A/B/C/D/E/G/H/1/2.
- **Xuất Excel**: mẫu S03a-DN mở rộng (20 cột, header 3 nhóm: Chuẩn TT99 / Cơ cấu tổ chức / Chiều phân tích), chỉ **mã**, theo đúng bộ lọc.

### Chốt khác biệt so với design gốc
1. Vụ việc = `work_id` (không suy từ ProjectContract).
2. Ngày CT không có cột riêng → = Ngày ghi sổ (gap ghi rõ).
3. Thêm: Kỳ báo cáo, TK prefix-match, Số lũy kế kỳ trước, quick search, cài đặt trường lọc, badge cân đối, dòng tổng đầu bảng.
4. "Khoản mục" đổi tên "Mã phí"; thực tế trống.

---

## Đối chiếu "Sổ chi tiết tài khoản" (chốt mapping + TÁI DÙNG — 2026-07-16)

Tham chiếu: `AccountDetailController@searchDataAccountDetailBook` + `App\Services\Reports\AccountDetailReportService` (getBuilder/filter/getData/getTotal/getDeptBegin). Sổ NKC **tái dùng** service này (cùng nguồn `account_details`, cùng join/filter), chỉ khác **select đầy đủ 20 chiều** + hiển thị (không có số dư luỹ kế theo TK).

### Mapping trường (chuẩn theo select của sổ chi tiết)
| Cột NKC | Nguồn (như sổ chi tiết) |
|---|---|
| Nhân viên | `ad.employee_id` → employees → `employee_infos.fullname` |
| Phòng ban | join `departments` trên **`ad.employee_department_id`** (hiển thị); **filter** dùng `ad.department_id` |
| Vụ việc | `ad.work_id` → `works.code` |
| Mã phí | `ad.cost_debt_id` → `cost_debts.code` |
| Đối tượng | `COALESCE(sup.code, cus.code, em_info.code, em_info1.code, pro.code)` (NCC/KH/NV/HH — sup & cus đều bảng `customers`) |
| Diễn giải | sổ chi tiết dùng `COALESCE(pe.note,pi.note,bi.note,bpa.note,bir.note)` (note từ phiếu nguồn qua leftJoin 5 loại). **NKC (Phương án A):** ưu tiên `ad.accounting_note`/`service_name` (generic), có thể enrich bằng cách join giống sổ chi tiết. → chốt: dùng `accounting_note` trước, phiếu-note là tuỳ chọn. |
| TK đối ứng (cột IN S03a-DN) | `account_detail_refs` → `accounts` (`GROUP_CONCAT(ac_ref.identify_number)`) |
| Loại tiền | `ad.currency_id` → `currencies.name` |

### TK tổng hợp (chuẩn hơn LIKE)
Filter TK dùng **cây tài khoản**: `accounts.identify_number_parent` — chọn 331 → lấy các TK con (`identify_number_parent = '331'`) + chính nó, `whereIn(account_id, [...])`. (Không dùng LIKE prefix như đã note trước.)

### Tổng & cân đối
- `getTotal`: `SUM(IF(type=1, money_value_exchange,0))` / `SUM(IF(type=2, ...))` group theo `currency_id`. **Cộng phát sinh** = tổng Nợ / tổng Có (quy đổi `money_value_exchange`). Cân đối = ΣNợ ?= ΣCó.
- **Số lũy kế kỳ trước** = `getDeptBegin` (ΣNợ−ΣCó các dòng `< date_from` cùng filter) — **đã có sẵn**, tái dùng.

### Filter đã có sẵn trong `AccountDetailReportService::filter` (tái dùng nguyên)
date_from/to • company_id • department_id • part_id • account_id (+TK con) • account_ref_id • contract_id • invoice (Số CT LIKE) • currency_id • contract_code • customer_id • supplier_id • work_id • cost_debt_id • money_from/to • type. → NKC gần như chỉ cần thêm **quick-search** gộp + **GD nội bộ** (`obj_company_id`) nếu cần.

### KHÔNG làm (chốt lại theo user)
- **Bỏ Sổ Cái + deep-link** hoàn toàn (ERP không có màn Sổ Cái). Chỉ làm Sổ Nhật ký chung.

---

## Cơ chế "Số CT link về phiếu gốc" — GENERIC (chốt 2026-07-16)

**Yêu cầu:** thêm loại phiếu mới hạch toán → Sổ NKC (a) tự lấy dữ liệu, (b) Số CT tự link về phiếu gốc — **KHÔNG sửa journal**.

### KHÔNG dùng `AccountDetail::getInvoiceableLinkAttribute()` (if-chain)
Accessor `invoiceable_link` sẵn có là **chuỗi `if ($invoiceable_type === X::class) route(...)`** cho ~24 loại. Thêm phiếu mới **phải thêm 1 nhánh elseif** → vi phạm yêu cầu. Sổ chi tiết dùng cái này, nhưng NKC **không copy**.

### Dùng convention `invoiceable->link` (không if theo loại)
- `AccountDetail::invoiceable()` = `morphTo` (có sẵn). Eager-load `with('invoiceable')` (Laravel gom theo type, ~N-type query).
- Cột **Số CT** render: `$row->invoiceable?->link ?: e($row->invoiceable_code)`.
  - `link` = accessor `getLinkAttribute()` trên **chính model phiếu** (convention ERP: `<a href=route(...show, id)>code</a>`). Đã có ở ProductExport, ProductImport, BorrowSell, BillIncome, BillIncomeReport...
  - Model phiếu **chưa** có accessor → trả null → fallback text `invoiceable_code` (không lỗi).
- **Thêm phiếu mới:** chỉ cần model phiếu có `getLinkAttribute()` (việc của phía phiếu, không phải journal) → Số CT tự có link. **Journal 0 thay đổi.**

### Trách nhiệm & backfill
- **Journal (bất biến):** chỉ gọi `invoiceable?->link`. Không biết, không cần biết có bao nhiêu loại phiếu.
- **Phía phiếu:** model morphable nên có `getLinkAttribute()`. Task phụ (incremental, KHÔNG chặn NKC): thêm accessor cho các model còn thiếu (SettlementContract, DeclareDebtBeginning, WrAccountingService, ProductTransfer, ...). Link "đầy dần" mà journal không đổi.
- Ghi rõ trong tài liệu/onboarding: "Tạo loại phiếu hạch toán mới → thêm `getLinkAttribute()` vào model để Số CT trên Sổ NKC click được."

### Hiệu năng
- `with('invoiceable')` gom theo type; nếu nặng, chỉ load cột cần (`id, code` per type) — nhưng accessor `link` cần `id`+`code` nên load 2 cột là đủ. Cân nhắc constrain eager-load.
