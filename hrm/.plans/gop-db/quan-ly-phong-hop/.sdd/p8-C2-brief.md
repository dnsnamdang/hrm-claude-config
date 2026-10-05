# Brief — Phase 8 / lượt C2 (task T138–T141): FE "Yêu cầu dịch vụ" trên phiếu đặt phòng

Repo **`hrm-client`** (Nuxt 2 / Vue 2), nhánh `gop_db`. **Chỉ sửa `hrm-client`**, không đụng `hrm-api`.

## Bối cảnh

Người đặt phòng nhờ người phụ trách phòng chuẩn bị trà / nước / hoa quả… BE đã xong (lượt C1):
đọc `.sdd/p8-C1-report.md` mục **"bàn giao cho lượt FE"** để lấy đúng tên trường, mã lỗi và payload.

Màn liên quan: popup đặt phòng `pages/meeting/bookings/components/BookingFormModal.vue` (2.485 dòng)
và màn danh sách `pages/meeting/bookings/index.vue`.

**Skill phải đọc trước khi viết dòng nào** (trong `HRM/.claude/skills/`): `form-validate`,
`modal-popup`, `button-convention`, `list-page`, `select-and-input-state`. Skill **thắng** mọi mô tả
trong brief này về hình thức UI (chữ trên nút, màu, icon, khuôn popup).

## Việc phải làm

### T138 — Khối nhập "Yêu cầu dịch vụ" (chỉ ở chế độ TẠO MỚI)

- Đặt trong popup đặt phòng, dùng **tiêu đề nhóm phẳng** giống các khối khác của chính modal này —
  **KHÔNG** dựng card `V2BaseFormSection` (user đã chốt 19/09/2026 bỏ card ở modal này; đọc comment
  ~dòng 2393 trước khi làm).
- **Chỉ hiện khi**: đang TẠO MỚI **và** đã chọn phòng **và** phòng đó có ≥ 1 người phụ trách.
  Phòng không có ai phụ trách → **không hiện khối**, thay bằng 1 dòng giải thích màu xám `#6b7280`
  ("Phòng này chưa khai người phụ trách nên chưa nhận yêu cầu dịch vụ").
  ⚠️ **`.text-muted` trong dự án bị SCSS toàn cục ép thành MÀU ĐỎ** — đừng dùng.
- Mỗi dòng gồm: món (`V2BaseSelectInModal`, nguồn `GET meeting/room-services/options`) · số lượng ·
  ghi chú · nút xoá dòng. Cuối khối là nút "Thêm dòng".
- **Món đã chọn ở dòng khác phải biến khỏi dropdown** của dòng còn lại (BE cũng chặn trùng, nhưng để
  user chọn được rồi mới báo lỗi là tệ).
- Số lượng: **để trống**, KHÔNG tự điền theo số người dự kiến (user đã chốt). Bắt buộc nhập, phải > 0.
  Hiển thị theo chuẩn quốc tế `1,234.5` — dùng `toLocaleString('en-US')`, **CẤM `'vi-VN'` cho số**.
- **Không tự sửa giá trị user gõ**: nhập sai thì báo đỏ ngay dưới ô và **giữ nguyên số đã gõ**; cấm
  kéo về max/min, cấm làm tròn, cấm tự xoá dòng trống.
- Bấm Lưu phải hiện **hết lỗi của mọi dòng cùng lúc**, không bắt sửa từng dòng.
- Payload gửi kèm khi tạo phiếu: `services: [{ service_id, quantity, note }]` theo đúng thứ tự trên
  màn. Không có dòng nào thì **không gửi khoá `services`** (hoặc gửi mảng rỗng — theo đúng cái C1 mô
  tả trong báo cáo).

### T139 — Chế độ CHỈ ĐỌC (màn Sửa phiếu + popup Xem)

- Sửa phiếu: khối dịch vụ hiện **chỉ đọc**, không có nút thêm/xoá dòng, không ô nhập.
- Popup Xem: liệt kê các món + số lượng + ghi chú, kèm `V2BaseBadge` trạng thái với **màu do BE trả**
  (`service_status_color`) và chữ do BE trả (`service_status_text`) — **TUYỆT ĐỐI không map số →
  chữ và không tự chọn màu ở FE**.
