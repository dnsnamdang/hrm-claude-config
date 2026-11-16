# Plan — Phiếu phân chia thị trường theo nhân viên (#11695)

> @junfoke · nhánh `task_11695` · design: `design.md` · spec: `docs/superpowers/specs/gop-db/2026-10-16-division-market-employee-design.md`

## Phase 0 — Chuẩn bị nhánh
- [x] Tạo `task_11695` từ `task_11694` (cả 2 repo)
- [x] Merge `origin/gop_db` vào `task_11694` — sửa 4 quyền #11694 sang `$this->perm`, `V2BaseSegmented` lấy bản gop_db
- [x] Merge `task_11694` vào `task_11695` (fast-forward)
- [x] Phân tích demo + code ERP, chốt 5 quyết định với user

## Phase 1 — BE
- [x] Migration thêm cột (`employee_id`, `division_part_id`, `business_area_id`) + index 5 bảng
- [x] Migration tách 14 phiếu cũ theo nhân viên
- [x] 5 entity + trạng thái / quyền / phạm vi xem / canX / mã phiếu
- [x] Service: danh sách + lọc + sort, phạm vi NV, options form, chi tiết cây, lưu (validate phạm vi, hãng, SL tối đa), gửi / thu hồi / duyệt / từ chối / hủy duyệt, xoá, lịch sử
- [x] Controller + request + list resource + route + blade in + export rows
- [x] 5 quyền seeder (`$this->perm`), `CatalogHistoryService` (bảng + nhãn `sent` / `recalled`), `ExportColumnRegistry`
- [x] Chặn Hủy duyệt / Xoá phiếu phòng ban khi còn phiếu NV Chờ duyệt / Đã duyệt
- [x] Test API (sau khi user cho chạy migrate + permission:sync)

## Phase 2 — FE
- [x] Danh sách (bộ lọc, cột, hành động theo trạng thái, xuất Excel)
- [x] Form Tạo / Sửa / Chi tiết (cây Tỉnh/TP → khu vực, popup chọn khu vực trong phạm vi, popup phường/xã chỉ xem, nhãn SL tối đa)
- [x] Popup Từ chối (lý do bắt buộc), Lịch sử, In
- [x] Menu "Theo nhân viên"
- [x] Verify Playwright

### Checkpoint — 2026-10-16
Vừa hoàn thành: BE + FE #11695. DB local đã migrate 2 file (--path), tách 14 phiếu cũ → 135 phiếu (mỗi phiếu 1 NV), permission:sync, gán 5 quyền mới cho role 18. Test API: lưu, chặn SL tối đa, hãng ngoài phạm vi, NV khác phòng, 423 khi chờ duyệt/đã duyệt, gửi/thu hồi/duyệt/từ chối/hủy duyệt, chặn hủy duyệt phiếu phòng ban, lọc/sort/xuất Excel/in/lịch sử. Playwright: danh sách, sửa + thêm khu vực + lưu, chi tiết, gửi duyệt, từ chối (lý do hiện ở form), tạo mới với NV chưa thuộc bộ phận.
Đang làm dở: —
Bước tiếp theo: user review UI; commit task_11695 (chưa commit); đưa skill sửa vào PR hrm-claude-config.
Blocked:
Ghi chú: dữ liệu test còn trong DB local — phiếu NV 140 (Đang tạo, NV 237), 141 (Đang tạo, đã từ chối 1 lần, NV 235).

## Phase 3 — E2E
- [x] Dựng bộ e2e `e2e/` (ngang hàng hrm-client; workspace chưa có) — Playwright 1.61 alpha (cùng bản MCP, dùng lại Chromium 1226), Node 24 nvm
- [x] `tests/division-market-employees.spec.ts` — 15 kịch bản + setup đăng nhập: 16/16 đạt (15 phút trên dev server `php -S` + Nuxt dev)

