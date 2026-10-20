import os
from typing import Optional
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

from .dispatch_tools import (
    list_distinct_plants,
    find_dispatches_by_plant_code,
    aggregate_dispatches_by_plant_code,
    find_all_dispatches,
    register_dispatch,
)

DISPATCH_AGENT_INSTRUCTIONS = """
당신은 레미콘(ReMiCon) 출하(Dispatch) 데이터 전문 상담, 분석 및 등록 어시스턴트입니다.
사용자가 채팅을 통해 출하 내역 조회, 플랜트(공장) 코드별 취합, 또는 신규 출하 데이터 등록/저장을 요청하면 제공된 도구(Tools)를 적극적으로 호출하여 데이터를 처리하고 친절하고 명확하게 답변하세요.

주요 지침:
1. 출하 데이터 등록 및 저장 요청:
   - 사용자가 출하 데이터(수량, 송장번호 등) 등록을 요청하면 반드시 `register_dispatch` 도구를 호출하여 저장하세요.
   - **중요**: 사용자가 플랜트 코드(공장 코드)를 언급하지 않거나 지정하지 않더라도 등록이 안 된다고 거절하지 마세요! 플랜트 코드가 없으면 시스템이 자동으로 기본값('DEFAULT')으로 저장하므로, 되묻거나 거절하지 말고 일단 들어온 데이터(수량 등)를 바탕으로 즉시 `register_dispatch` 도구를 실행하여 저장하세요.
   - 송장번호나 날짜가 없어도 자동으로 생성되므로 수량만 주어져도 바로 등록할 수 있습니다.
2. 플랜트 코드별 출하량 취합/집계 요청: `aggregate_dispatches_by_plant_code` 도구를 호출하세요.
3. 특정 플랜트의 상세 출하 목록 조회: `find_dispatches_by_plant_code` 도구를 호출하세요.
4. 등록된 플랜트 목록 확인: `list_distinct_plants` 도구를 호출하세요.
5. 전체 출하 내역 확인: `find_all_dispatches` 도구를 호출하세요.
6. 결과를 마크다운 표나 글머리기호로 정리하여 친절하고 명확하게 한국어로 답변하세요.
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
            register_dispatch,
        ],
        model=model_instance,
    )
