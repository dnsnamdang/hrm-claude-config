# Đặc tả màn hình — Phân hệ Meeting (TPE_APP Flutter)

> Nguồn: file thiết kế `meeting-mobile.pen` (đọc lại 22/10/2026). Tài liệu này chép lại **đúng nội dung thiết kế** để dev Flutter bám theo — không thêm nội dung ngoài bản vẽ. Các khối "CHỐT CHO DEV" / "LƯU Ý CHO DEV" được chép **nguyên văn**.
>
> Quy ước trong tài liệu: `*` = trường/khối bắt buộc (dấu sao đỏ `#DC2626`) · **[Primary]** = nút chính (gradient xanh ngọc) · **[Secondary]** = nút viền trắng · "dòng chọn" = nhãn trái – giá trị phải + chevron (bấm mở màn/sheet chọn) · "ô gõ" = ô nhập có khung.
>
> Dữ liệu mẫu xuyên suốt: meeting `MTG.26.0245` — "Thương thảo hợp đồng và chốt phương án cung cấp - Xưởng 3S VinFast", 08:30–10:00 Thứ 2 14/09/2026, Phòng 302 Trụ sở Hà Nội, chủ trì Nguyễn Hữu Học - Phó TGĐ, KH `KH.26.0187 - CT CP Sản xuất & KD VinFast`.

---

## A. Tổng quan luồng (artboard "00 · Tổng quan luồng")

"LUỒNG NGHIỆP VỤ MEETING TRÊN APP · 50 artboard · thiết kế cho TPE_APP (Flutter), bám design system app hiện hành và bám 100% logic bản web. Đọc từ trên xuống theo 5 bước + bộ màn chỉ xem + nhóm ngoại lệ; mỗi bước đọc từ trái sang phải."

| Bước | Tên | Mô tả (nguyên văn) | Màn |
|---|---|---|---|
| 1 | TÌM CUỘC HỌP | Mở app vào tab Meeting. Tìm nhanh theo mã / tên, hoặc lọc sâu 10 tiêu chí để ra đúng cuộc họp cần xử lý. | 01 Lịch meeting · 02 Bộ lọc |
| 2 | TẠO CUỘC HỌP | Từ nút + ở màn Lịch. Nhập 7 trường tối thiểu; lưu xong vào thẳng Hub, trạng thái Lưu nháp. | 03 Tạo meeting · 04a Hub — Lưu nháp |
| 3 | CHUẨN BỊ HỒ SƠ | Hub ở trạng thái Lưu nháp. Bấm từng dòng trong Hub để điền; thanh Mức độ hoàn thiện hồ sơ đếm các khối cần cho Hoàn thành, tăng dần 1/3 → 2/3. Có 2 loại tài liệu tách bạch: Tài liệu chuẩn bị (trước họp) và Tài liệu biên bản (sau họp). Khối Khách hàng & Người liên hệ có màn chọn riêng + lối thêm nhanh (5 màn cam). | 05 · 06 · 06b · 07 · 17 · 18 · 19 · 20 · 21 · 25 · 28 · 41 · 41b · 42 · 43 · 44 · 48 · 49 |
| 4 | CHỐT LỊCH & HỌP | Gửi lịch hẹn xong meeting sang Đã chốt lịch — đây mới là lúc cột điểm danh (Nhân sự tham gia) mở và bắt đầu ghi biên bản. Sửa giờ lịch đã chốt sẽ hỏi xác nhận gửi lịch mới. | 04b · 08 · 09 · 10 · 14 · 22 · 23 · 29 · 30 · 31 · 46 |
| 5 | GHI NHẬN & HOÀN TẤT | Đính kèm tài liệu, khảo sát nhu cầu, ghi biên bản — nội dung trao đổi + kết luận (bắt buộc) — rồi chuyển sang Đã hoàn thành và xuất biên bản. | 11 · 12 · 13 · 04c · 15 |
| ! | NGOẠI LỆ & TRẠNG THÁI KHÁC | Ngoài luồng chính: huỷ cuộc họp (lý do không bắt buộc — *ghi chú ở artboard bước; màn 16 lại đánh `*` cho Lý do huỷ, xem mục 16*), lỗi validate khi bấm Lưu, trường hợp người dùng chỉ là thành viên tham dự (chỉ xem), và cảnh báo khi bấm Quay lại lúc còn thay đổi chưa lưu. | 16 · 24 · 26 · 27 · 45 |
| XEM | CHẾ ĐỘ CHỈ XEM — MEETING ĐÃ HOÀN THÀNH | Web bật cờ isShow cho toàn bộ khối: khoá mọi ô nhập, ẩn nút thêm/xoá. Trên app thiết kế thành bộ màn riêng — bỏ khung ô, chuyển sang nhãn–giá trị để đọc nhanh; thanh dưới chỉ còn Quay lại. | 33 · 34 · 32 · 36 · 37 · 38 · 39 |

**Mũi tên luồng trên canvas** (nhãn nguyên văn): `↓ Bấm nút + tạo mới` · `→ Bấm ⚙ Bộ lọc` · `→ Bấm Tạo meeting` · `↓ Lưu → trạng thái Lưu nháp` · `→ Về Hub → bấm Dự án TKT` · `→ Bấm Phiếu thu thập thông tin` · `→ Bấm ô Dự án TKT` · `↓ Bấm ô Hợp đồng` · `→ Về Hub → bấm Nhân sự tham gia` · `↓ Thêm nhân sự` · `→ Màn phụ của bước 3` · `→ Bấm ô Khách hàng` · `→ Lọc không ra kết quả` · `↓ Bấm Thêm nhanh KH` · `→ Bấm ô Người liên hệ` · `→ Bấm Thêm nhanh liên hệ` · `↓ Gửi lịch hẹn → Đã chốt lịch` · `→ Bấm Nhân sự tham gia` · `→ Về Hub → Ghi biên bản` · `→ Bấm Thêm nội dung` · `↓ Chọn người thực hiện` · `→ Popup của bước 4` · `→ Thiếu nhiều khối` · `↓ Họp xong` · `→ Về Hub → Khảo sát` · `→ Biên bản → Sửa kết luận` · `→ Xong · Lưu biên bản → Hoàn thành` · `↓ Hoàn thành → khoá sửa` · `↓ Bấm Xem biên bản` · `↓ Từ menu ⋮ trên Hub`.

### Vòng đời trạng thái meeting (theo bản vẽ)
`Lưu nháp` (status 0, nút **Lên lịch hẹn**) → `Đã chốt lịch` (nút **Hoàn thành**) → `Đã hoàn thành` (status 3, khoá sửa) · nhánh `Huỷ` (status 4, từ menu ⋮). Trên chip/badge danh sách còn có nhãn "Đang tạo (nháp)" trong ghi chú dev = Lưu nháp.

---

## B. Quy ước thông báo (nguyên văn)

"Quy ước thông báo — 3 loại dải, không dùng toast nổi:
- **ĐỎ `#FEE2E2`** = lỗi / chặn / đã huỷ (dải full-width dưới header)
- **XÁM `#F1F5F9`** = đã khoá, chỉ xem (dải full-width dưới header)
- **XANH `#E3F2FD`** = thông tin, hướng dẫn (thẻ bo góc trong nội dung).

Hộp thoại (huỷ meeting, đổi giờ, menu ⋮, chọn liên hệ, cảnh báo chưa lưu) vẫn là popup vì bắt người dùng ra quyết định."

---

## C. Điều hướng phân hệ Meeting

### C1. Bottom menu (C/BottomNav) — "Template · Bottom menu dùng chung các phân hệ"
"1 component C/BottomNav cho cả 5 phân hệ — chỉ đổi theme `phanhe` (màu tự đổi theo màu nhận diện) + icon / nhãn từng tab. Thay thanh 5 phím tắt cũ (không có trạng thái đang chọn)."

Giải phẫu (nguyên văn):
1. **Thanh** — Nền trắng, bo 24 góc trên, bóng mờ hướng lên; cao 64 + vùng an toàn 26 (home indicator).
2. **4 tab** — Icon 22 + nhãn 11. Tab đang chọn: viên thuốc nền nav-tint, icon + nhãn đậm màu nav-c. Tab thường: xám `#94A3B8` / `#64748B`.
3. **Nút chính (giữa)** — Tròn 58, gradient nav-c2 → nav-c, viền trắng 4, nổi lên 28px, bóng cùng màu. Là thao tác TẠO hay dùng nhất của phân hệ (= nút CTA đầu drawer).
4. **Badge** — Chấm đỏ 9px góc trên phải icon — có việc cần xử lý (quá hạn, chờ duyệt, chưa đọc). Số cụ thể xem trong drawer.
5. **Quy tắc** — Đúng 4 tab + 1 nút chính. Tab 1 = màn chính của phân hệ. Mục ít dùng để trong drawer (☰). Ẩn thanh ở màn form / chi tiết (có Bottom Bar Lưu riêng).

Bảng áp dụng 5 phân hệ (thông tin tham chiếu):

| Phân hệ | Màu | Tab |
|---|---|---|
| Chấm công | `#2E71C3` | Tổng quan · Lịch sử · [Chấm công] · Bảng công · Đơn từ |
| Công việc | `#1E8A63` | Tasks · Tiến độ · [Giao việc] · Phiếu · Phê duyệt |
| **Meeting** | **`#0E8FA8`** | Lịch · Danh sách · [Tạo meeting] · Phòng họp · Báo cáo *(bảng anatomy)* |
| Quản lý cơm | `#D9752A` | Lịch cơm · Thông báo · [Ăn dài ngày] · Phiếu · Cài đặt |
| Đào tạo | `#6B54B8` | Tổng quan · Khoá học · [Đăng ký] · Lịch thi · Năng lực |

**Bottom menu Meeting CHỐT (theo 00h, màn 01):** `Tổng quan` · `Lịch` · **[Tạo meeting]** (nút tròn giữa, icon `plus`) · `Danh sách` · `Phòng họp` — "Báo cáo vào drawer". Màn 01 đang chọn tab **Lịch**; màn 00h đang chọn tab **Tổng quan**.

> Lưu ý lệch: bảng anatomy (5 phân hệ) vẫn ghi Meeting = Lịch · Danh sách · Tạo meeting · Phòng họp · Báo cáo; ghi chú 00h chốt lại là Tổng quan · Lịch · [Tạo meeting] · Danh sách · Phòng họp. Theo 00h (bản chốt sau, user chốt).

Thông số C/BottomNav (component `TTVFU`): bar padding `[8,6,26,6]`, stroke top `#E8ECF1`, bóng `#0F172A14` offset y −4 blur 20; pill tab chọn 52×30 bo 15 nền `#0E8FA81F`, icon `#0E8FA8`, nhãn 11 bold 700 `#0E8FA8`; tab thường icon `#94A3B8`, nhãn 11/500 `#64748B`; FAB 58×58 bo 29, gradient 215° `#2CC3D6`→`#0E8FA8`, viền trắng 4 (outer), bóng `#0E8FA859` y 8 blur 18, icon plus 28 trắng, nhãn "Tạo meeting" 11/700 `#0E8FA8` dưới FAB; badge chấm đỏ `#EF4444` 9×9 viền trắng 2 (mặc định ẩn).

### C2. 00d · Menu trái (drawer) — phân hệ Meeting
Mô tả (nguyên văn): "Cùng khuôn drawer 00c, màu nhận diện Meeting xanh ngọc #0E8FA8. Mục lấy từ menu phân hệ Meeting của web (components/subsystem-menu/meeting.js), BỎ Cấu hình + Danh mục (loại meeting, lý do huỷ, phòng họp, tiện nghi, mục đích) — việc quản trị làm trên web. Nút "Tạo meeting" đặt đầu menu (thao tác hay dùng nhất, mở màn 03). Báo cáo chưa có màn ở web (Meeting theo khách hàng, Hiệu quả sử dụng phòng họp) hiện xám + nhãn "Sắp có", không bấm được. Badge: số meeting hôm nay / chờ biên bản. Ở 852px vùng Menu cuộn dọc (đầu + cuối drawer cố định như 00c'), nút Tạo meeting cuộn cùng danh sách."

