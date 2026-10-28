# Phase 20 — Mẫu in & chế độ in Hợp đồng bán hàng (KHẢO SÁT, chưa code)

> 27/10/2026 · nhánh `gop_db-hop-dong-ban` · trạng thái: ĐÃ CHỐT hết (mục 5–6), chờ xin phép code.

## 1. ERP đang in HĐ bán thế nào (`ERP/TanPhatDev`)

**Cơ chế:** mẫu là HTML (CKEditor) chứa `{{BIEN}}`. Lúc lập HĐ, mẫu được **chép vào chính HĐ** (`firm_contracts.template`), người dùng sửa riêng cho từng HĐ. Lúc in, server chạy `clearNull(fillReport($contract->template, FirmContractPrint::handlePrint()))` → trang `print.blade.php` (A4, lề 15/22/22/20mm), người dùng bấm In của trình duyệt. Không sinh docx/PDF.

**Nguồn mẫu:** bảng `print_templates` (dùng chung trên DB gộp), `type = 1` "Hợp đồng bán hàng": **17 mẫu** (HD-01A … HD-07B, HD-05A "Đơn hàng < 20tr", HĐ đại lý, HĐ nguyên tắc, phụ lục, bản quyền phần mềm…). `type = 12` Biên bản giao nhận: 8 mẫu. Mẫu không chia theo công ty. Soạn ở màn ERP `/admin/print-templates` (quyền "Quản lý mẫu in").
Dữ liệu thật: 27,951 HĐ đều có `template`; `contract_type_print` hay dùng nhất: 165 Đơn hàng < 20tr (7,957) · 141 Vật tư phòng Dầu (4,511) · 145 TB đơn giản (2,399) · 147 VT thông thường (2,205) · 9,117 HĐ không ghi mẫu (HĐ cũ).

**Tab "Mẫu in" trên form HĐ ERP** (`resources/views/sale/firm/contracts/form.blade.php:1265-1336`) — 2 tab con:
1. *Mẫu in hợp đồng*: select "Loại hợp đồng" (`contract_type_print` = id mẫu, bắt buộc) + CKEditor `template` (bắt buộc). Đổi loại khi đã có nội dung ⇒ hỏi xác nhận "thông tin mẫu in sẽ bị thay đổi".
2. *Mẫu in phụ lục hàng hoá*: CKEditor `template_print_product` (mặc định từ `report_templates` id 106).

**Chế độ in (modal "Mẫu in" ở danh sách / chi tiết):**

| Lựa chọn | Nút | Ghi chú |
|---|---|---|
| In hợp đồng | IN TỔNG HỢP / IN CHI TIẾT (`print_group=1` ⇒ bảng hàng nhóm theo group) | chi tiết chỉ có ở danh sách |
| In phụ lục hàng hoá – mẫu 1 | như trên | `printExtraProduct?template_type=1` |
| In phụ lục hàng hoá – mẫu 2 | như trên | **lỗi ERP**: cũng gửi `template_type=1` ⇒ mẫu 2 không bao giờ in được |
| In biên bản giao nhận – bàn giao | modal riêng: chọn mẫu type 12 + NV đại diện bên giao, người nhận, chức vụ, SĐT | đọc thẳng `print_templates` mỗi lần in |

Tự động (không có nút): **ẩn giá** khi có quyền "Xem hợp đồng ẩn giá" và HĐ ngoài phạm vi xem giá (cột giá bỏ, tiền thành `*****`); **QR** ở góc khi HĐ đã hiệu lực/quyết toán. Khách cá nhân/tổ chức xử lý bằng biến `*_OPTION`, không phải chế độ riêng. Phụ lục (giảm/bổ sung) in qua cùng route với biến `SO_PHU_LUC`, `SO_HOP_DONG_GOC`.

**Biến** (`PrintTemplateVariable::variablesType1()` L44-405, giá trị ở `FirmContractPrint::handlePrint` L46-174; service 2,943 dòng): `HEADER`, `SO_HOP_DONG`; bảng hàng HTML `CHI_TIET_HOP_DONG` (+3 alias `CHI_TIET_HOP_DONG_HANG_HOA_THIET_BI`, `CHI_TIET_DON_HANG_MAU_1/2`); Bên A–khách (`KHACH_HANG`, địa chỉ, ĐT, MST/CCCD + `_OPTION`, STK/ngân hàng, người đại diện + chức vụ…); Bên B–công ty (`TEN_CONG_TY`, MST, STK, `NGUOI_DAI_DIEN_CONG_TY`, `CHUC_VU_…`, `NVKD`…); `DIA_CHI_GIAO_HANG`; `THANH_TIEN`, `THANH_TIEN_BANG_CHU`, `THANH_TOAN` (HTML từng đợt + bằng chữ), `DIEU_KHOAN_BAO_GIA`.

