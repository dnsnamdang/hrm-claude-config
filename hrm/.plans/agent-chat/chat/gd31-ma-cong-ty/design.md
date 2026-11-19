# GĐ31 — Người khác công ty: họ tên + mã công ty (17/11/2026) @namdangit

## Vấn đề
Ô liên hệ (ConversationRow) của người khác công ty in nhãn TÊN công ty đầy đủ (`flex: 0 0 auto`) ⇒ chiếm hết dòng, họ tên 0px ⇒ chỉ thấy tên công ty.

## Quyết định đã chốt (user 17/11, phương án 1)
- Dòng hội thoại: họ tên như bình thường + nhãn MÃ công ty (`companies.code`: TPE, TPHP, TPV, TPSG, TPA, UPS, EG…). Nhãn co được (max 40%), rê chuột ra tên đầy đủ.
- Đầu cửa sổ chat 1–1 (ChatPane, dùng chung trang + ngăn trượt): họ tên + nhãn mã; dòng phụ GIỮ tên công ty đầy đủ.
- Chỉ hiện khi khác công ty đang làm (`$store.state.current_company`); không mã ⇒ không nhãn. Nhóm (space) không nhãn.

## Kỹ thuật
- BE: `EmployeeProfiles::baseQuery/format` thêm `company_code`; `ChatPresenter` (other/member) + `ChatProfileService` trả kèm. Không migration.
- FE: helper `otherCompanyCode(person, currentCompany)` ở `utils/chat/chatFormat.js`; `ConversationRow.vue` (`chat-conv-company-<id>`), `ChatPane.vue` (`chat-head-company`). Kiểu nhãn nền #fef3c7 chữ #92400e như cũ.
- e2e: `chat-giao-dien.spec.ts` G6 (env `CHAT_OTHER_CO_ID`, mặc định 222 — TPSG trên db_gop_6_11).
