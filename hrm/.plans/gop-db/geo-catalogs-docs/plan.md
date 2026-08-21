# Tài liệu 10 màn danh mục — SRS + HDSD + TC

> Nhánh `gop_db` · **@junfoke phụ trách tài liệu** · user chốt 2026-08-17
> Phạm vi: **10 màn, mỗi màn 1 SRS + 1 HDSD + 1 TC = 30 file**.
> Thứ tự user chốt: **Địa lý (6 màn) → Tài chính (3 màn) → Công việc-lỗi thiết bị (1 màn)**.

## Ba nhóm theo khuôn code

| Nhóm | Màn | Đường dẫn | Quyền |
|---|---|---|---|
| Địa lý | Quốc gia | `/human/nations` | **KHÔNG có** |
| | Khu vực | `/human/areas` | **KHÔNG có** |
| | Tỉnh/TP | `/human/provinces` | **KHÔNG có** |
| | Quận/Huyện | `/human/districts` | **KHÔNG có** |
| | Phường/Xã | `/human/wards` | **KHÔNG có** |
| | Đường/Phố | `/human/hamlets` | **KHÔNG có** |
| Tài chính | Vụ việc | `/finance/works` | Quản lý danh mục vụ việc |
| | Mã phí | `/finance/cost-debts` | Quản lý danh mục mã phí |
| | Nguồn vốn | `/finance/source-capitals` | Quản lý danh mục nguồn vốn |
| CSKH | Công việc, lỗi thiết bị | `/customer-care/device-errors` | Quản lý danh mục công việc - lỗi thiết bị |

## ⚠️ Phát hiện phải nêu trong tài liệu

**6 màn địa lý không gắn quyền ở bất kỳ endpoint nào** — kể cả Thêm / Sửa / Xóa / Khóa. Ai đăng
nhập cũng sửa được danh mục địa lý dùng chung toàn hệ thống. FE cố ý KHÔNG tạo cờ quyền giả
(`canManage = true` bị CLAUDE.md cấm), nên nút luôn hiện với mọi người.
Đã ghi chú sẵn trong `pages/human/nations/index.vue` dòng 36-38.

## Nhóm Địa lý — khác biệt giữa 6 màn (đã đọc code 17/08/2026)

| | Quốc gia | Khu vực | Tỉnh/TP | Quận/Huyện | Phường/Xã | Đường/Phố |
|---|---|---|---|---|---|---|
| Cột Trạng thái | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Khóa / Mở khóa | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Trường bắt buộc | Tên, Mã | Tên, Quốc gia | Tên, Biển số xe, Quốc gia, Khu vực | Tên, Tỉnh/TP | Tên, Mã, Tỉnh/TP | Tên, Quốc gia, Tỉnh/TP, Phường/Xã (+ Quận/Huyện nếu KHÔNG phải Việt Nam) |
| Trường tuỳ chọn | Mã bưu chính | — | Mã Tỉnh/TP | — | — | — |
| Điều kiện trùng tên | toàn hệ thống | toàn hệ thống | trong cùng Quốc gia + Khu vực | trong cùng Tỉnh/TP | trong cùng Tỉnh/TP | trong cùng Phường/Xã |

**Quy tắc riêng Đường/Phố**: chọn Quốc gia = Việt Nam thì ô Quận/Huyện **bị ẩn**; quốc gia khác
thì hiện và bắt buộc.

**Hai màn Quận/Huyện + Đường/Phố** chỉ hiện bản ghi còn hoạt động (lọc cứng ở tầng máy chủ) nên
không có cột Trạng thái — "xóa" thực chất là khóa mềm.

**Bản ghi đã Khóa thì ẩn hẳn Sửa và Xóa**, chỉ còn Mở khóa + Lịch sử (đã kiểm chứng trên màn Quốc gia).

**Cột Hành động**: Sửa + Xóa hiện thẳng; Khóa/Mở khóa và Lịch sử nằm trong nút ba chấm
"Hành động khác".

**Cửa sổ thêm mới có 3 nút**: Lưu · **Lưu và tiếp tục** · Đóng.

