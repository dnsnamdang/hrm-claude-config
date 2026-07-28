# Tối ưu tốc độ load màn danh sách báo giá (/assign/quotations)

## Nguyên nhân
- `index.vue mounted()` await `loadFilterOptions()` (Promise.all 3 request nặng: prospective-projects/getAll 5.4s, solutions/getAll 1.8s, customers 10k) TRƯỚC `fetchData()` → danh sách (chỉ 150ms) bị chặn ~5.4s+.
- Deep-watcher `filters` bắn `fetchData` trùng do gán `this.filters` từ savedState.

## FE
- [x] Đảo thứ tự mounted: khôi phục savedState → fire `fetchData()` ngay (không await) → `getFields()` + `loadFilterOptions()` chạy nền
- [x] Thêm cờ `suppressFilterWatch` chặn watcher bắn `fetchData` trùng khi khởi tạo
- [x] Khởi tạo `loading: true` để bảng hiện spinner ngay frame đầu (giống prospective-projects)

## Đã đo trên local (127.0.0.1:3001 → BE :8002) sau fix
- quotations list API: 139ms; bảng render khung + header ngay lập tức ✅
- Các request filter nặng (projects/solutions/customers getAll per_page=10000) chạy nền, không chặn danh sách
- Màn create (/quotations/create): ~15 call; phần lớn call chậm là của LAYOUT sidebar (user-profile, master-settings, training/*, daily-report/count) bắn ở MỌI trang; 6 call riêng của form đã Promise.all song song (chậm nhất ~864ms), có hiện "Đang tải..."

## Lưu ý
- Nuxt HMR KHÔNG chạy lại mounted() → phải HARD REFRESH (Ctrl/Cmd+Shift+R) mới thấy tác dụng

---

# Phase 2 — Tối ưu sâu (user chọn #1 + #2)

## ⚠️ Phát hiện quan trọng: sửa NHẦM thư mục
- Server :3001 (FE) chạy từ `HRM-tpe/hrm-client` nhánh **tpe**; BE :8002 từ `HRM-tpe/hrm-api`
- Ban đầu sửa nhầm ở `HRM/hrm-client` (nhánh tpe-develop-assign) → không có tác dụng
- Đã revert HRM/hrm-client. TẤT CẢ thay đổi giờ CHỈ trên nhánh **tpe** (HRM-tpe)

## #1 Tối ưu layout sidebar (dùng chung — lợi mọi trang) — DONE
- [x] Khảo sát: thủ phạm = `middleware/authenticated.js` await `master-settings?category=use_erp` MỖI route → chặn hiển thị trang ~0.5-1.5s
- [x] Sửa middleware (HRM-tpe): chỉ fetch use_erp cho /assign/assign_business; các route khác bỏ hẳn → chuyển route tức thì
- [x] Verified: SPA nav → spinner hiện 245ms (trước 1.4s); list call 255ms (trước 1409ms)

## #2 Filter dropdown → search server-side lazy (Dự án / Giải pháp / Khách hàng) — DONE
- [x] Dùng component có sẵn `V2BaseSelectRemote` (select2 ajax + debounce 300ms)
- [x] FE (HRM-tpe index.vue): 3 dropdown → V2BaseSelectRemote + fetchProjects/fetchSolutions/fetchCustomers (keyword, per_page=20); initialOption khôi phục nhãn khi vào lại từ filter đã lưu; @change reset field phụ thuộc
- [x] BE (HRM-tpe): thêm `keyword` cho ProspectiveProjectService::getAll; solutions/getAll + customers/search đã sẵn
- [x] Verified: không còn call per_page=10000; fetchProjects('dự')→8 kết quả (213ms), fetchCustomers→20 (253ms)

---

# Phase 3 — Áp cho bom-list + pricing-requests (nhánh tpe)

## pricing-requests — full (list-load + lazy) — DONE
- [x] mounted reorder (fetchData ngay), loading:true, suppressFilterWatch
- [x] 2 dropdown (Dự án, Giải pháp) → V2BaseSelectRemote lazy + restoreFilterLabels
- [x] Verified: không còn per_page=10000; fetchProjects trả 20; 0 lỗi console

## bom-list — chỉ Part A (list-load) — DONE
- [x] mounted reorder (loadData ngay, options nạp nền), loading:true
- [x] Guard isCascading để cascade KHÔNG phá giá trị khi khôi phục filter đã lưu
- [x] KHÔNG chuyển dropdown sang lazy: bom-list có cascade (chọn dự án → auto-fill giải pháp/khách hàng/hạng mục) dựa vào full data client-side; lazy sẽ phá cascade → giữ full-load nhưng chạy NỀN
- [x] Verified: list call 2174ms (sớm), cascade auto-fill customer OK, options nạp nền 33 dự án
- Ghi chú: 6 Vue dev-warning "V2BaseButton prop type" là CÓ SẴN (nút thao tác dòng bảng, dùng chung V2BaseDataTable), không phải regression

## BE: không cần thêm — dùng chung endpoint đã có keyword (prospective getAll thêm ở Phase 2, solutions/customers sẵn)

---

# Phase 4 — Form tạo/sửa báo giá hiện ngay (edit.vue, nhánh tpe)

## FE (HRM-tpe/hrm-client/pages/assign/quotations/_id/edit.vue)
- [x] mounted: KHÔNG await Promise.all 5 call options/config (currencies/configs/units/discount_types/term-templates) → cho chạy NỀN (this._optsReady); chỉ chờ initCreateMode/fetchData
- [x] initCreateMode: tạo trắng → loadMyProjects() chạy NỀN (form hiện ngay); luồng ?project_id= giữ nguyên (await projects + _optsReady + selectProject trước khi auto-fill giá)
- [x] Verified 1 phần LIVE (trước khi BE tắt): sau khi bỏ await Promise.all → form hiện 1404ms (options nạp nền từ ~217ms); 2 lỗi console là VatBulkApplyToolbar quotationId=null CÓ SẴN (create mode id=null), không phải regression
- [x] Verified LIVE (BE đã chạy lại):
  - CREATE (tạo trắng): form hiện **115ms** (trước 1404ms → gốc ~1.5-2s). 6 lỗi = VatBulkApplyToolbar quotationId=null CÓ SẴN (create mode id=null), không phải regression
  - EDIT (/91/edit): **0 lỗi**, form load đủ data (4 SP, giá, tỷ giá AUD, tổng); roundingMode=null = "Mặc định (tối đa 2 số lẻ)" hiển thị đúng (KHÔNG phải bug — currencyDefaultRounding=null cho AUD kể cả khi currencies đã nạp → code cũ cũng vậy)
  - SHOW (/91): load tốt; 2 lỗi V2BaseButton prop type CÓ SẴN (dùng chung, không đụng _id/index.vue)
