from pathlib import Path
import shutil, math
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import ImageReader

BIO=[
('S1','细胞证件核对','小熊来访时 推荐第一次','看材料第14页，标出动物细胞1至4。\n说出两种细胞的共同结构，再找出植物图特有的结构。\n妹妹：指小熊来访图，请它进诊室。\n完成：哥哥说对共性与至少两处差异。','熊'),
('S2','显微镜图像侦探','任意病例 可纸上完成','看第16页。目镜10倍，物镜4倍：总倍数多少？换40倍物镜呢？\n左下图像想移到中央，玻片往哪移？\n妹妹：拿观察镜看玩偶。\n完成：算出两次倍数并解释移动。','镜子'),
('S3','细胞怎样变多','小兔来访时','假设一个细胞分裂，每轮所有细胞各分裂一次。用大纸片摆出三轮。\n辨别“数量增多”与“出现不同类型”。\n妹妹：把玩偶送到纸床。\n完成：摆对数量，区分分裂与分化。','兔'),
('S4','一个细胞也能生活','任意病例','第15页有草履虫观察资料。它由几个细胞组成？能独立完成哪些生命活动？\n比较它与真实兔子的细胞数量。\n妹妹：给草履虫图找个位置。\n完成：说清单细胞不等于细胞器。','星贴'),
('S5','机器人身份核对','机器人来访时','把第15页六张卡分成生物和非生物。卡片代表其说明中的对象。\n解释：会移动足以证明是生物吗？\n妹妹：指机器人来访图，再听诊。\n完成：分类有依据，辨清玩具与活物。','机器人'),
('S6','身体里的层次','任意病例','用纸写细胞、组织、器官、系统、生物体，排出动物结构层次。\n再排绿色开花植物，哪个层次不放？叶是什么层次？\n妹妹：选故事主题。\n完成：顺序正确，说明叶是器官。','故事')]

EXTRA_RULES=[
('哥哥的生物任务怎么融入',[
('苏教版的主题安排','按你们使用苏教版的情况，把游戏重点放在细胞结构、显微观察、细胞分裂与分化、单细胞生物和多细胞结构层次。初版按这些知识主题设计，不固定教材页码；以哥哥手中的课本章节与课堂进度为准。已学内容作为复习，未学内容可先跳过。'),
('一次只加一张','每局最多选一张S1至S6生物任务，原A1至A6逻辑挑战可在另一局玩。生物任务约3至5分钟，放在接待和检查期间。哥哥可以查课本，解释不清时共同核对；妹妹不等待答案才能继续检查。每个病例送别前，哥哥回到协作照顾环节。'),
('推荐的三次开诊','第1次小熊搭配S1：哥哥核对真实动物的细胞图，妹妹接待小熊并听诊。第2次小兔搭配S3：哥哥摆细胞分裂模型，妹妹给小兔铺床。第3次机器人搭配S5：哥哥分辨生物与机器，妹妹给机器人做童话检查。身份区别是在现实知识里讨论，不取消机器人在故事中的就诊。'),
('图画给妹妹 科学图给哥哥','材料第17页是小医生和三位来访者，第18页是拥抱、故事、音乐、星贴的动作图。妹妹指图做决定，大人读台词。哥哥的第14页细胞图用简化结构与编号表示，第16页用于倒像与放大倍数练习；它们都是示意图，不是显微照片。'),
('首局打印建议','材料第1、3、6、8、10、13、14、17、18页，共九页，足够玩小熊和S1。图画卡可用第18页代替第6页供妹妹选择，第6页留给大人读步骤。彩色打印更直观；不能彩打时图案轮廓也可辨认。'),
('故事和知识分别确认','勇气星、笑声瓶和星光灯都是童话。哥哥的生物结论按证据和课本核对；拥抱、音乐、故事不能当作真实疾病的诊疗方案。工具选择谜题表达玩偶的偏好，不把偏好称为生物诊断。')]),
('生物任务答案与资料',[
('S1 细胞结构','动物图：1细胞膜，2细胞核，3细胞质，4线粒体。植物图：A细胞壁，B细胞膜，C细胞核，D液泡，E叶绿体，F线粒体，G细胞质。共同结构包括细胞膜、细胞质、细胞核、线粒体。植物图另有细胞壁、大液泡、叶绿体。所画为含叶绿体的绿色叶肉细胞；不能说所有植物细胞都有叶绿体。'),
('S2与S3 观察和数量','S2：10×4=40倍，10×40=400倍；玻片往左下移动，倒像向右上移动到中央。这个问题只模拟图像方向，不要求操作真实显微镜。S3：第0至3轮为1、2、4、8个；分裂使数量增多，分化使细胞在形态、结构和功能等方面产生差异，形成不同组织。纸片只是数量模型。'),
('S4与S5 生物判断','S4：草履虫是单细胞生物，一个细胞可以独立完成获取营养、呼吸、排出废物等生命活动；真实兔子是多细胞动物。S5：资料卡中活兔、活盆栽、草履虫是生物，玩具机器人、石头、纸画兔子是非生物。会动不能单独证明有生命，不会主动移动也不能排除植物。'),
('S6 结构层次','动物：细胞→组织→器官→系统→生物体。绿色开花植物：细胞→组织→器官→植物体。叶属于器官，含有不同组织。妹妹不用记术语，听懂一句解释或选图即可。'),
('知识核对与课本对照','核对参考：教育部《义务教育生物学课程标准（2022年版）》“生物体的结构层次”主题及显微观察活动；细胞结构与分裂另核对OpenStax Biology 2e第4.3与10.2节。游戏、题目与示意图为原创，不复制教材图片。完整链接和核对记录在套装的05_生物主题与来源.md。'),
('新版打印材料索引','原第1至12页保留。第13页：6张生物任务。第14页：动植物细胞示意图。第15页：6张生物身份资料。第16页：显微镜倒像和放大倍数。第17页：4张医生与来访者图画。第18页：4张照顾动作图画。规则书10页＋材料18页，共28页，家庭版1.1。')])]

