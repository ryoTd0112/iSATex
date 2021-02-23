from copy import deepcopy
from datetime import date
from os.path import dirname, isdir
from typing import Iterable, List, Tuple, Union

from matplotlib.colors import Colormap
from wx import Colour, NewEventType, PyCommandEvent, PyEventBinder

from const import (ERROR_COLOR, MAIN_SELECTION_COLOR, NAME, SELECTION_COLOR,
                   SUCCESS_COLOR)
from core import iSATexObject
from objects import (DEFAULT_DIRECTION_CONTAINER, NEW_PROJECT_NAME,
                     ChoiceContainer, Container2Value, DataContainer,
                     DecodeFunctionContainerBase, EncodeFunctionContainerBase,
                     FunctionContainerBase, IntContainer,
                     MappingFunctionContainerBase, PeakFunctionContainerBase,
                     PeakType, Preset, Recipe, SpectrumFunctionContainerBase)
from util import GetFileName, HasValidElement


class iSATexEventBinder(PyEventBinder, iSATexObject):
    """Binder of events related to iSATex.
    """
    pass


class iSATexEvent(PyCommandEvent):
    """Events managed by iSATex.
    """
    pass


wxEVT_PROJECT_NEW = NewEventType()
EVT_PROJECT_NEW = iSATexEventBinder(wxEVT_PROJECT_NEW)

wxEVT_PROJECT_OPEN = NewEventType()
EVT_PROJECT_OPEN = iSATexEventBinder(wxEVT_PROJECT_OPEN)

wxEVT_PROJECT_SAVE = NewEventType()
EVT_PROJECT_SAVE = iSATexEventBinder(wxEVT_PROJECT_SAVE)

wxEVT_PROJECT_MEMO_CHANGE = NewEventType()
EVT_PROJECT_MEMO_CHANGE = iSATexEventBinder(wxEVT_PROJECT_MEMO_CHANGE)

wxEVT_PROJECT_EXIT = NewEventType()
EVT_PROJECT_EXIT = iSATexEventBinder(wxEVT_PROJECT_EXIT)

wxEVT_DATA_CONTENTS_CHANGE = NewEventType()
EVT_DATA_CHANGE = iSATexEventBinder(wxEVT_DATA_CONTENTS_CHANGE)

wxEVT_DATA_SELECTION_CHANGE = NewEventType()
EVT_DATA_SELECTION_CHANGE = iSATexEventBinder(wxEVT_DATA_SELECTION_CHANGE)

wxEVT_ENCODE_FUNCTION_SELECT = NewEventType()
EVT_ENCODE_FUNCTION_SELECT = iSATexEventBinder(wxEVT_ENCODE_FUNCTION_SELECT)

wxEVT_DECODE_FUNCTION_SELECT = NewEventType()
EVT_DECODE_FUNCTION_SELECT = iSATexEventBinder(wxEVT_DECODE_FUNCTION_SELECT)

wxEVT_MAPPING_FUNCTION_SELECT = NewEventType()
EVT_MAPPING_FUNCTION_SELECT = iSATexEventBinder(wxEVT_MAPPING_FUNCTION_SELECT)

wxEVT_SPECTRUM_FUNCTION_LIST_SELECT = NewEventType()
EVT_SPECTRUM_FUNCTION_LIST_SELECT = iSATexEventBinder(wxEVT_SPECTRUM_FUNCTION_LIST_SELECT)

wxEVT_ENCODE_FUNCTION_REGISTER = NewEventType()
EVT_ENCODE_FUNCTION_REGISTER = iSATexEventBinder(wxEVT_ENCODE_FUNCTION_REGISTER)

wxEVT_ENCODE_FUNCTION_DEREGISTER = NewEventType()
EVT_ENCODE_FUNCTION_DEREGISTER = iSATexEventBinder(wxEVT_ENCODE_FUNCTION_DEREGISTER)

wxEVT_DECODE_FUNCTION_REGISTER = NewEventType()
EVT_DECODE_FUNCTION_REGISTER = iSATexEventBinder(wxEVT_DECODE_FUNCTION_REGISTER)

wxEVT_DECODE_FUNCTION_DEREGISTER = NewEventType()
EVT_DECODE_FUNCTION_DEREGISTER = iSATexEventBinder(wxEVT_DECODE_FUNCTION_DEREGISTER)

wxEVT_SPECTRUM_FUNCTION_REGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_REGISTER = iSATexEventBinder(wxEVT_SPECTRUM_FUNCTION_REGISTER)

wxEVT_SPECTRUM_FUNCTION_DEREGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_DEREGISTER = iSATexEventBinder(wxEVT_SPECTRUM_FUNCTION_DEREGISTER)

wxEVT_PEAK_FUNCTION_REGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_REGISTER = iSATexEventBinder(wxEVT_PEAK_FUNCTION_REGISTER)

wxEVT_PEAK_FUNCTION_DEREGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_DEREGISTER = iSATexEventBinder(wxEVT_PEAK_FUNCTION_DEREGISTER)

wxEVT_MAPPING_FUNCTION_REGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_REGISTER = iSATexEventBinder(wxEVT_MAPPING_FUNCTION_REGISTER)

wxEVT_MAPPING_FUNCTION_DEREGISTER = NewEventType()
EVT_SPECTRUM_FUNCTION_DEREGISTER = iSATexEventBinder(wxEVT_MAPPING_FUNCTION_DEREGISTER)

wxEVT_ENCODE = NewEventType()
EVT_ENCODED = iSATexEventBinder(wxEVT_ENCODE)
# EVT_ENCODED_FUNCTION = CustomEventBinder(wxEVT_ENCODE)

wxEVT_DECODE = NewEventType()
EVT_DECODE = iSATexEventBinder(wxEVT_DECODE)
# EVT_DECODE_FUNCTION = CustomEventBinder(wxEVT_DECODE)

wxEVT_TABLE_SIZE_CHANGE = NewEventType()
EVT_TABLE_SIZE = iSATexEventBinder(wxEVT_TABLE_SIZE_CHANGE)

wxEVT_DIRECTION_CHANGE = NewEventType()
EVT_DIRECTION = iSATexEventBinder(wxEVT_DIRECTION_CHANGE)

wxEVT_RECIPE_SELECT = NewEventType()
EVT_RECIPE_SELECT = iSATexEventBinder(wxEVT_RECIPE_SELECT)

wxEVT_PRESET_REGISTER = NewEventType()
EVT_PRESET_REGISTER = iSATexEventBinder(wxEVT_PRESET_REGISTER)

wxEVT_PRESET_DEREGISTER = NewEventType()
EVT_PRESET_DEREGISTER = iSATexEventBinder(wxEVT_PRESET_DEREGISTER)

wxEVT_PRESET_SELECT = NewEventType()
EVT_PRESET_SELECT = iSATexEventBinder(wxEVT_PRESET_SELECT)

wxEVT_PEAK_TYPE_REGISTER = NewEventType()
EVT_PEAK_TYPE_REGISTER = iSATexEventBinder(wxEVT_PEAK_TYPE_REGISTER)

wxEVT_PEAK_TYPE_CHANGE = NewEventType()
EVT_PEAK_TYPE_CHANGE = iSATexEventBinder(wxEVT_PEAK_TYPE_CHANGE)

wxEVT_PANEL_SELECTION_CHANGE = NewEventType()
EVT_PANEL_SELECTION_CHANGE = iSATexEventBinder(wxEVT_PANEL_SELECTION_CHANGE)

wxEVT_PANEL_VIEW = NewEventType()
EVT_PANEL_VIEW = iSATexEventBinder(wxEVT_PANEL_VIEW)

wxEVT_PANEL_REGISTER = NewEventType()
EVT_PANEL_REGISTER = iSATexEventBinder(wxEVT_PANEL_REGISTER)

wxEVT_LAYOUT_CHANGE = NewEventType()
EVT_LAYOUT_CHANGE = iSATexEventBinder(wxEVT_LAYOUT_CHANGE)

wxEVT_LAYOUT_REGISTER = NewEventType()
EVT_LAYOUT_REGISTER = iSATexEventBinder(wxEVT_LAYOUT_REGISTER)

wxEVT_PREFERENCE = NewEventType()
EVT_PREFERENCE = iSATexEventBinder(wxEVT_PREFERENCE)

wxEVT_COLOR_REGISTER = NewEventType()
EVT_COLOR_REGISTER = iSATexEventBinder(wxEVT_COLOR_REGISTER)

wxEVT_COLOR_SELECT = NewEventType()
EVT_COLOR_SELECT = iSATexEventBinder(wxEVT_COLOR_SELECT)

wxEVT_COLORMAP_CHANGE = NewEventType()
EVT_COLOR_MAP_CHANGE = iSATexEventBinder(wxEVT_COLORMAP_CHANGE)

wxEVT_LAUNCH = NewEventType()
EVT_LAUNCH = iSATexEventBinder(wxEVT_LAUNCH)

wxEVT_EXIT = NewEventType()
EVT_EXIT = iSATexEventBinder(wxEVT_EXIT)


class ProjectEvent(iSATexEvent):
    """Events related to the project.
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType=eventType, id=id)


class ProjectLoadEvent(ProjectEvent):
    """Event related to Project
    """

    def __init__(self, data_list: Iterable[DataContainer], peak_type: PeakType, eventType: int, id: int):
        """Default constructor

        :type data_list: Iterable[DataContainer]
        :type peak_type: PeakType
        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)
        if not HasValidElement(data_list, DataContainer):
            raise TypeError()

        if not isinstance(peak_type, PeakType):
            raise TypeError()

        self.__data_list = data_list
        self.__peak_type = peak_type

    def GetDataList(self) -> Iterable[DataContainer]:
        """Get loaded data list. This value is deepcopied.
        """
        return deepcopy(self.__data_list)

    def GetPeakType(self) -> PeakType:
        """Get type of peak that was selected. This value is deepcopied.

        :rtype: PeakType
        """
        return deepcopy(self.__peak_type)

    def GetDataSize(self) -> int:
        """Get size of data list.

        :rtype: int
        """
        return len(self.__data_list)


class ProjectNewEvent(ProjectLoadEvent):
    """Event related to loading a new project
    """

    def __init__(self, data_list: Iterable[DataContainer], peak_type: PeakType, id=0):
        """Default constructor

        :type data_list: Iterable[DataContainer]
        :type peak_type: PeakType
        :type id: int, optional
        """
        super().__init__(data_list, peak_type, wxEVT_PROJECT_NEW, id)


class ProjectOpenEvent(ProjectLoadEvent):
    """event related to loading an existing project
    """

    def __init__(self, data_list: Iterable[DataContainer], path: str, peak_type: PeakType, note: str, experimental_date: date, id=0):
        """Default constructor

        :type data_list: Iterable[DataContainer]
        :param path: The path where the project is saved.
        :type path: str
        :type peak_type: PeakType
        :param note: Note on the project, defaults to ''.
        :type note: str
        :param experimental_date: Date of experiment.
        :type experimental_date: date
        :type id: int, optional
        """
        super().__init__(data_list, peak_type, wxEVT_PROJECT_OPEN, id)
        if not (path == '' or isdir(dirname(path))):
            raise TypeError()

        if not isinstance(note, str):
            raise TypeError()

        if not isinstance(experimental_date, date):
            raise TypeError()

        self.__path = path
        self.__note = note
        self.__experimental_date = experimental_date

    def GetPath(self) -> str:
        """Get the path where the project is saved.

        :rtype: str
        """
        return self.__path

    def GetNote(self) -> str:
        """Get note on the project

        :rtype: str
        """
        return self.__note

    def GetExperimentalDate(self) -> date:
        """Get date of experiment

        :rtype: date
        """
        return self.__experimental_date


class ProjectSaveEvent(ProjectEvent):
    """Event related to saving a project
    """

    def __init__(self, path, data_list, peak_type, note, experimental_date, id=0):
        """Default constructor

        :param path: The path where the project is saved.
        :type path: str, optional
        :param data_list: a list of DataContainer class.
        :type data_list: List[DataContainer].
        :param peak_type: type of peak.
        :type peak_type: PeakType
        :param note: Note on the project, defaults to ''
        :type note: str
        :param experimental_date: Date of experiment, defaults to None
        :type experimental_date: date
        :type id: int, optional
        """
        super().__init__(wxEVT_PROJECT_SAVE, id)

        self.__path = path
        self.__data_list = data_list
        self.__peak_type = peak_type
        self.__note = note
        self.__experimental_date = experimental_date

    def GetPath(self) -> str:
        """Get the path where the project is saved.

        :rtype: str
        """
        return self.__path

    def GetDataList(self) -> Iterable[DataContainer]:
        """Get loaded data list. This value is deepcopied.
        """
        return deepcopy(self.__data_list)

    def GetFileName(self) -> str:
        """Get the name of file in which the project is saved, if it is not set, return NEW_PROJECT_NAME.

        :rtype: str
        """
        return NEW_PROJECT_NAME if (name := GetFileName(self.__path)) == '' else name

    def GetPeakType(self) -> PeakType:
        """Get type of peak. This value is deepcopied.

        :rtype: PeakType
        """
        return deepcopy(self.__peak_type)

    def GetNote(self) -> str:
        """Get note on the project.

        :rtype: str
        """
        return self.__note

    def GetExperimentalDate(self) -> date:
        """Get date of experiment.

        :rtype: date
        """
        return self.__experimental_date


class ProjectMemoChangeEvent(ProjectEvent):
    """Event related to a change in a project memo
    """

    def __init__(self, experimental_date: date, previous_experimental_date: date, note: str, previous_note: str, id=0):
        """Default constructor

        :param experimental_date: Date of experiment after change
        :type experimental_date: date
        :param previous_experimental_date: Date of experiment before change
        :type previous_experimental_date: date
        :param note: Note of experiment after change
        :type note: str
        :param previous_note: Note of experiment before change
        :type previous_note: str
        :type id: int, optional
        """
        super().__init__(wxEVT_PROJECT_MEMO_CHANGE, id)
        if not isinstance(experimental_date, date):
            raise TypeError()

        if not isinstance(previous_experimental_date, date):
            raise TypeError()

        if not isinstance(note, str):
            raise TypeError()

        if not isinstance(previous_note, str):
            raise TypeError()

        self.__date = experimental_date
        self.__prev_date = previous_experimental_date
        self.__note = note
        self.__prev_note = previous_note

    def GetExperimentalData(self) -> date:
        """Date of experiment after change.

        :rtype: date
        """
        return self.__date

    def GetPreviousExperimentalData(self) -> date:
        """Date of experiment before change.

        :rtype: date
        """
        return self.__date

    def GetNote(self) -> str:
        """Note of experiment after change.

        :rtype: str
        """
        return self.__note

    def GetPreviousNote(self) -> str:
        """Note of experiment before change.

        :rtype: str
        """
        return self.__note


