# timesheet-detail-note — Plan

> Plan chi tiết (TDD/steps): `docs/superpowers/plans/2026-06-15-timesheet-detail-note.md`

## Phase 1 — Hiển thị cột Ghi chú

### BE
- [x] Thêm `'note' => $guide->note` vào `TimekeeperListResource::toArray` (sau `'place'`)

### FE
- [x] Thêm `{ key: 'note', label: 'Ghi chú' }` cuối mảng `fields` của `TimeSheetDetailModal.vue`

### Verify
- [ ] Browser: modal hiện ghi chú app đúng nội dung
- [ ] Browser: chấm máy / không ghi chú → ô trống, không vỡ layout
- [ ] Browser: màn "Dữ liệu chấm công" độc lập giữ nguyên (không có cột Ghi chú)

---

### Checkpoint — 2026-06-15
Vừa hoàn thành: Code BE (TimekeeperListResource +note) + FE (TimeSheetDetailModal +cột Ghi chú). php -l pass.
Đang làm dở: chưa verify browser
Bước tiếp theo: user verify trên browser (3 case Task 3)
Blocked:
