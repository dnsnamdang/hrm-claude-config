/**
 * Dữ liệu MOCK cho màn "Khai Quy chế – Cấu hình".
 *
 * ⚠️ Giai đoạn hiện tại CHỈ dựng UI — toàn bộ dữ liệu dưới đây là mock tĩnh,
 * chưa gọi API / chưa đụng store / DB. Khi làm logic sẽ thay bằng dữ liệu thật
 * từ backend (bảng configs cấp công ty + quy chế theo phòng ban, kèm cột
 * effective_from / status cho tính năng "hẹn ngày áp dụng").
 *
 * Port 1-1 từ bản mockup đã demo (hen-ngay-ap-dung-mockup.html).
 */

/* ---------- helper khai field ---------- */
export const num = (label, unit, val, def) => ({ t: 'number', label, unit, val, def })
export const txt = (label, val) => ({ t: 'text', label, val })
export const area = (label, val, wide = true) => ({ t: 'area', label, val, wide })
export const tags = (label, val) => ({ t: 'tags', label, val, wide: true })
export const tog = (label, items) => ({ t: 'toggles', label, items, wide: true })
export const logo = () => ({ t: 'logo', label: 'Logo hệ thống' })
export const sub = (label, cols, rows) => ({ t: 'subtable', label, cols, rows, wide: true })
export const sel = (label, val, opts) => ({ t: 'select', label, val, opts })
export const dateField = (label, val, fixed = false) => ({ t: 'date', label, val, fixed })

/**
 * Các tab KHÔNG hẹn ngày áp dụng (sửa là áp dụng ngay):
 * - chung: nhận diện & thông tin công ty
 * - thitruong: cơ cấu tổ chức / danh mục thị trường
 * - quyettoan: mốc ngày cố định theo năm
 */
export const NO_HEN = ['chung', 'thitruong', 'quyettoan']
export const canHenTab = (gid) => !NO_HEN.includes(gid)

