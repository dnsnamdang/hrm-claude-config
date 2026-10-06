import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
def field(page, label):
    return page.locator('xpath=//label[normalize-space(.)="%s" or starts-with(normalize-space(.),"%s")]/ancestor::div[.//span[contains(@class,"select2")]][1]' % (label, label)).first
def choose(page, label, option):
    f = field(page, label)
    f.locator('.select2-selection').first.click(); page.wait_for_timeout(800)
    page.locator('.select2-container--open .select2-results__option', has_text=option).first.click()
    page.wait_for_timeout(1500)
def pick_customer(page, code):
    page.get_by_placeholder('Nhấn vào đây để chọn thông tin khách hàng').first.click(); page.wait_for_timeout(2500)
    page.get_by_placeholder('Nhập tên / mã khách hàng').fill(code); page.keyboard.press('Enter'); page.wait_for_timeout(3500)
    page.locator('#choose-erp-customer tbody tr', has_text=code).first.click(); page.wait_for_timeout(4000)
