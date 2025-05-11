from lotr_sdk.core.settings import Settings


def test_settings_initialization():
    """Test that settings can be initialized with arguments."""
    settings = Settings(
        api_key="test-key",
        base_url="https://custom-url.com",
        timeout=60.0,
        max_retries=5,
        retry_delay=2.0,
        user_agent="custom-agent/1.0",
    )

    assert settings.api_key == "test-key"
    assert settings.base_url == "https://custom-url.com"
    assert settings.timeout == 60.0
    assert settings.max_retries == 5
    assert settings.retry_delay == 2.0
    assert settings.user_agent == "custom-agent/1.0"


def test_settings_default_values():
    """Test that settings have correct default values when not specified."""
    settings = Settings(api_key="test-key")

    assert settings.api_key == "test-key"
    assert settings.base_url == "https://the-one-api.dev"
    assert settings.timeout == 30.0
    assert settings.max_retries == 3
    assert settings.retry_delay == 1.0
    assert "lotr-sdk" in settings.user_agent


def test_settings_from_environment_variables(monkeypatch):
    """Test that settings can be loaded from environment variables."""
    # Set environment variables
    monkeypatch.setenv("LOTR_API_KEY", "env-key")
    monkeypatch.setenv("LOTR_BASE_URL", "https://env-url.com")
    monkeypatch.setenv("LOTR_TIMEOUT", "45.0")
    monkeypatch.setenv("LOTR_MAX_RETRIES", "4")
    monkeypatch.setenv("LOTR_RETRY_DELAY", "3.0")
    monkeypatch.setenv("LOTR_USER_AGENT", "env-agent/1.0")

    # Initialize settings with default API key from env
    settings = Settings(api_key="env-key")

    assert settings.api_key == "env-key"
    assert settings.base_url == "https://env-url.com"
    assert settings.timeout == 45.0
    assert settings.max_retries == 4
    assert settings.retry_delay == 3.0
    assert settings.user_agent == "env-agent/1.0"


def test_argument_precedence_over_environment(monkeypatch):
    """Test that constructor arguments take precedence over environment variables."""
    # Set environment variables
    monkeypatch.setenv("LOTR_API_KEY", "env-key")
    monkeypatch.setenv("LOTR_BASE_URL", "https://env-url.com")
    monkeypatch.setenv("LOTR_TIMEOUT", "45.0")
    monkeypatch.setenv("LOTR_MAX_RETRIES", "4")
    monkeypatch.setenv("LOTR_RETRY_DELAY", "3.0")
    monkeypatch.setenv("LOTR_USER_AGENT", "env-agent/1.0")

    # Initialize with arguments that should override env vars
    settings = Settings(
        api_key="arg-key",
        base_url="https://arg-url.com",
        timeout=60.0,
        max_retries=5,
        retry_delay=2.0,
        user_agent="arg-agent/1.0",
    )

    # Verify that arguments take precedence
    assert settings.api_key == "arg-key"
    assert settings.base_url == "https://arg-url.com"
    assert settings.timeout == 60.0
    assert settings.max_retries == 5
    assert settings.retry_delay == 2.0
    assert settings.user_agent == "arg-agent/1.0"


def test_partial_override_of_environment(monkeypatch):
    """Test that arguments partially override environment variables."""
    # Set environment variables
    monkeypatch.setenv("LOTR_API_KEY", "env-key")
    monkeypatch.setenv("LOTR_BASE_URL", "https://env-url.com")
    monkeypatch.setenv("LOTR_TIMEOUT", "45.0")
    monkeypatch.setenv("LOTR_MAX_RETRIES", "4")
    monkeypatch.setenv("LOTR_RETRY_DELAY", "3.0")
    monkeypatch.setenv("LOTR_USER_AGENT", "env-agent/1.0")

    # Override only some settings
    settings = Settings(
        api_key="arg-key",
        base_url="https://arg-url.com",
    )

    # Check that specified args override env vars
    assert settings.api_key == "arg-key"
    assert settings.base_url == "https://arg-url.com"

    # Check that unspecified args use env vars
    assert settings.timeout == 45.0
    assert settings.max_retries == 4
    assert settings.retry_delay == 3.0
    assert settings.user_agent == "env-agent/1.0"
