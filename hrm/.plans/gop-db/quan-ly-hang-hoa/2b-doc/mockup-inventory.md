# Kiểm kê mockup — 4 màn danh sách hàng hoá + Form hàng hoá

> Nguồn: `HRM/.plans/gop-db/quan-ly-hang-hoa/man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` (7.428 dòng, ~460KB).
> Viết ngày 04/10/2026 để phục vụ phase 2b (CHỈ ĐỌC). Thao tác ghi dữ liệu được gắn **[GHI]**.
> Số dòng `Lxxxx` là dòng trong file mockup.

---

## 0. Khung chung (dùng cho cả 4 màn)

### 0.1 Topbar + menu

- Topbar: nhãn phân hệ **DANH MỤC**; ô chọn **"Đang làm việc tại"** (`#cty-sel`) — đổi công ty là mọi màn vẽ lại theo công ty đó (trạng thái hàng hoá tính theo từng công ty).
- Danh sách công ty (`CTY`, đúng thứ tự): TÂN PHÁT · ETEK POWER · ETEK GREEN · ETEK · TÂN PHÁT SG · CN HẢI PHÒNG · CN VINH.
- Mockup **không có breadcrumb**; tên màn lấy từ nhãn sidebar + tiêu đề card danh sách.
- Thứ tự sidebar (L833–L848): Ghi chú & sơ đồ luồng │ Chính sách giá bán nội bộ · **Kho dữ liệu hàng hoá** · **Dữ liệu hàng hoá công ty** │ **Hàng hoá nhập thông tin** · **Hàng đang kinh doanh** · Yêu cầu tính giá · Phiếu tính giá. Badge đếm số trên menu **đã bỏ** (29/09).
- Màn Form mở ra thì menu sáng mục `Hàng hoá nhập thông tin` (`navMap.form = 'nav-l1'`).

### 0.2 Khuôn bộ lọc (khuôn `V2BaseSmartFilterPanel`)

- Card 1, hàng tiêu đề: `[icon phễu] <tiêu đề bộ lọc>` … nút **Cài đặt bộ lọc** (secondary, icon bánh răng — trong mockup **không có handler**) + nút **Tìm kiếm nâng cao** (secondary, icon 3 vạch; bấm thì đổi chữ thành **"Ẩn tìm kiếm nâng cao"**, bung/thu khối `.adv`).
- Hàng 1: ô tìm nhanh (placeholder giống nhau ở cả 4 màn: **"Tìm theo mã, tên hàng hoá, model, barcode"**; mockup tìm trong `code + name + model + bar`) → [công tắc lọc nhanh nếu có] → **Tìm kiếm** (primary, icon kính lúp) → **Làm mới** (tertiary, icon xoay vòng).
- Ô lọc nâng cao: **toàn bộ là select chọn 1, KHÔNG nhãn ngoài** — nhãn nằm ở option rỗng đầu tiên (chưa chọn: chữ xám `.trong`). Không có ô chọn nhiều, không có ô ngày, không có ô text trong bộ lọc nâng cao.
- Mặc định: khối nâng cao **thu gọn**, mọi ô trống, công tắc tắt.

### 0.3 Khuôn bảng (`veBangDS`, L2786)

