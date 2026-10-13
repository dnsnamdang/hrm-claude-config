# G0 — Mockup 2 màn giá HRM: ghi chú (09/10/2026)

File: `mockup-gia.html` (cùng thư mục, tự chứa; chỉ tải font Roboto + Remix Icon 4.3.0 từ CDN).
Mở: `file:///Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/gia-theo-cong-ty/mockup-gia.html`
Đây chỉ là tài liệu. Không đụng source, không ghi DB. App HRM chỉ được mở để đo.

## 1. Có gì trong mockup

- **Menu Tài chính (D9).** Thêm nhóm rail **"Quản lý giá - CTKM"** ngay sau "Kế toán công nợ". Nhóm có 1 nhóm con "Giá bán" gồm
  6 mục: Phiếu tính giá (xám, Phase 7) · **Cập nhật giá bán** (1657) · **Duyệt giá bán** (1658) · Cập nhật giá theo hãng (xám, N36) ·
  Trạng thái cập nhật giá ↗ERP · Hàng sắp điều chỉnh tăng giá ↗ERP. Nhóm đủ 6 mục nên panel chia 2 cột, xếp theo cột như app.
  Thêm lối phụ ở rail "Chờ duyệt": nhóm "Giá bán chờ duyệt" → "Hàng hoá chờ duyệt giá bán". Các mục ẩn theo quyền. Không có 1658
  thì nhóm còn 5 mục (vẫn 2 cột). Không có cả 2 quyền thì còn 4 mục (1 cột).
- **Màn Cập nhật giá bán.**
  - Bộ lọc: ô tìm, cây 4 cấp, Hãng SX, Thương hiệu, Trạng thái duyệt, Tồn kho Còn/Hết (lọc thật theo tồn công ty, D6/T6).
  - Bảng: mỗi hàng × ĐVT là 1 khối 6 loại giá (rowspan). Giá theo công ty: đổi công ty ở bảng "Giả lập" thì giá đổi theo
    (Cty 2/3/4 = chép × hệ số, tròn nghìn — P1). Cty 7 danh sách trống.
  - JS tính thật T1–T11, ô giá hiệu lực, cờ chờ duyệt / không duyệt, lý do sửa giá. Công khoán + ghi chú chỉ hiển thị.
  - Có 1 ca khoá dòng kèm lý do. Lưu thường áp ngay. Khi công ty bật duyệt giá, nút đổi thành "Gửi duyệt" (có popup xác nhận) và
    sinh yêu cầu ở màn Duyệt.
  - Hỏi "Thông tin chưa lưu" khi đổi ĐVT, trang, bộ lọc, công ty hoặc rời màn.
- **Màn Duyệt giá bán.**
  - Bộ lọc gồm Người cập nhật. Nút Xuất Excel đặt trên header bộ lọc.
  - Người duyệt sửa được hệ số, giá, ĐMGG và ngày hiệu lực. Bảng hiện chênh lệch ±.
  - Duyệt / Không duyệt từng yêu cầu hoặc hàng loạt. Tick giữ nguyên khi lọc lại, có báo "N đang ẩn do bộ lọc".
  - Popup duyệt báo các giá hiệu lực sẽ dời về ngày mai, và cảnh báo khi giá đang chạy đã đổi sau lúc đề nghị (ca bản ghi PTG ERP).
  - Không duyệt thì lý do là bắt buộc. Có tắt quyền 1092 để thử ẩn cột Giá vốn (xem Q1).
- **Popup.** Lịch sử giá (khuôn entity-history: bộ lọc 3 nhóm, timeline, có dòng giá vốn) · Nhập lý do Không duyệt · Xác nhận
  duyệt (đơn và hàng loạt). Thêm 2 popup phụ: Gửi duyệt và Thông tin chưa lưu, cộng 1 popup đọc: Công thức lắp ráp.

## 2. Điểm tự chốt (thuần UI) — chi tiết ở comment đầu file, U1–U18

Gồm: tiêu đề 1 tầng · bảng có vùng cuộn riêng · đo bề rộng bằng flex · ghim tổng bề rộng · nút Lưu nằm trong ô "ĐVT · Lưu" dính trái ·
Tồn/Mã/Model/Hãng dời ra sau Hiệu lực · công tắc Sửa tay TMĐT nằm trong ô Loại giá · badge gắn theo dòng · giá hiệu lực TMĐT chỉ đọc ·
chênh lệch giảm hiện màu cam (không đỏ) · nút Duyệt/Không duyệt nằm trong ô Tên · toast tạm.

