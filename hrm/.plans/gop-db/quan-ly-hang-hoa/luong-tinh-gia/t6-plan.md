# Plan T6 — Bản in 4 chứng từ (YCHG · YCTG · PTG · KQ) — 11/10/2026

> Nguồn: `design.md` §9 (YCHG mẫu 98 · YCTG mẫu 99 dùng `report_templates`; PTG + KQ dựng blade `prints/_layout`; letterhead theo công ty phiếu) ·
> `ton.md` Q17 (in cả 4, popup xem trước), Q20 (KQ chỉ giá bán, "In kết quả" ở nhóm trong YCHG), Q12 · mockup đã duyệt `moIn()` (4 bản in cùng 1 khuôn:
> đầu công ty · tiêu đề · khối thông tin · bảng · khối ký) · skill `print-page` mục 0, 2d, 3b, 4b, 4c, 8 · khảo sát `khao-sat-hrm.md` §8.
> ✅ **User cho "LÀM" 11/10/2026** — đúng phạm vi mục 4 (không migration / seeder / report_templates).
> Môi trường: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t6-print` từ nhánh chung `feat/chuyen-doi-hang-hoa`; DB dev `hrm_erp_giacty`.

## 0. Hiện trạng (đo 11/10)

- `report_templates` 98 `YC_HOI_GIA`, 99 `YC_TINH_GIA` CÓ; 100 (PTG) KHÔNG có; KQ không có hằng. Biến mẫu 98: `LOGO · CONG_TY · DIA_CHI_CONG_TY · SO_PHIEU ·
  NGUOI_LAP · NGAY_LAP · GHI_CHU · CHI_TIET`; mẫu 99 thêm `YC_HOI_GIA · NGUOI_YEU_CAU · DON_VI_TIEN · CHI_PHI`. Cả 2 mẫu: **logo nhỏ + tên/địa chỉ công ty**
  (KHÔNG phải letterhead ngang `{{HEADER}}` như skill 8b), **không có khối ký**, nhãn "Ngày lập", `CHI_TIET`/`CHI_PHI` là bảng HTML do code sinh.
- Khuôn blade dùng chung có sẵn: `Modules/Finance/Resources/views/prints/_layout.blade.php` (letterhead ngang theo `companies.header`, tiêu đề, số phiếu,
  "Ngày tạo", khối thông tin `$infoRows`, `$tableHtml`, khối ký `$signers`, CSS inline) — 24 mẫu Finance đang dùng (vd `prepick-cancel-request`).
  Trait `Modules/CustomerCare/Services/Concerns/PrintsCompanyLetterhead::letterheadUrl($companyId)` (theo công ty TRÊN chứng từ).
- FE dùng chung: `components/print/ReportPrintPreviewModal.vue` + `utils/mixins/reportPrintPreviewMixin.js` (`openPrintDetail(base, id, title)` gọi
  `{base}/{id}/print-data`, BE trả `{ data: { template: '<html>' } }`).
- T3/T4/T5 chưa có nút In nào (T5 ghi "In ⇒ T6").

## 1. Tự chốt theo design / mockup / skill (không hỏi — ghi để duyệt)

| # | Chốt |
|---|---|
| E1 | Popup xem trước `ReportPrintPreviewModal` (skill mục 0, 8) — không trang `/print`. A4 dọc cho cả 4. Không in DANH SÁCH (Q17 chỉ chứng từ) |
| E2 | Endpoint `GET …/{id}/print-data` cho YCHG / YCTG / PTG; KQ: `GET master-data/price-calculates/{id}/result-print-data` (1 KQ / PTG — Q20). Gate = gate XEM của chứng từ (YCHG: ai trong công ty thấy phiếu; YCTG / PTG: 1663 / 1664 / 1092; KQ: ai xem được YCHG — chỉ giá bán) |
| E3 | Letterhead / đầu trang theo `company_id` GHI TRÊN CHỨNG TỪ (skill 4b, trait `PrintsCompanyLetterhead`) |
| E4 | Số chuẩn quốc tế `1,234,567` (`number_format`), ngày `dd/mm/yyyy` (skill 2d) |
| E5 | Nội dung theo mockup `moIn()`: **YCHG** khối thông tin (Số phiếu, Ngày tạo, Người lập, Trạng thái, Ghi chú) + bảng gom nhóm La Mã (dòng nhóm: Thương hiệu – Hãng · XNK · trạng thái nhóm; dòng hàng: STT · Mã · Tên · Model · ĐVT · Giá bán lẻ hiện hành); ký **Người lập · PTKD duyệt**. **YCTG** (YCHG, Thương hiệu – Hãng, Tiền tệ / tỉ giá, Người lập) + bảng hàng × ĐVT: STT · Mã · Tên · ĐVT · Giá NCC · Đơn giá VNĐ · Thuế NK · Sau thuế · Chi phí (VNĐ); ký **XNK lập · Kế toán mua hàng**. **PTG** như YCTG + YCTG + 2 cột Giá nhập kho · Giá bán lẻ; ký **Người lập · Người duyệt**. **KQ** (PTG, YCTG, YCHG, Thương hiệu – Hãng, Người hỏi giá, Ngày áp giá) + bảng mỗi ĐVT × 6 loại giá: STT · Mã · ĐVT · Loại giá · Giá mới · ĐMGG (%); ký **Người tính giá**. KQ chỉ giá bán (Q20) |
| E6 | Nút **In** (tertiary, `ri-printer-line`, chỉ điều hướng — không popup xác nhận): footer màn chi tiết YCHG / YCTG / PTG + menu ⋮ dòng ở 3 danh sách (khớp chi tiết ↔ danh sách). **In kết quả**: dòng nhóm đã tính giá trong YCHG (mockup "Sửa 11/10") + footer PTG Đã duyệt. In được ở mọi trạng thái người đó xem được |
| E7 | Kiểm: Playwright mở 4 popup, đo theo skill 8b (letterhead trải ngang, cỡ chữ chỉ 13px / 10px, bảng ký rộng bằng thân phiếu, không tràn mép phải khổ in) + PHPUnit `print-data` 200 / 403 / đúng công ty letterhead / số định dạng |

## 2. Tồn — hỏi lần lượt (chưa chốt)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| T6-Q1 | YCHG / YCTG in theo mẫu ERP 98 / 99 hay blade `_layout` cho cả 4? | A | ✅ 11/10 user: **A — dựng blade `_layout` cho cả 4 chứng từ** (letterhead ngang, khối ký, "Ngày tạo", đồng bộ mockup). Mẫu ERP 98 / 99 giữ nguyên, không sửa, không dùng. Design §9 cập nhật theo chốt này |

## 3. Task

### 3.1 BE
- [x] `PriceCalculationPrintService` (dùng `finance::prints._layout` — T6-Q1; dữ liệu qua `show()` của từng service ⇒ giữ quyền xem) + 4 route:
  `price-asking-requests/{id}/print-data` · `price-calculate-requests/{id}/print-data` · `price-calculates/{id}/print-data` · `price-calculates/{id}/result-print-data`.
- [x] PHPUnit `PriceCalculateApiTest::ban_in_4_chung_tu…` (tiêu đề, số phiếu, số định dạng, khối ký, letterhead, KQ không có giá NCC / giá nhập kho, quyền 403); MasterData **397/397**.

### 3.2 FE
- [x] Nút **In** (secondary, `ri-printer-line`) ở chân màn chi tiết YCHG / YCTG / PTG + hành động "In" ở menu dòng 3 danh sách; **In kết quả** ở dòng nhóm đã tính giá trong YCHG + chân PTG có KQ; `ReportPrintPreviewModal` + `reportPrintPreviewMixin`.
- [x] Playwright MCP đo 4 bản in + hành động "In" ở menu dòng 3 danh sách (mục 3.3).
- [x] Thêm ca In vào 3 spec e2e (T3 N1 · T4 P4 · T5 P4) + sửa kỳ vọng chân form có thêm nút In; **CHẠY 12/10 (user cho): T3 + T4 + T5 19/19 passed** (1.9 phút, worktree 3031/8031, `--no-deps --workers=1`); afterAll dọn sạch.

### 3.3 Kết quả (12/10)
- api `a6220a001`, client `3e427f100` trên `feat/t6-print` ⇒ merge LOCAL nhánh chung: **api `1e194fe5c` · client `58965aa63`** (CHƯA push; api +23, client +21).
- Playwright MCP (NV 13 + role tạm 1092/1663/1664 — ĐÃ GỠ; tạm khai `ERP_URL` trong `.env` worktree để thấy letterhead — ĐÃ TRẢ `.env` gốc), chứng từ cũ PYCHG-03519 / PYCTG-03163 / PTG-03177:
  4 bản in đúng tiêu đề + người ký theo mockup (YCHG: Người lập · PTKD duyệt; YCTG: XNK lập · Kế toán mua hàng; PTG: Người lập · Người duyệt; KQ: Người tính giá) ·
  letterhead TPE trải ngang 716px = thân phiếu · bảng = khối ký = thân phiếu 716px (không tràn) · YCHG nhóm La Mã kèm XNK + trạng thái nhóm · KQ chỉ giá bán + ĐMGG ·
  "In kết quả" ở dòng nhóm YCHG mở đúng KQ của PTG-03177. Ảnh `anh-mockup/t6-in-{ptg,ychg,kq}.png`.
  🐞 Tự bắt khi đo: cột "Tên hàng hoá" bị bóp còn ~40px (độ rộng px cố định) ⇒ đổi sang % (150–257px).
  ⚠️ Lúc đo menu dòng danh sách, lệnh bấm `getByText('In')` trúng nút **In trong popup** ⇒ bật hộp thoại in của trình duyệt ⇒ trình duyệt MCP bị khoá
  (không đóng được bằng lệnh; không `pkill` theo memory). User đóng hộp thoại 12/10 ⇒ đo tiếp: "In" ở menu dòng PTG / YCTG / YCHG mở đúng bản in của dòng
  (PTG-03178, PYCTG-03163, PYCHG-04287 — `print-data` 200), Escape đóng popup. Console chỉ 404 ảnh avatar `e2e.png` + letterhead tương đối ở local (thiếu `ERP_URL`, khuôn tự ẩn ảnh).
- Ghi nhận (không sửa — khuôn dùng chung `_layout` của 24 bản in Tài chính): khối thông tin `.pr-info` có viền (CSS trang in kẻ viền bảng không mang class `no-border`), cỡ chữ thân 14px.

### Checkpoint — 2026-10-12 (T6)
Vừa hoàn thành: T6 bản in 4 chứng từ (BE + FE, PHPUnit 397/397, đo 4 bản in), merge LOCAL nhánh chung (api `1e194fe5c`, client `58965aa63`).
Đang làm dở: không (menu dòng đã đo 12/10; role tạm đã gỡ).
✅ ĐÃ PUSH nhánh chung `feat/chuyen-doi-hang-hoa` 12/10 (api `1e194fe5c`, client `58965aa63`).
Bước tiếp theo: plan T7 (chặn ERP + nghiệm thu). (e2e T3 + T4 + T5 19/19 đã chạy 12/10.)
Blocked: —

## 4. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/t6-print` từ nhánh chung; xong merge LOCAL, không push |
| DB | `hrm_erp_giacty`: KHÔNG migration / seeder; KHÔNG ghi `report_templates` (bảng dùng chung ERP); chỉ dữ liệu thử khi kiểm rồi dọn |
| Không đụng | ERP, gop_db, logic nghiệp vụ T3–T5 (chỉ thêm nút + endpoint đọc) |
