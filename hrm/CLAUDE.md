# HRM Project — Hướng dẫn cho AI

## Scope thư mục

> **Thư mục gốc của dự án HRM là `HRM/`** (chứa file CLAUDE.md này).
> Tất cả đường dẫn tương đối trong file này (`.plans/`, `docs/`, `.claude/`, `hrm-api/`, `hrm-client/`, `Modules/`, `pages/`) đều tính từ thư mục `HRM/`, KHÔNG phải từ thư mục cha `ERP-HRM/`.
> Khi tạo file, đọc file, hay thao tác git — luôn thực hiện bên trong `HRM/`.

---

## Nguyên tắc chung

- Luôn gợi ý và làm việc bằng tiếng Việt
- Không xử lý commit hay đẩy code lên git
- Không đọc file thư viện hệ thống — tốn token không cần thiết
- Ưu tiên dùng helper có sẵn, tạo helper mới nếu logic dùng lại nhiều nơi
- Khi cần sửa hàm dùng chung → hỏi ý kiến trước khi làm
- **SKILL THẮNG SPEC KHI VỀ HÌNH THỨC UI.** Quy ước trong `.claude/skills/` (chữ trên nút, variant/màu, icon, thứ tự nút, khuôn popup, cách hiển thị…) là **chuẩn cao nhất** — mô tả task Redmine / URD / yêu cầu khách viết khác thì **theo skill**, không copy nguyên văn spec. Spec quyết định **nghiệp vụ** (làm gì, điều kiện nào, chặn ở đâu); skill quyết định **trình bày** (chữ gì, màu gì, icon gì, nằm ở đâu).
  - Ví dụ: spec ghi nút "Tiếp tục trình duyệt" nhưng bảng text chuẩn của `button-convention` cấm chữ "Trình duyệt" → đặt "Tiếp tục gửi duyệt".
  - **Lệch nhau thì PHẢI confirm lại với user trước khi code**, nêu rõ: spec ghi gì · skill quy định gì · đề xuất theo hướng nào. KHÔNG tự chọn im lặng, cũng không mặc định chiều theo spec chỉ vì khách nghiệm thu theo từng chữ.
  - Chốt xong theo hướng nào thì ghi lại vào `.plans/[feature]/design.md` mục "Quyết định đã chốt" để lần sau không hỏi lại.
- **BẮT BUỘC rà project trước khi làm bất kỳ UI/logic nào — không tự phát minh kiểu mới.** Trước khi code 1 thành phần (icon, tooltip, popup, badge/chip, bảng, filter, upload, phân trang, xác nhận xoá, kéo thả, biểu đồ, export…) phải **grep xem trong project đã có chỗ nào làm chưa, kể cả ở phân hệ/chức năng khác**, rồi **copy đúng pattern đó** hoặc tách ra component dùng chung. Mỗi màn tự làm một kiểu là lỗi, không phải "tuỳ ý thiết kế".
  - Cách rà: grep theo class/tên component đặc trưng (vd `custom-class="info-popover"`, `V2Base`, `draggable`, `BaseConfirmModal`), và quét `.claude/skills/` xem đã có SKILL.md quy định chưa.
  - Đã có ≥1 màn làm đúng → **bám theo màn đó**, ghi rõ trong plan.md: "copy pattern từ `<file:dòng>`".
  - Chưa có ở đâu → tự thiết kế, nhưng phải **tách thành component/util dùng chung** ngay từ lần đầu và bổ sung SKILL.md để lần sau không lệch.
  - Phát hiện project đang có **nhiều kiểu khác nhau** cho cùng 1 thứ → nêu ra cho user chọn kiểu chuẩn, KHÔNG tự chọn rồi làm tiếp, cũng KHÔNG tự sửa đại trà các màn cũ.
