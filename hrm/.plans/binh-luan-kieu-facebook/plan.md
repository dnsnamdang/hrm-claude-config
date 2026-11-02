# Bình luận kiểu Facebook — Nhiệm vụ & Vấn đề (web + app) — @cuong61n

Phạm vi: bình luận của Nhiệm vụ (task) và Vấn đề (issue). Web `hrm-client/components/comments/*`, app `TPE_APP/app/lib/ui/task/task_comments_page.dart`, BE `Modules/Assign/.../{Task,Issue}CommentController`. Nhánh `develop`.
Đối chiếu hiện trạng (31/10/2026): BE đã có thông báo reply/mention/react và giới hạn 3 cấp; chỉ chủ bình luận được sửa/xoá; chưa có `is_edited`, chưa phân trang.

## Đợt 1 — BE nhỏ + web
- [x] (31/10) BE: thêm `is_edited` vào `formatComment` (Task + Issue)
- [x] (31/10) Web: giờ tương đối ("5 phút trước"), rê chuột hiện giờ đầy đủ
- [x] (31/10) Web: nhãn "Đã chỉnh sửa"
- [x] (31/10) Web: gom Sửa/Xóa vào menu ⋯; dòng hành động gọn (giờ · Thích · Trả lời)
- Web: Enter gửi/Shift+Enter đã có sẵn từ trước — bỏ. Ô soạn gọn: chưa làm
- [x] (31/10) Web: xóa bình luận con tại chỗ (không tải lại cả cây) + đồng bộ reaction khi load lại; thêm nút icon 👍 một chạm (kèm số lượt, thay chip 👍)
- [ ] Web: thumbnail ảnh đính kèm

## Đợt 2 — App
- [x] (31/10) App: nhãn "Đã chỉnh sửa"
- [x] (31/10) App: icon 👍 một chạm kèm số lượt (bỏ nút chữ "Thả cảm xúc", chọn cảm xúc bằng nhấn giữ icon 👍; ⋯ Sửa/Xóa chuyển xuống cuối dòng hành động)
- [x] (31/10) App: giờ tương đối ("Vừa xong", "5 phút trước", "2 giờ trước"), chạm vào giờ hiện giờ đầy đủ
- [x] (31/10) App: nhấn giữ icon 👍 mở bảng chọn cảm xúc; chạm số lượt / nhấn giữ chip → bảng "Cảm xúc" liệt kê ai đã thả
- [x] (31/10) App: "Xem N phản hồi" thu gọn nhánh con
- [ ] App: màn chi tiết task dùng `comments_count` thay vì tải cả cây để đếm

## Đợt 3 — App chuyên nghiệp hơn + ghim/đã giải quyết/phân trang (31/10/2026, bỏ "tự cập nhật")
- [x] (31/10) App: ảnh đính kèm thumbnail trong bong bóng (1 ảnh to, nhiều ảnh lưới) + thumbnail ở ô soạn (có ✕)
- [x] (31/10) App: gửi tức thì (đang gửi / lỗi → Thử lại · Xóa). Sửa kèm: thiếu header `Accept: application/json` làm BE trả 302 khi 422 và app tưởng gửi thành công (bình luận biến mất không báo lỗi) — đã thêm cho tạo + sửa bình luận
- [x] (31/10) App: nhấn giữ bong bóng và nút ⋯ dùng chung 1 menu (Sao chép · Trả lời · Sửa · Ghim · Đã giải quyết · Xóa theo quyền)
- [x] (31/10) App: cụm cảm xúc ở góc bong bóng
- [x] (31/10) App: bình luận dài "Xem thêm" (link bấm được: chưa làm — app chưa có gói url_launcher)
- [x] (31/10) App: lưu nháp khi thoát (trong phiên chạy app, chưa lưu qua lần mở app sau)
- [x] (31/10) App: vuốt phải để trả lời
- [x] (31/10) BE: migration `2026_10_31_000001_add_pin_resolve_to_comments_table` (is_pinned/pinned_by/pinned_at/is_resolved/resolved_by/resolved_at), trait `CommentModeration`, API `POST .../comments/{id}/pin|resolve`, xóa bởi người tạo/phụ trách (`can_delete`, `can_manage`), phân trang `?limit=&before_id=` (trả `total`, `count_all`, `meta`)
- [x] (31/10) Web + App: ghim (tối đa 3, chỉ bình luận gốc) · "Đã giải quyết" · quản lý xóa · phân trang "Xem bình luận cũ hơn"
- [x] (31/10) App: mở màn bình luận dừng ở bình luận mới nhất; màn chi tiết task dùng `comments_count`
- [x] (31/10) Sửa chung: `action_menu_sheet.dart` đáy trắng liền (SafeArea vào trong khối trắng)

