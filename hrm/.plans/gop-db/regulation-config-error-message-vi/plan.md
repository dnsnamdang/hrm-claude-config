# Màn cấu hình quy chế — thông báo lỗi để tiếng Việt

> Nhánh: `gop_db` (develop). Phụ trách: @dangquang.tom

## Bối cảnh

Màn `/sale/regulation-config` (dùng chung component `components/regulation-config/RegulationConfigScreen.vue`
với `/finance/regulation-config` và `/assign/regulation-config`) hiển thị thông báo lỗi
**tiếng Anh** khi thao tác lưu/xoá thất bại.

**Nguyên nhân gốc:** các message validate BE (FormRequest) đều tiếng Việt, NHƯNG khi lỗi 422
Laravel đặt top-level `message` = **"The given data was invalid."** (tiếng Anh). Nhiều handler
catch trong component toast thẳng `resp.message` / `data.message` → lộ câu tiếng Anh. Rõ nhất ở
tab "Quy chế thưởng năm" (dept-grid) — chỗ duy nhất toast `resp.message` ngay trong nhánh 422.

**Giải pháp (đúng convention):** dùng util chung có sẵn `utils/api-error-message.js`
(`apiErrorMessage(error, fallback)`) — ưu tiên câu lỗi đầu tiên trong `errors` (câu nghiệp vụ
tiếng Việt), bỏ qua chuỗi mặc định Laravel, fallback câu tiếng Việt màn truyền vào. KHÔNG tự viết
message mới (tuân thủ CLAUDE.md: message rule phổ biến đã ở lang file).

## Tasks

- [x] **Task 1: Route toàn bộ toast lỗi của `RegulationConfigScreen.vue` qua `apiErrorMessage`**
  - File: `hrm-client/components/regulation-config/RegulationConfigScreen.vue`
  - Import `apiErrorMessage` từ `@/utils/api-error-message`
  - Thay 8 chỗ toast đọc trực tiếp `resp.message` / `data.message` bằng
    `apiErrorMessage(e, '<câu fallback tiếng Việt>')`:
    1. `saveConfig` → fallback 'Lỗi khi lưu cấu hình'
    2. `saveVersion` → 'Lỗi khi lưu phiên bản'
    3. commission save → 'Lỗi khi lưu quy chế hoa hồng'
    4. `deleteReg` → 'Lỗi khi xoá quy chế hoa hồng'
    5. year-bonus nhánh 422 (bug chính) → 'Dữ liệu chưa hợp lệ, vui lòng kiểm tra các ô báo đỏ'
    6. year-bonus non-422 → 'Lỗi khi lưu quy chế thưởng năm'
    7. terms save → 'Lỗi khi lưu điều khoản'
    8. `deleteTerm` → 'Lỗi khi xoá điều khoản'
  - Handler GET đã có fallback tiếng Việt hardcoded — KHÔNG đụng. Lỗi 500 ("Server Error") ngoài scope.

- [x] **Task 2: Verify bằng Playwright**
  - Tái hiện 422 qua catch block đã sửa (tab Quy chế thưởng năm, `bonus_rate = -5` lọt FE
    nhưng FAIL BE rule `min:0`).
  - Kết quả: toast ra **"Tỉ lệ chia thưởng không được nhỏ hơn 0"** (tiếng Việt), đúng câu từ
    `errors`. Confirm raw 422: `message: "The given data was invalid."`,
    `errors: { "rows.0.bonus_rate": ["Tỉ lệ chia thưởng không được nhỏ hơn 0"] }`.

### Checkpoint — 2026-10-16
Vừa hoàn thành: Task 1 (9 edit: 1 import + 8 toast) + Task 2 (verify Playwright PASS).
  Commit hrm-client `bd63c0489`, merge origin/develop (8 commit, không conflict), đã PUSH origin/develop (`6d79b4190`).
Đang làm dở: (không)
Bước tiếp theo: (feature hoàn tất)
Blocked: (không)