class DataEvent(iSATexEvent):
    """Event related to data
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id=id)


class DataContentsChangeEvent(DataEvent):
    """Event related to a change in the contents of the data
    """

    def __init__(
            self,
            index_list: Iterable[int],
            data_list: Iterable[DataContainer],
            x_changed_list: Iterable[bool] = None,
            y_changed_list: Iterable[bool] = None,
            bg_changed_list: Iterable[bool] = None,
            peaks_changed_list: Iterable[bool] = None,
            recipe_changed_list: Iterable[bool] = None,
            msg_changed_list: Iterable[bool] = None,
            id=0):
        """Default constructor

        :param index_list: Index list of data whose contents have been changed
        :type index_list: Iterable[int]
        :param data_list: A list of data specified by index_list.
        :type data_list: Iterable[DataContainer]
        :param x_changed_list: List of which data x has been changed, defaults to None
        :type x_changed_list: Iterable[bool], optional
        :param y_changed_list: List of which data y has been changed, defaults to None
        :type y_changed_list: Iterable[bool], optional
        :param bg_changed_list: List of which data background has been changed, defaults to None
        :type bg_changed_list: Iterable[bool], optional
        :param peaks_changed_list: List of which data peaks has been changed, defaults to None
        :type peaks_changed_list: Iterable[bool], optional
        :param recipe_changed_list: List of which data recipe has been changed, defaults to None
        :type recipe_changed_list: Iterable[bool], optional
        :param msg_changed_list: List of which data message has been changed, defaults to None
        :type msg_changed_list: Iterable[bool], optional
        :type id: int, optional
        """
        super().__init__(wxEVT_DATA_CONTENTS_CHANGE, id)
        self.__index_list = index_list
        self.__data_list = data_list
        self.__x_changed_list = [False] * len(index_list) if x_changed_list is None else x_changed_list
        self.__y_changed_list = [False] * len(index_list) if y_changed_list is None else y_changed_list
        self.__bg_changed_list = [False] * len(index_list) if bg_changed_list is None else bg_changed_list
        self.__peaks_changed_list = [False] * len(index_list) if peaks_changed_list is None else peaks_changed_list
        self.__recipe_changed_list = [False] * len(index_list) if recipe_changed_list is None else recipe_changed_list
        self.__msg_changed_list = [False] * len(index_list) if msg_changed_list is None else msg_changed_list

    def GetIndexList(self) -> Iterable[int]:
        """Get index list of data whose contents have been changed

        :rtype: Iterable[int]
        """
        return tuple(self.__index_list)

    def GetDataList(self) -> Iterable[DataContainer]:
        """Get a list of data specified by index_list

        :rtype: Iterable[DataContainer]
        """
        return deepcopy(self.__data_list)

    def __IsChanged(self, changed_list: Iterable[bool], index: int) -> bool:
        """Private function to check if changes have been made.

        :param changed_list: list to check
        :type changed_list: Iterable[bool]
        :type index: int
        :rtype: bool
        """
        if index is None:
            return any([changed for changed in changed_list])

        if index not in self.__index_list:
            return False

        return changed_list[self.__index_list.index(index)]

    def IsXChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "X".

        :param index: If index is None, it will return True if any of the data x has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__x_changed_list, index)

    def IsYChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "Y".

        :param index: If index is None, it will return True if any of the data y has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__y_changed_list, index)

    def IsBackGroundChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "background".

        :param index: If index is None, it will return True if any of the data background has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__bg_changed_list, index)

    def IsPeaksChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "peaks".

        :param index: If index is None, it will return True if any of the data peaks has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__peaks_changed_list, index)

    def IsRecipeChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "Recipe".

        :param index: If index is None, it will return True if any of the data recipe has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__recipe_changed_list, index)

    def IsMessageChanged(self, index=None) -> bool:
        """Return True, if data specified by index is changed "Message".

        :param index: If index is None, it will return True if any of the data message has been changed. defaults to None
        :type index: int, optional to None
        :rtype: bool
        """
        return self.__IsChanged(self.__msg_changed_list, index)


class DataSelectionChangeEvent(DataEvent):
    """Event related to a change in data selection
    """

    def __init__(self, main_selection: int = None, previous_main_selection: int = None, selection: Iterable[int] = None, previous_selection: Iterable[int] = None, id=0):
        """Default constructor

        :param main_selection: Index of the data selected mainly, If None, it means no change. Defaults to None
        :type main_selection: int, optional
        :param previous_main_selection: previous main selection same as the main selection, defaults to None
        :type previous_main_selection: int, optional
        :param selection: A list of index specified the selected data, includes the main selection. If None, it means no change. Defaults to None
        :type selection: Iterable[int], optional
        :param previous_selection: previous selection same as the selection, defaults to None
        :type previous_selection: Iterable[int], optional
        :type id: int, optional
        """
        super().__init__(wxEVT_DATA_SELECTION_CHANGE, id)
        if main_selection is None and selection is None:
            raise ValueError()

        previous_selection = [] if previous_selection is None else previous_selection
        selection = [] if selection is None else selection
        if previous_main_selection is not None and previous_main_selection not in previous_selection:
            previous_selection.append(previous_main_selection)

        if main_selection is not None and main_selection not in selection:
            selection.append(main_selection)

        previous_selection.sort()
        selection.sort()

        self.__prev_main_selection = previous_main_selection
        self.__main_selection = main_selection
        self.__prev_selection = previous_selection
        self.__selection = selection

    def GetMainSelection(self) -> int:
        """Get index of the data selected mainly

        :rtype: int
        """
        return self.__main_selection

    def GetPreviousMainSelection(self) -> int:
        """Get previous index of the data selected mainly

        :rtype: int
        """
        return self.__prev_main_selection

    def IsMainSelectionChanged(self) -> bool:
        """Returns whether the main selection has been changed.

        :rtype: bool
        """
        return self.GetMainSelection() != self.GetPreviousMainSelection()

    def GetSelection(self) -> Tuple[int, ...]:
        """Get a list of index specified the selected data

        :rtype: Tuple[int, ...]
        """
        return tuple(self.__selection)

    def GetPreviousSelection(self) -> Tuple[int, ...]:
        """Get a previous list of index specified the selected data

        :rtype: Tuple[int, ...]
        """
        return tuple(self.__prev_selection)

    def IsSelectionChanged(self) -> bool:
        """Returns whether the selection has been changed.

        :rtype: bool
        """
        return self.GetSelection() != self.GetPreviousSelection()

    def GetAddedSelection(self) -> List[int]:
        """Returns a list of newly selected indexes.

        :rtype: List[int, ...]
        """
        return list(set(self.GetSelection()) - set(self.GetPreviousSelection()))

    def GetRemoveSelection(self) -> List[int]:
        """Returns a list of deselected indices.

        :rtype: List[int, ...]
        """
        return list(set(self.GetPreviousSelection()) - set(self.GetSelection()))


class FunctionEvent(iSATexEvent):
    """Event related to the function
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)


class EncodeFunctionSelectEvent(FunctionEvent):
    """event related to the selection of an encoding function
    """

    def __init__(self, function: EncodeFunctionContainerBase, previous_function: EncodeFunctionContainerBase, id=0):
        """Default constructor

        :param function: Selected encode function
        :type function: EncodeFunctionContainerBase
        :param previous_function: Previous selected encode function
        :type previous_function: EncodeFunctionContainerBase
        :type id: int, optional
        """
        super().__init__(wxEVT_ENCODE_FUNCTION_SELECT, id)
        self.__function = function
        self.__prev_function = previous_function

    def GetFunction(self):
        """Get encode function. This value is deepcopied.

        :rtype: EncodeFunctionContainerBase
        """
        return deepcopy(self.__function)

    def GetPreviousFunction(self):
        """Get previous encode function. This value is deepcopied.

        :rtype: EncodeFunctionContainerBase
        """
        return deepcopy(self.__prev_function)