Bố cục:
- **Đầu drawer (cố định, nền gradient):** avatar chữ tắt `DA` · `DNS Admin` · `HN_KD2 · 11010057` · thẻ `PHÂN HỆ` / `Meeting` + nút `Đổi` (mở 00b chọn phân hệ).
- **Nút CTA** `Tạo meeting` (full-width, icon lịch) → màn 03.
- **Menu:** `Lịch meeting` (badge **3**, đang chọn) · `Danh sách meeting` (badge **2**, cam) · `Nhu cầu khách hàng`.
- Nhóm **PHÒNG HỌP:** `Đăng ký phòng họp` · `Tình trạng phòng họp`.
- Nhóm **BÁO CÁO:** `Theo nhân viên / phòng ban` · `Theo dự án` · `Theo khách hàng` (xám, nhãn `Sắp có`) · `Hiệu quả phòng họp` (xám, `Sắp có`).
- **Cuối drawer (cố định):** `Cài đặt` · `Đăng xuất` (đỏ) · `Phiên bản 2.2.4+146`.

### C3. 00j · Thông báo (chuông) — dùng chung các phân hệ
Mô tả (nguyên văn): "Mở từ chuông ở MỌI phân hệ (thay NotificationPage + NewNotificationPage Thành An). Header tông navy chung của app (không theo màu 1 phân hệ). Nút gạt Chưa đọc / Tất cả + chip lọc theo phân hệ (chấm màu nhận diện, số chưa đọc). Gom theo ngày: Hôm nay · Hôm qua · Trước đó. Mỗi dòng tách đúng template thông báo [PREFIX] Nhóm hành động: Tên đối tượng. Ghi chú (skill notification-convention): tag PREFIX màu phân hệ · nhóm hành động tô màu theo nghĩa (Quá hạn đỏ, Đã duyệt xanh lá, Sắp đến hạn/Nhắc hổ phách, Thay đổi lịch tím, Tạo mới xanh dương) · tên đối tượng ĐẬM · ghi chú xám. Chưa đọc: nền xanh nhạt + chấm xanh; bấm = đánh dấu đã đọc + mở deep-link (ID đối tượng). Vuốt trái 1 dòng: Đã đọc / Xoá. "Đọc tất cả" áp theo bộ lọc đang chọn. Prefix DXN/COM/KH/TBNB là đề xuất — cần chốt theo mã đối tượng thật."

Nội dung: header `Thông báo` · `3 thông báo chưa đọc` · `Đọc tất cả`; nút gạt `Tất cả` / `Chưa đọc (3)`; chip `Tất cả 3` · `Meeting 1` · `Công việc 1` · `Chấm công 1` · `Đào tạo`. Nhóm **HÔM NAY**: `MET` Thay đổi lịch · 5 phút · **Thương thảo hợp đồng - Xưởng 3S VinFast** · "Thời gian: 14:00 hôm nay. Phòng 302, Trụ sở Hà Nội." — `TASK` Quá hạn · 1 giờ · Khảo sát hiện trạng kho A · "Hạn: 18/10/2026." — `DXN` Đã duyệt · 2 giờ · Đơn xin nghỉ 21/10 – 22/10 · "Người duyệt: Nguyễn Hữu Học." — `BBH` Sắp đến hạn · 08:00 · **Biên bản MTG.26.0231** · "Còn 6 giờ — quá hạn sẽ tự huỷ cuộc họp." Nhóm **HÔM QUA**: `COM` Nhắc báo cáo · Đăng ký cơm ngày 20/10 · `KH` Tạo mới · An toàn điện cơ bản - Khoá 03/2026 · `TBNB` Tạo mới · Lịch nghỉ lễ Ngày Nhà giáo 20/11.

Prefix liên quan Meeting: `MET` (meeting), `BBH` (biên bản họp).

---

## D. Thư viện component dùng chung

"THƯ VIỆN COMPONENT — 11 thành phần dùng chung — sửa ở đây là lan ra toàn bộ 18 màn." Font toàn bộ: **Inter**. Icon: **lucide**.

| Component | id | Đặc tả |
|---|---|---|
| **C/StatusBar** | `krF2D` | 393×63, gradient 270° `#0B6B80`→`#0E8FA8`, padding 0/16; giờ "16:50" 15/600 trắng; icon signal/wifi/battery 16 trắng, gap 6. |
| **C/Header** | `VvtCd` | 393×48, cùng gradient `#0B6B80`→`#0E8FA8`, padding 0/16, space-between. Trái: `chevron-left` 24 trắng (màn chọn/popup toàn màn dùng `x`; màn gốc tab dùng ☰). Giữa: tiêu đề 17/600 trắng. Phải: action 22 trắng (mặc định `bell`; tuỳ màn là chữ "Lưu"/"Xong"/"Làm mới", `more-vertical` ⋮, `plus`, `user-plus`). |
| **C/Field** | `j3MKD` | Cột gap 6. Nhãn 12/600 `#444444`. Ô 44 cao, nền trắng, bo 8, viền 1 `#D0D0D0` inner, padding 0/12; giá trị/placeholder 14 normal `#999999`; icon phải 18 `chevron-down` `#999999` (ô ngày dùng icon lịch). |
| **C/FieldReq** | `iZueY` | Như C/Field, dòng nhãn có thêm `*` 12/600 `#DC2626` (gap 3). |
| **C/HubRow** | `TCpUV` | 361 rộng, nền trắng, viền dưới 1 `#F0F0F0`, padding 12/16, gap 12. Icon khối 34×34 bo 10 nền `#E6F6F9`, icon 18 `#0E8FA8`. Cột chữ: tên khối 14/600 `#1A1A1A` (+ `*` đỏ nếu bắt buộc), gợi ý 12 `#999999`. Giá trị phải 13/600 (xanh lá `#43A047` = "Đủ"; số đếm xanh ngọc; "Trống" xám; đỏ khi lỗi/"Thiếu"). Chevron-right 18 `#BBBBBB`. |
| **C/PersonRow** | `Vjvkg` | 361, nền trắng, viền dưới `#F0F0F0`, padding 10/14, gap 10. Avatar tròn 36 nền `#EEF2F6` chữ tắt 13/700 `#64748B`. Tên 14/600 `#1A1A1A`; dòng phụ 12 `#666666`. Đuôi phải 12/600 (vd "Chủ trì" `#E8972C`); chevron/× 18 `#BBBBBB`. |
| **C/Chip** | `m1yTWS` | Cao 42, nền trắng, bo 10, viền 1 `#D0D0D0`, padding 0/6, gap 6; chấm `circle` 12 `#BBBBBB`; chữ 12/600 `#666666` (vd "Có mặt"). Dùng cho nút gạt 3 mức điểm danh — trạng thái chọn tô màu: Có mặt xanh lá, Vắng có lý do cam, Vắng không lý do đỏ. |
| **C/TabBar** | `QgxPf` | (Thanh tab cũ của app) 393×60, nền trắng, viền trên `#E0E0E0`; 4 tab Trang chủ · Meeting · Công việc · Cá nhân, icon 20 + nhãn 9/500, chọn `#E8972C`, thường `#9AA3AD`. *Bị thay bằng C/BottomNav.* |
| **C/ViewRow** | `oR43E` | Cặp nhãn–giá trị màn chỉ xem: nhãn 11/600 `#9AA3AD` letter-spacing 0.3; giá trị 14 normal `#1A1A1A` line-height 1.4; gap 3. |
| **C/CustomerCard** | `gupJj` | 361, nền trắng, bo 10, viền 1 `#EAECEF`, padding 12/14, gap 6. Dòng 1: `Mã - Tên KH` 14/600 `#1A1A1A` + chevron 18 `#BBBBBB`. Dòng 2: `Loại · MST …` 12 `#666666`. Dòng 3: icon phone 12 `#9AA3AD` + SĐT 12 `#374151` · icon map-pin + Tỉnh. Dòng 4: địa chỉ 11 `#8A94A0` line-height 1.35. |
| **C/BottomNav** | `TTVFU` | Xem mục C1. |
| **C/Badge** | `Wbg54` | Bo 4, padding 3/8, viền 1 inner; chữ 11/600. Mẫu: nền `#FEF3C7`, viền `#D9770640`, chữ `#B45309` ("Chờ báo cáo"). Màu trạng thái theo bảng 9 màu chuẩn web. |
| **C/BtnPrimary** | `ANcb1` | 48 cao, bo 12, gradient 215° `#2CC3D6`→`#0E8FA8`; icon 16 trắng + chữ 15/600 trắng, gap 8. |
| **C/BtnSecondary** | `U41VZ` | 48 cao, bo 12, nền trắng, viền 1.5 `#D0D0D0`; icon 16 + chữ 15/600 `#444444`. |
| C/ArrowRight · C/ArrowDown | `S67Bnv` · `M8mgMc` | Chỉ là mũi tên chú thích trên canvas (không code). |

**Bottom Bar màn form/chi tiết:** 2 nút ngang nhau — trái [Secondary], phải [Primary]. Màn chỉ xem: 1 nút `Quay lại` [Secondary] full-width.

**Thẻ Hero (đầu Hub):** mã meeting nhỏ xám · badge trạng thái phải · tên meeting đậm 2 dòng · 3 dòng icon: lịch (`08:30 - 10:00 · Thứ 2, 14/09/2026`), map-pin (địa điểm), user-round (`Chủ trì: …`).

**Thanh Mức độ hoàn thiện hồ sơ:** nhãn trái `Mức độ hoàn thiện hồ sơ`, phải `x/3`; track cao 6.

**Khối gập/mở (form Thông tin chung):** thẻ bo góc, tiêu đề có vòng số ①②③ màu khối (① tím, ② xanh dương, ③ xanh lá), dấu ✓ màu khối khi đủ, chevron gập/mở; khi gập hiện 1 dòng tóm tắt; nhãn phải "Chưa nhập" khi chưa có dữ liệu; "n lỗi" đỏ khi có lỗi.

---

## E. Màn hình chi tiết

### 00h · Tổng quan Meeting
- **Mục đích:** "Màn chính của phân hệ Meeting (tab 1 bottom menu). Web /meeting/dashboard hiện chỉ là hub link — app thiết kế mới, số liệu từ dữ liệu meeting sẵn có."
- **Thứ tự khối (user chốt, nguyên văn):** "thẻ meeting SẮP DIỄN RA (trong dải màu đầu) → CẦN XỬ LÝ GẤP (biên bản sắp quá hạn #11014 tự huỷ, chưa nhập biên bản, chưa điểm danh, nháp chưa gửi lịch) → LỊCH HÔM NAY (dòng thời gian, meeting kế tiếp viền màu) → THỐNG KÊ THÁNG (1 dải 4 số: Tổng · Hoàn thành · Chờ biên bản · Đã huỷ — bấm từng số mở Danh sách lọc sẵn) → PHÒNG TRỐNG NGAY BÂY GIỜ. Bottom menu: Tổng quan · Lịch · [Tạo meeting] · Danh sách · Phòng họp (Báo cáo vào drawer). Màu trạng thái theo bảng 9 màu chuẩn web."
- **Header:** ☰ · `Meeting` · chuông.
- **Dải màu đầu (gradient):** `THỨ HAI, 19/10/2026` · `Chào buổi sáng, DNS Admin 👋` · tóm tắt `Hôm nay bạn có 3 cuộc họp` · `1 biên bản sắp quá hạn`.
  - Thẻ **SẮP DIỄN RA** (trắng, nằm trong dải): nhãn `Bắt đầu sau 25 phút` · tiêu đề `[Đấu thầu] Thương thảo hợp đồng…` (tiền tố [Loại meeting]) · `08:30 – 10:00` · `Trực tiếp` · `Phòng 302, Trụ sở Hà Nội` · `CT CP Sản xuất & KD VinFast` · cụm avatar `HH TL MĐ +9` · nút **[Primary] `Vào cuộc họp`**.
