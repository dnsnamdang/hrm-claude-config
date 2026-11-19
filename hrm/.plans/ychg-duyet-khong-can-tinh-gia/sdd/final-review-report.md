# Final whole-branch review — YCHG "Duyệt không cần tính giá"

**Reviewer:** final gate (Opus 4.8) · **Date:** 2026-11-03
**Repos:** hrm-api (`f5c07c588^..17e4f433f`, 12 files) · hrm-client (`57539391d..602e0a959`, Tasks 5-6)

## Verdict: CHANGES_REQUIRED

One real data-corruption path (item 1, the parked risk) is confirmed reachable and unguarded. Everything else is clean or minor.

---

## Finding 1 — [HIGH] Promoted no-price line (status 3) leaks back into a MIXED group's YCTG and gets re-priced, destroying the no-price catalog price

**Files:**
- `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php:739-774` (`promoteNoPriceLine` — promotes 9→3 but leaves the `price_asking_request_products` row in its group)
- `Modules/MasterData/Services/PriceCalculation/PriceCalculateRequestService.php:248-282` (`skeletonRows` + `excludeTempLines` — excludes only `TEMP_STATUSES [6,7,8,9]`, NOT `STATUS_TRADING (3)`)
- `Modules/MasterData/Services/PriceCalculation/PriceCalculateWriter.php:336` (`ProductPriceWriter::apply` overwrites the catalog unconditionally — no status guard)

**Mechanism.** Groups are keyed by (brand × manufacture). In `ptkdApprove` (PriceAskingRequestWriter.php:651-660) a group is routed to the no-price close path (`pricedGroups`) ONLY if *every* line is in `{9, 8}`. A **mixed** group that has at least one status-9 line AND at least one Đồng ý (status-7) line fails that test, so it stays in `$groups` → `STATUS_WAITING_XNK`. Meanwhile the `$resolved` promotion loop (lines 684-686) is group-agnostic: it promotes every status-9 line to **status 3 (TRADING)** regardless of group, and does **not** detach the line from the group (the `price_asking_request_products` row and its `group_id` are untouched).

The group then proceeds: XNK duyệt nhóm → kế toán lập YCTG. `skeletonRows($group)` (line 250) enumerates `price_asking_request_products.group_id = group`, filtered only by `excludeTempLines`, which excludes pcc status in `TEMP_STATUSES [6,7,8,9]`. The promoted line is now status **3**, which is NOT temp → it is **included** as a `chosen => true` row. The kế toán has no signal it was already priced/promoted. On "Lưu và duyệt"/áp giá, `PriceCalculateWriter.php:336` calls `ProductPriceWriter::apply(...)` and **overwrites** the product's catalog prices (all 6 sale types via `resolvePrices`, where TMĐT is auto-computed from Bán lẻ) and `cost_price`.

**Concrete failure scenario.** YCHG with two hàng tạm of the same brand+manufacturer: product A (won-bid, TH2) and product B (normal). PTKD picks "Duyệt không cần tính giá" for A, "Đồng ý" for B, then Duyệt phiếu. A is promoted to 3 with its won-bid price (e.g. cost 100 / sale 150); group → WAITING_XNK. XNK approves; kế toán opens the YCTG form → A appears as a chosen line. Kế toán prices the group → A's carefully-recorded won-bid price is replaced by the freshly-computed price (and for a TH1 product, its intended 0 price is replaced by a non-zero computed price). The feature's core guarantee ("skip pricing, record the exact price") is silently defeated for A.

**Why uncaught.** `test_parent_no_price_child_normal_route_independently` (diff lines 1023-1038) builds exactly this mixed group (pid2 = `mkSecondProduct` copies brand_id/manufacture_id, so A and B share one group) and asserts A=3, B=2, phiếu=10 — but stops before XNK approve + YCTG creation, which is where the corruption occurs. The invariant `excludeTempLines` relied on ("a WAITING_XNK group never already contains a trading product", stated in its own docblock lines 271-273) is broken by this feature.

**Suggested direction (not applied):** detach the promoted line from its group when promoting (null `group_id` on the `price_asking_request_products` row, mirroring how the promote removes it from the pricing flow), or exclude `STATUS_TRADING` lines from `skeletonRows`/`excludeTempLines`. All-no-price groups (`pricedGroups`, closed `STATUS_PRICED`) are safe — closed groups are rejected at the top of `ptkdApprove` and `lockForXnk` returns 423. Only MIXED groups are affected.

---

## Finding 2 — [INFO] Downstream "status 3 ⇒ has a Phiếu tính giá" assumption: verified NOT present

Grepped `price_calculate*` / `PriceCalculate` usage across all Modules: effectively unreferenced outside `Modules/MasterData/Services/PriceCalculation/` (only a coincidental Currency.php and a migration). ERP-sync / contract-creation keys off the product being tradeable + having rows in `product_unit_prices` / `product_company_units.cost_price`, which `promoteNoPriceLine` writes via `ProductPriceWriter::apply` + `ProductPriceSetWriter::ensureProductSet` — identical to the normal `PriceCalculateFinalizer::promoteProducts` path. A no-price status-3 product is indistinguishable from a normally-priced status-3 product for downstream readers. The implementer's claim holds. No defect.

