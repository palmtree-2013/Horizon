---
layout: default
title: "Horizon Summary: 2026-02-28 (ZH)"
date: 2026-02-28
lang: zh
---

> From 39 items, 18 important content pieces were selected

---

1. [美国战争部将 Anthropic 指定为供应链风险](#item-1) ⭐️ 9.0/10
2. [OpenAI 以 7300 亿美元投前估值融资 1100 亿美元，完成历史性私募融资。](#item-2) ⭐️ 9.0/10
3. [加州新法要求所有操作系统（包括 Linux）在账户设置时进行年龄验证](#item-3) ⭐️ 8.0/10
4. [持怀疑态度的开发者通过尝试将 scikit-learn 移植到 Rust 来测试 AI 编程智能体](#item-4) ⭐️ 8.0/10
5. [Unsloth 发布更新的 Qwen3.5-35B 动态 GGUF 量化版本，附带大量基准测试和新指标标准](#item-5) ⭐️ 8.0/10
6. [混合 CPU/GPU 运行时在单张 RTX 5080 上为 80B MoE 模型实现 3324 tok/s 的预填充速度。](#item-6) ⭐️ 8.0/10
7. [Qwen3.5-35B 模型获生产环境验证，性能比肩 Claude Sonnet](#item-7) ⭐️ 8.0/10
8. [美国国防部向 Anthropic 下达最后通牒，要求解除 Claude AI 模型安全限制](#item-8) ⭐️ 8.0/10
9. [Stripe 据称正就收购 PayPal 全部或部分业务进行早期谈判](#item-9) ⭐️ 8.0/10
10. [SpaceX 猎鹰 9 号火箭碎片在高层大气中形成金属污染羽流](#item-10) ⭐️ 8.0/10
11. [Cloudflare 提出使用异步迭代器构建更简单的 JavaScript 流 API](#item-11) ⭐️ 7.0/10
12. [安全专家呼吁开发者停止使用通行密钥加密用户数据](#item-12) ⭐️ 7.0/10
13. [社区驱动的 Qwen3.5-35B-A3B 量化基准测试确认 KV q8_0 节省显存，Q4_K_M 为最优选择。](#item-13) ⭐️ 7.0/10
14. [Qwen3.5-35B-A3B 模型在 Raspberry Pi 5 上运行，通过 2-bit 量化实现超过 3 tokens/秒的速度。](#item-14) ⭐️ 7.0/10
15. [Qwen 3.5 27B 与 35B-A3B 模型在逻辑推理基准测试中表现出色，可与更大模型媲美。](#item-15) ⭐️ 7.0/10
16. [连接标准联盟发布 Aliro 1.0 规范，统一移动访问控制标准](#item-16) ⭐️ 7.0/10
17. [逾 200 名 Google 与 OpenAI 员工联署声援 Anthropic 限制军事与监控用途](#item-17) ⭐️ 7.0/10
18. [Anthropic 为开源维护者提供 6 个月免费 Claude Max 权限](#item-18) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [美国战争部将 Anthropic 指定为供应链风险](https://twitter.com/secwar/status/2027507717469049070) ⭐️ 9.0/10

美国战争部已将人工智能公司 Anthropic 指定为供应链风险，这一标签历来只用于外国对手，此前从未应用于一家美国公司。这造成了一种矛盾局面：Anthropic 一方面被标记为安全威胁，另一方面又被认为对国家安全至关重要，以至于战争部据称威胁要动用《国防生产法》来强制其 AI 模型移除某些安全防护措施。 这一将国内 AI 领军企业指定为供应链风险的前所未有的举措，可能会严重限制 Anthropic 的业务，可能将其排除在拥有政府合同的主要云平台（如 AWS、Azure 和 Google Cloud）之外，从而威胁其企业收入和生存。这标志着政府对 AI 发展的干预显著升级，凸显了国家安全要求、企业自主权和 AI 伦理防护措施之间的紧张关系。 据报道，这一指定源于 Anthropic 拒绝移除其合同中的安全防护条款，这些条款禁止将其 AI 用于大规模国内监控，并要求在致命应用中保持人在回路。如果广泛执行，该指定将阻止任何美国军事承包商或合作伙伴与 Anthropic 开展业务，社区分析认为这可能对公司的商业生存能力构成生存威胁。

hackernews · jacobedawson · Feb 27, 22:31

**背景**: Anthropic 是一家美国 AI 安全和研究公司，以开发 Claude 系列大语言模型而闻名。美国国防部已建立正式的供应链风险管理流程，以识别和减轻其采购项目中的风险，通常使用供应商绩效风险系统等工具。'供应链风险'指定是一项严肃的行政措施，通常适用于外国实体，以限制其获得国防相关合同的机会。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.dau.edu/sites/default/files/2025-06/DoD+SCRM+Guidebook+FINAL+V1.0_06_24_2025.pdf">DoD Supply Chain Risk Management Guidebook - DAU</a></li>
<li><a href="https://www.sprs.csd.disa.mil/">DISA - Supplier Performance Risk System</a></li>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区讨论凸显了对契约失信行为及对 Anthropic 生存威胁的深切担忧。评论者指出了战争部立场的矛盾：既将 Anthropic 标记为风险，又认为其技术至关重要到足以强制使用。人们非常担心，强制执行可能会切断 Anthropic 与主要云平台的连接，重创其企业业务，并可能扼杀这家公司，因为它无法仅靠个人用户订阅生存。

**标签**: `#AI Regulation`, `#National Security`, `#Government Policy`, `#Anthropic`, `#Supply Chain`

---

<a id="item-2"></a>
## [OpenAI 以 7300 亿美元投前估值融资 1100 亿美元，完成历史性私募融资。](https://techcrunch.com/2026/02/27/openai-raises-110b-in-one-of-the-largest-private-funding-rounds-in-history/) ⭐️ 9.0/10

2026 年 2 月 27 日，OpenAI 宣布在一轮私募融资中筹集了 1100 亿美元，公司在此轮投资前的估值（投前估值）为 7300 亿美元。本轮的主要投资者包括亚马逊、英伟达和软银。 这是历史上规模最大的私募融资轮次之一，表明投资者对前沿人工智能及其经济潜力的巨大信心。这笔巨额资金将支撑 OpenAI 庞大的算力和研发成本，加剧全球对通用人工智能（AGI）的竞争，并重塑行业格局。 据报道，亚马逊的投资与 OpenAI 在其'Frontier'产品中使用 AWS 服务挂钩，且部分投资承诺以 OpenAI 实现 IPO 或达成 AGI 为条件。值得注意的是，现有的主要投资者微软并未参与本轮融资。

hackernews · zlatkov · Feb 27, 14:56

**背景**: '投前估值'是指公司在获得新的外部投资之前立即估算的价值。投资后的估值（投后估值）等于投前估值加上投入的现金。此类私募融资轮通常发生在公司考虑通过首次公开募股（IPO）上市之前。AI 中的扩展定律指的是观察到的模型性能可预测地随着算力、数据和模型规模的增加而改善的关系，尽管最近的研究对这些收益的可持续性提出了质疑。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Pre-money_valuation">Pre-money valuation - Wikipedia</a></li>
<li><a href="https://www.investopedia.com/terms/p/premoneyvaluation.asp">Understanding Pre-Money Valuation: Methods, Examples, and ... Pre-money valuation - Wikipedia Pre Money Valuation - Types, Examples, Formula, Differences What is a Pre-Money Valuation? | AngelList Education Center Pre-Money Valuation: Overview, Types and Examples Pre-Money Valuation | Founder & CTO Glossary Pre-Money Valuation - AllBusiness.com</a></li>
<li><a href="https://pulley.com/guides/startup-funding-rounds-series-a-b-c">Startup Funding Rounds Explained: From Seed to IPO | Pulley</a></li>

</ul>
</details>

**社区讨论**: 社区表达了显著的怀疑和担忧。核心观点质疑 OpenAI 商业模式的可持续性，因为训练每个新模型的成本呈指数级增长，而收入增长却相对有限。一些人认为这些投资是'循环性的'，与使用投资者的云服务或硬件服务的承诺挂钩。另一些人将 OpenAI 比作网景公司，强调尽管其拥有先发优势，但被认为缺乏持久的竞争护城河。

**标签**: `#AI`, `#Venture Capital`, `#OpenAI`, `#Business Strategy`, `#Scaling Laws`

---

<a id="item-3"></a>
## [加州新法要求所有操作系统（包括 Linux）在账户设置时进行年龄验证](https://www.pcgamer.com/software/operating-systems/a-new-california-law-says-all-operating-systems-including-linux-need-to-have-some-form-of-age-verification-at-account-setup/) ⭐️ 8.0/10

美国加利福尼亚州通过了一项法律，要求所有操作系统提供商在初始账户设置过程中实施某种形式的年龄验证。这项要求明确包括了像 Linux 这样的开源系统，而不仅仅是苹果或微软的商业产品。 这标志着监管首次深入到软件的核心架构，可能为其他司法管辖区开创先例，并为全球开发者带来新的合规负担。它引发了关于在去中心化的开源项目上强制执行此类规则的技术可行性的根本问题，并可能影响用户隐私和软件自由。 根据对科罗拉多州类似提案的分析，该法律可能只要求用户“表明”其出生日期或年龄，而非像检查身份证件那样严格的验证机制。如何对全球分发、开源的 Linux 发行版进行技术和法律上的强制执行，仍然是一个尚未解决的主要挑战。

hackernews · WalterSobchak · Feb 27, 14:55

**背景**: 年龄验证法律在全球范围内被越来越多地提出和颁布，其主要目的是通过限制访问不适合年龄的内容或服务来保护未成年人。这些法律通常要求数字平台确认用户的年龄，其方法往往引发严重的隐私担忧。操作系统是计算的基础层，与应用程序层面的要求相比，在这一层级强制进行年龄检查是一种新颖且更具侵入性的监管方式。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.pcgamer.com/software/operating-systems/a-new-california-law-says-all-operating-systems-including-linux-need-to-have-some-form-of-age-verification-at-account-setup/">A new California law says all operating systems ... | PC Gamer</a></li>
<li><a href="https://itsfoss.com/news/colorado-age-attestation-bill/">US State Colorado Wants Operating Systems (Including Linux) to Tell ...</a></li>

</ul>
</details>

**社区讨论**: 社区反应以高度批评为主，焦点集中在技术上的不可行性和监管越权。评论者质疑该法律将如何应用于没有用户界面的嵌入式系统、如何在自由开源软件上强制执行，或如何处理旧版软件。情绪包括对命令行工具进行“年龄分级”的讽刺提议、对滑向“保姆国家”式监控的担忧，以及呼吁针对加州政府系统进行恶意合规。

**标签**: `#regulation`, `#open-source`, `#privacy`, `#operating-systems`, `#policy`

---

<a id="item-4"></a>
## [持怀疑态度的开发者通过尝试将 scikit-learn 移植到 Rust 来测试 AI 编程智能体](https://simonwillison.net/2026/Feb/27/ai-agent-coding-in-excessive-detail/#atom-everything) ⭐️ 8.0/10

开发者 Max Woolf 最初对 AI 编程智能体持怀疑态度，他进行了一项详细实验，逐步为智能体分配更复杂的任务，最终尝试将 Python 机器学习库 scikit-learn 移植到 Rust，暂定项目名为 'rustlearn'。实验表明，像 Anthropic 的 Opus 4.6 和 OpenAI 的 Codex 5.3 这样的模型能够成功处理复杂的编码项目，而这些项目以往需要数月的手动工作。 这项实验为 AI 辅助编程能力的显著飞跃提供了具体、真实的证据，表明其已超越简单的代码生成，能够管理复杂、多步骤的软件工程项目。这预示着开发者工作流程可能发生转变，AI 智能体可以加速诸如库移植或系统重写等重大任务，从而影响软件开发的生产力以及大规模代码迁移项目的可行性。 作者指出了沟通这种改进幅度的具体困难，他表示 2025 年 11 月前后发布的模型（如 Opus 4.5 及后续版本）比仅仅几个月前的编程大语言模型要'好一个数量级'。雄心勃勃的 'rustlearn' 项目不仅旨在翻译算法，还要实现逻辑回归和 K 均值聚类等标准机器学习算法的高性能版本，力求匹配或超越 scikit-learn 的性能。

rss · Simon Willison · Feb 27, 20:43

**背景**: Scikit-learn 是 Python 中一个基础性的开源机器学习库，被广泛认为是数据科学任务的金标准，提供了各种分类、回归和聚类算法的实现。AI 编程智能体是基于大语言模型构建的 AI 系统，能够根据自然语言指令自主或半自主地执行软件开发任务，如编写、调试和重构代码。Rust 是一种以其性能和内存安全性著称的系统编程语言，而 'crate' 是 Rust 中对代码包或库的称呼。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Scikit-learn">scikit-learn - Wikipedia</a></li>
<li><a href="https://aiforcode.io/articles/best-ai-coding-agents">Best AI Coding Agents 2026: Complete Rankings & Reviews</a></li>

</ul>
</details>

**标签**: `#AI-agents`, `#software-development`, `#machine-learning`, `#Rust`, `#code-generation`

---

<a id="item-5"></a>
## [Unsloth 发布更新的 Qwen3.5-35B 动态 GGUF 量化版本，附带大量基准测试和新指标标准](https://www.reddit.com/r/LocalLLaMA/comments/1rgel19/new_qwen3535ba3b_unsloth_dynamic_ggufs_benchmarks/) ⭐️ 8.0/10

Unsloth 团队发布了针对 Qwen3.5-35B-A3B 模型的更新版动态 GGUF 量化版本，在几乎所有比特级别上都达到了最先进的性能。他们进行了超过 150 次 KL 散度基准测试，生成了 9TB 的 GGUF 文件，并宣布将标准化发布每个量化版本的困惑度和 KL 散度指标。 这项工作为评估量化质量提供了一种严谨的、数据驱动的方法，超越了简单的性能声明。承诺为所有未来的量化版本发布标准化指标（困惑度和 KL 散度）将极大提高透明度，帮助用户做出明智选择，使整个开源 LLM 社区受益。 团队发现使用重要性矩阵有助于降低 KL 散度和困惑度，但某些 'I' 量化（如 iq3_xxs）会使推理速度降低 5-10%。他们还识别出特定的张量，例如 Mamba 层中的张量和 ffn_down_exps，对量化特别敏感，并建议不要对它们进行量化。

reddit · r/LocalLLaMA · danielhanchen · Feb 27, 18:23

**背景**: GGUF 是一种为灵活性设计的模型文件格式，常用于在 CPU 和 Apple Silicon 上运行大语言模型。量化是一种降低模型权重精度（例如，从 16 位降至 4 位）的技术，旨在减少内存占用并加速推理，通常以轻微的精度损失为代价。KL 散度（Kullback-Leibler divergence）是量化中使用的一种统计度量，用于评估量化后模型的输出概率分布与原始全精度模型分布的差异程度，是衡量质量损失的关键指标。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.shepbryan.com/blog/what-is-gguf">What is GGUF? A Beginner's Guide — Shep Bryan</a></li>
<li><a href="https://en.wikipedia.org/wiki/Kullback–Leibler_divergence">Kullback-Leibler divergence - Wikipedia</a></li>
<li><a href="https://unsloth.ai/blog/dynamic-v2">Unsloth Dynamic v.20 GGUFs</a></li>

</ul>
</details>

**社区讨论**: 社区反响极为积极，赞扬了分析的深度及其作为研究贡献的价值。AesSedai 和 ubergarm 等专家验证了这项工作的重要性，他们同意虽然 KL 散度和困惑度不能说明全部问题，但它们是评估量化版本的关键起点。许多评论强调了发布指标的新标准化举措的重要性，称这是该领域在透明度和可复现性方面迈出的重要一步。

**标签**: `#quantization`, `#benchmarking`, `#open-source-llm`, `#model-optimization`, `#machine-learning`

---

<a id="item-6"></a>
## [混合 CPU/GPU 运行时在单张 RTX 5080 上为 80B MoE 模型实现 3324 tok/s 的预填充速度。](https://i.redd.it/3bt68udk33mg1.png) ⭐️ 8.0/10

开发者发布了名为 Krasis 的新型混合 CPU/GPU 运行时的基准测试结果，显示其在使用单张 16GB VRAM 的 RTX 5080 GPU 的情况下，能在 800 亿参数的 Qwen3-Coder-Next 模型上实现每秒 3324 个令牌的预填充速度。该运行时将计算密集的预填充阶段卸载到 GPU，并在 CPU 上处理解码阶段，利用系统 RAM 来运行超出可用 GPU 内存的大型模型。 这很重要，因为它通过巧妙地将预填充和解码阶段分离，展示了一条在消费级硬件上运行超大型 MoE 模型的实用路径，使先进 AI 模型更易获取。它解决了有限的 GPU VRAM 这一关键约束，而这是本地部署最先进大语言模型的主要瓶颈。 基准测试对 800 亿参数模型使用了 Q4（4 位）量化，报告的 3324 tok/s 预填充速度是使用 1 万到 5 万令牌提示词得到的最佳结果。虽然预填充性能很高，但解码速度明显较低（例如，同一 80B 模型为 14.9 tok/s），凸显了这种混合架构固有的权衡。

reddit · r/LocalLLaMA · mrstoatey · Feb 27, 19:01

**背景**: 混合专家模型（MoE）是一种机器学习架构，其中模型由多个“专家”子网络组成，并通过路由机制决定对给定输入使用哪些专家。这使得模型可以拥有海量参数，同时保持每个令牌的计算成本可控。大语言模型推理通常有两个阶段：“预填充”（或上下文编码），即并行处理初始提示词；以及“解码”（或令牌生成），即顺序生成输出令牌。量化（如 Q4、Q8）通过使用更少的比特表示权重来减少模型的内存占用，使其能够在内存有限的硬件上运行。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Mixture_of_experts">Mixture of experts - Wikipedia</a></li>
<li><a href="https://medium.com/@sailakkshmiallada/understanding-the-two-key-stages-of-llm-inference-prefill-and-decode-29ec2b468114">Understanding the Two Key Stages of LLM Inference: Prefill and Decode(Part-1) | by Saiii | Medium</a></li>
<li><a href="https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3">Demystifying LLM Quantization Suffixes: What Q4_K_M, Q8_0 ...</a></li>

</ul>
</details>

**社区讨论**: 社区反应非常积极，赞扬了其技术创新、Rust 实现以及手工优化的汇编内核的使用。一些评论指出了其在强大集成显卡（如 Strix Halo）与 eGPU 搭配的系统上的有趣潜力。讨论的一个关键点是涉及的权衡，用户承认“残酷”的 RAM 和磁盘成本以及相对较低的解码速度（令牌生成吞吐量）是该方法的局限性。

**标签**: `#MoE`, `#LLM Inference`, `#GPU Optimization`, `#Rust`, `#Benchmarks`

---

<a id="item-7"></a>
## [Qwen3.5-35B 模型获生产环境验证，性能比肩 Claude Sonnet](https://www.reddit.com/r/LocalLLaMA/comments/1rg6ph3/qwen35_feels_ready_for_production_use_never_been/) ⭐️ 8.0/10

一位开发者报告称，Qwen3.5-35B-A3B-UD-Q6_K_XL 模型在五个真实的 JavaScript、Go 和 Rust 客户端项目中表现卓越，其输出仅需微小调整。用户将其性能和实用性直接与商业模型 Claude Sonnet 4 相提并论。 这代表了开源模型一次重要的验证，表明一个本地的 350 亿参数模型现在能够在实际编码任务中与顶级商业 API 竞争。它强化了可行混合开发工作流的论据，即高性价比的本地模型处理核心工作，而云 API 则用于专门任务。 用户获得的基准测试分数约为 1504 pp2048 和 47.71 tg256，在单 GPU 上生成速度达到每秒 80 个 token。他们使用 Git worktrees 将项目代码回滚到已知状态进行测试，且模型规格由 Claude 生成，展示了一种潜在的混合工作流。

reddit · r/LocalLLaMA · alphatrad · Feb 27, 13:29

**背景**: Qwen3.5 是 QwenLM 团队推出的一系列大语言模型，其中 35B-A3B 版本是一个混合专家模型，总参数量为 350 亿，但每个 token 仅激活 30 亿参数以提高效率。'pp2048'和'tg256'分别是评估语言模型困惑度和 token 生成速度的常见基准指标。Git worktrees 是一项功能，允许开发者在同一代码库中拥有多个工作目录，这对于在不同代码状态下隔离 AI 测试非常有用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-35B-A3B">Qwen/Qwen3.5-35B-A3B · Hugging Face</a></li>
<li><a href="https://github.com/mozilla-ai/llamafile/discussions/450">Lots of CPU benchmarks · mozilla-ai llamafile · Discussion #450 - GitHub</a></li>
<li><a href="https://medium.com/@mike-welsh/supercharging-development-using-git-worktree-ai-agents-4486916435cb">Supercharging Development: Using Git Worktree & AI Agents | by Mike Welsh | Medium</a></li>

</ul>
</details>

**社区讨论**: 社区情绪 overwhelmingly 积极，多位用户认同 Qwen3.5-35B 代表了本地模型的重大飞跃，感觉堪比 Claude Sonnet。讨论强调了其用于生产工作的“智能体”能力，分享了自定义量化版本，并探讨了用于本地部署的高性价比硬件配置。也有人提醒注意企业合规政策可能限制使用在中国开发的模型。

**标签**: `#local-llm`, `#qwen`, `#model-evaluation`, `#production-deployment`, `#open-source-ai`

---

<a id="item-8"></a>
## [美国国防部向 Anthropic 下达最后通牒，要求解除 Claude AI 模型安全限制](https://t.me/zaihuapd/39913) ⭐️ 8.0/10

美国国防部长皮特·赫格塞斯已向 Anthropic 首席执行官 Dario Amodei 发出最后通牒，要求其在周五晚间前解除 Claude AI 模型的关键安全限制以供军方使用，并威胁称如果公司拒绝，将取消一份价值 2 亿美元的国防部合同并将其列为'供应链风险'。该通牒暗示五角大楼可能动用冷战时期的《国防生产法》来强制其服从。 这次对抗是对 AI 伦理和公司治理在面对国家权力时的一次关键考验，可能为政府如何迫使私营 AI 公司为国家安全目的绕过自身安全协议开创先例。其结果可能显著加速先进 AI 的军事化，并重塑美国政府与 AI 行业之间的关系。 Anthropic 最近为其 Claude Opus 4 模型激活了 AI 安全等级 3（ASL-3）保护措施，其中包括防止模型被盗的增强安全措施和针对性强的部署标准。该公司目前的政策明确禁止其模型用于大规模监视或自主武器开发，这很可能正是五角大楼要求解除的限制。

telegram · zaihuapd · Feb 27, 14:44

**背景**: Anthropic 是一家以开发 Claude 系列大语言模型而闻名的 AI 安全与研究公司。其'负责任扩展政策'（RSP）和 AI 安全等级（ASL）是为了确保 AI 系统在能力增强时能安全部署而设计的框架。《国防生产法》（DPA）是美国 1950 年的一项法律，授予总统为国防目的监管行业的广泛权力，包括强制公司优先处理政府合同。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.btimesonline.com/articles/176751/20260225/hegseth-gives-anthropic-72-hour-ultimatum-over-claude-ai-threatens-200-million-pentagon-contract.htm">Hegseth Gives Anthropic 72-Hour Ultimatum Over Claude AI, Threatens ...</a></li>
<li><a href="https://www.anthropic.com/news/activating-asl3-protections">Activating AI Safety Level 3 protections \ Anthropic</a></li>
<li><a href="https://apnews.com/article/anthropic-military-ai-hegseth-department-of-defense-f05674f7195051ab843e5087d12c8cf8">What to know about Defense Protection Act and the Pentagon's ...</a></li>

</ul>
</details>

**标签**: `#AI Ethics`, `#Military AI`, `#Government Regulation`, `#AI Safety`, `#Anthropic`

---

<a id="item-9"></a>
## [Stripe 据称正就收购 PayPal 全部或部分业务进行早期谈判](https://t.me/zaihuapd/39914) ⭐️ 8.0/10

据 Telegram 频道引用的彭博社报道，支付处理巨头 Stripe 正在考虑收购 PayPal 的全部或部分业务，相关讨论尚处于非常早期的阶段。目前双方公司均拒绝就此潜在交易置评。 这笔潜在收购将是数字支付行业的一次重大整合，将 Stripe 专注于现代开发者工具和在线业务的优势与 PayPal 庞大的消费者网络和商户基础相结合。如果成功，它可能重塑与 Apple Pay 等主要竞争对手及传统金融机构的竞争格局。 Stripe 近期在一次员工要约收购中的估值达到 1590 亿美元，远高于 PayPal 约 433 亿美元的市值。报道指出，PayPal 近年来面临来自 Apple Pay 等竞争对手的冲击、技术现代化困境以及支付量增速放缓的挑战。

telegram · zaihuapd · Feb 27, 15:35

**背景**: Stripe 是领先的互联网金融基础设施平台，主要为企业提供接受在线支付和管理财务的工具。PayPal 是一个广泛使用的数字钱包和在线支付系统，允许个人和企业进行电子转账。数字支付市场竞争激烈，苹果（Apple Pay）和谷歌（Google Pay）等科技巨头提供了集成钱包解决方案，并获得了大量消费者的采用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://finance.yahoo.com/news/stripe-reaches-159bn-valuation-employee-114932525.html">Stripe reaches $159bn valuation in employee tender offer</a></li>
<li><a href="https://finance.yahoo.com/news/apple-pay-competitor-profile-2025-145500241.html">Apple Pay Competitor Profile 2025: Business Proposition, Key ...</a></li>

</ul>
</details>

**标签**: `#fintech`, `#mergers-acquisitions`, `#payments`, `#stripe`, `#paypal`

---

<a id="item-10"></a>
## [SpaceX 猎鹰 9 号火箭碎片在高层大气中形成金属污染羽流](https://doi.org/10.1038/s43247-025-03154-8) ⭐️ 8.0/10

发表在《自然·通讯地球与环境》上的一项研究首次提供了直接证据，表明 SpaceX 猎鹰 9 号火箭上面级在不受控再入大气层时，在高层大气中形成了显著的锂金属蒸气污染羽流。德国科学家利用高精度激光雷达在 96 公里高空探测到一股锂原子羽流，其浓度瞬间飙升了十倍，并通过风场模型倒推，将其源头锁定为 20 小时前解体的猎鹰 9 号火箭上面级。 这一发现揭示了快速发展的航天工业造成大气污染的一个先前未被量化的直接机制，可能对臭氧化学和地球辐射平衡产生长期影响。随着数万颗低地球轨道卫星（如 SpaceX 的星链星座）在未来几十年内达到寿命终点并再入大气层，金属物质的累积沉积可能成为一个重大的环境问题。 所涉及的单个猎鹰 9 号上面级估计含有约 30 公斤的锂，这些锂来自其燃料罐壁使用的铝锂合金（Al-Li AA 2198）。探测是由德国北部的莱布尼茨大气物理研究所运行的激光雷达系统完成的，大气轨迹模型确认了其与火箭在爱尔兰以西大西洋上空再入路径的关联。

telegram · zaihuapd · Feb 27, 17:15

**背景**: 激光雷达（Lidar）是一种遥感技术，利用激光脉冲测量大气特性，包括特定原子或分子的浓度。不受控再入是指航天器或火箭上面级在没有制导推进的情况下落回地球，通常会因剧烈的大气摩擦而烧毁和碎裂。高层大气，特别是中间层和低热层（约 80-100 公里高度），是存在流星体烧蚀产生的天然金属层的区域，但人为输入是一个新的研究领域。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.nature.com/articles/s43247-025-03154-8">Measurement of a lithium plume from the uncontrolled re-entry of a ...</a></li>
<li><a href="https://skyandtelescope.org/astronomy-news/rocket-reentry-leaves-lithium-in-earths-upper-atmosphere/">Rocket Reentry Leaves Lithium in Earth's Upper Atmosphere</a></li>
<li><a href="https://www.sciencealert.com/lithium-plume-in-our-atmosphere-traced-back-to-returning-spacex-rocket">Lithium Plume in Our Atmosphere Traced Back to Returning SpaceX Rocket</a></li>

</ul>
</details>

**标签**: `#space-environment`, `#atmospheric-science`, `#spacex`, `#pollution`, `#climate-impact`

---

<a id="item-11"></a>
## [Cloudflare 提出使用异步迭代器构建更简单的 JavaScript 流 API](https://blog.cloudflare.com/a-better-web-streams-api/) ⭐️ 7.0/10

Cloudflare 发布了一篇博客文章，为当前的 Web Streams API 提出了一个更符合人体工程学的替代方案，建议将其简化为本质上是一个 UInt8Array 数据块的异步迭代器。该提案认为，为不同时代设计的当前 API 对于许多常见用例来说过于复杂。 这很重要，因为 Web Streams API 现在已普遍存在于各种 JavaScript 运行时（浏览器、Node.js、边缘平台）中，用于处理网络数据、文件和实时通信。一个更简单、更直观的 API 可以显著改善开发者体验，减少样板代码，并可能影响未来的 Web 标准。 该提案的核心是将流建模为类型 `Stream<T> = { next(): Promise<{ done, value: UInt8Array<T> }> }`。然而，讨论揭示了其中的权衡，例如与同步迭代器相比，Promise 和栈切换可能带来的性能开销，特别是对于小而频繁的数据块。

hackernews · nnx · Feb 27, 14:02

**背景**: 由 WHATWG 标准化的 JavaScript Web Streams API 提供了 ReadableStream、WritableStream 和 TransformStream 等对象，用于以编程方式访问和处理数据流（例如来自网络请求），并具有内置的反压管理。ES2018 中引入的异步迭代器是一种语言特性，允许使用 `for await...of` 对数据序列进行异步迭代。当前的 ReadableStream 已经实现了异步迭代器协议。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/API/Streams_API">Streams API - Web APIs | MDN</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/AsyncIterator">AsyncIterator - JavaScript | MDN</a></li>
<li><a href="https://blog.cloudflare.com/a-better-web-streams-api/">We deserve a better streams API for JavaScript</a></li>

</ul>
</details>

**社区讨论**: 社区讨论揭示了关于 API 设计权衡的积极辩论。一位评论者提出了一种可以同步或异步返回值的替代“流迭代器”类型。其他人指出了异步可迭代对象在处理小对象时的性能问题，并提到了像 Repeater.js 这样的现有抽象。也有关于原生流 API 反压实现存在实际性能问题的报告。

**标签**: `#javascript`, `#web-standards`, `#api-design`, `#streams`, `#async-programming`

---

<a id="item-12"></a>
## [安全专家呼吁开发者停止使用通行密钥加密用户数据](https://simonwillison.net/2026/Feb/27/passkeys/#atom-everything) ⭐️ 7.0/10

安全专家 Tim Cappalli 于 2026 年 2 月公开发出呼吁，敦促身份识别行业停止推广和使用通行密钥（passkeys）来加密用户数据。他警告称，当用户不可避免地丢失其通行密钥时，这种做法将导致数据永久丢失。 这一警告突出了一个关键的错误使用模式，即开发者混淆了身份验证与数据加密，可能导致用户永久无法访问自己的数据。随着通行密钥的普及，区分这两者对于防止大规模、不可逆的数据丢失以及维护用户对无密码技术的信任至关重要。 该警告特别针对使用 WebAuthn PRF（伪随机函数）扩展的做法，该扩展允许从通行密钥派生加密密钥。尽管像 1Password 这样的工具已将其用于加密，但核心问题在于，与传统的密码重置流程不同，当通行密钥丢失时，缺乏用户友好的恢复机制。

rss · Simon Willison · Feb 27, 22:49

**背景**: 通行密钥是一种数字凭证，它使用公钥-私钥对进行防网络钓鱼的无密码身份验证，通常基于 WebAuthn 标准构建。它们的主要设计目的是向服务证明用户身份（身份验证）。WebAuthn PRF 扩展是一项较新的功能，它允许从相同的加密材料中派生加密密钥，从而模糊了身份验证和加密之间的界限。虽然某些服务可能提供如 iCloud 钥匙串托管之类的恢复选项，但这些并非普遍存在，且用户可能不理解加密的永久性。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.corbado.com/blog/passkeys-prf-webauthn">Passkeys & WebAuthn PRF for End-to-End Encryption (2026)</a></li>
<li><a href="https://1password.com/blog/encrypt-data-saved-passkeys">1Password can now encrypt data using your saved passkeys |</a></li>
<li><a href="https://support.apple.com/en-us/102195">About the security of passkeys - Apple Support</a></li>

</ul>
</details>

**标签**: `#security`, `#passkeys`, `#encryption`, `#authentication`, `#usability`

---

<a id="item-13"></a>
## [社区驱动的 Qwen3.5-35B-A3B 量化基准测试确认 KV q8_0 节省显存，Q4_K_M 为最优选择。](https://www.reddit.com/r/LocalLLaMA/comments/1rg4zqv/followup_qwen3535ba3b_7_communityrequested/) ⭐️ 7.0/10

一项在 RTX 5080 16GB GPU 上对 Qwen3.5-35B-A3B 模型进行的后续基准测试，验证了社区的假设：KV 缓存量化为 q8_0 带来的困惑度损失可忽略不计（<0.4%），而 Q4_K_M 权重量化方法仍然是质量与速度的最佳平衡。测试还显示，使用`--fit on`标志而不使用批处理标志，可将 token 生成速度提升 7%，达到每秒 74.7 个 token。 这项工作为在显存有限的 GPU（如 16GB 的 RTX 5080）上本地部署大语言模型的用户提供了具体、有数据支持的指导。它通过识别出能节省内存且不牺牲质量的“免费午餐”式优化，直接影响本地 LLM 社区，使模型推理更高效、更易实现。 实验使用了基于 CUDA 12.8 从源码构建的 llama.cpp，并测试了基于 MoE 的 Qwen3.5-35B-A3B 模型，该模型每个 token 激活约 30 亿参数。结果还表明，UD-Q4_K_XL 量化变体的性能比 Q4_K_M 更差，这一发现得到了困惑度之外的 KL 散度测量的证实。

reddit · r/LocalLLaMA · gaztrab · Feb 27, 12:09

**背景**: 量化通过降低模型权重的精度（例如，从 16 位降至 4 位）来减少其内存占用并提高推理速度，这对于在消费级硬件上运行模型至关重要。KV（键-值）缓存量化专门针对注意力机制的缓存，以在文本生成过程中节省内存。llama.cpp 是一个流行的开源框架，用于在 CPU 和 GPU 上高效运行 LLM，支持 Q4_K_M 和 q8_0 等多种量化方法。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/5932">4-bit KV Cache · ggml-org/llama.cpp · Discussion #5932</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/discussions/2094">Difference in different quantization methods · ggml-org llama.cpp...</a></li>
<li><a href="https://blog.theproductguy.xyz/understanding-ai-model-parameters-quantization-floating-point-and-more-94b06e15633f">Understanding AI Model Parameters, Quantization ... | The Product Guy</a></li>

</ul>
</details>

**社区讨论**: 社区反响非常积极，赞扬了这项全面且实用的分析。关键见解包括：对确认 KV q8_0 是节省显存的“免费午餐”表示赞赏；讨论了该发现是否适用于 Q5 等其他量化级别；另有用户分享了他们自己对超过 120 个模型变体进行广泛基准测试的链接。也有一个次要的反驳观点，提醒人们注意不要直接比较 MoE 和稠密模型等不同架构模型之间的困惑度分数。

**标签**: `#LLM Quantization`, `#Benchmarking`, `#Local LLM`, `#GPU Optimization`, `#Qwen`

---

<a id="item-14"></a>
## [Qwen3.5-35B-A3B 模型在 Raspberry Pi 5 上运行，通过 2-bit 量化实现超过 3 tokens/秒的速度。](https://v.redd.it/mfr3o67pn1mg1) ⭐️ 7.0/10

一位开发者成功在 Raspberry Pi 5 上运行了拥有 350 亿参数的 Qwen3.5-35B-A3B 大语言模型，通过 2-bit 量化，在 16GB 内存版本上实现了超过 3 tokens/秒的推理速度，在 8GB 版本上实现了超过 1.5 tokens/秒的速度。 这表明强大的大规模语言模型现在可以在成本极低、资源受限的边缘设备上运行，显著降低了在数据中心之外部署用于智能体任务、教育等高级 AI 应用的门槛。 这一性能是在没有使用 NVMe SSD、仅使用相对较快的 SD 卡以及导致降频问题的散热不佳的条件下实现的。开发者还在为 Pi 开发定制的 llama.cpp 版本，并尝试使用 ARM 的 KleidiAI 以进一步优化性能。

reddit · r/LocalLLaMA · jslominski · Feb 27, 14:30

**背景**: Qwen3.5-35B-A3B 是阿里巴巴通义千问团队推出的一个拥有 350 亿参数的大语言模型，采用混合专家（MoE）架构和门控增量网络以提高效率。量化是一种降低模型权重精度（例如，从 32 位浮点数降至 2 位整数）的技术，能大幅减少模型的内存占用和计算需求，使其能在像 Raspberry Pi 这样资源有限的设备上运行。Raspberry Pi 5 是一款流行的低成本单板计算机，采用基于 ARM 的处理器，常用于爱好者和嵌入式项目。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-35B-A3B">Qwen/Qwen3.5-35B-A3B - Hugging Face</a></li>
<li><a href="https://arxiv.org/abs/2307.13304">[2307.13304] QuIP: 2-Bit Quantization of Large Language Models With Guarantees</a></li>
<li><a href="https://rmauro.dev/running-llama-cpp-in-docker-on-raspberry-pi/">Running llama.cpp in Docker on Raspberry Pi</a></li>

</ul>
</details>

**社区讨论**: 社区对这一技术成果反应热烈，普遍表示赞扬，称其“令人印象深刻”和“疯狂”。评论包括技术性追问，例如分享了一张在 8GB Pi 上使用 mmap 实现 2.16 t/s 的截图，建议尝试在多块 Pi 上进行流水线并行或使用不同的量化级别（Q3/Q4），以及与其他硬件（如 RK3588 或 Orion O6 SoC）进行比较。也有人对将模型移植到更强大的手机上感兴趣。

**标签**: `#edge-ai`, `#model-quantization`, `#raspberry-pi`, `#llm-inference`, `#embedded-systems`

---

<a id="item-15"></a>
## [Qwen 3.5 27B 与 35B-A3B 模型在逻辑推理基准测试中表现出色，可与更大模型媲美。](https://i.redd.it/s1gze7y5g1mg1.png) ⭐️ 7.0/10

Qwen 3.5 27B 和 Qwen 3.5 35B-A3B 模型在 lineage-bench 逻辑推理基准测试中取得了令人惊讶的优异成绩，展示了从数百个前提中进行可靠推理的能力。它们的性能可与更大的模型竞争，这一点在 Artificial Analysis 平台的得分上得到了印证。 这表明较小规模的开源模型在推理效率上取得了重大飞跃，使得高级逻辑推理能力在消费级硬件上进行本地部署变得更加可行。它挑战了“卓越的推理能力仅为庞大、资源密集型模型所独有”的假设，可能加速先进 AI 的民主化进程。 Qwen 3.5 35B-A3B 是一个采用混合专家（MoE）架构的混合模型，总参数量为 350 亿，但每次前向传播仅激活 30 亿参数，从而提高了推理效率。在 Artificial Analysis 上，Qwen 3.5 27B 的推理得分为 42，远高于类似规模的稠密模型 Seed-OSS-36B-Instruct 的 25 分。

reddit · r/LocalLLaMA · fairydreaming · Feb 27, 15:24

**背景**: Lineage-bench 是一个旨在评估大语言模型（LLM）逻辑推理能力的基准测试，特别关注其处理来自众多前提的复杂推理链的能力。Qwen 3.5 系列是由阿里巴巴开发的开源多模态模型家族，其中 27B 是稠密模型，而 35B-A3B 是混合模型，它结合了线性注意力与稀疏混合专家（MoE）设计以提高效率。基准测试对于客观比较不同 AI 模型在推理等特定任务上的性能至关重要。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/Qwen/Qwen3.5-35B-A3B">Qwen/Qwen3.5-35B-A3B · Hugging Face</a></li>
<li><a href="https://sonusahani.com/blogs/qwen-27b-vs-qwen-35b">Qwen 3 . 5 27 B vs 35B: In-Depth Local Performance Comparison</a></li>
<li><a href="https://benchable.ai/models/qwen/qwen3.5-35b-a3b-20260224">Qwen: Qwen3.5-35B-A3B - AI Model Details & Benchmarks</a></li>

</ul>
</details>

**社区讨论**: 社区表达了惊讶和认可，指出 Qwen 3.5 27B 的推理水平可与 Claude 3.5 Sonnet 等大得多的模型相媲美。评论者将 lineage-bench 的结果与 Artificial Analysis 的得分进行了交叉验证，确认了 Qwen 模型与其他类似规模模型之间存在显著的性能差距。人们对能在消费级 GPU 上本地运行如此强大的模型感到兴奋，部分用户认为这些模型满足了他们的实际需求。

**标签**: `#llm-benchmarks`, `#model-evaluation`, `#qwen`, `#reasoning`, `#open-source-ai`

---

<a id="item-16"></a>
## [连接标准联盟发布 Aliro 1.0 规范，统一移动访问控制标准](https://csa-iot.org/newsroom/introducing-aliro-1-0-a-unified-standard-to-transform-the-access-control-ecosystem/) ⭐️ 7.0/10

连接标准联盟（CSA）正式发布了 Aliro 1.0 规范，旨在建立一个统一的通信标准，以简化智能手机、可穿戴设备与门禁系统之间的交互。该标准已获得 Apple、Google 和 Samsung 的支持，并将深度集成到主流移动钱包中。 此举意义重大，因为它为原本碎片化的市场创建了一个单一的、可互操作的标准，用户有望使用现有设备在各种环境（如企业、校园、酒店、住宅）中开门。获得主要科技公司的支持极大地提高了其被广泛采用的可能性，推动行业摆脱专有、封闭的解决方案。 该规范采用非对称加密技术保障安全，并支持多种无线技术：用于“碰一碰开门”的 NFC、用于基于接近度开锁的低功耗蓝牙（Bluetooth LE），以及用于精确、无感开门的超宽带（UWB）技术。已有超过 220 家成员公司参与协作，首批认证程序现已启动。

telegram · zaihuapd · Feb 27, 04:00

**背景**: 连接标准联盟（CSA），前身为 Zigbee 联盟，是一个开发和推广物联网（IoT）开放标准的行业组织，其近期最著名的标准是用于智能家居互操作的 Matter 协议。传统的移动访问控制依赖于专有系统，用户需要为不同的建筑使用不同的应用程序或凭证。NFC、低功耗蓝牙（Bluetooth LE）和超宽带（UWB）等技术在与门锁进行无线通信时，在距离、功耗和精度方面各有不同的权衡。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://csa-iot.org/">CSA-IOT - Connectivity Standards Alliance</a></li>
<li><a href="https://finance.yahoo.com/news/introducing-aliro-1-0-unified-130000043.html">Introducing Aliro 1.0: A Unified Standard to Transform the Access ...</a></li>

</ul>
</details>

**标签**: `#IoT`, `#Access Control`, `#Wireless Standards`, `#Mobile Security`, `#Industry Standards`

---

<a id="item-17"></a>
## [逾 200 名 Google 与 OpenAI 员工联署声援 Anthropic 限制军事与监控用途](https://www.axios.com/2026/02/27/google-openai-workers-push-for-military-ai-limits) ⭐️ 7.0/10

超过 200 名来自 Google 和 OpenAI 的员工签署了一封公开信，声援 Anthropic 限制先进 AI 用于国内监控或完全自主武器的政策。这封由自称与任何 AI 公司或政治团体无关的组织者发起的信函还提及，Google 已于 2025 年 2 月撤销了其内部关于 AI 用于武器和监控的禁令。 领先 AI 公司的技术人员此次协调行动，表明行业内部对其技术用于军事和监控领域所引发的道德争议和内部压力正在增长。这凸显了企业合同（例如与美国国防部的谈判）与员工驱动的道德标准之间可能存在的冲突。 签署者包括 160 余名 Google 员工和 40 余名 OpenAI 员工，签名经过核验且可选择匿名。公开信特别呼吁 Google 和 OpenAI 的领导层在 Anthropic 已拒绝的 AI 用途上采取一致立场，并提及了正在进行的与五角大楼的谈判。

telegram · zaihuapd · Feb 27, 09:50

**背景**: Anthropic 是一家以 Claude 大语言模型闻名的 AI 安全与研究公司，作为一家公益公司运营，专注于开发安全的 AI。完全自主武器系统是一种军事平台，一旦激活，可以在无需人工干预的情况下选择和攻击目标。将 AI 用于国内监控，特别是在警务和国家监控方面，引发了关于公民自由和民主规范的重大关切。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Anthropic">Anthropic - Wikipedia</a></li>
<li><a href="https://www.belfercenter.org/what-are-autonomous-weapon-systems">What are Autonomous Weapon Systems? - belfercenter.org</a></li>
<li><a href="https://thebulletin.org/2024/06/how-ai-surveillance-threatens-democracy-everywhere/">How AI surveillance threatens democracy everywhere - Bulletin</a></li>

</ul>
</details>

**标签**: `#AI Ethics`, `#Corporate Governance`, `#Military AI`, `#Employee Activism`, `#AI Policy`

---

<a id="item-18"></a>
## [Anthropic 为开源维护者提供 6 个月免费 Claude Max 权限](https://claude.com/contact-sales/claude-for-oss) ⭐️ 7.0/10

Anthropic 启动了一项针对开源社区的赠送计划，为符合条件的开源项目维护者提供六个月的免费 Claude Max 权限。申请者需维护的项目在 GitHub 上拥有至少 5000 个星标或月下载量超过 100 万，但若项目属于生态系统关键依赖，即使未达量化指标也可尝试申请。 这项举措通过向维护广泛使用项目的开发者提供高价值的 AI 工具，代表了企业对开源软件可持续性的重要支持。它认可了开源维护者在软件生态系统中扮演的关键角色，并帮助他们利用先进的 AI 助手进行开发工作。 免费的 Claude Max 权限包含的使用限额是标准 Pro 计划的 20 倍，为开发任务提供了显著更多的容量。符合条件的项目必须在 2025 年 11 月之后有提交记录，确保该计划支持的是积极维护的软件。

telegram · zaihuapd · Feb 27, 14:00

**背景**: Claude 是 Anthropic 公司开发的 AI 助手，提供包括免费版、专业版和 Max 版在内的多种订阅计划。Max 计划将 Claude 桌面和移动应用与 Claude Code 相结合，提供比专业版高得多的使用限额，并且通常最先获得新功能。开源维护者是指自愿管理和贡献于公开可用软件项目的开发者，这些项目构成了许多现代软件开发的基础。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://claude.com/pricing/max">Max plan | Claude</a></li>
<li><a href="https://claude.com/pricing">Plans & Pricing | Claude by Anthropic</a></li>

</ul>
</details>

**标签**: `#open-source`, `#developer-tools`, `#ai-assistants`, `#community-support`

---