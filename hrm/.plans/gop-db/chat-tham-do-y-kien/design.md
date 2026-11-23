# Chat nhóm: Cuộc thăm dò ý kiến — thiết kế (@cuong61n)

Nhánh `gop_db`. Tham chiếu hình thức: Pencil `meeting-mobile_v2.pen` (6+1 khung: App · Gửi kèm · Tạo thăm dò · Bong bóng · Người bầu · Ẩn kết quả; Web · Khung chat · Popup tạo). Hành vi theo Messenger/Zalo.

## Quyết định đã chốt
- Tin chat mới `type = poll` (body = câu hỏi), dữ liệu ở 3 bảng: `chat_polls`, `chat_poll_options`, `chat_poll_votes` (migration `2026_11_23_000001`). Không dùng cột `meta`, không mượn bảng cảm xúc.
- Tạo được trong nhóm (space/group), KHÔNG chat 1–1. Ai gửi được tin thì tạo được; vai trò Xem chỉ xem.
- 2–10 lựa chọn (≤100 ký tự, không trùng, không phân biệt hoa thường), câu hỏi ≤200.
- Tuỳ chọn: `multiple` (chọn nhiều đáp án, mặc định tắt) · `allow_add_option` (thành viên thêm lựa chọn, mặc định BẬT) · `hide_results` (ẩn kết quả khi chưa bình chọn, mặc định tắt) · `closes_at` (hạn đóng, tuỳ chọn).
- Bầu = gửi TẬP lựa chọn của mình (thay cả tập; rỗng = bỏ phiếu); đổi ý tuỳ ý đến khi đóng.
- Đóng: người tạo hoặc Quản lý nhóm; hoặc quá `closes_at`. Đã đóng: không bầu / thêm / đóng lại, vẫn xem hết kết quả.
- Ẩn kết quả: CHỐT CHẶN Ở BE. Người chưa được xem (chưa bầu, không phải người tạo, chưa đóng) nhận `results_visible=false`, mọi số phiếu / người bầu = null, API người bầu trả 422. Bỏ phiếu rồi thì lại bị ẩn.
- Thứ tự lựa chọn: người xem ĐƯỢC THẤY kết quả ⇒ lựa chọn nhiều phiếu nhất lên trước (bằng phiếu giữ thứ tự tạo); đang ẨN kết quả ⇒ giữ thứ tự tạo (sắp theo phiếu sẽ làm lộ lựa chọn dẫn đầu). BE sắp (`PollPresenter::sortByVotes`, áp cho cả gói socket trung lập và API người bầu); web/app hiển thị đúng thứ tự BE trả, KHÔNG tự sắp lại. Bầu xong thì thứ tự có thể đổi ngay.
- Tin thăm dò: không sửa, không thu hồi, không chia sẻ (có Xoá ở phía tôi như tin khác). Xem trước hội thoại: `[Thăm dò] <câu hỏi>`.
- Không thêm mã quyền (chat không dùng mã quyền, kiểm theo vai trò trong nhóm).

## API (prefix `v1/assign/chat`, trả tin ĐÃ dựng góc nhìn của người gọi — cùng dạng `messages[]`, thêm khoá `poll`)
| | Route | Middleware |
|---|---|---|
| Tạo | `POST conversations/{id}/polls` {question, options[], multiple?, allow_add_option?, hide_results?, closes_at? `Y-m-d H:i:s`} | send |
| Xem bản của tôi | `GET messages/{messageId}/poll` | read |
| Bầu | `POST messages/{messageId}/poll/vote` {option_ids: []} | send |
| Thêm lựa chọn | `POST messages/{messageId}/poll/options` {text} | send |
| Đóng | `POST messages/{messageId}/poll/close` | send |
| Người bầu | `GET messages/{messageId}/poll/voters` → {options:[{id,text,vote_count,voters:[person + voted_at]}]} | read |

Lỗi luật: 422 `{code, errors:{<trường>: "<câu>"}}` (trường `poll` / `option_ids` / `options` / `text` / `question`).

## Khoá `poll` của tin
`{id, question, multiple, allow_add_option, hide_results, closes_at, closed, closed_at, closed_by_name, results_visible, total_voters|null, my_option_ids[], options:[{id, text, vote_count|null, voter_ids[]|null, voters:[person≤4]}], can_vote, can_add_option, can_close}`
- Realtime: gói socket `message.created` / `message.updated` mang bản TRUNG LẬP (viewer 0): `my_option_ids=[]`, `can_* = false`; chỉ có số phiếu khi không ẩn hoặc đã đóng. FE phải **tự dựng phần của mình**: `my_option_ids` = các lựa chọn có `voter_ids` chứa id mình; `can_vote` = !closed && mình gửi được tin trong hội thoại; `can_add_option`/`can_close` tương tự (người tạo = `sender_id`). Nếu `results_visible=false` mà mình đã bầu / là người tạo ⇒ gọi `GET .../poll` lấy bản của riêng mình (debounce).
- `closed` tính theo giờ máy chủ; FE hết hạn theo `closes_at` thì coi là đã đóng và gọi lại `GET .../poll`.

## Việc còn lại
- [ ] Web `hrm-client` (ChatComposer nút Thăm dò + popup tạo + bong bóng trong `ChatMessageItem` + popup người bầu).
- [ ] App `TPE_APP` (mục Gửi kèm + màn tạo + bong bóng + màn người bầu).