## 3. Câu hỏi nghiệp vụ — user ĐÃ CHỐT 09/10/2026

- **Q1** Màn **Duyệt giá**: người KHÔNG có quyền 1092 "Xem giá vốn hàng hoá" ⇒ ẩn **cả cột Giá vốn lẫn cột Hệ số**, vì hệ số × giá vốn
  = giá nên suy ngược ra được giá vốn. Người duyệt sửa giá bằng ô Giá mới. **BE cũng không trả `cost_price` / `coefficient`** cho người này.
  - **Màn Cập nhật giá bán: tôi chọn KHÔNG áp luật 1092.** Lý do: quyền 1657 đã gồm "xem giá vốn trên màn" (design §6.2), và
    Giá vốn là ô nhập bắt buộc khi Lưu. Ai đã vào được màn này thì đã thấy giá vốn, nên cột Hệ số không lộ thêm gì.
  - Popup Lịch sử: người có 1658 nhưng không có 1657 lẫn 1092 thì không thấy dòng Giá vốn, cũng không thấy đoạn "Hệ số: …".
- **Q2** Công ty tắt duyệt giá trong lúc còn yêu cầu đang chờ ⇒ Lưu áp giá mới ngay và **xoá yêu cầu chờ cũ** (mockup giữ nguyên hành vi này).

## 4. Số đo từ app (127.0.0.1:3000, nhánh `gop_db`) và so với mockup — viewport 1440×900

App đo ở: `/finance/bill-incomes` (danh sách V2 + SmartFilterPanel + hub Tài chính), `/finance/bill-income-requests` ($confirm
thật + modal "Tuỳ chỉnh cột" + probe class `v2-input`/`v2-badge`), `/customer-care/wr-quotations/create` (bảng `v2-form-table`).
Lưu ý: dev server 3000 đang chạy nhánh `gop_db`, nhánh này chưa có `/master-data/products/*`, nên **không mở được
`ProductFormUnitsTable`**. Thay vào đó đo bảng nhập `v2-form-table` của báo giá dịch vụ (cùng class).

| Thành phần | App | Mockup | Khớp |
|---|---|---|---|
| body | Roboto 12.8px/19.2, chữ rgb(17,17,17), nền rgb(245,246,248) | như app | ✓ |
| Sidebar | 220px, gradient rgb(18,60,116)→rgb(10,28,61) + 2 radial; mục rail 13.5px, pad 9/16, cao 38.25 | 220, cùng gradient, 38.3 | ✓ |
| Rail đang chọn | nền rgba(111,178,255,.16), viền trái 3px rgb(111,178,255), 700, chữ rgb(234,247,255) | như app | ✓ |
| Tên phân hệ | 15px/800 trắng | 15/800 | ✓ |
| Topbar | cao 60, gradient 100deg rgb(10,28,61)→rgb(26,90,160); tiêu đề 16px/600 trắng, lh 42 | như app | ✓ |
| Panel hub | x220 y60, rộng 1180, nền gradient rgb(233,239,248)→rgb(238,243,249); dtop pad 18/26/14 nền rgb(226,234,245); tiêu đề 17/800 | x220 y60 1180, như app | ✓ |
| Nhóm con hub | cột 224 nền rgb(221,230,243); mục 207×35.5, radius 9, pad 8/11, 13px; đang chọn nền rgb(46,113,195) trắng 700 | như app | ✓ |
| Mục hub | 13px rgb(55,65,79), pad 8/10, radius 9; 2 cột 451.5 (≥5 mục), xếp theo cột | như app (442.5 do thiếu thanh cuộn trang) | ✓ |
| Thẻ (tp-card) | trắng, viền 1px rgb(229,231,235), radius 8, shadow 0 6px 18px rgba(15,23,42,.04) | như app | ✓ |
| Thẻ bộ lọc | pad 10/16, cao 102 (chưa mở nâng cao) | 102 | ✓ |
| "Bộ lọc danh sách" | 12px/900 rgb(10,153,167); icon tròn 26 nền rgba(22,163,74,.1) | như app | ✓ |
| Ô tìm | cao 32, viền rgb(209,213,219), radius 8, 12px, pad trái 32 | như app | ✓ |
| Ô lọc nổi nhãn | input cao 32, viền rgb(220,223,230), radius 6; nhãn 11px rgb(110,117,128) scale 1.1818 | như app | ✓ |
| Nút primary (Tìm kiếm, compact) | cao 30, #1abc9c, 12px/600, radius 8, pad 4/10.4 | 30, như app | ✓ |
| Nút tertiary (Làm mới) | cao 30, trắng, viền rgb(226,232,240), chữ rgb(31,41,55) | như app | ✓ |
| Nút secondary (Cài đặt bộ lọc) | cao 32, viền rgb(203,213,225), chữ rgb(51,51,51); khi bật nền rgb(209,250,229) | như app | ✓ |
| Tiêu đề thẻ bảng | 15px/500 rgb(10,153,167) | như app | ✓ |
| th | 12px/700 rgb(10,124,136), nền gradient rgb(234,252,254)→rgb(210,244,249), đáy 2px rgb(32,217,234), pad 6/8, cao 33 | như app, cao 33 (cả 2 màn) | ✓ |
| td (v2-form-table) | pad 4/8, viền rgb(237,239,241) / list rgb(229,231,235) | pad 4/8, viền rgb(229,231,235) | ✓ |
| Ô tiền trong bảng | cao 32, 13px, viền rgb(209,213,219), radius 6, căn phải | như app (pad 4/8 so với 4/10 của app, để ô hẹp vừa số) | ≈ |
| Ô khoá | nền rgb(241,245,249), chữ rgb(71,85,105), viền rgb(226,232,240), not-allowed, opacity 1 | như app | ✓ |
| Mã (link) | rgb(40,83,157), gạch đứt rgb(183,196,207) | như app | ✓ |
| Badge (V2BaseBadge xs) | 11px/600, pad 4/8, radius 999, cao 27; nền rgba(màu,.1), viền rgba(màu,.2) | cùng màu/radius, nhưng bản nhỏ 10.5px pad 1/7 cao 19 (U6) | ≈ (cố ý) |
| Trang đang chọn | nền #1abc9c, 32×34 | như app | ✓ |
| Dòng đếm | 12px rgb(107,114,128) | như app | ✓ |
| Modal | content radius 3.2, shadow 0 0 8px rgba(154,161,171,.3); header pad 16, đáy 1px rgb(229,232,235); tiêu đề 14/800 rgb(52,58,64); icon tròn 28 nền (màu .1); footer pad 12; backdrop rgb(50,58,70) .5 | như app; confirm rộng 500, Lịch sử 800 (lg) | ✓ |
| $confirm danger | nút đồng ý rgb(220,38,38) đứng TRƯỚC nút Hủy; textarea viền rgb(206,212,218) cao 74 | như app | ✓ |

Chưa đo được, đang tự đặt: toast (vue-toasted), nút secondary màu xanh lá (Xuất Excel, màn đo không có nút này),
V2BaseDatePicker (mockup dùng ô chữ dd/mm/yyyy).

## 5. Kiểm Playwright (HTTP tĩnh, mỗi lần sửa đổi cổng 8761→8772, đã tắt đúng PID)

Viewport 1440×900 và 1280×900, cả 2 màn:

- Console: **0 lỗi, 0 cảnh báo**, gồm cả các luồng popup, duyệt, đổi quyền, đổi công ty.
- `thead tr` = 1. Mọi th cao **33px**, không th nào bị cắt chữ (scrollWidth ≤ clientWidth).
- rowSpan của ô Tên = số `tr` của khối, cho cả 12 khối màn 1 và 3 khối màn 2.
- Sticky:
  - Lúc chưa cuộn, đáy tiêu đề = đỉnh dòng 1 (275 = 275 ở màn 1, 281 = 281 ở màn 2), không đè.
  - Cuộn dọc 700px: tiêu đề vẫn dính đỉnh vùng cuộn (lệch 1px viền).
  - Cuộn ngang 400–500px: ô Tên lệch 0px.
  - z-index: th 5 > ô dính 2 > ô thường.
- Chỉ **1** vùng cuộn dọc (`pScroll` / `aScroll`). Trang cao 900 = khung nhìn, kể cả khi mở "Tìm kiếm nâng cao".
  Footer phân trang nằm ngay dưới đáy vùng cuộn (833 = 833), không đè.
- Phép tính (khối ABAC-FML7.5, giá vốn 86,500,000):
  - Hệ số Bán lẻ 1.5 cho giá 129,750,000. Loại 2–5 = 1.5 / 129,750,000. TMĐT = 1.95 / 168,675,000, ĐMGG 0.
  - Sửa giá Bán lẻ 120,000,000: loại 2–5 = 120,000,000, TMĐT = 156,000,000.
  - ĐMGG Bán lẻ 8: loại 2–5 = 8, TMĐT = 0.
  - Tick "Sửa tay · Giá" mở ô TMĐT. Sau đó đổi Bán lẻ, giá TMĐT giữ nguyên 150,000,000.
  - Giá vốn 90,000,000: Giá mới giữ nguyên, Giá công thức thành 135,000,000 (T9).
  - Giá hiệu lực hệ số 1.4 cho 126,000,000, không làm tròn (T7). Dòng hiệu lực TMĐT tự thêm, giá 163,800,000.
- Validate:
  - Báo đồng thời 3 lỗi: giá vốn trống "Bắt buộc phải nhập", hệ số 100 "Không được vượt quá 2 chữ số trước dấu phẩy",
    ngày hôm nay "Phải chọn ngày tương lai". Chưa lưu gì.
  - Sửa xong thì lưu được: Giá hiện tại cập nhật, lịch sử thêm 1 dòng.
  - Bấm Lưu khi không đổi gì: báo "Chưa có thay đổi". Bấm 2 lần liên tiếp chỉ lưu 1 lần.
- Duyệt:
  - Bật duyệt giá: nút đổi thành "Gửi duyệt", có popup xác nhận, sinh yêu cầu, 6 badge Chờ duyệt, Giá hiện tại không đổi.
  - Lọc Chờ duyệt / Không duyệt / Hết tồn ra đúng mã. Hết tồn chỉ ra mã có tồn 0.
  - Tick 2 yêu cầu rồi lọc còn 1: Set vẫn 2, có báo "(1 đang ẩn do bộ lọc)". Bỏ lọc: cả 2 vẫn tick.
  - Sửa hệ số 1.35 cho giá 177,525,000 = round(1.35 × 131,500,000 / 100) × 100, chênh +13,685,000.
  - Duyệt yêu cầu có giá hiệu lực hôm nay: ngày dời về ngày mai, cờ về 0, yêu cầu biến mất.
  - Không duyệt với lý do trống: báo "Vui lòng nhập lý do không duyệt", popup vẫn mở. Có lý do: cờ thành 2, màn 1 hiện
    badge Không duyệt + "Lý do không duyệt: …".
  - Duyệt hàng loạt ca PTG: popup cảnh báo giá đang chạy đã đổi.
- Popup Lịch sử (rộng 800): lọc "Thay đổi thông tin" còn 1/2 mục. Đóng được bằng nút Đóng hoặc bấm ra nền.
- Quyền: tắt 1657 hoặc 1658 thì màn tương ứng báo không được cấp quyền và mục menu ẩn. Tắt 1092 thì màn Duyệt không có cột Giá vốn.
- Ảnh chụp: `ERP-HRM/.playwright-mcp/final-{prices,approve}-{1440,1280}.png`, `mk-history.png`, `mk-approve-confirm.png`,
  `mk-reject.png`, `mk-bulk-confirm.png`, `mk-hub.png`.

### Kiểm lại sau khi áp Q1/Q2 (cổng 8773, đã tắt đúng PID) — 1440 và 1280

- Tắt 1092 ở màn Duyệt:
  - Tiêu đề còn `☐|#|Tên|ĐVT|Loại giá|Giá cũ|Giá mới|ĐMGG cũ|ĐMGG mới|Hiệu lực|Người cập nhật|Thời gian|Mã`, tức 0 ô nhập Hệ số.
  - Bảng không còn con số giá vốn nào. Bảng rộng 1540 = tổng bề rộng các th.
  - rowSpan đúng, th cùng cao 32px, 0 cột bị cắt chữ.
  - Đáy tiêu đề = đỉnh dòng 1 (280 = 280), 1 vùng cuộn dọc, trang cao 900.
- Sửa ô Giá mới thành 175,000,000 rồi Duyệt: giá áp vào công ty đúng 175,000,000, yêu cầu biến mất.
- Lịch sử khi chỉ có 1658: không có chữ "Giá vốn", không có chữ "Hệ số".
- Bật lại 1092: cột Giá vốn và Hệ số hiện lại.
- Q2: tắt duyệt rồi lưu mã đang chờ (CORGHI): yêu cầu chờ = 0, badge Chờ duyệt = 0.
- Console 0 lỗi, 0 cảnh báo. Ảnh: `.playwright-mcp/q1-approve-{1440,1280}.png`.
