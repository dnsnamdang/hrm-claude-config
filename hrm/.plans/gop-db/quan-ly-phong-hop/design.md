# Design — Quản lý phòng họp (phân hệ Meeting)

> **Tóm tắt.** Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-17-quan-ly-phong-hop-design.md`

- **Ngày chốt design**: 17/09/2026 · **Phụ trách**: @namdangit
- **Nhánh**: `gop_db` (cả `hrm-api` và `hrm-client`)
- **Module BE mới**: `Modules/Meeting` · **FE**: `pages/meeting/`

## Mục tiêu

Lấp 3 mục đang treo trống trong menu phân hệ Meeting: **khai báo phòng họp**, **đặt phòng họp**
(gắn với phiếu Meeting), **màn theo dõi tình trạng phòng**. Kèm check-in chống giữ chỗ ảo, đặt lặp
định kỳ, thông báo và báo cáo hiệu quả sử dụng. Tham khảo MISA AMIS Phòng họp.

## Hiện trạng

- Menu `components/subsystem-menu/meeting.js` đã chừa sẵn *Danh sách phòng họp*, *Đăng ký phòng họp*
  (chưa có link) và *Hiệu quả sử dụng phòng họp*.
- `meetings` hiện ghi địa điểm bằng **text tự do**, không kiểm tra trùng phòng.
- Phòng họp **chưa có dòng code nào** ở cả 2 repo; DB gộp không có bảng trùng tên.
- `@fullcalendar` v5 có sẵn nhưng **không có resource-timeline** → lưới Phòng × Giờ phải tự dựng.

## Quyết định đã chốt (không hỏi lại)

1. **Bảng `meeting_room_bookings` riêng**; phiếu Meeting chọn phòng thì **tự sinh booking** — booking là
   nguồn duy nhất kiểm tra trùng.
2. **Duyệt tùy phòng** (`require_approval` trên từng phòng), người duyệt là `manager_employee_id`.
3. **Chờ duyệt được phép trùng giờ**; duyệt phiếu nào phiếu đó thắng, các phiếu trùng còn lại **tự Từ chối**.
   Phiếu *Đã duyệt* thì chặn cứng.
4. Phòng gắn `company_id` + cờ **`allow_cross_company`** cho đặt liên công ty.
5. **Danh mục tiện nghi riêng**, phòng chọn nhiều → lọc "phòng ≥ 20 chỗ có máy chiếu".
6. **Mọi nhân viên đặt phòng được**, không cần quyền riêng.
7. **Không lưu ảnh phòng họp.**
8. Mã phòng **tự nhập**; mã phiếu **tự sinh** `DPH-YYYY-NNNNN`.
9. **Nhắc check-out trước N phút**, N từ `general_regulations` (mặc định 10, `0` = tắt); chỉ nhắc phiếu
   đã check-in, có cờ `checkout_reminded_at` chống gửi trùng.
10. **Phiếu gắn Meeting thì KHÔNG AI hủy được** ở màn phòng họp, kể cả người quản lý phòng — phải đổi ở
    phiếu Meeting. Lối thoát của quản lý là *Từ chối* (khi còn Chờ duyệt) hoặc **khóa phòng**.
11. Prefix thông báo **`[DPH]`**.
12. **Tính trước cho app mobile**: một bộ API dùng chung; **BE trả cờ hành động**
    (`is_can_edit/cancel/approve/reject/checkin/checkout`); thời gian **ISO-8601 có offset**;
    thêm endpoint `/meeting-rooms/available` (chọn giờ → xem phòng trống) vì điện thoại không dùng được lưới.
13. **Cột `checkin_qr_token` đưa vào phase 1** (endpoint quét QR để phase 5) — thêm sau phải in và dán lại QR.

## Phạm vi

6 bảng mới + `meetings.meeting_room_id` + 5 cột cấu hình trong `general_regulations`;
5 màn FE; 3 job nền; 7 loại thông báo; 5 quyền mới.

## Chia phase

1. Nền tảng + danh mục → 2. Đặt phòng + duyệt → 3. Màn theo dõi → 4. Nối với Meeting →
5. Check-in + định kỳ → 6. Báo cáo

## Rủi ro chính

Race khi đặt trùng (phải `lockForUpdate`) · cron không chạy làm job chết lặng ·
sync Meeting bỏ sót đường ghi (đặt ở model event) · web và app lệch luật ẩn/hiện nút (BE trả cờ).

## Quyết định đã chốt (bổ sung trong lúc thực thi)

- **20/09/2026 — KHÔNG làm "giữ chỗ tạm" khi đang soạn form** (user chốt sau khi cân 3 phương án).
  Chống tranh chỗ dừng ở mức: tình trạng phòng theo đúng khung giờ (Task 76), gợi ý phòng/khe thay thế
  (76–77), **kiểm lại ngay trước khi gửi + theo dõi sống 45s** (Task 78). Lý do bỏ giữ chỗ tạm: phải
  thêm cột/bảng + lệnh dọn định kỳ, và sinh cảnh "phòng bị giữ ảo" khi người dùng bỏ form giữa chừng.
  Chốt chặn thật vẫn là `assertNoOverlap()` có khóa lúc ghi.
- **20/09/2026 — lưu CUỘC HỌP mà phòng đã bị chiếm thì CHẶN CẢ cuộc họp** (giữ nguyên hành vi đang
  chạy, user chốt). KHÔNG lưu meeting rồi âm thầm bỏ phòng. FE bù lại bằng: nạp lại tình trạng phòng
  ngay khi BE trả lỗi ở ô `meeting_room_id`, hiện phòng còn trống / khe giờ gần nhất để đổi 1 bấm —
  dữ liệu đang nhập KHÔNG mất, người dùng chỉ việc đổi phòng rồi bấm Lưu lại.
- **20/09/2026 — MỌI việc đặt phòng quy về FORM ĐẶT PHÒNG** (user chốt, Task 80). Form meeting và màn
  danh sách meeting KHÔNG tự chọn phòng nữa, chỉ có nút "Đăng ký phòng" mở popup đó với dữ liệu cuộc
  họp truyền sẵn (chỉ đọc). Lý do: logic chọn phòng nằm trên form meeting phải xử lý quá nhiều (tình
  trạng phòng, giờ mở cửa, tranh chỗ) mà vẫn hở — một form, một chỗ sửa.
- **20/09/2026 — được đăng ký phòng TỪ trạng thái "Lên lịch" (status 1)**, không ép phải "Chốt lịch"
  (user chốt sau khi cân 3 phương án). Cuộc họp nháp (status 0) chưa có giờ chắc chắn nên chưa cho
  đăng ký. **Phiếu bám theo thay đổi giờ của cuộc họp một cách tự động** (`MeetingRoomBookingSyncService`):
  đổi giờ họp thì phiếu đổi theo, giờ mới trùng phòng khác thì BE chặn ngay lúc lưu cuộc họp.
- **20/09/2026 — chỉ NGƯỜI TẠO hoặc NGƯỜI CHỦ TRÌ được đăng ký phòng cho cuộc họp** (Task 83).
  BE `Meeting::canBookRoom()` = `canEdit()` (tạo hoặc chủ trì) **và** `status >= LEN_LICH`, chưa
  Hoàn thành / Hủy; Resource trả cờ `can_book_room`, FE ẩn nút theo cờ đó (không tự suy ở FE).

- **17/09/2026 — sửa component dùng chung `components/modal/V2BaseModal.vue`** (user duyệt): thêm method
  `hide()` alias của `close()`. Lý do: `unsavedModalMixin` gọi `.hide()` nhưng `V2BaseModal` không có, nên
  popup "chưa lưu" bấm Thoát không đóng được mà không báo lỗi. Thuần bổ sung, không đổi `show()`/`close()`.
  Modal mới trong repo **cứ dùng `V2BaseModal` + `unsavedModalMixin` bình thường**, không cần sửa lại nữa.
- **17/09/2026 — `$store.state.permissions` là mảng OBJECT `{id, name, …}`**, không phải mảng chuỗi.
  Kiểm quyền phải viết `perms.some(p => p.name === '<Tên quyền>')` (hoặc `utils/mixins/CheckPermission.js`).
  Viết `perms.includes('<Tên quyền>')` sẽ luôn false → cờ quyền chết cứng ở trạng thái không quyền,
  console không báo gì.
- **19/09/2026 — bộ quyền của feature gộp còn 1: "Khai báo phòng họp"** (id 1574). Có quyền này thì
  tạo/sửa/khoá/xoá được CẢ phòng họp lẫn tiện nghi, và vào được 2 màn danh mục. Bỏ hẳn 3 quyền
  1575/1576/1577 (không còn trạng thái "chỉ xem"). Ghi đè mục 10 của spec.
- **19/09/2026 — công ty nào tạo thì phòng thuộc công ty đó**: form KHÔNG có ô Công ty, `company_id`
  do `BaseModel::creating()` điền; sửa/khoá/mở khoá/xoá chỉ cho phòng CÙNG công ty (BE trả 403,
  `is_can_edit`/`is_can_delete`/`is_can_lock` tính kèm điều kiện này). Màn danh sách vẫn xem phòng của
  MỌI công ty + có ô lọc Công ty. `meeting_rooms` DROP `department_id`/`part_id` — để lại thì
  `BaseModel` tự điền phòng ban của NGƯỜI TẠO mỗi lần save, sai dữ liệu âm thầm.
- **19/09/2026 — sửa component dùng chung `components/V2BaseRowActions.vue`** (user duyệt): bỏ qua sự
  kiện `scroll` trong 250ms đầu sau khi mở menu `⋮`. Lý do: trình duyệt tự cuộn nút `⋮` vào tầm nhìn
  lúc bấm, sự kiện scroll bắn ra SAU khi menu vừa mở nên đóng nó ngay — người dùng phải bấm 2 lần.
  Ảnh hưởng mọi màn dùng cột Hành động chuẩn (đã đo lại: cuộn thật sau đó vẫn đóng menu như cũ).
- **19/09/2026 — popup Xem KHÔNG thêm chip `Cập nhật / Bởi`** như màn `/assign/meeting_type`: màn đó
  là popup `b-modal` khuôn CŨ (skill modal-popup mục 1), còn khuôn `V2BaseModal` (mục 0) chỉ có
  icon + tiêu đề + dòng mô tả bản ghi + ×; thông tin ai-sửa-gì-lúc-nào đã nằm trong khối Lịch sử.
- **19/09/2026 — khoảng cách ô trong popup form là `mb-2`** (chuẩn dùng chung, 32 màn khác đang dùng),
  `V2BaseFormSection` dùng `class="mb-2"` chứ KHÔNG `mt-3`.
- **19/09/2026 — PHIẾU ĐĂNG KÝ PHÒNG TÁCH LÀM 2 HƯỚNG** (user chốt, 4 câu hỏi):
  1. **Gắn với cuộc họp** — chọn cuộc họp đã tạo; Tiêu đề / Thời gian / Chủ trì / Số người / Nội dung
     **CHỈ ĐỌC**, người dùng chỉ chọn PHÒNG. Lưu = `POST meeting/room-bookings/assign-meeting` → BE ghi
     `meetings.meeting_room_id` rồi để hook Phase 4 sinh phiếu (`source = 2`). **Một nguồn sự thật**:
     không có đường ghi thứ hai vào bảng phiếu, phiếu không bao giờ lệch cuộc họp.
  2. **Nhu cầu khác** — đào tạo, phỏng vấn, sự kiện, ăn uống… Chọn **Mục đích sử dụng** từ DANH MỤC
     (bảng `meeting_room_purposes` + màn `/meeting/room-purposes`, quyền "Khai báo phòng họp"), nhập
     Nội dung sử dụng / Ngày giờ / Người phụ trách / Số người / Ghi chú.
  - **Bỏ hẳn "Người tham dự" khỏi form** (hướng 2): đó là việc của cuộc họp. Phiếu cũ vẫn giữ danh sách
    và popup Xem vẫn hiện; form Sửa gửi lại nguyên danh sách cũ để không xoá trắng.
  - **Phiếu `source = 2` KHÔNG sửa được** ở màn phòng họp (BE 423, `isCanEdit()` trả false) — sửa ở màn
    Cuộc họp. Trước đó chỉ có "không hủy được", nay chặn cả sửa.
  - Lý do đổi: form cũ bê nguyên bộ trường của cuộc họp (agenda, chủ trì, người tham dự) vào phiếu →
    người dùng tạo "cuộc họp ảo" không hề tồn tại ở phân hệ Cuộc họp (user: *"form đăng ký đăng kiêm
    luôn chức năng tạo cuộc họp là chưa đúng"*).
  - Bấm ô trống ở màn **Tình trạng phòng họp** = đặt cho một khung giờ cụ thể → form ép sang hướng
    "Nhu cầu khác" (hướng 1 không có ô ngày/giờ).

---

## Phase 8 — Yêu cầu dịch vụ trên phiếu đặt phòng (chốt 23/09/2026)

> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-09-23-yeu-cau-dich-vu-phong-hop-design.md`

