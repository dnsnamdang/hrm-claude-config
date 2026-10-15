# Brief T3 + T4 — A3 (2-E) FE hrm-client + kiểm

Repo `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-client`, nhánh **`feat/cdhh-2e-excel`** (đã checkout — KHÔNG đổi nhánh/merge/push/stash). Nuxt 3031 + API 8031 đang chạy từ worktree — không kill/restart trừ khi bắt buộc (nếu buộc: đúng PID theo cổng, node 12 + `NODE_OPTIONS=--max-old-space-size=8192`).
Đọc trước: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/excel-nghiem-thu-2e/` — `khao-sat.md` (§4 tự chốt kỹ thuật, §5 T3/T4, **§6 chốt user**) và **`t12-report.md` (hợp đồng BE: endpoint, key cột theo màn)**. Skill `HRM/.claude/skills/export-excel`, `list-page`, `button-convention` (bám repo thật nếu lệch). Tuân thủ `HRM/CLAUDE.md`.

## T3 — FE
- 5 màn danh sách hàng hoá (Kho dữ liệu · Dữ liệu công ty · Nhập thông tin · Đang KD · Hàng tạm) có nút "Xuất Excel" theo khuôn xuất Excel chung của repo (tìm màn khác đang dùng `ExportFieldsModal` + `exportFieldsMixin` + `exportListFile`/dựng file FE theo trang — bám đúng khuôn đó), popup chọn trường tick sẵn cột đang hiện, dòng tiến độ khi tải nhiều trang. Gate quyền **"Xuất excel danh sách hàng hoá"** (1654): không quyền ⇒ ẩn nút.
- Chủ yếu sửa `components/product/ProductListPage.vue` + `utils/product-list-screens.js` (cờ export + khoá registry theo màn); màn Hàng tạm nếu không dùng ProductListPage thì làm theo khuôn màn đó.
- Ô Catalog nhiều dòng trong 1 ô (wrap text). Tên file theo khuôn repo (vd `<slug-man>_<mã cty>_<ddmmyyyy>.xlsx`).

## T4 — kiểm
- **Playwright đo DOM** (bắt buộc): 5 màn đều có nút (có quyền), mở popup ⇒ số ô tick = số cột đang hiện, tải file thật (bắt `download`), đọc file bằng ExcelJS (`HRM/e2e/node_modules`) — đúng heading, số dòng = tổng theo bộ lọc hiện tại (thử 1 bộ lọc), ô catalog nhiều dòng có `\n`, Kho không có cột Catalog, không cột giá; không quyền 1654 ⇒ không thấy nút + gọi API 403.
- Fixture: cần hàng có ≥2 nhánh catalog ở công ty đang làm — tự dựng (qua API HRM hoặc SQL insert vào `product_business_catalogs` theo đúng cấu trúc), ghi id, dọn sau.
- Tài khoản `e2e_assign` (nhân viên 1180), token trong `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/e2e/.auth/user.json`. Cấp quyền bằng **role tạm** trên `hrm_erp_giacty` (bảng roles / role_has_permissions có `company_id=1` / employee_has_roles có `company_id`, model_type `Modules\Timesheet\Entities\Employee`), xoá cache (`php artisan cache:clear` ở hrm-api). Ghi id role tạm, **gỡ khi xong**.
- e2e spec mới `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/e2e/tests/master-data/products-export-ui.spec.ts` (có quyền / không quyền, đọc file đo ô, dọn fixture). Chạy riêng spec này `--workers=1` (node 20 `~/.nvm/versions/node/v20.20.1/bin`, từ thư mục e2e worktree, truyền `API_BASE=http://127.0.0.1:8031 BASE_URL=http://127.0.0.1:3031`), đọc dòng tổng kết (passed/failed/did not run). KHÔNG chạy cả bộ e2e.

## Ràng buộc
Giữ EOL; comment tiếng Việt; không dùng prop `trim`. Cần sửa BE tối thiểu ⇒ được, trong hrm-api cùng nhánh, commit riêng, ghi rõ. Commit cuối message:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3
```
Dữ liệu thử + role tạm phải dọn; báo số dòng `products`, `product_business_catalogs`, `catalog_histories` trước/sau bằng nhau. Không dispatch subagent.

## Report
`excel-nghiem-thu-2e/t34-report.md`: commit, file, bảng số đo Playwright, nội dung file Excel đo được, kết quả spec, role tạm đã gỡ, ngoài luồng. Trả lời ngắn.
