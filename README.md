# 儿童游戏

持续积累的家庭儿童游戏资料库。每款游戏独立保存规则、打印材料、可修改源稿、插画和生成脚本，今后新增游戏都放在这个仓库。

## 游戏总目录

| 游戏 | 一起玩的人 | 内容 | 完整套装 |
|---|---|---|---|
| [玩偶小医院·苏教生物与图画版](games/001-puppet-hospital/README.md) | 3岁妹妹、初一哥哥与父母 | 角色扮演、家庭合作、初一生物 | [ZIP](downloads/001-puppet-hospital/玩偶小医院苏教生物图画版.zip?raw=true) |
| [诗画小舞会](games/002-poetry-dance/README.md) | 3岁女孩与父母 | 舞蹈动作、古诗、汉字、亲子合作 | [ZIP](downloads/002-poetry-dance/诗画小舞会亲子套装.zip?raw=true) |

点击游戏名称查看首局打印页码和玩法；下载ZIP后打开其中的“开始这里”。直接使用PDF，无需运行代码。

## 目录结构

```text
children-games/
├── README.md                  游戏总目录与入口
├── catalog.json               游戏清单：编号、版本、适用对象、下载路径
├── games/
│   ├── 001-puppet-hospital/    玩偶小医院
│   ├── 002-poetry-dance/       诗画小舞会
│   └── 003-游戏短名/           以后新增的游戏
│       ├── README.md          这款游戏的玩法入口与首局打印页码
│       ├── game.json          版本、对象、材料与生成配置
│       ├── printable/         规则书.pdf、打印材料.pdf
│       ├── editable/          规则源稿、卡片源稿、cards.json
│       ├── assets/            图片原稿
│       ├── src/               生成脚本
│       └── references/        资料来源、图画提示词
├── downloads/                 按游戏编号保存的完整ZIP
├── docs/
│   ├── 新增游戏规范.md        后续统一按这个结构添加
│   └── templates/            游戏信息与说明模板
├── scripts/
│   ├── build_game.py          重新生成一款游戏的PDF与源稿
│   ├── package_game.py        更新对应完整ZIP
│   └── check_library.py       检查目录、页码、卡片编号和下载包
├── requirements.txt          PDF生成依赖
├── SHA256SUMS.txt             文件完整性清单
└── AGENTS.md                  本仓库后续维护约定
```

游戏目录使用稳定编号和短名，版本记在`game.json`中；更新同一款游戏时沿用原目录。第三款从`003-...`开始，不必新建仓库。

## 第一次建议

- **玩偶小医院**：小熊＋S1细胞证件。规则书第2页；材料第1、3、6、8、10、13、14、17、18页，共九页。
- **诗画小舞会**：小鹅池塘。规则书第2页；材料第1、2、5、7、10页，共五页，只拿水图与水字这一对。

A4、实际大小100%、单面打印，图卡建议彩色。孩子可以指图、坐着做动作或观看，任何环节都能跳过、休息或提前结束。两套PDF已核对排版，尚未实际家庭试玩。

## 修改、生成与新增

先安装依赖，然后在仓库根目录执行：

```powershell
python -m pip install -r requirements.txt
python scripts/build_game.py 001-puppet-hospital
python scripts/build_game.py 002-poetry-dance
python scripts/package_game.py 001-puppet-hospital
python scripts/check_library.py
```

当前生成器使用Windows黑体`C:\Windows\Fonts\simhei.ttf`；其他系统需替换源脚本中的字体路径。改Markdown不会自动更新PDF；需修改对应生成脚本。更新后渲染检查PDF，再更新ZIP及目录中的版本信息。

新增游戏见[新增游戏规范](docs/新增游戏规范.md)。古诗、生物核对资料和内置ImageGen生成提示词保留在每款游戏的`references/`目录中，插画为虚构人物。

整理日期：2026年10月12日。
