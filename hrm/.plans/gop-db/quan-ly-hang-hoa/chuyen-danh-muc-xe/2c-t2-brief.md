# Brief T2 — HRM FE Phase 2c (hrm-client)

Repo: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-client`, nhánh **`feat/cdhh-2c-xe`** (đã checkout — KHÔNG đổi nhánh, KHÔNG merge, KHÔNG push, KHÔNG git stash).
Nuxt dev đang chạy cổng **3031** (API 8031) cho worktree này — KHÔNG kill / restart trừ khi bắt buộc (nếu buộc: kill đúng PID theo cổng 3031, khởi lại bằng node 12 + `NODE_OPTIONS=--max-old-space-size=8192`, ghi lại cách làm).
Đọc trước: thư mục `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/` — `khao-sat-2c.md`, `plan-2c.md` (Đợt T2), và **`2c-t1-report.md` (hợp đồng API BE đã làm — endpoint, quyền, JSON)**. Tuân thủ `HRM/CLAUDE.md` + skill tương ứng nếu repo có (`.claude/skills/list-page`, `modal-popup`, `form-validate`, `select-and-input-state`, `button-convention`) — nhưng **bám khuôn repo thật** (6 màn xe 2b) khi skill lệch repo.

## Khuôn bắt chước
- `pages/master-data/vehicle-payloads/{index.vue,AddVehiclePayloadModal.vue}` (danh mục phẳng) và `pages/master-data/vehicle-models/*` (có ô chọn cha, lọc dây chuyền).
- Menu `components/subsystem-menu/master-data.js` nhóm "Xe" (`subItems`, KHÔNG `children`).

## Việc
1. **Biển số xe** `pages/master-data/license-plates/` — cột: STT · Biển số · Ghi chú · Trạng thái · Người tạo · Ngày tạo · Hành động. Popup thêm/sửa: Biển số (bắt buộc, ≤90), Ghi chú (≤255). Lọc: Biển số, Trạng thái, Người tạo, Ngày tạo.
2. **Lái xe ngoài** `pages/master-data/external-drivers/` — cột: Họ tên · SĐT · Năm sinh · CCCD · Số GPLX · Trạng thái · Người tạo · Ngày tạo · Hành động. Popup: 5 ô bắt buộc (bố trí đủ 12 cột mỗi hàng, không để ô lẻ). Lọc: Tên, SĐT, Trạng thái…
3. **Nhiên liệu** `pages/master-data/fuels/` — cột: Tên · Giá (định dạng số VN, phần nghìn) · Trạng thái · Người tạo · Ngày tạo · Hành động. Popup: Tên (bắt buộc), Giá (bắt buộc, số ≥0, ô số có phân cách nghìn theo khuôn repo).
4. **Danh mục xe** `pages/master-data/vehicles/` — list cột: Biển số · Chủ xe (công ty hoặc NCC) · Hãng xe · Loại xe · Model xe · Dòng xe · Tải trọng · Nhiên liệu · Tài xế (tên, nối dấu phẩy) · Trạng thái · Người tạo · Ngày tạo · Hành động. Lọc: Biển số, Chủ xe, Hãng, Loại, Model, Tải trọng, Dòng xe, Trạng thái.
   Form (popup lớn `size="lg"`/`xl` hoặc trang riêng — chọn theo khuôn repo có sẵn cho form nhiều ô; ghi lý do): Biển số (chọn, chỉ biển đang hoạt động) · Hãng xe → Loại xe → Model xe (dây chuyền: đổi cha thì xoá con, danh sách con lọc theo cha) · Dòng xe · Tải trọng · Nhiên liệu · Công tắc/radio "Xe Tân Phát" ⇒ Công ty + Bộ phận (bộ phận lọc theo công ty), ngược lại ⇒ Chủ xe là NCC (ô chọn có tìm) · Loại tài xế (radio Lái xe ngoài / Tài xế công ty) ⇒ chọn NHIỀU lái xe ngoài hoặc nhân viên (lưu `employee_infos.id` — dùng đúng endpoint T1 report chỉ). Khi sửa xe có giá trị đã khoá vẫn hiển thị được tên.
   ⚠️ `V2BaseRadio` option phải là `{value,label}`. Radio/checkbox: Playwright bấm nhãn. Validate bấm Lưu báo đồng thời mọi ô (marker `.v2-error`). Không dùng prop `trim` ở ô nhập.
5. Mỗi `index.vue`: prop `entity-type` của popup lịch sử = đúng tên bảng (`license_plates`, `drives`, `fuels`, `vehicles`) — chỗ hay sót.
6. Menu: nhóm "Xe" thêm 4 mục sau "Tải trọng xe": Biển số xe · Lái xe ngoài · Danh mục xe · Nhiên liệu, `isShow` = cặp quyền Quản lý/Xem đúng chuỗi T1.
7. Cột Hành động: `V2BaseRowActions` emit **chuỗi** key; nút Mở khoá phải gọi `/unlock` (danh mục bảng ERP khoá = 0). Không quyền Quản lý ⇒ ẩn nút ghi.
8. e2e (`/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/e2e`, nằm ngoài git): thêm 3 màn danh mục phẳng vào danh sách màn của `tests/master-data/product-catalog-ui.spec.ts` / `product-catalog-common.api.spec.ts` nếu cấu trúc cho phép; thêm spec mới `tests/master-data/vehicles-ui.spec.ts` cho Danh mục xe (tạo xe bằng form → dây chuyền → đổi loại tài xế → sửa → khoá/mở khoá → xoá; dọn dữ liệu). KHÔNG chạy cả bộ e2e; chỉ chạy spec mới/spec đã sửa với `--workers=1` (node 20 tại `~/.nvm/versions/node/v20.20.1/bin`, chạy từ thư mục e2e, truyền `API_BASE=http://127.0.0.1:8031 BASE_URL=http://127.0.0.1:3031` — xem `.env` e2e ghim cổng). Nếu setup e2e hỏng do DB gộp: chạy `--no-deps` + tự ghi `.auth/user.json` (xem cách cũ trong thư mục e2e).
9. **Kiểm bằng Playwright đo DOM** (bắt buộc): 4 màn mở được, số dòng trang 1 + tổng khớp DB (license_plates active 161, drives 69, vehicles 134, fuels 4 khi lọc Hoạt động), đúng bộ cột, ô lọc bắn đúng param (bắt request), nút hành động bấm thật; form xe: dây chuyền + đổi chủ xe + đổi loại tài xế đo bằng DOM; menu nhóm Xe đủ 10 link (đếm DOM trên hub Danh mục chung). Tài khoản test `e2e_assign` (nhân viên 1180) — cấp quyền bằng **role tạm** trên `hrm_erp_giacty` (được phép), xoá cache quyền; GHI id role tạm vào report và **gỡ** khi xong. Dữ liệu thử phải dọn sạch, số dòng bảng về đúng mốc (license_plates 163 · drives 72 · vehicles 137 · fuels 4 · vehicle_drivers 110 · vehicle_company_drivers 74).

## Ràng buộc
- Giữ EOL từng dòng. Comment tiếng Việt, mật độ như file mẫu. Thấy lỗi ngoài luồng ⇒ ghi report, không vá.
- Commit tiếng Việt trên `feat/cdhh-2c-xe`, kết thúc:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3
  ```
- Cần sửa BE (thiếu trường, sai JSON) ⇒ được sửa tối thiểu trong hrm-api cùng nhánh, commit riêng, ghi rõ trong report.
- Không dispatch subagent.

## Report
`/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/2c-t2-report.md`: commit, file, số đo Playwright (bảng số), kết quả spec e2e (đọc dòng tổng kết: passed/failed/did not run), role tạm đã gỡ, số dòng bảng, ngoài luồng. Trả lời ngắn: trạng thái, commit, 1 dòng test, lo ngại.
