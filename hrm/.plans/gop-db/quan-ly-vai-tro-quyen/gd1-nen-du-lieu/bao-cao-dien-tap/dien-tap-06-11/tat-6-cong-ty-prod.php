use Illuminate\Support\Facades\DB;
$m = config("auth.providers.employees.model") ?: config("auth.providers.users.model");
auth("api")->login($m::find(13));
echo "nguoi thao tac: " . auth("api")->id() . "\n";
$s = app(\App\Services\Admin\GroupScopeCompanyService::class);
foreach ([2, 3, 4, 7, 8, 9] as $id) { echo $id . ":" . ($s->update($id, false) ? "tat" : "khong doi") . " "; }
echo "\n" . DB::table("companies")->orderBy("id")->get(["id", "allow_group_scope"])->map(function ($c) { return $c->id . ":" . $c->allow_group_scope; })->implode(",") . "\n";
$r = DB::selectOne("select count(*) c, count(distinct rhp.role_id) v from role_has_permissions rhp join roles r on r.id=rhp.role_id join companies c on c.id=r.company_id where rhp.scope=4 and c.allow_group_scope=0");
echo "dong muc 4 bi ha: {$r->c} / vai tro: {$r->v}\n";
\App\Support\Permissions\PermissionChecker::flush(); cache()->forget("spatie.permission.cache");
