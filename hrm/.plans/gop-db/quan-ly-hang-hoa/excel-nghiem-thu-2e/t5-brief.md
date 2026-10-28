# Brief T5 — Nghiệm thu "ERP không vỡ" (A3 / 2-E)

KHÔNG sửa code ở bất kỳ repo nào (lỗi phát hiện ⇒ ghi report, không vá). Được ghi dữ liệu thử + role tạm vào DB dev `hrm_erp_giacty` rồi **xoá đúng id**.
Đọc trước: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/excel-nghiem-thu-2e/khao-sat.md` §3 (bảng 14 bước + điều kiện tiên quyết) và **§6 chốt user** (Q6 làm rõ, Q7). Hợp đồng gốc: `man-danh-muc-hang-hoa/hop-dong-tuong-thich-erp.md:134-165`. Tham khảo cách 2-D1 kiểm: `2d-erp-khong-loi/d1-kiem-p3.md`.

## Môi trường
- HRM: API 8031 + Nuxt 3031 (worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa`), tài khoản `e2e_assign` (nhân viên 1180), storageState `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/e2e/.auth/user.json`.
- ERP: worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi`, KHÔNG đổi nhánh). Trước artisan: `ls bootstrap/cache/config.php` không tồn tại + `php artisan config:clear`; chạy `php artisan serve --port=8090` nền, ghi PID, **kill đúng PID** khi xong. Đăng nhập form `/login` bằng `TEST_EMAIL`/`TEST_PASSWORD` trong `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/.env`. Route ERP dưới `/admin/...`. POST AJAX cần header `X-CSRF-TOKEN` (lấy từ trang có meta) + `X-Request-ID` (PreventDuplicateSubmission).
- Playwright headless: `require('/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/playwright')`, node 20 `~/.nvm/versions/node/v20.20.1/bin`; script để trong `/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/ce46831b-69c7-4db5-95ea-c2037135f6ea/scratchpad/a3t5/`. Mẫu helper: `.../scratchpad/pw/c2_erp.js`, `c2_hrm2.js`.
- Quyền: HRM chỉ đọc qua role (role tạm: roles + role_has_permissions `company_id=1` + employee_has_roles `company_id`, model_type `Modules\Timesheet\Entities\Employee`; `php artisan cache:clear` ở hrm-api). ERP đọc quyền theo `App\Employee` — tra cách gán role ERP (bảng model_has_roles/… ERP) nếu tài khoản test thiếu quyền màn báo giá/hàng hoá. Mọi role tạm ghi id, gỡ khi xong.
- Tài khoản test e2e_assign không có một số quyền ERP (vd vehicle_categories) — nếu thiếu quyền, cấp qua role tạm.

## Kịch bản xuyên suốt
0. **Mốc trước**: đếm TỪNG bảng (không GROUP_CONCAT) — `products`, `product_units`/ĐVT, `product_company_coefficients`/`product_company_units`, `product_unit_prices` (giá theo công ty), `product_suppliers`, `product_business_catalogs`, `product_approves`, `catalog_histories`, `product_histories`, cây phân loại (`product_natures`, `product_function_groups`, `product_families`, `product_types`, đặc tính), `firm_quotations` + bảng con báo giá ERP. Ghi max id từng bảng.
1. **Dựng cây phân loại tối thiểu** qua API HRM (Tính chất › Nhóm CN › Nhóm SP › Loại SP + Đặc tính nếu bắt buộc) và nhánh catalog có Lĩnh vực nếu popup Xây dựng catalog cần (DB dev gần rỗng — B5/B6).
2. **Tạo 1 hàng** bằng form HRM (Playwright UI), **xếp catalog bằng popup "Xây dựng catalog" thật**, đưa sang **Đang kinh doanh** bằng nút sẵn có trên UI (vd nút "Chuyển kinh doanh" H1). Nếu không có đường UI tới status 3 (cần giá / luồng Phase 7) ⇒ DỪNG phần này, ghi rõ chặn ở đâu, KHÔNG đặt bằng SQL (user chốt), làm tiếp các bước còn làm được. Hàng cần giá bán để bước 4 kiểm giá: dùng màn Cập nhật giá bán HRM (1657) nếu được.
3. ERP 8090:
   - B1: `admin/products` tìm mã hàng mới, đếm dòng DOM; mã đúng khuôn.
   - B2: popup chọn hàng (picker mới) ở báo giá + phiếu xuất kho + HĐ mua: (i) trước khi KD không hiện, (ii) sau khi KD hiện, (iii) công ty khác chưa lấy về không hiện. SQL đối chiếu.
   - B3': `admin/products/{id}/show` đủ tab, đếm ô có giá trị, 0 lỗi console.
   - B4: báo giá ERP thêm hàng mới ⇒ giá đúng công ty chứng từ (so DOM với bảng giá); **Lưu 1 báo giá rồi xoá đúng id** (xoá cả bảng con); chứng từ khác chỉ mở form + thêm hàng, không lưu.
   - B5: Người tạo/cập nhật đúng tên (SQL + DOM).
4. SQL B11 (so từng bảng: chỉ tăng đúng số vừa tạo), B12 (`products.code` rỗng = 0), B13 (mã trùng = 0).
5. B6–B10: chạy lại PHPUnit giá HRM (`ProductPriceScreenApiTest`, `ProductPriceApprovalApiTest`, `ProductWriteApiTest`) — ở hrm-api worktree, ghi số. B14': PHPUnit do T2 viết (`ProductCodeRetryTest` hoặc tên trong `t12-report.md`) — chạy lại, ghi số. PHPUnit ERP (`tests/` wt-erp-2d1) chạy cả bộ, ghi số (mốc 185 xanh + skipped).
6. **Dọn**: xoá đúng id mọi bản ghi đã tạo (hàng + bảng con + lịch sử + catalog + cây phân loại thử + báo giá + role tạm), xoá cache quyền; đếm lại = mốc trước. Kill ERP 8090 đúng PID.

## Report
`excel-nghiem-thu-2e/nghiem-thu.md`: bảng 14 bước (Đạt / Không đạt / Không làm được + lý do + bằng chứng: số DOM, SQL, ảnh chụp lưu scratchpad), id đã tạo/xoá, mốc trước/sau, lỗi phát hiện (đề xuất mã N mới bắt đầu từ N109). Trả lời ngắn: tổng số bước đạt, lỗi, dữ liệu đã dọn chưa. Không dispatch subagent, không đổi CLAUDE.md/cấu hình, không pkill theo tên.

## Lượt 2 (15/10) — chạy tiếp sau khi user cho phép
- **User đã cho phép (15/10): "Cho phép ghi dữ liệu vào database"** — ghi dữ liệu thử + role tạm vào DB dev `hrm_erp_giacty` (qua API HRM/ERP, UI, hoặc SQL cho role tạm/dọn), xoá đúng id khi xong. Vẫn KHÔNG đặt catalog/trạng thái hàng bằng SQL (Q6).
- **User chốt N110 = chạy đủ luồng giá trên UI HRM**: hàng mới → YCHG → YCTG → phiếu tính giá → kết quả → duyệt ⇒ hàng sang Đang KD (status 3) đúng đường thật. Ghi id từng phiếu, dọn hết theo id (cả bảng con, lịch sử, registry chờ duyệt nếu có).
- Lượt 1 đã chạy xong B6–B10, B12, B13, B14', PHPUnit ERP (xem `nghiem-thu.md`) — KHÔNG chạy lại. Làm: bước 0 (mốc mới), 1, 2, 3 (B1–B5), 4 (B11 + B12/B13 đo lại), 6 (dọn). Form tạo hàng bắt buộc ≥1 Tiểu mục; popup "Xây dựng catalog" xếp thêm nhánh MỚI (không dùng 3730).
- Script/mốc ở scratchpad `a3t5/` (snap.sh, tables.txt) dùng lại được; bổ sung bảng phiếu Phase 7 vào mốc.
- Cập nhật `nghiem-thu.md` (thêm mục "Lượt 2", sửa bảng 14 bước). Lỗi mới đặt mã từ **N111**.
