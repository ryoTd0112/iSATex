from abc import abstractmethod
from collections import deque
from copy import deepcopy
from datetime import date
from os.path import basename, dirname, isdir, join
from random import random
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, final

from numpy import array, cos, exp, inf, log, ndarray, sin, zeros
from wx import FileSelectorDefaultWildcardStr

from core import RestrictedStorableListBase, StorableObject
from util import GetFileName, HasValidElement

# default value is not storable


class ArgumentContainerBase(StorableObject):
    """This class is for connecting the argument and the UI.
    """

    def __init__(self, default=None):
        """Default constructor
        :param default: default value.
        """
        self.__value = None
        self.SetValue(default)
        self.__default = self.GetValue()

    def GetValue(self) -> Any:
        """Return contain value. If contain invalid value, return default value. This value is deepcopied.

        :return: contain value
        :rtype: Any
        """
        v = self.__value if self.HasValidValue() else self.__default
        return deepcopy(v)

    def SetValue(self, v):
        """
        This function manage to convert value to a valid type as much as possible,
        even if it can't, it will accept the value.

        :param v: Set value
        :type v: Any
        """
        self.__value = v

    @final
    def GetDefault(self) -> Any:
        """Get default value.

        :rtype: Any
        """
        return deepcopy(self.__default)

    def IsValidValue(self, value) -> bool:
        """Returns True if the given value is valid. This method is intended to be overridden.

        :type value: Whether the valid value.
        :rtype: bool
        """
        return True

    def HasValidValue(self) -> bool:
        """Returns True if the contain value is valid.

        :rtype: bool
        """
        return self.IsValidValue(self.__value)

    @final
    def __str__(self):
        v = self.GetValue()
        return '' if v is None else str(self.GetValue())

    def __add__(self, other):
        return self.__value.__add__(other)

    def __sub__(self, other):
        return self.__value.__sub__(other)

    def __mul__(self, other):
        return self.__value.__mul__(other)

    def __matmul__(self, other):
        return self.__value.__matmul__(other)

    def __truediv__(self, other):
        return self.__value.__truediv__(other)

    def __floordiv__(self, other):
        return self.__value.__floordiv__(other)

    def __mod__(self, other):
        return self.__value.__mod__(other)

    def __pow__(self, other):
        return self.__value.__pow__(other)

    def __lshift__(self, other):
        return self.__value.__lshift__(other)

    def __rshift__(self, other):
        return self.__value.__rshift__(other)

    def __and__(self, other):
        return self.__value.__and__(other)

    def __xor__(self, other):
        return self.__value.__xor__(other)

    def __or__(self, other):
        return self.__value.__or__(other)

    def __radd__(self, other):
        return self.__value.__radd__(other)

    def __rsub__(self, other):
        return self.__value.__rsub__(other)

    def __rmul__(self, other):
        return self.__value.__rmul__(other)

    def __rmatmul__(self, other):
        return self.__value.__rmatmul__(other)

    def __rtruediv__(self, other):
        return self.__value.__rtruediv__(other)

    def __rfloordiv__(self, other):
        return self.__value.__rfloordiv__(other)

    def __rmod__(self, other):
        return self.__value.__rmod__(other)

    def __rpow__(self, other):
        return self.__value.__rpow__(other)

    def __rlshift__(self, other):
        return self.__value.__rlshift__(other)

    def __rrshift__(self, other):
        return self.__value.__rrshift__(other)

    def __rand__(self, other):
        return self.__value.__rand__(other)

    def __rxor__(self, other):
        return self.__value.__rxor__(other)

    def __ror__(self, other):
        return self.__value.__ror__(other)

    def __iadd__(self, other):
        return self.__value.__iadd__(other)

    def __isub__(self, other):
        return self.__value.__isub__(other)

    def __imul__(self, other):
        return self.__value.__imul__(other)

    def __imatmul__(self, other):
        return self.__value.__imatmul__(other)

    def __itruediv__(self, other):
        return self.__value.__itruediv__(other)

    def __ifloordiv__(self, other):
        return self.__value.__ifloordiv__(other)

    def __imod__(self, other):
        return self.__value.__imod__(other)

    def __ipow__(self, other):
        return self.__value.__ipow__(other)

    def __ilshift__(self, other):
        return self.__value.__ilshift__(other)

    def __irshift__(self, other):
        return self.__value.__irshift__(other)

    def __iand__(self, other):
        return self.__value.__iand__(other)

    def __ixor__(self, other):
        return self.__value.__ixor__(other)

    def __ior__(self, other):
        return self.__value.__ior__(other)

    def __neg__(self, other):
        return self.__value.__neg__(other)

    def __pos__(self, other):
        return self.__value.__pos__(other)

    def __abs__(self, other):
        return self.__value.__abs__(other)

    def __invert__(self, other):
        return self.__value.__invert__(other)

    def __complex__(self, other):
        return self.__value.__complex__(other)

    def __int__(self, other):
        return self.__value.__int__(other)

    def __float__(self, other):
        return self.__value.__float__(other)

    def __index__(self, other):
        return self.__value.__index__(other)

    def __round__(self, other):
        return self.__value.__round__(other)

    def __trunc__(self, other):
        return self.__value.__trunc__(other)

    def __floor__(self, other):
        return self.__value.__floor__(other)

    def __ceil__(self, other):
        return self.__value.__ceil__(other)

    def __eq__(self, other):
        return self.__value.__eq__(other)

    def __le__(self, other):
        return self.__value.__le__(other)

    def __lt__(self, other):
        return self.__value.__lt__(other)

    def SendSaveData(self):
        """Send contained value as save data.

        :rtype: Any
        """
        return self.GetValue()

    def ReceiveSaveData(self, save_data):
        """Receive saved data.

        :type save_data: Any
        """
        self.SetValue(save_data)


class BoundedArgumentContainerBase(ArgumentContainerBase):
    """Contains numbers and their bounds. This value displayed by Entry.
    """

    def __init__(self, default: Union[int, float, None] = 0, min_: Union[int, float, None] = None, max_: Union[int, float, None] = None):
        """Default constractor
        :param default: default value
        :type default: Union[int, float, None]
        :param min: minimum value, should be lesser than or equal to "max", if None convert infinity, defaults to None
        :type min: Union[int, float, None], optional
        :param max: maxmum value, should be greater than or equal to "min" if None convert  negative infinity, defaults to None
        :type max: Union[int, float, None], optional
        """
        self.__min = - inf if min_ is None else min_
        self.__max = inf if max_ is None else max_

        if not isinstance(self.__min, (int, float)):
            raise TypeError('"min_" should be instance of "int" or "float".')

        if not isinstance(self.__max, (int, float)):
            raise TypeError('"max_" should be instance of "int" or "float".')

        if not (default is None or isinstance(default, (int, float))):
            raise TypeError('"default" should be instance of "int" or "float" or "None".')

        if not (default is None or (self.__min <= default <= self.__max)):
            raise ValueError(f'Please set valid bound. "default" value of {default} is not in bounds of {[self.__min, self.__max]}')

        super().__init__(default)

    def IsValidValue(self, value: Union[int, float, None]) -> bool:
        """Returns True if the value is within the specified bounds.

        :param value: Value to be contained.
        :type value: Union[int, float, None]
        :rtype: bool
        """
        if value is None or (self.__min <= value <= self.__max):
            return True
        else:
            return False

    def GetMin(self) -> Union[int, float]:
        """Get the specified minimum value.

        :rtype: Union[int, float]
        """
        return self.__min

    def GetMax(self) -> Union[int, float]:
        """Get the specified maximum value.

        :rtype: Union[int, float]
        """
        return self.__max

    def GetBounds(self) -> Tuple[Union[int, float], Union[int, float]]:
        """Get the specified bounds.

        :rtype: Union[int, float]
        """
        return self.__min, self.__max

    def SendSaveData(self) -> Tuple[Union[int, float], Union[int, float], Union[int, float]]:
        """Send contained value and bounds as save data.

        :rtype: Tuple[Union[int, float], Union[int, float], Union[int, float]]
        """
        return (self.GetValue(), self.__min, self.__max,)

    def ReceiveSaveData(self, save_data: Tuple[Union[int, float], Union[int, float], Union[int, float]]):
        """Receive saved data.

        :param save_data: (value, min, max,)
        :type save_data: Tuple[Union[int, float], Union[int, float], Union[int, float]]
        """
        self.SetValue(save_data[0])
        self.__min = save_data[1]
        self.__max = save_data[2]


class OptionalIntContainer(BoundedArgumentContainerBase):
    """Contains Int or None.
    """

    def __init__(self, default: Optional[int] = 0, min_: Union[int, float, None] = None, max_: Union[int, float, None] = None):
        if not (default is None or isinstance(default, int)):
            raise TypeError('"default" should be instance of "int" or "None".')

        super().__init__(default, min_, max_)

    def SetValue(self, v):
        """Convert as much as possible to int or None and save the value.

        :type v: Any
        """

        if v is not None:
            try:
                v = int(v)
            except ValueError:
                pass
        super().SetValue(v)

    def IsValidValue(self, value: Optional[int]) -> bool:
        """Return True, if "value" is instance of int or None and within the specified bounds.

        :return: Whether the valid value.
        :rtype: bool
        """
        return value is None or (isinstance(value, int) and super().IsValidValue(value))


class IntContainer(OptionalIntContainer):
    """Contain int.
    """

    def __init__(self, default: int = 0, min_: Union[int, float, None] = None, max_: Union[int, float, None] = None):
        """Default constractor

        :param default: default value, defaults to 0
        :type default: int, optional
        :param min_: minimum value, should be lesser than or equal to "max", if None convert infinity, defaults to None
        :type min_: Union[int, float, None], optional
        :param max_: maxmum value, should be greater than or equal to "min", if None convert negative infinity, defaults to None
        :type max_: Union[int, float, None], optional
        """
        if not isinstance(default, int):
            raise TypeError('"default" should be instance of "int"')

        super().__init__(default, min_, max_)

    def IsValidValue(self, value: int) -> bool:
        """Return True, if "value" is instance of int and within the specified bounds.

        :return: Whether the valid value.
        :rtype: bool
        """
        return value is not None and super().IsValidValue(value)


class OptionalFloatContainer(BoundedArgumentContainerBase):
    """Contain float, like "OptionalIntContainer" class.
    """

    def __init__(self, default: Optional[float] = 0.0, min_: Union[int, float, None] = None, max_: Union[int, float, None] = None):
        """Default constructor

        :param default: default value, defaults to 0.0
        :type default: Optional[float], optional
        :param min_: minimum value, should be lesser than "max", defaults to None
        :type min_: Optional[int], optional
        :param max_: maximam value, should be greater than "min", defaults to None
        :type max_: Optional[int], optional
        """
        if default is not None:
            default = float(default)
        if not (default is None or isinstance(default, float)):
            raise TypeError('"default" should be instance of "float" or "None".')

        super().__init__(default, min_, max_)

    def SetValue(self, v):
        """Convert as much as possible to float or None and save the value.

        :type v: Any
        """
        if v is not None:
            try:
                v = float(v)
            except ValueError:
                pass

        super().SetValue(v)

    def IsValidValue(self, value: Optional[float]) -> bool:
        """Return True, if "value" is instance of float or None and within the specified bounds.

        :return: Whether the valid value.
        :rtype: bool
        """
        return value is None or (isinstance(value, float) and super().IsValidValue(value))


class FloatContainer(OptionalFloatContainer):
    """Contain float.
    """

    def __init__(self, default: float = 0.0, min_: Union[int, float, None] = None, max_: Union[int, float, None] = None):
        """Default constructor

        :param default: default value, defaults to 0
        :type default: float, optional
        :param min: minimum value, should be lesser than or equal to "max", if None convert infinity, defaults to None
        :type min: Union[int, float, None], optional
        :param max: maxmum value, should be greater than or equal to "min", if None convert negative infinity, defaults to None
        :type max: Union[int, float, None], optional
        """
        default = float(default)
        if not isinstance(default, float):
            raise TypeError('"default" should be instance of "float"')

        super().__init__(default, min_, max_)

    def IsValidValue(self, value: float) -> bool:
        """Return True, if "value" is instance of float and within the specified bounds.

        :return: Whether the valid value.
        :rtype: bool
        """
        return value is not None and super().IsValidValue(value)


class StrContainer(ArgumentContainerBase):
    """Contain str.
    """

    def __init__(self, default: str = ''):
        """Default constructor

        :param default: default value, defaults to ''
        :type default: str, optional
        """
        if not isinstance(default, str):
            raise TypeError('"default" should be instance of "str"')

        super().__init__(default)

    def IsValidValue(self, value: str) -> bool:
        """Return True, if "value" is instance of int or None and within the specified bounds.

        :return: Whether the valid value.
        :rtype: bool
        """
        if not isinstance(value, str):
            return False

        return True


class ChoiceContainer(ArgumentContainerBase):
    """Contain choice. This value displayed by ComboBox.
    """

    def __init__(self, default='', choices=None):
        """Default constructor.

        :param default: default value, defaults to ''
        :type default: str, optional
        :param choices: list of options, if "choices" is None, [default] will be used, default to None
        :type choices: [type], optional
        """
        if not isinstance(default, (int, float, str)):
            raise TypeError('"default" should be instance of "int" or "float", "str".')

        self.__choices = [default] if choices is None else choices
        super().__init__(default)

    @final
    def IsValidValue(self, value) -> bool:
        """Returns True if "value" is included in the "choices".

        :return: Whether the valid value.
        :rtype: bool
        """
        return value in self.__choices

    @final
    def GetChoices(self) -> Tuple[Union[int, float, str], ...]:
        """Get choices.

        :rtype: Tuple[Union[int, float, str], ...]
        """

        return self.__choices

    def SendSaveData(self) -> Tuple[Union[int, float, str], Tuple[Union[int, float, str], ...]]:
        """Send contained value and choices as save data.

        :return: [description]
        :rtype: Tuple[Union[int, float, str], Tuple[Union[int, float, str], ...]]
        """
        return (self.GetValue(), self.GetChoices(),)

    def ReceiveSaveData(self, save_data: Tuple[Union[int, float, str], Tuple[Union[int, float, str], ...]]):
        """Receive saved data.

        :param save_data: (value, choices)
        :type save_data: Tuple[Union[int, float, str], Tuple[Union[int, float, str], ...]]
        """
        self.SetValue(save_data[0])
        self.__choices = save_data[1]


class IterableArgumentContainerBase(ArgumentContainerBase):
    """Contain iterable
    """

    def __init__(self, arg_container_list: Union[List[ArgumentContainerBase], None] = None):
        """Default constructor

        :param arg_container_list: List of instance of argcontainer, defaults to None
        :type arg_container_list: Union[List[ArgumentContainerBase], None], optional
        """
        if arg_container_list is None:
            arg_container_list = []

        if not all([isinstance(arg_container, ArgumentContainerBase) for arg_container in arg_container_list]):
            raise TypeError('Element of "arg_container" should be instance of "ArgumentContainerBase".')

        self.arg_container_list = arg_container_list

        default = self.GetValue()
        super().__init__(default)

    def GetValue(self) -> list:
        """Get value.

        :rtype: list
        """
        return [arg_container.GetValue() for arg_container in self.arg_container_list]

    def SetValue(self, values: Union[str, Iterable]):
        """Convert as much as possible to iterable and save the value. If it cannot be converted, it will save the list with empty str as an element instead.
        """
        if not isinstance(values, str):
            values = repr(values)
        try:
            values = eval(values)
        except (ValueError, TypeError, SyntaxError, NameError):
            values = [''] * len(self.arg_container_list)

        for i, c in enumerate(self.arg_container_list):
            if i < len(values):
                c.SetValue(values[i])
            else:
                c.SetValue('')

    def IsValidValue(self, value: list) -> bool:
        """Returns True if "value" is valid value. This method is intended to be overridden.

        :return: Whether the valid value.
        :rtype: bool
        """
        return True

    def HasValidValue(self) -> bool:
        """Returns True if the contain value is valid.

        :rtype: bool
        """
        value = self.GetValue()
        # for c in self.arg_container_list:
        #     if not c.HasValidValue():
        #         return False

        # if not self.IsValidValue(value):
        #     return False

        # return True
        return all([c.HasValidValue() for c in self.arg_container_list]) and self.IsValidValue(value)

    @final
    def __iter__(self):
        return self.arg_container_list.__iter__()

    @final
    def __getitem__(self, key):
        return self.arg_container_list[key]

    @final
    def __len__(self):
        return len(self.arg_container_list)

    def SendSaveData(self) -> Tuple[ArgumentContainerBase, ...]:
        """Send contained list of ArgumentContainerBase class as save data.

        :rtype: Tuple[ArgumentContainerBase, ...]
        """
        return self.arg_container_list

    def ReceiveSaveData(self, save_data: Tuple[ArgumentContainerBase, ...]):
        """Receive saved data.

        :type save_data: Tuple[ArgumentContainerBase, ...]
        """
        self.arg_container_list = save_data


class ListArgumentContainer(IterableArgumentContainerBase):
    @final
    def GetValue(self) -> list:
        """Return contain value. If contain invalid value, return default value. This value is deepcopied.

        :rtype: list
        """
        return list(super().GetValue())

    def IsValidValue(self, value) -> bool:
        """Return True, if "value" is instance of list class.

        :return: Whether the valid value.
        :rtype: bool
        """
        return isinstance(value, List)

    @final
    def __setitem__(self, key, value):
        if not isinstance(value, ArgumentContainerBase):
            raise ValueError

        self.arg_container_list[key] = value


class TupleArgumentContainer(IterableArgumentContainerBase):
    @final
    def GetValue(self) -> Tuple:
        """Return contain value. If contain invalid value, return default value. This value is deepcopied.

        :return: [description]
        :rtype: Tuple
        """
        return tuple(super().GetValue())

    def IsValidValue(self, value) -> bool:
        """Return True, if "value" is instance of tuple class.

        :return: Whether the valid value.
        :rtype: bool
        """
        return isinstance(value, Tuple)


class FunctionContainerBase(StorableObject):
    """This class is for connecting the function and the UI.
    """

    def __init__(self, arg_container_dict: Dict[str, ArgumentContainerBase] = None):
        """Default container

        :param arg_container_dict: The argument dictionary, key, is used as the name of the argument, defaults to None
        :type arg_container_dict: Dict[str, ArgumentContainerBase], optional
        """
        arg_container_dict = {} if arg_container_dict is None else arg_container_dict
        self.arg_container_dict = {}
        for key, value in arg_container_dict.items():
            if not isinstance(key, str):
                raise TypeError()

            if not isinstance(value, ArgumentContainerBase):
                raise TypeError()

            self.arg_container_dict[key] = value

    @abstractmethod
    def Function(self) -> Any:
        """Describe the body of the function. This method is intended to be overridden.

        :raises NotImplementedError: Error sent if the method is not overridden.
        :rtype: Any
        """
        raise NotImplementedError()

    def GetArgumentNames(self) -> Tuple[str, ...]:
        """Get tuple of argument names

        :rtype: Tuple[str, ...]
        """
        return tuple(self.GetArgumentContainerDict())

    def GetArgumentContainerList(self) -> Tuple[ArgumentContainerBase, ...]:
        """Get tuple of argument containers

        :rtype: Tuple[ArgumentContainerBase, ...]
        """
        return tuple(self.GetArgumentContainerDict().values())

    def GetArgumentContainerDict(self) -> Dict[str, ArgumentContainerBase]:
        """Get argument container dict.

        :rtype: Dict[str, ArgumentContainerBase]
        """
        return self.arg_container_dict

    def GetArgs(self) -> Tuple[Any, ...]:
        """Get the value of the argument.

        :rtype: Tuple[Any, ...]
        """
        return tuple([c.GetValue() for c in self.GetArgumentContainerList()])

    def SetArgs(self, args: Union[Dict[str, Any], Iterable[Any]]):
        """
        Sets the value of the argument.
        If the number of "args" is less, the value will be reflected as much as possible.
        If the number of "args" is greater, the excess will be ignored.

        :param args: Argument values
        :type args: Union[Dict[str, Any], Iterable[Any, ...]]
        """
        if isinstance(args, dict):
            arg_container_dict = self.GetArgumentContainerDict()
            for key, value in args:
                arg_container_dict[key].SetValue(value)
        else:
            for arg, container in zip(args, self.GetArgumentContainerList()):
                container.SetValue(arg)

    @final
    def HasValidArguments(self) -> bool:
        """Return True, If the arguments have the correct value

        :rtype: bool
        """
        args = self.GetArgs()
        return all([c.HasValidValue() for c in self.GetArgumentContainerList()]) and self.IsGoodCondition(*args)

    def IsGoodCondition(self, *args) -> bool:
        """
        Returns true if the argument satisfies the condition.
        Unlike HasValidArguments, this method checks the conditions between arguments, such as whether they are large or small.
        This method is intended to be overridden.
        :rtype: bool
        """
        return True

    def GetHelpText(self) -> str:
        """Returns text to help understand the "Function".

        :rtype: str
        """
        return 'Sorry, but there was no help available.'

    def __str__(self):
        return f'{self.__class__.__name__}{str(self.GetArgs())}'

    def SendSaveData(self) -> Tuple[Any, ...]:
        """Send contained argument as save data.

        :rtype: Tuple[Any, ...]
        """
        return {key: value for key, value in zip(self.GetArgumentNames(), self.GetArgs())}

    def ReceiveSaveData(self, save_data: Tuple[Any, ...]):
        """Receive saved data

        :type save_data: Tuple[Any, ...]
        """
        for key, value in save_data.items():
            if key not in self.arg_container_dict:
                continue

            self.arg_container_dict[key].SetValue(value)


class PeakFunctionContainerBase(FunctionContainerBase):
    """Contain function of peak
    """
    @abstractmethod
    def Function(self, x, args: Tuple) -> ndarray:
        """Describe the formula for calculating the peak.

        :param x: xdata of spectral data
        :type x: ndrray
        :param args: The peak arguments. The specified value will be passed. If you want to know more details, please refer the "__init__" document for how to specify them.
        :type args: Tuple
        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()

    def Execution(self, x) -> ndarray:
        """ "Function" wrapper

        :param x: xdata of spectral data
        :type x: Iterable
        :return: Value of the peak for the given x
        :rtype: ndarray
        """
        return self.Function(x, self.GetArgs())

    @property
    def Amp(self) -> float:
        """Amplitude

        :type: float
        """
        return self.GetArgumentContainerList()[0].GetValue()

    @Amp.setter
    def Amp(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError

        self.GetArgumentContainerList()[0].SetValue(max(value, 0.0))

    @property
    def Ctr(self) -> float:
        """Center position of peak

        :type: float
        """
        return self.GetArgumentContainerList()[1].GetValue()

    @Ctr.setter
    def Ctr(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError

        self.GetArgumentContainerList()[1].SetValue(value)

    @property
    def Wid(self) -> float:
        """Width of peak, like half maximum full width (HMFW).

        :type: float
        """
        return self.GetArgumentContainerList()[2].GetValue()

    @Wid.setter
    def Wid(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError

        self.GetArgumentContainerList()[2].SetValue(max(value, 0.0))

    def SetArgs(self, args):
        """Set arguments(amp, ctr, wid, etc...) of peak.　amp and wid will be converted to 0 or more.

        :param args: argument of peak.
        """
        args[0] = max(args[0], 0.0)
        args[2] = max(args[2], 0.0)
        super().SetArgs(args)

    @abstractmethod
    def GetTex(self) -> str:
        """Get statement of function following the Tex syntax.

        :raises NotImplementedError: Error sent if the method is not overridden.
        :return: Statement of Tex.
        :rtype: str
        """
        raise NotImplementedError()


class Gaussian(PeakFunctionContainerBase):
    """Gaussian. Default peak on iSATex
    """

    def __init__(self):
        amp = FloatContainer(1.0, min_=0.0)
        ctr = FloatContainer()
        wid = FloatContainer(1.0, min_=0.0)
        super().__init__({'Amplitude': amp, 'Center': ctr, 'Width': wid})

    def Function(self, x, args):
        return args[0] * exp(- 4 * log(2) * ((x - args[1]) / args[2]) ** 2) if args[2] != 0 else 1e10

    def GetTex(self):
        return r'$Amp\ exp\left(-4\ \ln{2}\left( \frac{x - Ctr}{Wid}\right)^2 \right)$'


class SpectrumFunctionContainerBase(FunctionContainerBase):
    """Contain function on spectral data
    """
    _instance_list = []
    data_accessor = None

    def __new__(cls, *args, **kwargs):
        self = super(SpectrumFunctionContainerBase, cls).__new__(cls)
        cls._instance_list.append(self)
        return self

    def Execution(self, x: Iterable, y: Iterable, bg: Iterable, peaks: Iterable[PeakFunctionContainerBase]):
        """ "Function" wrapper

        :param x: xdata of spectrum
        :type x: Iterable
        :param y: ydata of spectrum
        :type y: Iterable
        :param bg: background of spectrum
        :type bg: Iterable
        :param peaks: peak of spectrum
        :type peaks: Iterable[PeakFunctionContainerBase, ...]
        :rtype: Any
        """
        args = []
        for require in self.SendRequireParams():
            if require == 'x':
                args.append(x)
            elif require == 'y':
                args.append(y)
            elif require == 'b':
                args.append(bg)
            elif require == 'p':
                args.append(peaks)

        args += self.GetArgs()

        return self.Function(args)

    @abstractmethod
    def Function(self, args):
        """Describe the body of the function here.

        :param args: The parameters specified in "SendRequireParams". If you want to know more details, please refer to the documentation of "SendRequireParams".
        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()

    def SendRequireParams(self) -> str:
        """Send the required parameters.

        :return: Send the required parameters. 'x', 'y', 'b', and 'p' can be specified. If you specify 'xyp', the arguments passed to 'Function' are x, y, and p of the spectral data.
        :rtype: str
        """
        return ''

    def SendReturnParams(self) -> str:
        """Send the return value of "Function".

        :return: Send the return parameters. If you want to know more details, please refer the "SendRequireParams" document for how to specify them.
        :rtype: str
        """
        return ''

    def OnPeakTypeChanged(self, event):
        """Called when the peak type is changed in the application. This method is intended to be overridden.

        :param event: Events with information about type of peak changes
        :type event: PeakTypeChangeEvent
        """
        pass


class EncodeFunctionContainerBase(FunctionContainerBase):
    """Contain function on encode. This class is used to load experimental data.
    """

    def __init__(self, arg_container_dict=None):
        super().__init__(arg_container_dict)
        if any([c not in self.SendReturnParams() for c in 'xy']):
            raise ValueError('Return value of "GetReturnParams" should be contains "x" and "y".')

    @final
    def Execution(self, contents: str):
        """ "Function" wrapper

        :param contents: The experimental data
        :type contents: str
        """
        return self.Function(contents, self.GetArgs())

    @abstractmethod
    def Function(self, contents: str, args):
        """Describe the body of the function here.

        :param contents: experimental data
        :type contents: str
        :param args: The parameters specified in "SendRequireParams". If you want to know more details, please refer to the documentation of "SendRequireParams".
        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()

    def SendReturnParams(self) -> str:
        """Send the return value of "Function".

        :return: Send the return parameters. If you want to know more details, please refer the "SendRequireParams" document for how to specify them. default to 'xy' and should contain 'xy'.
        :rtype: str
        """
        return 'xy'

    def SendFileTypeWildcard(self) -> str:
        """Send the supported file formats.

        :return: default to FileSelectorDefaultWildcardStr. If you want to know more details, please refer the wxPython document at (https://docs.wxpython.org/wx.functions.html?highlight=fileselector#wx.FileSelector).
        :rtype: str
        """
        return FileSelectorDefaultWildcardStr


class Text(EncodeFunctionContainerBase):
    def __init__(self):
        super().__init__({'Delimiter': ChoiceContainer('Comma', ['Colon', 'Tab', 'Space', 'Comma', 'Equals Sign', 'Semicolon'])})

    def Function(self, contents, args):
        xdata = []
        ydata = []
        delimiter_name, = self.GetArgs()
        delimiter_dict = {'Colon': ':', 'Tab': '\t', 'Space': ' ', 'Comma': ',', 'Equals Sign': '=', 'Semicolon': ';'}
        delimiter = delimiter_dict[delimiter_name]
        for line in contents.split('\n'):
            if line == '':
                continue

            x, y = map(float, line.split(delimiter))

            xdata.append(x)
            ydata.append(y)

        return xdata, ydata


class PeakFunctionContainerList(RestrictedStorableListBase):
    @classmethod
    def CreateDummyPeaks(cls, x=None, size=None):
        """Generate dummy data. Can be used for testing, etc.

        :param x: xdata, If "x" is none, it will be converted to an array of size 100, defaults to None
        :type x: ndrray, optional
        :param size: size of peaks, if size is none, then a value between 0 and 5 will be randomly selected, defaults to None
        :type size: int, optional
        :return: instance of PeakFunctionContainerList
        :rtype: PeakFunctionContainerList
        """
        peaks = PeakFunctionContainerList()
        x = array(range(300))
        size = int(random() * 5) if size is None else size
        for _ in range(size):
            peak = DEFAULT_PEAK
            peak.X = x
            peak.Amp = random()
            peak.Ctr = size * random()
            peak.Wid = size * random()
            peaks.append(peak)
        return peaks

    def __init__(self, *args, **kwargs):
        """List with elements restricted to PeakFunctionContainerBase
        """
        super().__init__(PeakFunctionContainerBase, *args, **kwargs)


class PeakType(StorableObject):
    """Data object for peak type
    """

    def __init__(self, peak_func_container: PeakFunctionContainerList = None):
        """Default constructor

        :param peak_func_container: The original peak function, defaults to None
        :type peak_func_container: PeakFunctionContainerList, optional
        """
        if peak_func_container is not None and not isinstance(peak_func_container, PeakFunctionContainerBase):
            raise TypeError()
        self.__peak_func_container = peak_func_container

    def GetName(self) -> str:
        """Get name of peak

        :rtype: str
        """
        return self.__peak_func_container.__class__.__name__

    def GetArgumentLength(self) -> int:
        """Get length of argument

        :rtype: int
        """
        return len(self.__peak_func_container.GetArgs())

    def GetArgumentNames(self) -> Tuple[str, ...]:
        """Get a list of argument names

        :rtype: Tuple[str, ...]
        """
        return self.__peak_func_container.GetArgumentNames()

    def GetArgumentContainerList(self) -> List[ArgumentContainerBase]:
        """Get a list of "ArgumentContainerBase" class. This value is deepcopied.

        :rtype: List[ArgumentContainerBase, ...]
        """
        return deepcopy(self.__peak_func_container.GetArgumentContainerList())

    def GetFunction(self) -> callable:
        """Get function of peak

        :rtype: callable
        """
        return self.__peak_func_container.Function

    def GetPeakInstance(self) -> PeakFunctionContainerBase:
        """Get an instance of the "PeakFunctionContainerBase" class contained. This value is deepcopied.

        :rtype: PeakFunctionContainerBase
        """
        return deepcopy(self.__peak_func_container)

    def GetHelpText(self) -> str:
        """Returns text to help understand the "Function".

        :rtype: str
        """
        return self.__peak_func_container.GetHelpText()

    def GetTex(self) -> str:
        """Get statement of function following the Tex syntax.

        :rtype: str
        """
        return self.__peak_func_container.GetTex()

    def SendSaveData(self) -> PeakFunctionContainerBase:
        """Send contained instance of peak.

        :rtype: PeakFunctionContainerBase
        """
        return (self.__peak_func_container,)

    def ReceiveSaveData(self, save_data) -> PeakFunctionContainerBase:
        """Receive saved data

        :type save_data: PeakFunctionContainerBase
        """
        self.__peak_func_container = save_data[0]


class Spectrum(StorableObject):
    """Data object for spectrum
    """

    @classmethod
    def CreateDummySpectrum(cls, size=100):
        """Generate dummy data. Can be used for testing, etc.

        :param size: data size, defaults to 100
        :type size: int, optional
        :rtype: Spectrum
        """
        x = array(range(size))
        y = cos([v + 0.05 * random() for v in x])
        bg = sin([0.05 * v + 0.01 * random() for v in x])
        peaks = PeakFunctionContainerList.CreateDummyPeaks(x)
        return Spectrum(x, y, bg, peaks)

    def __init__(self, x: ndarray = None, y: ndarray = None, bg: ndarray = None, peaks: PeakFunctionContainerList = None):
        """Default constructor

        :param x: xdata of spectrum. if x is None, x convert to empty ndarray. defaults to None
        :type x: ndarray, optional
        :param y: ydata of spectrum. y should be same size of x. if x is None or None, y convert to empty ndarray. defaults to None
        :type y: ndarray, optional
        :param bg: background of spectrum. bg should be same size of x or None. if bg is None, bg convert to empty ndarray. defaults to None
        :type bg: ndarray, optional
        :param peaks: peak of spectrum. if peaks is None, peaks convert to empty list, defaults to None
        :type peaks: PeakFunctionContainerList, optional
        :raises ValueError: [description]
        """
        self.__x = array([0]) if x is None else array(x)
        self.__y = array(zeros(self.__x.shape, dtype=float)) if y is None else array(y)
        self.__bg = array(zeros(self.__x.shape, dtype=float)) if bg is None or len(bg) == 0 else bg
        self.__peaks = PeakFunctionContainerList() if peaks is None else PeakFunctionContainerList(peaks)

        if not(len(self.__x) == len(self.__y) == len(self.__bg)):
            raise ValueError()

    @property
    def X(self) -> ndarray:
        """xdata of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        return deepcopy(self.__x)

    @X.setter
    def X(self, x):
        if len(x) != len(self.__y):
            raise TypeError('The length of "x" should be the same as the length of "y".')

        self.__x = array(x)
        for peak in self.__peaks:
            peak.X = self.__x

    @property
    def Y(self) -> ndarray:
        """ydata of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        return deepcopy(self.__y)

    @Y.setter
    def Y(self, y):
        if len(y) != len(self.__x):
            raise TypeError('The length of "y" should be the same as the length of "x".')

        self.__y = array(y)

    @property
    def XY(self) -> Tuple[ndarray, ndarray]:
        """data of spectrum. This value is deepcopied.

        :rtype: Tuple[ndarray, ndarray]
        """
        return deepcopy(self.__x), deepcopy(self.__y)

    @XY.setter
    def XY(self, x, y=None):
        if y is None:
            x, y = x

        if len(x) != len(y):
            raise TypeError('The length of "x" should be the same as the length of "y".')

        self.__x = array(x)
        self.__y = array(y)
        self.__bg = self.__x * 0
        for peak in self.__peaks:
            peak.X = self.__x

    @property
    def BackGround(self):
        return deepcopy(self.__bg)

    @BackGround.setter
    def BackGround(self, bg):
        """Background of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        if len(bg) != len(self.__x):
            raise TypeError('The length of "bg" should be the same as the length of "x".')

        self.__bg = array(bg)

    @BackGround.deleter
    def BackGround(self):
        self.__bg = array(zeros(self.__x.shape, dtype=float))

    @property
    def Peaks(self) -> PeakFunctionContainerList:
        """Peaks of spectrum. This value is deepcopied.

        :rtype: PeakFunctionContainerList
        """
        return deepcopy(self.__peaks)

    @Peaks.setter
    def Peaks(self, peaks):
        self.__peaks = PeakFunctionContainerList(peaks)

    @Peaks.deleter
    def Peaks(self):
        self.__peaks = PeakFunctionContainerList()

    def GetSize(self) -> int:
        """Get size of spectrum.

        :rtype: int
        """
        return len(self.__x)

    def SendSaveData(self) -> Tuple[ndarray, ndarray, ndarray, PeakFunctionContainerList]:
        """Send (x, y, background, peaks) as save data.

        :rtype: Tuple[ndarray, ndarray, ndarray, PeakFunctionContainerList]
        """
        return list(self.X), list(self.Y), list(self.BackGround), self.Peaks

    def ReceiveSaveData(self, save_data: Tuple[ndarray, ndarray, ndarray, PeakFunctionContainerList]):
        """Receive saved data

        :type save_data: Tuple[ndarray, ndarray, ndarray, PeakFunctionContainerList]
        """
        x, y, bg, self.__peaks = save_data
        self.__x = array(x)
        self.__y = array(y)
        self.__bg = array(bg)


# TODO Composite pattern of "RecipeFunctionContainerBase".
class Recipe(RestrictedStorableListBase):
    """Data object. Record the functions, their order, and the arguments that each function has.
    """

    def __init__(self, *args, **kwargs):
        """Default constructor
        """
        super().__init__(SpectrumFunctionContainerBase, *args, **kwargs)


class Preset(Recipe):
    """Data object for "Recipe" class with name.
    """

    def __init__(self, name: str = '', *args, **kwargs):
        """Default constructor

        :param name: name of preset, defaults to ''
        :type name: str, optional
        """
        super().__init__(*args, **kwargs)

        if not isinstance(name, str):
            raise TypeError('"name" should be instance of "str".')

        self.__name = name

    def GetName(self) -> str:
        """Get name of preset.

        :rtype: str
        """
        return self.__name

    def SendSaveData(self) -> Tuple[str, Iterable[SpectrumFunctionContainerBase]]:
        """Send name of preset and recipe as save data.

        :rtype: Tuple[str, Iterable[SpectrumFunctionContainerBase]]
        """
        return (self.GetName(), [element for element in self.__iter__()],)

    def ReceiveSaveData(self, save_data: Tuple[str, Iterable[SpectrumFunctionContainerBase]]):
        """Receive saved data

        :type save_data: Tuple[str, Iterable[SpectrumFunctionContainerBase]]
        """
        self.__name = save_data[0]
        self.extend(save_data[1])


class SpectrumFunctionContainerAccessor:
    """Utility class for letting "PeakType" class access data
    """

    def __init__(self, data_mgr, peak_mgr):
        """Default constructor

        :param data_mgr: Manager of data
        :type data_mgr: DataManager
        :param peak_mgr: Manager of peak
        :type peak_mgr: PeakManager
        """
        self.__data_mgr = data_mgr
        self.__peak_mgr = peak_mgr

    def GetPeakType(self) -> PeakType:
        """Get selected type of peak

        :rtype: PeakType
        """
        return self.__peak_mgr.GetSelectedPeakType()

    def GetRecipe(self) -> Recipe:
        """Get selected "Recipe"

        :rtype: Recipe
        """
        return self.__data_mgr.GetSelectedRecipe()

    def GetDataSize(self) -> int:
        """Get the number of data being loaded.

        :rtype: int
        """
        return self.__data_mgr.GetDataSize()


class DataContainer(StorableObject):
    """Recoverable data object
    """
    @classmethod
    def CreateDummyData(cls, spectrum_size=100):
        """Generate dummy data. Can be used for testing, etc.

        :param spectrum_size: size of spectrum, defaults to 100
        :type spectrum_size: int, optional
        :return: instance of DataContainer
        :rtype: DataContainer
        """
        data = DataContainer(f'./DummyDataPathSize{spectrum_size}')
        spectrum = Spectrum.CreateDummySpectrum(spectrum_size)
        data.Append(spectrum)

        return data

    def __init__(self, path='', buffer_size=20):
        """Default constructor

        :param path: Path of the file containing the experimental data, defaults to ''
        :type path: str, optional
        :param buffer_size: Size of the buffer for data recovery, defaults to 20
        :type buffer_size: int, optional
        """
        self.__path = path
        self.__buffer = deque(maxlen=buffer_size)

    @property
    def X(self) -> ndarray:
        """xdata of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        return self.__buffer[0][0].X

    @X.setter
    def X(self, v):
        self.__buffer[0][0].X = v

    @property
    def Y(self) -> ndarray:
        """ydata of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        return self.__buffer[0][0].Y

    @Y.setter
    def Y(self, v):
        self.__buffer[0][0].Y = v

    @property
    def XY(self) -> Tuple[ndarray, ndarray]:
        """data of spectrum. This value is deepcopied.

        :return: [description]
        :rtype: Tuple[ndarray, ndarray]
        """
        return self.__buffer[0][0].XY

    @XY.setter
    def XY(self, v):
        self.__buffer[0][0].XY = v

    @property
    def BackGround(self) -> ndarray:
        """Background of spectrum. This value is deepcopied.

        :rtype: ndarray
        """
        return self.__buffer[0][0].BackGround

    @BackGround.setter
    def BackGround(self, v):
        self.__buffer[0][0].BackGround = v

    @BackGround.deleter
    def BackGround(self):
        del self.__buffer[0][0].BackGround

    @property
    def Peaks(self) -> PeakFunctionContainerList:
        """Peaks of spectrum. This value is deepcopied.

        :rtype: PeakFunctionContainerList
        """
        return self.__buffer[0][0].Peaks

    @Peaks.setter
    def Peaks(self, v):
        self.__buffer[0][0].Peaks = v

    @Peaks.deleter
    def Peaks(self):
        del self.__buffer[0][0].Peaks

    def GetSpectrumSize(self) -> int:
        """Get size of spectrum.

        :rtype: int
        """
        return self.__buffer[0][0].GetSize()

    @property
    def Recipe(self) -> Recipe:
        """Get recipe applied to the data

        :rtype: Recipe
        """
        return deepcopy(self.__buffer[0][1])

    @Recipe.setter
    def Recipe(self, v):
        if not isinstance(v, Recipe):
            raise TypeError('Can not include anything other than an instance of "Recipe"')

        self.__buffer[0][1] = v
        self.__buffer[0][2] = [None] * len(v)

    @property
    def SuccessList(self) -> List[Optional[bool]]:
        """A list of the results of executing the recipe.

        :return: If the value is bool, it indicates success or failure, and if the value is none, it indicates that it has not been executed.
        :rtype: List[Optional[bool]]
        """
        return deepcopy(self.__buffer[0][2])

    @SuccessList.setter
    def SuccessList(self, v):
        if any([not isinstance(element, bool) for element in v]):
            raise TypeError()

        self.__buffer[0][2] = v

    @property
    def Msg(self) -> str:
        """Message on recipe execution

        :rtype: str
        """
        return self.__buffer[0][3]

    @Msg.setter
    def Msg(self, v):
        if not isinstance(v, str):
            raise TypeError('Can not include anything other than an instance of "str"')

        self.__buffer[0][3]

    @property
    def Path(self) -> str:
        """Path of the file containing the experimental data

        :rtype: str
        """
        return self.__path

    @Path.setter
    def Path(self, v):
        if not isinstance(v, str):
            raise TypeError()

        self.__path = v

    def Append(self, spectrum: Spectrum, recipe: Recipe = None, success_list: List[Optional[bool]] = None, msg: str = ''):
        """Append data to the history.

        :type spectrum: Spectrum
        :param recipe: Recipe, If the recipe is none, it will be converted to an empty recipe. defaults to None
        :type recipe: Recipe, optional
        :param success_list: A list of the results of executing the recipe. If success_list is None, It assume that all the steps have not been executed. defaults to None
        :type success_list: List[Optional[bool]], optional
        :param msg: Message for this data history, defaults to ''
        :type msg: str, optional
        """
        if not isinstance(spectrum, Spectrum):
            raise TypeError('"spectrum" must be an instance of "Spectrum".')

        recipe = Recipe() if recipe is None else recipe

        if not isinstance(recipe, Recipe):
            raise TypeError('"recipe" must be an instance of "Recipe".')

        success_list = [None] * len(recipe) if success_list is None else success_list

        if any([not (success is None or isinstance(success, bool)) for success in success_list]):
            raise TypeError()

        if len(success_list) != len(recipe):
            raise TypeError()

        if not isinstance(msg, str):
            raise TypeError('"msg" must be an instance of "str"')

        self.__buffer.appendleft([spectrum, recipe, success_list, msg])

    def Clear(self):
        """Clear buffer
        """
        self.__buffer.clear()

    def Restore(self, delta: int):
        """Restore buffer data. Adds a copy of the specified data to the latest history.

        :param delta: 0 represents the latest, and the larger the number, the older the data.
        :type delta: int
        """
        spectrum, recipe, success_list, msg = self.__GetBufferData(delta)
        self.Append(deepcopy(spectrum), deepcopy(recipe), deepcopy(success_list), f'restore from\n{msg}')

    def GetBufferData(self, delta: int):
        """Get buffered data. This value is deepcopied.

        :param delta: 0 represents the latest, and the larger the number, the older the data.
        :type delta: int
        :rtype: Tuple[Spectrum, Recipe, List[Optional[bool]], str]
        """
        return deepcopy(self.__GetBufferData(delta))

    def __GetBufferData(self, delta):
        return self.__buffer[min(delta, len(self.__buffer) - 1)]

    @property
    def BufferSize(self) -> int:
        """size of buffer.

        :rtype: int
        """
        return len(self.__buffer)

    @BufferSize.setter
    def BufferSize(self, size):
        new_buffer = deque(maxlen=size)
        new_buffer.extend(self.__buffer)
        self.__buffer = new_buffer

    def SendSaveData(self):
        """Send path and latest data as save data.

        :rtype: Tuple[str, Tuple[Spectrum, Recipe, List[Optional[bool]], str]]
        """
        return (self.Path, self.__buffer[0],)

    def ReceiveSaveData(self, save_data):
        """Receive saved data

        :type save_data: Tuple[str, Tuple[Spectrum, Recipe, List[Optional[bool]], str]]
        """
        self.__path = save_data[0]
        self.__buffer.clear()

        spectrum, recipe, success_list, msg = save_data[1]
        self.Append(spectrum, recipe, success_list, msg)


class Project(StorableObject):
    """Data object for project
    """
    @classmethod
    def CreateDummyProject(cls, data_size: int = 3, spectrum_size: int = 100):
        """Generate dummy data. Can be used for testing, etc.

        :param data_size: size of data, defaults to 3
        :type data_size: int, optional
        :param spectrum_size: size of spectrum, defaults to 100
        :type spectrum_size: int, optional
        :rtype: instance of Project
        """
        data_list = []
        for i in range(data_size):
            data = DataContainer.CreateDummyData(spectrum_size)
            data.Path = data.Path + str(i)
            data_list.append(data)

        return Project('./Dummy Data.itsv', 'dummy note...', data_list, DEFAULT_PEAK_TYPE, date.today())

    def __init__(self, path='', note: str = '', data_list: Optional[List[DataContainer]] = None, peak_type: Optional[PeakType] = None, experimental_date: Optional[date] = None):
        """Default constructor

        :param path: The path where the project is saved, defaults to ''
        :type path: str, optional
        :param note: Note on the project, defaults to ''
        :type note: str, optional
        :param data_list: a list of DataContainer class, defaults to None
        :type data_list: Optional[List[DataContainer]], optional
        :param peak_type: type of peak. If peak_type is None, it is converted to the peak of the default., defaults to None
        :type peak_type: Optional[PeakType], optional
        :param experimental_date: Date of experiment, defaults to None
        :type experimental_date: Optional[date], optional
        """
        if not self.__IsValidPath(path):
            raise TypeError()

        if not isinstance(note, str):
            raise TypeError()

        data_list = [] if data_list is None else data_list
        if not HasValidElement(data_list, DataContainer):
            raise TypeError()

        peak_type = DEFAULT_PEAK_TYPE if peak_type is None else peak_type
        if not isinstance(peak_type, PeakType):
            raise TypeError()

        experimental_date = date.today() if experimental_date is None else experimental_date
        if not isinstance(experimental_date, date):
            raise TypeError()

        self.__path = path
        self.__note = note
        self.__data_list = data_list
        self.__peak_type = peak_type
        self.__experimental_date = experimental_date

    def GetPath(self) -> str:
        """Get path where the project is saved.

        :rtype: str
        """
        return self.__path

    def SetPath(self, path):
        """Set path where the project is saved. The specified path must be empty or directly under an existing directory.
        """
        if not self.__IsValidPath(path):
            raise TypeError()

        self.__path = path

    def __IsValidPath(self, path):
        return path == '' or isdir(dirname(path))

    def GetFileName(self) -> str:
        """Get the name of file in which the project is saved, if it is not set, return NEW_PROJECT_NAME.

        :rtype: str
        """
        return NEW_PROJECT_NAME if (name := GetFileName(self.__path)) == '' else name

    def SetFileName(self, name: str):
        """Set the name of file in which the project is saved

        :type name: str
        """
        if not isinstance(name, str):
            raise TypeError()

        self.__path = join(self.GetDirectory(), name)

    def GetDirectory(self) -> str:
        """Get the name of the directory where the project is saved. If it is not set, it returns empty string.

        :rtype: str
        """
        return dirname(self.__path)

    def SetDirectory(self, directory: str):
        """Set the name of the directory where the project is saved.

        :type directory: str
        """
        if not isdir(directory):
            raise ValueError()

        self.__path = join(directory, self.GetFileName())

    def GetDataList(self, index_list: Optional[Iterable[int]] = None) -> Tuple[DataContainer]:
        """Get the list of DataContainer.

        :param index_list: Returns the data for a given index. If not specified, all data will be returned. defaults to None
        :type index_list: Optional[Iterable[int]], optional
        :return: [description]
        :rtype: Tuple[DataContainer]
        """
        data_list = self.__data_list
        return data_list if index_list is None else [data_list[index] for index in index_list]

    def SetDataList(self, data_list: Iterable[DataContainer], index_list: Optional[Iterable[int]] = None):
        """Set the list of DataContainer

        :type data_list: Iterable[DataContainer]
        :param index_list: If specified, the data at the specified index will be updated, otherwise it will be recorded as a new data list., defaults to None
        :type index_list: Optional[Iterable[int]], optional
        """
        if not HasValidElement(data_list, DataContainer):
            raise TypeError()

        if index_list is None:
            self.__data_list = data_list
            return

        if len(data_list) != len(index_list):
            raise TypeError()

        original_data_list = self.__data_list
        for index, data in zip(index_list, data_list):
            original_data_list[index] = data

    def GetNote(self) -> str:
        """Get note on the project.

        :rtype: str
        """
        return self.__note

    def SetNote(self, note: str):
        """Set note on the project

        :type note: str
        """
        if not isinstance(note, str):
            raise TypeError()

        self.__note = note

    def GetPeakType(self) -> PeakType:
        """Get type of peak. This value is deepcopied.

        :rtype: PeakType
        """
        return deepcopy(self.__peak_type)

    def SetPeakType(self, peak_type: PeakType):
        """Set type of peak.

        :type peak_type: PeakType
        """
        if not isinstance(peak_type, PeakType):
            raise TypeError()

        self.__peak_type = peak_type

    def GetExperimentalDate(self) -> date:
        """Get date of experiment.

        :rtype: date
        """
        return self.__experimental_date

    def SetExperimentalDate(self, experimental_date: date):
        """Set date of experiment.

        :type experimental_date: date
        """
        if not isinstance(experimental_date, date):
            raise TypeError()

        self.__experimental_date = experimental_date

    def SendSaveData(self) -> Tuple[str, str, PeakType, List[DataContainer], date]:
        """Send path, note, type of peak, the list of data and date of experiment as save data.

        :return: [description]
        :rtype: Tuple[str, str, PeakType, List[DataContainer], date]
        """
        return (self.__path, self.__note, self.__peak_type, self.__data_list, self.__experimental_date.strftime(r'%Y-%m-%d'))

    def ReceiveSaveData(self, save_data: Tuple[str, str, PeakType, List[DataContainer], date]):
        """Receive saved data

        :type save_data: Tuple[str, str, PeakType, List[DataContainer], date]
        """
        self.__path, self.__note, self.__peak_type, self.__data_list, date_value = save_data
        y, m, d = map(int, date_value.split('-'))
        self.__experimental_date = date(y, m, d)


class DecodeFunctionContainerBase(FunctionContainerBase):
    """Contain function on decode. This class is used to output experimental data as a file.
    """

    def Execution(self, project: Project) -> str:
        """wrapper of "Function"

        :type project: Project
        :return: contents of a output file
        :rtype: str
        """
        return self.Function(project, self.GetArgs())

    @abstractmethod
    def Function(self, project: Project, args) -> Union[str, Iterable[str]]:
        """Describe the function to convert the experimental data to the contents of the output file.

        :param project: Information on experimental data
        :type project: Project
        :param args: The parameters specified in "SendRequireParams". If you want to know more details, please refer to the documentation of "SendRequireParams".
        :raises NotImplementedError: Error sent if the method is not overridden.
        :return: contents of the output file. If the return value is str, it will be output as a single file, and if it is Iterable[str], it will be output as multiple files.
        :rtype: Union[str, Iterable[str]]
        """
        raise NotImplementedError()

    def SendFileTypeWildcard(self):
        """Send the file format for output.

        :return: default to FileSelectorDefaultWildcardStr. If you want to know more details, please refer the wxPython document at (https://docs.wxpython.org/wx.functions.html?highlight=fileselector#wx.FileSelector).
        :rtype: str
        """
        return FileSelectorDefaultWildcardStr


class CSV(DecodeFunctionContainerBase):

    def Function(self, project, args):
        peak_type = project.GetPeakType()
        peak_arg_length = peak_type.GetArgumentLength()

        data_list = project.GetDataList()
        table = []

        seperater = ' ,'

        row = []
        for data in data_list:
            header = [basename(data.Path)] + [''] * 2 + ['Peak'] + [''] * peak_arg_length
            row.extend(header)

        table.append(seperater.join(row))

        row = []
        param_header = ['x', 'y', 'bg'] + [seperater.join(peak_type.GetArgumentNames())] + ['']
        row.extend(param_header * len(data_list))

        table.append(seperater.join(row))

        max_data_size = max([data.GetSpectrumSize() for data in data_list])

        x_list = [data.X for data in data_list]
        y_list = [data.Y for data in data_list]
        bg_list = [data.BackGround for data in data_list]
        peaks_list = [data.Peaks for data in data_list]
        for i in range(max_data_size):
            row = []
            for j in range(len(data_list)):
                if i >= len(x_list[j]):
                    row.extend([''] * 3)
                else:
                    row.extend(map(str, (x_list[j][i], y_list[j][i], bg_list[j][i])))

                if i >= len(peaks_list[j]):
                    row.extend([''] * (peak_arg_length + 1))
                else:
                    row.extend(map(str, peaks_list[j][i].GetArgs()))
                    row.append('')

            table.append(seperater.join(row))

        project_name = project.GetFileName()

        return (project_name, '\n'.join(table),)

    def SendFileTypeWildcard(self):
        return 'CSV files (.csv)|*.csv'


class MappingFunctionContainerBase(FunctionContainerBase):
    """Contain function on mapping
    """

    def Execution(self, data_list: Iterable[DataContainer]) -> Iterable[Union[int, float]]:
        """Wrapper "Function"

        :type data_list: Iterable[DataContainer]
        :return: List of Value corresponding to data_list
        :rtype: Iterable[Union[int, float]]
        """
        return self.Function(data_list, self.GetArgs())

    @abstractmethod
    def Function(self, data_list, args) -> Iterable[Union[int, float]]:
        """Describe the body of the function here.

        :type data_list: Iterable[DataContainer]
        :param args: The parameters specified in "SendRequireParams". If you want to know more details, please refer to the documentation of "SendRequireParams".
        :return: The value corresponding to data_list. The values are used for mapping and are colored according to the size of the value.
        :rtype: Iterable[Union[int, float]]
        """
        raise NotImplementedError()


class PeakMapping(MappingFunctionContainerBase):
    def __init__(self):
        super().__init__({
            'Mode': ChoiceContainer(default='Amplitude', choices=['Amplitude', 'Center', 'FWHM']),
            'Standard': FloatContainer(),
            'Left': OptionalFloatContainer(None),
            'Right': OptionalFloatContainer(None),
            'Bottom': OptionalFloatContainer(None),
            'Top': OptionalFloatContainer(None),
        })

    def Function(self, data_list, args):
        mode = args[0]
        standard = args[1]
        left, right, bottom, top, = args[2:]

        left = -inf if left is None else left
        right = inf if right is None else right
        bottom = -inf if bottom is None else bottom
        top = inf if top is None else top

        value_list = []
        for data in data_list:
            if data is None:
                value_list.append(None)
                continue

            v = inf
            for peak in data.Peaks:
                amp, ctr, wid = peak.Amp, peak.Ctr, peak.Wid

                if bottom <= amp <= top and left <= ctr <= right:
                    if mode == 'Amplitude':
                        w = amp
                    elif mode == 'Center':
                        w = ctr
                    elif mode == 'FWHM':
                        w = wid

                    v = w if abs(w - standard) < abs(v - standard) else v

            if v != inf:
                value_list.append(v)
            else:
                value_list.append(None)

        return array(value_list)

# class StorableLinearSegmentedColormap(StorableObject, LinearSegmentedColormap):
#     def __init__(self, *args, **kw):
#         if 'name' in kw and len(args) >= 1:
#             raise TypeError()

#         name = kw.get('name', 'custom')
#         name = args[0] if len(args) >= 1 else name

#         if 'segmentdata' in kw and len(args) >= 2:
#             raise TypeError()

#         segmentdata = kw.get('segmentdata', {
#             'red': [[0.0, 1.0, 1.0], [1, 1, 1]],
#             'blue': [[0.0, 1.0, 1.0], [1, 1, 1]],
#             'green': [[0.0, 1.0, 1.0], [1, 1, 1]],
#             'alpha': [[0.0, 1.0, 1.0], [1, 1, 1]],
#         })
#         segmentdata = args[1] if len(args) >= 2 else segmentdata
#         super().__init__(name, segmentdata)

#     def FromColorsPositions(self, colors, positions):
#         if len(colors) != len(positions):
#             return

#         _segmentdata = {'red': [], 'green': [], 'blue': [], 'alpha': []}
#         if 0 not in positions:
#             _segmentdata['red'].append([0, 1, 1])
#             _segmentdata['blue'].append([0, 1, 1])
#             _segmentdata['green'].append([0, 1, 1])
#             _segmentdata['alpha'].append([0, 0, 0])

#         for color, pos in zip(colors, positions):
#             red, green, blue, alpha = color
#             if pos not in [value[0] for value in _segmentdata['red']]:
#                 _segmentdata['red'].append([pos, red, red])
#                 _segmentdata['blue'].append([pos, blue, blue])
#                 _segmentdata['green'].append([pos, green, green])
#                 _segmentdata['alpha'].append([pos, alpha, alpha])

#         if 1 not in positions:
#             _segmentdata['red'].append([1, 1, 1])
#             _segmentdata['blue'].append([1, 1, 1])
#             _segmentdata['green'].append([1, 1, 1])
#             _segmentdata['alpha'].append([1, 0, 0])

#         self.name = 'custom'
#         self._segmentdata = _segmentdata

#     def GetColorsPositions(self):
#         # todo
#         red = self._segmentdata['red']
#         blue = self._segmentdata['blue']
#         green = self._segmentdata['green']
#         alpha = self._segmentdata['alpha']

#         colors = []
#         positions = {0, 1}
#         positions |= set([v[0] for v in red])
#         positions |= set([v[0] for v in blue])
#         positions |= set([v[0] for v in green])
#         positions |= set([v[0] for v in alpha])
#         positions = list(positions)

#         def get_pos(pos, idx, list_):
#             while idx < len(list_) and list_[idx][0] < pos:
#                 idx += 1

#             return list_[idx][0], idx

#         r_i = 0
#         b_i = 0
#         g_i = 0
#         a_i = 0
#         for pos in positions:
#             r_p, r_i = get_pos(pos, r_i, red)
#             b_p, b_i = get_pos(pos, b_i, blue)
#             g_p, g_i = get_pos(pos, g_i, green)
#             a_p, a_i = get_pos(pos, a_i, alpha)

#             r_v = (red[r_i][1] if r_p == pos else InterpolateValue(pos, (red[r_i][0], red[r_i][2]), (red[r_i][0], red[r_i][1]))) * 255
#             b_v = (blue[b_i][1] if b_p == pos else InterpolateValue(pos, (blue[b_i][0], blue[b_i][2]), (blue[b_i][0], blue[b_i][1]))) * 255
#             g_v = (green[g_i][1] if g_p == pos else InterpolateValue(pos, (green[g_i][0], green[g_i][2]), (green[g_i][0], green[g_i][1]))) * 255
#             a_v = (alpha[a_i][1] if a_p == pos else InterpolateValue(pos, (alpha[a_i][0], alpha[a_i][2]), (alpha[a_i][0], alpha[a_i][1]))) * 255

#             colors.append([r_v, b_v, g_v, a_v])

#             r_v2 = (red[r_i][2] if r_p == pos else r_v) * 255
#             b_v2 = (blue[b_i][2] if b_p == pos else b_v) * 255
#             g_v2 = (green[g_i][2] if g_p == pos else g_v) * 255
#             a_v2 = (alpha[a_i][2] if a_p == pos else a_v) * 255

#             if any([p == pos and cl[pos][1] != cl[pos][2] for p, cl in zip([r_p, b_p, g_p, a_p], [red, blue, green, alpha])]):
#                 colors.append([r_v2, b_v2, g_v2, a_v2])

#         return colors, positions

#     def SendSaveData(self):
#         return (self.name, self._segmentdata,)

#     def ReceiveSaveData(self, save_data):
#         self.name, self._segmentdata = save_data


def Container2Value(v):
    return v.GetValue() if isinstance(v, ArgumentContainerBase) else v


NEW_PROJECT_NAME = 'New Project'
DEFAULT_ENCODE_FUNCTION = Text()
DEFAULT_DECODE_FUNCTION = CSV()
DEFAULT_MAPPING_FUNCTION = PeakMapping()
DEFAULT_PEAK = Gaussian()
DEFAULT_PEAK_TYPE = PeakType(DEFAULT_PEAK)
DEFAULT_BUFFER_SIZE = IntContainer(20, 1, 100)
DEFAULT_DIRECTION_CONTAINER = ChoiceContainer('r2d', ['r2d', 'r2u', 'l2d', 'l2u', 'u2r', 'u2l', 'd2r', 'd2l'])


__all__ = [
    'ArgumentContainerBase',
    'BoundedArgumentContainerBase',
    'OptionalIntContainer',
    'IntContainer',
    'OptionalFloatContainer',
    'FloatContainer',
    'StrContainer',
    'ChoiceContainer',
    'IterableArgumentContainerBase',
    'ListArgumentContainer',
    'TupleArgumentContainer',
    'FunctionContainerBase',
    'PeakFunctionContainerBase',
    'Gaussian',
    'SpectrumFunctionContainerBase',
    'EncodeFunctionContainerBase',
    'Text',
    'PeakFunctionContainerList',
    'PeakType',
    'Spectrum',
    'Recipe',
    'Preset',
    'SpectrumFunctionContainerAccessor',
    'DataContainer',
    'Project',
    'DecodeFunctionContainerBase',
    'CSV',
    'MappingFunctionContainerBase',
    'PeakMapping',
]
