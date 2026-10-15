# Brief D — Báo giá: Import Excel · Xuất Excel · In · Xem chi tiết · Lịch sử

> Nguồn: đọc code nhánh gop_db (CODE là chuẩn). Viết tắt đường dẫn:
> - FE = `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client/`
> - BE = `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api/`
> - `IDX` = FE `pages/assign/quotations/_id/index.vue` (màn Xem chi tiết)
> - `EDIT` = FE `pages/assign/quotations/_id/edit.vue` (màn Sửa / Làm giá; `create.vue` extends file này)
> - `QIM` = FE `pages/assign/quotations/components/QuotationImportModal.vue`
> - `QIS` = BE `Modules/Assign/Services/QuotationImportService.php`
> - `QC` = BE `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
> - `QEX` = BE `Modules/Assign/Export/QuotationExcelExport.php`
> - `PPV` = FE `components/assign/quotation/QuotationPrintPreview.vue`, `PCM` = FE `components/assign/quotation/QuotationPrintConfigModal.vue`
> - `SIS` = FE `components/assign/SystemInfoSection.vue`, `SLS` = BE `Modules/Assign/Services/SystemLogService.php`, `QHS` = BE `Modules/Assign/Services/QuotationHistoryService.php`

## 0. Bối cảnh chung (cần cho mọi mục)

**Trạng thái báo giá** (BE `Modules/Assign/Entities/Quotation.php:11-19, 66-77`): 1 Đang tạo (#64748B) · 2 Chờ TP duyệt (#D97706) · 3 Chờ BGĐ duyệt (#D97706) · 4 Đã duyệt (#16A34A) · 5 Đóng (#6B7280) · 6 Dừng (#DC2626) · 7 Trúng thầu (#7C3AED).
**Loại báo giá**: 1 Từ BOM (kế thừa BOM, cấu trúc hàng hoá khoá) · 2 Tự nhập (báo giá độc lập/trực tiếp) (`Quotation.php:21-22, 88-89`).
**Loại giảm giá (GG)** `discount_method`: null = Không GG · 1 = GG theo mặt hàng · 2 = GG theo tổng (`Quotation.php:28-30`).

**Đường vào menu** (không ghi URL trong tài liệu):
- Phân hệ Quản lý CSKH trước khi bán → **Báo giá** (FE `components/subsystem-menu/presale.js:63-68`).
- Phân hệ Bán hàng → nhóm **Bán hàng › Báo giá › Danh sách báo giá** (FE `components/subsystem-menu/sale-hub.js:41-48`).
- Phê duyệt › Dự án TKT › **Báo giá chờ duyệt** (`sale-hub.js:276-282`; `components/menu-sidebar.js:171`) — màn riêng hàng chờ duyệt.

---

## 1. IMPORT BÁO GIÁ TỪ EXCEL

### 1.1 Mở từ đâu / điều kiện
- Nút **"Import Excel"** (icon upload `ri-upload-2-line`) nằm trên thanh công cụ của bảng "Chi tiết báo giá" trong **màn Sửa / Làm giá**, cạnh các nút "Thu gọn/Mở rộng tất cả", "Ẩn/Hiện cột chi tiết", "Xuất Excel" (EDIT:382-399).
- Điều kiện hiện nút: `canEdit && !isCreateMode` (EDIT:396).
  - **Không có ở màn Tạo mới** (chưa có id báo giá) — `create.vue` override `isCreateMode = !item.id` (FE `pages/assign/quotations/create.vue:8-10`). Phải lưu báo giá trước.
  - `canEdit` = báo giá ở trạng thái **Đang tạo (1)** VÀ người đang đăng nhập là **người lập** báo giá (EDIT:1715-1720).
- Phòng thủ khi chưa có id: toast lỗi **"Vui lòng lưu báo giá trước khi import."** (EDIT:5138-5143).
- BE chặn lại (không gắn quyền riêng — route không có checkPermission, BE `Modules/Assign/Routes/api.php:658-662`):
  - Báo giá phải nằm trong phạm vi xem của user (`scopedQuotationQuery`), không thấy → 404 **"Không tìm thấy báo giá."** (QC:519-525, 569-575).
  - Trạng thái ≠ Đang tạo → 422 **"Chỉ được import khi báo giá ở trạng thái Đang tạo."** (QC:527-532, 577-582).
  - Không có quyền nào riêng cho Import (quyết định #5 spec — QC route comment api.php:658-659).

### 1.2 Bố cục popup
Tiêu đề **"Import báo giá từ Excel"**, mô tả dưới tiêu đề: *"Import hàng hoá, dịch vụ, giảm giá và chi phí vận chuyển vào báo giá — chọn phương thức (từng phần / thay thế) khi bấm Import"* (QIM:38-43). Popup cỡ xl; không cho bấm nền đóng khi đang xử lý (QIM:29).

Thanh công cụ 3 nhóm (QIM:52-114):
| Nhóm | Nút | Trạng thái |
|---|---|---|
| File | **Chọn file Excel** (primary) | luôn bấm được |
| File | **Tải file mẫu** (secondary) | luôn bấm được; sau khi chọn file hiện tên file kèm icon Excel |
| Hành động | **Load lên bảng** | chỉ bấm được khi đã chọn file và không đang xử lý (QIM:78) |
| Hành động | **Validate** | chỉ bấm được khi bảng đã có dòng và không đang xử lý (QIM:90) |
| Hiển thị | **Chỉ dòng lỗi** ⇄ **Hiện tất cả** | bấm được khi bảng có dòng (QIM:106-112) |

Dải thống kê (hiện sau Validate hoặc khi có lỗi) (QIM:117-138): **Tổng: N · Hợp lệ: N · Lỗi: N**, link **"Xem chi tiết N lỗi"**, và nếu có dòng sẽ tự tạo danh mục: **"Tạo mới danh mục: N"**. Không có trạng thái "Chờ xác nhận" như Import BOM.

Bảng xem trước (QIM:161-247) — luôn hiển thị; cột: **#** (số dòng Excel), **Trạng thái**, rồi các cột dữ liệu (xem 1.4). Header cột bắt buộc có dấu `*` đỏ. Bảng rỗng: *"Chưa có dữ liệu. Chọn file Excel rồi bấm "Load lên bảng"."*; đang lọc không khớp: *"Không có dòng nào khớp bộ lọc đang bật."* (QIM:243).

Trạng thái dòng (QIM:1305-1310): **Chưa validate** (xám) · **Hợp lệ** (xanh) · **Hợp lệ (tạo mới)** (vàng — có Model/Thương hiệu/Xuất xứ/Dịch vụ chưa có danh mục) · **Lỗi** (đỏ). Dưới dòng Lỗi liệt kê từng lỗi dạng `[Tên cột] message`; dưới dòng vàng liệt kê cảnh báo (QIM:215-238).

Ô trên bảng: dòng "Hợp lệ" bị khoá cả dòng; ô dữ liệu chuẩn ERP (Tên hàng, Model, Thương hiệu, Xuất xứ, ĐVT, Thông số kỹ thuật) của hàng ERP khoá, tooltip: *"(Dữ liệu chuẩn của hệ thống — giá trị trong file bị bỏ qua, không sửa được)"* hoặc *"Ô do hệ thống quản lý (dữ liệu chuẩn ERP) — không sửa được."* (QIM:1311-1354). Ô chưa khoá **sửa trực tiếp được trên bảng**; sửa xong dòng về "Chưa validate" và phải Validate lại mới Import được (QIM:1331-1349).

Footer (QIM:251-282): dòng hướng dẫn *"Còn dòng lỗi thì sửa file rồi Validate lại. Bấm Import để chọn phương thức (từng phần / thay thế)."* · nút **Import** (primary) · **Làm mới** (xoá sạch trạng thái popup) · **Đóng**.
- Nút **Import** chỉ bấm được khi: đã Validate thành công, không còn dòng lỗi, bảng có dòng (QIM:568-577). Tooltip khi chưa bấm được: *"Còn dòng lỗi — sửa file rồi Validate lại."* hoặc *"Bấm Validate để kiểm tra dữ liệu trước khi Import."* (QIM:578-582).
- **Không có** checkbox/nút "Bỏ qua dòng lỗi" — báo giá import kiểu tất cả hoặc không (all-or-nothing) (QIM:252-253; QIS:24).

### 1.3 Các bước & thông báo nguyên văn
1. **Chọn file Excel** — chỉ nhận `.xlsx`, `.xls` (QIM:287, 646-653). Sai đuôi → alert đỏ: **"Định dạng file không hỗ trợ. Vui lòng chọn file Excel (.xlsx, .xls)."** Chọn file khác thì mọi kết quả cũ bị xoá (QIM:633-644).
   - **Không có giới hạn dung lượng file hay số dòng** trong code (FE/BE đều không kiểm).
2. **Tải file mẫu** — tải file TĨNH theo Loại GG của báo giá (không gọi BE) (QIM:660-672):
   - Không GG → `import_baogia_khong_gg.xlsx`; GG mặt hàng → `import_baogia_gg_mat_hang.xlsx`; GG tổng → `import_baogia_gg_tong.xlsx` (FE `static/`).
3. **Load lên bảng** — đọc file ngay trên trình duyệt (sheet ĐẦU TIÊN), dòng hiện "Chưa validate". Lỗi đọc file (QIM:1357-1486):
   - **"Vui lòng chọn file Excel trước."** (chưa chọn file)
   - **"Thiếu thư viện XLSX. Vui lòng tải lại trang rồi thử lại."**
   - **"Không thể đọc file. Vui lòng đóng file Excel nếu đang mở, sau đó thử lại."**
   - **"File Excel đang được bảo vệ bằng mật khẩu. Vui lòng gỡ mật khẩu trước khi tải lên."**
   - **"File Excel bị lỗi hoặc không đúng định dạng. Vui lòng kiểm tra lại file."**
   - **"Không tìm thấy sheet dữ liệu trong file Excel."**
   - **"File không đúng mẫu: không tìm thấy khu vực "Khai báo hàng hoá - dịch vụ"."** (không có dòng header chứa cả "Tên hàng" và "Mã hàng")
   - **"File không có dòng dữ liệu nào để import."**
   - Fallback: **"Không đọc được file Excel."**
   - Nhận diện header khoan dung: bỏ dấu `*`/`(*)` cuối; "Nhóm hàng cha"→"Nhóm hàng cha (Cấp 1)", "Nhóm hàng con"→"Nhóm hàng con (Cấp 2)" (QIM:1396-1402). Bỏ 2 dòng hướng dẫn dưới header của file mẫu (cột Loại = "Bắt buộc", "Nhập tự do", "Tùy chọn", "Nhập liệu", bắt đầu "Chọn 1 giá trị…" hoặc "(") (QIM:1406-1411). Dòng trống bị bỏ; 2 cột "Hình ảnh", "Thời gian bảo hành" không tính là dữ liệu (QIM:436, 1474-1477).
4. **Validate** — gửi dữ liệu lên BE kiểm tra (không ghi DB) (QIM:746-801; QC:515-556).
   - Thiếu id: **"Không xác định được báo giá để import."**; chưa Load: **"Chưa có dữ liệu. Hãy bấm "Load lên bảng" trước."**
   - Thành công: toast **"Dữ liệu hợp lệ. Bấm "Import" để ghi đè báo giá."**; bảng dựng lại từ dữ liệu đã chuẩn hoá (hàng ERP lấy theo master), mọi dòng "Hợp lệ"/"Hợp lệ (tạo mới)"; các cột công thức tính lại (QIM:948-1148).
   - Có lỗi (422): dòng lỗi tô đỏ + lỗi dưới dòng; lỗi không thuộc dòng nào hiện trong alert trên bảng; alert: **"Phát hiện N lỗi dữ liệu. Sửa các dòng bôi đỏ trong file Excel rồi bấm Validate lại."** + link **"Xem bảng lỗi"**; toast cảnh báo **"Import thất bại: N lỗi dữ liệu."**; tự mở popup lỗi (QIM:810-856).
   - Lỗi khác: **"Có lỗi khi kiểm tra dữ liệu import."** (fallback; lưu ý FE ưu tiên `e.message` của axios trước message BE — QIM:790-793, nên lỗi 422 do trạng thái có thể hiện chuỗi kỹ thuật "Request failed with status code 422" thay vì câu BE).
5. **Popup báo lỗi** (QIM:347-414): tiêu đề **"Import thất bại: Phát hiện N lỗi dữ liệu"**; bảng 3 cột **Dòng Excel | Tên cột sai | Mô tả chi tiết**; lỗi sắp theo số dòng Excel tăng dần, lỗi không gắn dòng xếp cuối (QIS:773-805). Nút:
   - **Sao chép lỗi** → toast **"Đã sao chép N lỗi vào clipboard."** / lỗi: **"Không sao chép được. Vui lòng bôi đen và sao chép thủ công."**
   - **Tải File lỗi** → tải CSV `loi_import_bao_gia_YYYYMMDD_HHmmss.csv`, toast **"Đã tải file lỗi: <tên file>"** (QIM:902-923)
   - **Đóng**.
6. **Import** → mở popup **chọn phương thức** (QIM:295-341, 1227-1234):
   - Tiêu đề **"Chọn phương thức import"**; nếu file xuất từ **báo giá khác** (cột ẩn "ID Báo Giá" ≠ báo giá đang sửa) tiêu đề đổi thành **"Phát hiện dữ liệu thuộc báo giá khác"** kèm cảnh báo *"Dữ liệu trong file thuộc một báo giá khác. Bạn có chắc muốn sao chép sang báo giá này?"*, nút OK đổi chữ **"Sao chép"** (mặc định **"Import"**), nút **"Huỷ"**.
   - Lựa chọn **"Import từng phần"** (mặc định): *"Giữ nguyên dòng đang có không xuất hiện trong file, cập nhật dòng khớp, thêm dòng mới."*
   - Lựa chọn **"Thay thế hoàn toàn"** (chỉ báo giá Tự nhập; nút OK chuyển màu đỏ): *"Xoá toàn bộ dòng đang có rồi đổ lại từ đầu theo file. Thao tác không thể hoàn tác."*
   - Báo giá kế thừa BOM: chỉ có "từng phần", ghi chú *"Báo giá kế thừa BOM có cấu trúc cố định — chỉ hỗ trợ cập nhật từng phần."*
7. Xác nhận → BE chạy lại validate 2 lượt (lượt 1 còn lỗi đỏ thì trả lỗi, KHÔNG tạo danh mục; lượt 2 tự tạo danh mục mới + trả id thật) (QC:557-606; QIM:1241-1280). Thành công: popup đóng, dữ liệu đổ vào lưới màn Sửa, toast **"Đã nạp dữ liệu từ file Excel. Kiểm tra lại rồi bấm "Lưu báo giá" để chốt."** (EDIT:5236-5238). Lỗi: **"Có lỗi khi import dữ liệu."** (fallback).

### 1.4 Sau Import — có cần bấm Lưu không?
- **CÓ.** Import KHÔNG ghi báo giá; chỉ đổ dữ liệu lên lưới màn Sửa. Phải bấm **"Lưu báo giá"** mới lưu (QIS:20-22; EDIT:5146-5238). Ngoại lệ: danh mục Model/Thương hiệu/Xuất xứ/Dịch vụ-Chi phí mới đã được **tạo thật** ở bước Import kể cả khi không bấm Lưu (QC:557-566; QIS:2384-2427, 2732-2773).
- Cách đổ (EDIT:5152-5500):
  - **Báo giá Tự nhập – Thay thế**: dựng lại toàn bộ nhóm + hàng hoá + dịch vụ từ file.
  - **Báo giá Tự nhập – Từng phần**: khớp theo id dòng (cột ẩn "ID Hệ Thống", chỉ khi file xuất từ chính báo giá này): dòng khớp → cập nhật; dòng không khớp → thêm mới; dòng đang có không có trong file → giữ nguyên.
  - **Báo giá từ BOM**: chỉ ghi đè giá nhập, giá bán, VAT, ghi chú, GG theo từng dòng BOM; không thêm/bớt dòng.
  - Dịch vụ & chi phí khác: thay thế = thay cả danh sách; từng phần = gộp theo id.
  - Chi phí vận chuyển, Giảm giá tổng (GG tổng) luôn lấy theo file.
  - GG tổng: sau import cờ "phân bổ lại" bật (cần phân bổ lại) (EDIT:5232-5234).

### 1.5 Cấu trúc file mẫu (FE `static/import_baogia_*.xlsx`, kiểm bằng openpyxl)
Sheet 1 = dữ liệu, Sheet 2 = "huong_dan" (hướng dẫn điền). Header có `*` = bắt buộc. Hàng 2 = loại nhập (Bắt buộc/Tùy chọn/Nhập tự do/Nhập liệu/(Công thức Excel)/Khóa / Nhập liệu), hàng 3 = mô tả, từ hàng 4 = dữ liệu mẫu (phải xoá trước khi import — hướng dẫn mục 4).

**Không GG (23 cột A→W)**: Loại (*) · Có tính doanh thu · Nhóm hàng cha · Nhóm hàng con · STT* · Mã hàng cha · Mã hàng* · Tên hàng* · Model · Thương hiệu* · Xuất xứ* · Thông số kỹ thuật · Ghi chú · ĐVT* · Số lượng* · Đơn Giá nhập · Thành tiền nhập · Đơn Giá bán · Thành tiền bán · Tỷ suất lợi nhuận (%) · Thuế VAT (%) · Giá trị VAT · Thành tiền sau VAT.
**GG mặt hàng (26 cột A→Z)**: như trên + chèn **GG(%) · GG(đ) · Đơn giá sau GG** sau "Đơn Giá bán".
**GG tổng (25 cột A→Y)**: có thêm **Khối 1 "KHU VỰC CẤU HÌNH GIẢM GIÁ TỔNG (Nhập nếu có)"** ở đầu: STT · Loại GG · Kiểu · Giá trị · Thành tiền GG (hướng dẫn: "(Bắt buộc)", "Dropdown (%,đ)", "khi chọn %, Giá trị = % nhân với tổng giá trị đơn hàng (Bao gồm Vận chuyển, Dịch vụ & chi phí, Hàng hóa trước giảm giá)"); sau đó **Khối 2 "KHU VỰC KHAI BÁO HÀNG HÓA - DỊCH VỤ"** chèn **Đơn giá sau GG · Phân bổ GG** sau "Đơn Giá bán".
Cột công thức (Thành tiền nhập, Đơn giá sau GG, Thành tiền bán, Tỷ suất, Giá trị VAT, Thành tiền sau VAT) — import **bỏ qua**, hệ thống tự tính lại (QIS:46-47).
Hướng dẫn sheet 2: phân cấp nhóm bằng [Nhóm hàng cha]/[Nhóm hàng con]; cấu trúc sản phẩm bằng [STT] + [Mã hàng cha]; báo giá kế thừa BOM "không được phép điều chỉnh/sửa đổi vị trí, các thông tin hàng hóa/dịch vụ từ bom, chỉ được bổ sung thêm mới phần chi phí vận chuyển, dịch vụ & chi phí khác"; "Dữ liệu màu đỏ là dữ liệu mẫu, trước khi import cần xóa dữ liệu mẫu đi".

Ghi chú: `GET export-blank-template` (QC:1689-1700, QEX::forBlank) có tồn tại ở BE (tên file `Mau_import_bao_gia.xlsx`) nhưng **FE không gọi** — nút "Tải file mẫu" dùng 3 file tĩnh.

### 1.6 Quy tắc validate từng cột (BE QIS) — thông báo nguyên văn
`{dòng}` trong message = giá trị cột STT của dòng (nếu trống thì số dòng Excel) (QIS:1709-1714); khối GG tổng dùng " tại dòng {số dòng Excel}" (QIS:1698-1701). Mỗi lỗi có cột "Dòng Excel" = "Dòng N".

**Chung**
- Dòng trống (mọi cột import đọc đều trống) → bỏ qua (QIS:1605-1614).
- **STT** — bắt buộc, duy nhất toàn file, dạng `1` hoặc `1.1`, tối đa 2 cấp (QIS:230-285):
  - "STT tại dòng {N} không được để trống."
  - "Sai định dạng cây cấu trúc."
  - "STT {x} vượt quá 2 cấp."
  - "STT {x} bị trùng lặp."
  - STT chỉ quyết định thứ tự; quan hệ cha-con do cột **Mã hàng cha** quyết định.
- **Loại** — chỉ nhận "Hàng hoá"/"Hàng hóa", "Dịch vụ & Chi phí khác"/"Dịch vụ và Chi phí khác", "Chi phí vận chuyển" (không phân biệt hoa thường) (QIS:851-864): "Loại hạng mục tại dòng {dòng} không tồn tại trong hệ thống."
- **Nhóm hàng cha/con** (báo giá Tự nhập) (QIS:299-370): "Nhóm hàng cha tại dòng {dòng} không được trống." (có nhóm con mà thiếu nhóm cha) · "Nhóm hàng cha tại dòng {dòng} vượt quá 255 ký tự." · "Nhóm hàng con tại dòng {dòng} vượt quá 255 ký tự." Nhóm trùng tên (không phân biệt hoa thường/khoảng trắng) gộp làm 1.
- **Mã hàng cha** (chỉ dòng Hàng hoá): tìm dòng cha gần nhất PHÍA TRÊN, CÙNG nhóm lá, có Mã hàng trùng (QIS:377-403): "Không tìm thấy Mã hàng cha {mã} ở phía trên cùng nhóm (dòng {dòng})."
- **Mã hàng**: "Mã hàng tại dòng {dòng} vượt quá 255 ký tự." (QIS:992-995). Hàng tạm để trống → mã tự sinh khi **Lưu** (QIS:1148-1149; file mẫu: "nếu để trống hệ thống sẽ tự sinh ra theo quy chuẩn hàng tạm").
- **Ghi chú**: "Ghi chú tại dòng {dòng} vượt quá 500 ký tự cho phép." (QIS:997-1001, 1320-1324)
- **Số lượng** (hàng hoá; dịch vụ/vận chuyển bỏ qua cột này, SL = 1) (QIS:1003-1006, 1857-1884): bắt buộc, ≥ 0 (**cho phép 0**), tối đa 3 số lẻ:
  - "Số lượng tại dòng {dòng} phải là số không âm."
  - "Số lượng tại dòng {dòng} vượt quá giới hạn cho phép." (≥ 1e14)
  - "Số lượng tại dòng {dòng} chỉ được tối đa 3 chữ số thập phân."
- Số được đọc khoan dung: chấp nhận "250,000,000", "250.000.000", "10.00%", "1.500.000đ", "VND" (QIS:1761-1802).

**Hàng hoá ERP (Mã hàng tra được trong danh mục hàng hoá ERP)** (QIS:1018-1057, 2064-2084, 2500-2567)
- Tên, Model, Thương hiệu, Xuất xứ, Thông số kỹ thuật, VAT **lấy từ ERP, bỏ qua file**.
- ĐVT: nếu ĐVT trong file là 1 ĐVT hợp lệ của sản phẩm đó thì dùng, không thì về **ĐVT cơ bản**.
- **Giá nhập/Giá bán lấy từ ERP** theo bảng giá của báo giá (`price_type_id`, mặc định 1 = Bán lẻ) và công ty; hàng ERP đơn (không cha/không con) lấy giá theo đúng ĐVT; hàng ERP là cha/con lấy giá ĐVT cơ bản; báo giá ngoại tệ thì chia tỷ giá (làm tròn 2 số lẻ). Giá trong file bị bỏ qua.
- "Mã hàng {mã} không tồn tại." — khi dòng cũ cùng mã của báo giá là hàng ERP nhưng mã không còn tra được ở ERP (QIS:1022-1030).

**Hàng tạm (không phải ERP)** (QIS:1058-1126)
- **Tên hàng** bắt buộc ≤ 255: "Tên hàng tại dòng {dòng} không được để trống." / "Tên hàng tại dòng {dòng} vượt quá 255 ký tự." (QIS:1815-1828)
- Độ dài: "Model tại dòng {dòng} vượt quá 255 ký tự." · "Thương hiệu … vượt quá 255 ký tự." · "Xuất xứ … vượt quá 255 ký tự." · "ĐVT tại dòng {dòng} vượt quá 50 ký tự." (QIS:1835-1842)
- **Thương hiệu, Xuất xứ bắt buộc**: "Thương hiệu tại dòng {dòng} là bắt buộc với hàng tạm." · "Xuất xứ tại dòng {dòng} là bắt buộc với hàng tạm." (QIS:1080-1088)
- **Model/Thương hiệu/Xuất xứ chưa có trong danh mục → KHÔNG chặn**: lúc Validate hiện cảnh báo vàng "Model "X" chưa có trong danh mục — sẽ tự tạo mới khi import." (tương tự "Thương hiệu", "Xuất xứ"); lúc bấm Import **tự tạo mới** danh mục (dò trùng tên không phân biệt hoa thường; Thương hiệu tự sinh mã từ chữ-số trong tên) (QIS:2339-2445).
- **ĐVT** không tự tạo: "ĐVT '{x}' tại dòng {dòng} không khớp với Master Data." (QIS:2371-2372). ĐVT trống được (không bắt buộc ở BE dù file mẫu ghi `*`).
- Thông số kỹ thuật: "Thông số kỹ thuật tại dòng {dòng} vượt quá 65535 ký tự." (QIS:1098-1102)
- **Thuế VAT (%)** chỉ dòng cha/độc lập (dòng con luôn 0): bắt buộc, 0–100: "Thuế VAT tại dòng {dòng} không hợp lệ." (QIS:1104-1111, 1887-1900)
- **Đơn Giá nhập** tùy chọn ≥ 0: **ô trống = GIỮ giá nhập cũ của dòng cùng Mã hàng** (không ghi 0 — vì người không có quyền xem giá vốn xuất file sẽ để trống cột này) (QIS:1113-1120, 1938-1959): "Đơn giá nhập tại dòng {dòng} không hợp lệ." · "… vượt quá giới hạn cho phép." (≥ 1e13)
- **Đơn Giá bán** bắt buộc ≥ 0: "Đơn giá bán tại dòng {dòng} không được để trống." · "Đơn giá bán tại dòng {dòng} không hợp lệ." · "Đơn giá bán tại dòng {dòng} vượt quá giới hạn cho phép." (QIS:1906-1930)
- **Hàng hoá dự án**: mã hàng tạm trùng mã trong "Hàng hoá dự án" của cùng dự án (BOM tổng hợp đã duyệt / báo giá tự lập Đã duyệt-Trúng thầu) → giữ mã, **lấy Tên/Model/TH/XX/ĐVT/TSKT từ bản ghi đó** (QIS:2099-2204).
- **Trùng mã hàng tạm mới** ở nhiều dòng mà khác Tên/ĐVT/Model/TH/XX/TSKT/Giá nhập/Giá bán/VAT: "Mã hàng {mã} xuất hiện ở nhiều dòng nhưng có sự khác biệt về thông tin định danh hoặc Giá nhập/Giá bán. Vui lòng kiểm tra và đồng bộ lại dữ liệu trong file Excel." (QIS:2211-2248)
- **Giá sàn cha–con (chặn lỗ)**: hàng cha TẠM có con → Thành tiền bán cha (giá bán × SL) không được nhỏ hơn Σ thành tiền bán các con (dung sai 0.01). **Hàng cha ERP được miễn** (combo ERP có thể rẻ hơn tổng linh kiện) (QIS:1191-1234): "Đơn giá bán của Cụm thiết bị tại dòng {STT} không được nhỏ hơn tổng giá bán của các thiết bị thành phần." (Plan `.plans/quotation-import-floor-erp-exempt/plan.md` là rule GIÁ VỐN cha ≥ Σ con ở luồng Lưu/Gửi duyệt — cha ERP cũng được miễn; import không kiểm giá vốn.)

**Giảm giá theo dòng** (QIS:1979-2052) — dòng con không có GG:
- Không GG: bỏ qua mọi cột GG.
- **GG mặt hàng**: đọc **GG(đ) trước**; > 0 thì dùng và tự tính ngược %; bỏ qua GG(%). GG(đ) trống/0 thì đọc GG(%) và tính ra tiền (làm tròn 2 số lẻ).
  - "GG(đ) tại dòng {dòng} không được lớn hơn đơn giá bán."
  - "GG(%) tại dòng {dòng} phải trong khoảng 0 đến 100%."
  - "GG(đ)/GG(%) tại dòng {dòng} không hợp lệ." / "… vượt quá giới hạn cho phép."
- **GG tổng**: bỏ GG(%)/GG(đ), chỉ đọc **Phân bổ GG** (≥ 0, trống = 0): "Phân bổ GG tại dòng {dòng} không hợp lệ."

**Dịch vụ & Chi phí khác** (QIS:2599-2725)
- Dòng có Nhóm hàng / tham gia cây cha-con / có Model-TH-XX-TSKT / Mã trùng dòng hàng đang có → coi là dòng **trong lưới hàng hoá**; còn lại → danh sách dịch vụ riêng (B — Dịch vụ & Chi phí khác).
- **Có tính doanh thu** bắt buộc, chỉ "Có"/"Không" (có thể không dấu): "Có tính doanh thu tại dòng {dòng} không tồn tại trong hệ thống. Chỉ nhập Có hoặc Không." — Có → nhóm II Dịch vụ; Không → nhóm III Chi phí.
- **Tên** bắt buộc: "Tên hàng tại dòng {dòng} không được để trống." Tên khớp danh mục Chi phí/Dịch vụ ERP → lấy tên chuẩn, VAT, tỷ lệ giá vốn từ danh mục. Chưa có → cảnh báo vàng "Dịch vụ / chi phí "X" chưa có trong danh mục — sẽ tự tạo mới khi import." và **tự tạo** khi Import (VAT theo file, cờ doanh thu theo cột, tỷ lệ giá vốn 0).
- SL luôn 1; Đơn giá bán bắt buộc; Đơn giá nhập trống = giữ giá cũ (chỉ khi file của chính báo giá này); dịch vụ không có Mã/ĐVT trên lưới.

**Chi phí vận chuyển** (QIS:1538-1602)
- Tối đa 1 dòng: "Chỉ được khai báo tối đa 1 dòng Chi phí vận chuyển." (mỗi dòng thừa 1 lỗi)
- Đơn Giá bán bắt buộc (= Chi phí vận chuyển); Đơn Giá nhập tùy chọn (trống = giữ cũ); **VAT cố định 8%** bỏ qua file; GG mặt hàng đọc GG(đ); GG tổng đọc Phân bổ GG. Không có dòng → vận chuyển = 0.

**Khối Giảm giá tổng** (chỉ đọc khi báo giá GG tổng) (QIS:435-549)
- Dòng trống bỏ qua. Loại GG khớp theo mã trước rồi theo tên trong danh mục Loại giảm giá:
  - "Loại giảm giá tại dòng {N} không được để trống."
  - "Loại giảm giá '{x}' tại dòng {N} không tồn tại trong hệ thống. Vui lòng chọn đúng danh mục."
  - "Kiểu giảm giá tại dòng {N} không hợp lệ. Chỉ nhập % hoặc đ."
  - "Giá trị giảm giá tại dòng {N} phải lớn hơn 0." / "Giá trị giảm giá tại dòng {N} không được vượt quá 100%."
  - "Thành tiền giảm giá tại dòng {N} phải lớn hơn 0." / "Thành tiền giảm giá tại dòng {N} vượt quá giới hạn cho phép."
- Kiểu % → Thành tiền GG **tính lại** = % × tổng bán gộp (hàng cha + dịch vụ + vận chuyển, trước GG), làm tròn 2 số lẻ (QIS:750-761).

**Báo giá kế thừa BOM** (QIS:1254-1450)
- Mã hàng phải thuộc BOM gốc: "Mã hàng {mã} tại dòng {dòng} không thuộc BOM gốc. Báo giá kế thừa BOM không cho phép thêm hàng hoá mới."
- Không được đổi: "Không được phép thay đổi số lượng của vật tư thuộc cấu trúc BOM." · "{Tên hàng|Thông số kỹ thuật|Model|ĐVT} tại dòng {dòng} không khớp với BOM gốc." · "Nhóm hàng tại dòng {dòng} không khớp báo giá gốc (nhóm '{tên}')."
- Dòng ERP: giữ nguyên giá/VAT đang có (file không đổi được). Dòng tạm: đọc Giá nhập/Giá bán/VAT như hàng tạm.
- Giá sàn cha–con (cha tạm): "Đơn giá bán của hàng cha "{tên}" không được nhỏ hơn tổng giá bán của các hàng con."
- Dòng BOM vắng trong file → giữ nguyên, không lỗi.
- File xuất từ báo giá khác thuộc BOM khác: "⚠️ Không thể import dữ liệu từ BOMLIST khác cấu trúc." (QIS:653-660)

**Cột ẩn định danh** (file xuất từ hệ thống): "ID Hệ Thống" (id dòng), "ID Báo Giá", "ID BOM" (QIS:77-79). File của chính báo giá → luồng cập nhật theo id dòng; id dòng không thuộc báo giá: "ID Hệ thống {id} không hợp lệ hoặc đã bị thay đổi. Vui lòng không can thiệp vào cột ẩn." (QIS:1132-1143).

**Giá vốn trong kết quả import** (QIS:585-588, 2451-2454): người không có quyền "Xem giá vốn hàng hoá" → giá nhập hàng ERP trả trống; hàng tạm hiện nếu là người tạo báo giá.

---

## 2. XUẤT EXCEL

### 2a. Xuất Excel theo file mẫu (export-quotation-data) — **nút đang dùng trên màn Báo giá**
- Nút **"Xuất Excel"** (icon download) ở **footer màn Xem chi tiết** — luôn hiện, đang tải đổi chữ **"Đang xuất..."** và khoá nút (IDX:683-694, 1607-1629).
- Nút **"Xuất Excel"** (icon Excel) trên thanh công cụ bảng ở **màn Sửa / Làm giá** — hiện khi không phải tạo mới (EDIT:392-395, 5111-5136).
- Không có điều kiện trạng thái/quyền riêng; BE chỉ chặn ngoài phạm vi xem → 404 "Không tìm thấy báo giá." (QC:1712-1745).
- Lỗi: toast **"Không xuất được file Excel. Vui lòng thử lại."** (IDX:1625; EDIT:5134).
- **Tên file tải về**: `{Mã báo giá}_{DD-MM-YYYY}.xlsx` (FE tự đặt — IDX:1619; EDIT:5119-5122; fallback "BaoGia" nếu thiếu mã). (BE tự sinh `{mã}_{ddmmyyyy}.xlsx` — QEX:327-334 — nhưng FE ghi đè tên.)
- **Nội dung** (QEX + blade BE `resources/views/exports/assign/quotation_excel.blade.php`) — **cùng khuôn với file mẫu import** để import lại được (round-trip):
  - **Không có logo / letterhead / khối thông tin khách hàng / chữ ký** — chỉ có bảng dữ liệu.
  - GG tổng: dòng 1 tiêu đề **"KHU VỰC CẤU HÌNH GIẢM GIÁ TỔNG"**, dòng 2 header (STT · Loại GG · Kiểu · Giá trị · Thành tiền GG), các dòng GG tổng (không có → 5 dòng trống), 1 dòng trống, tiêu đề **"KHU VỰC KHAI BÁO HÀNG HOÁ - DỊCH VỤ"**, header, dữ liệu. Không GG / GG mặt hàng: header hàng hoá ở dòng 1 (QEX:500-521).
  - Cột khối 2 (QEX:118-172): Loại · Có tính doanh thu · Nhóm hàng cha (Cấp 1) · Nhóm hàng con (Cấp 2) · STT · Mã hàng cha · Mã hàng · Tên hàng · Model · Thương hiệu · Xuất xứ · Thông số kỹ thuật · Ghi chú · ĐVT · Số lượng · Đơn Giá nhập · Thành tiền nhập · Đơn Giá bán · [GG mặt hàng: GG(%) · GG(đ) · Đơn giá sau GG] / [GG tổng: Đơn giá sau GG · Phân bổ GG] · Thành tiền bán · Tỷ suất lợi nhuận (%) · Thuế VAT (%) · Giá trị VAT · Thành tiền sau VAT · **Hình ảnh** · **Thời gian bảo hành** · 3 cột ẩn (ID Hệ Thống, ID Báo Giá, ID BOM).
  - 2 cột Hình ảnh + Thời gian bảo hành **luôn có** (có thể tắt bằng tham số `with_image=0`/`with_warranty=0`, FE không dùng) (QC:1731-1739); ảnh nhúng thật vào ô (cao ~60px), lấy từ ảnh sản phẩm ERP; bảo hành dạng "X tháng/ngày/năm"; hàng tạm/dịch vụ để trống (QEX:766-806).
  - Thứ tự dòng: theo nhóm (nhóm cha → nhóm con) → hàng cha → hàng con; STT `1`, `1.1`…; dịch vụ rồi vận chuyển nối tiếp STT (QEX:723-759, 1080-1174). Dòng con lặp nhóm của cha, "Mã hàng cha" = mã dòng cha. Vận chuyển chỉ có khi chi phí vận chuyển > 0, tên "Chi phí vận chuyển", SL 1.
  - Cột công thức là **công thức Excel thật**: Thành tiền nhập = SL × Đơn giá nhập; Đơn giá sau GG (GG mặt hàng: nếu GG(đ)>0 thì Giá bán − GG(đ), không thì Giá bán × (1 − GG%/100); GG tổng: Giá bán − Phân bổ GG/SL); Thành tiền bán = SL × (Đơn giá sau GG hoặc Đơn giá bán); Tỷ suất = ROUND((Giá bán − Giá nhập)/Giá nhập×100, 2); Giá trị VAT = Thành tiền bán × VAT/100; Thành tiền sau VAT = Thành tiền bán + VAT. Dòng con để trống các cột này và cột GG (QEX:1197-1285). Thành tiền GG (kiểu %) = Giá trị% × tổng bán gộp (QEX:641-702).
  - Định dạng: tiền `#,##0`, Số lượng `#,##0.##`, cột % General; header nền #D9E1F2 đậm; Thông số kỹ thuật rộng 45, xuống dòng, HTML đã hạ về text thuần (QEX:394-437, 1049-1052). Chống công thức độc hại: ô text bắt đầu bằng "=" giữ nguyên là chữ (QEX:474-481).
  - "Có tính doanh thu": dịch vụ ghi Có/Không theo danh mục chi phí (không có → "Không") (QEX:1207-1213).
