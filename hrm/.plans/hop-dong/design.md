# Hợp đồng bán hàng HRM (tạo từ Báo giá) — Tóm tắt

> Module `Assign` · Màn `/assign/contracts` (menu Sale hub › "Hợp đồng (dự án TKT)")
> Phụ trách: @dnsnamdang (Phase 1–10) · @dangquang / nguyentrancu97 (Phase 11–17)
> Nhánh: `gop_db` (hrm-api + hrm-client); Phase 18–20 trên `gop_db-hop-dong-ban` (chưa commit). Cập nhật tóm tắt: 28/10/2026.
> Spec chi tiết: `design-phase11-firm-fields.md` (Phase 11) · `design-phase18-danh-sach.md` (Phase 18) · `design-phase20-mau-in.md` (Phase 20) · mockup form `mockup-form-hd-gon.html` (Phase 19). Các spec `docs/superpowers/specs/2026-08-1x-hop-dong-*.md`
> mà plan cũ nhắc tới KHÔNG có trong repo tài liệu (chỉ nằm máy người viết).

## 1. Mục tiêu
Chuyển nghiệp vụ HĐ hãng (FirmContract ERP) sang HRM. Gộp 3 loại HĐ ERP (bán/nguyên tắc/dự án) thành
**1 hợp đồng**, tạo **1-1 từ báo giá trúng thầu**. Nguyên tắc xuyên suốt: **khớp ERP** (luồng, validate,
công thức HTHT) trừ khi user chốt khác.

## 2. Quyết định đã chốt (hiệu lực hiện tại)

