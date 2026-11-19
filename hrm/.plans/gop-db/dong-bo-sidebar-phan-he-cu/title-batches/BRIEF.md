# Brief cho subagent — đặt tên màn trên topbar + bỏ cụm tiêu đề trong màn

## Bối cảnh
Repo FE: `D:\laragon\www\hrm\hrm-client` (Nuxt 2 / Vue 2, Options API). 4 phân hệ cũ (Nhân sự `pages/human`, Chấm công
`pages/timesheet`, Tính lương `pages/payroll`, Cơm `pages/rice`) vừa chuyển từ menu ngang sang sidebar hub
(`layout: 'subsystem'`). Layout hub có topbar hiện TÊN MÀN cạnh nút ☰ — giá trị lấy từ `$store.state.pageTitle`, do
từng page tự đặt qua mixin `@/utils/mixins/PageTitleMixin` (mixin watch `pageTitle` của component, commit vào store).
Các page cũ chưa đặt → topbar trống. Đồng thời các page cũ có CỤM TIÊU ĐỀ + BREADCRUMB riêng ngay trong màn (thường là
`<PageHeader :title=… :items=… [:fullname=…] />` từ `@/components/Page-header`, đôi khi là khối `page-title-box` /
`<h4 class="page-title">` tự viết) → user yêu cầu BỎ cụm đó, tên chuyển lên topbar.

## Việc phải làm với MỖI file trong lô của bạn
File lô là TSV: `file \t route \t (trống) \t nhãn menu khớp đúng route \t tên gợi ý screenTitleOf \t heading tìm thấy trong file`.

1. Thêm mixin: `import PageTitleMixin from '@/utils/mixins/PageTitleMixin'` và đưa vào `mixins: [...]` (giữ mixin cũ;
   chưa có mảng thì tạo).
2. Thêm computed `pageTitle()` trả chuỗi tên màn. Trước khi thêm, grep trong file: KHÔNG được có `pageTitle` ở data/props/
   methods (Vue 2: computed trùng tên data bị bỏ qua âm thầm). Nếu trùng thì đổi cách (đặt data `pageTitle` cho đúng).
3. Quy tắc tên (tiếng Việt, viết hoa chữ đầu, còn lại theo chính tả thường):
   - Màn danh sách có nhãn menu khớp (cột 4) → dùng NGUYÊN VĂN nhãn menu.
   - Màn Thêm → "Thêm <đối tượng>" (danh mục) hoặc "Tạo <phiếu/đơn …>" (chứng từ). Màn Sửa → "Sửa <đối tượng>".
     Màn Chi tiết → "Chi tiết <đối tượng>". Màn Duyệt → "Duyệt <đối tượng>" (màn duyệt danh sách: "<Đối tượng> chờ duyệt"
     hoặc theo nhãn menu nhóm Phê duyệt nếu đúng).
   - Sửa/Chi tiết/Duyệt 1 bản ghi: nếu bản ghi đã tải CÓ mã (code/số phiếu…) thì nối `: ${mã}`; chưa tải xong thì trả tên trần.
     Không có mã thì KHÔNG thay bằng tên — trừ hồ sơ nhân viên: dùng họ tên nhân viên (vd "Hồ sơ nhân viên: Nguyễn Văn A")
     nếu PageHeader đang truyền `fullname`.
   - Nếu page đang có `title` cho PageHeader và nó đúng nghĩa thì có thể dùng lại (`return this.title`), nhưng nếu nó sai
     (copy-paste kiểu "Thêm công ty" ở màn bộ phận) thì đặt đúng theo màn thật.
   - Màn đổi chế độ theo query/tab (vd add vs edit dùng chung 1 file) → tên đổi theo chế độ.
   - Màn ngoài menu, không rõ: đọc template/route để đặt tên mô tả đúng chức năng.
4. BỎ cụm tiêu đề + breadcrumb trong màn: xoá thẻ `<PageHeader … />` (và import + đăng ký component nếu không còn dùng,
   và data `items` breadcrumb nếu không còn ai dùng — grep trước khi xoá). Nếu là khối tiêu đề tự viết (`page-title-box`,
   `<h4 class="page-title">` đứng riêng làm tiêu đề màn) cũng bỏ. KHÔNG bỏ tiêu đề của card/bảng/khối nội dung, KHÔNG bỏ
   nút bấm nằm cùng hàng — nếu nút nằm trong cụm tiêu đề thì giữ nút, chỉ bỏ phần chữ tiêu đề/breadcrumb.
   Biến `title` vẫn được dùng chỗ khác (head(), in, …) thì giữ.
5. KHÔNG sửa file dùng chung (`components/**`, `utils/**`, `layouts/**`) — chỉ sửa file page trong lô. Không đổi logic khác,
   không format lại file, giữ kiểu xuống dòng (CRLF/LF) và thụt lề sẵn có. Không commit git, không chạy dev server/Playwright.
6. File rỗng / không phải component → bỏ qua, ghi vào báo cáo.

## Verify (bắt buộc trước khi báo xong)
Ghi danh sách file đã sửa ra 1 file txt (mỗi dòng 1 path tương đối `pages/...`), rồi chạy trong `hrm-client` (Git Bash):
`NODE_PATH=$PWD/node_modules node ../.plans/gop-db/dong-bo-sidebar-phan-he-cu/title-batches/parse.js <file-list.txt>`
→ phải ra `bad 0` (script parse template + script, kiểm mỗi page còn đúng 1 `layout: 'subsystem'`).
Thêm: `grep -L "PageTitleMixin"` trên danh sách phải rỗng; `grep -l "<PageHeader"` trên danh sách phải rỗng.

## Báo cáo trả về (ngắn)
Bảng `file → tên màn (biểu thức)`; danh sách file bỏ qua + lý do; chỗ nào phân vân (tên không chắc, cụm tiêu đề có nút) để
người điều phối rà lại. Kết quả verify (số ok/bad).