## Kết quả test (31/10/2026)
BE (curl, Task + Issue): danh sách đủ/phân trang/ghim đầu trang; ghim tối đa 3 (422 khi thứ 4); ghim bình luận con → 422; ghim không đổi `updated_at` (không hiện nhầm "Đã chỉnh sửa"); người ngoài 403 khi ghim/giải quyết/xóa; người tạo xóa được bình luận người khác; người phụ trách ghim được.
App (simulator iPhone 15, ~60 bước, log không có lỗi Flutter mới): phân trang 20 + "Xem bình luận cũ hơn"; ghim/bỏ ghim; đã giải quyết; gửi tức thì; gửi lỗi 422 → Thử lại/Xóa; vuốt phải trả lời; phản hồi tự mở; nhấn giữ 👍 chọn cảm xúc; bảng "Cảm xúc" ai đã thả; xóa bình luận người khác (người tạo) có hỏi + DB mất; menu người không phải quản lý (không có Ghim/Đã giải quyết); sửa → "Đã chỉnh sửa"; nháp giữ khi vào lại; ảnh thumbnail 1/nhiều + xem toàn màn; chọn ảnh từ thư viện → thumbnail ô soạn → gửi chỉ ảnh.
Web (Playwright): thread phân trang 22→31 không trùng; ghim/đã giải quyết hiển thị; menu ⋯ đủ mục; ghim qua menu; tiêu đề đếm đúng 31.
Bổ sung cùng ngày (31/10): App màn Vấn đề (ghim · đã giải quyết · xóa bình luận người khác, API `issues`) — chạy đúng. Web: người tạo xóa bình luận người khác (hộp xác nhận → mất khỏi giao diện và DB); tài khoản không phải quản lý (bình luận người khác không có ⋯, của mình chỉ Sửa/Xóa); hồ sơ thẩm định giải pháp (API cũ không có trường mới: không phân trang, không hiện Ghim, chủ bình luận vẫn Sửa/Xóa).
CHƯA test: Android (user chốt không cần, chỉ test local); mất mạng thật (chỉ thử lỗi 422); link bấm được trong bình luận (chưa làm).
Triển khai: cần chạy migration trên dev/prod.

## Đã đẩy (31/10/2026) — nhánh develop
- hrm-api `ff1ccbaed` (đã gộp origin → `eea87c38b`), hrm-client `84c49fc81` (→ `bee1f06f6`), TPE_APP `7b7670c` (App 2.2.6 build 158 tpeDev)
- TestFlight: Tân Phát ERP-HRM (tpeDev) 2.2.6 (158) — build trong worktree sạch `~/.tpe-release-tpedev` ở commit `7b7670c` (thư mục chính đang có file Meeting dở của người khác nên không build từ đó)
- CHƯA làm: chạy migration + deploy BE lên server dev; merge develop → tpe (theo skill app-build-release)

## Để sau (cần chốt)
- Phân trang bình luận (BE + web + app), cập nhật gần thời gian thực, ghim, "Đã giải quyết", quyền xoá của quản lý.

## Trạng thái (31/10/2026)
Chưa test trình duyệt / simulator, chưa commit. Web: eslint sạch. App: `dart analyze` sạch. Cần test: sửa bình luận → hiện "Đã chỉnh sửa"; thu gọn/mở phản hồi; mở từ thông báo vào bình luận con.
