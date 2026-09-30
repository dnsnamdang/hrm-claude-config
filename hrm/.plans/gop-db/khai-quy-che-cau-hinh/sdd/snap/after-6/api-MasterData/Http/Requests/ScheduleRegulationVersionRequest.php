<?php

namespace Modules\MasterData\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ScheduleRegulationVersionRequest extends FormRequest
{
    public function authorize()
    {
        return true; // gate ở controller bằng isCurrentEmployeeHasPermission
    }

    public function rules()
    {
        return [
            'company_id' => 'required|integer',
            'effective_date' => 'required|date',
            'note' => 'nullable|string|max:500',
            'values' => 'required|array',
            'values.limit_export_debt_employee' => 'required|integer|min:0',
            'values.adjust_odd_balance' => 'required|integer|min:0',
            'values.overdue_date_max_customer' => 'required|integer|min:0',
            'values.overdue_date_max_agency' => 'required|integer|min:0',
            'values.overdue_date_max_service' => 'required|integer|min:0',
            'values.warning_due_date' => 'nullable|integer|min:0',
            'values.interest_rate' => 'required|numeric|min:0',
        ];
    }

    public function messages()
    {
        return [
            'required' => 'Bắt buộc phải nhập',
            'integer' => 'Chỉ cho phép nhập số nguyên',
            'numeric' => 'Chỉ cho phép nhập số',
            'min' => 'Giá trị không được nhỏ hơn :min',
            'date' => 'Ngày không hợp lệ',
        ];
    }
}
