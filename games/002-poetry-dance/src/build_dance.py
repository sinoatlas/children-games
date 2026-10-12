from pathlib import Path
import json, math, shutil
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from pypdf import PdfReader

ROOT=Path(__file__).parent
NAME='诗画小舞会亲子套装'
OUT=ROOT if ROOT.name==NAME else ROOT/NAME
OUT.mkdir(exist_ok=True)
(OUT/'assets').mkdir(exist_ok=True)
art=ROOT/'诗画小舞会动作插画.png'
if not art.exists():art=ROOT/'assets'/'诗画小舞会动作插画.png'
ART=OUT/'assets'/'诗画小舞会动作插画.png'
if art.resolve()!=ART.resolve():shutil.copy2(art,ART)
pdfmetrics.registerFont(TTFont('CN',r'C:\Windows\Fonts\simhei.ttf'))
W,H=595.276,841.89
INK=HexColor('#303C45');ACC=HexColor('#925E70');LINE=HexColor('#DCC8CC')
CARDS=[]

def wrap(s,fs,width):
    result=[]
    for para in s.split('\n'):
        line=''
        for ch in para:
            if pdfmetrics.stringWidth(line+ch,'CN',fs)>width:
                if ch in '。，、；：？！）】”' and len(line)>1:
                    result.append(line[:-1]);line=line[-1]+ch
                else:result.append(line);line=ch
            else:line+=ch
        result.append(line)
    return result

def txt(c,s,x,y,fs=11,width=519,leading=None,color=INK):
    c.setFont('CN',fs);c.setFillColor(color)
    for line in wrap(s,fs,width):
        c.drawString(x,y,line);y-=leading or fs*1.55
    return y

def base(c,title,n,kind):
    txt(c,'诗画小舞会  /  '+kind,38,H-32,9,color=ACC)
    txt(c,title,38,H-69,23,color=black)
    c.setStrokeColor(LINE);c.line(38,42,W-38,42)
    txt(c,f'{n:02d}  /  3岁亲子版 1.0',38,24,9,color=ACC)

def sec(c,title,body,y):
    y=txt(c,title,38,y,14,color=black)-7
    y=txt(c,body,38,y,11,leading=18)-18
    assert y>55,(title,y)
    return y

