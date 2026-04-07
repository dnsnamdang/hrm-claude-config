# Bug Fixer — ERP TPE

## Mục đích
Hướng dẫn debug và fix bug theo đúng quy trình project ERP TPE.

## Khi nào dùng
- Khi gặp lỗi trên local hoặc production
- Khi user báo bug cần trace nguyên nhân
- Khi test phát hiện behavior sai

## Quy trình debug

### Bước 1: Thu thập thông tin lỗi
- User mô tả: hành động nào → kết quả gì → kết quả mong muốn
- URL / màn hình nào?
- Lỗi xảy ra khi nào? (luôn luôn / random / lần đầu)

### Bước 2: Xác định lỗi BE hay FE

**Lỗi BE** (API trả 500, 400, response sai):
```
# Đọc log Laravel
hrm-api/storage/logs/laravel-[YYYY-MM-DD].log

# Tìm error gần nhất
Grep pattern: "ERROR" hoặc "Exception" trong file log ngày hôm nay
```

**Lỗi FE** (UI sai, không hiện data, crash):
```
# Check browser console
# Check network tab — API response có đúng không?
# Check Vue devtools — state/props có đúng không?
```

### Bước 3: Trace code

**BE trace flow:**
1. Route file: `Modules/[Module]/Routes/api.php` → tìm endpoint
2. Controller: method xử lý request
3. Service: business logic
4. Model/Entity: query, relationship
5. Transformer/Resource: format response

**FE trace flow:**
1. Page component: `pages/[module]/[page].vue`
2. Store action: `store/actions.js` → `apiGetMethod` / `apiPostMethod`
3. Component con: props, events
4. Computed/watch: reactive data

### Bước 4: Fix

- Tạo task trong `.plans/[feature]/plan.md` trước khi fix (kể cả bug nhỏ)
- Fix tại đúng layer gây lỗi — không patch ở layer khác
- Nếu cần sửa hàm dùng chung → HỎI trước, không tự sửa

### Bước 5: Verify
- Test lại flow gây lỗi
- Test các flow liên quan (regression)
- Check log không còn error

## Lỗi thường gặp trong project

| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| API 500 | Missing relation `with()`, null access, validation fail |
| API 403 | Thiếu permission trong seeder, sai tên permission |
| FE blank page | Import component sai, missing layout |
| FE data rỗng | API endpoint sai, response format khác expect |
| FE không reactive | Dùng `this.obj.newKey = val` thay vì `this.$set()` |
| Export Excel lỗi | Template blade sai column, data null |

## Quy tắc
- KHÔNG đoán nguyên nhân — đọc log/trace code trước
- KHÔNG sửa hàm dùng chung khi chưa được xác nhận
- KHÔNG tự quyết định `is_can_delete` — phải hỏi điều kiện
- Mỗi fix PHẢI có task trong plan.md
