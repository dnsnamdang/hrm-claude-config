# Popup CHỌN bản ghi — số dòng/trang 10 / 20 / 50 / 100

**Người phụ trách:** @junfoke — 2026-10-06 · Nhánh `gop_db` (hrm-client)

## Mục tiêu
User chốt 06/10/2026 (theo QA #11524): mọi **popup chọn** (chọn hàng hoá, khách hàng, phiếu nguồn,
hợp đồng, nhân sự…) có số dòng/trang **mặc định 10, chọn được 10 / 20 / 50 / 100**. Trước đó các
popup mỗi cái một kiểu: `[20, 50, 100]` mặc định 20, `[10, 20, 50]`, `[10, 25, 50, 100]`, hoặc không
truyền nên ra mặc định màn danh sách 5 / 10 / 20 / 50 / 100.

## Quyết định
- Nguồn duy nhất: `utils/pickerPagination.js` (`PICKER_PAGE_SIZE_OPTIONS`, `PICKER_DEFAULT_PAGE_SIZE`).
  Không sửa default của `V2BasePagination` (đó là chuẩn màn danh sách).
- Popup chỉ XEM (lịch sử, drill báo cáo, Upcoming/LateTasks) KHÔNG thuộc phạm vi.
- Popup không có phân trang (tải 1 lần) KHÔNG thuộc phạm vi.
- Màn cũ (không dùng V2Base) không sửa — skill `new-screens-sweep` mục 1.
- Tài liệu: skill `modal-popup` §4b, `list-page` mục Số dòng/trang, `erp-to-hrm-screen` checklist D.
