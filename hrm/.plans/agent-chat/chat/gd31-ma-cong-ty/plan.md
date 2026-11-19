# GĐ31 — Người khác công ty: hiện họ tên + mã công ty (17/11/2026) @namdangit

Nhánh `gop_db-chat-ma-cong-ty` (api + client, wt-nhom-trao-doi), không migration.

## Lỗi (tái hiện Playwright :3080, NV 13 ↔ NV 222 công ty TPSG)
Dòng 1 ô liên hệ 231px; nhãn `.cr__company` in tên đầy đủ 235px `flex: 0 0 auto` ⇒ `.cr__title` 0px (cần 86px) ⇒ chỉ thấy tên công ty.

## Chốt (user 17/11, phương án 1)
- Dòng hội thoại: họ tên như bình thường + nhãn MÃ công ty (companies.code), nhãn co được, không mã thì không nhãn.
- Đầu cửa sổ chat: họ tên + nhãn mã; dòng phụ giữ tên công ty đầy đủ.

## Task
- [x] BE EmployeeProfiles + ChatPresenter + ChatProfileService trả `company_code`
- [x] FE ConversationRow nhãn mã
- [x] FE ChatPane tiêu đề + nhãn mã
- [x] Playwright đo lại + ca e2e + chạy lại bộ e2e chat

## Kết quả kiểm (17/11)
- API: `chat/conversations`, `chat/direct/{id}`, `chat/profile/{id}` trả `company_code` (curl).
- Playwright đo: dòng Hồ Văn Hồng họ tên 0px ⇒ 150px (đủ chữ), nhãn `TPSG` 40px nằm gọn trong dòng; 50 dòng chỉ 1 nhãn (người cùng công ty không nhãn); đầu cửa sổ chat tên + `TPSG` cùng hàng cách 8px, dòng phụ giữ tên đầy đủ, rê nhãn ra tên đầy đủ.
- e2e mới G6 trong `chat-giao-dien.spec.ts` (6/6). Chạy lại chat-core · drawer · bo-sung · thong-bao-emoji · members-paging · gd2-polish · workspace-tasks: xanh hết trừ chat-drawer N7.
- chat-drawer N7 CHẬP CHỜN CÓ SẴN: mã gốc (gỡ patch) 1/3 lượt đỏ, có patch 2/5 lượt đỏ, đỏ ở 2 bước khác nhau (BE unread 0 · mở lại ngăn chưa thấy tin) ⇒ không do GĐ31; ghi ngoài luồng.
- PHPUnit Workspace 259/259.
- Chưa chạy: agent-chat-pin.spec (cần API AGENT_FAKE).

### Checkpoint — 17/11/2026
Vừa hoàn thành: GĐ31 code xong + kiểm, CHƯA commit (api + client nhánh gop_db-chat-ma-cong-ty, wt-nhom-trao-doi; e2e sửa ở HRM/e2e).
Đang làm dở: —
Bước tiếp theo: user xem :3080 → báo commit → push gop_db + deploy TPE (không migration).
Blocked:

### Checkpoint — 17/11/2026 — ĐÃ DEPLOY TPE
Vừa hoàn thành: commit + fast-forward origin/gop_db + build_tpe EXIT 0 — prod api `f95e246e6` · client `04995de37`, Nothing to migrate, site 200.
Bước tiếp theo: user thử prod; ngoài luồng: chat-drawer N7 chập chờn.
Blocked:
