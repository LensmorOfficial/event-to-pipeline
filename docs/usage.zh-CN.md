# 安装与使用

Skills 负责研究步骤，现有 Lensmor MCP 提供数据，AI 客户端执行任务。先看[完整案例](../examples/README.md)即可了解结果形式，无需运行程序。

## 安装一次

在仓库目录中打开终端，使用 Python 3.11+，选择另一个项目作为业务工作区：

```bash
python scripts/install_mcp_skills.py --destination ../my-event-project/.agents/skills --dry-run
python scripts/install_mcp_skills.py --destination ../my-event-project/.agents/skills
```

第一条预览，第二条安装 **6 个研究 Skills + `booth-invitation-writer`**，附带完整资源和许可证。无需安装 pip 包；发现同名目录时停止，保留已有文件。

`.agents/skills` 适用于支持这一发现目录的客户端。随后按 [MCP 接入说明](../integrations/mcp/README.md)合并配置、完成认证，并在业务工作区确认 Skills 和 Lensmor 工具均可用。已有连接时核对工具即可。文件安装成功不代表账号已经获得数据访问权。

## 从你当前的任务开始

| 任务 | 主要 Skill | 需要你提供 |
| --- | --- | --- |
| 选展会 | `event-fit-scorer` | 产品、客户画像、地区与时间 |
| 筛公司 | `event-account-prioritizer` | 展会届次、完整能力条件、数量 |
| 找联系人 | `event-buying-committee-mapper` | 已选公司、目标职能和职位要求 |
| 写邀约 | `booth-invitation-writer` | 选中的对象、发件人及产品真实信息、行动目标 |

例如，先发送：

```text
请使用 event-account-prioritizer，在 MEDICA 2026 中研究最多 10 家
提供外科机器人系统的公司。先确认展会届次，完整保留能力要求。
返回公司、官网与匹配证据，把符合条件和证据不足的候选分开。
只使用账号现有权益。
```

确认公司后再指定联系人角色；选择收件人、补充发件人资料后，让 `booth-invitation-writer` 写草稿供审阅。需要保存最终名单时，让具备文件能力的客户端生成与表格一致的 CSV。

## 开发者直接导出 CSV

仓库根目录执行以下命令可试跑两页虚构数据，无需账号：

```bash
python scripts/export_exhibitors.py --sample examples/exhibitor-export/sample.json --max-pages 2 --output exhibitors.csv
```

查询真实展商时，在环境中设置 `LENSMOR_API_KEY`，把 `EVENT_ID` 换成已确认届次的 ID：

```bash
python scripts/export_exhibitors.py --event-id EVENT_ID --country Germany --max-pages 3 --output live-exhibitors.csv
```

同一脚本也安装在 `research-exhibitors/scripts/` 下，AI 可按需调用。MCP 认证与 REST API key 分开配置。CSV 是指定条件下的展商记录；另附 `.metadata.json` 说明页数、访问范围、去重和完整性。预览结果不会被当成完整名单。详见[参数与结果说明](exhibitor-export.md)。

现有 [Lensmor Agent](use-lensmor-agent.md) 使用线上版本与产品权限，本地安装不会更新线上产品。候选包的验证范围见[验证记录](verification.md)。
