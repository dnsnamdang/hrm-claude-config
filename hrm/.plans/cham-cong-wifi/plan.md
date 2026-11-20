# Chấm công qua WiFi công ty — plan

@namdangit · Repo dự kiến: hrm-api · hrm-client · TPE_APP · Nhánh: chưa chọn

## Phase 0 — Brainstorm + thiết kế

- [x] 19/11/2026 Đọc hiện trạng: máy chấm công (`TimeWorkingService`), app chấm GPS (`ui/check_in_out`, API `v1/timekeeper*`), nơi chấm = JSON trong `working_shifts.place`, bán kính ở `general_regulations`, `locations` không phải danh mục văn phòng
- [x] 19/11/2026 Chốt lý do: nhân viên quên chấm ⇒ tự động
- [x] 19/11/2026 Chốt cách: geofence đánh thức app + xác nhận WiFi (BSSID) + API chấm hiện có
- [x] 19/11/2026 Chốt: chỉ tự chấm giờ vào; giờ ra chấm tay + nhắc
- [x] 19/11/2026 Chốt: bật theo nơi chấm
- [ ] Chốt nơi cấu hình: danh mục "Văn phòng chấm công WiFi" (khuyên) hay WiFi trong từng ca
- [ ] Chốt các câu hỏi còn lại (spec §7: khung giờ, nhắc giờ ra, tắt tự chấm, quyền, thông báo, báo cáo, phát hành)
- [ ] Mockup web (màn cấu hình) + app (xin quyền, thêm WiFi, thông báo)
- [ ] Hoàn thiện spec + duyệt
- [ ] Lên plan code (writing-plans) — chia phase BE / web / app
- [ ] Hỏi riêng cho phép code (repo · nhánh · bảng · migration)

### Checkpoint — 19/11/2026
Vừa hoàn thành: brainstorm vòng 1 — chốt lý do, cách làm (geofence + WiFi), chỉ giờ vào, bật theo nơi chấm; ghi design + spec.
Đang làm dở: câu hỏi "cấu hình ở đâu" (1 danh mục văn phòng / 2 trong từng ca) — đã hỏi, user chưa trả lời.
Bước tiếp theo: lấy câu trả lời câu cấu hình → hỏi lần lượt spec §7 → mockup → viết plan code.
Blocked:
