<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes - phan he Danh muc chung
|--------------------------------------------------------------------------
|
| Route nghiep vu cua phan he dat trong group duoi day.
| Controller nam o Modules/MasterData/Http/Controllers/V1.
|
*/

Route::group(['prefix' => '/v1/master-data', 'middleware' => 'auth:api'], function () {
    Route::get('regulation-config/congno', 'V1\RegulationConfigController@showCongno');
    Route::post('regulation-config/congno/versions', 'V1\RegulationConfigController@store');
    Route::put('regulation-config/congno/versions/{id}', 'V1\RegulationConfigController@update');
    Route::delete('regulation-config/congno/versions/{id}', 'V1\RegulationConfigController@cancel');
});
