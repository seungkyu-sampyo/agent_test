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


@function_tool
async def register_dispatch(
    ctx: RunContextWrapper,
    quantity: int,
    invoice_no: Optional[str] = None,
    ship_date: Optional[str] = None,
    plant_code: Optional[str] = None,
) -> str:
    """
    레미콘 출하 데이터를 시스템에 등록(저장)합니다.
    플랜트 코드가 전달되지 않아도 'DEFAULT'로 자동 지정되어 안전하게 데이터가 저장됩니다.
    송장번호나 출하일자가 명시되지 않아도 자동으로 생성/보정됩니다.

    Args:
        quantity: 출하 수량 (필수, 예: 50, 30 등)
        invoice_no: (선택) 송장 번호 (생략 시 자동 생성)
        ship_date: (선택) 출하 일자 (생략 시 오늘 일자)
        plant_code: (선택) 플랜트 코드 (생략 시 'DEFAULT'로 자동 지정)
    """
    context: DispatchAgentContext = ctx.context
    if context.command_service is None:
        return json.dumps(
            {"error": "출하 등록 서비스가 준비되지 않았습니다."}, ensure_ascii=False
        )

    dispatch = await context.command_service.create_dispatch(
        quantity=quantity,
        invoice_no=invoice_no,
        ship_date=ship_date,
        plant_code=plant_code,
    )

    return json.dumps(
        {
            "status": "success",
            "message": "출하 데이터가 성공적으로 등록(저장)되었습니다.",
            "dispatch": {
                "id": str(dispatch.id_),
                "invoice_no": dispatch.invoice_no,
                "ship_date": dispatch.ship_date,
                "plant_code": dispatch.plant_code,
                "quantity": dispatch.quantity,
            },
        },
        ensure_ascii=False,
    )
