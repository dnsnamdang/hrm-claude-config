# Design — Thiết kế lại màn Tạo / Sửa / Chi tiết meeting

Phụ trách: @dnsnamdang · Nhánh `gop_db` (hrm-client) · Bắt đầu 15/10/2026 · **Mockup CHỐT 15/10/2026**
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-15-meeting-form-redesign-design.md`
Mockup chốt: `mockup-chot-2026-10-15.html` (bản đóng băng) · `mockup.html` (bản làm việc) · Ảnh hiện trạng: `hien-trang-tao-meeting.png`

## Yêu cầu user (15/10/2026)
- Form meeting gọn, có cấu trúc, dễ phân biệt nhóm nội dung; bố cục theo THỨ TỰ CHỌN nội dung.
- Bỏ thanh trạng thái (Lên lịch / Đã chốt / Hoàn thành / Huỷ) phía trên.
- Ghi chú dưới ô → icon ⓘ. Thiết kế đủ các tab (Thông tin, Nhân sự tham gia, Biên bản, Nhiệm vụ, Dự án TKT).

## Hiện trạng (trước khi làm)
Tab Thông tin là 1 cột dài không chia nhóm; ô Dự án nằm TRÊN ô Khách hàng dù phải chọn KH trước; khối KH lặp 3 ô khoá
(tên/chức vụ/SĐT); editor 2 hàng ~40 nút; ghi chú cam/đỏ dưới ô. Tab Biên bản có I–III chỉ là dòng chữ "tự thêm khi in",
nút "Excel" sai chữ chuẩn. Dự án TKT dùng tab gạch chân bootstrap + form dài.

## Quyết định đã chốt (15/10/2026 — user "Chốt mockup")
| # | Nội dung |
|---|---|
| D1 | Bỏ thanh trạng thái ở CẢ Tạo/Sửa/Chi tiết; trạng thái hiện bằng badge trong khối "Thông tin bản ghi" ở cột phải |
| D2 | Tab Thông tin chia 5 khối `V2BaseFormSection` đánh số theo thứ tự chọn: ① Loại meeting → ② Khách hàng & đối tượng (chỉ khi loại có KH; khoá tới khi chọn Loại; KH → Người liên hệ → Dự án TKT/Hợp đồng lọc theo KH) → ③ Nội dung → ④ Thời gian, địa điểm & chủ trì → ⑤ Tài liệu chuẩn bị. Ẩn khối ② thì đánh lại số |
| D3 | Mọi ghi chú dưới ô → icon ⓘ `ri-information-line` + popover `info-popover` cạnh nhãn |
| D4 | Cột phải (chỉ ở tab Thông tin): "Xác nhận tham dự" (chỉ Chi tiết) · "Thông tin bản ghi" (mã, trạng thái, người tạo, ngày tạo, cập nhật gần nhất) · "Tóm tắt cuộc họp" (mục bắt buộc đủ/thiếu + tiến độ, bấm cuộn tới khối). Tab khác dùng full chiều ngang |
| D5 | Nút "Gợi ý tên" cạnh Tên meeting (Loại + Dự án/Hợp đồng + KH, sửa lại được) |
| D6 | Màn Chi tiết dùng CHUNG bố cục, ô ở trạng thái chỉ đọc |
| D7 | **4 thành phần làm mới thành DÙNG CHUNG, áp cả hệ thống (chấp nhận màn khác đổi theo)** — xem bảng dưới |
| D8 | Phần còn lại theo chuẩn chung: `V2BaseFormSection`, `V2BaseInput`/`V2BaseLabel` (viền `#cbd5e1`, bo 5px, cao 34px), `V2BaseBadge :color` màu BE, `V2Footer`, font Roboto, nút theo `button-convention` |
| D9 | (15/10/2026, user) Tab Dự án TKT › Thông tin chung = THẺ TÓM TẮT chỉ các trường chính + bắt buộc (Mã, Tên, tiến trình, Ứng dụng, Nhóm ngành, NV KD chính, Quy mô, Phân loại đầu tư, Cách triển khai, Địa điểm; thẻ KH + Loại hình, Lĩnh vực, Người liên hệ) + nút "Xem chi tiết" chuyển tới `/assign/prospective-projects/{id}`. Bỏ nhúng nguyên form dự án (bớt ~8 request mỗi lần mở tab). Tên danh mục do BE trả sẵn |

### D7 — 4 thành phần dùng chung (theo mockup chốt)
| Thành phần | Thiết kế |
|---|---|
| **Tab chính** (`V2BaseTabNavigation`) | Thanh viên thuốc bo 999px, nền `rgba(242,242,247,.78)` + `backdrop-filter: blur(22px) saturate(180%)`, viền trắng, bóng nhẹ `0 2px 8px rgba(15,23,42,.05)`; tab cao 32px, chữ 13px 600, khe 4px, cột theo nội dung. Tab chọn: viên `rgba(5,150,105,.12)` viền mảnh, chữ/icon `#059669` đậm 700, số đếm nền `#059669` chữ trắng. Hover: viên trắng `rgba(255,255,255,.95)` nở 2px mỗi bên (đổi width thật, KHÔNG `transform: scale` chữ — mờ). Đổi tab: viên giãn phủ đường đi 160ms rồi co về kiểu lò xo. Dính trên cùng khi cuộn (màn form) |
| **Nút gạt** (`V2BaseSegmented` mới) | Rãnh `rgba(118,118,128,.12)` bo 9px padding 2px; viên chọn trắng bóng nhẹ, chữ đen 600, icon `#059669`; cao 34px (= ô nhập), bản `sm` 24px cho trong bảng; mỗi lựa chọn có thể mang màu riêng (điểm danh). Dùng: Phân loại họp, Hình thức, điểm danh, câu Có/Không khảo sát, tab con Dự án TKT, câu chọn 1 trong phiếu |
| **Thẻ khách hàng** (mới) | Ô icon 42px bo 12px nền chuyển màu (doanh nghiệp `#0ea5e9→#2563eb` `ri-building-4-fill` / cá nhân `#a78bfa→#7c3aed` `ri-user-3-fill`); tên đậm + mã KH dạng nhãn mono + badge loại KH (`#0EA5E9` / `#7C3AED`); lưới MST · SĐT · email · địa chỉ có icon xám; slot nút icon bên phải (Lịch sử meeting, Đổi KH) |
| **Thêm nhanh** (mới) | Chip cao 22px bo 11px viền đứt `#86efac` nền `#f0fdf4` chữ `#15803d` 12px 500 + icon; hover viền liền nền `#dcfce7`; đặt bên phải nhãn / đầu nhóm. Chữ "Thêm nhanh <đối tượng>"; dùng cả cho "Thêm nhân sự", "Thêm dòng" đầu nhóm, "Giao nhiệm vụ", "Mở dự án". Thay 4 kiểu đang lệch nhau trong dự án |

### Các tab (theo mockup chốt)
- **Nhân sự tham gia**: 1 bảng nhóm Phía Công ty / Phía Khách hàng (+ số người), kéo ⋮⋮; NV hiện tên + "Mã phòng · Mã NV", badge "Chủ trì"; điểm danh = nút gạt 3 lựa chọn (Có mặt `#16A34A` / Vắng có lý do `#D97706` / Vắng không lý do `#DC2626`), hiện từ Chốt lịch; tiêu đề có bộ đếm + "Tất cả có mặt"; Chi tiết hiện badge.
- **Biên bản**: cảnh báo hạn nhập; I–III gộp 1 dòng "tự thêm khi in" + In · **Xuất Excel**; Khảo sát (chỉ loại Giới thiệu SP); Nội dung trao đổi (Thêm dòng · Xóa hết; Chi tiết có cột Nhiệm vụ: mã đã giao / "Giao nhiệm vụ"); Tài liệu; Kết luận*. Số La Mã tự đánh lại.
- **Nhiệm vụ** (chỉ Chi tiết): ô tìm + Tìm kiếm / Làm mới, badge Quá hạn, Tạo mới; bảng mã · tên · loại · người thực hiện · hạn · trạng thái.
- **Dự án TKT**: thẻ chọn dự án khi gắn nhiều dự án; tab con nút gạt "Thông tin chung / Phiếu thu thập thông tin"; Thông tin chung CHỈ XEM (thẻ KH dùng chung + ô khoá) + "Mở dự án"; Phiếu có "Lưu phiếu".
- **Footer** (`V2Footer`, không đổi logic): Tạo mới = Lưu nháp · Lưu và Lên lịch · Lưu và Chốt lịch · Quay lại; Sửa = Lưu · Hoàn thành · Hủy · Quay lại; Chi tiết = Sửa · In · Tạo phiếu công tác khác · Hủy · Quay lại.

## Phạm vi ảnh hưởng (rà 15/10/2026)
- `V2BaseTabNavigation`: 7 màn (meeting, Dự án TKT manager, Giải pháp form + manager, Hạng mục manager, Yêu cầu giải pháp, Công việc của tôi).
- Thêm nhanh: GeneralInfo (2) · prospective-projects/CustomerBlock (2) · tasks/CreateTaskModal (2) · WarrantyRepairHandleRequestForm (1) · CustomerEquipmentPickerModal (1) · MeetingRoomModal (1, "Thêm tiện nghi" → "Thêm nhanh tiện nghi") · WrMaintenanceTable.
- Thẻ KH: meeting/GeneralInfo + prospective-projects/CustomerBlock (khối `readonly-customer-info`).
- Không đổi BE / DB / quyền / API (trừ khi API chi tiết thiếu người cập nhật — sẽ hỏi).

