---
name: hdsd-documenter
description: Generate tài liệu Hướng dẫn sử dụng (HDSD) Word cho màn hình — bản GỌN theo khuôn tester duyệt 29/09/2026 (mỗi chức năng 1 phần, các bước ngắn không giải thích, mỗi chức năng 1 ảnh màn hình, mọi nút đều có ảnh nút)
---

# HDSD Documenter — ERP TPE (bản GỌN, chốt 29/09/2026)

## Khuôn chuẩn
**`assets/HDSD_MAU_GON.docx`** = *HDSD_Danh mục khu vực* do tester rút gọn (Drive ID
`1aZNDBVW4qa4G2N8HirqnM7N9BJqVS1Ea`). Mở ra xem trước khi viết. Mọi HDSD mới phải **dài và gọn đúng
như file này** — một màn danh mục đầy đủ chức năng chỉ khoảng **15–17 trang**.

> `assets/HDSD_MAU.docx` + `hdsd_engine.py` là khuôn CŨ (bản chi tiết: bảng từng trường, box giá trị
> mặc định, mục theo từng quyền…). **Không dùng cho tài liệu mới.** Chỉ giữ để mở lại file cũ.

## Yêu cầu của tester (nguyên văn — đây là tiêu chí nghiệm thu)
> Tổng quan: Bỏ mục đích. Chia mỗi chức năng là 1 phần, Mô tả các bước ngắn gọn, k cần giải thích.
> Với mỗi chức năng cho 1 ảnh màn hình, các nút đều phải có hình ảnh nút. Riêng chức năng import thêm
> ảnh tương ứng với sau khi nhấn các nút Load lên bảng, Validate

## 5 nguyên tắc
1. **Mỗi chức năng = 1 PHẦN** (Heading 1 `PHẦN N: <TÊN CHỨC NĂNG>`, sang trang mới). Không gộp nhiều
   chức năng vào một phần, không chia tiểu mục trong phần (ngoại lệ: phần có 2 thao tác cặp đôi như
   Khóa / Mở khóa được tách `1.` `2.` bằng Heading 2).
2. **Chỉ có các bước, không giải thích.** Mỗi dòng là `Bước N: <động từ> <đối tượng> [ảnh nút] <kết quả ngắn>`.
   Nhánh phụ viết dòng thụt lề bắt đầu bằng **"Hoặc …"** ngay dưới bước đó.
   ❌ KHÔNG viết: mục đích/ý nghĩa nghiệp vụ, đoạn văn mô tả, "lưu ý"/"cần đặc biệt lưu ý", bảng từng
   trường, box giá trị mặc định, bảng "khác với Thêm mới", ví dụ số, edge case, FAQ.
3. **Mỗi chức năng đúng 1 ảnh màn hình** — ảnh cái form/popup/hộp xác nhận mà chức năng đó mở ra, đặt
   ngay sau bước làm nó hiện ra, kèm chú thích `Hình N: <tên cửa sổ>`.
   **Riêng Import: 3 ảnh** — cửa sổ vừa mở · sau khi bấm **Load lên bảng** · sau khi bấm **Validate**
   (có dòng lỗi để thấy lý do).
