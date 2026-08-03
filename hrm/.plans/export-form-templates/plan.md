# Plan — Export phiếu thu thập thông tin ra Excel

Phụ trách: @namdangit

## Phase 1 — Command export

### BE
- [x] Tạo Command `assign:export-form-templates` (`app/Console/Commands/Assign/ExportFormTemplatesCommand.php`)
- [x] Load tất cả FormTemplate + sections/groups/questions (kể cả câu hỏi con) + options
- [x] Sheet "Danh sách phiếu": tổng quan từng phiếu (id, tên, app, trạng thái, số section/câu hỏi)
- [x] Sheet "Chi tiết câu hỏi": flat toàn bộ câu hỏi (section, group, cấp lồng, type, label, code/key, required, visibility, options)
- [x] Lưu file ra `storage/app/exports` + tham số `--path` tuỳ chọn
- [x] Chạy thử trên DB local để xác nhận output (19 phiếu, 254 câu hỏi)

### Checkpoint
Vừa hoàn thành: viết command export
Bước tiếp theo: chạy `php artisan assign:export-form-templates` kiểm tra file