- Trạng thái Từ chối thì hiện thêm lý do + ai xử lý lúc nào (`service_handled_by_name`,
  `service_handled_at`, `service_reject_reason`). Dòng nhãn màu xám `#6b7280`, giá trị `#374151`,
  **không in đậm, không tô đỏ** — đỏ chỉ dành cho lỗi validate.

### T140 — 2 nút xử lý ở popup Xem

- "Đã chuẩn bị" (primary) và "Từ chối" (nhóm nguy hiểm) — chữ/màu/thứ tự theo `button-convention`.
- **`v-if="item.is_can_handle_service"`** — nút không dùng được thì **ẩn hẳn**, KHÔNG hiện rồi disable.
- "Từ chối" mở `components/modal/base-confirm-modal.vue` (hoặc `this.$confirm({...})`) để nhập lý do
  bắt buộc — **KHÔNG** tự dựng popup xác nhận riêng, **KHÔNG** dùng `$bvModal.msgBoxConfirm()`.
- Nút trong cùng cụm khai `class="mr-2 mb-2"`, nút cuối cụm `mb-2` (thiếu `mr-2` là 2 nút dính sát
  nhau 0px — đã đo thật trên chính màn này).
- Gọi `PUT meeting/room-bookings/{id}/service-prepared` / `/service-rejected`. Thành công → đóng
  popup, nạp lại danh sách. Lỗi **409** (người khác vừa xử lý xong) → hiện đúng câu BE trả về rồi
  nạp lại, **không** hiện câu chung chung "Có lỗi xảy ra".

### T141 — Màn danh sách `pages/meeting/bookings/index.vue`

- Thêm **cột "Dịch vụ"**: badge trạng thái (màu BE trả), phiếu không kèm dịch vụ thì **để trống** —
  không in chữ "Không có". Cột nằm trong bộ cột cấu hình được; **không đổi bộ cột mặc định** hiện tại
  (nếu skill `list-page` quy định số cột mặc định thì theo skill).
- Thêm ô lọc **"Trạng thái dịch vụ"** vào khối Tìm kiếm nâng cao: Chờ chuẩn bị · Đã chuẩn bị ·
  Từ chối · Không có yêu cầu. Placeholder/nhãn theo quy tắc trong `list-page` (màn này đã bật
  `floating` hay chưa — kiểm rồi làm đúng loại, **cấm** placeholder "Tất cả" / "Chọn...").

## Ràng buộc bắt buộc

- Mọi element form là `V2Base*` (`<input>`/`<select>`/`<button>`/`<label>` thô là sai);
  select trong modal là `V2BaseSelectInModal`.
- Badge dùng `V2BaseBadge`, màu lấy từ BE.
- Cờ quyền khởi tạo `false`, cấm hard-code `true`.
- **Không `git commit`/`push`/`stash`**. Không đụng `hrm-api`. Không tạo subagent, không tự gọi
  reviewer. **KHÔNG tự mở trình duyệt / không dùng Playwright** — người điều phối đo sau.

## Cách tự kiểm (ghi kết quả thật vào báo cáo)

1. `grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/meeting/bookings | grep -v V2Base`
   → chỉ được còn những dòng ĐÃ CÓ TỪ TRƯỚC (liệt kê rõ dòng nào là cũ, dòng nào của bạn — của bạn
   phải là 0).
2. `grep -rn "toLocaleString('vi-VN')" pages/meeting/bookings` → RỖNG (trừ chỗ format NGÀY GIỜ).
3. `grep -rn "text-muted" pages/meeting/bookings` → không được có dòng nào do bạn thêm.
4. Tự rà: mọi nút mới có `mr-2 mb-2` (nút cuối `mb-2`) chưa; mọi nút có `v-if` điều kiện chưa (không
   `disabled`).

## Báo cáo

`.sdd/p8-C2-report.md`: từng task, kết quả 4 mục tự kiểm, file sửa, chỗ tự quyết, và mục **"Người
điều phối cần đo gì trên trình duyệt"** — liệt kê cụ thể: mở màn nào, bấm gì, đo số gì (toạ độ,
khoảng cách nút, số phần tử, màu tính bằng `getComputedStyle`).
Trả về chat ngắn gọn: trạng thái, file đã sửa, điểm nghi ngờ.