**Lỗi / điểm lệch ở ERP — KHÔNG chép sang:**
- Route in HĐ chính nằm ngoài middleware, không `canView()` ⇒ ai có URL đều xem được HĐ (để quét QR).
- Phụ lục mẫu 2 gửi nhầm tham số (trên).
- 3 route `printExtraOther`, `exportExtraProduct`, `exportExtraOther` không có method.
- `TEN_CONG_TY` (in hoa) / `TEN_CONG_TY_IN_HOA` (tên gốc) đặt tên ngược.
- Letterhead lấy theo công ty của **người lập**, không theo công ty trên HĐ (HRM chuẩn: theo `company_id` chứng từ).
- `CHI_PHI` khai biến nhưng không gán giá trị.

## 2. HRM đã có gì

- **2 hệ mẫu**: `hrm_print_templates` (HC-NS: HĐLĐ, Quyết định, Biên bản, Meeting… — màn `pages/decision/category/print_templates`) và **`print_templates` ERP** (đọc thẳng trên DB gộp, không có màn quản lý ở HRM).
- **Khuôn gần nhất — Hợp đồng dịch vụ (`wr-service-contracts`)** đi đúng đường ERP: `GET …/print-templates` (`print_templates` type 6) + `GET …/{id}/print-data` (`canView` + `fillReport($model->template, contractVariables())`); form có khối "Mẫu hợp đồng" (`WrServiceContractForm.vue:513-545`): `V2BaseSelect` chọn mẫu ở slot actions + `CompactReviewEditor`; lưu `contract_type` + `template` trên bản ghi (lý do ghi ở service: HĐ cũ in lại vẫn đúng lời văn đã ký).
- **Chọn kiểu in**: popup `wr-quotations/components/SelectPrintTemplateModal.vue` (`V2BaseModal` + select mẫu + checkbox) → `print-data?template=…`.
- **Biên bản giao nhận type 12** đã port ở YC xuất hàng: `ProductExportRequestController::handoverTemplates()/printHandoverData()` + `ProductExportRequestHandoverPrintService`.
- **Popup xem trước**: `ReportPrintPreviewModal` + `reportPrintPreviewMixin` (`openPrintDetail('assign/contracts', id, title)` ⇒ BE trả `{data:{template}}`, route `/{id}/print-data` khai trước `/{id}`). Letterhead: trait `Modules/Assign/Services/Concerns/PrintsCompanyLetterhead::letterheadUrl($companyId)`.
- `fillReport/clearNull` có sẵn ở `app/Helper/FormatHelper.php:998-1019`.
- **HĐ bán HRM hiện chưa có gì về in**: `hrm_contracts` không có cột template; không endpoint, không nút In.

## 3. Đề xuất hướng làm (theo khuôn `wr-service-contracts`)

1. **Nguồn mẫu = `print_templates` ERP `type = 1`** — dùng lại 17 mẫu đang chạy, biến giữ tên ERP ⇒ mẫu soạn ở ERP in được ở HRM, không phải làm màn quản lý mẫu.
2. **Lưu lời văn vào HĐ**: migration thêm `hrm_contracts.print_template_id` + `template` (longText) (+ `template_print_product` nếu làm phụ lục hàng hoá). Khi tạo từ báo giá: chưa chọn mẫu.
3. **Tab "Mẫu in"** (tab thứ 6, trước Đính kèm hoặc sau) theo khuôn `WrServiceContractForm`: select "Mẫu hợp đồng" ở hàng tab + `CompactReviewEditor`; đổi mẫu khi đã có nội dung ⇒ `$confirm`. Màn Chi tiết: `v-html` chỉ đọc.
4. **BE**: `GET assign/contracts/print-templates`, `GET assign/contracts/{id}/print-data?mode=…` (gate `canView`, ẩn giá theo quyền), `ContractPrintService` port từ `FirmContractPrint::handlePrint` (bảng hàng A/B theo cấu trúc HĐ HRM, thanh toán từng đợt + bằng chữ, letterhead theo `company_id` HĐ).
5. **Chế độ in**: nút In (màn Chi tiết + dòng danh sách) mở popup chọn chế độ (khuôn `SelectPrintTemplateModal`) → `ReportPrintPreviewModal`.

## 4. Câu cần user chốt

