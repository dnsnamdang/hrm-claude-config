# Design — Bổ sung cột "Phương án xử lý" cho biên bản cuộc họp

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-05
**Module:** Assign (Giao việc) — màn `assign/meeting/create` + `edit` + màn in

## Mục tiêu

Thêm 1 trường text `solution` (Phương án xử lý) vào mỗi dòng biên bản cuộc họp, hiển thị ngay **sau cột "Nội dung / Vấn đề trao đổi"**, đồng bộ ở 3 nơi: màn nhập (create/edit), file Excel export, và màn in.

## Quyết định đã chốt (brainstorming 2026-06-05)

1. **Không bắt buộc nhập** — nullable, không validate, không viền đỏ.
2. **Bố cục FE (grid 12 cột):** STT 1 · **Nội dung 3 · Phương án 2** · Đề xuất 2 · Thực hiện 2 · Hạn 2.
3. **Đồng bộ cả Excel** — file export thêm cột tương ứng.

## Scope thay đổi

### 1. Database
- Migration mới `add_solution_to_meeting_reports_table`: thêm cột `solution` kiểu `text` nullable, `->after('content')`, `comment('Phương án xử lý')`.
- Cột nullable → bản ghi biên bản cũ hiển thị trống, không ảnh hưởng dữ liệu hiện có.

### 2. Model `MeetingReport.php`
- Thêm `'solution'` vào `$fillable` (sau `'content'`).
- `syncReports()` mass-assign theo `$fillable` → tự lưu, **không sửa** service.
- `MeetingResource` trả nguyên `reports` → FE edit/show tự nhận, **không sửa** transformer.

### 3. Request validation
- `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`: thêm `reports.*.solution => nullable|string` (chỉ khi 2 request đã khai báo rule cho `reports.*` — kiểm tra lúc implement; nếu không có thì bỏ qua).

### 4. FE `MeetingReport.vue` (màn nhập)
- Header: `col-5` "Nội dung" → `col-3`, thêm `<div class="col-2">Phương án xử lý</div>` ngay sau.
- Mỗi dòng: cột Nội dung `col-5` → `col-3`, thêm ô `col-2` với `V2BaseTextarea v-model="r.solution" rows="2"` (không `<Required />`, không error block).
- `addReport()`: thêm `solution: ''` vào object mặc định.

### 5. FE Excel export (cùng file `MeetingReport.vue`)
- Bảng report đổi từ 5 → 6 cột (`A–F`): `['STT','Nội dung / Vấn đề trao đổi','Phương án xử lý','Người đề xuất','Người thực hiện','Hạn dự kiến']`.
- Cập nhật `worksheet.columns` (+1 width), các `mergeCells(...:E...)` → `...:F...`, block info/section dùng `:E` → `:F`.
- Phần ghi dữ liệu report: dịch index cột — `C=solution`, `D=proposer_name`, `E=executor_name`, `F=expected_deadline`. Rà kỹ tránh lệch cột.

### 6. Màn in — blade `meeting_record.blade.php`
- Khung cột "Phương án xử lý (Solution plan)" **đã có sẵn** (header dòng 193) + ô `<td>` trống (dòng 204).
- Chỉ cần fill `<td>` dòng 204: `{!! nl2br(e($report->solution ?? '')) !!}`.

## Điểm cần lưu ý

- Excel export là phần sửa nhiều dòng nhất (dịch index cột + nhiều `mergeCells`) → rủi ro lệch cột, rà từng dòng khi implement.
- Migration: theo convention project cần PHPDoc trên `up()/down()` theo file mẫu chuẩn — kiểm tra file mẫu trước khi viết.
- Không sửa hàm dùng chung (`syncReports`, `MeetingResource`) — chỉ thêm field qua fillable.

## Files dự kiến đụng tới

| # | File | Loại |
|---|------|------|
| 1 | `hrm-api/Modules/Assign/Database/Migrations/*_add_solution_to_meeting_reports_table.php` | Mới |
| 2 | `hrm-api/Modules/Assign/Entities/Meeting/MeetingReport.php` | Sửa (fillable) |
| 3 | `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php` | Sửa (nếu có rule reports.*) |
| 4 | `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php` | Sửa (nếu có rule reports.*) |
| 5 | `hrm-client/pages/assign/meeting/components/MeetingReport.vue` | Sửa (UI + Excel) |
| 6 | `hrm-api/resources/views/exports/meeting_record.blade.php` | Sửa (fill td) |
