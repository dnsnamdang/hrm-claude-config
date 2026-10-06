# C3.1 — Đặc tả popup *Xây dựng catalog kinh doanh* + lối *Xếp vào tiểu mục…*

> Ngày đọc: 04/10/2026. Chỉ đọc, chưa đụng source.
> Nguồn: `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` (markup L1879–2003, CSS L407–411 + L696–766,
> bộ lọc `BO_LOC.cat` L3532–3543, cột `cat` của lưới L2748, JS L6896–7380) · `design.md` §33a–§33w, §35b/§35c (C5, C5-a),
> §36f · `2c-ghi/chot.md` (G4, G6) · `2c-ghi/yeu-cau-ghi.md` §1.6 · `2b-doc/mockup-inventory.md` §2.
> Nguyên tắc ưu tiên khi lệch: bản muộn nhất thắng (§36f 01/10 > §33w 30/09 > §33j–§33u 29/09 > §33a–§33d 29/09).

---

## 1. Mở popup

### 1.1 Hai lối mở — cùng ở màn *Dữ liệu hàng hoá công ty* (`sc-kho`)

| Lối | Vị trí | Nút | Hành vi |
|---|---|---|---|
| A | Tiêu đề lưới (cạnh *Xuất Excel*, *Cấu hình cột*) | **Xây dựng catalog** — `v2-btn--primary`, icon sơ đồ nhánh | `moXayCatalog(false)`: **không mang mã nào**, mở ở tab **Hàng trong tiểu mục** |
| B | Thanh xanh hàng loạt (hiện khi tick ≥ 1 dòng lưới): *"Đã chọn **N** hàng hoá"* · [**Xếp vào tiểu mục…**] · [Bỏ chọn] | **Xếp vào tiểu mục…** — primary, icon `+` | `moXayCatalog(true)`: mang danh sách mã đã tick (`sanCo`), mở thẳng tab **Thêm hàng vào tiểu mục** |

- Chỉ có ở màn này. **Không** có ở *Hàng đang kinh doanh* (§33e), *Kho dữ liệu hàng hoá* (toàn hệ thống), *Hàng hoá nhập thông tin*.
- Quyền **1655 *Xây dựng catalog kinh doanh***: không có thì **ẩn** cả 2 nút; BE gate mọi endpoint ghi của popup (§33a, §35b, yeu-cau-ghi §1.6). Super admin không ngoại lệ.
- Lối B mang sẵn mã: các mã này **chưa tick ngay** khi mở (chưa có tiểu mục). Chỉ khi user **bấm một Tiểu mục trên cây trong lúc đang ở tab Thêm** thì tick sẵn những mã đó **mà chưa nằm trong tiểu mục ấy** (mã đã nằm rồi không xuất hiện ở tab Thêm). `sanCo` giữ suốt phiên popup ⇒ bấm sang tiểu mục khác là tick lại cùng bộ mã — xếp một bộ hàng vào nhiều tiểu mục liên tiếp được.

### 1.2 Mỗi lần mở đều reset

Ô tìm cây + ô tìm hàng rỗng · Trạng thái về rỗng · công tắc *Chỉ hàng chưa xếp catalog* tắt · 8 ô nâng cao rỗng và
**khối nâng cao THU GỌN** (nhãn nút về *"Tìm kiếm nâng cao"*) · **khổ thường** (không giữ toàn màn hình lần trước) ·
khung *Dán danh sách mã* đóng · chưa chọn tiểu mục · trang 1, 20 dòng/trang · giỏ chờ rỗng · cây về mặc định (§2.4).

### 1.3 Tiêu đề

- Icon sơ đồ nhánh (khuôn `.modal-h .ico`) · **H3: "Xây dựng catalog kinh doanh"**.
- Mô tả (`cat-mo-ta`), nguyên văn:
  - Lối A: `Công ty <TÊN CÔNG TY> · chọn Tiểu mục ở cây bên trái rồi tick hàng hoá`
  - Lối B: `Công ty <TÊN CÔNG TY> · chọn Tiểu mục ở cây bên trái rồi tick hàng hoá — mang sang <N> hàng hoá đã tick ở lưới`
- Bên phải: nút **⤢ Phóng to toàn màn hình** (tooltip `Phóng to toàn màn hình` ⇄ `Thu nhỏ`, icon đổi theo) · nút **✕** (= Đóng, có cảnh báo chưa lưu).

### 1.4 Bố cục + kích thước (khuôn `V2BaseModal`, body cuộn riêng, **footer ghim đáy**)

```
┌ Header ─────────────────────────────────────────────────────────── ⤢ ✕ ┐
│ ┌ TRÁI 330px cố định ──┐  ┌ PHẢI flex:1, min-width:0 ─────────────────┐ │
│ │ [🔍 Tìm trong cây…][⇊][⇈]│  [Tab Hàng trong TM (N) | Thêm hàng vào TM]  │ │
│ │ cây 4 cấp            │  │            [Tìm kiếm nâng cao][Dán ds mã] │ │
│ │ (max-height 52vh)    │  │ dải "Đang xem tiểu mục: …"                 │ │
│ │                      │  │ [🔍 tìm][Trạng thái▾][⬤ Chỉ hàng chưa xếp][Làm mới]│
│ │                      │  │ (khối nâng cao 8 ô) (khung dán mã)         │ │
│ │ ghi chú dưới cây     │  │ Đã chọn N · Chọn tất cả N…   [Thêm vào TM] │ │
│ └──────────────────────┘  │ bảng 12 cột (max-height 42vh, cuộn ngang)  │ │
│                           │ Hiển thị x–y / z   Số dòng/trang [20▾] «1 2»│ │
│                           └────────────────────────────────────────────┘ │
├ Footer: Đang chờ lưu: +12 · −3 [Hoàn tác]                  [Lưu] [Đóng] ┤
```

| Thông số | Khổ thường | Toàn màn hình (`.toan-man`) |
|---|---|---|
| Modal | `width: min(1460px, 100%)` (đo 1460×418) | 100% × 100vh, bo góc 0 (đo 1512×773) |
| Khoảng cách 2 cột | `gap: 14px` | như cũ |
| Cột cây | `flex: 0 0 330px` | như cũ |
| Cây cao tối đa | `max-height: 52vh` (đo 224px) | `calc(100vh - 210px)` (đo 471px) |
| Bảng cao tối đa | `max-height: 42vh`, cuộn dọc riêng (đo 325px) | `calc(100vh - 330px)` (đo 443px) |
| Footer | ghim đáy (đáy footer = đáy modal) | ghim đáy |

Gợi ý code: `size="xl"` không đủ 1460px ⇒ dùng `V2BaseModal` với class/width riêng; nút phóng to theo popup *Xem hàng hoá Công ty khác* nếu repo đã có (mockup dùng chung cơ chế `.mask.toan-man`).

---

## 2. Cây catalog (cột trái)

### 2.1 Cấp + nguồn dữ liệu

| Cấp | Nhãn | Bảng | Ghi chú |
|---|---|---|---|
| 1 | Lĩnh vực Công ty kinh doanh | `internal_business_scopes` (8 dòng, status 1/2) | status 2 = khoá ⇒ 🔒 |
| 2 | Chương | `chapters` qua `internal_business_scope_id` (H3) | chỉ chương có gốc mới; dòng cũ ẩn |
| 3 | Mục | `job_groups` | con của Chương hiện |
| 4 | Tiểu mục | `job_clusters` | **cấp DUY NHẤT bấm chọn được** |

Đổi tên §33w: *Nhóm công việc* → **Mục**, *Cụm công việc* → **Tiểu mục** (chỉ chữ hiển thị; CSDL giữ `job_groups`/`job_clusters`).
Toàn popup **không được còn** chữ "Nhóm công việc"/"Cụm công việc"/"cụm" (đo bằng `innerText`).

### 2.2 Trình bày dòng (§33u — phương án A + số thứ tự)

| Cấp | Số thứ tự | Chữ | Đặc biệt |
|---|---|---|---|
| 1 Lĩnh vực | La Mã `I.` `II.` (màu `#8494a6`) | **CHỮ HOA** 11px/700 xám `#64748b` | `position: sticky; top:0` (dính đầu khi cuộn), nền trắng, viền dưới `#eef2f6`; có nút 20×20 mở/thu cả lĩnh vực (§2.5) |
| 2 Chương | `1.` | 12.5px/600 `#0f172a` | |
| 3 Mục | `1.1` | 12px/400 `#64748b` | |
| 4 Tiểu mục | `1.1.1` (teal `#0a99a7`, 600) | 12px `#0f172a` | đang chọn: nền `rgba(26,188,156,.12)`, chữ `#0a7c88` 600, badge `rgba(10,153,167,.16)` |

- Số thứ tự đánh **theo từng nhánh** (mở lĩnh vực khác thì Chương lại từ `1.`); La Mã đánh theo các lĩnh vực **đang hiện** (sau lọc tìm).
- Đường nối dọc 1px `#e8eef4` mỗi cấp (thay thụt lề trần): mỗi cấp con thêm 1 vạch `width 15px; margin-left 5px`.
- Mũi `▾`/`▸` (màu `#b6c2d1`, 9px) đẩy **sát mép phải**; cấp 4 không có mũi.
- Tên dài: `ellipsis`, 1 dòng. Hover dòng nền `#f8fafc`.
- Lĩnh vực khoá: tiền tố **`🔒 `** trước tên.

### 2.3 Số đếm trên nút

- Ý nghĩa (ghi dưới cây, 11.5px xám): **"Số bên phải mỗi nút là số hàng hoá đang thuộc nhánh đó"**.
- Đếm = số hàng của **công ty đang đăng nhập** (mọi trạng thái) thuộc nhánh, **đã cộng/trừ giỏ chờ** ⇒ tick *Thêm vào tiểu mục* xong số nhảy ngay (đo: tiểu mục 0→2, chương 1→3, lĩnh vực cộng dồn).
- Cấp 4: **luôn hiện** badge (kể cả 0), sát mép phải.
- Cấp 1–3: chỉ hiện khi **đang đóng VÀ số > 0**; mở ra thì ẩn.
- Lưu ý đếm cấp trên = **tổng các tiểu mục con** ⇒ một hàng ở 2 tiểu mục cùng chương được tính 2 lần ở chương (mockup cộng dồn). Xem §6 câu tự chốt U5.
- Badge: nền `#f1f5f9`, bo 9px, 10.5px.

### 2.4 Đóng/mở