1. Nguồn mẫu: `print_templates` ERP type 1 (đề xuất) hay mẫu riêng HRM?
2. Phạm vi chế độ in đợt này: In hợp đồng (Tổng hợp / Chi tiết theo nhóm) · Phụ lục hàng hoá (mẫu 1 / mẫu 2) · Biên bản giao nhận (type 12) — làm những cái nào?
3. Tab "Mẫu in" có cả tab con "Mẫu in phụ lục hàng hoá" như ERP không?
4. Ẩn giá: port quyền "Xem hợp đồng ẩn giá" (HRM chưa có quyền này) hay để sau?
5. QR trên bản in (ERP mở link in công khai): bỏ, hay làm link xác thực có đăng nhập?
6. Bắt buộc chọn mẫu khi Trình duyệt (ERP bắt buộc) hay chỉ cần trước khi In?

## 5. Quyết định đã chốt (27/10/2026)

1. **Mẫu in làm MỚI trên màn quản lý mẫu in của HRM** (`hrm_print_templates`, `pages/decision/category/print_templates`) — KHÔNG đọc `print_templates` ERP. ⇒ thêm loại mẫu + bộ biến HĐ bán vào `PrintTemplateVariable` HRM (thay đổi mục 3.1 đề xuất cũ).
2. Làm **đủ các chế độ in**: In hợp đồng (Tổng hợp / Chi tiết theo nhóm) · Phụ lục hàng hoá mẫu 1 / mẫu 2 (sửa lỗi mẫu 2 của ERP) · Biên bản giao nhận – bàn giao.
3. Tab "Mẫu in" **giống ERP**: 2 tab con "Mẫu in hợp đồng" + "Mẫu in phụ lục hàng hoá".
4. **Ẩn giá làm luôn.**
5. **Giữ QR** trên bản in.
6. Bắt buộc chọn mẫu **giống ERP**.

Luật ERP đã đọc thêm:
- Ẩn giá (`FirmContract::shouldHidePrice`, `app/Model/Sale/Firm/Contract/FirmContract.php`): quyền "Xem hợp đồng ẩn giá" cho XEM danh sách + chi tiết mọi HĐ toàn tổng công ty; HĐ ngoài phạm vi xem thật (`isWithinPriceScope` = SA + chủ phiếu + người duyệt + 4 quyền xem) ⇒ ẩn giá ở danh sách, chi tiết và bản in. Không có quyền này ⇒ không đổi gì.
- Bắt buộc mẫu: `FirmContractStoreRequest:76-78` / `UpdateRequest:76-78` — `contract_type_print`, `template`, `template_print_product` đều `required` ở mọi lần lưu (status 1 nháp lẫn 2).
- QR: SVG 12mm, nội dung = URL route in công khai `firmContract.print` (kèm query), chỉ khi status ∈ {3, 6, 9, 10}.

## 6. Câu tồn — đã chốt (27/10/2026)

7. **Loại mẫu**: thêm 1 loại "Hợp đồng bán hàng" vào `hrm_print_templates` + 3 loại con (cơ chế `sub_type` có sẵn): **Hợp đồng** · **Phụ lục hàng hoá** · **Biên bản giao nhận**. Biến chung (letterhead, Bên A/B, số HĐ) khai 1 lần, biến riêng theo loại con.
8. **Chép sẵn mẫu ERP** sang HRM làm mẫu ban đầu: 17 mẫu `print_templates` type 1 → loại con Hợp đồng; 8 mẫu type 12 → Biên bản giao nhận; mẫu phụ lục hàng hoá mặc định (`report_templates` id 106) → Phụ lục hàng hoá. Giữ nguyên tên biến ERP. Lệnh chép ghi DB ⇒ xin phép riêng lúc chạy. Sau khi chép, mẫu tách rời ERP.
9. **Ẩn giá đủ như ERP**: quyền mới "Xem hợp đồng bán hàng ẩn giá" (guard api, seeder sync theo tên) ⇒ người có quyền xem danh sách + chi tiết MỌI HĐ toàn tổng công ty; HĐ ngoài phạm vi thật (4 cấp Phase 18 + chủ phiếu + người duyệt) ⇒ ẩn giá ở danh sách, chi tiết (bảng hàng, tổng hợp thanh toán, đợt thanh toán) và bản in (bỏ cột giá, tiền = `*****`). BE trả `null` cho trường giá (không dựa FE ẩn). Như ERP (`FirmContractDatatable.php:122-125`): HĐ ẩn giá **ẩn các thao tác lộ giá** — Xem HTHT, In hợp đồng & phụ lục hàng hoá — nhưng **vẫn cho In biên bản giao nhận** (chưa kiểm ERP xử lý biến `CHI_TIET_CO_GIA*` thế nào khi ẩn giá — đọc `getAcceptanceDeliveryTemplate` ở bước B6, lệch thì hỏi lại); Sửa/Duyệt giữ theo quyền hiện có (không thêm luật).
10. **QR** = link màn Chi tiết HĐ trên HRM (cần đăng nhập + quyền xem), SVG ~12mm góc trên phải, chỉ khi status ∈ {6 Có hiệu lực, 8 Đang xuất hàng, 12 Đang quyết toán, 11 Đã quyết toán} (ánh xạ ERP {3, 6, 9, 10}).
11. **Bắt buộc mẫu khi Trình duyệt** (theo quy ước HRM, khác ERP): Lưu nháp không cần; Trình duyệt bắt cả 3 ô (mẫu HĐ, nội dung HĐ, nội dung phụ lục hàng hoá) — FE đỏ đồng loạt + tab "Mẫu in" đỏ & có `*`, BE 422.

