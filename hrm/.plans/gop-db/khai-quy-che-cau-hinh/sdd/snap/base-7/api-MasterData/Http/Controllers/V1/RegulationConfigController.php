<?php

namespace Modules\MasterData\Http\Controllers\V1;

use App\Http\Controllers\Api\Traits\ResponseTrait;
use Illuminate\Routing\Controller;
use Illuminate\Http\Request;
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

    public function showCongno(Request $request)
    {
        $this->guard();
        $companyId = (int) $request->query('company_id');
        $config = $this->service->getCongnoConfig($companyId);
        return $this->responseSuccessJson('OK', 200, $config);
    }

    public function store(ScheduleRegulationVersionRequest $request)
    {
        $this->guard();
        $data = $request->validated();
        $version = $this->service->createCongnoVersion(
            (int) $data['company_id'], $data['effective_date'], $data['values'],
            $data['note'] ?? null, auth()->id()
        );
        return $this->responseSuccessJson('Đã lưu phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig((int) $data['company_id']),
        ]);
    }

    public function update(ScheduleRegulationVersionRequest $request, $id)
    {
        $this->guard();
        $data = $request->validated();
        $version = $this->service->updateCongnoVersion(
            (int) $id, $data['effective_date'], $data['values'], $data['note'] ?? null
        );
        return $this->responseSuccessJson('Đã cập nhật phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig((int) $version->scope_id),
        ]);
    }

    public function cancel($id)
    {
        $this->guard();
        $version = \Modules\MasterData\Entities\RegulationScheduledVersion::findOrFail($id);
        $companyId = (int) $version->scope_id;
        $this->service->cancelCongnoVersion((int) $id);
        return $this->responseSuccessJson('Đã huỷ phiên bản', 200, [
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }
}
