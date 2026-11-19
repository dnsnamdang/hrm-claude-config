# Agent — Chọn model (cấu hình hệ thống) + so sánh model — TÓM TẮT

> 15/11/2026 · @namdangit · Spec đầy đủ: `docs/superpowers/specs/agent-chat/2026-11-15-agent-chon-model-design.md`
> Trạng thái: CODE XONG 15/11 (nhánh gop_db-agent-chon-model, chưa push) — đã so sánh thật 50 câu (DeepSeek Flash 100% đúng công cụ, ~8 lần rẻ hơn Sonnet) — chờ user quyết. Checkpoint: plan.md cuối file.

**Mục đích (user):** đổi model Agent để tối ưu chi phí + so sánh chất lượng (Claude ↔ DeepSeek…).

**Quyết định đã chốt**
- Đánh giá chất lượng = **1 + 3**: thống kê theo model khi chạy thật + lệnh so sánh bộ câu hỏi mẫu trên nhiều model (Excel đặt cạnh nhau). 👍/👎 để sau.
- Phạm vi: **1 model cho toàn hệ thống**, người có quyền **Cài hạn mức** (`assign.tpe_agent_cai_dat.manage`, dùng lại — user chốt 15/11) đổi.
- Phương án **A**: danh mục model khai trong `Modules/Agent/Config/config.php` (key ở `.env`), DB lưu model đang dùng (`agent_system_settings`, cache, lịch sử đổi), popup "Cấu hình model" trên màn Thống kê Agent, `agent:eval --models=a,b` xuất Excel, Thống kê có lọc + bảng theo model.
- DeepSeek dùng cổng tương thích Anthropic (`https://api.deepseek.com/anthropic`) ⇒ dùng lại `HttpClaudeClient`. Giá ghi mức giờ cao điểm.
- Lối vào: popup trên màn Thống kê ⇒ người chọn model phải có **cả** quyền Xem thống kê (user chốt 15/11).
- Chốt của Claude: có lựa chọn "Dùng mặc định máy chủ" (NULL) · lịch sử theo khuôn SettingHistory (bảng `agent_system_settings_history`) · lọc model ⇒ ẩn khối Ngân sách.
- Đã loại: B (CRUD model trên web), C (chạy so sánh từ web).
