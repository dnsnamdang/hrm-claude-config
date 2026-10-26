# Plan — App Meeting trên di động (TPE_APP / Flutter)

Phụ trách: @dnsnamdang · File thiết kế: `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen`

> Đây là công việc **THIẾT KẾ**, chưa đụng code `hrm-api` / `hrm-client`.
> Mọi phát hiện cần BE/FE làm đều gom ở mục "Việc chuyển cho dev" bên dưới.

---

## Phase 1 — Bộ màn nền (trước 15/09) ✅

- [x] 42 artboard: 5 bước nghiệp vụ + bộ màn chỉ xem + nhóm ngoại lệ
- [x] 14 component dùng chung `C/*`, accent `#E8972C`
- [x] Trang `00 · Tổng quan luồng` + bản đồ luồng toàn cảnh
- [x] Đề xuất API lưu từng phần → `api-luu-tung-phan.md`

## Phase 2 — Chọn khách hàng & người liên hệ (15/09) ✅

- [x] Màn **41 · Chọn khách hàng** (ô tìm + lọc MST/SĐT, kết quả dạng thẻ)
- [x] Màn **41b · Không tìm thấy khách hàng**
- [x] Màn **42 · Thêm nhanh khách hàng** (rút gọn, chỉ trường bắt buộc)
- [x] Sheet **43 · Chọn người liên hệ** · Sheet **44 · Thêm nhanh người liên hệ**
- [x] Bỏ field Trạng thái meeting khỏi W05 / W25 / W28 / W33
- [x] Khối tóm tắt KH đã chọn (Mã KH · MST · SĐT · Địa chỉ) + nút ✕ bỏ chọn
- [x] Bổ sung ô Người liên hệ còn thiếu ở màn 03

## Phase 3 — Bổ sung theo phản hồi (15/09) ✅

- [x] Bỏ logic "KH đã có người đăng ký" (không suy diễn từ web)
- [x] Xếp lại bản đồ: tối đa 4 màn/hàng, khung 5685 → 2825px ngang
- [x] Đổi nhãn thành phần **Nội bộ → Công ty** toàn hệ thống (giữ "Họp nội bộ" ở Phân loại họp)
- [x] Màn **45 · Cảnh báo chưa lưu khi Quay lại** (3 nút)
- [x] Hub: dấu `*` bắt buộc + thanh Mức độ hoàn thiện hồ sơ (9 Hub) + màn **46 · Hub chặn Hoàn thành**
- [x] Màn **47 · Thêm nhanh dự án TKT** + nút ở màn 06
- [x] Mã công ty trên dòng nhân sự (màn 07 · 14 · 17 · 35)
- [x] Màn 18: bỏ nút Thêm thừa ở khối người liên hệ, gắn badge "Người liên hệ" vào NGƯỜI 1
- [x] Gỡ 19 dòng chú thích logic khỏi trong khung điện thoại

## Phase 4 — Chuẩn hoá & chỉnh theo nghiệm thu (15–16/09) ✅

- [x] Nút **Xem** trên 10 dòng file ở 4 màn tài liệu (11 · 19 · 36 · 38)
- [x] Sửa chữ tràn nút màn 23 (`Xác nhận gửi lịch` → `Xác nhận`); quét 93 nút còn lại, không nút nào tràn
- [x] Đồng nhất thông báo: bỏ toast đè, gom còn 3 loại dải (đỏ / xám / xanh)
- [x] Màn **21** dựng lại theo timeline: ngày–giờ là mốc trên trục, thêm người chủ trì
- [x] Màn **06**: khối giải pháp đổi sang cây cha – con
- [x] Màn **01**: tab `Tôi chủ trì` / `Tôi tham gia` + 3 chip lọc nhanh; màn **02** bỏ ô Công ty / Phòng ban
- [x] Dấu `*` trên Hub đổi sang **theo trạng thái từng màn** (tắt 28, giữ 22)
- [x] DEV NOTE trên artboard 01 · 04a · 06 · 21

## Phase 5 — Bàn giao v11 (16/09) ✅

- [x] Xuất **PDF bản đồ theo bước** — 8 trang, 4 màn/hàng đúng bố cục canvas (bản khách hàng + bản nội bộ)
- [x] Xuất **PDF chi tiết 50 trang** (bản khách hàng + bản nội bộ có ghi chú dev)
- [x] Xuất **50 ảnh PNG 3x**
- [x] File tóm tắt thay đổi gửi khách: `exports/Meeting-Mobile_v11_Tom-tat-thay-doi_2026-09-16.md`