RULES=[
('一起把诗跳出来',[
('游戏的故事','花园要举办一场小舞会，小鹅、月亮和小鱼都来邀请你们。妹妹选一个地方，爸爸妈妈和她一起把诗里的画面演出来，再把汉字送到画面旁，最后跳一段全家自己编的小舞。'),
('三个人都有自己的事','妹妹是小领舞：选场景、选动作、选快慢，还可以随时休息。一位家长是念诗人：慢读一句诗、展示图和字，同时参与动作。另一位是伴舞：先模仿孩子，再提供一个动作，负责腾出空间。下一局两位家长交换。爸爸妈妈都参加最后的小舞。'),
('一局怎样完成','选一个场景，做两个舒服的动作，让一个汉字与图画见面，再由孩子选两个动作带全家跳一遍，就能谢幕。指图、点头、坐着摆手、只看父母示范都算参与；这些环节可以跳过，也可重复喜欢的部分。'),
('时长与节奏','第一次约8至12分钟，只玩小鹅池塘。想多玩可以再开一局，先休息。第一次每次听一句，做一次，再留几秒给孩子反应。古诗不用配现成歌曲；家长拍手或轻念就能带出节奏。'),
('家里要准备什么','桌上放图卡、字卡，地面留出三个人伸手不碰人的空间。纸、打印机和剪刀由大人准备；不需要买舞裙、音箱或舞蹈道具。卡片留在桌上，不铺地面当跳格。'),
('首局最少打印','材料第1、2、5、7、10页，共五页。规则书第2页可在屏幕上看。全套规则6页、材料11页；A4、100%、单面。彩色动作图更直观，汉字用黑字白底。')]),
('首局：小鹅池塘',[
('开场 约1分钟','念诗人说：“小鹅要开舞会，你愿意带我们跳吗？”展示材料第2页的小鹅和波浪图。妹妹指哪张就先做哪张。伴舞面对妹妹，留出手臂距离，也做动作。没有回应时家长先示范，不追问。'),
('听一句 做一下 约3分钟','先念“鹅，鹅，鹅”，双肘轻轻向外弯，小翅膀晃三下；妹妹做一下也可以。再念“白毛浮绿水”，双手在身前摆波浪。两位家长一起动。喜欢再念“曲项向天歌”和“红掌拨清波”；不要求妹妹记住或跟读。'),
('给水找家 约1分钟','只拿第5页水图卡和“水”字卡，放在桌上。念诗人指着字说：“这是水，诗里也有水。”请妹妹把水图卡放到水字旁。想让父母放也可以。首局直接提供对应的一对，不混入另外两个字。'),
('妹妹编舞 约2分钟','把小鹅与波浪两张动作卡放在第10页小舞谱的两个格子里。妹妹决定先后；念诗人按顺序读诗句，伴舞跟妹妹做第一动作、第二动作。全家做完一轮，可以让妹妹换顺序再来一次。'),
('全家谢幕 约1分钟','孩子摆一个舒服的姿势，爸爸妈妈跟着摆，停一小会儿就好。念诗人说：“你刚才先做小鹅，再做波浪，我们都跟上了。”妹妹挥手告别，三个人一起收卡。谢幕不拍照也能完成。'),
('今天到这里也很好','时间是建议，不设倒计时。妹妹只喜欢小鹅，就围绕小鹅反复跳；不想看字，念诗人展示一次便收起。出现疲倦、走开或说不玩，就结束。背出诗、认出字都不是完成条件。')]),
('另外两场小舞会',[
('月亮庭院的邀请','念诗人说：“月亮来听我们的安静小舞了。”用材料第2、3页的月亮、举头、低头动作；诗在第8页，字在第5页。第一次先玩“举头望明月，低头思故乡”两句，完整原诗由家长读给孩子听。'),
('月亮的动作与意思','“举头望明月”：双手在头上或胸前做一个松松的圆，眼睛轻轻向前上方看。“低头思故乡”：轻点下巴，两手放胸前，或安静站着。诗里的故乡是家乡；家长可解释：“诗人看到月亮，想起自己的家乡。”孩子愿意时说说想念谁，不要求说。'),
('月字见面与编舞','展示月亮图和“月”字，说：“图里是月亮，这是月字。”妹妹把图放字旁。再选月亮、举头、低头中的两个动作编舞，父母跟随。做圆时不要求手指相碰；全程可坐着用手表示。'),
('荷叶鱼塘的邀请','念诗人说：“小鱼在荷叶间游，我们也来游一游。”材料第3页选小鱼和荷花图；诗在第9页，字在第5页。先念“江南可采莲，莲叶何田田，鱼戏莲叶间”前三句，也可以只玩“鱼戏莲叶间”。'),
('小鱼的动作与意思','两手合拢当小鱼，在胸前轻轻游动；双掌打开当花瓣，或双臂画一个大荷叶。家长解释：“江南可以采莲，荷叶长得很茂盛，小鱼在荷叶之间玩。”原诗中的“采莲”通常指采莲蓬或莲子；开花动作帮助想象荷塘，不解释成摘花。'),
('鱼字与后四句','把鱼图送到“鱼”字旁，孩子指认或让父母摆都可以。喜欢再听东、西、南、北四句，只需每句让小鱼换一个位置；不用考方向。家长保留原诗用字，在动作口令中可说“游到这边、再到那边”。妹妹选两个动作，全家编舞谢幕。')]),
('让汉字跟图画做朋友',[
('每次先见一个字','核心字是“水、月、鱼”，分别在三首诗中出现。三岁的玩法从家长读字、孩子看图开始，不要求独立读出字。动作名里的鹅、莲、停等是给家长看的说明，不作为本轮识字目标。'),
('玩法一 图和字见面','只放同一主题的一张图和一个字，家长读“水”，孩子把波浪图送到字旁，家长也参与摆卡。下一局还是这一个字也可以。这是图、声音和字形的接触，不据此认定已经会认字。'),
('玩法二 两个字找家 可选','孩子熟悉一对之后，最多同时放两个字和两张图，例如水与月。家长边指边读：“这是水，这是月。”妹妹指图，父母一起找对应字；不顺利就恢复一对。三字混排留到孩子主动愿意时，不设计时或对错积分。'),
('玩法三 身体猜字 可选','伴舞做波浪，念诗人指着字说“水”；妹妹可以做相同动作，也可以选月亮或鱼让父母猜。动作帮助记住画面，不当作汉字的笔顺或字形教学。不要把手势解释成真实写字方式。'),
('一二三是数拍扩展','材料第6页一、二、三字卡配一、二、三个圆点，只在孩子想数时加入。先玩“一”：父母读字，全家拍一下；熟悉再玩二和三。它们是本游戏新增的节奏口令，不是这三首古诗的诗句。'),
('先不加入的要求','不安排描红、默写、认完六字或背完三诗的任务。家长自然示范读音，孩子指错时说“我们一起看，这是月亮的月”，然后继续跳。留住想玩的兴趣比多放几张卡更有用。')]),
('父母也要认真玩',[
('孩子做什么 父母跟什么','先让妹妹领舞，两位家长都模仿她选的动作；动作与图不同也可以，请她教一教。下一轮伴舞领一个动作，妹妹可跟、改或观看；念诗人照样参加，不始终站在旁边指挥。'),
('镜子舞 约2分钟','面对面留出空间：妹妹摆一个姿势，父母做同样姿势；换家长摆，妹妹自由回应。只模仿形状，不要求左手右手完全一致。先用一个动作，熟悉再接第二个。'),
('停一停 重新动','展示第1页休息卡或第3页“停一停”动作卡，任何人都可说停。一起站稳或坐下，自然停一两秒，再由妹妹决定继续还是收尾。不是抢停游戏，慢了、动了也不淘汰；不要求憋气或维持姿势。'),
('大波浪 小波浪','伴舞示范舒服的大波浪，念诗人做小波浪，妹妹选喜欢的版本。两位家长交换大小，再按妹妹选的版本一起跳。只改变幅度或速度中的一项；快慢都以孩子能轻松跟上为准。'),
('我们自己编一首舞','妹妹从任意两张动作图中选卡，摆到第10页小舞谱。全家做两个动作，再加妹妹自己的结尾。跨场景编舞时家长用自编口令，例如“小鱼游一游，月亮圆圆的”；把自编口令与古诗原文分开。'),
('记录一句具体发现','第11页可由家长记一句：“她今天让爸爸做小鱼，自己做月亮。”妹妹可以涂一笔。不排名，不用记录背诗数量或动作好坏；照片仅在家里愿意时拍，玩过一次也可以不记录。')]),
('打印索引与主持提醒',[
('材料第1至5页','第1页：三个角色与休息卡。第2页：小鹅、波浪、月亮、举头四张动作图。第3页：低头、小鱼、荷花、停一停四张动作图。第4页：三个场景选择卡。第5页：水、月、鱼的三张图卡与三张字卡。'),
('材料第6至11页','第6页：一、二、三的三张字卡与三张点数卡，可不打印。第7页：《咏鹅》原诗与动作。第8页：《静夜思》原诗与动作。第9页：《江南》原诗与动作。第10页：两格小舞谱。第11页：自创场景、回忆与首局提示。'),
('怎样剪 怎样摆','动作图是大卡，每页四张；字图卡每页六张。大人沿虚线剪，保留整张外框。小舞谱整页保留，两张动作卡刚好放入两个格子。纸卡只放桌上，跳舞区域保持干燥、平整、无散落玩具；不穿容易滑的袜子跳。'),
('姿势以舒服为准','这是模仿和律动游戏，不训练舞蹈基本功。不做劈叉、下腰、脚尖站立、单脚久站或拉扯关节；不拉手把孩子转起来。头部只轻轻抬、轻轻点，举手可改胸前做圆。孩子想坐着就坐着摆手，累了随时休息。'),
('古诗与资料','三首古诗原文完整印给家长，首局只取一两句来玩。《静夜思》采用“床前明月光、举头望明月”的通行本。诗文作者、文本版本与网页来源见套装05_古诗与图画来源.md；动作、台词、卡片与插画另行设计。'),
('可调整的家庭初版','2026年10月12日，亲子版1.0。文件已检查排版，尚未进行实际家庭试玩。妹妹偏爱某首诗，就多玩那一首；觉得识字打断舞蹈，可以先只展示一次字卡。规则允许跳过环节、暂停和提前谢幕。')])]

ROLES=[
('R1','小领舞','妹妹','我选去哪一场舞会。\n我选动作和先后。\n我可以跳、坐着动或看。\n我说停，大家一起休息。'),
('R2','念诗人','一位家长','我慢念一句，让画面出现。\n我读字，让图和字见面。\n我也跟着妹妹跳。\n下一局和伴舞交换。'),
('R3','伴舞','另一位家长','我先跟着妹妹做。\n我再提供一个舒服的动作。\n我腾出空间，陪她休息。\n我参加全家的小舞。'),
('R4','休息一下','谁都可以用','举起手，或指这张卡。\n全家站稳、坐下都可以。\n继续、换动作、收尾都行。\n不淘汰，不扣分。')]
POSES=[
('A1','小鹅','小翅膀晃一晃','双肘轻轻向外弯，手放松。\n可以原地晃，也可慢走两小步。',0),
('A2','波浪','水在轻轻动','双手在身前轻摆波浪。\n坐着摆手，也能参加。',1),
('A3','月亮','做一个松松的圆','双手在头上或胸前做圆。\n不用把指尖碰在一起。',2),
('A4','举头','望一望明月','眼睛轻轻向前上方看。\n不把脖子用力往后仰。',3),
('A5','低头','安静想一想','下巴轻轻点一下。\n也可以低眼睛、不动头。',4),
('A6','小鱼','在荷叶间游一游','两手合拢，在胸前轻摆。\n小鱼游这边，再游那边。',5),
('A7','荷花','花瓣打开啦','双掌在胸前打开，像花瓣。\n也可以双臂画一片大荷叶。',6),
('A8','停一停','站稳或坐下','双掌向前，放松停一小会儿。\n妹妹决定继续还是休息。',7)]
POEMS=[
dict(id='P1',title='咏鹅',author='唐·骆宾王',lines=['鹅，鹅，鹅，','曲项向天歌。','白毛浮绿水，','红掌拨清波。'],focus='水',first='鹅，鹅，鹅；白毛浮绿水。',meaning='白鹅弯着脖子向天叫，白羽毛浮在绿水上，红脚掌拨动清清的水波。',mapping=['鹅，鹅，鹅 → 小翅膀轻晃。','曲项向天歌 → 看前方，学鹅叫或张嘴。','白毛浮绿水 → 双手摆波浪。','红掌拨清波 → 原地慢踏两小步，或用手划水。'],note='动作是亲子模仿，不要求把脖子弯成鹅的形状。先玩两句，喜欢再读全诗。'),
dict(id='P2',title='静夜思',author='唐·李白',lines=['床前明月光，','疑是地上霜。','举头望明月，','低头思故乡。'],focus='月',first='举头望明月；低头思故乡。',meaning='明亮月光洒在床前，诗人疑心像地上的霜。他抬头望月，又低头想起自己的家乡。',mapping=['床前明月光 → 双手做圆，表示月亮。','疑是地上霜 → 手指前方地面，不用蹲。','举头望明月 → 轻看前方上面。','低头思故乡 → 轻点下巴，或两手放胸前。'],note='采用通行本。两句也能开一场舞会；“想念谁”只是可选聊天，不解释为诗人看到爸爸妈妈。'),
dict(id='P3',title='江南',author='汉乐府',lines=['江南可采莲，','莲叶何田田。','鱼戏莲叶间。','鱼戏莲叶东，','鱼戏莲叶西，','鱼戏莲叶南，','鱼戏莲叶北。'],focus='鱼',first='江南可采莲；莲叶何田田；鱼戏莲叶间。',meaning='江南可以采莲，荷叶长得茂盛，鱼儿在荷叶之间游来游去、嬉戏。',mapping=['江南可采莲 → 伸手做采莲的动作。','莲叶何田田 → 双臂画圆，像大荷叶。','鱼戏莲叶间 → 双手当小鱼，在胸前游。','东、西、南、北四句 → 每句换一处游，不考方向。'],note='首轮一至三句即可；后四句可暂不玩。莲是荷，采莲通常采莲蓬或莲子，花瓣图帮助想象荷塘。')]

