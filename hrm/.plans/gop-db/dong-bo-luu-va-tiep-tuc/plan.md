# Plan — Đồng bộ nút "Lưu và tiếp tục" (Redmine #11177)

Nhánh: `gop_db` (cả `hrm-client`) · @junfoke · Bắt đầu 2026-09-05
Issue: http://quanly.dnsmedia.vn/issues/11177

> Chỉ sửa FE `hrm-client`. Không đụng BE, không đổi API, không đụng DB.

## Phase 1 — Hạ tầng dùng chung

- [x] `utils/mixins/saveAndContinueMixin.js` — cho COMPONENT FORM: `runSaveAndContinue(fn)` bật cờ
      `continueAfterSave`, `afterSaveRedirect(url)` thay cho `this.$router.push(url)` ở cuối hàm lưu
- [x] `utils/mixins/saveAndContinuePageMixin.js` — cho TRANG VỎ `create.vue`: `formKey` + `onSavedAndContinue()`
      (remount form con, cuộn lên đầu trang)

## Phase 2 — Popup danh mục (3 màn trong danh sách issue)

- [x] `pages/finance/works/WorkModal.vue` — Danh mục vụ việc
- [x] `pages/finance/cost-debts/CostDebtModal.vue` — Danh mục mã phí
- [x] `pages/finance/source-capitals/SourceCapitalModal.vue` — Danh mục nguồn vốn (thêm luôn guard chống click đúp)

Cách làm: copy `components/modal/customer-care/level-modal.vue` — nút `secondary` "Lưu và tiếp tục"
`v-if="!isView && !id"`, `submit(true)` → `reset()` + `markFormPristine()` ở `nextTick`, giữ popup mở.
Nút Lưu đổi `@click="submit"` → `@click="submit(false)"` (nếu để nguyên, MouseEvent rơi vào tham số
`continueAfterSave` → luôn chạy nhánh tiếp tục).

## Phase 3 — Trang Tạo mới (26 màn Tài chính + CSKH)

Mỗi màn 4 chỗ sửa: (1) trang vỏ `:key="formKey"` + `@savedAndContinue` + page mixin ·
(2) form gắn `saveAndContinueMixin` · (3) footer thêm nút/cờ `submit_and_continue` chỉ ở chế độ Tạo ·
(4) cuối hàm lưu đổi `$router.push(...)` → `afterSaveRedirect(...)`.

**CSKH**

- [x] Danh mục công việc / lỗi thiết bị
- [x] Danh mục gói bảo dưỡng (ẩn nút khi đang nhân bản `copy_from`)
- [x] Phiếu yêu cầu bảo hành / sửa chữa
- [x] Phiếu xử lý yêu cầu (ẩn khi lập từ `?warranty_repair_request_id`)
- [x] Phiếu cung cấp thông tin (ẩn khi lập từ `?warranty_repair_handle_request_id`)
- [x] Báo giá dịch vụ (ẩn khi lập từ `?wr_information_id` / `?copy`) — form `extends` form Phiếu cung
      cấp thông tin nên KHÔNG khai lại mixin

**Tài chính — nhóm hàng giữ (đúng danh sách issue)**

- [x] Phiếu yêu cầu giữ hàng
- [x] Phiếu yêu cầu gia hạn giữ hàng
- [x] Phiếu yêu cầu hủy hàng giữ
- [x] Phiếu yêu cầu điều chuyển hàng giữ
- [x] Phiếu hủy hàng giữ (chỉ hiện khi KHÔNG vào từ `?request_id`)
- [x] Phiếu yêu cầu xuất giữ (mượn hàng)

**Tài chính — nhóm nhập/xuất/chuyển hàng**

- [x] Phiếu yêu cầu nhập hàng
- [x] Phiếu chuyển hàng nhập thẳng
- [x] Phiếu nhập hàng
- [x] Phiếu yêu cầu điều chuyển hàng hoá
- [x] Phiếu yêu cầu xuất hàng (luồng lưu nằm ở trang vỏ → trang vỏ tự tăng `formKey`, không dùng mixin)

**Tài chính — nhóm chứng từ tiền**

- [x] Phiếu báo có
- [x] Đề nghị thu tiền
- [x] Phiếu thu tiền (ẩn khi lập từ đề nghị thu)
- [x] Đề nghị thanh toán
- [x] Phiếu chi tiền (ẩn khi lập từ đề nghị chi)
- [x] Ủy nhiệm chi (ẩn khi lập từ đề nghị chi)
- [x] Đề nghị hạch toán bổ sung
- [x] Đề nghị điều chỉnh công nợ
- [x] Phiếu điều chỉnh công nợ

## Không làm (đã rà, không có chỗ gắn nút) — nêu rõ để QA không báo thiếu

- [x] Cập nhật nhanh giá dịch vụ · Danh sách hàng giữ · Danh mục serial thiết bị làm dịch vụ →
      **không có chức năng Tạo mới**
- [x] Phiếu xuất hàng · Phiếu nhập kho · Phiếu xuất kho · Phiếu giữ hàng (kho) → màn Tạo **bắt buộc đi
      từ một yêu cầu nguồn trên URL**; lưu xong "tiếp tục" sẽ nạp lại đúng yêu cầu vừa xử lý → tạo phiếu trùng

## Kiểm thử

- [x] Parse lại toàn bộ 55 file đã sửa bằng `vue-template-compiler` + `@babel/parser` — 0 lỗi cú pháp
- [x] Kiểm tra không file nào bị trộn line ending (CRLF giữ nguyên)
- [x] Verify tay trên dev server riêng `localhost:3009` (cổng 3000 là worktree khác, 3001 là elearning): 1 popup danh mục + 1 trang phiếu (lưu xong form trắng, ở lại màn,
      không hiện popup "chưa lưu")

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ code Phase 1-3 (2 mixin mới + 3 popup + 26 trang Tạo mới) + verify tay.
Verify (dev server riêng cổng 3009, tài khoản DNS Admin):
  · `/finance/works` — popup Tạo có đủ 3 nút Lưu · **Lưu và tiếp tục** · Đóng; bấm Lưu và tiếp tục →
    POST 201, danh sách tự tải lại, popup GIỮ NGUYÊN, 2 ô nhập về trắng, tiêu đề vẫn "Tạo vụ việc";
    bấm Đóng sau đó KHÔNG hỏi "chưa lưu".
  · `/finance/prepick-cancel-requests/create` — footer đúng thứ tự: Lưu nháp · Lưu và gửi duyệt ·
    **Lưu và tiếp tục** · Quay lại.
  · `/customer-care/device-errors/create` — nút hiện đúng; lưu thiếu trường → 422, form GIỮ NGUYÊN dữ
    liệu (không reset khi lưu lỗi); kích hoạt `onSavedAndContinue()` → `formKey` 0→1, form về trắng,
    vẫn ở nguyên màn Tạo. Console chỉ còn warning `rows="1"` có sẵn từ trước, không phải do thay đổi này.
  · 55 file parse sạch (`vue-template-compiler` + `@babel/parser`), line ending CRLF nguyên vẹn.
Đang làm dở: không.
Bước tiếp theo: user review giao diện; nếu OK thì commit lên `gop_db`.
Ghi chú: dev DB local có 1 bản ghi rác do test — vụ việc mã `TEST770262`, xoá tay khi tiện.
Blocked:
