<?php

namespace Modules\MasterData\Entities;

use App\Models\BaseModel;

class RegulationScheduledVersion extends BaseModel
{
    protected $table = 'regulation_scheduled_versions';

    protected $fillable = [
        'scope_type', 'scope_id', 'tab_key', 'effective_date',
        'status', 'payload', 'diff_snapshot', 'note', 'applied_at',
    ];

    protected $casts = [
        'payload' => 'array',
        'diff_snapshot' => 'array',
        'effective_date' => 'date',
        'applied_at' => 'datetime',
    ];

    const STATUS_PENDING = 'pending';
    const STATUS_APPLIED = 'applied';
    const STATUS_CANCELED = 'canceled';

    public function scopePending($q) { return $q->where('status', self::STATUS_PENDING); }
    public function scopeApplied($q) { return $q->where('status', self::STATUS_APPLIED); }

    public function scopeFor($q, $scopeType, $scopeId, $tabKey)
    {
        return $q->where('scope_type', $scopeType)
                 ->where('scope_id', $scopeId)
                 ->where('tab_key', $tabKey);
    }
}
