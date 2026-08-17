---
name: erp-to-hrm-screen
description: Dùng khi chuyển/port một màn hình từ ERP (Laravel + AngularJS, TanPhatDev) sang HRM (Nuxt + Vue, hrm-client) — kể cả khi chỉ dựng lại 1 phần màn, thêm màn danh sách/chi tiết/form theo mẫu ERP, hoặc rà lại màn đã port xem có lệch quy chuẩn UI không.
---

# Chuyển màn ERP → HRM

## Vấn đề skill này giải

Màn ERP viết bằng AngularJS + Blade, không có quy chuẩn UI thống nhất. Khi port sang HRM, lỗi
lặp lại nhiều nhất **không phải lỗi nghiệp vụ** mà là lỗi UI: quên mixin ghi nhớ bộ lọc, tự dựng
badge riêng, nút sai màu/sai thứ tự, thiếu Cấu hình cột, thông báo tự chế câu mới, cột căn lề lung tung.

Skill này khoá 3 thứ lại:
1. **Quy trình 6 bước** — làm đúng thứ tự thì không sót phần nào.
2. **Khuôn màn mẫu** — copy pattern từ màn Danh mục khách hàng, không tự phát minh.
3. **Checklist tự kiểm** — chạy trước khi báo xong.

## Nguyên tắc gốc

> **Màn HRM phải trông như các màn HRM khác, KHÔNG phải như màn ERP gốc.**
> ERP là nguồn của **nghiệp vụ** (cột nào, lọc gì, hành động nào, ai được làm).
> HRM là nguồn của **giao diện** (component nào, màu gì, thứ tự nào).
> Bê nguyên UI của ERP sang là sai, kể cả khi "ERP đang làm thế".

---

## Quy trình 6 bước

### Bước 1 — Khảo sát màn ERP gốc (chỉ lấy nghiệp vụ)

Đọc file ERP và ghi ra **bảng nghiệp vụ**, chưa động tới code HRM:

| Cần ghi | Lấy ở đâu trong ERP |
|---|---|
| Danh sách cột + ý nghĩa | blade `datatable` / `columns` trong file js |
| Trường lọc + kiểu (text/select/date/range) | form filter trong blade |
| Hành động mỗi dòng + **điều kiện hiện/ẩn** | cột action trong blade + `if` quyền |
| Quyền dùng cho từng hành động | `@can` / `hasPermission` trong blade + controller |
| Trạng thái & nhãn tiếng Việt | hằng số/`status_text` ở model |
| Xuất/In/Import có không | nút trên toolbar |

⚠️ **Ghi cả điều kiện ẩn nút**, không chỉ tên nút. Lỗi hay gặp nhất là port nút nhưng bỏ điều kiện.

### Bước 2 — Chốt phân hệ, route, quyền

- Màn thuộc phân hệ nào (theo sơ đồ tách phân hệ) → route `/<phân-hệ>/<slug>`.
- Quyền: dùng lại **đúng permission ERP** hay tạo mới? Nếu dùng lại thì migration `UPDATE permissions`
  **giữ nguyên `id`** và phải sửa cả `PermissionsTableSeeder`.
- Có cần phân quyền theo cấp (công ty / phòng ban / bộ phận) không → **hỏi user**, đừng tự quyết.
- Thêm mục menu vào `components/subsystem-menu/<slug>.js`.

### Bước 3 — Dựng khung theo khuôn màn mẫu

Đọc `references/khuon-man-mau.md` rồi dựng 4 file theo đúng cấu trúc:
`index.vue` (danh sách) · `add.vue` · `_id/edit.vue` · `_id/index.vue` + 1 `XxxForm.vue` dùng chung.

**Trước khi tự viết bất kỳ thành phần UI nào** (badge, tooltip, popup, upload, kéo thả, phân trang,
biểu đồ…) → grep xem project đã có chưa. Đã có ≥ 1 màn làm đúng thì bám theo màn đó và ghi vào
`plan.md`: "copy pattern từ `<file:dòng>`".

### Bước 4 — Áp quy tắc chung SRS

Đọc `references/srs-quy-tac-chung.md` — bảng tra đầy đủ: cột mặc định, sort, tìm kiếm, phân trang,
căn lề, màu nút, màu trạng thái, thứ tự nút, định dạng dữ liệu, bộ thông báo QLDA_001…025.

**Thông báo phải lấy nguyên văn từ bảng QLDA**, không tự chế câu mới.

### Bước 5 — Đối chiếu ngược với ERP

Mở song song màn ERP và màn HRM vừa dựng, đối chiếu **từng dòng bảng ở bước 1**:
- Đủ cột chưa? Cột ERP có mà HRM không có → thêm vào, mặc định **ẩn** trong Cấu hình cột nếu ít dùng.
- Đủ trường lọc chưa?
- Đủ hành động chưa, **và điều kiện hiện/ẩn có khớp không**?

### Bước 6 — Chạy checklist tự kiểm + verify trình duyệt

