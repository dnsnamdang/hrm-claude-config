import sys
from _khien import khien_page, BASE
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import clip
S = 'shots/'
def open_recv(page, hid):
    page.goto(BASE + '/assign/handover/%d/receive' % hid, wait_until='domcontentloaded')
    page.wait_for_selector('text=Danh sách cần bàn giao', timeout=120000); page.wait_for_timeout(3500)
def row(page, code): return page.locator('tr.ho-item-row', has_text=code).first

with khien_page() as page:
    # D (id 4): accept-all confirm + leave warning (no write)
    open_recv(page, 4)
    page.screenshot(path=S + '07-tiep-nhan.png')
    clip(page, page.locator('button.btn-accept', has_text='Tiếp nhận tất cả'), S + 'icon_tiepnhantatca.png')
    r = row(page, '0971')
    r.locator('button.btn-accept').scroll_into_view_if_needed()
    clip(page, r.locator('button.btn-accept'), S + 'icon_nhan.png', pad=4)
    clip(page, r.locator('button.btn-reject-sm'), S + 'icon_tuchoi.png', pad=4)
    page.evaluate("() => { const t = document.querySelector('.table-responsive'); if (t) t.scrollLeft = 10000 }"); page.wait_for_timeout(600)
    page.screenshot(path=S + '07b-tiep-nhan-xacnhan.png')
    page.locator('button.btn-accept', has_text='Tiếp nhận tất cả').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '09-tiep-nhan-tat-ca.png')
    page.locator('.modal.show .close').first.click(); page.wait_for_timeout(1200)
    btns = page.locator('.footer .group-select-btn').first.locator(':scope > *')
    clip(page, btns.last, S + 'icon_quaylai.png')
    btns.last.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '12-canh-bao-quay-lai.png')
    page.locator('.modal.show button', has_text='Tiếp tục xác nhận').first.click(); page.wait_for_timeout(2500)
    print('URL sau Tiep tuc xac nhan:', page.url)
    open_recv(page, 4)
    # item detail popup
    row(page, '0971').locator('a.text-primary').first.click(); page.wait_for_timeout(4500)
    page.screenshot(path=S + '11-chi-tiet-nhiem-vu.png')
    page.keyboard.press('Escape'); page.wait_for_timeout(1500)

    # A (id 3): accept 966, reject 967 (real writes)
    open_recv(page, 3)
    page.evaluate("() => { const t = document.querySelector('.table-responsive'); if (t) t.scrollLeft = 10000 }"); page.wait_for_timeout(600)
    row(page, '0966').locator('button.btn-accept').click(); page.wait_for_timeout(3500)
    page.screenshot(path=S + '08-da-tiep-nhan.png')
    page.evaluate("() => { const t = document.querySelector('.table-responsive'); if (t) t.scrollLeft = 10000 }"); page.wait_for_timeout(600)
    row(page, '0967').locator('button.btn-reject-sm').click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '10-tu-choi.png')
    ta = page.locator('.modal.show textarea').first
    ta.fill('Không đủ'); page.locator('.modal.show button', has_text='Từ chối').first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=S + '10b-tu-choi-ngan.png')
    if page.locator('.modal.show').count() == 0:
        row(page, '0967').locator('button.btn-reject-sm').click(); page.wait_for_timeout(1500)
    ta = page.locator('.modal.show textarea').first
    ta.fill('Đang phụ trách 2 dự án lắp đặt, không đủ thời gian nhận thêm bản vẽ bố trí')
    page.locator('.modal.show button', has_text='Từ chối').first.click(); page.wait_for_timeout(3500)
    page.evaluate("() => { const t = document.querySelector('.table-responsive'); if (t) t.scrollLeft = 10000 }"); page.wait_for_timeout(600)
    page.screenshot(path=S + '10c-da-tu-choi.png')
