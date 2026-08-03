# Fix — Màn Danh sách làm giải pháp: 4 cột master data lấy sai nguồn

## Bối cảnh
- URL: `/assign/solutions` → `GET /assign/solutions` → `SolutionController::index` → `SolutionService::index()` → `SolutionResource`.
- Bug: `SolutionResource` lấy Nhóm ngành / Nhóm giải pháp / Ứng dụng / Lĩnh vực KD khách hàng qua `prospectiveProject->*`, trong khi filter cùng tên lại lọc trên cột của chính bảng `solutions` (`SolutionService::index()` dòng 90-101).
- Hệ quả: khi user chọn giá trị khác dự án TKT trên form giải pháp (`SolutionService.php:607-609` — ưu tiên giá trị user chọn, chỉ fallback theo dự án), lọc ra dòng mà cột hiển thị tên khác hẳn filter.
- Nghiệp vụ đúng: cột hiển thị phải bám `solutions.scope_id` / `industry_id` / `application_id` / `customer_scope_id` — đúng như filter và như màn chi tiết (`DetailSolutionResource.php:114-116` đã dùng `$this->industry`).
- Entity `Solution` đã có sẵn 4 relation `scope()` / `industry()` / `application()` / `customerScope()` (`Modules/Assign/Entities/Solution.php:100-118`) → không cần thêm relation.
- Chốt với user (2026-07-15): fix cả 4 cột, KHÔNG fallback về dự án. Cột "Loại hình hoạt động KH" giữ nguyên (cột + filter đều đi qua dự án TKT → đang khớp).

## Phase 1 — Fix BE
- [x] `SolutionResource`: `scope_name` đổi sang `$this->scope->name`, `industry_name` → `$this->industry->name`, `application_name` → `$this->application->name`, `customer_scope` → `$this->customerScope->name`.
- [x] `SolutionService::index()`: thêm `with(['scope:id,name', 'industry:id,name', 'application:id,name', 'customerScope:id,name'])` — hàm trước đó KHÔNG eager load gì.
- [x] `SolutionService::getAll()`: bổ sung 4 relation trên vào đầu mảng `with()` sẵn có — cùng dùng `SolutionResource` cho popup Danh sách giải pháp.

## Verify (empirical, tinker + DB local, 2026-07-15)
- [x] Bug tái hiện trước fix: 2/11 giải pháp lệch — `GP02` solution="Dịch vụ tư vấn cấp phép" nhưng cột hiện "Toyota" (của dự án); `GP03` solution có giá trị nhưng dự án NULL → cột hiện "—".
- [x] Sau fix, lọc `industry_id=9` ("Dịch vụ tư vấn cấp phép") → 2/2 dòng cột hiển thị khớp filter.
- [x] Filter Nhóm ngành → 2 dòng, lệch=0. Filter Lĩnh vực KD KH → 2 dòng, lệch=0.
- [x] Eager load ăn: 11 dòng → 10 query, không tăng theo số dòng.
- [ ] Filter Ứng dụng: CHƯA verify được có ý nghĩa — xem mục Tồn đọng.
- [ ] Test UI thật trên `/assign/solutions` + popup Danh sách giải pháp (mới verify ở tầng service/resource).

## Tồn đọng / rủi ro cần user quyết
- **FK mồ côi**: 2 solution có `application_id = 222` nhưng id 222 KHÔNG tồn tại trong bảng `applications` (các id hợp lệ đang dùng: 8, 38, 76, 100, 101, 137). Hệ quả: `GP02` trước fix hiện "Đại lý hãng (3S-4S-5S)" (lấy của dự án), sau fix hiện "—". Dòng này vốn không lọc ra được vì dropdown không có id 222. Chưa rõ là rác dữ liệu local hay có ở production → cần kiểm tra prod trước khi release.
- Resource vẫn lazy-load `prospectiveProject` từng dòng trong `index()` (N+1 có sẵn từ trước, không do fix này) — chưa xử lý, nằm ngoài scope.