- **Cần xử lý gấp** — danh sách dòng có số đếm phải:
  | Dòng | Phụ đề | Số |
  |---|---|---|
  | Biên bản sắp quá hạn | `MTG.26.0231 · còn 6 giờ — quá hạn sẽ tự huỷ` | 1 |
  | Chưa nhập biên bản | Đã họp xong, chưa có nội dung trao đổi | 3 |
  | Chưa điểm danh | Meeting đã chốt lịch hôm qua | 2 |
  | Nháp chưa gửi lịch hẹn | Lưu nháp > 2 ngày | 2 |
- **Lịch hôm nay** + link `Xem lịch tuần`: dòng thời gian, mỗi dòng giờ bắt đầu/kết thúc · tên · địa điểm · hình thức · badge trạng thái: `08:30–10:00 Thương thảo hợp đồng - Xưởng 3S VinFast · Phòng 302 · Trực tiếp · Đã chốt lịch` (meeting kế tiếp viền màu) · `13:30–14:30 Khảo sát nhu cầu trạm sạc - EVN HN · Google Meet · Online · Đã chốt lịch` · `16:00–17:00 Họp nội bộ phòng KD1 tuần 43 · Phòng 205 · Lưu nháp`.
- **Thống kê tháng 10/2026** + link `Xem báo cáo`: 4 số `24 Tổng` · `15 Hoàn thành` · `4 Chờ biên bản` · `2 Đã huỷ` (bấm → Danh sách lọc sẵn).
- **Phòng họp trống ngay bây giờ** + link `Đặt phòng`: thẻ cuộn ngang `Trống · Phòng 201 · 8 chỗ · đến 10:00` · `Phòng 305 · 12 chỗ · cả sáng` · `Phòng 402 · 20 chỗ · đến 9:30`.
- **Bottom nav:** Tổng quan (chọn) · Lịch · [Tạo meeting] · Danh sách · Phòng họp.

### 00h' · Tổng quan Meeting (trống)
- Nguyên văn: "Trạng thái của 00h khi KHÔNG có cuộc họp sắp diễn ra: ẨN HẲN khối thẻ meeting sắp diễn ra (user chốt 19/10), dải màu đầu chỉ còn lời chào + tóm tắt ngày. Lịch hôm nay thu thành 1 dòng trống. Cần xử lý gấp / Thống kê / Phòng trống giữ như 00h. Tạo meeting qua nút giữa bottom menu."
- Tóm tắt dải đầu: `Hôm nay bạn không có cuộc họp nào` · `1 biên bản sắp quá hạn`. Lịch hôm nay: `Không có cuộc họp nào hôm nay`.

---

### 01 · Lịch meeting
- **Mục đích:** "Điểm vào. Tab cấp 1: Tôi chủ trì / Tôi tham gia — app chỉ quản lý meeting của chính mình. 3 chip vừa là số liệu vừa là lọc nhanh, bấm để lọc, bấm lại để bỏ."
- **Header:** ☰ (mở drawer 00d) · `Meeting` · chuông.
- **Thanh tìm kiếm:** ô `Tìm theo mã / tên meeting` + nút vuông 38×38 icon bộ lọc ⚙ (→ màn 02).
- **Tab cấp 1:** `Tôi chủ trì` (chọn, gạch chân) · `Tôi tham gia`.
- **3 chip số liệu/lọc nhanh** (ô bo góc, số to + nhãn): `12 Đã hoàn thành` (xanh lá) · `5 Sắp diễn ra` (xanh dương) · `3 Chờ biên bản` (cam).
- **Thẻ meeting** (mỗi thẻ): mã (`MTG.26.0245`) + badge trạng thái phải · tên (đậm, 2 dòng) · dòng giờ + ngày (`08:30 - 10:00 · Hôm nay 14/09`) · dòng địa điểm (`Phòng 302, Trụ sở Hà Nội` / `Online · Google Meet` / `Chưa chọn địa điểm`) · các tag nhỏ: tình trạng biên bản (`Chưa có biên bản` cam / `Đã có biên bản` xanh) · điểm danh (`12/15 có mặt`) · với nháp: `Chưa gửi lịch`. Meeting nháp chỉ có giờ bắt đầu (`15:00 · 12/09/2026`).
  - Mẫu: `MTG.26.0245 Đã chốt lịch` · `MTG.26.0244 Đã chốt lịch (Online · Google Meet)` · `MTG.26.0243 Đã hoàn thành · Đã có biên bản · 15/15 có mặt` · `MTG.26.0242 Lưu nháp · Chưa chọn địa điểm · Chưa gửi lịch`.
- **Bottom nav:** Tổng quan · **Lịch** (chọn) · [Tạo meeting] · Danh sách · Phòng họp.

> **CHỐT CHO DEV — PHẠM VI DỮ LIỆU & 2 TAB** (nguyên văn)
> - App CHỈ quản lý meeting của chính mình → KHÔNG dùng MeetingCriteria của màn danh sách web (lọc theo quyền tổng công ty / công ty / phòng ban / bộ phận). Dùng MeetingCalendarCriteria — đã có sẵn, đang phục vụ tab Lịch của /assign/my-todo.
> - Vì sao không tái dùng MeetingCriteria: criteria AND với nhau, khối phạm vi theo quyền nằm cứng bên trong nên AND thêm điều kiện "liên quan tới tôi" vẫn không cứu được người chủ trì nằm ngoài phạm vi quyền (false AND true = false). Comment trong chính file đã ghi rõ, kèm số đo: 49 meeting lên lịch thì 37 cái không liên quan người xem.
> - MeetingCalendarCriteria chỉ có ĐÚNG 1 điều kiện: user có tên trong Thành phần — Phía Công ty (meeting_employees.type = 1). KHÔNG xét host_employee_id vì MeetingService::ensureHostIsCompanyMember() đã tự đưa người chủ trì vào Thành phần ở MỌI lượt lưu. KHÔNG xét created_by vì thư ký nhập hộ không phải người dự.
> - 2 TAB LẤY ĐÚNG VAI TRÒ, RỜI NHAU (chốt 16/09). Tôi chủ trì = host_employee_id = auth()->id(). Tôi tham gia = có trong meeting_employees type=1 VÀ host_employee_id <> auth()->id(). Lý do phải loại trừ: chủ trì LUÔN nằm trong thành phần (ensureHostIsCompanyMember tự thêm ở mọi lượt lưu), lấy nguyên meeting_employees thì meeting mình chủ trì đếm ở cả 2 tab. Tách vai trò thì tổng 2 tab = tổng meeting của tôi, không trùng.
> - Meeting trạng thái Đang tạo (nháp) chỉ NGƯỜI TẠO thấy — luật này giữ nguyên, nhớ áp cả vào số đếm của 3 chip.
> - 3 chip vừa là số liệu vừa là lọc nhanh: bấm để lọc, bấm lại để bỏ; số đếm tính trong phạm vi tab đang chọn. Bản vẽ đang ở trạng thái chưa bấm chip nào (xem tất cả).

### 02 · Bộ lọc
- **Mục đích:** "8 tiêu chí lọc — KHÔNG có Công ty / Phòng ban vì app chỉ xem meeting mình chủ trì hoặc tham gia. Nút Áp dụng đếm sẵn số bộ lọc đang bật." (Vào từ nút ⚙ màn 01.) *Ghi chú: artboard tổng quan ghi "10 tiêu chí", màn vẽ thực tế 8 trường.*
- **Header:** `x` · `Bộ lọc` · chữ `Làm mới` (phải).
- **Trường** (đều là select dạng C/Field, ô đang có giá trị viền xanh ngọc):
  | Nhãn | Kiểu | Placeholder / giá trị mẫu |
  |---|---|---|
  | Loại meeting | chọn | `Chọn loại meeting` |
  | Hình thức | chọn | `Chọn hình thức` |
  | Trạng thái | chọn | `Đã chốt lịch` (đang bật) |
  | Khách hàng | chọn | `Chọn khách hàng` |
  | Dự án TKT | chọn | `Chọn dự án` |
  | Có biên bản? | chọn | `Chưa lập biên bản` (đang bật) |
  | Ngày họp từ | ngày (2 cột) | `01/09/2026` |
  | Ngày họp đến | ngày | `30/09/2026` |
- **Bottom bar:** [Secondary] `Làm mới` (icon xoay) · [Primary] `Áp dụng (2)` (số = số bộ lọc đang bật).

---

### 03 · Tạo meeting
- **Mục đích (nguyên văn):** "Theo web (19/10, Phase 4): 3 khối + Tài liệu — ① Thông tin cuộc họp (Phân loại · Loại meeting * · Tên * · Mục tiêu/Nội dung) → ② Đối tác (Khách hàng * · Người liên hệ · Dự án TKT * / Hợp đồng *) → ③ Thời gian, địa điểm & chủ trì. App GẬP/MỞ từng khối cho vừa 1 màn hình: mở màn tạo thì ① mở sẵn; khối đủ thì gập thành 1 dòng tóm tắt (✓ màu khối), bấm tiêu đề để mở lại. Tên đứng TRƯỚC Đối tác nên "Gợi ý tên" (ghép [Loại] Dự án/HĐ – KH) dùng sau khi chọn Đối tác. Trường CHỌN = dòng nhãn trái – giá trị phải, trường GÕ giữ ô nhập. Họp Nội bộ → ẩn ②, ③ thành ②. Đối tượng bắt buộc cả khi Lưu nháp."
- Vào từ: nút + / FAB "Tạo meeting" / CTA drawer. Lưu xong → Hub 04a (Lưu nháp).
- **Header:** ‹ · `Tạo meeting`.
- **Khối ① Thông tin cuộc họp** (mở sẵn, vòng số tím):
  | Nhãn | Kiểu | * | Giá trị/placeholder |
  |---|---|---|---|
  | Phân loại họp | segmented 2 nút (icon) | — | `Đối tác` (chọn) / `Nội bộ` |
  | Loại meeting | dòng chọn (nhãn trái – giá trị phải) | * | `Đấu thầu` |
  | Tên cuộc họp | ô gõ nhiều dòng + chip nút `Gợi ý tên` (✨) ở dòng nhãn | * | `Nhập tên, hoặc chọn Đối tác rồi bấm Gợi ý tên` |
  | Mục tiêu / Nội dung | ô gõ nhiều dòng | — | `Mục tiêu, nội dung chính cần trao đổi` |
- **Khối ② Đối tác** (gập, nhãn phải `Chưa nhập`, tóm tắt `Khách hàng, người liên hệ, dự án TKT / hợp đồng`). Khi mở:
  | Nhãn | Kiểu | * | Placeholder |
  |---|---|---|---|
  | Khách hàng | dòng chọn → màn 41 | * | `Chọn khách hàng` |
  | Người liên hệ | dòng chọn → sheet 43 (khoá khi chưa có KH) | — | `Chọn khách hàng trước` |
  | Dự án TKT (loại meeting theo đối tượng Dự án TKT) / Hợp đồng (loại theo đối tượng Hợp đồng) | dòng chọn → 48 / 49 (khoá khi chưa có KH — riêng Hợp đồng chọn được trước, xem 49) | * | `Chọn khách hàng trước` |