class DecodeFunctionSelectEvent(FunctionEvent):
    """Event related to the selection of the decode function
    """

    def __init__(self, function: DecodeFunctionContainerBase, previous_function: DecodeFunctionContainerBase, id=0):
        """Default constructor

        :param function: Selected decode function
        :type function: DecodeFunctionContainerBase
        :param previous_function: Previous selected decode function
        :type previous_function: DecodeFunctionContainerBase
        :type id: int, optional
        """
        super().__init__(wxEVT_DECODE_FUNCTION_SELECT, id)
        self.__function = function
        self.__prev_function = previous_function

    def GetFunction(self) -> DecodeFunctionContainerBase:
        """Get decode function. This value is deepcopied.

        :rtype: DecodeFunctionContainerBase
        """
        return deepcopy(self.__function)

    def GetPreviousFunction(self) -> DecodeFunctionContainerBase:
        """Get previous decode function. This value is deepcopied.

        :rtype: DecodeFunctionContainerBase
        """
        return deepcopy(self.__prev_function)


class SpectrumFunctionListSelectEvent(FunctionEvent):
    """Event related to the selection of a spectral function
    """

    def __init__(self, function_list: Iterable[SpectrumFunctionContainerBase], previous_function_list: Iterable[SpectrumFunctionContainerBase], id=0):
        """Default constructor

        :param function: Selected decode function
        :type function: Iterable[SpectrumFunctionContainerBase]
        :param previous_function: Previous selected decode function
        :type previous_function: Iterable[SpectrumFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(wxEVT_SPECTRUM_FUNCTION_LIST_SELECT, id)

        self.__func_list = function_list
        self.__prev_func_list = previous_function_list

    def GetFunctionList(self) -> Iterable[SpectrumFunctionContainerBase]:
        """Get a list of spectrum function. This value is deepcopied.

        :rtype: Iterable[SpectrumFunctionContainerBase]
        """
        return deepcopy(self.__func_list)

    def GetPreviousFunctionList(self) -> Iterable[SpectrumFunctionContainerBase]:
        """Get previous a list of spectrum function. This value is deepcopied.

        :rtype: Iterable[SpectrumFunctionContainerBase]
        """
        return deepcopy(self.__prev_func_list)


class MappingFunctionSelectEvent(FunctionEvent):
    """Event related to the selection of a mapping function
    """

    def __init__(self, function: MappingFunctionContainerBase, previous_function: MappingFunctionContainerBase, id=0):
        """Default constructor

        :param function: Selected decode function
        :type function: MappingFunctionContainerBase
        :param previous_function: Previous selected decode function
        :type previous_function: MappingFunctionContainerBase
        :type id: int, optional
        """
        super().__init__(wxEVT_MAPPING_FUNCTION_SELECT, id)
        self.__function = function
        self.__prev_function = previous_function

    def GetFunction(self) -> MappingFunctionContainerBase:
        """Get mapping function. This value is deepcopied.

        :rtype: MappingFunctionContainerBase
        """
        return deepcopy(self.__function)

    def GetPreviousFunction(self) -> MappingFunctionContainerBase:
        """Get previous mapping function. This value is deepcopied.

        :rtype: MappingFunctionContainerBase
        """
        return deepcopy(self.__prev_function)


class FunctionRegisterEvent(FunctionEvent):
    """Event related to the registration of a function
    """

    def __init__(self, function_list: Iterable[FunctionContainerBase], previous_function_list: Iterable[FunctionContainerBase], eventType: int, id=0):
        """Default constructor

        :param function_list: List of functions to be registered
        :type function_list: Iterable[FunctionContainerBase]
        :param previous_function_list: List of previously registered functions
        :type previous_function_list: Iterable[FunctionContainerBase]
        :param eventType: type of event
        :type eventType: int
        :type id: int, optional
        """
        super().__init__(eventType, id)

        self.__func_list = function_list
        self.__prev_func_list = [] if previous_function_list is None else previous_function_list

    def GetFunctionList(self) -> Iterable[FunctionContainerBase]:
        """Get a list of functions to be registered. This value is deepcopied.

        :rtype: Iterable[FunctionContainerBase]
        """
        return deepcopy(self.__func_list)

    def GetPreviousFunctionList(self) -> Iterable[FunctionContainerBase]:
        """Get a list of previously registered functions. This value is deepcopied.

        :rtype: Iterable[FunctionContainerBase]
        """
        return deepcopy(self.__prev_func_list)


class EncodeFunctionRegisterEvent(FunctionRegisterEvent):
    """Event related to the registration of an encoding function.
    """

    def __init__(self, function_list: Iterable[EncodeFunctionContainerBase], previous_function_list: Iterable[EncodeFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of encode functions to be registered
        :type function_list: Iterable[EncodeFunctionContainerBase]
        :param previous_function_list: List of previously registered encode functions
        :type previous_function_list: Iterable[EncodeFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_ENCODE_FUNCTION_REGISTER, id)


class EncodeFunctionDeregisterEvent(FunctionRegisterEvent):
    """Event related to deregistering an encoding function
    """

    def __init__(self, function_list: Iterable[EncodeFunctionContainerBase], previous_function_list: Iterable[EncodeFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of encode functions to be unregistered
        :type function_list: Iterable[EncodeFunctionContainerBase]
        :param previous_function_list: List of previously unregistered encode functions
        :type previous_function_list: Iterable[EncodeFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_ENCODE_FUNCTION_DEREGISTER, id)


class DecodeFunctionRegisterEvent(FunctionRegisterEvent):
    """Event related to the registration of the decode function
    """

    def __init__(self, function_list: Iterable[DecodeFunctionContainerBase], previous_function_list: Iterable[DecodeFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of decode functions to be registered
        :type function_list: Iterable[DecodeFunctionContainerBase]
        :param previous_function_list: List of previously registered decode functions
        :type previous_function_list: Iterable[DecodeFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_DECODE_FUNCTION_REGISTER, id)


class DecodeFunctionDeregisterEvent(FunctionRegisterEvent):
    """Event related to deregistering an decoding function
    """

    def __init__(self, function_list: Iterable[DecodeFunctionContainerBase], previous_function_list: Iterable[DecodeFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of decode functions to be unregistered
        :type function_list: Iterable[DecodeFunctionContainerBase]
        :param previous_function_list: List of previously unregistered decode functions
        :type previous_function_list: Iterable[DecodeFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_DECODE_FUNCTION_DEREGISTER, id)


class SpectrumFunctionRegisterEvent(FunctionRegisterEvent):
    """Event related to the registration of the spectral function
    """

    def __init__(self, function_list: Iterable[SpectrumFunctionContainerBase], previous_function_list: Iterable[SpectrumFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of spectrum functions to be registered
        :type function_list: Iterable[SpectrumFunctionContainerBase]
        :param previous_function_list: List of previously registered spectrum functions
        :type previous_function_list: Iterable[SpectrumFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_SPECTRUM_FUNCTION_REGISTER, id)


class SpectrumFunctionDeregisterEvent(FunctionRegisterEvent):
    """Event related to deregistering a spectral function
    """

    def __init__(self, function_list: Iterable[SpectrumFunctionContainerBase], previous_function_list: Iterable[SpectrumFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of spectrum functions to be unregistered
        :type function_list: Iterable[SpectrumFunctionContainerBase]
        :param previous_function_list: List of previously unregistered spectrum functions
        :type previous_function_list: Iterable[SpectrumFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_SPECTRUM_FUNCTION_DEREGISTER, id)


class PeakFunctionRegisterEvent(FunctionRegisterEvent):
    """Event related to the registration of the peak function
    """

    def __init__(self, function_list: Iterable[PeakFunctionContainerBase], previous_function_list: Iterable[PeakFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of peak functions to be registered
        :type function_list: Iterable[PeakFunctionContainerBase]
        :param previous_function_list: List of previously registered peak functions
        :type previous_function_list: Iterable[PeakFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_PEAK_FUNCTION_REGISTER, id)


class PeakFunctionDeregisterEvent(FunctionRegisterEvent):
    """Event related to deregistering a peak function
    """

    def __init__(self, function_list: Iterable[PeakFunctionContainerBase], previous_function_list: Iterable[PeakFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of peak functions to be unregistered
        :type function_list: Iterable[PeakFunctionContainerBase]
        :param previous_function_list: List of previously unregistered peak functions
        :type previous_function_list: Iterable[PeakFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_PEAK_FUNCTION_DEREGISTER, id)


class MappingFunctionRegisterEvent(FunctionRegisterEvent):
    """Event related to the registration of the mapping function
    """

    def __init__(self, function_list: Iterable[MappingFunctionContainerBase], previous_function_list: Iterable[MappingFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of mapping functions to be registered
        :type function_list: Iterable[MappingFunctionContainerBase]
        :param previous_function_list: List of previously registered mapping functions
        :type previous_function_list: Iterable[MappingFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_MAPPING_FUNCTION_REGISTER, id)


class MappingFunctionDeregisterEvent(FunctionRegisterEvent):
    """Event related to deregistering a mapping function
    """

    def __init__(self, function_list: Iterable[MappingFunctionContainerBase], previous_function_list: Iterable[MappingFunctionContainerBase] = None, id=0):
        """Default constructor

        :param function_list: List of mapping functions to be unregistered
        :type function_list: Iterable[MappingFunctionContainerBase]
        :param previous_function_list: List of previously unregistered mapping functions
        :type previous_function_list: Iterable[MappingFunctionContainerBase]
        :type id: int, optional
        """
        super().__init__(function_list, previous_function_list, wxEVT_MAPPING_FUNCTION_DEREGISTER, id)


class RecipeSelectEvent(FunctionEvent):
    """Event related to the selection of a recipe
    """

    def __init__(self, recipe: Recipe, previous_recipe: Recipe, id=0):
        """Default constructor

        :param recipe: Selected recipe
        :type recipe: Recipe
        :param previous_recipe: Previously selected recipe
        :type previous_recipe: Recipe
        :type id: int, optional
        """
        super().__init__(wxEVT_RECIPE_SELECT, id)
        self.__recipe = recipe
        self.__prev_recipe = previous_recipe

    def GetRecipe(self) -> Recipe:
        """Get selected recipe

        :rtype: Recipe
        """
        return deepcopy(self.__recipe)

    def GetPreviousRecipe(self) -> Recipe:
        """Get previously selected recipe

        :rtype: Recipe
        """
        return deepcopy(self.__prev_recipe)

    def IsRecipeChanged(self) -> bool:
        """Return True, whather recipe is changed.

        :rtype: bool
        """
        return self.__recipe != self.__prev_recipe


class PresetEvent(FunctionEvent):
    """Event related to a preset
    """

    def __init__(self, preset_list: Iterable[Preset], eventType: int, id=0):
        """Default constructor

        :param preset_list: List of presets
        :type preset_list: Iterable[Preset]
        :param eventType: type of event
        :type eventType: int
        :type id: int, optional
        """
        super().__init__(eventType, id)
        self.__preset_list = preset_list

    def GetPresetList(self) -> Iterable[Preset]:
        """Get list of presets. This value is deepcopied.

        :rtype: Iterable[Preset]
        """
        return deepcopy(self.__preset_list)


class PresetRegisterEvent(PresetEvent):
    """Event related to preset registration
    """

    def __init__(self, preset_list: Iterable[Preset], previous_preset_list: Iterable[Preset] = None, id=0):
        """Default constructor

        :param preset_list: List of registered presets
        :type preset_list: Iterable[Preset]
        :param previous_preset_list: List of previously registered presets, defaults to None
        :type previous_preset_list: Iterable[Preset], optional
        :type id: int, optional
        """
        super().__init__(preset_list, wxEVT_PRESET_REGISTER, id)
        self.__prev_preset_list = [] if previous_preset_list is None else previous_preset_list

    def GetPreviousPresetList(self) -> Iterable[Preset]:
        """Get list of previously registered presets. This value is deepcopied.

        :rtype: Iterable[Preset]
        """
        return deepcopy(self.__prev_preset_list)


class PresetDeregisterEvent(PresetEvent):
    """Event related to deregistering presets
    """

    def __init__(self, preset_list: Iterable[Preset], previous_preset_list: Iterable[Preset] = None, id=0):
        """Default constructor

        :param preset_list: List of registered presets
        :type preset_list: Iterable[Preset]
        :param previous_preset_list: List of previously registered presets, defaults to None
        :type previous_preset_list: Iterable[Preset], optional
        :type id: int, optional
        """
        super().__init__(preset_list, wxEVT_PRESET_DEREGISTER, id)
        self.__prev_preset_list = [] if previous_preset_list is None else previous_preset_list

    def GetPreviousPresetList(self) -> Iterable[Preset]:
        """Get list of previously registered presets. This value is deepcopied.

        :rtype: Iterable[Preset]
        """
        return deepcopy(self.__prev_preset_list)


class PresetSelectEvent(PresetEvent):
    """Event related to preset selection
    """

    def __init__(self, preset_list: Iterable[Preset], id=0):
        """Default constructor

        :param preset_list: List of selected presets
        :type preset_list: Iterable[Preset]
        :type id: int, optional
        """
        super().__init__(preset_list, wxEVT_PRESET_SELECT, id)


class EncodeEvent(iSATexEvent):
    """Event related to encoding
    """

    def __init__(self, encoding: ChoiceContainer = None, delimiter: ChoiceContainer = None, previous_encoding: ChoiceContainer = None, previous_delimiter: ChoiceContainer = None, id=0):
        """Default constructor

        :param encoding: Encoding of the file to be read.
        :type encoding: ChoiceContainer, optional
        :param delimiter: Delimiter of the file to be read.
        :type delimiter: ChoiceContainer, optional
        :param previous_encoding: Encoding of the file to be read previously. Defaults to None
        :type previous_encoding: ChoiceContainer, optional
        :param previous_delimiter: Delimiter of the file to be read previously. Defaults to None
        :type previous_delimiter: ChoiceContainer, optional
        :type id: int, optional
        """
        super().__init__(wxEVT_ENCODE, id)
        self.__encode_type = encoding
        self.__previous_encode_type = previous_encoding
        self.__delimiter = delimiter
        self.__previous_delimiter = previous_delimiter

    def GetEncoding(self) -> ChoiceContainer:
        """Get encoding of the file to be read. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__encode_type)

    def GetPreviousEncoding(self) -> ChoiceContainer:
        """Get encoding of the file to be read previously. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__previous_encode_type)

    def IsEncodingChanged(self) -> bool:
        """Return True, encoding of file to be read is changed.

        :rtype: bool
        """
        return self.__encode_type != self.__previous_encode_type

    def GetDelimiter(self) -> ChoiceContainer:
        """Get delimiter of the file to be read. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__delimiter)

    def GetPreviousDelimiter(self) -> ChoiceContainer:
        """Get delimiter of the file to be read previously. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__previous_delimiter)

    def IsDelimiterChanged(self) -> bool:
        """Return True, delimiter of file to be read is changed.

        :rtype: bool
        """
        return self.__delimiter != self.__previous_delimiter


class DecodeEvent(iSATexEvent):
    """Event related to decoding
    """

    def __init__(self, encoding: ChoiceContainer = None, previous_encoding: ChoiceContainer = None, id=0):
        """Default constructor

        :param encoding: Encoding of the file to be read.
        :type encoding: ChoiceContainer, optional
        :param previous_encoding: Encoding of the file to be read previously. Defaults to None
        :type previous_encoding: ChoiceContainer, optional
        :type id: int, optional
        """
        super().__init__(wxEVT_DECODE, id)

        self.__encoding = encoding
        self.__prev_encoding = previous_encoding

    def GetEncoding(self) -> ChoiceContainer:
        """Get encoding of the file to be read. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__encoding)

    def GetPreviousEncoding(self) -> ChoiceContainer:
        """Get encoding of the file to be read previously. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__prev_encoding)

    def IsEncodingChanged(self) -> bool:
        """Return True, encoding of file to be read is changed.

        :rtype: bool
        """
        return self.__encoding != self.__prev_encoding


class MappingEvent(iSATexEvent):
    """Event related to mapping
    """

    def __init__(self, eventType: int, id=0):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int, optional
        """
        super().__init__(eventType, id)


