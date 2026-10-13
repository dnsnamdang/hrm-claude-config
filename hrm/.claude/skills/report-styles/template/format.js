/**
 * Định dạng dùng chung của báo cáo tổng hợp CSKH tiềm năng (khối tổng hợp, bảng cây, popup).
 * Số: `,` ngăn nghìn, `.` thập phân (toLocaleString('en-US')). Ngày: dd/mm/yyyy.
 * Khuôn copy từ `pages/assign/report/service-demand/format.js`.
 */

export function num(v) {
    const n = Number(v)
    if (v === null || v === undefined || v === '' || isNaN(n)) return ''
    return n.toLocaleString('en-US', { maximumFractionDigits: 2 })
}

/** 'yyyy-mm-dd' (có thể kèm giờ) -> 'dd/mm/yyyy'. Chuỗi rỗng/sai khuôn -> ''. */
export function dmy(ymd) {
    if (!ymd) return ''
    const m = String(ymd).match(/^(\d{4})-(\d{2})-(\d{2})/)
    return m ? `${m[3]}/${m[2]}/${m[1]}` : ''
}

/** Dòng phụ cạnh hạn theo dõi: "còn N ngày" / "hết hạn hôm nay" / "quá hạn N ngày" (cron đóng hằng ngày nên âm chỉ tạm thời) */
export function daysNote(daysLeft) {
    if (daysLeft === null || daysLeft === undefined || daysLeft === '') return ''
    const d = Number(daysLeft)
    if (isNaN(d)) return ''
    if (d === 0) return 'hết hạn hôm nay'
    return d > 0 ? `còn ${num(d)} ngày` : `quá hạn ${num(-d)} ngày`
}

/** Nhãn loại việc */
export function typeText(type) {
    return type === 'nc' ? 'Nhu cầu' : 'Dự án TKT'
}
