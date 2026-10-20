import json
from typing import Optional
from agents import function_tool, RunContextWrapper

from .dispatch_agent_context import DispatchAgentContext


@function_tool
async def list_distinct_plants(ctx: RunContextWrapper) -> str:
    """
    현재 시스템에 등록되어 있는 모든 플랜트 코드(공장 코드) 목록을 조회합니다.
    """
    context: DispatchAgentContext = ctx.context
    plant_codes = await context.query_service.get_distinct_plant_codes()
    return json.dumps({"plant_codes": plant_codes}, ensure_ascii=False)


@function_tool
async def find_dispatches_by_plant_code(
    ctx: RunContextWrapper, plant_code: str
) -> str:
    """
    특정 플랜트 코드(공장 코드)에 대한 모든 레미콘 출하 상세 목록을 조회합니다.

    Args:
        plant_code: 조회할 플랜트 코드 (예: '1001', 'P01' 등)
    """
    context: DispatchAgentContext = ctx.context
    dispatches = await context.query_service.get_by_plant_code(plant_code)

    items = [
        {
            "id": str(d.id_),
            "invoice_no": d.invoice_no,
            "ship_date": d.ship_date,
            "plant_code": d.plant_code,
            "quantity": d.quantity,
        }
        for d in dispatches
    ]
    return json.dumps(
        {"plant_code": plant_code, "count": len(items), "dispatches": items},
        ensure_ascii=False,
    )


@function_tool
async def aggregate_dispatches_by_plant_code(
    ctx: RunContextWrapper, plant_code: Optional[str] = None
) -> str:
    """
    플랜트 코드로 출하 수량(총 수량 합계, 총 출하 건수)을 취합 및 집계합니다.
    plant_code를 지정하지 않으면 전체 플랜트별로 각각 취합합니다.

    Args:
        plant_code: (선택 사항) 특정 플랜트 코드. 없으면 모든 플랜트별로 취합.
    """
    context: DispatchAgentContext = ctx.context
    aggregations = await context.query_service.aggregate_by_plant_code(plant_code)

    results = []
    for agg in aggregations:
        results.append(
            {
                "plant_code": agg.plant_code,
                "total_quantity": agg.total_quantity,
                "dispatch_count": agg.dispatch_count,
                "dispatches": [
                    {
                        "invoice_no": d.invoice_no,
                        "ship_date": d.ship_date,
                        "quantity": d.quantity,
                    }
                    for d in agg.dispatches
                ],
            }
        )

    return json.dumps({"aggregations": results}, ensure_ascii=False)


@function_tool
async def find_all_dispatches(ctx: RunContextWrapper) -> str:
    """
    전체 레미콘 출하 내역 목록을 조회합니다.
    """
    context: DispatchAgentContext = ctx.context
    dispatches = await context.query_service.get_all()

    items = [
        {
            "id": str(d.id_),
            "invoice_no": d.invoice_no,
            "ship_date": d.ship_date,
            "plant_code": d.plant_code,
            "quantity": d.quantity,
        }
        for d in dispatches
    ]
    return json.dumps(
        {"total_count": len(items), "dispatches": items}, ensure_ascii=False
    )