def register(cid,title,kind,body):
    CARDS.append(dict(id=cid,title=title,kind=kind,body=body))

def border(c,x,y,w,h):
    c.setStrokeColor(LINE);c.setLineWidth(.8);c.setDash(3,3);c.roundRect(x,y,w,h,6);c.setDash()

WINDOWS=[(0,8,512,346),(512,8,1024,346),(0,362,512,729),(512,362,1024,729),
         (0,752,512,1086),(512,752,1024,1086),(0,1101,488,1504),(488,1101,1024,1504)]
def panel(c,index,x,y,w,h):
    left,top,right,bottom=WINDOWS[index];scale=min(w/(right-left),h/(bottom-top))
    px=x+(w-(right-left)*scale)/2;py=y+(h-(bottom-top)*scale)/2
    c.saveState();p=c.beginPath();p.rect(px,py,(right-left)*scale,(bottom-top)*scale);c.clipPath(p,stroke=0)
    c.drawImage(str(ART),px-left*scale,py-(1536-bottom)*scale,width=1024*scale,height=1536*scale,mask='auto')
    c.restoreState()

def icon(c,name,x,y,s):
    c.saveState();c.translate(x,y);c.setStrokeColor(INK);c.setLineWidth(2)
    if name=='水':
        c.setStrokeColor(HexColor('#4D91AB'))
        for yy in [-s*.4,0,s*.4]:
            p=c.beginPath();p.moveTo(-s,yy);p.curveTo(-s*.5,yy+s*.5,-s*.5,yy-s*.5,0,yy);p.curveTo(s*.5,yy+s*.5,s*.5,yy-s*.5,s,yy);c.drawPath(p)
    elif name=='月':
        c.setFillColor(HexColor('#F7D36C'));c.setStrokeColor(HexColor('#AE883D'));c.circle(0,0,s,fill=1)
        c.setFillColor(white);c.setStrokeColor(white);c.circle(s*.5,s*.25,s*.83,fill=1)
    elif name=='鱼':
        c.setFillColor(HexColor('#EFAA65'));c.ellipse(-s*.9,-s*.55,s*.55,s*.55,fill=1)
        p=c.beginPath();p.moveTo(s*.4,0);p.lineTo(s,s*.65);p.lineTo(s,-s*.65);p.close();c.drawPath(p,fill=1)
        c.setFillColor(INK);c.circle(-s*.5,s*.14,s*.07,fill=1)
    c.restoreState()

