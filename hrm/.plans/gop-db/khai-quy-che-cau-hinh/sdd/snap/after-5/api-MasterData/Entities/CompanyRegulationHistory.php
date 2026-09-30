<?php

namespace Modules\MasterData\Entities;

use Illuminate\Database\Eloquent\Model;

class CompanyRegulationHistory extends Model
{
    protected $table = 'company_regulation_histories';

    protected $fillable = [
        'company_id', 'created_by', 'field_name', 'name', 'value_before', 'value_after',
    ];

    public $timestamps = true;
}