- **Khối ③ Thời gian, địa điểm & chủ trì** (gập, `Chưa nhập`, tóm tắt `Thời gian, chủ trì, hình thức, địa điểm`). Khi mở:
  | Nhãn | Kiểu | * | Mẫu |
  |---|---|---|---|
  | Bắt đầu | ngày giờ | * | `14/09/2026 08:30` |
  | Kết thúc | ngày giờ | * | `14/09/2026 10:00` |
  | Người chủ trì | dòng chọn → màn 14 | * | `Nguyễn Hữu Học - Phó TGĐ` |
  | Hình thức | segmented | — | `Trực tiếp` / `Online` |
  | Địa điểm meeting | ô gõ + nút `Chọn địa điểm từ bản đồ` (→ 20) | * (khi Trực tiếp) | `Phòng 302, Trụ sở Hà Nội` |
  | Link họp (nếu Online) | ô gõ | — | (xem 28) |
- **Bottom bar:** [Secondary] `Lưu nháp` · [Primary] `Tạo meeting` (icon mũi tên).

### 04a · Hub — Lưu nháp
- **Mục đích:** "Bảng điều khiển của cuộc họp, trạng thái Lưu nháp. Dấu * đỏ = khối bắt buộc NGAY Ở TRẠNG THÁI NÀY — ở đây chỉ Thông tin chung + Nhân sự tham gia. Thanh Mức độ hoàn thiện đếm theo bộ khối cần cho Hoàn thành (x/3)."
- **Header:** ‹ · `Chi tiết meeting` · ⋮ (menu 22).
- **Hero:** `MTG.26.0245` + badge `Lưu nháp` · tên · `08:30 - 10:00 · Thứ 2, 14/09/2026` · `Phòng 302, Trụ sở Hà Nội` · `Chủ trì: Nguyễn Hữu Học - Phó TGĐ`.
- **Mức độ hoàn thiện hồ sơ:** `1/3`.
- **Danh sách khối (C/HubRow)** — tên · gợi ý · giá trị phải:
  | Khối | * | Gợi ý | Giá trị | Đi tới |
  |---|---|---|---|---|
  | Thông tin chung | * | `Đấu thầu · Trực tiếp · 90 phút` | `Đủ` (xanh) | 05 |
  | Dự án TKT (chỉ hiện khi đã gắn dự án) | — | `DA.26.018 · DA.26.031 · phiếu 3/4 câu` | `2` | 06 |
  | Nhân sự tham gia | * | `8 công ty · 4 khách hàng` | `12` | 07 |
  | Tài liệu chuẩn bị | — | `Tài liệu gửi kèm trước buổi họp` | `0` | 19 |
  | Biên bản cuộc họp | (ẩn * ở trạng thái này) | `Chưa nhập nội dung trao đổi, kết luận` | `Trống` | 09 |
  | Tài liệu biên bản | — | `Chưa có tệp nào` | `0` | 11 |
  | Khảo sát nhu cầu KH | — | `Chỉ với loại Họp tìm hiểu & Giới thiệu sản phẩm` | `Trống` | 12 |
- **Bottom bar:** [Secondary] `Lưu nháp` · [Primary] `Lên lịch hẹn` (icon gửi) → chuyển Đã chốt lịch (04b).

> **CHỐT CHO DEV — DẤU * THEO TRẠNG THÁI** (nguyên văn)
> - Dấu * trên Hub = khối bắt buộc để LƯU ĐƯỢC Ở TRẠNG THÁI HIỆN TẠI của màn, không phải bộ khối cần cho Hoàn thành.
> - Bắt buộc ở MỌI lượt lưu, kể cả Lưu nháp — MeetingCreateApiRequest / MeetingUpdateApiRequest: name, meeting_type_id, start_date, end_date, host_employee_id đều required; location required_if mode_id=1; company_members required|array. BE KHÔNG nới rule khi status=0, nên Lưu nháp vẫn phải có Thông tin chung + Thành phần.
> - Chỉ bắt buộc khi HOÀN THÀNH (status=3): conclusion = required_if:status,3 · Biên bản qua guard FE hasMeetingReport() · Điểm danh (trong Nhân sự tham gia) qua guard FE isAllAttended() · Khảo sát nhu cầu KH (has_investment_demand, has_maintenance_demand) = required_if:status,3 NHƯNG chỉ khi loại meeting có mã CODE_PRODUCT_INTRO.
> - KHÔNG bao giờ bắt buộc: Dự án TKT (trừ loại meeting theo đối tượng Dự án TKT — khi đó ≥1 dự án, kể cả Lưu nháp; dòng Hub chỉ hiện khi meeting đã gắn dự án) · Tài liệu chuẩn bị · Tài liệu biên bản (đều nullable).
> - Riêng dòng biên bản đã nhập thì có required cấp dòng: reports.*.content, reports.*.executor_name, reports.*.expected_deadline — áp mọi trạng thái, không chờ tới Hoàn thành.
> - Vì vậy dấu * theo màn: 04a Lưu nháp · 04b Đã chốt lịch · 24 Hub có lỗi · 16/22/23 (nền popup) = CHỈ Thông tin chung + Nhân sự tham gia. 04c Đã hoàn thành và 46 Hub chặn Hoàn thành = đủ 3 khối (Thông tin chung · Nhân sự tham gia · Biên bản cuộc họp). 26 Đã huỷ và 27 Chỉ xem = KHÔNG có dấu * vì không sửa được nữa.
> - Thanh Mức độ hoàn thiện hồ sơ đếm x/3 theo bộ khối cần cho HOÀN THÀNH (4 nếu loại meeting có Khảo sát) — cố ý khác dấu *, vì nó trả lời câu "còn bao xa tới Hoàn thành". Kết luận nằm TRONG Biên bản (như tab Biên bản bản web) nên Biên bản chỉ tính đủ khi có ≥1 nội dung trao đổi VÀ đã nhập kết luận.

### 04b · Hub — Đã chốt lịch
- **Mục đích:** "Sau khi Gửi lịch hẹn. Đây là lúc cột điểm danh trong Nhân sự tham gia mở. Lưu ở trạng thái này vẫn chỉ bắt buộc Thông tin chung + Nhân sự tham gia; Biên bản (gồm cả Kết luận) chỉ bắt buộc khi bấm Hoàn thành."
- Header/Hero như 04a, badge `Đã chốt lịch`. Mức độ hoàn thiện `2/3`.
- Khối: Thông tin chung * `Đấu thầu · Trực tiếp · 90 phút` `Đủ` · Dự án TKT `DA.26.018 · DA.26.031 · phiếu 3/4 câu` `2` · Nhân sự tham gia * `8 công ty · 4 KH · điểm danh 12/15` `12/15` · Tài liệu chuẩn bị `2 tệp · gửi kèm trước buổi họp` `2` · Biên bản cuộc họp `Chưa nhập nội dung trao đổi, kết luận` `Trống` · Tài liệu biên bản `3 tệp · 4,2 MB` `3` · Khảo sát nhu cầu KH `Trống`.
- **Bottom bar:** [Secondary] `Lưu` · [Primary] `Hoàn thành`.

### 04c · Hub — Đã hoàn thành
- **Mục đích:** "Đã Hoàn thành nên đủ cả 3 khối bắt buộc — dấu * hiện ở đủ 3. Kết luận nằm trong Biên bản nên dòng Biên bản ghi luôn "có kết luận". Chuyển sang xem và chia sẻ biên bản."
- Badge `Đã hoàn thành`; Mức độ hoàn thiện `3/3`.
- Khối: Thông tin chung * `Đủ` · Dự án TKT `2` · Nhân sự tham gia * `8 công ty · 4 KH · điểm danh đủ 15/15` `15/15` · Tài liệu chuẩn bị `2` · Biên bản cuộc họp * `6 nội dung · 4 việc cần làm · có kết luận` `6` · Tài liệu biên bản `5 tệp · 8,1 MB` `5` · Khảo sát nhu cầu KH `Đủ`.
- Bấm khối → bộ màn chỉ xem (33/34/32/36/37/38/39). Mũi tên "↓ Bấm Xem biên bản" → 15.
- **Bottom bar:** chỉ [Secondary] `Quay lại`.

---

### 05 · Thông tin chung (sửa)
- **Mục đích (nguyên văn):** "Mở màn sửa: 3 khối đều GẬP, mỗi khối 1 dòng tóm tắt — thấy toàn bộ meeting trong 1 màn hình, bấm khối nào mở khối đó. ① Thông tin cuộc họp tóm tắt Phân loại · Loại · Tên. Ví dụ loại meeting theo Hợp đồng: ② Đối tác mở ra có Khách hàng + thẻ thông tin KH + Lịch sử meeting, Người liên hệ, Hợp đồng * (màn 49). Đổi KH / đổi loại meeting thì bỏ hợp đồng đã chọn."
- **Header:** ‹ · `Thông tin chung` · chữ `Lưu`.
- **Trạng thái gập (mặc định):**
  - ① Thông tin cuộc họp ✓ — `Đối tác · Thương thảo HĐ · Thương thảo hợp đồng và chốt phương án cung cấp - Xưởng 3S VinFast`
  - ② Đối tác ✓ — `VinFast · Trần Minh Đức · HĐ_TPE_KD1_26_0112`
  - ③ Thời gian, địa điểm & chủ trì ✓ — `T2 14/09 · 08:30 – 10:00 · Nguyễn Hữu Học · Trực tiếp · Phòng 302, Trụ sở Hà Nội`
- **Khi mở:**
  - ①: Phân loại họp (segmented `Đối tác`/`Nội bộ`) · Loại meeting * (dòng chọn, `Thương thảo HĐ`) · Tên cuộc họp * + `Gợi ý tên` · Mục tiêu / Nội dung.
  - ②: Khách hàng * (`CT CP Sản xuất & KD VinFast`) + thẻ thông tin KH (`Mã KH KH.26.0187` · `MST 0106 999 888` · `SĐT 024 3939 8888` · `Địa chỉ Lô 5, KCN Bắc Thăng Long, Đông Anh, Hà Nội`) + 2 nút nhỏ `Lịch sử meeting` (→ 21) · `Thêm nhanh KH` (→ 42) · Người liên hệ (dòng chọn `Trần Minh Đức - TP Mua hàng`, nút `Thêm nhanh` → 44) · Hợp đồng * (thẻ: `HĐ_TPE_KD1_26_0112` · `CT CP Sản xuất & KD VinFast` · badge `Có hiệu lực`).
  - ③: Bắt đầu * · Kết thúc * · Người chủ trì * · Hình thức (segmented) · Địa điểm meeting * + `Chọn địa điểm từ bản đồ`.
- **Bottom bar:** [Secondary] `Huỷ` (icon x) · [Primary] `Lưu` (icon save).

### 25 · Thông tin chung — lỗi validate
- **Mục đích (nguyên văn):** "Bấm Lưu khi thiếu trường bắt buộc: MỌI lỗi báo cùng lúc. Khối có lỗi tự MỞ và tô đỏ ô lỗi + chữ đỏ dưới ô (① thiếu Tên, ② thiếu KH + Dự án TKT); khối ③ ở ví dụ vẫn gập nhưng tiêu đề ghi "1 lỗi", dòng tóm tắt đỏ nói thiếu gì. Chưa chọn KH thì Người liên hệ / Dự án TKT khoá nhưng Dự án TKT vẫn báo bắt buộc."
- **Dải ĐỎ dưới header:** `Còn 4 lỗi. Khối có lỗi đã tự mở, khối gập ghi số lỗi trên tiêu đề; đã cuộn tới ô lỗi đầu tiên.`
- ① `1 lỗi` (mở): Tên cuộc họp * trống → `Tên cuộc họp không được để trống`. Mục tiêu có giá trị mẫu `Thương thảo điều khoản giao hàng, chốt phương án cung cấp và tiến độ bàn giao trạm sạc số 2.`
- ② `2 lỗi` (mở): Khách hàng * → `Vui lòng chọn Khách hàng` · Người liên hệ (khoá, `Chọn khách hàng trước`) · Dự án TKT * (khoá) → `Vui lòng chọn Dự án TKT.`
- ③ `1 lỗi` (gập): tóm tắt đỏ `Chưa chọn Người chủ trì` · `T2 14/09 · 08:30 – 10:00 · Phòng 302`. (Khi mở: Người chủ trì * `Chọn Người chủ trì` → `Vui lòng chọn Người chủ trì`.)
- Bottom bar: `Huỷ` · `Lưu`.