- **Giá vốn theo quyền** (QEX:297-307, 1303-1308): có quyền **"Xem giá vốn hàng hoá"** → thấy Đơn giá nhập/Thành tiền nhập/Tỷ suất mọi dòng; không có quyền nhưng là **người tạo báo giá** → chỉ thấy của hàng tạm/dịch vụ tự nhập/vận chuyển; còn lại để trống 3 cột này.

### 2b. Xuất Excel chi tiết "bản gửi khách" (export-excel)
- `GET .../{id}/export-excel` (QC:1392-1679) — **không dùng trên màn Báo giá** (EDIT:5107-5110 ghi rõ đã bỏ). Chỉ được gọi từ **tab Báo giá của màn Dự án TKT** (nút icon "Xuất Excel" — FE `pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue:196, 639-656`), tên file `BaoGia_{mã}.xlsx`; lỗi toast "Xuất Excel chưa được triển khai đầy đủ".
- Nội dung (class `App\ExcelExport\BomListExport`): cột mặc định stt, code, name, qty, uom, estimated_price, import_amount, sale_price, (GG theo loại), amount, profit_margin, vat_percent, vat_amount, after_vat, image, warranty; có dịch vụ, bảng giảm giá tổng, bảng tổng hợp theo nhóm chi phí; Tổng thành tiền nhập + TSLN chỉ khi có quyền "Xem giá vốn hàng hoá" (QC:1573-1673). Ngoài phạm vi màn này — nhắc qua nếu cần.

