# Plan — Danh mục khu vực kinh doanh (#11623)

> @junfoke · design: `design.md`

## Phase 1 — BE (hrm-api)

- [x] Migration `business_areas` + `business_area_wards` (UNIQUE ward_id) — chưa chạy migrate (chờ user)
- [x] Entity `BusinessArea` (extends BaseModel), phường/xã qua belongsToMany bảng nối
- [x] Service: list (lọc/sort/phân trang), detail, store/update (sync phường/xã, chặn phường/xã đã thuộc khu vực khác), delete, lock/unlock, lịch sử (`catalog_histories`)
- [x] Endpoint phường/xã theo tỉnh kèm khu vực đang giữ
- [x] Request validate (tên unique trong tỉnh), middleware chặn sửa/xoá khi khoá (423)
- [x] Export (DynamicExport + ExportColumnRegistry) + Import (validate/import)
- [x] Đăng ký `business_areas` vào `CatalogHistoryService::TABLES`
- [x] Routes `/human/business-areas`

## Phase 2 — FE (hrm-client)

- [x] Menu Danh mục › Địa lý › Khu vực kinh doanh
- [x] `pages/human/business-areas/index.vue` (copy pattern `pages/human/wards/index.vue`)
- [x] `pages/human/business-areas/components/BusinessAreaModal.vue` (Tạo/Sửa/Xem + bảng tick phường/xã + chip lọc)
- [x] Import modal + file mẫu `buildImportTemplate`
- [x] Kiểm Playwright (danh sách, Sửa, chip, xác nhận đổi tỉnh, Xem→Sửa, dòng khoá ẩn Sửa/Xóa)

## Phase 3 — Bàn giao

- [x] Chạy migrate (user cho phép 10/10) + test API toàn luồng (tạo/trùng tên/phường đã gán/sai tỉnh/sửa/khoá 423/lịch sử/sort/lọc/xuất/import/xoá)

### Checkpoint — 2026-10-10
Vừa hoàn thành: code BE + FE xong (chưa chạy được vì MySQL/API/client local đang tắt). Đã fast-forward `gop_db` local lên `origin/develop` ở cả 2 repo theo yêu cầu user (chưa push).
Đang làm dở: kiểm thử — cần bật MySQL + chạy migration `2026_10_10_000001_create_business_areas_tables` (chờ user cho phép).
Bước tiếp theo: migrate → bật API :8000 + client :3000 → Playwright kiểm toàn luồng (tạo/sửa/xem/khoá/xoá/lịch sử/xuất/import).
Blocked: quyền chạy migrate.

### Checkpoint — 2026-10-10 (2)
Vừa hoàn thành: migrate + kiểm API & UI. Sửa 3 lỗi phát hiện khi test: sort Người tạo/cập nhật (employee_infos không có employee_id sau gộp DB), checkbox "chọn tất cả" tự bỏ tick khi đổi chip, Xem→Sửa bị reset về Tạo.
Đang làm dở: không.
Bước tiếp theo: user duyệt → commit 2 repo (chưa commit). Dữ liệu test local: 3 khu vực (Cầu Giấy, Hoàn Kiếm[Khóa], Hoàn Kiếm mới).
Blocked:

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Hỗ trợ check "Khu vực kinh doanh cần quyền gì": màn chưa gắn quyền nào (menu `master-data.js`, trang `business-areas/index.vue`, route API không `checkPermission`) — đúng chốt 10/10 cho cả nhóm danh mục Địa lý; ai đăng nhập cũng thêm/sửa/xoá/khoá/nhập Excel được, chỉ chặn sửa/xoá bản ghi đã khoá. Không sửa code.

## Ngày 11/11/2026 (@junfoke)
- [x] 11/11/2026 — Lỗi #12111 (DM khu vực kinh doanh): khối "Phường/Xã thuộc khu vực" có icon tròn, số "N phường/xã" màu teal, đầu bảng xanh (áp cả Xem / Tạo / Sửa); popup Xem bỏ dòng chú thích dưới tiêu đề, nút Sửa đổi màu teal, có đủ hành động như cột Hành động (Sửa · Xoá · Khoá/Mở khoá · Đóng), thao tác xong đóng popup. Client `16625f555` (develop, đã push). Chờ user: con nháy chuột ở ô khoá (không tái hiện — trên dev chỉ hiện biểu tượng "cấm", nên hỏi lại QA); màu chữ đầu bảng đang đen đậm theo chuẩn bảng mới (muốn teal như ảnh QA thì đổi 1 dòng).
- [x] 11/11/2026 — Lỗi #12116 (Import Excel KVKD): cột Tỉnh/TP trong file mẫu đổi thành ô gõ chữ, bỏ danh sách sổ xuống (file mẫu nhẹ, mở không đơ), không phân biệt hoa/thường, gõ sai báo "Không tìm thấy Tỉnh/TP: …"; thêm cột Trạng thái (Hoạt động / Khóa, bỏ trống = Hoạt động, giá trị lạ báo lỗi ở dòng đó như import Phường/Xã).
- [x] 11/11/2026 — Lỗi #12113 (Sửa KVKD): (1) đổi Quốc gia / Vùng / Tỉnh-TP: trong lúc popup xác nhận mở ô vẫn giữ giá trị cũ, bấm Đồng ý mới đổi, Hủy thì giữ nguyên giá trị + phường/xã đã tick; (2) ô "Tìm phường/xã" có chữ thì hiện dấu x xoá nhanh; (4) tổng số lệch do phường/xã đang thuộc khu vực khác (dòng xám) ⇒ thêm chip thứ 4 "Khu vực khác (n)" để Tất cả = Đã chọn + Chưa gán + Khu vực khác (dựng đúng ca QA 75 = 1 + 73 + 1). Commit #12113 + #12116: client `a9dc4afc1`, api `eb72258c7` (develop, đã push). User hỏi lại mục 4 (ảnh 1 + 73 = 74) ⇒ giải thích ảnh QA là bản trước khi sửa (3 chip), chờ user xác nhận bản dev mới.
- [x] 11/11/2026 — #12113 mục 3 (user chốt đổi đồng bộ): Khóa / Mở khóa ở Lịch sử thay đổi hiện tiêu đề "Thay đổi trạng thái" màu cam cho MỌI màn (đổi bộ nhãn lịch sử dùng chung `CatalogHistoryService` — các danh mục, Tài khoản, Cài đặt; trước Mở khóa màu xanh), dòng "Trạng thái: Hoạt động → Khóa" giữ nguyên; bỏ cấu hình riêng đã thêm cho KVKD; test tài khoản `AdminAccountApiTest` sửa theo nhãn mới (12/12). Lịch sử Khách hàng chưa đổi (lưu lịch sử kiểu riêng). Api `d0d2a261e` (develop, đã push).

