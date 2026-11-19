# Task 6 report — FE recognizes status 9 (PriceAskingRequestForm.vue)

Findings (all spots generic; no logic change needed):
- Cha button (~255): `v-if Number(row.company_status) === 6` Duyệt, `v-else` Sửa -> generic, 9 falls to Sửa. No change.
- Cha badge (~222): `<V2BaseBadge :color="row.company_status_color">{{ row.company_status_text }}</V2BaseBadge>` -> BE-driven, no FE map. No change.
- Con button (~311): same `=== 6` / v-else. No change. Con rows have no status badge at all (none rendered), so nothing to do.
- openTempApprove (~754): plain `$router.push(.../temp/<productId>)`, no guard. `isTempRejected` only matches 8 (reject-note styling), 9 not affected. No change.
- Whole-phiếu Duyệt (~394-395): `:interactable="!tempPendingCount"`, tempPendingCount = BE `detail.temp_pending_count`. BE (PriceAskingRequestService ~441) counts only company_status == STATUS_TEMP (6) for Cha + recipe_children, so 9 is decided. No FE change.
- Changed: only the "Sửa" popover tooltip text (Cha + Con) -> "Mở lại form để đổi quyết định: Đồng ý ↔ Duyệt không cần tính giá ↔ Không duyệt. Đổi được tới khi bấm Duyệt phiếu." plus two code comments (7/8 -> 7/8/9). Grey popover, no red.
- Convention grep (raw button/input/class="btn" not V2Base): empty.
- Playwright: NOT run (local dev server runs main clone on another branch without this code; not fighting env).
Concerns: live end-to-end deferred. Con rows show no badge (pre-existing).