Người đặt phòng nhờ người phụ trách chuẩn bị trà, nước, hoa quả… ngay trên phiếu DPH; người phụ trách
nhận thông báo, chuẩn bị rồi xác nhận lại.

**11 quyết định user chốt (hỏi từng câu 23/09/2026):**

1. **Danh mục mới `meeting_room_services`** (tên · đơn vị tính · icon · khoá/mở khoá), khuôn
   `meeting_room_purposes`, KHÔNG gắn cờ vào danh mục Tiện nghi — tiện nghi là THIẾT BỊ gắn phòng
   dùng để lọc phòng, dịch vụ là đồ TIÊU HAO nhờ chuẩn bị.
2. Mỗi dòng yêu cầu = **món + số lượng + ghi chú dòng** → bảng con `meeting_room_booking_services`,
   snapshot `service_name`/`unit` để danh mục đổi tên không làm sai phiếu cũ.
3. Người nhận việc = **người phụ trách phòng**.
4. **Đổi `manager_employee_id` (1 người) → bảng nối `meeting_room_managers` (NHIỀU người)** và **bắt
   buộc khai ≥ 1 người** khi tạo/sửa phòng. Đây là thay đổi lan ra ngoài phạm vi dịch vụ: lọc phạm vi
   xem phiếu, gate duyệt, người nhận thông báo, sort cột, import/export, lịch sử danh mục, 4 chỗ FE
   (bảng đối chiếu đầy đủ ở mục 5 của spec).
