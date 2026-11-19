# Danh bạ cá nhân (gắn vào Nhắc việc cá nhân) — web + app

> Brainstorm 07/11/2026 với user. Nhánh `gop_db` (hrm-api, hrm-client) · TPE_APP nhánh `develop` (hỏi lại nhánh trước khi sửa).
> Mockup app (Pencil): `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` — khu **VIỆC CỦA TÔI (APP)**,
> **Nhóm ② Danh bạ cá nhân** (x 25400, y −1580): DB-01…DB-09. Web chưa có mockup (mô tả ở §6).
> Liên quan: `.plans/my-todo/design.md` (form nhắc việc, "Loại nhắc việc" chốt 07/11), `.plans/gop-db/lich-cong-tac-lanh-dao/design.md`.
> **Chưa có lệnh code** — mọi bước code / migration / quyền phải xin phép riêng (CLAUDE.md gốc).

## 1. Vì sao làm

Ví dụ thật của user: vừa có thông tin một khách hàng, hẹn 3 ngày sau trao đổi → muốn tạo nhắc việc NGAY, kèm thông
tin khách. Về sau còn nhiều lần nhắc việc với khách này → muốn có sẵn thông tin, không gõ lại, và xem lại được các lần
đã hẹn. Khách có thể là khách MỚI (chưa có trong danh mục KH công ty) hoặc KH ĐÃ CÓ.

## 2. Mục tiêu / Không làm / Thất bại nếu

- **Mục tiêu**: mỗi user có 1 danh bạ riêng (Tên*, SĐT*, Địa chỉ, Ghi chú); gắn 1 liên hệ vào nhắc việc ngay trong
  form, chỉ khi cần; xem lại 1 liên hệ cùng mọi nhắc việc đã gắn với họ. Web + app như nhau (trừ phần danh bạ máy).
- **Không làm**: chia sẻ danh bạ cho người khác; ghi ngược vào danh mục KH công ty / lịch sử KH; đồng bộ TOÀN BỘ danh
  bạ điện thoại; gắn nhiều liên hệ cho 1 nhắc việc.
- **Thất bại nếu**: form nhắc việc rườm rà hơn khi KHÔNG dùng liên hệ; ô tìm biến thành chỗ dò danh mục khách hàng
  công ty (tìm theo tên, gõ vài số ra cả loạt KH); danh bạ sinh liên hệ rác (huỷ form vẫn lưu, trùng số tạo bản 2);
  người khác thấy được danh bạ / nhắc việc riêng.

## 3. Quyết định đã chốt (user, 07/11/2026)

1. **Chỉ quản lý cá nhân** — danh bạ và nhắc việc gắn liên hệ chỉ chủ nhân thấy; không móc vào hồ sơ KH công ty.
2. **KH công ty chỉ hiện để chọn khi tìm theo SĐT** — khớp SĐT khách hàng hoặc SĐT người liên hệ của KH đó. Không tìm
   KH công ty theo tên.
3. **Liên hệ đã dùng trong 1 nhắc việc thì tự vào danh bạ cá nhân** (kể cả chọn từ KH công ty → lưu bản sao).
4. Form gọn: dưới Tiêu đề chỉ 1 dòng **icon + "Gắn liên hệ"** (không nhãn, không khung). Chọn xong mới hiện ô
   "Liên hệ" (nhãn + thẻ). (DB-01, DB-05)
5. Sheet gắn liên hệ mở ra **hiện sẵn danh bạ** để chọn, chưa cần gõ (DB-02): dải "Gần đây" + danh sách A→Z.
6. Bắt đầu xem lại khách **từ danh bạ** → màn Danh bạ (DB-06) → Chi tiết liên hệ + nhắc việc với người này (DB-07).
7. **Danh bạ điện thoại (chỉ app)**: ① "Chọn từ danh bạ điện thoại" khi tạo liên hệ (bộ chọn hệ thống, chọn 1 người);
   ③ "Lưu vào danh bạ điện thoại" ở chi tiết liên hệ. KHÔNG đồng bộ toàn bộ danh bạ máy.