| Chủ đề | Chốt | Phase |
|---|---|---|
| Nguồn tạo | 1 báo giá trúng thầu (status 7) → 1 HĐ (`quotation_id` UNIQUE); chỉ người lập báo giá được lập | 1, 4 |
| Dòng hàng | Snapshot từ báo giá, đóng băng; chỉ dòng CHA được nhập Doanh số vượt trội + chỉnh giảm giá | 1, 4 |
| Bảng | Prefix `hrm_` (tránh `contracts` ERP). HTHT + phòng thực hiện tái dùng bảng ERP polymorphic (`firm_support_accounting*`, `implement_*`) | 1, 6 |
| Mã HĐ | `HĐ_{mã cty}_{mã phòng}_{yy}_{STT 4 số}_{số HĐ nhập}` như ERP; "Số hợp đồng" bắt buộc | 5c |
| Trường bắt buộc | Số HĐ, TK ngân hàng Bên A (dropdown, không chọn sẵn), người ký + chức vụ, ≥1 đợt thanh toán, các trường Bên B theo loại khách. **Ngày ký KHÔNG bắt buộc** (chỉ có khi xác nhận KH đã ký) | 5d, 9, 10, 11 |
| Bên B | Rẽ nhánh cá nhân / tổ chức; tổ chức chọn người đại diện + TK ngân hàng qua dropdown | 11 |
| Trạng thái | Enum ERP: Đang tạo(3) → Chờ duyệt(2) → **Duyệt = Có hiệu lực(6)** (1 bước, qua màn HTHT) → Thanh lý(10). Không duyệt bắt buộc lý do, về Đang tạo | 6, 15 |
| Hiệu lực | Điều kiện hiệu lực (ký / đặt cọc / bảo lãnh) + thời hạn thực hiện tự tính ngày kết thúc | 7.3 |
| Hạn mức vượt trội | `departments.max_extra_price_percent`; vượt thì chỉ role "Giám đốc" duyệt được | 4 |
| Quyền | Lập: **không cần quyền**. Sửa/Xoá: **không cần quyền**, chỉ người lập + Đang tạo (middleware `contractEditable`). Duyệt/Không duyệt: `Duyệt hợp đồng`. Thanh lý: `Thanh lý hợp đồng`. Còn chặn hàng quá hạn (`dueConfig`, #11722) | 8, 16 |
| HTHT | Chỉ ghi 4 bảng `firm_support_accounting*` (không bút toán). DSTC = min(giá sau giảm + vượt trội, net) × G × H; `sale_max_percent` đọc `product_unit_prices`, giá vốn `product_units.cost_price`; freeze lúc tạo VÀ lúc sửa; không backfill HĐ cũ; hệ số DSTC đọc `company_product_natures`; giá theo công ty chứng từ | 6, 13, 17 |
| Tiến độ thanh toán | Loại thanh toán (Tạm ứng/Đặt cọc/Thanh toán) + điều kiện thanh toán (danh mục `payment_conditions`) + số ngày; lệch tổng chỉ cảnh báo | 5e, 17 |
| Danh sách | Quyền xem chuẩn 4 cấp ("Xem tất cả / theo công ty / phòng ban / bộ phận Hợp đồng bán hàng") + HĐ mình tạo; ẩn "Đang tạo" của người khác ở mọi cấp; 17 ô lọc (5 ô ngày cột phải, Nhóm ngành + Ứng dụng theo dự án TKT, Phòng thực hiện khớp chính + hỗ trợ) | 18 |
| Form Lập/Sửa | 2 khối (Thông tin HĐ · Các bên ký kết, Bên A chỉ đọc) + 6 tab (Chi tiết HĐ · Thực hiện* · Giao hàng* · Điều khoản thanh toán* · Mẫu in* · Đính kèm); bảng Chi tiết HĐ = 1 bảng khuôn Báo giá (A Hàng hoá + B Dịch vụ & Chi phí, nhãn DV/CP theo `costs.revenue_calculation`), Tổng = A + B; "Tổng hợp thanh toán" chiếm 6 cột cuối, ẩn dòng giá trị 0, tách Dịch vụ / Chi phí; ô chỉ đọc không mờ (sửa gốc `V2BaseFloatingField`) | 19 |
| Mẫu in | Mẫu ở màn Mẫu in HRM: loại 7 "Hợp đồng bán hàng" × 3 loại con (Hợp đồng / Phụ lục hàng hoá / Biên bản giao nhận), chép sẵn 26 mẫu ERP giữ tên biến. Lời văn CHÉP vào HĐ (`template`, `template_print_product`, `print_template_id`), sửa riêng từng HĐ; bắt buộc khi Trình duyệt (Lưu nháp không) | 20 |
| Chế độ in | Popup In: hợp đồng (Tổng hợp / Chi tiết theo nhóm) · phụ lục hàng hoá mẫu 1 / mẫu 2 · biên bản giao nhận (chọn mẫu + người giao/nhận). Xem trước `ReportPrintPreviewModal`; letterhead theo `company_id` HĐ; gate phạm vi xem (KHÔNG công khai như ERP) | 20 |
| QR | Status Có hiệu lực / Đang xuất hàng / Đang & Đã quyết toán; QR 12mm trỏ màn Chi tiết HĐ (cần đăng nhập), dựng ở FE (gói `qrcode`) | 20 |
| Ẩn giá | Dùng CHUNG quyền có sẵn "Xem hợp đồng ẩn giá" (như ERP): xem mọi HĐ; HĐ ngoài phạm vi 4 cấp + người lập ⇒ mọi ô tiền `*****` (BE null), ẩn HTHT + Duyệt + In hợp đồng/phụ lục; biên bản in bản KHÔNG giá (vá lỗ ERP); Excel ghi `*****` | 20 |
| Xuất hàng từ HĐ | Nút "Yêu cầu xuất hàng" ở danh sách + chi tiết: CHỈ người lập HĐ + HĐ đủ điều kiện xuất (Có hiệu lực + ngày hiệu lực + thời hạn thực hiện). BE chặn: API tạo YCXH từ HĐ (403), lưu YCXH 20/21 kể cả nháp (422), picker HĐ HRM chỉ HĐ mình lập. Bấm ⇒ màn Tạo YCXH đầy đủ loại 21 nạp sẵn HĐ (`?hrm_contract_id=`). Để sau: điều kiện "hàng chưa xuất hết" | 22 |
| Bố cục YCXH 20/21 | Theo mockup `mockup-ycxh-xuat-ban-hd.html`: Loại (4) · Hợp đồng (8, "mã · Ngày ký · Hạn thực hiện") → KH (8) · MST (4) / Địa chỉ (8) · Người liên hệ "Tên • SĐT" (4) → Hình thức xuất · Kho · Vận chuyển(+km) · Lắp đặt (3×4; Xuất thẳng ⇒ chú thích 6 cột) → Ghi chú bút chì (Chi tiết chỉ hiện khi có). Khối thu gọn được. Bảng 1 hàng tiêu đề, Model · Thương hiệu dòng phụ, icon lùi dòng ở cột Mã, ghim TT sau VAT (bóng khi đang trượt), dòng TỔNG theo dòng tick. Đính kèm sau bảng. Tiêu đề khối giữ chữ thường (V2BaseFormCard). Nhãn 14px / cách ô 8px | 23 |

## 3. Bản đồ code (gop_db)
- **BE `hrm-api/Modules/Assign/`**: `Entities/Contract/*` (Contract + 6 bảng con + Implement* + SupportAccounting*),
  `Services/ContractService.php`, `Services/ContractSupportAccountingService.php`,
  `Http/Controllers/Api/V1/ContractController.php`, `Http/Requests/Contract/*`,
  `Transformers/ContractResource.php` + `DetailContractResource.php`, routes nhóm `/assign/contracts` trong `Routes/api.php`.
- **Migrations** `hrm-api/database/migrations/*hrm_contract*` (08/10 → 23/10) + `2026_10_16_*payment_condition*`.
- **FE `hrm-client/`**: `pages/assign/contracts/{index,create}.vue`, `_id/{index,edit,support-accounting}.vue`,
  `pages/assign/contracts/components/*` (QuotationSearch, Implement, ExportRequest, **ContractPrintModal**, **contractPrintMixin**), `components/ContractPaymentTermsTable.vue`.
- **In (Phase 20)**: `Modules/Assign/Services/ContractPrintService.php`, `Modules/Human/Entities/PrintTemplateVariable.php` (loại 7), `Modules/Assign/Database/Seeders/SaleContractPrintTemplatesSeeder.php`, route `print-templates` + `{id}/print-data`.
- **E2E** (`HRM/e2e/tests/assign/`): `contracts-list.api`, `contracts-hide-price.api`, `contracts-filter`, `contracts-form-layout`.
- **Liên quan**: YCXH loại 21 từ HĐ (feature `gop-db/hop-dong-xuat-hang`), ô chọn HĐ ở form meeting, nút Lập/Xem HĐ ở báo giá.

## 4. Ngoài phạm vi / để sau
Duyệt đa cấp, cảnh báo (mục 7 spec Logic HĐ), Chuyển duyệt BGD + notify, phụ lục (giảm / bổ sung), khối giao hàng
+ tiến độ TT #11252, quyết toán; HTHT cho sửa % phòng; đối chiếu số HTHT với 1 HĐ ERP thật.

## 5. Phase 24 — Bộ 16 trạng thái + duyệt đa cấp (03/11/2026)
Chi tiết: `design-phase24-trang-thai.md`. Trạng thái do code tự chuyển theo nghiệp vụ, user không tự chọn.
- Bước 1: sửa mẫu in ⇒ cờ cần Pháp chế duyệt (+ so chữ "Xem thay đổi", khôi phục mẫu gốc).
- Bước 2: TP (phòng được giao quản lý) → Pháp chế (nếu cờ) → BGĐ (Chuyển duyệt khi dính ĐK y ERP) → Chờ KH ký → Xác nhận KH đã ký (người lập, file + ngày) → Có hiệu lực (đủ ĐK hiệu lực + tới ngày, lệnh lịch). Quyền Duyệt KHÔNG có phạm vi: 3 mã riêng. Thông báo `[HDB]`.
- Bước 3: lập YCXH khi Có hiệu lực / Đang thực hiện; PXK đầu tiên ⇒ Đang thực hiện; thu tiền từ KH đã ký.
- 05/11 (24.7–24.9): Hết hiệu lực (lệnh 00:20 quá ngày kết thúc thực hiện) · Hủy duyệt / Đóng HĐ (Chờ KH ký, lý do bắt buộc) · Đang thực hiện khi thu tiền / mượn bán đã hạch toán sau hiệu lực.
- Còn: Gia hạn, Quyết toán, Thanh lý theo luật tự chuyển; hộp "chờ tôi duyệt" để màn duyệt tập trung (user 05/11).

## 6. Phase 25 — Hạch toán dịch vụ / chi phí / vận chuyển (05–06/11/2026)
Chi tiết: `design-phase25-hach-toan-dich-vu.md` (D1–D7, C1–C4). HĐ HRM thay HĐ hãng ⇒ dùng chung 2 màn Yêu cầu / Phiếu hạch toán dịch vụ HĐBH (port gop_db), rẽ nhánh `contractable_type`; cờ `hrm_contract_service_items.exported` / `hrm_contracts.shipping_exported`; HTHT tách chi phí sang other_cost; giá vốn = estimated × qty (chụp tuyệt đối cost_price); phiếu ghi sổ ⇒ Đang thực hiện; 3 nút ở chi tiết + danh sách HĐ; ERP bỏ qua phiếu HĐ HRM (scope excludeHrmContract, không gỡ morphMap).