- **Icon Info (chữ "i") + tooltip mô tả**: dùng `ri-information-line` 14px màu `#94a3b8` + `b-popover` với `custom-class="info-popover"`. KHÔNG dùng `fa-info-circle`, không tự vẽ vòng tròn chữ `i`, không dùng `title=""` thuần, không dùng `v-b-tooltip`. Chi tiết + trường hợp icon nằm trong dropdown select2: `.claude/skills/info-icon-tooltip/SKILL.md`
- FE: Tuân thủ style list của module đang triển khai (mỗi module có thể khác nhau)
- **MÀN MỚI: MỌI element form phải dùng component `V2Base*`, TUYỆT ĐỐI không viết HTML thô.** `<input>` → `V2BaseInput` (ngày → `V2BaseDatePicker`, tiền → `V2BaseCurrencyInput`, file → `V2BaseFile`) · `<textarea>` → `V2BaseTextarea` · `<select>` → `V2BaseSelect` · `<label>` → `V2BaseLabel` (tự render dấu `*` + icon ⓘ tooltip) · `<button>` → `V2BaseButton` / `V2BaseIconButton` · badge → `V2BaseBadge`. Ô chỉ để ĐỌC vẫn dùng `V2Base*` + `disabled`, KHÔNG `<input readonly>` thô. Lý do: rule `vee-validate` nằm trong mixin `v2ValidateMixin` của chính các component này (viết thô là mất validate realtime), và kiểu ô khoá dùng chung chỉ nhắm vào class `.v2-input`/`.v2-textarea`. Tự kiểm: `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/<màn>/ | grep -v V2Base` phải RỖNG. Bảng tra đầy đủ: `.claude/skills/form-validate/SKILL.md` mục 1b
- FE: Select trong modal/popup BẮT BUỘC dùng `V2BaseSelectInModal` thay cho `V2BaseSelect` (chi tiết xem `.claude/skills/modal-popup/SKILL.md`)
- Trước khi làm màn danh sách mới → hỏi có cần phân quyền theo cấp không
- Trước khi viết accessor `is_can_delete` → hỏi điều kiện xóa cụ thể của màn đó
- Mọi form có validate: BE phải rethrow `ValidationException` (không catch chung `Exception`), FE phải hiện lỗi inline tại từng input required (viền đỏ `is-invalid` + text lỗi `invalid-feedback`), dùng flag `touched` để chỉ hiện sau lần submit đầu (áp dụng cho màn cũ)
- **Màn MỚI: validate realtime bằng `vee-validate` gắn trên component `V2Base*`** — chỉ trường **Tên** mới gắn `required` ở FE (vì Lưu nháp không được chặn các trường khác), required còn lại do BE quyết theo `status` rồi trả 422 → FE map vào `formError`. Chi tiết: `.claude/skills/form-validate/SKILL.md`
- **Cờ phân quyền phải fail-closed (KHÔNG BAO GIỜ hard-code `= true`)**: mọi cờ quyền FE (`canViewCostPrice`, `canEdit`, `canDelete`, `can_view_*`,…) BẮT BUỘC khởi tạo mặc định `false` và chỉ set từ `$store.state.permissions` (quyền thật) hoặc field BE trả về. TUYỆT ĐỐI không gán literal `true` cho cờ quyền (kể cả ở màn tạo mới / khi "chưa có data") — đây là lỗ hổng fail-open làm lộ dữ liệu nhạy cảm (vd giá vốn). Nếu màn tạo mới cần hiện dữ liệu do user tự nhập, dùng cờ nghiệp vụ riêng (vd `hasUserCreatedProducts`), KHÔNG bật cờ quyền. BE: mọi endpoint trả dữ liệu nhạy cảm (giá vốn/cost, lương…) phải gate bằng `isCurrentEmployeeHasPermission('<Tên quyền>')` trước khi trả, trả `null` nếu không quyền — không dựa vào FE ẩn (defense-in-depth). Khi review: chặn pattern `can[A-Za-z]*\s*=\s*true`.
- **Chỗ nào cho chọn/đính kèm file thì dùng `components/V2BaseFile.vue`** (khuôn "Import tài liệu kèm biên bản" của màn Meeting: nút `⬆ Chọn tệp` → đang tải → icon theo loại file + tên + Tải xuống/Thay đổi/Xóa). Cần cả BẢNG tài liệu thì dùng `components/FileAttachmentTable.vue`. KHÔNG tự dựng `<input type="file">` + `<label class="btn">`. Chi tiết: `.claude/skills/form-validate/SKILL.md` mục 1d
- **Màn IN (`**/print.vue`) phải vẽ KHUNG TỜ GIẤY ở bản xem trước**: `#content` rộng đúng khổ (`210mm` dọc / `297mm` ngang), padding bằng lề `@page`, viền `1px #d3d3d3` + bo 5px + bóng nhẹ, căn giữa bằng `margin: 0 auto` (KHÔNG flex `align-items:center` — nó căn giữa cả nút In). Nền quanh giấy dùng CHUNG màu **xám `#eee`** ở **mọi** màn in, dọc lẫn ngang (đừng mỗi màn một màu) — màu này đã nằm sẵn trong `layouts/print.vue`, màn in KHÔNG khai `background` riêng; lớp bọc `.print-preview` chỉ cần `min-height: 100vh` + `display: flow-root` (thiếu `flow-root` là hở dải khác màu 16px ở đầu trang). Nút **In** là `V2BaseButton primary size="sm"` như bình thường, **căn phải** thẳng mép phải tờ giấy. Thông số copy từ ERP `print.blade.php` / `print_landscape.blade.php`. Chi tiết: `.claude/skills/print-page/SKILL.md` mục 2c
- **Bảng tràn ngang phải có thanh cuộn ở CẢ TRÊN VÀ DƯỚI** — màn danh sách đã có sẵn trong `V2BaseDataTable`; bảng viết tay trong form/modal thì bọc `components/V2BaseTableScroll.vue` (tự đo độ rộng, đồng bộ `scrollLeft` 2 chiều, `ResizeObserver`, tự ẩn thanh trên khi không tràn). KHÔNG chép lại cặp `topScroll`/`tableWrapper` cho từng màn. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 3b-1
- ⚠️ **`.text-muted` trong hrm-client là màu ĐỎ** — 4 file SCSS toàn cục ép `color: #dc3545 !important`. Dòng "không có dữ liệu", ghi chú phụ… dùng `.text-muted` sẽ ra đỏ, user tưởng lỗi. Dùng xám `#6b7280` thay thế. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 3b-2
- **CHỮ MÀU ĐỎ CHỈ DÙNG CHO LỖI VALIDATE** (chốt 2026-08-15). Text mô tả, dòng phụ đề trong popup
  (`Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`), ghi chú, hướng dẫn, nhãn thông tin… đều dùng chữ
  XÁM (`#6b7280` cho nhãn, `#374151` cho giá trị), KHÔNG in đậm và **KHÔNG bao giờ tô đỏ**. Đỏ chỉ
  dành cho: text lỗi validate dưới input (`invalid-feedback`), viền `is-invalid`, dấu `*` bắt buộc,
  giá trị CŨ trong lịch sử thay đổi, và nút nhóm nguy hiểm (Xóa/Từ chối). Dùng đỏ cho chữ mô tả làm
  user tưởng đang có lỗi.
- **Khối NHÓM trong màn form/chi tiết dùng `components/V2BaseFormSection.vue`** (card + tiêu đề + slot `#actions` cho nút bên phải) — KHÔNG tự dựng `<div class="card"><div class="card-header">…` cho từng màn. Khuôn gốc: mục "Địa chỉ giao hàng" màn `/assign/customers/{id}`. Trước khi có component này, markup + SCSS `.card-header.section-header` bị copy-paste ở **35 file**, mỗi nơi lệch một chút. Chi tiết: `.claude/skills/form-validate/SKILL.md` mục 1c
- **Mọi popup MỚI dựng trên `components/modal/V2BaseModal.vue`** — khuôn dùng chung đã chốt sẵn:
  body cuộn riêng padding `0.5rem` (sát, không thừa khoảng trắng), **footer ghim đáy luôn nhìn thấy**
  kể cả khi nội dung dài, header có icon tròn + tiêu đề + dòng mô tả bản ghi. KHÔNG tự khai
  `b-modal` + header + footer riêng cho từng màn. Chi tiết: `.claude/skills/modal-popup/SKILL.md` mục 0
- **Mọi popup XÁC NHẬN dùng đúng 1 component `components/modal/base-confirm-modal.vue`** (Xóa, Khóa/Mở khóa, Duyệt/Từ chối, Hủy, thoát khi chưa lưu…). Gọi từ code ngoài template thì dùng `await this.$confirm({...})` — plugin render chính component đó. TUYỆT ĐỐI không tạo confirm riêng cho từng màn và không dùng `$bvModal.msgBoxConfirm()`. Chi tiết: `.claude/skills/modal-popup/SKILL.md` mục 3a
- **Mọi màn form (Tạo mới/Sửa) phải cảnh báo khi thoát lúc chưa lưu** — dùng mixin có sẵn `@/utils/mixins/unsavedChangesMixin`, gọi `markFormSaved()` sau khi lưu thành công; KHÔNG tự viết `beforeRouteLeave` riêng. Chi tiết: `.claude/skills/unsaved-changes/SKILL.md`
- **Mọi thông báo nghiệp vụ (chuông/push/socket) theo template `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`** — tên đối tượng ≤ 50 ký tự và in đậm, tổng ≤ 120 ký tự, deep-link bắt buộc kèm ID. Chi tiết + bảng prefix/nhóm hành động: `.claude/skills/notification-convention/SKILL.md` (đọc trước khi code phần có thông báo)
- **Bản ghi ĐÃ KHOÁ thì KHÔNG cho sửa/xoá nữa — chặn ở BE, không chỉ ẩn nút ở FE** (áp cho mọi màn, mọi module: danh mục, khách hàng, phiếu, dự án…). Muốn sửa thì phải Mở khoá trước.
  - **BE (bắt buộc, là chốt chặn thật)**: mọi endpoint `update` / `destroy` / thao tác đổi dữ liệu phải kiểm tra trạng thái khoá NGAY ĐẦU HÀM, trước cả validate nghiệp vụ → trả `423 LOCKED` kèm message rõ ("Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật."). Đặt điều kiện trong 1 accessor/method của Entity (vd `isLocked()` / `isCanEdit()`) rồi dùng lại, KHÔNG rải `if ($x->status == ...)` khắp controller.
    - ⚠️ **Controller nhận `FormRequest` thì `if` ở đầu hàm KHÔNG chạy trước validate** — Laravel validate ngay lúc resolve tham số, payload thiếu trường sẽ trả `422` và guard không bao giờ tới lượt. Trường hợp này phải đặt guard ở **middleware route** (khuôn `CheckCustomerNotLocked` / `CheckServiceNotLocked`, alias `customerNotLocked` / `serviceNotLocked`), KHÔNG gắn cho route mở khoá và route chỉ đọc.
    - **Chặn update thì phải có lối MỞ KHOÁ** — màn nào chưa có thao tác mở khoá thì bổ sung endpoint + nút, nếu không bản ghi bị khoá sẽ kẹt vĩnh viễn.
  - **FE**: ẩn (KHÔNG disable) nút Sửa, Xoá và mọi nút thao tác đổi dữ liệu khi `is_locked` / `is_can_edit = false`; vào màn Sửa bằng URL trực tiếp thì chuyển về màn Chi tiết. FE chỉ là lớp trải nghiệm — **không được coi là đã chặn**.
  - **Ngoại lệ duy nhất là thao tác Mở khoá** (và các thao tác chỉ đọc: xem, in, export, xem lịch sử).
  - **Ẩn nút phải làm ĐỦ CẢ 2 NƠI**: dòng ở màn danh sách VÀ footer màn chi tiết (xem gạch đầu dòng dưới).
  - Thao tác Khoá/Mở khoá vẫn phải ghi lịch sử (nhóm "Thay đổi trạng thái" — xem `.claude/skills/entity-history/SKILL.md`).
- **Placeholder ô lọc phải nói đúng trường đó lọc gì**: ô chọn dùng `Chọn <tên trường>`, ô gõ tay dùng `Nhập <tên trường>`, ô tìm nhanh dùng `Tìm theo <các trường BE thực sự lọc>`. CẤM `Tất cả`, `Chọn...`, để trống — bộ lọc ≤ 3 ô chạy chế độ gọn KHÔNG có nhãn, placeholder là thứ duy nhất cho user biết ô đó là gì. Chi tiết: `.claude/skills/list-page/SKILL.md`
- **Chữ trong ô bảng để THƯỜNG, không in đậm — kể cả cột Mã.** Class dùng chung `.field-line` và `.v2-cell-link` đã để `font-weight: 400`; đừng thêm `font-weight-bold` / `titleBold` vào ô. Cần nhấn mạnh thì dùng badge/màu.
- **Badge trạng thái dùng component chung `V2BaseBadge`**, KHÔNG tự khai `<span class="status-pill">` / class badge riêng cho từng màn. **Chữ VÀ MÀU đều do BE quyết định** — Resource trả `status_text` + `status_color` (mã hex), FE chỉ hiển thị: `<V2BaseBadge :color="item.status_color">{{ item.status_text }}</V2BaseBadge>`. TUYỆT ĐỐI không map số → chữ và không tự chọn màu ở FE. Chỉ **danh mục dùng chung** (2–3 trạng thái cố định) mới dùng `variant` (`brand` = hoạt động, `required` = khoá/từ chối, `muted` = nháp) mà không cần BE trả màu. Toàn hệ thống dùng **đúng 9 mã màu chuẩn** (`#16A34A` hoàn thành · `#2563EB` đang thực hiện · `#D97706` chờ duyệt · `#F59E0B` cảnh báo · `#DC2626` từ chối/khoá · `#0EA5E9` theo dõi · `#7C3AED` chốt · `#64748B` nháp · `#6B7280` đã đóng) — trạng thái mới gán vào 1 nhóm có sẵn, KHÔNG tự chế mã màu mới. Khuôn: `pages/assign/pricing-requests/index.vue`. Chi tiết + bảng đầy đủ: `.claude/skills/list-page/SKILL.md` mục 3c
- **Nút KHÔNG DÙNG ĐƯỢC thì ẨN HẲN — không hiện rồi disable.** Áp cho MỌI lý do: không có quyền, **và cả** chưa đủ điều kiện nghiệp vụ (đã phát sinh chứng từ, sai trạng thái, đã khoá…). Điều kiện phải nằm trong `visible` / `v-if`, KHÔNG dùng `interactable` + `disabledTitle` để hiện nút xám. Áp cho cả cột Hành động ở màn danh sách lẫn footer màn chi tiết (nút ẩn ở danh sách thì phải ẩn ở chi tiết). Cần cho user biết vì sao không thao tác được thì ghi ở chỗ khác (cột Trạng thái, ghi chú trong form), không giữ nút xám trên giao diện.
- **Màn chi tiết/form: nút BẮT BUỘC đặt trong `V2Footer`**, không tự dựng khối `<div class="d-flex justify-content-end">` + loạt `V2BaseButton`. Hành động không có sẵn trong `V2Footer.menu`, hoặc cần variant/màu khác với mặc định của component, thì đưa vào slot `#custom-actions`. `V2Footer` tự render "Quay lại" ở cuối — đừng tự thêm. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 7.2
- **Thao tác xong thì QUAY VỀ MÀN DANH SÁCH** — Lưu nháp / Lưu / Lưu và gửi duyệt / Duyệt / Không duyệt / Từ chối / Hủy / Xóa: sau khi API thành công gọi `markFormSaved()` rồi `$router.push('<danh sách>')`, KHÔNG ở lại và KHÔNG đẩy sang màn chi tiết (user phải bấm "Quay lại" mới thấy kết quả là thừa 1 thao tác ở mọi lần lưu). Ngoại lệ: thao tác chưa kết thúc luồng (nút Duyệt chỉ là lối sang màn lập chứng từ tiếp theo). Nút "Quay lại" (`url-back`) phải trỏ về **nơi user đi vào** — màn mở từ màn khác qua query thì `url-back` là computed động. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 7.3
- **KHÔNG tự sửa giá trị user vừa nhập** — nhập vượt trần/dưới sàn/sai định dạng thì **báo đỏ ngay dưới ô** và giữ nguyên số user gõ; cấm kéo về max/min, làm tròn, cắt ký tự, tự xoá dòng trống. Báo bằng toast thay cho lỗi dưới ô cũng sai (bảng dài không biết dòng nào hỏng). Còn lỗi thì không gọi API. Chi tiết: `.claude/skills/form-validate/SKILL.md` mục 3
- **Tiêu đề màn chi tiết chỉ ghép mã khi bản ghi CÓ mã**: `Chi tiết <đối tượng>: <mã>`. Bảng không có cột mã → để tiêu đề TRẦN, **không lấy tên thay thế** (tên dài làm tiêu đề/tab lê thê mà không giúp định danh).
- **Hành động ở màn CHI TIẾT phải khớp màn DANH SÁCH của đúng bản ghi đó** — giống cả danh sách hành động lẫn **điều kiện hiện/ẩn**. Với cùng 1 bản ghi, số nút ở 2 màn phải bằng nhau (chi tiết chỉ được thiếu "Xem" vì đang ở màn xem, và "Lịch sử" nếu đã có mục Lịch sử nhúng sẵn trong form). Nút ẩn ngoài danh sách mà chi tiết vẫn hiện là SAI. Sai hay gặp: danh sách gate `perm.edit && isActive`, chi tiết chỉ gate `perm.edit`. Điều kiện nên đọc từ cùng 1 nguồn (cờ BE `is_can_edit`/`is_can_delete` hoặc computed dùng chung). **Sửa điều kiện của 1 hành động thì phải kiểm cả 2 nơi trước khi báo xong.** Chi tiết + cách tự kiểm: `.claude/skills/list-page/SKILL.md` mục 7.2
- **Danh mục bị khoá / ngừng hoạt động vẫn phải hiện ở bản ghi đang dùng nó** (nghiệp vụ xuyên suốt MỌI màn, mọi module): dropdown/select lấy từ danh mục (giai đoạn dự án, loại hình, lĩnh vực, nguồn khách hàng, phòng ban, chức danh…) mặc định chỉ liệt kê bản ghi còn hoạt động (`is_active = 1` / chưa khoá), NHƯNG khi mở màn Sửa/Chi tiết của đối tượng đã chọn giá trị nay bị khoá thì giá trị đó BẮT BUỘC vẫn là 1 option và hiển thị đúng tên — không được để select trống, không tự đổi sang giá trị khác, không mất dữ liệu khi lưu lại.
  - **BE**: API danh mục nhận thêm id đang dùng (vd `include_ids` / `current_id`) → `where('is_active', 1)->orWhereIn('id', $includeIds)`. Nếu không sửa được API danh mục thì Resource của đối tượng phải trả kèm object danh mục đang chọn (id + name) để FE merge.
  - **FE**: sau khi load options, nếu `form.xxx_id` có giá trị mà không có trong options → push object đang chọn (lấy từ data detail) vào mảng options. Hiển thị **đúng tên gốc**, KHÔNG thêm hậu tố kiểu `(đã khoá)` vào text.
  - **Đánh dấu bằng 🔒 — TỰ ĐỘNG**: BE trả cờ `is_locked`, FE **không phải khai gì**: `utils/select2LockedOption.js` đã được `V2BaseSelect` + `V2BaseSelectInModal` gọi sẵn, tự gắn `🔒 ` trước tên option ở **cả danh sách chọn lẫn ô đang hiển thị giá trị đã chọn** (kể cả chip của select chọn nhiều), và **tự ẩn option đã khoá mà bản ghi hiện tại KHÔNG dùng** — đổi sang giá trị khác là option khoá cũ biến mất ngay. KHÔNG nối chữ vào `name`, KHÔNG tự viết `templateResult` ở từng màn, **KHÔNG cache danh mục đã khoá vào store dùng chung** (nó rò sang bản ghi khác — xem `optionsSelect/fetchProjectPhases` + `utils/mixins/projectPhaseOptionsMixin.js`). ⚠️ Ngoại lệ: wrapper nào **tự khai `templateResult`** (vd `DescriptionInfoSelect.vue`) thì helper nhường quyền → wrapper đó phải tự gắn `LOCKED_OPTION_PREFIX`, nếu không 🔒 mất im lặng. Chi tiết: `.claude/skills/select-and-input-state/SKILL.md` mục 1.
  - Áp dụng cả cho filter màn danh sách (giá trị đang lọc/đã lưu), cột hiển thị trong bảng và màn in/export.
