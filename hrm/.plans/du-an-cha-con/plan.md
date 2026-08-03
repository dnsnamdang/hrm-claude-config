# Plan — Dự án cha → Dự án con (dự án TKT)

**Spec:** `docs/superpowers/specs/2026-07-20-du-an-cha-con-design.md`
**Design tóm tắt:** `.plans/du-an-cha-con/design.md`
**Phụ trách:** @dnsnamdang · **Branch dự kiến:** `tpe-develop-assign` (xác nhận với user trước khi code)

---

## Phase 0 — Brainstorming & Design
- [x] Khảo sát hiện trạng Modules/Assign (dự án TKT, quotation, BOM, luồng duyệt)
- [x] Chốt 5 quyết định nghiệp vụ (mô hình con, 2 tầng, tạo con, cấp duyệt, vòng đời, hiển thị)
- [x] Viết spec đầy đủ + design tóm tắt
- [ ] User review spec → xác nhận trước khi lên plan chi tiết / code

## Phase 1 — Backend (chưa bắt đầu)
- [ ] Migration index `prospective_projects.parent_id`
- [ ] Entity `ProspectiveProject`: quan hệ `parent()/children()`, const CLOSED_STATUSES, `isClosed()`, `openChildren()`
- [ ] `ProspectiveProjectRequest`: rule `parent_id` + `withValidator()` 6 rule nghiệp vụ
- [ ] `ProspectiveProjectService::close()`: chặn khi còn con mở (kèm mã con)
- [ ] API `GET {id}/children` (method `children`) + roll-up giá bán đã duyệt (status=4), KHÔNG lộ giá vốn
- [ ] `getAll?parent_candidates=1`: lọc `whereNull parent_id` + chưa đóng
- [ ] Transformers: detail thêm `parent` + `children_count`; index thêm `parent_code/name`; filter `parent_id`
- [ ] Route `children`; `php -l` sạch

## Phase 2 — Frontend (chưa bắt đầu)
- [ ] `RelatedSection.vue`: nguồn `parent_candidates`, disable khi có con, map 12 status, xóa console.log
- [ ] `_id/index.vue`: tab "Dự án con" + roll-up tổng + nút "Tạo dự án con" + link về cha
- [ ] `add.vue`: prefill từ `?parent_id=` (KH khóa, NVKD + phân loại cho sửa)
- [ ] `index.vue`: cột "Dự án cha" + filter `parent_id`

## Phase 3 — Kiểm thử (chưa bắt đầu)
- [ ] E2E validation parent_id (6 ca) + đóng cha có con mở
- [ ] Tab con roll-up đúng, không lộ giá vốn (cover có quyền + không quyền)
- [ ] Regression luồng báo giá dự án con (BOM→request→báo giá→duyệt 1/2/3)

---

### Checkpoint — 2026-07-20
Vừa hoàn thành: Brainstorming xong 5 quyết định nghiệp vụ; viết spec đầy đủ (`docs/superpowers/specs/2026-07-20-du-an-cha-con-design.md`) + design tóm tắt (`.plans/du-an-cha-con/design.md`); tự rà soát spec (không placeholder, nhất quán).
Đang làm dở: chưa code. Chờ user review spec.
Bước tiếp theo: user duyệt spec → dùng skill writing-plans lên plan chi tiết hoặc bắt đầu Phase 1 BE (migration + validation). Xác nhận branch trước khi code.
Blocked: chờ user review spec.
