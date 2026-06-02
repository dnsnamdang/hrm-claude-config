# Xóa mềm mẫu in (chỉ mẫu chưa được sử dụng & không phải mẫu hệ thống) — Design Spec

## Mục tiêu

Cho phép **xóa mềm** mẫu in tại màn `decision/category/print_templates`, **chỉ với mẫu in chưa được sử dụng ở bất kỳ đâu** trong HRM. Mẫu đang được dùng (dữ liệu hoặc bị code phụ thuộc) thì chặn xóa và báo lý do.

## Bối cảnh / Hiện trạng

- Frontend `index.vue` có dropdown "Xóa" nhưng `v-if="item.status"` — mà `PrintTemplateResource` **không trả** `status`, và bảng `print_templates` **chưa có cột `status`** → nút không bao giờ hiện. Template còn tham chiếu `getStatusClass`/`getStatusText` không tồn tại (code chết).
- Route `DELETE /human/print-templates/{id}` trỏ method `delete`, nhưng controller chỉ có `destroy()` **rỗng**; service chưa có hàm xóa → luồng xóa **chưa hoạt động**.
- `BaseModel` **không** dùng Laravel SoftDeletes. Convention soft-delete của codebase là **cột `status`** (set 0 khi xóa, lọc ở list) — xem `PrintTemplateService::deleteCompanyAccountBank` (đang comment) và `index.vue` đã code sẵn theo `item.status`.

## Quyết định thiết kế

- **Xóa mềm bằng cột `status`**: thêm `status` (tinyint, default 1 = hoạt động); xóa = set `status = 0`; danh sách chỉ hiển thị `status = 1`. (Không dùng `deleted_at` để khớp convention + frontend sẵn có.)
- **Precompute `can_delete` ở list**: API danh sách tính sẵn cờ `can_delete` cho từng dòng; frontend **chỉ hiện nút Xóa khi `can_delete = true`**. API xóa **vẫn validate lại** khi nhận request (phòng race/stale list — defense in depth).
- **Chặn xóa theo 2 lớp** (mẫu "đang được sử dụng" = thỏa **một trong hai**):
  1. **Tham chiếu dữ liệu**: `print_template_id` xuất hiện ở 1 trong 9 bảng (lịch sử quyết định đã dùng).
  2. **Mẫu hệ thống**: `code` nằm trong danh sách `PrintTemplate::PROTECTED_CODES` (bị code hardcode tra cứu theo `code`).
- **Phạm vi**: chỉ HRM (`hrm-api` + `hrm-client`). Phân hệ Dự án/Giao việc (module Assign) dùng `form_templates` — **hệ template khác**, không liên quan; nhưng `MeetingController` (Assign) có dùng print template `BIEN_BAN_CUOC_HOP` theo `code` → đã đưa vào `PROTECTED_CODES`.

## Lớp 1 — Tham chiếu dữ liệu (9 bảng FK)

Mẫu in coi là đang dùng nếu `print_templates.id` được tham chiếu ở bất kỳ bảng nào:

| # | Bảng | Cột FK |
|---|---|---|
| 1 | `decisions` | `print_template_id` |
| 2 | `department_establishments` | `print_template_id` |
| 3 | `department_dissolutions` | `print_template_id` |
| 4 | `trouble_shooting_reports` | `print_template_id` |
| 5 | `decision_labor_contracts` | `print_template_id` |
| 6 | `appendix_labor_contracts` | `print_template_id` |
| 7 | `training_contracts` | `print_template_id` |
| 8 | `self_notifications` | `print_template_id` |
| 9 | `suspend_labor_contracts` | `print_template_agreement_id` |

Ghi chú: ~20 loại quyết định nhưng hội tụ về 9 bảng này (rất nhiều loại lưu chung bảng `decisions`). Mỗi bảng còn có cột `print_template` (longText) lưu **snapshot nội dung** → tài liệu đã tạo không vỡ khi mẫu gốc bị xóa mềm.

## Lớp 2 — Mẫu hệ thống (tham chiếu theo `code` trong code)