**Bộ lọc mặc định KHÔNG lọc trạng thái** — vào màn thấy cả bản ghi Hoạt động lẫn Khóa (trước đây
để mặc định `Hoạt động` nên giấu mất bản ghi đã khóa, đã sửa).

## Thông báo lỗi lấy nguyên văn từ code

| Màn | Thông báo |
|---|---|
| Chung | `Bắt buộc phải nhập` |
| Quốc gia | `Mã quốc gia này đã tồn tại` · `Tên quốc gia này đã tồn tại` · `Phải là số` · `Chỉ được nhập chữ số, từ :min đến :max chữ số` |
| Khu vực | `Tên khu vực này đã tồn tại` |
| Tỉnh/TP | `Tên khu vực này đã tồn tại` (⚠️ thông báo ghi nhầm "khu vực" cho màn Tỉnh/TP) · `Mã tỉnh này đã tồn tại` · `Biển số tỉnh này đã tồn tại` |
| Quận/Huyện | `Tên quận/huyện này đã tồn tại trong tỉnh/TP` |
| Phường/Xã | `Tên phường/xã này đã tồn tại` |
| Đường/Phố | `Tên đường/phố này đã tồn tại trong phường/xã` |

⚠️ **Lỗi nhỏ đáng báo dev**: `CreateProvinceRequest` dùng thông báo `Tên khu vực này đã tồn tại`
cho ô Tên Tỉnh/TP — copy nhầm từ màn Khu vực.

⚠️ **Lỗi thứ 2 — lịch sử màn Khu vực hiện tên trường thô `nation_name`** (chụp được trên dev,
ảnh `areas_03_lichsu.png`). Người dùng thấy dòng `nation_name: China → Italy` thay vì
`Quốc gia: China → Italy`.
Nguyên nhân: `AreaService::historyColumns()` ghi lịch sử bằng khóa `nation_name`
(dòng 21 + 100 + 112) nhưng bảng nhãn `CatalogHistoryService` chỉ khai `nation_id => 'Quốc gia'`
(dòng 115) → tra nhãn trượt, rơi về hiển thị tên khóa.
Sửa: thêm `'nation_name' => 'Quốc gia'` vào cấu hình `areas`, hoặc đổi `AreaService` ghi theo
`nation_id`.

⚠️ **Lỗi thứ 3 — lịch sử Quận/Huyện và Đường/Phố hiện SỐ ĐỊNH DANH thay vì tên.**
Chụp được trên dev (`districts_04_lichsu.png`, `hamlets_05_lichsu.png`):

- Quận/Huyện: `Tỉnh/TP: 1 → 2`
- Đường/Phố: `Phường/xã: 13322 → 13400`

Nhãn trái đã đúng, nhưng giá trị hai vế là số định danh nội bộ — người dùng không hiểu được đã
đổi từ tỉnh nào sang tỉnh nào. Cần đổi giá trị hiển thị sang TÊN của bản ghi tham chiếu.

**Tóm lại nhóm địa lý có 2 kiểu lỗi lịch sử ngược nhau**: Khu vực ghi tên nhưng thiếu nhãn
(`nation_name`), còn Quận/Huyện + Đường/Phố có nhãn nhưng ghi số định danh. Nên gom sửa một lượt.
Chưa kiểm được `wards` (bản ghi thử chưa có lịch sử) — cần kiểm khi có dữ liệu.

## Tiến độ

- [x] Khảo sát 10 màn: route, quyền, cột, bộ lọc, trường nhập, rule validate
- [x] Ảnh nhóm Địa lý: **20** trong `geo_shots/` — chụp trên **cổng dev `hrm-crm.eteksofts.com`**
      (user chốt 2026-08-17: local nạp ~25 giây/màn, dev ~6 giây và đã đăng nhập sẵn).
      Gồm: 6 màn danh sách · 6 cửa sổ thêm mới · lỗi validate · menu ba chấm · xác nhận Khóa ·
      xác nhận Xóa · Lịch sử có dữ liệu (Quốc gia, Khu vực) · Lịch sử rỗng (Tỉnh/TP) ·
      Đường/Phố khi chọn quốc gia khác Việt Nam (hiện thêm ô Quận/Huyện)
