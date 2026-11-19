# Đề xuất: Agent tra Phiếu công tác + Phiếu giao việc — 11/11/2026 (user "ưu tiên", CHƯA CODE)

Khảo sát code + dữ liệu (subagent, đã tự kiểm lại các điểm chính): xem mục 1. Nền: `tu-van-mo-rong-tham-so.md` mục 4–5.

## 1. Hiện trạng (đã kiểm)
| | Phiếu công tác | Phiếu giao việc |
|---|---|---|
| Bảng | `assign_requests` **type = 2** (type 1 = phiếu đề xuất) | `assign_jobs` |
| Người | Người đi: `assign_request_employees.employee_id` (= employees.id), `is_leader` trưởng nhóm | Người thực hiện: `assign_job_employees.employee_info_id` (= employee_infos.id — KHÁC loại id) |
| Khách hàng / nơi | Phiếu khác (business_type 2): cột `customer_name`, `place`; phiếu kỹ thuật (1): ở bảng con `assign_business_tasks` (`customer_name`, `work_address`) | `customer_name` (chỉ chữ, không id), `place` |
| Thời gian | `from_time` → `to_time` | hạn `deadline` |
| Trạng thái | 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 5 Chờ duyệt KQ · 6 Không duyệt · 7 Đã duyệt KQ · 8 Đang lập HS thanh toán · 9 Đã lập HS TT · 10 Đang lập đề nghị TT · 11 Đã lập đề nghị TT | 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Từ chối · 5 Chờ duyệt KQ · 6 Đã duyệt KQ |
| Phạm vi màn danh sách | `AssignBusinessService::searchByFilter` (`:71-306`), mã `assign.danh_sach_phieu_giao_cong_tac.view`, **chỉ áp khi `type=all`** (thiếu là KHÔNG lọc gì); ẩn nháp người khác; trả paginator | `AssignJobService::searchByFilter` (`:40-142`), mã `assign.danh_sach_phieu_giao_viec.view`, áp vô điều kiện; KHÔNG ẩn nháp; tham số `employee_info_id` thực ra lọc NGƯỜI TẠO; không lọc người thực hiện / hạn; trả paginator |
| "Của tôi" có sẵn | `MyJobService::getAssignBusinessList`: người tạo HOẶC người đi (Builder) | — |
| API chi tiết | `GET assign/assign_business/{id}` — **KHÔNG kiểm quyền** | `GET assign/assign_jobs/{id}` — **KHÔNG kiểm quyền** (`dd($exception)` khi lỗi) |
| Màn xem FE | `/assign/assign_business/{id}/show` | `/assign/assign_jobs/{id}/show` |
| Panel có sẵn | `WorkItemDetailDrawer` type `assign_business` / `assign_job` (màn Việc của tôi) | như trái |
| DB local | 7,746 phiếu (3: 5,975 · 11: 1,218 · 9: 452 …); NV 13 đi 3 phiếu | 354 phiếu (6: 285 · 3: 54 …); NV 341 / 1017 / 589 thực hiện nhiều nhất; NV 13 = 0 |

## 2. Thiết kế
**`phieu_cong_tac`** — pham_vi: `toi` (mặc định — mình đi HOẶC mình tạo, như MyJob) / `phong` (phòng mình hoặc phong_ban_id) / `cong_ty` / `nguoi` (nhan_vien_id: người ĐI) · `tu_ngay/den_ngay`: phiếu có thời gian GIAO với khoảng (`from_time <= den` và `to_time >= tu`) ⇒ "hôm nay ai đang đi công tác" đúng nghĩa (màn gốc lọc kiểu nằm trọn) · `trang_thai` (cho_duyet, da_duyet, cho_duyet_kq, khong_duyet, da_duyet_kq, thanh_toan = 8–11) · `loai` (ky_thuat / khac) · `khach_hang` (chữ, khớp cột phiếu + bảng con) · `dang_di` (đang trong thời gian công tác lúc hỏi). Trả: tổng, theo trạng thái, ≤ 20 dòng (mã, người đi + trưởng nhóm, khách hàng / nơi, từ – đến, trạng thái).
**`phieu_giao_viec`** — pham_vi: `toi` (mặc định — mình THỰC HIỆN; `vai_tro=tao` = mình tạo) / `phong` / `cong_ty` / `nguoi` (nhan_vien_id: người thực hiện) · `trang_thai` · `khach_hang` (chữ) · `tu_ngay/den_ngay` theo hạn · `qua_han` (hạn đã qua, chưa nhập / duyệt KQ). Trả: tổng, theo trạng thái, ≤ 20 dòng (mã, tên việc, khách hàng, người thực hiện, hạn, trạng thái, quá hạn).
- Quyền: đúng phạm vi màn danh sách của từng loại (mục 3 câu 1); phòng khác / công ty cần phạm vi ⇒ denied + tên quyền (khuôn PresaleScopeGuard). Nháp người khác ẩn ở cả 2.
- Trạng thái + màu: BE Agent giữ bảng riêng đủ mã (MyTodo thiếu 8–11), màu theo 9 mã chuẩn: Đang tạo `#64748B` · Chờ duyệt / Chờ duyệt KQ `#D97706` · Đã duyệt `#2563EB` · Đã duyệt KQ `#16A34A` · Không duyệt / Từ chối `#DC2626` · nhóm thanh toán 8–11 `#7C3AED`.
- Thẻ FE: `tasks` có sẵn, `type` = `assign_business` / `assign_job` ⇒ icon + màu + nhãn theo `work-item-types.js` (đã làm 11/11); bấm ⇒ mở panel `WorkItemDetailDrawer` ngay trên `/agent` (thêm 2 mẫu link `/show` vào `agentOpenTarget`), nút "Mở chi tiết" của panel ⇒ tab mới màn `/show`.
- Eval: ~10 câu ("tuần sau tôi đi công tác đâu", "phiếu công tác của tôi duyệt chưa", "hôm nay phòng tôi ai đang đi công tác", "phiếu công tác chờ thanh toán", "tôi còn phiếu giao việc nào chưa nhập kết quả", "phiếu giao việc chờ duyệt của phòng", "việc lắp đặt cho khách TPSG tới đâu", không quyền ⇒ deny…).

## 3. Câu hỏi chốt (hỏi lần lượt)
1. ✅ (11/11) Tách phần phạm vi thành hàm public dùng chung `applyListScope($query)` ở `AssignBusinessService` (phạm vi nhánh `type=all` + ẩn nháp người khác) và `AssignJobService` (phạm vi vô điều kiện); `searchByFilter` gọi lại ⇒ màn danh sách không đổi hành vi (có test). Agent dùng cùng hàm.

## 4. Ghi thêm (ngoài luồng — vào `va-lo-hong-quyen-doc/ghi-chu.md`)
- #19 `AssignBusinessController::show` không kiểm quyền xem · #20 `AssignJobController::show` không kiểm quyền xem (+ `dd($exception)`).
- `MyJobService::getAssignBusinessList` lọc `parent_code` trên cột không tồn tại ⇒ lỗi SQL nếu truyền.
- `MyTodoService::getUrl` 2 loại phiếu trỏ màn CẬP NHẬT (thiếu `/show`); bảng trạng thái MyTodo + `work-item-types.js` thiếu 8–11 (drawer hiện trạng thái rỗng cho phiếu thanh toán).
