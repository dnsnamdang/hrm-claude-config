# Quy chế – Chuyển tab "Kỹ thuật" & tách "Đơn giá công" — Design

> Nhánh: `gop_db` · Nguồn: phản hồi tester phần "gộp quy chế" (Khai Quy chế – Cấu hình).

## Yêu cầu (tester)
1. Chuyển **Công khoán** + **Bảng tính công khoán** sang Quy chế–Cấu hình ở **Phân hệ Công việc**.
2. **Đơn giá công** → chuyển sang **Tab Giá bán** ở **Phân hệ Tài chính**.
3. **Bỏ Tab Kỹ thuật** ở phân hệ hiện tại (Danh mục).

**User chốt (2026-09-23):**
- (1) Route/màn Quy chế của phân hệ Công việc = **tạo mới** `/assign/regulation-config`.
- (2)+(3) "Bỏ tab Kỹ thuật" = **gỡ khỏi phân hệ hiện tại (Danh mục) và chuyển NGUYÊN tab sang
  Cấu hình phân hệ Công việc, GIỮ NGUYÊN tên tab "Kỹ thuật"** (không đổi tên). Chỉ tách riêng
  "Đơn giá công" ra tab Giá bán; phần còn lại (Công khoán + Bảng tính công khoán) đi cùng tab Kỹ thuật.

## Hiện trạng (đã trace)
Tab **Kỹ thuật** khai ở **2 nơi phải khớp `label` 1-1** (BE resolve field theo từng `tabKey`,
FE gửi `tabKey = group.id`, join value theo `label`):

| Field | Key / cột đích | Store | Nơi hiện tại |
|---|---|---|---|
| Đơn giá công | `work_price` → `companies.work_price` | company | tab `kythuat` |
| Công khoán | `work_bond` → `companies.work_bond` | company | tab `kythuat` |
| Bảng tính công khoán | `contract_rows` (subtable, GLOBAL, fk=`configs.id`) | config | tab `kythuat` |

- BE registry: `hrm-api/Modules/MasterData/Support/RegulationTabRegistry.php` — tab `kythuat` (dòng 130-161),
  tab `giaban` (dòng 162-173, scope MIXED company+config).
- FE registry: `hrm-client/components/regulation-config/data.js` — group `kythuat` (dòng 117-133),
  group `giaban` (dòng 134-158, đã gắn `subsystem: 'finance'`).
- `subsystem` **thuần FE** (`RegulationConfigScreen.vue:1226` lọc `groups.filter(g => (g.subsystem||'master-data')===this.subsystem)`).
  Route: `/sale/regulation-config` (=master-data, mặc định) · `/finance/regulation-config` (=finance).
  **Chưa có** subsystem `assign` / route `/assign/regulation-config`.
- Phân hệ Công việc (`subsystems.js` key `assign`) dùng `layout: 'default-sidebar'` + menu `menuItemsAssign`
  (`components/menu-sidebar.js`), có sẵn nhóm **"Thiết lập"** (dòng 246-268).
- `kythuat` + `giaban` đều đã nằm trong `API_TABS` (RegulationConfigScreen.vue:1099) → nối API thật.
- `contract_rows` scope GLOBAL (fk=configs singleton), REPLACE-ALL khi lưu; test
  `Modules/MasterData/Tests/Feature/RegulationKythuatSubtableTest.php`.

## Quyết định thiết kế
**Giữ nguyên `tabKey = 'kythuat'` và tên hiển thị "Kỹ thuật"** — chỉ:
- Gỡ field `work_price` (Đơn giá công) khỏi `kythuat`, thêm vào `giaban` (cột DB `companies.work_price`
  KHÔNG đổi → không migrate dữ liệu; join theo label nên chỉ cần khai đúng nhãn ở tab đích).
- Gắn `subsystem: 'assign'` cho group `kythuat` ở data.js → biến mất khỏi `/sale`, chỉ hiện ở `/assign`.
- Tạo route `/assign/regulation-config` (extends `RegulationConfigScreen`, `subsystem: 'assign'`).
- Thêm mục menu vào nhóm "Thiết lập" của `menuItemsAssign`, gate quyền `'Cài đặt cấu hình'`
  (đồng nhất với Finance/Sale — cùng 1 màn, cùng gate BE).

→ Ưu điểm: giữ nguyên wiring `contract_rows` (fk/history/test theo tabKey `kythuat`), không tạo tabKey
mồ côi, không phải remap history/test. Rủi ro thấp nhất.

Scope tab `kythuat` sau khi bỏ `work_price`: vẫn MIXED (work_bond=company + contract_rows=config) → giữ
`scope=MIXED, shape=SCALAR`, không đổi.

## Phạm vi ảnh hưởng
- Tab Kỹ thuật rời khỏi màn `/sale/regulation-config` (Danh mục) — đúng yêu cầu.
- "Đơn giá công" xuất hiện trong tab Giá bán ở `/finance/regulation-config`.
- Không migrate dữ liệu; không đổi cột; không tạo bảng mới.

## Rủi ro / lưu ý
- Nếu có "phiên bản hẹn ngày" (pending version) đã lưu cho field `work_price` dưới tabKey `kythuat`:
  sau khi field dời sang `giaban`, BE `fields('kythuat')` không còn `work_price` → giá trị pending cũ
  của riêng field này (nếu có) sẽ không hiển thị ở tab kythuat nữa. Trên DB gộp local hầu như chưa có
  dữ liệu thật → chấp nhận. Cần rà lại nếu chạy trên prod (kiểm `regulation_config_*` versions có
  work_price chưa áp).
- Test `RegulationKythuatSubtableTest.php`: nếu assert `work_price` thuộc tab kythuat thì cập nhật;
  subtable `contract_rows` giữ nguyên nên phần chính không đổi.
