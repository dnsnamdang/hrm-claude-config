# Design — Chuẩn hoá màn "Báo giá chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Màn hình: `/assign/quotations/pending-approval`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-quotation-pending-approval-list-page-standard-design.md`
Màn anh em: `/assign/quotations` — **cùng entity, cùng `QuotationResource`, cùng
`applyListFilters()`**, đã chuẩn hoá ở `.plans/gop-db/quotation-list-page-standard/`

## Mục tiêu

Đưa màn chờ duyệt về đúng khuôn `list-page` và dùng lại phần BE đã sửa cho màn danh sách. Phần
truy vấn dùng chung sẵn (`applyListFilters` → `applyQuotationSort`) nên khối lượng BE nhỏ; việc
chính nằm ở giao diện.

## Hiện trạng trước khi sửa

- Bộ lọc còn `V2BaseFilterPanel` cũ, **chỉ 2 ô** (Dự án TKT · Cấp duyệt) trong khi máy chủ đã nhận
  sẵn 12 khoá lọc; có `title`/`subtitle` riêng.
- Cột **"Mã BG • BOM"** gộp mã + tên BOM, và **nút "Xem và duyệt" nằm trong chính ô đó**.
- **8 cột, không cột nào khai `width`**, không `fixed-layout`.
- Cấp duyệt vẽ bằng **badge tự chế** (`.badge-level-2` / `.badge-level-3`, nền đậm chữ trắng, mã màu
  cứng `#ff9800` / `#e91e63`) — trái quy tắc badge nền nhạt của skill, trong khi Resource **đã trả
  sẵn `approval_level_color`**.
- Cấu hình cột viết tay trong page; STT và cột mã **không `locked`** nên user ẩn được cột định danh.
- **Không có Xuất Excel**; thiếu Ngày tạo · Người/Ngày cập nhật · Giai đoạn dự án · Tiền tệ · Giá trị.
- `'N/A'` ở cột Dự án; `font-weight-bold` trong ô; `head()` nạp lại **CSS remixicon từ CDN** (đã có
  sẵn trong dự án).
- `mounted()` `await Promise.all([loadFilterOptions, getFields])` **trước** khi gọi danh sách →
  bảng chờ 2 request không liên quan mới bắt đầu tải (skill mục 8).

## 3 lỗi CÓ SẴN sửa kèm

| Lỗi | Hậu quả |
| --- | --- |
| `QUOTATION_SORTABLE_COLUMNS` **thiếu `submitted_at`** — mà đó chính là khoá sắp xếp MẶC ĐỊNH của màn này (`initialFilters.sort_field = 'submitted_at'`) | Mặc định âm thầm rơi về `created_at desc`; bấm sort cột "Ngày gửi" **không đổi gì** |
| Whitelist cũng thiếu `customer_name`, `price_approval_level`, `status` — 3 cột FE khai `sortable: true` | Bấm sort 3 cột đó cũng không đổi gì, không báo lỗi |
| `QuotationResource` trả `submitted_at` **THÔ** (chuỗi ISO), khác hẳn `approved_at`/`created_at`/`updated_at` đã format ở BE | Màn phải tự nhập `dayjs` để format lại — mỗi nơi hiển thị một kiểu |

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã báo giá**, `nuxt-link` vào `/assign/quotations/{id}`, sticky + locked |
| Hành động | **Duyệt** (điều hướng sang chi tiết — skill giữ "Duyệt" ở danh sách làm lối tắt) + **Lịch sử phê duyệt** (dùng lại `QuotationHistoryModal`) |
| Số cột | **17**, mặc định hiện hết, `fixed-layout`; bộ cột + bề rộng lấy theo màn `/assign/quotations` |
| Bộ lọc | `V2BaseSmartFilterPanel`, **6 mục** — thêm các ô máy chủ đã nhận mà FE chưa bày (ô Khách hàng để lại: cần select2-remote, ô tìm nhanh đã tìm theo tên KH) |
| Cấp duyệt | `V2BaseBadge :color="item.approval_level_color"` — bỏ 2 class badge tự chế |
| Xuất file | Route + `pendingApprovalExport()` + `DynamicExport` + registry **`quotations`** dùng chung |

## Điểm đáng nhớ

- **BỎ 2 cột "Người duyệt" / "Ngày duyệt"** — quyết định sau khi đo **ĐÚNG dữ liệu màn trả về**,
  không phải đếm thô toàn bảng:

  | Cách đếm | Kết quả |
  | --- | --- |
  | Thô `status IN (3,4) AND is_summary = 0` (KHÔNG qua gate quyền) | 38 dòng — **38 có `approved_at`**, chỉ 4 có `submitted_at` |
  | `getPendingApproval()` của một người duyệt thật (đủ quyền TP + BGĐ) | **13 dòng — 0 có `approved_at`, 13/13 có `submitted_at`** |

  Tức 25 dòng còn lại là dữ liệu cũ/nhập tay nằm ngoài hàng chờ của bất kỳ ai trong DB dev này. Đúng như
  code nói: `submitForApproval()` không ghi `approved_by`/`approved_at`, còn `reject()` xoá chúng — nên
  phiếu đang chờ duyệt thật sự luôn rỗng 2 cột đó.

  ⚠️ Bài học: đếm thô trên bảng **không thay được** việc chạy đúng hàm truy vấn của màn — bản
  nháp đầu của design này đã kết luận ngược (“giữ 2 cột vì 38/38 có dữ liệu”) vì đếm thiếu gate quyền.

- Cột **"Ngày gửi duyệt" có dữ liệu đủ 13/13 dòng** và là khoá sắp xếp mặc định — giữ, và chính
  nó là lý do phải vá whitelist sắp xếp ở Phase 1.
- `columnScreenKey` giữ **`quotations_pending_approval`** (khác `quotations` của màn danh sách).
