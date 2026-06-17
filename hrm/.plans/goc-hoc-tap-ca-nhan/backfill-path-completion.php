<?php
/**
 * Backfill một lần: set LearningPathEnrollment.status = DONE cho các lộ trình
 * mà MỌI khoá thành phần của user đều đã hoàn thành nhưng status enrollment còn kẹt.
 *
 * Cách chạy (tại thư mục hrm-api):
 *   php artisan tinker
 *   >>> require base_path('../.plans/goc-hoc-tap-ca-nhan/backfill-path-completion.php');
 *
 * Hoặc: php artisan tinker --execute="require '<đường dẫn tuyệt đối tới file này>';"
 *
 * An toàn để chạy lại nhiều lần (idempotent) — chỉ cập nhật bản ghi đủ điều kiện.
 */

use Modules\Training\Entities\LearningPathEnrollment;
use Modules\Training\Entities\LearningPathSubject;
use Modules\Training\Entities\SubjectEnrollment;

$updated = 0;
$checked = 0;

LearningPathEnrollment::where('status', '!=', LearningPathEnrollment::STATUS_DONE)
    ->chunkById(200, function ($rows) use (&$updated, &$checked) {
        foreach ($rows as $pe) {
            $checked++;

            $column = !empty($pe->learner_id)
                ? 'learner_id'
                : (!empty($pe->employee_id) ? 'employee_id' : null);
            if (!$column) {
                continue;
            }
            $ownerId = $pe->$column;

            $subjectIds = LearningPathSubject::where('learning_path_id', $pe->learning_path_id)
                ->pluck('subject_id')
                ->filter()
                ->unique();
            if ($subjectIds->isEmpty()) {
                continue;
            }

            $doneCount = SubjectEnrollment::where($column, $ownerId)
                ->whereIn('subject_id', $subjectIds)
                ->where('status', SubjectEnrollment::STATUS_DONE)
                ->distinct('subject_id')
                ->count('subject_id');

            if ($doneCount >= $subjectIds->count()) {
                $pe->status       = LearningPathEnrollment::STATUS_DONE;
                $pe->completed_at = $pe->completed_at ?: now();
                $pe->save();
                $updated++;
            }
        }
    });

echo "Đã kiểm tra: {$checked} enrollment lộ trình. Cập nhật DONE: {$updated}.\n";
