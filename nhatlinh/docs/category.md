# Danh mục (Category)

## Mục đích

Phân hệ quản lý các danh mục dùng chung và cấu hình hệ thống cho toàn bộ ứng dụng (ngành nghề, loại tài liệu, vai trò dự án, các thiết lập chung...). Các module nghiệp vụ khác (HCNS, Chấm công, Tính lương) tham chiếu danh mục con và cấu hình từ phân hệ này.

## Vị trí

- **Backend:** `nhatlinh-api/Modules/Category/`
- **Frontend:** `nhatlinh-client/pages/category/`
- **Route prefix:** `/api/v1/category`
- **Layout FE:** `nhatlinh-client/layouts/category.vue`

## Trạng thái hiện tại

Đã scaffold base (module Laravel + layout + dashboard placeholder). Chưa có entity danh mục con — sẽ bổ sung ở task sau theo nhu cầu.

## Spec

`docs/superpowers/specs/2026-05-16-category-module-scaffold-design.md`

## Convention khi thêm entity danh mục con

Luồng BE: Route → Controller (`extends ApiController`) → Request (1 file dùng chung cho store + update, `extends Modules\Training\Http\Requests\BaseRequest`) → Service (wrap `DB::transaction()` cho store/update/destroy) → Model (`extends BaseModel`, `$guarded = []`) → Resource (tách 2 file: List + Detail) → Migration (cột có `->comment()`, không foreign key constraint).
