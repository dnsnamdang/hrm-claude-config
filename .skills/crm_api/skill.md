---
name: CRM sync pattern (Mate API)
description: Convention viết service đồng bộ dữ liệu HRM sang CRM (Mate) — create truyền crm_id/crm_model/module_code để CRM tự tạo mapping; update chỉ truyền ids (CRM id) + values; delete dùng active=false
type: project
---

Khi viết service `Modules\CRM\Services\CRMServices\CRM*Service` đồng bộ entity HRM sang CRM (Mate), tuân theo pattern dưới đây. Tham khảo các service mẫu trong cùng thư mục: `CRMBankService`, `CRMDepartmentService`, `CRMEmployeeService`, `CRMCompanyService`, `CRMWorkingPositionService`, `CRMEmployeeInfoService`.

**Why:** Phía CRM (Mate) tự tạo mapping (`crm_id` ↔ `hrm_id`) khi nhận đủ 3 trường `crm_id`, `crm_model`, `module_code` trong payload create. HRM KHÔNG cần gọi thêm API tạo mapping riêng. Khi update/delete, chỉ cần `ids` (CRM id) tra cứu từ bảng `ModuleMapping`.

**How to apply:**

## 1. Khung service

```php
namespace Modules\CRM\Services\CRMServices;

use GuzzleHttp\Exception\RequestException;
use Illuminate\Support\Facades\Log;
use Modules\CRM\Services\Auth\MateAuthService;
use Modules\CRM\Entities\ModuleMapping;
use Modules\Human\Entities\<Entity>;

class CRM<Entity>Service
{
    protected $authService;

    public function __construct(MateAuthService $authService)
    {
        $this->authService = $authService;
    }
    // create<Entity> / update<Entity> / delete<Entity>
}
```

Lấy config + token:
```php
$client     = new \GuzzleHttp\Client();
$mateConfig = $this->authService->getConfig();
$dbName     = $mateConfig['db_name'] ?? null;
$token      = $this->authService->getAccessToken();
$url        = $mateConfig['base_url'] . '/create/<mate.model>'; // hoặc /write/<mate.model>
```

## 2. Create — `POST {base_url}/create/<mate.model>`

Multipart body:
- `db` = `$dbName`
- `values` = `json_encode([...])` gồm:
  - Các field entity (vd `name`, `code`, `company_id`, ...)
  - `crm_id` = `$data['local_id']` (ID bên HRM — controller phải truyền `local_id` = `$model->id` sau khi `save()`)
  - `crm_model` = `<Entity>::class` (FQCN của model HRM, vd `Modules\Human\Entities\Bank::class`)
  - `module_code` = `"HRM"` (cố định)

KHÔNG gọi thêm endpoint tạo id.mapping — CRM tự tạo mapping từ 3 trường trên sau khi create thành công.

## 3. Update — `PUT {base_url}/write/<mate.model>`

- Lookup CRM id từ bảng mapping:
  ```php
  $moduleMapping = ModuleMapping::where('hrm_model', <Entity>::class)
      ->where('hrm_id', $id)
      ->first();
  if (!$moduleMapping || !$moduleMapping->crm_id) {
      Log::warning("Không tìm thấy mapping cho <entity> ID: {$id}");
      return null;
  }
  $crmId = $moduleMapping->crm_id;
  ```
- Filter bỏ field null/rỗng để không ghi đè sai:
  ```php
  $updateData = array_filter($data, fn($v) => $v !== null && $v !== '');
  if (empty($updateData)) {
      Log::warning("Không có trường nào để cập nhật cho <entity> ID: {$id}, CRM ID: {$crmId}");
      return true;
  }
  ```
- Multipart body:
  - `db` = `$dbName`
  - `ids` = `$crmId` (CHỈ CRM id, KHÔNG gửi `crm_model`/`module_code`)
  - `values` = `json_encode($updateData)`

## 4. Delete — soft-delete qua `/write/<mate.model>` với `active=false`

- Lookup CRM id tương tự update (từ `ModuleMapping`).
- Multipart body:
  - `db` = `$dbName`
  - `ids` = `$crmId`
  - `values` = `json_encode(['active' => false])`

KHÔNG dùng endpoint `/delete/...` — Mate xử lý xóa mềm qua `active`.

## 5. Quy tắc chung (create/update/delete)

- Headers mặc định:
  ```php
  'Authorization' => 'Bearer ' . $token,
  'Accept'        => 'application/json',
  ```
- Retry 401: trong `catch (RequestException $e)`, nếu `$e->getCode() == 401` thì gọi `$this->authService->refreshToken()` rồi `return $this-><method>(...same args...)` (retry đúng 1 lần — lần sau nếu vẫn 401 sẽ rơi vào nhánh throw).
- Log qua `Log::...` (chưa chuẩn hóa channel riêng — dùng default):
  - `Log::info('data', $data)` trước khi gửi (create).
  - `Log::info("Kết quả <hành động> <entity>: " . json_encode($result))` sau response thành công.
  - `Log::error('Lỗi ... ở API CRM (HTTP Error): ' . $e->getMessage(), [...])` kèm `request_url`, `status_code`, `response_body`.
- Throw lại exception sau khi log (trừ nhánh 401 đã retry).
- Trả về `json_decode($response->getBody(), true)`.

## 6. Controller gọi service

- Gọi service SAU `DB::commit()` — tránh rollback DB nhưng data đã lên CRM.
- Bọc try/catch riêng hoặc dispatch job để không fail flow chính nếu CRM lỗi (tùy nghiệp vụ — hỏi trước khi quyết).
- Create: truyền `['name' => ..., ..., 'local_id' => $model->id]`.
- Update: truyền `($id, ['name' => ..., ...])` — chỉ các field cần cập nhật.
- Delete: truyền `$id` (HRM id) — service tự lookup CRM id.

## 7. Checklist khi thêm entity mới

- [ ] Model HRM đã có và đã migrate.
- [ ] Biết `<mate.model>` phía CRM (hỏi team Mate nếu chưa rõ).
- [ ] Tạo `CRM<Entity>Service` theo khung trên.
- [ ] Register service vào `Modules\CRM\Providers\CRMServiceProvider` hoặc `ExternalApiServiceProvider` nếu cần inject qua interface.
- [ ] Controller bên HRM gọi service đúng 3 điểm: sau `store()`, sau `update()`, trong `destroy()` (nếu có soft-delete).
- [ ] Kiểm tra bảng `ModuleMapping` sau khi create lần đầu để xác nhận mapping đã được CRM tạo.