---

## Việc chuyển cho dev (chưa làm, cần chốt/triển khai)

**BE bắt buộc sửa**
- [ ] `customerMeetingHistory()` lọc sai đối tượng: đang so `me.employee_id` với `m.created_by` (người TẠO) thay vì user đang đăng nhập → mọi user thấy danh sách giống nhau. Port khuôn `PotentialCustomerCareService::applyPermissionFilter()`
- [ ] Endpoint `customer-history` trả thêm `host_name` + `end_date` (màn 21 hiện người chủ trì và khung giờ)
- [ ] API danh sách nhân viên trả thêm `company_code` (`c.code as company_code` như các báo cáo đang làm)
- [ ] `projects.*.scope_id` / `implementation_type` / `project_address` đang nullable trong khi FE bắt buộc → lưu thiếu không báo lỗi (cùng loại lỗi Redmine #10874)
- [ ] App dùng `MeetingCalendarCriteria` cho danh sách meeting, KHÔNG dùng `MeetingCriteria`
- [ ] Nhóm API lưu từng phần cho điều hướng Hub → xem `api-luu-tung-phan.md`
- [ ] Danh mục Lý do huỷ + `meetings.cancel_reason_id` → xem `api-luu-tung-phan.md` mục 7

**Cần chốt với khách trước khi code** — ✅ ĐÃ CHỐT 14/10, xem bảng trong `design.md`
- [x] (14/10: bỏ chọn GP/HM, meeting chỉ chọn tới dự án) Màn 06: web chỉ cho 1 Giải pháp + 1 Hạng mục mỗi dự án (SearchPicker đơn), app vẽ chọn nhiều → đổi web hay đổi app?
- [x] (14/10: hết vướng sau khi bỏ GP/HM) Màn 06: meeting gắn NHIỀU dự án thì chọn dự án trước rồi mới tới cây giải pháp — chưa thiết kế
- [x] (14/10: chép sang, cho sửa) Màn 42: bản rút gọn mặc định copy địa chỉ chính sang địa chỉ xuất hoá đơn
- [x] (14/10: Có) Màn 44: liên hệ tạo từ app có tự thêm vào Thành phần khách hàng không
- [x] (14/10: theo web) Màn 18: dòng NGƯỜI 1 (người liên hệ) có cho xoá tại màn này không
- [x] (14/10: Có đưa vào → Phase 6) Khối "Phiếu tổng hợp kết quả meeting" (#11130) chưa vẽ ở Hub lẫn màn nhập

**Chưa vẽ**
- [ ] Trạng thái rỗng màn 21 ("Bạn chưa tham gia cuộc họp nào với khách hàng này")
- [ ] Biến thể màn 01 lúc đang bật 1 chip lọc
- [ ] Tab `Nhân sự Khách hàng` ở màn 14 (web `PopupStaff` có 2 tab, app mới có 1)
- [ ] Người thực hiện biên bản chọn NHIỀU (Redmine #11044) — màn 10 đang vẽ ô đơn

## Phase 6 — Sửa theo chốt khách 14/10 (thiết kế, file .pen)

- [ ] Màn 06 + 34: bỏ khối cây Giải pháp / Hạng mục, chỉ còn danh sách dự án TKT; gỡ DEV NOTE màn 06 phần GP/HM
- [ ] Màn 42: ô Địa chỉ xuất hoá đơn điền sẵn từ địa chỉ chính, vẫn sửa được (không khoá)
- [ ] Màn 11 · 19 · 36 · 38: nút Xem chỉ hiện ở dòng PDF / ảnh
- [ ] Vẽ khối "Phiếu tổng hợp kết quả meeting" (#11130): dòng Hub + màn nhập + màn xem + chặn Hoàn thành khi thiếu câu bắt buộc
- [x] Meeting theo đối tượng (14/10) — ô theo loại meeting đặt dưới Loại meeting:
  - [x] 03: ô `Dự án TKT *` trống (loại Đấu thầu = đối tượng TKT)
  - [x] 05: ô `Hợp đồng *` đã chọn (mã · KH · badge trạng thái · ✕), loại đổi thành "Thương thảo HĐ"
  - [x] 25: ô Dự án TKT viền đỏ + "Vui lòng chọn Dự án TKT.", banner 4 lỗi
  - [x] 33: dòng Hợp đồng chỉ xem (mã link mở HĐ + KH + badge)
  - [x] Màn mới **48 · Chọn dự án TKT** (chọn nhiều, chip đã chọn, dải lọc theo KH, badge tiến trình, cuộn tải thêm, Thêm nhanh dự án + Xác nhận)
  - [x] Màn mới **49 · Chọn hợp đồng** (chọn 1, bấm thẻ là xong, không hiện tiền) — chèn hàng mới, dịch phần dưới bản đồ +1150px
  - [x] Caption 03 · 05 · 25 · 33, tiêu đề bản đồ 52 artboard, chip 48/49 ở trang Tổng quan
  - [ ] Màn 06 / dòng Hub "Dự án tiền khả thi": ⏸ HOÃN (user chốt 19/10) — tối ưu web xong mới sửa 1 loạt thiết kế app
- [ ] Đồng bộ theo web (14/10, `.plans/gop-db/meeting-tab-du-an-nhan-su`): Hub/màn Dự án TKT chỉ hiện khi meeting đã có dự án, chỉ XEM thông tin dự án (phiếu vẫn nhập); gộp màn Thành phần + Điểm danh thành "Nhân sự tham gia" (nhóm Phía Công ty / Phía Khách hàng, cột điểm danh chỉ từ Chốt lịch)
- [x] Mũi tên luồng tới 48 / 49 (19/10): `→ Bấm ô Dự án TKT` ở khe trái màn 48; `↓ Bấm ô Hợp đồng` trên màn 49 — dời phần bản đồ từ 49 trở xuống +150px (khung 2825 × 25917)
- [ ] Cập nhật caption / bản đồ / số artboard sau khi thêm màn
- [ ] Xuất bản v12

**BE (bổ sung từ chốt 14/10)**
- [ ] `customerMeetingHistory()`: THAY `created_by` bằng điều kiện user có trong thành phần (không giữ cả hai)
- [ ] Endpoint xem file inline cho PDF / ảnh

---

### Checkpoint — 2026-10-14 (wrap up)
Vừa hoàn thành: chốt 9 câu với khách; khảo sát "Meeting theo đối tượng" trên gop_db; đề xuất API chọn dự án dùng chung web + app (đã duyệt); vẽ ô đối tượng ở 03 / 05 / 25 / 33 + 2 màn mới 48, 49 (52 artboard, đã kiểm không chồng lấn / không tràn).
Đang làm dở: Phase 6 — còn màn 06 + 34 (bỏ GP/HM), màn 42 (địa chỉ HĐ điền sẵn cho sửa), nút Xem chỉ PDF/ảnh (11 · 19 · 36 · 38), Phiếu tổng hợp kết quả #11130, mũi tên luồng 48/49, xuất v12.
Bước tiếp theo: user chốt màn 06 bỏ hay giữ dạng xem → sửa 06 / 34 / dòng Hub; rồi làm tiếp các mục Phase 6.
Blocked: chờ user chốt màn 06.

### Checkpoint — 2026-09-16 08:50
Vừa hoàn thành: xuất bản giao hàng v11 (4 PDF + 50 PNG 3x + file tóm tắt), 50 artboard, khung 2825 × 24617.
Đang làm dở: không có — bộ thiết kế ở trạng thái bàn giao được.
Bước tiếp theo: gửi khách bản `BAN-DO-THEO-BUOC_v11_…_BAN-KHACH-HANG.pdf` + file tóm tắt; chờ phản hồi để chốt 6 câu hỏi ở mục "Cần chốt với khách".
Blocked: "logic tạo task giao cho người xử lý ở biên bản" — user báo đã có nhưng KHÔNG tìm thấy trên `tpe`, `tpe-develop-assign`, `gop_db` (Task entity không có FK sang meeting). Chờ user cho số Redmine / tên nhánh.

### Checkpoint — 2026-10-14 (wrap up tối)
Vừa hoàn thành: phía web (gop_db, local chưa commit) — endpoint `options-for-meeting` + ô chọn dự án tìm phía server; tab Dự án TKT chỉ xem; tab Nhân sự tham gia.
Đang làm dở: Phase 6 thiết kế app (như checkpoint trước).
Bước tiếp theo: chốt màn 06 — theo web nay = chỉ xem, hiện khi có dự án (đề xuất giữ dạng chỉ xem); vẽ lại Thành phần + Điểm danh thành 1 màn "Nhân sự tham gia".
Blocked:

### Checkpoint — 2026-10-19
Vừa hoàn thành: vẽ mũi tên luồng tới 48 / 49 (đã kiểm không chồng lấn).
User chốt 19/10: **phần thiết kế app phụ thuộc web (màn 06 · 34 · dòng Hub Dự án TKT, gộp Thành phần + Điểm danh thành "Nhân sự tham gia") HOÃN — tối ưu web xong mới sửa 1 loạt.**
User chốt tiếp 19/10: "làm web cho xong đã" → **TẠM DỪNG TOÀN BỘ Phase 6** (kể cả màn 42, nút Xem PDF/ảnh, Phiếu #11130); web xong mới sửa app 1 loạt.
Blocked: chờ web `gop_db` xong (meeting-tab-du-an-nhan-su, meeting-chon-du-an-tkt).

## Phase 7 — Đồng bộ thiết kế app theo web gop_db (19/10/2026)
Sao lưu trước khi sửa: `meeting-mobile.backup-20261019-truoc-dong-bo-web.pen`
- [x] 03 Tạo meeting: 5 khối theo thứ tự chọn + màu khối, KH trước → Dự án TKT lọc theo KH, Gợi ý tên, liên hệ 1 ô
- [x] 05 · 25 · 28 · 33: cùng khuôn 5 khối (sửa / lỗi validate / họp Online / chỉ xem)
- [x] 48 Chọn dự án TKT: bỏ Thêm nhanh dự án, dải lọc KH cố định; xoá màn 47 + mũi tên/caption trỏ tới 47
- [x] Hub 04a · 04b · 04c · 24 · 26 · 27 · 46: "Dự án TKT" chỉ khi có dự án; gộp "Nhân sự tham gia"
- [x] 06 · 34 Dự án TKT: thẻ tóm tắt chỉ xem + nút gạt "Thông tin chung / Phiếu thu thập thông tin", không "Xem chi tiết"
- [x] Nhân sự tham gia: gộp 07 + 08 (31 nội bộ, 32/35 chỉ xem, 30 chặn Hoàn thành)
- [x] 12 · 39 Khảo sát: câu Có/Không = nút gạt
- [x] Caption · bản đồ · trang Tổng quan · số artboard; kiểm chồng lấn / tràn

### Checkpoint — 2026-10-19 (Phase 7 đồng bộ web — XONG trong file .pen, CHƯA xuất bản)
Vừa hoàn thành (meeting-mobile.pen, 51 artboard, khung 2825 × 27307, 0 chồng lấn):
- 03 · 05 · 25 · 28 · 33: 4 khối màu theo thứ tự chọn (① Loại indigo · ② KH & đối tượng sky · ③ Nội dung amber · ④ Thời gian, địa điểm & chủ trì
  emerald), vòng số đặc = khối đủ; Phân loại / Hình thức = nút gạt; KH bắt buộc + chọn trước, Dự án TKT khoá "Chọn khách hàng trước";
  Gợi ý tên; 33 thêm khối "Thông tin bản ghi" (slate). 25 sửa lỗi cũ: Tên có chữ mà báo trống.
- 48: bỏ "Thêm nhanh dự án"; xoá màn 47 + mũi tên + chip Tổng quan (chốt W1).
- 06 → "Dự án TKT — Thông tin chung" chỉ xem (chip dự án · nút gạt · thẻ tóm tắt dự án + KH), bỏ DEV NOTE GP/HM; MỚI 06b "Phiếu thu thập
  thông tin" (nhập + Lưu phiếu), đặt vào chỗ màn 47; 34 cùng khuôn chỉ xem.
- Hub 04a/04b/04c/24/26/27/46: "Dự án TKT" (DA.26.018 · DA.26.031 · phiếu 3/4 câu); gộp Thành phần + Điểm danh → "Nhân sự tham gia";
  thanh hoàn thiện x/5 → x/4 (cả popup 16/22/23).
- 07 · 08 · 31 · 32 → "Nhân sự tham gia" 2 nhóm Phía Công ty / Phía KH (Mã phòng · Mã NV, badge Chủ trì / Người liên hệ, chip Thêm nhanh,
  điểm danh = nút gạt 3 màu từ Chốt lịch); xoá 35 (gộp vào 32); 30 chặn Hoàn thành chuyển khuôn mới.
- 12: câu Có/Không = nút gạt. Caption, DEV NOTE 04a, tiêu đề bước, mũi tên, trang Tổng quan, số artboard cập nhật theo.
⚠️ File .pen trên đĩa vẫn là bản 16/10 22:32 tới khi user bấm Cmd+S trong app Pen (Claude không gửi được phím tắt). Sao lưu trước sửa:
  meeting-mobile.backup-20261019-truoc-dong-bo-web.pen.
Bước tiếp theo: user duyệt trên Pen → xuất bản v12 (PDF bản đồ + PDF chi tiết + PNG) + file tóm tắt thay đổi gửi khách.
Còn tồn (chưa làm): màn 42 địa chỉ HĐ điền sẵn · nút Xem chỉ PDF/ảnh (11·19·36·38) · Phiếu tổng hợp kết quả #11130.
Blocked:

### Checkpoint — 2026-10-19 (W4 gộp Kết luận vào Biên bản)
Vừa hoàn thành: hub 04a/04b/04c/16/22/23/24/26/27/46 bỏ dòng Kết luận, dòng Biên bản ghi kèm kết luận, tiến độ x/3; màn 09 thêm khối Kết luận; màn 13 → "Biên bản — soạn kết luận" (nút Xong); màn 40 gộp vào 37 rồi xoá; caption/ghi chú dev/mũi tên/chip tổng quan cập nhật; bản đồ 50 artboard, 0 chồng lấn
Đang làm dở: —
Bước tiếp theo: user bấm Cmd+S trong Pen, duyệt thiết kế → xuất v12 khi được yêu cầu
Blocked:

### Checkpoint — 2026-10-19 (W5 Thông tin chung gập/mở)
Vừa hoàn thành: 03 (① gập ✓, ② mở dạng dòng, ③④ gập "Chưa nhập"), 05 (4 khối gập + tóm tắt), 25 (②③ mở kèm lỗi, ④ gập "1 lỗi"), 28 (④ mở, Online); caption 4 màn; bản đồ 0 chồng lấn
Đang làm dở: —
Bước tiếp theo: user Cmd+S trong Pen, duyệt → xuất v12 khi được yêu cầu
Blocked:

### Checkpoint — 2026-10-19 (wrap up: W6 gộp khối + khảo sát TPE_APP)
Vừa hoàn thành: W6 gộp khối 03/05/25/28/33 theo web Phase 4 (① Thông tin cuộc họp · ② Đối tác · ③ Thời gian) + sửa vòng số ③ ở 03; khảo sát mã nguồn TPE_APP → khao-sat-tpe-app.md; cài Mobile MCP (@mobilenext/mobile-mcp@1.0.8, scope local ERP-HRM); chạy TPE_APP flavor erp trên máy ảo iPhone 18 Pro (2.2.4), chụp được màn Chọn phân hệ
Đang làm dở: khảo sát app thật bằng Mobile MCP — chờ user restart Claude Code để nạp tool
Bước tiếp theo: (phiên mới) chạy lại API :8000 + Nuxt :3000 + `fvm flutter run --flavor erp -d D0C0E274-8590-4D39-9196-CD5D535338DD` (từ TPE_APP/app); đi phân hệ Chấm công & Giao việc trước (Tổng quan, drawer, thanh phím tắt, Task/Phiếu giao việc) — CHỈ xem, không lưu phiếu (server dev); rồi đề xuất sắp xếp lại màn
Blocked: user phải Cmd+S trong Pen để lưu thiết kế hôm nay

### Checkpoint — 2026-10-19 (wrap up: khung phân hệ + dashboard)
Vừa hoàn thành: 00b chọn phân hệ (5 màu nhận diện + hiệu ứng nền) · drawer 00c/00c'/00d/00e/00f/00g · template C/BottomNav (theme phanhe) · Tổng quan Meeting 00h + 00h' · style phân hệ áp vào ~50 màn meeting (cam → xanh ngọc, header gradient, badge chờ → hổ phách, màn 01 BottomNav) · Tổng quan Chấm công 00i (khảo sát logic ca/chấm công → khối Ca làm trong ngày)
Đang làm dở: —
Bước tiếp theo: user Cmd+S trong Pen + duyệt; chờ chốt: tab BottomNav từng phân hệ, ý nghĩa badge, thanh tiến độ/badge "Đã chốt lịch" đổi tím?, tên "Đào tạo" vs "Đào tạo - đánh giá", vẽ thêm trạng thái chưa chấm vào / đã chấm ra / không có ca (00i); dashboard Công việc / Cơm / Đào tạo chưa vẽ; xuất v12 khi được yêu cầu
Blocked: BE thiếu allow_app/allow_conn theo từng mục listTimesheetTypes, job_id ở timekeeper/employee (cho 00i)

### Checkpoint — 2026-10-20 (wrap up)
Vừa hoàn thành: xuất PNG @3x v12 (60 màn) · 00b đổi nền theo màn đăng nhập app · 00j Thông báo (chuông) dùng chung
Đang làm dở: —
Bước tiếp theo: user Cmd+S trong Pen (file đĩa còn bản 19/10 15:56) + duyệt; chốt các câu tồn (tab BottomNav, ý nghĩa badge, màu "Đã chốt lịch", tên Đào tạo, prefix thông báo DXN/COM/KH/TBNB, trạng thái 00i chưa chấm vào / đã ra / không ca, vuốt trái + trạng thái trống 00j); cập nhật trang 00 Tổng quan luồng rồi xuất lại v12; dashboard Công việc / Cơm / Đào tạo
Blocked: BE thiếu allow_app/allow_conn theo từng mục listTimesheetTypes, job_id ở timekeeper/employee (00i)

### Checkpoint — 2026-10-22 (wrap up)
Vừa hoàn thành: 00i' (frame t41x9, đặt cạnh 00i) — khối "Ca làm trong ngày" v2: 3 thẻ rời gom thành 1 khối = dải thời gian 08–18h (thanh màu theo loại, vạch cam giờ hiện tại, vùng đã qua mờ, thanh nhạt = đã xong) + mỗi ca/phiếu 1 dòng (tên · giờ ca · địa điểm/đếm ngược; bên phải chỉ 1 thứ: Vào→Ra + "Tại máy" / "Xong" / nút Chấm). Ghi W10 trong design.md (đã xoá dòng W9 bị lặp)
Đang làm dở: —
Bước tiếp theo: user Cmd+S trong Pen + chọn 00i hay 00i' (chọn 00i' → thay vào màn chính, xoá bản cũ); vẽ màn chi tiết khi bấm 1 dòng (chứa mã phiếu, KH, tên máy, hình thức, PGV con); các câu chốt tồn ở checkpoint 20/10 vẫn còn nguyên
Blocked: BE thiếu allow_app/allow_conn theo từng mục listTimesheetTypes, job_id ở timekeeper/employee (00i)

### Checkpoint — 2026-10-26 (Bộ lọc dùng chung — đề xuất)
Vừa hoàn thành: khảo sát bộ lọc app thật + bản thiết kế (`khao-sat-bo-loc.md`); pull TPE_APP develop 331f51b chạy máy ảo (flavor tpeDev), xem 3 màn lọc thật (Phiếu giao việc · Danh sách khoá học · Task); vẽ 4 trạng thái bộ lọc mới BL1–BL4 trên màn Phiếu giao việc (design.md W11)
Đang làm dở: chờ user duyệt hướng BL1–BL4 (đã chỉnh 1 vòng: Đặt lại / Bỏ chọn xuống footer cùng hàng nút chính)
Bước tiếp theo: chỉnh theo góp ý → áp mẫu cho 1 màn phân hệ khác (Đào tạo / Meeting 01–02) để kiểm tính dùng chung → viết spec component (FilterBar · FilterSheet · 4 loại trường · chip tiêu chí) cho dev Flutter
Blocked: nút "Xem N kết quả" cần API đếm trước — chưa kiểm; không có thì dùng "Áp dụng (n)"
⚠️ Pen không tự lưu — user bấm Cmd+S
Ghi chú TPE_APP (local, KHÔNG commit/push): app/ios/Podfile comment lại dòng EXCLUDED_ARCHS arm64 + project.pbxproj bỏ EXCLUDED_ARCHS — chỉ để build máy ảo chip Apple; flavor mới tpeDev
