# Chat + Agent trên app mobile — design (17/11/2026) · @namdangit

> Phân tích đầy đủ (bảng App / Web từng tính năng, nguồn code): `phan-tich-app-web.md` cùng thư mục.
> Đầu ra đợt này: **mockup trong `meeting-mobile.pen`** (khu mới, xoá KG-01…24 cũ). Chưa code app.

## Mục đích
Đưa Chat (nhóm trao đổi + 1–1) và TPE SMART AGENT lên app TPE_APP, bám logic mới nhất `origin/gop_db`. Trục chính là các
NHÓM CHAT; Nhiệm vụ / Meeting / Vấn đề là tab tuỳ chỉnh của nhóm. Chat là phần độc lập, mở nhanh từ mọi màn. Giao diện
dễ nhìn, thoáng.

## Không làm (đợt này)
Thống kê / hạn mức / model / nhật ký Agent · sửa nhóm, bật-tắt tab, gắn Dự án KH, đóng / mở lại nhóm · thêm thành viên theo
phòng ban / cả công ty, thao tác hàng loạt · YC hỗ trợ · gọi thoại/video · `@Agent` trong nhóm · dòng chi phí token.

## Quyết định đã chốt (user 17/11/2026)
1. **Lối vào**: icon 💬 + badge chưa đọc cạnh chuông trên `PrimaryAppBar` (mọi màn) → Chat toàn màn, ‹ về đúng màn cũ.
2. **Agent**: dòng ghim đầu danh sách Chat như web, không icon riêng.
3. **Thông tin nhóm**: Thành viên + Ảnh · Tệp · Link + Rời nhóm ở màn Thông tin nhóm (bấm tên nhóm / ⓘ). Dải tab chỉ có
   Trò chuyện · Nhiệm vụ · Meeting · Vấn đề (tab nào nhóm bật mới hiện; chỉ có Trò chuyện thì không có dải tab).
4. **Tạo nhóm trên app — rút gọn**: Tên * · Mô tả · chọn người lẻ (Danh bạ mọi công ty) · công tắc dùng tab Nhiệm vụ.
   Người tạo = Quản lý, người được chọn = Thành viên. Dùng lại `POST workspaces` (name, description, member_ids,
   enabled_tabs). Thời hạn, chọn theo phòng ban / cả công ty, 3 vai trò, Dự án KH → web.
5. **Quản lý thành viên trên app**: Quản lý thêm người lẻ, đổi vai trò, mời ra TỪNG người (nhấn giữ dòng thành viên);
   hàng loạt + theo phòng ban chỉ web. Chặn như BE: Quản lý cuối, người còn việc dở (422 → báo + link sang tab Nhiệm vụ lọc).
6. **Tab Vấn đề**: vẽ luôn theo Vấn đề v2 (IssuePanel), ghi chú "phụ thuộc web Phase 3 — chưa dùng được tới khi web xong".

## Quyết định Claude tự chốt (thuần UI — user sửa được)
- Thao tác trên tin = nhấn giữ → bottom sheet (hàng biểu cảm trên cùng); thao tác dòng hội thoại = nhấn giữ → sheet.
- Thẻ nhiệm vụ / tin hệ thống / thẻ Agent mở **màn có sẵn của app**; đích app chưa có (KH, Dự án TKT, Giải pháp, đơn) ⇒ "Xem trên web".
- Chỉnh ảnh trên app chỉ cắt + xoay. Thêm "Chụp ảnh" (camera) trong sheet [+].
- Agent: khối kết quả dạng thẻ dọc; `timesheet` 3 ô/hàng; panel quyền → sheet Hạn mức hôm nay + Quyền liên quan.
- Thoáng: dòng hội thoại 72px (avatar 48, tên 16, tin cuối 14 xám), header 1 hàng, bong bóng chữ 16, ô soạn 1 hàng
  [+] · ô nhập · 😊 · gửi; nút có icon, Huỷ/Đóng cuối (quy ước app).
- Accent theo app; trạng thái nhiệm vụ lấy màu BE.

## Khung màn tiết kiệm chỗ — tham khảo Zalo (user chốt 17/11: "theo đề xuất")
Ngân sách iPhone 393×852: trừ status bar 59 + home indicator 34 ⇒ 759px.
- Chat mở toàn màn PHỦ thanh dưới + FAB của phân hệ; không màn chat nào có thanh dưới. Header trắng 52px 1 hàng, viền mảnh.
- Danh sách: header = ‹ · ô tìm · ✎ (Tin nhắn mới / Tạo nhóm) 52px + chip 36px ẩn khi cuộn xuống ⇒ khung 88px.
- **Chat nhóm PA1**: KHÔNG dải tab. Header ‹ · avatar · tên (dòng phụ số thành viên) · 📋 n · ⓘ. 📋 ⇒ màn "Việc của nhóm"
  thanh chuyển Nhiệm vụ · Meeting · Vấn đề (chỉ tab nhóm bật; badge = việc dở). Tìm tin chuyển vào ⓘ. Khung 104px.
  (Thay quyết định 3 phần "dải tab": tab không còn nằm trên màn chat.)
- Tin ghim: dải 32px; × thu thành 📌 trên header (nhớ theo nhóm, trên máy). Bàn phím mở ⇒ dải ghim ẩn.
- Ô soạn 52px: + · ô nhập · 😊 · gửi; dải trả lời 40px chỉ khi đang trả lời; ô nhập cao tối đa 5 dòng.
- 1–1: ‹ · avatar · tên + mã công ty / trực tuyến · 📞 (tel:) · ⓘ.
- Agent: ‹ · 🤖 TPE SMART AGENT · 🕘 Lịch sử · ✎ Hội thoại mới; chip gợi ý chỉ ở màn chào; thẻ bước thu 1 dòng 28px khi xong.
- Bộ màn đổi: CH-12/13/14 thành 1 màn "Việc của nhóm" 3 trạng thái (Nhiệm vụ / Meeting / Vấn đề); CH-15 Thông tin nhóm có "Tìm tin nhắn".

## Bộ màn (19)
CH-01 màn bất kỳ có 💬 + badge · CH-02 Danh sách hội thoại (dòng Agent, Đã ghim, chip lọc) · CH-03 nhấn giữ dòng → sheet ·
CH-04 Tin nhắn mới / Danh bạ (+ lối Tạo nhóm) · CH-05 Tạo nhóm rút gọn · CH-06 Chat 1–1 (đã xem, mã công ty) ·
CH-07 Chat nhóm có dải tab, đủ trạng thái (ghim, trả lời, @, thẻ NV, tin hệ thống, mốc chưa đọc) · CH-08 nhấn giữ tin → sheet ·
CH-09 sheet [+] · CH-10 gợi ý @ / # · CH-11 Emoji / Sticker · CH-12 tab Nhiệm vụ · CH-13 tab Meeting · CH-14 tab Vấn đề ·
CH-15 Thông tin nhóm (thành viên, ảnh/tệp/link, rời nhóm; nhấn giữ thành viên → sheet Quản lý) · CH-16 Hồ sơ người ·
CH-17 Chỉ đọc (vai trò Xem / nhóm đóng) · AG-01 Agent màn chào + Lịch sử · AG-02 Agent trả lời (thẻ bước, khối kết quả,
thẻ chọn, thẻ thiếu quyền, sheet Hạn mức).

## Việc khi code app (ngoài mockup — ghi lại)
Socket client (`chat`, `presence`, `agent`) · xử lý push `chat_message` mở hội thoại · bản nháp + cài đặt thông báo đang ở
localStorage web ⇒ đồng bộ cần API · "Đề nghị cấp quyền" của Agent web chưa có luồng thật.

## Mockup đã vẽ (17/11/2026)
`~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` — khu "CHAT + AGENT (APP)" x 30600, y −1900…3550
(bản lưu trước khi vẽ: `meeting-mobile.backup-20261117-truoc-chat-agent-app.pen`). Đã XOÁ KG-01…25 + tiêu đề Nhóm ② ③ ④ ⑭
của khu Công việc (Mục lục khu Công việc + Nhóm ① còn nhắc tên các nhóm cũ — chưa sửa).
- Hàng ① CH-01 icon 💬 · CH-02 danh sách · CH-03 nhấn giữ dòng · CH-04 Tin nhắn mới · CH-05 Tạo nhóm rút gọn
- Hàng ② CH-06 1–1 · CH-07 nhóm đủ trạng thái · CH-08 nhấn giữ tin · CH-09 nút + · CH-10 @ · CH-10b # · CH-11 emoji
- Hàng ③ CH-12/13/14 Việc của nhóm (Nhiệm vụ / Meeting / Vấn đề) · CH-15 Thông tin nhóm · CH-15b sheet thành viên (Quản lý) · CH-16 hồ sơ · CH-17 chỉ đọc
- Hàng ④ AG-01 màn chào · AG-02 trả lời + khối kết quả · AG-03 thẻ chọn + thiếu quyền · AG-04 Lịch sử · AG-05 Hạn mức
Claude tự chốt khi vẽ: màu nhấn chat teal #0E9384 (chat độc lập, không theo màu phân hệ); lưới 4 cột cho sheet thao tác tin
(gọn hơn danh sách dọc); Agent bỏ ⓘ — dòng phụ "Còn n/20 câu hôm nay ›" mở Hạn mức; "Bản nháp:" màu nâu #B45309 (không đỏ).

## Góp ý 17/11 (tối) — đã sửa mockup
- **Tab sử dụng ở Tạo / Sửa nhóm**: CH-05 có 3 công tắc Nhiệm vụ · Meeting · Vấn đề (Vấn đề chờ web Vấn đề v2). Thêm **CH-05b Sửa nhóm**
  (Quản lý, nút "Sửa" trên header CH-15): Tên · Mô tả · Tab sử dụng ⇒ **đổi quyết định cũ "bật/tắt tab chỉ web"**: app sửa được tên/mô tả/tab;
  Thời hạn, Dự án KH, Đóng/Mở lại vẫn web. BE sẵn: StoreWorkspaceRequest/UpdateWorkspaceRequest nhận enabled_tabs ⊂ tasks,meetings,issues,files.
- **Web còn thiếu (việc riêng, chưa làm)**: `CreateWorkspaceModal.vue` chỉ có checkbox Nhiệm vụ (`enabled_tabs: tab_tasks ? ['tasks'] : []`),
  `SettingsPanel.vue` chỉ có công tắc Nhiệm vụ/Meeting ⇒ thêm Meeting (+ Vấn đề khi xong v2) vào form tạo nhóm web.
- **Gợi ý # (CH-10b)** (chốt sau 2 lượt góp ý 17/11): bỏ mã nhiệm vụ; hàng 1 = icon Người giao (user-round-pen, tím) + HỌ TÊN ĐỦ → icon Người làm (user-round-check, xanh) + HỌ TÊN ĐỦ; hàng 2 = tên nhiệm vụ rộng hết màn; hàng 3 = 📅 Hạn · nhãn trạng thái có icon. Chú giải icon cuối danh sách. Không dùng avatar chữ tắt (không biết ai là người giao).

## Góp ý 17/11 (lượt 3) — icon thống nhất + ưu tiên + bỏ nhấn giữ ở quản lý thành viên
**Bộ icon dùng chung** (lấy từ màn chi tiết đã thiết kế NV2-04, VD2-02, meeting Wrap 01 / Hub 04b):
| Đối tượng | Icon |
|---|---|
| Nhiệm vụ | Người giao `user-check` · Người làm `user-round` · Hạn `alarm-clock` (đỏ khi quá hạn) · Ưu tiên `flag` (Bình thường #64748B / Cao #F97316 / Khẩn cấp #DC2626) · trạng thái: Đang thực hiện `loader-circle` #2563EB · Chờ duyệt KQ `clock-3` #D97706 · Chờ bắt đầu `circle-dashed` · Hoàn thành `circle-check` #16A34A |
| Vấn đề | Người báo `user-plus` · Người phụ trách `user-round` · Hạn xử lý `alarm-clock` · Ưu tiên `flag` · Đang xử lý `loader-circle` · Mới ghi nhận `circle-dot` |
| Meeting | Thời gian `calendar` · Địa điểm `map-pin` / Online `video` · Chủ trì `user-round` · Đã chốt lịch `calendar-check` · Hoàn thành `circle-check` |
Đã áp: CH-10b (gợi ý #, thêm ưu tiên + chú giải), thẻ nhiệm vụ trong chat (CH-07 và 7 màn sao chép), CH-12, CH-13, CH-14, khối kết quả AG-02. Bỏ mã nhiệm vụ / vấn đề trên thẻ.
**Lệch có sẵn trong khu Công việc — ĐÃ SỬA 17/11 (user: làm luôn)**: 16 icon 'Giao:' → user-check, 5 icon 'Báo:' → user-plus, 22 cờ ưu tiên chuẩn màu (Khẩn cấp #DC2626, Cao #F97316) trong cả khu Công việc x 15600–21300 (kể cả khu Bản cũ). Ghi chú cũ: NV2-01 / VD2-01 (danh sách) dùng `user-round` + chữ "Giao:" / "Báo:" cho người giao / người báo, trong khi chi tiết NV2-04 dùng `user-check`, VD2-02 dùng `user-plus`; màu Khẩn cấp list #DC2626 vs chi tiết #EA580C.
**Quản lý thành viên**: bỏ nhấn giữ — mỗi dòng thành viên ở CH-15 có nút ⋮ hiện sẵn → sheet CH-15b.

## Phong cách thương hiệu (17/11 — "hiện đại + màu đặc thù của khách hàng")
Nguồn màu: logo `TPE_APP/app/assets/images/tanphat_logo_2026_vector.svg` (#225AA6) + `app_color.dart` (primary #193463, orange #E77D00).
- Màu nhấn chat: #0E9384 (teal, tự chốt trước) ⇒ **#225AA6**; nền nhạt #EAF1FB; nền chat #EDF2F9.
- Header + status bar: dải ngang #193463 → #225AA6, chữ/icon trắng, nút trên header nền trắng 15%; avatar trên header viền trắng 2px.
- Tin của mình: bong bóng dải #3473CF → #225AA6, chữ trắng, giờ trắng 78%.
- Số chưa đọc ở danh sách: cam thương hiệu #E77D00 (icon 💬 trên thanh phân hệ vẫn đỏ như chuông).
- Thông tin nhóm: khối đầu là "hero" nối liền header (dải màu, bo góc dưới 24px).
- Agent: dải #193463 → #225AA6 → #38BDF8; màn chào nền dải xanh nhạt → trắng, mascot 88px viền trắng + bóng xanh, thẻ gợi ý nổi nhẹ.

- **Dòng hội thoại (CH-02/CH-03)**: thêm nút ⋮ hiện sẵn cuối mỗi dòng (trừ dòng Agent); nhấn giữ vẫn mở cùng sheet. Tin nhắn (CH-08) giữ nhấn giữ — thêm ⋮ trên từng tin làm rối màn chat.
- **Nền header kiểu các phân hệ khác** (17/11, khuôn NV2-01 / Meeting Hero): StatusBar + Header gói chung khung `HeaderBg` (clip) — dải chéo 3 điểm #3473CF → #225AA6 → #193463 (rotation 200), 2 quầng sáng radial #6FA8FF, 2 vòng tròn trắng mảnh, icon chìm Material Symbols cỡ lớn #FFFFFF0F ở góc phải (`forum` cho chat, `smart_toy` cho Agent). Thông tin nhóm: khối Top nằm trong cùng HeaderBg, bo góc dưới 24px.

## Rà soát bổ sung (17/11) — đủ màn cho dev
Đối chiếu kiểm kê tính năng gop_db, vẽ thêm 18 màn (2 hàng mới ⑤ ⑥ + AG-06 + CH-05c). Tổng khu: 43 màn.
- Hàng ⑤ Tiện ích trong hội thoại: CH-18 Tìm tin (≤30 kết quả, tô từ khoá, nhảy tới tin) · CH-19 Tin đã ghim (≤20, nút ⋮: Xem / Bỏ ghim) · CH-20 Chia sẻ tin (≤20 hội thoại + lời nhắn) · CH-21 Xem ảnh toàn màn · CH-22 Ảnh/Tệp/Link xem tất cả · CH-23 Xem trước ảnh khi gửi (Cắt + Xoay, ≤10 ảnh) · CH-24 Sửa tin (dải vàng 'Đang sửa', nút ✓) · CH-24b Xác nhận thu hồi.
- Hàng ⑥: CH-25 Thông tin hội thoại 1–1 · CH-26 Thêm thành viên (Quản lý, chọn vai trò khi thêm, 'Đã trong nhóm' không chọn được) · CH-27 Xác nhận rời nhóm · CH-27b Mời ra bị chặn 422 (báo trong sheet + 'Xem việc của người này') · CH-28 Tạo nhiệm vụ từ tin (DÙNG LẠI form NV2-10, thêm khối 'Tạo từ tin nhắn', điền sẵn nhóm / tên / người được @) · CH-29 Push màn khoá · CH-29b Banner tin mới trong app · CH-30 Rỗng + 'Đang kết nối lại…'.
- CH-05c Tạo nhóm thiếu Tên (validate dưới ô, không toast). AG-06 Agent: quá 150s chưa có kết quả (Hỏi lại) · hỏi quá nhanh · hết hạn mức (ô nhập khoá, header 'Còn 0/20' cam).
Claude tự chốt: hộp xác nhận (thu hồi, rời nhóm) đặt nút nguy hiểm trước, Huỷ cuối; lỗi nghiệp vụ hiện trong sheet thay vì toast; banner trong app tự ẩn 4 giây.

## Chi tiết 3 tab Việc của nhóm (17/11) — bám logic web gop_db
Nguồn: `WorkspaceTaskListService` (QUICK all/mine/overdue/waiting_my_approval · GROUP_BY status/assignee/due · DUE_GROUPS · SORTABLE), `TaskGroupToolbar/TaskRowActions` (nút bước tiếp next_action_label · ⇄ · 💬 · ⋯), `WorkspaceMeetingList` (bucket upcoming/done/cancelled/all, màu chip, Hôm nay, result_pending, has_minutes), app `work_issue_list_page` (lọc 'Tôi …').
- CH-12 làm lại: thanh công cụ Lọc nhanh · '1 quá hạn' · 🔍 · ☰ · ⚙; gom Trạng thái; thẻ có tiến độ + hàng nút hiện sẵn (bước tiếp theo vai trò / dòng khoá 'Chờ X…', ⇄, 💬, ⋯); Đã xong thu gọn.
- Hàng ⑦: G-01 Lọc nhanh (số đếm quick_counts) · G-02 Cách xem (Gom theo 3 · Sắp xếp 6 + chiều · Thu gọn tất cả) · G-05 Đổi trạng thái (chỉ allowed_next_statuses) · G-03 Gom theo Người làm + dải lọc 'Người làm: X ×' (từ CH-27b) · G-06 Gom theo Hạn (đúng DUE_GROUPS: Quá hạn · 7 ngày tới · Sau đó · Không có hạn · Chờ duyệt · Đã xong) · G-04 Bộ lọc nâng cao (Người làm · Người giao · Trạng thái · Ưu tiên · Hạn từ–đến; Áp dụng · Đặt lại · Huỷ) · G-07 Tìm không có kết quả · G-08 Nhóm chưa có nhiệm vụ.
- CH-13 làm lại + M-01 Đã họp (biên bản, 'Chưa cập nhật kết quả') + M-02 Đã huỷ rỗng.
- CH-14 làm lại (gom trạng thái Issue, nút Nhận xử lý / Báo đã xử lý / Xác nhận đóng, phòng ban khi chưa phân công) + V-01 Lọc nhanh 'Tôi …' + V-02 Nhóm chưa có vấn đề.
- Số trên thanh chuyển = việc dở (Nhiệm vụ 4 · Meeting 2 sắp họp · Vấn đề 4) — đồng bộ mọi màn.
- Tự chốt: Cách xem lưu BE theo người dùng (dùng chung web/app) — CẦN BE nếu web chưa lưu; khi code hỏi lại.
