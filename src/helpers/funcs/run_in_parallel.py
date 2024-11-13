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
# def meow3(a) -> int:
#   for i in range(a):
#       pass
#   print('1')

# if __name__ == "__main__":
#     a = run_in_parallel(meow, (1, ))
#     b = run_in_parallel(meow2, *[(1, 2), (2, 3), (3, 4)])
#     c = run_in_parallel(meow3, *( (10**8,), (10**8,), (10**8,), (10**8,), (10**8,) )) # much faster than do it in for
#     print(a) # output = [1]
#     print(b) # output = [3, 5, 7]
