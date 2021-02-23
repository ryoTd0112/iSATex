from abc import abstractmethod
from typing import Union

from wx import (ITEM_CHECK, ITEM_NORMAL, ITEM_RADIO, EmptyString, MenuItem,
                NewIdRef, Panel, PyCommandEvent)

from core import (CommunicableObjectBase, SettingStorableObjectBase,
                  iSATexObject)
from defaultevent import (ColorEvent, ColormapChangeEvent, ColorRegisterEvent,
                          ColorSelectionEvent, DataContentsChangeEvent,
                          DataEvent, DataSelectionChangeEvent, DecodeEvent,
                          DecodeFunctionDeregisterEvent,
                          DecodeFunctionRegisterEvent,
                          DecodeFunctionSelectEvent, DirectionChangeEvent,
                          EncodeEvent, EncodeFunctionDeregisterEvent,
                          EncodeFunctionRegisterEvent,
                          EncodeFunctionSelectEvent, ExitEvent, FunctionEvent,
                          FunctionRegisterEvent, LaunchEvent,
                          LayoutChangeEvent, LayoutEvent, LayoutRegisterEvent,
                          MappingEvent, MappingFunctionDeregisterEvent,
                          MappingFunctionRegisterEvent,
                          MappingFunctionSelectEvent, PanelEvent,
                          PanelRegisterEvent, PanelSelectionChangeEvent,
                          PanelViewEvent, PeakFunctionDeregisterEvent,
                          PeakFunctionRegisterEvent, PeakTypeChangeEvent,
                          PeakTypeEvent, PeakTypeRegisterEvent,
                          PreferenceEvent, PresetDeregisterEvent, PresetEvent,
                          PresetRegisterEvent, PresetSelectEvent, ProjectEvent,
                          ProjectLoadEvent, ProjectMemoChangeEvent,
                          ProjectNewEvent, ProjectOpenEvent, ProjectSaveEvent,
                          RecipeSelectEvent, SpectrumFunctionDeregisterEvent,
                          SpectrumFunctionListSelectEvent,
                          SpectrumFunctionRegisterEvent, TableSizeChangeEvent,
                          wxEVT_COLOR_REGISTER, wxEVT_COLOR_SELECT,
                          wxEVT_COLORMAP_CHANGE, wxEVT_DATA_CONTENTS_CHANGE,
                          wxEVT_DATA_SELECTION_CHANGE,
                          wxEVT_DECODE_FUNCTION_DEREGISTER,
                          wxEVT_DECODE_FUNCTION_REGISTER,
                          wxEVT_DECODE_FUNCTION_SELECT, wxEVT_DIRECTION_CHANGE,
                          wxEVT_ENCODE_FUNCTION_DEREGISTER,
                          wxEVT_ENCODE_FUNCTION_REGISTER,
                          wxEVT_ENCODE_FUNCTION_SELECT, wxEVT_LAYOUT_CHANGE,
                          wxEVT_LAYOUT_REGISTER,
                          wxEVT_MAPPING_FUNCTION_DEREGISTER,
                          wxEVT_MAPPING_FUNCTION_REGISTER,
                          wxEVT_MAPPING_FUNCTION_SELECT, wxEVT_PANEL_REGISTER,
                          wxEVT_PANEL_SELECTION_CHANGE, wxEVT_PANEL_VIEW,
                          wxEVT_PEAK_FUNCTION_DEREGISTER,
                          wxEVT_PEAK_FUNCTION_REGISTER, wxEVT_PEAK_TYPE_CHANGE,
                          wxEVT_PEAK_TYPE_REGISTER, wxEVT_PRESET_DEREGISTER,
                          wxEVT_PRESET_REGISTER, wxEVT_PRESET_SELECT,
                          wxEVT_PROJECT_EXIT, wxEVT_PROJECT_MEMO_CHANGE,
                          wxEVT_PROJECT_NEW, wxEVT_PROJECT_OPEN,
                          wxEVT_PROJECT_SAVE, wxEVT_RECIPE_SELECT,
                          wxEVT_SPECTRUM_FUNCTION_DEREGISTER,
                          wxEVT_SPECTRUM_FUNCTION_LIST_SELECT,
                          wxEVT_SPECTRUM_FUNCTION_REGISTER,
                          wxEVT_TABLE_SIZE_CHANGE)
from objects import PeakType
from util import GetShowPanelLabel


class EventReceptorBase(iSATexObject):
    """Base class for receiving events
    """

    def OnProjectEvent(self, event: ProjectEvent):
        """Called when an event related to Project is fired. This method is intended to be overridden.

        :type event: ProjectEvent
        """
        pass

    def OnProjectLoad(self, event: ProjectLoadEvent):
        """Called when an event related to project loading is fired. This method is intended to be overridden.

        :type event: ProjectLoadEvent
        """
        pass

    def OnProjectNew(self, event: ProjectNewEvent):
        """Called when an event related to loading a new project is fired. This method is intended to be overridden.

        :type event: ProjectNewEvent
        """
        pass

    def OnProjectOpen(self, event: ProjectOpenEvent):
        """Called when an event related to loading an existing project is fired. This method is intended to be overridden.

        :type event: ProjectOpenEvent
        """
        pass

    def OnProjectSave(self, event: ProjectSaveEvent):
        """Called when an event related to saving a project is fired. This method is intended to be overridden.

        :type event: ProjectSaveEvent
        """
        pass

    def OnProjectMemoChange(self, event: ProjectMemoChangeEvent):
        """Called when an event related to a change in a project memo is fired. This method is intended to be overridden.

        :type event: ProjectMemoChangeEvent
        """
        pass

    def _OnProjectExit(self, event):
        """FURUTE WORK. Called when an event related to project exit is fired. This method is intended to be overridden.
        """
        pass

    def OnDataEvent(self, event: DataEvent):
        """Called when an event related to data is fired.

        :type event: DataEvent
        """
        pass

    def OnDataContentsChange(self, event: DataContentsChangeEvent):
        """Called when an event related to a change in the contents of the data is fired. This method is intended to be overridden.

        :type event: DataContentsChangeEvent
        """
        pass

    def OnDataSelectionChange(self, event: DataSelectionChangeEvent):
        """Called when an event related to a change in data selection is fired. This method is intended to be overridden.

        :type event: DataSelectionChangeEvent
        """
        pass

    def OnFunctionEvent(self, event: FunctionEvent):
        """Called when an event related to the function fires. This method is intended to be overridden.

        :type event: FunctionEvent
        """
        pass

    def OnEncodeFunctionSelect(self, event: EncodeFunctionSelectEvent):
        """Called when an event related to the selection of an encoding function is fired. This method is intended to be overridden.

        :type event: EncodeFunctionSelectEvent
        """
        pass

    def OnDecodeFunctionSelect(self, event: DecodeFunctionSelectEvent):
        """Called when an event related to the selection of the decode function is fired. This method is intended to be overridden.

        :type event: DecodeFunctionSelectEvent
        """
        pass

    def OnSpectrumFunctionListSelect(self, event: SpectrumFunctionListSelectEvent):
        """Called when an event related to the selection of a spectral function fires. This method is intended to be overridden.

        :type event: SpectrumFunctionListSelectEvent
        """
        pass

    def OnMappingFunctionSelect(self, event: MappingFunctionSelectEvent):
        """Called when an event related to the selection of a mapping function fires. This method is intended to be overridden.

        :type event: MappingFunctionSelectEvent
        """
        pass

    def OnFunctionRegisterEvent(self, event: FunctionRegisterEvent):
        """Called when an event related to the registration of a function fires. This method is intended to be overridden.

        :type event: FunctionRegisterEvent
        """
        pass

    def OnEncodeFunctionRegister(self, event: EncodeFunctionRegisterEvent):
        """Called when an event related to the registration of an encoding function is fired. This method is intended to be overridden.

        :param event: [description]
        :type event: [type]
        """
        pass

    def OnEncodeFunctionDeregister(self, event: EncodeFunctionDeregisterEvent):
        """Called when an event related to deregistering an encoding function is fired. This method is intended to be overridden.

        :type event: EncodeFunctionDeregisterEvent
        """
        pass

    def OnDecodeFunctionRegister(self, event: DecodeFunctionRegisterEvent):
        """Called when an event related to the registration of the decode function is fired. This method is intended to be overridden.

        :type event: DecodeFunctionRegisterEvent
        """
        pass

    def OnDecodeFunctionDeregister(self, event: DecodeFunctionDeregisterEvent):
        """Called when an event related to deregistering an decoding function is fired. This method is intended to be overridden.

        :type event: EncodeFunctionDeregisterEvent
        """
        pass

    def OnSpectrumFunctionRegister(self, event: SpectrumFunctionRegisterEvent):
        """Called when an event related to the registration of the spectral function is fired. This method is intended to be overridden.

        :type event: SpectrumFunctionRegisterEvent
        """
        pass

    def OnSpectrumFunctionDeregister(self, event: SpectrumFunctionDeregisterEvent):
        """Called when an event related to deregistering a spectral function is fired. This method is intended to be overridden.

        :type event: SpectrumFunctionDeregisterEvent
        """
        pass

    def OnPeakFunctionRegister(self, event: PeakFunctionRegisterEvent):
        """Called when an event related to the registration of the peak function is fired. This method is intended to be overridden.

        :type event: PeakFunctionRegisterEvent
        """
        pass

    def OnPeakFunctionDeregister(self, event: PeakFunctionDeregisterEvent):
        """Called when an event related to deregistering a peak function is fired. This method is intended to be overridden.

        :type event: PeakFunctionDeregisterEvent
        """
        pass

    def OnMappingFunctionRegister(self, event: MappingFunctionRegisterEvent):
        """Called when an event related to the registration of the mapping function is fired. This method is intended to be overridden.

        :type event: MappingFunctionRegisterEvent
        """
        pass

    def OnMappingFunctionDeregister(self, event: MappingFunctionDeregisterEvent):
        """Called when an event related to deregistering a mapping function is fired. This method is intended to be overridden.

        :type event: MappingFunctionDeregisterEvent
        """
        pass

    def OnRecipeSelect(self, event: RecipeSelectEvent):
        """Called when an event related to the selection of a recipe is fired. This method is intended to be overridden.

        :type event: RecipeSelectEvent
        """
        pass

    def OnPresetEvent(self, event: PresetEvent):
        """Called when an event related to a preset is fired. This method is intended to be overridden.

        :type event: PresetEvent
        """
        pass

    def OnPresetRegister(self, event: PresetRegisterEvent):
        """Called when an event related to preset registration is fired. This method is intended to be overridden.

        :type event: PresetRegisterEvent
        """
        pass

    def OnPresetDeregister(self, event: PresetDeregisterEvent):
        """Called when an event related to deregistering presets is fired. This method is intended to be overridden.

        :type event: PresetDeregisterEvent
        """
        pass

    def OnPresetSelect(self, event: PresetSelectEvent):
        """Called when an event related to preset selection is fired. This method is intended to be overridden.

        :type event: PresetSelectEvent
        """
        pass

    def OnEncodeEvent(self, event: EncodeEvent):
        """Called when an event related to encoding is fired. Note that it is not an encoding function. This method is intended to be overridden.

        :type event: EncodeEvent
        """
        pass

    def OnDecodeEvent(self, event: DecodeEvent):
        """Called when an event related to decoding is fired. Note that it is not an decoding function. This method is intended to be overridden.

        :type event: DecodeEvent
        """
        pass

    def OnMappingEvent(self, event: MappingEvent):
        """Called when an event related to mapping is fired. Note that it is not an mapping function. This method is intended to be overridden.

        :type event: MappingEvent
        """
        pass

    def OnTableSizeChange(self, event: TableSizeChangeEvent):
        """Called when an event related to a change in the mapping table size is fired. This method is intended to be overridden.

        :type event: TableSizeChangeEvent
        """
        pass

    def OnDirectionChange(self, event: DirectionChangeEvent):
        """Called when an event related to a change in mapping direction is fired. This method is intended to be overridden.

        :type event: DirectionChangeEvent
        """
        pass

    def OnColormapChange(self, event: ColormapChangeEvent):
        """Called when an event related to a change in the mapping's color map is fired. This method is intended to be overridden.

        :type event: ColormapChangeEvent
        """
        pass

    def OnPeakTypeEvent(self, event: PeakTypeEvent):
        """Called when an event related to the type of peak is fired. This method is intended to be overridden.

        :type event: PeakTypeEvent
        """
        pass

    def OnPeakTypeRegisterEvent(self, event: PeakTypeRegisterEvent):
        """Called when an event related to the registration of a peak type fires. This method is intended to be overridden.

        :type event: PeakTypeRegisterEvent
        """
        pass

    def OnPeakTypeChange(self, event: PeakTypeChangeEvent):
        """Called when an event related to a change in peak type fires. This method is intended to be overridden.

        :type event: PeakTypeChangeEvent
        """
        pass

    def OnPanelEvent(self, event: PanelEvent):
        """Called when an event related to the panel fires. This method is intended to be overridden.

        :type event: PanelEvent
        """
        pass

    def OnPanelSelectionChange(self, event: PanelSelectionChangeEvent):
        """Called when an event related to panel selection is fired. This method is intended to be overridden.

        :type event: PanelSelectionChangeEvent
        """
        pass

    def OnPanelView(self, event: PanelViewEvent):
        """Called when an event related to the display of the panel is fired. This method is intended to be overridden.

        :type event: PanelViewEvent
        """
        pass

    def OnShow(self):
        """Called when the panel is displayed. This method is intended to be overridden.
        """
        pass

    def OnHide(self):
        """Called when the panel is hidden. This method is intended to be overridden.
        """
        pass

    def OnPanelRegister(self, event: PanelRegisterEvent):
        """Called when an event related to the registration of a panel is fired. This method is intended to be overridden.

        :type event: PanelRegisterEvent
        """
        pass

    def OnLayoutEvent(self, event: LayoutEvent):
        """Called when an event related to the layout is fired. This method is intended to be overridden.

        :type event: LayoutEvent
        """
        pass

    def OnLayoutChange(self, event: LayoutChangeEvent):
        """Called when an event related to a layout change is fired. This method is intended to be overridden.

        :type event: LayoutChangeEvent
        """
        pass

    def OnLayoutRegister(self, event: LayoutRegisterEvent):
        """Called when an event related to registering a layout is fired. This method is intended to be overridden.

        :type event: LayoutRegisterEvent
        """
        pass

    def OnPreferenceEvent(self, event: PreferenceEvent):
        """Called when an event related to the preferences is fired. This method is intended to be overridden.

        :type event: PreferenceEvent
        """
        pass

    def OnColorEvent(self, event: ColorEvent):
        """Called when a color-related event fires. This method is intended to be overridden.

        :type event: ColorEvent
        """
        pass

    def OnColorRegister(self, event: ColorRegisterEvent):
        """Called when an event related to color registration is fired. This method is intended to be overridden.

        :type event: ColorRegisterEvent
        """
        pass

    def OnColorSelect(self, event: ColorSelectionEvent):
        """Called when an event related to color selection is fired. This method is intended to be overridden.

        :type event: ColorSelectionEvent
        """
        pass

    def OnLaunch(self):
        """Called when the iSATex is launched. This method is intended to be overridden.
        """
        pass

    def OnExitEvent(self):
        """Called when the iSATex is exited. This method is intended to be overridden.
        """
        pass

    def __OnProjectEvent(self, event):
        event_type = event.GetEventType()
        if isinstance(event, ProjectLoadEvent):
            self.__OnProjectLoadEvent(event)
        elif event_type == wxEVT_PROJECT_SAVE:
            self.OnProjectSave(event)
        elif event_type == wxEVT_PROJECT_MEMO_CHANGE:
            self.OnProjectMemoChange(event)
        elif event_type == wxEVT_PROJECT_EXIT:
            self._OnProjectExit(event)

        self.OnProjectEvent(event)

    def __OnProjectLoadEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_PROJECT_NEW:
            self.OnProjectNew(event)
        elif event_type == wxEVT_PROJECT_OPEN:
            self.OnProjectOpen(event)

        self.OnProjectLoad(event)

    def __OnDataEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_DATA_CONTENTS_CHANGE:
            self.OnDataContentsChange(event)
        elif event_type == wxEVT_DATA_SELECTION_CHANGE:
            self.OnDataSelectionChange(event)

        self.OnDataEvent(event)

    def __OnFunctionEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_ENCODE_FUNCTION_SELECT:
            self.OnEncodeFunctionSelect(event)
        elif event_type == wxEVT_DECODE_FUNCTION_SELECT:
            self.OnDecodeFunctionSelect(event)
        elif event_type == wxEVT_SPECTRUM_FUNCTION_LIST_SELECT:
            self.OnSpectrumFunctionListSelect(event)
        elif event_type == wxEVT_MAPPING_FUNCTION_SELECT:
            self.OnMappingFunctionSelect(event)
        elif event_type == wxEVT_RECIPE_SELECT:
            self.OnRecipeSelect(event)
        elif isinstance(event, FunctionRegisterEvent):
            self.__OnFunctionRegisterEvent(event)

        elif isinstance(event, PresetEvent):
            self.__OnPresetEvent(event)

        self.OnFunctionEvent(event)

    def __OnFunctionRegisterEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_ENCODE_FUNCTION_REGISTER:
            self.OnEncodeFunctionRegister(event)
        elif event_type == wxEVT_ENCODE_FUNCTION_DEREGISTER:
            self.OnEncodeFunctionDeregister(event)
        elif event_type == wxEVT_DECODE_FUNCTION_REGISTER:
            self.OnDecodeFunctionRegister(event)
        elif event_type == wxEVT_DECODE_FUNCTION_DEREGISTER:
            self.OnDecodeFunctionDeregister(event)
        elif event_type == wxEVT_SPECTRUM_FUNCTION_REGISTER:
            self.OnSpectrumFunctionRegister(event)
        elif event_type == wxEVT_SPECTRUM_FUNCTION_DEREGISTER:
            self.OnSpectrumFunctionDeregister(event)
        elif event_type == wxEVT_PEAK_FUNCTION_REGISTER:
            self.OnPeakFunctionRegister(event)
        elif event_type == wxEVT_PEAK_FUNCTION_DEREGISTER:
            self.OnPeakFunctionDeregister(event)
        elif event_type == wxEVT_MAPPING_FUNCTION_REGISTER:
            self.OnMappingFunctionRegister(event)
        elif event_type == wxEVT_MAPPING_FUNCTION_DEREGISTER:
            self.OnMappingFunctionDeregister(event)

        self.OnFunctionRegisterEvent(event)

    def __OnMappingEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_TABLE_SIZE_CHANGE:
            self.OnTableSizeChange(event)

        elif event_type == wxEVT_DIRECTION_CHANGE:
            self.OnDirectionChange(event)

        elif event_type == wxEVT_COLORMAP_CHANGE:
            self.OnColormapChange(event)

        self.OnMappingEvent(event)

    def __OnPresetEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_PRESET_REGISTER:
            self.OnPresetRegister(event)
        elif event_type == wxEVT_PRESET_DEREGISTER:
            self.OnPresetDeregister(event)
        elif event_type == wxEVT_PRESET_SELECT:
            self.OnPresetSelect(event)

        self.OnPresetEvent(event)

    def __OnPeakTypeEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_PEAK_TYPE_REGISTER:
            self.OnPeakTypeRegisterEvent(event)
        elif event_type == wxEVT_PEAK_TYPE_CHANGE:
            self.OnPeakTypeChange(event)

        self.OnPeakTypeEvent(event)

    def __OnPanelEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_PANEL_SELECTION_CHANGE:
            self.OnPanelSelectionChange(event)
        elif event_type == wxEVT_PANEL_VIEW:
            if self in event.GetShowPanelList():
                self.OnShow()
            elif self in event.GetHidePanelList():
                self.OnHide()

            self.OnPanelView(event)

        elif event_type == wxEVT_PANEL_REGISTER:
            self.OnPanelRegister(event)

        elif isinstance(event, LayoutEvent):
            self.__OnLayoutEvent(event)

        self.OnPanelEvent(event)

    def __OnLayoutEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_LAYOUT_CHANGE:
            self.OnLayoutChange(event)
        elif event_type == wxEVT_LAYOUT_REGISTER:
            self.OnLayoutRegister(event)

        self.OnLayoutEvent(event)

    def __OnColorEvent(self, event):
        event_type = event.GetEventType()
        if event_type == wxEVT_COLOR_REGISTER:
            self.OnColorRegister(event)
        elif event_type == wxEVT_COLOR_SELECT:
            self.OnColorSelect(event)

        self.OnColorEvent(event)

    def OnEvent(self, event: PyCommandEvent):
        """Called when an event is fired.

        :type event: PyCommandEvent
        """
        if event.GetId() == self.GetId():
            return

        if isinstance(event, ProjectEvent):
            self.__OnProjectEvent(event)

        elif isinstance(event, DataEvent):
            self.__OnDataEvent(event)

        elif isinstance(event, FunctionEvent):
            self.__OnFunctionEvent(event)

        elif isinstance(event, EncodeEvent):

            self.OnEncodeEvent(event)

        elif isinstance(event, DecodeEvent):

            self.OnDecodeEvent(event)

        elif isinstance(event, MappingEvent):

            self.__OnMappingEvent(event)

        elif isinstance(event, PeakTypeEvent):
            self.__OnPeakTypeEvent(event)

        elif isinstance(event, PanelEvent):
            self.__OnPanelEvent(event)

        elif isinstance(event, PreferenceEvent):
            self.OnPreferenceEvent(event)

        elif isinstance(event, ColorEvent):
            self.__OnColorEvent(event)

        elif isinstance(event, LaunchEvent):
            self.OnLaunch()

        elif isinstance(event, ExitEvent):
            self.OnExitEvent()


