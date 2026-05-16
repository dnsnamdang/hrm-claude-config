# Spec — Đồng bộ CKEditor loader cho Self-Notification

**Ngày:** 2026-04-15
**Feature:** self-notification-ckeditor-loader
**Loại:** FE-only, thay đổi 1 dòng

## Bối cảnh

Trên hệ thống có 2 màn dùng CKEditor với bảng biến bên cạnh:

| Màn | URL | Loader hiện tại |
|---|---|---|
| Chi tiết mẫu in | `/decision/category/print_templates/:id/edit` | `$loadCKEditorPrint` |
| Nội dung self-notification | `/human/self-notification/add` (và edit/approve/show) | `$loadCKEditor` |

Hai loader có config toolbar/plugin khác nhau. Yêu cầu của user: editor của self-notification hiển thị giống "chi tiết mẫu in" → dùng cùng loader.

## Quyết định

Đổi `$loadCKEditor` → `$loadCKEditorPrint` trong component `SelfNotificationForm.vue`.

Chọn phương án này (thay vì đổi print template sang loader khác) vì:
- Print template là màn gốc thiết kế cho soạn nội dung in, config của nó là "canonical"
- User chỉ yêu cầu self-notification giống print template, không yêu cầu ngược lại

## Thay đổi chi tiết

**File:** `hrm-client/pages/human/self-notification/components/SelfNotificationForm.vue`

**Dòng 314 (trong `mounted()`):**

```diff
- this.$loadCKEditor(this.$refs.editor).then((editor) => {
+ this.$loadCKEditorPrint(this.$refs.editor).then((editor) => {
```

Không đụng các phần khác của file (data `editorOptions` cục bộ có thể không còn áp dụng nhưng không xóa — loader mới sẽ tự quyết config).

## Phạm vi ảnh hưởng

Component `SelfNotificationForm.vue` được import vào 4 trang:

| Trang | Prop `isShow` | Tác động |
|---|---|---|
| `add.vue` | false | Editor dùng loader mới khi tạo mới |
| `_id/edit.vue` | false | Editor dùng loader mới khi sửa |
| `_id/approve.vue` | (tùy) | Editor dùng loader mới khi duyệt |
| `_id/show.vue` | true | Editor ở chế độ disabled, loader mới |

Không có downstream BE/DB/migration.

## Không trong scope

- Không thêm click-to-insert biến cho self-notification (giá trị tốt nhưng user chưa yêu cầu)
- Không đồng bộ style sticky-header / hover / cursor-pointer cho bảng biến
- Không refactor `typeLabel` helper
- Không đổi loader ở các màn khác dùng `$loadCKEditor`

## Rủi ro & giảm thiểu

| Rủi ro | Giảm thiểu |
|---|---|
| Toolbar `$loadCKEditorPrint` thiếu tính năng mà người soạn self-notification quen dùng (image resize, font, background color...) | User đã xác nhận chấp nhận thay đổi toolbar. Nếu phát sinh phản hồi, hot-fix sau |
| Content đã lưu dạng HTML từ editor cũ có thể render khác ở editor mới | `$loadCKEditorPrint` là CKEditor → nhìn chung tương thích HTML. Verify bằng mở 1 bản ghi cũ ở `/show` |
| `editorOptions` data trong component (toolbar Quill-style) trở nên thừa | Để lại, không xóa — có thể còn được reference. Cleanup ở task khác nếu cần |

## Verification

- [ ] Vào `/human/self-notification/add` → editor load, toolbar hiển thị giống `/decision/category/print_templates/:id/edit`
- [ ] Soạn nội dung, chọn Mẫu in từ dropdown → template đổ đúng vào editor (`onChangeTemplate`)
- [ ] Submit lưu thành công
- [ ] Mở 1 bản ghi cũ tại `/human/self-notification/:id/show` → nội dung render đúng
- [ ] Màn `/human/self-notification/:id/edit` → sửa và lưu OK
