/**
 * Video hướng dẫn phần phân quyền — Phần mềm quản trị ERP TPE (bản rbac, cổng 3011). CHỈ XEM, không bấm Lưu.
 * Đồng bộ theo TỪNG BƯỚC: mỗi bước = 1 lời thoại + thao tác. Thao tác chạy lúc bắt đầu bước; bước sau chỉ bắt đầu khi lời
 * của bước trước đã đọc xong ⇒ popup/màn không bị đóng trước khi nói xong (đóng là một bước riêng, có lời).
 * Lời đọc: giọng neural Hoài My (edge-tts), đọc từng câu + cache. Dựng mp4: build2.py.
 */
const { chromium } = require('playwright')
const fs = require('fs')
const path = require('path')
const crypto = require('crypto')
const { execFileSync } = require('child_process')

const OUT = __dirname
const BASE = 'http://127.0.0.1:3011'
const TOKEN = fs.readFileSync(path.join(OUT, '..', 'jwt13.txt'), 'utf8').trim()
const W = 1600
const H = 900
const GAP = 0.35 // nghỉ giữa 2 bước (giây)

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

// ---------- hiệu ứng trên trang ----------
const OVERLAY_INIT = () => {
    const ensure = () => {
        if (document.getElementById('__cur')) return
        const cur = document.createElement('div')
        cur.id = '__cur'
        cur.style.cssText = 'position:fixed;z-index:2147483647;width:22px;height:22px;border-radius:50%;background:rgba(239,68,68,.35);border:2px solid #ef4444;pointer-events:none;left:-50px;top:-50px;transform:translate(-50%,-50%);transition:left .25s ease,top .25s ease'
        document.body.appendChild(cur)
        document.addEventListener('mousemove', (e) => {
            cur.style.left = e.clientX + 'px'
            cur.style.top = e.clientY + 'px'
        }, true)
        document.addEventListener('mousedown', () => {
            cur.style.background = 'rgba(239,68,68,.7)'
            setTimeout(() => (cur.style.background = 'rgba(239,68,68,.35)'), 250)
        }, true)
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ensure)
    else ensure()
}

async function caption(page, chapter, text) {
    await page.evaluate(([chapter, text]) => {
        let box = document.getElementById('__cap')
        if (!box) {
            box = document.createElement('div')
            box.id = '__cap'
            box.style.cssText = 'position:fixed;z-index:2147483646;left:50%;bottom:72px;transform:translateX(-50%);max-width:1150px;background:rgba(15,23,42,.88);color:#fff;font:500 19px/1.45 Roboto,Arial,sans-serif;padding:12px 22px;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.25);pointer-events:none;text-align:center'
            document.body.appendChild(box)
            const ch = document.createElement('div')
            ch.id = '__chap'
            ch.style.cssText = 'position:fixed;z-index:2147483646;right:24px;top:72px;background:#16a34a;color:#fff;font:700 14px Roboto,Arial,sans-serif;padding:6px 14px;border-radius:999px;pointer-events:none;box-shadow:0 4px 12px rgba(0,0,0,.2)'
            document.body.appendChild(ch)
        }
        document.getElementById('__chap').textContent = chapter
        box.textContent = text
    }, [chapter, text])
}

async function mark(locator, ms = 2200) {
    try {
        await locator.first().evaluate((el, ms) => {
            const r = el.getBoundingClientRect()
            const m = document.createElement('div')
            m.style.cssText = `position:fixed;z-index:2147483645;left:${r.left - 6}px;top:${r.top - 6}px;width:${r.width + 12}px;height:${r.height + 12}px;border:3px solid #f59e0b;border-radius:8px;box-shadow:0 0 0 4px rgba(245,158,11,.25);pointer-events:none`
            document.body.appendChild(m)
            setTimeout(() => m.remove(), ms)
        }, ms)
    } catch (e) {}
}

async function hover(page, locator) {
    try {
        await locator.first().scrollIntoViewIfNeeded({ timeout: 5000 })
        const box = await locator.first().boundingBox()
        if (box) await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 12 })
    } catch (e) {}
}

async function click(page, locator) {
    await hover(page, locator)
    await sleep(250)
    await locator.first().click()
}

async function pickSelect2(page, container, text, search) {
    await click(page, container.locator('.select2-selection'))
    const s = page.locator('.select2-container--open .select2-search__field')
    if (search && (await s.count())) await s.first().type(search, { delay: 40 })
    await sleep(500)
    const opt = page.locator('.select2-container--open .select2-results__option', { hasText: text }).first()
    await hover(page, opt)
    await sleep(300)
    await opt.click()
    await page.keyboard.press('Escape').catch(() => {})
}

const topModal = (page) => page.locator('.modal.show').last()

/** Đóng popup trên cùng bằng nút Đóng / Hủy (có chuột), không có thì Escape. */
async function closeModal(page) {
    const m = topModal(page)
    const btn = m.locator('button', { hasText: /^\s*(Đóng|Hủy|Huỷ)\s*$/ }).last()
    if (await btn.count()) {
        await click(page, btn)
    } else {
        await page.keyboard.press('Escape')
    }
    await sleep(600)
}

/** Menu trái phân hệ Quản trị → nhóm "Người dùng & phân quyền" (mở bảng con). */
async function openUsersGroup(page) {
    await page.mouse.move(300, 500, { steps: 6 })
    await sleep(300)
    await page.mouse.move(30, 254, { steps: 14 })
    await sleep(1200)
    await click(page, page.getByText(/^Người dùng & phân/).first())
    await sleep(1000)
}
const menuLink = (page, item) => page.locator('a', { hasText: new RegExp(`^${item}\\s*☆?$`) }).first()

const roleRow = (page, name) => page.locator('table tbody tr').filter({ has: page.getByRole('button', { name, exact: true }) }).first()
const SEARCH_PQ = 'input[placeholder="Tìm quyền theo tên hoặc mã..."]'
const pqCard = (page, name) => page.locator('.pq-sub', { has: page.locator('.pq-sub__name', { hasText: new RegExp(`^${name}$`) }) })

// ---------- kịch bản: [chương, [{say, cap?, act?}]] ----------
const C0 = 'Giới thiệu'
const C1 = '1. Danh sách vai trò'
const C2 = '2. Phân quyền cho vai trò'
const C3 = '3. Vai trò nhân viên'
const C9 = 'Kết thúc'

const steps = [
    // ===== Giới thiệu + vào menu =====
    { ch: C0, cap: 'Hướng dẫn sử dụng Phần mềm quản trị ERP TPE', say: 'Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.' },
    { ch: C0, cap: 'Phân quyền: vai trò · phân quyền cho vai trò · vai trò nhân viên', say: 'Video này hướng dẫn các chức năng phân quyền, gồm quản lý vai trò, phân quyền cho vai trò, và cấp vai trò cho nhân viên.' },
    { ch: C0, cap: 'Từ trang chủ, bấm "Quản trị" ở vòng tròn giữa', say: 'Để bắt đầu, từ trang chủ, bạn bấm vào mục Quản trị ở vòng tròn giữa màn hình.',
        act: async (p) => { const q = p.getByText(/^\s*Quản trị\s*$/i).first(); await hover(p, q); await mark(q, 3500) } },
    { ch: C0, cap: 'Trang tổng quan phân hệ Quản trị hệ thống', say: 'Đây là trang tổng quan của phân hệ Quản trị hệ thống.',
        act: async (p) => { await p.getByText(/^\s*Quản trị\s*$/i).first().click(); await p.getByText('Phân hệ Quản trị hệ thống').waitFor({ timeout: 60000 }) } },
    { ch: C0, cap: 'Menu trái › Người dùng & phân quyền', say: 'Bạn rê chuột vào thanh menu bên trái và chọn nhóm Người dùng và phân quyền. Nhóm này có ba chức năng: Quản lý tài khoản, Vai trò nhân viên, và Vai trò.',
        act: async (p) => { await openUsersGroup(p); await mark(p.locator('a', { hasText: 'Quản lý tài khoản' }).first().locator('xpath=ancestor::*[3]'), 4000) } },
    { ch: C0, cap: 'Menu trái › Người dùng & phân quyền › Vai trò', say: 'Mình bấm vào Vai trò.',
        act: async (p) => { const l = menuLink(p, 'Vai trò'); await hover(p, l); await mark(l, 1500); await sleep(900); await l.click(); await p.locator('table tbody tr').first().waitFor({ timeout: 120000 }); await sleep(800) } },

    // ===== 1. Danh sách vai trò =====
    { ch: C1, cap: 'Màn Vai trò: vai trò của công ty đang làm việc', say: 'Màn Vai trò liệt kê toàn bộ vai trò của công ty bạn đang làm việc.',
        act: async (p) => { await mark(p.locator('table').first(), 3000) } },
    { ch: C1, say: 'Mỗi dòng cho biết số quyền đang có, số người đang giữ, trạng thái, người cập nhật, và thời điểm cập nhật gần nhất.',
        act: async (p) => { for (const t of ['Quyền đang có', 'Số người giữ', 'Trạng thái', 'Người cập nhật', 'Cập nhật lúc']) { const th = p.locator('table thead th', { hasText: t }); await hover(p, th); await mark(th, 1300); await sleep(1300) } } },
    { ch: C1, cap: 'Tìm nhanh theo tên / mô tả · Tìm kiếm · Làm mới', say: 'Ô tìm nhanh cho phép tìm theo tên hoặc mô tả vai trò, gõ xong bấm Tìm kiếm. Nút Làm mới để xoá điều kiện tìm.',
        act: async (p) => { const c = p.locator('.smart-filter-card'); await mark(c.locator('input').first(), 2200); await sleep(2400); await mark(c.locator('button', { hasText: /^\s*Tìm kiếm\s*$/ }), 1600); await sleep(1700); await mark(c.locator('button', { hasText: 'Làm mới' }), 1600) } },
    { ch: C1, cap: 'Tìm kiếm nâng cao: Trạng thái · Người sửa gần nhất · Quyền · Người đang giữ', say: 'Bấm Tìm kiếm nâng cao để mở thêm bộ lọc theo trạng thái, người sửa gần nhất, quyền, và người đang giữ.',
        act: async (p) => { await click(p, p.locator('button', { hasText: 'Tìm kiếm nâng cao' })); await sleep(1200); const c = p.locator('.smart-filter-card'); for (const n of [0, 1, 2, 3]) { await mark(c.locator('.select2-container').nth(n), 1300); await sleep(1100) } } },
    { ch: C1, say: 'Ví dụ, chọn quyền Xem danh sách đơn nghỉ phép, danh sách chỉ còn những vai trò đang có quyền này.',
        act: async (p) => { const c = p.locator('.smart-filter-card'); await pickSelect2(p, c.locator('.select2-container').nth(2), 'Xem danh sách đơn nghỉ phép', 'đơn nghỉ phép'); await sleep(1800); await mark(p.locator('table tbody'), 2500) } },
    { ch: C1, say: 'Bấm Làm mới để bỏ bộ lọc.',
        act: async (p) => { await click(p, p.locator('.smart-filter-card button', { hasText: 'Làm mới' })) } },
    { ch: C1, cap: 'Cài đặt bộ lọc: chọn ô lọc hiển thị, kéo thả sắp xếp', say: 'Nút Cài đặt bộ lọc cho phép chọn những ô lọc nào được hiển thị, và kéo thả để sắp xếp thứ tự. Cài đặt được lưu riêng cho từng màn hình.',
        act: async (p) => { await click(p, p.locator('button', { hasText: 'Cài đặt bộ lọc' })); await sleep(1200); await mark(topModal(p).locator('.modal-body'), 3500) } },
    { ch: C1, say: 'Bấm Lưu để áp dụng, hoặc Khôi phục mặc định để trở về như ban đầu.',
        act: async (p) => { const m = topModal(p); await mark(m.locator('button', { hasText: 'Lưu' }), 1800); await sleep(1900); await mark(m.locator('button', { hasText: 'Khôi phục mặc định' }), 1800) } },
    { ch: C1, say: 'Mình bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Cấu hình cột hiển thị: chọn cột, kéo đổi thứ tự', say: 'Biểu tượng Cấu hình cột hiển thị cho phép chọn cột nào hiện trên bảng, và kéo để đổi thứ tự cột.',
        act: async (p) => { await click(p, p.locator('[title="Cấu hình cột hiển thị"], button:has-text("Cấu hình cột hiển thị")')); await sleep(1200); await mark(topModal(p).locator('.modal-body'), 3500) } },
    { ch: C1, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Thêm mới vai trò: Tên · Mô tả · Sao chép quyền từ', say: 'Để tạo vai trò mới, bấm Thêm mới. Bạn nhập tên vai trò, mô tả, và có thể chọn sao chép quyền từ một vai trò có sẵn.',
        act: async (p) => { await click(p, p.locator('button', { hasText: 'Thêm mới' })); await sleep(1200); await mark(topModal(p).locator('.modal-body'), 4000) } },
    { ch: C1, say: 'Bấm Lưu để tạo. Vai trò mới chưa có quyền sẽ được chuyển thẳng sang màn phân quyền.',
        act: async (p) => { await mark(topModal(p).locator('button', { hasText: 'Lưu' }), 3000) } },
    { ch: C1, say: 'Ở đây mình bấm Đóng, không tạo mới.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Cột Hành động: Phân quyền · Sửa · thao tác khác (⋮)', say: 'Ở cột Hành động, mỗi vai trò có nút Phân quyền, nút Sửa, và nút ba chấm cho các thao tác khác.',
        act: async (p) => { const r = roleRow(p, 'Chăm sóc khách hàng'); await mark(r.locator('td:last-child'), 3500); await hover(p, r.locator('[title="Phân quyền"]')); await sleep(1300); await hover(p, r.locator('[title="Sửa"]')); await sleep(1300); await hover(p, r.locator('td:last-child button').last()) } },
    { ch: C1, cap: 'Sửa: đổi tên, mô tả (có ghi lịch sử)', say: 'Nút Sửa dùng để đổi tên và mô tả vai trò. Mọi lần đổi tên đều được ghi vào lịch sử.',
        act: async (p) => { await click(p, roleRow(p, 'Chăm sóc khách hàng').locator('[title="Sửa"] button')); await sleep(1200); await mark(topModal(p).locator('.modal-body'), 3500) } },
    { ch: C1, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Nút ⋮: Lịch sử · Khoá / Mở khoá · Xoá', say: 'Nút ba chấm gồm Lịch sử, Khoá, và Xoá. Mục Xoá chỉ hiện với vai trò không còn ai giữ. Khi khoá, người đang giữ vai trò sẽ tạm mất các quyền của vai trò, mở khoá là có lại.',
        act: async (p) => { await click(p, roleRow(p, 'Admin').locator('td:last-child button').last()); await sleep(700); await mark(p.locator('.v2-row-actions__item').filter({ visible: true }).first().locator('xpath=..'), 6000) } },
    { ch: C1, cap: 'Lịch sử thay đổi của vai trò', say: 'Bấm Lịch sử để xem các thay đổi của vai trò: tạo mới, đổi tên, thay đổi quyền, khoá và mở khoá, kèm người sửa và thời gian.',
        act: async (p) => { await p.keyboard.press('Escape'); await p.mouse.click(800, 140); await sleep(400); await click(p, roleRow(p, 'Admin_QTTT').locator('td:last-child button').last()); await sleep(600); await click(p, p.locator('.v2-row-actions__item', { hasText: 'Lịch sử' }).filter({ visible: true }).first()); await sleep(1500) } },
    { ch: C1, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Bấm tên vai trò / số "Quyền đang có" để xem nhanh quyền', say: 'Bấm vào tên vai trò, hoặc con số ở cột Quyền đang có, để xem nhanh các quyền của vai trò. Quyền được gom theo phân hệ và chức năng.',
        act: async (p) => { await click(p, roleRow(p, 'Chăm sóc khách hàng').locator('td').nth(2).locator('button')); await topModal(p).locator('.psl-info').first().waitFor({ timeout: 30000 }) } },
    { ch: C1, say: 'Mỗi quyền có nhãn Xem, Thao tác hoặc Duyệt, cùng phạm vi được cấp như công ty, hay tổng công ty.',
        act: async (p) => { const m = topModal(p); await mark(m.locator('.psl-tag').first(), 2200); await sleep(2300); await mark(m.locator('.psl-kv__b').first(), 2200) } },
    { ch: C1, say: 'Phía trên có bộ lọc theo phân hệ, chức năng, loại quyền, và ô tìm theo tên hoặc mã quyền.',
        act: async (p) => { await mark(topModal(p).locator('.rpv-filters'), 4000) } },
    { ch: C1, say: 'Bấm vào một phân hệ ở hàng chip để chỉ xem phân hệ đó, bấm lần nữa để xem lại tất cả.',
        act: async (p) => { const c = topModal(p).locator('.psl-chip').first(); await click(p, c); await sleep(2500); await click(p, c) } },
    { ch: C1, say: 'Tích Hiện mã quyền nếu cần xem mã của từng quyền.',
        act: async (p) => { await click(p, topModal(p).locator('.rpv-opts label', { hasText: 'Hiện mã quyền' })) } },
    { ch: C1, say: 'Nút Phân quyền ở cuối popup mở thẳng màn phân quyền của vai trò này.',
        act: async (p) => { await click(p, topModal(p).locator('.rpv-opts label', { hasText: 'Hiện mã quyền' })); await sleep(500); await mark(topModal(p).locator('.modal-footer button', { hasText: 'Phân quyền' }), 3000) } },
    { ch: C1, say: 'Mình bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Bấm số "Số người giữ" để xem ai đang được cấp vai trò', say: 'Bấm vào con số ở cột Số người giữ để xem những ai đang được cấp vai trò, kèm phòng ban, công ty chính, và trạng thái tài khoản.',
        act: async (p) => { await click(p, roleRow(p, 'Chăm sóc khách hàng').locator('td').nth(3).locator('button')); await topModal(p).locator('.data-table tbody tr').first().waitFor({ timeout: 30000 }); await sleep(800); await mark(topModal(p).locator('.data-table thead'), 3000) } },
    { ch: C1, say: 'Có ô tìm theo mã, họ tên hoặc email, và phân trang ở cuối bảng.',
        act: async (p) => { await click(p, topModal(p).locator('input').first()); await p.keyboard.type('Nguyễn', { delay: 80 }); await sleep(1500); await mark(topModal(p).locator('.modal-body'), 2000) } },
    { ch: C1, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C1, cap: 'Phân trang · số dòng mỗi trang', say: 'Cuối danh sách là phân trang, bạn có thể chọn số dòng hiển thị trên mỗi trang.',
        act: async (p) => { const pg = p.locator('text=/Số dòng\\/trang/').first(); await hover(p, pg); await mark(pg.locator('xpath=ancestor::*[2]'), 3000) } },

    // ===== 2. Phân quyền =====
    { ch: C2, cap: 'Biểu tượng khiên "Phân quyền" ở cột Hành động', say: 'Để phân quyền cho một vai trò, bấm biểu tượng hình khiên ở cột Hành động.',
        act: async (p) => { const b = roleRow(p, 'Admin').locator('[title="Phân quyền"]'); await hover(p, b); await mark(b, 3000) } },
    { ch: C2, cap: 'Tên vai trò · công ty đang phân quyền', say: 'Phía trên màn phân quyền là tên vai trò và công ty đang phân quyền. Bạn chỉ phân quyền trong phạm vi công ty của mình.',
        act: async (p) => { await roleRow(p, 'Admin').locator('[title="Phân quyền"] button').click(); await p.getByText('quyền đã phân').first().waitFor({ timeout: 120000 }); await sleep(1000); await mark(p.locator('.rp-banner'), 4000) } },
    { ch: C2, cap: 'Biểu tượng chữ i: hướng dẫn nhanh · nút Danh sách', say: 'Rê chuột vào biểu tượng chữ i để xem hướng dẫn nhanh. Nút Danh sách để quay về màn vai trò.',
        act: async (p) => { await hover(p, p.locator('#rp-banner-info')); await sleep(2800); await p.mouse.move(800, 300, { steps: 5 }); await hover(p, p.locator('.rp-banner .v2-btn', { hasText: 'Danh sách' })); await mark(p.locator('.rp-banner .v2-btn', { hasText: 'Danh sách' }), 2000) } },
    { ch: C2, cap: 'Bộ lọc: nhóm phân hệ · phân hệ · chức năng · loại quyền · nền tảng · tìm nhanh · Xoá lọc', say: 'Bộ lọc gồm nhóm phân hệ, phân hệ, chức năng, loại quyền, nền tảng ERP hoặc HRM, và ô tìm nhanh theo tên hoặc mã quyền. Nút Xoá lọc để bỏ hết điều kiện.',
        act: async (p) => { await mark(p.locator('.rp-filters'), 6000); await sleep(6200); await mark(p.locator('.rp-filters button', { hasText: 'Xoá lọc' }), 2000) } },
    { ch: C2, cap: 'Hiện mã quyền · Chỉ hiện quyền đã chọn · Mở tất cả · Thu gọn', say: 'Ở thẻ Cây quyền có các tuỳ chọn: Hiện mã quyền, Chỉ hiện quyền đã chọn, Mở tất cả, và Thu gọn.',
        act: async (p) => { await mark(p.locator('.rp-card__tools'), 5000) } },
    { ch: C2, say: 'Bấm Mở tất cả để mở mọi phân hệ, hoặc Thu gọn để đóng lại.',
        act: async (p) => { await click(p, p.locator('.rp-card__hd button', { hasText: 'Mở tất cả' })); await sleep(2200); await click(p, p.locator('.rp-card__hd button', { hasText: 'Thu gọn' })) } },
    { ch: C2, cap: 'Mỗi phân hệ một thẻ: bảng Loại · Tên quyền · Phạm vi', say: 'Mỗi phân hệ là một thẻ, bấm để mở. Bên trong là bảng gồm loại quyền, tên quyền và phạm vi, chia theo từng chức năng.',
        act: async (p) => { const c = pqCard(p, 'Chấm công'); await click(p, c.locator('.pq-sub__hd')); await sleep(1300); await mark(c.locator('.pq-table thead'), 2500); await sleep(2600); await mark(c.locator('.pq-grow').first(), 2500) } },
    { ch: C2, cap: 'Quyền có phạm vi: chọn cấp ở ô bên phải', say: 'Với quyền có phạm vi, bạn chọn cấp ở ô bên phải: tổng công ty, công ty, phòng ban, hoặc bộ phận.',
        act: async (p) => { await click(p, p.locator('.pq-item[data-code="timesheet.bang_cham_cong_tong_hop.view"] :is(.pq-lite, .select2-selection)')) } },
    { ch: C2, cap: '"Không xem" = không cấp quyền', say: 'Chọn Không xem nghĩa là không cấp quyền đó. Ở đây mình chọn cấp Công ty.',
        act: async (p) => { await sleep(2500); const o = p.locator('.select2-container--open .select2-results__option').filter({ hasText: /^Công ty$/ }).first(); await hover(p, o); await sleep(400); await o.click(); await sleep(800); await mark(p.locator('.pq-item[data-code="timesheet.bang_cham_cong_tong_hop.view"] .pq-scope'), 2000) } },
    { ch: C2, cap: 'Tick quyền Thao tác → tự tick quyền Xem mà nó cần', say: 'Quyền không có phạm vi thì bật tắt bằng ô tick. Khi tick một quyền thao tác, quyền xem mà nó cần sẽ được tự động tick theo.',
        act: async (p) => { await click(p, p.locator(SEARCH_PQ)); await p.keyboard.type('mẫu bảng lương', { delay: 70 }); await sleep(1600); const u = p.locator('.pq-item[data-code="payroll.mau_bang_luong.update"]'); await hover(p, u.locator('.pq-chk')); await sleep(400); await u.locator('.pq-chk .custom-control-label').evaluate((e) => e.click()); await sleep(1000); await mark(p.locator('.pq-item[data-code="payroll.mau_bang_luong.view"]'), 3000) } },
    { ch: C2, say: 'Còn nếu bỏ một quyền xem đang được quyền khác cần, hệ thống sẽ hỏi lại cho chắc.' },
    { ch: C2, cap: '"Chọn cả / Bỏ" theo chức năng hoặc cả phân hệ', say: 'Nút Chọn cả và Bỏ trên mỗi chức năng, hoặc trên mỗi phân hệ, giúp cấp hay gỡ nhanh cả nhóm quyền.',
        act: async (p) => { await p.locator(SEARCH_PQ).fill(''); await sleep(1200); const c = pqCard(p, 'Chấm công'); await mark(c.locator('.pq-sub__hd .pq-bulk'), 2000); await sleep(2200); await click(p, c.locator('.pq-group').nth(1).locator('.pq-grow .v2-btn', { hasText: 'Chọn cả' })) } },
    { ch: C2, cap: 'Chỉ hiện quyền đã chọn: rà lại quyền đang cấp', say: 'Tích Chỉ hiện quyền đã chọn để rà lại những quyền đang cấp.',
        act: async (p) => { await click(p, p.locator('.rp-card__hd label', { hasText: 'Chỉ hiện quyền đã chọn' })) } },
    { ch: C2, cap: 'Bảng tổng hợp: số quyền theo loại · thay đổi chưa lưu · theo phân hệ', say: 'Bảng bên phải tổng hợp số quyền đã phân theo loại, số thay đổi chưa lưu, và danh sách quyền theo từng phân hệ.',
        act: async (p) => { await click(p, p.locator('.rp-card__hd label', { hasText: 'Chỉ hiện quyền đã chọn' })); await sleep(600); await mark(p.locator('.rp-sumhead'), 2200); await sleep(2300); await mark(p.locator('.rp-changes'), 2000); await sleep(2100); await mark(p.locator('.rp-summary .psl-list'), 2200) } },
    { ch: C2, say: 'Bấm vào một phân hệ trong bảng tổng hợp để lọc danh sách bên dưới, đồng thời cây quyền sẽ nhảy tới phân hệ đó.',
        act: async (p) => { const c = p.locator('.rp-summary .psl-chip').nth(1); await click(p, c); await sleep(3500); await click(p, c) } },
    { ch: C2, say: 'Tích Hiện mã quyền nếu cần xem mã của từng quyền.',
        act: async (p) => { await click(p, p.locator('.rp-card__hd label', { hasText: 'Hiện mã quyền' })) } },
    { ch: C2, cap: 'Bấm "Lưu phân quyền" để lưu', say: 'Chọn xong, bấm Lưu phân quyền ở góc dưới để lưu. Trong video này mình không lưu, để giữ nguyên dữ liệu.',
        act: async (p) => { await click(p, p.locator('.rp-card__hd label', { hasText: 'Hiện mã quyền' })); await sleep(500); const s = p.locator('.role-perm-page > .footer button', { hasText: 'Lưu phân quyền' }); await hover(p, s); await mark(s, 3500) } },

    // ===== 3. Vai trò nhân viên =====
    { ch: C3, cap: 'Menu trái › Người dùng & phân quyền › Vai trò nhân viên', say: 'Tiếp theo là cấp vai trò cho nhân viên. Bạn mở menu bên trái, chọn Người dùng và phân quyền, rồi chọn Vai trò nhân viên.',
        act: async (p) => { await openUsersGroup(p); const l = menuLink(p, 'Vai trò nhân viên'); await hover(p, l); await mark(l, 1500); await sleep(900); await l.click(); await sleep(1200) } },
    { ch: C3, cap: 'Rời màn khi chưa lưu ⇒ hệ thống hỏi lại', say: 'Vì màn phân quyền còn thay đổi chưa lưu, hệ thống hỏi lại trước khi rời đi. Ở đây mình chọn Thoát.',
        act: async (p) => { const m = topModal(p); if (await m.count()) await mark(m.locator('.modal-content'), 3500) } },
    { ch: C3, cap: 'Màn Vai trò nhân viên: vai trò đang giữ · loại · người cập nhật', say: 'Màn Vai trò nhân viên liệt kê nhân viên của công ty, kèm các vai trò đang giữ, loại công ty chính hay kiêm nhiệm, và người cập nhật.',
        act: async (p) => { const b = p.locator('.modal.show button', { hasText: 'Thoát' }).first(); if (await b.count()) await click(p, b); await p.locator('table tbody tr').first().waitFor({ timeout: 120000 }); await sleep(800); await mark(p.locator('table').first(), 3500) } },
    { ch: C3, say: 'Bấm vào chip vai trò để xem quyền của vai trò đó.',
        act: async (p) => { const c = p.locator('.er-role-chip').first(); await hover(p, c); await mark(c, 2500) } },
    { ch: C3, cap: 'Tìm nhanh · Tìm kiếm nâng cao: phòng ban · bộ phận · vai trò · loại · trạng thái · chưa có vai trò', say: 'Ô tìm nhanh tìm theo mã, tên hoặc email nhân viên. Tìm kiếm nâng cao có thêm bộ lọc phòng ban, bộ phận, vai trò, loại, trạng thái tài khoản, và chưa có vai trò nào.',
        act: async (p) => { const c = p.locator('.smart-filter-card'); await mark(c.locator('input').first(), 2500); await sleep(2700); await click(p, c.locator('button', { hasText: 'Tìm kiếm nâng cao' })); await sleep(1200); await mark(c, 5000) } },
    { ch: C3, cap: 'Cài đặt bộ lọc · Xuất Excel · Cấu hình cột', say: 'Cài đặt bộ lọc và Cấu hình cột hoạt động giống màn Vai trò. Nút Xuất Excel để tải danh sách về máy.',
        act: async (p) => { await mark(p.locator('button', { hasText: 'Cài đặt bộ lọc' }), 1800); await sleep(1900); await mark(p.locator('[title="Cấu hình cột hiển thị"], button:has-text("Cấu hình cột hiển thị")'), 1800); await sleep(1900); await mark(p.locator('button', { hasText: 'Xuất Excel' }), 2000) } },
    { ch: C3, cap: 'Phân quyền hàng loạt: cấp vai trò cho nhiều người', say: 'Nút Phân quyền hàng loạt dùng để cấp vai trò cho nhiều người một lúc.',
        act: async (p) => { await click(p, p.locator('button', { hasText: 'Phân quyền hàng loạt' })); await p.locator('#bulk-permission-modal').waitFor({ timeout: 30000 }); await sleep(800) } },
    { ch: C3, say: 'Bạn chọn đối tượng theo khối, phòng ban, bộ phận, chức vụ, chức danh, hoặc thêm từng nhân viên, rồi chọn vai trò cần cấp.',
        act: async (p) => { const m = p.locator('#bulk-permission-modal'); await mark(m.getByText('Đối tượng phân quyền').locator('xpath=ancestor::*[2]'), 5000); await sleep(5200); await mark(m.getByText('Chọn vai trò').first().locator('xpath=..'), 2500) } },
    { ch: C3, say: 'Bảng bên phải liệt kê nhân viên sẽ được cập nhật, có thể loại trừ từng người. Bấm Áp dụng, hoặc Áp dụng và làm tiếp để lưu.',
        act: async (p) => { const m = p.locator('#bulk-permission-modal'); await mark(m.locator('table').first(), 3500); await sleep(3700); await mark(m.locator('button', { hasText: 'Áp dụng' }).first(), 1800); await sleep(1900); await mark(m.locator('button', { hasText: 'Áp dụng và làm tiếp' }), 1800) } },
    { ch: C3, say: 'Ở đây mình bấm Hủy.', act: async (p) => { await closeModal(p) } },
    { ch: C3, cap: 'Cột Hành động: Sửa · Quyền đang được cấp · Lịch sử', say: 'Ở cột Hành động có nút Sửa, Quyền đang được cấp, và Lịch sử.',
        act: async (p) => { const r = p.locator('table tbody tr').first(); await mark(r.locator('td:last-child'), 3000); for (const t of ['Sửa', 'Quyền đang được cấp', 'Lịch sử']) { await hover(p, r.locator(`[title="${t}"]`)); await sleep(900) } } },
    { ch: C3, cap: 'Quyền đang được cấp: quyền từ các vai trò, quyền trùng', say: 'Quyền đang được cấp cho biết nhân viên có những quyền nào từ các vai trò, và quyền nào bị trùng giữa các vai trò. Quyền trùng vẫn có hiệu lực, phạm vi lấy theo mức cao hơn.',
        act: async (p) => { await click(p, p.locator('table tbody tr').first().locator('[title="Quyền đang được cấp"] button')); await sleep(1800); await mark(topModal(p).locator('.modal-body'), 5000) } },
    { ch: C3, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C3, cap: 'Tìm nhân viên rồi bấm vào mã (hoặc nút Sửa)', say: 'Để cấp vai trò cho một người, bạn tìm nhân viên rồi bấm vào mã, hoặc bấm nút Sửa.',
        act: async (p) => { const s = p.locator('.smart-filter-card input').first(); await click(p, s); await p.keyboard.type('DNS01', { delay: 90 }); await p.keyboard.press('Enter'); await sleep(2000); await click(p, p.locator('table tbody tr').first().locator('a.v2-cell-link').first()); await p.locator('.er-role-list').waitFor({ timeout: 120000 }); await sleep(800) } },
    { ch: C3, cap: 'Mặc định chỉ hiện vai trò đang cấp · bấm số quyền để xem', say: 'Thẻ vai trò mặc định chỉ hiện những vai trò đang được cấp. Bấm vào số quyền để xem chi tiết quyền của vai trò.',
        act: async (p) => { await mark(p.locator('.er-role-list'), 3000); await sleep(3100); await hover(p, p.locator('.er-role-row a').first()); await mark(p.locator('.er-role-row a').first(), 2000) } },
    { ch: C3, cap: '"Cấp thêm vai trò": hiện toàn bộ để tick thêm', say: 'Bấm Cấp thêm vai trò để hiện toàn bộ vai trò của công ty, rồi tick những vai trò cần cấp. Ô tìm giúp tìm nhanh theo tên vai trò.',
        act: async (p) => { await click(p, p.locator('.er-role-search .v2-btn', { hasText: 'Cấp thêm vai trò' })); await sleep(2000); const u = p.locator('.er-role-row:not(.is-checked):not(.is-locked)').first(); await hover(p, u); await u.locator('.custom-control-label').evaluate((e) => e.click()); await sleep(1500); await mark(p.locator('.er-role-search input'), 2000) } },
    { ch: C3, cap: 'Quyền hiệu lực: tính lại ngay khi đổi vai trò', say: 'Bảng quyền hiệu lực bên phải được tính lại ngay khi bạn đổi vai trò, chưa cần lưu.',
        act: async (p) => { const t = p.locator('.er-side .rp-summary__total').first(); await t.evaluate((e) => e.scrollIntoView({ block: 'center' })); await sleep(500); await mark(t.locator('xpath=..'), 4000) } },
    { ch: C3, cap: 'Phân công quản lý phòng ban', say: 'Phần Phân công quản lý phòng ban xác định nhân viên được quản lý những phòng ban, bộ phận nào. Tích Quản lý tất cả phòng ban nếu người này quản lý toàn công ty.',
        act: async (p) => { const h = p.locator('.er-main').getByText('Phân công quản lý phòng ban tại').first(); await h.evaluate((e) => e.scrollIntoView({ block: 'center' })); await sleep(600); await mark(h.locator('xpath=ancestor::div[contains(concat(" ",@class," ")," card ")][1]'), 6000) } },
    { ch: C3, cap: 'Thông tin nhân viên · Quyền đang được cấp', say: 'Bên phải là thông tin nhân viên, và nút Quyền đang được cấp.',
        act: async (p) => { await p.evaluate(() => window.scrollTo(0, 0)); await sleep(500); const s = p.locator('.er-side').first(); await mark(s, 3000); await hover(p, s.locator('button', { hasText: 'Quyền đang được cấp' })) } },
    { ch: C3, cap: 'Công ty làm việc: Thêm · Gỡ công ty', say: 'Thẻ Công ty làm việc cho biết nhân viên làm ở những công ty nào. Bấm Thêm để thêm công ty làm việc. Gỡ công ty là gỡ luôn vai trò và phân công phòng ban ở công ty đó.',
        act: async (p) => { const t = p.getByText(/^Công ty làm việc/).first(); await mark(t.locator('xpath=ancestor::*[3]'), 4000); await sleep(4200); await click(p, p.locator('.er-side button', { hasText: 'Thêm' }).first()); await sleep(1000) } },
    { ch: C3, say: 'Bấm Đóng để quay lại.', act: async (p) => { await closeModal(p) } },
    { ch: C3, cap: 'Lịch sử thay đổi vai trò của nhân viên', say: 'Cuối màn là lịch sử thay đổi vai trò của nhân viên.',
        act: async (p) => { const b = p.locator('button', { hasText: 'Xem lịch sử' }).first(); await b.scrollIntoViewIfNeeded(); await sleep(500); await hover(p, b); await mark(b.locator('xpath=ancestor::*[3]'), 3000) } },
    { ch: C3, cap: 'Bấm "Lưu" để lưu thay đổi', say: 'Thay đổi xong, bấm Lưu ở góc dưới để lưu. Trong video này mình không lưu.',
        act: async (p) => { const s = p.locator('.footer button', { hasText: /^\s*Lưu\s*$/ }).first(); await hover(p, s); await mark(s, 3500) } },

    // ===== Kết thúc =====
    { ch: C9, cap: 'Các chức năng chính của phần phân quyền', say: 'Đó là các chức năng chính của phần phân quyền.' },
    { ch: C9, cap: 'Cảm ơn các bạn đã xem video!', say: 'Cảm ơn các bạn đã xem video!' },
]

