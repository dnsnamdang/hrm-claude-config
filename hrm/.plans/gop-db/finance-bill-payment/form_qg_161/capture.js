// Chụp ảnh HDSD/SRS màn Phiếu chi tiền (STT 161) trên DEV — trình duyệt headless riêng.
// Chạy: C:/Users/Legion/AppData/Local/nvm/v24.6.0/node.exe capture.js [bước...]
// AN TOÀN: chặn MỌI request ghi (POST/PUT/PATCH/DELETE) tới API phiếu chi — không bấm xác nhận thật.
// Tài khoản dev không có phiếu nháp/phiếu chờ đúng cấp nên cờ is_can_* được BẬT TẠM trên trình duyệt
// (sửa response GET, không ghi dữ liệu) để chụp nút Sửa / Xóa / Duyệt / Hủy — giống màn 27.
const fs = require('fs')
const path = require('path')
const { openDev, DEV } = require('../../phieu-theo-form-quoc-gia/pw_dev.js')

const HERE = __dirname
const SHOTS = path.join(HERE, 'hdsd_shots')
const ICONS = path.join(SHOTS, 'icons')
fs.mkdirSync(ICONS, { recursive: true })

const ID_A = 1629 // Chi trả nhà cung cấp — Chờ chi tiền (bật tạm Sửa/Xóa/Duyệt/Hủy)
const ID_B = 1610 // Chi thu nhập cho nhân viên — Đã duyệt (bật tạm Duyệt để xem cửa sổ duyệt nhánh nhân viên)
const ID_CANCEL = 1147 // phiếu Hủy (dải băng Lý do hủy)
const ID_HIST = 1625 // phiếu có lịch sử
const FORCE = {
    [ID_A]: { is_can_edit: true, is_can_delete: true, is_can_approve: true, is_can_cancel: true },
    [ID_B]: { is_can_approve: true, is_can_cancel: true },
    [ID_CANCEL]: { cancel_reason: 'Sai thông tin tài khoản nhận tiền', cancel_note: 'Lập lại phiếu chi mới sau khi kiểm tra' },
}

function patch(o) {
    if (Array.isArray(o)) return o.forEach(patch)
    if (o && typeof o === 'object') {
        if (o.id && FORCE[o.id] && 'code' in o) Object.assign(o, FORCE[o.id])
        Object.values(o).forEach(patch)
    }
}

async function login(page, ctx) {
    await page.goto(DEV + '/finance/bill-payments').catch(() => {})
    await page.waitForTimeout(2500)
    if (page.url().includes('/login')) {
        await page.waitForSelector('input[type=password]')
        await page.fill('#emailaddress, input[type=email], input[name=email]', 'namdangit@gmail.com')
        await page.fill('input[type=password]', '2025Dns@2')
        await page.keyboard.press('Enter')
        await page.waitForURL((u) => !String(u).includes('/login'), { timeout: 60000 })
        await page.waitForLoadState('networkidle').catch(() => {})
        await ctx.storageState({ path: path.join(HERE, '.dev_state.json') })
    }
}

async function settle(page, ms = 2500) {
    await page.waitForLoadState('networkidle').catch(() => {})
    await page.waitForTimeout(ms)
    await page.mouse.move(5, 5)
    await page.mouse.move(760, 45)
    await page.waitForTimeout(400)
}
const shot = (page, name, opt = {}) => page.screenshot({ path: path.join(SHOTS, name + '.png'), ...opt })
async function icon(loc, name) {
    try {
        await loc.first().scrollIntoViewIfNeeded()
        await loc.first().screenshot({ path: path.join(ICONS, name + '.png') })
    } catch (e) {
        console.log('ICON FAIL', name, e.message.split('\n')[0])
    }
}
async function modalShot(page, name) {
    const m = page.locator('.modal.show .modal-content').last()
    await m.waitFor({ state: 'visible', timeout: 15000 })
    await page.waitForTimeout(1200)
    await page.mouse.move(5, 5)
    await shot(page, name)
    return m
}
async function goto(page, url, ms) {
    await page.goto(DEV + url, { timeout: 60000 })
    await page.waitForFunction(() => /Thông tin chung|Bộ lọc danh sách/.test(document.body.innerText), null, { timeout: 90000 })
    await settle(page, ms)
}
async function pickSelect2(page, label, text) {
    const grp = page.locator('div.mb-2', { has: page.locator('label', { hasText: label }) }).first()
    await grp.locator('.select2-selection').first().click()
    await page.waitForTimeout(800)
    const opt = page.locator('.select2-results__option', { hasText: text }).first()
    await opt.click()
    await page.waitForTimeout(1500)
}

