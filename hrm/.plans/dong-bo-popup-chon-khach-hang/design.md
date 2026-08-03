# Đồng bộ popup chọn khách hàng với màn danh sách Khách hàng

Người phụ trách: @namdangit — 2026-07-02

## Mục tiêu

Đồng nhất logic lọc, sắp xếp, cột hiển thị và tìm kiếm giữa màn danh sách Khách hàng (/assign/customers) và popup chọn KH tại: Tạo meeting (Meetings → Lịch meeting) + Tạo dự án tiền khả thi (QLDA TKT → Dự án).

## Hiện trạng & quyết định

- Cả 2 popup dùng chung 1 component `components/modals/ChooseErpCustomerModal.vue`, gọi CÙNG endpoint `GET assign/customers` với màn chính → chỉ sửa FE modal, BE giữ nguyên.
- Sắp xếp đã trùng sẵn (id desc = mã mới nhất).
- **3 quyết định (theo khuyến nghị, user AFK khi hỏi — đảo 2 rule cũ của feature customer-individual-no-contact):**
  1. **Bỏ `hide_individual`** — popup hiện cả KH cá nhân, tìm được bằng mã/tên/SĐT như màn chính (trước: ẩn, chỉ hiện khi search đúng full SĐT).
  2. ~~Bỏ `phone_exact_bypass`~~ → **USER CHỐT GIỮ LẠI** (2026-07-02): search đúng full SĐT vẫn hiện KH ngoài phạm vi quyền xem.
  3. **Popup cố định `status=1`** (chỉ KH Hoạt động — không chọn KH khóa cho meeting/dự án mới); màn chính giữ nguyên filter Trạng thái tự do.
- Cột popup: STT, Mã KH - Tên KH (+ tên viết tắt), Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP — **USER CHỐT bỏ cột Trạng thái** (popup chỉ hiện KH Hoạt động nên thừa).
- 2 flag cũ vẫn còn trong `CustomerService::index` (opt-in, không ai gửi) → revert = đổi params FE.

## Verify

BE: main = popup = 41.209 KH Hoạt động, top-5 id trùng thứ tự (popup cũ chỉ 11.209). AC4: search mã KH cá nhân + SĐT đều khớp màn chính. UI Playwright: 2 popup 9 cột PASS, total khớp, search PASS. Bypass re-verify user quyền thấp id=25: đúng SĐT → thấy KH ngoài quyền.

Spec chi tiết: docs/superpowers/specs/2026-07-02-dong-bo-popup-chon-khach-hang-design.md
