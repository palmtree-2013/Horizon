---
layout: default
title: "Horizon Summary: 2026-04-09 (ZH)"
date: 2026-04-09
lang: zh
---

> From 27 items, 10 important content pieces were selected

---

1. [Nix 包管理器守护进程漏洞允许 root 权限提升](#item-1) ⭐️ 9.0/10
2. [Anthropic 发起 Project Glasswing，联合多家科技巨头利用 AI 检测关键软件漏洞](#item-2) ⭐️ 9.0/10
3. [Mac OS X 成功移植到任天堂 Wii 游戏机](#item-3) ⭐️ 8.0/10
4. [Meta 推出 Muse Spark，一款面向个人超级智能的前沿 AI 模型。](#item-4) ⭐️ 8.0/10
5. [文章质疑仅靠扩展能否带来真正的 AI 突破，强调机器学习的非传统未来。](#item-5) ⭐️ 8.0/10
6. [Linux 内核开发者就处理整数溢出错误的新 API 达成共识。](#item-6) ⭐️ 8.0/10
7. [日本批准修订《个人信息保护法》，放宽 AI 开发中个人数据使用限制](#item-7) ⭐️ 8.0/10
8. [《纽约时报》调查提出证据将 Adam Back 与中本聪联系起来](#item-8) ⭐️ 8.0/10
9. [男性避孕重大突破：靶向减数分裂实现安全可逆的非激素方案](#item-9) ⭐️ 8.0/10
10. [一份在阅读代码前分析代码库的 Git 命令指南](#item-10) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Nix 包管理器守护进程漏洞允许 root 权限提升](https://lwn.net/Articles/1066813/) ⭐️ 9.0/10

NixOS 项目宣布 Nix 包管理器守护进程中存在一个关键的权限提升漏洞（CVE-2024-27297），该漏洞是在修复先前问题时引入的。该缺陷影响所有默认的 NixOS 配置以及构建不受信任 derivations 的系统，允许用户通过在固定输出 derivation 注册期间利用符号链接跟随来获取 root 权限。 该漏洞非常关键，因为它影响了 NixOS 的默认配置以及 Nix 守护进程以 root 身份运行的多用户安装，可能允许任何能够提交构建的用户获得完整的系统控制权。鉴于 Nix 在可重现构建和系统配置管理方面的日益普及，此安全缺陷可能影响众多生产系统和开发环境。 该漏洞专门影响沙盒化的 Linux 构建，但不影响沙盒化的 macOS 构建，涉及 Nix 进程在输出注册期间跟随由 derivation 构建器创建的符号链接。在使用默认设置（其中 allowed-users 默认为所有用户）的多用户安装中，这为通过修改敏感文件实现 root 权限提升创造了途径。

rss · LWN.net · Apr 8, 13:52

**背景**: Nix 是一个最初作为大学研究项目开发的包管理器，旨在解决传统包管理器的不足，以其可重现的构建和声明式配置方法而闻名。在 Nix 中，derivations 是描述如何创建包的构建规范，而 Nix 守护进程在多用户安装中通常以 root 身份运行，以管理构建和系统范围的包。固定输出 derivations 是一种特殊的 derivations，其输出是预先已知的，例如源代码压缩包或 Git 检出。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.cjjackson.dev/posts/nix-package-manager/">Nix Package Manager</a></li>
<li><a href="https://nix.dev/manual/nix/2.25/language/derivations">Derivations - Nix Reference Manual</a></li>
<li><a href="https://ubuntu.com/security/CVE-2024-27297">CVE-2024-27297 | Ubuntu Fixed-Output Derivation Sandbox Bypass (CVE-2024-27297) Sandbox escape: file write via symlink at FOD `.tmp` copy ... CVE Record: CVE-2024-27297 Nix privilege escalation security advisory [LWN.net] CVE-2024-27297 - Vulnerability Details - OpenCVE</a></li>

</ul>
</details>

**标签**: `#security`, `#vulnerability`, `#nix`, `#package-management`, `#privilege-escalation`

---

<a id="item-2"></a>
## [Anthropic 发起 Project Glasswing，联合多家科技巨头利用 AI 检测关键软件漏洞](https://www.anthropic.com/glasswing) ⭐️ 9.0/10

Anthropic 发起了 Project Glasswing，与 AWS、Apple、Google、Microsoft、NVIDIA 和 JPMorganChase 合作，利用 Claude Mythos Preview AI 模型检测关键软件基础设施中的高风险零日漏洞。该模型在数周内已发现数千个涉及主要操作系统和浏览器的高危漏洞，Anthropic 承诺提供最高 1 亿美元的模型使用额度和 400 万美元的直接捐赠给开源安全组织。 这一举措代表了突破性的行业合作，通过主动识别漏洞来显著增强网络安全防御能力。主要科技公司和金融机构的参与表明了对 AI 时代关键软件基础设施安全的集体承诺，可能为 AI 驱动的防御性网络安全设定新标准。 Claude Mythos Preview 模型暂不计划全面开放，但 Anthropic 将在 90 天内公开阶段性成果，并已向 40 多家关键软件基础设施相关组织开放接入。该项目专门专注于防御性网络安全应用而非攻击性用途，部分已发现的漏洞已完成修补。

telegram · zaihuapd · Apr 8, 00:41

**背景**: 零日漏洞是先前未知的安全缺陷，攻击者可以在开发者修复之前利用它们，因此特别危险。AI 驱动的漏洞检测利用机器学习和模式识别来分析代码，比手动代码审查或模糊测试等传统方法更高效地识别潜在安全问题。根据搜索结果，Claude Mythos Preview 是 Anthropic 迄今为止最强大的 AI 模型，专门为网络安全应用设计。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/glasswing?ref=upstract.com">Project Glasswing : Securing critical software for the AI era \ Anthropic</a></li>
<li><a href="https://securifyai.co/learnings/how-ai-can-detect-and-prevent-zero-day-vulnerabilities/">How AI Detects and Prevents Zero - Day Vulnerabilities</a></li>
<li><a href="https://captaincompliance.com/education/anthropic-debuts-claude-mythos-preview-a-cybersecurity-game-changer-with-double-edged-implications/">Anthropic Debuts Claude Mythos Preview: A Cybersecurity</a></li>

</ul>
</details>

**标签**: `#AI`, `#Cybersecurity`, `#Software Engineering`, `#Industry Collaboration`, `#Vulnerability Detection`

---

<a id="item-3"></a>
## [Mac OS X 成功移植到任天堂 Wii 游戏机](https://bryankeller.github.io/2026/04/08/porting-mac-os-x-nintendo-wii.html) ⭐️ 8.0/10

一名开发者成功将 Mac OS X 移植到任天堂 Wii 游戏机上运行，并在一份详细的技术报告中记录了克服重大硬件限制和驱动挑战的过程。该项目需要编写自定义的帧缓冲驱动程序，并调整操作系统以适应 Wii 的 88MB 内存和基于 PowerPC 的 Broadway 处理器。 这展示了 Mac OS X 的 I/O Kit 抽象层的卓越适应性，并展现了可能激发类似非常规硬件项目的高级逆向工程技术。它突显了操作系统移植如何能够突破旧硬件的能力边界，可能影响未来的黑客和模拟器社区。 Wii 的硬件存在重大限制，包括仅有 88MB 总内存和需要大量内核修改的 PowerPC 架构。开发者必须编写自定义的帧缓冲驱动程序，才能使 Mac OS X 图形界面在 Wii 的视频输出上正常显示。

hackernews · blkhp19 · Apr 8, 15:40

**背景**: 移植操作系统涉及调整其在不同硬件架构上运行，这需要对操作系统内核和目标硬件规格都有深入理解。任天堂 Wii 使用基于 PowerPC 的 Broadway 处理器，与现代计算机相比内存有限，而 Mac OS X 最初是为苹果的 PowerPC 和英特尔硬件设计的，具有特定的驱动程序要求。之前的 Hackintosh 项目曾修改 Mac OS X 以在非苹果的 PC 硬件上运行，但移植到游戏机代表了更大的挑战，因为 Wii 具有专门的组件和限制。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Wii">Wii - Wikipedia</a></li>
<li><a href="https://en.wikipedia.org/wiki/Hackintosh">Hackintosh - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: 社区对技术成就和报告质量表达了热情赞赏，评论强调了令人印象深刻的工程工作和 Mac OS X 抽象层的惊人适应性。值得注意的反应包括来自 NetBSD Wii 移植作者的赞扬、对所展示的逆向工程技能的钦佩，以及对 Wii 内存与现代标准相比有限的幽默观察。

**标签**: `#reverse-engineering`, `#operating-systems`, `#hardware-hacking`, `#macos`, `#nintendo-wii`

---

<a id="item-4"></a>
## [Meta 推出 Muse Spark，一款面向个人超级智能的前沿 AI 模型。](https://ai.meta.com/blog/introducing-muse-spark-msl/?_fb_noscript=1) ⭐️ 8.0/10

2026 年 4 月 8 日，Meta 推出了 Muse Spark，这是其 Meta Superintelligence Labs (MSL) 的首个主要 AI 模型，设计为原生多模态推理模型，具备视觉思维链等功能。它旨在与 Opus 4.6 等顶级前沿模型竞争，标志着 Meta 在 AI 战略上的重要一步。 这很重要，因为 Muse Spark 将 Meta 定位为前沿 AI 竞赛的直接竞争者，可能减少对外部模型的依赖，并影响更广泛的 AI 生态系统。如果它能匹配领先模型，可能会加速个人超级智能的发展，为用户在编码和视觉分析等任务中提供增强的 AI 能力。 Muse Spark 被描述为原生多模态模型，支持视觉思维链，但提供的资料中未详细说明其架构或训练数据。它包含诸如 Code Interpreter Python 容器和名为 'container.visual_grounding' 的图像分析工具等功能，可通过 meta.ai 访问。

hackernews · chabons · Apr 8, 16:01

**背景**: 前沿 AI 模型代表了人工智能的最前沿，在多样化任务中推动性能边界。个人超级智能指的是大幅超越人类认知能力的 AI 系统，旨在赋能个人实现目标。Meta 之前的努力包括 Llama 等开源模型，但 Muse Spark 标志着向竞争性、专有前沿模型的转变。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://grokipedia.com/page/Muse_Spark_AI_model">Muse Spark (AI model)</a></li>
<li><a href="https://www.meta.com/superintelligence/">Personal Superintelligence - Meta</a></li>
<li><a href="https://klu.ai/glossary/frontier-models">Frontier AI Models — Klu</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示情绪复杂，一些用户赞扬 Muse Spark 与 Opus 4.6 等领先模型竞争的潜力及其实用工具，而另一些用户则质疑 Meta 从开放生态系统转向的战略，并担忧 AI 竞赛可能导致商品化。讨论还包括关于模型多模态功能的技术疑问。

**标签**: `#artificial-intelligence`, `#meta`, `#large-language-models`, `#ai-race`, `#hackernews`

---

<a id="item-5"></a>
## [文章质疑仅靠扩展能否带来真正的 AI 突破，强调机器学习的非传统未来。](https://aphyr.com/posts/411-the-future-of-everything-is-lies-i-guess) ⭐️ 8.0/10

一篇题为《The Future of Everything is Lies, I Guess》的文章探讨了机器学习未来发展的非传统性和潜在欺骗性，质疑当前的扩展方法是否能带来真正的突破。它认为机器学习的道路可能极其怪异，挑战了通过纯粹规模实现进步的假设。 这很重要，因为它批判了 AI 研究中的主流趋势，即对模型扩展的大规模投资可能掩盖基本限制和伦理问题，导致欺骗性结果而非真正的智能。它鼓励对 AI 发展进行哲学反思，影响研究人员、政策制定者和更广泛的科技行业。 文章引用了 2017 年《Attention is All You Need》论文作为突破性进展，但指出后续的复杂架构并未超越单纯增加参数的方法，暗示扩展带来的回报递减。它质疑在当前方法下，考虑到巨大的训练成本和语料库限制，是否能够实现人类等效的能力。

hackernews · pabs3 · Apr 8, 13:06

**背景**: 机器学习扩展涉及增加模型大小、数据和计算以提高性能，这在 GPT 等大型语言模型中可见。人工智能哲学探讨机器是否能真正思考或拥有意识，涉及智能和伦理问题。当前的 AI 趋势通常侧重于扩展，但这篇文章将其与更广泛的辩论联系起来，即这是否会导致真正的突破或欺骗性结果。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Philosophy_of_artificial_intelligence">Philosophy of artificial intelligence</a></li>
<li><a href="https://citizenside.com/technology/what-is-scaling-in-machine-learning/">What Is Scaling In Machine Learning | CitizenSide</a></li>

</ul>
</details>

**社区讨论**: 社区评论显示情绪复杂，一些人将其与工业革命等历史范式相提并论，而另一些人则辩论扩展或架构创新哪个更有效。关键观点包括对扩展回报递减的担忧、对 LLM 能力进行细致讨论的必要性，以及与 AI 研究中“苦涩教训”的比较。

**标签**: `#machine-learning`, `#artificial-intelligence`, `#future-of-ai`, `#technology-trends`, `#philosophy-of-ai`

---

<a id="item-6"></a>
## [Linux 内核开发者就处理整数溢出错误的新 API 达成共识。](https://lwn.net/Articles/1065889/) ⭐️ 8.0/10

2026 年 3 月 31 日，Kees Cook 分享了一个补丁集，为 Linux 内核引入了一个处理整数溢出的新 API，这是超过一年工作的成果；Linus Torvalds 最初反对，但开发者最终就不同的 API 设计达成共识。该 API 使用 __ob_wrap 和 __ob_trap 等注解来指定预期或非预期的溢出行为，覆盖编译器标志以确保一致的处理。 这很重要，因为整数溢出是系统编程中常见的安全漏洞来源，新 API 旨在消除内核中静默、无意的溢出，可能减少错误并增强安全性。它反映了内核加固工作的更广泛趋势，影响编写低级代码的开发者，并提高整体系统可靠性。 该 API 包括 __ob_wrap 用于预期回绕和 __ob_trap 用于非预期溢出（默认导致内核 oops 崩溃）；它还支持 Vincent Mailhol 建议的饱和整数，并提供了 u8t 和 s64w 等 typedef 以便引用。设计覆盖了如 -fno-strict-overflow 的编译器标志，确保无论编译设置如何行为都一致。

rss · LWN.net · Apr 8, 14:53

**背景**: 整数溢出发生在算术运算产生超出可表示范围的值时，可能导致系统编程中的安全漏洞，如缓冲区溢出。在 Linux 内核中，由于 -fno-strict-overflow 标志，整数溢出不是未定义行为，但它可能导致意外代码路径，例如缓冲区处理中的错误指针计算。内核加固技术旨在通过添加安全检查和使用 API 来防止此类错误被利用。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Integer_overflow">Integer overflow - Wikipedia</a></li>
<li><a href="https://reintech.io/blog/hardening-linux-kernel-sysctl-debian-12">Hardening the Linux Kernel with Sysctl on Debian 12 | Reintech media</a></li>
<li><a href="https://github.com/intel/safe-arithmetic">GitHub - intel/safe-arithmetic: Safe arithmetic library for C++20 and above. Safe arithmetic ensures correctness of arithmetic operations at compile-time. It protects against overflow, underflow, divide by zero, and out-of-bounds index access. This provides both functional correctness as well as greater protection against related security threats. · GitHub</a></li>

</ul>
</details>

**标签**: `#linux-kernel`, `#security`, `#api-design`, `#integer-overflow`, `#systems-programming`

---

<a id="item-7"></a>
## [日本批准修订《个人信息保护法》，放宽 AI 开发中个人数据使用限制](https://www.theregister.com/2026/04/08/japan_privacy_law_changes_ai/) ⭐️ 8.0/10

日本政府周二批准修订《个人信息保护法》，放宽了个人数据在 AI 开发中的使用条件，例如在共享低风险数据用于研究性统计时无需事先取得同意，健康数据也可用于改善公共卫生。面部扫描数据被纳入，采集时需说明处理方式但不再强制提供退出选项，同时保留了对未成年人数据的保护措施。 这一政策变化可能通过减少数据获取的监管障碍来加速日本的 AI 创新，使该国在全球 AI 竞争中更具竞争力，并可能影响其他国家在隐私保护与技术发展之间的平衡策略。这反映了政府调整数据保护法律以促进 AI 发展并应对伦理问题的更广泛趋势。 修订案包含具体豁免条款，例如用于研究性统计的低风险个人数据和用于改善公共卫生的健康数据无需事先同意，面部扫描数据采集不再强制提供退出选项。限制措施依然存在，包括采集 16 岁以下未成年人图像需父母同意、对未成年人数据进行'最大利益'审查，以及对数据滥用的处罚，但低风险数据泄露无需通知受影响者。

telegram · zaihuapd · Apr 8, 07:13

**背景**: 日本的《个人信息保护法》是一项关键的数据隐私法规，类似于欧盟的 GDPR，规范个人数据的收集、使用和共享。由于严格的同意要求，该法律被视为 AI 发展的障碍，因此进行了修订以顺应全球趋势，即各国更新隐私法律以支持 AI 研究，例如通过 GDPR 等框架为统计和研究目的提供豁免。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.ppc.go.jp/en/legal/">Laws and Policies |PPC Personal Information Protection ...</a></li>
<li><a href="https://link.springer.com/chapter/10.1007/978-3-030-21752-5_8">Re-using Personal Data for Statistical and Research Purposes in the Context of Big Data and Artificial Intelligence | SpringerLink</a></li>

</ul>
</details>

**标签**: `#AI Policy`, `#Data Privacy`, `#Regulation`, `#Japan`, `#AI Development`

---

<a id="item-8"></a>
## [《纽约时报》调查提出证据将 Adam Back 与中本聪联系起来](https://www.nytimes.com/2026/04/08/business/bitcoin-satoshi-nakamoto-identity-adam-back.html) ⭐️ 8.0/10

《纽约时报》于 2026 年 4 月发表的一项调查，通过语言分析、历史邮件档案和风格比较，提出了系统性的证据，表明 Adam Back 可能是比特币的匿名创造者中本聪。该调查分析了密码学邮件列表中超过 34,000 条帖子，基于词汇、标点错误和写作怪癖进行了七轮筛选，最终将 Back 确定为唯一剩下的嫌疑人。 这项调查之所以重要，是因为它触及了技术和加密货币历史上最持久的谜团之一，可能揭示比特币创造背后的身份。如果被证实，它将重塑我们对比特币起源的理解，并影响加密货币生态系统中关键人物的可信度，包括 Back 的公司 Blockstream。 关键证据包括 Back 在 1997 年至 1999 年间（比特币出现前）的著作，预见了比特币的核心概念，如分布式电子现金、拜占庭容错和哈希树时间戳，以及惊人的风格相似性，如共享词汇和标点错误。然而，Back 否认自己是中本聪，将相似性归因于巧合和统计偏差，而决定性证据需要从创世区块地址移动比特币。

telegram · zaihuapd · Apr 8, 12:30

**背景**: 中本聪是比特币的匿名创造者，于 2008 年发布了比特币白皮书，并于 2011 年消失，其真实身份未知。Adam Back 是一位英国密码学家，发明了 Hashcash（一种工作量证明系统，在比特币白皮书中被引用），并且是加密货币社区的重要人物，也是 Blockstream 的联合创始人。该调查借鉴了拜占庭将军问题（与分布式系统中的共识相关）和哈希树时间戳（用于创建不可变记录）等概念。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Hashcash">Hashcash</a></li>
<li><a href="https://en.wikipedia.org/wiki/Byzantine_Generals_Problem">Byzantine Generals Problem</a></li>
<li><a href="https://en.wikipedia.org/wiki/File:Hashtree_timestamping.svg">File:Hashtree timestamping .svg - Wikipedia</a></li>

</ul>
</details>

**标签**: `#Bitcoin`, `#Cryptocurrency`, `#Satoshi Nakamoto`, `#Investigative Journalism`, `#Cryptography`

---

<a id="item-9"></a>
## [男性避孕重大突破：靶向减数分裂实现安全可逆的非激素方案](https://news.cornell.edu/stories/2026/04/breakthrough-takes-big-step-toward-safe-reversible-male-contraception) ⭐️ 8.0/10

康奈尔大学的研究人员通过靶向减数分裂，利用小分子抑制剂 JQ1 干扰小鼠减数分裂前期 I 的粗线期，开发出一种安全、可逆且非激素的男性避孕方法。连续给药三周后，雄性小鼠的精子产量降至零，停药六周后生育能力完全恢复，且后代健康并具备正常生殖能力。 这一突破填补了男性避孕领域缺乏可逆、长效非激素选项的关键空白，有望促进生殖健康领域的性别责任共担。如果成功应用于人类，可能开发出每三个月注射一次或使用贴片的长效制剂，为家庭规划和公共卫生带来革命性变化。 该研究专门靶向减数分裂前期 I 的粗线期，利用 JQ1 干扰基因表达程序而不损害精原干细胞，确保了完全可逆性。目前研究仍处于小鼠概念验证阶段，团队正在探索减数分裂中更早期的靶点，以优化药物递送并确保精子完全清除。

telegram · zaihuapd · Apr 8, 16:00

**背景**: 减数分裂是一种特殊的细胞分裂过程，通过将染色体数目减半来产生配子（如精子），其中前期 I 包括粗线期等阶段，同源染色体在此配对和重组。JQ1 是一种小分子抑制剂，主要靶向 BET 蛋白家族中的 BRD4，通过阻断与乙酰化组蛋白的相互作用来干扰基因表达，广泛用于癌症研究，但在此被重新用于避孕。目前男性避孕手段仅限于避孕套（屏障法）和输精管结扎（手术绝育），缺乏可逆的长效非激素选项。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://zh.wikipedia.org/zh-hans/减数分裂">减数分裂 - 维基百科，自由的百科全书</a></li>
<li><a href="https://zhuanlan.zhihu.com/p/1956380493269406315">AbMole小课堂丨JQ1：BRD4抑制剂，在肿瘤、免疫和细胞分化研究中的应用</a></li>

</ul>
</details>

**标签**: `#biotechnology`, `#reproductive-health`, `#medical-research`, `#non-hormonal-contraception`, `#scientific-breakthrough`

---

<a id="item-10"></a>
## [一份在阅读代码前分析代码库的 Git 命令指南](https://piechowski.io/post/git-commands-before-reading-code/) ⭐️ 7.0/10

一篇题为《Git commands I run before reading any code》的博客文章发布，提供了一份实用指南，介绍如何使用 Git 命令来理解代码库中的变更、贡献者和提交历史。该指南包含诸如 'git shortlog' 和 'git log' 等具体命令，用于分析文件变更和作者贡献随时间的变化。 这很重要，因为它帮助开发者快速理解代码库的上下文和健康状况，提高生产力并减少新团队成员的适应时间。它通过提供基于 Git 的可操作分析技术，解决了软件开发中的常见挑战，如糟糕的提交消息和识别问题文件。 该指南侧重于诸如 'git shortlog -sn --no-merges' 等命令来列出主要贡献者，以及使用过滤器的 'git log' 来查找变更最多的文件，但它指出了局限性，例如由于糟糕的提交实践导致的指标不准确。它还提到了替代工具如 Jujutsu 用于类似分析，正如社区评论中所讨论的。

hackernews · grepsedawk · Apr 8, 08:53

**背景**: Git 是一个广泛用于软件开发的分布式版本控制系统，用于跟踪源代码的变更，促进开发者之间的协作。它允许用户通过命令行工具或图形界面管理代码历史、分支和合并。理解 Git 命令对于代码审查、调试和维护项目完整性等任务至关重要，尤其是在团队环境中。

**社区讨论**: 社区讨论显示出复杂的情感，一些用户赞赏该指南的实用性并分享了如 Jujutsu 等效工具的替代方案，而其他人则批评其对提交消息的假设，并强调了现实世界问题，如 'git shortlog' 产生的不准确指标。评论还包括个人经验和用于类似分析的自定义别名。

**标签**: `#git`, `#software-development`, `#code-analysis`, `#productivity`, `#version-control`

---