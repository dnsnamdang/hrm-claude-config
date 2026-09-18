# Chặn lập báo giá thường trên dự án cha

**Nhánh:** `fix_bug_17_9` (cả 2 repo) · **Phát hiện:** 2026-09-17, khi test #10804 — màn `/assign/quotations/create` vẫn chọn được dự án cha.

Dự án cha không tự lập báo giá (URD `du-an-cha-con`): báo giá của nó là BÁO GIÁ TỔNG (`is_summary = 1`) gộp từ báo giá đã duyệt của dự án con, qua luồng riêng `assign/summary-quotations`. Luồng Yêu cầu làm giải pháp + Giải pháp kỹ thuật đã chặn sẵn, riêng báo giá quên.

- [x] BE: trait `RejectsParentProject` + gắn vào `QuotationStoreRequest` / `QuotationUpdateRequest` (phủ cả `create-and-submit`)
- [x] BE: cờ `for_quotation=1` ở `ProspectiveProjectService::getAll()` lọc dự án cha khỏi dropdown
- [x] FE: `loadMyProjects()` trong `quotations/_id/edit.vue` gọi kèm `for_quotation=1`
- [x] Test 21/21 (`test_block_parent.php`) — chặn tạo/đổi dự án, không phá dự án con / độc lập / báo giá tổng / YC làm giải pháp
- [x] Dữ liệu cũ trỏ vào dự án cha: **để nguyên** (user chốt 2026-09-17)