### Checkpoint — 2026-10-16 (e2e)
Vừa hoàn thành: e2e #11695 chạy xanh 16/16; test tự dọn phiếu NV phòng 50 trước/sau (đã xoá luôn phiếu test tay 140, 141).
Đang làm dở: —
Bước tiếp theo: user review; commit task_11695.
Blocked:
Lệnh chạy: `cd e2e && PATH="/c/Users/Legion/AppData/Local/nvm/v24.6.0:$PATH" E2E_BASE_URL=http://127.0.0.1:3005 E2E_API_URL=http://127.0.0.1:8002 npx playwright test`

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Đưa `task_11694` + `task_11695` (làm lại xử lý phiếu phân chia thị trường) vào `develop` cả 2 repo: api merge `f58667fba` / `8475075a8` (làm ở worktree `gop-db` vì develop đang bị worktree giữ), client `76e54cf26` / `966d70450` (thư mục chính). Conflict `V2BaseSegmented.vue` giữ bản develop; menu `sale-hub.js` tự gộp, "Phiếu phân chia thị trường" có 2 link Theo phòng ban / Theo nhân viên.
- [x] 05/11/2026 — Xử lý lỗi editor gạch đỏ `V2BaseSegmented.vue`: comment HTML lồng trong comment đầu file (dòng 11) đóng sớm comment lớn → đổi thành chữ thường; có từ commit `868558c3c` của người khác, không do merge. Client `16c73fc24`.
- [x] 05/11/2026 — Hỗ trợ lỗi ERP sau khi develop vào `gop_db`: tạo HĐ… báo SQL 1052 `employee_id ambiguous`. Đã lỡ revert merge task_11695 khỏi `gop_db` hrm-api (`5eb4b971e`) rồi khôi phục lại (`abd54ea75`, code y như `a9147a0d9`). Nguyên nhân thật: migration thêm cột `employee_id` vào `division_market_department_employees` ⇒ truy vấn ERP join bảng này mà `where('employee_id')` không ghi tên bảng bị mơ hồ; revert HRM không gỡ được cột. Chữa ở ERP: `FirmQuotationService::marketDivisionContract` đã được @nguyentrancu97 sửa (`7bc428417b`, origin/gop_db TanPhatDev) → chỉ cần pull `gop_db` TanPhatDev trên server. Không chạy SQL gỡ DB.

## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Hỗ trợ check lại `gop_db` sau vụ revert/khôi phục task_11695 hôm 05/11: hrm-api đủ 18 file, không lệch dòng nào so với `a9147a0d9`; ERP `7bc428417b` (ghi rõ `division_market_employees.employee_id`) vẫn trên `gop_db`. Lỗi `employee_id ambiguous` còn thì chỉ do server ERP chưa pull.
- [x] 06/11/2026 — Fix phản hồi #12040 (Phiếu phân chia thị trường theo nhân viên): màn Sửa bỏ ô Số phiếu + badge "Đang tạo" (badge chỉ còn ở Chi tiết, áp cả phiếu phòng ban); màn Tạo bỏ Số phiếu, "Phạm vi được chia" thành ô riêng tự lấy theo nhân viên có ⓘ, thêm "Lưu và tiếp tục"; popup Thêm Tỉnh/TP trống là do dữ liệu (phường/xã của phiếu phòng ban TPE_PCTT_00001 chưa gán khu vực KD) → bảng ghi rõ lý do + cách gán, ẩn nút Thêm Tỉnh/TP; danh sách Người tạo / Ngày tạo, sort như #12042; ô hãng xe trống để trống. Icon "Lưu và gửi duyệt" giữ máy bay giấy, chỉnh cỡ 15px như WR (chờ QA nếu muốn icon khác). Commit cùng api `fb890c98d`, client `8b6321dbc`.
- [x] 06/11/2026 — Fix phản hồi #12057: bỏ dòng "Lý do từ chối" trên form; trạng thái cạnh mã phiếu, Xuất Excel xanh lá; bấm Từ chối mà chưa nhập lý do → toast "Bạn chưa nhập đầy đủ thông tin" + vẫn báo đỏ dưới ô (thêm prop `inputRequiredToast` mặc định tắt vào popup dùng chung `base-confirm-modal.vue`, màn khác không đổi). Bấm Từ chối thật trên trình duyệt; client `4269cf7cc` (develop, đã lên origin).

## Ngày 16/11/2026 (@junfoke) — PROD ĐÃ GỘP NGƯỢC VỀ 1 PHIẾU / PHÒNG

- [x] 16/11/2026 — TP kinh doanh báo không phân chia được trên ERP `admin/division_market/employee`. Nguyên nhân: migration
  `2026_10_16_000002_split_division_market_department_employees_by_employee` đã tách 14 phiếu (1 phiếu/phòng) thành 141 phiếu
  (1 phiếu/NV), còn màn ERP vẫn hiểu 1 phiếu/phòng → lập mới bị chặn (unique phòng), mở sửa thì phần lớn NV ra bảng trống.
  Màn HRM #11695 chưa test nên CHƯA chuyển được → **gộp ngược dữ liệu prod** để ERP chạy luồng cũ. Code không đổi.
- [x] Đã chạy prod 16/11: 141 → **14 phiếu / 14 phòng**, 0 dòng mồ côi. Sao lưu ở 6 bảng `bk20261116_dmde`, `_dme`, `_dmep`,
  `_dmew`, `_dmepv`, `_dmdeh` (bản trước khi gộp — xoá khi ERP dùng ổn).
  Cách gộp: nhóm bản tách theo (company_id, division_department_id, created_at, created_by), giữ MIN(id) (= phiếu gốc, giữ mã
  cũ); chuyển con ở `division_market_employees.parent_id` + `division_market_employee_{provinces,wards,province_vehicles}` +
  `division_market_department_employee_histories` (cột `division_market_department_employee_id`) về phiếu gốc; xoá bản tách;
  phiếu gốc set `employee_id = NULL`, `division_part_id = NULL`.
- [x] Đối chiếu prod sau gộp (16/11): phân công phường/xã ở lần lưu/duyệt gần nhất trong lịch sử ERP đều còn (chỉ lệch 3 dòng
  phiếu 14 = phường Hạnh Thông đổi id 0 → 13467, không phải mất); 0 tỉnh/xã/hãng mồ côi; trong lúc bị tách có 2 lần sửa trên
  ERP ngày 12/11 (phiếu gốc 12 phòng 107, phiếu tách 103 phòng 109 → nay thuộc phiếu 10, lịch sử #482/#483 đã chuyển theo),
  trạng thái giữ Đã duyệt, không lặp NV. Lần tách đầu chỉ xoá dòng NV chưa giao tỉnh nào (không kèm dữ liệu) ⇒ KHÔNG MẤT DỮ LIỆU.
- [ ] **KHI CHUYỂN PROD SANG MÀN HRM #11695** — phải TÁCH LẠI dữ liệu, vì bảng `migrations` trên prod đã ghi migration tách
  là "đã chạy" nên deploy/`migrate` sẽ KHÔNG tự tách nữa. Migration này idempotent (chỉ xử lý phiếu `employee_id IS NULL` —
  đúng là toàn bộ phiếu sau khi gộp + phiếu ERP lập thêm sau 16/11), nên chạy lại chính nó là đủ, không cần viết SQL tách tay:

  ```sql
  -- 1. Sao lưu (đổi hậu tố ngày)
  CREATE TABLE bkYYYYMMDD_dmde  AS SELECT * FROM division_market_department_employees;
  CREATE TABLE bkYYYYMMDD_dme   AS SELECT * FROM division_market_employees;
  CREATE TABLE bkYYYYMMDD_dmep  AS SELECT * FROM division_market_employee_provinces;
  CREATE TABLE bkYYYYMMDD_dmew  AS SELECT * FROM division_market_employee_wards;
  CREATE TABLE bkYYYYMMDD_dmepv AS SELECT * FROM division_market_employee_province_vehicles;
  -- 2. Kiểm trước: số phiếu / phòng (đang 1 phiếu / phòng)
  SELECT COUNT(*) phieu, COUNT(DISTINCT division_department_id) phong FROM division_market_department_employees;
  -- 3. Gỡ dấu "đã chạy" của migration tách
  DELETE FROM migrations WHERE migration = '2026_10_16_000002_split_division_market_department_employees_by_employee';
  ```

  ```bash
  # 4. Chạy lại đúng 1 file migration (hrm-api trên server)
  php artisan migrate --path=Modules/Finance/Database/Migrations/2026_10_16_000002_split_division_market_department_employees_by_employee.php --force
  ```

  ```sql
  -- 5. Kiểm sau: mỗi phiếu đúng 1 NV, không còn phiếu employee_id NULL, không mồ côi
  SELECT COUNT(*) phieu, SUM(employee_id IS NULL) chua_tach FROM division_market_department_employees;   -- chua_tach = 0
  SELECT parent_id, COUNT(*) n FROM division_market_employees GROUP BY parent_id HAVING n > 1;            -- rỗng
  SELECT COUNT(*) FROM division_market_employee_wards w
    LEFT JOIN division_market_department_employees d ON d.id = w.division_market_department_employee_id
   WHERE d.id IS NULL;                                                                                     -- 0
  ```

  Lưu ý khi tách lại: (1) NV không có Tỉnh/TP nào bị migration XOÁ khỏi phiếu (như lần đầu); (2) dữ liệu ERP gốc có 2 NV lặp
  trong 1 phiếu (local: phiếu 1 NV 25, phiếu 5 NV 61) → tách ra 2 phiếu cho cùng NV, cần dọn tay sau; (3) **cùng lúc** phải ẩn
  nút Thêm/Sửa ở màn ERP `division_market/employee` (ERP không hiểu 1 phiếu/NV), nếu không sẽ lặp lại lỗi 16/11;
  (4) phiếu phòng ban cũ của ERP chưa gán khu vực KD → popup Thêm Tỉnh/TP ở màn HRM trống, phải gán khu vực trước.
  Thử trên local trước khi làm prod. DB local hiện VẪN ở dạng đã tách (không gộp).