;(async () => {
    // B1: lời đọc từng bước
    const TTS = path.join(OUT, '..', 'ttsenv', 'bin', 'edge-tts')
    const CACHE = path.join(OUT, 'tts-cache')
    fs.mkdirSync(CACHE, { recursive: true })
    const ttsSentence = (text) => {
        const f = path.join(CACHE, crypto.createHash('md5').update(text).digest('hex') + '.mp3')
        if (fs.existsSync(f) && fs.statSync(f).size > 1000) return f
        for (let k = 0; k < 16; k++) {
            try {
                execFileSync(TTS, ['--voice', 'vi-VN-HoaiMyNeural', '--rate=+4%', '--text', text, '--write-media', f], { stdio: 'ignore' })
            } catch (e) {}
            if (fs.existsSync(f) && fs.statSync(f).size > 1000) return f
            execFileSync('sleep', [String(2 + k * 2)])
        }
        throw new Error('Không tạo được lời đọc: ' + text)
    }
    const silence = path.join(CACHE, 'gap.mp3')
    if (!fs.existsSync(silence)) execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.25', '-c:a', 'libmp3lame', silence])
    const voice = steps.map((s, i) => {
        const parts = s.say.match(/[^.!?]+[.!?]+/g).map((x) => x.trim()).filter(Boolean)
        const files = parts.map(ttsSentence)
        const list = path.join(OUT, `st-${i}.txt`)
        fs.writeFileSync(list, files.map((f, k) => (k ? `file '${silence}'\nfile '${f}'` : `file '${f}'`)).join('\n'))
        const f = path.join(OUT, `st-${String(i).padStart(2, '0')}.wav`)
        execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-ar', '48000', '-ac', '1', f])
        const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], { encoding: 'utf8' }).trim())
        return { file: f, dur }
    })
    console.log(`lời đọc: ${steps.length} bước, tổng ${voice.reduce((n, v) => n + v.dur, 0).toFixed(0)}s`)

    // B2: quay
    const browser = await chromium.launch()
    const context = await browser.newContext({ viewport: { width: W, height: H }, recordVideo: { dir: OUT, size: { width: W, height: H } }, locale: 'vi-VN' })
    await context.addInitScript((t) => {
        localStorage.setItem('access_token', t)
        localStorage.removeItem('admin.roles.showPermissionCode')
    }, TOKEN)
    await context.addInitScript(OVERLAY_INIT)
    const page = await context.newPage()
    page.setDefaultTimeout(30000)
    page.on('dialog', (d) => d.accept().catch(() => {}))
    const t0 = Date.now()
    const cuts = []
    const timeline = []
    // chuẩn bị trang chủ (cắt khỏi video)
    await page.goto(`${BASE}/`, { waitUntil: 'domcontentloaded' })
    await page.getByText(/^\s*Quản trị\s*$/i).first().waitFor({ timeout: 120000 })
    await sleep(1500)
    cuts.push([0, (Date.now() - t0) / 1000 - 0.3])

    let cap = ''
    for (let i = 0; i < steps.length; i++) {
        const s = steps[i]
        if (s.cap) cap = s.cap
        await caption(page, s.ch, cap).catch(() => {})
        const start = (Date.now() - t0) / 1000
        timeline.push({ i, start, dur: voice[i].dur, file: voice[i].file })
        const tStart = Date.now()
        try {
            if (s.act) await s.act(page)
        } catch (e) {
            console.error(`Bước ${i} lỗi: ${e.message.split('\n')[0]}`)
        }
        await caption(page, s.ch, cap).catch(() => {}) // trang mới (điều hướng trong bước) ⇒ gắn lại chú thích
        const left = (voice[i].dur + GAP) * 1000 - (Date.now() - tStart)
        if (left > 0) await sleep(left)
    }
    await sleep(1800)
    const video = page.video()
    await context.close()
    await browser.close()
    const webm = await video.path()
    fs.writeFileSync(path.join(OUT, 'timeline2.json'), JSON.stringify({ webm, timeline, cuts }, null, 2))
    console.log('VIDEO', webm, `${((Date.now() - t0) / 1000).toFixed(0)}s`)
})()