### 2c. Export bản trống (export-blank-template)
- BE có `GET .../export-blank-template?discount_method=` → file `Mau_import_bao_gia.xlsx` có dữ liệu mẫu (QC:1689-1700; QEX:313-334, 560-635). **FE không có nút gọi** — nút "Tải file mẫu" trong popup Import tải file tĩnh (mục 1.3).

---

## 3. IN BÁO GIÁ

### 3.1 Nút & điều kiện
- Màn Xem chi tiết: nút **"In"** (icon máy in) ở footer, **luôn hiện**, mọi trạng thái (IDX:695-702).
- Màn danh sách: hành động dòng **"In báo giá"** trong menu ⋮, luôn hiện (FE `pages/assign/quotations/index.vue:1189-1193`); bấm sẽ tải chi tiết rồi mở popup cấu hình; lỗi tải: toast **"Không tải được chi tiết báo giá"** (`index.vue:920-950`).
- Không có điều kiện quyền/trạng thái.

### 3.2 Popup "Cấu hình in báo giá" (PCM)
- Không có chọn mẫu in (chỉ 1 mẫu).
- Checkbox **"Hiện hàng hoá cấp con"** — mặc định tích (PCM:10-14).
- **"Chọn cột hiển thị"** + checkbox **"Chọn tất cả"** (PCM:18-35). Danh sách cột (PCM:89-117): STT · Tên hàng hoá · Mã hàng hoá · Model · Thương hiệu · Xuất xứ · Đơn vị tính · Thông số kỹ thuật · Ghi chú · Số lượng · Đơn giá bán · Thành tiền bán · [GG mặt hàng: GG (%) · GG (₫) · Đơn giá sau GG] / [GG tổng: GG phân bổ] · VAT (%) · Tiền VAT · Thành tiền sau VAT · **Hình ảnh** · **Thời gian bảo hành**.
- Mặc định tích **tất cả trừ "Mã hàng hoá"** (PCM:63-64, 124-129) ⇒ "Chọn tất cả" mặc định không tích.
- Không có cột giá nhập trong danh sách — bản in luôn ẩn giá vốn.
- Nút **"Huỷ"** · **"Xem trước"**. Không chọn cột nào → lỗi đỏ **"Vui lòng chọn ít nhất 1 cột để in"** (PCM:36-38, 136-146).

