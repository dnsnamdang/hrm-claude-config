# Plan — Sổ Nhật ký chung (Kế toán HRM)

> Design tóm tắt: `design.md` · Spec đầy đủ: `docs/superpowers/specs/2026-07-18-so-nhat-ky-chung-hrm-design.md`
> **Plan chi tiết từng step (code + verify):** `docs/superpowers/plans/2026-07-18-so-nhat-ky-chung-hrm.md`
> Nhánh: `tpe-develop-accounting` (hrm-api + hrm-client).

## Phase 0 — Scaffold Module
- [ ] 0.1 Tạo & đăng ký module `Accounting` (module:make, modules_statuses.json, route prefix)
- [ ] 0.2 Permission `Xem sổ nhật ký chung` (PermissionsTableSeeder)

## Phase 1 — Backend (mysql2)
- [ ] 1.1 `AccountDetailBaseService` — getBuilder + applyFilter + join tên
- [ ] 1.2 Helper cây TK `resolveAccountIds` (+ unit test)
- [ ] 1.3 `GeneralJournalService` — select 20 chiều + sort + STT
- [ ] 1.4 Tổng phát sinh + lũy kế kỳ trước + cân đối (+ unit test)
- [ ] 1.5 `AccountingOrgController` — cascade 4 cấp nguồn ERP
- [ ] 1.6 `GeneralJournalController@index` + route + checkPermission

## Phase 2 — FE cốt lõi
- [ ] 2.1 Store `accounting/general-journal` + fetch/fetchOrg
- [ ] 2.2 `AccountingOrgCascade.vue` (4 cấp, V2BaseSelectRemote)
- [ ] 2.3 `GeneralJournalFilter.vue` (core: kỳ, từ–đến, TK, quick search, cascade)
- [ ] 2.4 `GeneralJournalTable.vue` + `journal-columns.js` (20 cột, header nhóm, tổng, badge)
- [ ] 2.5 Page `index.vue` ráp filter+table+pagination+sort
- [ ] 2.6 Menu client "Kế toán → Sổ nhật ký chung"

## Phase 3 — FE phụ trợ
- [ ] 3.1 Cấu hình cột (reuse column-customization-modal, kéo-thả + ẩn/hiện, localStorage)
- [ ] 3.2 Cài đặt trường lọc mặc định/mở rộng + field nâng cao + badge đếm
- [ ] 3.3 Ẩn/hiện toàn bộ khu bộ lọc (localStorage)

## Phase 4 — In & Excel
- [ ] 4.1 Xuất Excel (Export FromView + blade S03a-DN + endpoint + nút)
- [ ] 4.2 In sổ S03a-DN client-side (9 cột chuẩn + TK đối ứng + chữ ký)

## Phase 5 — Verify
- [ ] 5.1 Đối chiếu ΣNợ=ΣCó, cascade+TK cây, lũy kế, hiệu năng + index ERP
- [ ] 5.2 Cập nhật plan.md/STATUS.md

## Phase 6 — Dọn ERP
- [ ] 6.1 Gỡ code Sổ NKC đã lỡ làm ở ERP (nhánh so_nhat_ky_chung) — hỏi user cách gỡ + cập nhật memory/STATUS ERP
