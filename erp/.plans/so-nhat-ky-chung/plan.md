# Plan — Sổ Nhật ký chung (S03a-DN, khớp demo HTML)

Design chốt: `design.md` (mục "Cập nhật theo demo HTML"). Đọc `account_details` generic (Phương án A), 20 cột, 1 công ty/lần. Pattern tham chiếu: báo cáo "sổ chi tiết" hiện có.

## Phase 0 — Chuẩn bị / khảo sát  ✅ (đã khảo sát)
- [x] Reference = `AccountDetailController@searchDataAccountDetailBook` + `App\Services\Reports\AccountDetailReportService` (getBuilder/filter/getData/getTotal/getDeptBegin). **NKC tái dùng service này.**
- [x] Mapping chốt theo `getData` của sổ chi tiết (xem design mục "Đối chiếu Sổ chi tiết").
- [x] Nguồn "Mã phí" = `cost_debt_id` → `cost_debts`. Vụ việc=`work_id`. Đối tượng=COALESCE(sup/cus/nv/hh).
- [x] TK tổng hợp = cây tài khoản `accounts.identify_number_parent` (chọn 331 → +TK con), KHÔNG dùng LIKE.
- [x] BỎ Sổ Cái + deep-link (ERP không có màn Sổ Cái).

## Phase 1 — Backend (tái dùng AccountDetailReportService)
- [ ] Tạo `GeneralJournalService` kế thừa/gọi `AccountDetailReportService::getBuilder` + `filter` (đã có sẵn đủ filter). Thêm `getData` **select đầy đủ 20 chiều** (thêm company/part/employee code+name, product, contract, exchange_rate, obj_company_id→GD nội bộ, work, cost_debt, currency, account số hiệu+tên). Thêm quick-search + filter GD nội bộ (`obj_company_id`) nếu cần.
- [ ] `GeneralJournalController@index` — view + init (công ty mặc định user, kỳ = năm hiện tại).
- [ ] `@searchData` — trả data (paginate như sổ chi tiết) + `getTotal` (ΣNợ/ΣCó theo currency, quy đổi `money_value_exchange`) + cờ cân đối.
- [ ] Số lũy kế kỳ trước = tái dùng `getDeptBegin` (ΣNợ−ΣCó dòng `< date_from` cùng filter).
- [ ] STT dòng: đánh số chạy theo tập kết quả.
- [ ] **Số CT link phiếu gốc (GENERIC):** eager-load `with('invoiceable')`; render `$row->invoiceable?->link ?: e(invoiceable_code)`. KHÔNG dùng `getInvoiceableLinkAttribute()` (if-chain). Journal bất biến khi thêm phiếu mới.
- [ ] (Task phụ, incremental — KHÔNG chặn) Backfill `getLinkAttribute()` cho model morphable còn thiếu (SettlementContract, DeclareDebtBeginning, WrAccountingService, ProductTransfer, ...). Ghi convention vào onboarding.
- [ ] STT dòng: đánh số chạy theo tập kết quả (offset DataTable).
- [ ] Route nhóm `admin/accounting/general-journal/*` + `checkPermission:Xem sổ nhật ký chung`.
- [ ] Permission "Xem sổ nhật ký chung" (theo cơ chế quyền ERP) + gán menu nhóm Kế toán.

## Phase 2 — Frontend (Blade + AngularJS + DataTable)
- [ ] `accounting/general_journal/index.blade.php`: header 3 nhóm gộp (TT99 / Cơ cấu tổ chức / Chiều phân tích) + 20 cột (web = mã + tên).
- [ ] Bộ lọc: Kỳ báo cáo (auto set ngày), Từ–Đến, TK, Công ty; cascade PB→BP→NV; khối nâng cao (toggle + badge đếm); quick search + clear; số tiền từ–đến (format nghìn); checkbox lũy kế kỳ trước.
- [ ] Dòng tổng "Cộng phát sinh (theo bộ lọc)" đầu bảng + tfoot (sticky); dòng lũy kế kỳ trước + cộng lũy kế từ đầu năm khi bật.
- [ ] Badge "Cân đối Nợ=Có / LỆCH".
- [ ] Cài đặt trường lọc mặc định/mở rộng lưu localStorage (LÀM — user chốt).
- (BỎ) Deep-link/Sổ Cái — không làm.

