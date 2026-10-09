# Task P2-11 Report — Màn danh sách phiếu xuất bán hàng mượn

**Status:** DONE

## File tạo
- `pages/finance/borrow-sells/index.vue` (mới, copy khuôn `pages/finance/borrow-sell-requests/index.vue` rồi cắt theo 6 điểm "Đổi" trong brief). Không sửa file nào khác.

## Param filter cuối cùng (buildParams = filters + page + per_page)
`code`, `contractable_type`, `status`, `startDate`, `endDate` — đúng 5 param BE `BorrowSell::searchByFilter` đọc, không thêm param nào khác.

## formatMoney
Không tìm thấy helper `formatCurrency`/`formatNumber`/`toLocaleString` trong `@/utils/common.js` (đã grep). Tự viết method `formatMoney(v)` tối giản như brief đề xuất:
```js
formatMoney(v) {
    const n = Number(v || 0)
    return n.toLocaleString('vi-VN')
}
```

## Các điểm đã đổi (đối chiếu brief)
1. Nhận diện màn: title `Phiếu xuất bán hàng mượn`; `columnScreenKey`/`localStorageKey`/`table`/`filterFieldName` key → `finance_borrow_sells`; `pathsToKeep: ['/finance/borrow-sells']`; filter panel title `Bộ lọc phiếu xuất bán hàng mượn`; `V2BaseDataTable title="Phiếu xuất bán hàng mượn"`.
2. Bỏ nút "Tạo phiếu" + method `createItem` (giữ nút "Cấu hình cột").
3. `initialStateForm`/`filterFields()` chỉ còn `contractable_type` (options morph string HĐ hãng/HĐ dịch vụ), `status` (1 option "Đã duyệt"), `startDate`, `endDate`; `code` là ô tìm nhanh (`ignoredFields: ['code']`).
4. `allColumns()` thêm cột `sum_amount_after_extra_after_vat` ("Tổng tiền", align right) với slot `formatMoney`; cột `code` link `/finance/borrow-sells/${item.id}`.
5. `getRowActions` chỉ còn action `view` (`is_can_view`, fail-closed, không gán `true`); `handleRowAction()` để rỗng. Xoá toàn bộ nhánh manager_approve/switch_board/board_approve/deny, method `runRowAction`/`handleDenyConfirm`/`denyItem`/`denyMessage`, xoá `<BaseConfirmModal>` khỏi template.
6. Xoá import + khai báo component `BaseConfirmModal`. Giữ `V2BaseButton`, `V2BaseRowActions`, `V2BaseSmartFilterPanel`, `V2BaseDataTable`, `getNumericalOrder`, `mergeKnownFilters`.

## Grep tự kiểm
`grep -nE "deny|createItem|runRowAction|manager_approve|switchBoardOfManager|boardOfManagerApprove|BaseConfirmModal|can[A-Za-z]*\s*=\s*true" pages/finance/borrow-sells/index.vue` → không có kết quả (sạch).

## Eslint
**Không chạy được.** Project không có eslint local (`node_modules/.bin/eslint` không tồn tại). `npx eslint` kéo bản global eslint@10.10.0 → lỗi `TypeError: SUPPORTED_VERSIONS.at is not a function` (không tương thích Node 14.21.3 mà project dùng). Không có cấu hình eslint cục bộ để cài đúng version — bỏ qua bước này theo cho phép của brief, ghi rõ tại đây.

## Concerns
- Không có concern về logic/scope. Route chi tiết `/finance/borrow-sells/:id` (Task 13) và filter theo `employeeOptions`/permission cấp cao chưa cần tới trong task này, đúng như brief.
- Chưa build/run thử (brief yêu cầu không `nuxt build`).
