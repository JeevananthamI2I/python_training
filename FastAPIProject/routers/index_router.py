from fastapi.routing import APIRouter
from views.index_view import  add_sum
from serializers.idex_serializer import Nums
index_router = APIRouter(prefix="/home")

@index_router.post("/")
def home(nums: Nums,a:int):
    return {"message": a+add_sum(nums.num1, nums.num2)}