- **Code phải TỐI ƯU HIỆU NĂNG, không phải "chạy được là xong"** — mọi màn/API viết ra đều phải cân nhắc số request, số query, khối lượng dữ liệu trả về. Cụ thể:
  - **FE: 1 màn = càng ít API càng tốt.** Không bắn hàng loạt API rời rạc lúc mở màn — gom danh mục dùng chung vào 1 endpoint tổng hợp (vd `GET .../form-options`) hoặc trả kèm trong API detail. TUYỆT ĐỐI không gọi API trong vòng lặp / trong `v-for` (mỗi dòng 1 request).
  - **Lazy load**: danh mục chỉ dùng ở tab/modal/select chưa mở → chỉ gọi khi mở, không gọi ở `mounted`. Select danh mục lớn (khách hàng, nhân viên, hàng hoá…) dùng search server-side có `limit`, KHÔNG load toàn bộ danh sách.
  - **Cache & huỷ request**: danh mục ít thay đổi (phòng ban, chức danh, đơn vị tính…) lưu Vuex/localStorage, không gọi lại mỗi lần vào màn. Ô tìm kiếm gõ liên tục → debounce ≥ 300ms + cancel request cũ.
  - **BE: cấm N+1 query** — luôn `with()` / `load()` eager load quan hệ dùng trong Resource; đếm/tổng hợp bằng `withCount` / `selectRaw`, không loop `->count()` từng dòng.
  - **Luôn phân trang**, không trả cả bảng. KHÔNG dùng `per_page` khổng lồ (5000…) — có endpoint `search?limit=` thì dùng. Chỉ `select` cột thực sự cần, không `SELECT *` rồi map.
  - **Index DB**: cột dùng `where` / `join` / `order by` thường xuyên phải có index; thêm bảng mới hoặc filter mới → kiểm tra index trước khi bàn giao.
  - Xử lý nặng (export, tính lương, tổng hợp báo cáo) → queue/job hoặc chunk, không chạy đồng bộ trong request.
  - **Xuất file danh sách > 2s → chia nhỏ API + dựng file ở FE**: BE thêm `GET <màn>/export-rows` trả JSON theo trang (2.000 dòng/lượt, trần 5.000), FE gọi lặp bằng `utils/export/listExportFile.js` rồi tự dựng Excel + hiện dòng tiến độ. `DynamicExport` (`FromView`) chỉ hợp danh mục nhỏ — đo thật: 5.365 dòng × 13 cột mất **10,8s** ở BE, còn **~4s** khi chia trang. Khuôn: `/assign/customers`, `/sale/warranty-repair-requests`. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 14c
  - Khi review/bàn giao: 1 màn gọi > 5 API lúc load, hoặc 1 request > 2s → phải nêu ra và đề xuất phương án gộp/tối ưu, không im lặng cho qua.
