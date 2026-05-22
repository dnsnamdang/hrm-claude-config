# Bộ lọc Kết quả thầu — Tóm tắt

**Mục tiêu:** Thêm filter "Kết quả thầu" vào màn danh sách gói thầu (`bid_package/bid_package`), cho phép lọc theo trường `result` trong bảng `bid_packages`.

**Scope:**
- FE: Thêm 1 Select2 filter vào khối bộ lọc trên `index.vue`
- BE: Thêm `->when()` xử lý param `result` trong `BidPackageService::index()`

**Quyết định lớn:**
- Dùng giá trị `0` cho "Chưa có kết quả" (result = null) để phân biệt với `undefined` (chưa chọn filter)
- 3 lựa chọn: Trúng thầu (1), Trượt thầu (2), Chưa có kết quả (0)

**Spec chi tiết:** `docs/superpowers/specs/2026-05-22-bid-package-result-filter-design.md`
