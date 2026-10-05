from common import *
with user_page('hungvq.da@tanphat.com') as page:
    go(page,'/assign/solutions')
    print(page.url)
    inp=page.locator('input[placeholder^="Tìm theo mã giải pháp"]').first
    inp.fill('DA090_GP01'); inp.press('Enter'); page.wait_for_timeout(6000); idle(page)
    snap(page,'x_list_pm')
    row=page.locator('tr', has_text='DA090_GP01').first
    print(row.locator('.v2-row-actions').inner_html())
    icon(page, row.locator('span[title="Giao cho Leader"] a'), 'btn_giao_leader_row')
    go(page,'/assign/solutions/%d/edit?mode=approve'%SID)
    snap(page,'05_pm_duyet_info')
    page.locator('text=Quản lý hạng mục').first.click(); page.wait_for_timeout(3000)
    snap(page,'05_pm_duyet')
    icon(page, btn(page,'Giao cho Leader'), 'btn_giao_leader')
    icon(page, btn(page,'Quay lại'), 'btn_quay_lai')