/* ---------- mô hình dữ liệu ---------- */
export const DATA = {
    company: {
        chip: 'chip-com',
        chipText: 'Theo công ty',
        groups: [
            {
                id: 'chung',
                name: 'Chung',
                sub: 'Nhận diện & thông tin công ty',
                icon: 'cog',
                type: 'form',
                fields: [
                    logo(),
                    txt('Tiêu đề hệ thống (theo công ty)', 'ERP Tân Phát – ETEK'),
                    area('Mô tả', 'Hệ thống quản trị bán hàng – kho – kế toán'),
                ],
            },
            {
                id: 'baogia',
                name: 'Báo giá – Hợp đồng',
                sub: 'Hiệu lực, điều khoản & ngưỡng HĐ',
                icon: 'doc',
                type: 'form',
                eff: '2026-01-01',
                pending: [
                    {
                        date: '2026-10-01',
                        who: 'DNS Admin',
                        note: 'Điều chỉnh chính sách báo giá Q4/2026',
                        changes: [
                            { label: 'Số ngày hiệu lực báo giá', old: '15', new: '20', unit: 'ngày' },
                            { label: '% Hiệu quả HĐ tối thiểu', old: '12', new: '14', unit: '%' },
                        ],
                    },
                ],
                fields: [
                    num('Số ngày hiệu lực báo giá', 'ngày', 15),
                    num('Số ngày hiệu lực báo giá dự án', 'ngày', 30),
                    num('Thời gian đăng ký khách hàng', 'ngày', 7),
                    num('% Hiệu quả HĐ tối thiểu', '%', 12),
                    num('% Thưởng thực hiện HĐ tối đa', '%', 8),
                    num('% Tối thiểu hưởng doanh số của người lập HĐ', '%', 30),
                    num('SL nhân viên tối đa / 1 phòng tham gia HĐ', 'NV', 8),
                    area('Điều khoản báo giá mặc định', 'Giá trên đã bao gồm VAT. Báo giá có hiệu lực trong thời hạn nêu trên…'),
                    area('Điều khoản báo giá dịch vụ mặc định', 'Chi phí dịch vụ chưa bao gồm vật tư thay thế…'),
                    tog('Ràng buộc lập HĐ theo thị trường', [
                        ['Thiết bị', 1],
                        ['Sửa chữa', 1],
                        ['Dự án', 0],
                        ['Nguyên tắc', 0],
                        ['Nguyên tắc nha khoa', 0],
                    ]),
                ],
            },
            {
                id: 'kythuat',
                name: 'Kỹ thuật',
                sub: 'Đơn giá công & bảng tính công khoán',
                icon: 'tech',
                type: 'form',
                eff: '2026-01-01',
                fields: [
                    num('Đơn giá công', 'đồng', 350000),
                    num('Công khoán', 'đồng', 500000),
                    sub('Bảng tính công khoán', ['Nhóm hàng', 'Tính chất hàng hóa', 'Số lượng'], [
                        ['Thiết bị nha khoa', 'Hàng nhập khẩu', '120'],
                        ['Vật tư tiêu hao', 'Hàng thương mại', '450'],
                        ['Máy nén khí', 'Hàng lắp ráp', '60'],
                    ]),
                ],
            },
            {
                id: 'giaban',
                name: 'Giá bán',
                sub: 'Hệ số giá bán, giá vốn & TMĐT',
                icon: 'price',
                type: 'form',
                eff: '2026-01-01',
                pending: [
                    {
                        date: '2026-12-01',
                        who: 'DNS Admin',
                        note: 'Áp dụng bảng hệ số 2027',
                        changes: [{ label: 'Hệ số tính giá bán dịch vụ', old: '1.35', new: '1.40', unit: '' }],
                    },
                ],
                fields: [
                    num('Hệ số tính giá bán dịch vụ', '', 1.35),
                    num('Hệ số tính giá bán dịch vụ thuê ngoài', '', 1.5),
                    num('Hệ số tính giá vốn dịch vụ', '', 1.2),
                    num('Hệ số giá thương mại điện tử', '', 1.05),
                    num('Định mức đàm phán giá', '%', 5),
                ],
            },
            {
                id: 'chietkhau',
                name: 'Chiết khấu & hỗ trợ bán hàng',
                sub: 'CK và hỗ trợ vận chuyển',
                icon: 'cut',
                type: 'form',
                eff: '2026-01-01',
                fields: [
                    num('Tỷ lệ % Chiết khấu dịch vụ', '%', 5),
                    num('Tỷ lệ % chiết khấu hàng làm dịch vụ', '%', 3),
                    num('Số KM hỗ trợ vận chuyển', 'km', 30),
                    num('Giá trị đơn hàng hỗ trợ vận chuyển', 'đồng', 5000000),
                ],
            },
            {
                id: 'thitruong',
                name: 'Tổ chức bán hàng & thị trường',
                sub: 'Phân & ràng buộc thị trường',
                icon: 'market',
                type: 'form',
                fields: [
                    sel('Phân thị trường theo', 'Theo tỉnh / thành phố', [
                        'Theo tỉnh / thành phố',
                        'Theo quận / huyện',
                        'Theo phòng ban',
                    ]),
                    tags('Phòng ban không ràng buộc thị trường', ['Phòng Dự án', 'Phòng Dịch vụ']),
                    tags('Nhóm KH không ràng buộc thị trường', ['Khách dự án', 'Đại lý cấp 1']),
                ],
            },
            {
                id: 'congno',
                name: 'Công nợ & tài chính',
                sub: 'Hạn mức, lãi suất & mốc công nợ',
                icon: 'debt',
                type: 'form',
                eff: '2026-01-01',
                pending: [
                    {
                        date: '2026-11-01',
                        who: 'DNS Admin',
                        note: 'Tăng lãi suất quá hạn',
                        changes: [{ label: 'Lãi suất', old: '1.5', new: '1.6', unit: '%' }],
                    },
                ],
                fields: [
                    dateField('Ngày khai báo công nợ đầu kỳ', '2026-01-01', true),
                    num('Hạn mức công nợ xuất hàng NV', 'đồng', 200000000),
                    num('Số dư lẻ tối đa cho phép điều chỉnh', 'đồng', 50000),
                    num('Số ngày quá hạn tính lãi (Bán lẻ)', 'ngày', 30),
                    num('Số ngày quá hạn tính lãi (Đại lý)', 'ngày', 45),
                    num('Số ngày quá hạn tính lãi (Dịch vụ)', 'ngày', 60),
                    num('Thời gian cảnh báo thu nợ đến hạn', 'ngày', 7),
                    num('Lãi suất', '%', 1.5),
                    num('Thuế vận tải', '%', 8),
                ],
            },
            {
                id: 'xnk',
                name: 'Xuất – nhập hàng',
                sub: 'Giữ / mượn / nhập thẳng',
                icon: 'box',
                type: 'form',
                eff: '2026-01-01',
                fields: [
                    num('Số ngày cảnh báo (mượn/giữ hàng)', 'ngày', 3),
                    num('Hạn xuất hàng nhập thẳng', 'ngày', 5),
                    num('Giới hạn giá trị hàng mượn', 'đồng', 100000000),
                    num('Số lượng hàng trong tờ khai hải quan', 'SP', 500),
                    num('Số ngày vượt quá thời gian cần giao', 'ngày', 3),
                    num('% Đặt cọc – điều kiện giữ hàng', '%', 30),
                    num('Giá trị giữ hàng khác', 'đồng', 2000000),
                    num('Số ngày giữ tối đa – HĐDA', 'ngày', 45),
                    num('Số ngày giữ tối đa của hàng gửi', 'ngày', 30),
                    num('Số ngày giữ tối đa', 'ngày', 15),
                    num('Số ngày mượn tối đa', 'ngày', 20),
                ],
            },
            {
                id: 'hanghoa',
                name: 'Hàng hóa',
                sub: 'Tính chất, duyệt giá & serial',
                icon: 'goods',
                type: 'form',
                eff: '2026-01-01',
                fields: [
                    tags('Tính chất hàng hóa', ['Hàng nhập khẩu', 'Hàng thương mại', 'Hàng lắp ráp']),
                    tags('Hàng không bắt buộc serial', ['Vật tư tiêu hao', 'Phụ kiện']),
                    tags('Nhãn hiệu áp dụng', ['Etek', 'Woson', 'Coxo']),
                    num('Hệ số thuế bảo vệ môi trường', '%', 2),
                    tog('Quy tắc duyệt giá', [
                        ['Hàng cập nhật giá', 1],
                        ['Cập nhật giá cần duyệt', 1],
                        ['Hàng mới cần duyệt giá', 1],
                        ['Hàng reset giá', 0],
                    ]),
                ],
            },
            {
                id: 'quyettoan',
                name: 'Kỳ quyết toán',
                sub: 'Khai theo năm',
                icon: 'cal',
                type: 'form',
                fields: [
                    sub('Kỳ quyết toán', ['Năm', 'Từ ngày', 'Đến ngày'], [
                        ['2025', '01/01/2025', '31/12/2025'],
                        ['2026', '01/01/2026', '31/12/2026'],
                    ]),
                ],
            },
            {
                id: 'dieukhoan',
                name: 'Điều khoản',
                sub: 'Báo giá & thanh toán',
                icon: 'doc',
                type: 'form',
                eff: '2026-01-01',
                note: 'Điều khoản thanh toán hiện chưa có màn khai — bổ sung khi làm logic',
                fields: [
                    area('Điều khoản báo giá (theo công ty)', 'Giá trên đã bao gồm VAT. Báo giá có hiệu lực trong thời hạn nêu trên…'),
                    area('Điều khoản thanh toán (theo công ty)', 'Thanh toán 50% khi ký hợp đồng, 50% khi bàn giao…'),
                ],
            },
        ],
    },

    department: {
        chip: 'chip-dep',
        chipText: 'Theo phòng ban – bộ phận',
        groups: [
            {
                id: 'hoahong',
                name: 'Quy chế hoa hồng / năng suất',
                sub: 'Thưởng năng suất tháng, quý',
                icon: 'gift',
                type: 'grid',
                deptOnly: false,
                hint: 'Mỗi dòng là 1 quy chế hoa hồng. Tab dạng bảng <b>hẹn theo từng dòng</b>: cột <b>Hiệu lực từ</b> đặt ngày tương lai → dòng đó tự áp dụng đúng ngày (trạng thái “Chờ áp dụng”).',
                rows: [
                    ['Hàng hóa', 'Giá bán lẻ', '0 – 5%', '3', '2', '40 / 30 / 30', '50 / 30 / 20', 'ok', '2026-01-01'],
                    ['Dịch vụ', 'Giá dịch vụ', '5 – 10%', '4', '3', '40 / 30 / 30', '50 / 30 / 20', 'ok', '2026-01-01'],
                    ['Hàng hóa', 'Giá đại lý', '> 10%', '5', '4', '30 / 40 / 30', '40 / 40 / 20', 'wait', '2026-10-01'],
                ],
            },
            {
                id: 'themquy',
                name: 'Thưởng thêm quý (lũy tiến)',
                sub: 'Bậc thang + tỉ lệ chia lũy tiến',
                icon: 'cut',
                type: 'ladder',
                deptOnly: false,
                hint: 'Bậc thang theo Tổng hoa hồng của phòng — mỗi khoảng giá trị hưởng một mức %. Tab này <b>hẹn theo cả phiên bản</b>: 1 ngày hiệu lực cho toàn bộ bảng bậc thang + tỉ lệ chia.',
                eff: '2026-01-01',
                pending: [
                    {
                        date: '2026-10-01',
                        who: 'DNS Admin',
                        note: 'Điều chỉnh bậc thang Q4/2026',
                        changes: [
                            { label: 'Mức bậc 3 (>100tr)', old: '12%', new: '15%', unit: '' },
                            { label: 'Tỉ lệ chia TP/TBP/NV', old: '50/30/20', new: '45/35/20', unit: '' },
                        ],
                    },
                ],
                ladder: [
                    ['Lớn hơn', '0', 'Nhỏ hơn bằng', '50.000.000', '5'],
                    ['Lớn hơn', '50.000.000', 'Nhỏ hơn bằng', '100.000.000', '8'],
                    ['Lớn hơn', '100.000.000', '—', '', '12'],
                ],
                progressive: { tp: 50, tbp: 30, nv: 20 },
            },
            {
                id: 'khac',
                name: 'Quy chế khác',
                sub: 'Quỹ rủi ro · % LN · Hạn mức duyệt',
                icon: 'check',
                type: 'form',
                deptOnly: true,
                eff: '2026-01-01',
                pending: [
                    {
                        date: '2026-10-01',
                        who: 'DNS Admin',
                        note: 'Nâng quỹ thưởng cuối năm',
                        changes: [{ label: 'Quỹ rủi ro / Quỹ thưởng cuối năm', old: '5', new: '6', unit: '%' }],
                    },
                ],
                fields: [
                    num('Quỹ rủi ro / Quỹ thưởng cuối năm', '%', 5),
                    num('% Hưởng lợi nhuận', '%', 10),
                    num('Giá trị HĐ tối đa Trưởng phòng được duyệt', 'đồng', 2000000000),
                ],
            },
        ],
    },
}