5. **Ai trong nhóm phụ trách cũng duyệt/xác nhận được, ai bấm trước tính người đó** (người sau nhận
   409), thông báo bắn cho tất cả.
6. Trạng thái **mức cả phiếu**: Chờ chuẩn bị → Đã chuẩn bị / Từ chối (lý do bắt buộc).
   `service_status = NULL` nghĩa là phiếu KHÔNG kèm dịch vụ — khác hẳn "đã yêu cầu, chưa chuẩn bị".
7. **Chỉ nhập lúc TẠO phiếu**; vào màn Sửa thì khối dịch vụ **khoá hẳn, chỉ xem** (BE `update()` không
   đọc `services[]`, không dựa FE ẩn).
8. **3 mốc thông báo `[DPH]`**: có yêu cầu mới → nhóm phụ trách · phiếu Hủy/Từ chối → nhóm phụ trách ·
   Đã chuẩn bị/Từ chối dịch vụ → người đặt. KHÔNG làm job nhắc trước giờ họp.
9. Xử lý **ngay trong phiếu** + thêm cột "Dịch vụ" và ô lọc "Trạng thái dịch vụ" ở `/meeting/bookings`.
   Chưa làm màn tổng hợp yêu cầu dịch vụ riêng.
10. **Chưa làm chi phí** vòng này (danh mục vẫn có `unit` để sau thêm `unit_price` không phải làm lại).
11. Phiếu sinh từ cuộc họp (`source = 2`) **cũng yêu cầu dịch vụ được**; ô số lượng **để trống**, không
    tự điền theo số người dự kiến; **không thêm quyền mới** (danh mục dùng "Khai báo phòng họp").

