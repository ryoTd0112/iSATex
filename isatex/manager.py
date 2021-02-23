import sys
from collections import deque
from copy import deepcopy
from datetime import date
from glob import glob
from importlib import import_module
from inspect import getmembers, isclass, isfunction
from json import JSONEncoder, dumps, load, loads
from json.decoder import JSONDecodeError
from logging import DEBUG, getLogger
from os import getcwd, mkdir
from os.path import abspath, dirname, exists, join
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from zlib import compress, decompress

from matplotlib.colors import Colormap
from matplotlib.lines import Line2D
from numpy import inf, ndarray
from wx import (CANCEL, CENTRE, ICON_INFORMATION, ID_CANCEL, ID_CLOSE,
                ITEM_NORMAL, NOT_FOUND, OK, LogError, Menu, MenuBar, MenuItem,
                MessageDialog, NewIdRef, Window, wxEVT_COMMAND_MENU_SELECTED)
from wx.lib.agw.aui.framemanager import (AUI_BUTTON_CLOSE,
                                         AUI_MGR_ALLOW_ACTIVE_PANE,
                                         AUI_MGR_ALLOW_FLOATING,
                                         AUI_MGR_LIVE_RESIZE,
                                         AUI_MGR_TRANSPARENT_DRAG, AuiManager,
                                         AuiPaneInfo)

from const import (ABOUT_MENU_ITEM, COLOR, COLOR_THEME,
                   COLOR_THEME_FOLDER_PATH, COLOR_THEME_LIST, COLORMAP, CUSTOM,
                   DATA_BUFFER_SIZE, DATA_MANAGER, DECODE, DECODE_ENCODING,
                   DECODE_FUNCTION_CLASS_LIST, DEFAULT, DEFAULT_COLOR_THEME,
                   DEFAULT_COLORMAP, DELIMITER, DIRECTION, EDIT_MENU, ENCODE,
                   ENCODE_DELIMITER, ENCODE_ENCODING,
                   ENCODE_FUNCTION_CLASS_LIST, ENCODING, ERROR_COLOR,
                   EVENT_LIST, EVENT_MANAGER, EVENT_RECEPTOR_CLASS_LIST,
                   EXIT_MENU_ITEM, EXPORT_MENU_ITEM, EXPORT_PLUGIN_MENU_ITEM,
                   FILE_MENU, FUNCTION, FUNCTION_CLASS_LIST, FUNCTION_MANAGER,
                   HELP_MENU, ID_SAVE, IMPORT_PLUGIN_MENU_ITEM, LAYOUT,
                   LAYOUT_MENU, LIST, MAIN_SELECTION_COLOR, MAIN_WINDOW,
                   MANAGER_LIST, MAPPING, MAPPING_COLORMAP, MAPPING_DIRECTION,
                   MAPPING_FUNCTION_CLASS_LIST, MAPPING_TABLE_SIZE,
                   MAX_DATA_BUFFER_SIZE, MENU_ITEM_LIST, MENUBAR_MANAGER, NAME,
                   NEW_MENU_ITEM, OPEN_MENU_ITEM, PANEL_CLASS_LIST,
                   PANEL_MANAGER, PEAK_FUNCTION_CLASS_LIST, PEAK_MANAGER,
                   PEAK_MENU, PEAK_TYPE, PERSPECTIVE_SETTING,
                   PLUGIN_FOLDER_PATH, PLUGIN_MENU, PREFERENCE_MENU_ITEM,
                   PRESET_LIST, PROJECT_MANAGER, PROJECT_MEMO_MENU_ITEM,
                   PROJECT_MENU, SAVE_AS_MENU_ITEM, SAVE_ENCODING,
                   SAVE_MENU_ITEM, SELECTED, SELECTED_DECODE_FUNCTION,
                   SELECTED_ENCODE_FUNCTION, SELECTED_LAYOUT,
                   SELECTED_MAPPING_FUNCTION, SELECTION_COLOR, SEPARATOR,
                   SETTING_FILE_PATH, SETTING_STORABLE_OBJECT_CLASS_LIST, SHOW,
                   SHOW_PANEL_MENU, SPECTRUM, SPECTRUM_FUNCTION_CLASS_LIST,
                   SPECTRUM_FUNCTION_PRESET_LIST, SPECTRUM_LAYOUT,
                   SPECTRUM_PANEL, STORABLE_OBJECT_DICT, SUCCESS_COLOR,
                   TABLE_SIZE, TEMPORARY, TUTORIAL_MENU_ITEM, UNKNOWN,
                   VIEW_MENU, WINDOW_SIZE)
from container import (CustomCheckMenuItemBase, CustomMenuItemBase,
                       CustomNormalMenuItemBase, CustomRadioMenuItemBase,
                       EventReceptorBase, LayoutMenuItem, PanelBase,
                       PeakMenuItem, ShowPanelMenuItem)
from control import SaveCheckDialog
from core import (CommunicableObjectBase, RestrictedStorableListBase,
                  SettingStorableObjectBase, StorableObject, iSATexObject)
from defaultevent import (ColormapChangeEvent, ColorRegisterEvent,
                          ColorSelectionEvent, DataContentsChangeEvent,
                          DataSelectionChangeEvent, DecodeEvent,
                          DecodeFunctionDeregisterEvent,
                          DecodeFunctionRegisterEvent,
                          DecodeFunctionSelectEvent, DirectionChangeEvent,
                          EncodeEvent, EncodeFunctionDeregisterEvent,
                          EncodeFunctionRegisterEvent,
                          EncodeFunctionSelectEvent, LayoutChangeEvent,
                          LayoutRegisterEvent, MappingFunctionDeregisterEvent,
                          MappingFunctionRegisterEvent,
                          MappingFunctionSelectEvent, PanelRegisterEvent,
                          PanelSelectionChangeEvent, PanelViewEvent,
                          PeakFunctionDeregisterEvent,
                          PeakFunctionRegisterEvent, PeakTypeChangeEvent,
                          PeakTypeRegisterEvent, PreferenceEvent,
                          PresetDeregisterEvent, PresetRegisterEvent,
                          ProjectMemoChangeEvent, ProjectNewEvent,
                          ProjectOpenEvent, ProjectSaveEvent,
                          RecipeSelectEvent, SpectrumFunctionDeregisterEvent,
                          SpectrumFunctionListSelectEvent,
                          SpectrumFunctionRegisterEvent, TableSizeChangeEvent,
                          iSATexEvent, iSATexEventBinder, wxEVT_COLOR_REGISTER,
                          wxEVT_COLOR_SELECT, wxEVT_COLORMAP_CHANGE,
                          wxEVT_DATA_CONTENTS_CHANGE,
                          wxEVT_DATA_SELECTION_CHANGE, wxEVT_DECODE,
                          wxEVT_DECODE_FUNCTION_DEREGISTER,
                          wxEVT_DECODE_FUNCTION_REGISTER,
                          wxEVT_DECODE_FUNCTION_SELECT, wxEVT_DIRECTION_CHANGE,
                          wxEVT_ENCODE, wxEVT_ENCODE_FUNCTION_DEREGISTER,
                          wxEVT_ENCODE_FUNCTION_REGISTER,
                          wxEVT_ENCODE_FUNCTION_SELECT, wxEVT_EXIT,
                          wxEVT_LAUNCH, wxEVT_LAYOUT_REGISTER,
                          wxEVT_MAPPING_FUNCTION_DEREGISTER,
                          wxEVT_MAPPING_FUNCTION_REGISTER,
                          wxEVT_PANEL_REGISTER, wxEVT_PANEL_SELECTION_CHANGE,
                          wxEVT_PANEL_VIEW, wxEVT_PEAK_FUNCTION_DEREGISTER,
                          wxEVT_PEAK_FUNCTION_REGISTER, wxEVT_PEAK_TYPE_CHANGE,
                          wxEVT_PEAK_TYPE_REGISTER, wxEVT_PREFERENCE,
                          wxEVT_PRESET_DEREGISTER, wxEVT_PRESET_REGISTER,
                          wxEVT_PROJECT_MEMO_CHANGE, wxEVT_PROJECT_NEW,
                          wxEVT_PROJECT_OPEN, wxEVT_PROJECT_SAVE,
                          wxEVT_RECIPE_SELECT,
                          wxEVT_SPECTRUM_FUNCTION_DEREGISTER,
                          wxEVT_SPECTRUM_FUNCTION_LIST_SELECT,
                          wxEVT_SPECTRUM_FUNCTION_REGISTER,
                          wxEVT_TABLE_SIZE_CHANGE)
from defaultpanel import SpectrumPanel
from objects import (DEFAULT_BUFFER_SIZE, DEFAULT_DECODE_FUNCTION,
                     DEFAULT_DIRECTION_CONTAINER, DEFAULT_ENCODE_FUNCTION,
                     DEFAULT_MAPPING_FUNCTION, DEFAULT_PEAK_TYPE,
                     NEW_PROJECT_NAME, ArgumentContainerBase,
                     BoundedArgumentContainerBase, ChoiceContainer,
                     DataContainer, DecodeFunctionContainerBase,
                     EncodeFunctionContainerBase, FunctionContainerBase,
                     IntContainer, MappingFunctionContainerBase,
                     PeakFunctionContainerBase, PeakFunctionContainerList,
                     PeakType, Preset, Project, Recipe, Spectrum,
                     SpectrumFunctionContainerBase)
from util import (Camel2Pascal, DotChain, DotNotationDict,
                  FindWindowToAncestors, GetFileName, GetShowPanelLabel,
                  HasValidElement, Singleton)

logger = getLogger('__main__').getChild(__name__)
logger.setLevel(DEBUG)


class IOManager(Singleton):
    """
    This class manages the external communication.
    The communication is mainly for configuring the application and loading and saving experimental data.
    """
    SAVE_MARKER_CLASS_NAME: str = '0__SAVE_CLASS_NAME__'
    SAVE_MARKER_DATA: str = '1__SAVE_DATA__'

    def __init__(self, setting_file_path: str, core_mgr):
        """Default constructor

        :param setting_file_path: Path to a file to read the setting.
        :type setting_file_path: str
        :type core_mgr: CoreManager
        """
        super().__init__()
        self.__id = NewIdRef()
        self.__core_mgr = core_mgr

        self.__setting_file_path = setting_file_path
        self.__used_setting = DotNotationDict()

        dir_name = dirname(__file__)

        default_path_list = [
            'objects.py',
            'container.py',
            'defaultevent.py',
            'defaultpeakfunction.py',
            'defaultdecodefunction.py',
            'defaultencodefunction.py',
            'defaultspectrumfunction.py',
            'defaultmappingfunction.py',
            'defaultpanel.py',
            'defaultmenuitem.py'
        ]
        exclude_class_list = [
            iSATexObject,
            CommunicableObjectBase,
            StorableObject,
            RestrictedStorableListBase,
            EventReceptorBase,
            ArgumentContainerBase,
            BoundedArgumentContainerBase,
            FunctionContainerBase,
            SpectrumFunctionContainerBase,
            DecodeFunctionContainerBase,
            EncodeFunctionContainerBase,
            PeakFunctionContainerBase,
            MappingFunctionContainerBase,
            PanelBase,
            CustomMenuItemBase,
            CustomNormalMenuItemBase,
            CustomRadioMenuItemBase,
            CustomCheckMenuItemBase,
            ShowPanelMenuItem,
            PeakMenuItem,
            LayoutMenuItem,
        ]

        plugin_path_list = self.__GetPluginPathList()
        iSATex_obj_list = self.__ImportObjectList(default_path_list + plugin_path_list, iSATexObject, exclude_class_list)

        storable_object_list = [Class() for Class in iSATex_obj_list if isclass(Class) and issubclass(Class, StorableObject) and Class not in exclude_class_list]
        storable_dict = {storable_object.__class__.__name__: storable_object for storable_object in storable_object_list}

        self.__temp_setting = DotNotationDict()
        self.__temp_setting.forced_setitem(STORABLE_OBJECT_DICT, storable_dict)

        dir_name = dirname(__file__)
        self.__setting = self.__ImportSetting(join(dir_name, setting_file_path))

        class_import_design = (
            (FUNCTION_CLASS_LIST, (PeakFunctionContainerBase, DecodeFunctionContainerBase, EncodeFunctionContainerBase, SpectrumFunctionContainerBase, MappingFunctionContainerBase,), False,),
            (PEAK_FUNCTION_CLASS_LIST, PeakFunctionContainerBase, False,),
            (DECODE_FUNCTION_CLASS_LIST, DecodeFunctionContainerBase, False,),
            (ENCODE_FUNCTION_CLASS_LIST, EncodeFunctionContainerBase, False,),
            (SPECTRUM_FUNCTION_CLASS_LIST, SpectrumFunctionContainerBase, False,),
            (MAPPING_FUNCTION_CLASS_LIST, MappingFunctionContainerBase, False,),
            (PANEL_CLASS_LIST, PanelBase, False,),
            (MENU_ITEM_LIST, CustomMenuItemBase, False,),
            (EVENT_LIST, iSATexEventBinder, True,),
            (EVENT_RECEPTOR_CLASS_LIST, EventReceptorBase, False,),
            (SETTING_STORABLE_OBJECT_CLASS_LIST, SettingStorableObjectBase, False,),
        )

        for key, BaseClass, instanced in class_import_design:
            obj_list = []
            for iSATex_obj in iSATex_obj_list:
                if instanced:
                    if not isinstance(iSATex_obj, BaseClass):
                        continue
                else:
                    if not (isclass(iSATex_obj) and issubclass(iSATex_obj, BaseClass) or iSATex_obj in exclude_class_list):
                        continue

                obj_list.append(iSATex_obj)

            self.__temp_setting.forced_setitem(key, obj_list)

        color_theme_list = []
        for path in self.__GetColorThemePathList():
            color_theme_list.append(self.__ImportSetting(path))

        self.__temp_setting.forced_setitem(COLOR_THEME_LIST, color_theme_list)

    def GetSetting(self, *args) -> Any:
        """
        This function get the settings held by this class.
        The settings are classified into three types: "SETTING", custom, and default.
        Note that the key is converted to prevent contamination of these settings.

        :param key: The key used to search for settings.
        :type key: Any type
        :param default: The return value to be used when the specified key was not found., defaults to None
        :type default: Any type, optional
        :return: Value for the specified key. Or the Default value.
        :rtype: Any type
        """
        if not 1 <= len(args) <= 2:
            raise TypeError()

        key = args[0]
        default = self.GetInitialSetting(key, args[1]) if len(args) == 2 else self.GetInitialSetting(key)

        if key in self.__temp_setting:
            value = self.__temp_setting.get(key, default)
            return value() if isfunction(value) else value

        if self.IsDefaultSetting(key) or DotChain(DEFAULT, key) in self.GetInitialSetting():
            key = DotChain(DEFAULT, key)
        else:
            key = DotChain(CUSTOM, key)

        self.__used_setting.forced_setitem(key, True)
        return self.__setting.get(key, default)

    def SetSetting(self, key: Any, value: Any) -> None:
        """
            This function sets the value to the specified key.
            "key" is acceptable with DotNotation. For more information, see Documentation of "DotNotationDict" class.

        :param key: The key used to search for settings.
        :type key: Any type
        :param value: Stored value.
        :type value: Any type
        """
        if self.IsDefaultSetting(key):
            self.__setting.forced_setitem(DotChain(DEFAULT, key), value)
            self.__used_setting.forced_setitem(DotChain(DEFAULT, key), True)
        else:
            self.__setting.forced_setitem(DotChain(CUSTOM, key), value)
            self.__used_setting.forced_setitem(DotChain(CUSTOM, key), True)

    def GetInitialSetting(self, *args) -> dict:
        """This function returns the initial value of the setting.

        :return: Initial value of the setting.
        :rtype: bool
        """
        if len(args) >= 3:
            raise TypeError()

        if not hasattr(self, '_initial_setting'):
            self._initial_setting = DotNotationDict({
                CUSTOM: {},
                DEFAULT: {
                    COLOR_THEME: {
                        SELECTED: "Default Color",
                        LIST: [],
                    },
                    DECODE: {
                        ENCODING: ChoiceContainer('utf-8', ['utf-8', 'shift_jis', 'euc_jp']),
                    },
                    ENCODE: {
                        ENCODING: ChoiceContainer('utf-8', ['utf-8', 'shift_jis', 'euc_jp']),
                        DELIMITER: ChoiceContainer('Comma[,]', ['Colon[:]', 'Tab[\t]', 'Space[ ]', 'Comma[,]', 'Equals Sign[=]', 'Semicolon[;]']),
                    },
                    MAPPING: {
                        DIRECTION: DEFAULT_DIRECTION_CONTAINER,
                        TABLE_SIZE: (10, 10),
                        COLORMAP: DEFAULT_COLORMAP
                    },
                    FUNCTION: {
                        SPECTRUM: {
                            PRESET_LIST: [],
                        },
                        ENCODE: {
                            SELECTED: DEFAULT_ENCODE_FUNCTION,
                        },
                        DECODE: {
                            SELECTED: DEFAULT_DECODE_FUNCTION,
                        },
                        MAPPING: {
                            SELECTED: DEFAULT_MAPPING_FUNCTION,
                        },
                    },
                    DATA_BUFFER_SIZE: DEFAULT_BUFFER_SIZE,
                    PEAK_TYPE: DEFAULT_PEAK_TYPE,
                    WINDOW_SIZE: [
                        800,
                        800
                    ],
                    LAYOUT: {
                        LIST: (
                            SPECTRUM_LAYOUT,
                        ),
                        SELECTED: SPECTRUM_LAYOUT,
                    },
                    PERSPECTIVE_SETTING: '',
                }
            })
        if len(args) != 0:
            key = args[0]
            default = args[1] if len(args) == 2 else None
            value = self._initial_setting.get(DotChain(CUSTOM, key), default)
            value = self._initial_setting.get(DotChain(DEFAULT, key), default) if value is default else value
            return value
        else:
            return self._initial_setting

    def GetSettingType(self, key) -> str:
        """This function returns the type to which the key belongs.

        :param key: The key used to search for settings.
        :type key: Any type
        :return: Setting type.
        :rtype: bool
        """
        if key in self.__setting[DEFAULT]:
            return DEFAULT
        elif key in self.__setting[CUSTOM]:
            return CUSTOM
        elif key in self.__temp_setting:
            return TEMPORARY
        else:
            return UNKNOWN

    def IsDefaultSetting(self, key) -> bool:
        """This function returns whether the specified key is for "DEFAULT".

        :param key: The key used to search for settings.
        :type key: Any type
        :return: Whether the "key" specifies "DEFAULT" or not.
        :rtype: bool
        """
        return self.GetSettingType(key) == DEFAULT

    def IsCustomSetting(self, key) -> bool:
        """This function returns whether the specified key is for "CUSTOM".

        :param key: The key used to search for settings.
        :type key: Any type
        :return: Whether the "key" specifies "CUSTOM" or not.
        :rtype: bool
        """
        return self.GetSettingType(key) == CUSTOM

    def IsTemporarySetting(self, key) -> bool:
        """This function returns whether the specified key is for "TEMPORARY".

        :param key: The key used to search for settings.
        :type key: Any type
        :return: Whether the "key" specifies "TEMPORARY" or not.
        :rtype: bool
        """
        return self.GetSettingType(key) == TEMPORARY

    def IsUnknownSetting(self, key) -> bool:
        """This function returns whether the specified key is for "UNKNOWN".

        :param key: The key used to search for settings.
        :type key: Any type
        :return: Whether the "key" specifies "TEMPORARY" or not.
        :rtype: bool
        """
        return self.GetSettingType(key) == UNKNOWN

    def SaveSetting(self):
        """
        This function saves the state of the application to an external file.
        Not all settings will be saved, but those that meet all of the following conditions will be saved
        * Belong to either "DEFAULT_SETTIN" or "CUSTOM_SETTING".
        * Have been used at least once in the application.
        """
        # Remove unused setting
        save_setting = DotNotationDict()
        initial_setting = self.GetInitialSetting()
        for key, value in self.__setting.items(True):
            if not (key in self.__used_setting or key in initial_setting):
                continue

            save_setting.forced_setitem(key, value)

        # Add the missind default setting
        for key, value in self.GetInitialSetting().items(True):
            if key in save_setting:
                continue

            save_setting.forced_setitem(key, value)

        app_setting = dumps(save_setting, ensure_ascii=False, indent=4, sort_keys=True, cls=IOManager.iSATexJsonEncoder)
        logger.debug(f'Save setting {app_setting}')
        dir_name = dirname(__file__)
        path = join(dir_name, self.__setting_file_path)
        try:
            with open(path, mode='w', encoding='utf-8') as f:
                f.write(app_setting)
        except FileNotFoundError as e:
            LogError('\n'.join(e.args))

    def SaveColorThemeList(self, color_theme_list: Iterable[Dict]):
        """Save color theme

        :type color_theme_list: Iterable[Dict]
        """
        folder_path = abspath(join(__file__, '../', COLOR_THEME_FOLDER_PATH))
        if not exists(folder_path):
            mkdir(folder_path)

        for color_theme in color_theme_list:
            name = color_theme[NAME]
            contents = dumps(color_theme, ensure_ascii=False, indent=4, sort_keys=True, cls=IOManager.iSATexJsonEncoder)
            path = join(folder_path, name + '.json')
            try:
                with open(path, mode='w', encoding='utf-8') as f:
                    f.write(contents)
            except FileNotFoundError as e:
                LogError('\n'.join(e.args))

    def __ImportSetting(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                setting_dict = DotNotationDict(load(f, object_hook=self.AsStorableObject))
            return setting_dict
        except FileNotFoundError as e:
            if path == join(dirname(__file__), SETTING_FILE_PATH):
                return self.GetInitialSetting()
            LogError(e)
        except JSONDecodeError as e:
            LogError(e.msg)

    def __GetPluginPathList(self):
        path = abspath(join(__file__, '../', PLUGIN_FOLDER_PATH))
        if not exists(path):
            mkdir(path)

        return glob(f'{path}**/*.py', recursive=True)

    def __GetColorThemePathList(self):
        path = abspath(join(__file__, '../', COLOR_THEME_FOLDER_PATH))
        if not exists(path):
            mkdir(path)

        return glob(f'{path}**/*.json', recursive=True)

    def __ImportObjectList(self, module_path_list, BaseClass, ExcludeClass=None):
        ExcludeClass = tuple(ExcludeClass)

        def is_match(x):
            if isclass(x):
                return issubclass(x, BaseClass) and (ExcludeClass is None or x not in ExcludeClass)
            else:
                return isinstance(x, BaseClass)

        obj_list = []
        for module_path in module_path_list:
            abs_module_path = abspath(module_path)
            dir_name = dirname(abs_module_path)
            module_name = GetFileName(abs_module_path)
            if dir_name not in sys.path:
                sys.path.append(dir_name)
            try:
                module = import_module(module_name)
            except ModuleNotFoundError:
                LogError(f'"{module_name}" module was not found.\n Please check the "setting.json"')
                continue

            for _, value in getmembers(module):
                if is_match(value):
                    obj_list.append(value)

        return obj_list

    def OpenProject(self, path: str) -> Project:
        """Load an existing project.

        :param path: Path to an existing project
        :type path: str
        :rtype: Project
        """
        with open(path, mode='rb') as f:
            compressed_contents = f.read()

        contents = decompress(compressed_contents).decode(SAVE_ENCODING, 'replace')
        return loads(contents, object_hook=self.AsStorableObject)

    def SaveProject(self, project: Project):
        """Save the project.

        :type project: Project
        """
        if not isinstance(project, Project):
            raise TypeError()

        contents = dumps(project, separators=(',', ':'), allow_nan=False, cls=IOManager.iSATexJsonEncoder)
        compressed_contents = compress(contents.encode(SAVE_ENCODING, 'replace'))

        path = project.GetPath()

        with open(path, mode='wb') as f:
            f.write(compressed_contents)

    # def ImportPlugin(self, path):
    #     """[summary]

    #     :param path: [description]
    #     :type path: [type]
    #     """
    #     pass

    # def ExportPlugin(self, path):
    #     pass

    def SearchStorableObject(self, class_name: str) -> StorableObject:
        """Returns an instance of a storable object.

        :param class_name: Name of the storable class
        :type class_name: str
        :rtype: StorableObject
        """
        return deepcopy(self.GetSetting(STORABLE_OBJECT_DICT)[class_name])

    def AsStorableObject(self, dct: dict) -> StorableObject:
        """Convert json to storable object

        :param dct: Dictionary read from json
        :type dct: dict
        :rtype: StorableObject
        """
        if IOManager.SAVE_MARKER_CLASS_NAME not in dct or IOManager.SAVE_MARKER_DATA not in dct:
            return dct

        class_name = dct[IOManager.SAVE_MARKER_CLASS_NAME]
        save_data = dct[IOManager.SAVE_MARKER_DATA]
        obj = self.SearchStorableObject(class_name)
        obj.ReceiveSaveData(save_data)
        return obj

    class iSATexJsonEncoder(JSONEncoder):
        """Class for converting iSATex to json files
        """

        def default(self, obj):
            if obj == inf:
                return 'Infinity'

            elif obj == -inf:
                return '-Infinity'

            elif isinstance(obj, StorableObject):
                return self.GetSaveDataDict(obj)

            return super().default(obj)

        def GetSaveDataDict(self, obj):
            save_data_dict = {}
            save_data_dict[IOManager.SAVE_MARKER_CLASS_NAME] = obj.__class__.__name__
            save_data = obj.SendSaveData()
            if isinstance(save_data, (list, tuple)):
                data = []
                for element in save_data:
                    if isinstance(element, StorableObject):
                        element = self.GetSaveDataDict(element)

                    data.append(element)

            elif isinstance(save_data, dict):
                data = {}
                for key, value in save_data.items():
                    if isinstance(value, StorableObject):
                        value = self.GetSaveDataDict(value)

                    data[key] = value

            else:
                data = save_data

            save_data_dict[IOManager.SAVE_MARKER_DATA] = data
            return save_data_dict


class EventManager(Singleton):
    """Class for control Event
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__event_list = []

        self.__event_receptor_list = []

    def GetEventList(self) -> Iterable[iSATexEventBinder]:
        """Get a list of registered events.

        :rtype: Iterable[iSATexEventBinder]
        """
        return self.__event_list

    def RegisterEventList(self, event_list: Iterable[iSATexEventBinder]):
        """Register a list of events.

        :type event_list: Iterable[Event]
        """
        if not HasValidElement(event_list, iSATexEventBinder):
            raise TypeError()

        self.__event_list = event_list

    def GetEventReceptorList(self) -> Iterable[EventReceptorBase]:
        """Get a list of registered event receptors.

        :rtype: Iterable[EventReceptorBase]
        """
        return self.__event_receptor_list

    def RegisterEventReceptorList(self, event_receptor_list: Iterable[EventReceptorBase]):
        """Register the event receptor.

        :type event_receptor_list: Iterable[EventReceptorBase]
        """
        if not HasValidElement(event_receptor_list, EventReceptorBase):
            raise TypeError()

        self.__event_receptor_list.extend(event_receptor_list)

    def SendEvent(self, event):
        """
        This function sends an event to an instance of the "PanelBase" class and to the manager.
        Note that the event will not be sent until the project is started.

        :param event: Event object to be sent.
        :type event: Any type
        """
        logger.debug(f'Event of {event.__class__.__name__} is occur.')
        self.__core_mgr.OnEvent(event)
        for manager in self.__core_mgr.Get(MANAGER_LIST, []):
            if not hasattr(manager, 'OnEvent'):
                continue
            manager.OnEvent(event)

        self.SendEventToReceptor(event)

    def SendEventToReceptor(self, event: iSATexEvent):
        """Notifies the event receptor of the event.

        :type event: iSATexEvent
        """
        event.Skip()
        receptor_list = sorted(self.__event_receptor_list, key=lambda x: self.GetReceptionOrder(x))
        for receptor in receptor_list:
            receptor.OnEvent(event)

    def GetReceptionOrder(self, receptor: EventReceptorBase) -> int:
        """
        Defines the event fired order.
        Events are fired in ascending order and default order is following.

        0 Managers  :  -1
        1 MenuItems :  90
        2 Panels    : 100

        """
        if not isinstance(receptor, EventReceptorBase):
            raise TypeError()

        if isinstance(receptor, CustomMenuItemBase):
            return 90
        if isinstance(receptor, PanelBase):
            return 100

        return 50


class MenubarManager(Singleton):
    """
    This class is used to manage the menubar. This class can generate and change the design of the menu bar.
    Please refer to the function of "CreateMenu" documentation for details on how to change the design.
    Note: If you want to know more about how to change the design, please refer to the documentation of the function "CreateMenubar".
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__peak_type_menu_design = [PEAK_MENU]
        self.__show_panel_menu_design = [SHOW_PANEL_MENU]
        self.__layout_menu_design = [LAYOUT_MENU]
        self.__plugin_menu_design = [PLUGIN_MENU]

        self.__menu_item_dict = {EXIT_MENU_ITEM: MenuItem(id=ID_CLOSE, text=EXIT_MENU_ITEM, helpString='', kind=ITEM_NORMAL)}
        self.__menubar = None
        self.__menubar_design = None

    def ExecuteMenuFunction(self, key: str) -> Any:
        """Executes the function of the menu item with the specified key.

        :type key: str
        :rtype: Any
        """
        menuitem = self.GetMenuItem(key)
        if not isinstance(menuitem, CustomMenuItemBase):
            return

        return menuitem.Function()

    def __FindMenuItem(self, item_label):
        for menu, _ in self.__menubar.GetMenus():
            if (id_ := menu.FindItem(item_label)) == NOT_FOUND:
                continue

            return menu.FindItemById(id_)

    def GetMenuItem(self, key: str) -> CustomMenuItemBase:
        """Gets the menu item for the specified key. If it is not found, return None.

        :type key: str
        :rtype: CustomMenuItemBase
        """
        return self.__menu_item_dict.get(key) if key in self.__menu_item_dict else self.__FindMenuItem(key)

    def GetMenuItemList(self) -> List[CustomMenuItemBase]:
        """Get a list of managed menu items.

        :rtype: List[CustomMenuItemBase]
        """
        return list(self.__menu_item_dict.values())

    def GetPeakMenuItemList(self) -> Tuple[PeakMenuItem, ...]:
        """Get a list of managed peak menu items.

        :rtype: Tuple[PeakMenuItem, ...]
        """
        return tuple([menu_item for menu_item in self.__menu_item_dict.values() if isinstance(menu_item, PeakMenuItem)])

    def GetShowMenuItemList(self) -> Tuple[ShowPanelMenuItem, ...]:
        """Get a list of maneged show panel menu items.

        :rtype: Tuple[ShowPanelMenuItem, ...]
        """
        return tuple([menu_item for menu_item in self.__menu_item_dict.values() if isinstance(menu_item, ShowPanelMenuItem)])

    def GetPluginMenuItemList(self):
        """FURUTE WORK

        :return: [description]
        :rtype: [type]
        """
        default_menu_list = self.__GetDefaultMenuItemLabelList()
        return tuple([mi for mi in self.__menu_item_dict.values() if not (mi.GetItemLabel() in default_menu_list or isinstance(mi, (PeakMenuItem, LayoutMenuItem, ShowPanelMenuItem)))])

    def CheckMenuItem(self, key: str, check=True):
        """Checks the menu item for the specified key.

        :param key: Key to specify a menu item. If the menu item is not found or cannot be checked, it will be ignored.
        :type key: str
        :param check: Checks the menu item for the specified key. Defaults to True
        :type check: bool, optional
        """
        menu_item = self.__menu_item_dict.get(key)
        if menu_item is not None and menu_item.IsCheckable():
            menu_item.Check(check)

    def EnableMenuItem(self, key: str, enable=True):
        """Enables the menu item for the specified key.

        :type key: str
        :param enable: If true, the menu item will be enabled for selection; if false, it will be disabled., defaults to True
        :type enable: bool, optional
        """
        menu_item = self.__menu_item_dict.get(key)
        if menu_item is not None:
            menu_item.Enable(enable)

    def RegisterMenuItemList(self, menu_item_list: Iterable[CustomMenuItemBase]):
        """Register a list of menu items.

        :type menu_item_list: Iterable[CustomMenuItemBase]
        """
        if any([not isinstance(menu_item, CustomMenuItemBase) for menu_item in menu_item_list]):
            raise TypeError('Element of "menu_item_list" should be instance of "CustomMenuItemBase".')

        # default_menu_item_label_list = self.__GetDefaultMenuItemLabelList()

        for menu_item in menu_item_list:
            item_label = menu_item.GetItemLabel()
            # if isinstance(menu_item, PeakMenuItem):
            #     self.__peak_menu_item_set.add(menu_item)
            # elif isinstance(menu_item, ShowPanelMenuItem):
            #     self.__show_menu_item_set.add(menu_item)
            # else:
            #     if item_label not in default_menu_item_label_list:
            #         self.__plugin_menu_item_set.add(menu_item)

            self.__menu_item_dict[item_label] = menu_item

        plugin_menu_item = self.GetPluginMenuItemList()
        self.AppendPluginMenuItem(plugin_menu_item)

    def CreateMenubar(self, design: dict) -> MenuBar:
        """Create a menu bar from the design.

        :param design: Menubar design. Refer to "GetMenubarDesign"\'s documentation for details.
        :type design: dict
        :rtype: MenuBar
        """
        logger.debug(f'Create menubar from {design}')
        menubar = MenuBar()
        for element in design:
            menu, title = self.__CreateMenu(element)
            menubar.Append(menu, title)

        self.__menubar = menubar

        return menubar

    def __CreateMenu(self, design):
        title = design[0]
        menu_item_keys = design[1:]

        menu = Menu()
        for key in menu_item_keys:
            if isinstance(key, (list, tuple)):
                sub_menu, sub_title = self.__CreateMenu(key)
                menu.AppendSubMenu(sub_menu, sub_title)
                continue

            if key == SEPARATOR:
                menu.AppendSeparator()
                continue

            menu_item = self.__menu_item_dict.get(key, None)
            if menu_item is None:
                continue

            if isinstance(menu_item, ShowPanelMenuItem):
                panel = menu_item.GetPanel()
                shown = self.__io_mgr.GetSetting(DotChain(panel.__class__.__name__, SHOW), False)
                menu_item.Check(shown)

            # if isinstance(menu_item, PeakMenuItem):
            #     peak_type = self.__core_mgr.Get(DotChain(PEAK_TYPE, SELECTED))
            #     if peak_type.GetName() == menu_item.GetItemLabel():
            #         menu_item.Check(True)
            #     else:
            #         menu_item.Check(False)

            menu.Append(menu_item)
            menu_item.SetMenu(menu)

        return menu, title

    def GetMenubarDesign(self) -> dict:
        """Get menubar design. The design of the menu bar consists of a key of menu items.
        The list is designed as a collapsible menu, with the 0th title representing the first menu item and the rest representing the children menu items.

        :rtype: dict
        """
        return self.GetDefaultMenubarDesign() if self.__menubar_design is None else self.__menubar_design

    def GetDefaultMenubarDesign(self) -> dict:
        """Get default menubar design.
        :rtype: dict
        """
        return [
            [FILE_MENU,
                NEW_MENU_ITEM,
                OPEN_MENU_ITEM,
                SEPARATOR,
                SAVE_MENU_ITEM,
                SAVE_AS_MENU_ITEM,
                SEPARATOR,
                EXPORT_MENU_ITEM,
                SEPARATOR,
                # IMPORT_PLUGIN_MENU_ITEM,
                # EXPORT_PLUGIN_MENU_ITEM,
                # SEPARATOR,
                EXIT_MENU_ITEM
             ],
            [EDIT_MENU,
                [PROJECT_MENU,
                    self.__peak_type_menu_design,
                    PROJECT_MEMO_MENU_ITEM,
                 ],
                SEPARATOR,
                self.__plugin_menu_design,
                SEPARATOR,
                PREFERENCE_MENU_ITEM,
             ],
            [VIEW_MENU,
                self.__show_panel_menu_design,
                # SEPARATOR,
                # self.__layout_menu_design,
             ],
            [HELP_MENU,
                ABOUT_MENU_ITEM,
                TUTORIAL_MENU_ITEM,
             ]
        ]

    def __GetDefaultMenuItemLabelList(self):
        return (
            NEW_MENU_ITEM,
            OPEN_MENU_ITEM,
            SAVE_MENU_ITEM,
            SAVE_AS_MENU_ITEM,
            EXPORT_MENU_ITEM,
            IMPORT_PLUGIN_MENU_ITEM,
            EXPORT_PLUGIN_MENU_ITEM,
            EXIT_MENU_ITEM,
            PROJECT_MEMO_MENU_ITEM,
            PREFERENCE_MENU_ITEM,
            ABOUT_MENU_ITEM,
            TUTORIAL_MENU_ITEM,
        )

    def SetMenubarDesign(self, design: dict):
        """Set the menu bar design.

        :param design: Please refer to "GetMenubarDesign"\'s Documentation for details.
        :type design: dict
        """
        if not self.__IsMenubarDesign(design):
            raise TypeError()

        self.__menubar_design = design

    def __IsMenubarDesign(self, design):
        for element in design:
            if isinstance(element, (list, tuple)) and not self.__IsMenubarDesign(element):
                return False

            if not isinstance(element, (str, CustomMenuItemBase)):
                return False

        return True

    # def __CreatePeakMenuDesign(self):
    #     selected_peak_type_name = self.__core_mgr.Get(PEAK_MANAGER).GetSelectedPeakType().GetName()
    #     peak_type_list = self.__core_mgr.Get(PEAK_MANAGER).GetPeakTypeList()

    #     design = [PEAK_MENU]
    #     for peak_type in peak_type_list:
    #         menu_item = PeakMenuItem(peak_type)
    #         item_label = menu_item.GetItemLabel()
    #         if item_label == selected_peak_type_name:
    #             menu_item.Check(True)

    #         self.__menu_item_dict[item_label] = menu_item
    #         self.__peak_menu_item_set.add(menu_item)

    #         design.append(item_label)

    #     return design

    # def __CreateShowPanelMenuDesign(self):
    #     panel_list = self.__core_mgr.Get(PANEL_MANAGER).GetPanelList()
    #     spectrum_panel = self.__core_mgr.Get(PANEL_MANAGER).GetPanel(SPECTRUM_PANEL)

    #     design = [SHOW_PANEL_MENU]
    #     for panel in panel_list:
    #         if spectrum_panel == panel:
    #             continue

    #         menu_item = ShowPanelMenuItem(panel)
    #         item_label = menu_item.GetItemLabel()

    #         self.__menu_item_dict[item_label] = menu_item
    #         self.__show_menu_item_set.add(menu_item)

    #         design.append(item_label)

    #     return design

    # def __CreatePluginMenuDesign(self):
    #     design = [PLUGIN_MENU]
    #     design.extend([plugin_menu.GetItemLabel() for plugin_menu in self.__plugin_menu_item_set])
    #     return design

    def AppendPeakMenu(self, peak_type_list: Iterable[PeakType]):
        """Append a peak menu.

        :type peak_type_list: Iterable[PeakType]
        """
        if isinstance(peak_type_list, PeakType):
            peak_type_list = (peak_type_list,)

        menu = None
        if self.__menubar is not None:
            menu = self.GetMenuItem(PEAK_MENU)

        for peak_type in peak_type_list:
            menu_item = PeakMenuItem(peak_type)
            item_label = menu_item.GetItemLabel()
            self.__menu_item_dict[item_label] = menu_item
            self.__peak_type_menu_design.append(item_label)

            if menu is not None:
                menu.Append(menu_item)

    def AppendShowPanelMenu(self, panel_list: Iterable[PanelBase]):
        """Append a show panel menu.

        :type panel_list: Iterable[PanelBase]
        """
        if isinstance(panel_list, PanelBase):
            panel_list = (panel_list,)

        menu = None
        if self.__menubar is not None:
            menu = self.GetMenuItem(SHOW_PANEL_MENU)

        for panel in panel_list:
            menu_item = ShowPanelMenuItem(panel)
            item_label = menu_item.GetItemLabel()
            self.__menu_item_dict[item_label] = menu_item
            self.__show_panel_menu_design.append(item_label)

            if menu is not None:
                menu.Append(menu_item)

    def AppendLayoutMenu(self, name_list: Union[str, Iterable[str]]):
        """Append layout menu.

        :param name_list: a list of layout name.
        :type name_list: Union[str, Iterable[str]]
        """
        if isinstance(name_list, str):
            name_list = (name_list,)

        menu = None
        if self.__menubar is not None:
            menu = self.GetMenuItem(LAYOUT_MENU)

        for name in name_list:
            menu_item = LayoutMenuItem(name)
            item_label = menu_item.GetItemLabel()
            self.__menu_item_dict[item_label] = menu_item
            self.__layout_menu_design.append(item_label)

            if menu is not None:
                menu.Append(menu_item)

    def AppendPluginMenuItem(self, menu_item_list: Iterable[CustomMenuItemBase]):
        """Append plugin menu item.

        :type menu_item_list: Iterable[CustomMenuItem]
        """
        if isinstance(menu_item_list, CustomMenuItemBase):
            menu_item_list = (menu_item_list,)

        menu = None
        if self.__menubar is not None:
            menu = self.GetMenuItem(LAYOUT_MENU)

        for menu_item in menu_item_list:
            item_label = menu_item.GetItemLabel()
            self.__menu_item_dict[item_label] = menu_item
            self.__plugin_menu_design.append(item_label)

            if menu is not None:
                menu.Append(menu_item)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        if event.GetId() == ID_CLOSE:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_LAUNCH:
            PeakMenuItem._mgr = self.__core_mgr.Get(PEAK_MANAGER)
            ShowPanelMenuItem._mgr = self.__core_mgr.Get(PANEL_MANAGER)
            LayoutMenuItem._mgr = self.__core_mgr.Get(PANEL_MANAGER)

        elif event_type == wxEVT_LAYOUT_REGISTER:
            layout_names = event.GetLayoutNames()
            self.AppendLayoutMenu(layout_names)

        elif event_type == wxEVT_PEAK_TYPE_REGISTER:
            peak_type_list = event.GetNewPeakTypeList()
            self.AppendPeakMenu(peak_type_list)
            self.__core_mgr.Get(EVENT_MANAGER).RegisterEventReceptorList(self.GetPeakMenuItemList())

        elif event_type == wxEVT_PANEL_REGISTER:
            panel_list = event.GetNewPanelList()
            self.AppendShowPanelMenu(panel_list)

        elif event_type == wxEVT_COMMAND_MENU_SELECTED:

            menu_item = self.__menubar.FindItemById(event.GetId())
            if menu_item is None:
                return

            logger.debug(f'Menu event of {event.__class__.__name__} is occur.')
            menu_item.Function()

        # elif event_type == wxEVT_MENU_OPEN:
        #     selected_peak_name = self.__core_mgr.Get(PROJECTMANAGER)
        #     menu = event.GetMenu()
        #     for menu_item in menu.GetMenuItems():
        #         if menu_item.Get

        # elif event_type == wxEVT_PEAK_TYPE_REGISTER:
        #     peak_type = self.__core_mgr.Get(PROJECT_MANAGER).GetSelectedPeakType()
        #     print(peak_type)

        # elif event_type == wxEVT_PEAK_TYPE_CHANGE:
        #     peak_type = event.GetPeakType()
        #     self.CheckMenuItem(peak_type.GetName())


class PanelManager(Singleton, AuiManager):
    """Manager to register panels and layout.
    """

    def __init__(self, *args, **kw):
        """This class is responsible for referencing, registering, and selecting Panels and implemented with the Singleton pattern.
        """
        super().__init__(agwFlags=AUI_MGR_ALLOW_FLOATING | AUI_MGR_ALLOW_ACTIVE_PANE | AUI_MGR_TRANSPARENT_DRAG | AUI_MGR_LIVE_RESIZE)
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__selected_panel = None
        self.__layout_dict = {}
        self.__selected_layout = None

        self.__panel_dict = {}

    def GetPanel(self, key: str) -> PanelBase:
        """Get the panel specified by the key.

        :type key: str
        :rtype: PanelBase
        """
        if key == MAIN_WINDOW:
            return self.GetManagedWindow()

        return self.__panel_dict.get(key)

    def GetPanelList(self) -> Iterable[PanelBase]:
        """Get the list of registered panels.

        :rtype: Iterable[PanelBase]
        """
        return [pane_info.window for pane_info in self.GetAllPanes() if isinstance(pane_info.window, PanelBase)]

    def GetSelectedPanel(self) -> PanelBase:
        """Get the selected panel. Returns None if it is not selected.

        :rtype: PanelBase
        """
        return self.__selected_panel

    def SetMainWindow(self, window: Window):
        """Register the passed window as the main window.

        :type window: Window
        """
        self.SetManagedWindow(window)

    # def RegisterPanelList(self, PanelClassList, perspective, main_window):
    #     panel_info_dict = self.__ConvertPanelInfoDict(perspective)

    #     notebook_dict = {}
    #     for notebook_info in sorted(panel_info_dict['notebook_list'], key=lambda x: x['notebookid']):
    #         notebookid = notebook_info['notebookid']

    #         parent = notebook_dict.get(notebookid, main_window)
    #         notebook = AuiNotebook(parent, agwStyle=AUI_NB_BOTTOM)
    #         notebook_dict[notebookid] = notebook

    #         aui_info = AuiPaneInfo()
    #         aui_info.caption = notebook_info['caption']
    #         aui_info.SetFlag(notebook_info['state'], True)
    #         aui_info.Layer(notebook_info['layer'])
    #         aui_info.Direction(notebook_info['dir'])
    #         aui_info.Row(notebook_info['row'])
    #         aui_info.Position(notebook_info['pos'])
    #         aui_info.BestSize(notebook_info['bestw'], notebook_info['besth'])
    #         aui_info.MinSize(notebook_info['minw'], notebook_info['minh'])
    #         aui_info.MaxSize(notebook_info['maxw'], notebook_info['maxh'])
    #         aui_info.FloatingSize((notebook_info['floatw'], notebook_info['floath']))

    #         self.AddPane(notebook, aui_info)

    #     prev_panel_list = self.GetPanelList()
    #     for PanelClass in PanelClassList:
    #         if PanelClass.__name__ in self.__panel_dict:
    #             continue

    #         if (key := Camel2Pascal(PanelClass.__name__)) in panel_info_dict:
    #             panel_info = panel_info_dict[key]

    #             aui_info = AuiPaneInfo()
    #             aui_info.Caption(panel_info['caption'])
    #             aui_info.SetFlag(panel_info['state'], True)
    #             aui_info.Layer(panel_info['layer'])
    #             aui_info.Direction(panel_info['dir'])
    #             aui_info.Row(panel_info['row'])
    #             aui_info.Position(panel_info['pos'])
    #             aui_info.BestSize(panel_info['bestw'], panel_info['besth'])
    #             aui_info.MinSize(panel_info['minw'], panel_info['minh'])
    #             aui_info.MaxSize(panel_info['maxw'], panel_info['maxh'])
    #             aui_info.FloatingSize((panel_info['floatw'], panel_info['floath']))

    #             aui_info.MaximizeButton().PinButton().CloseButton().NotebookDockable(False)

    #             if (key := panel_info['notebookid']) in notebook_dict:
    #                 notebook = notebook_dict[key]
    #                 panel = PanelClass(parent=notebook)
    #                 notebook.AddPage(panel, panel_info['caption'])
    #             else:
    #                 panel = PanelClass(parent=main_window)
    #         else:
    #             panel = PanelClass(parent=main_window)
    #             aui_info = self.__CreateAuiPaneInfo(panel)

    #         if isinstance(panel, SpectrumPanel):
    #             aui_info = aui_info.CenterPane()

    #         self.AddPane(panel, aui_info)

    #     self.Update()
    #     for panel in self.GetPanelList():
    #         self.__panel_dict[panel.__class__.__name__] = panel

    #     panel_list = self.GetPanelList()
    #     event = PanelRegisterEvent(panel_list, prev_panel_list, id=self.__id)
    #     self.__core_mgr.SendEvent(event)

    #     return panel_list

    def RegisterPanelList(self, panel_list: Iterable[PanelBase], layout: Optional[str] = None):
        """Register a list of panels. The panels will be placed in the passed layout.

        :type panel_list: Iterable[PanelBase]
        :type layout: Optional[str], optional
        """
        if layout is None:
            layout = {}

        self.__selected_layout, value = layout

        panel_info_dict = self.__ConvertPanelInfoDict(value)
        prev_panel_list = self.GetPanelList()
        for panel in panel_list:
            if panel.__class__.__name__ in self.__panel_dict:
                continue

            if (key := Camel2Pascal(panel.__class__.__name__)) in panel_info_dict:
                panel_info = panel_info_dict[key]

                aui_info = AuiPaneInfo()
                aui_info.Caption(panel_info['caption'])
                aui_info.SetFlag(panel_info['state'], True)
                aui_info.Layer(panel_info['layer'])
                aui_info.Direction(panel_info['dir'])
                aui_info.Row(panel_info['row'])
                aui_info.Position(panel_info['pos'])
                aui_info.BestSize(panel_info['bestw'], panel_info['besth'])
                aui_info.MinSize(panel_info['minw'], panel_info['minh'])
                aui_info.MaxSize(panel_info['maxw'], panel_info['maxh'])
                aui_info.FloatingSize((panel_info['floatw'], panel_info['floath']))

                aui_info.MaximizeButton().PinButton().CloseButton().NotebookDockable(False)

            else:
                aui_info = self.__CreateAuiPaneInfo(panel)

            if isinstance(panel, SpectrumPanel):
                aui_info = aui_info.CenterPane()

            self.AddPane(panel, aui_info)

        self.Update()
        for panel in self.GetPanelList():
            self.__panel_dict[panel.__class__.__name__] = panel

        panel_list = self.GetPanelList()
        event = PanelRegisterEvent(panel_list, prev_panel_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def __CreateAuiPaneInfo(self, panel) -> AuiPaneInfo:
        name = Camel2Pascal(panel.__class__.__name__)
        aui_info = AuiPaneInfo().MaximizeButton().PinButton().CloseButton().NotebookDockable(False).Hide().Caption(name)

        is_shown = self.__core_mgr.Get(f'{panel.__class__.__name__}.{SHOW}', True)
        if not is_shown:
            aui_info = aui_info.Hide()

        return aui_info

    def __ConvertPanelInfoDict(self, perspective):
        panel_info_dict = {'notebook_list': []}
        for panel_perspective in perspective.split('|')[1:]:
            panel_info = {}
            for item in panel_perspective.split(';'):
                if item == '':
                    continue

                key, value = item.split('=')
                try:
                    value = int(value)
                except ValueError:
                    pass
                panel_info[key] = value

            if len(panel_info) > 1:
                if '__notebook_' in panel_info['name'] or 'AuiNotebook' in panel_info['name']:
                    panel_info_dict['notebook_list'].append(panel_info)
                else:
                    panel_info_dict[panel_info['caption']] = panel_info
            else:
                panel_info_dict.update(panel_info)

        return panel_info_dict

    def GetSelectedLayout(self):
        """Get selected layout

        :rtype: str
        """
        return (self.__selected_layout, deepcopy(self.__layout_dict[self.__selected_layout]))

    def GetLayoutNames(self) -> Tuple[str, ...]:
        """Get a list of names of registered layouts.

        :rtype: Tuple[str, ...]
        """
        return tuple(self.__layout_dict)

    def GetLayoutList(self) -> Tuple[str, ...]:
        """Get the list of registered layouts.

        :rtype: Tuple[str, ...]
        """
        return tuple([(key, value) for key, value in self.__layout_dict.items()])

    def LoadLayout(self, name: str):
        """Places it in the layout with the specified name.

        :type name: str
        """
        perspective = self.__layout_dict.get(name, '')
        panel_info_dict = self.__ConvertPanelInfoDict(perspective)

        panel_list = self.GetPanelList()

        for pane in self.GetAllPanes():
            self.DetachPane(pane)

        # for panel in panel_list:
        #     panel_info = panel_info_dict.get(panel.__class__.__name__)

        #     if panel_info is None:
        #         continue

        #     aui_info = AuiPaneInfo()
        #     aui_info.Caption(panel_info['caption'])
        #     aui_info.SetFlag(panel_info['state'], True)
        #     aui_info.Layer(panel_info['layer'])
        #     aui_info.Direction(panel_info['dir'])
        #     aui_info.Row(panel_info['row'])
        #     aui_info.Position(panel_info['pos'])
        #     aui_info.BestSize(panel_info['bestw'], panel_info['besth'])
        #     aui_info.MinSize(panel_info['minw'], panel_info['minh'])
        #     aui_info.MaxSize(panel_info['maxw'], panel_info['maxh'])
        #     aui_info.FloatingSize((panel_info['floatw'], panel_info['floath']))

        #     aui_info.MaximizeButton().PinButton().CloseButton().NotebookDockable(False)

        #     self.AddPane(panel, panel_info)

        # self.DoFrameLayout()
        # self.Repaint()
        self.Update()

        prev_layout = self.__selected_layout
        self.__selected_layout = name
        event = LayoutChangeEvent(self.__selected_layout, prev_layout, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def RegisterCurrentLayout(self, name: str):
        """Register the current layout.

        :param name: layout name
        :type name: str
        """
        prev_layout_list = self.GetLayoutList()

        value = self.SavePerspective()
        self.__layout_dict[name] = value

        layout_list = self.GetLayoutList()

        event = LayoutRegisterEvent(layout_list, prev_layout_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def RegisterLayout(self, layout: Tuple[str, str], operand: str = None):
        """Register the layout.

        :param layout: Tuples of names and perspectives. Please Refer to wxPython (https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html#wx.lib.agw.aui.framemanager.AuiManager.SavePerspective) for detail of Perspective.
        :type layout: Tuple[str, str]
        :param operand: [description], defaults to None
        :type operand: str, optional
        """
        if isinstance(layout[0], str):
            layout = (layout,)

        layout_dict = {}
        for name, value in layout:
            layout_dict[name] = value

        prev_layout_list = self.GetLayoutList()
        if operand is None:
            self.__layout_dict = layout_dict
        elif operand == '|':
            self.__layout_dict.update(layout_dict)
        elif operand == '-':
            for key in layout_dict:
                del self.__layout_dict[key]

        layout_list = self.GetLayoutList()

        event = LayoutRegisterEvent(layout_list, prev_layout_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def __SendPanelSelectionChangeEvent(self, panel):
        if panel == self.__selected_panel:
            return

        event = PanelSelectionChangeEvent(panel, self.__selected_panel, self.__id)
        self.__selected_panel = panel
        self.__core_mgr.Get(EVENT_MANAGER).SendEvent(event)

    def OnGripperClicked(self, pane_window, start, offset):
        """Called when a panel is clicked and notify the "PanelSelectionChangeEvent". Please refer to wxPython (https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html#wx.lib.agw.aui.framemanager.AuiManager.OnGripperClicked) for details.
        """
        panel = FindWindowToAncestors(pane_window, PanelBase)
        self.__SendPanelSelectionChangeEvent(panel)

        return super().OnGripperClicked(pane_window, start, offset)

    # def OnChildFocus(self, event):
    #     event.Skip()
    #     panel = FindWindowToAncestors(event.Window, PanelBase)
    #     self.__SendPanelSelectionChangeEvent(panel)
    #     return super().OnChildFocus(event)

    def __SendPanelHideEvent(self, panel_list):
        menubar_mgr = self.__core_mgr.Get(MENUBAR_MANAGER)
        for panel in panel_list:
            menubar_mgr.CheckMenuItem(GetShowPanelLabel(panel), False)

        event = PanelViewEvent(hide_panel_list=panel_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def OnFloatingPaneClosed(self, wnd, event):
        """Called when a floating panel is closed and notify the "PanelViewEvent" Please refer to wxPython (https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html#wx.lib.agw.aui.framemanager.AuiManager.OnFloatingPaneClosed) for details.
        """
        event.Skip()
        self.__SendPanelHideEvent([wnd])
        return super().OnFloatingPaneClosed(wnd, event)

    def OnPaneButton(self, event):
        """Called when button on tho top of panel is pushed and notify the "PanelViewEvent"  Please refer to wxPython (https://docs.wxpython.org/wx.lib.agw.aui.framemanager.AuiManager.html#wx.lib.agw.aui.framemanager.AuiManager.OnFloatingPaneClosed) for details.

        :param event: [description]
        :type event: [type]
        :return: [description]
        :rtype: [type]
        """
        if event.GetButton() == AUI_BUTTON_CLOSE:
            self.__SendPanelHideEvent([event.GetPane().window])
        return super().OnPaneButton(event)

    # def LoadLayout(self, layout):
    #     pass

    # def SaveLayout(self):
    #     layout = {
    #         'notebooklist': []
    #     }
    #     queue = deque()
    #     notebook_idx = -1
    #     for dock in self._docks:
    #         for pane in dock.panes:
    #             queue.append((pane, notebook_idx))

    #     while len(queue) != 0:
    #         pane, idx = queue.popleft()
    #         window = pane.window

    #         if isinstance(window, AuiNotebook):
    #             for pane in [window.GetPage(i) for i in range(window.GetPageCount())]:
    #                 queue.append((pane, notebook_idx))

    #             notebook_idx += 1
    #             layout['notebooklist'].append(idx)

    #         layout[window.__class__.__name__] = {
    #             'notebook_idx': notebook_idx,
    #             'info': self.SavePaneInfo(pane)
    #         }

    #     print(layout)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_PANEL_SELECTION_CHANGE:
            self.__selected_panel = event.GetPanel()

        elif event_type == wxEVT_PANEL_VIEW:
            menubar_mgr = self.__core_mgr.Get(MENUBAR_MANAGER)
            for panel in event.GetShowPanelList():
                self.ShowPane(panel)
                menubar_mgr.CheckMenuItem(GetShowPanelLabel(panel), True)

            for panel in event.GetHidePanelList():
                self.HidePane(panel)
                menubar_mgr.CheckMenuItem(GetShowPanelLabel(panel), False)

        elif event_type == wxEVT_PANEL_REGISTER:
            panel_list = event.GetPanelList()
            if len(panel_list) == 0:
                return

            for panel in panel_list:
                aui_info = self.__CreateAuiPaneInfo(panel)
                if isinstance(panel, SpectrumPanel):
                    aui_info = aui_info.CenterPane()

                self.AddPane(panel, aui_info)

            self.Update()
            self.__panel_dict = {panel.__class__.__name__: panel for panel in self.GetPanelList()}

        elif event_type == wxEVT_EXIT:
            # notebook_count = 0
            for panel in self.GetPanelList():
                self.__io_mgr.SetSetting(DotChain(panel.__class__.__name__, SHOW), panel.Shown)

            self.__io_mgr.SetSetting(SELECTED_LAYOUT, (self.__selected_layout, self.SavePerspective()))


class FunctionManager(Singleton):
    """Manager for function and preset
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__function_dict = {}

        self.__selected_spectrum_func_list = []
        self.__selected_encode_func = None
        self.__selected_decode_func = None
        self.__selected_mapping_func = None

        self.__preset_dict = {}

    def GetFunction(self, name: str) -> FunctionContainerBase:
        """Get the function specified by name. This value is deepcopied.

        :param name: Class name of function.
        :type name: str
        :rtype: FunctionContainerBase
        """
        return deepcopy(self.__function_dict.get(name))

    def GetFunctionList(self) -> List[FunctionContainerBase]:
        """Get a list of registered functions. This value is deepcopied.

        :rtype: List[FunctionContainerBase]
        """
        return deepcopy(self.__GetFunctionList())

    def GetPeakFunctionList(self) -> List[PeakFunctionContainerBase]:
        """Get a list of registered peak functions. This value is deepcopied.

        :rtype: List[PeakFunctionContainerBase]
        """
        return deepcopy(self.__GetPeakFunctionList())

    def GetDecodeFunctionList(self) -> List[DecodeFunctionContainerBase]:
        """Get a list of registered decode functions. This value is deepcopied.

        :rtype: List[DecodeFunctionContainerBase]
        """
        return deepcopy(self.__GetDecodeFunctionList())

    def GetEncodeFunctionList(self) -> List[EncodeFunctionContainerBase]:
        """Get a list of registered encode functions. This value is deepcopied.

        :rtype: List[EncodeFunctionContainerBase]
        """
        return deepcopy(self.__GetEncodeFunctionList())

    def GetSpectrumFunctionList(self) -> List[SpectrumFunctionContainerBase]:
        """Get a list of registered spectrum functions. This value is deepcopied.

        :rtype: List[SpectrumFunctionContainerBase]
        """
        return deepcopy(self.__GetSpectrumFunctionList())

    def GetMappingFunctionList(self) -> List[MappingFunctionContainerBase]:
        """Get a list of registered mapping functions. This value is deepcopied.

        :rtype: List[MappingFunctionContainerBase]
        """
        return deepcopy(self.__GetMappingFunctionList())

    def __GetFunctionList(self):
        return list(self.__function_dict.values())

    def __GetPeakFunctionList(self):
        return [func for func in self.__GetFunctionList() if isinstance(func, PeakFunctionContainerBase)]

    def __GetDecodeFunctionList(self):
        return [func for func in self.__GetFunctionList() if isinstance(func, DecodeFunctionContainerBase)]

    def __GetEncodeFunctionList(self):
        return [func for func in self.__GetFunctionList() if isinstance(func, EncodeFunctionContainerBase)]

    def __GetSpectrumFunctionList(self):
        return [func for func in self.__GetFunctionList() if isinstance(func, SpectrumFunctionContainerBase)]

    def __GetMappingFunctionList(self):
        return [func for func in self.__GetFunctionList() if isinstance(func, MappingFunctionContainerBase)]

    def GetSelectedDecodeFunction(self) -> DecodeFunctionContainerBase:
        """Get the selected decode function. This value is deepcopied.

        :rtype: DecodeFunctionContainerBase
        """
        return deepcopy(self.__selected_decode_func)

    def GetSelectedEncodeFunction(self) -> EncodeFunctionContainerBase:
        """Get the selected encode function. This value is deepcopied.

        :rtype: EncodeFunctionContainerBase
        """
        return deepcopy(self.__selected_encode_func)

    def GetSelectedSpectrumFunctionList(self) -> SpectrumFunctionContainerBase:
        """Get the selected spectrum function. This value is deepcopied.

        :rtype: SpectrumFunctionContainerBase
        """
        return deepcopy(self.__selected_spectrum_func_list)

    def GetSelectedMappingFunction(self) -> MappingFunctionContainerBase:
        """Get the selected mapping function. This value is deepcopied.

        :rtype: MappingFunctionContainerBase
        """
        return deepcopy(self.__selected_mapping_func)

    def RegisterFunctionList(self, function_list: FunctionContainerBase, is_register=True):
        """Register or deregister a list of functions.

        :type function_list: FunctionContainerBase
        :param is_register: If True, register, if False, deregister., defaults to True
        :type is_register: bool, optional
        """
        if not hasattr(function_list, '__iter__'):
            function_list = [function_list]

        if any([not isinstance(function, FunctionContainerBase) for function in function_list]):
            raise TypeError()

        self.__RegisterFunctionList(function_list, is_register)

    def __Set2FunctionDict(self, function_list, is_register):
        for function in function_list:
            if (key := function.__class__.__name__) in self.__function_dict:
                continue
            if is_register:
                self.__function_dict[key] = function
            else:
                del self.__function_dict[key]

    def __RegisterFunctionList(self, function_list, is_register):
        prev_peak_func_list = self.__GetPeakFunctionList()
        prev_encode_func_list = self.__GetEncodeFunctionList()
        prev_decode_func_list = self.__GetDecodeFunctionList()
        prev_spectrum_func_list = self.__GetSpectrumFunctionList()
        prev_mapping_func_list = self.__GetMappingFunctionList()

        self.__Set2FunctionDict(function_list, is_register)

        peak_func_list = self.__GetPeakFunctionList()
        encode_func_list = self.__GetEncodeFunctionList()
        decode_func_list = self.__GetDecodeFunctionList()
        spectrum_func_list = self.__GetSpectrumFunctionList()
        mapping_func_list = self.__GetMappingFunctionList()

        event_design = [
            (PeakFunctionRegisterEvent, PeakFunctionDeregisterEvent, peak_func_list, prev_peak_func_list),
            (EncodeFunctionRegisterEvent, EncodeFunctionDeregisterEvent, encode_func_list, prev_encode_func_list),
            (DecodeFunctionRegisterEvent, DecodeFunctionDeregisterEvent, decode_func_list, prev_decode_func_list),
            (SpectrumFunctionRegisterEvent, SpectrumFunctionDeregisterEvent, spectrum_func_list, prev_spectrum_func_list),
            (MappingFunctionRegisterEvent, MappingFunctionDeregisterEvent, mapping_func_list, prev_mapping_func_list),
        ]

        for RegisterEvent, DeregisterEvent, value, prev_value in event_design:
            Event = RegisterEvent if is_register else DeregisterEvent
            event = Event(value, prev_value, id=self.__id)
            self.__core_mgr.SendEvent(event)

    def SelectEncodeFunction(self, function: EncodeFunctionContainerBase):
        """Select the encode function.

        :type function: EncodeFunctionContainerBase
        """
        if not(function is None or isinstance(function, EncodeFunctionContainerBase)):
            raise TypeError()

        prev_function = self.__selected_encode_func
        self.__selected_encode_func = function
        event = EncodeFunctionSelectEvent(function, prev_function, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def SelectDecodeFunction(self, function: DecodeFunctionContainerBase):
        """Select the decode function.

        :type function: DecodeFunctionContainerBase
        """
        if not (function is None or isinstance(function, DecodeFunctionContainerBase)):
            raise TypeError()

        prev_function = self.__selected_decode_func
        self.__selected_decode_func = function
        event = DecodeFunctionSelectEvent(function, prev_function, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def SelectSpectrumFunctionList(self, function_list: Iterable[SpectrumFunctionContainerBase]):
        """Select the list of spectrum functions.

        :type function_list: Iterable[SpectrumFunctionContainerBase]
        """
        func_list = self.__FormatFunctionList(function_list)
        if any([not isinstance(func, SpectrumFunctionContainerBase) for func in func_list]):
            raise TypeError()

        prev_func_list = self.__selected_spectrum_func_list
        self.__selected_spectrum_func_list = func_list
        event = SpectrumFunctionListSelectEvent(func_list, prev_func_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def SelectMappingFunction(self, function: MappingFunctionContainerBase):
        """Select the decode function.

        :type function: MappingFunctionContainerBase
        """
        if not (function is None or isinstance(function, MappingFunctionContainerBase)):
            raise TypeError()

        prev_function = self.__selected_mapping_func
        self.__selected_mapping_func = function
        event = MappingFunctionSelectEvent(function, prev_function, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def __FormatFunctionList(self, function_list):
        if isinstance(function_list, str):
            function_list = [self.GetFunction(function_list)]

        elif isinstance(function_list, (list, tuple)):
            if all([isinstance(function, FunctionContainerBase) for function in function_list]):
                function_list = function_list
            elif all([isinstance(function, str) for function in function_list]):
                function_list = [self.GetFunction(element) for element in function_list]
            else:
                raise TypeError()

        elif isinstance(function_list, FunctionContainerBase):
            function_list = [function_list]
        else:
            raise TypeError()

        return function_list

    def GetPreset(self, name: str) -> Preset:
        """Get a preset with the specified name. This value is deepcopied.

        :type name: str
        :rtype: Preset
        """
        return deepcopy(self.__preset_dict.get(name))

    def GetPresetNames(self) -> Tuple[str]:
        """Get a list of names of registered presets.

        :rtype: Tuple[str]
        """
        return tuple(self.__preset_dict.keys())

    def GetPresetList(self) -> List[Preset]:
        """Get a list of registered presets. This value is deepcopied.

        :rtype: List[Preset]
        """
        return deepcopy(self.__GetPresetList())

    def __GetPresetList(self):
        return list(self.__preset_dict.values())

    def SelectSpectrumPreset(self, preset: Union[str, Preset]):
        """Select the registered Spectrum Preset.

        :param preset: preset name or instance of Preset
        :type preset: Union[str, Preset]
        """
        preset_list = self.__FormatPresetList(preset)
        func_list = []
        for preset in preset_list:
            func_list.extend([func for func in preset])

        self.SelectSpectrumFunctionList(func_list)

    def RegisterPreset(self, preset: Preset, is_register=True):
        """Register the presets.

        :type preset: Preset
        :param is_register: If True, register, if False, deregister., defaults to True
        :type is_register: bool, optional
        """
        prev_preset_list = self.__GetPresetList()
        for preset in self.__FormatPresetList(preset):
            if is_register:
                self.__preset_dict[preset.GetName()] = preset
            else:
                del self.__preset_dict[preset.GetName()]
        preset_list = self.__GetPresetList()

        Event = PresetRegisterEvent if is_register else PresetDeregisterEvent
        event = Event(preset_list, prev_preset_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def __FormatPresetList(self, preset_list):
        if isinstance(preset_list, str):
            preset_list = [self.GetPreset(preset_list)]

        elif isinstance(preset_list, (list, tuple)):
            if all([isinstance(preset, Preset) for preset in preset_list]):
                preset_list = preset_list
            elif all([isinstance(preset, str) for preset in preset_list]):
                preset_list = [self.GetPreset(preset) for preset in preset_list]
            else:
                TypeError()
        elif isinstance(preset_list, Preset):
            preset_list = [deepcopy(preset_list)]
        else:
            TypeError()

        return preset_list

    def IsRegisteredPresetName(self, name: str) -> bool:
        """Returns True if the specified name has been registered.

        :param name: name of preset
        :type name: str
        :rtype: bool
        """
        return name in self.__preset_dict

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_ENCODE_FUNCTION_SELECT:
            self.__selected_encode_func = event.GetFunction()

        elif event_type == wxEVT_DECODE_FUNCTION_SELECT:
            self.__selected_decode_func = event.GetFunction()

        elif event_type == wxEVT_SPECTRUM_FUNCTION_LIST_SELECT:
            self.__selected_spectrum_func_list = event.GetFunctionList()

        elif event_type in [wxEVT_ENCODE_FUNCTION_REGISTER, wxEVT_DECODE_FUNCTION_REGISTER, wxEVT_SPECTRUM_FUNCTION_REGISTER, wxEVT_PEAK_FUNCTION_REGISTER, wxEVT_MAPPING_FUNCTION_REGISTER]:
            function_list = event.GetFunctionList()
            self.__Set2FunctionDict(function_list, True)

        elif event_type in [wxEVT_ENCODE_FUNCTION_DEREGISTER, wxEVT_DECODE_FUNCTION_DEREGISTER, wxEVT_SPECTRUM_FUNCTION_DEREGISTER, wxEVT_PEAK_FUNCTION_DEREGISTER, wxEVT_MAPPING_FUNCTION_DEREGISTER]:
            function_list = event.GetFunctionList()
            self.__Set2FunctionDict(function_list, False)

        elif event_type == wxEVT_PRESET_REGISTER:
            preset_list = event.GetPresetList()
            for preset in preset_list:
                self.__preset_dict[preset.GetName()] = preset

        elif event_type == wxEVT_PRESET_DEREGISTER:
            preset_list = event.GetPresetList()
            for preset in preset_list:
                del self.__preset_dict[preset.GetName()]

        elif event_type == wxEVT_EXIT:
            design = (
                (SELECTED_ENCODE_FUNCTION, self.__selected_encode_func),
                (SELECTED_DECODE_FUNCTION, self.__selected_decode_func),
                (SPECTRUM_FUNCTION_PRESET_LIST, self.__GetPresetList()),
                (SELECTED_MAPPING_FUNCTION, self.__selected_mapping_func),
            )

            for key, value in design:
                self.__io_mgr.SetSetting(key, value)


class ProjectManager(Singleton):
    """Manager for project
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__is_saved = None

        self.__project = Project()

    def GetProject(self) -> Project:
        """Get project

        :rtype: Project
        """
        return self.__project

    def NewProject(self, data_list: Iterable[DataContainer]):
        """Create a new project.

        :type data_list: Iterable[DataContainer]
        """
        if not HasValidElement(data_list, DataContainer):
            raise TypeError()

        peak_type = self.__core_mgr.Get(PEAK_MANAGER).GetSelectedPeakType()

        self.__project = Project()
        self.__project.SetDataList(data_list)
        self.__project.SetPeakType(peak_type)
        self.__SetIsProjectSaved(False)

        event = ProjectNewEvent(data_list, peak_type, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def OpenProject(self, path: str):
        """Load an existing project.

        :type path: str
        """
        if self.IsProjectStarted() and not self.IsProjectSaved():
            with MessageDialog(None, 'Project changes will not be saved.', style=OK | CANCEL | ICON_INFORMATION | CENTRE) as dialog:
                if dialog.ShowModal() == ID_CANCEL:
                    return

        project = self.__io_mgr.OpenProject(path)
        self.__project = project

        self.__SetIsProjectSaved(True)

        path = project.GetPath()
        note = project.GetNote()
        peak_type = project.GetPeakType()
        data_list = project.GetDataList()
        experimental_date = project.GetExperimentalDate()

        event = ProjectOpenEvent(data_list, path, peak_type, note, experimental_date, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def SaveProject(self, project: Project = None) -> bool:
        """Save the project.

        :param project: If project is None, Save the managed by this class. Defaults to None
        :type project: Project, optional
        """
        if not self.IsProjectStarted() or self.IsProjectSaved():
            return

        if project is None:
            project = self.GetProject()

        if not isinstance(project, Project):
            raise TypeError()

        path = project.GetPath()
        data_list = project.GetDataList()
        note = project.GetNote()
        peak_type = project.GetPeakType()
        experimental_date = project.GetExperimentalDate()
        self.__project = deepcopy(project)

        event = ProjectSaveEvent(path, data_list, peak_type, note, experimental_date, id=self.__id)
        self.__core_mgr.SendEvent(event)

        self.__io_mgr.SaveProject(self.__project)
        self.__SetIsProjectSaved(True)

    def SetProjectMemo(self, experimental_date: date, note: str):
        """Set the memo for the project.

        :param experimental_date: Date of Experiment
        :type experimental_date: date
        :param note: Notes on the project
        :type note: str
        """
        prev_date = self.__project.GetExperimentalDate()
        prev_note = self.__project.GetNote()
        self.__project.SetExperimentalDate(experimental_date)
        self.__project.SetNote(note)

        self.__SetIsProjectSaved(False)

        event = ProjectMemoChangeEvent(experimental_date, prev_date, note, prev_note)
        self.__core_mgr.SendEvent(event)

    def IsProjectStarted(self) -> bool:
        """Returns True if the project has been started

        :rtype: bool
        """
        return len(self.__project.GetDataList()) != 0

    def IsProjectSaved(self) -> bool:
        """Returns True if the project has saved the most recent state.

        :rtype: bool
        """
        return self.__is_saved

    def AskProjectSaving(self) -> bool:
        """Ask if the project needs to be saved.

        :return: Whether the operation is complete or not.
        :rtype: bool
        """
        if self.IsProjectStarted() and not self.IsProjectSaved():
            with SaveCheckDialog(None, title='Info') as dialog:
                dialog.Center()
                id_ = dialog.ShowModal()

            if id_ == ID_CANCEL:
                return False

            elif id_ == ID_SAVE:
                is_saved = self.__core_mgr.Get(MENUBAR_MANAGER).ExecuteMenuFunction(SAVE_MENU_ITEM)

                if not is_saved:
                    return False

                self.SaveProject()

        return True

    def GetDefaultProjectPath(self) -> str:
        """Returns the default project name.

        :rtype: str
        """
        return join(getcwd(), NEW_PROJECT_NAME)

    def __SetIsProjectSaved(self, is_saved):
        self.__is_saved = is_saved
        name = self.__project.GetFileName()
        self.__core_mgr.SetTitle(name)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_PROJECT_NEW:
            data_list = event.GetDataList()
            self.__project.SetDataList(data_list)

            peak_type = event.GetPeakType()
            self.__project.SetPeakType(peak_type)

            self.__SetIsProjectSaved(False)

        elif event_type == wxEVT_PROJECT_OPEN:
            data_list = event.GetDataList()
            self.__project.SetDataList(data_list)

            note = event.GetNote()
            self.__project.SetNote(note)

            peak_type = event.GetPeakType()
            self.__project.SetPeakType(peak_type)

            self.__SetIsProjectSaved(True)

        elif event_type == wxEVT_PROJECT_SAVE:
            data_list = event.GetDataList()
            self.__project.SetDataList(data_list)

            note = event.GetNote()
            self.__project.SetNote(note)

            peak_type = event.GetPeakType()
            self.__project.SetPeakType(peak_type)

            # Eventがパネルに飛ぶ通達される前に実行されちゃう
            self.__io_mgr.SaveProject(self.__project)
            self.__SetIsProjectSaved(True)

        elif event_type == wxEVT_PROJECT_MEMO_CHANGE:
            date = event.GetExperimentalData()
            note = event.GetNote()
            self.__project.SetExperimentalDate(date)
            self.__project.SetNote(note)

            self.__SetIsProjectSaved(False)

        elif event_type == wxEVT_DATA_CONTENTS_CHANGE:
            self.__SetIsProjectSaved(False)


class PeakManager(Singleton):
    """Manager related to peak.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__peak_type_dict = {}

    def GetPeakType(self, name: str) -> PeakType:
        """Get the peak type specified by name. This value is deepcopied.

        :param name: class name of peak type.
        :type name: str
        :rtype: PeakType
        """
        return deepcopy(self.__peak_type_dict.get(name))

    def SelectPeakType(self, peak_type: PeakType):
        """Select Peak Type

        :type peak_type: PeakType
        """
        if peak_type is None:
            print('select peak_type is None')
            return

        if isinstance(peak_type, str):
            peak_type = self.GetPeakType(peak_type)

        if not isinstance(peak_type, PeakType):
            raise TypeError()

        prev_peak_type = self.__GetProject().GetPeakType()

        self.__GetProject().SetPeakType(peak_type)
        self.__core_mgr.Get(MENUBAR_MANAGER).CheckMenuItem(peak_type.GetName())

        event = PeakTypeChangeEvent(peak_type, prev_peak_type, self.__id)

        for spectrum_func_instance in SpectrumFunctionContainerBase._instance_list:
            spectrum_func_instance.OnPeakTypeChanged(event)

        self.__core_mgr.SendEvent(event)

    def GetSelectedPeakType(self) -> PeakType:
        """Get selected type of peak.

        :rtype: PeakType
        """
        return self.__GetProject().GetPeakType()

    def RegisterPeakTypeList(self, peak_type_list: Union[PeakType, Iterable[PeakType]]):
        """Register the peak type.

        :type peak_type_list: Union[PeakType, Iterable[PeakType]]
        """
        if not hasattr(peak_type_list, '__iter__'):
            peak_type_list = [peak_type_list]

        if any(not isinstance(peak_type, PeakType) for peak_type in peak_type_list):
            raise TypeError()

        prev_peak_type_list = list(self.__peak_type_dict.values())

        for peak_type in peak_type_list:
            if (peak_name := peak_type.GetName()) not in self.__peak_type_dict:
                self.__peak_type_dict[peak_name] = peak_type

        peak_type_list = list(self.__peak_type_dict.values())

        event = PeakTypeRegisterEvent(peak_type_list, prev_peak_type_list, self.__id)
        self.__core_mgr.SendEvent(event)

    def GetPeakTypeNames(self) -> Tuple[str, ...]:
        """Get a list of registered peak type names.

        :rtype: Tuple[str, ...]
        """
        return tuple(self.__peak_type_dict.keys())

    def GetPeakTypeList(self) -> Tuple[PeakType, ...]:
        """Get a list of registered peak types.

        :rtype: Tuple[PeakType, ...]
        """
        return tuple(self.__peak_type_dict.values())

    def __GetProject(self):
        return self.__core_mgr.Get(PROJECT_MANAGER).GetProject()

    def OnEvent(self, event):
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_PROJECT_NEW:
            peak_type = self.GetSelectedPeakType()
            event = PeakTypeChangeEvent(peak_type, peak_type, self.__id)
            self.__core_mgr.SendEvent(event)

        elif event_type == wxEVT_PEAK_TYPE_CHANGE:
            peak_type = event.GetPeakType()
            self.__GetProject().SetPeakType(peak_type)
            self.__core_mgr.Get(MENUBAR_MANAGER).CheckMenuItem(peak_type.GetName())

            for spectrum_func_instance in SpectrumFunctionContainerBase._instance_list:
                spectrum_func_instance.OnPeakTypeChanged(event)

        elif event_type == wxEVT_PEAK_TYPE_REGISTER:
            peak_type_list = event.GetPeakTypeList()
            for peak_type in peak_type_list:
                if (peak_name := peak_type.GetName()) not in self.__peak_type_dict:
                    self.__peak_type_dict[peak_name] = peak_type

        elif event_type == wxEVT_EXIT:
            design = (
                (PEAK_TYPE, self.GetSelectedPeakType()),
            )

            for key, value in design:
                self.__io_mgr.SetSetting(key, value)


class DataManager(Singleton):
    """Manage references and selections about data.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        self.__core_mgr = kw['core_manager']
        self.__id = NewIdRef()

        self.__main_selection = deque([None, None], 2)
        self.__selection = deque([set(), set()], 2)
        self.__selected_recipe = Recipe()

    def __GetProject(self):
        return self.__core_mgr.Get(PROJECT_MANAGER).GetProject()

    def GetData(self, index: int) -> DataContainer:
        """Returns the data specified by the index.

        :type index: int
        :rtype: DataContainer
        """
        return self.GetDataList()[index]

    def SetData(self, index: int, data: DataContainer):
        """Set to the data specified by the index.

        :type index: int
        :type data: DataContainer
        """
        self.SetDataList([index], [data])

    def GetDataList(self, index_list: Iterable[int] = None) -> List[DataContainer]:
        """Returns the data specified in the list of indexes. If index_list is None, returns the all data list. This value is deepcopied.

        :type index_list: Iterable[int], optional
        :rtype: List[DataContainer]
        """
        data_list = self.__GetDataList()
        data_list = data_list if index_list is None else [data_list[index] for index in index_list]
        return deepcopy(data_list)

    def SetDataList(self, index_list: Iterable[int], data_list: Iterable[DataContainer]):
        """Sets the list of data corresponding to the specified list of indexes.

        :type index_list: Iterable[int]
        :type data_list: Iterable[DataContainer]
        """
        if any([not isinstance(data, DataContainer) for data in data_list]):
            raise TypeError()

        project = self.__GetProject()
        project.SetDataList(data_list, index_list)
        x_changed_list = y_changed_list = bg_changed_list = peaks_changed_list = recipe_changed_list = msg_changed_list = [True] * len(data_list)

        event = DataContentsChangeEvent(index_list, data_list, x_changed_list, y_changed_list, bg_changed_list, peaks_changed_list, recipe_changed_list, msg_changed_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def __GetDataList(self):
        return self.__GetProject().GetDataList()

    def GetX(self, index: int) -> ndarray:
        """Returns the x data of spectrum for a specified index.

        :type index: int
        :rtype: ndarray
        """
        return self.__GetDataList()[index].X

    def GetY(self, index: int) -> ndarray:
        """Returns the y data of spectrum for a specified index.

        :type index: int
        :rtype: ndarray
        """
        return self.__GetDataList()[index].Y

    def GetXY(self, index: int) -> Tuple[ndarray, ndarray]:
        """Returns the data of spectrum for a specified index.

        :type index: int
        :rtype: Tuple[ndarray, ndarray]
        """
        return self.__GetDataList()[index].XY

    def GetBackground(self, index: int) -> ndarray:
        """Returns the background of spectrum for a specified index.

        :type index: int
        :rtype: ndarray
        """
        return self.__GetDataList()[index].BackGround

    def GetPeaks(self, index: int) -> PeakFunctionContainerList:
        """Returns the peaks of spectrum for a specified index.

        :type index: int
        :rtype: PeakFunctionContainerList
        """
        return self.__GetDataList()[index].Peaks

    def GetRecipe(self, index: int) -> Recipe:
        """Returns the recipe for a specified index.

        :type index: int
        :rtype: Recipe
        """
        return self.__GetDataList()[index].Recipe

    def GetSelectedRecipe(self) -> Recipe:
        """Returns the selected recipe.

        :rtype: Recipe
        """
        return deepcopy(self.__selected_recipe)

    def SelectRecipe(self, recipe: Recipe):
        """Select a recipe.

        :type recipe: Recipe
        """
        if not isinstance(recipe, Recipe):
            raise TypeError()

        prev_recipe = self.__selected_recipe
        self.__selected_recipe = recipe
        event = RecipeSelectEvent(recipe, prev_recipe, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def ApplyRecipe(self, recipe: Recipe, index_list: Iterable[int] = None):
        """Applies a recipe.

        :type recipe: Recipe
        :param index_list: Applies a recipe to the specified list of indexes. Defaults to None
        :type index_list: Iterable[int], optional
        """
        if not isinstance(recipe, Recipe):
            raise TypeError()
        data_list = self.__GetDataList()
        index_list = self.GetSelection() if index_list is None else index_list

        if len(index_list) == 0:
            index_list = list(range(len(data_list)))

        for index in index_list:
            data = data_list[index]
            data.Recipe = deepcopy(recipe)

        event = DataContentsChangeEvent(index_list, data_list, recipe_changed_list=[True] * len(index_list), id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetMsg(self, index: int) -> str:
        """Returns the message for a specified index.

        :type index: int
        :rtype: str
        """
        return self.__GetDataList()[index].Msg

    def GetPath(self, index: int) -> str:
        """Returns the path for a specified index.

        :type index: int
        :rtype: str
        """
        return self.__GetDataList()[index].Path

    def GetSize(self, index: int) -> int:
        """Returns the size of spectrum for a specified index.

        :type index: int
        :rtype: int
        """
        return self.__GetDataList()[index].GetSpectrumSize()

    def GetDataSize(self) -> int:
        """Returns the size of data.
        """
        return len(self.__GetDataList())

    def GetMainSelection(self) -> int:
        """Return index of main selection.

        :rtype: int
        """
        return self.__main_selection[1]

    def GetSelection(self) -> Tuple[int, ...]:
        """Returns a list of indexes for the selection.

        :rtype: Tuple[int, ...]
        """
        return tuple(self.__selection[1])

    def Select(self, main_selection: Union[int, bool, None] = False, selection: Union[Iterable[int], bool, None] = False, operand: Optional[str] = None):
        """Change Data Selection.

        :param main_selection: If the main selection is int, select it; if None, deselect the selected one; if False, no change.
        :type main_selection: Union[int, False, None], optional
        :param selection: If the selection is a list of int, change the selection according to the operand; if None, deselect the all selection; if False, no change.
        :type selection: Union[Iterable[int], False, None], optional
        :param operand: The possible choices are '|', '-', '^' and None. They represent the sum set, difference set, exclusive set, and no change, respectively. defaults to None
        :type operand: Optional[str], optional
        """
        if main_selection is False and selection is False:
            raise ValueError()

        if selection is False:
            next_selection = self.__selection[1]
        elif selection is None:
            next_selection = set()
        else:
            selection = set(selection)
            if operand is None:
                next_selection = selection
            elif operand == '|':
                next_selection = self.__selection[1] | selection
            elif operand == '-':
                next_selection = self.__selection[1] - selection
            elif operand == '^':
                next_selection = self.__selection[1] ^ selection
            else:
                raise ValueError()

        if main_selection is False:
            next_main_selection = self.__main_selection[1]
        else:
            next_main_selection = main_selection

        if next_main_selection is not None:
            next_selection.add(main_selection)

        self.__selection.append(next_selection)
        self.__main_selection.append(next_main_selection)
        event = DataSelectionChangeEvent(self.__main_selection[1], self.__main_selection[0], list(self.__selection[1]), list(self.__selection[0]))
        self.__core_mgr.SendEvent(event)

    def GetIndexList(self, data_list: Iterable[DataContainer]) -> List[int]:
        """Returns the index list corresponding to the data list.

        :type data_list: Iterable[DataContainer]
        :rtype: List[int]
        """
        index_dict = {data: n for n, data in enumerate(self.__GetDataList())}
        return [index_dict[data] for data in data_list]

    def ExecuteSpectrumFunction(self, index_list: Optional[Iterable[int]] = None):
        """Executes the recipe provided for the data specified in the index list.

        :param index_list: If index_list is None, it will convert to all selections. Defaults to None
        :type index_list: Optional[Iterable[int]], optional
        :raises ValueError: [description]
        """
        data_list = self.__GetDataList()
        index_list = list(range(self.GetDataSize())) if index_list is None else index_list

        x_changed_list = []
        y_changed_list = []
        bg_changed_list = []
        peaks_changed_list = []
        msg_changed_list = []
        for index in index_list:
            data = data_list[index]

            x_changed_list.append(False)
            y_changed_list.append(False)
            bg_changed_list.append(False)
            peaks_changed_list.append(False)
            msg_changed_list.append(False)

            new_success_list = deepcopy(data.SuccessList)
            new_recipe = deepcopy(data.Recipe)
            for n in range(len(new_recipe)):
                if new_success_list[n]:
                    continue

                func_container = new_recipe[n]
                x, y = data.XY
                bg = data.BackGround
                peaks = data.Peaks

                try:
                    params = func_container.Execution(x, y, bg, peaks)
                    new_success_list[n] = True
                    msg = f'{str(func_container)} is successful in the execution.'
                    msg_changed_list[-1] = True
                except Exception as e:
                    params = []
                    new_success_list[n] = False
                    msg = '\n'.join(e.args)
                    msg_changed_list[-1] = True
                    LogError(msg)
                    break

                for param, return_param in zip(params, func_container.SendReturnParams()):
                    if return_param == 'x':
                        x = param
                        x_changed_list[-1] = True
                    elif return_param == 'y':
                        y = param
                        y_changed_list[-1] = True
                    elif return_param == 'b':
                        bg = param
                        bg_changed_list[-1] = True
                    elif return_param == 'p':
                        if isinstance(param, PeakFunctionContainerBase):
                            param = PeakFunctionContainerList([param])
                        peaks = param
                        peaks_changed_list[-1] = True
                    else:
                        raise ValueError()

                data.Append(Spectrum(x, y, bg, peaks), new_recipe, new_success_list, msg)

        index_list = self.GetIndexList(data_list)
        event = DataContentsChangeEvent(index_list, data_list, x_changed_list, y_changed_list, bg_changed_list, peaks_changed_list, [True] * len(index_list), msg_changed_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_DATA_SELECTION_CHANGE:
            prv_main_selection = event.GetPreviousMainSelection()
            crt_main_selection = event.GetMainSelection()
            self.__main_selection.append(prv_main_selection)
            self.__main_selection.append(crt_main_selection)
            prv_selection = event.GetPreviousSelection()
            crt_selection = event.GetSelection()
            self.__selection.append(set(prv_selection))
            self.__selection.append(set(crt_selection))

        elif event_type == wxEVT_DATA_CONTENTS_CHANGE:
            index_list = event.GetIndexList()
            data_list = event.GetDataList()
            project = self.__GetProject()
            project.SetDataList(data_list, index_list)

        elif event_type == wxEVT_RECIPE_SELECT:
            recipe = event.GetRecipe()
            self.__selected_recipe = recipe


class SpectrumManager(Singleton):
    """Manager for drawing spectra
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__id = NewIdRef()
        self.__focus_panel = None

    def Draw(self, need_bg=True, need_peaks=False, multi_draw_alpha=0.0):
        """Draws a spectrum.

        :param need_bg: Whether the background needs to be drawn or not. Defaults to True
        :type need_bg: bool, optional
        :param need_peaks: Whether the peak needs to be drawn or not, defaults to False
        :type need_peaks: bool, optional
        :param multi_draw_alpha: Transparency of the drawing of spectra selected other than the main selection. Defaults to 0.0
        :type multi_draw_alpha: float, optional
        """

        spectrum_panel = self.__core_mgr.Get(PANEL_MANAGER).GetPanel(SPECTRUM_PANEL)
        if spectrum_panel is None:
            print('set spectrum panel first!!')
            return

        spectrum_panel.Clear()

        data_mgr = self.__core_mgr.Get(DATA_MANAGER)

        if len(data_mgr.GetSelection()) == 0:
            spectrum_panel.canvas.draw()
            return

        main_selection = data_mgr.GetMainSelection()
        selection = data_mgr.GetSelection()

        line_list = []
        bg_line_list = []

        if main_selection is not None:
            x, y = data_mgr.GetXY(main_selection)
            line_list.append(Line2D(x, y, ls='', marker='.', ms=3, c='gray'))

            if need_bg:
                bg = data_mgr.GetBackground(main_selection)
                if len(bg) != 0:
                    bg_line_list.append(Line2D(x, bg, ls='', marker='.', ms=3, c='gray'))

            if need_peaks:
                for peak in data_mgr.GetPeaks(main_selection):
                    p_v = peak.Execution(x)
                    spectrum_panel.main_ax.add_line(Line2D(x, p_v, c='orange'))

        if multi_draw_alpha > 0:
            for i in selection:
                if i == main_selection:
                    continue

                x, y = data_mgr.GetXY(i)
                line_list.append(Line2D(x, y, alpha=multi_draw_alpha, ls='', marker='.', ms=3, c='gray'))

                if need_bg:
                    bg = data_mgr.GetBackground(i)
                    line_list.append(Line2D(x, y, alpha=multi_draw_alpha, ls='', marker='.', ms=3, c='gray'))

        for line in line_list:
            spectrum_panel.main_ax.add_line(line)

        if need_bg:
            for line in bg_line_list:
                spectrum_panel.bg_ax.add_line(line)

        spectrum_panel.main_ax.autoscale()
        spectrum_panel.bg_ax.autoscale()
        spectrum_panel.canvas.draw()

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()

        if event_type == wxEVT_PANEL_SELECTION_CHANGE:
            panel = event.GetPanel()
            if panel is not None and panel.NeedDraw():
                self.__focus_panel = panel

        if event_type in [wxEVT_DATA_SELECTION_CHANGE, wxEVT_DATA_CONTENTS_CHANGE, wxEVT_PANEL_SELECTION_CHANGE, wxEVT_PANEL_VIEW]:
            if self.__focus_panel is None or not self.__focus_panel.NeedDraw():
                self.Draw()
            else:
                need_bg = self.__focus_panel.NeedBackgroundDraw()
                need_peaks = self.__focus_panel.NeedPeaksDraw()
                multi_alpha = self.__focus_panel.NeedMultiDraw()
                self.Draw(need_bg, need_peaks, multi_alpha)


class EncodeManager(Singleton):
    """Manages parameters related to encode.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__encoding = None
        self.__delimiter = None

    def GetEncoding(self) -> ChoiceContainer:
        """Get the encoding to use when reading the file. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__encoding)

    def SelectEncoding(self, encoding: Union[str, ChoiceContainer]):
        """Select the encoding to be used when reading the file.

        :param encoding: type of encoding or instance of ChoiceContainer for encoding.
        :type encoding: Union[str, ChoiceContainer]
        """
        if isinstance(encoding, str):
            encoding_type = encoding
            encoding = deepcopy(self.__encoding)
            encoding.SetValue(encoding_type)

        if not isinstance(encoding, ChoiceContainer):
            raise TypeError()
        prev_encoding = self.__encoding
        self.__encoding = encoding
        event = EncodeEvent(encoding=encoding, previous_encoding=prev_encoding, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetDelimiter(self) -> ChoiceContainer:
        """Delimiter used to read files. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__delimiter)

    def SelectDelimiter(self, delimiter: Union[str, ChoiceContainer]):
        """Select the delimiter to be used when reading the file.

        :param delimiter: type of delimiter or instance of ChoiceContainer for delimiter.
        :type delimiter: Union[str, ChoiceContainer]
        """
        if isinstance(delimiter, str):
            delimiter_type = delimiter
            delimiter = deepcopy(self.__delimiter)
            delimiter.SetValue(delimiter_type)

        if not isinstance(delimiter, ChoiceContainer):
            raise TypeError()

        prev_delimiter = self.__delimiter
        self.__delimiter = delimiter
        event = EncodeEvent(delimiter=delimiter, previous_delimiter=prev_delimiter, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetEncodeFunctionNameContainer(self) -> ChoiceContainer:
        """Returns an instance of ChoiceContainer that contains a list of encoding functions.

        :rtype: ChoiceContainer
        """
        selected_func = self.__core_mgr.Get(FUNCTION_MANAGER).GetSelectedEncodeFunction()
        func_list = self.__core_mgr.Get(FUNCTION_MANAGER).GetEncodeFunctionList()
        selected_name = selected_func.__class__.__name__
        func_name_list = [func.__class__.__name__ for func in func_list]
        return ChoiceContainer(selected_name, func_name_list)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_ENCODE:
            if event.IsEncodingChanged():
                encoding = event.GetEncoding()
                self.__encoding = encoding

            if event.IsDelimiterChanged():
                delimiter = event.GetDelimiter()
                self.__delimiter = delimiter

        elif event_type == wxEVT_EXIT:
            design = (
                (ENCODE_ENCODING, self.__encoding),
                (ENCODE_DELIMITER, self.__delimiter),
            )

            for key, value in design:
                self.__io_mgr.SetSetting(key, value)


class DecodeManager(Singleton):
    """Manages parameters related to decode.
    """

    def __init__(self, *args, **kw):
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__encoding = None

    def GetEncoding(self) -> ChoiceContainer:
        """Get the encoding to use when reading the file. This value is deepcopied.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__encoding)

    def SelectEncoding(self, encoding: Union[str, ChoiceContainer]):
        """Select the encoding to be used when reading the file.

        :param encoding: type of encoding or instance of ChoiceContainer for encoding.
        :type encoding: Union[str, ChoiceContainer]
        """
        if isinstance(encoding, str):
            encoding_type = encoding
            encoding = deepcopy(self.__encoding)
            encoding.SetValue(encoding_type)

        if not isinstance(encoding, ChoiceContainer):
            raise TypeError()
        prev_encoding = self.__encoding
        self.__encoding = encoding
        event = DecodeEvent(encoding=encoding, previous_encoding=prev_encoding, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetDecodeFunctionNameContainer(self) -> ChoiceContainer:
        """Get an instance of ChoiceContainer that contains a list of encoding functions.

        :rtype: ChoiceContainer
        """
        selected_func = self.__core_mgr.Get(FUNCTION_MANAGER).GetSelectedDecodeFunction()
        func_list = self.__core_mgr.Get(FUNCTION_MANAGER).GetDecodeFunctionList()
        selected_name = selected_func.__class__.__name__
        func_name_list = [func.__class__.__name__ for func in func_list]
        return ChoiceContainer(selected_name, func_name_list)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_DECODE:
            if event.IsEncodingChanged():
                encoding = event.GetEncoding()
                self.__encoding = encoding

        elif event_type == wxEVT_EXIT:
            design = (
                (DECODE_ENCODING, self.__encoding),
            )

            for key, value in design:
                self.__io_mgr.SetSetting(key, value)


class MappingManager(Singleton):
    """Manages parameters related to mapping.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__table_size = (10, 10)
        self.__direction = DEFAULT_DIRECTION_CONTAINER
        self.__cmap = DEFAULT_COLORMAP

    def SetTableSize(self, *size):
        """
        Set table size related to the mapping.
        Tuple[int, int],
        int, int
        """
        if len(size) == 1:
            size = (size[0][0], size[0][1])

        if len(size) != 2:
            raise TypeError()

        if not HasValidElement(size, int):
            raise TypeError()

        x, y = size
        if x < 1 or y < 1:
            raise TypeError()

        prev_size = self.__table_size
        self.__table_size = tuple(size)

        event = TableSizeChangeEvent(size, prev_size, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetDirection(self) -> str:
        """
        Direction related to the mapping. The returned values are "r2u, "r2d", "l2u", "l2d", "u2r", "u2l", "d2r", "d2l".
        For example, r2d is

        0, 1, 2, 3,

        4, 5, 6, 7,

        8, 9, 10, 11,

        in that order.

        :rtype: str
        """
        return self.__direction.GetValue()

    def GetDirectionContainer(self) -> ChoiceContainer:
        """Get an instance of ChoiceContainer that contains a list of direction.

        :rtype: ChoiceContainer
        """
        return deepcopy(self.__direction)

    def SelectDirection(self, direction: Union[str, ChoiceContainer]):
        """Select direction

        :param direction: One of "r2u, "r2d", "l2u", "l2d", "u2r", "u2l", "d2r", "d2l".
        :type direction: Union[str, ChoiceContainer]
        """
        if isinstance(direction, ChoiceContainer):
            direction = direction.GetValue()

        if not isinstance(direction, str):
            raise TypeError()

        if not self.__direction.IsValidValue(direction):
            raise ValueError()

        prev_dir = self.GetDirection()
        self.__direction.SetValue(direction)

        event = DirectionChangeEvent(direction, prev_dir, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetDirectionList(self) -> Tuple[str, ...]:
        """Get a list of direction.

        :rtype: Tuple[str, ...]
        """
        return deepcopy(self.__direction.GetChoices())

    def GetColormap(self, name: str = None) -> Colormap:
        """Gets the colormap specified by name. If not specified, it gets the selected colormap.

        :type name: str, optional
        :rtype: Colormap
        """

        if name is None:
            return deepcopy(self.__cmap)

        return Colormap(name)

    def SelectColormap(self, cmap: Union[str, Colormap]):
        """Select the colormap related to the mapping.

        :type cmap: Union[str, Colormap]
        """
        if isinstance(cmap, Colormap):
            cmap = cmap.name

        if not isinstance(cmap, str):
            raise TypeError()

        prev_cmap = self.__cmap
        self.__cmap = cmap

        event = ColormapChangeEvent(cmap, prev_cmap, self.__id)
        self.__core_mgr.SendEvent(event)

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_TABLE_SIZE_CHANGE:
            self.__table_size = event.GetTableSize()
        elif event_type == wxEVT_DIRECTION_CHANGE:
            direction = event.GetDirection()
            self.__direction.SetValue(direction)

        elif event_type == wxEVT_COLORMAP_CHANGE:
            cmap = event.GetColorMap()
            self.__selected_cmap = cmap

        elif event_type == wxEVT_EXIT:
            self.__io_mgr.SetSetting(MAPPING_TABLE_SIZE, self.__table_size)
            self.__io_mgr.SetSetting(MAPPING_DIRECTION, self.__direction)
            self.__io_mgr.SetSetting(MAPPING_COLORMAP, self.__cmap)


# TODO: Create Color Theme Object
class ColorManager(Singleton):
    """Managers related to color
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__color_theme_dict = {}
        self.__selected_color_theme_name = None

    def GetDefaultColorTheme(self):
        return {
            "NAME": "Default Color",
            "COLOR": {
                "MAIN_SELECTION": "#fd7e00",
                "SELECTION": "#FFD400",
                "SUCCESS": "#00ff00",
                "ERROR": "#ff0000"
            }
        }

    def RegisterColorThemeList(self, color_theme_list: Union[List, Tuple, Dict]):
        """Register a list of color themes.

        :type color_theme_list: Union[List, Tuple, Dict]
        """
        if not isinstance(color_theme_list, (list, tuple)):
            color_theme_list = [color_theme_list]

        prev_color_theme_list = self.GetColorThemeList()

        for color_theme in color_theme_list:
            name = color_theme[NAME]
            self.__color_theme_dict[name] = color_theme

        if DEFAULT_COLOR_THEME not in self.__color_theme_dict:
            default_color_theme = self.GetDefaultColorTheme()
            name = default_color_theme[NAME]
            self.__color_theme_dict[name] = default_color_theme

        color_theme_list = self.GetColorThemeList()

        event = ColorRegisterEvent(color_theme_list, prev_color_theme_list, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetColorTheme(self, name: str) -> Dict:
        """Gets the color theme specified by name. If not found, an empty dictionary is returned.

        :type name: str
        :return: Color theme
        :rtype: Dict
        """
        return self.__color_theme_dict.get(name, {})

    def GetSelectedColorTheme(self) -> Dict:
        """Get the selected color theme.

        :rtype: Dict
        """
        return self.GetColorTheme(self.__selected_color_theme_name)

    def GetColorThemeNames(self) -> Tuple[str, ...]:
        """Get a list of registered color theme names.

        :rtype: Tuple[str, ...]
        """
        return tuple(self.__color_theme_dict.keys())

    def GetColorThemeList(self) -> Tuple[Dict, ...]:
        """Get a list of registered color themes.

        :rtype: Tuple[Dict, ...]
        """
        return tuple(self.__color_theme_dict.values())

    def SelectColorTheme(self, name: str):
        """Select a color theme.

        :param name: The name of the registered color theme.
        :type name: str
        """
        if not isinstance(name, str):
            raise TypeError()

        self.__selected_color_theme_name = name

        color_theme = self.GetSelectedColorTheme()
        event = ColorSelectionEvent(color_theme, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def GetMainSelectionColor(self) -> str:
        """Get the main selection color from the selected color theme.

        :return: e.g. #000000 ~ #FFFFFF
        :rtype: str
        """
        return self.GetSelectedColorTheme()[DotChain(COLOR, MAIN_SELECTION_COLOR)]

    def GetSelectionColor(self) -> str:
        """Get the selection color from the selected color theme.

        :return: e.g. #000000 ~ #FFFFFF
        :rtype: str
        """
        return self.GetSelectedColorTheme()[SELECTION_COLOR]

    def GetSuccessColor(self) -> str:
        """Get the success color from the selected color theme.

        :return: e.g. #000000 ~ #FFFFFF
        :rtype: str
        """
        return self.GetSelectedColorTheme()[SUCCESS_COLOR]

    def GetErrorColor(self) -> str:
        """Get the error color from the selected color theme.

        :return: e.g. #000000 ~ #FFFFFF
        :rtype: str
        """
        return self.GetSelectedColorTheme()[ERROR_COLOR]

    def OnEvent(self, event):
        event.Skip()
        if event.GetId() == self.__id:
            return

        event_type = event.GetEventType()
        if event_type == wxEVT_COLOR_REGISTER:

            for color_theme in event.GetColorThemeList():
                name = color_theme[NAME]
                self.__color_theme_dict[name] = color_theme

        elif event_type == wxEVT_COLOR_SELECT:
            name = event.GetName()
            self.__selected_color_theme_name = name

        elif event_type == wxEVT_EXIT:
            color_theme_list = self.GetColorThemeList()
            self.__io_mgr.SaveColorThemeList(color_theme_list)


class PreferenceManager(Singleton):
    """Managers related to preference
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__()
        self.__core_mgr = kw['core_manager']
        self.__io_mgr = kw['io_manager']
        self.__id = NewIdRef()

        self.__data_buffer = -1

    def GetDataBufferSize(self) -> int:
        """Get the data buffer size.

        :rtype: int
        """
        return self.__data_buffer

    def GetDataBufferSizeContainer(self) -> IntContainer:
        """Get an IntContainer containing the data buffer size.

        :rtype: IntContainer
        """
        return IntContainer(self.__data_buffer, 1, MAX_DATA_BUFFER_SIZE)

    def SetDataBufferSize(self, size: int):
        """Set the data buffer size, which must be greater than or equal to 0.

        :type size: int
        """
        if isinstance(size, IntContainer):
            size = size.GetValue()

        if not isinstance(size, int):
            raise TypeError()

        if size < 1:
            raise ValueError()

        prev_size = self.__data_buffer
        self.__data_buffer = size

        event = PreferenceEvent(size, prev_size, id=self.__id)
        self.__core_mgr.SendEvent(event)

    def OnEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_PREFERENCE:
            if event.IsDataBufferSizeChanged():
                self.__data_buffer = event.GetDataBufferSize()

        elif event_type == wxEVT_EXIT:
            design = (
                (DATA_BUFFER_SIZE, self.__data_buffer),
            )

            for key, value in design:
                self.__io_mgr.SetSetting(key, value)


__all__ = [
    'IOManager',
    'EventManager',
    'MenubarManager',
    'PanelManager',
    'FunctionManager',
    'ProjectManager',
    'PeakManager',
    'DataManager',
    'SpectrumManager',
    'EncodeManager',
    'DecodeManager',
    'MappingManager',
    'ColorManager',
    'PreferenceManager',
]
