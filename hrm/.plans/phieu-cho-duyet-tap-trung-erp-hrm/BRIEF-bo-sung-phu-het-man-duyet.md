# Phụ lục brief: PHỦ HẾT mọi màn duyệt trên HRM — @cuong61n

Đọc SAU `BRIEF-dinh-nghia-loai-phieu.md` (vẫn áp dụng toàn bộ: hợp đồng Definition, luật cứng, cách kiểm chứng, đột biến, báo cáo). Phụ lục này **thay đổi** một nguyên tắc và giao việc đợt 2.

## Quyết định của user (16–17/11/2026) — THAY THẾ quy tắc "bỏ nếu không đủ chắc"
> "Hiện tại ở code HRM có màn nào cần phải duyệt thì phải đưa vào Trung tâm phê duyệt hết."

Đợt 1 đã đăng ký 68 loại nhưng BỎ những loại mà code gốc không chốt quyền ở BE. Đợt 2: **không được bỏ chỉ vì BE không chốt quyền**. Phải đưa vào mọi màn mà trên HRM người dùng có thể **Duyệt hoặc Từ chối** một phiếu đang chờ.

### Thế nào là "màn cần duyệt" (phải đăng ký)
Màn / luồng trong HRM (có route FE trong `hrm-client/pages/**`) mà một người khác người lập bấm **Duyệt / Đồng ý / Xác nhận / Từ chối / Không duyệt / Tiếp nhận…** để phiếu rời trạng thái chờ. Gồm cả "nửa luồng": HRM chỉ có nút Không duyệt còn bước duyệt thật mở ERP (người đó vẫn là người duyệt trên HRM).

### KHÔNG phải màn cần duyệt (được bỏ, nhưng PHẢI ghi bằng chứng)
- Hàng đợi công việc thuần (chờ làm báo giá, chờ giao việc…) không có nút Duyệt / Từ chối.
- Người lập tự "duyệt" phiếu của chính mình, không có bước chờ người khác (vd Quyết toán thưởng năng suất quý).
- Bảng không có trạng thái duyệt (vd Ứng lương nếu code đúng như vậy — tự kiểm lại).
- Luồng chỉ còn trên ERP, không có màn HRM.
Mỗi loại bỏ phải kèm `file:dòng` chứng minh. Nghi ngờ thì ĐĂNG KÝ (đừng bỏ).

### Khi BE không chốt quyền — dùng "ĐIỀU KIỆN GIAO DIỆN" làm người duyệt
Người duyệt = người **mở được màn đó VÀ thấy nút duyệt** trên HRM:
1. Điều kiện vào màn: mã quyền / tên quyền của mục menu (`codes` / `isShow` trong `hrm-client/components/menu*.js`, `subsystem-menu/*.js`) + phạm vi dữ liệu danh sách (lọc theo công ty / phòng quản lý / người tạo…) mà API danh sách của màn đó áp.
2. Cờ hiện nút (`can_approve`, `canApprove`, `status==...` ở FE hoặc Entity).
3. `truth()` mô phỏng đúng điều đó cho người đang đăng nhập (đã `auth()->setUser` + công ty đang làm).
Ghi rõ trong docblock Definition: **"BE không chốt quyền — người duyệt lấy theo điều kiện giao diện"**, và liệt kê trong báo cáo để chuyển cho người phụ trách module vá BE.
Chỉ khi màn **không có bất kỳ gate nào** (ai đăng nhập cũng vào được, nút luôn hiện) thì dừng và báo người điều phối kèm đề xuất (đừng tự đoán "tất cả nhân viên").
Menu gate bằng tên quyền cũ: quy ra MÃ qua bảng `permission_aliases` / `legacy` trong Catalog; tên không tồn tại trong Catalog ⇒ không ai vào được màn ⇒ đăng ký với danh sách người duyệt rỗng + ghi rõ là lỗi cấu hình quyền (báo người điều phối).

## Việc phải làm (mỗi agent)
1. **KIỂM KÊ THEO MODULE CỦA BẠN**: liệt kê MỌI route FE (`pages/**/approve*`, `*waiting*`, `*pending*`, `*for-approve*`…), mọi mục menu thuộc nhóm "Phê duyệt / Duyệt", mọi route BE tên `approve|deny|reject|confirm|receive|refuse|cancel…` trong module bạn. So với `php artisan tinker`/script lấy `ApprovalDefinitionRegistry::all()` (doc_type đã đăng ký). Lập bảng: luồng · màn FE · đã đăng ký (doc_type) hay CHƯA · nếu chưa thì vì sao.
2. **Đăng ký mọi luồng còn thiếu** theo đúng quy trình của brief gốc (Definition + trait + seedTest + test đối soát `truth()` + đột biến + `approval-inbox:verify` + API thật). Danh sách khởi đầu cho từng nhóm ở prompt của bạn; kiểm kê có thể tìm thêm.
3. **Sửa lại các loại đã đăng ký ở đợt 1 nếu kiểm kê thấy sai / thiếu cấp** (vd thiếu một cấp duyệt, thiếu một nhánh người duyệt) — chỉ trong thư mục Definition của nhóm bạn, tăng `version()`.
4. Báo cáo: bảng kiểm kê đầy đủ (mọi luồng của module → doc_type hoặc lý do bỏ có file:dòng), kết quả verify từng loại mới, danh sách "BE không chốt quyền" cần chuyển người phụ trách, các điểm cần user quyết.

## Luật bổ sung
- Giữ nguyên luật cứng của brief gốc: không sửa file dùng chung của module (Definition base, Services, Http, Console, Providers, Migrations); cần sửa thì dừng và báo.
- **Được phép chạy migration CHỈ KHI** migration đó đã có sẵn trong repo, đang chờ chạy, và cần để kiểm chứng đúng loại phiếu của bạn trên DB local (`php artisan migrate --path=<đường dẫn migration đó> --force` — chỉ migration đó, không `migrate` cả hệ thống). Ghi lại đã chạy migration nào.
- Không chạy Playwright (người điều phối chạy e2e theo khoá sau). Không commit / push / deploy.
- Nhiều agent chạy song song trên cùng DB: gặp Deadlock / Lock wait chạy lại; chỉ chạy test của nhóm bạn.
- Mọi dữ liệu thử gắn `TEST-APPROVAL-CENTER`, dọn bằng `approval-center:clean-test --manifest=<tên-file-riêng-của-bạn>.json` (mỗi agent dùng manifest RIÊNG để dọn không giẫm nhau, vd `wave2-<nhóm>.json`).
- Ghi chi tiết vào `.plans/phieu-cho-duyet-tap-trung-erp-hrm/quyen-duyet/phu-het-<nhóm>.md`.
