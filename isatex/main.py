from logging import DEBUG, WARNING, FileHandler, getLogger
from typing import Any

from wx import (EVT_MENU, EVT_MENU_OPEN, ID_CLOSE, ICON_NONE, App, Frame,
                LogError, NewIdRef, wxEVT_CLOSE_WINDOW)

from const import (APPLICATION_NAME, COLOR_MANAGER, COLOR_THEME_LIST,
                   DATA_BUFFER_SIZE, DATA_MANAGER, DECODE_ENCODING,
                   DECODE_MANAGER, ENCODE_DELIMITER, ENCODE_ENCODING,
                   ENCODE_MANAGER, EVENT_LIST, EVENT_MANAGER,
                   EVENT_RECEPTOR_CLASS_LIST, FUNCTION_CLASS_LIST,
                   FUNCTION_MANAGER, LAYOUT_LIST, MANAGER_LIST,
                   MAPPING_COLORMAP, MAPPING_DIRECTION, MAPPING_MANAGER,
                   MAPPING_TABLE_SIZE, MENUBAR_MANAGER, PANEL_MANAGER,
                   PEAK_FUNCTION_CLASS_LIST, PEAK_MANAGER, PEAK_TYPE,
                   PERSPECTIVE_SETTING, PREFERENCE_MANAGER, PROJECT_MANAGER,
                   SELECTED_COLOR_THEME, SELECTED_DECODE_FUNCTION,
                   SELECTED_ENCODE_FUNCTION, SELECTED_LAYOUT,
                   SELECTED_MAPPING_FUNCTION, SETTING_FILE_PATH,
                   SPECTRUM_FUNCTION_PRESET_LIST, SPECTRUM_MANAGER,
                   WINDOW_SIZE)
from container import CustomMenuItemBase, PanelBase
from core import CommunicableObjectBase, SettingStorableObjectBase
from defaultevent import ExitEvent, LaunchEvent
from manager import (ColorManager, DataManager, DecodeManager, EncodeManager,
                     EventManager, FunctionManager, IOManager, MappingManager,
                     MenubarManager, PanelManager, PeakManager,
                     PreferenceManager, ProjectManager, SpectrumManager)
from objects import (PeakType, SpectrumFunctionContainerAccessor,
                     SpectrumFunctionContainerBase)
from util import DotChain, DotNotationDict, Singleton

logger = getLogger(__name__)
logger.setLevel(DEBUG)

handler = FileHandler('logger.log', 'a')
logger.addHandler(handler)


