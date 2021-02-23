from sys import modules

from wx import NewIdRef

from util import DotChain


class ConstError(TypeError):
    pass


class _ConstManager:
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError(f'Can\'t rebind const {name}')

        return super().__setattr__(name, value)


const_mgr = _ConstManager()
const_mgr.APPLICATION_NAME = 'iSATex'

const_mgr.SETTING_FILE_PATH = 'setting.json'
const_mgr.PLUGIN_FOLDER_PATH = './Plugin/'
const_mgr.COLOR_THEME_FOLDER_PATH = './ColorTheme/'

const_mgr.PLUGIN_EXTENSION = '.plgn'
const_mgr.SAVEFILE_EXTENSION = '.itsv'
const_mgr.SAVEFILE_WILDCARD = f'{const_mgr.SAVEFILE_EXTENSION[1:].upper()} files (*{const_mgr.SAVEFILE_EXTENSION})|*{const_mgr.SAVEFILE_EXTENSION}'
const_mgr.SAVE_ENCODING = 'utf-8'

# Setting
const_mgr.DATA_BUFFER_SIZE = 'DATA_BUFFER_SIZE'
const_mgr.WINDOW_SIZE = 'WINDOW_SIZE'
const_mgr.PERSPECTIVE_SETTING = 'PERSPECTIVE_SETTING'

# Manager
const_mgr.MENUBAR_MANAGER = 'MENUBAR_MANAGER'
const_mgr.SPECTRUM_MANAGER = 'SPECTRUM_MANAGER'
const_mgr.PEAK_MANAGER = 'PEAK_MANAGER'
const_mgr.DATA_MANAGER = 'DATA_MANAGER'
const_mgr.PROJECT_MANAGER = 'PROJECT_MANAGER'
const_mgr.PANEL_MANAGER = 'PANEL_MANAGER'
const_mgr.EVENT_MANAGER = 'EVENT_MANAGER'
const_mgr.FUNCTION_MANAGER = 'FUNCTION_MANAGER'
const_mgr.ENCODE_MANAGER = 'ENCODE_MANAGER'
const_mgr.DECODE_MANAGER = 'DECODE_MANAGER'
const_mgr.MAPPING_MANAGER = 'MAPPING_MANAGER'
const_mgr.COLOR_MANAGER = 'COLOR_MANAGER'
const_mgr.PREFERENCE_MANAGER = 'PREFERENCE_MANAGER'

const_mgr.NAME = 'NAME'
const_mgr.PEAK_TYPE = 'PEAK_TYPE'
const_mgr.STORABLE_OBJECT_DICT = 'STORABLE_OBJECT_DICT'

# Setting type
const_mgr.INITIAL = 'INITIAL'
const_mgr.DEFAULT = 'DEFAULT'
const_mgr.CUSTOM = 'CUSTOM'
const_mgr.TEMPORARY = 'TEMPORARY'
const_mgr.UNKNOWN = 'UNKNOWN'

# MenubarManager
const_mgr.SEPARATOR = 'SEPARATOR'
const_mgr.FILE_MENU = '&File'
const_mgr.NEW_MENU_ITEM = '&New\tCtrl+N'
const_mgr.NEW_MENU_ITEM_HELP = 'Load experimental data'
const_mgr.OPEN_MENU_ITEM = '&Open\tCtrl+O'
const_mgr.SAVE_MENU_ITEM = '&Save\tCtrl+S'
const_mgr.SAVE_AS_MENU_ITEM = '&Save As\tCtrl+Shift+S'
const_mgr.EXPORT_MENU_ITEM = '&Export\tCtrl+E'
const_mgr.IMPORT_PLUGIN_MENU_ITEM = 'Import Plugin'
const_mgr.EXPORT_PLUGIN_MENU_ITEM = 'Export Plugin'
const_mgr.EXIT_MENU_ITEM = 'E&xit\tCtrl+W'
const_mgr.EDIT_MENU = '&Edit'
const_mgr.PROJECT_MENU = '&Project'
const_mgr.PROJECT_MEMO_MENU_ITEM = '&Memo'
const_mgr.PEAK_MENU = '&Peak'
const_mgr.PLUGIN_MENU = 'P&lugind'
const_mgr.PREFERENCE_MENU_ITEM = 'P&reference'
const_mgr.SHOW_PANEL_MENU = 'Panel'
const_mgr.VIEW_MENU = '&View'
const_mgr.LAYOUT_MENU = 'Layout'
const_mgr.HELP_MENU = '&Help'
const_mgr.ABOUT_MENU_ITEM = 'About'
const_mgr.TUTORIAL_MENU_ITEM = 'Tutorial'