Code tra cứu mẫu in theo `code` cố định lúc chạy → xóa là vỡ tính năng dù chưa có dữ liệu. Đã rà toàn bộ backend (mọi module + seeders):

| `code` | Nơi dùng | Tính năng |
|---|---|---|
| `BIEN_BAN_CUOC_HOP` | `Modules/Assign/.../MeetingController` | In biên bản cuộc họp (dự án/giao việc) |
| `HOP_DONG_DAO_TAO` | `Modules/Decision/Jobs/CreateTrainingContractJob` | Sinh hợp đồng đào tạo |
| `PHU_LUC_HOP_DONG_LAO_DONG` | `IncreaseSeniorityService`, `AppendixLaborContractService` | Sinh phụ lục HĐLĐ |
| `QUYET_DINH_DIEU_CHINH_LUONG` | Seeder | Mẫu hệ thống |
| `HOP_DONG_LAO_DONG_CHINH_THUC_KHONG_THOI_HAN` | Seeder | Mẫu hệ thống |

→ Lưu thành hằng số `PrintTemplate::PROTECTED_CODES = [...]` (5 code trên).

> **Lưu ý bảo trì:** danh sách này phải cập nhật khi dev thêm chỗ tra cứu mẫu in theo `code` mới. Ngoài ra Payroll Import tra theo `name`+`type` (động, theo tên trong Excel) — không phải phụ thuộc cố định nên không đưa vào danh sách.

## Luồng xử lý

**Hiển thị list:** API trả mỗi dòng kèm `can_delete`; frontend chỉ render nút Xóa khi `item.can_delete = true`. Mẫu hệ thống hoặc đang dùng → không có nút Xóa.

**Khi xóa** (vẫn validate lại ở backend):
```
User bấm "Xóa" → modal xác nhận → DELETE /human/print-templates/{id}
  → Service: tìm mẫu in (status = 1)
      ├─ không thấy                         → 404
      ├─ code ∈ PROTECTED_CODES             → 400 "Mẫu in hệ thống, không thể xóa"
      ├─ isPrintTemplateInUse (9 bảng)      → 400 "Mẫu in đang được sử dụng, không thể xóa"
      └─ hợp lệ                             → set status = 0 → 200 "success"
Frontend:
  200 → toast success "Xoá mẫu in thành công" + reload list
  4xx → toast error theo message backend (fallback "Xoá mẫu in thất bại")
```

## Chi tiết kỹ thuật

### DB / Migration (`hrm-api`)

- Migration `add_status_to_print_templates_table`: thêm `status` (`tinyInteger`/`unsignedTinyInteger`) default `1`, comment "1: hoạt động, 0: đã xóa". `down()` drop cột.
- Có PHPDoc trên `up()`/`down()` theo file mẫu của project.

### Entity (`Modules/Human/Entities/PrintTemplate.php`)

- Thêm `'status'` vào `$fillable`.
- Thêm hằng số:
  ```php
  public const PROTECTED_CODES = [
      'BIEN_BAN_CUOC_HOP',
      'HOP_DONG_DAO_TAO',
      'PHU_LUC_HOP_DONG_LAO_DONG',
      'QUYET_DINH_DIEU_CHINH_LUONG',
      'HOP_DONG_LAO_DONG_CHINH_THUC_KHONG_THOI_HAN',
  ];
  ```

### Service (`PrintTemplateService.php`)

- `getPrintTemplates()`:
  - Thêm điều kiện `where('status', 1)` (chỉ hiện mẫu hoạt động).
  - Sau khi phân trang, **tính `can_delete` cho từng dòng** (tránh N+1): gom `$ids` của trang hiện tại → gọi `getUsedTemplateIds($ids)` lấy tập id đang được tham chiếu → gán `$row->can_delete = !in_array($row->code, PrintTemplate::PROTECTED_CODES) && !in_array($row->id, $usedIds)`.
- `getUsedTemplateIds(array $ids): array` — duyệt map `[table => column]` gồm 9 entry; mỗi entry `DB::table($table)->whereIn($column, $ids)->whereNotNull($column)->distinct()->pluck($column)`; gộp tất cả thành 1 mảng id duy nhất (tổng **9 query/trang**, không phụ thuộc số dòng).
- `isPrintTemplateInUse(int $id): bool` — dùng cho validate lúc xóa: duyệt cùng map; mỗi entry `DB::table($table)->where($column, $id)->exists()`; trả `true` ngay khi gặp tham chiếu đầu tiên.
- `deletePrintTemplate(int $id)` — tìm mẫu `status=1`:
  - null → not found.
  - `in_array($model->code, PrintTemplate::PROTECTED_CODES)` → trả lỗi `protected`.
  - `isPrintTemplateInUse($id)` → trả lỗi `in_use`.
  - hợp lệ → `$model->fill(['status' => 0])->save()`.

### Controller (`PrintTemplateController.php`)

- Thay `destroy()` rỗng bằng `delete($id)` (khớp tên route):
  - not found → `responseJson(..., HTTP_NOT_FOUND)`.
  - protected → `responseJson('Mẫu in hệ thống, không thể xóa', HTTP_BAD_REQUEST)`.
  - in_use → `responseJson('Mẫu in đang được sử dụng, không thể xóa', HTTP_BAD_REQUEST)`.
  - OK → `responseJson('success', HTTP_OK)`.
- Route giữ nguyên: `Route::delete('/{id}', [PrintTemplateController::class, 'delete'])`.

### Resource (`PrintTemplateResource.php`)

- Trả thêm `'status' => $data->status` và `'can_delete' => (bool) ($data->can_delete ?? false)` cho mỗi dòng.

### Frontend (`pages/decision/category/print_templates/index.vue`)

- Nút Xóa: đổi `v-if="item.status"` → **`v-if="item.can_delete"`** (chỉ hiện cho mẫu được phép xóa). Dọn `getStatusClass`/`getStatusText` không tồn tại.
- `deleteReportTemplate()`: `.catch` đọc message từ `error.response?.data` để toast đúng lý do (hệ thống / đang dùng); fallback `'Xoá mẫu in thất bại'`.

## Xử lý lỗi & edge case

- Mẫu hệ thống (`code` ∈ PROTECTED_CODES) → luôn chặn, ưu tiên kiểm tra trước check dữ liệu.
- Mẫu đang dùng ở bất kỳ bảng nào trong 9 bảng → chặn.
- ID không tồn tại / đã xóa mềm → 404.
- **Caveat unique `code`**: cột `code` có unique index; bản ghi xóa mềm vẫn giữ `code` nên không thể tạo lại mẫu mới trùng `code`. Chấp nhận được (mẫu xóa mềm có thể khôi phục bằng cách set lại status nếu cần) — ghi nhận, không xử lý thêm trong scope này.

## Kiểm thử

- Service test:
  - Mẫu thường, không tham chiếu, không protected → xóa mềm OK (`status` về 0, biến mất khỏi list).
  - Mẫu có `code ∈ PROTECTED_CODES` (vd `BIEN_BAN_CUOC_HOP`) → bị chặn `protected`.
  - Mẫu được `decisions.print_template_id` tham chiếu → bị chặn `in_use`.
  - Mẫu được `suspend_labor_contracts.print_template_agreement_id` (cột khác tên) → bị chặn `in_use`.
- List/can_delete test:
  - Trang gồm mẫu thường (chưa dùng), mẫu protected, mẫu đang dùng → trả `can_delete` lần lượt `true/false/false`; số query check không tăng theo số dòng (9 query/trang).

## Scope

- **Trong scope**: migration cột `status`; hằng `PROTECTED_CODES`; precompute `can_delete` ở list (`getUsedTemplateIds` theo lô); service `isPrintTemplateInUse` + `deletePrintTemplate`; controller `delete`; Resource trả `status` + `can_delete`; lọc list theo status; nút Xóa `v-if="item.can_delete"` + xử lý lỗi frontend.
- **Ngoài scope**: chức năng khôi phục mẫu đã xóa mềm; xử lý trùng `code` khi tạo lại; xóa cho hệ `form_templates` (Dự án/Giao việc); kiểm tra permission cho nút xóa; auto-quét code-reference (vẫn dùng danh sách `PROTECTED_CODES` bảo trì thủ công).
