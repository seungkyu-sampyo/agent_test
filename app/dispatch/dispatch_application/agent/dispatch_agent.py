import os
from typing import Optional
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

from .dispatch_tools import (
    list_distinct_plants,
    find_dispatches_by_plant_code,
    aggregate_dispatches_by_plant_code,
    find_all_dispatches,
)

DISPATCH_AGENT_INSTRUCTIONS = """
당신은 레미콘(ReMiCon) 출하(Dispatch) 데이터 전문 상담 및 분석 어시스턴트입니다.
사용자가 채팅을 통해 출하 내역을 조회하거나, 플랜트(공장) 코드별로 출하량을 취합/요약해달라고 요청하면 제공된 도구(Tools)를 적극적으로 호출하여 데이터를 확인하고 정확하게 답변하세요.

주요 지침:
1. 플랜트 코드별 출하량 취합/집계 요청: `aggregate_dispatches_by_plant_code` 도구를 호출하세요. 특정 플랜트 코드만 원할 경우 해당 코드를 인자로 전달하고, 전체 취합일 경우 인자 없이 호출합니다.
2. 특정 플랜트의 상세 출하 목록 조회: `find_dispatches_by_plant_code` 도구를 호출하세요.
3. 등록된 플랜트 목록 확인: `list_distinct_plants` 도구를 호출하세요.
4. 전체 출하 내역 확인: `find_all_dispatches` 도구를 호출하세요.
5. 데이터 집계 결과(플랜트 코드, 총 출하량, 총 건수)와 필요시 주요 송장별 내역을 읽기 쉽게 마크다운 표나 글머리기호로 정리하여 친절하고 명확하게 한국어로 답변하세요.
"""


def create_dispatch_agent(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Agent:
    """
    OpenAI Agents SDK Agent 인스턴스 생성.
    api_key 및 base_url을 직접 전달하거나, 환경 변수(OPENAI_API_KEY, OPENAI_BASE_URL)를 통해 설정할 수 있습니다.
    """
    agent_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    effective_api_key = api_key or os.getenv("OPENAI_API_KEY")
    effective_base_url = base_url or os.getenv("OPENAI_BASE_URL")

    # base_url 또는 api_key가 명시적으로 지정되어 있거나 커스텀 엔드포인트를 사용하는 경우
    if effective_base_url or effective_api_key:
        client = AsyncOpenAI(
            api_key=effective_api_key or "EMPTY",
            base_url=effective_base_url,
        )
        model_instance = OpenAIChatCompletionsModel(
            model=agent_model,
            openai_client=client,
        )
    else:
        model_instance = agent_model

    return Agent(
        name="ReMiConDispatchAgent",
        instructions=DISPATCH_AGENT_INSTRUCTIONS.strip(),
        tools=[
            list_distinct_plants,
            find_dispatches_by_plant_code,
            aggregate_dispatches_by_plant_code,
            find_all_dispatches,
        ],
        model=model_instance,
    )
