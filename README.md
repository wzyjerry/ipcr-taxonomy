# 解析第8版IPC分类体系（v.20060101）

+ [IPC技术支持](https://www.wipo.int/classifications/ipc/en/ITsupport/)
+ [IPC分类数据集](https://www.wipo.int/classifications/ipc/en/ITsupport/Categorization/dataset/index.html)

gen_md:
    解析ipcr_scheme_20060101.xml，在data/md下生成A~H.md
    结构化结果可以从字典ipcr中获取
    字段含义参考output_md


+ [SECTION A — HUMAN NECESSITIES](/data/md/A.md)
+ [SECTION B — PERFORMING OPERATIONS; TRANSPORTING](/data/md/B.md)
+ [SECTION C — CHEMISTRY; METALLURGY](/data/md/C.md)
+ [SECTION D — TEXTILES; PAPER](/data/md/D.md)
+ [SECTION E — FIXED CONSTRUCTIONS](/data/md/E.md)
+ [SECTION F — MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING](/data/md/F.md)
+ [SECTION G — PHYSICS](/data/md/G.md)
+ [SECTION H — ELECTRICITY](/data/md/H.md)

已知BUG:
- output_md中当subclass包含多个括号或括号后还有内容时，加粗显示错误，只会加粗第一括号前的内容
