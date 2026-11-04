# SDD ledger — plan: HRM/.plans/ychg-duyet-khong-can-tinh-gia/plan.md

## Environment
- Two repos, both on `develop` (user's established workflow for this project — not main/master).
- hrm-api BASE: 8f23401b778459cc2450c31bd87dd3109ad54571 (Tasks 1-4)
- hrm-client BASE: 57539391dcee2681c146f542027caadd32431587 (Tasks 5-6)
- Spec reachable: HRM/.plans/ychg-duyet-khong-can-tinh-gia/design.md (APPROVED)
- Workspace: HRM/.plans/ychg-duyet-khong-can-tinh-gia/sdd/
- **hrm-api working dir (T3+): ISOLATED WORKTREE `/Users/nguyentrancu/DEV/code/ERP-HRM/.worktrees/hrm-api-ychg` on branch `develop`** — commits land on develop directly. The main clone `HRM/hrm-api` is left to the parallel HDBH session (feature branch). hrm-client (T5/T6) still the main clone unless it too collides.
- **Ruling: moved remaining hrm-api work into a dedicated `develop` worktree** — two branch-switch incidents (Task 1 recovered via cherry-pick; Task 3 BLOCKED on wrong branch) proved an external session shares the `HRM/hrm-api` clone and fights over HEAD. A worktree checked out on develop gives my implementers a stable HEAD without me switching the main clone's branch (which would disrupt the parallel session's uncommitted `ServiceAccounting/` work). Non-destructive: develop already holds all my commits; worktree is removed at finish. Cost if wrong: one `git worktree remove` + re-point at main clone. Cleanup recognized by finishing skill (under `.worktrees/`).

## Pre-flight conflict scan

### Cross-task shared file / interface pairs
| A → B | A produces | B consumes | Finding |
|-------|-----------|-----------|---------|
| T1 → T3 | `STATUS_TEMP_APPROVED_NO_PRICE=9`, `TEMP_STATUSES=[6,7,8,9]` | T3 reopen relies on gate accepting 9 via TEMP_STATUSES | OK — T1 adds 9 to TEMP_STATUSES; T3 needs T1 first (order T1→T3 holds) |
| T1 → T4 | const 9 | T4 promotes 9→3 | OK — same const name |
| T1 → T6 | `STATUS_COLOR[9]`,`STATUS_TEXT[9]` | FE badge via BE text/color | OK |
| T2 → T4 | `resolve(int,int):?array` keys case/cost/sale/unit_id | T4 validate+write | OK — keys match |
| T3 → T4 | `tempApproveNoPrice():int=9`, route, `can_approve_no_price` | T4 lines at 9; FE flag | OK |
| T3 → T5/T6 | `can_approve_no_price` flag | FE button/badge | OK |
| T3,T4 share PriceAskingRequestWriter.php | T3 adds tempApproveNoPrice+gate; T4 edits ptkdApprove | different methods, serialized | OK — no overlap |
| T2,T3,T4 share test file PriceAskingNoPriceApproveTest.php | T2 creates; T3,T4 append | serialized growth | OK |

### Per-task self-agreement
| Task | Tests vs code | Files create vs touch | Finding |
|------|---------------|----------------------|---------|
| T1 | isTemp(9)=true ↔ adds 9 to TEMP_STATUSES | entity + test | agrees |
| T2 | won_bid/zero/null cases ↔ TH2-then-TH1-then-null | new service + new test | agrees; unit_id column name delegated to builder (flagged, has fallback) |
| T3 | set 9 / reopen 9→7 / gate / flag ↔ method+gate+route+tempForm | writer/controller/routes/service | agrees; depends T1 |
| T4 | promote/block/Cha-Con/4-vs-10/atomic ↔ ptkdApprove txn | writer + test | agrees; depends T2,T3 |
| T5 | button v-if flag ↔ ProductForm footer | FE | agrees; depends T3 |
| T6 | status-9 label/badge ↔ list form | FE | agrees; depends T1 |

### Rubric-defect mandates
None. No task mandates a test that asserts nothing or verbatim logic duplication.

**Scan result: clean.** Dependency order T1→T2→T3→T4→T5→T6 satisfies all cross-task needs. No pre-flight rulings required.

## Task log

### Task 1 — status 9 + maps + reader audit
- Implementer DONE_WITH_CONCERNS. hrm-api `develop`: 8f23401b7 → f5c07c588 (feat) → e359041b0 (test fix). 7 tests pass.
- Branch-switch incident: external process checked out `feature/phieu-hach-toan-dich-vu-hdbh-phase1` mid-task; implementer cherry-picked both commits onto develop and reset feature branch to its exact prior tip 8f23401b7. Verified via reflog — no commits lost, non-destructive. WATCH: a parallel session may be sharing this clone (untracked `Modules/Finance/.../ServiceAccounting/` HDBH remnants present, pre-existing, untouched).
- Extra in-scope audit fixes: `TempProductVisibilityTest.php:70` assertion [6,7,8]→[6,7,8,9]; `PriceAskingProductReader::blockReason` now gives status 9 the same "đã duyệt, chờ duyệt phiếu" message as 7.
- **CARRY to T3/T4 — hard-coded `7` sites still treating only 7 as approved (need 9 parallel handling):**
  - `PriceAskingRequestWriter`: reopen ~line 546 (→ T3); promote-on-phiếu-approval ~lines 648 & 684 (→ T4).
  - `TempProductService:152`: edit reset of 7/8 back to 6 (→ T3 reopen semantics; decide if 9 also resets on edit).