### 28 · Thông tin chung — họp Online
- **Mục đích (nguyên văn):** "Hình thức = Online: hiện ô Link họp, Địa điểm thành không bắt buộc. Ví dụ khối ③ đang mở (① ② gập, ✓): Bắt đầu / Kết thúc / Chủ trì là dòng chọn, Hình thức nút gạt, Link họp ô gõ, Địa điểm dòng chọn có icon bản đồ (thay nút "Chọn địa điểm từ bản đồ")."
- ① gập: `Đối tác · Đấu thầu · Thương thảo hợp đồng…` · ② gập: `VinFast · Trần Minh Đức`.
- ③ mở: Bắt đầu * `14/09/2026 08:30` · Kết thúc * `14/09/2026 10:00` · Người chủ trì * `Nguyễn Hữu Học - Phó TGĐ` · Hình thức `Online` (chọn) · **Link họp (nếu Online)** ô gõ `https://meet.google.com/abc-defg-hij` · **Địa điểm** (không *) dòng chọn + icon bản đồ, placeholder `Không bắt buộc khi Online`.
- Bottom bar: `Huỷ` · `Lưu`.

### 45 · Cảnh báo chưa lưu khi Quay lại
- **Mục đích:** "Bấm Quay lại (hoặc ‹ trên header) ở BẤT KỲ màn form nào khi còn thay đổi chưa lưu. Không còn thay đổi thì thoát thẳng, không hỏi."
- Nền: màn Thông tin chung (bản cũ, chưa chia khối) mờ.
- **Popup:** tiêu đề `Thông tin chưa được lưu` · nội dung `Bạn đã sửa màn Thông tin chung nhưng chưa lưu. Quay lại bây giờ sẽ mất các thay đổi.` · 3 nút dọc: [Primary] `Lưu và quay lại` · `Quay lại, không lưu` · `Ở lại màn này`.

### 20 · Chọn địa điểm từ bản đồ
- **Mục đích:** "Mở từ nút Chọn địa điểm ở màn Tạo meeting / Thông tin chung."
- **Header:** `Chọn địa điểm` · chữ `Xong`.
- Nút gạt nguồn bản đồ: `Google Map` / `OpenStreetMap`. Ô tìm `Tìm địa chỉ, toà nhà, khu công nghiệp...`. Vùng bản đồ có ghim.
- Thẻ **ĐỊA ĐIỂM ĐÃ CHỌN:** `Phòng 302, Trụ sở Hà Nội` · `168 Nguyễn Xiển, Thanh Xuân, Hà Nội` · toạ độ `20.9876, 105.7965`.
- Bottom bar: [Secondary] `Huỷ` · [Primary] `Chọn địa điểm này`.

### 21 · Lịch sử meeting khách hàng
- **Mục đích:** "Mở từ nút Lịch sử meeting cạnh ô Khách hàng. Timeline mới → cũ: NGÀY – GIỜ là mốc trên trục, thẻ bên dưới chở mã, trạng thái, tên, người chủ trì, biên bản / lý do huỷ."
- **Header:** `Lịch sử meeting`. Đầu màn: `CT CP Sản xuất & KD VinFast` · `4 cuộc họp bạn tham gia`.
- Mốc timeline (mỗi mốc: `Thứ x, dd/mm/yyyy · hh:mm - hh:mm`, thẻ: mã + badge trạng thái · tên · `Chủ trì: …` · dòng cuối):
  1. `Thứ 2, 14/09/2026 · 08:30 - 10:00` — `MTG.26.0245` Đã chốt lịch — Thương thảo hợp đồng… — Nguyễn Hữu Học - Phó TGĐ — `Chưa lập biên bản`
  2. `Thứ 5, 28/08/2026 · 14:00 - 15:30` — `MTG.26.0198` Đã hoàn thành — Rà soát tiến độ lắp đặt trạm sạc số 1 — Trần Thị Lan - TP Kinh doanh — link `Xem biên bản`
  3. `Thứ 6, 02/08/2026 · 09:00 - 11:00` — `MTG.26.0154` Đã hoàn thành — Khảo sát mặt bằng KCN Bình Dương — Phạm Văn Vinh - Kỹ sư trưởng — `Xem biên bản`
  4. `Thứ 3, 15/07/2026 · 15:00 - 16:00` — `MTG.26.0121` Huỷ — Giới thiệu giải pháp giám sát năng lượng — Lê Minh Anh - CV Đấu thầu — `Lý do huỷ: Khách hàng dời lịch sang quý sau`
- Bottom bar: `Quay lại`.

> **LƯU Ý CHO DEV — PHẠM VI DỮ LIỆU** (nguyên văn)
> - Chỉ liệt kê meeting mà USER ĐANG ĐĂNG NHẬP là người chủ trì HOẶC có tên trong thành phần tham dự (bảng meeting_employees).
> - BE hiện tại CHƯA đúng luật này. MeetingController::customerMeetingHistory() — MeetingController.php:978 — đang lọc me.employee_id = m.created_by, tức NGƯỜI TẠO meeting có nằm trong thành phần của chính meeting đó hay không. Đó là thuộc tính của bản ghi, không liên quan người đang mở popup → mọi user đều thấy danh sách y hệt nhau. Route /customer-history cũng không gắn checkPermission và trong hàm không có auth() nào.
> - Sửa theo khuôn đã có: PotentialCustomerCareService::applyPermissionFilter() — PotentialCustomerCareService.php:143
> ```php
> $userId = auth()->id();
> $query->where(function ($q) use ($userId) {
>     $q->where('m.host_employee_id', $userId)
>       ->orWhereExists(function ($s) use ($userId) {
>           $s->selectRaw(1)
>             ->from('meeting_employees as me')
>             ->whereColumn('me.meeting_id','m.id')
>             ->where('me.employee_id', $userId);
>       });
> ```
> - Cần chốt khi làm: THAY điều kiện created_by cũ, KHÔNG cộng thêm — cộng thêm sẽ hẹp gấp đôi.
> - Hệ quả: danh sách rỗng là tình huống thật (nhân viên mới, hoặc khách hàng do người khác phụ trách). Chưa vẽ artboard trạng thái rỗng.

### 41 · Chọn khách hàng
- **Mục đích:** "Mở từ ô Khách hàng ở màn 03 / 05. Bấm thẻ là chọn xong và quay lại form."
- **Header:** `Chọn khách hàng`.
- Ô tìm `Tìm theo tên, mã khách hàng` · 2 ô lọc thêm: `Mã số thuế` (`Nhập mã số thuế`) · `Số điện thoại` (`Nhập số điện thoại`).
- `KẾT QUẢ · 12 KHÁCH HÀNG` — danh sách **C/CustomerCard**: `KH.26.0187 - CT CP Sản xuất & KD VinFast · Doanh nghiệp · MST 0106 999 888 · 024 3939 8888 · Hà Nội · Lô 5…` · `KH.25.0042 - CT TNHH Thiết bị điện Hoàng Gia` · `KH.25.0309 - CT CP Xây lắp điện Miền Bắc` (Hải Phòng) · `KH.24.0765 - Nguyễn Thị Lan Anh · Cá nhân · MST —` (Bắc Ninh).
- Bottom bar: [Secondary] `Huỷ` · [Primary] `Thêm nhanh KH` (→ 42).

### 41b · Không tìm thấy khách hàng
- **Mục đích:** "Lọc không ra kết quả. Lối thoát duy nhất là tạo nhanh khách hàng ngay tại đây."
- Ô tìm có `vinfat`. Trạng thái rỗng: `Không tìm thấy khách hàng phù hợp` · `Thử bỏ bớt bộ lọc, hoặc tạo nhanh khách hàng mới rồi quay lại form meeting.` · nút `Xoá lọc`.
- Bottom bar: `Huỷ` · [Primary] `Thêm nhanh KH`.

### 42 · Thêm nhanh khách hàng
- **Mục đích:** "Bản rút gọn của form tạo khách hàng trên web — chỉ giữ trường bắt buộc, phần còn lại (MST, email, lĩnh vực, nhóm KH…) bổ sung sau trên web. Lưu xong tự chọn luôn vào meeting."
- **Header:** `Thêm nhanh KH`.
- Nhóm **THÔNG TIN KHÁCH HÀNG:** Tên khách hàng * (gõ, `Nhập tên khách hàng`) · Loại hình tổ chức * (chọn, `Công ty cổ phần`) · Tên đơn vị * (gõ, `Nhập tên đơn vị`) · Số điện thoại * (gõ, `Nhập số điện thoại`).
- Nhóm **ĐỊA CHỈ:** Quốc gia * (chọn, `Việt Nam`) · Tỉnh/Thành phố * (`Chọn tỉnh/TP`) · Quận/Huyện * (`Chọn quận/huyện`) · Phường/Xã * (`Chọn phường/xã`).
- Nhóm **ĐỊA CHỈ XUẤT HOÁ ĐƠN:** toggle/checkbox `Giống địa chỉ ở trên` · Địa chỉ xuất hoá đơn * (`Lô 5, KCN Bắc Thăng Long, Đông Anh, Hà Nội`).
- Nhóm **NGƯỜI LIÊN HỆ ĐẦU TIÊN:** Họ tên * · Chức vụ * · Số điện thoại *.
- Bottom bar: `Huỷ` · [Primary] `Lưu & chọn`.

### 43 · Chọn người liên hệ (bottom sheet)
- **Mục đích:** "Bottom sheet — danh sách liên hệ của khách hàng đã chọn, thường chỉ 3-8 người nên không cần đẩy sang màn riêng."
- Sheet: tiêu đề `Chọn người liên hệ` · ô tìm `Tìm theo họ tên hoặc số điện thoại` · danh sách (avatar · tên · chức vụ · SĐT): `Trần Minh Đức · TP Mua hàng · 0912 888 777` (nhãn `Đang chọn`) · `Nguyễn Thu Hà · Chuyên viên Kỹ thuật · 0987 112 334` · `Lê Quang Vinh · Phó GĐ Nhà máy · 0903 556 118` · `Phạm Minh Tuấn · Kế toán trưởng · 0944 220 907` · nút cuối `Thêm nhanh người liên hệ` (→ 44).

### 44 · Thêm nhanh người liên hệ (popup)
- **Mục đích:** "Đúng 3 ô bắt buộc như trên web. Lưu xong liên hệ mới được chọn luôn và thêm vào thành phần khách hàng."
- Popup `Thêm nhanh người liên hệ`: Họ tên * (`VD: Nguyễn Văn A`) · Chức vụ * (`VD: Trưởng phòng CNTT`) · Số điện thoại * (`VD: 0912 345 678`). Nút `Huỷ` · [Primary] `Lưu & chọn`.

### 48 · Chọn dự án TKT
- **Mục đích (nguyên văn):** "Mở từ ô Dự án TKT ở màn 03 / 05 (loại meeting theo đối tượng Dự án TKT). Chỉ mở được SAU KHI đã chọn Khách hàng — danh sách luôn lọc theo khách hàng của meeting (web 15/10). Chọn NHIỀU dự án; tìm + phân trang ở máy chủ. Không có "Thêm nhanh dự án" — web đã bỏ tạo dự án từ meeting (chốt 19/10)."
- Ô tìm `Tìm theo mã, tên dự án` · thẻ XANH `Chỉ hiện dự án của khách hàng CT CP Sản xuất & KD VinFast`.
- **ĐÃ CHỌN · 2** (chip có thể bỏ): `DA.26.018 Trạm sạc xe điện KCN Bình Dương - GĐ 1` · `DA.26.031 Hệ thống giám sát năng lượng Xưởng 3S`.
- **KẾT QUẢ · 8 DỰ ÁN** — mỗi thẻ: checkbox · mã · badge giai đoạn · tên · `Mã KH · Tên KH`: `DA.26.031 Đang làm giải pháp` · `DA.26.018 Thu thập thông tin dự án` · `DA.26.012 Thương thảo giá` (Mở rộng trạm biến áp 1000kVA nhà máy Hải Phòng) · `DA.25.044 Thực hiện hợp đồng` (Cải tạo hệ thống chiếu sáng LED khu văn phòng). Cuối: `Cuộn để tải thêm`.
- Bottom: [Primary] `Xác nhận (2)`.

### 49 · Chọn hợp đồng
- **Mục đích (nguyên văn):** "Mở từ ô Hợp đồng ở màn 03 / 05 (loại meeting theo đối tượng Hợp đồng). Chọn MỘT, bấm thẻ là chọn xong. Chưa có khách hàng → chọn hợp đồng tự điền Khách hàng + tên Người liên hệ; đã có khách hàng → chỉ hiện hợp đồng của khách hàng đó. Không hiện giá trị hợp đồng."
- Ô tìm `Tìm theo mã hợp đồng, khách hàng`. `KẾT QUẢ · 24 HỢP ĐỒNG` — mỗi thẻ: mã HĐ · badge trạng thái · `Mã KH · Tên KH` · `Liên hệ: …`: `HĐ_TPE_KD1_26_0112 Có hiệu lực` · `HĐ_TPE_KD2_26_0098 Chờ duyệt` · `HĐ_TPE_KD1_26_0071 Đang xuất hàng` · `HĐ_TPE_KD1_25_0233 Đã quyết toán`. Cuối `Cuộn để tải thêm`. (Không có bottom bar.)

---

### 06 · Dự án TKT — Thông tin chung
- **Mục đích (nguyên văn):** "Theo web 14–15/10: dòng Hub "Dự án TKT" CHỈ hiện khi meeting đã gắn dự án; màn này CHỈ XEM thông tin dự án (đổi dự án ở ô Dự án TKT — màn 05/48). Gắn nhiều dự án → chip chọn dự án ở đầu màn. Nút gạt "Thông tin chung / Phiếu thu thập thông tin" (phiếu vẫn nhập — màn 06b). Thẻ tóm tắt chỉ các trường chính; không có "Xem chi tiết" (app chưa có phân hệ Dự án — chốt 19/10). Đã bỏ chọn Giải pháp / Hạng mục (chốt 14/10)."
- **Header:** ‹ · `Dự án TKT` (action "Lưu" ẩn — trong suốt).
- Thẻ XANH: `Chỉ xem thông tin dự án. Đổi dự án ở ô Dự án TKT của Thông tin chung.`
- Chip dự án: `DA.26.018` (chọn) · `DA.26.031`. Nút gạt: `Thông tin chung` (chọn) / `Phiếu thu thập thông tin`.
- Thẻ **Thông tin dự án:** `DA.26.018` + badge `Thu thập thông tin` · tên `Trạm sạc xe điện KCN Bình Dương - Giai đoạn 1` · lưới 2 cột nhãn–giá trị: Ứng dụng `Trạm sạc EV` · Nhóm ngành `Năng lượng` · NV KD chính `Lê Văn Nam - HN_KD1 - 11010057` · Quy mô `Lớn` · Phân loại đầu tư `Đầu tư mới` · Cách triển khai `EPC trọn gói` · Địa điểm `Bình Dương`.
- Thẻ **Khách hàng:** C/CustomerCard `KH.26.0187 - CT CP Sản xuất & KD VinFast · Doanh nghiệp · MST … · SĐT · Hà Nội · địa chỉ` + Loại hình `Doanh nghiệp` · Lĩnh vực `Sản xuất ô tô` · Người liên hệ `Trần Minh Đức - Trưởng phòng Mua hàng · 0912 888 777`.
- Bottom bar: `Quay lại`.

### 06b · Dự án TKT — Phiếu thu thập thông tin
- **Mục đích (nguyên văn):** "Nút gạt sang "Phiếu thu thập thông tin" của dự án đang chọn (chip ở đầu màn). Phiếu VẪN NHẬP được ngay trong meeting và lưu riêng bằng "Lưu phiếu" (không cần lưu meeting) — như tab Dự án TKT trên web. Câu bắt buộc thiếu sẽ chặn Hoàn thành meeting. Câu Có/Không dùng nút gạt."
- Thẻ XANH: `Phiếu nhập được ngay trong meeting, lưu riêng bằng "Lưu phiếu". Thông tin dự án chỉ xem.`
- Chip dự án + nút gạt (đang ở `Phiếu thu thập thông tin`). Tiến độ `3/4 câu` · `Mẫu: Khảo sát trạm sạc EV` · `v2`.
- Câu hỏi (động theo mẫu phiếu):
  1. `Công suất trạm dự kiến (kW)` * — ô gõ số `120`
  2. `Khách hàng đã có mặt bằng lắp đặt chưa?` * — nút gạt `Có` / `Không`
  3. `Nguồn vốn đầu tư` * — chọn `Vốn tự có`
  4. `Ghi chú hiện trạng mặt bằng` * — ô gõ `Nhập câu trả lời`, lỗi đỏ `Bắt buộc phải nhập`
- Bottom bar: [Secondary] `Quay lại` · [Primary] `Lưu phiếu`.

---

### 07 · Nhân sự tham gia (trước Chốt lịch)
- **Mục đích (nguyên văn):** "Theo web 14/10: gộp Thành phần + Điểm danh thành 1 màn "Nhân sự tham gia", chia 2 nhóm Phía Công ty → Phía Khách hàng (thay 2 tab), mỗi nhóm có số người + chip Thêm nhanh. Dòng phía công ty: tên · Mã phòng · Mã NV · badge Chủ trì; phía khách hàng: chức vụ · SĐT, người liên hệ của meeting có badge. Trước khi Chốt lịch KHÔNG có cột điểm danh (xem 08). Thứ tự hiển thị đúng thứ tự đã lưu, thêm mới nối cuối nhóm — sắp xếp làm trên web (chốt 19/10)."
- **Header:** ‹ · `Nhân sự tham gia` · icon `user-plus`.
- Nhóm **Phía Công ty** (số `5`, chip `Thêm nhanh` → 17). Dòng C/PersonRow: avatar chữ tắt · tên · dòng phụ = tag mã công ty (`TPE`/`ETEK`) + `Mã phòng · Mã NV` · đuôi: `Chủ trì` (xanh, không xoá) hoặc `×` (xoá):
  `Nguyễn Hữu Học · TPE · HN_BGD · 11010003 · Chủ trì` · `Trần Thị Lan · TPE · HN_KD1 · 11010057` · `Phạm Văn Vinh · ETEK · HN_KT · 11010112` · `Lê Minh Anh · TPE · HN_DT · 11010140` · `Đỗ Quang Huy · ETEK · ET_KT · 21010021`.
- Nhóm **Phía Khách hàng** (số `2`, chip `Thêm nhanh` → 18): `Trần Minh Đức · Trưởng phòng Mua hàng · 0912 888 777 · Người liên hệ` (badge, không xoá) · `Nguyễn Thanh Tùng · Chuyên viên kỹ thuật · 0903 456 789` (×).
- Bottom bar: [Secondary] `Quay lại` · [Primary] `Lưu`.

### 17 · Thêm thành viên công ty (nhóm "MỞ TỪ MÀN 07 · THÀNH PHẦN THAM DỰ")
- **Mục đích:** "Vào từ tab Công ty. Chọn nhiều nhân viên có sẵn trên hệ thống; mỗi dòng hiện mã công ty."
- **Header:** `x` · `Thêm thành viên công ty` · chữ `Xong`.
- Ô tìm `Tìm theo tên / email / SĐT` · chip lọc `Chức vụ: Kỹ sư trưởng` · `Chức danh`.
- Thanh `Đã chọn 3 người` · `Bỏ chọn tất cả`.
- Dòng (checkbox · avatar · tên · tag công ty · chức vụ · phòng · email · SĐT): `Phạm Văn Vinh · ETEK · Kỹ sư trưởng · P. Kỹ thuật · vinhpv@tanphat.vn · 0987 654 321` (đã chọn) · `Lê Minh Anh · TPE · Chuyên viên Đấu thầu · P. Kinh doanh` (chọn) · `Đỗ Quang Huy · ETEK` (chọn) · `Nguyễn Hữu Học · TPE · Phó Tổng giám đốc · Ban Giám đốc` (nhãn `Đã có`, không chọn được) · `Nguyễn Minh Sơn · ETEK POWER` · `Vũ Thu Hà · TPE` · `Bùi Thanh Tú · ETEK GREEN`.
- Bottom bar: `Huỷ` · [Primary] `Thêm 3 người`.

### 18 · Nhân sự phía Khách hàng
- **Mục đích:** "Vào từ tab Khách hàng. Người liên hệ luôn là NGƯỜI 1, sửa ở màn Thông tin chung. Người còn lại nhập tay Họ tên · Chức vụ · SĐT."
- **Header:** `x` · `Nhân sự phía Khách hàng` · chữ `Lưu`.
- Thẻ KH: `CT CP Sản xuất & KD VinFast` · `Người liên hệ của khách hàng` · `Trần Minh Đức · TP Mua hàng · 0912 888 777`.
- **DANH SÁCH THÀNH PHẦN (2):**
  - `NGƯỜI 1` + badge `Người liên hệ`: Họ tên * `Trần Minh Đức` · Chức vụ `Trưởng phòng Mua hàng` · SĐT `0912 888 777` (khoá — sửa ở Thông tin chung).
  - `NGƯỜI 2`: Họ tên * `Nguyễn Thanh Tùng` · Chức vụ `Chuyên viên Kỹ thuật` · SĐT `0938 111 555` (gõ, có xoá).
- Nút `Thêm người`. Bottom bar: `Quay lại` · [Primary] `Lưu`.

### 08 · Nhân sự tham gia — đã chốt lịch (điểm danh)
- **Mục đích (nguyên văn):** "Từ trạng thái Chốt lịch, mỗi người có thêm nút gạt điểm danh 3 mức: Có mặt (xanh) / Vắng có lý do (cam) / Vắng không lý do (đỏ) — như web. Thanh trên: bộ đếm đã điểm danh + "Tất cả có mặt". Vẫn chia 2 nhóm Phía Công ty → Phía Khách hàng (bỏ bộ lọc Thành phần cũ). Hoàn thành meeting bị chặn nếu còn người chưa điểm danh (màn 30)."
- **Header:** ‹ · `Nhân sự tham gia` · chữ `Lưu`.
- Thanh trên: `Đã điểm danh` + progress `4/5` · nút `Tất cả có mặt` (✓).
- Nhóm Phía Công ty (`3`, `Thêm nhanh`) · Phía Khách hàng (`2`, `Thêm nhanh`). Mỗi người: dòng thông tin (công ty: `Mã phòng · Mã NV` + badge `Chủ trì`; KH: `Chức vụ - Tên KH`) + hàng 3 C/Chip `Có mặt` · `Vắng có lý do` · `Vắng không lý do`. Mẫu: Học/Lan/Đức = Có mặt, Vinh = Vắng có lý do, Tùng = chưa chọn.
- Bottom bar: `Quay lại` · [Primary] `Lưu`.

