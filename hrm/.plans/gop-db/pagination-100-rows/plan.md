# Plan — Thêm option 100 dòng/trang (gop-db)

> Nhánh: `gop_db` · Phụ trách: @khoipv

## Phase 1 — Khảo sát

- [x] Xác nhận đang đứng trên nhánh `gop_db` (cả `hrm-api` và `hrm-client`)
- [x] Liệt kê các màn đã chuyển sang HRM ở phần gop-db (finance, customer-care, assign/customers, human/banks)
- [x] Tìm mọi nơi render ô "Số dòng/trang" → `V2BaseDataTable` (default `[5,10,20,50]`),
      `V2BasePagination` (default `[10,20,50,100]`), 3 modal tự truyền `[20,50,100]`
- [x] Xác định màn gop-db nào tự truyền `page-size-options` (chỉ 3 modal, đều đã có 100)
- [x] Chốt với user: sửa default component chung, giữ option 5

## Phase 2 — Sửa code (FE)

- [x] `components/V2BaseDataTable.vue:250` — `[5, 10, 20, 50]` → `[5, 10, 20, 50, 100]`
- [x] Xác nhận không màn gop-db nào override prop bằng list thiếu 100

## Phase 3 — Verify

- [x] Parse lại `V2BaseDataTable.vue` bằng `vue-template-compiler` + `@babel/core` → template + script OK
- [x] Soát BE thật: `100` lọt ở mọi endpoint gop-db — phần lớn truyền thẳng vào `paginate()`;
      3 chỗ cap `min(100, …)` thì 100 đúng bằng trần; `/human/banks` dùng param `limit` (FE-BE khớp).
      Không phải sửa BE dòng nào.
- [x] User test trình duyệt — **PASS** (2026-08-13, user xác nhận)

## Phase 4 — Tài liệu

- [x] `.plans/gop-db/pagination-100-rows/design.md` — tóm tắt
- [x] `docs/superpowers/specs/gop-db/2026-08-13-pagination-100-rows-design.md` — spec đầy đủ
- [x] `.plans/gop-db/STATUS.md` — thêm entry vào mục "Đang làm"

---

### Checkpoint — 2026-08-13 (ĐÓNG FEATURE)
Vừa hoàn thành: **feature HOÀN THÀNH** — user đã test trình duyệt xong và xác nhận PASS.
Sửa default `pageSizeOptions` của `V2BaseDataTable` thành `[5, 10, 20, 50, 100]` (1 file / 1 dòng);
parse-check template + script pass; BE soát thật không phải sửa dòng nào; tài liệu đủ (design.md + spec + STATUS.md).
Đang làm dở: không có.
Bước tiếp theo: không còn việc trong feature này. Đã chuyển sang mục "Hoàn thành" của `.plans/gop-db/STATUS.md`.
Chờ merge về `gop_db` theo quy trình chung (chưa commit — theo quy tắc project, không tự commit).
Blocked:
