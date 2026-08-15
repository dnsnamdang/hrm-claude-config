# Tài liệu màn Danh mục khách hàng (`/assign/customers`) — SRS + HDSD + Test case

> Nhánh: `gop_db` · **Tài liệu do @junfoke lập** (code màn này do @khoipv phát triển — user chốt
> 2026-08-15: "cứ làm nhé, tôi sẽ phụ trách làm tài liệu phần này")
> Phạm vi user chốt: **toàn bộ 10 chức năng**, gồm cả màn Quản lý KH, Import Excel, Xuất file.

## Vì sao có thư mục riêng

Màn này không có thư mục feature "nhà" — nó trải trên **9 thư mục** đợt sửa rời rạc:
`customer-column-config`, `customer-export-file`, `customer-form-group`, `customer-history`,
`customer-import-excel`, `customer-lock`, `customer-date-no-future`,
`customer-list-empty-placeholder`, `customer-cut-mysql2`.
Tài liệu phải gộp tất cả nên đặt ở thư mục tổng hợp này.

## Quy mô (đã khảo sát 2026-08-15)

| | Số liệu |
|---|---|
| FE | ~7.700 dòng — `CustomerForm.vue` 3.410, `index.vue` 1.863, `EquipmentTab` 1.174 |
| BE | ~7.700 dòng — `CustomerService` 2.398, `CustomerManagerService` 1.481, `CustomerImportService` 1.151, `CustomerController` 916, `CustomerHistoryService` 782 |
| Dữ liệu thật (local) | 3.451 khách hàng |
| Cột danh sách | 20 (tuỳ chỉnh ẩn/hiện + kéo thả; STT và Mã KH bị khoá luôn hiện) |
| Tiêu chí lọc | 19 hiển thị / 15 nhóm cấu hình được |

## 10 chức năng đưa vào tài liệu

1. Truy cập + xem danh sách · 2. Tìm kiếm & bộ lọc nâng cao · 3. **Cài đặt bộ lọc** (mới) ·
4. Tuỳ chỉnh cột · 5. Tạo mới · 6. Sửa · 7. Xem chi tiết · 8. Khóa / Mở khóa ·
9. Lịch sử thay đổi · 10. Import Excel · 11. Xuất CSV / Excel / **PDF**
(Màn Quản lý KH gồm 5 tab: Thông tin chung, Báo giá, Hợp đồng, Danh sách trang thiết bị, Thông tin khác.)

⚠️ **Lệch so với design cũ** — tài liệu bám CODE HIỆN TẠI:
- `customer-export-file/design.md` ghi "Không port Xuất PDF", nhưng thực tế **đã có nút Xuất PDF**
  và route `export-pdf`.
- **"Cài đặt bộ lọc"** (chọn + kéo thả 15 trường lọc, lưu theo từng màn) là chức năng mới,
  KHÔNG có trong 9 design.md nào.

## Điểm nghiệp vụ cốt lõi đã xác minh trong code

- **Màn danh sách không gắn quyền xem** — ai cũng vào được; phạm vi dữ liệu do
  `CustomerService::applyErpVisibilityScope` lọc theo 4 cấp: *Xem tất cả khách hàng* → *của công ty*
  → *của phòng ban* → *của bộ phận*; không có cấp nào thì chỉ thấy KH **do chính mình tạo**.
- Chồng thêm lớp `applyB2cOwnershipVisibility` cho **khách cá nhân**: chỉ hiện khi mình tạo / mình
  đăng ký còn hạn / đã phát sinh báo giá - meeting - dự án TKT, hoặc **tìm khớp đúng full SĐT**.
- Quyền dùng là **quyền ERP** (`erpPermission:`): Thêm / Sửa / Xóa / Xuất dữ liệu khách hàng —
  KHÔNG phải quyền HRM trong seeder.
- Validate rẽ theo loại KH: cá nhân bắt buộc ≥1 SĐT `^(0)[0-9]{9,11}$`; tổ chức bắt buộc người đại
  diện, người liên hệ, địa chỉ xuất hoá đơn và MST — **MST thành không bắt buộc nếu đã chọn công ty mẹ**.
  Email / MST / CCCD unique. Lĩnh vực phải thuộc đúng loại hình đã chọn.
- Import: tối đa `CustomerImportService::MAX_ROWS` dòng/lần, có bước kiểm tra trước khi ghi;
  kết quả 200 (vào hết) / 207 (vào một phần) / 400 (trượt hết). File mẫu 3 sheet sinh từ danh mục thật,
  header dòng 1, dữ liệu từ dòng 3, dòng con bỏ trống Tên KH để thêm liên hệ cho KH dòng trên.
- Form 5 khối: Thông tin khách hàng (luôn) · Thông tin cá nhân (loại = Cá nhân) · Thông tin tổ chức
  (loại 2-5) · **Địa chỉ giao hàng (chỉ khi Sửa)** · Người liên hệ (loại 2-5).

## Tiến độ

- [x] Khảo sát phạm vi, đối chiếu 9 đợt sửa, chốt owner + phạm vi với user
- [x] Đọc BE: route (60+ endpoint), `CustomerController`, rule validate 2 FormRequest, scope phân quyền
- [x] Đọc FE: 20 cột, 19 tiêu chí lọc, 5 khối form, menu hành động
- [x] Cập nhật rule ảnh SRS (skill + CLAUDE.md) — mục Layout mỗi chức năng nay CÓ ảnh chụp thật
- [x] Ảnh: **17** trong `kh_shots/` — danh sách, bộ lọc nâng cao, cài đặt bộ lọc, tuỳ chỉnh cột,
      menu hành động, lịch sử, form tạo mới (rỗng / Cá nhân / Tổ chức), lỗi validate, Import Excel,
      Chọn trường xuất, chi tiết, Quản lý KH, thẻ trang thiết bị, form Sửa, hộp xác nhận Khóa
- [x] `testcase.xlsx` — **235 TC**, P0 60%, 21 TC phân quyền + 10 section La Mã
- [x] `SRS - Danh mục khách hàng.docx` — 12 chức năng FR-01…FR-12, 12 quy tắc BR-01…BR-12,
      42 bảng, 23 ảnh (13 use case vẽ thật + 10 ảnh chụp thật ở mục Layout)
- [x] `HDSD_Danh muc khach hang.docx` — 38 trang, 10 phần, 15 bảng, 16 ảnh thật;
      mục lục + danh mục hình ảnh đã cho Word cập nhật thật

## Lệch giữa giả định ban đầu và code thật (phát hiện khi chụp ảnh — đã sửa vào cả 3 tài liệu)

| Giả định sai | Thực tế trong code |
|---|---|
| 5 loại: Cá nhân, Công ty TNHH, Công ty CP, DNTN, Tổ chức khác | **Cá nhân, Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước** |
| Nhãn ô chọn loại là "Đối tượng" | Nhãn trên form là **"Loại hình tổ chức"** |
| Màn Quản lý KH có 5 thẻ | **6 thẻ** — có thêm "Thông tin liên hệ" |
| Khóa nằm trong menu ba chấm | Khóa là **biểu tượng ổ khóa riêng** trên cột Hành động; menu ba chấm chỉ có Quản lý + Lịch sử |
| Import có nút "Kiểm tra dữ liệu" / "Nhập dữ liệu" | Ba nút thật: **Load lên bảng → Validate → Import** |
| Cửa sổ xuất file tick chọn cột | Cửa sổ **"Chọn trường xuất Excel"**, 20 trường, **thứ tự cột chạy theo thứ tự chọn** (không kéo thả) |

## File sinh tài liệu (chạy lại được bất cứ lúc nào)

```
python .plans/gop-db/customer-docs/gen_testcase.py    # + tc_sections_a/b/c.py
python .plans/gop-db/customer-docs/gen_srs.py         # + srs_chuong5.py, srs_chuong5b.py
python .plans/gop-db/customer-docs/gen_hdsd.py        # + hdsd_noidung.py
```

⚠️ `srs_docx_lib.layout()` trong skill được bổ sung 3 tham số `route` / `shot` / `shot_caption`
để chèn ảnh chụp thật vào mục Layout (rule SRS 2026-08-13). Tương thích ngược, các generator cũ
không truyền thì hành xử y như trước.

### Ghi chú kỹ thuật khi chụp tiếp

- Form dùng **select2**: set `value` + `dispatchEvent('change')` KHÔNG cập nhật Vue. Phải click ô
  select2 rồi click đúng `li.select2-results__option`, hoặc gõ từ khoá + Enter.
- **Không chạy `browser_snapshot` toàn trang ở màn form** — dropdown "Nhóm khách hàng" và "Hãng xe"
  có hàng trăm option, snapshot phình rất to. Dùng `browser_evaluate` trả về đúng thứ cần kiểm.
- Trang load chậm: sau `navigate` phải chờ (kiểm `document.querySelectorAll('input').length` hoặc
  chờ chữ đặc trưng) rồi mới chụp, nếu không ảnh ra spinner.
