# Đối chiếu code hiện tại vs HDSD cũ — Màn "Phiếu thu thập thông tin" (Form Template)

> Nguồn: agent Opus đọc code FE+BE ngày 2026-07-16. Doc cũ = `DanhMuc/HDSD_PhieuThuThapThongTin.docx` (tạo 19/06/2026). Text doc cũ dump ở `scratchpad_doc_phieu.txt`.

## Kết luận cốt lõi
Toàn bộ khái niệm **"Nhóm ngành" + "Nhóm giải pháp"** trong doc cũ đã bị **loại bỏ hoàn toàn**, thay bằng **MỘT trường duy nhất: "Ứng dụng" (`application_id`)**. Bằng chứng DB: migration `2026_06_26_100004_drop_scope_industry_from_form_templates_table.php` (drop `scope_id`, `industry_id`) + `2026_06_26_100003_readd_application_id...`.

## 1. Bản đồ màn hiện tại
### Route thật
- Danh sách: `/assign/form-templates` (`pages/assign/form-templates/index.vue`)
- Tạo mới: `/assign/form-templates/add` (`add.vue`)
- Sao chép: `/assign/form-templates/add?copyFrom={id}`
- Xem chi tiết: `/assign/form-templates/{id}` (`_id/index.vue`)
- Sửa: `/assign/form-templates/{id}/edit` (`_id/edit.vue`)

### Cột danh sách — CHỈ CÒN 6 CỘT (index.vue:343-385)
1. STT (sticky) — 2. Mẫu phiếu (sticky, tên + Người tạo + Ngày tạo, nút thao tác ở cột này) — 3. Trạng thái (pill Nháp1/Hoạt động2/Khoá3) — 4. **Ứng dụng** (`application_name`, thay 2 cột Nhóm ngành+Nhóm giải pháp) — 5. Cập nhật (ngày + bởi, sortable) — 6. Số câu hỏi (`questions_count`, phải, sortable).

### Nút toolbar
- "Tạo mẫu phiếu" → /add
- "Xuất Excel" → GET `/api/v1/assign/form-templates/export`, file `danh_sach_mau_phieu_thu_thap_thong_tin.xls`

### Nút trên mỗi dòng (getRowActions:521-570)
- Xem (luôn) — Sao chép (luôn) — Sửa (luôn hiện; nếu status=3 Khoá → toast "Mẫu đang 'Khoá' nên không cho sửa. Hãy mở khoá trước.", không chuyển trang) — In mẫu phiếu (luôn, mở modal) — nếu status≠1: Khoá/Mở khoá — nếu status=1: Xoá.

### Bộ lọc — 7 tiêu chí (index.vue:17-81)
- Tìm kiếm nhanh (placeholder "Tìm theo tên mẫu phiếu...", lọc theo name) — **Ứng dụng** (V2BaseSelect allowClear, thay Nhóm ngành+Nhóm giải pháp) — Trạng thái (Nháp1/Hoạt động2/Khoá3) — Người tạo — Người cập nhật — Cập nhật từ (date) — Cập nhật đến (date). Lọc tự động (deep watcher), chỉ keyword cần bấm Tìm kiếm.

### Quyền
- Một quyền: `Quản lý danh mục mẫu phiếu thu thập thông tin` (id 1013, group "Danh mục", PermissionsTableSeeder.php:949). Gắn checkPermission cho index/export/store/update/lock/unlock/destroy/copy-data. Route show `/{formTemplate}` KHÔNG chặn quyền (xem chi tiết không cần quyền — KHỚP doc).

## 2. Đặc tả builder hiện tại
### B1 Thông tin chung (FormMeta.vue) — CHỈ CÒN 2 TRƯỜNG
| Trường | Control | Bắt buộc | Mặc định | Khoá |
|---|---|---|---|---|
| Tên form | V2BaseInput | Có (name required max 255) | rỗng | — |
| Ứng dụng | V2BaseSelect | Có (application_id required, exists:applications) | rỗng | Khoá khi status==2 (Hoạt động) |
- KHÔNG còn "Nhóm ngành"/"Nhóm giải pháp". Options Ứng dụng từ store `optionsSelect/fetchApplications`.
- **Thư viện câu hỏi chỉ hiện sau khi chọn Ứng dụng** (watch formMeta.applicationId). API: `GET assign/questions?application_id=...&include_all_scope=1&status=1&per_page=1000`.

### Nút "Thêm Section" + "Xem trước"/"Chỉnh sửa" (toggle previewMode, góc trên phải). Nút "Lưu nháp" trong FormBuilder bị ẩn (show-save-draft=false).

### Section (SectionBuilder.vue)
- Đánh số A,B,C… — Tên Section (required max 255, lỗi `sections.{i}.title`) — Mô tả (textarea, nullable max 500) — nút Group (disabled khi section đã có câu hỏi trực tiếp) / Nhân bản / Xoá (modal "Bạn có chắc muốn xóa Section này?"). Kéo sắp xếp. Section chỉ chứa câu hỏi trực tiếp HOẶC group; kéo câu hỏi thường vào section đã có group → tự tạo Group mới; câu hỏi loại `hierarchy`/`parent` kéo vào tự thành Group.