4. **Mọi nút đều có ảnh nút** (cắt từ UI, cao 0,22", chèn ngay sau chữ nhắc tới nút): nút thanh công
   cụ, icon ở cột Hành động, mục trong menu ba chấm, nút trong popup (Lưu / Lưu và tiếp tục / Đóng),
   nút trong hộp xác nhận (Xóa / Khóa / Mở khóa / Hủy), cả mục menu ở bước truy cập (phân hệ, nhóm
   menu, mục). Nút đổi dạng theo trạng thái (icon thẳng hay nằm trong ba chấm) thì chèn cả 2 ảnh:
   *"Chọn Khóa [ảnh icon] hoặc [ảnh mục menu] ở cột Hành động"*.
5. **Ngôn ngữ người dùng cuối**: dùng đúng nhãn trên màn hình. CẤM tên bảng/cột, id quyền, endpoint,
   mã HTTP, tên hàm/file, **URL và đường dẫn tương đối** — vào màn chỉ tả đường bấm menu.

## Cấu trúc tài liệu (bám `HDSD_MAU_GON.docx`)
```
Bìa  (Màn hình: <Tên màn>)
MỤC LỤC
TỔNG QUAN
  1. Thuật ngữ sử dụng trong tài liệu   ← bảng 2 cột Thuật ngữ | Giải thích (tên đối tượng + các trạng thái)
  2. Cập nhật tài liệu                   ← bảng 4 cột Phiên bản | Ngày | Người cập nhật | Nội dung
  3. Quyền sử dụng                       ← 1–2 câu, hoặc bảng 2 cột Chức năng | Quyền cần có
  4. Sơ đồ chức năng tổng quan           ← 1 ảnh sơ đồ use case + chú thích
PHẦN 1: TRUY CẬP VÀ TÌM KIẾM
PHẦN 2..N: mỗi chức năng một phần
```
- **Không** có mục "Mục đích/Mục tiêu", "Giới thiệu chung", "PHẦN Truy cập & bố cục" riêng.
- Quyền: chỉ nói ở TỔNG QUAN mục 3. Không làm tiểu mục "Người dùng có quyền …" trong từng phần.
- Thứ tự phần theo khuôn: Truy cập & tìm kiếm → Thêm mới → Chỉnh sửa → Xóa → Khóa → Mở khóa → Xem
  lịch sử → Xem chi tiết → Xuất Excel → Import → Tùy chỉnh cột → (In, Duyệt, … nếu màn có). Màn không
  có chức năng nào thì bỏ phần đó, đánh số liền lại.

## Mẫu câu từng loại chức năng (copy, chỉ đổi tên đối tượng)

| Phần | Các bước | Ảnh màn hình |
|---|---|---|
| Truy cập và tìm kiếm | B1: Từ phân hệ **X** [ảnh], tại menu **Y** [ảnh], chọn **Z** [ảnh] · B2: Nhập chữ vào ô tìm kiếm nhanh [ảnh ô] · B3: Nhấn [Tìm kiếm] · B4: Chọn giá trị trong **Trạng thái** [ảnh ô] để lọc… (mỗi ô lọc 1 dòng "Hoặc") · B5: Chọn [Làm mới] để xóa giá trị đã lọc | (không bắt buộc) màn danh sách |
| Thêm mới | B1: Truy cập vào màn hình … · B2: Bấm [Tạo mới] · **ảnh form** · B3: Nhập/chọn đầy đủ thông tin bắt buộc: *<liệt kê tên trường bắt buộc trên 1 dòng>* · B4: Bấm [Lưu] để lưu và đóng cửa sổ / Hoặc [Lưu và tiếp tục] … / Hoặc [Đóng] để không lưu | Cửa sổ Tạo … |
| Chỉnh sửa | B1: Truy cập … · B2: Bấm [Sửa] ở cột Hành động · B3: Hệ thống hiển thị cửa sổ "Sửa …" · **ảnh** · B4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới) · B5: Bấm [Lưu] / Hoặc [Đóng] | Cửa sổ Sửa … |
| Xóa / Khóa / Mở khóa | B1: Bấm [icon] ở cột Hành động · B2: Hệ thống hiện hộp xác nhận "…" · **ảnh** · B3: Bấm [Xóa/Khóa/Mở khóa] để xác nhận / Hoặc bấm [Hủy] nếu bấm nhầm | Hộp xác nhận |
| Xem lịch sử thay đổi | Cách 1 (từ danh sách): Ở cột Hành động chọn [Lịch sử] · Cách 2 (từ chi tiết): B1 bấm vào tên … để mở chi tiết, B2 chọn [Xem lịch sử] · **ảnh** | Cửa sổ Lịch sử thay đổi |
| Xem chi tiết | B1: Truy cập … · B2: Bấm vào tên … Hệ thống mở cửa sổ "Xem …" · **ảnh** | Cửa sổ Xem (chỉ đọc) |
| Xuất Excel | B1: Lọc danh sách theo dữ liệu cần lấy (xem PHẦN 1) · B2: Bấm [Xuất Excel], hệ thống mở "Chọn trường xuất file" · **ảnh** · B3: Tích chọn, kéo ☰ đổi vị trí trường · B4: Bấm [Xuất file] · B5: Mở file Excel đã xuất | Cửa sổ Chọn trường xuất file |
| Import | B1: Bấm [Import Excel], mở cửa sổ "Import …" · **ảnh 1** · B2: Bấm [Tải file mẫu] · B3: Điền dữ liệu vào file mẫu · B4: Bấm [Chọn file Excel], chọn file vừa điền · B5: Bấm [Load lên bảng] · **ảnh 2** · B6: Bấm [Validate] để kiểm tra từng dòng · **ảnh 3** · B7: 3 dòng con: sửa dòng lỗi rồi Validate lại / bấm [Bỏ dòng lỗi] / bấm [Xóa trạng thái validate] để sửa lại dòng đã khoá · B8: Bấm [Import] | 3 ảnh (vừa mở · sau Load · sau Validate) |
| Tùy chỉnh cột | B1: Bấm [biểu tượng tùy chỉnh cột] · **ảnh** · B2: Tích để hiện, bỏ tích để ẩn cột · B3: Kéo ba gạch đổi thứ tự · B4: Bấm [Lưu] / Hoặc [Đóng] | Cửa sổ Tùy chỉnh cột |