## Lệch so với mockup khi code (15/10/2026)
| Mục | Mockup | Đã làm | Lý do |
|---|---|---|---|
| Thanh tab / cột phải dính khi cuộn | sticky | KHÔNG sticky (prop `sticky` có sẵn nhưng chưa bật) | Layout chung `.content-page` đặt `overflow: hidden` → sticky vô hiệu; sửa layout là phạm vi khác |
| Hình thức Online | Online → Link thay Phòng họp | Online → thêm Link; Phòng họp vẫn hiện cả 2 hình thức | Task 75 (user chốt 20/09/2026): họp Online vẫn cần phòng |
| Số mục tab Biên bản | I · IV Khảo sát · V Nội dung · VI Tài liệu · VII Kết luận | Giữ I–III · IV (1/ Khảo sát, 2/ Nội dung khác, 3/ Tài liệu) · V Kết luận | Khớp đúng số mục trên bản in / Excel biên bản |
| Editor Kết luận | thanh công cụ rút gọn | giữ full toolbar | Redmine #11194 (soạn thảo giàu định dạng như ERP); chỉ rút gọn editor Mục tiêu |
| Thông tin bản ghi | người tạo · phòng, ngày giờ tạo, người cập nhật | ĐÃ ĐỦ (15/10): BE thêm `creator_label`, `created_at_full`, `updater_label` | — |
| Mã phòng · Mã NV trong Nhân sự | có | ĐÃ ĐỦ (15/10): BE trả `department_code`, `employee_code` cho từng thành viên | — |

## Vòng 2 — Form liền mạch (19/10/2026, CHỜ DUYỆT mockup)
Mockup: `mockup-lien-mach-2026-10-19.html` (DOM + CSS thật của /assign/meeting/6356/edit, gop_db e58f09621; thanh nổi góc phải chuyển Hiện trạng / A / B) · ảnh `anh-mockup/lien-mach-v-*.png`
Yêu cầu user: (1) card chính sau `<main>` p-3 → p-1 · (2) bỏ card từng khối, liền mạch, chia bằng tiêu đề khối · (3) vòng số mỗi khối một màu nền.

| Phương án | Mô tả | Cột form cao (1440) |
|---|---|---|
| Hiện trạng | 5 card viền + bóng, cách 14px, card chính padding 24px | 1461px · rộng 834px |
| **A (đề xuất)** | Tiêu đề = vòng số màu + chữ + đường kẻ mảnh `#e5e7eb` chạy hết hàng; không khung | **1303px (−158)** · rộng 874px |
| B | Dải tiêu đề nền `rgba(màu khối,.07)` bo 6px; không khung | 1333px (−128) · rộng 874px |

Tự chốt (thuần UI, ghi trong comment đầu file mockup): màu gắn theo LOẠI khối (data-sec) không theo số; giữ nghĩa vòng số
(nhạt = chưa xong, đặc = `.is-done`); khối ⑤ `FileAttachmentTable` đưa về cùng khuôn tiêu đề (hiện lệch: tiêu đề x=292 so với 266
của 4 khối kia) → khi code cần slot/prop tiêu đề cho component dùng chung này; cột phải giữ dạng card.
Bảng màu: ① type `#0EA5E9` · ② target `#8B5CF6` · ③ content `#F59E0B` · ④ time `#16A34A` · ⑤ files `#EC4899`.

### Vòng 2b (19/10/2026) — user chọn B (dải tiêu đề màu), thử viền màu nhẹ, phần còn lại giữ hiện trạng
Mockup cập nhật cùng file (thanh nổi: Hiện trạng / B không viền / **B + viền màu nhẹ** mặc định). Bỏ phương án A.
Màu theo ý nghĩa tiêu đề: ① Loại meeting indigo `#4F46E5` · ② Khách hàng & đối tượng sky `#0284C7` (đồng bộ thẻ KH + badge "Khách hàng") ·
③ Nội dung amber `#D97706` · ④ Thời gian, địa điểm & chủ trì emerald `#059669` · ⑤ Tài liệu pink `#DB2777`.
Dải tiêu đề = `rgba(màu,.07)` padding 6px 10px · viền khối = `1px rgba(màu,.28)` bo 8px · khối cách 12px · thân khối padding 10px 10px 8px.
Đo (1440): cột form 1461 → B 1333 · B+viền 1351px; rộng 834 → 874px; không tràn ngang (1440 + 1366). CHỜ user chọn có/không viền.

### Vòng 2c (19/10/2026) — tiêu đề lệch xuống + header cột phải cao hơn → 1 chuẩn header chung
Tái hiện bằng số đo: chữ tiêu đề lệch xuống 3,7px, vòng số 5px so với tâm dải (hiện trạng cũng lệch 3,2px). Gốc: `h6` dính
`margin-top: 10px` từ rule toàn cục (`mb-0` chỉ xoá margin dưới). Header 2 card cột phải cao 52,6px (padding 12px) vs dải khối 44px.
Chuẩn chung áp cho 5 khối + 2 card cột phải: header **cao 36px**, padding 0 10px, flex căn giữa, `h6` margin 0 · 14px/700 · lh 20px,
vòng số / icon 22px, dải `rgba(màu,.07)` không gạch dưới; cột phải màu trung tính slate `#64748B`, cùng khung viền khối.
Đo lại: 7/7 header cao 36px, lệch tâm 0px (khối ⑤ 0,5px — sai số font). Cột form (1440): hiện trạng 1461 → B 1293 · **B+viền 1327px**.
