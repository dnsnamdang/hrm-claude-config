<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateRegulationScheduledVersionsTable extends Migration
{
    public function up()
    {
        if (Schema::hasTable('regulation_scheduled_versions')) {
            return;
        }
        Schema::create('regulation_scheduled_versions', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('scope_type', 20);            // company | department | part
            $table->unsignedBigInteger('scope_id');
            $table->string('tab_key', 50);               // congno, baogia, ...
            $table->date('effective_date');
            $table->string('status', 20)->default('pending'); // pending | applied | canceled
            $table->json('payload');                     // toàn bộ giá trị mới của tab (nguồn chân lý)
            $table->json('diff_snapshot')->nullable();   // [{key,label,old,new,unit}] chỉ để hiển thị
            $table->string('note', 500)->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
            $table->timestamp('applied_at')->nullable();
            $table->index(
                ['scope_type', 'scope_id', 'tab_key', 'status', 'effective_date'],
                'rsv_scope_tab_status_date_idx'
            );
        });
    }

    public function down()
    {
        Schema::dropIfExists('regulation_scheduled_versions');
    }
}
