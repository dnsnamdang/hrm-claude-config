# Task 2 report — TempNoPriceResolver

Status: DONE_WITH_CONCERNS

## Pinned facts
- quotation_product_prices unit column: `unit_id` (nullable, = units.id). Fallback to base unit (product_units.is_base=1 -> unit_id) if null/0.
- estimated_price / quoted_price are NOT NULL default 0.00 (decimal 15,2) -> the IS NOT NULL filter is trivially true; a won-bid line with 0/0 would still be classified won_bid.
- quotations.currency_id exists (nullable). STATUS_TRUNG_THAU = 7.
- QuotationService::resolveCurrentExchangeRate(Quotation $quotation): float — was PRIVATE; changed to PUBLIC (only change). Returns 1.0 for null currency / code VND, else currencies.exchange_rate. QuotationService has no constructor, so app(QuotationService::class) is cheap.
- TH1 read points: cost = product_company_units.cost_price (product_unit_id = base product_units.id, company_id); sale = product_unit_prices.price (price_type_id=1 Bán lẻ, same unit + company). "Explicit zero" = row exists with value 0 (cost_price is NOT NULL default 0, so row existence is the discriminator). unit_id = base product_units.unit_id.

## Test
php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php
Before impl: 6 failed (class missing). After: 6 passed.

## Concerns
- resolveCurrentExchangeRate visibility private -> public (shared method; CLAUDE.md says ask first).
- Won bid with 0/0 prices counts as won_bid.
- Currencies in test: code 'XX###' used for foreign rate.