- Card 2, hàng tiêu đề: `[icon] <Tiêu đề danh sách>` … các nút … nút vuông **Cấu hình cột hiển thị** (tertiary, `title="Cấu hình cột hiển thị"`, icon lưới cột).
- Thanh cuộn ngang phụ ở TRÊN bảng (`.top-scroll`, bề rộng đồng bộ theo `scrollWidth` thật).
- Cột dính trái (`dinh`): ô tick (nếu có) · STT · Ảnh · Mã hàng · Tên hàng hoá; cột dính cuối có bóng đổ phải.
- Căn: giữa (`c`) = STT, Ảnh, Trạng thái, Hành động; phải (`r`) = % VAT, Giá vốn, Giá bán lẻ, SL tồn kho tối thiểu.
- STT đánh số **liên tục qua các trang** (không reset mỗi trang).
- Ô rỗng → `—` (riêng *Công ty đang kinh doanh* rỗng thì để TRỐNG).
- Không có dòng → `Không có hàng hoá nào` (căn giữa, xám #6b7280).
- **Mã hàng**: link `.v2-cell-link` (#28539d, 12px, không gạch chân, hover gạch chân) → **mở Form hàng hoá** (`moForm(code)`), ở cả 4 màn. Không còn dòng barcode phụ dưới mã.
- **Ảnh**: ô thumbnail 30×30, nền #eef2f7, viền #e5e7eb, icon ảnh xám.
- Phân trang (khuôn `V2BasePagination`): trái `Hiển thị x–y / z` (dấu gạch en) … `Số dòng/trang:` [20|50|100] (mặc định 20) … `« 1 2 … »` (>9 trang thì rút gọn bằng `…`).
- Đổi số dòng/trang → về trang 1.

### 0.4 Popup "Cấu hình cột hiển thị" (`#mask-cot`)

- Tiêu đề **Cấu hình cột hiển thị**, phụ đề *"Bỏ tích để ẩn cột khỏi bảng danh sách"*.
- Danh sách checkbox mọi cột của màn đó; cột `luon` (STT, Hành động) bị disable kèm chữ xám *"(luôn hiện)"*.
- Footer: **Mặc định** (tertiary — tick lại đúng bộ `mac`+`luon`; ⚠️ KHÔNG gồm cột `owner` được cộng thêm mặc định ở `tong/kho`) · **Lưu** (primary) · **Đóng**.
- Lưu xong toast *"Đã lưu cấu hình cột — hiển thị N cột"*. Cấu hình là của người xem (lưu cục bộ/cấu hình người dùng — không ghi dữ liệu nghiệp vụ).

### 0.5 Bảng đăng ký cột `COT` (L2655) — dùng chung, mỗi màn loại bớt bằng `khong`

| # | key | Tiêu đề | Rộng | Căn | Mặc định (`mac`) | Dính | Loại khỏi màn | Dữ liệu / định dạng |
|---|-----|---------|------|-----|------------------|------|---------------|---------------------|
| 1 | `stt` | STT | 44px | giữa | luôn hiện | ✓ | pp | số thứ tự toàn cục |
| 2 | `anh` | Ảnh | 52px | giữa | ✓ | ✓ | — | thumbnail ảnh đại diện |
| 3 | `code` | Mã hàng | 150px | | ✓ | ✓ | — | link → Form |
| 4 | `name` | Tên hàng hoá | 250px | | ✓ | ✓ | — | text |
| 5 | `model` | Model | 120px | | ✓ | | — | text |
| 6 | `tinhChat` | Tính chất hàng hoá | 140px | | ✓ | | — | cấp 1 cây phân loại |
| 7 | `nhomCN` | Nhóm chức năng | 130px | | ✓ | | — | cấp 2 |
| 8 | `nhomSP` | Nhóm sản phẩm | 140px | | ✓ | | — | cấp 3 |
| 9 | `type` | Loại sản phẩm | 180px | | ✓ | | — | cấp 4 (chỉ tên, không lặp đường dẫn) |
| 10 | `brand` | Thương hiệu | 120px | | ✓ | | — | text |
| 11 | `hangSX` | Hãng sản xuất | 150px | | ✓ | | — | text |
| 12 | `cat` | Catalog kinh doanh | 300px | | ✓ | | pp, **l1, tong** | chip tên Tiểu mục (xem 0.6) |
| 13 | `st` | Trạng thái | 150px | giữa | ✓ | | pp | badge trạng thái theo công ty đang làm việc |
| 14 | `bar` | Barcode | 140px | | | | — | text |
| 15 | `unit` | ĐVT | 70px | | | | — | ĐVT cơ bản |
| 16 | `xuatXu` | Xuất xứ | 120px | | | | — | text |
| 17 | `codeDH` | Code đặt hàng | 140px | | | | — | text |
| 18 | `tenEn` | Tên tiếng Anh | 220px | | | | — | text |
| 19 | `vat` | % VAT | 80px | phải | | | — | `8%` |
| 20 | `von` | Giá vốn | 130px | phải | | | **l3, pp, tong** | số `42,500,000` (dấu phẩy ngăn nghìn) — **số nhạy cảm, phải gate quyền xem giá vốn ở máy chủ** |
| 21 | `ban` | Giá bán lẻ | 130px | phải | | | — | = loại giá "Bán lẻ" của bảng giá |
| 22 | `baoHanh` | Bảo hành | 110px | | | | — | `12 tháng` / `24 tháng` (theo công ty) |
| 23 | `tonToiThieu` | SL tồn kho tối thiểu | 160px | phải | | | — | số (theo công ty) |
| 24 | `owner` | Công ty quản lý | 160px | | (thêm mặc định ở tong, kho, pp) | | — | tên công ty tạo ra hàng hoá |
| 25 | `ctyKD` | Công ty đang kinh doanh | 280px | | ✓ | | pp, **l1, l3, kho** | chip xanh lá tên công ty có trạng thái `kd`; 2 chip đầu + chip `+N` (tooltip liệt kê `• tên` từng dòng); rỗng = để trống |
| 26 | `nguoi` | Người nhập thông tin | 170px | | | | — | tên NV |
| 27 | `sua` | Ngày sửa | 110px | | | | — | `dd/mm/yyyy` |
| 28 | `actions` | Hành động | 110px (màn kho: 170px) | giữa | luôn hiện | | pp | xem từng màn |

Thứ tự cột hiển thị luôn theo thứ tự bảng trên (kể cả `owner` cộng thêm ⇒ nằm sau `st`, trước `ctyKD`/`actions`).

### 0.6 Định dạng ô đặc biệt

| Ô | Hiển thị |
|---|----------|
| Trạng thái (có) | badge `V2BaseBadge`: chữ = màu, nền `rgba(màu,.1)`, viền `rgba(màu,.2)` |
| Trạng thái (công ty chưa dùng mã này — chỉ ở màn Kho dữ liệu) | chữ xám `Chưa sử dụng` (`.cat-trong` #9aa7b8, 11.5px) |
| Catalog (có nhánh) | chip `.cat-chip` (nền rgba(10,153,167,.08), viền rgba(10,153,167,.2), chữ #0a7c88, 11.5px) ghi **tên Tiểu mục** của nhánh đầu; rê chuột tooltip đủ 4 cấp `Lĩnh vực › Chương › Mục › Tiểu mục`. Nhiều nhánh: thêm chip viền đứt `+N`, tooltip liệt kê `• <đường dẫn>` các nhánh còn lại |
| Catalog (chưa có) | chữ xám `Chưa xếp catalog` |
| Công ty đang KD | `.cty-chip` nền rgba(22,163,74,.08), viền rgba(22,163,74,.2), chữ #15803d |

### 0.7 Bảng trạng thái (`ST`, L2276) — theo TỪNG công ty

| key | Tên | Màu |
|-----|-----|-----|
| `nhap` | Đang nhập thông tin | `#64748B` (xám) |
| `cho` | Chờ tính giá bán | `#D97706` (cam) |
| `dang` | Đang tính giá | `#2563EB` (xanh dương) |
| `kd` | Đang kinh doanh | `#16A34A` (xanh lá) |
| (không có) | Chưa sử dụng | chữ xám #9aa7b8, không badge |

### 0.8 Menu ⋮ của dòng (`menuHtml`, L2499)

| Kiểu | Mục (thứ tự) | Ghi chú |
|------|--------------|---------|
| `nhap` (màn l1) | **Sửa** (→ Form) · **Sao chép** [GHI] · **Xoá** (đỏ, `is-danger`) [GHI] | |
| `kd` (các màn khác) | **Xem** (→ Form) · **Khóa** [GHI] · **In tem barcode** · **Lịch sử** | "Xem" mở CÙNG form sửa (mockup chưa có chế độ chỉ đọc riêng) |

---

## 1. Màn `sc-tong` — Kho dữ liệu hàng hoá

**Là gì:** toàn bộ hàng hoá của **mọi công ty** (thật: 45.890 mã), mọi trạng thái. Tra cứu chung + lối lấy hàng công ty khác về dùng. Không có Xây dựng catalog.

### 1.1 Tiêu đề
- Menu: **Kho dữ liệu hàng hoá** (icon màu #a78bfa).
- Card bộ lọc: **Bộ lọc kho dữ liệu hàng hoá**.
- Card danh sách: **Kho dữ liệu hàng hoá** + phụ đề xám *"Toàn bộ hàng hoá của mọi công ty"* (icon tím #7c3aed).

### 1.2 Nút
| Vị trí | Nút | Kiểu / icon | Hành vi |
|--------|-----|-------------|---------|
| Bộ lọc | Cài đặt bộ lọc | secondary · bánh răng | (chưa có handler) |
| Bộ lọc | Tìm kiếm nâng cao | secondary · 3 vạch | bung/thu |
| Bộ lọc | Tìm kiếm | primary · kính lúp | lọc (mockup lọc ngay khi gõ — `oninput`) |
| Bộ lọc | Làm mới | tertiary · xoay vòng | xoá ô tìm, tắt công tắc, xoá ô nâng cao |
| Danh sách | Xuất Excel | secondary · mũi tên tải xuống | (chưa có handler) |
| Danh sách | Cấu hình cột | tertiary vuông | popup 0.4 |
| Thanh hàng loạt | **Lấy về công ty** [GHI] | primary · tải xuống | lấy các mã đã tick mà công ty chưa dùng → trạng thái *Đang nhập thông tin* |
| Thanh hàng loạt | Bỏ chọn | tertiary | bỏ tick hết |
| Dòng — công ty CHƯA dùng | **Lấy về** [GHI] | primary · tải xuống | `layHangVe` → st = nhap; toast *"Đã lấy <mã> về <cty> — trạng thái Đang nhập thông tin"* |
| Dòng — công ty ĐANG dùng | **Xem** | tertiary · con mắt | mở Form |

### 1.3 Bộ lọc
- Tìm nhanh: *"Tìm theo mã, tên hàng hoá, model, barcode"*.
- Công tắc: **"Chỉ hàng công ty chưa dùng"** (mặc định tắt) — lọc `!st[CUR]`.
- Nâng cao (10 ô, select chọn 1):

| # | Nhãn | Nguồn option (mockup) | Mockup lọc thật? |
|---|------|------------------------|------------------|
| 1 | Công ty quản lý | danh sách 7 công ty | ✓ (`tong-cty`, so `owner`) |
| 2 | Tình trạng sử dụng | `Công ty đang dùng` / `Công ty chưa dùng` | ✓ (`tong-dung`) |
| 3 | Tính chất hàng hóa | DM Tính chất hàng hoá | ✗ |
| 4 | Nhóm chức năng | DM Nhóm chức năng | ✗ |
| 5 | Nhóm sản phẩm | DM Nhóm sản phẩm | ✗ |
| 6 | Loại sản phẩm | DM Loại sản phẩm | ✗ |
| 7 | Thương hiệu | DM Thương hiệu | ✗ |
| 8 | Hãng sản xuất | DM Hãng sản xuất | ✗ |
| 9 | Xuất xứ | DM Xuất xứ | ✗ |
| 10 | Model | DM Model | ✗ |

### 1.4 Cột (26 cột khả dụng, 15 hiện mặc định + ô tick)
Mặc định (theo thứ tự): ☐ · STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Trạng thái · **Công ty quản lý** · **Công ty đang kinh doanh** · Hành động.

Bật thêm được (11): Barcode · ĐVT · Xuất xứ · Code đặt hàng · Tên tiếng Anh · % VAT · Giá bán lẻ · Bảo hành · SL tồn kho tối thiểu · Người nhập thông tin · Ngày sửa.
Không có: Catalog kinh doanh, Giá vốn.

Cột Trạng thái = trạng thái của **công ty đang làm việc**; chưa dùng → *Chưa sử dụng*.

### 1.5 Badge / dòng nhắc
- 4 badge ở 0.7 + chữ *Chưa sử dụng*. Không có dòng nhắc cam.

### 1.6 Chọn dòng / hàng loạt
- Cột ô tick đầu bảng (dính), ô tick tiêu đề = chọn tất cả **trong trang đang hiện**.
- Có ≥1 dòng tick → hiện thanh xanh `.kho-bar` (nền #ecfdf5, viền #a7f3d0, chữ #065f46): *"Đã chọn **N** hàng hoá"* · [Lấy về công ty] [GHI] · [Bỏ chọn].
- Toast khi toàn mã đã dùng: *"Các hàng hoá đã chọn đều đang được công ty dùng rồi"*.

---

## 2. Màn `sc-kho` — Dữ liệu hàng hoá công ty

**Là gì:** hàng hoá **của riêng công ty đang đăng nhập**, đủ 4 trạng thái (gồm cả hàng lấy về từ công ty khác — phân biệt bằng cột Công ty quản lý). Nơi duy nhất có Xây dựng catalog và nút Tính giá.

### 2.1 Tiêu đề
- Menu: **Dữ liệu hàng hoá công ty** (icon #38bdf8).
- Card bộ lọc: **Bộ lọc dữ liệu hàng hoá công ty**.
- Card danh sách: **Dữ liệu hàng hoá công ty** (icon khối hộp #0a99a7).

### 2.2 Nút
| Vị trí | Nút | Kiểu / icon | Hành vi |
|--------|-----|-------------|---------|
| Bộ lọc | Cài đặt bộ lọc · Tìm kiếm nâng cao · Tìm kiếm · Làm mới | như 0.2 | Làm mới: xoá tìm, tắt công tắc, xoá 4 ô catalog + ô nâng cao |
| Danh sách | **Xây dựng catalog** [GHI] | primary · sơ đồ nhánh | mở popup *Xây dựng catalog kinh doanh* (ngoài phạm vi) |
| Danh sách | Xuất Excel | secondary · tải xuống | (chưa có handler) |
| Danh sách | Cấu hình cột | tertiary vuông | |
| Thanh hàng loạt | **Xếp vào tiểu mục…** [GHI] | primary · dấu + | mở popup Xây dựng catalog mang theo các mã đã tick |
| Thanh hàng loạt | Bỏ chọn | tertiary | |
| Dòng có st = `cho` hoặc `dang` | **Tính giá** [GHI] (primary, icon $) + menu ⋮ kiểu `kd` | | mở Phiếu tính giá đang dở / phiếu mới từ Yêu cầu đang chờ; không có → toast *"Hàng hoá chưa nằm trong yêu cầu tính giá nào — lập yêu cầu ở màn Hàng hoá nhập thông tin"* |
| Dòng khác (kể cả `nhap`) | menu ⋮ kiểu `kd`: Xem · Khóa [GHI] · In tem barcode · Lịch sử | | |

Quy ước: nút không dùng được thì **ẩn hẳn**, không disable (Tính giá chỉ render ở 2 trạng thái).

### 2.3 Bộ lọc
- Hàng 1: tìm nhanh + công tắc **"Chỉ hàng chưa xếp catalog"** (mặc định tắt; lọc hàng không có nhánh nào ở công ty đang làm việc).
- Hàng 2 — **4 ô catalog LUÔN HIỆN** (không giấu trong nâng cao), lọc dây chuyền, đổi cấp trên là xoá sạch cấp dưới:

| # | Nhãn trong ô | Nguồn | Khoá khi |
|---|--------------|-------|----------|
| 1 | Lĩnh vực Công ty kinh doanh | `internal_business_scopes` (8 dòng); dòng bị khoá hiện tiền tố 🔒 (vd `🔒 Khác`) | — |
| 2 | Chương | con của Lĩnh vực đã chọn | chưa chọn cấp 1 → nhãn *"Chương — chọn cấp trên trước"* |
| 3 | Mục | con của Chương | *"Mục — chọn cấp trên trước"* |
| 4 | Tiểu mục | con của Mục | *"Tiểu mục — chọn cấp trên trước"* |

Khớp khi **có ít nhất 1 nhánh** của hàng hoá (của công ty đang làm việc) khớp các cấp đã chọn.

- Nâng cao (12 ô):

| # | Nhãn | Nguồn option | Mockup lọc thật? |
|---|------|--------------|------------------|
| 1 | Trạng thái | Đang nhập thông tin / Chờ tính giá bán / Đang tính giá / Đang kinh doanh | ✓ (`kho-st`) |
| 2–8 | Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Xuất xứ | danh mục tương ứng | ✗ |
| 9 | Công ty quản lý | 7 công ty | ✗ |
| 10 | Người nhập thông tin | DS nhân viên | ✗ |
| 11 | Model | DM Model | ✗ |
| 12 | Bảo hành | `12 tháng` / `24 tháng` | ✗ |

Comment L1230: các trường nâng cao được bật/tắt ở popup **Cài đặt bộ lọc**.

### 2.4 Cột (27 khả dụng, 15 mặc định + ô tick)
Mặc định: ☐ · STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · **Catalog kinh doanh** · Trạng thái · **Công ty quản lý** · Hành động (170px).

Bật thêm được (12): Barcode · ĐVT · Xuất xứ · Code đặt hàng · Tên tiếng Anh · % VAT · **Giá vốn** (gate quyền) · Giá bán lẻ · Bảo hành · SL tồn kho tối thiểu · Người nhập thông tin · Ngày sửa.
Không có: Công ty đang kinh doanh.

### 2.5 Badge / dòng nhắc
- Đủ 4 badge trạng thái; ô catalog `Chưa xếp catalog` xám. Không có dòng nhắc cam.

### 2.6 Chọn dòng / hàng loạt
- Như màn Kho dữ liệu: ô tick dính đầu bảng + chọn tất cả trong trang; thanh xanh *"Đã chọn **N** hàng hoá"* · [Xếp vào tiểu mục…] [GHI] · [Bỏ chọn].

---

## 3. Màn `sc-l1` — Hàng hoá nhập thông tin

**Là gì:** bước 1 — hàng hoá trạng thái **Đang nhập thông tin** của công ty đang đăng nhập.

### 3.1 Tiêu đề
- Menu: **Hàng hoá nhập thông tin** (icon #9aa7b8).
- Card bộ lọc: **Bộ lọc danh sách**.
- Card danh sách: **Hàng hoá nhập thông tin**.

### 3.2 Nút
| Vị trí | Nút | Kiểu / icon | Hành vi |
|--------|-----|-------------|---------|
| Bộ lọc | Cài đặt bộ lọc · Tìm kiếm nâng cao · Tìm kiếm · Làm mới | như 0.2 | (mockup Tìm kiếm/Làm mới không có handler) |
| Danh sách | **Xem hàng hoá Công ty khác** [GHI qua nút Chọn trong popup] | secondary · con mắt | popup hàng công ty khác chưa dùng → chọn → về *Đang nhập thông tin* |
| Danh sách | **Lập yêu cầu tính giá** [GHI] | secondary · tờ giấy | mở form Yêu cầu tính giá |
| Danh sách | **Tạo mới** [GHI] | primary · dấu + | mở Form trống |
| Danh sách | Cấu hình cột | tertiary vuông | |
| Dòng | menu ⋮ kiểu `nhap`: **Sửa** (→ Form) · Sao chép [GHI] · Xoá [GHI] (đỏ) | | |

⚠️ Màn này **không có nút Xuất Excel** (3 màn còn lại có).

### 3.3 Bộ lọc
- Tìm nhanh như 0.2. Không công tắc. Không hàng catalog.
- Nâng cao (11 ô — mockup không nối ô nào vào lọc):

| # | Nhãn | Nguồn |
|---|------|-------|
| 1–7 | Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Xuất xứ | danh mục |
| 8 | Công ty quản lý | 7 công ty |
| 9 | Công ty tạo hàng hoá | 7 công ty |
| 10 | Người nhập thông tin | DS nhân viên |
| 11 | Model | DM Model |

Không có ô Trạng thái (mọi dòng cùng 1 trạng thái).

### 3.4 Cột (26 khả dụng, 13 mặc định, KHÔNG có ô tick)
Mặc định: STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Trạng thái · Hành động.

Bật thêm được (13): Barcode · ĐVT · Xuất xứ · Code đặt hàng · Tên tiếng Anh · % VAT · **Giá vốn** · Giá bán lẻ · Bảo hành · SL tồn kho tối thiểu · Công ty quản lý · Người nhập thông tin · Ngày sửa.
Không có: Catalog kinh doanh, Công ty đang kinh doanh.

### 3.5 Badge
- Chỉ badge **Đang nhập thông tin** (#64748B). Không dòng nhắc.

### 3.6 Hàng loạt
- Không có chọn dòng / thao tác hàng loạt trên lưới (chọn hàng chỉ có trong popup Xem hàng hoá Công ty khác).

---

## 4. Màn `sc-l3` — Hàng đang kinh doanh

**Là gì:** bước 3 — hàng trạng thái **Đang kinh doanh** của công ty đang đăng nhập. Từ §35c (04/10) **KHÔNG bắt buộc catalog**: mọi hàng đang KD đều hiện, hàng chưa xếp catalog vẫn hiện.

### 4.1 Tiêu đề
- Menu: **Hàng đang kinh doanh** (icon cặp #2ecc9b).
- Card bộ lọc: **Bộ lọc danh sách**.
- Card danh sách: **Hàng đang kinh doanh**.

### 4.2 Nút
| Vị trí | Nút | Kiểu | Hành vi |
|--------|-----|------|---------|
| Bộ lọc | Cài đặt bộ lọc · Tìm kiếm nâng cao · Tìm kiếm · Làm mới | như 0.2 | Làm mới: xoá 4 ô catalog, tắt công tắc |
| Danh sách | Xuất Excel | secondary | (chưa có handler) |
| Danh sách | Cấu hình cột | tertiary vuông | |
| Dòng | menu ⋮ kiểu `kd`: Xem · Khóa [GHI] · In tem barcode · Lịch sử | | |

### 4.3 Bộ lọc
- **4 ô catalog ở HÀNG ĐẦU**, luôn hiện (giống màn kho, mục 2.3), nằm TRÊN hàng tìm nhanh.
- Hàng tìm nhanh + công tắc **"Chỉ hàng chưa xếp catalog"** (mặc định tắt). **Bật công tắc thì 4 ô catalog bị bỏ qua** (không còn ý nghĩa).
- Nâng cao (11 ô — mockup không nối vào lọc):

| # | Nhãn | Nguồn |
|---|------|-------|
| 1–7 | Tính chất hàng hóa · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Xuất xứ | danh mục |
| 8 | Công ty quản lý | 7 công ty |
| 9 | Công ty tạo hàng hoá | 7 công ty |
| 10 | % VAT | `0%` / `8%` / `10%` |
| 11 | Có giá bán | `Đã có giá bán` / `Chưa có giá bán` |

### 4.4 Cột (26 khả dụng, 14 mặc định, KHÔNG có ô tick)
Mặc định: STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · **Catalog kinh doanh** · Trạng thái · Hành động.

Bật thêm được (12): Barcode · ĐVT · Xuất xứ · Code đặt hàng · Tên tiếng Anh · % VAT · Giá bán lẻ · Bảo hành · SL tồn kho tối thiểu · Công ty quản lý · Người nhập thông tin · Ngày sửa.
**Không có Giá vốn** (chốt 23/09 — số nhạy cảm), không có Công ty đang kinh doanh.

### 4.5 Badge / dòng nhắc cam
- Badge **Đang kinh doanh** (#16A34A); catalog trống → `Chưa xếp catalog`.
- **Dòng nhắc cam** `.kho-nhac` (nền #fff7ed, viền #fed7aa, chữ #9a3412, icon ⓘ tròn), nằm giữa tiêu đề card và bảng, **chỉ hiện khi có ≥1 hàng KD chưa xếp catalog** (đếm trên toàn bộ hàng KD của công ty, không theo bộ lọc):
  - Công tắc tắt: *"Có **N** hàng hoá đang kinh doanh chưa xếp catalog — [lọc ra các hàng này]"* → bấm link = bật công tắc.
  - Công tắc bật: *"… — [xem tất cả hàng đang kinh doanh]"* → bấm = tắt công tắc.
  - Link: #0a7c88, đậm, hover gạch chân.

### 4.6 Hàng loạt
- Không có.

---

## 5. Form hàng hoá `sc-form`

### 5.1 Bố cục
1. Dải báo phạm vi `#bao-muon` (nền #f5f8fc, viền #e3ebf5, 12px) — chỉ hiện khi hàng do công ty KHÁC tạo: *"Hàng hoá do **<Công ty tạo>** tạo — chỉ khai được tab **Quản trị hàng hoá**."*
2. Card tab: **tab CHA** (segmented control kiểu iOS, viên trắng trượt):
   - **Thông tin hàng hoá** ⓘ *"Thông tin CHUNG của mã hàng — mọi công ty dùng chung một bản. Chỉ công ty tạo ra hàng hoá được sửa phần này."*
   - **Quản trị hàng hoá** ⓘ *"Dữ liệu RIÊNG của công ty đang làm việc (nhà cung cấp, chính sách kinh doanh, tồn kho tối thiểu, bảo hành, hệ số công nghệ, catalog kinh doanh). Mỗi công ty tự khai, không ảnh hưởng công ty khác."*
3. **Tab CON** (chỉ dưới tab cha *Thông tin hàng hoá*), dựng dạng STEP: vòng tròn số + đường nối; step đã qua hiện ✓; step đang mở nền #1abc9c; bấm được mọi step (không ép tuần tự):
   1. Thông tin chung (`data-i=0`) · 2. Thông số kỹ thuật (`1`) · 3. Mua hàng (`2`) · 4. Phân loại xe (`4`) · 5. Nhóm máy (`5`)
   - Tab cha *Quản trị hàng hoá* = 1 pane `data-i=3`, không có tab con.
4. Footer `.v2-footer`: **Lưu nháp** (tertiary) [GHI] · **Lưu** (primary) [GHI] · **Quay lại** (tertiary → màn l1).
- Form **không hiển thị Mã hàng hoá và Trạng thái** (bỏ §36b, 01/10).
- Tab **Giá bán đã gỡ** (27/09) — tính giá qua Yêu cầu tính giá → Phiếu tính giá.

### 5.2 Tab con 1 — Thông tin chung (`data-i=0`)

**Card "Thông tin hàng hoá"**
| Nhãn | Loại | Bắt buộc | Ghi chú |
|------|------|----------|---------|
| Tên hàng hoá | text, placeholder *"Nhập tên hàng hoá"* | * | col 4 |
| Model | select (*"Chọn model"*) + nút vuông **+** *"Thêm model"* | * | col 4 |
| Công ty quản lý | text **disabled** luôn (tự điền) | | col 4; không bị vòng phân quyền mở ra |
| Tên hàng thường gọi | text | | col 4 |
| Tên tiếng Anh | text | | col 4 |
| Barcode | text | | col 4 |
| Ghi chú | textarea | | col 12 |

**Card "Phân loại"** (`#khoi-phan-loai`, chọn cấp con → 3 cấp cha tự điền)
| Nhãn | Loại | Bắt buộc | ⓘ tooltip |
|------|------|----------|-----------|
| Tính chất hàng hoá | text disabled, placeholder *"Tự điền theo Loại sản phẩm"* | | *"Phân loại theo bản chất, vai trò của hàng hóa"* |
| Nhóm chức năng | như trên | | *"Phân loại theo chức năng hoặc hệ kỹ thuật chính"* |
| Nhóm sản phẩm | như trên | | *"Tập hợp các sản phẩm có cùng chức năng cơ bản"* |
| Loại sản phẩm | select (*"Chọn loại sản phẩm"*) + nút **+** *"Thêm loại sản phẩm"* (col 6) | * | *"Phân biệt theo kết cấu, nguyên lý hoặc đặc điểm kỹ thuật"* |
| Đặc tính sản phẩm | select: Hàng nhập khẩu / Hàng lắp ráp trong nước / Hàng gia công / Hàng thương mại (col 6, mặc định *Hàng nhập khẩu*) | | *"Xác định sản phẩm thuộc loại tiêu chuẩn hay có khả năng thay đổi theo nhu cầu khách hàng"* |

Tooltip lấy nguyên văn `CATALOG_TOOLTIPS` (`hrm-client/utils/product-classification.js`).

**Card "Nguồn gốc"** (4 ô col 3)
| Nhãn | Loại |
|------|------|
| Thương hiệu | select |
| Xuất xứ | select |
| Hãng sản xuất | select |
| Code đặt hàng | select (*"Chọn code đặt hàng"*) + nút **+** *"Thêm code đặt hàng"* |

**Card "Đơn vị tính"** — nút header **Thêm đơn vị tính** (secondary). Bảng:
| Cột | Loại |
|-----|------|
| Đơn vị * | select |
| Đơn vị cơ bản | radio (1 dòng duy nhất) |
| Hệ số quy đổi * | input số; dòng cơ bản = 1 và disabled |
| Quy đổi | text xám tự sinh: *"Đơn vị cơ bản"* / *"1 Bộ = 2 Cái"* |
| (xoá) | nút thùng rác (không có ở dòng cơ bản) |

**Card "Tài liệu kỹ thuật · Hình ảnh · Video"** (3 ô col 4)
| Nhãn | Loại |
|------|------|
| Tài liệu kỹ thuật | ô upload *"Chọn tệp PDF / Word"* |
| Hình ảnh | ô upload *"Chọn ảnh (tối đa 10 ảnh)"* |
| Video | *"Dán đường dẫn video"* |

→ Tab 1: **19 trường** (7 + 5 + 4 + bảng ĐVT 3 cột nhập + 3 upload).

### 5.3 Tab con 2 — Thông số kỹ thuật (`data-i=1`)

**Card "Thông số cơ bản"** — nút header **Thêm thông số**
| Nhãn | Loại |
|------|------|
| Trọng lượng (kg) | text/số |
| Kích thước (cm) | text, placeholder *"D × R × C"* |
| Định mức công lắp đặt | text/số |

Bảng thuộc tính: **Thuộc tính** (text, đến từ cấu hình) · **Giá trị** (input) · **Đơn vị thuộc tính** (select) · **Bắt buộc** (checkbox) · **In tem** (checkbox) · (xoá).

**Card "Phụ kiện tiêu chuẩn · Đặc điểm"**: Phụ kiện tiêu chuẩn (rich text, col 6) · Đặc điểm (rich text, col 6).

**4 card bảng hàng hoá con** (mỗi card có nút **Chọn hàng hoá**; rỗng → *"Chưa chọn hàng hoá nào"*):
| Card | Cột |
|------|-----|
| Công thức lắp ráp | Mã · Tên hàng hoá · ĐVT · Số lượng (phải) · Thành phần chính (giữa, checkbox) · (xoá) |
| Phụ kiện tuỳ chọn mua thêm | Mã · Tên hàng hoá · ĐVT · Số lượng · (xoá) |
| Vật tư phục vụ lắp đặt | Mã · Tên hàng hoá · ĐVT · Số lượng · (xoá) |
| Vật tư phục vụ sửa chữa – bảo dưỡng | Mã · Tên hàng hoá · (xoá) |

→ Tab 2: **5 trường** + 1 bảng thuộc tính + 4 bảng hàng hoá con.

### 5.4 Tab con 3 — Mua hàng (`data-i=2`)

**Card "Thông tin nhập mua"**: Tên khai báo hải quan (text) · HS Code (text) · SL tối thiểu nhập mua (số).

**Card "Thuế"**
| Nhãn | Loại | Bắt buộc |
|------|------|----------|
| % VAT | select (8% / 10% / 0% / 5%) + nút **+** *"Thêm thuế suất"* | * |
| Thuế nhập khẩu (không có CO) | select (*"Chọn % thuế"*, 0–20%) + nút + | |
| Thuế nhập khẩu (có CO) | select + nút + | |
| Thuế chống bán phá giá (%) | select + nút + | |
| Hệ số tính thuế BVMT | input, KHÔNG bắt buộc (đã bỏ checkbox "Tính thuế BVMT") | |

→ Tab 3: **8 trường**.

### 5.5 Tab cha — Quản trị hàng hoá (`data-i=3`)

**Card "Dữ liệu quản trị"** — phải header: *"Đang khai báo cho: <Công ty đang làm việc>"*
| Nhãn | Loại | ⓘ tooltip |
|------|------|-----------|
| Nhà cung cấp | **chọn nhiều** (chip) — col 6 | *"Các nhà cung cấp mà công ty đang mua mặt hàng này."* |
| Chính sách kinh doanh | select: Hàng kinh doanh chính / Hàng đặt theo yêu cầu | *"Xác định chính sách kinh doanh của doanh nghiệp với từng sản phẩm"* |
| SL tồn kho tối thiểu | số | *"Số lượng tồn kho tối thiểu công ty cần duy trì cho mặt hàng này — làm mốc theo dõi tồn kho để nhập bổ sung."* |
| Bảo hành | số | *"Thời gian bảo hành áp dụng khi bán mặt hàng này cho khách hàng, tính theo Đơn vị bảo hành."* |
| Đơn vị bảo hành | select: Ngày / Tháng / Năm | *"Đơn vị tính thời gian bảo hành: Ngày / Tháng / Năm."* |
| Hệ số công nghệ | số | *"Hệ số hưởng của kỹ thuật khi lắp đặt mặt hàng này — tự điền sang phiếu phân công lắp đặt."* |

**Card "Phân loại theo lĩnh vực kinh doanh \*"** — phải header: *"Khai riêng cho: <Công ty>"*
- 4 cột checkbox song song (col 3 mỗi cột), mỗi cột: tiêu đề + `*` + ⓘ + bộ đếm số đang chọn, ô tìm *"Tìm <tên cột>"*, danh sách gom theo tên cha (tiêu đề in đậm), cột chưa có cha → *"Chọn ở cột bên trái trước"*; mục khoá có 🔒.

| Cột | ⓘ tooltip |
|-----|-----------|
| Lĩnh vực Công ty kinh doanh * | *"Cấp 1 — lĩnh vực kinh doanh của công ty (danh mục Lĩnh vực Công ty kinh doanh)."* |
| Chương * | *"Cấp 2 — nhóm lớn trong một lĩnh vực."* |
| Mục * | *"Cấp 3 — nhóm chi tiết trong một chương."* |
| Tiểu mục * | *"Cấp 4 — cấp cuối của catalog, nơi xếp hàng hoá. Hàng hoá phải gắn tới Tiểu mục; một hàng hoá gắn được nhiều nhánh."* |

- Ghi chú dưới: *"Tick ở cột **Tiểu mục** là gắn hàng hoá vào nhánh đó — bỏ tick ở cột bên trái sẽ gỡ luôn các nhánh thuộc nó."* (bỏ tick cấp trên → toast *"Đã gỡ N nhánh thuộc mục vừa bỏ tick"*).
- **Bảng nhánh đã gắn**: STT (số La Mã I, II…) · Lĩnh vực Công ty kinh doanh · Chương · Mục · Tiểu mục · nút xoá *"Gỡ khỏi tiểu mục"* [GHI]. Rỗng → *"Chưa gắn nhánh nào — tick ở cột Tiểu mục bên trên"*.
- Validate khi bấm **Lưu** (không áp cho Lưu nháp): phải có ≥1 nhánh → nhảy sang tab Quản trị, chấm đỏ trên nhãn tab cha, viền đỏ cột Tiểu mục, chữ đỏ *"Phải xếp hàng hoá vào ít nhất 1 Tiểu mục: Phân loại theo lĩnh vực kinh doanh"*, toast *"Chưa xếp hàng hoá vào tiểu mục nào"*.

→ Tab Quản trị: **6 trường** + khối catalog 4 cấp + bảng nhánh.

### 5.6 Tab con 4 — Phân loại xe (`data-i=4`)
Card **"Phân loại xe"** (icon xe #0ea5e9):
| Nhãn | Loại | Bắt buộc |
|------|------|----------|
| Hãng xe | chọn nhiều + ô tick *"Chọn tất cả"* | * |
| Loại xe | chọn nhiều (lọc theo Hãng) + *"Chọn tất cả"* | |
| Model xe | chọn nhiều (lọc theo Hãng + Loại) + *"Chọn tất cả"* | |
| Áp dụng tất cả đời xe cho model | checkbox (col 12) | |

Bảng bộ ba: **Hãng xe** (gộp dòng rowspan) · **Loại xe** · **Model xe** · **Đời xe** (chọn nhiều riêng từng model + *"Chọn tất cả"*). Rỗng → *"Chọn Model xe ở trên để khai đời xe cho từng model"*. Đổi Hãng/Loại → loại bỏ giá trị cấp dưới không còn hợp lệ.
→ **4 trường** + bảng đời xe.

### 5.7 Tab con 5 — Nhóm máy (`data-i=5`)
- Card **"Phụ tùng – Phụ kiện"**: Nhóm máy (chọn nhiều, col 12).
- Card **"Máy \*"** — CHỈ HIỆN khi đã chọn ≥1 nhóm; nút header **Chọn máy**; bảng: STT · Mã máy · Tên máy · (xoá). Rỗng → *"Không có máy"*.
→ **1 trường** + bảng máy (bắt buộc).

> Mockup để 2 tab Phân loại xe / Nhóm máy **luôn hiện**; bản thật chỉ hiện khi Loại sản phẩm bật cờ khai báo tương ứng (ERP: `product_type === 'automotive_parts'` / `accessories…`).

### 5.8 Phân quyền sửa trên form (`mucQuyenSua` / `datVaiForm`, L3262–L3317)

| Mức | Khi nào | Kết quả |
|-----|---------|---------|
| `full` | tạo mới, hoặc `owner === công ty đang làm việc` | sửa được toàn bộ; mở tab cha *Thông tin hàng hoá*, tab con 1 |
| `chiQuanTri` | hàng do công ty khác tạo (`owner !== CUR`) | chỉ pane `data-i=3` (Quản trị) mở; form mở thẳng tab cha **Quản trị hàng hoá** |
| `khong` | (khai trong comment cho "vai tính giá bán" — **code không còn trả về**) | khoá cả 6 pane |

Chế độ khoá trông như sau (áp từng pane bị khoá):
- Mọi `input/select/textarea` → `disabled` (trừ `#f-cty` và ô `data-chi-doc` — luôn chỉ đọc).
- Mọi nút `.v2-btn` và `.ra-btn` (thêm/xoá dòng, nút +, Chọn hàng hoá, Thêm ĐVT…) → **ẩn hẳn** (`display:none`), không disable.
- Ô chọn nhiều → class `.khoa`; các ô tick "Chọn tất cả" → disabled.
- Hiện dải `#bao-muon`.
- Nhãn tab cha *Thông tin hàng hoá* mờ (`.khoa` opacity .4, con trỏ mặc định — vẫn bấm được để xem).
- 5 step tab con mờ (`opacity .45`) và **không chuyển được step** (`doiTab` return sớm) ⇒ chỉ xem được step 1 *Thông tin chung*.
- Footer (Lưu nháp / Lưu / Quay lại) **không bị ẩn**.
- Sau phân quyền mức `full`, khối Phân loại vẽ lại để giữ 3 ô cha luôn chỉ đọc.

Bảng chốt trên `sc-flow` ("Ai được sửa gì trên form hàng hoá"):
| Trường hợp | Sửa được | Khoá |
|------------|----------|------|
| Công ty **tạo ra** hàng hoá · vai Nhập thông tin | toàn bộ 6 tab thông tin | — |
| Công ty **lấy hàng của công ty khác về** · vai Nhập thông tin | chỉ tab **Dữ liệu quản trị** | 5 tab còn lại |
| Bất kỳ công ty nào · vai **Tính giá bán** | chỉ tab **Giá bán** | cả 6 tab thông tin |

**Chế độ chỉ đọc cho phase 2b:** mockup KHÔNG có chế độ "Xem" riêng — menu *Xem* và *Sửa* cùng gọi `moForm`. Khuôn gần nhất để tái dùng là mức khoá ở trên (disable ô + ẩn nút) áp cho **cả 6 pane**, đồng thời ẩn Lưu nháp/Lưu.

### 5.9 Thông báo Lưu (tham khảo — [GHI])
- Lưu nháp: thiếu tên → *"Chưa nhập Tên hàng hoá"*; OK → *"Đã lưu nháp — hàng hoá giữ trạng thái Đang nhập thông tin"* → về l1.
- Lưu: thiếu tên/thiếu nhánh catalog → báo lỗi; OK → st = `cho`, toast *"Đã lưu — hàng hoá chuyển sang Chờ tính giá bán, lập Yêu cầu tính giá để đi tiếp"* → sang màn kho.

---

## 6. `sc-flow` — Ghi chú & sơ đồ luồng

### 6.1 Quy trình 3 bước
| Bước | Tên | Trạng thái | Quyền |
|------|-----|-----------|-------|
| 1 | Nhập thông tin hàng hoá | Đang nhập thông tin (#64748B) → Chờ tính giá bán (#D97706) | Nhập thông tin hàng hoá |
| 2 | Tính giá bán bằng chứng từ | Đang tính giá (#2563EB) → Đang kinh doanh (#16A34A) | Tính giá bán hàng hoá |
| 3 | Đưa vào kinh doanh | Đang kinh doanh (#16A34A) | Nguồn dữ liệu cho toàn hệ thống |

### 6.2 Bảng "Cùng một mã hàng — mỗi công ty một trạng thái" (`#tb-matrix`)
- Cột: Mã hàng hoá · Tên hàng hoá · Công ty tạo · **Tân Phát** · **Tân Phát Power** · **Tân Phát Sài Gòn** (tiêu đề tĩnh; dữ liệu lấy theo key TPE / POWER / TPSG).
- Ô: badge trạng thái 0.7, không dùng → chữ xám *"Chưa sử dụng"*.
- Dữ liệu mẫu (6 dòng đầu):

| Mã | Công ty tạo | TPE | POWER | TPSG |
|----|-------------|-----|-------|------|
| TPE-MNK-FS-15A | TÂN PHÁT | Đang kinh doanh | Đang nhập thông tin | Chưa sử dụng |
| TPE-MNK-FS-20A | TÂN PHÁT | Chờ tính giá bán | Chưa sử dụng | Chưa sử dụng |
| TPE-CN-2T-4500 | TÂN PHÁT | Đang kinh doanh | Chờ tính giá bán | Đang kinh doanh |
| TPE-MRL-LR-300 | TÂN PHÁT | Đang tính giá | Chưa sử dụng | Chưa sử dụng |
| TPE-MCB-BL-500 | TÂN PHÁT | Đang nhập thông tin | Chưa sử dụng | Chưa sử dụng |
| TPE-PT-LOC-001 | TÂN PHÁT | Đang kinh doanh | Chưa sử dụng | Đang tính giá |

### 6.3 "Những chỗ mockup làm khác bản thật — cần chốt khi code"
1. Tab Phân loại xe / Nhóm máy luôn hiện ở mockup; bản thật chỉ hiện khi Loại sản phẩm bật cờ.
2. Phiếu tính giá tính cho ĐVT cơ bản; bản thật phải tính đủ các ĐVT.
3. Lấy hàng công ty khác về = tham chiếu chung một mã, chưa chốt phương án chép mã riêng.
4. Mọi lớp khoá mới là khoá giao diện; bản thật phải chặn ở máy chủ theo công ty quản lý hàng hoá.

---

## 7. Điểm mơ hồ / mâu thuẫn trong mockup

1. **Vai "Tính giá bán" + tab "Giá bán"**: bảng phân quyền ở `sc-flow` còn ghi "chỉ tab Giá bán", nhưng tab Giá bán đã gỡ (27/09) và `mucQuyenSua` không bao giờ trả `'khong'`.
2. **"6 tab"** (sc-flow, comment) vs thực tế 2 tab cha + 5 tab con; *Dữ liệu quản trị* giờ là tab cha **Quản trị hàng hoá**.
3. **Màn l3 có/không bắt buộc catalog**: comment HTML L1205 nói l3 "chỉ hiện hàng ĐÃ xếp catalog", `veDem` cnt-l3 vẫn đếm hàng đã xếp; nhưng §35c (04/10) và `veBang3` hiện mọi hàng KD. Lấy bản 04/10.
4. Ô **Công ty quản lý** trong form luôn điền **công ty đang làm việc** (`CTY[CUR]`), không phải công ty tạo hàng ⇒ sai với hàng lấy về (dải báo lại ghi đúng công ty tạo). Nên hiển thị `owner`.
5. Tiêu đề cột bảng ma trận ("Tân Phát Power", "Tân Phát Sài Gòn") lệch tên `CTY` ("ETEK POWER", "TÂN PHÁT SG").
6. Bộ lọc nâng cao phần lớn **không nối** vào lọc ở mockup (chỉ `tong-cty`, `tong-dung`, `kho-st` lọc thật) — các ô còn lại là khai báo giao diện, nghĩa lọc phải tự suy (vd l3 "Có giá bán", kho "Bảo hành").
7. Nút **Cài đặt bộ lọc**, **Xuất Excel**, Tìm kiếm/Làm mới ở l1 **không có handler**.
8. Màn **l1 không có Xuất Excel** (3 màn kia có) — chưa rõ cố ý hay sót.
9. Màn Kho dữ liệu: công tắc *"Chỉ hàng công ty chưa dùng"* trùng nghĩa với ô *Tình trạng sử dụng = Công ty chưa dùng*.
10. Màn kho: dòng trạng thái `nhap` có menu **Xem** (kiểu kd) chứ không phải **Sửa** như màn l1.
11. Cột **Giá vốn** bật được ở l1 và kho (tắt mặc định) — số nhạy cảm, cần gate quyền xem giá vốn ở BE; ở l3/tong bị loại hẳn.
12. Nút **Mặc định** trong Cấu hình cột không tick lại cột *Công ty quản lý* vốn mặc định ở tong/kho.
13. Cột Trạng thái hiện mặc định ở l1/l3 dù mỗi màn chỉ có 1 trạng thái.
14. Nhãn ô lọc viết "Tính chất hàng **hóa**" (bộ lọc) vs "hàng **hoá**" (cột, form).
15. Options *Đặc tính sản phẩm* (Hàng nhập khẩu / lắp ráp / gia công / thương mại) không khớp nghĩa tooltip ("tiêu chuẩn hay thay đổi theo nhu cầu khách hàng") — cần lấy danh mục thật.
16. "Chọn tất cả" ô tick đầu bảng chỉ chọn trong trang hiện tại; chưa có "chọn tất cả N kết quả lọc" trên lưới (chỉ có trong popup Xây dựng catalog).
