# Event-to-Pipeline

**发现合适的展会，研究目标公司和联系人，并根据证据准备邀约草稿。**

Lensmor 面向开发者的展会获客工具包，包含 7 个 AI Skills、MCP 接入配置和可复用的 Python 脚本。可以让智能体完成研究，也可以直接用脚本导出展商数据。

[English](README.md) · [三个完整案例](examples/README.md) · [MCP 配置](integrations/mcp/README.md) · [CSV 导出说明](docs/exhibitor-export.md)

## 能做什么

| 任务 | 使用的 Skills | 输出 |
| --- | --- | --- |
| 找展会、比较展会 | `research-events`、`event-fit-scorer` | 展会对比、依据和待确认信息 |
| 筛选目标公司 | `research-exhibitors`、`event-account-prioritizer` | 公司名单、匹配证据和筛选理由 |
| 找相关联系人 | `research-people`、`event-buying-committee-mapper` | 联系人、实际角色和证据缺口 |
| 准备邀约 | `booth-invitation-writer` | 供你审核的个性化草稿 |

示例使用虚构数据，无需账号。真实研究使用已有的 Lensmor 访问权限。希望直接在产品中操作，可以使用 [Lensmor Agent](docs/use-lensmor-agent.md)。

## 快速开始

需要 **Python 3.11 或更高版本**。安装脚本无需额外的 pip 依赖：

```bash
git clone https://github.com/LensmorOfficial/event-to-pipeline.git
cd event-to-pipeline
python scripts/install_skills.py --destination ../my-project/.agents/skills --dry-run
python scripts/install_skills.py --destination ../my-project/.agents/skills
```

默认安装全部 7 个 Skills，并复制配套资源和许可证；已有的同名 Skill 不会被覆盖。请按客户端支持的位置调整安装目录，再根据 [MCP 连接指南](integrations/mcp/README.md)配置和认证。

连接后可以尝试：

```text
使用 event-account-prioritizer，研究 MEDICA 2026 上最多 10 家
外科手术机器人供应商。完整保留这一能力要求，将已确认符合要求的公司
与仍需补充证据的候选公司分开列出，仅使用现有访问权限。
```

## 用 Python 导出展商

先离线试跑，无需账号：

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

脚本输出 3 家虚构公司的 CSV，以及说明查询范围和完整性的 `.metadata.json`。真实查询需要在环境变量中设置 `LENSMOR_API_KEY`：

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --country Germany --max-pages 3 --output live-exhibitors.csv
```

将 `EVENT_ID` 替换为已确认的展会 ID。脚本支持筛选、有限分页和按公司 ID 去重，达到访问或预览上限时停止。MCP 登录与 REST API 密钥分别配置。[查看详细参数](docs/exhibitor-export.md)。

## 项目结构与状态

```text
event-to-pipeline/
├── skills/          # 7 个可独立安装的核心 Skills
├── scripts/         # 安装、导出、验证和打包脚本
├── integrations/    # MCP 配置与研究技能来源记录
├── examples/        # 三个完整案例和离线导出样例
├── docs/            # 使用参考、贡献指南和更新日志
├── tests/           # 功能、安装和发布包测试
├── .github/         # 自动检查与贡献模板
└── project.json     # 项目版本和技能目录
```

本仓库独立维护自己的功能范围、安装流程和发布包。当前为预览版 **0.6.0**；实际验证范围和待完成事项见[验证记录](docs/verification.md)。邀约只生成草稿，需要审核后再发送。

[贡献指南](docs/CONTRIBUTING.md) · [更新日志](docs/CHANGELOG.md) · [许可证与来源说明](NOTICE.md)