## Phase 3 — In & Excel
- [ ] `GeneralJournalExport` (maatwebsite): mẫu S03a-DN mở rộng, chỉ mã, theo bộ lọc; header 3 nhóm + Cộng phát sinh.
- [ ] Modal "In sổ (mẫu S03a-DN)": layout 9 cột chuẩn như demo `printSheetHTML` (hàng A/B/C/D/E/G/H/1/2 + chữ ký).

## Phase 4 — Verify
- [ ] Đối chiếu tổng Nợ = tổng Có trên vài công ty/kỳ (dữ liệu thật).
- [ ] Test filter cascade + TK prefix (331 ra 3311/3331...).
- [ ] Test carry-forward khớp (ΣNợ/ΣCó trước from).
- [ ] Test hiệu năng server-side + index chạy đúng.
- [ ] `php -l` sạch; browser test toàn màn.

## Ghi chú phạm vi (YAGNI — theo design)
- Chưa hợp nhất/loại trừ GD nội bộ (chỉ hiển thị cột GD nội bộ).
- Cột khuyết (Mã phí, Ngày CT, Diễn giải rỗng...) để trống — muốn đầy đủ hơn thì denormalize ở phía phiếu, KHÔNG sửa journal.

## Checkpoint — 2026-07-16 (Phase 1 + FE core DONE)
Vừa hoàn thành:
- **BE:** `app/Services/Reports/GeneralJournalService.php` (getBuilder/filter/getData 20 chiều/getTotal/getCarryForward + `attachInvoiceableLinks` generic link phiếu gốc) — smoke test OK (1139 dòng, link resolve được). `GeneralJournalController` (index+searchData). Route `general-journal.index|searchData`. Quyền 1047/1048 (`addGeneralJournalPermissions()` idempotent, mirror 302/303).
- **FE:** `resources/views/accounting/general_journal/index.blade.php` — bộ lọc (kỳ báo cáo, from-to, cascade qua partial `company-department-filter-singer-js`, TK, nâng cao: mã phí/vụ việc/loại tiền/GD nội bộ/loại BT/số tiền, quick search, checkbox lũy kế), bảng 20 cột (header 3 nhóm), Số CT link (`invoiceable_link` + trustAsHtml), tổng "Cộng phát sinh" + lũy kế kỳ trước + badge cân đối, uib-pagination. Blade compile sạch.
- **Menu:** thêm "Sổ nhật ký chung" (gated quyền) trong topmenubar.
- **Số CT link GENERIC:** dùng `invoiceable->link` (không if theo loại) → thêm phiếu mới không sửa journal.

## Checkpoint — 2026-07-16 (Phase 3 DONE: Excel + In)
- **Excel:** `app/ExcelExports/GeneralJournalExport.php` (FromView) + `general_journal/excel.blade.php` (mẫu S03a-DN mở rộng 20 cột, header 3 nhóm, Cộng phát sinh + cân đối). Route `general-journal.export`.
- **In S03a-DN:** `general_journal/print.blade.php` (9 cột chuẩn A/B/C/D/E/G/H/1/2 + TK đối ứng từ account_detail_refs + Cộng phát sinh + chữ ký, auto window.print). Route `general-journal.print`.
- **FE:** nút "In S03a-DN" + "Xuất Excel" (gửi đúng bộ lọc qua query). `buildQuery()`.
- **UI:** vùng cuộn dọc+ngang `#journal-scroll` (max-height 65vh) + sticky header 2 hàng; cột Diễn giải wrap.
- Verify: lint sạch + render thật (excel 6.8KB, print 5.9KB, 1139 dòng data).

Còn lại (tùy chọn, chưa chặn): "Cài đặt trường lọc" (localStorage). Test browser toàn màn (đặc biệt Excel tải + In).
Blocked: test trên DB chưa gán quyền 1047/1048 cho role user → gán quyền (hoặc super-admin).
