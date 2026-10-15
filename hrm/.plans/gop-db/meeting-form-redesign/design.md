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