- Mặc định khi mở popup: **Lĩnh vực + Chương ĐÓNG, Mục MỞ** ⇒ thấy 8 lĩnh vực; mở 1 chương là thấy ngay danh sách tiểu mục.
- Bấm dòng cấp 1–3 = đảo đóng/mở **một cấp** (lần bấm đầu phải tính theo mặc định: Mục đang mở ⇒ bấm là đóng).
- Bấm dòng cấp 4 = **chọn tiểu mục**: xoá hết tick đang chọn, về trang 1, vẽ lại cây + bảng; ở tab Thêm thì tick sẵn `sanCo` (§1.1).

### 2.5 Nút mở/thu hàng loạt (§36f)

| Nút | Vị trí | Kích thước | Tooltip | Hành vi |
|---|---|---|---|---|
| Mở toàn bộ | cạnh ô tìm cây | 28×28, bo 7px, viền `#e2e8f0`, icon mũi kép xuống | `Mở toàn bộ các cấp` | mở mọi Lĩnh vực + Chương + Mục (đo 8 → 71 nút / 29 tiểu mục) |
| Thu gọn toàn bộ | cạnh nút trên | 28×28, icon mũi kép lên | `Thu gọn toàn bộ các cấp` | đóng mọi cấp (về 8 nút) |
| Mở/thu 1 lĩnh vực | trên mỗi dòng Lĩnh vực, sau badge | 20×20, bo 5px, viền trong suốt, icon mũi **kép** (khác mũi đơn của dòng) | `Mở toàn bộ lĩnh vực này` ⇄ `Thu gọn lĩnh vực này` | bung toàn bộ Chương + Mục của riêng lĩnh vực (đo 8 → 24); bấm lại thu gọn; **không** lan sự kiện bấm dòng |

"Đã bung hết" của 1 lĩnh vực = lĩnh vực mở + mọi chương mở + mọi mục không bị đóng.

### 2.6 Ô tìm trong cây

- Placeholder **"Tìm trong cây catalog"**, kính lúp 14px, cao 32px; lọc ngay khi gõ (không phân biệt hoa thường, so chuỗi con).
- Giữ tiểu mục nếu **nó hoặc bất kỳ cấp cha nào** khớp ⇒ gõ tên lĩnh vực là hiện cả lĩnh vực.
- Đang tìm ⇒ **mọi cấp đều bung** (bỏ qua trạng thái đóng/mở).
- Không khớp gì: **"Không có nút nào khớp"**.

### 2.7 Nút bị khoá

Mockup chỉ có **Lĩnh vực khoá** (*Khác*, status 2) hiện 🔒 và **vẫn bấm chọn tiểu mục bên dưới được**. Chương/Mục/Tiểu mục khoá (status 0) mockup không có ⇒ cần chốt (§6, B2).

---

## 3. Bảng hàng hoá (cột phải)

### 3.1 2 tab (`.ctab` kiểu segmented, cao 26px)

| Thứ tự | Tab | Danh sách | Nút hành động |
|---|---|---|---|
| 1 (mặc định lối A) | **Hàng trong tiểu mục (N)** — N = số hàng thuộc tiểu mục đang chọn, đã tính giỏ; chưa chọn TM ⇒ `0` | hàng của công ty **đang thuộc** tiểu mục (gồm cả hàng vừa thêm vào giỏ) | **Gỡ khỏi tiểu mục** — `v2-btn--danger`, icon `−` |
| 2 (mặc định lối B) | **Thêm hàng vào tiểu mục** | hàng của công ty **chưa thuộc** tiểu mục (đã trừ giỏ) | **Thêm vào tiểu mục** — `v2-btn--primary`, icon `+` |

- Đổi tab: xoá tick, về trang 1.
- Thêm vào giỏ xong hàng **nhảy sang tab kia ngay** (tab Thêm 10 → 8 dòng; tab Trong tăng tương ứng).

### 3.2 Dải "Đang xem tiểu mục" (chỉ hiện khi đã chọn TM)

Nền `rgba(26,188,156,.09)`, viền `rgba(26,188,156,.25)`, chữ `#0a7c88` 12px, icon sơ đồ nhánh:
`Đang xem tiểu mục: <b>Máy nén trục vít</b>  Công nghiệp › Thiết bị khí nén › Lắp đặt hệ thống khí nén` (đường dẫn 11.5px xám, 3 cấp trên nối ` › `).

### 3.3 Hàng nút phía trên (ngang với tab)

[**Tìm kiếm nâng cao**] (secondary, bật/tắt khối 8 ô, nhãn đổi *Tìm kiếm nâng cao* ⇄ *Thu gọn* theo khuôn `moBoLoc`) · [**Dán danh sách mã**] (secondary, bật/tắt khung dán).

### 3.4 Hàng lọc nhanh

| Ô | Chi tiết |
|---|---|
| Tìm nhanh | placeholder **"Tìm theo mã, tên hàng hoá, model"** (không có barcode); khớp chuỗi con trên `mã + tên + model` |
| Trạng thái | select rộng 190px, placeholder **"Trạng thái"**, 4 lựa chọn: *Đang nhập thông tin · Chờ tính giá bán · Đang tính giá · Đang kinh doanh* (xem §6 B3 về *Ngừng kinh doanh*) |
| Công tắc | **"Chỉ hàng chưa xếp catalog"** — **chỉ hiện ở tab Thêm**; lọc hàng **chưa có nhánh nào đã lưu** ở công ty đang làm việc (không tính giỏ) |
| Làm mới | tertiary, icon xoay; xoá ô tìm + Trạng thái + công tắc + 8 ô nâng cao, về trang 1 (KHÔNG đổi tiểu mục, KHÔNG xoá tick — mockup giữ `CAT.chon`) |

Mockup lọc **ngay khi gõ/chọn** (không có nút *Tìm kiếm* trong popup). Ô lọc cao 32px.

### 3.5 Khối *Tìm kiếm nâng cao* — 8 ô (mặc định ẨN)

Thứ tự: **Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Xuất xứ · Model**.
Đã bỏ: *Đơn vị tính* (§33n-4) và *Công ty quản lý* (§36f-1). Mỗi ô 1 giá trị, so khớp bằng.
(Ghi chú: chữ "Tính chất hàng hóa" trong mockup viết "hóa" — các chỗ khác viết "hoá"; xem §6 U7.)

### 3.6 Cột — 12 cột, mọi ô **1 dòng** (`nowrap`), bảng 1.266px trong khung 1.069px ⇒ cuộn ngang

| # | Cột | Rộng | Căn | Nội dung |
|---|---|---|---|---|
| 1 | ☐ (tick tất cả **trang đang xem**) | 44 | giữa | ô tick dòng |
| 2 | STT | 48 | giữa | chạy tiếp qua trang (trang 2 bắt đầu 21) |
| 3 | Ảnh | 52 | giữa | thumbnail ảnh hàng hoá |
| 4 | Mã hàng | 160 | trái | **bấm ô = tick/bỏ tick dòng** (con trỏ tay, hover `#0a7c88`) |
| 5 | Tên hàng hoá | 230 | trái | **bấm ô = tick/bỏ tick dòng** |
| 6 | Model | 105 | trái | |
| 7 | Loại sản phẩm | 160 | trái | |
| 8 | Thương hiệu | 110 | trái | |
| 9 | ĐVT | 70 | trái | đơn vị cơ bản |
| 10 | **Thông số cơ bản** | 240 | trái | chuỗi `Thuộc tính: giá trị; …` cắt 190px `…` + nút **⋯** (22×18) mở khung *Thông số cơ bản · <mã>* liệt kê đủ từng dòng (2 cột: tên xám nowrap / giá trị); bấm ra ngoài hoặc cuộn ⇒ đóng; bấm lại ⋯ cùng mã ⇒ đóng. Không có thông số ⇒ ô **trống hẳn** |
| 11 | Trạng thái | 145 | giữa | badge trạng thái **của công ty đang đăng nhập** |
| 12 | Catalog đang xếp | 300 | trái | chip tên Tiểu mục của nhánh đầu (tooltip đủ `Lĩnh vực › Chương › Mục › Tiểu mục`), nhiều nhánh thêm chip viền đứt `+N` (tooltip `• <đường dẫn>` từng nhánh còn lại); chưa có ⇒ chữ xám **"Chưa xếp catalog"**. Chip trong popup tối đa 252px. **Dữ liệu ĐÃ LƯU**, không tính giỏ |

- Dòng đang tick: nền `rgba(26,188,156,.07)`. Dòng cao ~43px.
- §36f: khung ⋯ dùng `position: fixed` (không bị khung cuộn cắt), dòng cuối tự lật lên trên. Khi code: **`b-popover` theo khuôn info-popover**; API danh sách **eager load**, chỉ trả chuỗi tóm tắt + danh sách ngắn.
- Không có cột *Công ty quản lý* (đã bỏ §36f). Không có cột Hành động.

### 3.7 Câu rỗng (colspan 12)

| Tình huống | Câu |
|---|---|
| Chưa chọn tiểu mục | **"Chọn một Tiểu mục ở cây bên trái để bắt đầu"** |
| Tab Thêm, không còn hàng | **"Không còn hàng hoá nào khớp bộ lọc"** |
| Tab Trong, rỗng | **"Tiểu mục này chưa có hàng hoá nào"** |

### 3.8 Nguồn hàng

- **Toàn bộ hàng của công ty đang đăng nhập, mọi trạng thái** (§33a-5) = mọi `product_company_coefficients` của công ty có `status` (gồm hàng **lấy về** từ công ty khác). Không gồm hàng công ty khác chưa lấy về (§33i-8).
- Chỉ trong phạm vi công ty đang đăng nhập (§33a-3); catalog riêng theo công ty (cùng mã: TÂN PHÁT 2 nhánh · TÂN PHÁT SG 1 nhánh).
- Thực tế 45.890 mã ⇒ **phân trang + lọc ở BE**, không tải cả kho về FE như mockup.

### 3.9 Đếm chọn + "Chọn tất cả N kết quả lọc" + trần 100 (§33j-2)

Hàng trên bảng: `Đã chọn N hàng hoá` / **"Chưa chọn hàng hoá nào"** (11.5px xám) · link **"Chọn tất cả N kết quả lọc"** (chỉ hiện khi có kết quả và số đã chọn < tổng) · nút hành động bên phải.