## 7. Plan triển khai (chờ cho phép)

**BE — hrm-api**
- [ ] B1 `PrintTemplateVariable`: loại `HOP_DONG_BAN_HANG` (số tiếp theo, đánh số liên tục) + 3 sub_type + bộ biến (port `variablesType1` + biến phụ lục hàng hoá + biến biên bản type 12); `PrintTemplate::PROTECTED_CODES` nếu tra theo code.
- [ ] B2 Migration `hrm_contracts`: `print_template_id`, `template` (longText), `template_print_product` (longText). `PrintTemplateService::referencingTables()` thêm `hrm_contracts`.
- [ ] B3 Lệnh/seed chép mẫu ERP → `hrm_print_templates` (idempotent theo code, chạy riêng có xin phép).
- [ ] B4 Store/Update HĐ nhận 3 trường; rule `required` chỉ khi Trình duyệt (khuôn validate hiện có của HĐ).
- [ ] B5 `GET assign/contracts/print-templates?sub_type=` (lọc `hrm_print_templates` loại HĐ bán, status=1).
- [ ] B6 `ContractPrintService` port `FirmContractPrint::handlePrint`: letterhead theo `company_id` HĐ (`PrintsCompanyLetterhead`), Bên A/B, bảng hàng (A Hàng hoá + B Dịch vụ & Chi phí, chế độ Tổng hợp / Chi tiết theo nhóm), thanh toán từng đợt + bằng chữ, giao hàng, ẩn giá, QR.
- [ ] B7 `GET assign/contracts/{id}/print-data?mode=contract|product_annex_1|product_annex_2|handover&group=0|1` (+ tham số biên bản: template_id, NV giao, người nhận, chức vụ, SĐT) — gate `canView`, khai trước `/{id}`.
- [ ] B8 Quyền "Xem hợp đồng bán hàng ẩn giá" (seeder) + mở rộng `scopedContractQuery` + cờ `hide_price` trên Resource danh sách/chi tiết, null hoá trường giá; print-data chặn mode hợp đồng/phụ lục khi `hide_price`.

**FE — hrm-client**
- [ ] F1 Màn quản lý mẫu in: loại mới + 3 loại con hiện đúng, bảng biến theo loại con.
- [ ] F2 `edit.vue` tab "Mẫu in" (2 tab con như ERP): select mẫu ở hàng tab + `CompactReviewEditor`; đổi mẫu khi có nội dung ⇒ `$confirm`; lỗi Trình duyệt ⇒ tab đỏ.
- [ ] F3 Màn Chi tiết: mục Mẫu in chỉ đọc; nút In → popup chọn chế độ (khuôn `SelectPrintTemplateModal`) → `ReportPrintPreviewModal`; biên bản giao nhận có form NV giao/nhận.
- [ ] F4 Danh sách: hành động In ở dòng (cùng điều kiện với chi tiết).
- [ ] F5 Ẩn giá ở danh sách / chi tiết / form khi `hide_price`.
- [ ] F6 Playwright: đo tab Mẫu in, popup in từng chế độ, ẩn giá (có quyền / không quyền), QR; cập nhật spec e2e.

## 8. Đợt 2 — Ẩn giá: quyết định (27/10/2026)

12. Biên bản giao nhận khi HĐ ẩn giá: **vẫn in được, bảng luôn KHÔNG giá** (`CHI_TIET_CO_GIA*` trả bảng không cột giá kể cả mẫu "CÓ GIÁ") — vá lỗ ERP (ERP in giá).
13. Danh sách / Chi tiết: **giữ cột, số tiền hiện `*****`**; BE trả `null` cho mọi trường giá + cờ `hide_price`.
14. Xuất Excel danh sách: dòng HĐ ẩn giá ghi `*****` ở cột tiền.
Phạm vi xem giá = cổng xem hiện tại `scopedContractQuery` (4 cấp + người lập). Có quyền ẩn giá ⇒ thấy MỌI HĐ (vẫn ẩn "Đang tạo" của người khác — Q1 Phase 18); HĐ ngoài phạm vi ⇒ ẩn giá, ẩn Hỗ trợ hạch toán + In hợp đồng / phụ lục (chỉ còn In biên bản).