const STEPS = {
    async list(page) {
        await goto(page, '/finance/bill-payments', 3000)
        await shot(page, '01_list')
        await icon(page.locator('.v2-filter-quick input, input[placeholder^="Tìm theo mã phiếu chi"]'), 'o_timnhanh')
        await icon(page.getByRole('button', { name: 'Tìm kiếm', exact: true }), 'btn_timkiem')
        await icon(page.getByRole('button', { name: 'Làm mới' }), 'btn_lammoi')
        await icon(page.getByRole('button', { name: /Tìm kiếm nâng cao/ }), 'btn_timkiemnangcao')
        await icon(page.getByRole('button', { name: /Cài đặt bộ lọc/ }), 'btn_caidatboloc')
        await icon(page.getByRole('button', { name: /Tạo mới/ }), 'btn_taomoi')
        await icon(page.locator('button[title="Cấu hình cột hiển thị"]'), 'btn_cauhinhcot')
        const row = page.locator('tbody tr').first()
        await icon(row.locator('span[title="In"] button'), 'btn_in_row')
        await icon(row.locator('span[title="Xuất Excel"] button'), 'btn_xuatexcel_row')
        await icon(row.locator('span[title="Lịch sử"] button'), 'btn_lichsu_row')
        // menu
        await page.mouse.move(40, 400)
        await page.waitForTimeout(800)
        await icon(page.locator('.side-nav-link, a, li', { hasText: /^Quản lý tiền$/ }).filter({ hasText: 'Quản lý tiền' }), 'menu_nhom')
        await page.getByText('Quản lý tiền', { exact: true }).first().click()
        await page.waitForTimeout(1200)
        await icon(page.getByText('Thanh toán tiền mặt', { exact: true }).first().locator('xpath=..'), 'menu_thanhtoan')
        await icon(page.getByText('Phiếu chi', { exact: true }).first().locator('xpath=..'), 'menu_muc')
        await shot(page, '00_menu')
    },
    async filter(page) {
        await goto(page, '/finance/bill-payments', 3000)
        await page.getByRole('button', { name: /Tìm kiếm nâng cao/ }).click({ force: true })
        await settle(page, 1500)
        await shot(page, '02_filter')
        const lb = async (t, n) =>
            icon(page.locator('.ff, .filter-field, .smart-filter-field, div', { has: page.locator(`label:text-is("${t}")`) }).last(), n)
        await lb('Mã phiếu đề nghị chi', 'o_madenghi')
        await lb('Loại chi', 'o_loaichi')
        await lb('Trạng thái', 'o_trangthai')
        await lb('Người lập', 'o_nguoilap')
        await lb('Người đề nghị', 'o_nguoidenghi')
        await lb('Phòng ban', 'o_phongban')
        await lb('Khách hàng / Nhà cung cấp', 'o_doitac')
        await lb('Số tiền', 'o_sotien')
        await lb('Ngày lập', 'o_ngaylap')
        // cài đặt bộ lọc
        await page.getByRole('button', { name: /Cài đặt bộ lọc/ }).click({ force: true })
        const m = await modalShot(page, '26_filtercfg')
        await icon(m.locator('button').filter({ hasText: /^\s*Lưu\s*$/ }), 'btn_luu')
        await icon(m.getByRole('button', { name: /Khôi phục/ }), 'btn_khoiphuc')
        await icon(m.getByRole('button', { name: /Đóng/ }), 'btn_dong_filtercfg')
        await m.getByRole('button', { name: /Đóng/ }).click()
        await page.waitForTimeout(800)
        await page.locator('button[title="Cấu hình cột hiển thị"]').click({ force: true })
        const c = await modalShot(page, '25_colcfg')
        await icon(c.getByRole('button', { name: /Chọn tất cả/ }), 'btn_chontatca')
        await icon(c.getByRole('button', { name: /Bỏ chọn hết/ }), 'btn_bochonhet')
        await icon(c.locator('button').filter({ hasText: /^\s*Lưu\s*$/ }), 'btn_luu_col')
        await icon(c.getByRole('button', { name: /Đóng/ }), 'btn_dong_col')
    },
    async filterIcons(page) {
        await goto(page, '/finance/bill-payments', 3000)
        const open = await page.locator('input[placeholder*="Mã phiếu đề nghị"], label:text-is("Loại chi")').count()
        if (!open) await page.locator('button').filter({ hasText: /Tìm kiếm nâng cao/ }).first().click({ force: true })
        await settle(page, 1500)
        const L = [['Mã phiếu đề nghị chi', 'o_madenghi'], ['Loại chi', 'o_loaichi'], ['Trạng thái', 'o_trangthai'],
            ['Người lập', 'o_nguoilap'], ['Người đề nghị', 'o_nguoidenghi'], ['Phòng ban', 'o_phongban'],
            ['Khách hàng / Nhà cung cấp', 'o_doitac'], ['Số tiền', 'o_sotien'], ['Ngày lập', 'o_ngaylap']]
        for (const [t, n] of L) {
            const r = await page.evaluate((t) => {
                const lab = [...document.querySelectorAll('label, span, div')].find(
                    (e) => e.children.length === 0 && e.innerText && e.innerText.trim() === t && e.getBoundingClientRect().top > 80)
                if (!lab) return null
                let p = lab.parentElement
                while (p && !(p.querySelector('input, select, .select2') && p.getBoundingClientRect().width > 150)) p = p.parentElement
                const b = p.getBoundingClientRect()
                return { x: b.x, y: b.y, width: b.width, height: b.height }
            }, t)
            if (!r) { console.log('ICON FAIL', n); continue }
            await page.screenshot({ path: path.join(ICONS, n + '.png'), clip: { x: r.x - 2, y: r.y - 2, width: r.width + 4, height: r.height + 4 } })
        }
        await icon(page.locator('button').filter({ hasText: /^\s*Tìm kiếm\s*$/ }), 'btn_timkiem')
    },
    async more(page) {
        await goto(page, '/finance/bill-payments', 3000)
        const row = page.locator('tbody tr', { hasText: 'TPV.PC1026.00006' }).first()
        const b = row.locator('button[title="Hành động khác"]').first()
        await icon(b, 'btn_bacham_row')
        await b.click()
        await page.waitForTimeout(1000)
        await page.mouse.move(5, 5)
        await shot(page, '01c_more')
        for (const [t, n] of [['Duyệt', 'item_duyet'], ['Lịch sử', 'item_lichsu'], ['In', 'item_in'], ['Xuất Excel', 'item_xuatexcel']]) {
            const it = page.locator('a, button, li, div').filter({ hasText: new RegExp('^\\s*' + t + '\\s*$') })
                .filter({ has: page.locator('i') }).last()
            await icon(it, n)
        }
    },
    async sophieu(page) {
        await goto(page, '/finance/bill-payments/create', 3000)
        await pickSelect2(page, 'Loại chi', 'Chi trả nhà cung cấp')
        await page.mouse.move(760, 45)
        await icon(page.locator('input[placeholder="Nhấn vào đây để chọn phiếu đề nghị chi"]'), 'o_sophieudenghi')
        await icon(page.locator('button').filter({ hasText: /^\s*Lưu nháp\s*$/ }), 'btn_luunhap')
    },
    async create(page) {
        await goto(page, '/finance/bill-payments/create', 3000)
        await shot(page, '10_create')
        await icon(page.locator('button').filter({ hasText: /^\s*Lưu nháp\s*$/ }), 'btn_luunhap')
        await icon(page.getByRole('button', { name: /Lưu và gửi duyệt/ }), 'btn_luuguiduyet')
        await icon(page.getByRole('button', { name: /Lưu và tiếp tục/ }), 'btn_luutieptuc')
        await icon(page.getByRole('button', { name: /Quay lại/ }), 'btn_quaylai')
        await pickSelect2(page, 'Loại chi', 'Chi trả nhà cung cấp')
        await shot(page, '10b_loaichi')
        await page.locator('input[placeholder="Nhấn vào đây để chọn phiếu đề nghị chi"]').click()
        const m = await modalShot(page, '11_request')
        await icon(page.locator('input[placeholder="Nhấn vào đây để chọn phiếu đề nghị chi"]'), 'o_sophieudenghi')
        await icon(m.getByRole('button', { name: /Đóng/ }), 'btn_dong')
        const r = m.locator('tbody tr').first()
        await r.click()
        await settle(page, 3000)
        await shot(page, '12_create_request', { fullPage: true })
        // hộp xác nhận lưu và gửi duyệt (chỉ mở rồi Hủy)
        await page.getByRole('button', { name: /Lưu và gửi duyệt/ }).click()
        const cf = await modalShot(page, '13_confirm_submit')
        const btns = cf.locator('button')
        const n = await btns.count()
        for (let i = 0; i < n; i++) console.log('confirm-btn', i, (await btns.nth(i).innerText()).trim())
        await icon(cf.getByRole('button', { name: /Xác nhận|Đồng ý/ }), 'btn_confirm_xacnhan')
        await icon(cf.getByRole('button', { name: /Hủy|Đóng/ }), 'btn_huy_confirm')
        await cf.getByRole('button', { name: /Hủy|Đóng/ }).first().click()
    },
    async employee(page) {
        await goto(page, '/finance/bill-payments/create', 3000)
        await pickSelect2(page, 'Loại chi', 'Chi thu nhập cho nhân viên')
        await shot(page, '14_employee_form')
        const grp = page.locator('div.mb-2', { has: page.locator('label', { hasText: 'Phòng ban chi' }) }).first()
        await icon(grp, 'o_phongbanchi')
        await grp.locator('.select2-selection').first().click()
        await page.waitForTimeout(800)
        await page.keyboard.type(process.env.DEPT || 'Ô TÔ 1')
        await page.waitForTimeout(1200)
        await page.locator('.select2-results__option').first().click()
        await settle(page, 8000)
        await shot(page, '15_employee_table', { fullPage: true })
    },
    async edit(page) {
        await goto(page, `/finance/bill-payments/${ID_A}/edit`, 4000)
        await shot(page, '16_edit')
    },
    async listForced(page) {
        await goto(page, '/finance/bill-payments', 3000)
        const row = page.locator('tbody tr', { hasText: 'TPV.PC1026.00006' }).first()
        await page.evaluate(() => { document.querySelectorAll('*').forEach((w) => { if (w.scrollWidth > w.clientWidth + 50 && getComputedStyle(w).overflowX !== 'visible') w.scrollLeft = 99999 }) })
        await page.waitForTimeout(800)
        await shot(page, '01b_list_actions')
        console.log('row actions', await row.locator('td:last-child').innerHTML())
        await icon(row.locator('span[title="Sửa"] a, span[title="Sửa"] button'), 'btn_sua_row')
        await icon(row.locator('span[title="Xóa"] button'), 'btn_xoa_row')
        await icon(row.locator('span[title="Duyệt"] a, span[title="Duyệt"] button'), 'btn_duyet_row')
        await icon(row.locator('.dropdown-toggle, button[title="Thêm"], .v2-row-actions__more button'), 'btn_bacham_row')
        // menu ba chấm
        const more = row.locator('.dropdown-toggle, .v2-row-actions__more button').first()
        if (await more.count()) {
            await more.click()
            await page.waitForTimeout(800)
            await icon(page.locator('.dropdown-menu.show .dropdown-item', { hasText: 'In' }), 'item_in')
            await icon(page.locator('.dropdown-menu.show .dropdown-item', { hasText: 'Lịch sử' }), 'item_lichsu')
            await icon(page.locator('.dropdown-menu.show .dropdown-item', { hasText: 'Xuất Excel' }), 'item_xuatexcel')
            await page.keyboard.press('Escape')
            await page.waitForTimeout(500)
        }
        await row.locator('span[title="Xóa"] button').first().click()
        const m = await modalShot(page, '20_delete')
        await icon(m.locator('button').filter({ hasText: /^\s*Xóa\s*$/ }), 'btn_confirm_xoa')
        await m.locator('button').filter({ hasText: /^\s*Hủy\s*$/ }).click()
    },
    async detail(page) {
        await goto(page, `/finance/bill-payments/${ID_A}`, 4000)
        await shot(page, '17_detail')
        await icon(page.locator('button').filter({ hasText: /^\s*Sửa\s*$/ }), 'btn_sua')
        await icon(page.getByRole('button', { name: /Duyệt phiếu chi/ }), 'btn_duyetphieuchi')
        await icon(page.getByRole('button', { name: /Hủy phiếu chi/ }), 'btn_huyphieuchi')
        await icon(page.locator('button').filter({ hasText: /^\s*In\s*$/ }), 'btn_in')
        await icon(page.getByRole('button', { name: /Xuất Excel/ }), 'btn_xuatexcel')
        await icon(page.locator('button').filter({ hasText: /^\s*Xóa\s*$/ }), 'btn_xoa')
        // duyệt nhánh A
        await page.getByRole('button', { name: /Duyệt phiếu chi/ }).click()
        const m = await modalShot(page, '18_approve')
        await icon(m.locator('button').filter({ hasText: /^\s*Duyệt\s*$/ }), 'btn_duyet')
        await icon(m.getByRole('button', { name: /Đóng/ }), 'btn_dong_approve')
        await m.locator('button').filter({ hasText: /^\s*Duyệt\s*$/ }).click()
        await page.waitForTimeout(1500)
        const cf = await modalShot(page, '18b_approve_confirm')
        const bs = cf.locator('button')
        for (let i = 0; i < (await bs.count()); i++) console.log('approve-confirm-btn', (await bs.nth(i).innerText()).trim())
        await icon(cf.locator('button').filter({ hasText: /^\s*Duyệt\s*$/ }), 'btn_confirm_duyet')
        await cf.getByRole('button', { name: /Hủy|Đóng/ }).first().click()
        await page.waitForTimeout(800)
        await page.keyboard.press('Escape')
        await page.waitForTimeout(800)
        // hủy
        await goto(page, `/finance/bill-payments/${ID_A}`, 4000)
        await page.getByRole('button', { name: /Hủy phiếu chi/ }).click()
        const c = await modalShot(page, '21_cancel')
        await icon(c.getByRole('button', { name: /Xác nhận/ }), 'btn_confirm_huy')
        await icon(c.getByRole('button', { name: /Đóng/ }), 'btn_dong_cancel')
        await c.getByRole('button', { name: /Xác nhận/ }).click()
        await page.waitForTimeout(800)
        await page.mouse.move(5, 5)
        await shot(page, '21b_cancel_error')
        await c.getByRole('button', { name: /Đóng/ }).click()
    },
    async approveB(page) {
        await goto(page, `/finance/bill-payments/${ID_B}`, 4000)
        await page.getByRole('button', { name: /Duyệt phiếu chi/ }).click()
        await modalShot(page, '19_approve_employee')
    },
    async canceled(page) {
        await goto(page, `/finance/bill-payments/${ID_CANCEL}`, 4000)
        await shot(page, '22_detail_cancel')
    },
    async print(page) {
        await goto(page, '/finance/bill-payments', 3000)
        await page.locator('tbody tr').first().locator('span[title="In"] button').click()
        await page.waitForTimeout(6000)
        const m = page.locator('.modal.show .modal-content').last()
        await page.mouse.move(5, 5)
        await shot(page, '23_print')
        await icon(m.locator('button').filter({ hasText: /^\s*In\s*$/ }), 'btn_in_preview')
        await icon(m.getByRole('button', { name: /Đóng/ }), 'btn_dong_print')
    },
    async history(page) {
        await goto(page, '/finance/bill-payments', 3000)
        const row = page.locator('tbody tr', { hasText: 'TPE.PC1026.00051' }).first()
        await row.locator('span[title="Lịch sử"] button').click()
        const m = page.locator('.modal.show .modal-content').last()
        await m.waitFor({ state: 'visible' })
        await page.waitForFunction(() => !document.querySelector('.modal.show .spinner-border, .modal.show .v2-loading, .modal.show [class*=spin]'), null, { timeout: 60000 }).catch(() => {})
        await page.waitForTimeout(3000)
        await page.mouse.move(5, 5)
        await shot(page, '24_history')
        await icon(m.getByRole('button', { name: /Bộ lọc/ }), 'btn_boloc_ls')
        await icon(m.getByRole('button', { name: /Đóng/ }), 'btn_dong_ls')
        await goto(page, `/finance/bill-payments/${ID_HIST}`, 4000)
        const b = page.getByRole('button', { name: /Xem lịch sử/ })
        await icon(b, 'btn_xemlichsu')
        await b.click()
        await settle(page, 2500)
        await page.getByText('Lịch sử thay đổi').last().scrollIntoViewIfNeeded().catch(() => {})
        await page.waitForTimeout(800)
        await shot(page, '24b_history_detail')
    },
}

;(async () => {
    const want = process.argv.slice(2)
    const { browser, ctx, page } = await openDev(HERE)
    await page.route('**/api/**', async (route) => {
        const req = route.request()
        const u = req.url()
        if (req.method() !== 'GET' && /bill-payment|bill_payment/.test(u)) {
            console.log('CHẶN', req.method(), u)
            return route.abort()
        }
        if (req.method() === 'GET' && /finance\/bill-payments(\?|\/\d+(\?|$))/.test(u)) {
            const resp = await route.fetch()
            let body = await resp.text()
            try {
                const j = JSON.parse(body)
                patch(j)
                body = JSON.stringify(j)
            } catch (e) {}
            return route.fulfill({ response: resp, body })
        }
        return route.continue()
    })
    page.setDefaultTimeout(8000)
    await login(page, ctx)
    for (const k of Object.keys(STEPS)) {
        if (want.length && !want.includes(k)) continue
        try {
            console.log('==', k)
            await STEPS[k](page)
        } catch (e) {
            console.log('STEP FAIL', k, e.message.split('\n')[0])
        }
    }
    await browser.close()
})().catch((e) => {
    console.error(e)
    process.exit(1)
})