## Ngày 13/11/2026 (@junfoke)
- [x] 13/11/2026 — Xử lý gắn quyền cho màn Danh mục khu vực kinh doanh (trước đây mở cho mọi người theo chốt 10/10 nhóm Địa lý): thêm 2 mã `master_data.khu_vuc_kinh_doanh.view` (xem, popup Xem, xuất Excel) và `.manage` (Tạo/Sửa/Xoá/Khoá/Mở khoá/Import) ở Catalog `master_data.php`; route API `Human/Routes/api.php` gắn `checkPermission` (không quyền ⇒ 403); FE menu `master-data.js` chỉ hiện khi có 1 trong 2 mã, gõ URL không quyền ⇒ 404; người chỉ có Xem không thấy nút thao tác ở danh sách + popup Xem (`business-areas/index.vue`, `BusinessAreaModal.vue`). Khuôn màn Xuất xứ. Api `de66565a7`, client `2157a4e6d` (gop_db, đã push). Deploy: `build_tpe.sh` (tự sync quyền) rồi cấp 2 mã ở `/admin/roles` — chưa cấp thì không ai vào được, kể cả Super Admin. Chưa chạy thử trên app. 5 màn Địa lý còn lại vẫn chưa có quyền.
- [x] 13/11/2026 — Xử lý lỗi import khu vực kinh doanh (file `Mau_import_khu_vuc_kinh_doanh_chuan_ten_theo_danh_muc.xlsx`, 15 dòng lỗi "Không tìm thấy"): không phải do gộp DB mà do 33 phường/xã lưu tên kiểu Unicode tổ hợp (10 xã Lào Cai, 13 phường TP.HCM, 9 xã Vĩnh Long, Xã Nậm Nèn) ⇒ `BusinessAreaService` chuẩn hoá cả 2 phía trước khi so (dùng lại `CompanyMigrationService::normalizeNaturalKey()`: NFC + bỏ khoảng trắng thừa + chữ thường). Xã lặp trong cùng ô giờ báo "… bị nhập lặp trong cùng dòng" thay cho "đã được gán ở dòng N" (trỏ nhầm dòng). Đã lên gop_db (api `e65188bb0`, `43b618695`).
- [x] 13/11/2026 — Hỗ trợ check phường/xã trùng: 355 cặp trùng tên + mã cùng tỉnh, do ERP nhập 2 lần ngày 23/07/2025 (bản 17:25 đã khoá, không ai dùng) ⇒ không gây lỗi import. Xã trùng tên khác tỉnh là bình thường, code tra theo tỉnh + tên.
- [x] 13/11/2026 — Xử lý đối chiếu danh mục phường/xã với QĐ 19/2025/QĐ-TTg (3.321 đơn vị): DB thiếu 9 xã (Xã Văn Lang Thái Nguyên bị khoá nhầm + 8 xã chưa có: Cẩm Giang, Sơn Hà, Ba Tơ, Ia Mơ, Lộc Thạnh, Thanh An, Tân Thạnh Tây Ninh, Tân Thạnh Đồng Tháp). Viết SQL (sao lưu `wards_bk_20261113`), thử local trong transaction rồi huỷ; user chạy prod OK, prod đủ 3.321 mã. Bảng sao lưu còn trên prod, xoá sau khi import ổn.
- [x] 13/11/2026 — Xử lý sửa file Excel cho người dùng gửi lại (`…_da_sua.xlsx`, giữ file gốc): STT 15 Hải Phòng-3 đổi 1 "Xã Cẩm Giàng" lặp thành "Xã Cẩm Giang"; STT 63 Quảng Ngãi-2 đổi 1 "Xã Sơn Hạ" thành "Xã Sơn Hà"; STT 69 Gia Lai-2 "Ia Mơ" → "Xã Ia Mơ". Validate bằng code gop_db trên local đã thêm 9 xã: 103/103 dòng hợp lệ.