- **Logo/letterhead trên MỌI bản in + file Excel chứng từ**: nguồn duy nhất là `companies.header` (và `companies.logo`), lấy theo **`company_id` GHI TRÊN CHỨNG TỪ** — KHÔNG lấy theo người tạo phiếu, càng KHÔNG lấy theo người đang đăng nhập (thủ quỹ công ty A in phiếu công ty B là ra sai letterhead). Dùng NGUYÊN giá trị trong DB (đã chuẩn hoá về URL tuyệt đối), chỉ ghép `ERP_URL` khi giá trị còn là path tương đối, và **thiếu `ERP_URL` thì trả nguyên path chứ KHÔNG trả chuỗi rỗng**. Khuôn copy: `BillIncomePrintService::headerUrl()`. Chi tiết + 3 cái bẫy đã trả giá: `.claude/skills/print-page/SKILL.md` mục 4b
- **ĐỊNH DẠNG SỐ TOÀN HỆ THỐNG THEO CHUẨN QUỐC TẾ: `,` ngăn cách hàng nghìn, `.` phần thập phân** (`1,234,567.89` · `26,520.00` · `85.5%`) — chốt 2026-08-26, **thay cho** lần chốt kiểu Việt Nam (`1.234.567,89`) ngày 2026-08-22. Áp cho **MỌI** nơi hiển thị số, không có ngoại lệ: bảng danh sách, form, popup, **bản in**, **file Excel xuất ra**, chuỗi `*_text` do BE trả sẵn, nội dung thông báo/ghi chú tự sinh.
  - **FE**: `Number(x).toLocaleString('en-US')`. **CẤM `toLocaleString('vi-VN')` cho SỐ** (ngày tháng không dính rule này — vẫn `dd/mm/yyyy`).
  - **BE**: `number_format($x, $precision)` — mặc định của PHP đã đúng chuẩn (`,` + `.`). **CẤM truyền tham số kiểu VN** `number_format($x, 0, ',', '.')` và biến thể `number_format($x, 0, '', '.')`.
  - **File Excel**: ô số phải là **SỐ THẬT + `data-format="#,##0"` / `numFmt`**, KHÔNG đổ chuỗi đã format sẵn vào ô (đổ chuỗi thì Excel báo "number stored as text", SUM ra 0, và dấu phân cách cứng luôn không đổi theo máy user). Chi tiết: `.claude/skills/export-excel/SKILL.md` mục 1.
  - **Ô NHẬP tiền cũng đã đồng bộ**: `components/V2BaseCurrencyInput.vue` hiển thị `1,234,567.89`; hàm `parseRawValue()` bỏ `,` và giữ `.` thập phân. Giá trị emit ra ngoài vẫn là **số thuần**, payload gửi BE không đổi.
  - **Rule validate**: dùng `number_only` · `positive_number` · `max_value_decimal` (đọc chuẩn quốc tế). 3 rule cũ `number_vn` / `positive_vn` / `max_value_vn` **đã bị GỠ** khỏi `plugins/vee-validate.js` ngày 2026-08-26 — đừng khai lại.
  - **Ngoại lệ giữ nguyên `vi-VN`**: format NGÀY GIỜ (`toLocaleDateString('vi-VN')`, `new Date(x).toLocaleString('vi-VN')`) và các luồng ĐỌC FILE IMPORT của user (`Modules/Payroll/ExcelImports/*`) — người dùng gõ Excel theo thói quen VN, phải giữ khoan dung.
  - **Tự kiểm trước khi bàn giao** — cả 2 lệnh phải RỖNG:
    `grep -rnE "(toLocaleString|Intl\.NumberFormat)\(\s*'vi-VN'" pages components utils | grep -v "new Date"` (hrm-client)
    `grep -rnE "number_format\([^)]+,\s*'.?',\s*'\.'\)" app Modules resources` (hrm-api)
- `.claude`, `.plans`, `docs`, `CLAUDE.md` là symlink sang `hrm-claude-config/` — ghi file vào các path này bình thường, KHÔNG cần hỏi xác nhận

---

## Tech Stack

|                |                                               |
| -------------- | --------------------------------------------- |
| **Backend**    | PHP 7.4, Laravel 8 (`^8.65`), MySQL, Redis    |
| **Auth**       | JWT (`tymon/jwt-auth ^1.0`) + Laravel Sanctum |
| **Permission** | `spatie/laravel-permission ^5.4`              |
| **Module**     | `nwidart/laravel-modules ^8.2`                |
| **Excel**      | `maatwebsite/excel ^3.1`                      |
| **Storage**    | AWS S3                                        |
| **Frontend**   | Nuxt 2.14 (Vue 2), Node 14.21.3               |
| **CSS**        | Bootstrap 4 + Bootstrap-Vue 2.15              |
| **State**      | Vuex 3.5                                      |
| **HTTP**       | @nuxtjs/axios                                 |
| **Date**       | dayjs, vue2-datepicker                        |
| **Editor**     | Quill, CKEditor 5                             |
| **Chart**      | ApexCharts, Highcharts, Chart.js              |

---

## Kiến trúc Module

| #   | Module                      | Backend             | Frontend          |
| --- | --------------------------- | ------------------- | ----------------- |
| 1   | Hành chính nhân sự          | `Modules/Human`     | `pages/human`     |
| 2   | Chấm công                   | `Modules/Timesheet` | `pages/timesheet` |
| 3   | Tính lương                  | `Modules/Payroll`   | `pages/payroll`   |
| 4   | Đào tạo                     | `Modules/Training`  | `pages/training`  |
| 5   | Giao việc ← đang phát triển | `Modules/Assign`    | `pages/assign`    |
| 6   | Quyết định                  | `Modules/Decision`  | `pages/decision`  |
| 7   | CRM                         | `Modules/CRM`       | `pages/client`    |

---

## Tài liệu chi tiết

| Cần gì                                           | Đọc file nào                                |
| ------------------------------------------------ | ------------------------------------------- |
| Base classes, V2Base components, API store calls | `docs/shared.md`                            |
| Pattern CRUD đầy đủ (code mẫu)                   | `docs/conventions.md`                       |
| Onboarding dev mới                               | `docs/onboarding.md`                        |
| Design + Plan của từng feature                   | `.plans/[feature]/` (xem quy luật bên dưới) |

---

## Convention Database (toàn project)

- **Cấp tổ chức**: luôn dùng `company_id`, `department_id`, `part_id` — tất cả `unsignedBigInteger nullable`. KHÔNG dùng `branch_id`.
- **Audit**: dùng `$table->timestamps()` (tạo `created_at`, `updated_at`) + thêm thủ công `created_by`, `updated_by` (`unsignedBigInteger nullable`). KHÔNG dùng SoftDeletes cho entity chính (chỉ dùng cho bảng phụ như comment/log nếu thực sự cần).
- **Model MỚI BẮT BUỘC `extends BaseModel`** (`use App\Models\BaseModel;`) — KHÔNG `extends Model` của Laravel. `BaseModel` có sẵn hook `creating`/`saving` tự gán `created_by` / `updated_by` và 2 quan hệ `employee_create()` / `employee_update()`. Thiếu nó thì cột **Người tạo / Người cập nhật** rỗng vĩnh viễn mà **không có lỗi nào báo ra** — code chạy bình thường, chỉ tới lúc QA soi bảng mới lộ (đã dính thật: `Nation` extends `Model` thuần → 100% bản ghi `nations.updated_by = NULL`).

  ```php
  use App\Models\BaseModel;

  class Foo extends BaseModel   // KHÔNG: class Foo extends Model
  {
      protected $table = 'foos';
      // created_by / updated_by PHẢI có trong $fillable, nếu không create() bỏ qua
      protected $fillable = ['name', 'status', 'created_by', 'updated_by'];
  }
  ```

  - Model **buộc** phải `extends Model` (kế thừa class khác, model bảng ERP có hook riêng…) → **service tự gán** `$obj->updated_by = auth()->id();` ở MỌI đường ghi: create, update **và cả khoá / mở khoá / đổi trạng thái** (đây cũng là một lần cập nhật, hay bị quên nhất). Ghi rõ lý do không dùng `BaseModel` ngay trên class.
  - **Luôn lấy `auth()->id()`** (= `employees.id`). TUYỆT ĐỐI không dùng `auth()->user()->info->id` — đó là id bảng `employee_infos`, ghi vào `updated_by` sẽ trỏ tới nhân viên không tồn tại, join ra rỗng y như chưa ghi (bug thật ở hook đồng bộ ERP cũ của `Area` / `Province` / `Ward`).
  - Xong một màn danh mục: **sửa thử 1 bản ghi rồi mở lại danh sách xem cột Người cập nhật có ra tên không.** Đây là cách DUY NHẤT phát hiện thiếu audit — không có exception, không có log.
