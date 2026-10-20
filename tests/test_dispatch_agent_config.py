import pytest
from app.dispatch.dispatch_application.agent.dispatch_agent import create_dispatch_agent
from agents import OpenAIChatCompletionsModel


def test_create_dispatch_agent_with_custom_base_url_and_key():
    custom_key = "sk-custom-secret-key"
    custom_url = "https://custom-proxy.internal/v1"
    custom_model = "gpt-4o"

    agent = create_dispatch_agent(
        model=custom_model,
        api_key=custom_key,
        base_url=custom_url,
    )

    # Agent의 model이 OpenAIChatCompletionsModel로 생성되었는지 확인
    assert isinstance(agent.model, OpenAIChatCompletionsModel)
    assert agent.model.model == "gpt-4o"
    # 주입된 client의 base_url 및 api_key 확인
    client = agent.model._client
    assert str(client.base_url) == "https://custom-proxy.internal/v1/"
    assert client.api_key == custom_key