### Group: đánh số I,II,III… — Tên, Mô tả, nút Xoá Group (modal xác nhận).

### Câu hỏi (QuestionItem.vue)
- Đánh số 1,2,3 (con 1.1…) — sửa nội dung tại ô label — tag: code, type, badge "Bắt buộc", tag "Logic: …" — nút Bắt buộc (icon asterisk toggle)/Nhân bản/Xoá(đỏ). Câu hỏi cha (type=parent): khối "Câu hỏi con" + thêm/xoá con (con có checkbox Bắt buộc).
- Logic hiển thị: block "Logic hiển thị (nếu có)" → checkbox "Kích hoạt logic hiển thị" → "Nếu câu hỏi mã" (select) + "Thoả điều kiện" (operator) + "Giá trị". Toán tử thật: == (=), != (≠), >, <, >= (≥), <= (≤).

### Thư viện câu hỏi (QuestionLibrary.vue)
- Ô tìm "Tìm trong thư viện..." — tab lọc: Tất cả / Văn bản / Lựa chọn / Khác — thẻ: label, badge type, Mã, Trả lời — kéo-thả clone; câu hỏi đã dùng tự ẩn — nút "Tạo nhanh".

### Popup "Tạo nhanh câu hỏi" (AddQuestionQuickModal.vue) — 6 khối
| Trường | Control | Bắt buộc | Mặc định |
|---|---|---|---|
| Phạm vi áp dụng | V2BaseSelectInModal | Có | **2 = "Theo ứng dụng"** (1=Tất cả, 2=Theo ứng dụng) |
| Loại dữ liệu | V2BaseSelectInModal | Có | rỗng (9 loại: Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox nhiều lựa chọn, Ngày, File, Có/Không) |
| **Trạng thái** (MỚI) | V2BaseSelectInModal | — | **1 = Hoạt động** (Hoạt động1/Khóa2) |
| Tiêu đề câu hỏi | V2BaseTextarea | Có | rỗng |
| Mô tả | V2BaseTextarea | — | rỗng |
| Danh sách đáp án | (chỉ khi dropdown/radio/checkbox) | Có | tự sinh 2 dòng, nút Thêm đáp án/xoá |
- Nút: Lưu + Đóng. POST `assign/questions`; application_id tự lấy từ Ứng dụng đang chọn; sau lưu reload thư viện. Không tạo được câu hỏi cha-con từ Tạo nhanh.

### Xem trước (FormPreview.vue)
- Header tên form — mục "1. Thông tin chọn" chỉ còn "Ứng dụng *" (disabled) — render Section/Group/câu hỏi theo type; logic hiển thị áp dụng — mỗi câu hỏi không phải text/textarea có link "Ghi chú" mở textarea — số nhập định dạng vi-VN.

### Nút Lưu + validation
- add.vue: luôn có "Lưu"(status1) + "Lưu và duyệt"(status2). edit.vue: "Lưu" chỉ khi status==1; "Lưu và duyệt" khi status==1 hoặc ==2.
- Validation (FormTemplateRequest): name required max255; application_id required+exists; sections required array; mỗi section title required max255, description max500; **mỗi section ≥1 câu hỏi** ("Bắt buộc phải nhập"); nếu Published mà Ứng dụng đã có phiếu Published khác → lỗi application_id "Ứng dụng này đã có mẫu phiếu đang hoạt động".
- Update thay thế toàn bộ Section/câu hỏi (xoá hết tạo lại — Service.update).

