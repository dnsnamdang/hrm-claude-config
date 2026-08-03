# Task 8 — Menu "Tổng quan" — Report

**Status:** ✅ Completed

**File thay đổi:**
- `/Users/dnsnamdang/Documents/DNSMEDIA/websites/nhatlinh/nhatlinh-client/components/default-menu/warehouse.js`

**Thay đổi chi tiết:**
- Thêm mục mới vào đầu mảng `warehouseItems` (dòng 2-7):
  ```js
  {
      label: 'Tổng quan',
      icon: 'ri-dashboard-line',
      link: '/warehouse/dashboard',
      isShow: ['Xem dashboard kho'],
  },
  ```

**Verify:**
- ✅ Mục "Tổng quan" nằm đầu mảng (index 0)
- ✅ Indent 4 spaces khớp chuẩn file
- ✅ Cú pháp object hợp lệ: dấu phẩy đúng sau object này + sau tất cả object khác
- ✅ `isShow` chứa permission name "Xem dashboard kho" (khớp Task 3 permission 1138)
- ✅ `link: '/warehouse/dashboard'` khớp endpoint từ Task 5 + trang FE Task 7

**Concerns:**
- Không có — Task hoàn thành đầy đủ theo spec Task 8.
