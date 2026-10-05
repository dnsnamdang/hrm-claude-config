from common import *
with user_page('sondp.da@tanphat.com') as page:
    go(page,'/assign/solutions')
    inp=page.locator('input[placeholder^="Tìm theo mã giải pháp"]').first
    inp.fill('DA090_GP01'); inp.press('Enter'); page.wait_for_timeout(6000); idle(page)
    row=page.locator('tr', has_text='DA090_GP01').first
    print(row.locator('.v2-row-actions').inner_html())
    icon(page, row.locator('span[title="Lưu và duyệt"] a'), 'btn_luu_duyet_row')
    go(page,'/assign/solutions/%d/edit?mode=approve'%SID)
    page.locator('text=Quản lý hạng mục').first.click(); page.wait_for_timeout(3000)
    snap(page,'x_leader_duyet')
    icon(page, btn(page,'Lưu và duyệt'), 'btn_luu_duyet')
    btn(page,'Lưu và duyệt').first.click(); page.wait_for_timeout(6000)
    page.screenshot(path=EX+'after_leader.png'); print(page.url)
