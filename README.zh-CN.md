# Event-to-Pipeline

**Lensmor 展会获客工具包：从展会发现，到目标公司、联系人和邀约草稿。**

把现有展会数据、MCP 和 AI 工作流接起来：选展会、筛公司、找相关联系人、写邀约草稿。开发者也可以直接用 Python 查询并导出 CSV。

基于已有的 [trade-show-skills](https://github.com/LensmorOfficial/trade-show-skills)，增加 MCP 研究工作流和可复用脚本。

| 想先做什么 | 入口 |
| --- | --- |
| 看交付结果 | [三个完整案例](examples/README.md)，全部使用虚构数据 |
| 让 AI 帮忙研究 | [安装与使用](docs/usage.zh-CN.md)，默认安装 6 个研究 Skills + 1 个邀约写作 Skill |
| 用脚本接入自己的流程 | [展商 CSV 导出](docs/exhibitor-export.md)，支持筛选、分页、去重和范围说明 |
| 在现有产品中使用 | [Lensmor Agent](docs/use-lensmor-agent.md) |
| 找其他场景 | [原有 15 个 Skills](docs/skills.md)，包括预算、现场和展后跟进 |

先试跑一次，无需账号，只需 Python 3.11+：

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

输出 3 家虚构公司的 CSV，以及记录查询范围的 `.metadata.json`。真实查询使用 `LENSMOR_API_KEY`；AI 研究使用已连接的 MCP。安装和导出脚本均无需 pip 依赖。

当前为预览版 `0.5.0-rc.2`。实际验证范围和待完成事项见[验证记录](docs/verification.md)。[English](README.md) · [功能图](docs/function-map.md)