8. **Xoá liên hệ KHÔNG xoá nhắc việc** — nhắc việc giữ nguyên, chỉ bỏ liên kết liên hệ; hỏi xác nhận nêu số nhắc việc
   bị ảnh hưởng (DB-09).
9. **Web làm đầy đủ như app**: màn Danh bạ riêng + gắn liên hệ trong form nhắc việc.
10. Các điểm Claude đề xuất trong phiên đã được user "ok": vị trí dòng Gắn liên hệ dưới Tiêu đề; chỉ tra KH công ty khi
    gõ đủ số; trùng SĐT dùng lại liên hệ cũ; "Gần đây"; lối vào ở menu trái; dòng "Hẹn …" trong danh bạ; nút Nhắn tin
    mở app nhắn tin của máy.

## 4. Luồng & màn (mockup app)

| Màn | Nội dung |
|---|---|
| DB-01 | Form nhắc việc: dòng "Gắn liên hệ" dưới Tiêu đề. Không bấm → form như cũ |
| DB-02 | Sheet "Gắn liên hệ" vừa mở: tiêu đề + "24 người trong danh bạ của bạn", ô tìm, dải **Gần đây** (ô đầu "Thêm mới", avatar lớn, cuộn ngang, tối đa ~8), danh sách theo chữ cái + thanh chữ cái bên phải. Chạm 1 người = gắn + đóng |
| DB-03 | Đang gõ: nhóm "Trong danh bạ của bạn" (khớp tên / SĐT) + nhóm "Khách hàng công ty · khớp số điện thoại" + dòng "Tạo liên hệ mới với số …" |
| DB-04 | Sheet "Liên hệ mới": [Chọn từ danh bạ điện thoại] (app) · hoặc nhập tay Tên*, SĐT* (điền sẵn số vừa gõ), Địa chỉ, Ghi chú → [Gắn liên hệ] |
| DB-05 | Form đã gắn: ô "Liên hệ" = thẻ (avatar · tên · SĐT · công ty nếu từ KH công ty) + nút gọi + ✕ bỏ gắn; chạm thẻ → DB-02 đổi người |
| DB-06 | Màn **Danh bạ cá nhân** (menu trái Công việc): ô tìm, danh sách theo chữ cái, nút gọi mỗi dòng, dòng cam "Hẹn …" = nhắc việc CHƯA XONG có hạn gần nhất; nút 👤+ thêm liên hệ thủ công |
| DB-07 | **Chi tiết liên hệ**: avatar, tên, SĐT, ghi chú; nút Gọi · Nhắn tin · Tạo nhắc việc (form gắn sẵn người này); "Nhắc việc với {tên}": Sắp tới (chưa xong, hạn gần trước) + Đã xong (mới trước), mỗi dòng có nhãn Loại nhắc việc; chạm → chi tiết nhắc việc |
| DB-08 | Menu ⋮: Sửa liên hệ · Lưu vào danh bạ điện thoại (app) · Xoá liên hệ |
| DB-09 | Xác nhận xoá: "N nhắc việc đang gắn với {tên} vẫn được giữ nguyên, chỉ bỏ phần liên hệ…" [Xoá liên hệ] [Huỷ] |

Hình thức (Claude chốt khi vẽ, user khen bố cục ok sau 2 vòng chỉnh): avatar = chữ viết tắt trên 1 trong 6 màu nhạt cố
định theo liên hệ; liên hệ lấy từ KH công ty có huy hiệu toà nhà tím ở góc avatar + tên công ty màu tím; dải Gần đây
trên nền xanh rất nhạt.

## 5. Quy tắc nghiệp vụ