### 31 · Nhân sự tham gia — họp nội bộ
- **Mục đích:** "Phân loại họp = Nội bộ: chỉ có nhóm Phía Công ty, không có nhóm Phía Khách hàng. Điểm danh bằng nút gạt 3 mức như màn 08."
- `Đã điểm danh 3/3` · `Tất cả có mặt`. Thẻ XANH: `Họp nội bộ: danh sách điểm danh KHÔNG liệt kê khách hàng, nên không bị chặn Hoàn thành vì thiếu điểm danh phía khách.` · nhóm Phía Công ty (3). Bottom: `Quay lại` · `Lưu`.

### 30 · Chặn Hoàn thành → Nhân sự tham gia (điểm danh)
- **Mục đích:** "Bấm Hoàn thành khi còn người chưa điểm danh: dải đỏ dưới header + tự nhảy sang màn Nhân sự tham gia; nút gạt của người chưa điểm danh viền đỏ."
- Dải ĐỎ: `Chưa thể Hoàn thành` · `Còn 1 người chưa điểm danh. Điểm danh đủ mọi người rồi bấm Hoàn thành lại.`
- Như 08; người chưa điểm danh có viền đỏ + nhãn đỏ `Chưa điểm danh`.
- Bottom bar: `Quay lại` · [Primary] `Lưu điểm danh`.

### 14 · Chọn nhân sự
- **Mục đích:** "Màn dùng chung cho chủ trì / người đề xuất / người thực hiện. Mỗi dòng hiện mã công ty của nhân sự."
- **Header:** `Chọn người thực hiện` (đổi theo ngữ cảnh) · chữ `Xong`.
- Ô tìm `Tìm theo tên / mã nhân viên` · chip lọc `Tất cả (24)` · `P. Kinh doanh` · `P. Kỹ thuật`.
- Nhóm **GỢI Ý - THÀNH PHẦN THAM DỰ:** `Phạm Văn Vinh · ETEK · Kỹ sư trưởng - P. Kỹ thuật` · `Trần Thị Lan · TPE · Trưởng phòng Kinh doanh` · `Lê Minh Anh · TPE · Chuyên viên Đấu thầu`.
- Nhóm **TẤT CẢ NHÂN SỰ:** `Đỗ Quang Huy · ETEK` · `Nguyễn Minh Sơn · ETEK POWER` · `Vũ Thu Hà · TPE` · `Bùi Thanh Tú · ETEK GREEN`.
- Bottom bar: `Huỷ` · [Primary] `Chọn (1)`.

---

### 09 · Biên bản — danh sách
- **Mục đích (nguyên văn):** "Một màn gồm cả biên bản như tab Biên bản bản web: các nội dung trao đổi (phương án xử lý, người thực hiện, hạn) rồi tới Kết luận cuộc họp * ở cuối. Bấm khối Kết luận mở trình soạn (màn 13). Lưu biên bản ghi cả nội dung lẫn kết luận."
- **Header:** ‹ · `Biên bản cuộc họp` · `+` (thêm nội dung → 10).
- Dòng tóm tắt: `3 nội dung trao đổi · 2 việc cần làm · có kết luận`.
- Thẻ nội dung (mỗi thẻ có ⋮ sửa/xoá): `NỘI DUNG n` · nội dung · `PHƯƠNG ÁN XỬ LÝ` · phương án (hoặc `Chưa có phương án xử lý` xám nghiêng) · người thực hiện (avatar + tên) · badge hạn `Hạn dd/mm/yyyy` (tô đỏ nhạt).
  1. Khách hàng yêu cầu rút ngắn tiến độ bàn giao trạm sạc số 2 từ 90 ngày xuống 60 ngày. — Tách gói thầu thành 2 giai đoạn… — Phạm Văn Vinh — Hạn 20/09/2026
  2. Chốt đơn giá thiết bị sạc nhanh DC 120kW theo bảng giá tháng 9/2026. — Gửi lại báo giá chính thức… — Trần Thị Lan — Hạn 17/09/2026
  3. Khách hàng đề nghị bổ sung hạng mục giám sát năng lượng từ xa vào phạm vi hợp đồng. — Chưa có phương án xử lý — Lê Minh Anh — Hạn 25/09/2026
- Nút viền đứt `Thêm nội dung trao đổi`.
- Khối **KẾT LUẬN CUỘC HỌP** * : 2 ý đầu + `+1 ý nữa` · link `Sửa kết luận` (→ 13).
- Bottom bar: `Quay lại` · [Primary] `Lưu biên bản`.

### 10 · Thêm nội dung trao đổi
- **Mục đích:** "Đúng 5 trường của bảng biên bản bản web."
- **Header:** `Nội dung trao đổi`.
  | Nhãn | Kiểu | * | Mẫu |
  |---|---|---|---|
  | Nội dung / Vấn đề trao đổi | ô gõ nhiều dòng | * | Khách hàng yêu cầu rút ngắn tiến độ… |
  | Phương án xử lý | ô gõ nhiều dòng | — | Tách gói thầu thành 2 giai đoạn… |
  | Người đề xuất | dòng chọn (→14) | — | `Trần Minh Đức - VinFast` |
  | Người thực hiện | dòng chọn (→14) | * | `Phạm Văn Vinh - Kỹ sư trưởng` |
  | Hạn dự kiến | ngày | * | `20/09/2026` |
- Bottom bar: `Huỷ` · [Primary] `Lưu nội dung`.

### 13 · Biên bản — soạn kết luận
- **Mục đích:** "Mở từ khối Kết luận ở màn 09 — kết luận là phần V của biên bản, không còn là dòng riêng trên Hub. Bấm Xong quay về 09; bấm Lưu biên bản ở 09 mới ghi cả nội dung lẫn kết luận."
- **Header:** `Kết luận cuộc họp` · chữ `Xong`.
- Thẻ XANH: `Kết luận nằm trong biên bản — bắt buộc trước khi chuyển cuộc họp sang Đã hoàn thành.`
- Trình soạn (văn bản nhiều dòng): 3 ý đánh số mẫu.
- Bottom bar: `Quay lại` · [Primary] `Xong`.

### 29 · Chặn Hoàn thành → Biên bản
- **Mục đích:** "Bấm Hoàn thành khi chưa có nội dung biên bản: dải đỏ dưới header + tự nhảy sang khối Biên bản."
- Dải ĐỎ: `Chưa thể Hoàn thành` · `Cuộc họp chưa có nội dung biên bản nào. Thêm ít nhất 1 nội dung trao đổi rồi bấm Hoàn thành lại.` Phần dưới như 09 (bản vẽ có 3 nội dung mẫu, không có khối kết luận). Bottom: `Quay lại` · `Lưu biên bản`.

### 11 · Tài liệu đính kèm (Tài liệu biên bản)
- **Mục đích:** "Chụp ảnh, lấy từ thư viện, hoặc chọn tệp. Mỗi dòng có Xem · Tải xuống · Xoá." (Dòng Hub "Tài liệu biên bản".)
- **Header:** `Tài liệu đính kèm`.
- 3 nút nguồn: `Chụp ảnh` · `Thư viện ảnh` · `Chọn tệp`.
- **ĐÃ ĐÍNH KÈM (3):** mỗi dòng icon loại · tên tệp · `Loại · dung lượng · ngày` · 3 icon Xem/Tải/Xoá: `Bang gia thiet bi sac nhanh T9-2026.pdf · PDF · 1,2 MB · 14/09/2026` · `Du toan so bo tram sac so 2.xlsx · Excel · 386 KB` · `Anh hien trang mat bang KCN.jpg · Ảnh · 2,6 MB`.
- Bottom bar: `Quay lại` · [Primary] `Lưu`.

### 19 · Tài liệu chuẩn bị
- **Mục đích:** "Mở từ dòng Tài liệu chuẩn bị trong Hub. Tệp gửi kèm TRƯỚC buổi họp. Mỗi dòng có Xem · Tải xuống · Xoá."
- Thẻ XANH: `Tài liệu gửi kèm cho thành phần tham dự TRƯỚC buổi họp. Khác với Tài liệu đính kèm trong biên bản.`
- 3 nút `Chụp ảnh` · `Thư viện ảnh` · `Chọn tệp`. **ĐÃ CHUẨN BỊ (2):** `Ho so nang luc TPE 2026.pdf · PDF · 3,4 MB · 12/09/2026` · `Slide gioi thieu giai phap tram sac.pptx · PowerPoint · 5,1 MB · 12/09/2026`.
- Bottom bar: `Quay lại` · [Primary] `Lưu`.

### 12 · Khảo sát nhu cầu KH
- **Mục đích:** "Câu 1 có/không + bảng lĩnh vực và mức đầu tư dự kiến. Câu Có/Không dùng nút gạt (web 15/10)." Dòng Hub ghi "Chỉ với loại Họp tìm hiểu & Giới thiệu sản phẩm".
- **Header:** ‹ · `Khảo sát nhu cầu KH` · chữ `Lưu`.
- Câu 1 * `Anh/Chị có nhu cầu đầu tư trong thời gian tới?` — nút gạt `Có` / `Không`.
- Câu 2 * `Anh/Chị quan tâm tới lĩnh vực và nhóm ngành nào?` — Lĩnh vực Công ty kinh doanh * (chọn, `Chọn lĩnh vực Công ty kinh doanh`) · Nhóm ngành * (chọn nhiều, `Chọn nhóm ngành`) · khối `ĐÃ CHỌN 3 NHÓM NGÀNH` nhóm theo lĩnh vực: `Cơ khí chế tạo (2)` → `Gia công cơ khí chính xác`, `Kết cấu thép`; `Năng lượng & Điện (1)` → `Trạm sạc xe điện` (chip có ×).
- `CÂU 3. MỨC ĐẦU TƯ VÀ THỜI GIAN DỰ KIẾN TRIỂN KHAI` — dải tổng `Tổng mức đầu tư dự kiến 12.500.000.000 ₫` (tự cộng); mỗi nhóm ngành 1 thẻ `Lĩnh vực » Nhóm ngành`: `Mức đầu tư dự kiến (VNĐ)` (ô tiền) + `Thời gian dự kiến bắt đầu` (ngày): 8.000.000.000 ₫ / 01/11/2026 · 3.200.000.000 ₫ / 01/01/2027 · 1.300.000.000 ₫ / `Chọn thời gian`.
  - *Lưu ý format số: bản vẽ dùng `12.500.000.000 ₫` (kiểu VN); CLAUDE.md quy định chuẩn quốc tế `12,500,000,000` — cần đối chiếu khi code.*
- Câu 4 * `Anh/Chị có nhu cầu về dịch vụ sửa chữa bảo dưỡng/bảo trì máy móc thiết bị?` — `Có` / `Không`.
- Bottom bar: `Quay lại` · [Primary] `Lưu khảo sát`.

### 15 · Xem trước biên bản
- **Mục đích:** "Bản in khổ giấy thu nhỏ, tải PDF hoặc chia sẻ."
- Tờ giấy thu nhỏ: `CÔNG TY CỔ PHẦN TÂN PHÁT ETEK` · `Số: MTG.26.0245/BB-TPE` · `BIÊN BẢN CUỘC HỌP` · `V/v: <tên meeting>` ·
  - `I. THÔNG TIN CUỘC HỌP` — Loại · Hình thức · Địa điểm · Chủ trì (`Nguyễn Hữu Học - Phó Tổng giám đốc`)
  - `II. THỜI GIAN` — `Bắt đầu 08:30, kết thúc 10:00 ngày 14/09/2026`
  - `III. THÀNH PHẦN THAM GIA` — `Công ty: 8 người (có mặt 7, vắng có lý do 1)` · `Khách hàng: 4 người (có mặt 4)`
  - `IV. NỘI DUNG MEETING` — từng nội dung: `Nội dung. Phương án: … — Người thực hiện, hạn dd/mm/yyyy`
  - `V. KẾT LUẬN`
  - Chữ ký: `ĐẠI DIỆN KHÁCH HÀNG` Trần Minh Đức · `ĐẠI DIỆN TPE` Nguyễn Hữu Học.
