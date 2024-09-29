from typing import Callable, Dict, List, TypeVar, Union

T = TypeVar('T')
K = TypeVar('K')

def map_by(array: List[T], func: Callable[[T], K]) -> Dict[K, T]:
    '''
    array: list of objects
    func: function which return single field of object
    returns: map, where key is returning field, value is previous object
    '''
    res: Dict[K, T] = dict()
    for el in array:
        mapping_element = func(el)
        res[mapping_element] = el
    return res
