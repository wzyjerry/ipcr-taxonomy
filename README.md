# 解析第8版IPC分类体系（v.20060101）

+ [IPC技术支持](https://www.wipo.int/classifications/ipc/en/ITsupport/)
+ [IPC分类数据集](https://www.wipo.int/classifications/ipc/en/ITsupport/Categorization/dataset/index.html)

+ gen_md:
    + **将data/ipcr_scheme_20060101.7z解压至data/ipcr_scheme_20060101.xml**
    + 解析ipcr_scheme_20060101.xml，在data/md下生成A~H.md
    + 结构化结果可以从字典ipcr中获取
    + 字段含义参考output_md

+ International Patent Classification Eighth Edition (2006) Core Level
    1. [SECTION A — HUMAN NECESSITIES](/data/md/A.md)
    2. [SECTION B — PERFORMING OPERATIONS; TRANSPORTING](/data/md/B.md)
    3. [SECTION C — CHEMISTRY; METALLURGY](/data/md/C.md)
    4. [SECTION D — TEXTILES; PAPER](/data/md/D.md)
    5. [SECTION E — FIXED CONSTRUCTIONS](/data/md/E.md)
    6. [SECTION F — MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING](/data/md/F.md)
    7. [SECTION G — PHYSICS](/data/md/G.md)
    8. [SECTION H — ELECTRICITY](/data/md/H.md)

已知BUG:
- output_md中当subclass包含多个括号或括号后还有内容时，加粗显示错误，只会加粗第一括号前的内容
