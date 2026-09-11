# Design — Chuẩn hoá màn "Yêu cầu làm giải pháp chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
Màn hình: `/assign/request-solution/pending`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-request-solution-pending-list-page-standard-design.md`
Tiếp nối: `.plans/gop-db/request-solution-list-page-standard/` (màn `/assign/request-solution` —
**cùng entity, cùng Resource**, đã chuẩn hoá 2026-09-07)

## Mục tiêu

Đưa màn chờ duyệt về đúng khuôn `list-page` và **dùng lại toàn bộ phần BE đã sửa cho màn danh
sách** — hiện `pending()` là một nhánh code song song, không hưởng gì từ đợt chuẩn hoá trước.

## Hiện trạng trước khi sửa

- Bộ lọc còn `V2BaseFilterPanel` cũ (4 ô cứng trong slot, có `title`/`subtitle` riêng).
- Cột gộp **"Mã • Tên yêu cầu"** chứa mã + tên + 2 dòng phụ + **4 icon thao tác** (có cả "Xem").
- **17 cột, không cột nào khai `width`**, không `fixed-layout`.
- **5 cột in cứng dấu gạch trong template** (`requestStatus`, `receiverName`, `solutionCode`,
  `solutionPM`, và `priority`/`projectStage` khi rỗng) — không phải thiếu dữ liệu mà là **template
  không hề đọc dữ liệu**; riêng 4 cột đầu máy chủ cũng chưa eager load nên có đọc cũng rỗng.
- Không có cấu hình cột, không popup chọn trường xuất file; xuất `.xls` cột cứng.
- `handleFilterChange(filters)` nhận sai kiểu payload (panel mới phát `{key, value}`) → đổi ô lọc
  là **nhét 2 khoá rác `key`/`value` vào `filters` rồi gửi lên API**.
- `handleSort` / `handleReset` vừa đổi `filters` vừa gọi `loadData()` trong khi deep watcher cũng
  gọi → **2 request mỗi thao tác**.
- `$nuxt.$loading` gọi thẳng trong `exportExcel()`.

## 4 lỗi CÓ SẴN sửa kèm

| Lỗi | Hậu quả |
| --- | --- |
| `pending()` sắp xếp bằng `orderBy($request->sort_field, $request->sort_dir)` — nhận thẳng chuỗi từ URL, không whitelist, không chốt `id desc` | Gõ tay tên cột lạ là 500; lật trang thấy bản ghi lặp/mất. `applySort()` (whitelist 15 khoá) **đã có sẵn** từ đợt chuẩn hoá màn danh sách nhưng `pending()` không gọi |
| `pending()` thiếu 5 eager load mà `index()` đã bổ sung | 4 cột luôn rỗng (Phòng tiếp nhận · Người tiếp nhận · Mã GP · PM làm GP), cột Mức độ ưu tiên cũng không có nguồn; kèm N+1 query |
| Không có quyền → `pending()` trả **`[]` (mảng)**, còn `exportPending()` gọi `$query->get()` | **Fatal 500** ngay khi người không có quyền bấm Xuất Excel |
| FE `canReceive()` **hard-code `return true`** (kèm comment "tạm thời cho demo") | Nút Tiếp nhận hiện với mọi dòng, không theo cờ nghiệp vụ — trong khi entity đã có sẵn `isCanReceive()` |

## Quyết định chính

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã yêu cầu**, `nuxt-link` vào `/assign/request-solution/{id}`, sticky + locked |
| Hành động | **Tiếp nhận** (mở modal) + **Yêu cầu bổ sung thông tin** (điều hướng). Bỏ "Xem" |
| **Bỏ "Từ chối" khỏi danh sách** | Skill mục 1 (chốt 2026-08-24): hành động phủ quyết chỉ đặt ở màn CHI TIẾT — người duyệt phải đọc nội dung trước khi từ chối. Màn `_id/index.vue` đã có nút này |
| **Bỏ "Hủy yêu cầu" khỏi danh sách** | Cùng lý do trên. Thêm nữa `is_can_cancel` chỉ đúng với NGƯỜI TẠO, mà màn này là của người TIẾP NHẬN → gần như luôn ẩn |
| Số cột | **19**, mặc định hiện hết, `fixed-layout` — bộ cột + bề rộng lấy theo màn `/assign/request-solution`, trừ 3 cột luôn rỗng ở màn này (xem dưới) |
| Bộ lọc | `V2BaseSmartFilterPanel`, **5 mục**: Công ty–Phòng ban–Bộ phận · Nhân viên gửi YC · Giai đoạn dự án · Ngày tạo từ/đến |
| Xuất file | Popup chọn trường + `DynamicExport` + registry **`request_solutions`** dùng chung với màn danh sách (cùng entity, cùng bộ cột) |
| Hành động "Lịch sử" | **Chưa làm** — giữ đúng quyết định của màn danh sách (module Assign chưa có `LogsCatalogHistory`) |

## Điểm đáng nhớ

- `pending()` kiểm tra `isCurrentEmployeeHasPermission('Tiếp nhận yêu cầu làm giải pháp')` **2 lần
  liên tiếp** (dòng 170 và 174) — lần sau là code chết. Gộp còn 1, và trả **query rỗng** thay vì mảng.
- Cột "Tiến trình YC" trên màn này luôn là *Chờ tiếp nhận* (`pending()` lọc cứng
  `status = STATUS_CHO_TIEP_NHAN`) nhưng vẫn giữ cột + badge thật cho khớp màn danh sách, thay vì
  in cứng dấu gạch như bản cũ.
- **3 cột bị bỏ hẳn** (Người tiếp nhận YC · Mã GP · PM làm GP) và **ô lọc `receiver_by` không bày ra**:
  đo dữ liệu thật thấy `receive_id` chỉ được ghi từ trạng thái **Đã tiếp nhận** trở đi (4/4 phiếu
  *Chờ tiếp nhận* đều NULL) và không phiếu nào ở trạng thái này có giải pháp gắn vào — tức 3 cột đó
  rỗng theo ĐỊNH NGHĨA của màn, và ô lọc kia luôn ra 0 kết quả. Giữ lại chỉ tốn bề ngang.
  Phòng tiếp nhận YC thì **có dữ liệu** (4/4) nên giữ.
- `localStorageKey` giữ nguyên `assign_request_solution_pending` (khác màn danh sách), nhưng
  `columnScreenKey` là **`request_solutions_pending`** để cấu hình cột 2 màn không đè nhau.
