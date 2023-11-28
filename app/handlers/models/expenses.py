from pydantic import BaseModel


class ExpensesHandlers(BaseModel):
    summ: float
    summ_period: float
