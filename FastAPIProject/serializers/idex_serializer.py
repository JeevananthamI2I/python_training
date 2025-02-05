from pydantic import BaseModel


class Nums(BaseModel):
    num1: int
    num2: int

Nums.