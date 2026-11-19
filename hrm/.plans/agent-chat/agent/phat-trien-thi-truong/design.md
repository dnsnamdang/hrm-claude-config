# Agent — câu hỏi thị trường theo báo cáo "Phát triển thị trường - Khách hàng" (17/11/2026)

Phụ trách: @namdangit · Spec đầy đủ: `docs/superpowers/specs/agent-chat/2026-11-17-agent-phat-trien-thi-truong-design.md`
Trạng thái: thiết kế hoàn chỉnh, chờ user duyệt. Chưa đụng source.

## Tóm tắt
- "Kế hoạch đi thị trường của NV / phòng" = meeting CÓ KHÁCH HÀNG; nguồn số = báo cáo `assign/report/customer-market-development`
  (`CustomerMarketDevelopmentService`).
- Công cụ mới `phat_trien_thi_truong` gọi thẳng service báo cáo: chế độ **tổng hợp** (dải tổng hợp + cây theo Tiêu chí theo dõi
  mk / cus / dp, mỗi dòng 8 chỉ tiêu) và **chi tiết** (danh sách theo 1 chỉ tiêu, như popup).
- Thẻ FE mới `market_tree` + `market_list`; chi tiết dạng meeting dùng lại thẻ `meetings`.
- Quyền: mã `presale.bao_cao_phat_trien_thi_truong_khach_hang.view`, chặn trước khi gọi service (tránh service tự thu về mức self).

## Quyết định đã chốt
- 17/11: cách 1 — công cụ mới gọi service báo cáo (không sửa `meeting_theo_thi_truong`, không chỉ sửa prompt).
- 17/11: cấu trúc trả lời bám Tiêu chí theo dõi + cột bảng + popup chi tiết của báo cáo.
- 17/11 Q1: mặc định công ty đang làm; `pham_vi=tap_doan` (quyền Tổng công ty) khi hỏi rõ toàn tập đoàn; câu trả lời nêu phạm vi.
- Claude tự chốt (user soát): `bo_phan_id` + người quản lý bộ phận qua guard; mặc định bung tới NV ▸ Thị trường; trần 60 dòng
  cây / 50 dòng chi tiết; nhóm "Không thuộc bộ phận" / "Chưa xác định phòng ban" chỉ xem trên báo cáo.
