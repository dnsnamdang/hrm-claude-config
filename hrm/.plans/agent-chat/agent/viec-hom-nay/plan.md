# Agent — "Hôm nay tôi có việc gì cần làm": thẻ chia nhóm theo loại (18/11/2026)

Yêu cầu user: câu trả lời tạm ổn, bảng chi tiết bên dưới cần chia nhóm như gạch đầu dòng của câu trả lời.
Chốt: thứ tự nhóm CỐ ĐỊNH (Nhiệm vụ → Vấn đề → Meeting → Phiếu giao việc → Phiếu công tác → Nhắc việc) · mỗi nhóm tối đa 5 dòng + "Còn N … · Mở Việc của tôi".

- [x] hrm-api `ViecTongHopCuaToiTool`: ≥ 2 loại ⇒ `data.nhom` [{loai, so_viec, so_qua_han, dang_hien, con_lai}] + `block.sections` + `block.link_more=/assign/my-todo`; trong nhóm quá hạn lên trước; 1 loại ⇒ như cũ (≤ 20 dòng, `con_lai` khi bị cắt); `ghi_chu` "Thẻ hiện x/y việc"
- [x] AgentPrompt quy tắc 20: mỗi gạch đầu dòng = 1 nhóm, đúng thứ tự `nhom`, tên loại + số việc + 1 việc nổi bật
- [x] hrm-client `AgentResultBlock.vue` (thẻ tasks): đầu nhóm (icon loại · tên · số · "n quá hạn" đỏ), bỏ chip loại trên từng dòng khi đã chia nhóm, dòng "Còn N …" link màn Việc của tôi; không có sections ⇒ danh sách phẳng như cũ
- [x] Test `test_viec_tong_hop_chia_nhom_theo_loai`; bộ Agent 413/413 (1 lần chạy có 1 ca đỏ chưa rõ ca nào, 3 lần sau xanh — theo dõi)
- [x] Playwright :3070, NV 13: 4 nhóm Nhiệm vụ 7 · Vấn đề 1 · Meeting 6 · Nhắc việc 12, 15 dòng, không chồng lấn / tràn ngang; câu trả lời 4 gạch đầu dòng đúng thứ tự thẻ
- [x] 18/11 user chọn: trong nhóm việc hạn TRONG khoảng hỏi (hôm nay) lên trước, rồi quá hạn cũ (trước đó quá hạn trước ⇒ việc hôm nay bị đẩy vào "Còn N"); hỏi không theo khoảng ⇒ vẫn quá hạn trước. Kiểm thật NV 13: TPE.TASK.NB.26.0045 hạn 18/11 lên đầu nhóm Nhiệm vụ, câu trả lời cũng nêu nó đầu tiên
- [x] 18/11 ĐÃ merge + push gop_db (api 9600a92f0 · client b86b18b95), commit tính năng api 73ac0da2a · client 01420aae6
- [x] deploy TPE — 19/11 đã lên prod theo đợt GĐ35 (api e395dc12d · client a58679286 chứa bản này)

## 25/11/2026 — Điều tra phản hồi ông Phong (Chủ tịch HĐQT): "việc quá hạn đã hoàn thành mà vẫn hiển thị" — @cuong61n
- [x] 25/11 Kiểm code: `ViecTongHopCuaToiTool` hỏi "hôm nay có việc gì" ⇒ hạn hôm nay + `kem_qua_han`; nhắc việc lấy qua `MyTodoService::getPersonalTodosNormalized` chỉ `is_completed = 0` ⇒ việc đã tick KHÔNG thể lọt
- [x] 25/11 Kiểm DB prod `hrm_erp_gop.personal_todos` user 36: 3 việc quá hạn trong ảnh (#223 lễ hội bia 21/11, #309 + #310 nhà máy Hưng Yên 20/11) đều `is_completed = 0`, chưa tick bao giờ; #309/#310 là tạo 2 lần (10:05 và 10:47 ngày 20/11, lần 2 có giao thêm cho user 100). 2 việc hôm nay (#356, #363) tick lúc 08:40 và 08:51, SAU khi chụp ảnh 08:38. Tick của ông vẫn ghi DB bình thường (18–25/11 có 8 việc completed) ⇒ AI trả đúng dữ liệu, không phải lỗi
- [ ] Ghi nhận cải tiến (chưa làm, chờ chốt): `MyTodoService::getAll` sort chỉ theo `due_date`, bỏ `due_time` ⇒ dòng 25/11 18:00 đứng trước 25/11 09:00
- [x] 25/11 User hỏi lại "giao lưu Long toyota giải phóng": #239 là lịch lãnh đạo HÔM NAY 25/11 10:00–18:00, `is_completed = 0`, không có bước con, sửa lần cuối 18/11; chỉ có 1 bản ghi tên này của user 36 ⇒ hiện ở nhóm "hạn hôm nay" là đúng, không phải quá hạn. Toàn bộ việc chưa xong tới 25/11 của user 36 đúng 4 dòng (#309, #310, #223, #239) = khớp ảnh sau khi trừ 2 việc đã tick lúc 08:40/08:51
