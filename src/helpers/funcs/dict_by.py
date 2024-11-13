from typing import Callable, Dict, List, TypeVar

T = TypeVar('T')
K = TypeVar('K')

def dict_by(array: List[T], func: Callable[[T], K]) -> Dict[K, T]:
    '''
    array: list of objects
    func: function which returns one field of object
    returns: dict, where key is returnable field and value is full object
    '''
    res: Dict[K, T] = {}
    for el in array:
        mapping_element = func(el)
        res[mapping_element] = el
    return res
