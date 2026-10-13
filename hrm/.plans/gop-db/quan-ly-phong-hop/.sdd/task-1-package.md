# Review package — Task 1 (worktree phong-hop-api, KHÔNG commit)

## git status
 M modules_statuses.json
?? Modules/Meeting/

## diff file đã theo dõi
diff --git a/modules_statuses.json b/modules_statuses.json
index 0215290c2..fc500c704 100644
--- a/modules_statuses.json
+++ b/modules_statuses.json
@@ -25,5 +25,6 @@
     "Warehouse": true,
     "Transport": true,
     "CustomerCare": true,
-    "Finance": true
+    "Finance": true,
+    "Meeting": true
 }

## Cây thư mục Modules/Meeting
Modules/Meeting/Config/.gitkeep
Modules/Meeting/Config/config.php
Modules/Meeting/Console/.gitkeep
Modules/Meeting/Database/Migrations/.gitkeep
Modules/Meeting/Database/Seeders/.gitkeep
Modules/Meeting/Database/Seeders/MeetingDatabaseSeeder.php
Modules/Meeting/Database/factories/.gitkeep
Modules/Meeting/Entities/.gitkeep
Modules/Meeting/Http/Controllers/.gitkeep
Modules/Meeting/Http/Controllers/MeetingController.php
Modules/Meeting/Http/Middleware/.gitkeep
Modules/Meeting/Http/Requests/.gitkeep
Modules/Meeting/Providers/.gitkeep
Modules/Meeting/Providers/MeetingServiceProvider.php
Modules/Meeting/Providers/RouteServiceProvider.php
Modules/Meeting/Resources/lang/.gitkeep
Modules/Meeting/Routes/.gitkeep
Modules/Meeting/Routes/api.php
Modules/Meeting/Routes/web.php
Modules/Meeting/Tests/Feature/.gitkeep
Modules/Meeting/Tests/Unit/.gitkeep
Modules/Meeting/composer.json
Modules/Meeting/module.json

## Nội dung các file chính

### Modules/Meeting/module.json
```
{
    "name": "Meeting",
    "alias": "meeting",
    "description": "",
    "keywords": [],
    "priority": 0,
    "providers": [
        "Modules\\Meeting\\Providers\\MeetingServiceProvider"
    ],
    "aliases": {},
    "files": [],
    "requires": []
}
```

### Modules/Meeting/composer.json
```
{
    "name": "nwidart/meeting",
    "description": "",
    "authors": [
        {
            "name": "Nicolas Widart",
            "email": "n.widart@gmail.com"
        }
    ],
    "extra": {
        "laravel": {
            "providers": [],
            "aliases": {

            }
        }
    },
    "autoload": {
        "psr-4": {
            "Modules\\Meeting\\": ""
        }
    }
}
```

### Modules/Meeting/Routes/api.php
```
<?php

use Illuminate\Support\Facades\Route;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Danh mục tiện nghi phòng họp + danh mục phòng họp khai ở Task 5, Task 6
});
```

### Modules/Meeting/Providers/MeetingServiceProvider.php
```
<?php

namespace Modules\Meeting\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Eloquent\Factory;

class MeetingServiceProvider extends ServiceProvider
{
    /**
     * @var string $moduleName
     */
    protected $moduleName = 'Meeting';

    /**
     * @var string $moduleNameLower
     */
    protected $moduleNameLower = 'meeting';

    /**
     * Boot the application events.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerTranslations();
        $this->registerConfig();
        $this->registerViews();
        $this->loadMigrationsFrom(module_path($this->moduleName, 'Database/Migrations'));
    }

    /**
     * Register the service provider.
     *
     * @return void
     */
    public function register()
    {
        $this->app->register(RouteServiceProvider::class);
    }

    /**
     * Register config.
     *
     * @return void
     */
    protected function registerConfig()
    {
        $this->publishes([
            module_path($this->moduleName, 'Config/config.php') => config_path($this->moduleNameLower . '.php'),
        ], 'config');
        $this->mergeConfigFrom(
            module_path($this->moduleName, 'Config/config.php'), $this->moduleNameLower
        );
    }

    /**
     * Register views.
     *
     * @return void
     */
    public function registerViews()
    {
        $viewPath = resource_path('views/modules/' . $this->moduleNameLower);

        $sourcePath = module_path($this->moduleName, 'Resources/views');

        $this->publishes([
            $sourcePath => $viewPath
        ], ['views', $this->moduleNameLower . '-module-views']);

        $this->loadViewsFrom(array_merge($this->getPublishableViewPaths(), [$sourcePath]), $this->moduleNameLower);
    }

    /**
     * Register translations.
     *
     * @return void
     */
    public function registerTranslations()
    {
        $langPath = resource_path('lang/modules/' . $this->moduleNameLower);

        if (is_dir($langPath)) {
            $this->loadTranslationsFrom($langPath, $this->moduleNameLower);
        } else {
            $this->loadTranslationsFrom(module_path($this->moduleName, 'Resources/lang'), $this->moduleNameLower);
        }
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array
     */
    public function provides()
    {
        return [];
    }

    private function getPublishableViewPaths(): array
    {
        $paths = [];
        foreach (\Config::get('view.paths') as $path) {
            if (is_dir($path . '/modules/' . $this->moduleNameLower)) {
                $paths[] = $path . '/modules/' . $this->moduleNameLower;
            }
        }
        return $paths;
    }
}
```

### Modules/Meeting/Providers/RouteServiceProvider.php
```
<?php

namespace Modules\Meeting\Providers;

use Illuminate\Support\Facades\Route;
use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;

class RouteServiceProvider extends ServiceProvider
{
    /**
     * The module namespace to assume when generating URLs to actions.
     *
     * @var string
     */
    protected $moduleNamespace = 'Modules\Meeting\Http\Controllers';

    /**
     * Called before routes are registered.
     *
     * Register any model bindings or pattern based filters.
     *
     * @return void
     */
    public function boot()
    {
        parent::boot();
    }

    /**
     * Define the routes for the application.
     *
     * @return void
     */
    public function map()
    {
        $this->mapApiRoutes();

        $this->mapWebRoutes();
    }

    /**
     * Define the "web" routes for the application.
     *
     * These routes all receive session state, CSRF protection, etc.
     *
     * @return void
     */
    protected function mapWebRoutes()
    {
        Route::middleware('web')
            ->namespace($this->moduleNamespace)
            ->group(module_path('Meeting', '/Routes/web.php'));
    }

    /**
     * Define the "api" routes for the application.
     *
     * These routes are typically stateless.
     *
     * @return void
     */
    protected function mapApiRoutes()
    {
        Route::prefix('api')
            ->middleware('api')
            ->namespace($this->moduleNamespace)
            ->group(module_path('Meeting', '/Routes/api.php'));
    }
}
```