### 3.3 Popup "Xem trước báo giá" (PPV) + In
- Tiêu đề **"Xem trước báo giá"**, nút **"In"** cạnh tiêu đề (PPV:12-16). Bấm In → mở cửa sổ mới, chờ ảnh tải xong (tối đa 3 giây) rồi tự bật hộp thoại in; tiêu đề tab "Báo giá {mã}" (PPV:689-812).
- **Khổ giấy A4 NGANG**, lề 12mm (trên/dưới) × 10mm (trái/phải), font Times New Roman 13px (PPV `@page { size: A4 landscape; margin: 12mm 10mm; }`).
- **Bố cục** (PPV:18-219):
  1. **Letterhead**: ảnh header công ty toàn chiều ngang (cao tối đa 100px). Nguồn = `header` của **công ty của người đang đăng nhập** (`$store.state.employee_company`) — IDX:1067-1077, `index.vue:502-512`. ⚠️ Lệch quy tắc CLAUDE.md (phải theo `company_id` ghi trên chứng từ).
  2. Tiêu đề **"BÁO GIÁ HÀNG HÓA"** giữa trang.
  3. Khối thông tin 2 cột — Trái: **Kính gửi (ông/bà):** người liên hệ · **Tên đơn vị:** tên KH · **Địa chỉ:** · **Điện thoại/ Email:** "SĐT / email" · **Hiệu lực báo giá:** "Đến ngày dd/mm/yyyy" · **Bảo hành:** "X tháng". Phải: **Báo giá số:** mã · **Dự án:** tên dự án · **Ngày:** ngày lập · **Đại diện kinh doanh/ Email:** "Tên Sale phụ trách dự án / email" · **Giao hàng (ngày):** · **Loại tiền tệ:** tên tiền tệ.
  4. Câu dẫn: *"Chúng tôi xin gửi đến quý khách hàng báo giá thiết bị hàng hóa và dịch vụ như sau:"*
  5. **Bảng hàng hoá** theo cột đã chọn: dòng nhóm (La Mã I, II; nhóm con I.1…), dòng cha (STT 1,2…), dòng con (1.1…) nếu bật "Hiện hàng hoá cấp con" — trừ hàng cha ERP đã tắt hiện con. Dòng con: giá bán/thành tiền hiện nếu cha là hàng tự tạo, cha ERP hiện "—"; các cột GG/VAT của con "—". Khối **"Dịch vụ & Chi phí khác"** sau cùng. Dòng **"TỔNG CỘNG"** ở cột Tên (tổng Thành tiền bán, GG, Tiền VAT, Thành tiền sau VAT). Hình ảnh tối đa 60×90px; Thông số kỹ thuật giữ định dạng.
  6. **Bảng tổng hợp giá trị** (khi có breakdown): STT · Nhóm chi phí · Thành tiền trước VAT · [Giảm giá · Thành tiền sau GG (trước VAT) khi có GG] · Thuế VAT · Thành tiền sau VAT; dòng I Hàng hoá, II Dịch vụ, III Chi phí, IV Chi phí vận chuyển, V **Tổng giá trị báo giá** (kèm mã tiền tệ). **Luôn ẩn Thành tiền nhập** (bản gửi khách) (PPV:300-303). Ngoại tệ: dòng trên bảng "Tỷ giá: 1 {mã} = {tỷ giá} VND (dd/mm/yyyy) - Bảng giá bán lẻ" (PPV:396-404). Không có breakdown: bảng nhỏ Tổng doanh thu (trước GG) / Tổng giảm giá / Tổng doanh thu sau GG / Tổng VAT / Tổng thanh toán (sau VAT).
  7. **"Điều khoản báo giá:"** — nội dung điều khoản, đã thay biến động: {{VAT_NOTE}} ("Giá trên đã/chưa bao gồm thuế VAT"), {{VAN_CHUYEN_NOTE}} ("đã/chưa bao gồm chi phí vận chuyển"), {{NGAY}}/{{THANG}}/{{NAM}} (ngày in), {{SO_BAO_GIA}}, {{NGAY_BAO_GIA}}, {{HIEU_LUC_BAO_GIA}}, {{MA_KHACH_HANG}}, {{TEN_KHACH_HANG}}, {{TEN_DON_VI}}, {{DIA_CHI}}, {{DIEN_THOAI_LIEN_HE}}, {{EMAIL_LIEN_HE}}, {{NGUOI_BAO_GIA}}, {{EMAIL_NGUOI_BAO_GIA}}, {{TONG_THANH_TIEN}}, {{TONG_THUE}}, {{THANH_TIEN}}; biến lạ để trống (FE `utils/assign/quotation-term.js:47-86, 95-115`).
  8. **"Ghi chú:"** = Ghi chú Kinh doanh (nếu có).
  9. **Chữ ký** góc phải: "Ngày {d} Tháng {m} Năm {yyyy}" (ngày in) · **"ĐẠI DIỆN KINH DOANH"** · tên Sale phụ trách dự án.
