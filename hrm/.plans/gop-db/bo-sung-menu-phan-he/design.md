# Bổ sung menu đầy đủ cho các phân hệ

**Người phụ trách:** @junfoke — 2026-08-01

## Mục tiêu

Sau giai đoạn 1 của `tach-phan-he-erp-hrm`, 25 phân hệ đã có khung nhưng chỉ những màn **HRM
đã có** mới xuất hiện trong menu. Các màn còn nằm bên ERP và các chức năng theo sơ đồ nhưng
chưa xây dựng thì không nằm ở đâu — mở phân hệ mới chỉ thấy mục "Tổng quan" trống.

Feature này khai báo **toàn bộ mục menu còn thiếu** theo sheet `Gộp phân hệ ERP-HRM`, kể cả
mục chưa có màn, để mỗi phân hệ phản ánh đúng quy hoạch.

## Scope

- **355 mục menu mới** trên 14 phân hệ: master-data (7), admin (15), tax (5), recruitment (6),
  kpi (5), legal (9), asset (4), iso (6), operation (2), assign (18), production (7),
  sale (153), customer-care (17), finance (101).
- **10 mục link thật sang ERP** (mở tab mới), 345 mục còn lại hiển thị **xám mờ**.
- **Ẩn 3 phân hệ** Mua hàng / Kho / Vận chuyển khỏi màn chọn phân hệ, dropdown chuyển phân hệ
  và màn Phân quyền.
- **Tái phân bổ 14 màn** bị khuất do việc ẩn trên: 4 màn Kiểm kê → Tài chính (kèm link ERP),
  10 phiếu Khởi tạo yêu cầu → Bán hàng.
- **Bổ sung 5 màn** có trong `erp-menu-inventory` nhưng thiếu khỏi sheet gộp (4 màn báo giá
  gắn hậu tố `(ERP)` + Kết chuyển chi phí phải trả).
- **Cập nhật lại chính sheet gộp** cho khớp menu (đã sao lưu bản gốc).
- Sửa `Sidebar.vue` để render được 3 kiểu menu item.

**Không làm:** menu của 3 phân hệ bị ẩn (214 mục), phân hệ "Danh mục hàng hóa - dịch vụ",
di chuyển code màn ERP sang HRM, phân quyền cho mục mới.

## Quyết định chính

- **Mục chưa có màn hiển thị xám mờ, không bấm được** (thẻ `<a>` không có `href` +
  `opacity: .45` + `cursor: not-allowed` + tooltip "Chức năng chưa được xây dựng") — thay vì
  ẩn đi hoặc trỏ tới trang "đang xây dựng". User cần nhìn thấy quy hoạch đầy đủ ngay trên menu.
  Dùng `<a>` chứ không phải `<span>` vì toàn bộ style sidebar nằm ở selector `li > a`.
- **Chỉ mục có ghi chú "Đặt link sang ERP"/"Link ERP"/"Giữ ERP" trong `erp-menu-inventory`
  mới được link thật** (10 mục). Các mục nguồn ERP còn lại vẫn xám mờ, dù màn đó đang chạy bên ERP —
  đúng yêu cầu user, tránh đưa người dùng nhảy qua lại 2 cổng.
- **Phân hệ "Danh mục hàng hóa - dịch vụ" (35 màn) không tạo** — user phát hiện nó **không có
  trong sơ đồ v1.6**, là ô chứa do người lập sheet tự thêm. Sơ đồ thắng sheet khi mâu thuẫn.
- **Ẩn bằng cờ `hidden` trong registry, giữ nguyên `permissionType` 20/21/22** — cột `type`
  của `hrm_permissions` có thể đã có dữ liệu, đánh số lại sẽ làm lệch quyền.
- **Không sửa `isShowMenuParent`/`isShowSubItemMenu`** (hàm dùng chung). Hành vi mặc định đã
  đúng: subItem không khai `isShow` thì hiện; nhóm cha hiện khi có ≥1 sub hiện. Chỉ **thêm**
  nhánh render vào `Sidebar.vue`, không đổi nhánh `router-link` hiện có.
- **Chỉ đụng `Sidebar.vue`, không đụng topbar** — 14 phân hệ cần bổ sung đều dùng
  `layout: 'default-sidebar'`.
- **Tên mục/nhóm lấy nguyên văn sheet**, kể cả chỗ viết hoa lệch hay trùng tên ở 2 nhóm
  (Bán hàng có "Chương trình khuyến mại" ở cả `Thông báo` và `Quản lý giá bán - CTKM`) —
  không dedupe, để đối chiếu ngược lại sheet dễ.

## Spec chi tiết

`docs/superpowers/specs/2026-08-01-bo-sung-menu-phan-he-design.md`
(kèm Phụ lục A liệt kê đủ 350 mục theo phân hệ và nhóm, sinh lại từ menu thực tế)

## Nguồn dữ liệu

| Nguồn | Vai trò |
| --- | --- |
| `Bảng xử lý và test dữ liệu gộp cổng + sơ đồ tách phân hệ.xlsx` → sheet `Gộp phân hệ ERP-HRM` | 857 dòng chức năng — nguồn chuẩn của menu |
| `erp-menu-inventory (1).xlsx` → sheet `Chi tiết chức năng` | 275 chức năng ERP + ghi chú xác định màn nào link sang ERP |
| `TanPhatDev/routes/web.php` | Resolve route name Laravel → URL thật |
| `Sơ đồ tổng thể phần mềm v1.6 (24/07/2026)` | Chuẩn danh sách phân hệ — thắng sheet khi mâu thuẫn |

## Liên quan

- Tiền đề: `.plans/tach-phan-he-erp-hrm/` (giai đoạn 1 — khung phân hệ + registry)
- Giải quyết một phần Phase 7 của feature đó (mục "Rà lại sheet")

## Trạng thái

Phase 0-8 xong, kiểm thử tự động PASS hết (render thật template qua `vue-server-renderer`).
Còn Phase 9: **verify trên browser thật** — xem `plan.md`.

⚠️ Con số 326 ở bản đầu là sai (đối chiếu nhãn toàn hệ thống nên bỏ sót mục trùng tên giữa
2 phân hệ). Số thực tế sau cài đặt là 336, cộng 14 màn tái phân bổ (Phase 7) và 5 màn bổ sung
(Phase 8) thành **355**.

## Quyết định bổ sung (Phase 7)

- **Ẩn phân hệ làm khuất màn của phân hệ khác** — phải rà lại. Ẩn Mua hàng/Kho/Vận chuyển đã
  làm 14 màn thuộc diện chuyển sang HRM trở nên vô hình vì sheet gộp xếp chúng vào 3 phân hệ đó.
- **Chữ đỏ trong `erp-menu-inventory` = không chuyển đợt này** (24 dòng, note "Bỏ" /
  "Không chuyển, chờ logic mới"). Vẫn giữ trong menu vì chúng thuộc quy hoạch, chỉ chưa port.
- **4 màn Kiểm kê → Tài chính**: trong ERP vốn nằm ở menu `Kế toán > Kiểm kê`, sheet gộp mới
  xếp sang Kho. Trả về đúng chỗ gốc, cả 4 khai `erpPath`.
- **10 phiếu Khởi tạo → Bán hàng**: `erp-menu-inventory` ghi "Chuyển Khởi tạo của KD sang nền
  tảng HRM" — phiếu do NV kinh doanh lập.

## Quyết định bổ sung (Phase 8)

- **Sheet gộp có sẵn 4 dòng GIỮ CHỖ** (nhóm `Báo giá` 3 dòng, `Kết chuyển cuối kỳ` 1 dòng)
  — có nhóm nhưng cột `Chức năng` bỏ trống, nên đối chiếu theo tên không khớp được. Đã điền
  vào 4 dòng đó thay vì thêm dòng mới.
- **Hậu tố `(ERP)`** cho chức năng trùng vai trò với module có sẵn của HRM, để user lọc bỏ sau.
- **Sửa file Excel của user phải sao lưu trước** — bản gốc lưu ở
  `Bảng xử lý ... - truoc-khi-bo-sung-menu-20260801.xlsx`.
