# Design (tóm tắt) — Phân hệ Công việc: Không gian làm việc + Nhóm chat

- **Nhánh:** `gop_db` (hrm-api, hrm-client) + TPE_APP · **Phụ trách:** @namdangit · **Ngày:** 2026-11-02
- **Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md`
- **(11/11) Đợt CORE CHAT đã code xong + commit + push nhánh 11/11 (chưa merge gop_db)** — Nhóm trao đổi + chat 1–1 web: spec §11, plan `.plans/agent-chat/chat/gd1-core-chat/plan.md`, nhánh `gop_db-nhom-trao-doi`, worktree `websites/wt-nhom-trao-doi/`.
- **⚠ 09/11/2026 — đổi logic lớn:** chỉ còn 2 loại không gian: **Nhóm trao đổi** (thay Phòng làm việc + Dự án nội bộ) và **Dự án khách hàng**. Mục 0–3 và 8 bên dưới đã viết lại; mockup GĐ0 + app còn vẽ theo bản cũ, phải sửa.
- **Trạng thái:** **mockup GĐ0 đã chốt 05/11/2026** (30 màn + thuyết minh logic `gd0-mockup/thuyet-minh.html`); CHƯA có lệnh code. Feature lớn → folder con cho từng giai đoạn, chỉ tạo khi bắt đầu giai đoạn đó.

## Mục tiêu
Nhân viên vào phân hệ Công việc, chọn 1 không gian mình tham gia (Nhóm trao đổi / Dự án khách hàng), giao việc bằng Nhiệm vụ / Vấn đề, trao đổi bằng nhóm chat — web + app, quản lý đồng nhất mọi loại.

## Quyết định lớn (02/11/2026)
0. **(09/11, thay 03/11) 2 loại:** **Nhóm trao đổi** (người dùng tạo) và **Dự án khách hàng** (tự sinh: Tiền khả thi · Giải pháp · Hợp đồng; luôn hiện khách hàng). Bỏ Phòng làm việc, Dự án nội bộ, cây cha–con, Mở/Kín. Không dùng chữ "Dự án" đứng một mình.
1. **Nhóm trao đổi phẳng**, **thời hạn tuỳ chọn** (có hạn: hiện hạn + nhắc quá hạn hằng tuần từ ngày thứ 7; không hạn: chạy tới khi đóng). Mọi nhóm Đóng / Mở lại được. Dự án KH: GP có Hạng mục (giữ).
2. **Thành viên Nhóm trao đổi:** thêm từng người, hoặc **lấy toàn bộ nhân sự 1 hay nhiều phòng ban / bộ phận — chép 1 lần lúc chọn, KHÔNG đồng bộ về sau**; bỏ trùng; người lấy vào là Thành viên, người tạo là Quản lý.
3. Chỉ thành viên xem được Nhóm trao đổi (ngoại lệ: vai trò cá nhân trên việc + quyền xem theo tổ chức chỉ mở Nhiệm vụ/Vấn đề, không mở chat).
4. Vai trò: Quản lý / Thành viên / Xem. 1 hàm kiểm quyền chung web + app; bịt lỗ hổng show/update Task.
5. **Dự án TKT, Giải pháp, Hợp đồng tự có không gian**, thành viên lấy từ nguồn gốc; màn manager cũ giữ chỗ, thêm tab Trao đổi.
5b. **TKT và Giải pháp = 2 không gian riêng, nối bằng liên kết** (không cha–con); Hạng mục là cấu trúc con riêng của Giải pháp (giữ nguyên). 2 đội KHÔNG thấy không gian của nhau; ngoại lệ: màn TKT giữ nguyên tab Giải pháp / Vấn đề GP / Files (nơi đội GP trả kết quả).
6. Không có luồng nhận yêu cầu từ ngoài; giao việc chỉ bằng Nhiệm vụ / Vấn đề.
7. Trao đổi: bình luận trong Nhiệm vụ/Vấn đề (giữ) + **nhóm chat** mỗi không gian; chat nối việc: tạo việc từ tin, thẻ `#` việc, tin hệ thống theo sự kiện (Quản lý chọn sự kiện). Khung tin = kiểu tin + nội dung + đối tượng gắn kèm, mở rộng bằng loại thẻ / listener sự kiện.
8. **(09/11) Quyền tạo:** mọi nhân viên tạo được Nhóm trao đổi, không cần mã quyền riêng.
9b. **(10/11, thay 03/11) Thanh tab mọi không gian:** **Trao đổi · Nhiệm vụ · Meeting · Vấn đề · Báo cáo · File** + "Thêm ▾". Trao đổi là tab đầu, mở không gian là vào đây; "Tổng quan" đổi tên "Báo cáo". **Nhóm trao đổi: chỉ Trao đổi cố định, các tab khác bật mới hiện (mặc định tắt)**; Dự án KH chưa áp (user sửa sau).
9c. **(03/11) Sidebar truy cập nhanh (U14):** trên rail hub có mục "Không gian làm việc" mở panel chuyển nhanh (tìm, Ctrl K, Ghim & gần đây · Nhóm trao đổi · Dự án KH · Lưu trữ — sửa 09/11) + tối đa 5 không gian ghim nằm thẳng trên rail. Không thêm cột menu thứ 2.
9d. **(04/11) Sidebar + popover menu (mockup đã áp toàn bộ, `gd0-mockup/sb2.css` + `sb2.js`):** rail GIỮ nền navy (khách chốt màu nhận diện), icon 1 màu, mục ghim giữ màu theo loại, số tin chưa đọc là chip trong mờ (đỏ chỉ cho quá hạn). Thứ tự: Yêu thích · Gần đây | Tổng quan · Lịch làm việc · Không gian làm việc · Việc của tôi | Đã ghim | Làm giải pháp · Nhiệm vụ · Tiếp nhận · Phân công · Kết quả · Báo cáo · Phê duyệt; **Thiết lập ghim đáy rail**. Đổi tên: "Lịch làm việc của tôi" → "Lịch làm việc", "Công việc của tôi" → "Việc của tôi". Topbar bỏ hiệu ứng sáng (sóng, đốm sáng, vệt bóng). Popover cấp 2/3: **ĐÃ CHỐT nền navy giống sidebar** (khách chốt 04/11; phương án nền trắng đã loại). Panel Không gian làm việc gọn chữ: 1 dòng/không gian (mô tả vào tooltip), chỉ tiêu đề đậm.
7c. **(10/11) Khung chung kiểu Teams**: cột Hội thoại bên trái mọi màn không gian (chat nhóm + 1–1, thu gọn được); khung phải = đầu không gian + dải tab (khi chọn nhóm / dự án KH) hoặc chat 1–1 (khi chọn người). Chip không gian chuyển từ topbar xuống khung phải.
7b. **(10/11) Chat cá nhân 1–1** (spec §4.6): tin nhắn thuộc **Hội thoại** (nhóm của không gian / 1–1 / nhóm tự lập sau); tab Trao đổi có cột danh sách hội thoại (chat nhóm + nhắn riêng thành viên), rail có mục **Tin nhắn** gom mọi hội thoại; 1–1 là 1 luồng duy nhất cho mỗi cặp người; nhắn được mọi NV cùng công ty.
9. App đợt 1: không gian của tôi, chat, cập nhật + tạo nhanh việc. Cấu hình/thành viên/báo cáo chỉ trên web.
9e. **(05/11) U26 — thanh dưới app:** Việc của tôi · Không gian · [+ Tạo mới] · Nhiệm vụ · Phê duyệt (đổi U3 của app Nhiệm vụ/Vấn đề); Vấn đề vào drawer, vẫn tạo từ [+]. Mockup app M8: 8 màn KG-01…KG-08 trong `meeting-mobile.pen` (hàng y 5040).

## Giai đoạn đề xuất
1 Nền không gian + quyền · 2 Nhiệm vụ/Vấn đề theo không gian · 3 Chat đợt 1 · 4 App · 5 Chat tin hệ thống + Hợp đồng · 6 Mở rộng.

## Tồn / quyết định Claude tự chốt
Xem spec §8 (K1–K6), §9 (ảnh hưởng luồng đang chạy). Socket: `hrm-api/server_node/server.js`, phải sửa để tách sự kiện chat khỏi chuông (§4.5).
