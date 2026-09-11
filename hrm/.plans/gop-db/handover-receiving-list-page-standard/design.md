# Design — Chuẩn hoá màn "Phiếu bàn giao chờ tiếp nhận" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-handover-receiving-list-page-standard-design.md`

## Mục tiêu

Đưa `/assign/handover/receiving` về đúng khuôn `list-page`, và **sửa lỗi gốc về đơn vị dữ liệu**:
màn hiển thị theo PHIẾU nhưng API trả theo CÔNG VIỆC rồi để FE gom bằng JS.

## Hiện trạng trước khi sửa

- **Phân trang sai từ gốc**: `GET assign/handovers/receiving` trả từng `handover_item` đã phân
  trang, FE gom `handover_id` bằng JS trong `loadData()`. Hệ quả: số dòng mỗi trang không đều (1
  phiếu 30 việc ăn hết 1 trang), cột "Số công việc" chỉ đếm phần việc rơi vào trang đó, và **1
  phiếu có thể hiện lại ở trang sau với con số khác**. `meta.total` là số công việc, không phải số
  phiếu.
- Cột "Số công việc" đếm **mọi** công việc của phiếu có trong trang, không phân biệt việc của ai.
- Nút **Xuất Excel là nút chết**: gọi lại chính API danh sách rồi hiện toast "Chức năng xuất Excel
  đang phát triển".
- **Không sắp xếp được** (bảng không nhận `@sort`, không có `sortBy`).
- Mã phiếu là `<a href="javascript:void(0)" @click="$router.push()">`; nút thao tác nằm trong ô Mã
  phiếu; 8 cột không cột nào khai `width`; không `fixed-layout`.
- Ô lọc **Giải pháp bị `disabled` cứng** — không bao giờ chọn được, chỉ tự điền theo Dự án.
- Không cấu hình cột, không giữ bộ lọc, không hành động Lịch sử; slot `#toolbar` thay cả khối tiêu
  đề bảng.

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Đơn vị dòng | **PHIẾU** — BE thêm `HandoverService::receivingHandovers()` trả `Handover` + `withCount` |
| 4 con số | Đếm **công việc CỦA TÔI** trong phiếu (`receiver_id` = người đăng nhập), không phải toàn bộ phiếu |
| Resource | Tạo mới `ReceivingHandoverResource` (không đụng `HandoverResource` đang dùng ở 2 màn khác) |
| Cột định danh | **Mã phiếu**, `sticky` + `locked`, `nuxt-link` sang `/assign/handover/{id}/receive` |
| Hành động | **Tiếp nhận** (điều hướng) + Lịch sử; bỏ "Xem & Tiếp nhận" trong ô Mã phiếu |
| Số cột | **14**, mặc định hiện hết |
| Xuất file | Route + `receivingExport()` + `ExportColumnRegistry['handover_receiving']` 15 cột |
| Bộ lọc | `V2BaseSmartFilterPanel`, 6 mục; Giải pháp thành ô chọn thật, lọc theo Dự án |

## Điểm đáng nhớ

- `Handover::items()` không có khoá `receiver_id` nên 4 `withCount` phải **dùng lại đúng closure
  lọc** đã dùng cho `whereHas` — nếu không, con số đếm cả việc của người khác trong cùng phiếu.
- Hạng mục lưu ở 2 cột khác nhau: Task → `solution_module_id`, Issue → `module_id`, nên bộ lọc phải
  tách 2 nhánh `whereExists` (giữ nguyên cách bản cũ làm).
- 2 bảng `handovers` và `handover_items` **đều rỗng trên DB dev** → kiểm chứng bằng 4 phiếu + 7
  công việc giả trong transaction rồi `ROLLBACK`.
