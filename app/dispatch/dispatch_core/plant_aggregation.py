from dataclasses import dataclass, field
from .re_mi_con_dispatch import ReMiConDispatch


@dataclass
class PlantDispatchAggregation:
    """플랜트 코드별 출하 취합 데이터 모델"""

    plant_code: str
    total_quantity: int
    dispatch_count: int
    dispatches: list[ReMiConDispatch] = field(default_factory=list)
