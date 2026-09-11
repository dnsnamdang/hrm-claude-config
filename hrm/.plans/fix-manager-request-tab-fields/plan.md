# Fix: tab Yêu cầu ở màn /assign/prospective-projects/{id}/manager mất Nhóm ngành / Nhóm giải pháp

- [x] FE `pages/assign/prospective-projects/_id/manager.vue` — `loadRequestSolution()` whitelist 12 key nên rơi mất `scope_id`, `industry_id`, `project_phase_id`, `reject_reason`, `cancel_reason` → đổi sang spread nguyên response API (2026-08-27)
