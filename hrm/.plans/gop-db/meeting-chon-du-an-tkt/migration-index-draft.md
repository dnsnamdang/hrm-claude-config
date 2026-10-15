# Bản nháp migration index (CHƯA tạo trong hrm-api — tạo file bị chặn quyền 14/10)

Đích: `hrm-api/Modules/Assign/Database/Migrations/2026_10_14_000001_add_meeting_option_indexes_to_prospective_projects_table.php`
Khuôn: `Modules/CustomerCare/Database/Migrations/2026_09_08_000001_add_customer_product_index_to_serials_table.php` (kiểm index tồn tại trước khi thêm).

Hiện trạng DB local `local_hrm_erp` (SHOW INDEX 14/10):
- `prospective_projects` (334 dòng): PRIMARY, code, form_template_snapshot_id, is_parent_project, parent_id
- `prospective_project_support_departments`: chỉ PRIMARY
- `prospective_project_support_department_employees`: chỉ PRIMARY

| Bảng | Index | Cột |
|---|---|---|
| prospective_projects | prospective_projects_status_index | status |
| prospective_projects | prospective_projects_customer_id_index | customer_id |
| prospective_projects | prospective_projects_created_by_index | created_by |
| prospective_projects | prospective_projects_solution_employee_id_index | solution_employee_id |
| prospective_project_support_departments | pp_support_departments_prospective_project_id_index | prospective_project_id |
| prospective_project_support_department_employees | pp_support_dept_employees_support_department_id_index | prospective_project_support_department_id |
| prospective_project_support_department_employees | pp_support_dept_employees_employee_id_index | employee_id |

```php
class AddMeetingOptionIndexesToProspectiveProjectsTable extends Migration
{
    private const INDEXES = [ /* như bảng trên: table => [indexName => column] */ ];

    public function up(): void
    {
        foreach (self::INDEXES as $table => $indexes) {
            if (!Schema::hasTable($table)) continue;
            foreach ($indexes as $name => $column) {
                if (!Schema::hasColumn($table, $column) || $this->indexExists($table, $name)) continue;
                Schema::table($table, function ($t) use ($column, $name) { $t->index($column, $name); });
            }
        }
    }

    public function down(): void { /* dropIndex nếu indexExists */ }

    private function indexExists(string $table, string $name): bool
    {
        return count(DB::select('SHOW INDEX FROM `' . $table . '` WHERE Key_name = ?', [$name])) > 0;
    }
}
```
