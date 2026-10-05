from common import *
A='Đã có máy nén khí trục vít 7,5 kW đặt ở phòng kỹ thuật cạnh xưởng; đường ống chính D27 đã chạy tới cửa phòng thực hành. Bản vẽ mặt bằng đính kèm ở mục Files của dự án.'
with browser_page() as page:
    go(page,'/assign/request-solution',30000)
    row=page.locator('tbody tr').filter(has_text='TPE.YCP.TC.26.0912').first
    page.screenshot(path='explore/h_list.png')
    go(page,'/assign/prospective-projects',35000)
    r=page.locator('tbody tr').filter(has_text='DA093').first
    cut(page, r.locator('a').filter(has_text='DA093').first, 'link_ma_duan.png')
    go(page,'/assign/prospective-projects/153/manager',40000)
    t=page.get_by_text('Thu thập thông tin', exact=True).first
    cut(page, t.locator('xpath=..'), 'tab_thuthap.png')
    t.click(); page.wait_for_timeout(10000)
    sec=page.get_by_text('Thông tin bổ sung', exact=True).first
    sec.scroll_into_view_if_needed()
    ta=page.get_by_placeholder('Nhập câu trả lời...').first
    ta.fill(A); page.wait_for_timeout(500)
    bb=sec.bounding_box(); page.mouse.wheel(0, bb['y']-300); page.wait_for_timeout(800); page.mouse.move(5,5)
    page.screenshot(path=S+'n16_update.png')
    btn=page.get_by_role('button', name='Lưu phiếu').last
    cut(page, btn, 'btn_luuphieu.png')
    btn.click(); page.wait_for_timeout(10000)
    go(page,'/assign/request-solution/34/edit',45000)
    page.locator('.footer').get_by_role('button', name='Lưu và gửi').click(); page.wait_for_timeout(2500)
    page.locator('#confirm').get_by_role('button', name='Xác nhận').click(); page.wait_for_timeout(20000)
    print(page.url)
