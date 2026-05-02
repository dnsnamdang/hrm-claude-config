# Plan — Close Prospective Projects

> **Spec:** [design.md](./design.md)
> **Ngày bắt đầu:** 2026-04-19
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign` (cả API + Client)

**Goal:** NV KD phụ trách đóng dự án tiền khả thi từ `/assign/prospective-projects/:id/manager` — modal chọn lý do + ghi chú + xác nhận → cascade 5 entity sang Đóng + notify người đang dính việc.

---

## Trạng thái tổng

- Brainstorm: Done (2026-04-19, 4 Q&A)
- Design: Done (`design.md`)
- Plan: Done
- Tiến độ: 16/18 tasks

---

## Quy tắc thực thi

1. Không commit/push — user tự quản lý git.
2. Hoàn thành 1 task → đánh `[x]` ngay.
3. Sau mỗi nhóm → smoke test thủ công.
4. FE tuân thủ V2Base + convention Batch 6-8 Phase 12 đã xác định (V2BaseButton boolean props, `:interactable`, toast `$toasted.global.*`).

---

## 1. BE — Migration + Entity constants (3 tasks)

- [x] **Task 1:** Migration `2026_04_19_100004_add_close_fields_to_prospective_projects.php`
  ```php
  public function up() {
      Schema::table('prospective_projects', function (Blueprint $t) {
          $t->unsignedBigInteger('closed_reason_id')->nullable()->after('status')
            ->comment('FK → reason_project_failures.id');
          $t->text('closed_note')->nullable()->after('closed_reason_id');
          $t->timestamp('closed_at')->nullable()->after('closed_note');
          $t->unsignedBigInteger('closed_by')->nullable()->after('closed_at');
      });
  }
  public function down() {
      Schema::table('prospective_projects', function (Blueprint $t) {
          $t->dropColumn(['closed_reason_id', 'closed_note', 'closed_at', 'closed_by']);
      });
  }
  ```
  Chạy `php artisan migrate` + verify 4 cột mới.

- [x] **Task 2:** Thêm status constants vào 3 entity mới:
  - `Modules/Assign/Entities/SolutionModule.php`: `const STATUS_DONG = 10;` + label `'Đóng'` trong `getStatusList()` (nếu có).
  - `Modules/Assign/Entities/PricingRequest.php`: `const STATUS_DONG = 5;` + label + màu xám `#6B7280`.
  - `Modules/Assign/Entities/Quotation.php`: `const STATUS_DONG = 5;` + label trong `getStatusList()` (line 58-66) + màu xám.

- [x] **Task 3:** Smoke test constants:
  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-api && \
  php artisan tinker --execute="\
  echo 'SolutionModule.STATUS_DONG=' . Modules\Assign\Entities\SolutionModule::STATUS_DONG . PHP_EOL;\
  echo 'PricingRequest.STATUS_DONG=' . Modules\Assign\Entities\PricingRequest::STATUS_DONG . PHP_EOL;\
  echo 'Quotation.STATUS_DONG=' . Modules\Assign\Entities\Quotation::STATUS_DONG . PHP_EOL;\
  "
  ```
  Expected 3 dòng output hợp lệ.

---

## 2. BE — Service logic (4 tasks)

- [x] **Task 4:** Verify endpoint `GET /api/v1/assign/reason-project-failures/getAll` (hoặc tương đương).
  - Controller `ReasonProjectFailureController@getAll` + service `ReasonProjectFailureService::getAll` ĐÃ CÓ sẵn (trả active reasons theo `STATUS_ACTIVE=1`).
  - Route thiếu → đã thêm: `GET /api/v1/assign/reason_project_failures/getAll` (prefix dùng underscore theo convention hiện tại của group).
  - Response format: `responseJson('success', 200, Collection<ReasonProjectFailure>)` → `{ message, status, data: [...]}`.

- [x] **Task 5:** Service method `ProspectiveProjectService::closeProject(ProspectiveProject $p, int $reasonId, ?string $note): array`

  File: `Modules/Assign/Services/ProspectiveProjectService.php`

  ```php
  public function closeProject(ProspectiveProject $p, int $reasonId, ?string $note): array
  {
      // Validate creator
      $currentEmployeeId = $this->currentEmployeeId();  // adjust theo pattern hiện có
      if ((int) $p->main_sale_employee_id !== (int) $currentEmployeeId) {
          throw new \Exception('Chỉ NV KD phụ trách mới được đóng dự án.', 403);
      }
      if ((int) $p->status === ProspectiveProject::STATUS_DONG_DU_AN) {
          throw new \Exception('Dự án đã đóng.', 422);
      }
      if (!ReasonProjectFailure::find($reasonId)) {
          throw new \Exception('Nguyên nhân thất bại không hợp lệ.', 422);
      }

      $notifyTargets = [];

      DB::transaction(function () use ($p, $reasonId, $note, &$notifyTargets) {
          // 1. Thu thập notify targets trước khi cascade
          $solutions = Solution::where('prospective_project_id', $p->id)
              ->whereNotIn('status', [Solution::STATUS_DONG])
              ->get();
          $notifyTargets = $this->collectCloseNotifyTargets($solutions, $p->id);

          // 2. Update project
          $p->update([
              'status' => ProspectiveProject::STATUS_DONG_DU_AN,
              'closed_reason_id' => $reasonId,
              'closed_note' => $note,
              'closed_at' => now(),
              'closed_by' => auth()->id(),
          ]);

          // 3. Cascade Solutions
          $solutionIds = $solutions->pluck('id')->toArray();
          Solution::whereIn('id', $solutionIds)->update([
              'status' => Solution::STATUS_DONG,
              'updated_by' => auth()->id(),
          ]);

          // 4. Cascade SolutionModules (của các solution vừa đóng)
          SolutionModule::whereIn('solution_id', $solutionIds)
              ->whereNotIn('status', [SolutionModule::STATUS_DONG])
              ->update([
                  'status' => SolutionModule::STATUS_DONG,
                  'updated_by' => auth()->id(),
              ]);

          // 5. Cascade PricingRequests (status 1/2/3, không đụng 4)
          PricingRequest::where('project_id', $p->id)
              ->whereIn('status', [1, 2, 3])
              ->update([
                  'status' => PricingRequest::STATUS_DONG,
                  'updated_by' => auth()->id(),
              ]);

          // 6. Cascade Quotations (status 1/2/3, không đụng 4) + log history
          $quotationIds = Quotation::where('project_id', $p->id)
              ->whereIn('status', [1, 2, 3])
              ->pluck('id')
              ->toArray();

          Quotation::whereIn('id', $quotationIds)->update([
              'status' => Quotation::STATUS_DONG,
              'updated_by' => auth()->id(),
          ]);

          // Log history cho từng quotation
          foreach ($quotationIds as $qid) {
              $this->logQuotationHistory($qid, 'closed_by_project', [
                  'project_id' => $p->id,
                  'reason_id' => $reasonId,
                  'note' => $note,
              ]);
          }
      });

      // 7. Notify sau commit
      $this->sendCloseNotifications($p, $notifyTargets, $reasonId, $note);

      return [
          'project_id' => $p->id,
          'status' => $p->status,
          'cascade' => [
              'solutions' => count($solutionIds ?? []),
              // ... counts cho các entity khác
          ],
      ];
  }
  ```

  **VERIFY trước khi code:**
  - Method `currentEmployeeId()` có sẵn trong service không? (Pattern Phase 11). Nếu không → dùng `auth()->user()->employee_info_id` + lookup Employee.
  - `logQuotationHistory()` có sẵn không? Reuse từ QuotationService hoặc copy pattern.

- [x] **Task 6:** Helper `collectCloseNotifyTargets($solutions, $projectId): array`

  Trong cùng service:
  ```php
  private function collectCloseNotifyTargets($solutions, int $projectId): array
  {
      $userIds = [];

      // (a) Creator của solutions
      foreach ($solutions as $s) {
          if ($s->created_by) $userIds[] = (int) $s->created_by;
          if (!empty($s->pm_id)) $userIds[] = (int) $s->pm_id;  // adjust tên field PM theo entity
      }

      // (b) NLG đang làm giá (Quotation status 1/2/3)
      $nlgIds = Quotation::where('project_id', $projectId)
          ->whereIn('status', [1, 2, 3])
          ->pluck('created_by')
          ->toArray();
      $userIds = array_merge($userIds, $nlgIds);

      // (c) Nếu có quotation status 2 → notify TP
      $hasStatus2 = Quotation::where('project_id', $projectId)->where('status', 2)->exists();
      if ($hasStatus2) {
          $tpIds = $this->getUsersByPermission('Trưởng phòng duyệt giá Bom giải pháp');
          $userIds = array_merge($userIds, $tpIds);
      }

      // (d) Nếu có quotation status 3 → notify BGĐ
      $hasStatus3 = Quotation::where('project_id', $projectId)->where('status', 3)->exists();
      if ($hasStatus3) {
          $bgdIds = $this->getUsersByPermission('Ban giám đốc duyệt giá Bom giải pháp');
          $userIds = array_merge($userIds, $bgdIds);
      }

      // Dedup + loại creator (để không tự notify mình)
      $userIds = array_unique($userIds);
      $userIds = array_diff($userIds, [auth()->id()]);

      return array_values($userIds);
  }

  private function getUsersByPermission(string $permission): array
  {
      // Pattern đã có ở Phase 11 — copy/reuse. VD:
      return \Spatie\Permission\Models\Permission::where('name', $permission)
          ->first()?->users()->pluck('id')->toArray() ?? [];
  }
  ```

- [x] **Task 7:** Method `sendCloseNotifications($project, $userIds, $reasonId, $note): void`

  ```php
  private function sendCloseNotifications($project, array $userIds, int $reasonId, ?string $note): void
  {
      if (empty($userIds)) return;

      $reason = ReasonProjectFailure::find($reasonId);
      $reasonName = $reason ? $reason->name : 'Không rõ';
      $projectName = $project->name ?? $project->code ?? "dự án #{$project->id}";

      $message = "Dự án \"{$projectName}\" đã được đóng. Lý do: {$reasonName}. " .
                 "Các giải pháp/hạng mục/báo giá liên quan đã chuyển sang trạng thái Đóng.";
      $link = "/assign/prospective-projects/{$project->id}/manager";

      // Dùng helper sendToAllNotification hoặc pattern Phase 11
      foreach ($userIds as $uid) {
          app(\Modules\Human\Services\EmployeeInfoService::class)
              ->sendNotification($uid, [
                  'type' => 'project_closed',
                  'title' => 'Dự án đã đóng',
                  'message' => $message,
                  'link' => $link,
                  'data' => ['project_id' => $project->id, 'reason_id' => $reasonId],
              ]);
      }
  }
  ```

  **VERIFY:** Tên method + signature của `EmployeeInfoService` hiện tại. Nếu khác → adjust.

---

## 3. BE — Controller + Route + Request (3 tasks)

- [x] **Task 8:** FormRequest `ProspectiveProjectCloseRequest.php`

  File: `Modules/Assign/Http/Requests/ProspectiveProject/ProspectiveProjectCloseRequest.php` (theo convention subfolder Phase 11).

  ```php
  <?php
  namespace Modules\Assign\Http\Requests\ProspectiveProject;
  use Illuminate\Foundation\Http\FormRequest;

  class ProspectiveProjectCloseRequest extends FormRequest {
      public function authorize() { return true; }
      public function rules() {
          return [
              'closed_reason_id' => 'required|integer|exists:reason_project_failures,id',
              'closed_note' => 'nullable|string|max:500',
          ];
      }
      public function messages() {
          return [
              'closed_reason_id.required' => 'Vui lòng chọn nguyên nhân',
              'closed_reason_id.exists' => 'Nguyên nhân không hợp lệ',
              'closed_note.max' => 'Ghi chú tối đa 500 ký tự',
          ];
      }
  }
  ```

- [x] **Task 9:** Controller action `close` vào `ProspectiveProjectController`

  File: `Modules/Assign/Http/Controllers/Api/V1/ProspectiveProjectController.php`

  ```php
  use Modules\Assign\Http\Requests\ProspectiveProject\ProspectiveProjectCloseRequest;

  public function close(ProspectiveProjectCloseRequest $request, $id)
  {
      $project = ProspectiveProject::findOrFail($id);
      $result = $this->service->closeProject(
          $project,
          (int) $request->closed_reason_id,
          $request->closed_note
      );
      return response()->json(['data' => $result]);
  }
  ```

- [x] **Task 10:** Route + transformer update

  File: `Modules/Assign/Routes/api.php` — thêm:
  ```php
  Route::post('prospective-projects/{id}/close', [ProspectiveProjectController::class, 'close']);
  ```

  Transformer `DetailProspectiveProjectResource` (hoặc tương đương) — thêm fields:
  ```php
  'closed_reason_id' => $this->closed_reason_id,
  'closed_reason' => $this->closedReason ? [
      'id' => $this->closedReason->id,
      'name' => $this->closedReason->name,
  ] : null,
  'closed_note' => $this->closed_note,
  'closed_at' => $this->closed_at ? $this->closed_at->format('Y-m-d H:i:s') : null,
  'closed_by' => $this->closed_by,
  'closed_by_name' => $this->closedBy?->name,  // adjust relationship
  ```

  ProspectiveProject entity thêm relationship:
  ```php
  public function closedReason() {
      return $this->belongsTo(ReasonProjectFailure::class, 'closed_reason_id');
  }
  public function closedBy() {
      return $this->belongsTo(\Modules\Human\Entities\Employee::class, 'closed_by');
  }
  ```

---

## 4. BE — Smoke test (1 task)

- [x] **Task 11:** Smoke test Postman/tinker:
  - POST `/api/v1/assign/prospective-projects/167/close` với body `{"closed_reason_id": 1, "closed_note": "test"}`.
  - Expected: 200 với cascade counts.
  - Check DB: `prospective_projects.status=11, closed_*` set. Solutions status=2. SolutionModules status=10. PricingRequests + Quotations có row status=5. `quotation_histories` có entry `closed_by_project`.
  - Gọi lần 2: expected 422 "Dự án đã đóng".
  - Gọi với user khác creator: expected 403.

---

## 5. FE — Component mới (2 tasks)

- [x] **Task 12:** Tạo `components/assign/prospective-project/CloseProjectModal.vue`

  ```vue
  <template>
      <b-modal :visible="show" title="Đóng dự án" size="md" hide-footer no-close-on-backdrop @hide="onCancel">
          <div class="alert alert-danger p-3 mb-3">
              <b>⚠ Đóng dự án</b> sẽ huỷ toàn bộ công việc:
              <ul class="mb-0 mt-2 pl-4">
                  <li>Các giải pháp chuyển sang <b>Đóng</b>.</li>
                  <li>Các hạng mục giải pháp chuyển sang <b>Đóng</b>.</li>
                  <li>Các yêu cầu xây dựng giá chuyển sang <b>Đóng</b>.</li>
                  <li>Các báo giá đang soạn/chờ duyệt chuyển sang <b>Đóng</b>.</li>
              </ul>
              <div class="mt-2 font-weight-bold">Hành động này KHÔNG THỂ khôi phục.</div>
          </div>

          <div class="mb-3">
              <V2BaseLabel required>Nguyên nhân thất bại</V2BaseLabel>
              <V2BaseSelect
                  v-model="form.closed_reason_id"
                  :options="reasonOptions"
                  placeholder="-- Chọn nguyên nhân --"
              />
          </div>

          <div class="mb-3">
              <V2BaseLabel>Ghi chú bổ sung</V2BaseLabel>
              <V2BaseTextarea v-model="form.closed_note" rows="3" maxlength="500" placeholder="Tối đa 500 ký tự" />
          </div>

          <div class="mb-3">
              <b-form-checkbox v-model="confirmed">
                  Tôi xác nhận muốn đóng dự án này.
              </b-form-checkbox>
          </div>

          <div class="d-flex justify-content-end">
              <V2BaseButton light class="mr-2" @click="onCancel">Huỷ</V2BaseButton>
              <V2BaseButton
                  status="danger"
                  :interactable="canSubmit"
                  @click="onSubmit"
              >
                  Xác nhận đóng
              </V2BaseButton>
          </div>
      </b-modal>
  </template>

  <script>
  export default {
      name: 'CloseProjectModal',
      props: {
          show: { type: Boolean, default: false },
          projectId: { type: [Number, String], required: true },
      },
      data() {
          return {
              form: { closed_reason_id: null, closed_note: '' },
              confirmed: false,
              reasonOptions: [],
          }
      },
      computed: {
          canSubmit() {
              return !!this.form.closed_reason_id && this.confirmed
          },
      },
      watch: {
          show(v) {
              if (v) {
                  this.reset()
                  this.loadReasons()
              }
          },
      },
      methods: {
          async loadReasons() {
              try {
                  const res = await this.$axios.get('/api/v1/assign/reason-project-failures/getAll')
                  this.reasonOptions = (res?.data?.data || []).map(r => ({
                      value: r.id,
                      text: r.name,
                  }))
              } catch (e) {
                  this.$toasted.global.error({ message: 'Không load được danh mục nguyên nhân' })
              }
          },
          reset() {
              this.form = { closed_reason_id: null, closed_note: '' }
              this.confirmed = false
          },
          async onSubmit() {
              if (!this.canSubmit) return
              try {
                  this.$safeLoadingStart && this.$safeLoadingStart()
                  const res = await this.$axios.post(
                      `/api/v1/assign/prospective-projects/${this.projectId}/close`,
                      this.form
                  )
                  this.$toasted.global.success({ message: 'Đã đóng dự án' })
                  this.$emit('closed', res?.data?.data)
              } catch (e) {
                  const msg = e?.response?.data?.message || 'Đóng dự án thất bại'
                  this.$toasted.global.error({ message: msg })
              } finally {
                  this.$safeLoadingFinish && this.$safeLoadingFinish()
              }
          },
          onCancel() {
              this.$emit('cancel')
          },
      },
  }
  </script>
  ```

- [x] **Task 13:** Smoke SFC compile `CloseProjectModal.vue` — pass 0 errors.

---

## 6. FE — Manager.vue integration + readonly banner (3 tasks)

- [x] **Task 14:** Import + mount `CloseProjectModal` vào `pages/assign/prospective-projects/_id/manager.vue`.

  - Import + register trong `components: {}`.
  - Thêm data: `showCloseModal: false`.
  - Thêm button "Đóng dự án" vào action bar (chỗ có button edit/delete):
    ```html
    <V2BaseButton
        v-if="canCloseProject"
        status="danger"
        size="sm"
        @click="showCloseModal = true"
    >
        <template #prefix>
            <i class="ri-close-circle-line"></i>
        </template>
        Đóng dự án
    </V2BaseButton>
    ```
  - Thêm computed:
    ```js
    canCloseProject() {
        const currentEmployeeId = this.$store.state.current_employee?.id
        return this.project
            && Number(this.project.status) !== 11  // STATUS_DONG_DU_AN
            && Number(this.project.main_sale_employee_id) === Number(currentEmployeeId)
    },
    ```
  - Mount modal cuối template:
    ```html
    <CloseProjectModal
        :show="showCloseModal"
        :project-id="$route.params.id"
        @closed="onProjectClosed"
        @cancel="showCloseModal = false"
    />
    ```
  - Handler:
    ```js
    onProjectClosed() {
        this.showCloseModal = false
        this.fetchProspectiveProjects()  // reload project detail để hiện banner + disable
    },
    ```

- [x] **Task 15:** Thêm banner đỏ post-close vào `manager.vue`.

  Vị trí: đầu trang, ngay sau header.
  ```html
  <div v-if="project && Number(project.status) === 11" class="alert alert-danger mb-3">
      <div class="d-flex align-items-start">
          <i class="ri-close-circle-line mr-2" style="font-size: 20px"></i>
          <div class="flex-grow-1">
              <h5 class="mb-1">Dự án đã đóng</h5>
              <div><b>Lý do:</b> {{ project.closed_reason?.name || '—' }}</div>
              <div v-if="project.closed_note"><b>Ghi chú:</b> {{ project.closed_note }}</div>
              <div class="text-muted mt-1">
                  Đóng ngày {{ project.closed_at }} bởi {{ project.closed_by_name || '—' }}
              </div>
          </div>
      </div>
  </div>
  ```

- [x] **Task 16:** Ẩn các action button khác khi đã đóng.

  Grep trong manager.vue các button hành động (Sửa, Xoá, Tạo YCBG, Tạo hồ sơ, v.v.). Thêm condition `v-if="Number(project.status) !== 11"` vào mỗi button, hoặc wrap trong `<template v-if="!isClosed">` với computed `isClosed`.

---

## 7. FE — Readonly trên các entity cascade (1 task — optional polish)

- [ ] **Task 17:** Thêm check readonly trên quotation edit + solution edit khi status=Đóng.

  **quotations/_id/edit.vue:** nếu `Number(item.status) === 5` → redirect về show, hoặc hiển thị banner + disable tất cả input.

  **solutions/_id/edit.vue:** nếu `Number(item.status) === 2 (STATUS_DONG)` → readonly + banner.

  (Optional — nếu không làm ngay, báo giá/giải pháp đóng vẫn lock qua BE validate ở save, nhưng FE nên feedback sớm hơn.)

---

## 8. Test thủ công end-to-end (1 task)

- [ ] **Task 18:** Test 8 scenario:
  - [ ] Mở manager dự án chưa đóng → button "Đóng dự án" hiện (user là creator). Click → modal.
  - [ ] Modal dropdown load được danh mục nguyên nhân.
  - [ ] Chưa chọn nguyên nhân + chưa tick checkbox → button "Xác nhận đóng" disabled.
  - [ ] Chọn nguyên nhân + tick checkbox → enable. Submit → toast success + banner đỏ xuất hiện.
  - [ ] Sau đóng: button "Đóng dự án", "Sửa", "Tạo YCBG", v.v. đều ẩn.
  - [ ] DB verify: solutions → status=2, modules → status=10, pricing_requests → status=5, quotations → status=5 (chỉ status 1/2/3, không đụng status=4).
  - [ ] `quotation_histories` có entry `action=closed_by_project` cho từng quotation bị cascade.
  - [ ] Notification xuất hiện ở creator Solution + NLG đang làm giá (check table `notifications`).
  - [ ] User khác mở manager của dự án đã đóng → không thấy button "Đóng" + banner đỏ hiện đầy đủ.
  - [ ] User không phải creator gọi API close → 403.
  - [ ] Gọi close lần 2 → 422 "Dự án đã đóng".

---

## Checkpoints

### Checkpoint — 2026-04-19
Vừa hoàn thành: Brainstorm (4 Q&A: scope, nguyên nhân+ghi chú, cascade 5 entity, notify stakeholders). Design + Plan đầy đủ.
Đang làm dở: Không.
Bước tiếp theo: Bắt đầu Task 1 (migration) khi user xác nhận.
Blocked: Không.

### Checkpoint — 2026-04-19 Batch 3
Vừa hoàn thành: Task 8 (FormRequest `ProspectiveProjectCloseRequest`), Task 9 (controller action `close`), Task 10 (route `POST /prospective-projects/{id}/close` + 2 relationship `closedReason`/`closedByEmployee` trên entity + 5 field closed_* trên `DetailProspectiveProjectResource`), Task 11 (smoke test 3 tinker command pass).
Đang làm dở: Không.
Bước tiếp theo: Task 12 (FE — tạo `CloseProjectModal.vue` trên repo client).
Blocked: Không.

### Checkpoint — 2026-04-19 Wrap up (Batch 4 + 5 + final)
Vừa hoàn thành:
- **Batch 4 (Task 12-13):** Tạo `components/assign/prospective-project/CloseProjectModal.vue` — warning alert đỏ + V2BaseSelect `{id,name}` dropdown reason + V2BaseTextarea maxlength 500 + b-form-checkbox xác nhận + V2BaseButton danger `:interactable`. Subagent adjust từ `$axios` direct sang `apiPostMethod/apiGetMethod` store dispatch (đồng bộ pattern QuotationRejectModal). Thêm `submitting` flag chống double-click. URL underscore `reason_project_failures/getAll`. Compile pass 0 errors.
- **Batch 5 (Task 14-16):** Integrate vào `manager.vue` — import + register CloseProjectModal + V2BaseButton, `showCloseModal` data state, 2 computed `canCloseProject` (gate creator + status≠11) và `isProjectClosed` (status=11), method `fetchProjectDetail` reload sau đóng + `onProjectClosed` handler, button "Đóng dự án" trong slot `#custom-actions` của V2Footer, banner đỏ post-close đầu container-fluid với lý do/ghi chú/ngày/người đóng, `footerMenu` computed ẩn edit+delete khi `isProjectClosed`. Compile pass 0 errors.