class TableSizeChangeEvent(MappingEvent):
    """Event related to a change in the mapping table size
    """

    def __init__(self, table_size: Tuple[int, int], previous_table_size: Tuple[int, int], id=0):
        """Default constructor

        :param table_size: Table size used for mapping.
        :type table_size: Tuple[int, int]
        :param previous_table_size: Table sizes previously used for mapping.
        :type previous_table_size: Tuple[int, int]
        :type id: int, optional
        """
        super().__init__(wxEVT_TABLE_SIZE_CHANGE, id)

        if not self.__IsValidSize(table_size):
            raise TypeError()

        if not self.__IsValidSize(previous_table_size):
            raise TypeError()

        self.__table_size = table_size
        self.__prev_table_size = previous_table_size

    def GetTableSize(self) -> Tuple[int, int]:
        """Get table size used for mapping.

        :rtype: Tuple[int, int]
        """
        return self.__table_size

    def GetPreviousTableSize(self) -> Tuple[int, int]:
        """Get table sizes previously used for mapping

        :rtype: Tuple[int, int]
        """
        return self.__prev_table_size

    def __IsValidSize(self, size):
        return any((isinstance(v, int)) and v >= 1 for v in size)


class DirectionChangeEvent(MappingEvent):
    """Event related to a change in mapping direction
    """

    def __init__(self, direction: ChoiceContainer, previous_direction: ChoiceContainer, id=0):
        """Default constructor

        :param direction: The direction of mapping.
        :type direction: ChoiceContainer
        :param previous_direction: Previous direction of mapping.
        :type previous_direction: ChoiceContainer
        :type id: int, optional
        """
        super().__init__(wxEVT_DIRECTION_CHANGE, id)
        direction = Container2Value(direction)
        previous_direction = Container2Value(previous_direction)

        if not(direction == '' or direction in DEFAULT_DIRECTION_CONTAINER.GetChoices()):
            raise TypeError()

        if not(previous_direction == '' or previous_direction in DEFAULT_DIRECTION_CONTAINER.GetChoices()):
            raise TypeError()

        self.__direction = direction
        self.__prev_direction = previous_direction

    def GetDirection(self) -> ChoiceContainer:
        """Get the direction of mapping. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__direction)

    def GetPreviousDirection(self) -> ChoiceContainer:
        """Get the previous direction of mapping. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__prev_direction)


class ColormapChangeEvent(MappingEvent):
    """Event related to a change in the mapping's color map
    """

    def __init__(self, colormap: Colormap, prev_colormap: Colormap, id=0):
        """Default constructor

        :param colormap: Colormap for mapping.
        :type colormap: Colormap
        :param prev_colormap: Previous colormap for mapping.
        :type prev_colormap: Colormap
        :type id: int, optional
        """
        super().__init__(wxEVT_COLORMAP_CHANGE, id)

        self.__cmap = colormap
        self.__prev_cmap = prev_colormap

    def GetColormap(self) -> Colormap:
        """Get colormap for mapping.

        :rtype: Colormap
        """
        return self.__cmap

    def GetPreviousColormap(self) -> Colormap:
        """Get previous colormap for mapping.

        :rtype: Colormap
        """
        return self.__prev_cmap


class PeakTypeEvent(iSATexEvent):
    """Event related to the type of peak
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)


class PeakTypeChangeEvent(PeakTypeEvent):
    """Event related to a change in peak type
    """

    def __init__(self, peak_type: PeakType, previous_peak_type: PeakType = None, id=0):
        """Default constructor

        :param peak_type: Type of peak after change.
        :type peak_type: PeakType
        :param previous_peak_type: Type of peak before change. Defaults to None
        :type previous_peak_type: PeakType, optional
        :type id: int, optional
        """
        super().__init__(wxEVT_PEAK_TYPE_CHANGE, id)
        self.__peak_type = peak_type
        self.__prev_peak_type = previous_peak_type

    def GetPeakType(self) -> PeakType:
        """Get type of peak after change. This value is deepcopied.

        :rtype: PeakType
        """
        return deepcopy(self.__peak_type)

    def GetPreviousPeakType(self) -> PeakType:
        """Get type of peak before change. This value is deepcopied.

        :rtype: PeakType
        """
        return deepcopy(self.__prev_peak_type)


class PeakTypeRegisterEvent(PeakTypeEvent):
    """Event related to the registration of a peak type
    """

    def __init__(self, peak_type_list: Iterable[PeakType], previous_peak_type_list: Iterable[PeakType] = None, id=0):
        """Default constructor

        :param peak_type_list: The list of peak types after registration
        :type peak_type_list: Iterable[PeakType]
        :param previous_peak_type_list: The list of peak types before registration, defaults to None
        :type previous_peak_type_list: Iterable[PeakType], optional
        :type id: int, optional
        """
        super().__init__(wxEVT_PEAK_TYPE_REGISTER, id)
        self.__peak_type_list = peak_type_list
        self.__prev_peak_type_list = [] if previous_peak_type_list is None else previous_peak_type_list

    def GetPeakTypeList(self) -> Iterable[PeakType]:
        """Get the list of peak types after registration. This value is deepcopied.

        :rtype: Iterable[PeakType]
        """
        return deepcopy(self.__peak_type_list)

    def GetPreviousPeakTypeList(self) -> Iterable[PeakType]:
        """Get the list of peak types before registration. This value is deepcopied.

        :rtype: Iterable[PeakType]
        """
        return deepcopy(self.__prev_peak_type_list)

    def GetPeakTypeNames(self) -> List[str]:
        """Get the list of names of peak types after registration

        :rtype: List[str, ...]
        """
        return [peak_type.GetName() for peak_type in self.GetPeakTypeList()]

    def GetPreviousPeakTypeNames(self) -> List[str]:
        """Get the list of names of peak types before registration

        :rtype: List[str, ...]
        """
        return [peak_type.GetName() for peak_type in self.GetPreviousPeakType()]

    def GetNewPeakTypeList(self) -> Tuple[PeakType, ...]:
        """Get the list of newly added peak types

        :rtype: Tuple[PeakType, ...]
        """
        prev_pt_names = [pt.GetName() for pt in self.__prev_peak_type_list]
        return tuple([pt for pt in self.__peak_type_list if pt.GetName() not in prev_pt_names])

    def GetDeletePeakTypeList(self):
        """Get the list of deleted peak types

        :rtype: Tuple[PeakType, ...]
        """
        pt_names = [pt.GetName() for pt in self.__peak_type_list]
        return tuple([pt for pt in self.__prev_peak_type_list if pt.GetName() not in pt_names])


class PanelEvent(iSATexEvent):
    """Event related to the panel
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)


# class PanelSelectionChangeEvent(PanelEvent):
#     """Event related to panel selection
#     """

#     def __init__(self, panel: PanelBase, previous_panel: PanelBase, id=0):
#         """Default constructor

#         :param panel: Selected panel
#         :type panel: PanelBase
#         :param previous_panel: The previously selected panel
#         :type previous_panel: PanelBase
#         :type id: int, optional
#         """
#         super().__init__(wxEVT_PANEL_SELECTION_CHANGE, id)
#         self.__panel = panel
#         self.__previous_panel = previous_panel

#     def GetPanel(self) -> PanelBase:
#         """Get selected panel

#         :rtype: PanelBase
#         """
#         return self.__panel

#     def GetPreviousPanel(self) -> PanelBase:
#         """Get previously selected panel

#         :rtype: PanelBase
#         """
#         return self.__previous_panel


# class PanelViewEvent(PanelEvent):
#     """Event related to the display of the panel
#     """

#     def __init__(self, show_panel_list: Iterable[PanelBase] = None, hide_panel_list: Iterable[PanelBase] = None, id=0):
#         """Default constructor

#         :param show_panel_list: Shown panel list, defaults to None
#         :type show_panel_list: Iterable[PanelBase], optional
#         :param hide_panel_list: Hidden panel list, defaults to None
#         :type hide_panel_list: Iterable[PanelBase], optional
#         :type id: int, optional
#         """
#         super().__init__(wxEVT_PANEL_VIEW, id)
#         self.__show_panel_list = [] if show_panel_list is None else show_panel_list
#         self.__hide_panel_list = [] if hide_panel_list is None else hide_panel_list

#     def GetShowPanelList(self) -> Iterable[PanelBase]:
#         """Get shown panel list

#         :rtype: Iterable[PanelBase]
#         """
#         return self.__show_panel_list

#     def GetHidePanelList(self) -> Iterable[PanelBase]:
#         """Get hidden panel list

#         :rtype: Iterable[PanelBase]
#         """
#         return self.__hide_panel_list


# class PanelRegisterEvent(PanelEvent):
#     """Event related to the registration of a panel
#     """

#     def __init__(self, panel_list: Iterable[PanelBase], previous_panel_list: Iterable[PanelBase] = None, id=0):
#         """Default constructor

#         :param panel_list: The list of panel after registration
#         :type panel_list: Iterable[PanelBase]
#         :param previous_panel_list: The list of panel before registration, defaults to None
#         :type previous_panel_list: Iterable[PanelBase], optional
#         :type id: int, optional
#         """
#         super().__init__(wxEVT_PANEL_REGISTER, id)

#         self.__panel_list = panel_list
#         self.__prev_panel_list = previous_panel_list

#     def GetPanelList(self) -> Iterable[PanelBase]:
#         """Get the list of panel after registration

#         :rtype: Iterable[PanelBase]
#         """
#         return self.__panel_list

#     def GetPreviousPanelList(self) -> Iterable[PanelBase]:
#         """Get the list of panel before registration

#         :rtype: Iterable[PanelBase]
#         """
#         return self.__prev_panel_list

#     def GetNewPanelList(self) -> Tuple[PanelBase, ...]:
#         """Get the list of newly added panels

#         :rtype: Tuple[PanelBase, ...]
#         """
#         prev_panel_names = [panel.__class__.__name__ for panel in self.__prev_panel_list]
#         return tuple([panel for panel in self.__panel_list if panel.__class__.__name__ not in prev_panel_names])

#     def GetDeletePanelList(self) -> Tuple[PanelBase, ...]:
#         """Get the list of deleted panels

#         :rtype: Tuple[PanelBase, ...]
#         """
#         panel_names = [panel.__class__.__name__ for panel in self.__panel_list]
#         return tuple([panel for panel in self.__prev_panel_list if panel.__class__.__name__ not in panel_names])


class PanelSelectionChangeEvent(PanelEvent):
    """Event related to panel selection
    """

    def __init__(self, panel, previous_panel, id=0):
        """Default constructor

        :param panel: Selected panel
        :type panel: PanelBase
        :param previous_panel: The previously selected panel
        :type previous_panel: PanelBase
        :type id: int, optional
        """
        super().__init__(wxEVT_PANEL_SELECTION_CHANGE, id)
        self.__panel = panel
        self.__previous_panel = previous_panel

    def GetPanel(self):
        """Get selected panel

        :rtype: PanelBase
        """
        return self.__panel

    def GetPreviousPanel(self):
        """Get previously selected panel

        :rtype: PanelBase
        """
        return self.__previous_panel


class PanelViewEvent(PanelEvent):
    """Event related to the display of the panel
    """

    def __init__(self, show_panel_list=None, hide_panel_list=None, id=0):
        """Default constructor

        :param show_panel_list: Shown panel list, defaults to None
        :type show_panel_list: Iterable[PanelBase], optional
        :param hide_panel_list: Hidden panel list, defaults to None
        :type hide_panel_list: Iterable[PanelBase], optional
        :type id: int, optional
        """
        super().__init__(wxEVT_PANEL_VIEW, id)
        self.__show_panel_list = [] if show_panel_list is None else show_panel_list
        self.__hide_panel_list = [] if hide_panel_list is None else hide_panel_list

    def GetShowPanelList(self):
        """Get shown panel list

        :rtype: Iterable[PanelBase]
        """
        return self.__show_panel_list

    def GetHidePanelList(self):
        """Get hidden panel list

        :rtype: Iterable[PanelBase]
        """
        return self.__hide_panel_list


class PanelRegisterEvent(PanelEvent):
    """Event related to the registration of a panel
    """

    def __init__(self, panel_list, previous_panel_list=None, id=0):
        """Default constructor

        :param panel_list: The list of panel after registration
        :type panel_list: Iterable[PanelBase]
        :param previous_panel_list: The list of panel before registration, defaults to None
        :type previous_panel_list: Iterable[PanelBase], optional
        :type id: int, optional
        """
        super().__init__(wxEVT_PANEL_REGISTER, id)

        self.__panel_list = panel_list
        self.__prev_panel_list = previous_panel_list

    def GetPanelList(self):
        """Get the list of panel after registration

        :rtype: Iterable[PanelBase]
        """
        return self.__panel_list

    def GetPreviousPanelList(self):
        """Get the list of panel before registration

        :rtype: Iterable[PanelBase]
        """
        return self.__prev_panel_list

    def GetNewPanelList(self):
        """Get the list of newly added panels

        :rtype: Tuple[PanelBase, ...]
        """
        prev_panel_names = [panel.__class__.__name__ for panel in self.__prev_panel_list]
        return tuple([panel for panel in self.__panel_list if panel.__class__.__name__ not in prev_panel_names])

    def GetDeletePanelList(self):
        """Get the list of deleted panels

        :rtype: Tuple[PanelBase, ...]
        """
        panel_names = [panel.__class__.__name__ for panel in self.__panel_list]
        return tuple([panel for panel in self.__prev_panel_list if panel.__class__.__name__ not in panel_names])


class LayoutEvent(PanelEvent):
    """Event related to the layout
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)


class LayoutChangeEvent(LayoutEvent):
    """Event related to a layout change
    """

    def __init__(self, layout: str, previous_layout: str, id=0):
        """Default constructor

        :param layout: Layout after selection
        :type layout: str
        :param previous_layout: Layout before selection
        :type previous_layout: str
        :type id: int, optional
        """
        super().__init__(wxEVT_LAYOUT_CHANGE, id)

        self.__layout = layout
        self.__prev_layout = previous_layout

    def GetLayout(self) -> str:
        """Get layout after selection

        :rtype: str
        """
        return self.__layout

    def GetPreviousLayout(self) -> str:
        """Get layout before selection

        :rtype: str
        """
        return self.__prev_layout


class LayoutRegisterEvent(LayoutEvent):
    """Event related to registering a layout
    """

    def __init__(self, layout_list: Iterable[Tuple[str, str]], previous_layout_list: Iterable[Tuple[str, str]], id=0):
        """Default constructor

        :param layout_list: List of layouts after registration, refer to wxPython (https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html#wx.lib.agw.aui.framemanager.AuiManager.SavePerspective) for details.
        :type layout_list: Iterable[Iterable[str, str]]
        :param previous_layout_list: List of layouts before registration
        :type previous_layout_list: Iterable[Iterable[str, str]]
        :type id: int, optional
        """
        super().__init__(wxEVT_LAYOUT_REGISTER, id)

        self.__layout_list = layout_list
        self.__previous_layout_list = previous_layout_list

    def GetLayoutList(self) -> Iterable[Tuple[str, str]]:
        """Get list of layouts after registration

        :rtype: Iterable[Iterable[str, str]]
        """
        return deepcopy(self.__layout_list)

    def GetLayoutNames(self) -> Iterable[str]:
        """Get list of names for the layout after registration

        :rtype: Iterable[str]
        """
        return tuple([layout[0] for layout in self.__layout_list])

    def GetPreviousLayoutList(self) -> Iterable[Tuple[str, str]]:
        """Get list of layouts before registration

        :rtype: Iterable[Iterable[str, str]]
        """
        return deepcopy(self.__prev_layout_list)

    def GetPreviousLayoutNames(self):
        """Get list of names for the layout before registration

        :rtype: Iterable[str]
        """
        return tuple([layout[0] for layout in self.__prev_layout_list])


class PreferenceEvent(iSATexEvent):
    """Event related to the preferences
    """

    def __init__(self, data_buffer_size: Union[int, IntContainer], previous_data_buffer_size: Union[int, IntContainer], id=0):
        """Default constructor

        :param data_buffer_size: Size of the buffer for after data recovery
        :type data_buffer_size: Union[int, IntContainer]
        :param previous_data_buffer_size: Size of the buffer for before data recovery
        :type previous_data_buffer_size: int
        :type id: Union[int, IntContainer], optional
        """
        super().__init__(wxEVT_PREFERENCE, id)
        self.__data_buffer_size = self.__DataBufferSizeFormmat(data_buffer_size)
        self.__previous_data_buffer_size = self.__DataBufferSizeFormmat(previous_data_buffer_size)

    def GetPreviousDataBufferSize(self) -> int:
        """Get size of the buffer for before data recovery

        :rtype: int
        """
        return self.__DataBufferSizeFormmat(self.__previous_data_buffer_size)

    def GetDataBufferSize(self) -> int:
        """Get size of the buffer for after data recovery

        :rtype: int
        """
        return self.__DataBufferSizeFormmat(self.__data_buffer_size)

    def IsDataBufferSizeChanged(self) -> bool:
        """Returns True if the size of the data recovery buffer has been changed.

        :rtype: bool
        """
        return self.GetDataBufferSize() != self.GetPreviousDataBufferSize()

    def __DataBufferSizeFormmat(self, dbs) -> int:
        if isinstance(dbs, IntContainer):
            return dbs.GetValue()

        if not isinstance(dbs, int):
            raise TypeError()

        return dbs


class ColorEvent(iSATexEvent):
    """a color-related event
    """

    def __init__(self, eventType: int, id: int):
        """Default constructor

        :param eventType: Type of event
        :type eventType: int
        :type id: int
        """
        super().__init__(eventType, id)


class ColorRegisterEvent(ColorEvent):
    """Event related to color registration
    """

    def __init__(self, color_theme_list: Iterable[str], previous_color_theme_list: Iterable[str], id=0):
        """Default constructor

        :param color_theme_list: List of color themes after registration
        :type color_theme_list: Iterable[str]
        :param previous_color_theme_list: List of color themes before registration
        :type previous_color_theme_list: Iterable[str]
        :type id: int, optional
        """
        super().__init__(wxEVT_COLOR_REGISTER, id)

        self.__color_theme_list = color_theme_list
        self.__prev_color_theme_list = previous_color_theme_list

    def GetColorThemeList(self):
        """Get list of color themes after registration

        :rtype: str
        """
        return self.__color_theme_list

    def GetPreviousColorThemeList(self):
        """Get list of color themes before registration

        :rtype: str
        """
        return self.__prev_color_theme_list


class ColorSelectionEvent(ColorEvent):
    """Event related to color selection
    """

    def __init__(self, color_theme: str, id=0):
        """Default constructor

        :param color_theme: List of color themes after selection
        :type color_theme: str
        :type id: int, optional
        """
        super().__init__(wxEVT_COLOR_REGISTER, id)

        self.__color_theme = color_theme

    def Get(self, key) -> Colour:
        """Get the color of the specified key.

        :param key: The color of the specified key.
        :type key: Colour
        :rtype: Colour
        """
        return self.__color_theme.Get(key)

    def GetName(self) -> str:
        """Get a name for your color theme.

        :rtype: str
        """
        return self.__color_theme[NAME]

    def GetMainSelectionColor(self) -> Colour:
        """Get main selection color

        :rtype: Colour
        """
        return self.__color_theme.Get(MAIN_SELECTION_COLOR)

    def GetSelectionColor(self) -> Colour:
        """Get selection color

        :rtype: Colour
        """
        return self.__color_theme.Get(SELECTION_COLOR)

    def GetSuccessColor(self) -> Colour:
        """Get success color

        :rtype: Colour
        """
        return self.__color_theme.Get(SUCCESS_COLOR)

    def GetErrorColor(self) -> Colour:
        """Get error color

        :rtype: Colour
        """
        return self.__color_theme.Get(ERROR_COLOR)


class LaunchEvent(iSATexEvent):
    """iSATex launched event
    """

    def __init__(self, id=0):
        """Default constructor

        :type id: int, optional
        """
        super().__init__(wxEVT_LAUNCH, id)


class ExitEvent(iSATexEvent):
    """iSATex exit event
    """

    def __init__(self, id=0):
        """Default constructor

        :type id: int, optional
        """
        super().__init__(wxEVT_EXIT, id)


__all__ = [
    'ProjectEvent',
    'ProjectLoadEvent',
    'ProjectNewEvent',
    'ProjectOpenEvent',
    'ProjectSaveEvent',
    'ProjectMemoChangeEvent',
    'DataEvent',
    'DataContentsChangeEvent',
    'DataSelectionChangeEvent',
    'FunctionEvent',
    'EncodeFunctionSelectEvent',
    'DecodeFunctionSelectEvent',
    'SpectrumFunctionListSelectEvent',
    'MappingFunctionSelectEvent',
    'FunctionRegisterEvent',
    'EncodeFunctionRegisterEvent',
    'EncodeFunctionDeregisterEvent',
    'DecodeFunctionRegisterEvent',
    'DecodeFunctionDeregisterEvent',
    'SpectrumFunctionRegisterEvent',
    'SpectrumFunctionDeregisterEvent',
    'PeakFunctionRegisterEvent',
    'PeakFunctionDeregisterEvent',
    'MappingFunctionRegisterEvent',
    'MappingFunctionDeregisterEvent',
    'RecipeSelectEvent',
    'PresetEvent',
    'PresetRegisterEvent',
    'PresetDeregisterEvent',
    'PresetSelectEvent',
    'EncodeEvent',
    'DecodeEvent',
    'MappingEvent',
    'TableSizeChangeEvent',
    'DirectionChangeEvent',
    'ColormapChangeEvent',
    'PeakTypeEvent',
    'PeakTypeChangeEvent',
    'PeakTypeRegisterEvent',
    'PanelEvent',
]