**Tự đề xuất, user duyệt:** đổi phòng lúc sửa phiếu thì giữ nguyên dòng dịch vụ và **bắn thông báo cho
nhóm phụ trách phòng MỚI**; phiếu đã qua giờ vẫn xác nhận được (không thì kẹt "Chờ chuẩn bị" vĩnh viễn);
phòng chưa khai người phụ trách thì ẩn khối và BE trả 422; xoá món đang có phiếu dùng thì chặn, gợi ý Khoá.

### Phase 8 — quyết định phát sinh trong lúc thực thi (23/09/2026)

Bổ sung vào 11 quyết định chốt lúc brainstorm ở trên. Chi tiết + số đo: `.sdd/progress.md`.

1. **Khoá tên trường người phụ trách**: `manager_names[]` (mảng, FE render "2 tên + +N") ·
   `manager_employee_ids[]` (mảng id) · `manager_name` (chuỗi ghép `"; "`, khớp dấu import tách).
   **Bỏ `manager_name_text`** — 2 khoá cùng nghĩa thì FE/export mỗi chỗ đọc một kiểu.
2. **Nút trong footer popup KHÔNG khai `mr-2`** — Bootstrap `.modal-footer > *` đã tự cách 8px; khai
   thêm là cộng dồn thành 16px. Đo thật: 75 file có `<template #footer>`, chỉ 2 file khai `mr-2`.
   Quy ước "`mr-2 mb-2`, đo 12px" trong CLAUDE.md là cho **toolbar / cụm nút trong thân form**.
