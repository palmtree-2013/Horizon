from src.models import AIConfig, AIProvider
from src.setup.presets import load_presets, match_domains
from src.setup.wizard import build_config


def _ai_config() -> AIConfig:
    return AIConfig(
        provider=AIProvider.OPENAI,
        model="gpt-4",
        api_key_env="OPENAI_API_KEY",
        languages=["en", "zh"],
    )


def test_preset_library_is_rss_first_and_geoeconomic() -> None:
    presets = load_presets()

    assert presets["domains"]
    assert all(source["type"] == "rss" for domain in presets["domains"] for source in domain["sources"])

    matched_ids = [domain["id"] for domain, _ in match_domains("tariffs export controls industrial policy", presets)]
    assert "geoeconomics" in matched_ids


def test_build_config_does_not_enable_hackernews_by_default() -> None:
    config = build_config(_ai_config(), [])

    assert config.sources.hackernews.enabled is False
    assert config.sources.rss == []
    assert config.sources.reddit.enabled is False


def test_build_config_keeps_hackernews_off_for_rss_only_selection() -> None:
    config = build_config(
        _ai_config(),
        [
            {
                "type": "rss",
                "config": {
                    "name": "Financial Times World",
                    "url": "https://www.ft.com/world?format=rss",
                    "category": "global-economy",
                },
            }
        ],
    )

    assert config.sources.hackernews.enabled is False
    assert [source.name for source in config.sources.rss] == ["Financial Times World"]
