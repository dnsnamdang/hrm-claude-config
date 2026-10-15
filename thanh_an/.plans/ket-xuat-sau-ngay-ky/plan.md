# Plan — Chỉ kết xuất HĐ sang cung ứng từ ngày ký trở đi

> @khoipv — Bắt đầu 05/10/2026

## Yêu cầu
Kết xuất HĐ sang cung ứng chỉ được làm khi đã tới ngày ký HĐ (`contracts.contract_sign_time`, datetime).
- So theo NGÀY (bỏ giờ): hôm nay >= ngày ký → cho kết xuất; ngày ký ở tương lai → chặn.
- HĐ cũ không có ngày ký (NULL) → chặn, báo chưa có ngày ký.
- Chặn ở bước GỬI kết xuất (`renderSupply`, 3/11 → 10). Bước duyệt luôn diễn ra sau bước gửi nên không cần chặn lại.

## Phase 1 — BE
- [x] `ContractService::renderSupply()` — thêm guard ngày ký (throw Exception → 400, FE toast message sẵn có)
- [x] Kiểm tra cú pháp PHP (`php -l`)

## Phase 1b — Ẩn nút khi chưa tới ngày ký (user báo HD-193/2026 ký 14/10 vẫn hiện nút)
- [x] `Contract::canRenderSupply()` — thêm điều kiện có ngày ký + hôm nay >= ngày ký → ẩn nút ở DS HĐ và chặn vào thẳng `render.vue`
- [x] Test tinker (không lưu DB) với HĐ 221: ký 14/10 → false · ký hôm nay → true · ký hôm qua → true

## Phase 2 — FE
- [x] Không cần sửa: `render.vue` đã toast `error.response.data.message` với lỗi khác 422

### Checkpoint — 05/10/2026
Vừa hoàn thành: guard ngày ký ở BE + ẩn nút qua canRenderSupply()
Đang làm dở:
Bước tiếp theo: user test với HĐ có ngày ký tương lai / hôm nay / quá khứ
Blocked:
