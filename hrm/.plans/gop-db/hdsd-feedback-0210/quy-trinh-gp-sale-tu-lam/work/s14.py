from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/prospective-projects/151/manager'); page.wait_for_timeout(8000); wait_load(page)
    page.locator('button:has-text("Chốt giải pháp")').wait_for(timeout=180000); wait_load(page)
    page.locator('button:has-text("Chốt giải pháp")').evaluate('e=>e.click()')
    page.get_by_text('Chọn hồ sơ giải pháp').first.wait_for(timeout=120000); page.wait_for_timeout(2000)
    mod=page.locator('.modal.show').last
    mod.locator('tbody tr').filter(has_text='HS.TD.CTV_NV').first.click(); page.wait_for_timeout(500)
    mod.locator('textarea').first.fill('Khách hàng đồng ý phương án 02 cầu nâng 2 trụ và hệ thống khí nén.')
    page.screenshot(path='chot_dbg.png')
    if not mod.locator('input[placeholder^="Nhập tên tài liệu"]').count():
        mod.locator('button:has-text("Thêm file")').first.evaluate('e=>e.click()'); page.wait_for_timeout(1000)
    mod.locator('input[placeholder^="Nhập tên tài liệu"]').first.fill('Biên bản xác nhận giải pháp')
    mod.locator('input[type=file]').first.set_input_files('Bien_ban_xac_nhan_giai_phap.pdf')
    page.wait_for_timeout(8000)
    mod.locator('textarea').first.click(); settle(page)
    page.screenshot(path=SH+'10_chotgp.png')
    tight(page, mod.locator('button:has-text("Lưu & gửi thông báo")'), IC+'btn_luuguitb.png')
    tight(page, mod.locator('button:has-text("Đóng")').last, IC+'btn_dong_chot.png')
    tight(page, mod.locator('label:has-text("Chọn file"), .upload-btn').first, IC+'btn_chonfile.png') if mod.locator('.upload-btn').count() else None
    resp=[]
    page.on('response', lambda r: resp.append((r.status, r.url, r.text()[:400])) if 'finalize' in r.url else None)
    mod.locator('button:has-text("Lưu & gửi thông báo")').evaluate('e=>e.click()'); page.wait_for_timeout(15000)
    for x in resp: print(x)
    settle(page); page.screenshot(path='after_chot.png')
