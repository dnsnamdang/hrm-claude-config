# Plan — Danh mục Lĩnh vực công ty kinh doanh (Redmine #11184)

Nhánh `tpe`. Phụ trách: @cuong61n. Xử lý 4 phản hồi của QA ngày 17/09/2026.

## Phản hồi #13–#15
- [x] BUG 1 — Mã: hậu tố phải ĐỦ 4 ký tự (`LVCTKD.XXXX`), trước đây `{1,4}` nên lưu được mã ngắn hơn.
      Sửa 4 nơi: regex FormRequest, validate import ở BE, rule `lvctkd_code` ở modal, validate import ở FE.
      ⚠️ Mô tả task ban đầu ghi "tối đa 4 ký tự" — làm theo phản hồi mới nhất của QA (đủ 4).
- [x] BUG 2 — Form Sửa không được khoá bản ghi đang có Nhóm ngành hoạt động dùng:
      FE ẩn hẳn option "Khoá" (theo cờ `is_can_lock_update`), BE thêm `assertCanChangeStatus()` chặn thật ở
      `update` + `updateOrCreate` (trước chỉ endpoint `lock` mới kiểm).
- [x] BUG 3 — Màu nút theo skill `button-convention`: popup Xóa dùng prop `danger` (nút đỏ + icon cảnh báo),
      Xuất Excel `status="success"`, Import Excel `status="warning"` + icon `ri-upload-line`, icon Xoá dòng `ri-delete-bin-line`.
- [x] BUG 4 — Tự cập nhật ẩn/hiện Xoá/Khoá theo luồng Nhóm ngành: thêm mixin dùng chung
      `utils/mixins/refreshOnWindowFocus.js`, áp cho cả màn Lĩnh vực và màn Nhóm ngành.
      (Điều hướng SPA trong cùng tab vốn đã đúng — lỗi chỉ xảy ra khi mở 2 tab / 2 người thao tác.)

## Kiểm thử local (UI thật + API)
- BUG 1: hậu tố 2 ký tự → lỗi đỏ dưới ô, không lưu; đủ 4 ký tự → lưu OK; API trả 422 đúng câu.
- BUG 2: form Sửa chỉ còn option "Hoạt động"; ép `status=2` qua API → 400 "Dữ liệu đang được sử dụng",
  DB không đổi; sau khi Nhóm ngành bị khoá thì khoá được (200).
- BUG 3: popup Xóa nền `rgb(220,38,38)` + icon cảnh báo đỏ; Xuất Excel xanh lá, Import Excel cam.
- BUG 4: đổi trạng thái Nhóm ngành ở ngoài → quay lại tab thì nút Khoá ẩn/hiện đúng cả 2 chiều;
  3 sự kiện focus liên tiếp chỉ bắn 1 request; đang mở modal thì KHÔNG tải lại (0 request, dữ liệu đang nhập còn nguyên).

## Rà lại button-convention (18/09/2026)
- [x] Modal Thêm/Sửa: nút Đóng `light` → `tertiary`, bổ sung `size="sm"`, đổi `:disabled` → `:interactable="!isSubmitSave"`
      (V2BaseButton không nhận `disabled` → trước đó nút vẫn bấm được khi đang lưu), text `Lưu & Tiếp tục` → `Lưu và tiếp tục`.
- [x] Chuẩn hóa chính tả kiểu mới toàn màn: `Khoá/Mở khoá/Xoá` → `Khóa/Mở khóa/Xóa` (FE index.vue + modal;
      BE `status_text` và message 423 của `InternalBusinessScopeService`).
- [x] BUG 1 (phản hồi #13) — đưa ô Mã về **đúng khuôn danh mục Nhóm ngành** (`ScopeRequest` + `industry-groups/AddScopeModal.vue`)
      thay cho rule tự chế: FE bỏ `Validator.extend('lvctkd_code')` + `maxlength`, chỉ còn `V2BaseCodeInput prefix="LVCTKD."`
      placeholder "Nhập 4 ký tự", lỗi lấy từ 422 của BE; BE đổi `regex {4}` + closure → `size:11` (tiền tố + 4) đứng trước
      `regex` bộ ký tự, message "Vui lòng nhập 4 ký tự" giống Nhóm ngành. Vẫn giữ regex có tiền tố để không mất chốt `LVCTKD.`.
- [x] Bỏ HẾT validate FE ở modal (cả ô Tên): gỡ `v-validate` / `data-vv-*`, `$validator.validateAll()`, `focusFirstError()`
      và `this.errors` — modal không chặn nữa, chỉ hiện lỗi 422 của BE dưới từng ô (đúng khuôn Nhóm ngành).
- [x] Ô Trạng thái trong modal theo khuôn Nhóm ngành: giữ đủ 2 option cố định (Hoạt động / Khóa),
      bản ghi chưa được phép khóa thì **disable cả ô** (`isShow || isLocked || !isCanLockUpdate`)
      thay vì cắt bớt option "Khóa" như trước. Gỡ nốt `$validator.reset()` còn sót.
- [x] Fix: ô Trạng thái bị kẹt sau khi chọn "Khóa" — điều kiện disable trước đó xét `data.status === 2`
      (giá trị user VỪA chọn) nên vừa chọn Khóa là ô tự xám, không chọn ngược lại được.
      Đổi sang `isCannotLock = status === 1 && !isCanLockUpdate` đúng khuôn Nhóm ngành.
