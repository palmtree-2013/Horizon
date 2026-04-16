---
layout: default
title: Source Presets
---

# Horizon

<div id="lang-zh" class="lang-section" markdown="1">

## 预设信息源库

Horizon 内置了一套围绕地缘经济、外交政策与国际事务的预设信息源库。运行 `horizon-wizard` 时，系统会根据你的兴趣关键词自动匹配这些领域，并推荐以专业新闻机构和资深记者为主的 RSS 源。

你也可以直接浏览下方列表，手动把感兴趣的源加入 `data/config.json`。

---

### 地缘经济 / 贸易 / 产业政策

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | Financial Times World | 全球贸易、政策、市场与经济治国术报道 |
| RSS | WSJ World News | 兼具商业与政策视角的国际报道 |
| RSS | Foreign Policy | 外交政策、经济与战略的专业报道与分析 |
| RSS | POLITICO Europe Trade | 布鲁塞尔贸易防御、产业政策与监管报道 |

### 全球事务 / 国际突发动态

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | BBC World | BBC 驻外记者网络的广泛国际报道 |
| RSS | DW English | 以欧洲视角报道外交、安全与经济议题 |
| RSS | RFI International | 覆盖非洲、欧洲与中东较强的国际日报道 |
| RSS | France 24 English | 持续更新的国际报道与地区连线 |

### 欧洲 / 布鲁塞尔 / 跨大西洋政策

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | POLITICO Europe Economy | 欧盟财政、产业与竞争政策报道 |
| RSS | POLITICO Europe Trade | 贸易争端、关税与布鲁塞尔规则制定 |
| RSS | POLITICO Europe Energy | 欧洲能源安全与气候政策报道 |
| RSS | Financial Times World | 欧洲与跨大西洋外溢影响背景 |

### 印太 / 中国 / 亚洲

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | The Diplomat | 亚太战略、外交与政治经济报道 |
| RSS | Nikkei Asia | 亚洲政治、商业、市场与供应链报道 |
| RSS | Foreign Policy | 将亚洲议题连接到更大策略背景的分析 |

### 能源 / 大宗商品 / 航运

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | POLITICO Europe Energy | 欧洲能源安全、基础设施与监管 |
| RSS | Financial Times World | 大宗商品、航运与宏观外溢报道 |
| RSS | Nikkei Asia | 亚洲供应链、航道与产业风险敞口 |

### 主权金融 / 宏观风险

| 类型 | 信息源 | 说明 |
|------|--------|------|
| RSS | Financial Times World | 全球宏观、主权压力与政策传导 |
| RSS | WSJ World News | 跨境金融与政策影响报道 |
| RSS | POLITICO Europe Economy | 欧元区、财政规则与竞争政策 |
| RSS | Nikkei Asia | 亚洲资本流动、产业战略与国家支持型金融 |

---

## 贡献你的信息源

我们欢迎社区补充高质量的国际事务信息源：

1. Fork [Horizon 仓库](https://github.com/thysrael/Horizon)
2. 编辑 `data/presets.json`
3. 提交 Pull Request

建议优先提交：

- 由专业新闻机构、记者站或资深通讯员持续维护的源
- 在贸易、制裁、产业政策、能源安全、主权金融、地区外交等方向有明确专长的源
- 同时提供 `description` 和 `description_zh`
- 添加清晰的 `tags` 与 `keywords`，帮助向导正确匹配

</div>

<div id="lang-en" class="lang-section" markdown="1">

## Source Preset Library

Horizon ships with a preset library built around geoeconomics, foreign policy, and international affairs. When you run `horizon-wizard`, it matches your interest keywords against these domains and recommends sources that lean heavily toward professional newsroom reporting.

You can also browse the list below and manually add any source to `data/config.json`.

---

### Geoeconomics / Trade / Industrial Policy

| Type | Source | Description |
|------|--------|-------------|
| RSS | Financial Times World | Global reporting on trade, policy, markets and economic statecraft |
| RSS | WSJ World News | International reporting with a strong business and policy frame |
| RSS | Foreign Policy | Specialist reporting and analysis on foreign policy, economics and strategy |
| RSS | POLITICO Europe Trade | Brussels coverage of trade defense, industrial policy and regulation |

### Global Affairs / Breaking International News

| Type | Source | Description |
|------|--------|-------------|
| RSS | BBC World | Broad international newsgathering from BBC correspondents |
| RSS | DW English | Europe-centered reporting on diplomacy, security and economics |
| RSS | RFI International | Daily international reporting with strong Africa, Europe and Middle East coverage |
| RSS | France 24 English | Rolling international coverage with frequent regional dispatches |

### Europe / Brussels / Transatlantic Policy

| Type | Source | Description |
|------|--------|-------------|
| RSS | POLITICO Europe Economy | EU fiscal, industrial and competition policy coverage |
| RSS | POLITICO Europe Trade | Reporting on trade disputes, tariffs and Brussels rulemaking |
| RSS | POLITICO Europe Energy | European energy security and climate-policy reporting |
| RSS | Financial Times World | Cross-border context on Europe and transatlantic spillovers |

### Indo-Pacific / China / Asia

| Type | Source | Description |
|------|--------|-------------|
| RSS | The Diplomat | Asia-Pacific reporting on strategy, diplomacy and political economy |
| RSS | Nikkei Asia | Reporting on Asian politics, business, markets and supply chains |
| RSS | Foreign Policy | Regional analysis that connects Asia stories to wider strategy |

### Energy / Commodities / Shipping

| Type | Source | Description |
|------|--------|-------------|
| RSS | POLITICO Europe Energy | Energy security, infrastructure and regulation in Europe |
| RSS | Financial Times World | Market-moving coverage of commodities, shipping and macro spillovers |
| RSS | Nikkei Asia | Useful on Asian supply chains, shipping lanes and industrial exposure |

### Sovereign Finance / Macro Risk

| Type | Source | Description |
|------|--------|-------------|
| RSS | Financial Times World | Global macro, sovereign stress and policy transmission |
| RSS | WSJ World News | Strong on cross-border financial and policy implications |
| RSS | POLITICO Europe Economy | Eurozone, fiscal rules and competition-policy coverage |
| RSS | Nikkei Asia | Asia-facing view on capital flows, industrial strategy and state-backed finance |

---

## Contribute Your Sources

We welcome additions to the preset library:

1. Fork the [Horizon repository](https://github.com/thysrael/Horizon)
2. Edit `data/presets.json`
3. Submit a Pull Request

Best additions are usually:

- Professionally reported sources maintained by established newsrooms or specialist correspondents
- Clearly differentiated coverage on trade, sanctions, industrial policy, energy security, sovereign finance, or regional diplomacy
- Sources that include both `description` and `description_zh`
- Entries with strong `tags` and domain keywords so the wizard can match them accurately

</div>