# Widget ID
const_mgr.ID_NORMAL_TEXT = NewIdRef()
const_mgr.ID_NORMAL_LINE = NewIdRef()
const_mgr.ID_NORMAL_BUTTON = NewIdRef()
const_mgr.ID_NORMAL_COMBOBOX = NewIdRef()
const_mgr.ID_COLORMAP_COMBOBOX = NewIdRef()
const_mgr.ID_BROWSE = NewIdRef()
const_mgr.ID_PREVIEW = NewIdRef()
const_mgr.ID_SET = NewIdRef()
const_mgr.ID_CLEAR = NewIdRef()
const_mgr.ID_SAVE = NewIdRef()
const_mgr.ID_ADD = NewIdRef()
const_mgr.ID_DONT_SAVE = NewIdRef()

# Core Panel
const_mgr.MAIN_WINDOW = 'MAIN_WINDOW'
const_mgr.SPECTRUM_PANEL = 'SpectrumPanel'
const_mgr.SUB_SPECTRUM_PANEL = 'SubSpectrumPanel'

# Suffix
const_mgr.SHOW = 'SHOW'
const_mgr.HIDE = 'HIDE'

const_mgr.DEFAULT_COLORMAP = 'viridis'
const_mgr.SPECTRUM_LAYOUT = ('Default Layout', 'layout2|name=panel5fffe7470000000100000001;caption=Data Selector;state=738199548;dir=4;layer=0;row=0;pos=0;prop=100000;bestw=120;besth=100;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=panel5fffe7470000000100000002;caption=Execute Panel;state=738199548;dir=2;layer=1;row=2;pos=0;prop=100000;bestw=95;besth=64;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=95;floath=64;notebookid=-1;transparent=255|name=panel5fffe7470000000100000003;caption=Function Selector;state=738199548;dir=4;layer=0;row=1;pos=1;prop=100000;bestw=0;besth=29;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=109;floath=158;notebookid=-1;transparent=255|name=panel5fffe7470000000100000004;caption=Mapping Viewer;state=9328134140;dir=2;layer=1;row=3;pos=1;prop=100000;bestw=402;besth=268;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=402;floath=268;notebookid=-1;transparent=255|name=panel5fffe7470000000100000005;caption=Peak Selector;state=738199548;dir=4;layer=0;row=0;pos=1;prop=100000;bestw=128;besth=75;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=panel5fffe7470000000100000006;caption=Preset Selector;state=738199548;dir=4;layer=0;row=1;pos=0;prop=100000;bestw=0;besth=29;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=0;floath=29;notebookid=-1;transparent=255|name=panel5fffe7470000000100000007;caption=Recipe Panel;state=738199548;dir=2;layer=1;row=3;pos=0;prop=100000;bestw=190;besth=74;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=190;floath=74;notebookid=-1;transparent=255|name=panel5fffe7470000000100000008;caption=Recovery Panel;state=738199550;dir=4;layer=0;row=0;pos=0;prop=100000;bestw=357;besth=52;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|name=panel5fffe7470000000100000009;caption=Spectrum Panel;state=768;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=244;besth=134;minw=-1;minh=-1;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1;notebookid=-1;transparent=255|dock_size(4,0,0)=130|dock_size(2,1,2)=97|dock_size(4,0,1)=10|dock_size(2,1,3)=235|dock_size(5,0,0)=235|',)

MANAGER = const_mgr.MANAGER = 'MANAGER'
FUNCTION = const_mgr.FUNCTION = 'FUNCTION'
PANEL = const_mgr.PANEL = 'PANEL'
MENU_ITEM = const_mgr.MENU_ITEM = 'MENU_ITEM'
EVENT = const_mgr.EVENT = 'EVENT'
RECEPTOR = const_mgr.RECEPTOR = 'RECEPTOR'

CLASS_LIST = const_mgr.CLASS_LIST = 'CLASS_LIST'
SELECTED = const_mgr.SELECTED = 'SELECTED'
const_mgr.FUNCTION_CLASS_LIST = DotChain(FUNCTION, CLASS_LIST)
const_mgr.PANEL_CLASS_LIST = DotChain(PANEL, CLASS_LIST)
const_mgr.EVENT_RECEPTOR_CLASS_LIST = DotChain(EVENT, RECEPTOR, CLASS_LIST)

DECODE = const_mgr.DECODE = 'DECODE'
const_mgr.DECODE_FUNCTION_CLASS_LIST = DotChain(FUNCTION, DECODE, CLASS_LIST)
const_mgr.SELECTED_DECODE_FUNCTION = DotChain(FUNCTION, DECODE, SELECTED)