- Số theo chuẩn quốc tế, làm tròn theo "Làm tròn" của báo giá (mặc định tối đa 2 số lẻ) (PPV:475-482).
- Hình ảnh / Thời gian bảo hành lấy từ master ERP theo hàng ERP; hàng tạm trống (BE `Modules/Assign/Transformers/DetailQuotationResource.php:169-202`).

---

## 4. XEM CHI TIẾT

### 4.1 Mở từ đâu
- Màn danh sách: bấm **Mã báo giá** (cột Mã là link; danh sách không còn nút "Xem chi tiết") (`index.vue:1130-1134`).
- Màn **Báo giá chờ duyệt** (mở kèm nguồn để sau Duyệt/Từ chối quay về hàng chờ) (IDX:852-853, 902-907, 931-936).
- Tab báo giá ở màn Dự án TKT.
- BE: xem được khi báo giá nằm trong phạm vi xem theo cấp tổ chức HOẶC đang chờ chính user duyệt; ngoài phạm vi → **"Không tìm thấy báo giá."** (QC:214-236). FE: đang tải "Đang tải..."; không có dữ liệu "Không tìm thấy báo giá."; lỗi tải toast **"Không tải được báo giá"** (IDX:4-5, 1544).

### 4.2 Tiêu đề
`Chi tiết báo giá: <b>{mã}</b> ({tên trạng thái, tô màu trạng thái}) {nhãn cấp duyệt}` — nhãn cấp duyệt: "Cấp 1 — Tự duyệt" / "Cấp 2 — TP duyệt" / "Cấp 3 — TP & BGĐ duyệt" (IDX:909-930).

