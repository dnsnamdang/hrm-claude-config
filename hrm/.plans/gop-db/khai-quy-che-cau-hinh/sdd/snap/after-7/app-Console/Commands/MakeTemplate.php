<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Str;

class MakeTemplate extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'crud:make-template {module} {obj}
                                                        {--a}
                                                        {--c}
                                                        {--rs}
                                                        {--s}
                                                        {--ro}
                                                        {--rq}
                                                        {--tran}
                                                        {--cr}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    protected $moduleName;

    protected $objName;

    protected $nameSingular;

    protected $namePlural;

    protected $namePluralLowerCase;

    protected $nameSingularLowerCase;

    protected $modulePrefix;

    protected $renderAll;

    protected $renderController;

    protected $renderRepository;

    protected $renderService;

    protected $renderRoute;

    protected $renderRequest;

    protected $renderTransformer;

    protected $renderCriteria;


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
        $this->moduleName = $this->argument('module');
        $this->objName = $this->argument('obj');
        $this->nameSingular = Str::singular($this->objName);
        $this->namePlural = Str::plural($this->objName);
        $this->nameSingularLowerCase = Str::lower($this->nameSingular);
        $this->namePluralLowerCase = Str::plural($this->nameSingularLowerCase);
        $this->modulePrefix = 'Modules/'.$this->moduleName;

        $this->renderAll = $this->option('a');

        $this->renderController = $this->option('c');

        $this->renderRepository = $this->option('rs');

        $this->renderService = $this->option('s');

        $this->renderRoute = $this->option('ro');

        $this->renderRequest = $this->option('rq');

        $this->renderTransformer = $this->option('tran');

        $this->renderCriteria = $this->option('cr');


        // repository
        if($this->renderAll || $this->renderRepository) {
            $this->repository();
        }

        // service
        if($this->renderAll || $this->renderService) {
            $this->service();
        }

        // transformers
        if($this->renderAll || $this->renderTransformer) {
            $this->transformers();
        }

        // api request
        if ($this->renderAll || $this->renderRequest) {
            $this->apiRequest();
        }

        // controllers
        if($this->renderAll || $this->renderController) {
            $this->apiController();
        }
        if($this->renderAll || $this->renderRoute) {
            $this->routes();
        }

        if($this->renderAll || $this->renderCriteria) {
            $this->criteria();
        }

    }

    protected function getStub($type)
    {
        return file_get_contents(resource_path("stubs/$type.stub"));
    }

    protected function repository()
    {
        $entityTemplate = $this->getTemplateContent('Entity');
        file_put_contents(base_path("$this->modulePrefix/Entities/" . $this->objName . ".php"), $entityTemplate);

        $path_folder_repository = "$this->modulePrefix/Repositories/";
        if(!file_exists($path_folder_repository)) {
            mkdir($path_folder_repository);
        }

        $repositoryTemplate = $template = $this->getTemplateContent('Repository');
        file_put_contents(base_path($path_folder_repository . $this->objName . "Repository.php"), $repositoryTemplate);
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
        $path_folder_transformers = "$this->modulePrefix/Transformers/";
        if(!file_exists($path_folder_transformers)) {
            mkdir($path_folder_transformers);
        }
        $template = $this->getTemplateContent('transformers');
        file_put_contents(base_path($path_folder_transformers. $this->objName . "Transformer.php"), $template);
    }


    protected function apiRequest()
    {
        $template = $this->getTemplateContent('apiCreateRequest');
        file_put_contents(base_path("$this->modulePrefix/Http/Requests/" . $this->objName . "CreateApiRequest.php"), $template);

        $template = $this->getTemplateContent('apiUpdateRequest');
        file_put_contents(base_path("$this->modulePrefix/Http/Requests/" . $this->objName . "UpdateApiRequest.php"), $template);
    }

    protected function apiController()
    {
        $path_folder_api = "$this->modulePrefix/Http/Controllers/Api/";
        if(!file_exists($path_folder_api)) {
            mkdir($path_folder_api);
        }

        $controllerTemplate = $this->getTemplateContent('apiController');
        file_put_contents(base_path($path_folder_api . $this->objName . "Controller.php"), $controllerTemplate);
    }

    protected function routes()
    {
        $path_folder_route = "$this->modulePrefix/Routes/". $this->nameSingular;
        if(!file_exists($path_folder_route)) {
            mkdir($path_folder_route);
        }

        $routeTemplate = $this->getTemplateContent('route');
        file_put_contents(base_path($path_folder_route . '/api.php'), $routeTemplate);

        $txt = "require(base_path().'/$path_folder_route/api.php');";

        $targetFile = base_path("$this->modulePrefix/Routes/api.php");

        file_put_contents($targetFile, $txt.PHP_EOL , FILE_APPEND | LOCK_EX);
    }

    protected function criteria()
    {
        $path_folder_criteria = "$this->modulePrefix/Repositories/Criteria/";
        if(!file_exists($path_folder_criteria)) {
            mkdir($path_folder_criteria);
        }

        $criteria = $this->getTemplateContent('criteria');
        file_put_contents(base_path($path_folder_criteria .$this->nameSingular.'Criteria.php'), $criteria);
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
                $this->namePlural,
                $this->namePluralLowerCase,
                $this->nameSingularLowerCase
            ],
            $this->getStub($templateName)
        );
    }


}
