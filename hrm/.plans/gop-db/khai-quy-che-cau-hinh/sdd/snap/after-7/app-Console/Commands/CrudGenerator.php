<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Str;

class CrudGenerator extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'crud:generator {name : Class (singular) for example User}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create CRUD operations (Module + Api)';

    protected $moduleName;
    protected $objName;
    protected $moduleNamePlural;
    protected $moduleNamePluralLowerCase;
    protected $moduleNameSingularLowerCase;
    protected $modulePrefix;

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->moduleName = $this->argument('name');
        $this->objName = $this->moduleName;
        $this->moduleNamePlural = $this->moduleName;
        $this->moduleNamePluralLowerCase = strtolower($this->moduleName);
        $this->moduleNameSingularLowerCase = strtolower($this->moduleName);
        $this->modulePrefix = "Modules/$this->moduleNamePlural";

        // create new module
        Artisan::call("module:make $this->moduleNamePlural", []);

        // migrate module table
        Artisan::call("module:make-migration create_" . $this->moduleNamePluralLowerCase . "_table $this->moduleNamePlural", []);

        $this->config();

        // repository
        $this->repository();

        // repository
        $this->service();

        // transformers
        $this->transformers();

        // api request
        $this->apiRequest();

        // controllers
        $this->apiController();

        $this->routes();

    }

    protected function getStub($type)
    {
        return file_get_contents(resource_path("stubs/$type.stub"));
    }

    protected function config()
    {
        $template = $this->getTemplateContent('config');
        file_put_contents(base_path("$this->modulePrefix/Config/config.php"), $template);
    }

    protected function repository()
    {
        $entityTemplate = $this->getTemplateContent('Entity');
        file_put_contents(base_path("$this->modulePrefix/Entities/" . $this->moduleName . ".php"), $entityTemplate);

        mkdir("$this->modulePrefix/Repositories/");
        $repositoryTemplate = $template = $this->getTemplateContent('Repository');
        file_put_contents(base_path("$this->modulePrefix/Repositories/" . $this->moduleName . "Repository.php"), $repositoryTemplate);
    }

    protected function service()
    {
        $path_folder_service = $this->modulePrefix . '/Services/';
        if(!file_exists($path_folder_service)) {
            mkdir($path_folder_service);
        }

        $template = $this->getTemplateContent('service');
        file_put_contents(base_path($path_folder_service . $this->objName . "Service.php"), $template);
    }

    protected function transformers()
    {
        mkdir("$this->modulePrefix/Transformers/");
        $template = $this->getTemplateContent('transformers');
        file_put_contents(base_path("$this->modulePrefix/Transformers/". $this->moduleName . "Transformer.php"), $template);
    }


    protected function apiRequest()
    {
        $template = $this->getTemplateContent('apiCreateRequest');
        file_put_contents(base_path("$this->modulePrefix/Http/Requests/" . $this->moduleName . "CreateApiRequest.php"), $template);

        $template = $this->getTemplateContent('apiUpdateRequest');
        file_put_contents(base_path("$this->modulePrefix/Http/Requests/" . $this->moduleName . "UpdateApiRequest.php"), $template);
    }

    protected function apiController()
    {
        mkdir("$this->modulePrefix/Http/Controllers/Api/");
        $controllerTemplate = $this->getTemplateContent('apiController');
        file_put_contents(base_path("$this->modulePrefix/Http/Controllers/Api/" . $this->moduleNamePlural . "Controller.php"), $controllerTemplate);
    }

    protected function routes()
    {
        $routeTemplate = $this->getTemplateContent('route');
        file_put_contents(base_path("$this->modulePrefix/Routes/api.php"), $routeTemplate);

        $template = $this->getTemplateContent('routeServiceProvider');
        file_put_contents(base_path("$this->modulePrefix/Providers/RouteServiceProvider.php"), $template);
    }

    protected function getTemplateContent($templateName)
    {
        return str_replace(
            [
                '{{moduleName}}',
                '{{objName}}',
                '{{moduleNamePlural}}',
                '{{moduleNamePluralLowerCase}}',
                '{{moduleNameSingularLowerCase}}'
            ],
            [
                $this->moduleName,
                $this->objName,
                $this->moduleNamePlural,
                $this->moduleNamePluralLowerCase,
                $this->moduleNameSingularLowerCase
            ],
            $this->getStub($templateName)
        );
    }
}