### 4.3 Các khối (từ trên xuống — không có tab)
1. **Cảnh báo từ chối** (nếu có lý do từ chối): "Đã bị từ chối: {lý do}" (IDX:8-10).
2. **Ghi chú Mỏ neo** (báo giá dự án con có Báo giá Mỏ neo) (IDX:14-26): đồng bộ → "Hệ thống xác nhận: Tiền tệ, Giảm giá, Đơn giá hàng hoá đã đồng bộ 100% với Báo giá Mỏ neo {mã}. Đủ tiêu chuẩn gộp Báo giá tổng."; lệch → "Cảnh báo: báo giá đang lệch N điểm so với Báo giá Mỏ neo {mã}:" + danh sách.
3. **"Thông tin chung"** (thu gọn/mở được; đầu khối: "Người lập: …· Ngày tạo: …") (IDX:28-180). Bảng 2 cặp nhãn–giá trị:
   - Mã báo giá · YCBG (link mở popup chi tiết yêu cầu tính giá; ẩn với báo giá tự nhập)
   - BOM list (link mở tab mới "mã — tên"; ẩn với báo giá tự nhập)
   - Dự án (link tab mới) · Giải pháp ("mã — tên" + chip phiên bản; ẩn với báo giá tự nhập)
   - Hạng mục (nếu có, kèm phiên bản; ẩn với tự nhập)
   - Khách hàng · MST
   - Người liên hệ · SĐT liên hệ
   - Địa chỉ · Email khách hàng
   - Hiệu lực báo giá · Giao hàng (ngày)
   - Bảo hành (tháng) · Loại tiền tệ (tên tiền; ngoại tệ thêm "— Tỷ giá: 1 {mã} = {tỷ giá} VND (ngày lập)"; chip "Bảng giá: {tên bảng giá | Bán lẻ}")
   - Giai đoạn dự án (chỉ khi có dự án; icon ⓘ mô tả giai đoạn)
   - Ngày lập báo giá · Người lập báo giá
   - Ghi chú yêu cầu (nội dung định dạng)
4. **"Chi tiết báo giá"** (thanh công cụ ghim khi cuộn) (IDX:183-477): nhãn Giảm giá = badge "GG theo mặt hàng" / "GG theo tổng" / "Không áp dụng"; nút **"Thu gọn tất cả" ⇄ "Mở rộng tất cả"** (nhóm), **"Ẩn cột chi tiết" ⇄ "Hiện cột chi tiết"** (mặc định hiện).
   - Cột: STT · Mã (icon cảnh báo "Giá bán thay đổi ngày dd/mm/yyyy" nếu giá ERP vừa đổi) · Tên hàng (badge DV nếu dịch vụ; dòng ghi chú nội bộ) · [Model · Thương hiệu · Xuất xứ · Thông số kỹ thuật · Ghi chú — khi hiện cột chi tiết] · SL · ĐVT · Giá nhập ({mã tiền}) · Thành tiền nhập · Giá bán ({mã tiền}) · Thành tiền bán · [GG mặt hàng: GG(%) · GG(₫) · Đơn giá sau GG] / [GG tổng: GG phân bổ tự động (ⓘ "Tham khảo — tự tính theo tỷ lệ giá trị") · Phân bổ GG] · Tỷ suất LN (%) (xanh/đỏ theo ngưỡng "Tỷ suất lợi nhuận mức sàn") · VAT(%) · Tiền VAT · Thành tiền sau VAT.
   - Phần **A — Hàng hoá** (tổng phần trên dòng tiêu đề), nhóm La Mã thu/mở được, dòng cha, dòng con (STT x.y; hàng con không có thành tiền bán/GG/VAT; con của cha ERP ẩn nếu cha tắt hiện con).
   - Phần **B — Dịch vụ & Chi phí khác** "(N dòng)"; badge **CP** (không tính doanh thu) / **DV**; badge "Tỷ lệ giá vốn: X%" (tooltip "Giá vốn = Giá bán × tỷ lệ này"); trống: "Chưa có dịch vụ / chi phí".
   - Dòng **TỔNG**.
   - Giá nhập / Thành tiền nhập tổng / Tỷ suất tổng hiện "—" khi không có quyền **"Xem giá vốn hàng hoá"** (`can_view_cost_price` do BE trả — DetailQuotationResource.php:338-343).