class CoreManager(Singleton):
    """Core manager supervising managers.
    """

    def __init__(self, setting_file_path: str):
        """Default constructor

        :param setting_file_path: Path to a file to read the settings
        :type setting_file_path: str
        """
        super().__init__()
        self.__app = App()
        self.__id = NewIdRef()

        self.__io_mgr = IOManager(setting_file_path, self)
        self.__public_mgr_dict = DotNotationDict()
        self.__temp_setting = {}

        CommunicableObjectBase._core_mgr = self

        window_size = self.Get(WINDOW_SIZE)
        self.__main_window = MainWindow(self, parent=None, size=window_size)

        self.__public_mgr_dict = self.__CreatePublicManager()
        self.__temp_setting[MANAGER_LIST] = lambda: list(self.__public_mgr_dict.values())

        SpectrumFunctionContainerBase.data_accessor = SpectrumFunctionContainerAccessor(self.Get(DATA_MANAGER), self.Get(PEAK_MANAGER))
        self.__InitializePublicManagers()
        self.__RestoreStorableObjSetting()

        self.InitialTitle()

    def Launch(self, menubar_design: dict = None, setting_file_path: str = SETTING_FILE_PATH):
        """Launch iSATex.

        :param menubar_design: Menu bar design. Please refer to "MenubarManager.GetMenubarDesign"\'s documentation for details. Defaults to None
        :type menubar_design: dict, optional
        :param setting_file_path: Path to a file to read the settings, defaults to SETTING_FILE_PATH
        :type setting_file_path: str, optional
        """
        logger.info('launch app.')

        menubar_design = self.Get(MENUBAR_MANAGER).GetMenubarDesign() if menubar_design is None else menubar_design
        menubar = self.Get(MENUBAR_MANAGER).CreateMenubar(menubar_design)
        self.__main_window.SetMenuBar(menubar)
        self.__main_window.Show()

        event = LaunchEvent(id=self.__id)
        self.SendEvent(event)
        try:
            self.__app.MainLoop()
        except Exception as e:
            LogError('The application did not terminate successfully.\nPlease check the log file.')
            logger.error(e)

        logger.info('end app.')

    def Get(self, key: str, default: Any = None, *args):
        """Get a reference to the manager.

        :type key: str
        :param default: Return value when the specified key is not found, defaults to None
        :type default: Any, optional
        :rtype: Any
        """
        if key in self.__temp_setting:
            func = self.__temp_setting[key]
            return func() if len(args) == 0 else func(args)

        if key in self.__public_mgr_dict:
            return self.__public_mgr_dict[key]

        return self.__io_mgr.GetSetting(key, default)

    def SendEvent(self, event):
        """
            This function sends an event to an instance of the "PanelBase" class and to the manager.
            Note that the event will not be sent until the project is started.

        :param event: Event object to be sent.
        :type event: Any type
        """
        self.Get(EVENT_MANAGER).SendEvent(event)

    def InitialTitle(self):
        """Initializes the title of the main window.
        """
        self.__main_window.SetTitle(APPLICATION_NAME)

    def GetTitle(self) -> str:
        """Get the title of the current main window.

        :rtype: str
        """
        full_title = self.GetFullTitle()
        start = full_title.find('-')
        end = full_title.rfind('-')
        return full_title[start + 1: end]

    def GetFullTitle(self) -> str:
        """Get the title of the main window that is being displayed.

        :rtype: str
        """
        return self.__main_window.GetTitle()

    def SetTitle(self, title: str):
        """Sets the title of the main window.

        :type title: str
        """
        is_saved = self.Get(PROJECT_MANAGER).IsProjectSaved()
        title = f'{APPLICATION_NAME} -{title}- '
        title += '' if is_saved else '(unsaved)'
        self.__main_window.SetTitle(title)

    def __CreatePublicManager(self):
        design = (
            (MENUBAR_MANAGER, MenubarManager),
            (PANEL_MANAGER, PanelManager),
            (EVENT_MANAGER, EventManager),
            (FUNCTION_MANAGER, FunctionManager),
            (ENCODE_MANAGER, EncodeManager),
            (DECODE_MANAGER, DecodeManager),
            (MAPPING_MANAGER, MappingManager),
            (PROJECT_MANAGER, ProjectManager),
            (PEAK_MANAGER, PeakManager),
            (DATA_MANAGER, DataManager),
            (SPECTRUM_MANAGER, SpectrumManager),
            (COLOR_MANAGER, ColorManager),
            (PREFERENCE_MANAGER, PreferenceManager),
        )
        public_mgr_dict = {}
        for key, mgr in design:
            public_mgr_dict[key] = mgr(core_manager=self, io_manager=self.__io_mgr)

        return public_mgr_dict

    def __InitializePublicManagers(self):
        """
            Initialize the manager.
            The 'Get' function should not be used for anything other than getting the manager, because of the complexity of the reference.
        """

        # Create the necessary instances for the setting
        event_list = self.__io_mgr.GetSetting(EVENT_LIST)
        spectrum_preset_list = self.__io_mgr.GetSetting(SPECTRUM_FUNCTION_PRESET_LIST)
        function_list = [FuncClass() for FuncClass in self.__io_mgr.GetSetting(FUNCTION_CLASS_LIST)]
        peak_function_list = list(sorted([PeakFunc() for PeakFunc in self.__io_mgr.GetSetting(PEAK_FUNCTION_CLASS_LIST, [])], key=lambda x: x.__class__.__name__))
        peak_type_list = [PeakType(peak) for peak in peak_function_list]
        peak_type = self.__io_mgr.GetSetting(PEAK_TYPE)
        data_buffer_size = self.__io_mgr.GetSetting(DATA_BUFFER_SIZE)
        selected_encode_func = self.__io_mgr.GetSetting(SELECTED_ENCODE_FUNCTION)
        selected_decode_func = self.__io_mgr.GetSetting(SELECTED_DECODE_FUNCTION)
        selected_mapping_func = self.__io_mgr.GetSetting(SELECTED_MAPPING_FUNCTION)
        encode_encoding = self.__io_mgr.GetSetting(ENCODE_ENCODING)
        encode_delimiter = self.__io_mgr.GetSetting(ENCODE_DELIMITER)
        decode_encoding = self.__io_mgr.GetSetting(DECODE_ENCODING)
        table_size = self.__io_mgr.GetSetting(MAPPING_TABLE_SIZE)
        direction = self.__io_mgr.GetSetting(MAPPING_DIRECTION)
        cmap = self.__io_mgr.GetSetting(MAPPING_COLORMAP)
        layout_list = self.__io_mgr.GetSetting(LAYOUT_LIST)
        selected_layout = self.__io_mgr.GetSetting(SELECTED_LAYOUT)
        color_theme_list = self.__io_mgr.GetSetting(COLOR_THEME_LIST)
        selected_color_theme = self.__io_mgr.GetSetting(SELECTED_COLOR_THEME)

        event_receptor_list = []
        menu_item_list = []
        panel_list = []
        for EventReceptor in self.__io_mgr.GetSetting(EVENT_RECEPTOR_CLASS_LIST):
            if issubclass(EventReceptor, CustomMenuItemBase):
                event_receptor = EventReceptor()
                menu_item_list.append(event_receptor)
            elif issubclass(PanelBase, PanelBase):
                event_receptor = EventReceptor(parent=self.__main_window)
                panel_list.append(event_receptor)
            elif issubclass(EventReceptor, PanelBase):
                continue
            else:
                event_receptor = EventReceptor()

            event_receptor_list.append(event_receptor)

        self.Get(MENUBAR_MANAGER).RegisterMenuItemList(menu_item_list)
        self.Get(EVENT_MANAGER).RegisterEventList(event_list)
        self.Get(PANEL_MANAGER).SetMainWindow(self.__main_window)
        # PanelClassList = self.__io_mgr.GetSetting(DotChain(PANEL, CLASS_LIST))
        # panel_list = self.Get(PANEL_MANAGER).RegisterPanelList(PanelClassList, perspective_setting, self.__main_window)
        # event_receptor_list.extend(panel_list)
        self.Get(PANEL_MANAGER).RegisterLayout(layout_list)
        self.Get(PANEL_MANAGER).RegisterPanelList(panel_list, selected_layout)
        self.Get(EVENT_MANAGER).RegisterEventReceptorList(event_receptor_list)
        self.Get(FUNCTION_MANAGER).RegisterFunctionList(function_list)
        self.Get(FUNCTION_MANAGER).RegisterPreset(spectrum_preset_list)
        self.Get(FUNCTION_MANAGER).SelectEncodeFunction(selected_encode_func)
        self.Get(FUNCTION_MANAGER).SelectDecodeFunction(selected_decode_func)
        self.Get(FUNCTION_MANAGER).SelectMappingFunction(selected_mapping_func)
        self.Get(PEAK_MANAGER).RegisterPeakTypeList(peak_type_list)
        self.Get(PEAK_MANAGER).SelectPeakType(peak_type)
        self.Get(ENCODE_MANAGER).SelectEncoding(encode_encoding)
        self.Get(ENCODE_MANAGER).SelectDelimiter(encode_delimiter)
        self.Get(DECODE_MANAGER).SelectEncoding(decode_encoding)
        self.Get(MAPPING_MANAGER).SelectDirection(direction)
        self.Get(MAPPING_MANAGER).SetTableSize(table_size)
        self.Get(MAPPING_MANAGER).SelectColormap(cmap)
        self.Get(COLOR_MANAGER).RegisterColorThemeList(color_theme_list)
        self.Get(COLOR_MANAGER).SelectColorTheme(selected_color_theme)
        self.Get(PREFERENCE_MANAGER).SetDataBufferSize(data_buffer_size)

    def __RestoreStorableObjSetting(self):
        for editor in self.__GetEditorList():
            if not isinstance(editor, SettingStorableObjectBase):
                continue

            setting = {}
            for key in editor.RequireSetting():
                if self.__io_mgr.IsUnknownSetting(key) and key not in self.__temp_setting:
                    register_key = self.__ConvertRegisterKey(key, editor)
                    value = self.Get(register_key)
                else:
                    value = self.Get(key)

                setting[key] = value

            editor.ReceiveSetting(setting)

    def __StoreStorableObjectSetting(self):
        for editor in self.__GetEditorList():
            if not isinstance(editor, SettingStorableObjectBase):
                continue

            for key, value in editor.SendSetting().items():
                if not (self.__io_mgr.IsUnknownSetting(key) or self.__io_mgr.IsCustomSetting(key)):
                    continue

                key = self.__ConvertRegisterKey(key, editor)
                self.__io_mgr.SetSetting(key, value)

    def SaveSetting(self):
        """Save the state of the application.
        """
        event = ExitEvent(self.__id)
        self.SendEvent(event)

        self.__StoreStorableObjectSetting()
        self.__io_mgr.SaveSetting()

    def __ConvertRegisterKey(self, key, editor: SettingStorableObjectBase):
        if not isinstance(editor, SettingStorableObjectBase):
            raise TypeError()

        return DotChain(editor.__class__.__name__, key)

    def __DeConvertRegisterKey(self, key, editor: SettingStorableObjectBase):
        if not isinstance(editor, SettingStorableObjectBase):
            raise TypeError()

        return key.lstrip(f'{editor.__class__.__name__}.')

    def __GetEditorList(self):
        return [obj for obj in self.Get(PANEL_MANAGER).GetPanelList() + self.Get(MENUBAR_MANAGER).GetMenuItemList() if isinstance(obj, SettingStorableObjectBase)]

    def OnEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_CLOSE_WINDOW:
            event.Skip()
            self.__main_window.Destroy()


