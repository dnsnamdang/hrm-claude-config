# YCXH — Loại "Xuất bán hàng" (type 14) + chuẩn hoá Lưu nháp

**Người phụ trách:** @namdangit
**Nhánh:** `gop_db` (cả `hrm-api` và `hrm-client`)
**Ngày:** 2026-10-05
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-10-05-ycxh-xuat-ban-hang-type14-design.md`

Màn: HRM **Tạo yêu cầu xuất hàng** (`/finance/product-export-requests/create`).
Redmine: *"[ERP => HRM] Yêu cầu xuất hàng - Tạo mới - Validate khi lưu nháp"*.

## Bối cảnh / Sự cố (2 triệu chứng)

1. Chọn **Loại yêu cầu = "Xuất bán hàng"** rồi lưu → toast đỏ **"Loại yêu cầu không được phép
   tạo."** Mong đợi: lưu được, phiếu vào "Đang tạo" (nháp).
2. **Lưu nháp** vẫn validate quá nhiều trường (Kiểu nhập kho, Gửi đến công ty, Hợp đồng…).
   Mong đợi: lưu nháp chỉ cần chọn **Loại yêu cầu**.

## Nguyên nhân gốc (đã xác định — Phase 1 systematic-debugging)

Cả 2 đều là **thiết kế cố ý** đang xung đột với yêu cầu ticket, không phải lỗi ngẫu nhiên:

- Có **2 danh sách loại** tách biệt:
  - `CREATABLE_TYPE_IDS = [3,6,7,12,18,99,20,21]` — gác cổng `store()`.
  - `DROPDOWN_TYPE_IDS` (14 loại, **có 14**) — đổ vào dropdown FE.
  - → Loại 14 hiện trong dropdown nhưng bị `store()` chặn (422) vì chưa nằm trong `CREATABLE_TYPE_IDS`.
- `rulesForType()` nhánh nháp (`$isDraft`) và `ProductExportRequestForm.validateForm()`
  vẫn bắt buộc HĐ cho loại HĐ (20/21) **kể cả khi nháp**.

## Hướng giải quyết (user chốt: **Hướng B**)

Dựng luồng tạo thật cho loại 14, đồng thời chuẩn hoá quy tắc Lưu nháp. Trích nguyên văn chốt của
user: **"1 ok, 2 chỉ cần chọn loại là được, 3 chỉ chọn loại"** và **"ok"** (duyệt: chỉ 2 check
thiết yếu + không làm loại 15 đợt này).

### A. Quy tắc Lưu nháp thống nhất (status = 3) cho MỌI loại

Nháp chỉ bắt buộc **"Loại yêu cầu"**. Nới cả loại HĐ 20/21 (bỏ ràng buộc `emplement_contract_id`
khi nháp) và loại mới 14. Ràng buộc nguồn (HĐ hãng, HĐ HRM) chỉ áp khi **Gửi duyệt** (status = 2).

### B. Loại 14 "Xuất bán hàng" — luồng tạo đầy đủ

- Nguồn = **HĐ hãng** (`firm_contracts` + `firm_contract_tab_products`), mô phỏng đúng mẫu
  20/21 đang dùng (`contractProductLines()`), đổi sang bảng HĐ hãng.
- Chọn HĐ hãng → tự nạp dòng hàng theo tab + VAT, trừ SL in-flight (3 nguồn) + quỹ cha-con.
- Mở `store()` cho loại 14 (thêm 14 vào `CREATABLE_TYPE_IDS`).

### C. Business-check khi Gửi duyệt (status = 2) cho loại 14 — chỉ 2 check thiết yếu

1. **`canProductExport`** — HĐ hãng còn hiệu lực (status = CO_HIEU_LUC/3) **và** đúng người lập HĐ.
2. **SL-còn-được-xuất** — trừ in-flight 3 nguồn (phiếu YC xuất, phiếu xuất kho, phiếu mượn-bán)
   + quỹ cha-con (parent-child quota).

**Tạm bỏ** 3 check phụ (ghi chú bật lại sau): hạn mức công nợ, lệch giá, support_accounting.

### D. Không làm trong đợt này

- **Loại 15 "Xuất khuyến mại"** — để đợt sau (dùng lại pattern 14).
- 3 check phụ ở mục C.
- Loại 4/16/17/19 còn lại của Hướng B — các đợt sau.

## Quyết định đã chốt

- Nháp = chỉ "Loại yêu cầu" cho mọi loại (gồm 20/21 được nới lỏng + 14 mới).
- Loại 14 lấy nguồn từ `firm_contracts`, không tạo bảng mới (gộp DB — ghi thẳng bảng ERP sẵn có).
- Gửi duyệt loại 14 chỉ 2 check thiết yếu; 3 check phụ skip + để lại TODO trong code.
- Không đụng loại 15 đợt này.

## Verify

- `php -l` sạch các file BE sửa.
- Playwright tại `http://127.0.0.1:3000`: (1) chọn 14 + lưu → vào "Đang tạo", không toast đỏ;
  (2) nháp các loại khác + 20/21 chỉ cần chọn loại; (3) 14 Gửi duyệt chặn đúng khi SL vượt /
  HĐ hết hiệu lực / sai người lập.
