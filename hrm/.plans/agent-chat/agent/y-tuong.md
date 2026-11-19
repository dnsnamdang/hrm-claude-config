# Ý tưởng — Trợ lý AI trong trung tâm chat ERP (tư vấn 11/11/2026, CHƯA chốt)

User 11/11: *"tư vấn ý tưởng tạo 1 AI agent dạng botchat trên hệ thống chat ERP, chat với các user, nhận câu hỏi và trả lời dựa trên các API có sẵn"*.
Trạng thái: **11/11 user chốt thử nghiệm cho phân hệ Công việc, làm cùng đợt Nhóm trao đổi** ("làm thử nghiệm cho phân hệ Công việc cùng đợt với làm Nhóm trao đổi") — việc ghi ở `phan-he-cong-viec/plan.md` mục **GĐ3-AI** (AI0–AI5). Chưa có lệnh code; còn chốt AI2 (model, chi phí, dữ liệu loại trừ, ZDR, nhóm thử, API key).

## Đề xuất đã nêu
1. **Vị trí:** hội thoại 1–1 "Trợ lý" (ghim sẵn) + gọi `@Trợ lý` trong nhóm (chỉ trả lời khi được gọi). Trả lời = tin nhắn thường, dùng lại thẻ việc của chat.
2. **Quyền:** bot chạy với danh tính + công ty đang làm của NGƯỜI HỎI; không có tài khoản bot siêu quyền; mọi kiểm quyền hiện có giữ nguyên; thiếu quyền thì báo, không đoán.
3. **Công cụ:** lớp công cụ riêng 10–20 cái, mỗi cái = 1 câu hỏi nghiệp vụ, bọc service hrm-api có sẵn, trả JSON gọn. Đợt 1 (Công việc): việc của tôi · việc quá hạn của nhóm · chi tiết nhiệm vụ/vấn đề · lịch meeting · tìm nhân viên.
4. **Đọc trước, ghi sau:** đợt 1 chỉ đọc; đợt 2 ghi qua **thẻ đề xuất + nút Xác nhận** (chặn cả prompt injection từ nội dung do người khác viết).
5. **Kiến trúc:** tin nhắn → Job queue Laravel → Claude API + tool use (SDK PHP chính thức, có tool runner) → lưu thành tin nhắn → socket; "Trợ lý đang trả lời…"; log mỗi lượt (câu hỏi, tool, tham số, token, thời gian).
6. **Model / chi phí (ước tính, 33K câu/tháng, ~3 vòng tool, prefix 8K cache):** Opus 5.5 ~$0,05/câu ≈ $1.600/th · Sonnet 5.5 ~$0,025 ≈ $800 · Haiku 5.5 ~$0,001 ≈ $40. Chọn bằng bộ ~50 câu hỏi thật chấm đúng/sai; Opus 5.5 nên để effort `low` cho chat. User quyết model.
7. **Dữ liệu ra ngoài:** chốt trước loại dữ liệu không đưa vào công cụ (lương, giá vốn, công nợ…) + có cần ZDR / khu vực xử lý.
8. **Lộ trình:** thử nghiệm ~2 tuần (5 tool đọc Công việc, 1 nhóm user, 50 câu chấm) → mở rộng đọc theo phân hệ → ghi có xác nhận. Phụ thuộc nền chat (GĐ3 Phân hệ Công việc); muốn thử sớm thì làm khung chat nhỏ riêng trước.

## Định hướng chọn API khi user hỏi (tư vấn sâu 11/11/2026)
- **Không viết bộ định tuyến riêng**: Claude tự chọn công cụ dựa trên tên + mô tả + schema tham số. Chất lượng định tuyến ≈ chất lượng mô tả công cụ.
- **Công cụ = câu hỏi nghiệp vụ, không = endpoint.** Một route REST thô (`GET /tasks` 20 tham số) làm model đoán sai; bọc thành `viec_cua_toi(trang_thai, tu_ngay, den_ngay)`, `viec_qua_han(pham_vi: toi|nhom|phong)`… Bên trong vẫn gọi service có sẵn (vd `TaskController@index`, `SolutionController@peopleWithLateTasks`, `meetingUpcomingSchedule`).
- **Mô tả công cụ viết theo 4 ý:** dùng khi nào · KHÔNG dùng khi nào (chỉ sang công cụ nào) · tham số suy ra thế nào ("hôm nay/tuần này" → ngày cụ thể) · trả về gì.
- **Tham số dùng enum + id**, không nhận chữ tự do cho trạng thái/phạm vi.
- **Phân giải tên → id bằng công cụ tra cứu** (`tim_nhan_vien`, `tim_nhom`, `tim_du_an`): nhiều kết quả → bot hỏi lại user chọn, không đoán.
- **Ngữ cảnh tiêm vào system prompt mỗi lượt:** người hỏi (id, tên, phòng), công ty đang làm, hôm nay + múi giờ, hội thoại đang đứng (nhóm nào → mặc định phạm vi = nhóm đó).
- **Chuỗi nhiều bước:** tra id → gọi công cụ chính → (nếu cần) chi tiết 1 bản ghi. Giới hạn ~5 vòng/câu.
- **Kết quả trả về gọn:** tổng số + tối đa ~20 dòng + link mở màn; cắt cột không cần.
- **Ngoài phạm vi:** không công cụ nào khớp → trả lời "chưa hỗ trợ" + gợi ý màn; thiếu quyền → công cụ trả lỗi quyền, bot báo nguyên văn.
- **Khi mở rộng >~30 công cụ (nhiều phân hệ):** bật cơ chế tìm công cụ của Claude API (tải công cụ theo nhu cầu, `defer_loading`) hoặc gom nhóm theo phân hệ; chưa cần ở đợt thử.
- **Đo:** bộ ~50 câu thật, mỗi câu ghi công cụ + tham số mong đợi → chấm riêng "chọn đúng công cụ" và "trả lời đúng"; log mọi lượt để soát câu chọn sai rồi sửa mô tả.

## Mục đích + yêu cầu demo (user 11/11)
*"mục đích để giới thiệu giải pháp cho khách hàng nên cần ấn tượng, mượt, phản hồi chính xác · thể hiện được việc phân quyền rõ ràng ai được hỏi gì, bị chặn khi quá quyền hạn"*.
- Mockup: `phan-he-cong-viec/gd0-mockup/screens/33-tro-ly-erp.html` (xem plan AI1).
- Hệ quả cho bản thật: hiện "các bước" (kiểm quyền trước, tra sau) là tính năng sản phẩm, không chỉ demo ⇒ log mỗi lượt phải lưu đủ bước; chữ hiện dần ⇒ cần streaming từ Claude API qua socket; chính xác ⇒ ưu tiên model mạnh cho demo (Opus 5.5 / Sonnet 5.5) + bộ 50 câu chấm trước buổi giới thiệu; quá quyền ⇒ công cụ trả lỗi quyền có tên quyền cần, không trả dữ liệu.

## Đếm token theo từng user (tư vấn 11/11)
- Mỗi lần gọi Claude API trả về `usage`: input · output · cache ghi · cache đọc. 1 câu hỏi = nhiều lần gọi (vòng công cụ) ⇒ cộng hết các lần gọi của lượt đó.
- Lưu vào bảng log lượt hỏi (đã có trong đề xuất kiến trúc): user, công ty, phòng ban, hội thoại, model, 4 loại token, số lần gọi, công cụ đã dùng, kết quả (trả lời / chặn / không hỗ trợ), thời gian, chi phí quy đổi.
- Chi phí tính từ bảng giá cấu hình được (theo model, theo ngày hiệu lực), không hard-code; lưu token thô để tính lại khi giá đổi.
- Báo cáo Usage/Cost của Anthropic Console chỉ tổng theo tài khoản / API key / model, KHÔNG biết user ERP ⇒ số theo user phải tự lưu; dùng số Anthropic để đối soát tổng tháng.
- Có số theo user thì làm được: hạn mức ngày/tháng theo user hoặc vai trò, trần ngân sách công ty (vượt ⇒ báo nhẹ nhàng, không gọi API), báo cáo theo phòng ban, cảnh báo khi dùng bất thường.
