<?php

namespace Modules\MasterData\Services;

use App\Models\Company;
use Modules\MasterData\Entities\RegulationScheduledVersion;

class RegulationConfigService
{
    const SCOPE_COMPANY = 'company';
    const TAB_CONGNO = 'congno';

    /** Metadata 7 field tab Công nợ — thứ tự cố định. */
    const CONGNO_FIELDS = [
        'limit_export_debt_employee' => ['label' => 'Hạn mức công nợ xuất hàng NV',       'unit' => 'đồng', 'type' => 'integer'],
        'adjust_odd_balance'         => ['label' => 'Số dư lẻ tối đa cho phép điều chỉnh', 'unit' => 'đồng', 'type' => 'integer'],
        'overdue_date_max_customer'  => ['label' => 'Số ngày quá hạn tính lãi (Bán lẻ)',   'unit' => 'ngày', 'type' => 'integer'],
        'overdue_date_max_agency'    => ['label' => 'Số ngày quá hạn tính lãi (Đại lý)',    'unit' => 'ngày', 'type' => 'integer'],
        'overdue_date_max_service'   => ['label' => 'Số ngày quá hạn tính lãi (Dịch vụ)',   'unit' => 'ngày', 'type' => 'integer'],
        'warning_due_date'           => ['label' => 'Thời gian cảnh báo thu nợ đến hạn',    'unit' => 'ngày', 'type' => 'integer'],
        'interest_rate'              => ['label' => 'Lãi suất',                             'unit' => '%',    'type' => 'decimal'],
    ];

    private function castValue($value, string $type)
    {
        if ($value === null) {
            return null;
        }
        return $type === 'decimal' ? (float) $value : (int) $value;
    }

    public function getCurrentCongnoValues(int $companyId): array
    {
        $company = Company::findOrFail($companyId);
        $values = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $values[$key] = $this->castValue($company->{$key}, $meta['type']);
        }
        return $values;
    }

    public function getCongnoConfig(int $companyId): array
    {
        $current = $this->getCurrentCongnoValues($companyId);

        $fields = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $fields[] = [
                'key' => $key,
                'label' => $meta['label'],
                'unit' => $meta['unit'],
                'type' => $meta['type'],
                'value' => $current[$key],
            ];
        }

        $applied = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->applied()
            ->orderByDesc('effective_date')->orderByDesc('id')
            ->first();

        $appliedVersion = $applied ? [
            'effective_date' => optional($applied->effective_date)->toDateString(),
            'created_by' => $applied->created_by,
            'created_by_name' => $applied->employee_create_name,
            'note' => $applied->note,
        ] : null;

        $pending = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->pending()
            ->orderBy('effective_date')->orderBy('id')
            ->get()
            ->map(function ($v) {
                return [
                    'id' => $v->id,
                    'effective_date' => optional($v->effective_date)->toDateString(),
                    'created_by_name' => $v->employee_create_name,
                    'note' => $v->note,
                    'diff_snapshot' => $v->diff_snapshot ?? [],
                ];
            })->values()->toArray();

        return [
            'fields' => $fields,
            'applied_version' => $appliedVersion,
            'pending' => $pending,
        ];
    }
}