- **Version solution**: các entity gắn với solution phải có `solution_version_id` NOT NULL. Nếu áp dụng cả cấp module thì thêm `solution_module_id` + `solution_module_version_id` (nullable).
- **File đính kèm**: KHÔNG tạo bảng pivot riêng. Dùng bảng `files` chung với `table='<table_name>'` + `table_id=<entity_id>`. Model khai báo:
  ```php
  public function files() {
      return $this->hasMany(File::class, 'table_id', 'id')
          ->where('table', '<table_name>');
  }
  ```
- **Mã code tự sinh**: pattern `PREFIX-YYYY-NNNNN`, implement `getNextCode()` trên Entity (copy pattern `BomList::getNextCode()`).
- **Permission**: Khi thêm/sửa/đổi tên/xóa permission → sửa trực tiếp trong file `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`. KHÔNG tạo migration riêng cho permission.
- **Middleware checkPermission**: Khi có quyền tương ứng trong `PermissionsTableSeeder`, các route thao tác dữ liệu (store, update, destroy, approve, toggle,...) phải gắn middleware `checkPermission:TênQuyền`. Route xem (index, show) chỉ gắn nếu có quyền xem riêng. Cú pháp: `->middleware('checkPermission:Tên quyền')`, nhiều quyền dùng `|`: `->middleware('checkPermission:Quyền A|Quyền B')`. Không gắn middleware nếu chưa có quyền tương ứng trong seeder.

**Skills tự động:** Trước khi thực hiện bất kỳ task nào, quét `.claude/skills/` → đọc tên thư mục → nếu task khớp với tên skill thì đọc `SKILL.md` tương ứng và follow hướng dẫn bên trong. Ví dụ: yêu cầu "tạo SRS" → đọc `.claude/skills/srs-documenter/SKILL.md`, yêu cầu "fix bug" → đọc `.claude/skills/bug-fixer/SKILL.md`.

---

## Quy luật tổ chức tài liệu feature

Tất cả tài liệu của 1 feature nằm trong `.plans/[feature]/`. KHÔNG tạo file trong `docs/superpowers/specs/`.

**Feature nhỏ (1-2 phase):**

```
.plans/[feature]/
├── design.md          ← design duy nhất
├── plan.md            ← plan duy nhất
├── SRS - <Tên màn hình>.docx ← SRS (tạo khi được yêu cầu, CHỈ 1 file .docx)
└── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
```

**Feature lớn (3+ phase):**

```
.plans/[feature]/
├── design.md          ← tóm tắt tổng thể feature (scope, hiện trạng, quyết định chung)
├── design-phase{N}.md ← design chi tiết cho từng phase lớn
├── plan.md            ← TẤT CẢ tasks (append phase mới vào cuối, trước checkpoint)
├── SRS - <Tên màn hình>.docx ← SRS (tạo khi được yêu cầu, CHỈ 1 file .docx)
├── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
└── (các file phụ: testcase, script...)
```

**Quy tắc:**

- `design.md`: tóm tắt chung, KHÔNG chứa spec chi tiết từng phase
- `design-phase{N}.md`: spec đầy đủ (DB, BE, FE, edge cases) — tạo khi phase có nhiều thay đổi
- `plan.md`: 1 file duy nhất chứa tất cả phase, append liên tục
- SRS: **CHỈ 1 file `.docx`** đặt tên `SRS - <Tên màn hình>.docx`, lưu cùng folder feature. Bám **form chuẩn của team** (`.claude/skills/srs-documenter/assets/SRS_MAU.docx` — **bản mẫu đổi 2026-08-17, nay là "SRS - Danh mục khách hàng"**). Form mới gọn còn **4 chương**: Phần 1 Giới thiệu / Phần 2 Phân quyền / Phần 3 Đặc tả chi tiết theo từng chức năng / Phần 4 Quy tắc nghiệp vụ — đã **bỏ** chương Tổng quan, mục Phạm vi, mục Quy tắc truy cập bắt buộc, chương Danh mục chức năng (Function list), mục Tiêu chí nghiệm thu và bảng thông tin trang bìa. Biểu đồ Use Case phải là **ảnh thật**; mục Layout màn hình của **mỗi chức năng** chỉ ghi **URL đầy đủ** (bỏ dòng Menu/Route) **VÀ kèm ảnh chụp thật** của chức năng đó. Bắt buộc đọc `.claude/skills/srs-documenter/SKILL.md` trước khi viết. (`srs.html` là format CŨ, chỉ còn ở feature sinh trước 2026-08-07, không tạo mới)
- Testcase: chỉ Excel (`testcase.xlsx`) — lưu cùng folder feature
- KHÔNG tạo `plan-phase{N}.md` riêng (đã có convention cũ nhưng không tiếp tục)

---

## ⚠️ Phần GỘP DATABASE — nhánh `gop_db` (bắt buộc cả team)

### 0. Cách nhận biết — NHÌN VÀO NHÁNH GIT, không đoán theo tên feature

**Bước bắt buộc trước mọi task đụng tới code:** kiểm tra nhánh đang đứng ở repo đang sửa.

```bash
git branch --show-current                              # nhánh hiện tại
git merge-base --is-ancestor gop_db HEAD && echo GOPDB # nhánh có checkout ra từ gop_db không
```

- Đang ở **`gop_db`**, hoặc nhánh **checkout ra từ `gop_db`** (lệnh trên in `GOPDB`) → **áp dụng toàn bộ mục 1-3 dưới đây**: tài liệu vào `.plans/gop-db/`, spec vào `docs/superpowers/specs/gop-db/`
- Đang ở nhánh khác (`tpe`, `tpe-develop-assign`, `main`…) → làm theo quy luật thường ở mục trên, tài liệu để `.plans/[feature]/`
- Nhánh không suy ra được (worktree lạ, detached HEAD) → **hỏi** trước khi tạo folder tài liệu, đừng đoán

### 1. Tài liệu — thêm 1 cấp `gop-db/`

```
.plans/gop-db/
├── STATUS.md                    ← STATUS RIÊNG của phần gộp DB (Đang làm / Tạm dừng / Hoàn thành)
├── design.md                    ← NỀN TẢNG chung của việc gộp DB (đọc TRƯỚC khi làm bất kỳ feature nào)
├── [feature-a]/design.md + plan.md
├── [feature-b]/design.md + plan.md
└── ...
docs/superpowers/specs/gop-db/YYYY-MM-DD-<feature>-design.md   ← spec chi tiết (cũng thêm 1 cấp gop-db/)
```