/* ---------- lịch sử thay đổi (mock) ---------- */
export const HIST = {
    company: [
        ['08/09/2026 09:12', 'DNS Admin', 'Hẹn phiên bản mới tab Báo giá – HĐ (2 thay đổi)', 'ETEK Group', 'Hiệu lực 01/10/2026', true],
        ['28/05/2026 10:30', 'DNS Admin', 'Tab Kỹ thuật: Đơn giá công 320.000 → 350.000', 'ETEK Group', 'Áp dụng ngay', false],
        ['15/06/2026 14:15', 'DNS Admin', 'Tab Công nợ: Lãi suất 1.2% → 1.5% (đã áp dụng)', 'ETEK Group', '', false],
    ],
    department: [
        ['28/05/2026 10:30', 'DNS Admin', 'Thêm quy chế hoa hồng (Hàng hóa · Giá bán lẻ · NS tháng 3%)', 'Phòng Kinh doanh', '', false],
        ['02/09/2026 11:20', 'DNS Admin', 'Hẹn dòng hoa hồng (Hàng hóa · Giá đại lý) hiệu lực 01/10/2026', 'Phòng Kinh doanh', 'Chờ áp dụng', true],
        ['20/06/2026 09:45', 'DNS Admin', 'Hẹn phiên bản bậc thang Q4 hiệu lực 01/10/2026', 'Phòng Kinh doanh', 'Chờ áp dụng', true],
    ],
}

/* ---------- danh sách phòng ban / bộ phận (mock chọn phạm vi) ---------- */
export const SCOPE_UNITS = [
    { id: 'kd', name: 'Phòng Kinh doanh', type: 'dept' },
    { id: 'kdmb', name: 'Phòng Kinh doanh Miền Bắc', type: 'dept' },
    { id: 'dv', name: 'Phòng Dịch vụ', type: 'dept' },
    { id: 'muahang', name: 'Bộ phận mua hàng ngoài', type: 'part' },
    { id: 'kythuat', name: 'Bộ phận Kỹ thuật', type: 'part' },
]

/* ---------- công ty đang cấu hình (mock — thật sẽ lấy theo tài khoản đăng nhập) ---------- */
export const CURRENT_COMPANY = 'CÔNG TY CỔ PHẦN ĐẦU TƯ TẬP ĐOÀN ETEK'
