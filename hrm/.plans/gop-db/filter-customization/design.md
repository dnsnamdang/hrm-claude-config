# Cài đặt bộ lọc — chọn trường hiển thị + kéo thả sắp xếp

**Phụ trách:** @dnsnamdang · **Nhánh:** `gop_db` (worktree `gop_db-api` + `gop_db-client`) · **Ngày:** 2026-08-12

> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-12-filter-customization-design.md`

## Mục tiêu

Mỗi user tự chọn **trường lọc nào hiển thị** trên khối bộ lọc và **kéo thả sắp xếp vị trí** — giống popup "Tuỳ chỉnh cột" của bảng, nhưng cho bộ lọc. Mặc định chưa cấu hình → **hiện đủ**.

UX tham chiếu: demo kế toán `demo 3/assets/app.js` — `setupFilterSettings()` (checkbox, chưa kéo thả) + `setupColumnConfig()` (checkbox + kéo thả). Feature này ghép 2 cái, và lưu BE thay vì localStorage.

## Scope

- **BE**: bảng mới `filter_customizations` + Entity + Service + 2 route (`human/filter-customizations` GET detail / POST).
- **FE**: 2 component mới — `V2BaseSmartFilterPanel.vue` (panel khai báo bằng schema) + `modal/filter-customization-modal.vue` (popup checkbox + `vuedraggable`).
- **Pilot**: áp dụng màn `/assign/customers` (15 trường lọc), render bằng `V2Base*`.

## Quyết định lớn

1. Lưu **BE theo user**, không localStorage.
2. Bảng **generic** `(created_by, table, config json)`, unique `(created_by, table)` — **không** copy schema cột-mỗi-màn của `column_customizations` (Entity đó đang có 25 cột trong `$casts`, thêm màn là phải migration).
3. Khoá màn = **tên bảng chính** (`table`, vd `'customers'`), giống param của "Tuỳ chỉnh cột". Bảng dùng nhiều màn → thêm tiền tố ngữ cảnh (`my_job_tasks`…), vẫn không cần migration.
4. `config` = `[{key, isVisible}]` — thứ tự mảng = thứ tự hiển thị. **Không lưu `label`.**
5. Trường bỏ tick = **ẩn hẳn** (không rơi xuống "Tìm kiếm nâng cao"), và **reset giá trị lọc về null** để không lọc ngầm.
6. Không có trường `locked` — mọi trường đều bật/tắt và kéo được.
7. **Component mới**, không sửa `V2BaseFilterPanel` (26 màn đang dùng) — panel cũ nhận markup qua slot nên không thể sắp xếp được. Component mới nhận **schema mảng field** + slot escape hatch `#field-<key>` cho field cần logic riêng.
8. **Merge DB ↔ schema FE nằm trong component** (không để mỗi page tự copy như `solutions/index.vue:827`): key còn trong schema → giữ `isVisible` + vị trí từ DB, lấy phần còn lại từ schema; key đã xoá khỏi FE → **bỏ hẳn** (khác code cũ đang giữ lại — với bộ lọc sẽ vỡ UI/bắn param rác); key mới ở FE → **append cuối, hiện**. Nhờ vậy **bổ sung trường lọc mới không bị lỗi, không bị mất**.

9. **Quy tắc gom nhóm field (áp cho mọi màn dùng component này)**: nhiều ô nhập phải gom thành **một** field trong schema khi (a) **cùng một component render ra** (vd `V2BaseCompanyDepartmentFilter` → Công ty/Phòng ban/Bộ phận/Nhân viên; `CascadePairSelect` → Loại hình hoạt động + Lĩnh vực kinh doanh), hoặc (b) **dữ liệu phụ thuộc lẫn nhau** (cascade cha → con). Tách ra thì user ẩn được cha mà giữ con (con mất options) hoặc kéo con lên trước cha (sai trình tự nhập). Field nhóm **bắt buộc** khai `resetKeys` để ẩn nhóm là xoá hết giá trị con. Hai ô chỉ giống nhau về nghiệp vụ nhưng độc lập dữ liệu thì để riêng (vd Quốc gia và Tỉnh/Thành phố ở màn KH — API `provinces` không nhận `nation_id`).

## Không làm

Không migrate 26 màn `V2BaseFilterPanel`; không refactor `column_customizations`; không làm saved filter preset; chưa áp dụng phân hệ Kế toán (sau khi nghiệm thu pilot).