5. **"Giảm giá tổng đơn hàng"** (chỉ GG tổng): Loại GG · Giá trị · dòng Tổng GG (IDX:482-494).
6. **"Tổng hợp giá trị báo giá"** (IDX:497-625): bảng theo nhóm chi phí I Hàng hoá · II Dịch vụ · III Chi phí · IV Chi phí vận chuyển · V Tổng giá trị báo giá; cột Thành tiền nhập chỉ khi có quyền giá vốn; Giảm giá + Thành tiền sau GG khi có GG. Có quyền giá vốn: thêm "TSLN trước GG: x%  TSLN sau GG: y%".
7. Khối **Điều khoản báo giá** (đã thay biến động), **Ghi chú nội bộ** (nếu có), **Ghi chú Kinh doanh** (chỉ khi trạng thái Đã duyệt) (IDX:629-668):
   - Người là **Sale phụ trách dự án**: ô nhập "Nhập ghi chú kinh doanh..." + nút **"Lưu ghi chú"** ("Đang lưu..."); toast **"Đã lưu ghi chú"** / lỗi **"Lỗi lưu"**. BE: chỉ khi Đã duyệt — "Chỉ có thể sửa ghi chú khi báo giá đã duyệt."; có dự án: chỉ Sale phụ trách — "Chỉ NV Kinh doanh phụ trách dự án mới có thể cập nhật ghi chú."; không dự án: chỉ người lập — "Chỉ người lập báo giá mới có thể cập nhật ghi chú." (BE `QuotationService.php:4281-4301`). ⚠️ FE chỉ cho sửa theo Sale dự án ⇒ báo giá không gắn dự án không hiện ô sửa.
   - Người khác: chỉ đọc.
8. **Khối "Lịch sử"** nằm ngay dưới (mục 5).

**Không có mục "Thông tin hệ thống" riêng** (người lập / ngày tạo nằm ở header khối Thông tin chung và các dòng "Ngày lập báo giá", "Người lập báo giá"; không hiển thị người cập nhật/ngày cập nhật).

### 4.4 Footer (thanh cố định) — thứ tự & điều kiện (IDX:671-773)
| Nút | Điều kiện hiện | Hành động / thông báo |
|---|---|---|
| **Quay lại** | luôn | về trang trước trong app; mở thẳng thì về Danh sách báo giá (IDX:1356-1362) |
| **Xuất Excel** | luôn | mục 2a |
| **In** | luôn | mục 3 |
| **Sao chép** | có quyền sao chép: BG từ YCBG → có 1 trong 2 quyền "Xây dựng giá bán theo công ty"/"…theo phòng"; BG tự lập → là Sale phụ trách dự án (không có dự án: người tạo) — mọi trạng thái (FE `utils/mixins/Assign/QuotationCopyMixin.js:78-101`) | gọi kiểm tra thay đổi ERP; có thay đổi → popup **"Phát hiện thay đổi dữ liệu từ ERP"** (cột Loại thay đổi · Mã / Tên vật tư · Thông tin cũ (V1) · Thông tin mới (Cập nhật) · Hành động hệ thống; nút "Xác nhận Sao chép báo giá" / "Hủy bỏ"); không thay đổi → mở thẳng màn Tạo mới điền sẵn. Không ghi DB tới khi Lưu. Lỗi: "Không kiểm tra được thay đổi từ ERP". Chữ khi chờ "Đang sao chép..." |
| **Sửa / Làm giá** | trạng thái Đang tạo VÀ là người lập (IDX:1015-1017) | sang màn Sửa |
| **Xoá** (đỏ) | như Sửa | hộp xác nhận tiêu đề **"Xác nhận xoá"**, nội dung **"Bạn có chắc muốn xoá báo giá '{mã}'?"**, nút "Xoá"/"Huỷ"; thành công toast **"Đã xoá báo giá"** → về danh sách; lỗi toast message BE hoặc **"Xoá thất bại"** (IDX:1371-1389). BE: "Báo giá không ở trạng thái Đang tạo, không thể sửa." / "Chỉ người tạo báo giá mới có thể sửa." (BE `QuotationService.php:4719-4727`); xoá kéo theo xoá dòng giá + lịch sử, trả YCBG về "Chờ xây dựng giá" nếu không còn báo giá nào (`QuotationService.php:1783-1802`) |
| **Duyệt** / **Duyệt & chuyển BGĐ** | có quyền "Trưởng phòng duyệt giá Bom giải pháp" VÀ trạng thái Chờ TP duyệt; chữ "Duyệt & chuyển BGĐ" khi cấp duyệt = 3 (IDX:1024-1026, 730-733) | xác nhận "Xác nhận duyệt": "Duyệt & chuyển BGĐ?" / "Duyệt báo giá?" (nút Duyệt/Huỷ); toast **"Đã duyệt báo giá"**, lỗi "Lỗi duyệt" → về danh sách nguồn (IDX:1549-1568) |
| **BGĐ duyệt** | quyền "Ban giám đốc duyệt giá Bom giải pháp" VÀ Chờ BGĐ duyệt | xác nhận "BGĐ duyệt báo giá?"; toast **"BGĐ đã duyệt báo giá"** (IDX:1569-1587) |
| **Từ chối** | (TP & Chờ TP duyệt) hoặc (BGĐ & Chờ BGĐ duyệt) | popup **"Từ chối báo giá"**: ô "Lý do từ chối" * ("Nhập lý do từ chối..."), nút "Huỷ"/"Xác nhận từ chối"("Đang gửi..."); trống → **"Vui lòng nhập lý do từ chối"**; toast **"Đã từ chối báo giá"**, lỗi "Không thể từ chối" → về danh sách nguồn (FE `components/assign/quotation/QuotationRejectModal.vue`) |
| **Chốt báo giá (Trúng thầu)** | BE cờ `can_finalize`: báo giá **không gắn dự án**, trạng thái Đã duyệt, là người lập (BE `Quotation.php:367-372`) | popup **"Xác nhận chốt báo giá"** (phụ đề Báo giá: {mã}): "Chốt báo giá {mã} thành Trúng thầu?" + bảng **"File xác nhận của khách hàng"** (bắt buộc — "Vui lòng đính kèm file xác nhận của khách hàng"); nút "Chốt"/"Huỷ"; toast **"Đã chốt báo giá (Trúng thầu)"**, lỗi "Lỗi chốt báo giá"; ở lại màn, nạp lại (FE `components/assign/prospective-project/FinalizeQuotationModal.vue`) |
| **Hủy chốt** | cờ `can_unfinalize`: không gắn dự án, Trúng thầu, chưa có hợp đồng, là người lập (`Quotation.php:375-381`) | popup **"Hủy chốt báo giá"**: "Hủy chốt báo giá {mã} — báo giá sẽ quay lại trạng thái "Đã duyệt"." + "Lý do hủy chốt" * (trống: "Bắt buộc phải nhập"); nút "Hủy chốt"("Đang lưu...")/"Huỷ"; toast **"Đã hủy chốt báo giá"**, lỗi "Lỗi hủy chốt" (FE `components/assign/quotation/UnfinalizeQuotationModal.vue`) |
| **Lập hợp đồng** | trạng thái Trúng thầu, chưa có hợp đồng, là người lập (không cần quyền) (IDX:1028-1036) | sang màn tạo hợp đồng |
| **Xem hợp đồng** | đã có hợp đồng (thay cho Lập hợp đồng) | sang chi tiết hợp đồng |

- **Không có nút "Lịch sử" ở footer** — đã có khối Lịch sử cuối trang (IDX:677). Không có "Gửi duyệt" ở màn xem (gửi duyệt nằm ở màn Sửa).
- Đối chiếu danh sách (`index.vue:1135-1199`): danh sách có Sửa / Làm giá, Xóa, Sao chép báo giá, Chốt báo giá (Trúng thầu), Hủy chốt, Lập hợp đồng, Xem hợp đồng, In báo giá, Lịch sử — không có Xuất Excel từng dòng, không có Duyệt/Từ chối (nằm ở màn Báo giá chờ duyệt).
- Lưu ý: nút Duyệt FE chỉ kiểm quyền + trạng thái, không kiểm phòng ban; BE chặn theo phòng (route `tp-approve` gắn checkPermission — `api.php:646-651`).

---

## 5. LỊCH SỬ

### 5.1 Mở từ đâu
- **Màn Xem chi tiết**: khối **"Lịch sử"** riêng, nằm ngay dưới nội dung, **mặc định thu gọn**; nút **"Xem lịch sử"** ⇄ **"Thu gọn"**; chỉ tải dữ liệu lần mở đầu; sau khi tải có nút **"Làm mới"** và số đếm dòng cạnh tiêu đề (IDX:825-828; SIS:7-31, 377-383).
- **Màn danh sách**: hành động dòng **"Lịch sử"** (icon history) → popup tiêu đề **"Lịch sử báo giá: {mã}"**, mở là thấy nội dung ngay (FE `components/assign/quotation/QuotationHistoryModal.vue:14-19, 59-62`; `components/modal/CatalogHistoryModal.vue`; `index.vue:1194-1198, 908-912`).
- Hai nơi dùng **cùng nguồn** `assign/system-logs/quotation/{id}` nên hiển thị giống hệt. (Endpoint cũ `GET .../{id}/histories` QC:1747-1773 không còn được FE dùng.)
- Không gate quyền xem riêng (SystemLogController::show chỉ trả log).

### 5.2 Giao diện
- Đang tải: spinner; lỗi: **"Không tải được lịch sử."** + nút **"Thử lại"**; rỗng: **"Chưa có lịch sử thao tác nào."** (SIS:35-53, 472).
- **Bộ lọc** (nút **"Bộ lọc"** bung/thu; vùng lọc ghim đầu khối; chọn là lọc ngay, không có nút Tìm kiếm) (SIS:61-117):
  - **Loại hành động** ("Chọn loại hành động"): 3 nhóm cố định **Tạo mới / Thay đổi thông tin / Thay đổi trạng thái** (SLS:64-72, 1921-1934).
  - **Người thực hiện** ("Chọn người thực hiện"): nhân viên cùng công ty với người tạo báo giá, khuôn "Tên - Mã phòng - Mã NV" (SLS:1942-1974).
  - **Từ ngày** / **Đến ngày** (dd/mm/yyyy).
  - Nút **"Làm mới"** xoá lọc. Không khớp: **"Không có lịch sử phù hợp bộ lọc."**
- **Dạng timeline** (không phải bảng cột), mới → cũ (SLS:1831-1889). Mỗi mục:
  - Thời gian `dd/mm/yyyy HH:mm`
  - **Nhãn hành động** (tô màu theo hành động)
  - "Người thực hiện: {họ tên}" + " — {tên phòng ban hiện tại}" (không có → "Hệ thống") (SIS:153-156, 433-435)
  - Danh sách thay đổi: trường đơn `{Trường}: {cũ (đỏ)} → {mới (xanh)}` (không có giá trị cũ thì chỉ hiện giá trị mới) (SIS:207-211); bảng con hiển thị theo nhóm **"{Bảng} thêm mới:"** (+ dòng "- Nhãn: giá trị — Nhãn: giá trị…"), **"{Bảng} đã xóa:"**, **"{Bảng} sửa thông tin:"** (+ "- {tên dòng}: Trường: cũ → mới; …") (SIS:162-204, 418-422; BE `MeetingHistoryService.php:249-392`).
  - Ghi chú / lý do (icon bình luận) — ghép từ note + meta.reason (SLS:2000-2014).

### 5.3 Hành động được ghi (BE `Modules/Assign/Entities/QuotationHistory.php:19-80`; nhóm lọc theo SLS:79-108)
| action | Nhãn hiển thị | Nhóm lọc | Ghi khi |
|---|---|---|---|
| create | Tạo mới | Tạo mới | tạo báo giá (QuotationService.php:252, 436-438, 1613, 1771) |
| update (và save_draft cũ) | Thay đổi thông tin | Thay đổi thông tin | mỗi lần Lưu có thay đổi nội dung (QuotationService.php:2088) — không đổi gì thì không ghi |
| submit | Gửi duyệt | Thay đổi trạng thái | (QuotationService.php:3915, meta cấp duyệt) |
| self_approve | Tự duyệt | Thay đổi trạng thái | :3949 |
| tp_approve | TP duyệt | Thay đổi trạng thái | :3998 |
| tp_approve_forward | TP duyệt & chuyển BGĐ | Thay đổi trạng thái | :3980 |
| bgd_approve | BGĐ duyệt | Thay đổi trạng thái | :4034 |
| reject | Từ chối | Thay đổi trạng thái | :4100 (ghi chú = lý do) |
| finalize | Chốt | Thay đổi trạng thái | :4150 |
| unfinalize | Hủy chốt | Thay đổi trạng thái | :4192 (ghi chú = lý do) |
| update_sales_note | Cập nhật ghi chú KD | Thay đổi thông tin | :4308 |
| update_vat_bulk | Áp dụng VAT đồng loạt | Thay đổi thông tin | :4261 (VAT áp dụng / Phạm vi áp dụng / Số dòng áp dụng với log cũ) |
| closed_by_project | Đóng theo dự án | Thay đổi trạng thái | đóng dự án TKT (ProspectiveProjectService.php:2120) / dự án cha đóng (SummaryQuotationService.php:999) |
| expired | Hết hiệu lực | Thay đổi trạng thái | báo giá tổng hợp (SummaryQuotationService.php:934, 1029) |
| import_prices, update_discount | Import giá / Cập nhật giảm giá | Thay đổi thông tin | khai báo nhãn nhưng **không còn nơi nào ghi** (Import không ghi lịch sử riêng — chỉ khi Lưu ra dòng "Thay đổi thông tin") |

Các dòng chuyển trạng thái tự thêm thay đổi **"Trạng thái: {cũ} → {mới}"** (SLS:429-440).

### 5.4 Trường được theo dõi trong "Thay đổi thông tin" (QHS:70-125, 260-360)
- Thông tin chung: **Tên báo giá · Dự án** ("mã - tên") · **Khách hàng** ("mã - tên") · **Mã số thuế · Email khách hàng · Địa chỉ · Người liên hệ · SĐT liên hệ · Mô tả · Hạn báo giá** (dd/mm/yyyy) · **Giao hàng (ngày) · Bảo hành (tháng) · Điều khoản báo giá · Ghi chú nội bộ · Ghi chú kinh doanh · BOM tổng hợp · Loại tiền tệ · Bảng giá · Giai đoạn dự án · Giảm giá** ("Không giảm giá"/"Giảm giá theo mặt hàng"/"Giảm giá theo tổng") · **Làm tròn** ("Hàng nghìn (-3)"… "2 số lẻ (2)", trống = "Mặc định (tối đa 2 số lẻ)").
- Vận chuyển: **Giá nhập vận chuyển · Chi phí vận chuyển · Giảm giá vận chuyển · Phân bổ GG vận chuyển · VAT vận chuyển (%)**.
- Bảng con (thêm/xoá/sửa từng dòng):
  - **Nhóm hàng hoá**: Tên nhóm · Thuộc nhóm.
  - **Hàng hoá**: Tên hàng · Mã · Nhóm · Thuộc hàng cha · Model · Thương hiệu · Xuất xứ · Thông số kỹ thuật · Ghi chú · SL · ĐVT · Giá nhập · Giá bán · GG (%) · GG (đ) · Phân bổ GG · VAT (%).
  - **Dịch vụ & Chi phí khác**: Tên · Mã · Nhóm · Ghi chú · SL · ĐVT · Giá nhập · Giá bán · GG (%) · GG (đ) · Phân bổ GG · VAT (%).
  - **Giảm giá tổng đơn hàng**: Loại giảm giá · Kiểu ("Phần trăm"/"Số tiền") · Giá trị ("x%" hoặc số tiền).
- **Không** theo dõi: trạng thái (có dòng riêng), Hiệu lực báo giá (tự tính lại theo ngày), tổng tiền/thành tiền (QHS:34-39).
- Số hiển thị chuẩn quốc tế, bỏ số 0 thừa; ô giảm giá = 0 coi như trống (QHS:532-545).
- **Giá vốn**: người xem không có quyền **"Xem giá vốn hàng hoá"** → bị bỏ "Giá nhập", "Giá nhập vận chuyển" khỏi lịch sử (QHS:42, 199-224; SLS:415-416, 445-448, 563-565).
- Báo giá tổng hợp theo dõi thêm "Báo giá nguồn", "Section" (QHS:96-98, 228-256) — ngoài phạm vi màn này.

---

## 6. Ghi chú lệch / rủi ro phát hiện khi đọc (để QA/BA biết, KHÔNG đưa nguyên văn vào SRS nếu không cần)
1. Letterhead bản in lấy theo công ty người đăng nhập, không theo công ty trên báo giá (IDX:1067-1077).
2. Xác nhận Xoá/Duyệt dùng `$bvModal.msgBoxConfirm` (không phải popup xác nhận dùng chung) — chữ nút "Huỷ".
3. Nút Duyệt FE không kiểm phòng ban (BE kiểm).
4. Ô sửa "Ghi chú Kinh doanh" không hiện cho báo giá không gắn dự án dù BE cho người lập sửa.
5. Lỗi 422 không phải lỗi dữ liệu (vd trạng thái ≠ Đang tạo) ở Validate/Import có thể hiện chuỗi kỹ thuật của axios thay vì câu BE (QIM:790-793, 1270-1273).
6. File mẫu đánh `*` cho ĐVT nhưng BE không bắt buộc ĐVT hàng tạm; file mẫu ghi "Loại (*)" — BE bắt buộc qua kiểm "Loại hạng mục … không tồn tại".
7. Ảnh/bảo hành (export, chi tiết) vẫn đọc qua connection `mysql2` (QEX:783; DetailQuotationResource.php:176) — trái ràng buộc gop_db.
8. Hành động "Import giá", "Cập nhật giảm giá" có nhãn nhưng không còn được ghi.
