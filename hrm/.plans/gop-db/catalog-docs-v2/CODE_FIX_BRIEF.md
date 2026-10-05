# Brief sửa code danh mục theo nguyên tắc (user chốt 26/09/2026)

Nhánh gop_db. BE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api`, FE `/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client`, DB local `mysql -h127.0.0.1 -uroot local_hrm_erp`, API local http://127.0.0.1:8003 (php -S).
⚠️ Worktree DÙNG CHUNG nhiều phiên: KHÔNG commit, KHÔNG stash, KHÔNG reset/checkout file. Chỉ sửa file của màn được giao; file dùng chung (vd `app/ExcelExport/ExportColumnRegistry.php`, `app/Http/Kernel.php`, route file chung) chỉ sửa đúng đoạn của màn mình bằng Edit nhỏ, đọc lại ngay trước khi sửa (agent khác có thể đang sửa song song).

Đọc trước: `/Users/manhcuong/Desktop/dns/HRM/CLAUDE.md` (bản ghi khoá chặn BE 423; nút không dùng được thì ẨN; V2Base*; message lang file; BaseModel/updated_by; lịch sử; hiệu năng — không N+1) và skill `/Users/manhcuong/Desktop/dns/HRM/.claude/skills/` (list-page, modal-popup, form-validate, entity-history, select-and-input-state, unsaved-changes).

KHUÔN MẪU BẮT BUỘC COPY: màn Quận/Huyện vừa làm xong —
- BE `Modules/Human/Entities/District.php` (LOCKED_MESSAGE, USED_MESSAGE, USAGE_REFERENCES, isLocked(), isUsed(), canDelete(), usedIds(array $ids) — 1 query/bảng cho cả trang), `Modules/Human/Services/DistrictService.php` (list hiện cả 2 trạng thái + lọc status; create/update nhận status + log đổi trạng thái; lock()/unlock() có GuardsCatalogStatus; deleteXxx() XOÁ CỨNG + log), controller lock/unlock/delete, routes `PUT /{id}/lock`, `PUT /{id}/unlock`, `PUT /{id}` và `DELETE /{id}` gắn middleware `recordNotLocked:id,<EntityClass>`, Resource trả `status_text`, `is_locked`, `is_can_delete`, request rule `status nullable|in:0,1`.
- FE `pages/human/districts/index.vue` + `components/DistrictModel.vue`: ô Trạng thái trong popup (mặc định Hoạt động), cột badge + bộ lọc Trạng thái, hành động: Sửa (chỉ khi Hoạt động), Xóa (chỉ khi Hoạt động && is_can_delete), Khóa/Mở khóa, Lịch sử; hộp xác nhận chung BaseConfirmModal/$confirm; toast lỗi hiện đúng câu BE.

NGUYÊN TẮC (user chốt):
1. KHÔNG xoá mềm. Xoá = XOÁ CỨNG, chỉ khi bản ghi đang Hoạt động và CHƯA được dùng. Đã dùng → FE ẩn nút Xoá, BE chặn câu nghiệp vụ "<Đối tượng> đang được sử dụng, không thể xóa." (400). Bỏ mọi nhánh "xoá thành khoá".
2. "Đã dùng" = có ít nhất 1 dòng ở BẤT KỲ bảng nào có cột id trỏ tới bản ghi (tra information_schema các cột `<tên>_id` / tên tương đương + grep code). KHÔNG tính cột chỉ lưu TÊN bằng chữ. Liệt kê đủ vào USAGE_REFERENCES.
3. Có Khoá / Mở khoá (endpoint + nút), CHO KHOÁ CẢ KHI BẢN GHI ĐANG ĐƯỢC DÙNG (bỏ luật cấm khoá nếu có). Bản ghi khoá vẫn hiển thị đúng ở chứng từ cũ (🔒 qua `is_locked` — skill select-and-input-state mục 1), chỉ không chọn được ở chứng từ mới.
4. Popup/form Tạo-Sửa có ô Trạng thái (Hoạt động/Khóa), mặc định Hoạt động. Danh sách hiện cả bản ghi Khoá + bộ lọc Trạng thái + cột badge.
5. Bản ghi Khoá: BE chặn sửa/xoá 423 bằng middleware route `recordNotLocked` (vì controller nhận FormRequest).
6. Bảng chưa có cột `status` → thêm migration (theo cách repo đang làm migration trên gop_db; KHÔNG bọc addColumn trong DB::transaction), chạy riêng file đó ở local: `php artisan migrate --path=<đường dẫn file>`; mặc định 1 = Hoạt động cho dữ liệu cũ.
7. Import (nếu có) tạo bản ghi Hoạt động; nếu file mẫu có cột Trạng thái thì giữ. Export thêm trường Trạng thái nếu registry có mục của màn.
8. Lịch sử: ghi Tạo mới / Cập nhật / Thay đổi trạng thái / Xóa theo trait LogsCatalogHistory như Quận/Huyện.
9. Model nên `extends BaseModel`; nếu không được thì service tự gán updated_by ở MỌI đường ghi (kể cả khoá/mở khoá).

Tự kiểm: `php -l`; gọi API thật (curl với token: đăng nhập `POST http://127.0.0.1:8003/api/v1/users/auth/login` email namdangit@gmail.com / 2025Dns@2, hoặc tinker) cho: list 2 trạng thái, tạo có status, khoá/mở khoá, sửa/xoá bản ghi khoá → 423, xoá bản ghi đã dùng → 400, xoá bản ghi chưa dùng → xoá thật; dọn dữ liệu thử sau khi kiểm. FE: grep không HTML thô mới, không `.text-muted`.
Trả về: file đã sửa (file:dòng), migration mới, bảng tham chiếu "đã dùng" của từng màn, câu thông báo mới, kết quả kiểm API, điểm cần kiểm trên màn hình, và NHỮNG THAY ĐỔI NGHIỆP VỤ so với trước (để cập nhật tài liệu).
