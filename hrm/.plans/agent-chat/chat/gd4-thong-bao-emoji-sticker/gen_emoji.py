import json, re, sys
src, out = sys.argv[1], sys.argv[2]
GROUPS = {
 'Smileys & Emotion': ('mat-cuoi', 'Mặt cười', 'ri-emotion-line'),
 'People & Body': ('con-nguoi', 'Con người', 'ri-hand-heart-line'),
 'Animals & Nature': ('thien-nhien', 'Động vật & thiên nhiên', 'ri-leaf-line'),
 'Food & Drink': ('do-an', 'Đồ ăn & uống', 'ri-cake-3-line'),
 'Travel & Places': ('du-lich', 'Du lịch & địa điểm', 'ri-plane-line'),
 'Activities': ('hoat-dong', 'Hoạt động', 'ri-football-line'),
 'Objects': ('do-vat', 'Đồ vật', 'ri-lightbulb-line'),
 'Symbols': ('ky-hieu', 'Ký hiệu', 'ri-heart-line'),
}
VI = {
 '😀':'cười vui','😁':'cười toe','😂':'cười ra nước mắt','🤣':'cười lăn','😊':'vui mỉm cười','😍':'yêu mắt tim','🥰':'yêu thương','😘':'hôn',
 '😎':'ngầu kính','🤔':'suy nghĩ','😮':'ngạc nhiên wow','😢':'buồn','😭':'khóc','😡':'giận tức','😠':'giận','😱':'hoảng sợ','😴':'ngủ',
 '🙄':'chán','😅':'cười ngượng','😉':'nháy mắt','🙂':'mỉm cười','🙃':'lộn ngược','😇':'thiên thần','🤩':'thích thú sao','🥺':'năn nỉ',
 '😤':'bực','😬':'ngại','🤗':'ôm','🤭':'che miệng cười','🤫':'im lặng suỵt','😷':'ốm khẩu trang','🤒':'sốt ốm','🥳':'tiệc chúc mừng',
 '😏':'nhếch mép','😌':'nhẹ nhõm','😋':'ngon','😜':'lè lưỡi','🤯':'nổ não sốc','😳':'đỏ mặt','🥲':'cười trong nước mắt','😐':'không cảm xúc',
 '👍':'thích ok đồng ý like','👎':'không thích','👏':'vỗ tay','🙏':'cảm ơn cầu xin','👋':'chào vẫy tay','👌':'ok được','✌️':'chiến thắng',
 '🤝':'bắt tay hợp tác','💪':'cố lên mạnh','🙌':'hoan hô','🤞':'may mắn','✋':'dừng lại','👉':'chỉ','👀':'nhìn xem','🫶':'trái tim tay',
 '❤️':'tim yêu','💔':'tim vỡ','💯':'100 điểm tuyệt','🔥':'cháy lửa hot','✅':'xong đúng hoàn thành','❌':'sai không','⚠️':'cảnh báo',
 '🎉':'chúc mừng','🎊':'chúc mừng hoa giấy','🎁':'quà','🎂':'sinh nhật bánh','🏆':'cúp vô địch','🚀':'tên lửa tăng tốc','💡':'ý tưởng',
 '⏰':'báo thức gấp','📌':'ghim','📅':'lịch','📞':'điện thoại gọi','💰':'tiền','📈':'tăng trưởng','📉':'giảm','☕':'cà phê','🍻':'cạn ly bia',
 '🌹':'hoa hồng','🌸':'hoa','☀️':'nắng mặt trời','🌧️':'mưa','⭐':'sao','✨':'lấp lánh','💤':'ngủ','🆗':'ok','❓':'hỏi','❗':'chú ý',
 '🐶':'chó','🐱':'mèo','🍜':'phở mì','🍚':'cơm','🍺':'bia','🎵':'nhạc','⚽':'bóng đá','🏠':'nhà','🚗':'xe ô tô','🏍️':'xe máy','✈️':'máy bay',
}
def ver(line):
    m = re.search(r'#\s*\S+\s+E(\d+\.\d+)', line); return float(m.group(1)) if m else 0
groups = {}; order=[]
g=None
for line in open(src, encoding='utf-8'):
    if line.startswith('# group:'):
        g = line.split(':',1)[1].strip(); continue
    if g not in GROUPS or '; fully-qualified' not in line: continue
    if ver(line) > 13.0: continue
    cps, rest = line.split(';',1)
    cps = cps.split()
    if any(c in ('1F3FB','1F3FC','1F3FD','1F3FE','1F3FF') for c in cps): continue
    ch = ''.join(chr(int(c,16)) for c in cps)
    name = re.sub(r'^.*?E\d+\.\d+\s+','',rest.split('#',1)[1]).strip()
    key = GROUPS[g][0]
    if key not in groups: groups[key]=[]; order.append(g)
    kw = name.lower()
    if ch in VI: kw += ' ' + VI[ch]
    groups[key].append([ch, kw])
data = [{'key':GROUPS[g][0],'label':GROUPS[g][1],'icon':GROUPS[g][2],'items':groups[GROUPS[g][0]]} for g in order]
with open(out,'w',encoding='utf-8') as f:
    f.write('/* eslint-disable */\n// SINH TỰ ĐỘNG từ Unicode emoji-test.txt 15.1 (chỉ emoji ≤ E13.0 để Windows 10 hiển thị được; bỏ biến thể màu da\n')
    f.write('// và nhóm Cờ). Mỗi mục: [emoji, "tên tiếng Anh + từ khoá tiếng Việt"]. Sinh lại: .plans/agent-chat/chat/gd4-thong-bao-emoji-sticker/gen_emoji.py\n')
    f.write('export const EMOJI_GROUPS = ' + json.dumps(data, ensure_ascii=False, separators=(',',':')) + '\n')
print(sum(len(d['items']) for d in data), [ (d['key'],len(d['items'])) for d in data])
