from math import floor, isclose
from os.path import basename

from keyboard import is_pressed
from matplotlib.backends.backend_wxagg import (FigureCanvasWxAgg,
                                               NavigationToolbar2WxAgg)
from matplotlib.cm import get_cmap
from matplotlib.collections import QuadMesh
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.text import Annotation
from numpy import array
from wx import (ALIGN_CENTER, ALIGN_CENTER_VERTICAL, ALL, ART_CLOSE,
                ART_GO_BACK, ART_GO_DOWN, ART_GO_FORWARD, ART_GO_UP,
                BORDER_NONE, BOTTOM, CB_READONLY, CB_SORT, CENTER, EVT_BUTTON,
                EVT_CHAR_HOOK, EVT_CLOSE, EVT_COMBOBOX,
                EVT_COMMAND_SCROLL_CHANGED, EVT_LEFT_UP, EXPAND, HORIZONTAL,
                ID_CANCEL, LEFT, RIGHT, TE_MULTILINE, TE_READONLY, TOP,
                VERTICAL, ArtProvider, BitmapButton, BoxSizer, Button,
                NullColour, Panel, SizerFlags, Slider)
from wx.lib.agw.ultimatelistctrl import (EVT_LIST_ITEM_DESELECTED,
                                         EVT_LIST_ITEM_SELECTED,
                                         ULC_BORDER_SELECT, ULC_FORMAT_CENTER,
                                         ULC_HAS_VARIABLE_ROW_HEIGHT,
                                         ULC_HRULES, ULC_NO_FULL_ROW_SELECT,
                                         ULC_REPORT, UltimateListCtrl)
from wx.lib.scrolledpanel import ScrolledPanel

from const import (COLOR_MANAGER, DATA_MANAGER, FUNCTION_MANAGER,
                   MAPPING_MANAGER, PEAK_MANAGER)
from container import PanelBase
from control import (AddButton, ClearButton, ColormapEntry, ExecuteButton,
                     FunctionArgumentEntry, FunctionListEntry, HelpButton,
                     LabeledValidateEntry, NormalComboBox, NormalEntry,
                     NormalLine, NormalText, RegisterButton, RegisterDialog,
                     SetButton)
from objects import (ChoiceContainer, DataContainer, IntContainer, Preset,
                     Recipe, SpectrumFunctionContainerBase)


# TODO: Focus is not obtained even if the list is selected. So the spectrum may not be drawn.
class DataSelector(PanelBase):
    """Panel for data selection
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__main_selection = None

        self.__list_ctrl = UltimateListCtrl(self, style=0, agwStyle=ULC_HRULES | ULC_REPORT | ULC_BORDER_SELECT |
                                            ULC_NO_FULL_ROW_SELECT | ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.__list_ctrl.Bind(EVT_LIST_ITEM_SELECTED, self.__OnListItemSelected)
        self.__list_ctrl.Bind(EVT_LIST_ITEM_DESELECTED, self.__OnListItemDeselected)
        self.__list_ctrl.Bind(EVT_LEFT_UP, self.__OnListItemLeftClick)
        for n, heading in enumerate(['', 'FILE NAME', 'DATA SIZE']):
            self.__list_ctrl.InsertColumn(n, heading, ULC_FORMAT_CENTER)
        self.__list_ctrl.SetColumnWidth(0, 30)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__list_ctrl, 1, EXPAND | ALL, 10)

        self.Disable()

    def __GetSelection(self):
        selection = []
        n_i = self.__list_ctrl.GetFirstSelected()

        while n_i != -1:
            selection.append(n_i)
            n_i = self.__list_ctrl.GetNextSelected(n_i)

        return selection

    def __OnListItemSelected(self, event):
        if (is_pressed('shift') or is_pressed('ctrl')) and self.__main_selection is not None:
            return

        self.__main_selection = event.Index

    def __OnListItemDeselected(self, event):
        if self.__main_selection == event.Index:
            self.__main_selection = None

    def __OnListItemLeftClick(self, event):
        selection = self.__GetSelection()
        self.Get(DATA_MANAGER).Select(self.__main_selection, selection)
        self.SetFocus()

    def __CreateRow(self, index, data: DataContainer):
        if not isinstance(data, DataContainer):
            raise TypeError()

        path = data.Path
        file_name = basename(path)
        size = data.GetSpectrumSize()

        self.__list_ctrl.InsertStringItem(index, str(index + 1))
        self.__list_ctrl.SetStringItem(index, 1, file_name)
        self.__list_ctrl.SetStringItem(index, 2, str(size))

    def OnProjectLoad(self, event):
        self.__list_ctrl.DeleteAllItems()
        data_list = event.GetDataList()

        if len(data_list) == 0:
            self.Disable()
            return

        for index, data in enumerate(data_list):
            self.__CreateRow(index, data)

        self.Enable()

    def OnDataSelectionChange(self, event):
        self.__main_selection = event.GetMainSelection()
        prev_selection = set(event.GetPreviousSelection())
        selection = set(event.GetSelection())
        for index in event.GetAddedSelection():
            self.__list_ctrl.Select(index)

        for index in event.GetRemoveSelection():
            self.__list_ctrl.Select(index, False)

        # for index in prev_selection:
        #     self.__list_ctrl.SetItemBackgroundColour(index, NullColour)
        #     item = self.__list_ctrl.GetItem(index)
        #     item.SetBackgroundColour(NullColour)

        # color = self.Get(DotChain(COLOR, SELECTION))
        # for index in selection:
        #     self.__list_ctrl.SetItemBackgroundColour(index, color)
        #     item = self.__list_ctrl.GetItem(index)
        #     item.SetBackgroundColour(color)

        # color = self.Get(DotChain(COLOR, MAIN_SELECTION))
        # if (index := self.__main_selection) is not None:
        #     self.__list_ctrl.SetItemBackgroundColour(index, color)

        #     item = self.__list_ctrl.GetItem(index)
        #     item.SetBackgroundColour(color)

    def NeedDraw(self):
        return True

    def NeedPeaksDraw(self):
        return True

    def NeedMultiDraw(self):
        return 0.3


class SpectrumPanel(PanelBase):
    """Panel for spectral display
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)

        self.fig = Figure()
        spec_list = GridSpec(ncols=1, nrows=2, bottom=0.05, top=0.95, hspace=0.3, figure=self.fig, height_ratios=[3, 1])
        self.main_ax = self.fig.add_subplot(spec_list[0])
        self.bg_ax = self.fig.add_subplot(spec_list[1])
        self.bg_ax.sharex(self.main_ax)
        self.bg_ax.tick_params(labelbottom=False, bottom=False)

        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.canvas.MinSize = (100, 100)

        self.nav_toolbar = NavigationToolbar2WxAgg(self.canvas)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.canvas, 1, EXPAND)
        self.Sizer.Add(self.nav_toolbar, 0, EXPAND)

    def Clear(self):
        """Clearing the display
        """
        self.main_ax.clear()
        self.bg_ax.clear()

    def _IsActive(self, name):
        return self.nav_toolbar.GetToolState(self.nav_toolbar.wx_ids[name])

    def IsNormal(self) -> bool:
        """Return whether the state is operable or not

        :rtype: bool
        """
        return all(not self._IsActive(name) for name in self.nav_toolbar.wx_ids.keys())