| Hành vi | Chi tiết |
|---|---|
| Trần | `GIOI_HAN_CAT = 100` mã **mỗi lượt** (một lần bấm Thêm/Gỡ); tick giữ qua các trang |
| Tick 1 ô khi đủ 100 | ô **tự bỏ tick** + toast cảnh báo *"Mỗi lượt chỉ xếp tối đa 100 mã hàng — hãy Lưu lượt này rồi chọn tiếp"* |
| Tick đầu bảng | chỉ **trang đang xem**; vượt trần thì tick tới 100 + cùng toast; bỏ tick đầu bảng = bỏ tick cả trang |
| Chọn tất cả N | tick lần lượt kết quả lọc tới 100. N > 100 ⇒ toast cảnh báo *"Đã chọn 100/127 hàng hoá — mỗi lượt tối đa 100 mã, Lưu xong chọn tiếp phần còn lại"*; N ≤ 100 ⇒ toast thành công *"Đã chọn tất cả N hàng hoá đang lọc"* |
| BE | FE gửi danh sách id (≤ 100/lượt) ⇒ **KHÔNG cần** `assign-by-filter` (§33i-6 hết hiệu lực) — nhưng "Chọn tất cả N" cần BE trả **id của N kết quả lọc** (tối đa 100 đầu) vì FE chỉ có trang đang xem |

### 3.10 Dán danh sách mã

Khung (ẩn mặc định), nút [Dán danh sách mã] bật/tắt; mở là focus ô:
- Ghi chú: **"Dán danh sách mã hàng từ Excel — mỗi mã một dòng (hoặc cách nhau bằng dấu phẩy). Mã không tồn tại sẽ được báo ra."**
- Textarea placeholder `TPE-MNK-FS-15A` ↵ `TPE-CN-2T-4500`. Tách theo xuống dòng, `,`, `;`, Tab; bỏ khoảng trắng; so **không phân biệt hoa thường**.
- Nút [**Tick theo danh sách**] (primary, ✓) · [**Đóng**] (tertiary).
- Chưa dán gì: **"Chưa dán mã nào"**.
- Kết quả (1 dòng, nguyên văn ghép): `Đã tick x/y mã` + ` · z mã không nằm trong danh sách đang lọc (A, B, C)` + ` · t mã KHÔNG TỒN TẠI (A, B, C)` — mỗi nhóm liệt kê tối đa **3 mã** đầu.
  Ví dụ đã đo: `Đã tick 2/4 mã · 1 mã không nằm trong danh sách đang lọc (SG-MKD-SC-800) · 1 mã KHÔNG TỒN TẠI (MA-KHONG-CO-01)`.
- Có mã không tồn tại ⇒ thêm toast cảnh báo *"t mã không tồn tại trong hệ thống"*.
- "Danh sách đang lọc" = kết quả của tab + bộ lọc hiện tại (**mọi trang**). Mã có trong hệ thống nhưng ngoài danh sách (vd đã nằm trong tiểu mục, công ty chưa lấy về, khác bộ lọc) ⇒ nhóm *không nằm trong danh sách đang lọc*. "Không tồn tại" = không có trong toàn hệ thống.
- Đủ trần 100 thì dừng tick (mã thừa không được báo riêng — x < y). Chưa chọn tiểu mục thì danh sách rỗng ⇒ mọi mã rơi vào 2 nhóm báo lỗi.
- ⇒ BE cần endpoint **tra mã theo bộ lọc hiện tại** (trả id khớp + mã ngoài danh sách + mã không tồn tại).

### 3.11 Phân trang (khuôn `V2BasePagination`)

Trái: `Hiển thị 1–20 / 127` (en dash; rỗng ⇒ `Hiển thị 0–0 / 0`) · phải: `Số dòng/trang:` [20 ▾ 20/50/100] đứng **trước** dãy `« 1 2 3 … »`. Đổi số dòng ⇒ về trang 1.

---

## 4. Thao tác ghi

### 4.1 Mô hình dữ liệu + quy tắc

- Bảng nối `product_business_catalogs (product_id, company_id, job_cluster_id)` UNIQUE 3 cột, **chỉ lưu Tiểu mục** (A6). `company_id` gán tay = công ty đang đăng nhập.
- **Một hàng nằm được ở NHIỀU tiểu mục** (§33a-1, §33b); chỉ gán ở **cấp lá** (§33a-2).
- Popup chỉ ghi `product_business_catalogs`, **KHÔNG sinh/đổi dòng `product_company_coefficients`** ⇒ xếp catalog không đổi giá ERP (G4).
- Gỡ nhánh **cuối cùng** được, không cảnh báo (C5: màn Đang KD không còn bắt buộc catalog). Hệ quả cố ý: lần sau lưu tab *Quản trị* của form sẽ bị C5-a chặn tới khi xếp lại.
- Catalog ghi được từ **2 cửa, 2 quyền**: popup (1655) và tab *Quản trị hàng hoá* của form (1652).

### 4.2 Giỏ chờ (§33a-7, §33d) — gom, bấm Lưu một lần

**Bấm *Thêm vào tiểu mục* / *Gỡ khỏi tiểu mục*** (`lamCat`):

| Điều kiện | Kết quả |
|---|---|
| Chưa chọn tiểu mục | toast cảnh báo **"Chưa chọn Tiểu mục"** |
| Chưa tick | toast cảnh báo **"Chưa chọn hàng hoá nào"** |
| > 100 | toast trần (§3.9) |
| OK | tạo **1 lượt** (lot) gồm các cặp (mã × tiểu mục đang chọn × kiểu them/go); cặp trùng đang có trong giỏ bị **thay** bằng cặp mới; xoá tick; cây + tab + footer vẽ lại; toast thành công: **`Đã đưa N hàng hoá vào "<Tiểu mục>" — bấm Lưu để ghi lại`** / **`Đã gỡ N hàng hoá khỏi "<Tiểu mục>" — bấm Lưu để ghi lại`** |

