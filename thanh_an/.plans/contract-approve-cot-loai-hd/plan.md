# Thêm cột "Loại hợp đồng" — màn Danh sách hợp đồng chờ duyệt

@khoipv — Bắt đầu 30/09/2026

Màn: `/contract/contract/approve` (`hrm-thanhan-client/pages/contract/contract/approve.vue`)

## Phase 1 — FE
- [x] Kiểm tra BE: `ContractResource` đã trả sẵn `type_name` (`Contract::TYPE_NAME`) → không sửa BE
- [x] Thêm cột "Loại hợp đồng" ngay sau "Mã hợp đồng" (đồng bộ thứ tự với màn `contract/contract/index.vue`)
- [x] Sửa colspan dòng "Không có dữ liệu" 8 → 14 cho khớp số cột

### Checkpoint — 30/09/2026
Vừa hoàn thành: thêm cột Loại hợp đồng
Đang làm dở:
Bước tiếp theo: build lại client + hard refresh, test UI
Blocked:
