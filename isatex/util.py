from collections import deque
from os.path import basename, splitext
from typing import Any, Iterable, List, Tuple

from wx import Panel, Window


class Singleton:
    """Base class for realizing the Singleton pattern.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance


class DotNotationDict(dict):
    """A dictionary that allows grouping of values using dot-delimited keys.
    """

    def __init__(self, *args, **kwargs):
        """Default constructor
        """
        super().__init__(*args, **kwargs)
        items = tuple(self.items())
        self.clear()
        for key, value in items:
            self.forced_setitem(key, value)

    def __getitem__(self, key):
        if not isinstance(key, str) or '.' not in key:
            return super().__getitem__(key)

        next_dct, branch_key = self.__get_next_item(key)
        value = self.__get_dict_from_dotted_key(branch_key, next_dct)
        if isinstance(value, dict):
            value = DotNotationDict(value)
            super().__setitem__(key, value)
        return value

    def get(self, key: Any, default: Any = None) -> Any:
        """Get the value corresponding to the specified key.

        :type key: Any
        :param default: Value to be returned if the value for the specified key is not found., defaults to None
        :type default: Any, optional
        :rtype: Any
        """
        if not isinstance(key, str) or '.' not in key:
            return super().get(key, default)

        root_key = key[: key.find('.')]
        branch_key = key[key.find('.') + 1:]
        branch_dct = super().get(root_key, None)
        if branch_dct is None or not isinstance(branch_dct, dict):
            return default

        return branch_dct.get(branch_key, default)

    def __setitem__(self, key, value):
        if not isinstance(key, str) or '.' not in key:
            if isinstance(value, dict):
                value = DotNotationDict(value)
            return super().__setitem__(key, value)

        r_index = key.rfind('.')
        root_key = key[:r_index]
        leaf_key = key[r_index + 1:]

        next_dct, branch_key = self.__get_next_item(root_key)
        return self.__get_value_from_dotted_key(branch_key, next_dct).__setitem__(leaf_key, value)

    def forced_setitem(self, key: Any, value: Any):
        """If the key contains a dot, create the specified grouping and store the value

        :type key: Any
        :type value: Any
        """
        if not isinstance(key, str) or '.' not in key:
            return self.__setitem__(key, value)

        r_index = key.rfind('.')
        root_key = key[: r_index]
        leaf_key = key[r_index + 1:]

        branch_dct, branch_key = self.__get_next_item(root_key)
        return self.__get_dict_from_dotted_key(branch_key, branch_dct, True).__setitem__(leaf_key, value)

    def __delitem__(self, key):
        if not isinstance(key, str) or '.' not in key:
            return super().__delitem__(key)

        r_index = key.rfind('.')
        root_key = key[:r_index]
        leaf_key = key[r_index + 1:]

        next_dct, branch_key = self.__get_next_item(root_key)
        return self.__get_value_from_dotted_key(branch_key, next_dct).__delitem__(leaf_key)

    def __get_next_item(self, key) -> Tuple[str, str, dict]:
        if '.' not in key:
            return self, key
        l_index = key.find('.')
        root_key = key[: l_index]
        branch_key = key[l_index + 1:]
        if root_key not in self:
            self[root_key] = {}
        return super().__getitem__(root_key), branch_key

    def __get_dict_from_dotted_key(self, key, dct, forced=False) -> dict:
        if not isinstance(key, str) or '.' not in key:
            if forced and not (key in dct and isinstance(dct[key], dict)):
                dct[key] = DotNotationDict()
            return dct[key]

        index = key.find('.')
        dict_key = key[: index]

        next_key = key[index + 1:]
        if forced and dict_key not in dct:
            dct[dict_key] = DotNotationDict()
        next_dct = dct[dict_key]
        return self.__get_dict_from_dotted_key(next_key, next_dct, forced)

    def __contains__(self, key) -> bool:
        if not isinstance(key, str) or '.' not in key:
            return super().__contains__(key)

        root_key = key[:key.find('.')]
        if root_key not in self:
            return False

        dct = self[root_key]
        if not isinstance(dct, dict):
            return False

        key = key[key.find('.') + 1:]

        while isinstance(dct, dict) and '.' in key:
            if key not in dct:
                return False

            root_key = key[:key.find('.')]
            if root_key not in dct:
                return False

            dct = dct[root_key]
            if not isinstance(dct, dict):
                return False

            key = key[key.find('.') + 1:]

        return key in dct

    # TODO def items(self, is_recursive=False, is_dfs=True):
    # Return "dict_items" and integrate it into dict.items
    def items(self, recursive=False, is_dfs=True) -> Iterable[Tuple[Any, Any]]:
        """Returns a key/value pair.

        :param recursive: If True, it returns the key and value of the leaf value. Defaults to False
        :type recursive: bool, optional
        :param is_dfs: Whether the transformation order should be depth-first or breadth-first search., defaults to True
        :type is_dfs: bool, optional
        :rtype: Iterable[Tuple[Any, Any]]
        """
        if not recursive:
            return super().items()

        items = []
        deq = deque()
        for key, value in super().items():
            if isinstance(value, dict):
                item = (key, value)
                deq.appendleft(item) if is_dfs else deq.append(item)
            else:
                items.append((key, value))

        while len(deq) != 0:
            ancestor_key, dct = deq.pop() if is_dfs else deq.popleft()

            for key, value in dct.items():
                if isinstance(value, dict):
                    deq.append((f'{ancestor_key}.{key}', value))
                else:
                    items.append((f'{ancestor_key}.{key}', value))

        return items

    def keys(self, recursive=False, is_dfs=True) -> List[Any]:
        """Returns a list of keys

        :param recursive: If True, it returns the key and value of the leaf value. Defaults to False
        :type recursive: bool, optional
        :param is_dfs: Whether the transformation order should be depth-first or breadth-first search., defaults to True
        :type is_dfs: bool, optional
        :rtype: Iterable[Any]
        """
        return sum([item[0] if isinstance(item[0], list) else [item[0]] for item in self.items(recursive, is_dfs)], []) if recursive else super().keys()

    def values(self, recursive=False, is_dfs=True) -> List[Any]:
        """Return a list of values

        :param recursive: If True, it returns the key and value of the leaf value. Defaults to False
        :type recursive: bool, optional
        :param is_dfs: Whether the transformation order should be depth-first or breadth-first search., defaults to True
        :type is_dfs: bool, optional
        :rtype: Iterable[Any]
        """
        return sum([item[1] if isinstance(item[1], list) else [item[1]] for item in self.items(recursive, is_dfs)], []) if recursive else super().values()


class RestrictedList:
    """A restricted list of elements that can be included.
    """

    def __init__(self, ElementClass, *args, **kwargs):
        """Default constructor

        :param ElementClass: Classes that can be included in the element
        :type ElementClass: Union[Tuple[Type of class, ...], Type of class]
        """
        self.__ElementClass = ElementClass
        self.__list = list(*args, **kwargs)

        if any([not isinstance(element, self.__ElementClass) for element in self]):
            raise TypeError(f'Element should be instance of "{self.__ElementClass}".')

    def __iter__(self):
        return self.__list.__iter__()

    def __getitem__(self, key):
        return self.__list.__getitem__(key)

    def __setitem__(self, key, value):
        if not isinstance(value, self.__ElementClass):
            raise TypeError(f'Can not include anything other than an instance of "{self.__ElementClass}".')

        return self.__list.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__list.__delitem__(key)

    def __contains__(self, key):
        return self.__list.__contains__(key)

    def __add__(self, value):
        if isinstance(value, list) and any([not isinstance(element, self.__ElementClass) for element in value]):
            raise TypeError(f'Can not include anything other than an instance of "{self.__ElementClass}".')

        return self.__list.__add__(value)

    def __iadd__(self, value):
        if isinstance(value, list) and any([not isinstance(element, self.__ElementClass) for element in value]):
            raise TypeError(f'Can not include anything other than an instance of "{self.__ElementClass}".')

        return super().__iadd__(value)

    def __len__(self):
        return self.__list.__len__()

    def append(self, object):
        """Same as default list.
        """
        if not isinstance(object, self.__ElementClass):
            raise TypeError(f'Can not include anything other than an instance of "{self.__ElementClass}".')

        return self.__list.append(object)

    def insert(self, index, object):
        """Same as default list.
        """
        if isinstance(object, list) and any([not isinstance(element, self.__ElementClass) for element in object]):
            raise TypeError(f'Can not include anything other than an instance of "{self.__ElementClass}".')

        return self.__list.insert(index, object)

    def extend(self, iterable):
        """Same as default list.
        """
        if any([not isinstance(element, self.__ElementClass) for element in iterable]):
            raise TypeError(f'Element should be instance of "{self.__ElementClass}".')

        return self.__list.extend(iterable)

    def remove(self, x):
        """Same as default list.
        """
        self.__list.remove(x)

    def pop(self, i=-1):
        """Same as default list.
        """
        self.__list.pop

    def clear(self):
        """Same as default list.
        """
        self.__list.clear()

    def index(self, x, start=0, end=-1):
        """Same as default list.
        """
        return self.__list.index(x, start, end)

    def count(self, x):
        """Same as default list.
        """
        return self.__list.count(x)

    def reverse(self):
        """Same as default list.
        """
        return self.__list.reverse()

    def copy(self):
        """Same as default list.
        """
        return self.__list.copy


def FormatArguments(design: dict, *args, **kw) -> dict:
    key_list = design.keys()
    if any([key not in key_list for key in kw.keys()]):
        raise TypeError()

    if len(args) + len(kw) > len(key_list):
        raise TypeError()

    value_dict = {}
    index = 0
    for key, value in design.items():
        if key in kw:
            value_dict[key] = kw[key]
        elif index < len(args):
            value_dict[key] = args[index]
            index += 1
        else:
            value_dict[key] = value

    return value_dict


def GetFileName(path: str) -> str:
    """Get the name of the file from the path

    :type path: str
    :rtype: str
    """
    return splitext(basename(path))[0]


def GetFileExtention(path: str) -> str:
    """Get extension from path

    :type path: str
    :rtype: str
    """
    return splitext(basename(path))[1]


def Camel2Pascal(camel: str) -> str:
    """Convert from Camel to Pascal format.

    e.g. HogeTitle -> Hoge Title

    :type camel: str
    :rtype: str
    """
    return camel[0] + ''.join([' ' + c if c.isupper() else c for c in camel[1:]])


def Camel2Const(camel: str) -> str:
    """Convert from Camel to Const format.

    e.g. HogeTitle -> HOGE_TITLE

    :type camel: str
    :rtype: str
    """
    return camel[0] + ''.join(['_' + c if c.isupper() else c.upper() for c in camel[1:]])


def GetShowPanelLabel(panel: Panel) -> str:
    """Get the label to be displayed on the menu item from the panel.

    :type panel: Panel
    :rtype: str
    """
    return f'Show {Camel2Pascal(panel.__class__.__name__)}'


def GetExtension(wildcard: str) -> str:
    """Get the extension from the wildcard.

    :param wildcard: Please refer to wxPython (https://docs.wxpython.org/wx.FileDialog.html?highlight=filedialog#wx.FileDialog) for details.
    :type wildcard: str
    :rtype: str
    """
    wildcard = wildcard[wildcard.rfind('|') + 1:]
    wildcard = wildcard[wildcard.find('.'):]
    return wildcard.strip()


def InterpolateValue(x: float, xy0: Tuple[float, float], xy1: Tuple[float, float]) -> float:
    """Get the position of x on the line between xy0 and xy1.

    :type x: float
    :type xy0: Tuple[float, float]
    :type xy1: Tuple[float, float]
    :return: y
    :rtype: float
    """
    if xy0[0] < xy1[0]:
        min_xy = xy0
        max_xy = xy1
    else:
        min_xy = xy1
        max_xy = xy0

    a = (max_xy[1] - max_xy[1]) / (max_xy[0] - min_xy[0])
    b = min_xy[1] - a * min_xy[0]

    return a * x + b


def DotChain(*args) -> str:
    """Returns a list of the given characters, separated by dots.

    :rtype: str
    """
    return '.'.join(args)


def FindWindowToAncestors(window: Window, Class):
    """Find instances of the given class by tracing the ancestors of the given window.

    :type window: Window
    :type Class: Class
    :rtype: Any
    """
    if not isinstance(window, Window):
        return None

    if isinstance(window, Class):
        return window

    return FindWindowToAncestors(window.Parent, Class)


def HasValidElement(iterable: Iterable, cls_) -> bool:
    """Checks if the given iterable element is an instance of the given class.

    :type iterable: Iterable
    :type cls_: Class
    :rtype: bool
    """
    return all([isinstance(element, cls_) for element in iterable])


__all__ = [
    'Singleton',
    'DotNotationDict',
    'RestrictedList',
    'FormatArguments',
    'GetFileName',
    'GetFileExtention',
    'Camel2Pascal',
    'Camel2Const',
    'GetShowPanelLabel',
    'GetExtension',
    'InterpolateValue',
    'DotChain',
    'FindWindowToAncestors',
    'HasValidElement',
]

if __name__ == "__main__":
    test_data = {
        'PROJECT': {
            'DATA': {
                'LIST': {
                    'NEXT': 9
                }
            },
            'NAME': {
                'NEXT': 'New Project'
            },
            'PATH': {
                'PREVIOUS': '',
                'NEXT': ''
            }
        },
    }
    dotdict = DotNotationDict(test_data)

    # print('PROJECT' in dotdict)
    # print('PROJECT.DATA' in dotdict)
    # print('PROJECT.NAME.NEXT' in dotdict)
    # print('PROJECT.PATH.PREVIOUS' in dotdict)

    # print('PROJECT.PATH.NEXT' in dotdict)
    # print('PROJECT.DATA.LIST.NEXT.PIYO' in dotdict)
    # print('PROJECT.DATA.NEXT' in dotdict)