Chạy hết checklist bên dưới, rồi mở trình duyệt bấm thật. **Không báo xong khi chưa bấm thật.**

---

## Checklist tự kiểm (chạy trước khi báo xong)

### A. Màn danh sách
- [ ] Có đủ 4 mixin: `PageTitleMixin`, `CheckPermission`, `filterStateMixin`, `columnCustomizationMixin`
- [ ] `localStorageKey` và `columnScreenKey` **duy nhất**, không trùng màn khác
- [ ] Cột mặc định có: STT, Mã, Tên, Người tạo, Ngày tạo, Trạng thái (nếu có), Hành động
- [ ] Mã và Tên là **2 cột riêng**; cột Mã là `<nuxt-link>` thật (chuột phải mở tab mới được)
- [ ] Sắp xếp mặc định **giảm dần theo ngày tạo**
- [ ] Bảng trống hiện dòng "Không có dữ liệu phù hợp", không phải bảng rỗng
- [ ] Sort bật cho cột mã / tên / tiền / ngày; sort cột mới hủy sort cột cũ
- [ ] Phân trang mặc định 10, chọn được 5/10/20/50/100, đổi số dòng nhảy về trang 1
- [ ] Ô lọc dạng chọn tự tìm ngay khi chọn; ô gõ tay chờ Enter/nút Tìm kiếm
- [ ] Placeholder nói đúng trường lọc gì (`Chọn <X>` / `Nhập <X>` / `Tìm theo <các trường>`) —
      không `Tất cả`, không `Chọn...`, không để trống
- [ ] Nút **Làm mới** xóa hết điều kiện **và tải lại danh sách**
- [ ] Vào chi tiết rồi quay lại → **bộ lọc còn nguyên**
- [ ] Có nút Cấu hình cột; STT / Mã / Hành động **không tắt được**
- [ ] > 3 trường lọc → có popup "Cài đặt bộ lọc"; ≤ 3 trường → hiện thẳng, bỏ khối nâng cao

### B. Nút & hành động
- [ ] Mọi nút có **icon + text** (nút chỉ icon → dùng `V2BaseIconButton`)
- [ ] Thứ tự toolbar danh sách: Thêm mới → Import → Xuất → Cấu hình cột
- [ ] Thứ tự cột thao tác: Sửa → Xóa → menu "…"
- [ ] > 3 hành động → chỉ hiện 2 nút chính + nút "Hành động khác"
- [ ] Nút không dùng được thì **ẩn hẳn** (`visible`/`v-if`), KHÔNG hiện xám
- [ ] Hành động ở màn **chi tiết khớp hệt** màn danh sách — cả danh sách nút lẫn điều kiện ẩn/hiện
- [ ] Nút màn chi tiết/form nằm trong `V2Footer`, không tự dựng khối nút
- [ ] Màu nút đúng nhóm (chính = teal, Duyệt = xanh lá, Gửi duyệt/Khóa = cam, Xóa/Từ chối = đỏ,
      Import = vàng nhạt, Xuất = xanh nhạt)

### C. Hiển thị dữ liệu
- [ ] Trạng thái dùng `V2BaseBadge`, text từ `status_text` của BE (không map số→chữ ở FE)
- [ ] Căn lề đúng: STT/badge/hành động = giữa; số & tiền = phải; chữ & ngày = trái
- [ ] Ngày `dd/mm/yyyy`, ngày+giờ `dd/mm/yyyy HH:mm` (BE trả sẵn, FE không format lại)
- [ ] Tiền: `.` ngăn nghìn, `,` ngăn thập phân
- [ ] Ô rỗng in `—`, không để trắng
- [ ] Chữ trong ô để **thường**, kể cả cột Mã — không `font-weight-bold`
- [ ] Chữ đỏ **chỉ** dùng cho lỗi validate / nút nguy hiểm / giá trị cũ trong lịch sử

### D. Form (thêm mới / chỉnh sửa)
- [ ] Lỗi validate hiện **ngay dưới ô nhập**, dạng `Tên trường – Nội dung lỗi`
- [ ] Còn lỗi thì **không gọi API lưu**; nhiều lỗi thì con trỏ nhảy về ô lỗi đầu tiên
- [ ] Chỉ trường **Tên** gắn `required` ở FE; required còn lại do BE trả 422
- [ ] Lưu nháp chỉ bắt required trường Tên
- [ ] Dropdown danh mục chỉ liệt kê danh mục **đang hoạt động**…
- [ ] …nhưng màn Sửa/Chi tiết vẫn hiện đúng tên danh mục **đã khóa** đang gắn với bản ghi (🔒)
- [ ] Có `unsavedChangesMixin` + gọi `markFormSaved()` sau khi lưu thành công
- [ ] Chưa đổi gì mà bấm Hủy → **không** hiện popup confirm
- [ ] Date picker: click ra lịch **và** gõ tay được, định dạng `dd/mm/yyyy`