def text_grid(c,items,n,title):
    base(c,title,n,'打印材料')
    for k,(cid,name,subtitle,body) in enumerate(items):
        x=38+(k%2)*266;y=H-102-(k//2+1)*332-(k//2)*12
        border(c,x,y,253,332);txt(c,cid,x+14,y+311,8,color=ACC)
        txt(c,name,x+14,y+284,19,color=black);txt(c,subtitle,x+14,y+257,10,color=ACC)
        end=txt(c,body,x+14,y+221,12,width=225,leading=22);assert end>y+14,(name,end,y)
        register(cid,name,subtitle,body)
    c.showPage()

def actions(c,start,n):
    base(c,'动作图卡 '+('一' if start==0 else '二'),n,'妹妹看图玩')
    for k,item in enumerate(POSES[start:start+4]):
        cid,name,sub,body,index=item;x=38+(k%2)*266;y=H-102-(k//2+1)*332-(k//2)*12
        border(c,x,y,253,332);txt(c,name,x+14,y+301,20,color=black)
        panel(c,index,x+12,y+107,229,178)
        txt(c,sub,x+14,y+87,11,color=ACC)
        txt(c,body,x+14,y+60,10,width=225,leading=17)
        register(cid,name,'动作图卡',body)
    c.showPage()

def scenes(c):
    base(c,'今天去哪一场舞会',4,'妹妹选图')
    items=[('C1','小鹅池塘',0,'听《咏鹅》，做小鹅和波浪。\n汉字朋友：水。'),('C2','月亮庭院',2,'听《静夜思》，做月亮、举头或低头。\n汉字朋友：月。'),('C3','荷叶鱼塘',5,'听《江南》，做小鱼和荷叶。\n汉字朋友：鱼。')]
    for k,(cid,title,index,body) in enumerate(items):
        x=38;y=H-105-(k+1)*209-k*8
        border(c,x,y,519,209);panel(c,index,x+12,y+22,169,161)
        txt(c,title,x+204,y+160,23,width=285,color=black)
        txt(c,body,x+204,y+115,12,width=285,leading=22)
        txt(c,'妹妹指图，大人读名字。',x+204,y+39,10,color=ACC)
        register(cid,title,'场景卡',body)
    c.showPage()

def matches(c,n,numbers=False):
    base(c,'一二三数拍卡 可选' if numbers else '汉字和图画做朋友',n,'打印材料')
    words=['一','二','三'] if numbers else ['水','月','鱼']
    for row,word in enumerate(words):
        for col in range(2):
            x=38+col*266;y=H-105-(row+1)*217-row*10
            border(c,x,y,253,217)
            is_char=(col==1);kind='字卡' if is_char else ('点数卡' if numbers else '图卡')
            cid=('N' if numbers else 'W')+str(row+1)+('B' if is_char else 'A')
            txt(c,kind,x+14,y+193,9,color=ACC)
            if is_char:txt(c,word,x+(253-90)/2,y+83,90,width=150,color=black)
            elif numbers:
                count=row+1;c.setFillColor(ACC)
                for j in range(count):c.circle(x+126.5+(j-(count-1)/2)*44,y+117,13,fill=1,stroke=0)
            else:icon(c,word,x+126.5,y+116,53)
            txt(c,'大人读字，孩子指、摆或看。' if is_char else ('一起数点，再拍同样次数。' if numbers else '把图送到对应字旁边。'),x+14,y+24,10,width=225)
            register(cid,word,kind,'家长陪同配对；首局只用水的一对。' if not numbers else '可选数拍扩展，不属于诗句原文。')
    c.showPage()

def poem_page(c,poem,n):
    base(c,'古诗舞台  '+poem['title'],n,'家长念给孩子听')
    txt(c,poem['author']+'  /  汉字朋友：'+poem['focus'],38,735,12,color=ACC)
    y=680
    for line in poem['lines']:y=txt(c,line,76,y,25,leading=39)-2
    y-=10
    y=sec(c,'首轮可只玩这些句子',poem['first'],y)
    y=sec(c,'这首诗的画面',poem['meaning'],y)
    y=sec(c,'动作提示', '\n'.join(poem['mapping']),y)
    y=sec(c,'给家长',poem['note'],y)
    register(poem['id'],poem['title'],'古诗原文','\n'.join(poem['lines']))
    c.showPage()

def score(c):
    base(c,'妹妹编的两步小舞',10,'小舞谱 整页保留')
    txt(c,'妹妹选两张动作卡，决定先后，爸爸妈妈一起跟着跳。',38,730,12)
    for k,label in enumerate(['一  先做这个','二  再做这个']):
        x=38+k*266;txt(c,label,x,689,16,color=ACC);border(c,x,336,253,332)
    txt(c,'读一句 → 动一下 → 留一会儿 → 再做下一个',38,290,14,color=black)
    txt(c,'全家做完一轮，妹妹可以换顺序，再跳一次。\n最后摆一个舒服的姿势，挥手谢幕。',38,245,12,leading=23)
    txt(c,'自编口令 _________________________________',38,163,12)
    txt(c,'古诗原文另读；自编口令不写成诗人的句子。',38,128,10,color=ACC)
    txt(c,'卡片留在桌上，舞蹈区域不铺纸卡。',38,85,11)
    c.showPage()

LAST=[
('B1','我们新的舞会','家长填写 孩子选图','舞会名字：________________\n画一个场景：\n\n\n\n想做的动作：______________\n想听的诗句：______________'),
('B2','我们新的舞会','可以只有动作 不加新字','舞会名字：________________\n画一个场景：\n\n\n\n想做的动作：______________\n想听的诗句：______________'),
('M1','今天的小舞会','家长代写 妹妹可涂画','日期：____________________\n她选了：__________________\n她带我们做：______________\n想再玩：__________________\n\n一句具体发现：\n__________________________'),
('Q1','首局速查','小鹅池塘 约8至12分钟','选小鹅或波浪。\n听一句，一起做一下。\n水图送到水字旁。\n妹妹选两卡，父母跟着跳。\n舒服摆姿势，挥手谢幕。\n\n任何环节都能跳过或休息。')]

SOURCES='''# 古诗与图画来源

核对日期：2026年10月12日。古诗原文属于历史作品；本套装没有复制网页的现代鉴赏文章或教材插画。规则、亲子台词和动作编排均为本游戏设计。

## 古诗文本

- 《咏鹅》，唐·骆宾王。青海师范大学文学院“吟诵进课堂”展示作者与完整诗文：https://wxy.qhnu.edu.cn/info/1074/2322.htm
- 《静夜思》，唐·李白。本套装采用通行的“床前明月光”“举头望明月”版本。维基文库收录《唐诗三百首》文本及异文对照：https://zh.wikisource.org/zh-hans/靜夜思
- 《江南》，汉乐府。人民教育出版社页面展示完整文本，注明朗读来源中央人民广播电台：https://m.pep.com.cn/zt/ysywjc/sfsd/1s/201807/t20180704_1926207.shtml

“首轮选句”是从原诗中节选供游戏使用，不替换完整原文。跨场景的自编口令明确标为自编。莲指荷；采莲通常指采莲蓬或莲子，不能把花瓣手势说成原诗要求采花。四个方位在原文里保留，游戏不考核三岁孩子的方向概念。

## 图画与字卡

- 八个动作场景用内置 ImageGen 生成，原图保存在 assets/诗画小舞会动作插画.png。完整提示词与生成说明见06_图画生成说明.md。
- PDF显示原图相应窗口，没有修改图像像素。插画只是动作提示，孩子可采用自己的舒适版本。
- 水、月、鱼图标、圆点、小舞谱和汉字由PDF绘图工具排版。汉字用Windows黑体嵌入，不让生成模型绘制字形。
- 核心识字接触：水、月、鱼。扩展数拍字：一、二、三。动作说明中的其他字由成人读，不作为本轮学习目标。

此为家庭游戏初版，未进行实际家庭试玩；不承诺特定识字或运动发展效果。
'''

def build():
    c=canvas.Canvas(str(OUT/'01_诗画小舞会规则书.pdf'),pagesize=(W,H));c.setTitle('诗画小舞会 3岁亲子规则书');c.setAuthor('家庭游戏设计')
    for i,(title,sections) in enumerate(RULES,1):
        base(c,title,i,'规则书');y=H-108
        for name,body in sections:y=sec(c,name,body,y)
        c.showPage()
    c.save()
    c=canvas.Canvas(str(OUT/'02_诗画小舞会打印材料.pdf'),pagesize=(W,H));c.setTitle('诗画小舞会 动作古诗汉字打印材料');c.setAuthor('家庭游戏设计')
    text_grid(c,ROLES,1,'全家的三个角色与休息卡')
    actions(c,0,2);actions(c,4,3);scenes(c);matches(c,5);matches(c,6,True)
    for n,poem in enumerate(POEMS,7):poem_page(c,poem,n)
    score(c);text_grid(c,LAST,11,'自创舞会与家庭回忆');c.save()
    rule_md=['# 诗画小舞会规则可修改源稿\n\n修改此文字稿不会自动更新PDF。重新生成请修改build_dance.py。\n']
    for title,sections in RULES:
        rule_md.append('\n## '+title+'\n')
        for sub,body in sections:rule_md.append('\n### '+sub+'\n\n'+body+'\n')
    (OUT/'03_规则可修改源稿.md').write_text('\n'.join(rule_md),encoding='utf-8')
    card_md=['# 诗画小舞会卡片可修改源稿\n']
    for item in CARDS:card_md.append('\n## '+item['id']+' '+item['title']+'\n\n'+item['kind']+'\n\n'+item['body']+'\n')
    (OUT/'04_卡片可修改源稿.md').write_text('\n'.join(card_md),encoding='utf-8')
    (OUT/'cards.json').write_text(json.dumps(CARDS,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'05_古诗与图画来源.md').write_text(SOURCES,encoding='utf-8')
    prompt=ROOT/'诗画小舞会图画生成说明.md'
    if prompt.exists():shutil.copy2(prompt,OUT/'06_图画生成说明.md')
    (OUT/'00_开始这里.md').write_text('''# 诗画小舞会 3岁亲子版

妹妹当小领舞，爸爸妈妈分别当念诗人与伴舞，下一局交换。三个人都要跳，孩子可以坐着做动作、指图或观看。

## 第一次小鹅池塘

1. 阅读规则书第2页。
2. 打印材料第1、2、5、7、10页，共五页。A4、实际大小100%、单面。图卡建议彩色。
3. 大人沿虚线剪角色、动作、图和字卡。小舞谱与古诗页整页保留。首局只取第5页水图与水字这一对，其他卡收起。
4. 妹妹选小鹅或波浪；家长念一句，三个人一起做一次。
5. 将水图送到水字旁；不想玩字就展示一次收起。
6. 妹妹把两个动作摆到小舞谱上，父母跟着跳，挥手谢幕。

约8至12分钟，任何环节可跳过；不用背诗、写字或认对字才结束。第二次可仍玩小鹅，也可改月亮庭院；再喜欢才加荷叶鱼塘。

## 文件

- 01_诗画小舞会规则书.pdf：6页，完整规则、首局台词、另外两场舞会、汉字玩法、父母互动与打印索引。
- 02_诗画小舞会打印材料.pdf：11页，8张动作图卡、三场景、字图配对、三首完整古诗、两格小舞谱、角色与空白扩展。
- 03与04：可修改文字源稿。
- 05：古诗作者、文本来源、版本和动作说明。
- 06与assets：内置ImageGen生成提示词与原始插画。
- cards.json：34张卡片的文字数据；小舞谱另在PDF第10页。
- build_dance.py：生成脚本，需Python、reportlab、pypdf、Windows黑体字体。复制整个套装后也可运行。

## 打印材料索引

1角色与休息；2动作一；3动作二；4场景；5水月鱼字图；6一二三数拍（可选）；7咏鹅；8静夜思；9江南；10小舞谱；11自创与回忆。

卡片放桌上，跳舞地面保持干燥、平整、无散落物，不穿易滑袜子。姿势舒服即可，不进行拉伸训练。累了随时休息。

版本：2026年10月12日，家庭初版1.0。PDF已检查排版，尚未实际家庭试玩。
''',encoding='utf-8')
    (OUT/'build_dance.py').write_text(Path(__file__).read_text(encoding='utf-8'),encoding='utf-8')
    for name,count in [('01_诗画小舞会规则书.pdf',6),('02_诗画小舞会打印材料.pdf',11)]:
        r=PdfReader(OUT/name);assert len(r.pages)==count;assert all(p.extract_text() for p in r.pages)
    assert len(CARDS)==len({x['id'] for x in CARDS})==34
    print('Validated 6 rule pages, 11 material pages, 34 unique cards')

if __name__=='__main__':build()