class PanelBase(CommunicableObjectBase, SettingStorableObjectBase, EventReceptorBase, Panel):
    """Base class for panel UI used in iSATex
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super(iSATexObject, self).__init__(*args, **kw)

    def NeedDraw(self) -> bool:
        """Return whether it is necessary to draw spectral data, etc. If True, the spectral data will be drawn when the panel gets the focus.

        :rtype: bool
        """
        return False

    def NeedMultiDraw(self) -> Union[bool, float]:
        """Return whether all data should be drawn when multiple data are selected. If the return value is between 0.0 and 1.0, it represents transparency.

        :rtype: Union[bool, float]
        """
        return False

    def NeedBackgroundDraw(self) -> bool:
        """Returns whether the background needs to be drawn or not.

        :rtype: bool
        """
        return True

    def NeedPeaksDraw(self) -> bool:
        """Returns whether the peak needs to be drawn or not.

        :rtype: bool
        """
        return False


class CustomMenuItemBase(EventReceptorBase, MenuItem):
    """Base class for customizable menu items. Please refer to wxPython (https://docs.wxpython.org/wx.MenuItem.html?highlight=menuitem#wx.MenuItem) for details.
    """

    def __init__(self, text=EmptyString, helpString=EmptyString, kind=ITEM_NORMAL):
        """Default constructor

        :param text: Text to be displayed. If you want to set up hotkeys, refer to wxPython (https://docs.wxpython.org/wx.AcceleratorEntry.html#wx.AcceleratorEntry.FromString), defaults to EmptyString
        :type text: str, optional
        :param helpString: Text that pops when the mouse hover, defaults to EmptyString
        :type helpString: str, optional
        :param kind: Kind of menu, defaults to ITEM_NORMAL
        :type kind: int, optional
        """
        id = NewIdRef()
        super().__init__(id=id, text=text, helpString=helpString, kind=kind)

    @abstractmethod
    def Function(self):
        """Function called when a menu item is selected.

        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()


class CustomNormalMenuItemBase(CommunicableObjectBase, SettingStorableObjectBase, CustomMenuItemBase):
    """Wrapper for the CustomMenuItemBase. Normal menu.
    """

    def __init__(self, text=EmptyString, helpString=EmptyString):
        """Default constructor

        :param text: Text to be displayed. If you want to set up hotkeys, refer to wxPython (https://docs.wxpython.org/wx.AcceleratorEntry.html#wx.AcceleratorEntry.FromString), defaults to EmptyString
        :type text: str, optional
        :param helpString: Text that pops when the mouse hover, defaults to EmptyString
        :type helpString: str, optional
        """
        super().__init__(text=text, helpString=helpString, kind=ITEM_NORMAL)


class CustomRadioMenuItemBase(CommunicableObjectBase, SettingStorableObjectBase, CustomMenuItemBase):
    """Wrapper for the CustomMenuItemBase. Radio menu.
    """

    def __init__(self, text=EmptyString, helpString=EmptyString):
        """Default constructor

        :param text: Text to be displayed. If you want to set up hotkeys, refer to wxPython (https://docs.wxpython.org/wx.AcceleratorEntry.html#wx.AcceleratorEntry.FromString), defaults to EmptyString
        :type text: str, optional
        :param helpString: Text that pops when the mouse hover, defaults to EmptyString
        :type helpString: str, optional
        """
        super().__init__(text=text, helpString=helpString, kind=ITEM_RADIO)


class CustomCheckMenuItemBase(CommunicableObjectBase, SettingStorableObjectBase, CustomMenuItemBase):
    """Wrapper for the CustomMenuItemBase. Checkbox menu.
    """

    def __init__(self, text=EmptyString, helpString=EmptyString):
        """Default constructor

        :param text: Text to be displayed. If you want to set up hotkeys, refer to wxPython (https://docs.wxpython.org/wx.AcceleratorEntry.html#wx.AcceleratorEntry.FromString), defaults to EmptyString
        :type text: str, optional
        :param helpString: Text that pops when the mouse hover, defaults to EmptyString
        :type helpString: str, optional
        """
        super().__init__(text=text, helpString=helpString, kind=ITEM_CHECK)


class ShowPanelMenuItem(CustomMenuItemBase):
    """Checkbox menu for panel display.
    """
    _mgr = None

    def __init__(self, panel: PanelBase, helpString=EmptyString):
        """Defalt constructor

        :param panel: Panel to manage
        :type panel: PanelBase
        :param helpString: Text that pops when the mouse hover, defaults to EmptyString
        :type helpString: str, optional
        """
        if not isinstance(panel, PanelBase):
            raise TypeError()

        text = GetShowPanelLabel(panel)
        super().__init__(text=text, helpString=helpString, kind=ITEM_CHECK)

        self.__panel = panel
        self.Check(panel.Shown)

    def GetPanel(self) -> PanelBase:
        """Get panel manegered

        :rtype: PanelBase
        """
        return self.__panel

    def Function(self):
        """Switches the display of the panel you are managing.
        """
        ShowPanelMenuItem._mgr.ShowPane(self.__panel, self.IsChecked())


class PeakMenuItem(CustomMenuItemBase):
    """Radio menu for selecting the type of peak.
    """
    _mgr = None

    def __init__(self, peak_type: PeakType):
        """Default constructor

        :param peak_type: Type of peak to be managed.
        :type peak_type: PeakType
        """
        text = peak_type.GetName()
        helpString = peak_type.GetHelpText()
        super().__init__(text=text, helpString=helpString, kind=ITEM_RADIO)

        self.__peak_type = peak_type

    def Function(self):
        """Select type of peak.
        """
        PeakMenuItem._mgr.SelectPeakType(self.__peak_type)

    def OnLaunch(self):
        """Make it deselectable.
        """
        self.Enable(False)

    def OnProjectLoad(self, event):
        self.Enable()


class LayoutMenuItem(CustomMenuItemBase):
    """Menu for selecting the layout.
    """
    _mgr = None

    def __init__(self, name: str):
        """Default constructor

        :param name: name of layout
        :type name: str
        """
        super().__init__(text=name, helpString='', kind=ITEM_NORMAL)

    def Function(self):
        name = self.GetItemLabel()
        LayoutMenuItem._mgr.LoadLayout(name)


__all__ = [
    'EventReceptorBase',
    'PanelBase',
    'CustomMenuItemBase',
    'CustomNormalMenuItemBase',
    'CustomRadioMenuItemBase',
    'CustomCheckMenuItemBase',
    'ShowPanelMenuItem',
    'PeakMenuItem',
    'LayoutMenuItem',
]