class PeakSelector(PanelBase):
    """Panel to select the peak
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__peak_type_combo = NormalComboBox(self, style=CB_READONLY | CB_SORT)
        self.__peak_type_combo.Bind(EVT_COMBOBOX, lambda _: self.__PeakTypeSelected())

        self.__fig = Figure()
        self.__ax = self.__fig.add_subplot(111)
        self.__ax.set_frame_on(False)
        self.__ax.set_position([0, 0, 1, 1])
        self.canvas = FigureCanvasWxAgg(self, -1, self.__fig)
        self.canvas.MinSize = (50, 30)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__peak_type_combo, 0, ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)
        self.Sizer.Add(self.canvas, 1, EXPAND)

    def __SetPeakType(self, peak_type):
        self.__peak_type_combo.SetValue(peak_type.GetName())
        self.__SetTex(peak_type.GetTex())
        self.__prev_peak_type = peak_type

    def __SetTex(self, tex):
        self.__ax.clear()
        text = Annotation(tex, (0, 0), horizontalalignment='center', verticalalignment='center')
        self.__ax.add_artist(text)
        self.__ax.autoscale()
        self.canvas.draw()

    def __PeakTypeSelected(self):
        selected_peak_type_name = self.__peak_type_combo.GetValue()
        peak_type = self.Get(PEAK_MANAGER).GetPeakType(selected_peak_type_name)
        self.Get(PEAK_MANAGER).SelectPeakType(peak_type)

    def OnProjectOpen(self, event):
        peak_type = event.GetPeakType()
        self.__SetPeakType(peak_type)

    def OnPeakTypeRegisterEvent(self, event):
        peak_type_name_list = event.GetPeakTypeNames()
        self.__peak_type_combo.SetItems(peak_type_name_list)

    def OnPeakTypeChange(self, event):
        peak_type = event.GetPeakType()
        self.__SetPeakType(peak_type)


class FunctionSelector(PanelBase):
    """Panel to select a function
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__contents_panel = ScrolledPanel(self)
        self.__contents_panel.Sizer = BoxSizer(VERTICAL)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__contents_panel, 1, EXPAND)

    def OnSpectrumFunctionRegister(self, event):
        self.__ClearContents()

        for function in event.GetFunctionList():
            contents = FunctionSelector.Contents(function, parent=self.__contents_panel)
            self.__contents_panel.Sizer.Add(contents, 0, EXPAND | LEFT | RIGHT, 20)

        self.__contents_panel.SetupScrolling()
        self.Layout()

    def OnSpectrumFunctionDeregister(self, event):
        contents_dict = {contents.GetFunction().__class__.__name__: contents for contents in self.__GetContentsList()}
        for function in event.GetFunctionList():
            contents = contents_dict[function.__class__.__name__]
            contents.Hide()
            self.__contents_panel.Detach(contents)
            contents.Destroy()

        self.__contents_panel.SetupScrolling()
        self.Layout()

    def __ClearContents(self):
        for contents in self.__GetContentsList():
            contents.Hide()
            self.__contents_panel.Detach(contents)
            contents.Destroy()

    def __GetContentsList(self):
        return [item_sizer.Window for item_sizer in self.__contents_panel.Sizer]

    class Contents(Panel):
        def __init__(self, func_container, *args, **kw):
            super().__init__(*args, **kw)
            self.__func_container = func_container

            name = func_container.__class__.__name__
            doc = func_container.__doc__
            func_name_lbl = NormalText(self, label=name)
            help_btn = HelpButton(doc, name, parent=self)
            add_btn = AddButton(self)
            add_btn.Bind(EVT_BUTTON, lambda _: self.__OnAddBtnPushed())
            contents_sizer = BoxSizer(HORIZONTAL)
            contents_sizer.Add(func_name_lbl, 0, ALIGN_CENTER)
            contents_sizer.AddStretchSpacer()
            contents_sizer.Add(help_btn, 0, ALIGN_CENTER | ALL, 8)
            contents_sizer.Add(add_btn, 0, ALIGN_CENTER)

            self.Sizer = BoxSizer(VERTICAL)
            self.Sizer.Add(contents_sizer, 0, EXPAND)
            self.Sizer.AddSpacer(10)
            self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)

        def GetFunction(self):
            return self.__func_container

        def __OnAddBtnPushed(self):
            self.GrandParent.Get(FUNCTION_MANAGER).SelectSpectrumFunctionList(self.__func_container)


class PresetSelector(PanelBase):
    """Panel for select preset
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__contents_panel = ScrolledPanel(self)
        self.__contents_panel.Sizer = BoxSizer(VERTICAL)
        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__contents_panel, 1, EXPAND)

    def __AddContentsList(self, preset_list):
        self.__ClearContents()

        for preset in preset_list:
            contents = PresetSelector.Contents(preset, parent=self.__contents_panel)
            contents.Bind(EVT_CLOSE, self.__OnContentsClose)
            self.__contents_panel.Sizer.Add(contents, 0, EXPAND | ALL, 10)

        self.__contents_panel.SetupScrolling(scrollToTop=False, scrollIntoView=True)
        self.Layout()

    def __OnContentsClose(self, event):
        event.Skip()
        contents = event.GetEventObject()
        contents.Hide()
        self.__contents_panel.Sizer.Detach(contents)
        self.__contents_panel.SetupScrolling()
        self.Layout()

        preset = contents.GetPreset()
        self.Get(FUNCTION_MANAGER).RegisterPreset(preset, False)

    def __ClearContents(self):
        for contents in self.__GetContentsList():
            contents.Hide()
            self.__contents_panel.Sizer.Detach(contents)
            contents.Destroy()

    def __GetContentsList(self):
        return [item_sizer.Window for item_sizer in self.__contents_panel.Sizer]

    def OnPresetRegister(self, event):
        preset_list = event.GetPresetList()
        self.__AddContentsList(preset_list)

    class Contents(Panel):
        def __init__(self, preset: Preset, *args, **kw):
            super().__init__(*args, **kw)
            if not isinstance(preset, Preset):
                raise TypeError()

            self.__preset = preset
            name = self.__preset.GetName()
            name_lbl = NormalText(self, label=name)

            add_btn = AddButton(self)
            add_btn.Bind(EVT_BUTTON, lambda _: self.__SendSpectrumFunctionSelectedEvent())
            close_bitmap = ArtProvider().GetBitmap(ART_CLOSE)
            delete_btn = BitmapButton(self, bitmap=close_bitmap, size=(31, 31))
            delete_btn.Bind(EVT_BUTTON, lambda _: self.Close())
            header_h_sizer = BoxSizer(HORIZONTAL)
            header_h_sizer.Add(name_lbl, 0, ALIGN_CENTER_VERTICAL)
            header_h_sizer.AddStretchSpacer()
            header_h_sizer.Add(delete_btn)
            header_h_sizer.AddSpacer(10)
            header_h_sizer.Add(add_btn)

            contents_v_sizer = BoxSizer(VERTICAL)
            for func_container in preset:
                contents_v_sizer.Add(NormalText(self, label=str(func_container)))

            contents_h_sizer = BoxSizer(HORIZONTAL)
            contents_h_sizer.Add(NormalLine(self, size=(2, -1)), 0, EXPAND | LEFT | RIGHT, 10)
            contents_h_sizer.Add(contents_v_sizer, 0, EXPAND)

            self.Sizer = BoxSizer(VERTICAL)
            self.Sizer.Add(header_h_sizer, 0, EXPAND)
            self.Sizer.Add(contents_h_sizer, 0, EXPAND)
            self.Sizer.AddSpacer(10)
            self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND | LEFT | RIGHT, 30)

        def GetPreset(self):
            return self.__preset

        def __SendSpectrumFunctionSelectedEvent(self):
            self.GrandParent.Get(FUNCTION_MANAGER).SelectSpectrumPreset(self.__preset)


class RecipePanel(PanelBase):
    """Panel for editing the order of recipes and their arguments.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__set_btn = SetButton(parent=self)
        self.__set_btn.Disable()
        self.__set_btn.Bind(EVT_BUTTON, lambda _: self.__OnSetBtnPushed())
        self.__clear_btn = ClearButton(parent=self)
        self.__clear_btn.Disable()
        self.__clear_btn.Bind(EVT_BUTTON, lambda _: self.__OnClearBtnPushed())
        self.__register_btn = RegisterButton(parent=self)
        self.__register_btn.Disable()
        self.__register_btn.Bind(EVT_BUTTON, lambda _: self.__OnRegisterBtnPushed())
        ctrl_h_sizer = BoxSizer(HORIZONTAL)
        ctrl_h_sizer.Add(self.__set_btn, 0, LEFT, 10)
        ctrl_h_sizer.AddSpacer(10)
        ctrl_h_sizer.Add(self.__clear_btn, 0)
        ctrl_h_sizer.AddStretchSpacer()
        ctrl_h_sizer.Add(self.__register_btn, 0, RIGHT, 10)

        self.__contents_panel = ScrolledPanel(self)
        self.__contents_panel.Sizer = BoxSizer(VERTICAL)
        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(ctrl_h_sizer, 0, EXPAND | ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND | LEFT | RIGHT, 20)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__contents_panel, 1, EXPAND)

        self.Bind(EVT_CHAR_HOOK, self.__OnCharHook)

    def __GetRecipe(self):
        return Recipe([contents.GetFunctionContainer() for contents in self.__GetContentsList()])

    def OnSpectrumFunctionListSelect(self, event):
        function_list = event.GetFunctionList()

        for function in function_list:
            contents = RecipePanel.Contents(function, parent=self.__contents_panel)
            contents.Bind(EVT_CLOSE, self.__OnContentsClose)
            self.__contents_panel.Sizer.Add(contents, 0, EXPAND | LEFT | BOTTOM, 10)

        self.__contents_panel.SetupScrolling()
        self.Layout()

        self.__UpdateCtrl()

    def OnPeakTypeChange(self, event):
        for contents in self.__GetContentsList():
            contents.UpdateContents()

        self.Layout()

    def ChangeOrder(self, index: int, after: bool = True):
        """Change the order of the functions

        :param index: Index to specify the function to move from
        :type index: int
        :param after: Whether to move to later order., defaults to True
        :type after: bool, optional
        """
        contents_list = self.__GetContentsList()
        if isinstance(index, RecipePanel.Contents):
            index = contents_list.index(index)

        if not isinstance(index, int):
            raise TypeError()

        t_i = min(index + 1, len(contents_list) - 1) if after else max(index - 1, 0)

        contents = contents_list[index]
        self.__contents_panel.Sizer.Detach(contents)
        self.__contents_panel.Sizer.Insert(t_i, contents, SizerFlags().Border(BOTTOM, 10).Border(LEFT, 10).Expand())

        self.Layout()

    def __HasValidRecipe(self):
        return all([contents.HasValidArguments() for contents in self.__GetContentsList()])

    def __UpdateCtrl(self):
        if self.__HasValidRecipe() and self.__contents_panel.Sizer.ItemCount != 0:
            self.__set_btn.Enable()
            self.__clear_btn.Enable()
            self.__register_btn.Enable()
        else:
            self.__set_btn.Disable()
            self.__clear_btn.Disable()
            self.__register_btn.Disable()

    def __GetContentsList(self):
        return [sizer_item.Window for sizer_item in self.__contents_panel.Sizer]

    def __OnCharHook(self, event):
        event.Skip()

        self.__UpdateCtrl()

    def __OnContentsClose(self, event):
        event.Skip()
        contents = event.GetEventObject()
        contents.Hide()
        self.__contents_panel.Sizer.Detach(contents)
        self.__contents_panel.SetupScrolling()
        self.Layout()

    def __OnSetBtnPushed(self):
        recipe = self.__GetRecipe()
        self.Get(DATA_MANAGER).ApplyRecipe(recipe)

    def __OnClearBtnPushed(self):
        contents_list = self.__GetContentsList()
        for contents in contents_list:
            contents.Hide()
            self.__contents_panel.Sizer.Detach(contents)

        self.__contents_panel.SetupScrolling()
        self.Layout()

        self.__UpdateCtrl()

    def __OnRegisterBtnPushed(self):
        preset_name_list = self.Get(FUNCTION_MANAGER).GetPresetNames()
        with RegisterDialog(preset_name_list, self) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            name = dialog.GetName()

        recipe = self.__GetRecipe()
        preset = Preset(name, recipe)
        self.Get(FUNCTION_MANAGER).RegisterPreset(preset)

    class Contents(Panel):
        def __init__(self, func_container: SpectrumFunctionContainerBase, *args, **kw):
            super().__init__(*args, **kw)
            self.__func_name_lbl = NormalText(self, label=func_container.__class__.__name__)
            close_bitmap = ArtProvider().GetBitmap(ART_CLOSE)
            delete_btn = BitmapButton(self, bitmap=close_bitmap, size=(22, 22))
            delete_btn.Bind(EVT_BUTTON, lambda _: self.Close())
            header_h_sizer = BoxSizer(HORIZONTAL)
            header_h_sizer.Add(self.__func_name_lbl)
            header_h_sizer.AddStretchSpacer()
            header_h_sizer.Add(delete_btn, 0, ALIGN_CENTER | LEFT, 10)

            self.__func_arg_ety = FunctionArgumentEntry(self, func_container)

            contents_v_sizer = BoxSizer(VERTICAL)
            contents_v_sizer.Add(header_h_sizer, 0, EXPAND)
            contents_v_sizer.Add(self.__func_arg_ety, 0, EXPAND)

            art_go_up = ArtProvider.GetBitmap(ART_GO_UP)
            up_button = BitmapButton(self, bitmap=art_go_up, size=(25, 35))
            up_button.Bind(EVT_BUTTON, lambda _: self.GrandParent.ChangeOrder(self, False))

            art_go_down = ArtProvider.GetBitmap(ART_GO_DOWN)
            down_button = BitmapButton(self, bitmap=art_go_down, size=(25, 35))
            down_button.Bind(EVT_BUTTON, lambda _: self.GrandParent.ChangeOrder(self, True))

            arrow_v_sizer = BoxSizer(VERTICAL)
            arrow_v_sizer.Add(up_button, 0)
            arrow_v_sizer.AddStretchSpacer()
            arrow_v_sizer.Add(down_button, 0)

            h_sizer = BoxSizer(HORIZONTAL)
            h_sizer.Add(contents_v_sizer, 1, EXPAND)
            h_sizer.Add(NormalLine(self, size=(2, -1)), 0, EXPAND)
            h_sizer.Add(arrow_v_sizer, 0, EXPAND)

            self.Sizer = BoxSizer(VERTICAL)
            self.Sizer.Add(h_sizer, 0, EXPAND)
            self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND, 10)

        def GetFunctionContainer(self):
            return self.__func_arg_ety.GetFunction()

        def HasValidArguments(self):
            return self.__func_arg_ety.HasValidArguments()

        def UpdateContents(self):
            self.__func_arg_ety.UpdateContents()
            self.Layout()

        def __OnCharHook(self, event):
            event.Skip()
            color = NullColour if self.HasValidArguments() else self.Get(COLOR_MANAGER).GetErrorColor()
            self.__func_name_lbl.SetBackgroundColour(color)