3. **Thứ tự nút footer popup phiếu**: gom theo nhóm việc — `Duyệt · Từ chối · Hủy phiếu ·
   Đã chuẩn bị dịch vụ · Từ chối dịch vụ · Đóng`. Chữ nút dịch vụ có hậu tố "dịch vụ" vì footer đã
   có sẵn nút "Từ chối" của việc từ chối PHIẾU.
4. **Bảng dòng con không cần `created_by`/`updated_by`** (`meeting_room_booking_services`) — không
   màn nào hiện cột Người tạo cho nó; tiền lệ `meeting_room_booking_participants`.
5. **Sửa phiếu Đã duyệt: GIỮ NGUYÊN luật cũ** (user chốt 23/09) — sửa được tới trước giờ bắt đầu;
   đổi giờ/phòng thì tự về Chờ duyệt, sửa trường khác thì giữ Đã duyệt.
   ⚠️ Ghi nhận chưa làm: sửa trường KHÔNG phải giờ/phòng thì **không có thông báo cho người đã duyệt**.
6. **Message validate lấy từ lang file dùng chung**; module chỉ giữ câu **nghiệp vụ** + `attributes()`.
   Kéo theo: đã bổ sung **53 mục tiếng Việt** vào `resources/lang/vi/validation.php` và 26 key vào
   `hrm-client/locales/vi.json` (user duyệt sửa tài sản chung). Câu mới **không dùng `:attribute`**
   (100% câu Việt sẵn có đều vậy; đa số FormRequest không khai `attributes()` nên `:attribute` sẽ in
   ra tên cột snake_case tiếng Anh).
