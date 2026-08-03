# Plan — Phụ lục thay đổi điều khoản thanh toán

**Người phụ trách:** @khoipv · **Ngày:** 2026-07-07
**Spec:** `docs/superpowers/specs/2026-07-07-contract-annex-payment-terms-design.md`
**Plan chi tiết (10 task):** `docs/superpowers/plans/2026-07-07-contract-annex-payment-terms.md`

## Trạng thái
- [x] Brainstorming + spec chi tiết
- [x] Lên plan chi tiết (10 task)
- [x] Phase 1 — Backend
  - [x] Task 1: Nhãn ANNEX_TYPE_LABELS + StoreRequest (review clean)
  - [x] Task 2: DetailResource (review clean)
  - [x] Task 3: Service (store/update/approve/destroy) (review clean; Minor: điều kiện has100 dư, literal 100PCT)
  - [x] Task 4: Controller + bản in động (review clean)
  - [x] Task 5: Routes + getDataForAnnexPaymentTerms (review clean; 8+1 route)
- [x] Phase 2 — Frontend
  - [x] Task 6: GeneralComponent (review clean; Minor: variables dead code)
  - [x] Task 7: add.vue + edit.vue (review clean)
  - [x] Task 8: index/detail/print (review clean; đã dọn dead code vat trong index.vue, PASS integrity)
  - [x] Task 9: ROUTE_MAP + API_MAP + menu (review clean)
  - [x] Task 10: Verify UI end-to-end (verify UI PASS)
- [x] Fix UI polish/bug
  - [x] Thêm `mt-3` cho row bọc GeneralComponent ở add/detail/edit (giãn cách header–tabs như phụ lục số lượng)
  - [x] Fix crash `Cannot read properties of undefined (reading 'number')` ở màn chi tiết: khởi tạo `formSubmit.contract = {}` + `getDetail` đọc `data.contract.groups` an toàn
  - [x] Fix HĐ gốc hiển thị sai điều khoản sau khi duyệt phụ lục: `ContractDetailResource` đọc `payment_terms`/`payment_terms_note` từ snapshot version 0 (giống `contract_end_time`/`time_progress`), fallback live cho HĐ cũ. Backfill điều khoản gốc vào v0 của HĐ 154 (test)
  - [x] Đăng ký biến mẫu in cho phụ lục: thêm 4 biến (`NGAY_LAP`, `BANG_DIEU_KHOAN`, `GHI_CHU_CU`, `GHI_CHU_MOI`) vào `PrintTemplateVariable::variablesType3()` + INSERT vào bảng `print_template_variables` (type 3) để bảng gợi ý biến hiển thị đầy đủ
  - [x] Chặn tạo phụ lục khi HĐ đang có phụ lục dở: nếu HĐ có bất kỳ phụ lục nào ở trạng thái đang tạo (1)/chờ duyệt (2) thì ẩn khỏi dropdown chọn HĐ ở CẢ 8 màn tạo phụ lục
    - BE: `ContractService::index` thêm filter opt-in `exclude_in_progress_annex` (`whereDoesntHave('annexes', status IN [1,2])`)
    - FE: 8 màn truyền `&exclude_in_progress_annex=1`; riêng `price` + `discount_appendix` (gọi getContracts cả màn sửa) chỉ truyền param khi `!isShow && !isEdit` để màn sửa vẫn thấy HĐ đã chọn