Màn có chức năng khác (Duyệt, In, Quản lý…) viết cùng khuôn: các bước bấm + 1 ảnh cửa sổ mở ra.
Màn phụ nhiều thẻ mở từ một nút: mỗi thẻ có thao tác thì là 1 PHẦN riêng, vẫn giữ khuôn trên.

⚠️ File mẫu tester sửa tay còn 2 lỗi, **đừng chép theo**: số Hình nhảy lộn (Hình 12 → 13 → 10) và
bước Import nhảy từ Bước 5 sang Bước 7. Tài liệu sinh ra phải đánh số Hình và số Bước liên tục.

## Quy trình

### Bước 1 — Đọc code (vừa đủ để viết ĐÚNG, không để viết DÀI)
Đọc FE màn + popup để lấy: danh sách chức năng, **nhãn nút nguyên văn**, tên cửa sổ, **tên các trường
bắt buộc**, các ô lọc, chức năng nào gắn quyền nào (seeder `PermissionsTableSeeder` + `checkPermission`
trên route + `isCurrentEmployeeHasPermission` trong controller). Đọc BE chỉ khi cần xác nhận trường bắt
buộc / nút có thật chạy không. Không cần khảo sát luồng xuôi-ngược, edge case — tài liệu gọn không dùng.
Hành vi nghi là lỗi → báo riêng cho user, không ghi vào HDSD.

### Bước 2 — Chụp ảnh + cắt ảnh nút (Playwright MCP)
- Mở `http://127.0.0.1:3000` (không `localhost`), resize 1440x900. Danh sách chụp cần: sơ đồ use case,
  1 ảnh/chức năng theo bảng trên, Import đủ 3 ảnh (Validate bằng file có cả dòng đúng lẫn dòng lỗi).
- **Cắt ảnh nút — SÁT, KHÔNG THỪA KHOẢNG TRẮNG** (chuẩn = icon trong `HDSD_MAU_GON.docx`, user chốt
  29/09/2026). Ảnh nút chèn cố định cao 0,22" nên mỗi px nền thừa làm nút trong ảnh bé lại và lệch dòng.
  - Nút có viền/nền (Tạo mới, Lưu, Xóa, icon trên dòng…): ôm sát viền nút, dư **0–2px**. Lấy đúng
    phần tử nút (`button`, `span[title=…]`), KHÔNG lấy ô bảng / thẻ `div` bọc ngoài.
  - Mục không viền (mục menu sidebar, mục trong menu ba chấm, ô lọc): sát icon + chữ, vẫn đủ cao ~26px
    để chữ trong ảnh không to hơn chữ thân bài.
  - **Mục menu thanh bên (phân hệ "DANH MỤC", nhóm "Địa lý"…)** — user bắt lỗi 29/09: ảnh dư nửa dải nền
    tối bên phải, hoặc chữ dính sát mép. Phần tử menu rộng hết thanh bên (220px) và nền là dải màu có hoa
    văn, nên: chụp khung phần tử **± 12px** (để chữ không bị hụt), **cắt khung trong phạm vi thanh bên**
    (`x + width ≤ 218`, lấn sang trang trắng là dải trắng thành "nội dung"), rồi chạy `trim_icon.py` —
    nền tối tự nhận ra, chỉ giữ chữ + icon sáng, chừa 6px.
  - Chụp `page.screenshot({clip: boundingBox})` (không cộng thêm lề), rồi **luôn chạy**
    `python3 .claude/skills/hdsd-documenter/assets/trim_icon.py <thư_mục_icons>` — tự bỏ nền thừa, chừa
    2px, bù chiều cao tối thiểu 26px. Kiểm trước bằng `--dry`: phải ra `Cần cắt 0/N`.
  - Lưu `icons/btn_<tên>.png` (mục menu `item_<tên>.png`, mục sidebar `menu_<tên>.png`). Nút chỉ-icon theo `span[title="Sửa"]` /
  `button[title="…"]`; nút trong hộp xác nhận theo id modal (`#confirm-…`), không dùng `.modal.show`.
  Icon nút chung (Tạo mới, Xuất Excel, Sửa…) có sẵn ở `.plans/gop-db/catalog-docs-v2/icons/` — dùng lại.
- Hộp xác nhận Xóa/Khóa: chụp xong bấm **Hủy**. Mở form Tạo mới không lưu.
- 🐛 Ảnh mờ trắng / nút nhạt = chụp lúc đang tải hoặc đang hiệu ứng: chờ ≥ 15 giây, `mouse.move(5,5)`
  rồi mới chụp. Chụp xong ghép toàn bộ ảnh + icon thành 1 tấm (Pillow) rồi Read ra soi một lượt.
- Ảnh lưu `.plans/[feature]/hdsd_<feature>_shots/` — **không commit**.

### Bước 3 — Dựng Word bằng `QgWriter` trên khuôn gọn
Dùng `.plans/gop-db/_catalog_docs_lib/qg_writer.py` (`QgWriter`): lấy CHÍNH file mẫu làm vỏ, giữ bìa +
mục lục, xoá thân bài, rồi nhân bản đoạn mẫu theo vai trò → giống file tester 100% (font, bullet số
bước, thụt lề dòng "Hoặc", cỡ ảnh, màu chú thích). Không dùng `add_paragraph(style=…)`.

Vai trò = chỉ số phần tử trong body của **`assets/HDSD_MAU_GON.docx`** (đã dò 29/09/2026):
```python
HDSD_GON_ROLES = {'pagebreak': 33, 'h1': 34, 'h2': 21, 'p': 28,
                  'step': 43,      # "Bước N: …" (bullet số cấp 0)
                  'sub': 49,       # dòng "Hoặc …" thụt lề dưới bước
                  'sub2': 126,     # bullet cấp 1 (các dòng con của Bước 7 Import)
                  'img': 45, 'cap': 46, 'blank': 23, 'tbl2': 22, 'tbl4': 25}
w = QgWriter(TPL_GON, HDSD_GON_ROLES, body_from=19,
             cover_replace={'Danh mục khu vực': '<Tên màn>'})
w.h1('PHẦN 2: THÊM MỚI KHU VỰC')
w.step(['Bước 2: Bấm ', ('img', ICONS + '/btn_tao_moi.png')])
w.image(SHOTS + '/02-tao.png', caption='Cửa sổ Tạo khu vực')
w.raw('sub', ['Hoặc ', ('img', ICONS + '/btn_dong.png'), ' để không lưu thông tin.'])
```
`segs` nhận chuỗi, `('b', chữ đậm)`, `('img', đường_dẫn, cao_inch=0.22)`.
⚠️ Thay file mẫu thì phải dò lại chỉ số vai trò (in `i, style, numPr, số ảnh, text` của từng phần tử
body) — chỉ số sai là heading ra kiểu bước, bước ra kiểu ảnh, không báo lỗi.
Generator lưu ở `.plans/[feature]/gen_hdsd.py` (được version control).

**Màn DANH MỤC (đủ bộ Thêm/Sửa/Xóa/Khóa/Mở khóa/Lịch sử/Chi tiết/Xuất/Import/Tùy chỉnh cột): KHÔNG viết
generator tay** — dùng `.plans/gop-db/_catalog_docs_lib/hdsd_gon.py` (`build(G, out)`), mỗi màn chỉ khai
dict `G` (menu, thuật ngữ, phiên bản, quyền, trường bắt buộc, ô lọc, bấm tên hay mã để xem chi tiết,
Khóa hiện icon thẳng hay chỉ trong ba chấm, tên 3 hộp xác nhận). Mẫu: `catalog-docs-v2/provinces/gen_hdsd_gon.py`.
Ảnh cần có trong `shots/`: 01_list · 10_create · 12_edit · 13_delete · 14_lock · 15_unlock · 16_history
(**bản ghi CÓ lịch sử**, không lấy ảnh "Chưa có lịch sử") · 17_detail · 20_export · 21/22/23_import · 25_colcfg.
Icon riêng của màn trong `icons/`: menu_*, o_timnhanh (dài quá ~330px thì cắt ngắn), o_<ô lọc>,
btn_bacham_row, item_khoa, item_lichsu, btn_khoa_row, btn_lichsu_row, btn_mokhoa_row, btn_confirm_khoa,
btn_confirm_xoa, btn_huy_confirm. Dòng có nút Xóa thì Khóa/Lịch sử nằm trong ba chấm, dòng không có Xóa
thì hiện thẳng icon → cắt đủ cả 2 dạng.

**2 lỗi trình bày đã xử lý sẵn trong `hdsd_gon.py` (29/09/2026) — generator tự viết thì phải làm y như vậy:**
- **Trang trắng**: KHÔNG sang trang bằng đoạn chứa dấu ngắt trang (vai trò `pagebreak`) — trang trước vừa kín
  (ảnh Sơ đồ dài) thì đoạn ngắt bị đẩy sang đầu trang sau rồi mới ngắt → dư 1 trang trắng. Dùng
  `h1_trang_moi(w, text)`: gắn `w:pageBreakBefore` vào chính tiêu đề.
- **Chú thích "Hình N" rơi sang trang sau, tách khỏi ảnh**: sau mỗi `w.image(...)` gọi `anh_lien_chu_thich(w)`
  (gắn `w:keepNext` cho đoạn ảnh). Kiểm bằng VỊ TRÍ, không bằng chữ: trang có khối chữ "Hình …" nằm CAO HƠN mọi
  ảnh lớn của trang đó mới là bị tách (ảnh không có chữ nên "trang bắt đầu bằng Hình" chưa chắc là lỗi).

**Làm hàng loạt nhiều màn** (thư mục `.plans/gop-db/catalog-docs-v2/`): `hdsd_gon_targets.json` (màn ↔ file Drive)
→ mỗi màn một `gen_hdsd_gon.py` → `python3 _rebuild_check_gon.py <scratch> [slug…]` (dựng lại + kiểm trang trắng /
chú thích tách / mũi tên / mục đích) → `push_hdsd_by_id.py <slug…>`. Chụp song song nhiều màn thì mỗi agent chạy
Playwright Python headless riêng (Playwright MCP chỉ có 1 trình duyệt dùng chung); LibreOffice chạy song song phải
thêm `-env:UserInstallation=file://<thư mục riêng>` nếu không lệnh sau im lặng không ra PDF.

### Bước 4 — Mục lục, dọn file, kiểm
0. Gọi `w.rebuild_toc(levels=(1, 2))` trước `w.save(...)`. Mục lục của chính file mẫu đang CŨ (còn
   dòng "3. Mục đích", "5. Sơ đồ…" dù thân bài đã bỏ) — không dựng lại là chép nguyên cái sai đó sang.
1. Cập nhật mục lục bằng Word trên macOS (một lệnh, không vòng `repeat`):
   ```bash
   osascript -e 'tell application "Microsoft Word"
     open POSIX file "<đường dẫn tuyệt đối .docx>"
     delay 3
     set d to active document
     update table of contents 1 of d
     save d
     close d saving no
   end tell'
   ```
   Mục lục nằm trong `w:sdt` → kiểm bằng `iter(qn('w:p'))` trong sdt, phải ra đúng các PHẦN của màn này.
2. Word lưu lại nhúng font (6 MB → 12 MB) → chạy `strip_embedded_fonts()` trong `qg_writer.py`.
3. `soffice --headless --convert-to pdf`, render các trang bằng PyMuPDF, ghép thành 1 tấm rồi soi.

## Checklist trước khi giao
- [ ] TỔNG QUAN đúng 4 mục (Thuật ngữ · Cập nhật tài liệu · Quyền sử dụng · Sơ đồ chức năng), **không có mục đích**.
- [ ] Mỗi chức năng là 1 PHẦN, sang trang mới; thứ tự theo khuôn.
- [ ] Chỉ có "Bước N" + dòng "Hoặc"; không đoạn giải thích, không bảng trường, không lưu ý.
- [ ] Mỗi chức năng đúng 1 ảnh màn hình; Import có đủ 3 ảnh (vừa mở · sau Load lên bảng · sau Validate).
- [ ] **Mọi nút được nhắc tới đều có ảnh nút inline** — kể cả mục menu ở bước truy cập, nút Hủy/Đóng.
- [ ] Ảnh nút đã cắt sát: `trim_icon.py --dry <icons>` ra `Cần cắt 0/N`.
- [ ] Số Bước và số Hình liên tục, không nhảy cóc.
- [ ] Không URL, không thuật ngữ code; tên nút/cửa sổ/trường khớp nguyên văn màn hình.
- [ ] Bìa đúng tên màn; mục lục đã cập nhật bằng Word, không còn dòng của file mẫu.
- [ ] Đã strip font nhúng; ảnh không mờ; thư mục ảnh không bị commit.

## Output & đẩy lên Drive
- File: `.plans/[feature]/HDSD_<Tên màn>.docx` (nhánh `gop_db` → `.plans/gop-db/[feature]/`).
- **Ai sửa, sửa lúc nào — xem lịch sử phiên bản qua API** (29/09/2026: tester sửa tay Tỉnh/TP 2 phút sau khi
  mình đẩy): `GET https://www.googleapis.com/drive/v3/files/<ID>/revisions?fields=revisions(modifiedTime,lastModifyingUser(displayName))`.
  Tài khoản rclone của mình hiện "Cuong Nguyen Manh", tester là `hangtechqa` → phân biệt được. Bản đã qua
  Google Docs khác hết định dạng, nên so NỘI DUNG (chuỗi text + số ảnh theo từng đoạn), chỉ gộp phần chữ họ sửa.
  Đẩy hàng loạt dùng `catalog-docs-v2/push_hdsd_by_id.py <slug>…` (ghi theo ID, chặn khi Drive đổi sau mốc
  đã biết, tự thử lại khi bị giới hạn yêu cầu, tải lại so từng byte).
- Đẩy lên Drive (folder HDSD, ghi đè giữ ID): trước khi ghi đè so `ModTime` trên Drive
  (`rclone lsjson … -M`) với lần đẩy gần nhất của mình — lệch là có người sửa tay → **dừng, hỏi user**,
  và kiểm lại ModTime ngay trước lệnh đẩy. File bị đổi tên trên Drive thì `copyto` theo tên cũ sẽ tạo
  bản trùng → đối chiếu ID sau khi đẩy. File đã thành Google Docs (ID > 40 ký tự) đẩy kèm
  `--drive-import-formats=docx`.
- ⚠️ **Folder HDSD có FILE TRÙNG TÊN** (29/09/2026: Loại tài khoản, Tiền tệ, Cấp dịch vụ bảo dưỡng, Ghi
  chú kiểm tra bảo dưỡng, Serial thiết bị — mỗi màn 2 file, link user gửi và link bảng theo dõi trỏ 2 ID
  khác nhau). Khi đó `rclone copy/copyto` theo tên sẽ ghi bừa vào một file → **ghi theo ID** vào đúng
  file ở link user gửi (và cả ID trong `catalog-docs-v2/index.json` nếu khác), qua Drive API:
  ```bash
  rclone about gdrive: >/dev/null   # làm mới token
  TOK=$(rclone config dump | python3 -c "import json,sys;print(json.loads(json.load(sys.stdin)['gdrive']['token'])['access_token'])")
  curl -s -X PATCH -H "Authorization: Bearer $TOK" \
    -H "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
    --data-binary @"<file.docx>" \
    "https://www.googleapis.com/upload/drive/v3/files/<ID>?uploadType=media&supportsAllDrives=true"
  ```
  Tải về kiểm bằng `rclone backend copyid gdrive: <ID> <file>` (không tải theo tên). Chi tiết gộp phần tester sửa tay: `srs-documenter/SKILL.md` mục
  "Đẩy lên Drive".