Đang làm dở: Không.

Bước tiếp theo:
1. User restart `yarn dev` + test manual Task 18 (10 scenario):
   - Creator thấy button "Đóng dự án" trên manager.vue → click → modal load dropdown reason
   - Chưa chọn + chưa tick → button "Xác nhận đóng" disabled
   - Chọn reason + tick checkbox + submit → toast "Đã đóng dự án" + banner đỏ xuất hiện + ẩn edit/delete
   - DB verify: project.status=11 + closed_*, cascade solutions status=2, modules=10, pricing_requests=5, quotations=5 (chỉ status 1/2/3, không đụng 4)
   - `quotation_histories` có entry `closed_by_project` + meta đủ
   - Notification gửi đến creator/PM/NLG/TP/BGĐ pending
   - User không phải creator → 403 nếu gọi API trực tiếp, button không hiện
   - Close lần 2 → 422 "Dự án đã đóng"
2. Task 17 (optional polish — readonly banner trên quotation/solution edit khi project đóng): skip, BE validation đã chặn save. User thêm sau nếu thấy cần UX warning sớm hơn.

Blocked: Không.

---

## Phase 17 — Bug fix sau test (2026-04-23)

**Scope:** 3 màn list khi dự án đóng: /assign/request-solution, /assign/solution-modules, /assign/pricing-requests. Objects cascade Đóng → vẫn hiện trong list (không ẩn), chặn sửa/xoá, filter có option "Đóng".

