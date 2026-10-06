from common import *
from stageA2 import fill_base
import subprocess
def q(sql): return subprocess.run(['mysql','-uroot','local_hrm_erp','-N','-e',sql],capture_output=True,text=True).stdout.strip()
with browser_page(1440, 1000) as page:
    fill_base(page, 'Họp rà soát tiến độ thu hồi công nợ tháng 10', '07/10/2026 14:00', '07/10/2026 15:00')
    btn(page.locator('.footer'),'Lưu và Lên lịch').click(); page.wait_for_timeout(7000)
    fill_base(page, 'Họp chuẩn bị hội nghị khách hàng cuối năm', '09/10/2026 09:00', '09/10/2026 10:00')
    btn(page.locator('.footer'),'Lưu nháp').click(); page.wait_for_timeout(7000)
print(q("select id,code,name,status from meetings where id>52"))
