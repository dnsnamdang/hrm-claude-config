# Plan — Sửa 2 lỗi UI (BOM LIST + popup Thêm hàng hoá)

## Phase 1 — FE
- [x] `utils/helpers.js`: thêm `trimHardSpaces()` — bỏ `&nbsp;`/U+00A0/U+3000/ký tự rộng-0 ở đầu-cuối chuỗi
- [x] BOM LIST: cột "Tên hàng" hết thụt đầu dòng — `BomBuilderEditor.mapProductToRow/buildImportGridRow/overlayImportGridRow` + `BomBuilderTableCard.cleanName()`
- [x] `V2BaseSelect.vue`: chip select chọn nhiều hết tràn ra ngoài ô — bỏ `flex-direction: row-reverse`, chip `inline-block` + × ghim tuyệt đối mép phải + cắt chữ bằng ellipsis

### Checkpoint — 2026-09-16
Vừa hoàn thành: cả 2 fix, chưa chạy thử trên trình duyệt
Đang làm dở: —
Bước tiếp theo: user xác nhận có cần test UI không
Blocked:

## Phase 2 — Nút × xoá nhanh ở dropdown (ảnh 3, màn /assign/industry-groups)
- [x] Rà: base `V2BaseSelect`/`V2BaseSelectInModal` ĐÃ mặc định `allowClear: true` — màn này khai đè `:allowClear="false"`
- [x] `AddScopeModal.vue`: gỡ `:allowClear="false"` ở ô "Lĩnh vực Công ty kinh doanh"
- [x] `AddScopeModal.vue`: GIỮ tắt × ở ô "Trạng thái" + ghi lý do cạnh dòng code (user chốt)
- [x] `V2BaseSelect.vue`: ẩn `.select2-selection__clear` khi ô bị khoá (select2 4.0.13 vẫn render × lúc disabled)
- [x] `.claude/skills/select-and-input-state/SKILL.md`: thêm mục 1b — mặc định bật ×, 2 nhóm ngoại lệ, ô khoá không hiện ×
- [ ] 32 chỗ `:allowClear="false"` còn lại ở các màn cũ — user chốt KHÔNG sửa đại trà lần này

### Checkpoint — 2026-09-16
Vừa hoàn thành: Phase 2, code nằm ở worktree `HRM/worktrees/tpe-client` (nhánh `tpe`)
Bước tiếp theo: user xác nhận có cần test UI không
Blocked:

## Phase 3 — Test UI (Playwright, FE :3005 + BE :8005 từ worktree tpe)
- [x] Ảnh 3 — Sửa nhóm ngành: chọn Lĩnh vực → hiện ×; bấm × → v-model về null, ô về placeholder
- [x] Ảnh 3 (nghịch) — xoá rỗng rồi Lưu → "Bắt buộc phải chọn" dưới ô, popup không đóng
- [x] Ảnh 3 — ô Trạng thái KHÔNG có × (đúng thiết kế); màn Xem chi tiết: × có trong DOM nhưng bị ẩn (rule mới)
- [x] Ảnh 2 — chip select nhiều: chọn 2 option không mất lựa chọn; chữ cắt ellipsis bên PHẢI, × trong khung
- [x] Ảnh 2 (đối chứng) — áp lại CSS row-reverse cũ ngay trên trang: chữ chạy ra ngoài mép trái 279px → xác nhận đúng nguyên nhân
- [x] Ảnh 2 — bấm × trên chip vẫn xoá đúng 1 chip, ô khác giữ nguyên
- [x] Ảnh 1 — chèn 4 ký tự NBSP vào đầu tên hàng trong DB local: API trả charCode 160 ở đầu, UI render indent 0px → fix ăn
- [x] Dọn môi trường: hoàn nguyên tên hàng id=2767, trả company_role tài khoản về 4

### Checkpoint — 2026-09-16
Vừa hoàn thành: test xong cả 3 ảnh trên nhánh tpe, tất cả PASS
Bước tiếp theo: chờ user duyệt để commit
Blocked:
