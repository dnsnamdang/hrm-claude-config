# FE Report — Dashboard Kinh doanh (Phase 2)

**Status:** DONE  
**Ngày:** 2026-06-28  
**Review:** Phase 2 FE đã được duyệt (Spec ✅, Quality Approved). Đã fix 1 Important [I-1].

## Fix sau review

- **[I-1] `emptyDashboard` reactive-share reference** — Đổi từ object const dùng chung sang **factory function** `const emptyDashboard = () => ({...})`. Mọi tham chiếu (`data()`, fallback khi không có `response.data`, và error handler) đều gọi `emptyDashboard()` để tạo object mới, tránh share nested reference (`kpis`, `conversion`...) giữa các lần reset. Đã grep xác nhận 4 chỗ đều gọi như function (dòng 216 định nghĩa; 253/498/506/509 gọi).

---

## File tạo / sửa

| File | Hành động |
|------|-----------|
| `nhatlinh-client/store/sale-dashboard.js` | Tạo mới |
| `nhatlinh-client/pages/sale/dashboard/index.vue` | Viết lại (thay placeholder) |
| `nhatlinh-client/components/default-menu/sale.js` | Sửa `isShow` của mục Tổng quan |

---

## Task 5 — Store `sale-dashboard.js`

Tạo theo đúng mẫu `store/sale-quotation.js`. Export `state`, `mutations`, `actions`, `getters`.  
Action `get` dispatch root `apiGetMethod` đến `sale/dashboard${query}`.

---

## Task 6 — Filter + 4 KPI card

- Thanh lọc: `V2BaseCompanyDepartmentFilter` + 2 `V2BaseDatePicker` trong một `form-row` bên trong card.
- `filters.from_date` default = `dayjs().startOf('year').format('YYYY-MM-DD')`, `filters.to_date` = `dayjs().format('YYYY-MM-DD')`.
- `loadData()` gọi `buildQueryString` → dispatch `sale-dashboard/get` → set `dashboardData`.
- Watch `filters` deep với debounce 400ms để tự reload khi đổi filter.
- 4 KPI card Bootstrap 4 col-md-3: Báo giá chờ duyệt (link `/sale/quotation-approval`), Hợp đồng chờ duyệt (link `/sale/contract-approval`), Doanh số HĐ đã duyệt, Tỉ lệ chốt.
- Số tiền dùng `| formatNumber` (global filter). Container chính `padding-bottom: 60px`. Spinner khi loading.
- Empty-safe: `dashboardData` init bằng `emptyDashboard` const với giá trị mặc định 0 cho mọi nested key.

---

## Task 7 — Chart Doanh số theo thời gian

- `apexchart: () => import('vue-apexcharts')` (lazy import, chuẩn dự án).
- Computed `revenueSeries` + `revenueOptions`: 2 series (Báo giá đã duyệt / Hợp đồng đã duyệt), xaxis = month, yaxis dùng `shortMoney()` helper (tr/tỷ), tooltip ra số đầy đủ qua `$options.filters.formatNumber`.
- Empty-state: khi `revenue_by_month` toàn 0 hoặc rỗng → hiện icon + text "Chưa có dữ liệu".

---

## Task 8 — Chart Tỉ lệ chuyển đổi + Top 10 KH

- Layout 2 cột `col-md-6`.
- Chart 4a (chuyển đổi): bar ngang `horizontal: true, distributed: true`, 2 categories: ['Báo giá đã duyệt', 'HĐ chốt']. Kèm 2 dòng text % phía dưới: theo số lượng + theo giá trị, guard chia 0.
- Chart 4b (top KH): bar ngang, series từ `top_customers.contract_amount`, categories = `customer_name`. Height động theo số lượng KH (`Math.max(250, count * 35 + 60)`).
- Empty-state mỗi khối khi data rỗng.

---

## Task 9 — Menu + Route guard

**File sửa:** `nhatlinh-client/components/default-menu/sale.js`  
**Cơ chế:** Mục `'Tổng quan'` đã có sẵn trong `saleItems` với `isShow: true`. Đã đổi thành `isShow: ['Xem dashboard kinh doanh']`.

**Cơ chế hoạt động (đúng pattern cũ):**
- `isShow: [...]` → `checkPermission.js` middleware kiểm `store.state.permissions` khi route change.
- Nếu user không có permission name trong mảng → redirect `/pages/extras/404` (ẩn menu + chặn URL trực tiếp).
- Sidebar component (component riêng render menu) cũng đọc `isShow` để ẩn/hiện item.

---

## Điểm lệch vs plan + cách xử lý

1. **Plan dùng V2BaseFilterPanel** (dạng collapsible) — Dashboard không cần advanced filter collapse vì không có bảng dữ liệu, nên dùng `card` đơn giản với `form-row`. Phù hợp hơn về UX dashboard.
2. **`permissions` cho V2BaseCompanyDepartmentFilter** — Plan không nêu rõ quyền nào dùng. Dùng OR của cả báo giá + hợp đồng để hiển thị filter level tương ứng mà user có.
3. **Chart `xaxis.labels` cho Top KH** — Khi `customer_name` dài, có thể bị cắt. Đã set `fontSize: '11px'` nhưng không cấu hình `trim` — có thể cần chỉnh sau khi test thực tế.

---

## Concerns (không build được)

1. **Không thể build/chạy để xác nhận runtime** — Node cũ, không build được. Đã kiểm tra thủ công:
   - Tất cả import file đều tồn tại thật (đã `ls` xác nhận).
   - Tên action store `sale-dashboard/get` khớp chính xác với store export.
   - Key API response (`response.data.kpis`, `.revenue_by_month`, `.conversion`, `.top_customers`) khớp với spec.
   - Global filter `formatNumber` và mixin `hasAPermission` đã xác nhận là global.
   - `apexchart` lazy import đúng pattern mẫu.
2. **`formatNumber` trả `-` khi value = 0** — KPI card sẽ hiện `- ₫` khi tiền = 0. Đây là convention toàn dự án, không thay đổi.
3. **Chart top KH axes** — Reviewer đã xác nhận `xaxis.categories` (tên KH) + `yaxis.labels.formatter` (rút gọn số tiền) hiện tại ĐÚNG. Không cần đổi. (Đã tinh chỉnh: chuyển formatter rút gọn từ `xaxis.labels` sang `yaxis.labels` cho horizontal bar.)
4. **Double-call loadData khi mount** — giữ nguyên (đúng pattern quotation-approval của dự án, reviewer xác nhận).