### 5.1 Liên hệ
- Trường: **Tên*** (≤ 100 ký tự), **SĐT*** (1 số; chuẩn hoá khi lưu để so trùng: bỏ khoảng trắng / dấu chấm / gạch / ngoặc, và quy đầu `+84` / `84` về `0` — số lấy từ danh bạ máy thường dạng `+84 912…`, còn `customers.mobile` lưu dạng `0912…`; hiển thị vẫn giữ dạng người dùng nhập),
  **Địa chỉ** (tuỳ chọn), **Ghi chú** (tuỳ chọn, nhiều dòng). Validate báo đồng thời mọi ô.
- **Duy nhất theo (user, SĐT đã chuẩn hoá)**: tạo mới / chọn từ KH công ty / chọn từ máy mà trùng SĐT liên hệ đã có →
  dùng lại liên hệ cũ (không tạo bản 2, không ghi đè tên cũ).
- Liên hệ chỉ được TẠO khi **lưu nhắc việc** (đường từ form) hoặc bấm Lưu ở form thêm thủ công (DB-06 👤+). Huỷ form
  nhắc việc → không để lại liên hệ.
- Chọn từ KH công ty → lưu **bản sao** tên, SĐT (đúng số khớp), địa chỉ KH, + tên công ty để hiển thị. Không đồng bộ
  về sau (KH đổi tên / số thì danh bạ không đổi).
- Sửa liên hệ: đổi được mọi trường; đổi SĐT trùng liên hệ khác → báo lỗi.
- Xoá: §3.8.

### 5.2 Gắn vào nhắc việc
- Mỗi nhắc việc cá nhân gắn **tối đa 1** liên hệ (tuỳ chọn). Có ở form Tạo + Sửa, web + app. Chỉ nhắc việc GỐC gắn được — "Các bước" (bản ghi con `parent_id`) không có liên hệ; mọi phép đếm (DB-07, DB-09, dòng "Hẹn …") chỉ tính nhắc việc gốc.
- **Liên hệ không bao giờ lộ ra ngoài chủ nhân**: nhắc việc bật "Báo lịch làm việc lãnh đạo" vẫn gắn liên hệ được, nhưng API / màn Lịch làm việc lãnh đạo và thông báo toàn công ty KHÔNG trả / không hiện liên hệ.
- Bỏ gắn (✕) chỉ bỏ liên kết, không xoá liên hệ.
- "Gần đây" = liên hệ xếp theo lần gắn vào nhắc việc gần nhất.
- Thẻ / chi tiết nhắc việc có liên hệ: hiện tên + nút gọi (chạm tên → DB-07).
- Danh bạ DB-06 dòng "Hẹn …": nhắc việc chưa xong, có hạn, gần nhất của liên hệ đó (quá hạn vẫn hiện, màu đỏ — Claude chốt).

### 5.3 Tìm KH công ty theo SĐT
- Chỉ tra khi chuỗi gõ là số và **đủ độ dài số điện thoại** (≥ 9 chữ số sau chuẩn hoá) — Claude chốt; gõ ít hơn chỉ lọc
  trong danh bạ cá nhân.
- Số gõ được chuẩn hoá như §5.1 (+84 → 0) trước khi so.
- Phạm vi bản ghi: **giống hệt popup chọn KH của form Meeting khi tra đúng SĐT** (cùng điều kiện KH còn hiệu lực / loại KH / công ty như popup đó — không tự đặt luật mới). Builder đọc query popup đó và dùng lại.
- Khớp **đúng toàn bộ số** (không LIKE giữa chuỗi) với `customers.mobile` và `customer_contacts.phones` — cả 2 cột có thể
  chứa nhiều số ngăn bằng dấu phẩy → chuẩn hoá giống `CustomerService` (`CONCAT(',', REPLACE(col,' ',''), ',') LIKE '%,{số},%'`).
- **Không lọc theo quyền xem KH** — theo tiền lệ `phone_exact_bypass` của popup chọn KH (Dự án / Họp): biết chính xác số
  thì được tra (Claude chốt dựa trên tiền lệ — xem §8).
- Kết quả trả: tên người (người liên hệ, hoặc tên KH nếu khớp SĐT của KH) + tên KH / công ty; tối đa 5 dòng.

## 6. Web (hrm-client) — đầy đủ như app
- **Form nhắc việc** (`pages/assign/my-todo/components/TodoFormModal.vue`): dòng link "Gắn liên hệ" dưới Tiêu đề → popup
  / dropdown tìm (cùng nội dung DB-02/03; không có "Chọn từ danh bạ điện thoại"). Gắn xong: thẻ liên hệ + ✕.
- **Màn Danh bạ**: trang riêng trong my-todo (lối vào: sidebar my-todo, cạnh khối "LOẠI NHẮC VIỆC") — danh sách bên
  trái + chi tiết liên hệ (thông tin + "Nhắc việc với …") bên phải, hoặc theo khuôn list-page có sẵn (builder chọn, giữ
  style V2). Thêm / Sửa / Xoá liên hệ như app.
- Nút gọi trên web: hiển thị SĐT + nút sao chép (link `tel:` vẫn để cho máy có hỗ trợ) — Claude chốt.

## 7. App (TPE_APP)
- Form `ui/my_todo/personal_todo_form_page.dart` + sheet chọn / tạo liên hệ; màn Danh bạ + Chi tiết liên hệ mới; mục
  menu trái "Danh bạ cá nhân" trong `module_shell/module_menus.dart` (cạnh "Lịch làm việc lãnh đạo").
- Danh bạ điện thoại: dùng bộ chọn liên hệ của hệ điều hành (chỉ trả về người được chọn, không cần quyền đọc toàn bộ);
  "Lưu vào danh bạ điện thoại" mở màn thêm liên hệ của hệ điều hành, điền sẵn. App hiện chưa có thư viện liên hệ (chỉ có
  `permission_handler`) → builder chọn thư viện.
- Gọi / Nhắn tin: mở trình gọi / nhắn tin của máy.

## 8. Claude tự chốt (user chưa trả lời riêng)
- Danh bạ theo **user** (dùng chung mọi công ty người đó làm), không theo công ty.
- Tra KH công ty không xét quyền xem KH (tiền lệ `phone_exact_bypass`), chỉ khớp đúng toàn bộ số, ≥ 9 chữ số.
- Trùng SĐT → dùng lại liên hệ cũ, không ghi đè.
- Web "gọi" = hiện số + sao chép.
- Trên web không có "Lưu vào danh bạ điện thoại".

- Chuẩn hoá SĐT quy `+84`/`84` → `0` (cả lúc lưu liên hệ lẫn lúc tra KH công ty).
- Phạm vi tra KH công ty = đúng phạm vi popup chọn KH của form Meeting khi tra đúng SĐT.
- Chỉ nhắc việc gốc gắn liên hệ; "Các bước" không.
- Liên hệ không hiện ở Lịch làm việc lãnh đạo / thông báo toàn công ty.
- Ai dùng được: mọi user dùng được my-todo (không thêm quyền mới). Khi deploy, mục menu "Danh bạ cá nhân" phải thêm key vào "Cài đặt phân hệ" theo quy ước (mục menu mới không tự ẩn).

## 9. Để builder quyết
- Nhánh làm + thứ tự phát hành: xem plan.md Global Constraints (local + prod TPE chạy `gop_db`; server dev chạy `develop`) — hỏi user khi xin phép code.
- Tên bảng / cột cụ thể (đề xuất: bảng liên hệ riêng theo user + cột liên hệ trên `personal_todos`, xoá liên hệ → cột về
  NULL), có xoá mềm hay không, index.
- API cụ thể (danh sách / tìm / CRUD liên hệ, tìm KH theo SĐT, liệt kê nhắc việc theo liên hệ).
- Thư viện liên hệ Flutter; khuôn trang web Danh bạ (giữ style V2 + skill list-page nếu hợp).
- Phân trang / tải danh bạ dài (thanh chữ cái nhảy nhanh).
