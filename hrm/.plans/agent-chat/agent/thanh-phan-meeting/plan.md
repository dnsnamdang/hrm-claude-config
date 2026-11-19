# Agent — tool `thanh_phan_meeting` (thành phần tham gia 1 meeting)

User yêu cầu + cho "làm" 16/11/2026 (cách 1: tool mới, không gộp vào chi_tiet_meeting). Nhánh `gop_db-agent-thanh-phan-meeting`
(hrm-api + hrm-client, tách origin/gop_db api c28aaa6d7 · client c7f0f1ff0, worktree wt-nhom-trao-doi). Không migration, không quyền mới.

- [x] BE `Modules/Agent/Support/MeetingGuard::participants(Meeting, $max=100)`: phía công ty (employeeOptionLabel, vai trò,
      điểm danh chữ+màu khớp FE AttendanceStatusCell, ghi chú bỏ HTML ≤200), phía khách hàng (tên, vai trò — KHÔNG SĐT),
      counts (total/present/absent_reason/absent_no_reason/pending/customer_total), truncated. 0 ⇒ "Chưa phản hồi" khi
      Lên/Chốt lịch, khác ⇒ "Chưa điểm danh". 14 query cố định (3 người hay 32 người như nhau — không N+1).
- [x] BE `Tools/ThanhPhanMeetingTool` (quyền: MeetingGuard::find ⇒ canView; không thấy = không tồn tại, cùng 1 nội dung);
      gửi model bản bỏ màu; block `meeting` + `participants`. Đăng ký AgentToolRegistry (46 tool).
- [x] PHPUnit MeetingExtraToolsTest +3 (denied = missing; 2 phía + điểm danh + không lộ SĐT + model không màu; Lên lịch +
      cắt 100). Sửa số đếm registry ở PersonalToolsTest / PayrollToolsTest. Agent: 262/265 — 3 lỗi KHÔNG liên quan (xem dưới).
- [x] Eval +2 câu (200: hỏi theo mã ⇒ thanh_phan_meeting; 201: "ai vắng họp gần nhất" ⇒ lich_meeting + thanh_phan_meeting).
      Chạy Haiku thật local: 2/2 đúng công cụ (~52 ₫).
- [x] FE `components/agent/AgentResultBlock.vue`: khối meeting thêm "Phía công ty" (dòng đếm + badge điểm danh) /
      "Phía khách hàng" / dòng "Chỉ hiện 100 người đầu…".
- [x] e2e `tests/agent/agent-chat.spec.ts` ca "thành phần tham gia meeting" (stub lượt): 1/1, đo không tràn ngang.
- [ ] Chạy lại TOÀN BỘ agent-chat.spec — cần BE AGENT_FAKE=1 của worktree này (đang chỉ có :8070 wt-tpe-agent code cũ).
- [x] 16/11 commit api 5fc3410df · client 9c2c89f3f, merge gop_db fast-forward, push cả 2 nhánh. ĐÃ DEPLOY TPE (user tự chạy build_tpe.sh vì lệnh của Claude bị chặn): EXIT 0, Nothing to migrate, registry có tool, bundle có khối mới, site 200.

## Ngoài luồng (ghi lại, chưa sửa)
- origin/gop_db có migration chưa chạy ở DB local `2026_11_16_000001_add_sort_order_to_meeting_rooms_table` (+ 2 bản khác của
  người khác) ⇒ 3 test phòng họp của Agent lỗi `Unknown column sort_order` và :8080 local màn phòng họp có thể lỗi. Deploy prod
  thì build_tpe.sh sẽ chạy cả 3 bản này — phải liệt kê cho user trước.

## Đợt 2 (16/11 chiều) — "hỏi gì lấy đúng số liệu đó" — nhánh `gop_db-agent-loc-dung-so-lieu` (từ 5fc3410df / 9c2c89f3f)
User chốt: quy tắc chung cho mọi loại câu hỏi — có điều kiện thì chỉ lấy đúng phần khớp, không lấy đầy đủ.
- [x] `AgentPrompt::system()` thêm luật 12 (truyền điều kiện vào tham số lọc; không lấy hết rồi tự lọc).
- [x] `thanh_phan_meeting` tham số `trang_thai` [co_mat|vang_co_ly_do|vang_khong_ly_do|chua] (mảng hoặc chuỗi): chỉ trả người
      phía công ty khớp, KHÔNG trả phía khách; `filter {labels, matched}`; counts vẫn đủ; giá trị lạ ⇒ error; [] = không lọc.
      Mô tả rút còn 508 ký tự (test giới hạn 600).
- [x] FE tiêu đề "Vắng có lý do, Vắng không lý do · 2/32 người phía công ty", lọc ra 0 ⇒ "Không có ai.".
- [x] PHPUnit +1 (lọc 1/2 trạng thái, chuỗi đơn, 0 người, [] , giá trị lạ). Agent 263/266 (3 lỗi sort_order phòng họp như cũ).
- [x] e2e +1 ca stub (lọc + 0 người): 2/2 ca thành phần.
- [x] AI thật (Haiku, local): "có ai vắng" ⇒ trang_thai [vang_co_ly_do, vang_khong_ly_do]; "ai có mặt" ⇒ [co_mat];
      "ai chưa điểm danh" ⇒ [chua]; "có những ai" ⇒ không lọc. 4/4 đúng.
- [x] Rà 45 tool ⇒ user chọn "2" (làm cả 7): thêm tham số lọc
      · tinh_hinh_di_lam_hom_nay `nhom` [vang_khong_ly_do|di_muon_ve_som|nghi_co_don|cong_tac] ⇒ chỉ nhóm đó + block.people (FE hiện tên)
      · lich_meeting `tu_khoa` (tên/mã, escape %_) + `trang_thai` [len_lich|chot_lich|hoan_thanh|huy]
      · cham_cong_theo_ngay `chi_ngay` [di_muon|ve_som|thieu_cham] (+ tong_so_ngay, loc)
      · viec_cua_nhan_vien `status` / `uu_tien` / `tu_khoa`; viec_qua_han `uu_tien` / `tu_khoa` (helper ViecCuaToiTool::extraFilters)
      · phieu_dat_phong_cua_toi `trang_thai` [cho_duyet|da_duyet|tu_choi|da_huy|hoan_thanh]
      · bien_ban_va_viec_giao `viec` [chua_xong|da_xong|qua_han] ⇒ chỉ dòng có việc khớp (+ loc_viec, so_viec_khop)
      PHPUnit +7 (Agent 270/273, 3 lỗi sort_order cũ); eval +9 câu; e2e +1 (thẻ hôm nay có tên): 3/3 ca liên quan.
      AI thật Haiku local: 8/8 câu truyền đúng tham số lọc (~270 ₫). thieu_cham chưa có test dữ liệu thật.
      Ngoài luồng: "Hôm nay PHÒNG TÔI ai đi muộn" với admin scope 4 ⇒ tra toàn công ty (không truyền phong_ban_id) — có từ trước.
- [x] 16/11 commit api 8510e95cb · client 5de4811ef, gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE: EXIT 0, Nothing to migrate, prompt có luật 12, bundle có khối mới, site 200.