- Code đang làm trên nhánh `gop_db` (hoặc nhánh con của nó) → **KHÔNG** tạo folder ở `.plans/[feature]/` mà tạo ở **`.plans/gop-db/[feature]/`**, kể cả khi tên feature nghe không liên quan gì tới database (VD: `finance-account-catalog`)
- Ngược lại, nhánh khác → vẫn để ở `.plans/[feature]/` như cũ
- **STATUS riêng**: mọi cập nhật trạng thái (tạo feature mới, `wrap up`, chuyển mục, merge xong) ghi vào **`.plans/gop-db/STATUS.md`**, KHÔNG ghi vào `.plans/STATUS.md`. File gốc chỉ giữ 1 khối con trỏ sang đây
- Đầu session, nếu đang đứng trên nhánh `gop_db` → đọc **`.plans/gop-db/STATUS.md`** thay cho `.plans/STATUS.md`
- Cấu trúc bên trong mỗi feature giữ nguyên quy luật ở mục trên (design.md / plan.md / srs / testcase)

### 2. Code — luôn đứng trên nhánh `gop_db`

- Code của phần này **chỉ làm trên nhánh `gop_db`**, hoặc nhánh con **checkout ra từ `gop_db`** (KHÔNG checkout từ `tpe`, `tpe-develop-assign`, `main`)
- Xong việc → merge/PR **về lại `gop_db`**, không merge thẳng sang nhánh khác
- Trước khi code: kiểm tra nhánh hiện tại ở CẢ 2 repo (`git branch --show-current`); đứng sai nhánh thì `Modules/Finance`, `components/subsystems.js`, `pages/finance`… sẽ không tồn tại
- Mỗi người tự chọn cách làm việc trên nhánh này (checkout thẳng hay dùng git worktree riêng) — không bắt buộc theo ai. Nếu dùng worktree: worktree KHÔNG có `.plans/`, `.claude/`, `docs/`, `CLAUDE.md` (là symlink ra ngoài repo) → **tài liệu luôn ghi về `HRM/.plans/gop-db/`**, worktree chỉ chứa code

### 3. Ràng buộc thường trực trên nhánh `gop_db`

- **KHÔNG dùng `DB_CONNECTION_SECOND` / connection `mysql2`** cho bất kỳ tính năng mới nào, kể cả ghép tiền tố tên bảng bằng `env('DB_DATABASE_SECOND')` trong constructor model — `mysql2` đang trỏ DB ERP CŨ, id lệch
- Bảng trùng tên: **ưu tiên bản ERP**; bản HRM đã đổi tên thành `hrm_*` (24 bảng). Model con không khai `$table` sẽ đọc nhầm bảng ERP
- Trước khi làm bất kỳ feature nào trong nhóm này → **đọc `.plans/gop-db/design.md`** (7 gotcha khi port màn ERP → HRM)

---

## Quản lý session

**Bắt đầu session mới — bắt buộc theo thứ tự:**

1. Đọc `.plans/STATUS.md` — nếu đang đứng trên nhánh `gop_db` (hoặc nhánh con của nó) thì đọc `.plans/gop-db/STATUS.md`
2. Tìm feature đang ở mục "Đang làm"
3. Đọc `.plans/[feature]/design.md` + `plan.md` (nhánh `gop_db` → `.plans/gop-db/[feature]/`)
4. Báo lại: "Đang làm [feature], checkpoint cuối: [X], task tiếp theo: [Y]"
5. Chờ xác nhận trước khi bắt đầu

**Khi nhận yêu cầu làm tiếp / cập nhật feature đã có — theo thứ tự:**

1. Cập nhật `STATUS.md` → chuyển feature về "Đang làm"
2. Đọc lại toàn bộ `.plans/[feature-name]/` (design.md + plan.md)
3. Kiểm tra branch:
   - Feature đã merge vào nhánh hiện tại → hỏi có tạo branch mới để update không? (cả API và Client)
   - Feature vẫn ở branch riêng → hỏi có chuyển về branch đó để làm tiếp không? (cả API và Client)
4. Yêu cầu nhập spec để brainstorming yêu cầu mới

**Khi nhận yêu cầu "tạo tính năng mới" / "tạo feature" — làm NGAY:**

1. Tạo folder `.plans/[feature-name]/`
2. Tạo file `.plans/[feature-name]/design.md` (placeholder, sẽ fill sau brainstorming)
3. Tạo file `.plans/[feature-name]/plan.md` (placeholder, sẽ fill sau khi lên plan)
4. Tạo file `docs/superpowers/specs/YYYY-MM-DD-<feature-name>-design.md` (placeholder, sẽ fill sau brainstorming)
5. Cập nhật `STATUS.md` → thêm vào "Đang làm" (kèm link tới spec chi tiết)
6. Sau đó mới bắt đầu brainstorming / hỏi yêu cầu

**Phân biệt 3 tài liệu của 1 feature:**

- `.plans/[feature]/design.md` — **TÓM TẮT** (1-2 trang): mục tiêu, scope, các quyết định lớn, link sang spec chi tiết
- `.plans/[feature]/plan.md` — task **TỔNG QUÁT** theo Phase → BE/FE (định dạng progress-manager)
- `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` — **SPEC ĐẦY ĐỦ**: schema DB, migration script, API contract, validation rule, business rule chi tiết, edge case, downstream impact, UX chi tiết
- Khi brainstorming: fill `docs/superpowers/specs/...` trước (chi tiết) → tóm tắt vào `.plans/[feature]/design.md`
- Khi `wrap up` lần đầu: cả 2 file design phải đầy đủ

**Khi nhận yêu cầu mới (feature/fix/task) — BẮT BUỘC trước khi code:**

1. Cập nhật `.plans/[feature]/plan.md` với danh sách task cụ thể
2. Đánh `[x]` khi xong mỗi task
3. Kể cả fix bug nhỏ cũng phải có task trong plan.md

**Khi nghe "wrap up" — làm ngay 4 việc theo thứ tự:**

1. Cập nhật `plan.md` — đánh `[x]` task xong, ghi checkpoint
2. Cập nhật `STATUS.md` — trạng thái feature hiện tại
3. Nếu là lần wrap up đầu tiên của feature (design.md còn trống hoặc chỉ có placeholder) → cập nhật `.plans/[feature]/design.md` (tóm tắt) VÀ `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` (chi tiết đầy đủ) dựa trên hiểu biết đã tích luỹ trong session (scope, data structure, UI, business rules, API endpoints, edge case, downstream impact)
4. Báo ra chat: "Đã cập nhật xong. Bước tiếp theo: [X]"

Không làm gì khác cho đến khi 3 việc này xong.

**Checkpoint format bắt buộc:**

```
### Checkpoint — [timestamp]
Vừa hoàn thành: [task vừa xong]
Đang làm dở: [file + dòng + dừng ở đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```

**Quy tắc STATUS.md — chỉ cập nhật khi có 1 trong 4 sự kiện:**

1. Tạo feature mới → thêm vào "Đang làm"
2. Nghe "wrap up" → cập nhật Checkpoint
3. Chuyển feature → move giữa các mục
4. Merge xong → move vào "Hoàn thành", giữ tối đa 3 entry

---

## Quy tắc team

- `CLAUDE.md`, `.claude/skills/`, `docs/` là tài sản chung — sửa qua PR, không tự ý sửa
- Mỗi dev KHÔNG tạo CLAUDE.md, .claude/skills/, docs/ riêng
- Mỗi feature trong `.plans/` ghi rõ người phụ trách (`@username`)
- Muốn thêm skill mới → tạo PR với SKILL.md đầy đủ
- Dev mới vào → đọc `docs/onboarding.md` trước

---

## Custom skills

Các skill tùy chỉnh nằm trong `.claude/skills/`.
Trước khi implement bất kỳ pattern lặp lại nào,
kiểm tra `.claude/skills/` xem đã có SKILL.md chưa.
Nếu có → đọc trước khi viết code.

**Skill bắt buộc đọc theo ngữ cảnh:**

| Khi làm gì                                          | Đọc skill nào                                |
| --------------------------------------------------- | -------------------------------------------- |
| **Chuyển/port màn từ ERP sang HRM** (dựng lại màn theo mẫu ERP) | `.claude/skills/erp-to-hrm-screen/SKILL.md` |
| Tạo/sửa button (nút bấm) trên FE hrm-client         | `.claude/skills/button-convention/SKILL.md`  |
| Tạo/sửa modal, popup, dialog trên FE hrm-client     | `.claude/skills/modal-popup/SKILL.md`        |
| Tạo màn danh sách mới ở hrm-client                  | `.claude/skills/list-page/SKILL.md` (nếu có) |
| Làm code trong project **elearning** (Vue 3 + Vite) | `.claude/skills/elearning-base/SKILL.md`     |
| Validate, error, toast trong elearning              | `.claude/skills/elearning-validate/SKILL.md` |
| Auth, SSO, profile, avatar trong elearning          | `.claude/skills/elearning-auth/SKILL.md`     |
| Viết tài liệu HDSD / hướng dẫn sử dụng màn hình     | `.claude/skills/hdsd-documenter/SKILL.md`    |
| Lịch sử thay đổi / audit log (BE ghi log + UI)      | `.claude/skills/entity-history/SKILL.md`     |
| **Viết MÔ TẢ NGHIỆP VỤ** (dùng để làm gì, luồng chạy, ai nhận thông báo) | `.claude/skills/business-flow-documenter/SKILL.md` |
| Viết tài liệu SRS / đặc tả yêu cầu màn hình         | `.claude/skills/srs-documenter/SKILL.md`     |
| Viết tài liệu test case cho màn hình                | `.claude/skills/testcase-documenter/SKILL.md` |
| Bắn/sửa thông báo nghiệp vụ (chuông, push, socket)  | `.claude/skills/notification-convention/SKILL.md` |
| Tạo/sửa màn form (add/edit, modal nhập liệu)        | `.claude/skills/unsaved-changes/SKILL.md`    |
| Validate form ở màn mới (realtime, required, lỗi)   | `.claude/skills/form-validate/SKILL.md`      |
| Icon Info (chữ "i") + tooltip/popover mô tả         | `.claude/skills/info-icon-tooltip/SKILL.md`  |
| Đụng tới **select / ô nhập** ở BẤT KỲ màn nào (form, modal, chi tiết, bộ lọc) | `.claude/skills/select-and-input-state/SKILL.md` |
| Select danh mục **mất giá trị đã chọn**, danh mục bị khoá/ngừng hoạt động, icon 🔒 | `.claude/skills/select-and-input-state/SKILL.md` |
| Ô nhập disabled/readonly sai màu hoặc vẫn bấm được; focus ra viền xanh/quầng sáng | `.claude/skills/select-and-input-state/SKILL.md` |
| Xuất Excel ở BE (class `*Export` + blade `exports/`) | `.claude/skills/export-excel/SKILL.md`       |
| Tạo/sửa màn IN (`print.vue`) · logo/letterhead đầu chứng từ | `.claude/skills/print-page/SKILL.md`         |

→ Gặp ngữ cảnh trên → **đọc SKILL.md trước khi viết code**, không cần user nhắc.

**Nguyên tắc viết tài liệu hướng dẫn (HDSD):** Phải CỰC KỲ CHI TIẾT, click-by-click tới từng hành động nhỏ. Liệt kê nút thôi là CHƯA ĐỦ — mỗi nút Tạo mới/Sửa/Duyệt/Nhập kết quả/Xóa… phải mô tả form mở ra, **từng trường nhập (bắt buộc + giá trị mặc định/điền sẵn)**, cách lưu, kết quả. Ảnh **chụp thật** từ hệ thống (Playwright MCP). Theo `.claude/skills/hdsd-documenter/SKILL.md`.

---

## Lưu ý fix bug

Lỗi BE → đọc log tại:
`hrm-api/storage/logs/laravel-[ngày-hôm-nay].log`

---

## Khi làm việc với git
- Repo API nằm ở: /hrm-api
- Repo Client nằm ở: /hrm-client

---

## ⚠️ Line ending — GIỮ NGUYÊN CRLF

Nhiều file trong `hrm-client` (và một số file `hrm-api`) đang dùng **CRLF (`\r\n`)**. Khi sửa code **KHÔNG được đổi line ending của file** — đổi cả file sang LF làm diff phình lên hàng nghìn dòng giả, che mất thay đổi thật và gây conflict vô nghĩa khi merge.

- **Kiểm tra trước khi sửa** file lạ: `file <path>` (thấy `with CRLF line terminators`) hoặc `grep -c $'\r' <path>`
- File đang CRLF → dòng **mới thêm vào cũng phải kết thúc bằng `\r\n`**, KHÔNG trộn 2 kiểu trong 1 file
- **Nguy hiểm nhất là sửa hàng loạt bằng script** (Python `open().write()`, `sed -i`, `awk`, prettier/eslint `--fix`): mặc định ghi ra LF → nuốt sạch `\r` toàn file. Dùng Python thì mở `newline=''` cho cả đọc lẫn ghi
- Sau khi sửa bằng script, **luôn chạy `git diff --stat` kiểm tra**: số dòng thay đổi lớn bất thường (cả file bị đánh dấu đổi) = đã phá line ending → trả lại ngay, không commit đè
- KHÔNG tự ý thêm `.gitattributes`, đổi `core.autocrlf`, hay "chuẩn hoá toàn bộ repo về LF" — muốn làm phải hỏi trước

## Không làm

- Không commit hay push git khi chưa có yêu cầu
- Không đọc file trong `vendor/`, `node_modules/`
- Không tự sửa hàm dùng chung khi chưa được xác nhận
- Không tự quyết định điều kiện `is_can_delete` — phải hỏi
- Không tự thêm phân quyền theo cấp — phải hỏi

---