ENCODE = const_mgr.ENCODE = 'ENCODE'
const_mgr.ENCODE_FUNCTION_CLASS_LIST = DotChain(FUNCTION, ENCODE, CLASS_LIST)
const_mgr.SELECTED_ENCODE_FUNCTION = DotChain(FUNCTION, ENCODE, SELECTED)

SPECTRUM = const_mgr.SPECTRUM = 'SPECTRUM'
PRESET_LIST = const_mgr.PRESET_LIST = 'PRESET_LIST'
const_mgr.SPECTRUM_FUNCTION_CLASS_LIST = DotChain(FUNCTION, SPECTRUM, CLASS_LIST)
const_mgr.SPECTRUM_FUNCTION_PRESET_LIST = DotChain(FUNCTION, SPECTRUM, PRESET_LIST)

PEAK = const_mgr.PEAK = 'PEAK'
const_mgr.PEAK_FUNCTION_CLASS_LIST = DotChain(FUNCTION, PEAK, CLASS_LIST)

MAPPING = const_mgr.MAPPING = 'MAPPING'
const_mgr.MAPPING_FUNCTION_CLASS_LIST = DotChain(FUNCTION, MAPPING, CLASS_LIST)
const_mgr.SELECTED_MAPPING_FUNCTION = DotChain(FUNCTION, MAPPING, SELECTED)

LIST = const_mgr.LIST = 'LIST'
const_mgr.MANAGER_LIST = DotChain(MANAGER, LIST)
const_mgr.MENU_ITEM_LIST = DotChain(MENU_ITEM, LIST)
const_mgr.PANEL_LIST = DotChain(PANEL, LIST)
const_mgr.EVENT_LIST = DotChain(EVENT, LIST)
const_mgr.EVENT_RECEPTOR_LIST = DotChain(EVENT, RECEPTOR, LIST)
const_mgr.SETTING_STORABLE_OBJECT_CLASS_LIST = 'SETTING_STORABLE_OBJECT_CLASS_LIST'

COLOR_THEME = const_mgr.COLOR_THEME = 'COLOR_THEME'
const_mgr.COLOR_THEME_LIST = DotChain(COLOR_THEME, LIST)
const_mgr.SELECTED_COLOR_THEME = DotChain(COLOR_THEME, SELECTED)

LAYOUT = const_mgr.LAYOUT = 'LAYOUT'
const_mgr.SELECTED_LAYOUT = DotChain(LAYOUT, SELECTED)
const_mgr.LAYOUT_LIST = DotChain(LAYOUT, LIST)

ENCODING = const_mgr.ENCODING = 'ENCODING'
DELIMITER = const_mgr.DELIMITER = 'DELIMITER'
const_mgr.ENCODE_ENCODING = DotChain(ENCODE, ENCODING)
const_mgr.ENCODE_DELIMITER = DotChain(ENCODE, DELIMITER)

const_mgr.DECODE_ENCODING = DotChain(DECODE, ENCODING)

TABLE_SIZE = const_mgr.TABLE_SIZE = 'TABLE_SIZE'
DIRECTION = const_mgr.DIRECTION = 'DIRECTION'
COLORMAP = const_mgr.COLORMAP = 'COLORMAP'
const_mgr.MAPPING_TABLE_SIZE = DotChain(MAPPING, TABLE_SIZE)
const_mgr.MAPPING_DIRECTION = DotChain(MAPPING, DIRECTION)
const_mgr.MAPPING_COLORMAP = DotChain(MAPPING, COLORMAP)

# Color
COLOR = const_mgr.COLOR = 'COLOR'
MAIN_SELECTION = const_mgr.MAIN_SELECTION = 'MAIN_SELECTION'
SELECTION = const_mgr.SELECTION = 'SELECTION'
SUCCESS = const_mgr.SUCCESS = 'SUCCESS'
ERROR = const_mgr.ERROR = 'ERROR'

const_mgr.DEFAULT_COLOR_THEME = 'Default Color'

const_mgr.MAIN_SELECTION_COLOR = DotChain(COLOR, MAIN_SELECTION)
const_mgr.SELECTION_COLOR = DotChain(COLOR, SELECTION)
const_mgr.SUCCESS_COLOR = DotChain(COLOR, SUCCESS)
const_mgr.ERROR_COLOR = DotChain(COLOR, ERROR)

const_mgr.MAX_DATA_BUFFER_SIZE = 100

modules[__name__] = const_mgr