class Manager(Singleton):
    """Manager of iSATex
    """

    def __init__(self, setting_file_path: str = SETTING_FILE_PATH):
        """Default constructor

        :param setting_file_path: Path to a file to read the settings, defaults to SETTING_FILE_PATH
        :type setting_file_path: str, optional
        """
        super().__init__()
        self.__core_manager = CoreManager(setting_file_path)

    def Launch(self):
        """Launch iSATex.
        """
        self.__core_manager.Launch()

    def GetMenubarDesign(self):
        """Get the design of the menu bar.
        """
        self.__core_manager.Get(MENUBAR_MANAGER).GetMenubarDesign()

    def SetMenubarDesign(self, design: dict):
        """Sets the design of the menu bar.

        :param design: Menu bar design. Please refer to "MenubarManager.GetMenubarDesign"\'s documentation for details.
        :type design: dict
        """
        self.__core_manager.Get(MENUBAR_MANAGER).SetMenubarDesign(design)


class MainWindow(Frame):
    """Main window
    """

    def __init__(self, core_manager, *args, **kw):
        """Default constructor

        :param core_manager: Manager
        """
        super().__init__(*args, **kw)
        self.__core_mgr = core_manager
        self.Bind(EVT_MENU, self.__OnEvent)
        self.Bind(EVT_MENU_OPEN, self.__OnEvent)
        self.Show()

    def SetEventList(self, event_list):
        for event in event_list:
            self.Bind(event, self.__OnEvent)

    def __OnEvent(self, event):
        event.Skip()
        self.__core_mgr.SendEvent(event)
        if event.GetId() == ID_CLOSE:
            self.Close()

    def Destroy(self):
        is_success = self.__core_mgr.Get(PROJECT_MANAGER).AskProjectSaving()

        if not is_success:
            return False

        self.__core_mgr.SaveSetting()
        return super().Destroy()


def iSATex(setting_file_path: str = SETTING_FILE_PATH):
    """

    :param setting_file_path: Path to a file to read the settings, defaults to SETTING_FILE_PATH
    :type setting_file_path: str, optional
    """
    manager = Manager(setting_file_path=setting_file_path)
    manager.Launch()


__all__ = [
    'CoreManager',
    'Manager',
    'MainWindow',
    'iSATex',
]

if __name__ == "__main__":
    from logging import basicConfig

    # If you want to see the logs of the imported module, you can change the log level of basicConfig.
    # Example basicConfig(filename='logger.log', level=DEBUG)
    basicConfig(filename='logger.log', level=WARNING, filemode='w')

    iSATex()
