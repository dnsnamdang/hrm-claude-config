# Design (tóm tắt) — Đổi toàn bộ UI app TPE_APP theo thiết kế meeting-mobile.pen

**Người phụ trách:** @cuong61n · **Bắt đầu:** 20/10/2026
**Repo / nhánh:** `TPE_APP` nhánh `develop` (rồi đưa sang `tpe`) · BE `hrm-api` (nhánh chốt khi tới Phase 5)
**Không áp dụng:** nhánh `thanhan`, `duclocson` (giữ nguyên UI cũ). Phân hệ Meeting mới chưa làm.
**Thiết kế:** `~/Downloads/meeting-mobile.pen` (bản gốc ở `.plans/app-meeting-mobile/`)
**Spec chi tiết:** `docs/superpowers/specs/2026-10-20-app-ui-redesign-design.md`

## Mục tiêu

Mọi màn đang có của app (Chấm công, Công việc, Đào tạo, Quản lý cơm, Thông báo) hiển thị và điều hướng
đúng khuôn thiết kế: màu nhận diện theo phân hệ, header gradient, drawer riêng từng phân hệ, bottom menu
4 tab + nút giữa có trạng thái đang chọn. Không đổi nghiệp vụ.

## Quyết định đã chốt (20/10/2026)

1. **Tách phân hệ theo thiết kế**: màn chọn phân hệ có 4 mục Chấm công · Công việc · Đào tạo · Quản lý cơm
   (Quản lý cơm ẩn với Kasaco). Giao việc / Công tác / Task chuyển sang phân hệ Công việc.
2. **Khung tab giữ trạng thái**: mỗi phân hệ 1 khung chứa 4 tab (IndexedStack, tab đang chọn sáng màu);
   nút giữa mở form tạo mới bằng push. Màn con push đè lên, che bottom menu.
3. **Tổng quan Chấm công (00i) làm cả BE `hrm-api`** để trả đủ trường (allow_app / allow_conn / tên máy theo
   từng ca-phiếu, job_type + job_id ở timekeeper/employee, ca làm việc không phụ thuộc job tính công).
4. **Màu phân hệ là trạng thái toàn cục** `AppModule.current` (gán khi chọn phân hệ); header / nút chính /
   bottom menu đọc từ đó. Màn chưa thuộc phân hệ nào dùng tông navy chung.
5. Cờ khách hàng (`env.isThanhAnGroup`, `isDLSGroup`, `isKasaco`, `isWhatTheFuckToDoThis`) giữ nguyên logic —
   chỉ đổi cách trình bày.
6. **Tiêu đề màn Quản lý cơm giữ tên cũ** (Quản lý đăng ký cơm · Thông báo · Quản lý đăng ký suất ăn ·
   Thiết lập phân hệ cơm) — nhãn tab bottom menu vẫn ngắn theo thiết kế.
7. **Thứ 7 / Chủ nhật trên lịch cơm giữ chữ đỏ** (ngoại lệ của quy ước "đỏ chỉ cho lỗi").
8. **Thanh nút đáy form ghim đáy như thiết kế** — bàn phím mở thì che nút, chấp nhận.
9. **Bám sát thiết kế mới nhất có thể** (chữ, nút, bố cục, màu, hành vi trình bày). Chỉ thay đổi đụng BE hoặc dữ liệu
   hiển thị (thêm/bớt trường, API mới, đổi cách tính số) phải báo user duyệt. (Ngoại lệ đã chốt: tiêu đề màn Cơm cũ,
   cuối tuần lịch cơm đỏ.)

## Thành phần dùng chung (đổi 1 chỗ ăn toàn app)

`resource/styles/app_module.dart` (màu) · `PrimaryAppBar` (header) · `CommonBottomNavigationBar` +
`PrimaryBottomNavigationItem` (bottom menu) · `PrimaryButton` / `SecondaryButton` · `PrimaryTextField` ·
`StatusBadge` · `LeftMenuView` (drawer, đang dùng chung cho 3 phân hệ) · khung tab phân hệ (mới).
10. **Thông báo (21/10/2026):** BE trả thêm `module` · `prefix` · `action` · `object_name` · `note` · `object_id` mỗi thông báo;
    API danh sách nhận `module` + `unread`, trả `counts` theo phân hệ cho chip; `mark_all_as_read` nhận `module`.
    Giữ thông báo xác nhận cơm trong chuông.
    **Đồng bộ hiển thị mọi thông báo** (đổi lại 21/10/2026, thay cho "chỉ chuẩn hoá thông báo mới"): câu cũ viết tự do
    được BE quy về `[MÃ] Nhóm hành động: Tên. Ghi chú` lúc trả API (`App\Support\NotificationLegacyFormat`, không sửa
    dữ liệu đã lưu); ghi chú mặc định "Người gửi: …" trừ loại hệ thống tự gửi; không nhận diện được → app hiện tag tên phân hệ.
    API cắt `data.employeeInfo` còn id/mã/tên/ảnh (trước trả nguyên hồ sơ có lương, CCCD, MST).
    **Push (màn khoá / khay)** cùng khuôn (`NotificationMeta::push`, dùng ở `SendNotification` + `SendMobileNotification`):
    tiêu đề `Nhóm hành động · Phân hệ` (iOS chỉ cho tiêu đề 1 dòng), thân `Tên đối tượng. Ghi chú`; trước là tiêu đề = tên app, thân = câu thô.
    **Web** cùng khuôn với app: chuông topbar + màn `/timesheet/notifications` dùng `components/notification/NotificationItem.vue`
    (+ `utils/notificationDisplay.js`, màu/icon phân hệ khớp AppModule). `user-profile` và socket cũng trả sẵn các phần hiển thị.
11. **Màn Tổng quan của MỌI phân hệ** (21/10/2026): tiêu đề "Tổng quan", header nền đặc + `OverviewHeaderBand`
    (ngày · lời chào + tên · tóm tắt), nút `NotificationBellButton` bên phải. Phân hệ mới có Tổng quan (Meeting) dùng lại 2 component này.
12. **Loading — mẫu E** (chốt 21/10/2026, chọn trên trang xem trước 5 mẫu): KHÔNG vòng xoay giữa màn / giữa vùng.
    Màn đang tải hoặc đang xử lý (`showLoading()`) → thanh 3px chạy ngay dưới header (`PrimaryAppBar` tự vẽ qua
    `PageLoadingScope`/`GlobalLoading`; header `flat` dùng thanh trắng; màn không có `PrimaryAppBar` thì lớp nền vẽ ở đầu màn).
    Vùng chưa có dữ liệu → skeleton (`ContentSkeleton`, `ListFooterSkeleton`, `SkeletonLines`, `NotificationSkeletonList`, `SkeletonCard`).
    `showLoading()` = thanh chạy + chặn chạm (bỏ khung HUD EasyLoading). Vòng xoay `AppSpinner` CHỈ còn trong nút/biểu tượng vừa bấm.
    Cấm màn tự đặt `CircularProgressIndicator` / `CupertinoActivityIndicator`; vòng/thanh có `value` (biểu đồ số liệu) là ngoại lệ.
13. **Nút cao 44 cố định** (chốt 21/10/2026, thiết kế ghi 48): `kAppButtonHeight` trong `custom_view/primary_button.dart`,
    không nhân hệ số màn hình (trước `h(48)` lên ~55 ở máy dài). Nút vuông chỉ-icon 44×44 giữ nguyên.