class ExecutePanel(PanelBase):
    """Panel for function execution
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__index = -1

        self.__execute_btn = ExecuteButton(self)
        self.__execute_btn.Bind(EVT_BUTTON, lambda _: self.__OnExecuteBtnPushed())
        self.__execute_btn.Disable()
        self.__contents_panel = ScrolledPanel(self)
        self.__contents_panel.Sizer = BoxSizer(VERTICAL)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__execute_btn, 0, CENTER | ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.Add(self.__contents_panel, 1, EXPAND)

    def __SetData(self, data: DataContainer):
        if not isinstance(data, DataContainer):
            raise TypeError()

        for func_container, success in zip(data.Recipe, data.SuccessList):
            contents = ExecutePanel.Contents(func_container, success, parent=self.__contents_panel)
            self.__contents_panel.Sizer.Add(contents, 0, EXPAND | ALL, 10)

        self.__contents_panel.SetupScrolling()
        self.Layout()

        self.__execute_btn.Enable()

    def __HasData(self) -> bool:
        return self.__index != -1

    def __OnExecuteBtnPushed(self):
        selection = self.Get(DATA_MANAGER).GetSelection()
        self.Get(DATA_MANAGER).ExecuteSpectrumFunction(selection)

    def __ClearContents(self):
        for contents in self.__GetContentsList():
            contents.Hide()
            self.__contents_panel.Sizer.Detach(contents)
            contents.Destroy()

    def __GetContentsList(self):
        return [sizer_item.Window for sizer_item in self.__contents_panel.Sizer]

    def OnDataSelectionChange(self, event):
        if event.GetId() == self.GetId():
            return
        self.__ClearContents()

        main_selection = event.GetMainSelection()
        if main_selection is None:
            self.__index = -1
            return

        self.__index = main_selection

        data = self.Get(DATA_MANAGER).GetData(self.__index)
        self.__SetData(data)

    def OnDataContentsChange(self, event):
        if not self.__HasData() or event.GetId() == self.GetId():
            return

        if event.IsRecipeChanged(self.__index):
            self.__ClearContents()
            data = self.Get(DATA_MANAGER).GetData(self.__index)
            self.__SetData(data)

    class Contents(Panel):
        def __init__(self, function_container, success, *args, **kw):
            super().__init__(*args, **kw)
            self.__state_beacon = Button(self, size=(14, 14))
            self.__state_beacon.Disable()
            self.Sizer = BoxSizer(HORIZONTAL)
            self.Sizer.Add(NormalText(self, label=str(function_container)))
            self.Sizer.AddSpacer(10)
            self.Sizer.AddStretchSpacer()
            self.Sizer.Add(self.__state_beacon)
            self.Sizer.AddSpacer(10)

            self.SetSuccess(success)

        def SetSuccess(self, success):
            if success is None:
                color = NullColour
            elif success:
                color = self.GrandParent.Get(COLOR_MANAGER).GetSuccessColor()
            else:
                color = self.GrandParent.Get(COLOR_MANAGER).GetErrorColor()
            self.__state_beacon.SetBackgroundColour(color)


class RecoveryPanel(PanelBase):
    """Panel for recovering data from history.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        go_back_bitmap = ArtProvider().GetBitmap(ART_GO_BACK)
        self.__backward_btn = BitmapButton(self, bitmap=go_back_bitmap, size=(30, 30))
        self.__backward_btn.Disable()
        self.__backward_btn.SetMaxSize((50, -1))
        self.__backward_btn.Bind(EVT_BUTTON, lambda _: [contents.TimeShift(1) for contents in self.__GetContentsList()])

        go_forward_bitmap = ArtProvider().GetBitmap(ART_GO_FORWARD)
        self.__forward_btn = BitmapButton(self, bitmap=go_forward_bitmap, size=(30, 30))
        self.__forward_btn.Disable()
        self.__forward_btn.SetMaxSize((50, -1))
        self.__forward_btn.Bind(EVT_BUTTON, lambda _: [contents.TimeShift(-1) for contents in self.__GetContentsList()])

        restore_btn_panel = Panel(self)
        self.__restore_btn = Button(restore_btn_panel, label='RESTORE')
        self.__restore_btn.Disable()
        self.__restore_btn.Bind(EVT_BUTTON, lambda _: self.__OnRestoreBtnPushed())
        restore_sizer = BoxSizer(VERTICAL)
        restore_sizer.Add(self.__restore_btn, 0, CENTER)
        restore_btn_panel.SetSizer(restore_sizer)

        ctrl_h_sizer = BoxSizer(HORIZONTAL)
        ctrl_h_sizer.AddStretchSpacer(2)
        ctrl_h_sizer.Add(self.__backward_btn, 2, EXPAND)
        ctrl_h_sizer.AddStretchSpacer(1)
        ctrl_h_sizer.Add(self.__forward_btn, 2, EXPAND)
        ctrl_h_sizer.Add(restore_btn_panel, 2, CENTER)

        self.__contents_panel = ScrolledPanel(self)
        self.__contents_v_sizer = BoxSizer(VERTICAL)
        self.__contents_panel.SetSizer(self.__contents_v_sizer)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(ctrl_h_sizer, 0, EXPAND | ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)
        self.Sizer.Add(self.__contents_panel, 1, EXPAND)

    def OnSliderShifted(self, index):
        pass

    def __AddContents(self, size):
        contents_list = self.__GetContentsList()
        crt_size = len(contents_list)
        if size == crt_size:
            return

        for index in range(crt_size, size):
            contents = RecoveryPanel.Contents(index, self.__contents_panel)
            self.__contents_v_sizer.Add(contents, 0, EXPAND | ALL, 10)

        for index in reversed(range(size, crt_size)):
            contents = contents_list[index]
            contents.Hide()
            self.__contents_panel.Sizer.Detach(contents)
            contents.Destroy()

        self.__contents_panel.SetupScrolling()
        self.Layout()

    def __OnRestoreBtnPushed(self):
        contents_list = self.__GetContentsList()

        selection = self.Get(DATA_MANAGER).GetSelection()
        if len(selection) == 0:
            selection = list(range(len(contents_list)))

        data_list = self.Get(DATA_MANAGER).GetDataList(selection)

        for index, data in zip(selection, data_list):
            contents = contents_list[index]
            delta = contents.GetDelta()
            data.Restore(delta)

        self.Get(DATA_MANAGER).SetDataList(selection, data_list)

    def __GetContentsList(self):
        return [item_sizer.Window for item_sizer in self.__contents_v_sizer]

    def OnProjectLoad(self, event):
        if event.GetId() == self.GetId():
            return

        for contents in self.__GetContentsList():
            contents.Hide()
            self.__contents_panel.Sizer.Detach(contents)
            contents.Destroy()

        data_list = event.GetDataList()
        self.__AddContents(len(data_list))

        self.__restore_btn.Enable()
        self.__backward_btn.Enable()
        self.__forward_btn.Enable()

    def OnDataContentsChange(self, event):
        if event.GetId() == self.GetId():
            return

        contents_list = self.__GetContentsList()
        index_list = event.GetIndexList()
        for index in index_list:
            contents = contents_list[index]
            contents.Update()

        self.Layout()

    class Contents(Panel):
        def __init__(self, index, *args, **kw):
            super().__init__(*args, **kw)
            self.__index = index

            file_name = basename(self.__GetData().Path)
            file_name_lbl = NormalText(self, label=file_name, style=TE_READONLY | BORDER_NONE)
            self.__msg_ety = NormalEntry(self, style=TE_MULTILINE | TE_READONLY)
            self.__slider = Slider(self)
            self.__slider.Bind(EVT_COMMAND_SCROLL_CHANGED, lambda _: self.__OnSliderShifted())
            self.__slider_tick_h_sizer = BoxSizer(HORIZONTAL)

            self.Sizer = BoxSizer(VERTICAL)
            self.Sizer.Add(file_name_lbl, 0, EXPAND | TOP | RIGHT | LEFT, 10)
            self.Sizer.Add(self.__msg_ety, 0, EXPAND | ALL, 10)
            self.Sizer.Add(self.__slider, 0, EXPAND | LEFT | RIGHT, 10)
            self.Sizer.Add(self.__slider_tick_h_sizer, 0, EXPAND | LEFT | RIGHT, 20)

            self.Update()

        def GetDelta(self):
            return self.__slider.GetValue()

        def TimeShift(self, delta):
            buffer_size = self.__GetBufferSize()
            if buffer_size <= 1:
                return

            prev_pos = self.__slider.GetValue()
            next_pos = min(max(prev_pos - delta, 0), buffer_size - 1)
            self.__slider.SetValue(next_pos)

            self.__UpdateMsg()

        def Update(self):
            self.__UpdateSlider()
            self.__UpdateMsg()

        def __UpdateSlider(self):
            buffer_size = self.__GetBufferSize()
            if buffer_size <= 1:
                self.__slider.Max = 1
                self.__slider.Value = 0
                self.__slider.Disable()

                self.__slider_tick_h_sizer.ShowItems(False)
                self.__slider_tick_h_sizer.Clear()

            else:
                self.__slider.Max = buffer_size - 1
                self.__slider.Value = 0
                self.__slider.Enable()

                self.__slider_tick_h_sizer.ShowItems(False)
                self.__slider_tick_h_sizer.Clear()

                self.__slider_tick_h_sizer.Add(NormalText(self, label='+'))
                for _ in range(buffer_size - 1):
                    self.__slider_tick_h_sizer.AddStretchSpacer()
                    self.__slider_tick_h_sizer.Add(NormalText(self, label='+'))

                self.__slider_tick_h_sizer.ShowItems(True)
                self.Layout()

        def __UpdateMsg(self):
            if self.__GetBufferSize() == 0:
                return

            _, _, _, msg = self.__GetSelectedBuffer()
            self.__msg_ety.SetValue(msg)

        def __OnSliderShifted(self):
            self.__UpdateMsg()
            self.GrandParent.OnSliderShifted(self.__index)

        def __GetData(self):
            return self.GrandParent.Get(DATA_MANAGER).GetData(self.__index)

        def __GetSelectedBuffer(self):
            return self.__GetData().GetBufferData(self.__slider.GetValue())

        def __GetBufferSize(self):
            return self.__GetData().BufferSize