- Giỏ gom được **nhiều tiểu mục khác nhau** (đổi tiểu mục giữa các lượt) ⇒ payload Lưu là danh sách (product × job_cluster × kiểu), **không** phải 1 tiểu mục (xem §6 B1).
- Footer trái: rỗng ⇒ **"Chưa có thay đổi nào"**; có ⇒ `Đang chờ lưu: +<t> · −<g>` (`+t` xanh `#15803d` đậm, `−g` đỏ `#b91c1c` đậm; t/g đếm theo **cặp**).
- **Hoàn tác** (tertiary, icon xoay ngược, cách 12px, chỉ hiện khi giỏ có) ⇒ bỏ **cả lượt gần nhất** ⇒ toast **`Đã hoàn tác lượt gần nhất (N hàng hoá)`**.

**Lưu** (footer phải, primary ✓) (`luuCat`):
- Giỏ rỗng ⇒ toast cảnh báo **"Chưa có thay đổi nào để lưu"**.
- Ghi: `them` mà chưa có ⇒ insert (t++); `go` mà đang có ⇒ delete (g++); **trùng thì bỏ qua lặng lẽ, không đếm** (idempotent theo UNIQUE).
- Xong: xoá giỏ + tick, **popup VẪN MỞ** (làm tiếp được), cây/tab/footer vẽ lại, **lưới màn Dữ liệu hàng hoá công ty tải lại** (cột *Catalog kinh doanh* + công tắc *Chỉ hàng chưa xếp* đổi theo), toast thành công **`Đã lưu catalog: thêm <t> · gỡ <g> lượt xếp hàng hoá`** (t/g = số thay đổi thực sự ghi).

### 4.3 Gỡ hàng khỏi tiểu mục — cách làm trên UI

1. Chọn tiểu mục ở cây → tab **Hàng trong tiểu mục (N)** → tick (hoặc *Chọn tất cả N*, hoặc dán mã) → **Gỡ khỏi tiểu mục** (đỏ) → **Lưu**.
2. Hoặc ở form sửa hàng hoá, tab *Quản trị hàng hoá*: bỏ tick ở cột Tiểu mục / xoá dòng bảng nhánh (*Gỡ khỏi tiểu mục*) — ngoài phạm vi popup.
- **Không** có gỡ ở lưới danh sách (§33a-6). Gỡ **không** có hộp xác nhận riêng — an toàn nhờ giỏ chờ + Hoàn tác + Lưu.

### 4.4 Trùng lặp

- Tab Thêm **không liệt kê** hàng đã ở tiểu mục (tính cả giỏ) ⇒ không tick trùng được; dán mã của hàng đã có ⇒ báo *không nằm trong danh sách đang lọc*.
- Thêm rồi gỡ cùng cặp trong giỏ ⇒ cặp sau thay cặp trước (net). Lưu bỏ qua cặp không đổi.
- BE: `insertOrIgnore`/UNIQUE cho thêm; delete theo cặp cho gỡ — 2 người cùng xếp không lỗi, chỉ số đếm toast nhỏ hơn.

### 4.5 Đóng khi còn giỏ — popup *Thông tin chưa lưu* (khuôn `base-confirm-modal`, rộng 480px)

- Icon ⓘ cam (nền `#fff7ed`, chữ `#b45309`) · H3 **"Thông tin chưa lưu"** · mô tả **`Còn <N> lượt xếp chưa lưu`** (N = số **cặp** trong giỏ) · thân: **"Các lượt xếp hàng hoá vào tiểu mục chưa được lưu. Có chắc chắn muốn thoát?"**
- Nút: [**Thoát**] (đỏ `btn-xoa`, bỏ giỏ + đóng popup) · [**Ở lại**] (tertiary). ✕ = Ở lại.
- Cả ✕ header lẫn nút **Đóng** footer đều đi qua kiểm tra này. Theo skill `unsaved-changes` ⇒ `unsavedModalMixin`.

### 4.6 Dấu hiệu "đã xếp"

Không có badge "Đã xếp" riêng. Thể hiện bằng: (1) hàng nằm ở tab *Hàng trong tiểu mục* hay *Thêm*; (2) cột **Catalog đang xếp** (đã lưu); (3) số đếm trên cây + số ở nhãn tab (tính cả giỏ); (4) footer giỏ chờ.

---

## 5. Validate / ca biên (tổng hợp câu chữ nguyên văn)

| Ca | Câu / hành vi |
|---|---|
| Bấm Thêm/Gỡ chưa chọn tiểu mục | `Chưa chọn Tiểu mục` (cảnh báo) |
| Bấm Thêm/Gỡ chưa tick | `Chưa chọn hàng hoá nào` (cảnh báo) |
| Vượt 100 khi tick | ô tự bỏ tick + `Mỗi lượt chỉ xếp tối đa 100 mã hàng — hãy Lưu lượt này rồi chọn tiếp` |
| Chọn tất cả > 100 | `Đã chọn 100/<N> hàng hoá — mỗi lượt tối đa 100 mã, Lưu xong chọn tiếp phần còn lại` |
| Chọn tất cả ≤ 100 | `Đã chọn tất cả <N> hàng hoá đang lọc` |
| Lưu giỏ rỗng | `Chưa có thay đổi nào để lưu` |
| Lưu xong | `Đã lưu catalog: thêm <t> · gỡ <g> lượt xếp hàng hoá` |
| Hoàn tác | `Đã hoàn tác lượt gần nhất (<N> hàng hoá)` |
| Dán rỗng | `Chưa dán mã nào` |
| Dán có mã lạ | toast `<t> mã không tồn tại trong hệ thống` |
| Đóng còn giỏ | popup *Thông tin chưa lưu* (§4.5) |
| Cây không khớp | `Không có nút nào khớp` |
| BE (đề xuất, chưa có câu trong mockup) | không có 1655 ⇒ 403; tiểu mục không thuộc cây mới (H3) / không tồn tại ⇒ 422; hàng không có dòng trạng thái ở công ty mình ⇒ 422 (hoặc bỏ qua); > trần ⇒ 422 |

---

## 6. Mâu thuẫn + việc phải chốt

### 6.1 Mâu thuẫn giữa các bản — đã xử lý theo bản muộn

| # | Chỗ lệch | Lấy |
|---|---|---|
| M1 | §33d: tab *Thêm* trước · §33j-5: *Hàng trong tiểu mục* trước | §33j-5 (tab 1 = Trong; lối B vào thẳng Thêm) |
| M2 | §33j-1: 10 cột có *Công ty quản lý* · §36f: 12 cột, bỏ *Công ty quản lý*, thêm STT/Ảnh/Thông số | §36f (12 cột §3.6) |
| M3 | §33j-6: 10 ô nâng cao · §33n-4 bỏ ĐVT · §36f bỏ Công ty quản lý | **8 ô** (§3.5) |
| M4 | §33i-6: cần `assign-by-filter` · §33j-2: trần 100 | trần 100 ⇒ gửi id (yeu-cau-ghi §1.6) |
| M5 | §33i-5 / §33e: gỡ nhánh cuối làm hàng rời màn KD · C5 (04/10) | C5: gỡ thoải mái, không cảnh báo |
| M6 | Comment mockup "cấp 4 có chấm ●" · §33u: số `1.1.1` | §33u (số thứ tự, không chấm) |
| M7 | Comment HTML màn kho: "Hàng đang KD chỉ hiện hàng ĐÃ xếp catalog" | lỗi thời theo C5 — bỏ qua |
| M8 | design §33c/§33l còn tên nút *Xếp vào cụm…* | §33w: **Xếp vào tiểu mục…** |

### 6.2 Việc UI thuần — tự chốt theo khuôn (ghi lại, không cần hỏi)

| # | Điểm | Đề xuất tự chốt |
|---|---|---|
| U1 | Ô *Trạng thái* hiện ở cả 2 tab nhưng mockup **chỉ lọc ở tab Thêm** (tab Trong chọn vẫn không lọc — lỗi mockup) | Áp lọc Trạng thái ở **cả 2 tab** (công tắc *Chỉ hàng chưa xếp* vẫn chỉ ở tab Thêm vì ở tab Trong vô nghĩa) |
| U2 | Popup lọc ngay khi gõ, không có nút *Tìm kiếm* | gọi API có debounce (~400ms) cho ô tìm; select đổi là gọi ngay; tránh 2 request (bẫy `hrm-list-page-2-loi-bo-loc-am-tham`) |
| U3 | *Làm mới* không xoá tick | giữ như mockup (tick là việc đang làm dở, không phải bộ lọc) |
| U4 | Chữ "lượt": footer/toast Lưu/hộp thoát đếm **cặp** ("Còn 2 lượt xếp"), còn Hoàn tác "lượt gần nhất" là **một lần bấm** | giữ nguyên văn mockup (đã đo §33g), không đổi câu |
| U5 | Đếm cấp 1–3 = tổng các tiểu mục con (1 hàng ở 2 TM cùng chương đếm 2) | giữ cộng dồn — rẻ, khớp mockup; BE trả count theo `job_cluster_id`, FE cộng lên + cộng/trừ giỏ |
| U6 | sanCo (lối B) chỉ áp khi bấm TM **lúc đang ở tab Thêm**; ở tab Trong rồi đổi sang Thêm thì không tick lại | áp `sanCo` cả khi **đổi sang tab Thêm** lúc đã có TM — tránh "mất" bộ mã mang sang |
| U7 | "Tính chất hàng hóa" (hóa) vs "hoá" | dùng nhãn trùng ô lọc cùng tên ở màn Dữ liệu hàng hoá công ty |
| U8 | Không có quyền 1655 thì thanh hàng loạt của màn công ty chỉ còn *Bỏ chọn* | ẩn luôn cột ô tick của màn công ty khi không có 1655 (thanh không còn việc gì) — nếu màn đã có thao tác hàng loạt khác thì chỉ ẩn nút |
| U9 | Hoàn tác khi lượt mới đã **thay** cặp của lượt cũ (cùng mã × TM) ⇒ hoàn tác lượt mới không khôi phục cặp cũ | chấp nhận như mockup (ca hiếm: thêm rồi gỡ cùng hàng cùng TM) — hoặc lưu stack nguyên vẹn; chọn đơn giản |
| U10 | Popup có cuộn ngang + footer ghim | đo bằng Playwright: đáy footer = đáy modal, bảng cuộn ngang trong khung, khung ⋯ nổi trên cùng (`elementFromPoint`) |

### 6.3 Câu nghiệp vụ / kỹ thuật cần user chốt trước khi code

| # | Câu | Vì sao / đề xuất |
|---|---|---|
| **B1** | **Trần 100 tính theo LƯỢT hay theo LẦN LƯU?** Mockup cho gom nhiều lượt (mỗi lượt ≤ 100, có thể khác tiểu mục) rồi Lưu một lần ⇒ một lần Lưu có thể vài trăm cặp. Plan 2c-ghi lại ghi endpoint `assign`/`unassign` = `product_ids ≤ 100 × 1 job_cluster_id` — **không chở được giỏ nhiều tiểu mục + cả thêm lẫn gỡ** | Đề xuất: **1 endpoint `POST .../catalogs/sync`** nhận `{add:[{product_id, job_cluster_id}], remove:[…]}` trong 1 transaction, trần mỗi lần Lưu = **500 cặp** (hoặc giới hạn giỏ ≤ 100 cặp nếu user muốn đúng chữ "Lưu lượt này rồi chọn tiếp") |
| **B2** | **Nút khoá trong cây**: Lĩnh vực khoá (status 2) mockup vẫn hiện 🔒 và **vẫn xếp được**; Chương/Mục/Tiểu mục khoá (status 0) mockup không thể hiện | Đề xuất: hiện cả nhánh khoá kèm 🔒 (để thấy hàng đang nằm ở đó và **gỡ** được), nhưng **chặn THÊM** vào tiểu mục thuộc nhánh có cấp nào khoá (nút Thêm ẩn/BE 422) |
| **B3** | **Trạng thái 4 "Ngừng kinh doanh"** (G6, chốt sau mockup): popup có liệt kê hàng ngừng KD không, ô lọc Trạng thái có thêm lựa chọn thứ 5 không | Đề xuất: có liệt kê (nguồn = "mọi trạng thái"), thêm lựa chọn *Ngừng kinh doanh*; cho xếp/gỡ bình thường (catalog không phải thông tin quản trị bị khoá 423) — cần user xác nhận |
| **B4** | **Nguồn "Thông số cơ bản"**: mockup dùng mẫu theo Loại sản phẩm; thật là `attribute_products` (thuộc tính của tab *Thông số kỹ thuật*) — lấy **mọi** thuộc tính hay chỉ thuộc tính *bắt buộc* / *in tem*; thứ tự; ghép đơn vị | Đề xuất: mọi thuộc tính có giá trị, thứ tự theo `attributes.position`, ghép `giá trị + đơn vị`; BE trả chuỗi tóm tắt (cắt ~10 dòng) |
| B5 | Hàng có `products.status = 0` (ERP đã xoá/khoá) nhưng còn dòng công ty | liên quan tồn nhỏ 2-C2; đề xuất **loại khỏi popup** |
| B6 | Đếm trên cây với 45.890 hàng: đếm theo **mọi trạng thái** của công ty (như mockup) | mặc định theo mockup; ghi lại để khỏi hỏi lại |

(B1–B4 hỏi lần lượt từng câu kèm hệ quả, theo quy tắc `hoi-het-ton-truoc-khi-code`.)

---

## 7. Gợi ý BE/FE (để lập C3.2/C3.3, chưa phải lệnh code)

- **Cây**: `GET master-data/products/catalogs/tree` — Lĩnh vực (gồm status) › Chương có `internal_business_scope_id` › Mục › Tiểu mục, kèm `product_count` theo `job_cluster_id` cho công ty đang đăng nhập (1 query `GROUP BY job_cluster_id`, không N+1).
- **Danh sách hàng**: `GET .../catalogs/products?job_cluster_id=&tab=in|out&keyword=&status=&unassigned_only=&<8 lọc>&page=&per_page=` — `in` = `whereExists` bảng nối, `out` = `whereNotExists`; eager load ảnh, ĐVT cơ bản, loại SP, thương hiệu, thuộc tính (tóm tắt), danh sách nhánh (cột *Catalog đang xếp*). FE trừ/cộng giỏ chờ phía client (hàng trong giỏ vẫn nằm trang BE cũ ⇒ cần gửi kèm `pending_add_ids`/`pending_remove_ids` cho TM đang xem, hoặc lọc phía FE — chốt khi code).
- **Chọn tất cả N**: `GET …/products/ids` cùng bộ lọc, `limit 100`.
- **Dán mã**: `POST …/products/match-codes` cùng bộ lọc ⇒ `{matched_ids, outside_filter[], not_found[]}`.
- **Lưu**: theo B1.
- Mọi endpoint: gate **1655**, `company_id` = công ty đang đăng nhập, kiểm hàng có dòng trạng thái ở công ty mình, kiểm tiểu mục thuộc cây mới (H3).
- E2E: có + không quyền 1655 (nút ẩn + 403), trần 100, Hoàn tác, Lưu đổi lưới, cảnh báo thoát, footer ghim, 12 cột đúng thứ tự, KHÔNG sinh dòng `product_company_coefficients` mới (G4).