def upgrade(g):
    root=g['ROOT'];out=root if root.name=='玩偶小医院苏教生物图画版' else root/'玩偶小医院苏教生物图画版'
    out.mkdir(exist_ok=True);g['OUT']=out
    art_source=root/'医院图画素材.png'
    if not art_source.exists():art_source=root/'assets'/'医院图画素材.png'
    (out/'assets').mkdir(exist_ok=True)
    dest=out/'assets'/'医院图画素材.png'
    if art_source.resolve()!=dest.resolve():shutil.copy2(art_source,dest)
    g['ART']=dest
    # Update the original scope and print index without losing the basic game.
    g['RULES'][0][1][3]=('套装与家里材料','规则书10页，材料册18页。原有角色、病例、照顾工具和逻辑挑战，加6张初一生物任务、细胞与显微观察图、身份资料及8张妹妹图画卡。家里准备1至3个玩偶、一条小毛巾、一张纸、胶带和大纸片。无需买医生玩具。')
    g['RULES'][0][1][4]=('第一次怎么玩','选小熊，打印材料第1、3、6、8、10、13、14、17、18页，共九页。读规则书第2页开诊，再加S1细胞任务。每局只加一个生物任务。全套28页，A4、100%、单面；妹妹图卡建议彩色打印。')
    g['RULES'][7][1][2]=('首次最少打印','纯故事局：材料第1、3、6、8、10页，共五页。想加生物和妹妹大图，再印第13、14、17、18页。规则书可在屏幕上读。四种工具要齐全，才能让哥哥按两条线索排除。')
    g['RULES'].extend(EXTRA_RULES)

def panel(g,c,index,x,y,w,h):
    # Clip a window of the original illustration sheet during PDF layout.
    # The image itself remains unchanged in assets.
    # Actual whitespace gutters differ slightly from equal-height grid rows.
    windows=[(0,0,512,368),(512,0,1024,368),
             (0,376,512,732),(512,376,1024,732),
             (0,738,500,1103),(500,738,1024,1103),
             (0,1110,500,1503),(500,1108,1024,1503)]
    left,top,right,bottom=windows[index]
    scale=min(w/(right-left),h/(bottom-top))
    px=x+(w-(right-left)*scale)/2
    py=y+(h-(bottom-top)*scale)/2
    c.saveState();p=c.beginPath();p.rect(x,y,w,h);c.clipPath(p,stroke=0)
    # Clip precisely to the selected scene, retaining the original raster.
    p=c.beginPath();p.rect(px,py,(right-left)*scale,(bottom-top)*scale);c.clipPath(p,stroke=0)
    c.drawImage(str(g['ART']),px-left*scale,py-(1536-bottom)*scale,width=1024*scale,height=1536*scale,mask='auto')
    c.restoreState()

def cell_page(g,c):
    txt,base=g['txt'],g['base'];W,H=g['W'],g['H'];base(c,'细胞观察证件',14,'哥哥的生物材料')
    txt(c,'简化结构图  不按真实比例  用S1核对编号  答案在规则书第10页',38,H-107,10)
    # Animal cell.
    txt(c,'动物细胞示意图',38,698,16,color=black)
    c.setFillColor(HexColor('#FFF0DA'));c.setStrokeColor(HexColor('#537E92'));c.setLineWidth(2);c.ellipse(91,474,405,650,fill=1)
    c.setFillColor(HexColor('#BEADD7'));c.circle(224,568,32,fill=1)
    for x,y in [(320,565),(169,517)]:
        c.setFillColor(HexColor('#E8AE82'));c.ellipse(x-19,y-9,x+19,y+9,fill=1);c.setStrokeColor(HexColor('#8F6144'));c.lines([(x-10,y-5,x-5,y+5),(x,y-5,x+5,y+5)])
    def call(label,tx,ty,px,py):
        c.setStrokeColor(g['ACC']);c.setLineWidth(.8);c.line(tx+12,ty-2,px,py);txt(c,label,tx,ty,14,width=80,color=g['ACC'])
    call('1',425,627,388,602);call('2',38,604,193,577);call('3',38,553,145,550);call('4',38,492,169,517)
    txt(c,'绿色叶肉细胞示意图',38,425,16,color=black)
    c.setStrokeColor(HexColor('#779661'));c.setFillColor(HexColor('#D4EAC5'));c.setLineWidth(5);c.roundRect(92,173,310,209,15,fill=1)
    c.setStrokeColor(HexColor('#527D87'));c.setFillColor(HexColor('#F5F5DB'));c.setLineWidth(1.5);c.roundRect(101,182,292,191,10,fill=1)
    c.setStrokeColor(HexColor('#7AB2C2'));c.setFillColor(HexColor('#D7EDF2'));c.roundRect(183,215,175,128,22,fill=1)
    c.setStrokeColor(HexColor('#8D73A9'));c.setFillColor(HexColor('#BEADD7'));c.circle(140,278,22,fill=1)
    c.setStrokeColor(HexColor('#65924D'));c.setFillColor(HexColor('#A8CD80'))
    for x,y in [(135,341),(264,360),(369,302)]:c.ellipse(x-15,y-7,x+15,y+7,fill=1)
    c.setStrokeColor(HexColor('#8F6144'));c.setFillColor(HexColor('#E8AE82'));c.ellipse(133,195,163,209,fill=1);c.line(138,198,149,206)
    for label,tx,ty,px,py in [('A',425,385,393,378),('B',425,355,393,351),('C',38,282,118,278),('D',425,287,349,280),('E',425,321,372,301),('F',425,219,151,203),('G',425,253,380,247)]:call(label,tx,ty,px,py)
    txt(c,'图上颜色只帮助辨认，不能用颜色或外形单独判断细胞种类。',38,122,10)
    txt(c,'此植物图含叶绿体；洋葱鳞片叶内表皮等细胞通常没有叶绿体。',38,100,10)
    c.showPage()

def specimens(g,c):
    # Data cards, not microscopic images; sufficient evidence is printed.
    items=[
    ('D1','真实兔子','资料卡代表活着的兔子','有细胞，会摄取营养、呼吸和排出废物，能生长繁殖。\n分类时看资料，不把纸卡本身当活物。','兔'),
    ('D2','活盆栽','资料卡代表活着的植物','有细胞，会生长，需要水和适宜环境。它不主动走路，仍有生命活动。','盆栽'),
    ('D3','草履虫','显微观察资料','整个个体由一个细胞组成，能获取营养、呼吸、排出废物并繁殖。\n图形为示意，不是显微照片。','草履虫'),
    ('D4','玩具机器人','电池驱动的玩具','能发声和移动，靠电池与程序工作；由电子元件等构成，没有由细胞组成的生命结构。','机器人'),
    ('D5','石头','普通石块','由矿物等构成，不以细胞构成生命体，不进行生物的营养、呼吸和繁殖等活动。','石头'),
    ('D6','纸画兔子','纸上的图案','画的是兔子，图案本身不进行生命活动。纸来自植物，也不等于这幅画是活着的兔子。','纸画兔子')]
    g['grid'](c,items,3,15,'六张身份资料卡')
    # grid appends these too; final count is adjusted by finalize checks.

def microscope(g,c):
    txt,base=g['txt'],g['base'];base(c,'显微图像侦探',16,'哥哥的生物材料')
    txt(c,'这是纸上练习，不要求准备或操作真实显微镜。',38,735,11)
    txt(c,'任务一 计算总放大倍数',38,687,16,color=black)
    for x,eyep,obj,label in [(145,10,4,'低倍'),(426,10,40,'换物镜')]:
        c.setStrokeColor(g['INK']);c.setLineWidth(3);c.line(x-33,583,x+12,626);c.line(x+12,626,x+30,614);c.line(x+30,614,x-12,563);c.line(x-12,563,x-33,583);c.line(x+29,568,x+43,493);c.line(x+43,493,x-55,493);c.line(x-47,540,x+26,540)
        txt(c,f'目镜 {eyep}×  物镜 {obj}×',x-85,465,11,width=220)
        txt(c,label+'总倍数 ________',x-85,441,11,width=220)
    txt(c,'任务二 把图像移到中央',38,390,16,color=black)
    c.setStrokeColor(g['INK']);c.setLineWidth(2);c.circle(196,247,93);c.setFillColor(g['ACC']);c.circle(162,211,8,fill=1);c.setDash(2,3);c.line(196,154,196,340);c.line(103,247,289,247);c.setDash()
    txt(c,'视野中的图像在左下',98,128,11,width=240)
    txt(c,'玻片移动方向',338,307,13,width=210)
    txt(c,'左上 / 右上 / 左下 / 右下',338,270,11,width=210)
    txt(c,'圈一个，并解释图像\n为什么向相反方向移动。',338,228,11,width=210)
    txt(c,'答案留给家长核对：规则书第10页。',38,79,11)
    c.showPage()

