from datetime import datetime
from app.models.base import FinanceBaseModel


def investing(
    target: FinanceBaseModel,
    sources: list[FinanceBaseModel]
) -> list[FinanceBaseModel]:
    close_date = datetime.now()
    updated = []

    for source in sources:
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )

        for obj, amount in ((target, transfer_amount),
                            (source, transfer_amount)):
            obj.invested_amount += amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = close_date

        updated.append(source)

        if target.fully_invested:
            break

    return updated
