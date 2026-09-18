<?php

namespace Modules\MasterData\Http\Controllers\V1;

use App\Http\Controllers\Api\Traits\ResponseTrait;
use Illuminate\Routing\Controller;
use Illuminate\Http\Request;
use Modules\MasterData\Entities\RegulationScheduledVersion;
use Modules\MasterData\Http\Requests\ScheduleRegulationVersionRequest;
use Modules\MasterData\Services\RegulationConfigService;

class RegulationConfigController extends Controller
{
    use ResponseTrait;

    // Quyền đã xác định ở Task 6 Step 1 — quyền sẵn có "Cài đặt cấu hình" (seeder id 149, group "Cấu hình").
    const PERM_EDIT = 'Cài đặt cấu hình';

    private $service;

    public function __construct(RegulationConfigService $service)
    {
        $this->service = $service;
    }

    private function guard()
    {
        if (!$this->isCurrentEmployeeHasPermission(self::PERM_EDIT)) {
            abort(403, 'Bạn không có quyền thao tác cấu hình quy chế');
        }
    }

    private function currentCompanyId(): int
    {
        // Suy công ty từ nhân viên đăng nhập (fail-closed) — KHÔNG tin company_id client gửi lên,
        // tránh đọc/sửa/huỷ cấu hình + version của công ty khác. current_company_role = công ty NV
        // đang thao tác (employee_infos.company_role, fallback company_id).
        $companyId = (int) optional(auth()->user())->current_company_role;
        // Fail-closed: NV thiếu công ty trong hồ sơ → chặn ngay, không cho rơi về công ty id=0
        // (tránh ghi bản ghi mồ côi scope_id=0 ở store).
        abort_unless($companyId > 0, 422, 'Tài khoản chưa gắn công ty, không thể thao tác cấu hình quy chế');

        return $companyId;
    }

    public function showCongno(Request $request)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $config = $this->service->getCongnoConfig($companyId);
        return $this->responseSuccessJson('OK', 200, $config);
    }

    public function store(ScheduleRegulationVersionRequest $request)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $data = $request->validated();
        $version = $this->service->createCongnoVersion(
            $companyId, $data['effective_date'], $data['values'],
            $data['note'] ?? null, auth()->id()
        );
        return $this->responseSuccessJson('Đã lưu phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }

    public function update(ScheduleRegulationVersionRequest $request, $id)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $version = RegulationScheduledVersion::findOrFail($id);
        abort_unless((int) $version->scope_id === $companyId, 403, 'Không thể thao tác phiên bản của công ty khác');

        $data = $request->validated();
        $version = $this->service->updateCongnoVersion(
            (int) $id, $data['effective_date'], $data['values'], $data['note'] ?? null
        );
        return $this->responseSuccessJson('Đã cập nhật phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }

    public function cancel($id)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $version = RegulationScheduledVersion::findOrFail($id);
        abort_unless((int) $version->scope_id === $companyId, 403, 'Không thể thao tác phiên bản của công ty khác');

        $this->service->cancelCongnoVersion((int) $id);
        return $this->responseSuccessJson('Đã huỷ phiên bản', 200, [
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }
}
