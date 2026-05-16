# Plan — Tách cột Excel xuất Ứng dụng

**Feature:** application-export-split-columns | **Phụ trách:** @manhcuong
**Spec:** [docs/superpowers/specs/2026-04-16-application-export-split-columns-design.md](../../docs/superpowers/specs/2026-04-16-application-export-split-columns-design.md)

## Phase 1: Viết lại Blade template

### BE
- [x] Sửa `hrm-api/resources/views/exports/applications.blade.php`: viết lại `<thead>` với 12 cột (STT, Mã ứng dụng, Tên ứng dụng, Mô tả, Nhóm ngành, Nhóm giải pháp, Lĩnh vực khách hàng, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật)
- [x] Viết lại `<tbody>` dùng **array access** (`$item['code']`, etc.), vì data đã qua Resource — xem code mẫu trong spec section 5.1
- [x] Cột "Nhóm ngành" giữ mapping cũ với `industry_names`, cột "Nhóm giải pháp" giữ mapping cũ với `scope_names`
- [x] Cột Ngày tạo/Ngày cập nhật dùng `explode(' ', $item['created_at'])[0]` để lấy phần ngày `d/m/Y` (vì Resource trả `d/m/Y H:i:s`)
- [x] Cập nhật tất cả `colspan="7"` thành `colspan="12"` (các dòng logo, tiêu đề, dòng trống, dòng "Ngày..., tháng..., năm...")
- [x] Cập nhật các `colspan="6"` (dòng "Người lập", "Ký, họ tên") thành `colspan="11"` để giữ cột cuối riêng
- [x] Gỡ dead import `@php use Carbon\Carbon; @endphp` (không còn dùng)

## Phase 2: Manual test

### QA
- [x] Vào `/assign/application`, click **Xuất Excel** không filter → check đủ 12 cột, data đúng, thứ tự đúng
- [x] Export có filter keyword + scope → file chỉ chứa bản ghi khớp
- [x] Ứng dụng có nhiều scope/industry/customerScope → nối bằng `, ` đúng format
- [x] Ứng dụng không có relationship → cell trống, không lỗi
- [x] Description dài → hiển thị đầy đủ (wrap text)
- [x] Ngày tạo/cập nhật hiển thị `DD/MM/YYYY` (không có giờ)
- [x] Trạng thái hiển thị text `Hoạt động` / `Khóa`
- [x] Người tạo/cập nhật đã nghỉ → cell trống, không crash
- [x] Filter theo `updated_from` + `updated_to` → file chỉ chứa bản ghi trong khoảng ngày
- [x] Filter theo `created_by` / `updated_by` → đúng kết quả
- [x] File mở được trong Excel/LibreOffice → không báo lỗi format, không vỡ layout

## Checkpoint — 2026-04-17
Vừa hoàn thành: Phase 1 (viết lại blade 12 cột) + Phase 2 (manual test passed)
Đang làm dở: Không
Bước tiếp theo: Feature hoàn thành, sẵn sàng merge
Blocked: Không
