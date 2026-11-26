# #12294 — [ERP => HRM] Đồng bộ UI tiêu đề khối (@khoipv)

Redmine: http://quanly.dnsmedia.vn/issues/12294 · Nhánh: hrm-client `develop` (con của gop_db)

Yêu cầu: lấy đầu khối màn `customer-care/device-errors/create` làm chuẩn → sửa mọi màn tạo mới / cập nhật / chi tiết
về màu tiêu đề, bo góc, cụm "người tạo - thời gian tạo"; căn giữa chữ theo chiều dọc; cập nhật rule vào skill chung.

## Quyết định (user chốt 25/11/2026)
- Đổi rule TOÀN CỤC `body .card .card-header.section-header` (default.scss) từ dải nền slate (chuẩn 19/10) sang
  nền trắng + gạch dưới #e5e7eb, khung #e5e7eb bo 8px, h6 14px đậm #1f2937 margin 0 (căn giữa dọc), min-height 36px.
- Sửa cả các màn tự chế header bằng class riêng (đầu khối cấp 1). Tiêu đề nhóm con bên trong khối giữ nguyên.
- Màn họp (meeting/GeneralInfo) giữ màu khối riêng. Popup, khung dựng form (form-templates builder) không thuộc phạm vi.

## Tasks
- [x] Đọc task + ảnh, kiểm kê phạm vi bằng `new-screens-sweep/inventory.py --kind form|other` (896 file)
- [x] Gốc: `assets/scss/default.scss` — chuẩn header khối mới (bao ~170 màn dùng V2BaseFormSection / section-header)
- [x] Màn mẫu: `DeviceErrorFormComponent.vue` `.form-card-head` thêm min-height 36px + h6 margin 0 (căn giữa dọc)
- [x] Gốc 2: `components/V2BaseFormCard.vue` (42 màn luồng xuất nhập) — `.form-card-head` nền #f9fafb → trắng, min-height 36px,
      line-height 20px; khối File đính kèm `.v2-attach-card` bỏ chữ IN HOA 12px xám → 14px đậm #1f2937, h6 margin 0
- [x] Lô A — assign: 16 file sửa (prospective-projects 9 component: mỗi mục thành khối có khung + đầu khối chuẩn;
      quotations/_id edit+index, SummaryQuotationForm: đầu khối + CreatorInfoLine; pricing-requests/_id; handover 2; BomBuilderTableCard).
      Bỏ qua: prospective-projects add/edit/index + MeetingProject (rule chết), leader-schedule-config (màn cấu hình, không phải đầu khối)
- [x] Lô B — 7 file: solutions InfoTab/ModulesTab/HumanResourceTab/ProjectInfoTab, solution-modules ProjectInfoTab (bỏ nền tím),
      FormPreview (CreatorInfoLine), OtherInfoTab. Bỏ qua: CustomerForm/DocumentTable (đã đúng), BomListTable (chỉ trong popup),
      FileAttachmentTable (bảng con dùng nhiều nơi)
- [x] Lô C — 10 file: BillAdjustDeptForm, PrepickCancelForm, PrepickExtend/ProductPrepick/WarehousePrepick RequestForm,
      ProductImportDirectTransferForm, ServiceFormComponent, PriceCalculateForm, PriceAskingRequestForm, PriceCalculateRequestForm
      (3 form giá: span .creator-line → CreatorInfoLine). Bỏ qua WarrantyRepairRequestForm (đã đúng)
- [x] Verify: 36 file thay đổi — vue-template-compiler + node-sass từng khối scss + default.scss: 0 lỗi.
      Grep nền khác trắng của `.section-header`: còn SectionBuilder (form builder), meeting GeneralInfo (màu khối có chủ đích),
      bill-income-reports 2 file (rule scoped yếu hơn chuẩn chung → chuẩn thắng)
- [x] Cập nhật skill: `form-validate` mục 1c "CHUẨN ĐẦU KHỐI" + checklist `erp-to-hrm-screen`
- [x] Kiểm tra theo yêu cầu (26/11): "bug này xem kỹ chưa" — đối chiếu lại task + ảnh (tiêu đề lệch xuống so với cụm
      người tạo trên dev) với diff 36 file: đủ 4 ý (màu, bo góc, cụm người tạo, căn giữa dọc) + đã ghi skill. Rà sót:
      không còn `.card-header` ngoài chuẩn ở màn form/chi tiết (chỉ còn báo cáo insurance-register); không còn cụm
      người tạo tự chế ở màn form/chi tiết (còn lại là báo cáo/danh sách/picker). Lệch nhỏ: pricing-requests/_id dòng 92
      đầu khối "Báo giá" dùng `<strong>` thay `<h6>`. Lưu ý: rule `:has()` mới thêm viền+bo cho MỌI card có section-header
      (cả popup/danh sách). Chưa kiểm trình duyệt.
- [ ] User kiểm trên trình duyệt (chưa mở Playwright) — ưu tiên: device-errors/create, prospective-projects/_id (khung lồng khung?),
      solutions/_id các tab, quotations/_id, 1 màn V2BaseFormCard (vd warehouse-prepick-requests)

### Checkpoint — 25/11/2026
Vừa hoàn thành: đổi chuẩn header khối toàn cục + sửa 36 file hrm-client, cập nhật skill
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm các màn ưu tiên; chưa commit
Blocked:

Lệnh phạm vi (chạy trong hrm-client):
```
python -X utf8 ../.claude/skills/new-screens-sweep/inventory.py --kind form --format paths  (+ --kind other)
| grep -lE 'class="[^"]*\b(form-card-head|tp-section-title|info-card-header|info-card-title|tp-card-header|q-section-title|section-title|fb-section-header|fb-card-header|support-block-head|project-solution-card-header|lsc-section-title|dm-section-title|ba-section-title|staff-section-title|bom-section-title)\b'
```
