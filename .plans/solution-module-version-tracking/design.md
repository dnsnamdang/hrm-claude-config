# Design: Liên kết solution_module_versions với solution_versions

## Bối cảnh

Bảng `solution_module_versions` hiện không có field `solution_version_id`. Cần thêm để track module version thuộc solution version nào.

## Thay đổi

- **Migration**: Thêm cột `solution_version_id` (unsignedBigInteger, nullable, index) vào `solution_module_versions`
- **Model** `SolutionModuleVersion`: Thêm relationship `solutionVersion()`
- **SolutionService.php**: Khi tạo module mới → gán `solution_version_id = $solution->current_version_id`
- **SolutionModuleService.php**: Khi tạo version mới cho module → gán `solution_version_id = $solutionModule->solution->current_version_id`

## Không thay đổi
- Bảng `solution_versions` giữ nguyên
- Logic khác không ảnh hưởng
