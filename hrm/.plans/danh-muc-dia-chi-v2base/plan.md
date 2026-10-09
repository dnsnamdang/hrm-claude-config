# Chuyển danh mục địa chỉ HRM sang V2Base (nhánh gop_db)

## Scope
4 trang danh mục địa chỉ (pages/human) hiện KHÔNG dùng V2Base → chuyển sang V2Base:
- provinces (Tỉnh/TP)
- districts (Quận/Huyện)
- wards (Phường/Xã)
- hamlets (Đường/Phố)

## Pattern áp dụng (theo cost-debts)
- V2BaseFilterPanel (quick search + advanced filters cascade) + V2BaseDataTable (columns + pagination + actions-bottom) + BaseConfirmModal (xóa/khóa mềm).
- filterStateMixin + deep watcher auto-search (list-page skill).
- `@import '@/assets/scss/v2-styles.scss'`.
- Giữ modal hiện có (DistrictModel/...) — chỉ đổi cách mở (v-b-modal → $bvModal.show + editId).
- Giữ nguyên: không permission (đồng bộ màn địa lý), "xóa" = khóa mềm, cascade Quốc gia→Tỉnh→(Huyện→Xã).

## Tasks
- [x] districts (pilot) → V2Base index + DistrictModel V2 (ref-based)
- [x] hamlets → V2Base index + HamletModel V2 (cascade tỉnh→phường/xã)
- [x] provinces → V2Base index (status + Sửa/Xóa/Khóa/Mở khóa) + ProvinceModel V2 (cascade quốc gia→khu vực, Lưu và làm tiếp)
- [x] wards → V2Base index (status + lock/unlock, cascade filter quốc gia→tỉnh) + WardModel V2
- [x] sửa cả modal sang V2 (ref-based open(id)/@saved, V2BaseInput/SelectInModal, inline error + touched)
- [x] fix merge conflict gop_db: dời 8 file V2Base human→master-data, đổi endpoint human/→master-data/, provinces/wards POST-kèm-id (BE không có PUT)
- [x] nations (quốc gia) → V2Base index (status + lock/unlock, filter name+status) + NationModel V2 (name/code/postal_code, POST upsert)
- [x] areas (khu vực) → V2Base index (status + lock/unlock, filter name+nation_id+status) + AreasModel V2 (name/nation_id cascade, POST upsert)
- [ ] user verify build/lint (yarn dev) — chưa chạy được tại chỗ

## Ghi chú
Branch gop_db. layout giữ 'subsystem'. API giữ nguyên (human/{provinces,districts,wards,hamlets}).
