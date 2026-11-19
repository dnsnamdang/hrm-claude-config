# YCXH — Đồng bộ giao diện popup "Chọn hợp đồng" loại 20/21 giống loại 14

## Bối cảnh
Màn HRM **Yêu cầu xuất hàng** (`pages/finance/product-export-requests`) có nhiều popup chọn hợp đồng
cho các loại xuất khác nhau:
- Loại **14** "Xuất bán hàng" → `FirmContractSearchModal.vue` — **b-modal full-width** (header icon tròn,
  picker-filter bar, b-table cuộn 2 chiều đồng bộ, phân trang, footer "Đóng" ghim đáy).
- Loại **20/21** "Xuất sản xuất hợp đồng / Xuất bán hợp đồng" → `HrmContractSearchModal.vue` — hiện dùng
  `V2BaseModal` (gọn, bảng viết tay) → **khác hình thức với loại 14**.

**Yêu cầu (user chốt Hướng A):** sửa `HrmContractSearchModal.vue` để **giống giao diện** popup loại 14
(`FirmContractSearchModal.vue`) — tức chuyển sang khuôn **b-modal full-width**.

## Quyết định đã chốt
- **Hướng A**: convert `HrmContractSearchModal` sang khuôn b-modal full-width của `FirmContractSearchModal`.
  Đây là **ngoại lệ có chủ đích** với quy ước `modal-popup` (vốn bắt dùng `V2BaseModal`) — user chấp nhận
  để 4 popup chọn HĐ trên màn YCXH đồng nhất. Popup tham chiếu = **loại 14**.
- **GIỮ NGUYÊN data/logic** của Hrm modal, chỉ đổi lớp vỏ UI:
  - Endpoint: `GET assign/product-export-requests/hrm-contracts` (params `type`, `customer_id`, `search`,
    `page`, `per_page`) — **KHÔNG đổi BE**.
  - Props: `type`, `customerId`. Emit: `select(row)`, `close`.
  - Cơ chế mở/đóng: **ref-based** `show()` / `hide()` (parent gọi `this.$refs.hrmContractModal.show()` ở
    `ProductExportRequestForm.vue:2704`) — **KHÔNG** đổi sang prop `:show` như Firm modal.
  - 6 cột: STT · Mã HĐ (`code`) · Khách hàng (`customer_name`) · Ngày ký (`sign_date`) ·
    Ngày hiệu lực (`effective_date`) · Hạn thực hiện (`execution_end_date`).
  - Phân trang `V2BasePagination` + debounce tìm kiếm 300ms.
- **Bộ lọc**: giữ **1 ô tìm** (BE chỉ nhận 1 param `search` gộp mã+KH), đặt trong `picker-filter` bar kèm
  nút "Tìm kiếm" + "Làm mới" cho giống thanh lọc loại 14. KHÔNG tách 2 ô vì BE không hỗ trợ.
- **Không sort server-side** (endpoint `hrm-contracts` không nhận `sort_by`) → b-table để cột thường,
  không `sortable`.
- CSS full-width: định nghĩa **class riêng** `modal-full-width-hrm` trong block `<style>` global của chính
  component (vì Firm modal bị `v-if` theo loại → style global của nó có thể không được inject khi đang ở
  loại 20/21).

## Tham chiếu khuôn
- Khuôn b-modal full-width: `FirmContractSearchModal.vue` (toàn bộ template + `<style>` scoped + global
  `.modal-full-width-firm`, `.header-icon`, `.picker-filter`, `.choose-contract-body`, `.table-shell`,
  scrollSync top/bottom, footer ghim đáy).
- scrollSync util: `@/utils/scrollSync` → `createScrollSyncHandlers`.

## Tasks
- [x] T1. Viết lại `HrmContractSearchModal.vue` theo khuôn b-modal full-width:
  - [x] T1.1 Template: `b-modal` + `#modal-header` (icon tròn + "Chọn hợp đồng" + nút X), `choose-contract-body`,
    `picker-filter` (1 ô tìm + Tìm kiếm + Làm mới), `table-shell` + top/bottom scroll + b-table 6 cột,
    `V2BasePagination`, footer "Đóng" ghim đáy.
  - [x] T1.2 Script: GIỮ props `type`/`customerId`, emit `select`/`close`, **ref-based `show()`/`hide()`**;
    thêm scrollSync handlers (created/bind/unbind), giữ `fetch()` endpoint cũ, debounce 300ms, `pick()`,
    `formatDate()`. b-table fields không `sortable`.
  - [x] T1.3 Style: copy scoped SCSS khuôn Firm + block global `.modal-full-width-hrm`.
- [x] T2. Verify Playwright (http://127.0.0.1:3000): mở YCXH tạo mới → chọn loại 21 "Xuất bán hợp đồng"
  → bấm "Hợp đồng" → popup render ĐÚNG khuôn full-width giống loại 14 (header icon tròn + "Chọn hợp đồng" + X,
  thanh lọc 1 ô tìm + "Tìm kiếm" + "Làm mới", bảng viền 6 cột STT/Mã HĐ/Khách hàng/Ngày ký/Ngày hiệu lực/
  Hạn thực hiện, footer "Đóng" ghim góc phải đáy). Dữ liệu trống ("Không có hợp đồng đủ điều kiện xuất hàng")
  do công ty test chưa có HĐ HRM đủ điều kiện — là điều kiện DỮ LIỆU, không phải lỗi UI. Console chỉ có nhiễu
  HMR/webpack reexport sẵn có của app, KHÔNG có lỗi JS từ component (modal mở + render đủ = lifecycle sạch).
- [ ] T3. Báo user, chờ duyệt commit (CHƯA commit/push khi chưa có yêu cầu).

### Checkpoint — 2026-10-28
Vừa hoàn thành: T1 (viết lại component) + T2 (verify Playwright PASS — popup đồng bộ khuôn loại 14).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt để commit/push nhánh gop_db (hiện CHƯA commit).
Blocked: không — chưa test được luồng click-chọn-dòng vì công ty test chưa có HĐ HRM đủ điều kiện;
logic `pick()`/`hide()` giữ nguyên + bám đúng khuôn Firm modal đã chạy ổn.
