# Design (tóm tắt) — GĐ2: Nhiệm vụ trong Nhóm trao đổi + nối chat (web)

- **Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-11-gd2-nhiem-vu-trong-nhom-design.md`
- **Phụ trách:** @namdangit · **Ngày:** 11/11/2026 · **Trạng thái:** CODE XONG 12/11/2026, chưa merge, chưa push
- **Nền:** core chat (nhánh `gop_db-nhom-trao-doi`, worktree `websites/wt-nhom-trao-doi/`) + Nhiệm vụ v2 (`TaskPanel`)

## Phạm vi (user chốt 11/11)
- LÀM: khối 1 (Nhiệm vụ thuộc nhóm) + khối 2 (`#` thẻ việc, tạo nhiệm vụ từ tin).
- ĐỂ SAU: Vấn đề · tin tự báo theo sự kiện việc (khối 3) · tab Meeting / File (khối 4) · Dự án KH · app.

## Quyết định đã chốt
| # | Chốt |
|---|---|
| Q1 | Tab Nhiệm vụ trong nhóm đúng mockup 03 (danh sách gom nhóm + Bảng) |
| Q2 | Người làm bắt buộc là Quản lý / Thành viên của nhóm |
| Q3 | Ô Nhóm có ở mọi form `TaskPanel`, không bắt buộc, sửa được |
| Q4 | `#` chỉ chọn việc của nhóm; chat 1–1 không có `#` |
| Q5 | Tạo từ tin ⇒ tự gửi thẻ trả lời tin gốc |
| Q6 | Chặn bớt / hạ Xem người còn việc dở trong nhóm |
| Q7 | Thao tác trên việc theo vai trò trên việc (người duyệt ngoài nhóm vẫn duyệt) |
| Q8 | Việc của nhóm KHÔNG thêm vào màn Nhiệm vụ chung / export / báo cáo |

## Điểm chính
- `tasks.workspace_id` + `tasks.source_message_id` (nullable). Nhóm ⟂ Giải pháp / Dự án TKT.
- `TaskAccess`: bịt lỗ hổng `TaskController::show` / update — xem = (a)+(b) đúng query danh sách + (c) thành viên nhóm.
- `V2BaseMiniTab` (component chung mới — hỏi trước khi tạo) cho cụm nút đầu nhóm; mục "Tab sử dụng" dựng mới.
- Đóng nhóm / tự lưu trữ ⇒ huỷ việc dở (1 hàm dùng chung).

## Đã triển khai (12/11/2026)
Task 1–11 xong trên nhánh `gop_db-nhom-trao-doi` (hrm-api `ef87152cb` · hrm-client `b6b9e4c6f`; nay đã merge gop_db — xem mục dưới). API/field thực tế ghi ở spec mục 11; ghi chú + checkpoint ở `plan.md`.

## Đợt Z + dọn tồn (12/11/2026 tối) — quyết định đã chốt
| # | Chốt |
|---|------|
| Z1 | Thanh thao tác tin kiểu Zalo: rê chuột vào tin ⇒ Trả lời · Chia sẻ · Tạo nhiệm vụ · ⋯ (Ghim/Bỏ ghim · Sao chép · Sửa · Thu hồi), có tooltip. Cảm xúc RA KHỎI thanh: nút 👍 ở góc bong bóng, rê vào mới hiện hàng emoji |
| Z2 | Chia sẻ = chọn NHIỀU hội thoại mình gửi được tin (nhóm + 1–1) + lời nhắn tuỳ chọn (thành tin riêng). `POST chat/messages/{id}/forward`; 1 đích không gửi được ⇒ 422 cả lô. Tin chia sẻ hiện "Chia sẻ từ <người gửi gốc>" (chỉ lộ tên), giữ người gốc qua nhiều lần chia sẻ, KHÔNG sửa được (vẫn thu hồi). Vai trò Xem vẫn chia sẻ RA được. Không chia sẻ tin hệ thống / thẻ / đã thu hồi |
| Z3 | "Tạo vấn đề từ tin" — HOÃN (làm sau) |
| U1 | Tab Nhiệm vụ nhóm: nút "+ Thêm" ở đầu nhóm |
| U2 | Nút ⇄ đổi trạng thái: không đổi được ⇒ hiện mờ + tooltip lý do (ngoại lệ có chủ đích với quy tắc "ẩn nút", user chốt theo spec gốc) — lý do mirror `Task::getAllowedNextStatuses` ở `statusLockReason()` |
| U3 | Tạm dừng hỏi lý do (tuỳ chọn, ≤1000) — cả tab nhóm lẫn TaskPanel dùng chung |
| U4 | Nhãn "Dự án / Nhóm" ⇒ "Dự án" (form + lịch sử BE). Màn Vấn đề còn nhãn cũ — chưa sửa |
| — | Màn danh sách nhóm (mockup 01) — BỎ |

Commit: Đợt Z api `4749f0165` / client `26cd19d42`; ĐÃ MERGE + PUSH `gop_db` 12/11 (api `174892532`, client `72b7a3bb3`). Deploy: 5 migration Assign `2026_11_13_000001..000004` + `2026_11_14_000001`, restart node socket.