### E. Chi tiết
- [ ] Số phiếu hiện ngay dưới/sau tiêu đề màn
- [ ] Tiêu đề `Chi tiết <đối tượng>: <mã>` — không có mã thì để trần, không lấy tên thay
- [ ] Lịch sử mặc định **ẩn**, click mới mở; có đủ 3 bộ lọc (Loại hành động / Người thực hiện /
      Khoảng thời gian); sắp mới → cũ; dropdown người thực hiện dạng `Mã phòng – Tên NV`

### F. Import / Xuất
- [ ] Import dùng `V2BaseImportModal`; có file mẫu tải về được
- [ ] Validate trước khi import; dòng lỗi đỏ sửa được tại chỗ, dòng hợp lệ xanh và khóa
- [ ] Vẫn import được khi còn dòng lỗi (chỉ import dòng hợp lệ)
- [ ] Xuất file: mở popup **chọn trường** trước, thứ tự cột theo user chọn
- [ ] Nút xuất bị khóa khi đang xuất + có dòng tiến độ

### G. Thông báo & xác nhận
- [ ] Toast thành công/thất bại dùng **đúng câu** trong bảng QLDA
- [ ] Mọi popup xác nhận dùng `base-confirm-modal` / `$confirm()`, không tự khai `b-modal`
- [ ] Thông báo nghiệp vụ (chuông/push) theo template
      `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`, tên ≤ 50 ký tự và in đậm,
      tổng ≤ 120 ký tự, deep-link kèm ID

### H. Bản ghi đã khóa
- [ ] BE chặn `update`/`destroy` bằng **423 LOCKED** (middleware nếu controller nhận `FormRequest`)
- [ ] FE **ẩn** nút Sửa/Xóa khi khóa; vào màn Sửa bằng URL trực tiếp → đá về Chi tiết
- [ ] Có lối **Mở khóa**, và Khóa/Mở khóa đều **ghi lịch sử**

---

## Bẫy hay dính khi port

| Bẫy | Hậu quả | Cách tránh |
|---|---|---|
| Port nút nhưng bỏ điều kiện ẩn/hiện của ERP | User không đủ điều kiện vẫn bấm được | Bước 1 ghi cả điều kiện, bước 5 đối chiếu lại |
| Danh sách gate `perm && isActive`, chi tiết chỉ gate `perm` | 2 màn lệch số nút | Đọc điều kiện từ **cùng 1 nguồn** (cờ BE `is_can_edit`) |
| Trùng `columnScreenKey` / `localStorageKey` với màn khác | 2 màn ghi đè cấu hình của nhau | Đặt theo slug màn, grep kiểm trùng |
| Tự dựng `<span class="status-pill">` | Badge lệch hẳn các màn khác | `V2BaseBadge` |
| STT tính `index + 1` | Sai từ trang 2 | `getNumericalOrder(currentPage, pageSize, index)` |
| Cột Mã để `@click` trên `<div>` | Không mở được tab mới (vi phạm SRS) | `<nuxt-link>` |
| `V2BaseRowActions` so `action.key` | Nút bấm im ru | Nó emit **chuỗi key**, so `action === 'edit'` |
| `V2BaseButton` truyền `disabled` | Không có prop đó → nút vẫn bấm được | Ẩn nút bằng `visible`, đừng disable |
| `$axios` tải file thiếu `Authorization` | Xuất Excel 401 | Tự gắn token cho request export |
| Bê nguyên `title` cho panel lọc | Mỗi màn một tiêu đề khác nhau | Bỏ prop, dùng mặc định "Bộ lọc danh sách" |
| Đổi route mà quên dữ liệu đã lưu URL trong DB | Màn bị đá 404 | Grep xem đường dẫn có bị lưu DB / so khớp ở BE không; redirect FE **không** cứu được |

---

## Khi phát hiện project đang có nhiều kiểu khác nhau

**Nêu ra cho user chọn kiểu chuẩn. KHÔNG tự chọn rồi làm tiếp, cũng KHÔNG tự sửa đại trà các màn cũ.**

## Tài liệu liên quan

| Nội dung | Đọc thêm |
|---|---|
| Bảng tra quy tắc chung (SRS) | `references/srs-quy-tac-chung.md` |
| Khuôn 4 màn + component/mixin | `references/khuon-man-mau.md` |
| Quyền theo cấp, `V2Footer`, badge | `.claude/skills/list-page/SKILL.md` |
| Nút, màu, icon | `.claude/skills/button-convention/SKILL.md` |
| Popup, modal, select trong modal | `.claude/skills/modal-popup/SKILL.md` |
| Validate form màn mới | `.claude/skills/form-validate/SKILL.md` |
| Cảnh báo thoát khi chưa lưu | `.claude/skills/unsaved-changes/SKILL.md` |
| Select / ô nhập ở mọi màn | `.claude/skills/select-and-input-state/SKILL.md` |
| Lịch sử thay đổi | `.claude/skills/entity-history/SKILL.md` |
| Thông báo nghiệp vụ | `.claude/skills/notification-convention/SKILL.md` |
| Import Excel | `.claude/skills/import-excel/SKILL.md` |