- Review: Spec ✅, Quality Approved. No Critical/Important. Minors = cross-task routing (deferred to owners) + branch confirm (verified: feature branch tip = 8f23401b7, f5c07c588 NOT duplicated there).
- **FULL carry-list of status-7-only sites (confirmed by reviewer) — later tasks MUST handle 9:**
  - `PriceAskingRequestWriter.php:546` reopen (7→6 only) → T3
  - `PriceAskingRequestWriter.php:648` promote on Duyệt phiếu (moves only [7]→WAITING_PRICE(2)); status 9 must go to TRADING(3) → T4
  - `PriceAskingRequestWriter.php:684` revert (7 only) → T4
  - `TempProductService.php:152` edit resets 7/8→6; decide if 9 also resets → T3
  - `ProductListResource.php:167` flag `[6,8]` → check in T6/relevant
  - Note: `PriceAskingProductReader.php:41` TEMP_SELECTABLE_STATUSES=[6,8] correctly EXCLUDES 9 (status-9 line can't be re-picked into a new YCHG) — leave as is.
- **Task 1: complete (commits 8f23401b7..e359041b0, review clean)**

### Task 2 — TempNoPriceResolver
- BASE hrm-api: e359041b0 → HEAD f31463e13 (1 commit, on develop confirmed). 6/6 tests pass.
- Pinned by implementer: `quotation_product_prices.unit_id` (fallback base unit if null/0); `resolveCurrentExchangeRate(Quotation):float` (1.0 for VND/none); TH1 reads `product_company_units.cost_price` + `product_unit_prices` where `price_type_id=1`, base unit, missing row ⇒ ineligible.
- **Ruling: accept `QuotationService::resolveCurrentExchangeRate` private→public** — visibility widening to reuse not duplicate; non-breaking for existing callers. Cost if wrong: a shared-file touch the user didn't pre-approve, trivially revertible to a 5-line local copy.
- **Ruling: accept won-bid 0/0 classifying as `won_bid` not `zero`** — qpp prices are NOT NULL default 0; T4 writes cost/sale+promotes identically for both cases, only label differs; `zero`(TH1) still reached when no won-bid + explicit 0/0 catalog. Cost if wrong: none observed (functionally equivalent downstream).
- Review: Spec ✅, Quality Approved. No Critical/Important.
- Task 2: minor (deferred): `TempNoPriceResolver.php:97-98` `Quotation::find()` could return null→TypeError (race only; FK + no soft-deletes make it near-impossible on the transactional approve path). Final-review triage.
- Task 2: minor (deferred): `TempNoPriceResolver.php:116-118` retail `->value('price')` takes arbitrary row if `product_unit_prices` has dup/effective-dated rows per (product_unit_id,company_id,price_type_id). Safe-fail toward `null` (blocks) in most cases; only mild risk of false-zero. Final review: confirm schema uniqueness/effective-date; add order-by if dups possible.
- Task 2: minor (deferred): missing test case "retail=0 but product_company_units row missing" (code handles correctly). Coverage gap only.
- **Task 2: complete (commits e359041b0..f31463e13, review clean)**

### Task 3 — approve-no-price endpoint + gate + FE flag
- BASE hrm-api: f31463e13
- First dispatch BLOCKED: main clone on wrong branch (feature/phieu-hach-toan-dich-vu-hdbh-phase1); implementer made NO changes, stopped correctly.
- Resolved by worktree ruling above. Re-dispatched in worktree `/Users/.../.worktrees/hrm-api-ychg` (develop, HEAD f31463e13).
- Implementer DONE. HEAD f31463e13 → 9b88dc7cb (1 commit). Tests: PriceAskingNoPriceApproveTest 10 passed (6 T2 + 4 new, failed pre-impl as expected); PriceAskingTempProductTest 16 passed.
- Decisions: (1) no status-7-only reopen branch existed — gate uses TEMP_STATUSES (incl 9) so 9 reopens to 7/8 free; (2) tempSave on a 9 line resets to 6 (like 7); (3) TempProductService edit-reset list now includes 9→6.
- Worktree note: implementer copied `vendor/` + `.env` from main clone (symlink breaks composer autoload). Both untracked/gitignored — expected scaffolding, not a code change.
- Review package: review-task-3.diff (BASE f31463e13, HEAD 9b88dc7cb). Reviewer dispatched.
- Review verdict: Spec ✅. Quality Changes-requested — 1 Important + minors.
  - IMPORTANT: `ptkdReject` (~698, "A9" block) resets only `[7]`→6 on whole-phiếu reject; a status-9 line stays stuck at 9 (9 ∉ TEMP_SELECTABLE_STATUSES[6,8] → product un-re-pickable). Last 7-only reset Task 3 made reachable → Task 3 owns it. (ptkdApprove ~662 promote stays Task 4's.)
  - Minors (cheap, folded into fix round): stale "6/7/8" comments in PriceAskingRequestService + tempReject docblock; test class docblock stale; missing tests for tempReject 9→8 and edit-reset 9→6.
  - Minors DEFERRED to final review: "assert no price-table writes" coverage; test_approve_no_price_gate coupling hardening.
- **Fix round 1** (resume same implementer ac2f1cd): fix ptkdReject reset to include 9 + test; add 9→8 reject test + edit-reset 9→6 test; stale-comment fixes. ptkdApprove untouched.
  - DONE commit d8d34725f. Tests: PriceAskingNoPriceApproveTest 13 passed (3 new), PriceAskingTempProductTest 16 passed.
  - Implementer concern: accidental `git checkout -- .` mid-work, re-applied; I VERIFIED worktree clean (status empty, tracked) + HEAD=d8d34725f on develop → committed state correct, nothing lost.
  - Fix-round re-review done inline (174-line diff, I held full review context): Important ptkdReject fix correct (moves [7,9]→6, ptkdApprove untouched); 3 tests assert real pcc/JSON state, non-vacuous; comments fixed. Approved.
  - Deferred to final review: (a) assert endpoint writes no price tables; (b) harden test_approve_no_price_gate coupling to ptkdApprove.
- **Task 3: complete (commits f31463e13..d8d34725f, review clean after fix round 1)**

### Task 4 — ptkdApprove integration (validate + write price + promote 9→3 + close request)
- BASE hrm-api: d8d34725f (worktree /Users/.../.worktrees/hrm-api-ychg, develop)
- Dispatched (implementer a342affc, sonnet).
- Implementer DONE. HEAD d8d34725f → b574b0cc6 (1 commit). Tests: PriceAskingNoPriceApproveTest 21 passed (13 old + 8 new); PriceAskingTempProductTest 16 passed. Worktree verified clean on develop.
- Implementer concerns: (1) wrote impl before running new tests → never saw fail-first (TDD step skipped; reviewer must independently judge test meaningfulness); (2) writes price coefficient = sale/cost (or 0 when cost=0) — own choice, not briefed; (3) ProductPriceWriter::apply clears pending future expected-price rows (none for new temp); (4) downstream audit: NO code assumes status-3 requires a Phiếu tính giá (ProductLifecycleService/ProductWriteService already promote to 3 without one) → no guard added.
- Review package: review-task-4.diff (BASE d8d34725f, HEAD b574b0cc6). Reviewer dispatched (a34005c, OPUS — high-risk task) with both flagged concerns called out for explicit adjudication.
- OPUS review verdict: Spec ❌ (ONE violation) / Quality Changes-requested. Logic, atomicity (throw in resolveNoPriceLines:649 BEFORE any write — traced), flat 6-price write, FX no-re-multiply, 9→3 promote, mixed/all-no-price transitions all CORRECT. All 8 tests MEANINGFUL (non-vacuous, traced). Coefficient sale/cost SAFE (div-0 guarded, price persisted explicitly so cannot corrupt catalog). Downstream audit holds (no status-3↔price_calculate coupling in Assign services).
  - BLOCKER (IMPORTANT, spec violation): cost leak — `PriceAskingRequestWriter.php:773` LOG_TEMP_NO_PRICE note `"<code>: giá nhập <cost>, giá bán <sale>"`; returned UNGATED via PriceAskingRequestService.php:382 (excludes only LOG_TEMP_CREATED) + :445-450 (note verbatim). Cost visible to any YCHG-detail viewer. Violates project cost-gate rule. FIX: note = code only (like LOG_TEMP_REJECT).
  - Minors: coefficient needs a clarifying comment (cheap, folded in); redundant head-write all-no-price branch (DEFERRED, harmless).
  - PARKED for final review (reviewer OBSERVATION, not a T4 bug): a status-9 line promoted to 3 while sharing a group with a Đồng ý(7) line stays a group member → may resurface in that group's later price-calc. Per-line independence is spec-intended + tested (test_parent_no_price_child_normal_route_independently). Final review must trace whether group price-calc re-touches a status-3 line.
- **Fix round 1** (resume implementer a342affc): kill cost leak (note=code only) + regression test asserting detail response has no cost; add coefficient comment. Redundant head-write deferred.
  - DONE commit 17e4f433f. Implementer confirmed leak first (ran new regression test against pre-fix code → detail response contained `giá nhập 123457` → FAIL; passes after fix). Tests: PriceAskingNoPriceApproveTest 22 passed (21 + new leak test); PriceAskingTempProductTest 16 passed.
  - Fix-round re-review done inline (82-line diff, full review context held): note now code-only `'<code>: duyệt không cần tính giá'` (mirrors LOG_TEMP_REJECT) — cost leak closed. Regression test exercises TH2 won-bid path (cost 123457), asserts cost string absent from whole detail body AND note is exactly code-only → non-vacuous, pins the real leak path. Coefficient comment added. Implementer dropped the sale-price absence assertion CORRECTLY: `retail_price` (sale) is the public selling price, not gated; only cost (giá vốn) is gated — test asserts cost-only, matching the project rule. Approved.
  - Still PARKED for final review: status-9 line promoted to 3 sharing a group with a Đồng ý(7) line stays a group member → trace whether group price-calc re-touches a status-3 line. Also deferred: redundant head-write in all-no-price branch (harmless).
- **Task 4: complete (commits d8d34725f..17e4f433f, review clean after fix round 1)**

### FE tasks (T5/T6) — hrm-client environment plan (prep done while T4 runs)
- hrm-client main clone ALSO hijacked by HDBH session: on `feature/phieu-hach-toan-dich-vu-hdbh-phase1` with uncommitted `pages/transport/delivery-quotations/components/DeliveryQuotationForm.vue` (parallel work — DO NOT touch this clone's HEAD or that file).
- hrm-client `develop` tip = 57539391d (= T5/T6 BASE, matches ledger), NOT checked out in any worktree. Both target files present on develop (ProductForm.vue, PriceAskingRequestForm.vue).
- PLAN: before T5, create worktree `/Users/.../.worktrees/hrm-client-ychg` on develop (mirror hrm-api approach). T5 then T6 serial in that worktree. BASE for each FE review = that worktree's HEAD at dispatch.
- Playwright caveat: local run-hrm server runs off main clones (likely on feature branch, without my develop code). End-to-end Playwright for T5/T6 is best-effort — may need dev server pointed at worktrees, else implementer notes limitation in report (brief already allows this).
- DONE: created worktree `/Users/.../.worktrees/hrm-client-ychg` on develop @ 57539391d (= T5/T6 BASE). node_modules symlinked from main clone, .env copied — `npm run dev` works. Worktree verified clean (only untracked node_modules).

### Task 5 — FE footer button "Duyệt không cần tính giá" (ProductForm.vue)
- BASE hrm-client: 57539391d (worktree /Users/.../.worktrees/hrm-client-ychg, develop)
- Dispatched (implementer ae9142ed, sonnet). Ruling carried: Playwright best-effort only (local dev server runs off main clones on feature branch, not this develop code); primary gates = code-read vs existing Đồng ý/Không duyệt patterns + convention grep; full end-to-end at controlled final checkpoint. No subagents.
- Implementer DONE_WITH_CONCERNS, commit 3d18f1b86. Convention grep clean; Playwright not run (dev server on feature branch) — expected per ruling.
- **node_modules mis-commit (I fixed):** implementer's `git add` staged the untracked `node_modules` SYMLINK (.gitignore has `node_modules/` with trailing slash → matches dir, NOT a symlink-as-file). Would pollute develop on merge. I `git rm --cached node_modules` + `git commit --amend` → 40bec88ef; symlink intact on disk, now untracked. **Lesson for T6 dispatch: tell implementer to `git add` the target file BY PATH, never `git add -A`/`.`**
- Review package: review-task-5.diff (BASE 57539391d, HEAD after amend). Task review done INLINE (ruling: 32-line additive FE diff, full plan+BE context held → independent reviewer adds little, conserve a seat; recorded here).
  - Spec ✅: button (V2BaseButton primary sm, label verbatim), v-if `can_approve_no_price && tempStatus !== 9`, `:interactable="ready && !saving"`, info-icon + b-popover TH1/TH2, loadTempForm destructures+maps `can_approve_no_price`, handler confirm→empty-payload POST `tempUrl('/approve-no-price')`→`tempDone`. Verified `tempUrl` builds exact URL; `tempDone` = markFormSaved()+toast+$emit('temp-done') (parent navigates; markFormSaved prevents false unsaved-warning).
  - Concern 1 (empty payload `{}`, skip tempValidate): RESOLVED correct-by-design — controller `tempApproveNoPrice($id,$product)` takes NO FormRequest; writer only `setTempStatus(...9)`; price comes from resolver at ptkdApprove, not the form. No body needed.
  - Concern 2 (dirty-form warning parity): VALID minor — reject warns when form dirty (edits discarded), approve-no-price also discards unsaved edits but didn't warn; project no-silent-data-loss convention. FIX applied by me (controller edit, 1-line): appended `isFormDirty()` clause to the confirm message, mirroring reject. Amended into commit → 0fd2a1da7. Convention grep still clean; isFormDirty() confirmed defined (L545).
- **Task 5: complete (commit 57539391d..0fd2a1da7, review clean inline)**

### Task 6 — FE status-9 recognition on YCHG detail (PriceAskingRequestForm.vue, Cha + Con)
- BASE hrm-client: 0fd2a1da7 (same worktree, develop)
- Dispatched (implementer ab64b7bb, sonnet). DONE commit 5a5acffe5 (tooltip + comments only; confirmed NO logic change needed — status 9 already handled generically). node_modules NOT staged (add-by-path instruction worked). Convention grep clean. Playwright deferred to final checkpoint (expected).
- Task review done INLINE (recognition task, tiny diff, full context held).
  - Recognition verified per spot: Cha & Con buttons both `Number(company_status) === 6 ? Duyệt : Sửa` → 9 falls to "Sửa" (reopen). Cha badge reads BE `company_status_text/color` (not hardcoded). `openTempApprove` = plain router.push, no guard; `isTempRejected` matches only 8 → 9 not blocked.
  - **Cross-repo correctness (I verified in hrm-api):** whole-phiếu Duyệt enable = `:interactable="!tempPendingCount"`; BE `temp_pending_count` (PriceAskingRequestService.php:441) counts ONLY `company_status === STATUS_TEMP(6)` across Cha + `recipe_children` (Con). So status 9 (like 7/8) counts as DECIDED → button enables when all lines leave 6; matches ptkdApprove gate. No FE/BE change needed — correct by construction.
  - Quality minor FIXED by me (controller edit): the pre-decision ("Duyệt", `=== 6`) tooltips for Cha AND Con still listed only 2 options; form now offers 3 → updated both to "Đồng ý, Duyệt không cần tính giá hoặc Không duyệt". Amended → 602e0a959.
  - Concern (pre-existing, NOT a regression, out of scope): Con rows show no colored status badge — but the Duyệt/Sửa button already distinguishes decided vs undecided, identical for 7/8/9. Changing Con badge rendering would touch the existing flow + wasn't requested. Noted for final review only.
- **Task 6: complete (commit 0fd2a1da7..602e0a959, review clean inline)**

### All 6 tasks complete — next: final whole-branch review (both repos), then finishing-a-development-branch
- hrm-api worktree /Users/.../.worktrees/hrm-api-ychg develop: d8d34725f..17e4f433f is T3(fix)+T4(+fix); full feature range from pre-feature base. T1 e359041b0.. ; whole BE range = <pre-T1-base>..17e4f433f.
- hrm-client worktree /Users/.../.worktrees/hrm-client-ychg develop: 57539391d..602e0a959 = T5+T6.
- Final review MUST include the PARKED observation: status-9 line promoted to 3 sharing a group with a Đồng ý(7) line stays a group member → trace whether group price-calc (PriceCalculate flow) re-touches a status-3 line. Plus Review Focus: audit-reader status-9 handling, null-price block/atomic tx, FX, downstream Phiếu-tính-giá assumptions.
- Feature ranges: hrm-api f5c07c588^(=8f23401b7)..17e4f433f (7 commits, 12 files, +704/-13); hrm-client 57539391d..602e0a959 (2 commits, 1 file). Full-feature diffs: final-review-hrm-api.diff, final-review-hrm-client.diff.
- **BE tests GREEN at final HEAD 17e4f433f** (re-run post-all-amends): PriceAskingNoPriceApproveTest 22 + PriceAskingTempProductTest 16 + ProductCompanyFoundationTest 6 + TempProductVisibilityTest 7 = **51 passed**. (FE Vue has no unit tests; Playwright end-to-end deferred to controlled checkpoint.)
- Final whole-branch reviewer dispatched (opus, agent abaa893e) with both diffs + both worktrees + parked trace + 7 must-investigate items. Awaiting verdict.

### Final review verdict: CHANGES_REQUIRED — Finding 1 (HIGH data-corruption) fixed
- final-review-report.md: Opus verdict CHANGES_REQUIRED. 1 blocker (Finding 1), Findings 2-7 INFO/PASS. Finding 1 = the PARKED risk, now confirmed REACHABLE: MIXED group (status-9 no-price line + status-7 Đồng ý line) → group stays WAITING_XNK → kế toán lập YCTG → `skeletonRows`/`excludeTempLines` excluded only TEMP_STATUSES[6,7,8,9], NOT the promoted-to-3 line → it leaked into the YCTG and áp-giá OVERWROTE its recorded no-price catalog price (TH2 won-bid) / replaced its intended 0 (TH1).
- **Ruling (fix direction):** added explicit marker column `price_asking_request_products.no_price` rather than the reviewer's two suggestions.
  - Rejected (a) "null group_id on promote": detail display (`PriceAskingRequestService` groups lines strictly by group_id) → the promoted line would VANISH from phiếu chi tiết (UX regression). Cost if wrong: line invisible after Duyệt.
  - Rejected (b) "exclude STATUS_TRADING(3) from skeleton": `PriceCalculateApiTest` proves a legit status-3 "hàng cũ" IS re-priced through a YCTG (fixture `n2`) — blanket-excluding 3 breaks that real flow + its test. Cost if wrong: can't re-price catalogued goods.
  - Chosen: marker targets ONLY the promoted no-price line (no_price=1 in `promoteNoPriceLine`), excluded NULL-safe in `excludeTempLines`; group_id KEPT (detail still shows it, badge 'Đang kinh doanh'). Legit status-3 re-price line has no_price=0 → stays in skeleton. Surgical, no collateral.
- **Why it's complete:** `excludeTempLines` is the single shared gate at BOTH call sites — line 197 (YCTG count) and line 250 (`skeletonRows`); `PriceCalculateRequestWriter::validate()` iterates ONLY `$skeleton` → a product absent from skeleton is never written → covers GET form AND POST create/update.
- Files: migration `2026_11_03_000001_add_no_price_...` (idempotent, default 0, after unit_name, reversible, RUN on erp_hrm_check); `PriceAskingRequestProduct` cast `no_price=>boolean`; `PriceAskingRequestWriter::promoteNoPriceLine` sets no_price=1; `PriceCalculateRequestService::excludeTempLines` NULL-safe exclusion + docblocks.
- Regression test ADDED: `test_promoted_no_price_line_excluded_from_yctg_skeleton_in_mixed_group` — mixed group, TH2 won-bid (cost 100/sale 150), approve phiếu → pid1=3 w/ price recorded; asserts `skeletonRows($group)` EXCLUDES pid1, INCLUDES pid2 (Đồng ý), no_price=1 + group_id preserved. (Guards the exact leak point: without the filter, status-3 pid1 is not-temp → leaks in → assert fails.)
- Tests GREEN: PriceAskingNoPriceApproveTest **23 passed** (22 + new regression); PriceCalculateApiTest + PriceAskingTempProductTest **19 passed** (confirms status-3 re-pricing + temp flow intact).
- Scoped re-review (sonnet, agent afa8200f) dispatched on fix diff — awaiting verdict.
- Scoped re-review (sonnet afa8200f): **APPROVED**. Confirmed: marker set in-transaction before XNK/Kế toán can read skeleton; single gate `excludeTempLines` covers count+skeleton+GET+POST (validate iterates $skeleton); hàng cũ status-3 inserted with no_price=0 stays in skeleton; whereNull-OR-0 parenthesised then ANDed with whereNotExists (correct); no reset needed (promotion only after PTKD approve → phiếu ASKING; reopen/edit/reject only possible pre-approve; creator edit re-inserts lines anyway); migration correct; regression test fails without fix (non-vacuous). Lone optional gap: no service-level test that status-3 hàng cũ stays in skeleton — already covered by PriceCalculateApiTest. No residual blockers.
- **COMMITTED develop (hrm-api worktree): ed57fb441** (5 files, +86/-5). Finding 1 CLOSED. Final review now fully resolved → proceed to finishing-a-development-branch.

### FINISHED (2026-11-03)
- Verify: 10 affected suites GREEN = 129 passed, 0 fail (price-asking/price-calculate/temp-product/product-company).
- hrm-api develop rebased onto origin/develop (8 behind → clean, no conflict; origin commits didn't touch PriceCalculation/Entities/Migrations) → re-tested 23 passed → PUSHED origin/develop 66ce147dd..4473321a7.
- hrm-client develop rebased onto origin/develop (11 behind → clean, origin didn't touch my 2 Vue files) → PUSHED origin/develop 66a3d7d47..468b6e9ae.
- Both worktrees removed (hrm-api-ychg, hrm-client-ychg); hrm-client node_modules symlink dropped first (target in main clone intact). Main clones untouched (both still on feature/phieu-hach-toan-dich-vu-hdbh-phase1).
- FEATURE COMPLETE. 6 tasks + final-review Finding 1 fix, all pushed to develop in both repos.
