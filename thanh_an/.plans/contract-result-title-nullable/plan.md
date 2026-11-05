# HĐ — Tab Kết quả: bỏ bắt buộc Tên file

> Người phụ trách: @khoipv — Bắt đầu 05/11/2026

## Yêu cầu
Tab **Kết quả** màn Hợp đồng, bảng "File dữ liệu kết quả hợp đồng": hiện phải nhập Tên file mới lưu được → bỏ bắt buộc.

## Nguyên nhân
- `UpdateContractResultRequest` không có rule cho `title`, FE cũng không chặn.
- Cột `contract_results.title` tạo `NOT NULL` (migration `2025_11_23_215019`) → để trống, `ConvertEmptyStringsToNull` đổi thành null → insert lỗi SQL → "Có lỗi xảy ra".
- Cột `note` từng bị y hệt, đã sửa bằng `2026_03_10_000000_alter_contract_results_note_nullable`.

## Phase 1 — BE
- [x] Migration `alter_contract_results_title_nullable`: `title` → nullable
- [x] Chạy migrate riêng file này

## Phase 2 — FE
- [x] Không cần sửa (không validate FE). Báo cáo file dữ liệu kết quả đã hiển thị `row.title || '---'`.

### Checkpoint — 05/11/2026
Vừa hoàn thành: migration title nullable
Đang làm dở:
Bước tiếp theo: user test lưu dòng không tên file ở tab Kết quả
Blocked:
