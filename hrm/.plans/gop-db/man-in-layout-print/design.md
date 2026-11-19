# Màn in cũ → popup xem trước — @namdangit

## Bối cảnh
- 08/10/2026: màn in HĐLĐ (`/decision/labor-contract/733/print`) trên cổng chính lòi cả thanh menu phân hệ
  (107 file `pages/**/print*.vue` rơi về layout `default`; Topbar đổi từ 16–17/09 hiện nguyên menu).
- Vá tạm: khai `layout: 'print'` cho 105 màn (chưa commit).
- User chốt: chuyển hẳn các màn in cũ sang **popup xem trước** (skill `print-page` mục 0), bỏ trang `/print`.

## Quyết định đã chốt (08/10/2026)
1. Gọi popup bằng **plugin chung `this.$printPreview({...})`** (giống `$confirm`): tự mount
   `ReportPrintPreviewModal`, tự gọi API, không phải đặt thẻ modal ở từng màn.
2. **Được sửa component chung `ReportPrintPreviewModal`** — chỉ THÊM tuỳ chọn, mặc định giữ nguyên hành vi
   cho 86 màn đang dùng:
   - `contentCss(root)` — hàm sinh CSS nội dung thay cho `buildReportPrintCss` (mẫu Quyết định cần Times 16px,
     không ép 13/10px của mẫu ERP);
   - `pageMargin` — lề `@page` + padding tờ giấy (Quyết định: `20mm 15mm 20mm 25mm`, khớp file Word HĐLĐ);
   - `src` — nhúng TRANG IN tự dựng vào iframe (đợt 3; thay cho phương án slot ban đầu).
3. Làm cả 3 đợt:
   - **Đợt 1** — in CHI TIẾT Quyết định (~28 file, BE trả sẵn `template`).
   - **Đợt 2** — in DANH SÁCH (~50 file): FE dựng HTML bảng từ API danh sách sẵn có (helper chung), không thêm BE.
   - **Đợt 3** — báo cáo/phiếu tự dựng (~30 file): popup NHÚNG chính trang `/…/print?embed=1` bằng iframe.
4. Màn đã chuyển → **xoá file `print.vue` cũ** (tiền lệ commit `ed1c24e53`, tránh 2 nguồn CSS in).
5. Nhánh: làm thẳng trên `gop_db` (nhánh chính mới, `tpe` bỏ).

## CSS mẫu Quyết định
Nguồn duy nhất `utils/print/decisionPrintStyle.js` cho cả xem trước lẫn iframe in. Chuẩn là **bản in GIẤY cũ**
(cửa sổ in của `$printContent` nạp `editor.css` + `print-app.css`), không phải bản xem trước cũ (dính Bootstrap):
- Times New Roman 16px, giãn dòng **1.6**, lề **20/20/20/30mm** (Nghị định 30) — mặc định cho mọi mẫu;
- HĐLĐ: giãn 1.4 + lề 20/15/20/25mm (đã chỉnh tay trước đây, khớp file Word); phụ lục: giãn 1.4 + `compactTable`;
- trả h1–h6, padding/valign ô bảng, `img` về mặc định trình duyệt + ép `box-sizing: border-box` 2 bên
  (đo thật: thiếu mấy rule này thì xem trước lệch giấy tới 8% chiều cao).
- Bỏ phương án nạp file CSS ngoài vào iframe: gom hết vào 1 hàm để không còn 2 nguồn CSS.

## Đợt 3 — vì sao nhúng iframe chứ không viết lại (chốt 08/10/2026)
- 33 trang còn lại mỗi trang một bố cục + CSS in riêng (bảng cây, ô gộp, phiếu công tác…) và in bằng 5 cách khác
  nhau (`$printContent`, `doPrint`, `printPDF`, `printPackage`, `window.print()`). Viết lại thành HTML = 33 chỗ có
  thể lệch bản in đã được nghiệm thu.
- Cách làm: `this.$printPreview({ page: '/…/print?…' })` → popup hiện iframe trang đó kèm `embed=1`;
  `layouts/print.vue` ở chế độ nhúng ẩn thanh nút của trang và phơi `window.__hrmPrintPage()` (bấm hộ nút In sẵn có).
  Nút In của popup gọi hàm đó ĐỒNG BỘ trong cú bấm → trang con cùng origin hưởng user activation, `window.open`
  của `$printContent` không bị chặn. Bản in giữ nguyên 100%.
- Đánh đổi: mỗi lần mở popup, iframe khởi động lại app (tải lại dữ liệu khởi tạo ~ vài giây); trang `/print` vẫn tồn tại
  (người dùng không còn được dẫn tới bằng tab mới).
- Biên bản họp (3 tab Cuộc họp): BE đã trả HTML mẫu → dùng `{ url }` như 8 báo cáo đang làm, xoá trang `/print` cũ.