---

## Finding 3 — [INFO] Cost-gate (giá vốn) leaks: prior leak fixed, no new leak found

The history-note leak was fixed in commit `17e4f433f`: `promoteNoPriceLine` writes `LOG_TEMP_NO_PRICE` note = `"<code>: duyệt không cần tính giá"` (no price), and the `ProductPriceWriter::apply` reason is `"Duyệt không cần tính giá - Yêu cầu hỏi giá <code>"` (no price). `test_no_price_history_note_does_not_leak_cost` asserts the raw price never appears in the request-detail response. The won-bid price is read only inside `TempNoPriceResolver` during `ptkdApprove` and never returned in any response. Line rows / `tempForm` expose only catalog `retail_price` (already gated by existing product-price gates) — no new un-gated path. Clean.

---

## Finding 4 — [INFO] Atomicity: correct

`resolveNoPriceLines` (PriceAskingRequestWriter.php:714-733) runs BEFORE any write and throws 422 (`temp_products`) if ANY status-9 line resolves null — pre-write, so nothing is promoted. All promotion (`promoteNoPriceLine`) runs inside the single `DB::transaction` of `ptkdApprove`. `promoteNoPriceLine`'s own late failure (missing base `product_units` row → ValidationException) also rolls back the whole transaction. `test_promote_is_atomic_on_failure` confirms: one valid + one invalid line → 422, both stay at 9, no price rows written, phiếu stays status 2. Correct.

---

## Finding 5 — [INFO] FX conversion: correct

`TempNoPriceResolver::resolveWonBid` multiplies `estimated_price`/`quoted_price` by `resolveCurrentExchangeRate($quotation)` exactly once. `resolveCurrentExchangeRate` (now `public`, QuotationService.php) returns 1.0 for VND/no-currency and the CURRENT `currencies.exchange_rate` otherwise — NOT the frozen `quotations.exchange_rate`. Cast precedence `((float)$row->estimated_price) * $rate` is correct (single multiply). `test_resolve_won_bid_foreign_currency_multiplies_rate` (2×25000=50000) and `test_ptkd_approve_th2_foreign_currency` confirm. Correct.

---

## Finding 6 — [INFO] Status-9 enumeration: adequately handled except the item-1 gap

- `TEMP_STATUSES` now `[6,7,8,9]`; `isTemp(9)=true`; `STATUS_TEXT[9]`/`STATUS_COLOR[9]` present → badges resolve (`ProductListResource` owner_status, `tempForm`, `lineRow` all use the maps / `isTemp`).
- `PriceAskingProductReader::blockReason` updated to cover 9 (diff). `SELECTABLE_STATUSES`=[1,3], `TEMP_SELECTABLE_STATUSES`=[6,8] — 9 correctly NOT re-selectable into another YCHG (design intent).
- `temp_pending_count` (PriceAskingRequestService.php:441-443) counts only status 6 for Cha + children → 9 does not block "Duyệt phiếu". Correct.
- `excludeTempOnly` / `excludeOwnerTemp` include 9 via `TEMP_STATUSES`. Catalog/picker hide status-9 lines. Correct.
- `can_temp_approve = $canPtkd && isTemp(status)` → status-9 line shows "Sửa" and can be reopened (reopen 9→7/8/6 proven by `test_can_reopen_from_9_to_approve`, `test_temp_reject_from_9_goes_to_8`).
- Whole-phiếu reject resets 9→6 (ptkdReject diff; `test_reject_whole_request_resets_9_to_6`); creator edit resets 9→6 (TempProductService diff; `test_creator_edit_resets_9_to_6`).
- FE: `isTempRejected` checks only status 8 → 9 not mis-flagged; `openTempApprove` has no status guard. Badge text/color from BE.

The only enumeration gap is Finding 1 (`excludeTempLines` not excluding the promoted TRADING line).

---

## Finding 7 — [INFO] Cross-repo contract: aligned

`can_approve_no_price` (BE `tempForm` ↔ FE `loadTempForm` destructure + `tempMeta`), endpoint `POST .../temp-products/{product}/approve-no-price` (route + controller + FE `tempUrl('/approve-no-price')`), `temp_pending_count` (BE-counted, FE `Duyèt phiếu` gate), `company_status`/`company_status_text`/`company_status_color` (badge text+color from BE, FE display-only). All line up.

---

## Minor / cosmetic (non-blocking)

- Stale comments: `ProductCompany::TEMP_STATUSES` docblock, `isTemp` docblock, and `PriceCalculateRequestService::excludeTempLines` docblock still say "6/7/8" though behavior now includes 9. (`excludeTempLines`'s stale invariant assumption is the root of Finding 1.)
- `price_data_text` / `temp_source_text` (Item-4 badges from a prior task) may be null for a status-9 line if their upstream computation only covers 6/7/8 — cosmetic only, not verified.
- `LOG_NO_PRICE_CLOSE` group-close writes `close_reason = ''` (empty) for no-price-closed groups — harmless.
- FE "Duyệt không cần tính giá" discards unsaved form edits (posts empty payload, like Reject); the confirm dialog warns when dirty. Matches design (price is taken from the resolver at Duyệt phiếu, not the form).