class MappingViewer(PanelBase):
    """Panel for displaying mappings.
    """
    LEFT = 1
    RIGHT = 3

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)
        self.__prev_idx = -1

        self.__s_pos = (-1, -1)
        self.__e_pos = (-1, -1)

        self.__direction = None

        self.__x_ety = LabeledValidateEntry('X', IntContainer(20, 1), parent=self)
        self.__x_ety.Bind(EVT_CHAR_HOOK, self.__OnTableSizeChanged)
        self.__y_ety = LabeledValidateEntry('Y', IntContainer(20, 1), parent=self)
        self.__y_ety.Bind(EVT_CHAR_HOOK, self.__OnTableSizeChanged)
        ctrl_l_v_sizer = BoxSizer(VERTICAL)
        ctrl_l_v_sizer.Add(self.__x_ety, 0, EXPAND)
        ctrl_l_v_sizer.Add(self.__y_ety, 0, EXPAND)

        choices = self.Get(MAPPING_MANAGER).GetDirectionList()
        self.__dir_ety = LabeledValidateEntry('Direction', ChoiceContainer('r2d', choices), parent=self)
        self.Bind(EVT_COMBOBOX, self.__OnDirectionSelected)
        self.__cmap_ety = ColormapEntry(self)
        self.__cmap_ety.Bind(EVT_COMBOBOX, self.__OnColormapSelected)
        ctrl_r_v_sizer = BoxSizer(VERTICAL)
        ctrl_r_v_sizer.Add(self.__dir_ety, 0, EXPAND)
        ctrl_r_v_sizer.Add(self.__cmap_ety, 0, EXPAND)

        table_h_sizer = BoxSizer(HORIZONTAL)
        table_h_sizer.Add(ctrl_l_v_sizer)
        table_h_sizer.AddSpacer(10)
        table_h_sizer.AddStretchSpacer()
        table_h_sizer.Add(ctrl_r_v_sizer)

        self.__func_list_ety = FunctionListEntry(parent=self)
        self.__func_list_ety.Bind(EVT_CHAR_HOOK, self.__OnCharHook)
        self.__exe_btn = ExecuteButton(parent=self.__func_list_ety)
        self.__exe_btn.Bind(EVT_BUTTON, lambda _: self.__OnExecuteBtnPushed())
        self.__func_list_ety.header_sizer.AddSpacer(10)
        self.__func_list_ety.header_sizer.AddStretchSpacer()
        self.__func_list_ety.header_sizer.Add(self.__exe_btn)
        self.__func_list_ety.header_sizer.AddSpacer(10)

        self.__fig = Figure()
        self.__ax = self.__fig.add_subplot(111)
        self.__ax.set_axis_off()
        self.__ax.set_aspect('equal')
        self.__ax.set_position([0, 0.05, 1, 1])

        self.__canvas = FigureCanvasWxAgg(self, -1, self.__fig)
        self.__canvas.MinSize = (100, 100)
        self.__canvas.mpl_connect('motion_notify_event', self.__OnMotion)
        self.__canvas.mpl_connect('button_press_event', self.__OnBtnPress)
        self.__canvas.mpl_connect('button_release_event', self.__OnBtnRelease)
        self.__canvas.Disable()

        self.__rect_selector = Rectangle(self.__s_pos, 0, 0, alpha=0.3)
        self.__ax.add_patch(self.__rect_selector)

        self.__nav_toolbar = NavigationToolbar2WxAgg(self.__canvas)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(table_h_sizer, 0, EXPAND | ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)
        self.Sizer.Add(self.__func_list_ety, 0, EXPAND | ALL, 10)
        self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)
        self.Sizer.Add(self.__canvas, 1, EXPAND)
        self.Sizer.Add(self.__nav_toolbar, 0, EXPAND)

    def __SetTitle(self, x, y, idx):
        self.__ax.set_title(f'(x, y, i)=({x + 1}, {y + 1}, {idx + 1})', {'fontsize': 11, 'color': 'gray'}, y=-0.15, loc='right')

    def __GetTableSize(self):
        return self.__x_ety.GetValue(), self.__y_ety.GetValue()

    def __GetDirection(self):
        return self.__dir_ety.GetValue()

    def __GetColormap(self):
        return self.__cmap_ety.GetColormap()

    def __Select(self, index):
        c_i = self.__ConvertOuter(index)
        previous_selection = (self.get_selected_index(), self.get_selected_index_list())

        self.__prev_idx = c_i
        self.__spot_selected_pos_set = {c_i}
        self.__range_selected_pos_set = set()
        self.__update_all_colors()

        current_selection = (self.get_selected_index(), self.get_selected_index_list())
        self.on_data_selection_changed(current_selection, previous_selection)

    def OnMappingFunctionRegister(self, event):
        func_list = event.GetFunctionList()
        self.__func_list_ety.RegisterFunctionList(func_list)

    def OnMappingFunctionSelect(self, event):
        func = event.GetFunction()
        self.__func_list_ety.Select(func)
        self.Layout()

    def __OnTableSizeChanged(self, event):
        event.Skip()
        if not (self.__x_ety.HasValidValue() and self.__y_ety.HasValidValue()):
            return

        x, y = self.__GetTableSize()
        if x * y == self.Get(DATA_MANAGER).GetDataSize():
            self.__exe_btn.Enable()
        else:
            self.__exe_btn.Disable()

        self.Get(MAPPING_MANAGER).SetTableSize(x, y)

    def __OnDirectionSelected(self, event):
        event.Skip()
        direction = self.__GetDirection()
        self.Get(MAPPING_MANAGER).SelectDirection(direction)

    def __OnColormapSelected(self, event):
        event.Skip()
        cmap = self.__cmap_ety.GetColormap()
        self.Get(MAPPING_MANAGER).SelectColormap(cmap)

    def __GetIndex(self, x, y):
        c, r = self.__GetTableSize()
        y = r - y - 1
        return self.__ConvertOuter(y * c + x)

    def __OnMotion(self, event):
        if not self.__IsNormal() or None in (data := [event.xdata, event.ydata]):
            return

        c, r = self.__GetTableSize()
        x, y = floor(data[0]), floor(data[1])
        if not (0 <= x < c and 0 <= y < r):
            return

        idx = self.__GetIndex(x, y)
        if idx == self.__prev_idx:
            return

        self.__SetTitle(x, y, idx)
        self.__canvas.draw()

        self.__prev_idx = idx

        if self.__IsPressed():
            self.__OnDrag(event)

    def __OnBtnPress(self, event):
        if not self.__IsNormal():
            return

        if event.button == MappingViewer.LEFT:
            if None in (data := [event.xdata, event.ydata]):
                return

            c, r = self.__GetTableSize()
            x, y = floor(data[0]), floor(data[1])
            if not (0 <= x < c and 0 <= y < r):
                return

            idx = self.__GetIndex(x, y)
            self.__SetTitle(x, y, idx)

            self.__rect_selector.set_bounds(x, y, 1, 1)
            self.__canvas.draw()

            self.__s_pos = (x, y)
            self.__prev_idx = idx

    def __OnDrag(self, event):
        if not self.__IsPressed() or None in (data := [event.xdata, event.ydata]):
            return

        c, r = self.__GetTableSize()
        x, y = floor(data[0]), floor(data[1])
        if not (0 <= x < c and 0 <= y < r):
            return

        l, b = min(self.__s_pos[0], x), min(self.__s_pos[1], y)
        w, h = abs(self.__s_pos[0] - x) + 1, abs(self.__s_pos[1] - y) + 1
        self.__rect_selector.set_bounds(l, b, w, h)
        self.__canvas.draw()

    def __OnBtnRelease(self, event):
        if not self.__IsNormal():
            return

        if event.button == MappingViewer.LEFT:
            if None in (data := [event.xdata, event.ydata]):
                return

            c, r = self.__GetTableSize()
            x, y = max(0, min(floor(data[0]), c)), max(0, min(floor(data[1]), r))
            e_i = self.__ConvertOuter(self.__GetIndex(x, y), 'r2d')
            s_i = self.__ConvertOuter(self.__GetIndex(self.__s_pos[0], self.__s_pos[1]), 'r2d')
            selection = self.__GetRectSelection(s_i, e_i)

            self.Get(DATA_MANAGER).Select(selection=selection)

            self.__s_pos = (-1, -1)
            self.__prev_idx = -1
            self.__rect_selector.set_bounds(-1, -1, 0, 0)

    def __GetRectSelection(self, r2d_i, r2d_j):
        selection = set()
        c, r = self.__GetTableSize()
        xs, ys = (r2d_i % c, r2d_j % c), (r2d_i // c, r2d_j // c)
        l, r, u, b = min(xs), max(xs), min(ys), max(ys)
        for y in range(u, b + 1):
            for x in range(l, r + 1):
                selection.add(y * c + x)

        return selection

    def __ConvertOuter(self, r2d_i, direction=None):
        if direction is None:
            direction = self.__GetDirection()

        c, r = self.__GetTableSize()
        y, x = divmod(r2d_i, c)

        if direction in ['l2d', 'd2l', 'l2u', 'u2l']:
            x = c - 1 - x

        if direction in ['r2u', 'u2r', 'l2u', 'u2l']:
            y = r - 1 - y

        if direction in ['d2r', 'd2l', 'u2r', 'u2l']:
            y, x = x, y
            r, c = c, r

        return int(y * c + x)

    def __ConvertInner(self, index, direction=None):
        if direction is None:
            direction = self.__GetDirection()

        c, r = self.__GetTableSize()
        if direction in ['r2d', 'l2d', 'r2u', 'l2u']:
            y, x = divmod(index, c)
        else:
            x, y = divmod(index, r)
        if direction in ['l2d', 'd2l', 'l2u', 'u2l']:
            x = c - 1 - x
        if direction in ['r2u', 'u2r', 'l2u', 'u2l']:
            y = r - 1 - y

        return int(y * c + x)

    def __ConvertDataList(self):
        data_size = self.Get(DATA_MANAGER).GetDataSize()
        index_list = [self.__ConvertInner(i) for i in range(data_size)]
        return self.Get(DATA_MANAGER).GetDataList(index_list)

    def __CreateQuadMesh(self, w, h, value_list, cmap):
        coordinate = array([[[x, y] for x in range(w + 1)] for y in range(h + 1)])
        if isinstance(cmap, str):
            cmap = get_cmap(cmap)

        vmin, vmax = min(value_list), max(value_list)
        if isclose(vmin, vmax):
            color_list = [cmap(0)]
        else:
            color_list = [cmap.badcolor if v is None else cmap(int(cmap.N * (v - vmin) / (vmax - vmin))) for v in value_list]
        return QuadMesh(w, h, coordinate, facecolors=color_list, linewidths=0, antialiased=False)

    def __OnExecuteBtnPushed(self):
        func = self.__func_list_ety.GetSelectedFunction()
        x, y = self.__GetTableSize()
        data_list = self.__ConvertDataList()
        value_list = func.Execution(data_list)
        cmap = self.__GetColormap()
        quadmesh = self.__CreateQuadMesh(x, y, value_list, cmap)

        self.__ax.set_xlim(0, x)
        self.__ax.set_ylim(0, y)
        self.__ax.add_collection(quadmesh)
        self.__canvas.draw()

    def __OnCharHook(self, event):
        event.Skip()
        self.__UpdateCtrl()

    def __IsPressed(self):
        return self.__s_pos != (-1, -1)

    def __IsActive(self, name):
        return self.__nav_toolbar.GetToolState(self.__nav_toolbar.wx_ids[name])

    def __IsNormal(self):
        return all(not self.__IsActive(x) for x in self.__nav_toolbar.wx_ids.keys())

    def __UpdateCtrl(self):
        x, y = self.__GetTableSize()
        if x * y == self.Get(DATA_MANAGER).GetDataSize():
            self.__exe_btn.Enable()
            self.__canvas.Enable()
        else:
            self.__exe_btn.Disable()
            self.__canvas.Disable()

    def OnProjectLoad(self, event):
        self.__UpdateCtrl()

    def OnTableSizeChange(self, event):
        x, y = event.GetTableSize()
        prev_x, prev_y = self.__GetTableSize()
        if prev_x == x and prev_y == y:
            return

        self.__ax.set_xlim(0, x)
        self.__ax.set_ylim(0, y)

        self.__x_ety.SetValue(x)
        self.__y_ety.SetValue(y)

        if x * y == self.Get(DATA_MANAGER).GetDataSize():
            self.__exe_btn.Enable()
        else:
            self.__exe_btn.Disable()

    def OnDirectionChange(self, event):
        direction = event.GetDirection()
        self.__dir_ety.Value = direction

    def OnColormapChange(self, event):
        cmap = event.GetColormap()
        self.__cmap_ety.SetColormap(cmap)

    def NeedDraw(self):
        return True

    def NeedMultiDraw(self):
        return True

    def NeedPeaksDraw(self):
        return True

# class ColormapSelector(PanelBase):
#     def __init__(self, *args, **kw):
#         super().__init__(*args, **kw)
#         self.__colorbar = Colorbar(parent=self)

#         self.__contents_panel = ScrolledPanel(self)
#         self.__contents_panel.Sizer = BoxSizer(VERTICAL)

#         self.__add_btn = AddButton(self)
#         self.__add_btn.Bind(EVT_BUTTON, lambda _: self.__OnAddBtnPushed())

#         self.Sizer = BoxSizer(VERTICAL)
#         self.Sizer.Add(self.__colorbar, 0, EXPAND | ALL, 10)
#         self.Sizer.Add(NormalLine(self, size=(-1, 2)), 0, EXPAND)
#         self.Sizer.Add(self.__contents_panel, 1, EXPAND | ALL, 10)
#         self.Sizer.Add(self.__add_btn, 0, CENTER | ALL, 10)

#         self.__contents_panel.SetupScrolling()

#     def __GetCmap(self):
#         colors, positions = self.__GetColors(), self.__GetPositions()
#         return self.__CreateCmap(colors, positions)

#     def __CreateCmap(self, colors, positions):
#         if len(colors) != len(positions):
#             return

#         color_dict = {'red': [], 'green': [], 'blue': [], 'alpha': []}
#         if 0 not in positions:
#             color_dict['red'].append([0, 1, 1])
#             color_dict['blue'].append([0, 1, 1])
#             color_dict['green'].append([0, 1, 1])
#             color_dict['alpha'].append([0, 0, 0])

#         for color, pos in zip(colors, positions):
#             red, green, blue, alpha = color
#             if pos not in [value[0] for value in color_dict['red']]:
#                 color_dict['red'].append([pos, red, red])
#                 color_dict['blue'].append([pos, blue, blue])
#                 color_dict['green'].append([pos, green, green])
#                 color_dict['alpha'].append([pos, alpha, alpha])

#         if 1 not in positions:
#             color_dict['red'].append([1, 1, 1])
#             color_dict['blue'].append([1, 1, 1])
#             color_dict['green'].append([1, 1, 1])
#             color_dict['alpha'].append([1, 0, 0])

#         return LinearSegmentedColormap('custom', color_dict)

#     def __GetColors(self):
#         return [contents.GetColor() for contents in self.__GetContentsList()]

#     def __GetPositions(self):
#         return [contents.GetPosition() for contents in self.__GetContentsList()]

#     def __GetContentsList(self):
#         return [item_sizer.Window for item_sizer in self.__contents_panel.Sizer]

#     def __ClearContentsList(self):
#         for contents in self.__GetContentsList():
#             contents.Hide()
#             self.__contents_panel.Sizer.Detach(contents)
#             contents.Destroy()

#     def __OnAddBtnPushed(self):
#         contents = ColormapSelector.Contents('#FFF', parent=self.__contents_panel)
#         contents.Bind(EVT_CLOSE, self.__OnContentsClose)

#         self.__contents_panel.Sizer.Add(contents, 0, EXPAND)
#         self.__contents_panel.SetupScrolling(scrollToTop=False)
#         self.__contents_panel.ScrollChildIntoView(contents)
#         self.Layout()

#         self._OnCmapChanged()

#     def __OnContentsClose(self, event):
#         event.Skip()
#         contents = event.GetEventObject()
#         contents.Hide()
#         self.__contents_panel.Sizer.Detach(contents)
#         contents.Destroy()

#         self.__contents_panel.SetupScrolling(scrollToTop=False)
#         self.Layout()

#         self._OnCmapChanged()

#     def _OnCmapChanged(self):
#         cmap = self.__GetCmap()
#         self.__colorbar.SetCmap(cmap)

#         self.Get(COLOR_MANAGER).SetColormap(cmap)

#     def OnColormapChange(self, event):
#         cmap = event.GetColormap()
#         self.__colorbar.SetCmap(cmap)

#         self.__ClearContentsList()
#         colors, positions = cmap.GetColorsPositions()
#         for color, position in zip(colors, positions):
#             contents = ColormapSelector.Contents(color, parent=self.__contents_panel)
#             contents.SetPosition(position)
#             contents.Bind(EVT_CLOSE, self.__OnContentsClose)

#             self.__contents_panel.Sizer.Add(contents, 0, EXPAND)

#         self.__contents_panel.SetupScrolling(scrollToTop=False)
#         self.Layout()

#     class Contents(ColorSliderCtrl):
#         def OnColorChange(self):
#             self.GrandParent._OnCmapChanged()


__all__ = [
    'DataSelector',
    'SpectrumPanel',
    'PeakSelector',
    'FunctionSelector',
    'PresetSelector',
    'RecipePanel',
    'ExecutePanel',
    'RecoveryPanel',
    'MappingViewer',
]
