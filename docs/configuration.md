---
layout: default
title: Configuration Guide
---

# Configuration Guide

Horizon is configured through two files: a `.env` file for API keys and a `data/config.json` file for sources, AI provider, and filtering options.

## API Requirements

- **Required**: one AI provider key referenced by `ai.api_key_env` in `config.json`. This key is used for scoring, filtering, summarization, and enrichment.
- **Optional**: `GITHUB_TOKEN` if you enable GitHub sources and want higher GitHub API rate limits.
- **Not required in the current implementation**: Reddit API credentials, Telegram bot tokens, or a separate web-search API key.

## AI Providers

Configure which AI model scores and summarizes your content.

**Anthropic Claude**:

```json
{
  "ai": {
    "provider": "anthropic",
    "model": "claude-sonnet-4.5-20250929",
    "api_key_env": "ANTHROPIC_API_KEY"
  }
}
```

**OpenAI**:

```json
{
  "ai": {
    "provider": "openai",
    "model": "gpt-4",
    "api_key_env": "OPENAI_API_KEY"
  }
}
```

**MiniMax**:

```json
{
  "ai": {
    "provider": "minimax",
    "model": "MiniMax-M2.7",
    "api_key_env": "MINIMAX_API_KEY"
  }
}
```

Available models: `MiniMax-M2.7`, `MiniMax-M2.7-highspeed`, `MiniMax-M2.5`, `MiniMax-M2.5-highspeed`

**Aliyun DashScope** (OpenAI-compatible):

```json
{
  "ai": {
    "provider": "ali",
    "model": "qwen-plus",
    "api_key_env": "DASHSCOPE_API_KEY"
  }
}
```

Use the [DashScope compatible-mode](https://help.aliyun.com/zh/dashscope/developer-reference/use-dashscope-by-calling-openai-api) endpoint. Set `DASHSCOPE_API_KEY` in your `.env`. Optional: set `base_url` to override the default `https://dashscope.aliyuncs.com/compatible-mode/v1`.

**Custom Base URL** (for proxies):

```json
{
  "ai": {
    "provider": "anthropic",
    "base_url": "https://your-proxy.com/v1",
    ...
  }
}
```

## Information Sources

All sources are configured under the top-level `sources` key in `config.json`.

### GitHub

```json
{
  "sources": {
    "github": [
      {
        "type": "repo_releases",
        "owner": "globaldothealth",
        "repo": "outbreak-info",
        "enabled": true
      }
    ]
  }
}
```

### Hacker News

```json
{
  "sources": {
    "hackernews": {
      "enabled": true,
      "fetch_top_stories": 30,
      "min_score": 100
    }
  }
}
```

### RSS Feeds

```json
{
  "sources": {
    "rss": [
      {
        "name": "Financial Times World",
        "url": "https://www.ft.com/world?format=rss",
        "enabled": true,
        "category": "global-economy"
      }
    ]
  }
}
```

### Reddit

```json
{
  "sources": {
    "reddit": {
      "enabled": true,
      "fetch_comments": 5,
      "subreddits": [
        {
          "subreddit": "geopolitics",
          "sort": "hot",
          "fetch_limit": 25,
          "min_score": 10
        }
      ],
      "users": []
    }
  }
}
```

## Filtering

Content is scored 0-10:

- **9-10**: Critical - Major geopolitical developments with immediate strategic significance
- **7-8**: High Value - Important diplomatic, military, sanctions, or policy developments
- **5-6**: Interesting - Useful context, follow-up reporting, or regional analysis
- **3-4**: Low Priority - Generic or repetitive coverage without major implications
- **0-2**: Noise - Weakly sourced, off-topic, or trivial content

```json
{
  "filtering": {
    "ai_score_threshold": 7.0,
    "time_window_hours": 24
  }
}
```

- `ai_score_threshold`: Only include content scoring >= this value
- `time_window_hours`: Fetch content from last N hours

## Environment Variable Substitution

RSS feed URLs support `${VAR_NAME}` syntax for secrets. The variable is expanded at runtime from environment variables (or `.env` file):

```json
{
  "name": "Private research feed",
  "url": "https://example.com/feed.xml?token=${PRIVATE_FEED_TOKEN}",
  "enabled": true
}
```

This way `config.json` can be committed to a public repo without leaking tokens.
