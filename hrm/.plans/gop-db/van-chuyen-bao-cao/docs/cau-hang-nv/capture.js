// Chụp ảnh "Báo cáo cẩu hàng bốc xếp theo nhân viên" trên DEV (chỉ đọc) — thân dùng chung ../cau-hang-ncc/_capture_boc_xep.js.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
require('../cau-hang-ncc/_capture_boc_xep.js').run(__dirname, {
    route: '/transport/arrange-reports/by-employee',
    nhom: 'Báo cáo bốc xếp',
    muc: 'Báo cáo cẩu hàng bốc xếp theo nhân viên',
    leaf: false,
    amountHead: 'Số tiền',
    filters: [['Kỳ', 'o_ky'], ['Công ty', 'o_congty'], ['Nhân viên', 'o_nhanvien']],
    dropdown: ['Nhân viên', '', '04_nv_dropdown'],
    emptyText: null,
    readPeriod: 'Tháng trước',
    pagingPeriod: 'Năm nay',
    popupPeriod: 'Tháng trước',
    popupRow: 'Lê Văn Chiến',
    printPeriod: 'Tháng trước',
}, process.argv.slice(2)).catch((e) => { console.error(e); process.exit(1); });