- Bottom bar: [Secondary] `Tải PDF` · [Primary] `Chia sẻ`.

---

### 22 · Menu hành động (⋮)
- **Mục đích:** "Thao tác không nằm ở thanh dưới: Sửa, Tạo phiếu công tác khác, In, Lịch sử, Huỷ."
- Action sheet trên nền Hub (04b): tiêu đề `Hành động` · `MTG.26.0245 · Đã chốt lịch` · mục: `Sửa thông tin` · `Tạo phiếu công tác khác` · `In biên bản` · `Lịch sử thay đổi` · `Huỷ meeting` (đỏ → 16).

### 16 · Hộp xác nhận huỷ
- **Mục đích:** "Gọi từ menu ⋮ trên Hub. Chọn Lý do huỷ từ danh mục (sẽ bổ sung trên web sau) rồi nhập ghi chú; ghi vào lịch sử, không hoàn tác."
- Popup: icon cảnh báo đỏ · `Huỷ cuộc họp này?` · `MTG.26.0245 sẽ chuyển sang trạng thái Huỷ. Thao tác được ghi vào lịch sử và không thể hoàn tác.` · Lý do huỷ * (chọn, `Chọn lý do huỷ từ danh mục`) · Ghi chú huỷ (ô gõ, `Nhập ghi chú huỷ (nếu có)`) · nút [Secondary] `Không` · [Danger đỏ] `Xác nhận huỷ`.

### 23 · Xác nhận đổi thời gian
- **Mục đích:** "Sửa giờ của lịch đã chốt → hỏi trước khi gửi lịch mới cho toàn bộ thành phần."
- Popup: `Xác nhận thay đổi thời gian` · `Thời gian cuộc họp đã thay đổi so với lịch đã chốt trước đó. Việc lưu sẽ gửi lịch họp mới đến tất cả thành viên tham dự. Bạn có xác nhận gửi lịch họp mới không?` · so sánh `Lịch đã chốt 14/09/2026 08:30 - 10:00` → `Lịch mới 15/09/2026 14:00 - 15:30` · nút `Hủy` · [Primary] `Xác nhận`.

> Lưu ý: nền Hub của 16/22/23 là bản Hub CŨ (các dòng "Thành phần tham dự", "Điểm danh" tách riêng, "Tài liệu đính kèm", bottom bar 16 là `Điểm danh · Ghi biên bản`; nền 23 lại mang badge `Lưu nháp`). Dev bám bộ dòng Hub mới của 04a/04b/04c.

### 24 · Hub — có lỗi khi lưu
- **Mục đích:** "Khối có lỗi tô đỏ kèm số lỗi; tự nhảy tới khối lỗi đầu tiên."
- Dải ĐỎ: `Còn 4 lỗi cần sửa` · `Đã chuyển tới khối lỗi đầu tiên. Các khối có lỗi được đánh dấu đỏ bên dưới.` Mức độ hoàn thiện `0/3`.
- Khối lỗi tô đỏ: Thông tin chung * `Thiếu Người chủ trì, Khách hàng` · `3 lỗi`; Biên bản cuộc họp `Nội dung 1 thiếu Người thực hiện` · `1 lỗi`. Các khối khác như 04a.
- Bottom bar: `Lưu nháp` · `Lên lịch hẹn`.

### 46 · Hub — chặn Hoàn thành
- **Mục đích:** "Bấm Hoàn thành khi còn khối bắt buộc chưa xong: dải đỏ liệt kê đúng khối thiếu, các khối đó tô đỏ. Web hiện chỉ bắn toast rồi nhảy tab."
- Dải ĐỎ: `Chưa thể Hoàn thành — còn 2 khối bắt buộc` · `Nhân sự tham gia (còn 3 người chưa điểm danh)` · `Biên bản cuộc họp (chưa có nội dung trao đổi, kết luận). Hai khối này tô đỏ bên dưới.`
- Mức `2/3`; Nhân sự tham gia * `điểm danh 12/15` (đỏ) · Biên bản cuộc họp * `Thiếu` (đỏ). Có * ở đủ 3 khối.
- Bottom bar: `Lưu` · [Primary] `Hoàn thành`.

### 26 · Hub — Đã huỷ
- **Mục đích:** "Status 4: alert đỏ Lý do huỷ, mọi thao tác ẩn, chỉ còn Quay lại."
- Badge `Huỷ`. Dải/thẻ ĐỎ `Lý do huỷ` · `Khách hàng dời lịch sang tuần sau do đoàn công tác Nhật Bản đổi lịch bay.` Không dấu *. Bottom: `Quay lại`.

### 27 · Hub — Chỉ xem (không có quyền)
- **Mục đích:** "can_manage = false: người chỉ tham dự, ẩn sạch nút và mũi tên mở khối."
- Dải XÁM: `Chế độ chỉ xem` · `Bạn chỉ là thành viên tham dự nên mọi thao tác sửa, huỷ, xoá đều được ẩn.` Khối không chevron, không dấu *. Bottom: `Quay lại`.

---

## F. Bộ màn CHỈ XEM (meeting Đã hoàn thành)
Chung: dải XÁM dưới header `Meeting đã hoàn thành — chỉ xem, không sửa được.`; nhãn–giá trị dùng C/ViewRow; bottom bar chỉ `Quay lại`. *(Bản vẽ 32 vẫn còn chữ "Lưu" trên header — coi là sót, phải ẩn.)*

### 33 · Thông tin chung — xem
- Nguyên văn: "Nhãn–giá trị phẳng, bỏ hết ô nhập. Hợp đồng: mã (bấm mở hợp đồng) + khách hàng + badge trạng thái. Trạng thái meeting chỉ nằm ở tiêu đề meeting trên Hub. Theo web 19/10: 3 khối màu như màn nhập (① Thông tin cuộc họp gồm Loại + Tên + Mục tiêu, ② Đối tác, ③ Thời gian…) (vòng số đặc vì đã đủ) + khối "Thông tin bản ghi" (slate) — mã, trạng thái, người tạo, ngày tạo, cập nhật gần nhất."
- ①: Phân loại họp `Họp đối tác` · Loại meeting `Thương thảo HĐ` · Tên cuộc họp · Mục tiêu / Nội dung.
- ②: Khách hàng · Người liên hệ `Trần Minh Đức - Trưởng phòng Mua hàng · 0912 888 777` · Hợp đồng `HĐ_TPE_KD1_26_0112 · CT CP… · Có hiệu lực`.
- ③: Bắt đầu `14/09/2026 08:30` · Kết thúc · Người chủ trì `Nguyễn Hữu Học - Phó Tổng giám đốc` · Hình thức `Trực tiếp` · Địa điểm meeting.
- **Thông tin bản ghi:** Mã meeting `MTG.26.0245` · Trạng thái `Hoàn thành` · Người tạo `Nguyễn Hữu Học - HN_BGD - 11010003` · Ngày tạo `10/09/2026 14:20` · Cập nhật gần nhất `Trần Thị Lan · 14/09/2026 10:15`.

### 34 · Dự án TKT — xem
- "Meeting đã hoàn thành: cùng bố cục màn 06 (chip dự án · nút gạt Thông tin chung / Phiếu thu thập thông tin · thẻ tóm tắt), không có Lưu phiếu, câu trả lời phiếu chỉ xem. Đã bỏ khối Giải pháp / Hạng mục (chốt 14/10)." Nội dung giống 06.

### 32 · Nhân sự tham gia — xem
- "Meeting đã hoàn thành: 1 màn xem chung cho Thành phần + Điểm danh (thay 32 + 35 cũ). 2 nhóm Phía Công ty / Phía Khách hàng, mỗi người hiện badge kết quả điểm danh; không nút gạt, không Thêm nhanh."
- Dải XÁM: `Meeting đã hoàn thành — kết quả điểm danh đã chốt, không sửa được nữa.` · `Kết quả điểm danh 4/5 có mặt`. Mỗi người badge `Có mặt` / `Vắng có lý do` (+ lý do vắng dưới: `Đi công tác Đà Nẵng`).

### 36 · Tài liệu chuẩn bị — xem
- "Bỏ 3 nút tải lên và nút xoá, chỉ còn Xem và Tải xuống." `ĐÃ CHUẨN BỊ (2)`.

### 37 · Biên bản cuộc họp — xem
- "Bỏ menu ⋮ từng dòng và nút Thêm nội dung. Kết luận cuộc họp nằm cuối biên bản (gộp màn 40 cũ): bỏ thanh công cụ soạn thảo, thêm dòng ai chốt và lúc nào."
- Nội dung như 09 + `KẾT LUẬN CUỘC HỌP` đầy đủ 3 ý + `Chốt bởi Nguyễn Hữu Học · 14/09/2026 10:12`.

### 38 · Tài liệu biên bản — xem
- "Như 36, cho tệp đính kèm trong biên bản: chỉ Xem và Tải xuống." `ĐÃ ĐÍNH KÈM (3)`.

### 39 · Khảo sát nhu cầu KH — xem
- "4 câu hiện dạng câu hỏi – câu trả lời, bỏ radio và ô nhập tiền." Câu 1 `Có` · Câu 2 `Cơ khí chế tạo (2)` → Gia công cơ khí chính xác, Kết cấu thép · `Năng lượng & Điện (1)` → Trạm sạc xe điện · Câu 3 Tổng `12.500.000.000 ₫`, mỗi nhóm `số tiền · Bắt đầu dd/mm/yyyy` (Trạm sạc: `Bắt đầu 01/03/2027`) · Câu 4 `Có`.

---

## G. Bảng tra nhanh màn ↔ mã

| Mã | Tên | Nhóm |
|---|---|---|
| 00h / 00h' | Tổng quan Meeting / trống | Tab 1 |
| 00d | Drawer Meeting | Điều hướng |
| 00j | Thông báo (chung) | Điều hướng |
| 01 | Lịch meeting | Bước 1 |
| 02 | Bộ lọc | Bước 1 |
| 03 | Tạo meeting | Bước 2 |
| 04a / 04b / 04c | Hub Lưu nháp / Đã chốt lịch / Đã hoàn thành | Bước 2/4/5 |
| 05, 25, 28, 45 | Thông tin chung: sửa / lỗi / Online / cảnh báo chưa lưu | Bước 3 / Ngoại lệ |
| 06, 06b, 48, 49 | Dự án TKT, phiếu thu thập, chọn dự án, chọn hợp đồng | Bước 3 |
| 07, 17, 18 | Nhân sự tham gia, thêm NV công ty, nhân sự phía KH | Bước 3 |
| 19, 20, 21 | Tài liệu chuẩn bị, bản đồ, lịch sử meeting KH | Bước 3 |
| 41, 41b, 42, 43, 44 | Chọn KH, không thấy KH, thêm nhanh KH, chọn liên hệ, thêm nhanh liên hệ | Bước 3 (5 màn cam) |
| 08, 30, 31 | Điểm danh, chặn HT điểm danh, họp nội bộ | Bước 4 |
| 09, 10, 13, 14, 29 | Biên bản, thêm nội dung, kết luận, chọn nhân sự, chặn HT biên bản | Bước 4/5 |
| 22, 23, 46 | Menu ⋮, đổi thời gian, chặn Hoàn thành | Bước 4 |
| 11, 12, 15 | Tài liệu biên bản, khảo sát, xem trước biên bản | Bước 5 |
| 16, 24, 26, 27 | Huỷ, Hub lỗi, Hub đã huỷ, Hub chỉ xem | Ngoại lệ |
| 32, 33, 34, 36, 37, 38, 39 | Bộ màn chỉ xem | Xem |