### BE

- [x] **Task 19:** `PricingRequestController::index` — thêm `PricingRequest::STATUS_DONG` vào whereIn cho NLG (trước chỉ [2,3,4] nên NLG không thấy YCBG đã Đóng).
- [x] **Task 20:** `PricingRequestService::ensureDraftAndOwner` — throw riêng message "Yêu cầu XD giá đã đóng theo dự án, không thể sửa/xoá" khi status=STATUS_DONG.
- [x] **Task 21:** `RequestSolution` entity — thêm `const STATUS_DONG = 10` + entry 'Đóng' (#6B7280) trong `STATUSES`.
- [x] **Task 22:** `ProspectiveProjectService::closeProject` — cascade RequestSolution (status NOT IN [4 Từ chối, 8 Đã hoàn thành, 10 Đóng] → 10). Thêm `request_solutions` vào mảng cascade counts.
- [x] **Task 23:** `RequestSolutionService::update/destroy` — guard 422 khi status=STATUS_DONG ("Yêu cầu làm giải pháp đã đóng theo dự án, không thể sửa/xoá").

### FE

- [x] **Task 24:** `pricing-requests/index.vue` statusOptions — thêm `{value:5, label:'Đóng'}`.
- [x] **Task 25:** `request-solution/index.vue` statusOptions — thêm `{value:10, label:'Đóng'}`.
- [x] **Task 26:** `solution-modules/constants.js` — thêm `STATUS_DONG=10` + option 'Đóng' vào `STATUS_OPTIONS`.
- [x] **Task 27:** `solution-modules/_id/manager.vue` — banner đỏ "Hạng mục đã đóng" + computed `isModuleClosed` (status===10), truyền `:is-closed` xuống 5 tab (Tasks/Issues/Meetings/Files/HumanResource).
- [x] **Task 28:** `TasksTab.vue` — prop `isClosed`, gate `canCreateTask`/`canEdit`/`canDelete`.
- [x] **Task 29:** `IssueTab.vue` — prop `isClosed`, gate `canCreateIssue` + action edit/delete/handle trong `getRowActions`.
- [x] **Task 30:** `MeetingsTab.vue` — prop `isClosed`, ẩn nút "Tạo mới", gate edit/create_task/delete.
- [x] **Task 31:** `HumanResourceTab.vue` — prop `isClosed`, ẩn nút "Thêm nhân sự".

### Không cần sửa (tự nhiên ẩn)
- `pricing-requests/index.vue` `canEdit`: đã check `status === 1` → Đóng tự false.
- `request-solution/index.vue` `getRowActions`: đã check `status == 1 || 9` → Đóng tự ẩn.
- `solution-modules/index.vue`: list chỉ có nút "Quản lý" (navigate), không có edit/delete trực tiếp.

### Pending manual test
- [ ] **Task 32:** Đóng dự án test → vào /assign/request-solution → YCP của dự án hiển thị với status "Đóng" xám, không có Sửa/Xoá.
- [ ] **Task 33:** /assign/pricing-requests với quyền NLG → thấy được YCBG trạng thái "Đóng" (trước đây ẩn). Filter "Đóng" dropdown hoạt động.
- [ ] **Task 34:** /assign/solution-modules → mở hạng mục đã Đóng → banner đỏ "Hạng mục đã đóng" + 4 tab Tasks/Issues/Meetings/HumanResource ẩn hết nút tạo mới/sửa/xoá.
- [ ] **Task 35:** Gọi API update/destroy trực tiếp trên request-solution/pricing-request đã Đóng → 422 đúng message.

### Checkpoint — 2026-04-23 Phase 17 code DONE
Vừa hoàn thành:
- BE: 5 file (PricingRequestController + PricingRequestService + RequestSolution entity + ProspectiveProjectService + RequestSolutionService) — cascade RequestSolution, whereIn STATUS_DONG cho NLG, 3 guard 422 thân thiện.
- FE: 7 file (3 list statusOptions + solution-modules constants + manager.vue banner + 4 tab props+gate).

Bước tiếp theo: User test Task 32-35.
Blocked: Không.

## Phase 17B — Bug fix sau test (2026-04-29)

- [x] **Task 36:** Thêm "Đóng" vào `progressOptions` trong `request-solution/index.vue` (filter "Tiến trình YC" trước đó thiếu, chỉ có ở `statusOptions`).
- [x] **Task 37:** Đóng dự án cascade tất cả Báo giá (bao gồm status=4 "Đã duyệt") — bỏ `whereIn([1,2,3])` → `where('status', '!=', STATUS_DONG)`.

### Checkpoint — 2026-04-29 Phase 17B
Vừa hoàn thành: 2 fix — progressOptions filter "Đóng" cho request-solution + cascade đóng tất cả báo giá.
Bước tiếp theo: User test Task 32-35 + 2 fix mới.
Blocked: Không.
