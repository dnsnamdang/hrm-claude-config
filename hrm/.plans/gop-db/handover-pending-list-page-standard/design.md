# Design — Chuẩn hoá màn "Phiếu bàn giao chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Màn hình: `/assign/handover/pending`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-handover-pending-list-page-standard-design.md`
Tiếp nối 2 màn anh em **cùng entity, cùng `HandoverResource`**, đã chuẩn hoá 2026-09-07:
`.plans/gop-db/handover-list-page-standard/` · `.plans/gop-db/handover-receiving-list-page-standard/`

## Mục tiêu

Đưa màn chờ duyệt về đúng khuôn `list-page` và **dùng lại phần BE đã sửa cho 2 màn kia** — hiện
`pending()` là nhánh code song song, không hưởng gì từ 2 đợt chuẩn hoá trước.

## Hiện trạng trước khi sửa

- Bộ lọc còn `V2BaseFilterPanel` cũ (8 ô cứng trong slot, có `title`/`subtitle` riêng); **không có
  auto-search** — đổi ô lọc xong phải bấm "Tìm kiếm" mới chạy.
- **Không sắp xếp được cột nào** — bảng không nhận `@sort`, không truyền `sortBy`/`sortDirection`.
- Mã phiếu là `<a href="javascript:void(0)" @click="$router.push()">` và **ô đó còn ôm cả nút thao
  tác** ("Xem & Duyệt").
- **8 cột, không cột nào khai `width`**, không `fixed-layout`; thiếu Người tạo · Ngày tạo · Người
  cập nhật · Ngày cập nhật · Phòng ban · Ghi chú.
- Không cấu hình cột, không giữ bộ lọc, không hành động Lịch sử.
- Nút **Xuất Excel là nút chết**: gọi lại chính API danh sách rồi hiện toast *"Chức năng xuất Excel
  đang phát triển"*.
- Ô lọc **Giải pháp bị `disabled` cứng** — không bao giờ chọn được, chỉ tự điền theo Dự án.
- 7 chỗ chèn `'—'`, 3 chỗ `font-weight-bold`; slot `#toolbar` thay cả khối tiêu đề bảng.

## 3 lỗi CÓ SẴN sửa kèm

| Lỗi | Hậu quả |
| --- | --- |
| Bộ lọc **"Ngày gửi duyệt từ/đến"** lọc trên cột `updated_at`, không phải `submitted_at` | Lọc ra sai phiếu: `updated_at` đổi mỗi lần sửa/duyệt, còn `submitted_at` mới là mốc gửi duyệt. Cột `submitted_at` **đã có sẵn** trong bảng và `submit()` có ghi |
| `pending()` chốt cứng `orderBy('created_at','desc')`, không dùng `applyHandoverSort()` (whitelist 13 khoá) **đã có sẵn trong cùng service** | Màn không sắp xếp được cột nào, và thiếu khoá chốt `id desc` |
| Nút Xuất Excel gọi lại API danh sách rồi báo "đang phát triển" | Bấm nút không bao giờ ra file |

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã phiếu**, `nuxt-link` vào `/assign/handover/{id}`, sticky + locked |
| Hành động | **Duyệt** (điều hướng sang chi tiết — skill giữ "Duyệt" ở danh sách làm lối tắt) + **Lịch sử** (dùng lại `HandoverHistoryModal` của màn danh sách) |
| Số cột | **15**, mặc định hiện hết, `fixed-layout` |
| Bộ lọc | `V2BaseSmartFilterPanel`, **8 mục**; ô Giải pháp thành ô chọn thật lọc theo Dự án |
| Xuất file | Route + `pendingExport()` + `DynamicExport` + registry **`handovers`** dùng chung với màn danh sách |

## 3 cột bị BỎ HẲN thay vì nối dữ liệu

`approver_name` · `approved_at` · `reject_reason` — màn này lọc cứng `status = Chờ duyệt`, mà
`submit()` đặt `reject_reason = null` và phiếu chưa ai duyệt nên `approved_by` / `approved_at` cũng
NULL. Ba cột đó rỗng theo **định nghĩa** của màn, giữ lại chỉ tốn bề ngang.

Cùng lý do bỏ 3 khoá đếm `accepted_items` / `rejected_items` / `pending_items`: công việc chỉ được
nhận/từ chối **sau khi phiếu được duyệt**, ở trạng thái này luôn là `0 / 0 / tổng`. Cột "Công việc"
chỉ còn **tổng số**.

## Điểm đáng nhớ

- Bảng `handovers` **rỗng trên DB dev** → kiểm chứng bằng phiếu giả trong transaction rồi `ROLLBACK`
  (giống 2 màn anh em).
- Cột "Trạng thái" trên màn này luôn là *Chờ duyệt* nhưng vẫn giữ + vẽ badge thật cho khớp 2 màn
  kia, thay vì bỏ đi.
- `columnScreenKey` là **`handover_pending`** (khác `handovers` của màn danh sách và
  `handover_receiving`) để cấu hình cột 3 màn không đè nhau.