- [x] **6 × `SRS - <Tên màn>.docx`** — theo FORM MỚI user chốt 2026-08-17 (4 phần:
      Giới thiệu / Phân quyền / Đặc tả chi tiết / Quy tắc nghiệp vụ). Sinh từ
      `gen_srs.py` + `srs_geo_config.py`.

      | Màn | Bảng | Ảnh | Chức năng |
      |---|---|---|---|
      | Quốc gia | 24 | 11 | 7 |
      | Khu vực | 24 | 10 | 7 |
      | Tỉnh/TP | 24 | 10 | 7 |
      | Quận/Huyện | 21 | 8 | 6 |
      | Phường/Xã | 24 | 10 | 7 |
      | Đường/Phố | 21 | 9 | 6 |

      ⚠️ Bẫy khi đặt tên file: tên màn chứa dấu `/` (Tỉnh/TP, Quận/Huyện, Phường/Xã, Đường/Phố)
      → phải `ten.replace('/', '-')` TRƯỚC khi ghép đường dẫn, nếu không dấu `/` bị hiểu là
      phân cách thư mục và file rơi vào thư mục con (`SRS - Danh mục Tỉnh/TP.docx` tạo ra thư mục
      `SRS - Danh mục Tỉnh` chứa file `TP.docx`).
- [x] **6 × `testcase - <Tên màn>.xlsx`** — tổng **327 TC**, P0 74-78%.
      Quốc gia 56 · Khu vực 56 · Tỉnh/TP 60 · Quận/Huyện 46 · Phường/Xã 58 · Đường/Phố 51.
      Không có section phân quyền vì màn chưa gắn quyền; thay bằng TC kiểm chứng
      "mọi tài khoản đều thao tác được" để QA ghi nhận đúng hiện trạng.
- [x] **6 × `HDSD_<Tên màn>.docx`** — 12-15 trang mỗi file, 8 bảng, 5-8 ảnh.
      Mục lục và danh mục hình ảnh đã cho Word cập nhật thật.

⚠️ **Đã sửa thư viện SRS dùng chung** (`srs_docx_lib.save()`): trước đây chỉ chèn trường mục lục
nên người đọc phải tự bấm "Update Field"; nay gọi Word cập nhật thật rồi lưu lại, giống
`hdsd_engine`. Máy không có Word thì chỉ cảnh báo, không làm gãy generator.
- [ ] Nhóm Tài chính (3 màn) — chưa bắt đầu
- [ ] Màn Công việc, lỗi thiết bị — chưa bắt đầu

## ⚠️ Vướng — cần xử lý trước khi làm tiếp

**Không chụp được cửa sổ Lịch sử thay đổi**: bảng lưu lịch sử danh mục chưa có trên máy local.
Migration `2026_08_16_000001_create_catalog_histories_table` đã có trong repo nhưng **chưa chạy**
(cùng 2 migration bổ sung dữ liệu người tạo cho danh mục tài chính). Mở Lịch sử hiện
"Không tải được lịch sử phiếu".

Lịch sử thay đổi là một chức năng của **cả 6 màn địa lý và 3 màn tài chính** nên phải có ảnh.
Hai cách: chạy `php artisan migrate` trên local, hoặc chụp trên cổng dev.

**Ngoài lề**: local đang lỗi biên dịch `Module not found: Can't resolve 'jspdf-autotable'`
(dùng cho Xuất PDF màn Khách hàng) — chưa cài gói. Lỗi này che nút bấm khi thao tác bằng công cụ
tự động, không ảnh hưởng người dùng thật.

## Ghi chú kỹ thuật khi chụp tiếp

- Trang local nạp rất chậm (~20-25 giây). Sau `navigate` phải chờ tới khi `tbody tr` ≥ 1 rồi mới chụp.
- Lớp phủ báo lỗi biên dịch của trình đóng gói chặn mọi cú click → gỡ bằng
  `document.getElementById('webpack-hot-middleware-clientOverlay').remove()` trước khi thao tác.
- Nút Khóa / Lịch sử nằm trong nút ba chấm: mở ba chấm rồi click phần tử `.v2-row-actions__item`
  đang hiển thị (lọc `offsetParent !== null`, vì mọi dòng đều render sẵn menu ẩn).
