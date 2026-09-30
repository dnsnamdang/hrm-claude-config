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

    public function normalizeValues(array $input): array
    {
        $values = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $raw = $input[$key] ?? null;
            $values[$key] = ($raw === null || $raw === '') ? null : $this->castValue($raw, $meta['type']);
        }
        return $values;
    }

    public function buildDiffSnapshot(array $old, array $new): array
    {
        $diffs = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $o = $old[$key] ?? null;
            $n = $new[$key] ?? null;
            if ((string) $o !== (string) $n) {
                $diffs[] = [
                    'key' => $key,
                    'label' => $meta['label'],
                    'old' => $o === null ? null : (string) $o,
                    'new' => $n === null ? null : (string) $n,
                    'unit' => $meta['unit'],
                ];
            }
        }
        return $diffs;
    }

    public function baselineForDate(int $companyId, string $effectiveDate, ?int $excludeVersionId = null): array
    {
        $query = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->pending()
            ->where('effective_date', '<', $effectiveDate)
            ->orderByDesc('effective_date')->orderByDesc('id');

        if ($excludeVersionId !== null) {
            $query->where('id', '!=', $excludeVersionId);
        }

        $prev = $query->first();

        return $prev ? $this->normalizeValues($prev->payload ?? []) : $this->getCurrentCongnoValues($companyId);
    }

    public function createCongnoVersion(int $companyId, string $effectiveDate, array $values, ?string $note, int $actorId): RegulationScheduledVersion
    {
        $payload = $this->normalizeValues($values);
        $version = new RegulationScheduledVersion([
            'scope_type' => self::SCOPE_COMPANY,
            'scope_id' => $companyId,
            'tab_key' => self::TAB_CONGNO,
            'effective_date' => $effectiveDate,
            'status' => RegulationScheduledVersion::STATUS_PENDING,
            'payload' => $payload,
            'diff_snapshot' => [],
            'note' => $note,
        ]);
        $version->created_by = $actorId;
        $version->updated_by = $actorId;
        $version->save();

        $this->recomputeDiffChain($companyId);
        return $version->fresh();
    }

    public function updateCongnoVersion(int $versionId, string $effectiveDate, array $values, ?string $note): RegulationScheduledVersion
    {
        $version = RegulationScheduledVersion::findOrFail($versionId);
        abort_unless($version->status === RegulationScheduledVersion::STATUS_PENDING, 422, 'Chỉ sửa được phiên bản đang chờ áp dụng');

        $version->effective_date = $effectiveDate;
        $version->payload = $this->normalizeValues($values);
        $version->note = $note;
        $version->save();

        $this->recomputeDiffChain((int) $version->scope_id);
        return $version->fresh();
    }

    public function cancelCongnoVersion(int $versionId): void
    {
        $version = RegulationScheduledVersion::findOrFail($versionId);
        abort_unless($version->status === RegulationScheduledVersion::STATUS_PENDING, 422, 'Chỉ huỷ được phiên bản đang chờ áp dụng');

        $companyId = (int) $version->scope_id;
        $version->status = RegulationScheduledVersion::STATUS_CANCELED;
        $version->save();

        $this->recomputeDiffChain($companyId);
    }

    public function recomputeDiffChain(int $companyId): void
    {
        $baseline = $this->getCurrentCongnoValues($companyId);

        $pendings = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->pending()
            ->orderBy('effective_date')->orderBy('id')
            ->get();

        foreach ($pendings as $v) {
            $payload = $this->normalizeValues($v->payload ?? []);
            $v->diff_snapshot = $this->buildDiffSnapshot($baseline, $payload);
            $v->saveQuietly(); // tránh đụng updated_by/log khi chỉ tính lại hiển thị
            $baseline = $payload; // bản sau lấy payload bản trước làm "cũ"
        }
    }
}