## 3. BẢNG LỆCH (doc cũ ≠ code) — DÙNG ĐỂ SỬA DOC
| Mục | Doc cũ | Code hiện tại | Sửa thành |
|---|---|---|---|
| Thuật ngữ/Giới thiệu | thiết kế theo "Nhóm giải pháp"; ràng buộc "mỗi Nhóm giải pháp 1 mẫu phiếu" | theo **Ứng dụng**; "1 Ứng dụng = 1 mẫu Published" | Thay hết Nhóm ngành/Nhóm giải pháp → Ứng dụng |
| Trạng thái (mục 4) | Nháp/Hoạt động/Khóa | DRAFT1/PUBLISHED2/LOCKED3 | KHỚP (chỉ đổi ràng buộc sang Ứng dụng) |
| Cột danh sách | 7 cột, có Nhóm ngành+Nhóm giải pháp | 6 cột, có Ứng dụng | STT, Mẫu phiếu, Trạng thái, Ứng dụng, Cập nhật, Số câu hỏi |
| Bộ lọc | có Nhóm ngành+Nhóm giải pháp (cascading) | có Ứng dụng (1 select allowClear) | Thay 2 filter → 1 "Ứng dụng", bỏ cascading |
| Tìm kiếm nhanh | tên mẫu phiếu | đúng | KHỚP |
| Nút toolbar | Tạo mẫu phiếu, Xuất Excel | đúng | KHỚP |
| Nút trên dòng | Xem/Sao chép/Sửa/In/Khóa-Mở khóa/Xóa | đúng (Sửa luôn hiện, bấm khi Khoá ra toast; Xóa chỉ Nháp; Khóa chỉ ≠Nháp) | KHỚP, ghi rõ Sửa chặn bằng toast |
| B1 Thông tin chung | 3 trường (Tên form, Nhóm ngành, Nhóm giải pháp) | 2 trường (Tên form, Ứng dụng) | Bỏ 2 trường, còn Tên form(*)+Ứng dụng(*) |
| ĐK hiện thư viện | sau khi chọn Nhóm ngành+Nhóm giải pháp | sau khi chọn Ứng dụng | "sau khi chọn Ứng dụng" |
| Popup Tạo nhanh trường | Phạm vi áp dụng, Loại dữ liệu, Tiêu đề(*), Mô tả, Đáp án | thêm **Trạng thái**; Phạm vi = Tất cả/Theo ứng dụng (mặc định Theo ứng dụng) | Bổ sung Trạng thái + đổi nghĩa Phạm vi áp dụng |
| Popup Tạo nhanh nút | (không nêu) | Lưu + Đóng | Ghi rõ 2 nút |
| B7 điều kiện hợp lệ | "Tên form, Nhóm ngành, Nhóm giải pháp" | "Tên form, Ứng dụng" + section title required + mỗi section ≥1 câu hỏi | Đổi sang Ứng dụng |
| B7 ràng buộc trùng | (không nêu) | Published trùng Ứng dụng → "Ứng dụng này đã có mẫu phiếu đang hoạt động" | Bổ sung message |
| Sửa khi Hoạt động | Nhóm ngành+Nhóm giải pháp bị khóa | "Ứng dụng" bị khoá (disabled khi status==2) | "trường Ứng dụng bị khoá" |
| Duyệt (4.1) | mỗi Nhóm giải pháp 1 mẫu Hoạt động | mỗi Ứng dụng 1 mẫu Hoạt động | Đổi |
| Mở khoá (4.2) | nếu Nhóm giải pháp đã có mẫu khác Hoạt động | nếu Ứng dụng đã có mẫu Published khác (unlock:206) | Đổi |
| Xem chi tiết (5.1) | chỉ đọc | đúng; footer có nút In mẫu phiếu + Sao chép | KHỚP, bổ sung 2 nút footer |
| In (5.2) | modal preview → In | đúng | KHỚP |
| Sao chép (5.3) | giữ Tên+Nhóm ngành, để TRỐNG Nhóm giải pháp | Giữ Tên+**Ứng dụng (KHÔNG để trống)**, ép Nháp, giữ Section+thứ tự; **bỏ câu hỏi/nhóm scope "Theo ứng dụng", giữ scope "Tất cả"** (Service.prepareCopyData:264-326) | Viết lại theo logic mới |
| Quyền | 1 quyền | đúng (id 1013) | KHỚP |

## 4. Điểm MỚI (doc chưa có)
1. Trường "Trạng thái" popup Tạo nhanh (Hoạt động/Khóa, mặc định Hoạt động).
2. "Phạm vi áp dụng" = Tất cả / Theo ứng dụng (ảnh hưởng logic sao chép — chỉ câu hỏi "Tất cả" mới clone).
3. Link "Ghi chú" per câu hỏi (không phải text/textarea) trong Xem trước.
4. Khi Lưu, kiểm câu hỏi thư viện còn tồn tại/không bị khoá — báo "Câu hỏi mã '...' không còn tồn tại/đang bị khóa, vui lòng chọn câu hỏi khác" (Controller:508-530).
5. Update trên mẫu Khoá do người khác đổi → HTTP 423 "Thao tác không thành công. Dữ liệu đã được thay đổi…".
6. Nút "Sao chép" ở trang Xem chi tiết (footer).
7. Định dạng số vi-VN ô nhập số ở Xem trước.
8. Cột "Số câu hỏi" & "Cập nhật" sortable; STT + Mẫu phiếu sticky.
9. Snapshot/"Thông tin bổ sung" trong FormPreview thuộc màn Yêu cầu làm giải pháp, KHÔNG bật ở màn danh mục (ngoài phạm vi HDSD này).
10. DB: form_templates bỏ scope_id/industry_id; application_id nullable; status tinyint default 1; có meta(JSON), created_by/updated_by. Export = FormTemplatesExport (.xls).

## File tham chiếu
FE: `pages/assign/form-templates/{index,add,_id/index,_id/edit}.vue` + `components/{FormBuilder,FormMeta,SectionBuilder,QuestionItem,QuestionLibrary,AddQuestionQuickModal,FormPreview}.vue`.
BE: `Modules/Assign/Http/Controllers/Api/V1/FormTemplateController.php`, `Services/FormTemplateService.php`, `Http/Requests/FormTemplate/FormTemplateRequest.php`, `Entities/FormTemplate.php`, `Transformers/FormTemplatesResource/FormTemplatesResource.php`, `Routes/api.php:280-292`, `Database/Migrations/2026_06_26_100004_*`, `PermissionsTableSeeder.php:949`.
