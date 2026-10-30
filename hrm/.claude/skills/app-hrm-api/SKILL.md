---
name: app-hrm-api
description: Cách TPE_APP nói chuyện với hrm-api — lớp ApiService (authAppServerClient), mapper trả object vs trả mảng (bẫy danh sách ra 0 dòng), model từ JSON an toàn, lỗi 422 theo trường, quyền lấy từ BE, chữ + màu trạng thái do BE trả, khi nào PHẢI sửa BE ở hrm-api (và theo skill HRM nào), làm BE + web + app cùng lúc, dữ liệu thử local / dev. Dùng khi thêm API cho app, app hiện 0 dòng dù API có dữ liệu, cần thêm trường / endpoint, nghiệp vụ app khác web.
---

# App ↔ hrm-api — TPE_APP

App không có BE riêng: mọi dữ liệu từ `HRM/hrm-api` (Laravel). Web `hrm-client` gọi CÙNG API → nghiệp vụ app =
nghiệp vụ web. Thiếu dữ liệu / sai nghiệp vụ → **sửa ở hrm-api**, không vá ở app.

## 1. Lớp gọi API (mẫu `MyTodoApiService` — `data/lib/src/repository/source/remote/api/api_services/app_server/my_todo_api_service.dart`)

```dart
@LazySingleton()
class XxxApiService {
  Future<DataResponse<Map<String, dynamic>>> _call(RestMethod m, String path, {Map<String, dynamic>? query, Map<String, dynamic>? body}) =>
      authAppServerClient.request(method: m, path: path, queryParameters: query, body: body,
          successResponseMapperType: SuccessResponseMapperType.dataResponse,   // data là OBJECT
          errorResponseMapperType: ErrorResponseMapperType.message, decoder: _safeMap);

  // data là MẢNG → dataResponse KHÔNG đọc được (ra 0 dòng, không báo lỗi) → đọc json gốc:
  Future<List<Map<String, dynamic>>> _getList(String path, [Map<String, dynamic>? q]) =>
      authAppServerClient.request<List<Map<String, dynamic>>, List<Map<String, dynamic>>>(method: RestMethod.get, path: path,
          queryParameters: q, successResponseMapperType: SuccessResponseMapperType.jsonObject,
          errorResponseMapperType: ErrorResponseMapperType.message, decoder: (json) => _mapList(json['data']));
}
```

- Đường dẫn bắt đầu `v1/...` (vd `v1/assign/my-todo`). Mảng query: `'types[]': list`. Ngày gửi `Y-m-d`, giờ `H:i`.
- Đăng ký DI bằng `@LazySingleton()` → chạy `make gen` (build_runner) cập nhật `di.config.dart`; lấy bằng `getIt<XxxApiService>()`.
- Màn mới gọi thẳng ApiService (Mytodo) hoặc qua repository + use case (màn BLoC cũ) — theo `app-new-screen`.

## 2. Model

- Model nhỏ / chỉ đọc: class thường + `factory fromJson` đọc an toàn (`'${j['x'] ?? ''}'`, `int.tryParse`,
  `_date()` nhận cả `Y-m-d` lẫn `Y-m-d H:i:s`) — mẫu `WorkItem` (`.../api/model/work_item.dart`).
- Model lớn / dùng nhiều nơi: freezed + json theo `app-new-model`.
- Không map số trạng thái → chữ / màu ở app: BE trả `status_text` + `status_color` (mã hex hoặc tên nhóm màu),
  app chỉ quy về 9 màu chuẩn nếu BE trả tên nhóm (`statusColorOf`).

## 3. Lỗi

- Lỗi lưu: `MeetingSaveError.from(e)` → `.fields` (Map trường → câu) tô đỏ đúng ô, `.summary` cho snackbar
  (`app-form` mục 3). Câu lỗi nguyên văn BE (lang file vi của hrm-api), không viết lại ở app.
- Lỗi tải danh sách / chi tiết: hiện câu BE qua `AppEmptyWidget(title:)` / `MeetingLoadError`, giữ kéo tải lại.
- 403: ẩn tính năng (quyền lấy từ `currentUser.permissions` / cờ BE), không để user bấm rồi mới báo.

## 4. Quyền

- Tên quyền = quyền HRM (guard `api`, `PermissionsTableSeeder`). App kiểm bằng
  `currentUser.permissions.map((e) => e.name)` cho menu / nút tạo; thao tác trên bản ghi đọc cờ BE (`can_edit`…).
- Cờ quyền khởi tạo `false` (fail-closed). Quyền mới → thêm ở seeder hrm-api (skill `permission-seeder`), admin
  gán cho vai trò; đăng nhập lại app mới nhận quyền mới.

## 5. Khi phải sửa BE (hrm-api)

Đọc skill HRM tương ứng TRƯỚC khi sửa BE: `notification-convention` (thông báo), `permission-seeder` (quyền),
`form-validate` (rule validate, không tự viết messages()), `entity-history` (lịch sử), `list-page` (phạm vi
theo cấp). Quy tắc CLAUDE.md HRM vẫn áp cho phần BE (BaseModel, eager load, index, không N+1…).

- Thêm trường cho app → thêm vào Resource dùng chung (web cũng nhận được), không làm endpoint riêng cho app
  nếu web đã có endpoint tương đương.
- Nghiệp vụ đổi → sửa 1 chỗ ở BE cho cả web + app; kiểm cả màn web tương ứng (vd hạn phiếu đổi → tab danh sách
  web và app cùng đổi). Làm xong cả 3 repo: ghi plan `HRM/.plans/<feature>/plan.md`, đẩy từng repo khi user cho.
- Migration DDL không bọc transaction; route mới trên prod cần `route:cache` (deploy `~/build_tpe.sh` đã chạy).

## 6. Môi trường + dữ liệu thử

| Flavor app | Trỏ API |
|---|---|
| `tpeLocal` (simulator) | `http://127.0.0.1:8000` = `HRM/hrm-api` nhánh develop, DB `local_hrm_erp` |
| `tpeDev` (TestFlight "Tân Phát ERP-HRM") | dev-hrm.eteksofts.com, DB `hrm_erp_test` |
| `tpeProd` | hrm.eteksofts.com — KHÔNG ghi dữ liệu thử |

- Dữ liệu thử: local + dev ghi thoải mái (prod phải hỏi); đặt tên có tiền tố `[TEST-…]` để dễ dọn.
  Tài khoản: namdangit@gmail.com (user 13, employee_info 6). Bẫy dev: bình luận task lưu bảng `comments`
  (không phải `task_comments`), file đính kèm ở bảng `files` (`table='tasks'`).
- Gọi thử API bằng curl với JWT từ `v1/users/auth/login` trước khi đổ lỗi app.