## Đợt 3 (16/11 chiều) — nhớ meeting đã tra + phạm vi toàn công ty + bỏ thẻ trung gian — nhánh `gop_db-agent-nho-meeting` (api, từ 8510e95cb)
User báo trên prod (#55–#59): (1) "họp giao ban toàn công ty hôm nay" ⇒ Agent tra lịch cá nhân; (2) hỏi danh sách nhân sự họp
giao ban 47 48 ⇒ kèm thẻ 20 meeting thừa, danh sách người bị đẩy xuống cuối; (3) câu trước đã có cuộc họp mà vẫn tìm lại.
Gốc: history chỉ gửi chữ trả lời (không có mã meeting) · meeting_cua_phong không tìm được theo tên · runner hiện thẻ của MỌI bước.
- [x] `meeting_cua_phong` thêm `tu_khoa` (tên/mã, escape %_); mô tả: câu nêu phạm vi ⇒ công cụ này (590 ký tự).
- [x] `lich_meeting` mô tả: nêu phạm vi ⇒ meeting_cua_phong; có câu về tu_khoa (đợt 2 lệnh thay mô tả không khớp nên THIẾU — đã bù).
- [x] `AgentRunner::knownMeetings()`: "[đã tra: Tên = mã meeting CODE]" từ (a) meeting gọi thẳng bằng mã/id (ok), (b) dòng thẻ
      meetings/meeting mà câu trả lời nêu tên; tối đa 5/lượt; chỉ gửi model.
- [x] `AgentRunner::withoutSteppingStones()`: công cụ gọi bằng mã/id có trong 1 dòng của thẻ trước ⇒ bỏ thẻ trước.
- [x] AgentPrompt luật 13 (đúng phạm vi người hỏi nêu; dùng ngay mã/id "đã tra").
- [x] PHPUnit +3 (Agent 273/276, 3 lỗi sort_order cũ); eval +2.
- [x] Haiku thật local (meeting tạm AGRP-*, đã xoá): chuỗi 4 câu của user ⇒ "toàn công ty" dùng meeting_cua_phong + tu_khoa (1 dòng);
      "danh sách nhân sự … 47 48" ⇒ thanh_phan_meeting thẳng bằng mã (1 bước, 1 thẻ); "vắng có lý do" ⇒ thẳng + lọc.
      Câu mới 2 bước ⇒ chỉ còn 1 thẻ thành phần. ~250 ₫.
- [x] Đã deploy cùng đợt 4 (api 5e9985e24).

## Đợt 4 (16/11 chiều) — câu trả lời chia gạch đầu dòng, in đậm, highlight
User: "câu trả lời văn bản có chia các ý thành các gạch đầu dòng, các giá trị hoặc từ khoá quan trọng in đậm hoặc highlight" — "làm".
- [x] api (cùng nhánh `gop_db-agent-nho-meeting`): AgentPrompt luật 6 viết lại — 1 câu dẫn (+ ":") + tối đa 4 dòng "- " (mỗi dòng 1 ý,
      không chép từng dòng thẻ); **…** cho số/mã/tên/trạng thái chính; ==…== cho điểm cần chú ý, tối đa 2; cấm #, đánh số, bảng |,
      gạch lồng. Luật 11 đổi theo (gạch cuối = đề xuất).
- [x] client nhánh `gop_db-agent-tra-loi-gach-dau-dong` (từ 5de4811ef): `utils/agentAnswerFormat.js` (escape trước, rồi chỉ nhận
      gạch đầu dòng / ** / ==; đang gõ dần ẩn dấu chưa đóng; bản thuần cho thẻ thiếu quyền + chữ tạm); AgentTurn dùng + CSS
      (ul disc, mark nền #fef3c7 chữ #92400e).
- [x] Haiku thật 5 câu: đúng khuôn (output ~100–720 token, 15–153 ₫). PHPUnit Agent 273/276 (3 lỗi sort_order cũ).
- [x] e2e +1 "khuôn trả lời" (3 li, 4 b, 2 p, mark nền rgb(254,243,199), không lộ **/==, <img> hiện thành chữ): 5/5 ca liên quan.
- [x] 16/11 commit api 5e9985e24 · client 09c8a4489 (đợt 3 + 4), gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE.

## Đợt 5 (16/11 tối) — rà soát "nhớ đối tượng / thẻ trung gian / phạm vi" trên toàn bộ công cụ — nhánh `gop_db-agent-ra-soat-pham-vi` (api, từ 5e9985e24)
User chọn "1" (làm cả 3 mục).
- [x] Nhớ đối tượng mọi loại: knownMeetings ⇒ DIRECT_LOOKUPS (thanh_phan/chi_tiet/bien_ban meeting, chi_tiet_nhiem_vu, chi_tiet_du_an_tkt,
      chi_tiet_giai_phap) + mọi dòng thẻ có code mà câu trả lời nêu TÊN hoặc MÃ; nhãn loại theo link (LINK_KINDS); tối đa 6/lượt; lỗi bảng ⇒ bỏ qua.
- [x] Thẻ trung gian: id trong link `/…/{id}`, `/{id}/show`, `/{id}/manager`; chỉ xét tham số định danh (ma_hoac_id, meeting_id, code, id, ma, ma_hoac_ten).
- [x] Phạm vi: don_cua_phong `nhan_vien_id` (employees.id ⇒ employee_infos.id; bỏ ép phòng người hỏi; applyViewScope vẫn chặn);
      bang_cong_nhan_vien `chi_ngay` [di_muon|ve_som] (từ timesheet_summaries); tinh_hinh_di_lam_hom_nay `pham_vi` [phong|cong_ty];
      công cụ MỚI `viec_cua_phong` (phòng/công ty · status / uu_tien / tu_khoa / hạn; không status ⇒ chưa xong; quyền như viec_qua_han).
      Mô tả viec_qua_han trỏ sang viec_cua_phong. Registry 47 công cụ.
- [x] PHPUnit +7 (Agent 279/282, 3 lỗi sort_order cũ); eval +4 (1 câu nối tiếp có history).
- [x] Haiku thật local 8 câu: đều đúng công cụ + tham số; câu nối tiếp gọi thẳng chi_tiet_nhiem_vu / chi_tiet_du_an_tkt bằng mã (1 bước, 1 thẻ).
- Ngoài luồng: "dự án mới nhất" ⇒ du_an_tkt trả 20 dòng (công cụ danh sách chưa có tham số số lượng) — chưa sửa.
- [x] 16/11 commit api 76dbd1641, gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE (EXIT 0, Nothing to migrate, registry có viec_cua_phong, site 200).
