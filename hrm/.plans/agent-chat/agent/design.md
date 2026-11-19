# TPE SMART AGENT — tóm tắt thiết kế (@namdangit)

> Spec đầy đủ: `docs/superpowers/specs/agent-chat/2026-11-11-tpe-smart-agent-design.md` · Plan: `plan.md` · Ý tưởng / tư vấn: `y-tuong.md`
> Mockup: `.plans/gop-db/phan-he-cong-viec/gd0-mockup/screens/33-tro-ly-erp.html`, `34-thong-ke-tro-ly.html`

- **Mục đích (user 11/11):** demo giới thiệu giải pháp cho khách — ấn tượng, mượt, trả lời chính xác, thể hiện rõ ai được hỏi gì và bị chặn khi quá quyền.
- **Phạm vi đợt 1:** chỉ ĐỌC, phân hệ Công việc (nhiệm vụ, lịch họp, quá hạn, xếp hạng hoàn thành). Không ghi dữ liệu, không lương/giá vốn/công nợ, chưa `@Agent` trong chat nhóm, chưa app.
- **Quyết định lớn:**
  - Agent chạy với danh tính + công ty đang làm của người hỏi (job `auth()->onceUsingId`), không có tài khoản Agent siêu quyền.
  - Công cụ kiểm quyền TƯỜNG MINH trước khi đọc (dùng mã sẵn có `assign.danh_sach_task.view`, `assign.bao_cao_hieu_suat_nv.view`…) ⇒ thiếu quyền trả "bị chặn + tên quyền", không truy vấn.
  - Số liệu trên thẻ do server dựng từ kết quả công cụ; model chỉ viết câu dẫn.
  - SDK PHP chính thức `anthropic-ai/sdk` ^1.8 ⇒ cần **PHP 8.1** (prod TPE đã 8.1.34; local 7.4 phải nâng). **Chỉ cổng TPE**, cổng khác cập nhật sau.
  - Model mặc định Sonnet 5.5, effort low; queue riêng `agent` (retry_after 180); realtime qua kênh Redis sẵn có + sự kiện socket mới `agent`.
  - Đo token + chi phí từng lượt theo bảng giá có ngày hiệu lực; hạn mức câu/ngày theo **Chức vụ trong hồ sơ nhân viên** (chức vụ cài riêng > nhóm chức vụ > chưa khai chức vụ) + ngân sách tháng công ty.
  - 3 mã quyền mới: `assign.tpe_agent.use`, `assign.tpe_agent_thong_ke.view`, `assign.tpe_agent_cai_dat.manage`.
  - Nút "Xem như" chỉ có ở mockup demo; bản thật demo bằng 3 tài khoản.
- **Còn mở (AI2):** model + trần chi phí · API key / tài khoản Anthropic · ZDR · nhóm thử.

## Cập nhật 11/11/2026 (wrap up)
- Model chạy: **Claude Haiku 5.5** (`AGENT_MODEL=claude-haiku-5-5`), ~12 ₫/câu; eval 124 câu 98.4% công cụ / 99.2% kind. Cache prompt 5 phút (theo dõi `pct_ghi`, xem plan.md).
- Phạm vi mở rộng: Công việc · Meeting · Chấm công · Lương (tắt) · **CSKH trước bán** (dự án TKT, meeting theo thị trường = tỉnh KH, giải pháp, khách hàng). 33 công cụ.
- Quyết định KD trước bán (5 câu đã chốt): `de-xuat-kd-truoc-ban.md` mục 3. Mở rộng tham số các đối tượng: `tu-van-mo-rong-tham-so.md`. Cách thêm công cụ cho team: `huong-dan-them-cong-cu.md`.
- Chưa commit — worktree `websites/wt-tpe-agent`, nhánh `gop_db-tpe-smart-agent`.

## Cập nhật 12/11/2026 (wrap up)
- 43 công cụ (45 khi bật lương). Thêm cho lãnh đạo: `bao_gia`; `tinh_trang_phong_hop` + `phieu_dat_phong_cho_toi_duyet`;
  `thong_ke_cham_cong` (Support/ChamCongTongHop — SQL khớp Bảng chấm công chi tiết), `phep_nhan_vien`, `thong_ke_cong_tac`;
  `thong_ke_giai_phap` + `chi_tiet_giai_phap` (Support/GiaiPhapScope — phạm vi 2 báo cáo). Đặc tả: `de-xuat-lam-giai-phap.md`,
  plan.md các mục 12/11.
- Nguyên tắc nguồn số: công (mọi công cụ, kể cả của chính mình) = Bảng chấm công chi tiết; công tác = ngày có chấm công CT;
  thống kê lấy phạm vi quyền của BÁO CÁO tương ứng, danh sách lấy phạm vi màn danh sách.
- Prompt luật 10: không đánh giá lại / đính chính câu trả lời lượt trước (lịch sử chỉ gửi câu hỏi + câu trả lời).
- Ghim Agent trong Tin nhắn (`de-xuat-ghim-agent-trong-chat.md`): `AgentWorkspace.vue` dùng chung /agent + `/assign/messages?agent=1`;
  điều kiện quyền "Dùng TPE SMART AGENT" + mục menu Agent không tắt. Nhánh Agent đã gộp nhánh chat ⇒ lên gop_db cùng/sau chat.
- Chi phí ~20 ₫/câu, tăng ~0.4 ₫ mỗi công cụ thêm (mô tả công cụ = 88% phần cố định) — phương án giảm đang tạm hoãn (plan.md).
