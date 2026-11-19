// Chụp ảnh "Báo cáo cẩu hàng bốc xếp theo nhà cung cấp" trên DEV (chỉ đọc) — thân dùng chung _capture_boc_xep.js.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước ...]
require('./_capture_boc_xep.js').run(__dirname, {
    route: '/transport/arrange-reports/by-supplier',
    nhom: 'Báo cáo bốc xếp',
    muc: 'Báo cáo cẩu hàng bốc xếp theo nhà cung cấp',
    leaf: true,
    amountHead: 'Số tiền (sau VAT)',
    filters: [['Kỳ', 'o_ky'], ['Công ty', 'o_congty'], ['Nhà cung cấp', 'o_ncc'], ['Loại bốc xếp', 'o_loai'], ['Phiếu hạch toán', 'o_phieuht']],
    dropdown: ['Nhà cung cấp', 'ETEK', '04_ncc_dropdown'],
    emptyText: 'Phiếu hạch toán',
    readPeriod: null,
    popupPeriod: null,
    popupRow: null,
    printPeriod: null,
}, process.argv.slice(2)).catch((e) => { console.error(e); process.exit(1); });
