# Fix: dropdown ngạch lương lẫn công ty khác

- [x] BE `RankService::getAll()` / `getAllGroup()` lọc theo công ty đang chọn (`current_company_role`) khi `!use_common_catalog`; ngạch đang dùng (`include_ids`) vẫn trả (28/10/2026)