def picture_cards(g,c,start,indices,labels,captions):
    txt,base=g['txt'],g['base'];base(c,'医生和来访者图画卡' if start==17 else '妹妹的照顾动作图卡',start,'妹妹看图玩')
    for k,index in enumerate(indices):
        x=38+(k%2)*266;y=g['H']-102-(k//2+1)*332-(k//2)*12
        c.setStrokeColor(g['LINE']);c.setDash(3,3);c.roundRect(x,y,253,332,6);c.setDash()
        txt(c,labels[k],x+14,y+299,19,color=black)
        panel(g,c,index,x+12,y+95,229,171.75)
        txt(c,captions[k],x+14,y+56,12,width=225,leading=19)
    c.showPage()

def append_materials(g,c):
    g['grid'](c,BIO,3,13,'哥哥的六个生物任务')
    cell_page(g,c);specimens(g,c);microscope(g,c)
    picture_cards(g,c,17,[0,1,2,3],['小医生','小熊来啦','小兔来啦','机器人来啦'],['请进，我来听一听。','勇气星躲起来了。','笑声瓶空了。','星光灯暗了。'])
    picture_cards(g,c,18,[4,5,6,7],['抱一抱','讲故事','拍一拍','贴星星'],['抱玩偶，或盖上毛巾。','我选主题，哥哥讲故事。','我先拍，大家跟着拍。','我选星星放在哪里。'])

def finalize(g):
    out=g['OUT'];root=g['ROOT']
    source='''# 生物主题与来源

本套装针对家长确认的苏教版初一生物使用情况设计，以知识主题对照，不声称与某一印次页码逐页一致。苏教版和苏科版是不同版本，本套装不将二者混用。第一次由哥哥在自己的课本中找到对应章节，已学就玩，未学可暂时跳过。

## 主题对应

| 游戏任务 | 课本中查找的主题 | 哥哥的活动 |
|---|---|---|
| S1 细胞证件 | 动物细胞、植物细胞的结构与功能 | 识图、比较共性与差异 |
| S2 显微图像 | 生物学实验室、显微镜 | 计算倍数、推理倒像方向 |
| S3 细胞变多 | 细胞的分裂与分化 | 摆数量模型、区分两个概念 |
| S4 一个细胞 | 单细胞生物 | 从资料中说明单细胞独立生活 |
| S5 机器人身份 | 生物与非生物、细胞与生命特征 | 用资料证据分类 |
| S6 身体层次 | 多细胞生物、生物体的组成 | 排层次、比较动植物 |

每局只选一张，不把六张全部变成必做测验。哥哥的生物任务可以查课本，不阻挡妹妹的医生流程。

## 科学内容核对

- 教育部《义务教育生物学课程标准（2022年版）》：生物体的结构层次与显微观察活动。https://www.moe.gov.cn/srcsite/A26/s8001/202204/W020220420582359998122.pdf
- 课程教材研究所课程标准下载入口：https://www.ictr.edu.cn/download_center/ywjy.html
- 教育部2024年教学用书目录：列出江苏凤凰教育出版社生物学与江苏凤凰科学技术出版社生物学为不同教材。https://hudong.moe.gov.cn/srcsite/A26/s8001/202408/W020250418502592948423.pdf
- OpenStax Biology 2e 4.3 Eukaryotic Cells：核对膜、核、细胞质、线粒体以及植物细胞结构差异。https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells
- OpenStax Biology 2e 10.2 The Cell Cycle：核对细胞分裂的基本过程。https://openstax.org/books/biology-2e/pages/10-2-the-cell-cycle

核对日期：2026年10月11日。没有复制教材图、课文或题目。图和任务均自行编排。生物事实与童话偏好谜题分别核对。

## 图画说明

妹妹的大图卡使用内置ImageGen生成的原创童话插画。原图保存在assets/医院图画素材.png；提示词在06_图画生成说明.md。卡片在PDF排版时取原图对应窗口，原图未修改。科学示意图使用确定性矢量绘制，不由插画推断真实结构。
'''
    (out/'05_生物主题与来源.md').write_text(source,encoding='utf-8')
    prompt=root/'医院图画生成说明.md'
    if prompt.exists():shutil.copy2(prompt,out/'06_图画生成说明.md')
    if (root/'hospital_biology.py').resolve()!=(out/'hospital_biology.py').resolve():shutil.copy2(root/'hospital_biology.py',out/'hospital_biology.py')
    (out/'00_开始这里.md').write_text('''# 玩偶小医院 苏教生物与图画版

妹妹当医生看图就诊，哥哥完成初一生物任务并参与照顾，爸爸妈妈轮流陪诊。

## 第一次小熊开诊

先读规则书第2页。材料册打印第1、3、6、8、10、13、14、17、18页，共九页。
准备一个玩偶、小毛巾、纸和胶带。哥哥选S1细胞证件任务；妹妹用第17、18页图画卡指选。
家长拿线索卡，哥哥排除两种不想用的工具；妹妹从两个可用办法中选一个，全家完成照顾表演。
生物任务约3至5分钟，不让妹妹等哥哥答完才继续检查。

## 文件

- 01_玩偶小医院规则书.pdf：10页，规则、主持答案与生物答案。
- 02_玩偶小医院打印材料.pdf：18页，完整卡片、科学图与妹妹图画。
- 03、04：可复制到Word修改的文字源稿。
- 05：生物主题、教材对照与核对来源。
- 06：ImageGen图画提示词与生成方式。
- assets/医院图画素材.png：原始插画，完整保留。
- build_hospital.py与hospital_biology.py：生成脚本，需Python、reportlab、pypdf、Windows黑体。
- cards.json：44张文字卡的结构化数据。

## 打印和试玩

A4，实际大小100%，单面，妹妹图卡建议彩色。沿虚线剪；工作台和记录不剪。道具保留大外框。
全套28页。妹妹不需要识字或记生物术语；哥哥每局只加一张生物任务。
此套装尚未进行真实家庭试玩，按你们兴趣调整。纸道具和童话照顾只用于玩偶。
''',encoding='utf-8')
