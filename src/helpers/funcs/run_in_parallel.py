from multiprocessing import Pool
from typing import Callable, List, Tuple, TypeVar

T = TypeVar('T')
K = TypeVar('K')

def run_in_parallel(func: Callable[..., K], *args: Tuple[T]) -> List[K]:
    with Pool() as pool:
        result = pool.starmap(func, args)
    return result

# # Usage example
# def meow(a1: int) -> int:
#     return a1
# def meow2(a1: int, a2: int) -> int:
#     return a1 + a2

# if __name__ == "__main__":
#     a = run_in_parallel(meow, (1, )) # output = [1]
#     b = run_in_parallel(meow2, *[(1, 2), (2, 3), (3, 4)]) # output = [3, 5, 7]
#     print(a)
#     print(b)
