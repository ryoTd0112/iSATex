
from copy import deepcopy
from datetime import datetime
from os.path import basename, join
from typing import Any, List, Optional, Tuple, Union

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.cm import cmap_d
from matplotlib.collections import PolyCollection
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from numpy import arange
from wx import (ALIGN_CENTER_VERTICAL, ALL, ART_CLOSE, ART_INFORMATION,
                ART_PLUS, BORDER_NONE, CB_READONLY, CENTER,
                DEFAULT_DIALOG_STYLE, EVT_BUTTON, EVT_CHAR_HOOK, EVT_CLOSE,
                EVT_COMBOBOX, EVT_KILL_FOCUS, EVT_SCROLL, EXPAND,
                FD_FILE_MUST_EXIST, FD_MULTIPLE, FD_OPEN, HORIZONTAL,
                ID_CANCEL, ID_CLOSE, ID_EXECUTE, ID_OK, LEFT, RESIZE_BORDER,
                RIGHT, TE_MULTILINE, TE_READONLY, VERTICAL,
                WXK_CATEGORY_NAVIGATION, ArtProvider, BitmapButton, BoxSizer,
                Button, Colour, ColourData, ComboBox, Dialog, DirDialog,
                FileDialog, LogError, NullColour, Panel, Slider,
                StaticBitmap, StaticText, TextCtrl, Window)
from wx.adv import DatePickerCtrl
from wx.lib.agw.cubecolourdialog import Colour as cube_color
from wx.lib.agw.cubecolourdialog import CubeColourDialog
from wx.lib.agw.ultimatelistctrl import (ULC_BORDER_SELECT, ULC_FORMAT_CENTER,
                                         ULC_HAS_VARIABLE_ROW_HEIGHT,
                                         ULC_HRULES, ULC_NO_FULL_ROW_SELECT,
                                         ULC_REPORT, UltimateListCtrl)
from wx.lib.dialogs import ScrolledMessageDialog
from wx.lib.scrolledpanel import ScrolledPanel

from const import (DEFAULT_COLORMAP, ID_ADD, ID_BROWSE, ID_CLEAR, ID_DONT_SAVE,
                   ID_NORMAL_BUTTON, ID_NORMAL_COMBOBOX, ID_NORMAL_LINE,
                   ID_NORMAL_TEXT, ID_PREVIEW, ID_SAVE, ID_SET,
                   NEW_MENU_ITEM_HELP)
from core import ChameleonWidgetBase
from objects import (ArgumentContainerBase, ChoiceContainer, DataContainer,
                     DecodeFunctionContainerBase, EncodeFunctionContainerBase,
                     FunctionContainerBase, IntContainer,
                     IterableArgumentContainerBase, ListArgumentContainer,
                     Project, Spectrum, StrContainer, TupleArgumentContainer)
from util import GetExtension, GetFileExtention, HasValidElement


class NormalText(StaticText, ChameleonWidgetBase):
    """
    Text widget used in normal contexts.
    # FURUTE WORK: It will be used by the application to recognize it.

    """

    def __init__(self, *args, **kw):
        """
        Default constructor. One of the keywords, id, has been used.
        Please refer to wxPython (https://docs.wxpython.org/wx.StaticText.html?highlight=statictext#wx.StaticText) for details.
        """
        super().__init__(id=ID_NORMAL_TEXT, *args, **kw)


class NormalLine(Panel, ChameleonWidgetBase):
    """Line widget used in normal contexts.
    """
    color = '#aaaaaa'

    def __init__(self, *args, **kw):
        """Default constructor.  Please refer wxPython (https://docs.wxpython.org/wx.Panel.html?highlight=panel#wx.Panel) for details.
        """
        super().__init__(style=BORDER_NONE, id=ID_NORMAL_LINE, *args, **kw)
        self.SetBackgroundColour(NormalLine.color)


class NormalEntry(TextCtrl, ChameleonWidgetBase):
    """Entry widget used in normal contexts.
    """

    def __init__(self, *args, **kw):
        """Default constructor.  Please refer wxPython (https://docs.wxpython.org/wx.TextCtrl.html?highlight=textctrl#wx.TextCtrl) for details.
        """
        super().__init__(*args, **kw)


class NormalComboBox(ComboBox, ChameleonWidgetBase):
    """Combobox widget used in normal contexts.
    """

    def __init__(self, parent, *args, **kw):
        """Default constructor.  Please refer wxPython (https://docs.wxpython.org/wx.ComboBox.html?highlight=combobox#wx.ComboBox) for details.
        """
        super().__init__(parent, id=ID_NORMAL_COMBOBOX, *args, **kw)


class NormalButton(Button, ChameleonWidgetBase):
    """Button widget used in normal contexts.
    """

    def __init__(self, *args, **kw):
        """Default constructor. Please refer wxPython (https://docs.wxpython.org/wx.Button.html?highlight=button#wx.Button) for details.
        """
        super().__init__(id=ID_NORMAL_BUTTON, *args, **kw)


class OkButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit ok.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_OK, *args, **kw)


class CancelButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit cancel.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_CANCEL, *args, **kw)


class SetButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit set.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_SET, label='Set', *args, **kw)


class ExecuteButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit execution.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_EXECUTE, label='Execute', *args, **kw)


class RegisterButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit registration.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_EXECUTE, label='Register', *args, **kw)


class BrowseButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit browsing.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_BROWSE, label='Browse', *args, **kw)


class PreviewButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit preview.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_PREVIEW, label='Preview', *args, **kw)


class ClearButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit clear.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_CLEAR, label='Clear', *args, **kw)


class SaveButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit saving.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_SAVE, label='Save', *args, **kw)


class DontSaveButton(Button, ChameleonWidgetBase):
    """Button widget used in contexts that submit don\'t saving.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(id=ID_DONT_SAVE, label='Don\'t save', *args, **kw)


class AddButton(BitmapButton, ChameleonWidgetBase):
    """Bitmap button widget used in contexts that submit addition.
    """

    def __init__(self, parent, *args, **kw):
        """Default constructor
        """
        bitmap = ArtProvider().GetBitmap(ART_PLUS)
        super().__init__(parent, id=ID_ADD, bitmap=bitmap, *args, **kw)


class CloseButton(BitmapButton, ChameleonWidgetBase):
    """Bitmap button widget used in contexts that submit widget close.
    """

    def __init__(self, parent, *args, **kw):
        bitmap = ArtProvider().GetBitmap(ART_CLOSE)
        super().__init__(parent, id=ID_CLOSE, bitmap=bitmap, *args, **kw)


class HelpButton(Button, ChameleonWidgetBase):
    """Bitmap button widget used in contexts that displaying help text.
    """

    def __init__(self, msg: str = None, caption: str = '', size=(31, 31), *args, **kw):
        """Default constructor

        :param msg: Message to be displayed, defaults to None
        :type msg: str, optional
        :param caption: Caption displayed at the top of the window, defaults to ''
        :type caption: str, optional
        :param size: size of button, defaults to (31, 31)
        :type size: tuple, optional
        """
        super().__init__(label='?', size=size, *args, **kw)
        self.__msg = 'Sorry, but there was no help available.' if msg is None else msg
        self.__caption = caption
        self.Bind(EVT_BUTTON, lambda _: self.__OnPushed())

    def GetMessage(self) -> str:
        """Get message.

        :rtype: str
        """
        return self.__msg

    def SetMessage(self, msg: str):
        """Set message.

        :type msg: str
        """
        if not isinstance(msg, str):
            raise TypeError()

        self.__msg = msg

    def GetCaption(self) -> str:
        """Get caption.

        :rtype: str
        """
        return self.__caption

    def SetCaption(self, caption: str):
        """Set caption.

        :type caption: str
        """
        if not isinstance(caption, str):
            raise TypeError()

        self.__caption = caption

    def __OnPushed(self):
        with ScrolledMessageDialog(self, self.__msg, self.__caption) as dialog:
            dialog.ShowModal()
            return


class Colorbar(Panel):
    """Colorbar widget.
    """

    def __init__(self, cmap: Colormap = DEFAULT_COLORMAP, size: Tuple[int, int] = (200, 30), is_horizontal: bool = True, resolution: int = 100, *args, **kw):
        """Default constructor

        :param cmap: colormap, defaults to DEFAULT_COLORMAP
        :type cmap: Colormap, optional
        :param size: size of widget, defaults to (200, 30)
        :type size: Tuple[int, int], optional
        :param is_horizontal: If True, it will be displayed horizontally otherwise,  vertically. defaults to True
        :type is_horizontal: bool, optional
        :param resolution: Color bar resolution, defaults to 100
        :type resolution: int, optional
        """
        super().__init__(*args, **kw)
        x, y = size
        figsize = x / 100, y / 100

        fig = Figure(figsize)
        self.__ax = fig.add_subplot(111)
        self.__ax.axis('off')
        self.__ax.set_position([0, 0, 1, 1])

        self.__canvas = FigureCanvasWxAgg(self, -1, fig)

        self.__colorbar = self.__CreateColorbar(is_horizontal, resolution)
        self.SetColormap(cmap)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__canvas, 1, EXPAND)

    def __CreateColorbar(self, is_horizontal, resolution=100):
        self.__ax.clear()
        if is_horizontal:
            verts = [((x, 0), (x, 100), (x + 1, 100), (x + 1, 0)) for x in range(100)]
            self.__ax.set_ylim([0, 1])
            self.__ax.set_xlim([1, 99])
        else:
            verts = [((0, y), (0, y + 1), (100, y + 1), (100, y)) for y in range(100)]
            self.__ax.set_ylim([0, 100])
            self.__ax.set_xlim([0, 1])
        intensities = arange(100)
        colorbar = PolyCollection(verts)
        colorbar.set_array(intensities)
        self.__ax.add_collection(colorbar)
        self.__canvas.draw()

        return colorbar

    def GetColormap(self) -> Colormap:
        """Get colormap

        :rtype: Colormap
        """
        return self.__colorbar.get_cmap()

    def SetColormap(self, cmap: Union[Colormap, str]):
        """Set colormap

        :type cmap: Colormap
        """
        if not isinstance(cmap, (Colormap, str)):
            raise TypeError()

        self.__colorbar.set_cmap(cmap)
        self.__canvas.draw()


class ColorSliderCtrl(Panel):
    """Widget for color and position.
    """
    _custom_colors = [cube_color(Colour(255, 255, 255, 255)) for _ in range(16)]
    _colour_selection = 15

    def __init__(self, color: Colour, *args, **kw):
        """Default constructor

        :param color: color. Please refer to wxPython (https://docs.wxpython.org/wx.Colour.html?highlight=colour#wx.Colour) for details.
        :type color: Colour
        """
        super().__init__(*args, **kw)
        self.__color_picker = Button(self, size=(30, 30))
        self.__color_picker.SetBackgroundColour(color)
        self.__color_picker.Bind(EVT_BUTTON, lambda _: self.__ShowColorDialog())
        self.__pos_slider = Slider(self)
        self.__pos_slider.Bind(EVT_SCROLL, lambda _: self.OnColorChange())
        self.__close_btn = CloseButton(self, size=(30, 30))
        self.__close_btn.Bind(EVT_BUTTON, lambda _: self.Close())

        h_sizer = BoxSizer(HORIZONTAL)
        h_sizer.Add(self.__color_picker)
        h_sizer.Add(self.__pos_slider, 1)
        h_sizer.Add(self.__close_btn)

        self.SetSizer(h_sizer)

    def GetColor(self) -> Tuple[float, float, float, float]:
        """Gets the color formatted to 0.0 to 1.0 rgba.

        :rtype: Tuple[float, float, float, float]
        """
        color = self.__color_picker.GetBackgroundColour().Get()
        return color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255

    def SetColor(self, color: Colour):
        """Set color. Please refer wxPython (https://docs.wxpython.org/wx.Window.html?highlight=window#wx.Window.SetBackgroundColour) for details.

        :type color: Colour
        """
        color = Colour(color)
        self.__color_picker.SetBackgroundColour(color)

    def GetPosition(self) -> float:
        """Get position of slider.

        :return: The right corresponds to 0.0 and the left to 1.0.
        :rtype: float
        """
        return self.__pos_slider.GetValue() / 100

    def SetPosition(self, position: float):
        """Set position of slider.

        :param position: The right corresponds to 0.0 and the left to 1.0.
        :type position: float
        """
        self.__pos_slider.SetValue(int(position * 100))

    def OnColorChange(self):
        # for override
        pass

    def __ShowColorDialog(self):
        color_data = ColourData()
        color_data.SetColour(self.__color_picker.GetBackgroundColour())
        with CubeColourDialog(self, color_data) as cd:

            for color in ColorSliderCtrl._custom_colors:
                cd.customColours.AddCustom(color)
            cd.customColours.colour_selection = ColorSliderCtrl._colour_selection
            cd.CenterOnScreen()
            cd.ShowModal()

        color = cd.GetRGBAColour()
        self.__color_picker.SetBackgroundColour(color)

        for n, color in enumerate(cd.customColours._customColours):
            ColorSliderCtrl._custom_colors[n] = cube_color(color)
        ColorSliderCtrl._colour_selection = cd.customColours._colourSelection

        self.OnColorChange()


class ColormapEntry(Panel):
    """Entry of colormap
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)

        cmap = kw.get('cmap', DEFAULT_COLORMAP)
        cmap_names = list(cmap_d.keys())
        self.__name_ety = NormalComboBox(self, value=cmap, choices=cmap_names, style=CB_READONLY)
        self.__name_ety.Bind(EVT_COMBOBOX, self.OnColormapSelected)
        size = self.__name_ety.GetSize()
        self.__colorbar = Colorbar(cmap=DEFAULT_COLORMAP, parent=self, size=size)

        self.Sizer = BoxSizer(HORIZONTAL)
        self.Sizer.Add(self.__name_ety)
        self.Sizer.AddSpacer(5)
        self.Sizer.Add(self.__colorbar, 0, EXPAND)

    def GetColormap(self) -> str:
        """Get name of colormap.

        :rtype: str
        """
        return self.__name_ety.GetValue()

    def SetColormap(self, cmap: Union[str, Colormap]):
        """Set colormap.

        :type cmap: Union[str, Colormap]
        """
        if isinstance(cmap, Colormap):
            cmap = cmap.name
        self.__name_ety.SetValue(cmap)
        self.__colorbar.SetColormap(cmap)

    def OnColormapSelected(self, event):
        """Called when Colormap is selected.
        """
        event.Skip()

        cmap = self.__name_ety.GetValue()
        self.__colorbar.SetColormap(cmap)


class ArgumentContainerEntryBase:
    """Base class for displaying ArgumentContainerBase.
    """

    def __init__(self, arg_container: ArgumentContainerBase):
        """Default constructor

        :type arg_container: ArgumentContainerBase
        """
        if not isinstance(arg_container, ArgumentContainerBase):
            raise TypeError()

        self.__arg_container = arg_container

    def GetValue(self) -> Any:
        """Get value

        :rtype: Any
        """
        return self.__arg_container.GetValue()

    def SetValue(self, value):
        """Set the value to "ArgumentContainerBase" class.
        """
        self.__arg_container.SetValue(value)

    def GetDefault(self) -> Any:
        """Get default value

        :rtype: Any
        """
        return self.__arg_container.GetDefault()

    def IsValidValue(self, value) -> bool:
        """Return True, if value is valid.

        :rtype: bool
        """
        return self.__arg_container.IsValidValue(value)

    def HasValidValue(self) -> bool:
        """Return True, if the value entered is a valid value.

        :rtype: bool
        """
        return self.__arg_container.HasValidValue()

    def GetArgumentContainer(self) -> ArgumentContainerBase:
        """Get instance of "ArgumentContainerBase" class managed.

        :rtype: ArgumentContainerBase
        """
        return self.__arg_container

    def SetArgumentContainer(self, arg_container: ArgumentContainerBase):
        """Set instance of "ArgumentContainerBase" class to be managed.

        :type arg_container: ArgumentContainerBase
        """
        if not isinstance(arg_container, ArgumentContainerBase):
            raise TypeError()

        self.__arg_contanier = arg_container


class ValidatableEntry(NormalEntry):
    """Entry with validate.
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        self.Bind(EVT_CHAR_HOOK, self.__OnCharHook)

    def OnEntered(self, value: str):
        """Called when the value has been entered. This method is intended to be overridden.

        :type value: str
        """
        # for override
        pass

    def __OnCharHook(self, event):
        """Calculates the next value from the current value and input and calls OnEntered.

        """
        event.Skip()
        if event.IsKeyInCategory(WXK_CATEGORY_NAVIGATION):
            return

        value = super(ArgumentContainerEntryBase, self).GetValue()
        keycode = event.GetUnicodeKey()
        if keycode == 0:
            return

        # Convert to upper case alphabet keycode.
        if event.shiftDown and 49 <= keycode <= 57:
            keycode -= 16

        # Convert numbers to symbolic keycode. It may not work properly on non-Japanese keyboards.
        if not event.shiftDown and 65 <= keycode <= 90:
            keycode += 32

        selection = self.GetSelection()
        n_value = GetNextStr(value, keycode, selection)

        self.OnEntered(n_value)


class ValidateEntry(ArgumentContainerEntryBase, NormalEntry):
    """Entry for displaying ArgumentContainerBase
    """

    def __init__(self, arg_container: ArgumentContainerBase, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default constructor

        :type arg_container: ArgumentContainerBase
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        super().__init__(arg_container)
        super(ArgumentContainerEntryBase, self).__init__(*args, **kw)
        if not isinstance(arg_container, ArgumentContainerBase):
            raise TypeError()

        self.__success_color = success_color
        self.__error_color = error_color

        if arg_container is not None:
            super(ArgumentContainerEntryBase, self).SetValue(str(arg_container))

        self.UpdateColor()

        self.Bind(EVT_CHAR_HOOK, self.__OnCharHook)
        self.Bind(EVT_KILL_FOCUS, self.__OnKillFocus)

    def SetValue(self, value, display=True):
        """Set value

        :type value: Castable to a str.
        :param display:  Whether display is required or not, defaults to True
        :type display: bool, optional
        """
        value = None if value == '' else value
        super().SetValue(value)
        if display:
            value = '' if value is None else value
            super(ArgumentContainerEntryBase, self).SetValue(str(value))

    def SetArgumentContainer(self, arg_container):
        """Set "ArgumentContainerBase" to be managed

        :param arg_container: [description]
        :type arg_container: [type]
        """
        super().SetArgumentContainer(arg_container)
        self.UpdateColor()

    def UpdateColor(self):
        """Update color
        """
        color = self.__success_color if self.HasValidValue() else self.__error_color

        self.SetBackgroundColour(color)
        self.Refresh()

    def __OnCharHook(self, event):
        event.Skip()
        if event.IsKeyInCategory(WXK_CATEGORY_NAVIGATION):
            return

        value = super(ArgumentContainerEntryBase, self).GetValue()
        keycode = event.GetUnicodeKey()
        if keycode == 0:
            return

        # Convert to upper case alphabet keycode.
        if event.shiftDown and 49 <= keycode <= 57:
            keycode -= 16

        # Convert numbers to symbolic keycode. It may not work properly on non-Japanese keyboards.
        if not event.shiftDown and 65 <= keycode <= 90:
            keycode += 32

        selection = self.GetSelection()
        n_value = GetNextStr(value, keycode, selection)

        self.SetValue(n_value, False)
        self.UpdateColor()

    def __OnKillFocus(self, event):
        """If empty value entered when the focus shifts elsewhere, enter the default value.
        """
        if self.Value == '':
            default = self.GetDefault()
            self.SetValue(default)
            # self.SetValue(str(self.__arg_container))

            self.UpdateColor()

        event.Skip()


class ValidateStrEntry(Panel):
    """Entry for displaying StrContainer
    """

    def __init__(self, str_container: StrContainer, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default constructor

        :type str_container: StrContainer
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(str_container, StrContainer):
            raise TypeError()
        super().__init__(*args, **kw)
        self.__ety = ValidateEntry(str_container, success_color, error_color, parent=self)

        self.Sizer = BoxSizer(HORIZONTAL)
        self.Sizer.Add(NormalText(self, label='"'), 0, ALIGN_CENTER_VERTICAL)
        self.Sizer.Add(self.__ety, 1, EXPAND)
        self.Sizer.Add(NormalText(self, label='"'), 0, ALIGN_CENTER_VERTICAL)

    def SetValue(self, value):
        """Set value

        :type value: Castable to a str.
        """
        self.__ety.SetValue(value)

    def GetDefault(self) -> str:
        """Get default value.

        :rtype: str
        """
        return self.__ety.GetDefault()

    def IsValidValue(self, value) -> bool:
        """Return True, if value is valid.

        :rtype: bool
        """
        return self.__ety.IsValidValue(value)

    def HasValidValue(self) -> bool:
        """Return True, if the value entered is a valid value.

        :rtype: bool
        """
        return self.__ety.HasValidValue()

    def GetArgumentContainer(self) -> ArgumentContainerBase:
        """Get instance of "ArgumentContainerBase" class managed.

        :rtype: ArgumentContainerBase
        """
        return self.__ety.GetArgumentContainer()

    def SetArgumentContainer(self, str_container: StrContainer):
        """Set instance of "StrContainer" class to be managed.

        :type str_container: StrContainer
        """
        if not isinstance(str_container, StrContainer):
            raise TypeError()

        self.__ety.SetArgumentContainer(str_container)


class ValidateIterableEntryBase(ValidateEntry):
    """Base Entry for displaying IterableArgumentContainerBase
    """

    def __init__(self, iter_container: IterableArgumentContainerBase, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default container

        :type iter_container: IterableArgumentContainerBase
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(iter_container, IterableArgumentContainerBase):
            raise TypeError()

        super().__init__(iter_container, success_color=success_color, error_color=error_color, *args, **kw)

        super(ArgumentContainerEntryBase, self).SetValue(str(iter_container)[1: -1])

    def SetValue(self, value, display=True):
        """Set value

        :type value: Castable to a str.
        :param display:  Whether display is required or not, defaults to True
        :type display: bool, optional
        """
        super(ValidateEntry, self).SetValue(value)
        if display:
            super(ArgumentContainerEntryBase, self).SetValue(str(value)[1: -1])


class ValidateIterableEntry(Panel):
    """Entry for displaying IterableArgumentContainerBase
    """

    def __init__(self, cap, iterable_container: IterableArgumentContainerBase, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default container

        :type iterable_container: IterableArgumentContainerBase
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(iterable_container, IterableArgumentContainerBase):
            raise TypeError()

        super().__init__(*args, **kw)
        self.__ety = ValidateIterableEntryBase(iterable_container, success_color, error_color, parent=self)

        self.Sizer = BoxSizer(HORIZONTAL)
        self.Sizer.Add(NormalText(self, label=cap[0]), 0, ALIGN_CENTER_VERTICAL)
        self.Sizer.Add(self.__ety, 1, EXPAND)
        self.Sizer.Add(NormalText(self, label=cap[1]), 0, ALIGN_CENTER_VERTICAL)

    def SetValue(self, value):
        """Set value

        :type value: Castable to a str.
        """
        self.__ety.SetValue(value)

    def GetDefault(self) -> Any:
        """Get default value

        :rtype: Any
        """
        return self.__ety.GetDefault()

    def IsValidValue(self, value) -> bool:
        """Return True, if value is valid.

        :rtype: bool
        """
        return self.__ety.IsValidValue(value)

    def HasValidValue(self) -> bool:
        """Return True, if the value entered is a valid value.

        :rtype: bool
        """
        return self.__ety.HasValidValue()

    def GetArgumentContainer(self) -> IterableArgumentContainerBase:
        """Get instance of "IterableArgumentContainerBase" class managed.

        :rtype: IterableArgumentContainerBase
        """
        return self.__ety.GetArgumentContainer()

    def SetArgumentContainer(self, iterable_container: IterableArgumentContainerBase):
        """Set instance of "IterableArgumentContainerBase" class to be managed.

        :type iterable_container: IterableArgumentContainerBase
        """
        if not isinstance(iterable_container, IterableArgumentContainerBase):
            raise TypeError()
        self.__ety.SetArgumentContainer(iterable_container)


class ValidateListEntry(ValidateIterableEntry):
    """Entry for displaying ListArgumentContainer
    """

    def __init__(self, list_container: ListArgumentContainer, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default container

        :type list_container: ListArgumentContainer
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(list_container, ListArgumentContainer):
            raise TypeError()
        super().__init__('[]', list_container, success_color=NullColour, error_color='#ff0000', *args, **kw)


class ValidateTupleEntry(ValidateIterableEntry):
    """Entry for displaying ListArgumentContainer
    """

    def __init__(self, tuple_container: TupleArgumentContainer, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default container

        :type tuple_container: TupleArgumentContainer
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(tuple_container, TupleArgumentContainer):
            raise TypeError()
        super().__init__('()', tuple_container, success_color=NullColour, error_color='#ff0000', *args, **kw)


class ValidateChoiceEntry(ArgumentContainerEntryBase, ComboBox):
    """Entry for displaying ChoiceContainer
    """

    def __init__(self, parent: Window, choice_container: ChoiceContainer, success_color: Colour = NullColour, error_color: Colour = '#ff0000'):
        """Default constructor

        :type parent: Window
        :type choice_container: ChoiceContainer
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        if not isinstance(choice_container, ChoiceContainer):
            raise TypeError()

        super().__init__(choice_container)

        value = choice_container.GetValue()
        choices = choice_container.GetChoices()
        super(ArgumentContainerEntryBase, self).__init__(parent, value=value, choices=choices, style=CB_READONLY)

        self.Bind(EVT_COMBOBOX, self.__OnSelected)

    def SetValue(self, value):
        """Set the value to "ArgumentContainerBase" class.
        """
        super().SetValue(value)
        self.__UpdateColor()

    def GetChoices(self) -> Tuple[Union[int, float, str], ...]:
        """Get choices.

        :rtype: Tuple[Union[int, float, str], ...]
        """
        return self.GetArgumentContainer().GetChoices()

    def SetArgumentContainer(self, choice_container: ChoiceContainer):
        """Set instance of "ChoiceContainer" class to be managed.

        :type choice_container: ChoiceContainer
        """
        if not isinstance(choice_container, ChoiceContainer):
            raise TypeError()

        super().SetArgumentContainer(choice_container)
        self.__UpdateColor()

    def __OnSelected(self, event):
        event.Skip()
        value = super(ArgumentContainerEntryBase, self).GetValue()
        super().SetValue(value)


class LabeledValidateEntry(ArgumentContainerEntryBase, Panel):
    """ValidateEntry and label widget.
    """

    def __init__(self, label, arg_container, *args, **kw):
        super(ArgumentContainerEntryBase, self).__init__(*args, **kw)

        self.__lbl = NormalText(label=label, parent=self)
        if isinstance(arg_container, ChoiceContainer):
            self.__ety = ValidateChoiceEntry(self, arg_container)
        elif isinstance(arg_container, ListArgumentContainer):
            self.__ety = ValidateListEntry(arg_container, parent=self)
        elif isinstance(arg_container, TupleArgumentContainer):
            self.__ety = ValidateTupleEntry(arg_container, parent=self)
        elif isinstance(arg_container, StrContainer):
            self.__ety = ValidateStrEntry(arg_container, parent=self)
        else:
            self.__ety = ValidateEntry(arg_container, parent=self)

        self.Sizer = BoxSizer(HORIZONTAL)
        self.Sizer.Add(self.__lbl, 0, ALIGN_CENTER_VERTICAL)
        self.Sizer.AddSpacer(10)
        self.Sizer.AddStretchSpacer()
        self.Sizer.Add(self.__ety, 0, ALIGN_CENTER_VERTICAL)

    def GetLabel(self) -> str:
        """Get label.

        :rtype: str
        """
        return self.__lbl.GetLabel()

    def SetLabel(self, value: str):
        """Set label.

        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError()

        self.__lbl.SetLabel(value)

    def GetValue(self) -> Any:
        """Get value

        :rtype: Any
        """
        return self.__ety.GetValue()

    def SetValue(self, value):
        """Set the value to "ArgumentContainerBase" class.
        """
        self.__ety.SetValue(value)

    def GetDefault(self) -> Any:
        """Get default value

        :rtype: Any
        """
        return self.__ety.GetDefault()

    def GetChoices(self):
        """Get choices. If the managed is not a ChoiceContainer, an empty list will be returned.

        :return: [description]
        :rtype: [type]
        """
        return self.__ety.GetChoices() if isinstance(self.GetArgumentContainer(), ChoiceContainer) else []

    def IsValidValue(self, value) -> bool:
        """Return True, if value is valid.

        :rtype: bool
        """
        return self.__ety.IsValidValue(value)

    def HasValidValue(self) -> bool:
        """Return True, if the value entered is a valid value.

        :rtype: bool
        """
        return self.__ety.HasValidValue()

    def GetArgumentContainer(self) -> ArgumentContainerBase:
        """Get instance of "ArgumentContainerBase" class managed.

        :rtype: ArgumentContainerBase
        """
        return self.__ety.GetArgumentContainer()

    def SetArgumentContainer(self, arg_container: ArgumentContainerBase):
        """Set instance of "ArgumentContainerBase" class to be managed.

        :type arg_container: ArgumentContainerBase
        """
        self.__ety.SetArgumentContainer(arg_container)


class DelimiterEntry(LabeledValidateEntry):
    """Entry of delimiter.
    """

    def __init__(self, choice_container: ChoiceContainer, *args, **kw):
        """Default constructor

        :param choice_container: Containing a choice of delimiters
        :type choice_container: ChoiceContainer
        """
        if not isinstance(choice_container, ChoiceContainer):
            raise TypeError()

        super().__init__('Delimiter', choice_container, *args, **kw)

    def GetSymbolValue(self) -> str:
        """Returns a value that has been converted to a form that can be processed by programming.

        :rtype: str
        """
        value = self.GetValue()
        start = value.rfind('[')
        end = value.rfind(']')
        return value[start + 1: end]


class FunctionArgumentEntry(ScrolledPanel):
    """Entry for displaying FunctionContainerBase
    """

    def __init__(self, parent: Window, func_container: FunctionContainerBase, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default constructor

        :type parent: Window
        :type func_container: FunctionContainerBase
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        super().__init__(parent, *args, **kw)
        self.__func_container = func_container
        self.__CreateContents()

    def GetFunction(self) -> FunctionContainerBase:
        """Get instance of "FunctionContainerBase" class managed.

        :rtype: FunctionContainerBase
        """
        return self.__func_container

    def HasValidArguments(self) -> bool:
        """Return True, if arguments is valid.

        :rtype: bool
        """
        return self.__func_container.HasValidArguments()

    def UpdateContents(self):
        """Update contents
        """
        self.Sizer.Clear(True)
        self.__CreateContents()

    def __CreateContents(self):
        arg_names_h_sizer = BoxSizer(HORIZONTAL)

        for name in self.__func_container.GetArgumentNames():
            arg_names_h_sizer.Add(NormalText(self, label=name), 1, LEFT, 3)

        arg_ety_h_sizer = BoxSizer(HORIZONTAL)
        arg_ety_h_sizer.AddSpacer(10)
        for arg_container in self.__func_container.GetArgumentContainerList():
            if isinstance(arg_container, ChoiceContainer):
                ety = ValidateChoiceEntry(self, arg_container)
            elif isinstance(arg_container, ListArgumentContainer):
                ety = ValidateListEntry(arg_container, parent=self)
            elif isinstance(arg_container, TupleArgumentContainer):
                ety = ValidateTupleEntry(arg_container, parent=self)
            elif isinstance(arg_container, StrContainer):
                ety = ValidateStrEntry(arg_container, parent=self)
            else:
                ety = ValidateEntry(arg_container, parent=self)
            arg_ety_h_sizer.Add(ety, 1, EXPAND)
            arg_ety_h_sizer.AddSpacer(10)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(arg_names_h_sizer, 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.Add(arg_ety_h_sizer, 0, EXPAND)

        self.SetupScrolling(scroll_y=False)
        self.Layout()


class FunctionEntry(Panel):
    """Widget for function name and FunctionArgumentEntry.
    """

    def __init__(self, func_container: FunctionContainerBase, success_color: Colour = NullColour, error_color: Colour = '#ff0000', *args, **kw):
        """Default constructor

        :type func_container: FunctionContainerBase
        :param success_color: Color if the entered value is valid. defaults to NullColour
        :type success_color: Colour, optional
        :param error_color: Color if the entered value is invalid. defaults to '#ff0000'
        :type error_color: Colour, optional
        """
        super().__init__(*args, **kw)
        self.__success_color = success_color
        self.__error_color = error_color

        self.__name_lbl = NormalText(self, label=func_container.__class__.__name__)
        self.__arg_ety = FunctionArgumentEntry(self, func_container, success_color=NullColour, error_color='#ff0000')

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__name_lbl, 0, LEFT, 10)
        self.Sizer.Add(self.__arg_ety, 0, EXPAND)

        self.Bind(EVT_CHAR_HOOK, self.__OnCharHook)

        self.UpdateColor()

    def GetFunction(self):
        """Get instance of "FunctionContainerBase" class managed.

        :rtype: FunctionContainerBase
        """
        return self.__arg_ety.GetFunction()

    def HasValidArguments(self):
        """Return True, if arguments is valid.

        :rtype: bool
        """
        return self.__arg_ety.HasValidArguments()

    def UpdateContents(self):
        """Update contents
        """
        self.__arg_ety.UpdateContents()
        self.Layout()

    def UpdateColor(self):
        """Update color
        """
        if self.__arg_ety.HasValidArguments():
            color = self.__success_color
        else:
            color = self.__error_color

        self.__name_lbl.SetBackgroundColour(color)
        self.Refresh()

    def __OnCharHook(self, event):
        event.Skip()
        self.UpdateColor()


class FunctionListEntry(Panel):
    """Entry for displaying a list of FunctionContainerBase.
    """

    def __init__(self, selected_function: Union[str, FunctionContainerBase] = '', function_list: Optional[List[FunctionContainerBase]] = None, *args, **kw):
        """Default constructor

        :type selected_function: Union[str, FunctionContainerBase], optional
        :type function_list: Optional[List[FunctionContainerBase]], optional
        """
        super().__init__(*args, **kw)
        if isinstance(selected_function, FunctionContainerBase):
            selected_function = selected_function.__class__.__name__

        if not isinstance(selected_function, str):
            raise TypeError()

        function_list = [] if function_list is None else function_list
        if not HasValidElement(function_list, FunctionContainerBase):
            raise TypeError()

        self.__selected_func = ''
        self.__func_dict = {}

        self.__name_ety = NormalComboBox(self, style=CB_READONLY)
        self.__name_ety.Bind(EVT_COMBOBOX, lambda _: self.__OnSelected())
        self.__help_btn = HelpButton(parent=self, size=(25, 25))
        self.header_sizer = BoxSizer(HORIZONTAL)
        self.header_sizer.Add(self.__name_ety)
        self.header_sizer.AddSpacer(10)
        self.header_sizer.Add(self.__help_btn)
        self.header_sizer.AddSpacer(10)

        self.__func_ety = None
        self.__func_ety_sizer = BoxSizer()

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.header_sizer, 0, EXPAND)
        self.Sizer.Add(self.__func_ety_sizer, 0, EXPAND)

        self.RegisterFunctionList(function_list)
        self.Select(selected_function)
        self.__UpdateCtrl()

    def GetSelectedFunctionName(self) -> str:
        """Get selected name of function.
        :rtype: str
        """
        return self.__name_ety.GetValue()

    def GetSelectedFunction(self) -> FunctionContainerBase:
        """Get selected function.

        :rtype: FunctionContainerBase
        """
        name = self.GetSelectedFunctionName()
        return self.__func_dict.get(name)

    def GetFunctionNames(self) -> Tuple[str, ...]:
        """Get a list of function\'s name

        :rtype: Tuple[str, ...]
        """
        return tuple(self.__func_dict.keys())

    def GetFunctionList(self) -> List[FunctionContainerBase]:
        """Get a list of functions

        :rtype: List[FunctionContainerBase, ...]
        """
        return list(self.__func_dict.values())

    def Select(self, function: Union[str, FunctionContainerBase]):
        """Select function.

        :param function: function name or instance of FunctionContainerBase
        :type function: Union[str, FunctionContainerBase]
        """
        if isinstance(function, FunctionContainerBase):
            function = function.__class__.__name__

        if not isinstance(function, str):
            raise TypeError()

        self.__name_ety.Value = function
        self.__OnSelected()

    def RegisterFunctionList(self, function_list: List[FunctionContainerBase]):
        """Register a list of functions.

        :type function_list: List[FunctionContainerBase, ...]
        """
        if not HasValidElement(function_list, FunctionContainerBase):
            raise TypeError()

        self.__func_dict.update({func.__class__.__name__: func for func in function_list})

        names = self.GetFunctionNames()
        self.__name_ety.SetItems(names)

        self.__UpdateCtrl()

    def DeregisterFunctionList(self, function_list: List[FunctionContainerBase]):
        """Deregister a list of functions.

        :type function_list: List[FunctionContainerBase, ...]
        """
        func_list = []
        for func in function_list:
            if isinstance(func, str):
                func_list.append(func)
            elif isinstance(func, FunctionContainerBase):
                func_list.append(func.__class__.__name__)
            else:
                raise TypeError()

        if self.__selected_func in func_list:
            self.__selected_func = ''
            self.__name_ety.Value = ''

        for func in func_list:
            del self.__func_dict[func]

        func_list = self.GetFunctionList()
        self.__name_ety.SetItems(func_list)

    def HasValidArguments(self) -> bool:
        """Return True, if arguments is valid.

        :rtype: bool
        """
        return None if self.__func_ety is None else self.__func_ety.HasValidArguments()

    def __UpdateCtrl(self):
        if not self.IsEnabled():
            return

        if len(self.__func_dict) != 0:
            self.__name_ety.Enable()
            self.__help_btn.Enable()
        else:
            self.__name_ety.Disable()
            self.__help_btn.Disable()

    def __OnSelected(self):
        if (func := self.GetSelectedFunction()) is None:
            return

        if (func_name := func.__class__.__name__) == self.__selected_func:
            return

        if self.__func_ety is not None:
            self.__func_ety.Hide()
            self.__func_ety_sizer.Detach(self.__func_ety)
            self.__func_ety.Destroy()

        self.__func_ety = FunctionArgumentEntry(self, func)
        self.__func_ety_sizer.Add(self.__func_ety, 1, EXPAND)

        self.__selected_func = func_name

        self.Layout()


class NewDialog(Dialog):
    """Dialog for inputting experimental data.
    """

    def __init__(
            self,
            encoding: ChoiceContainer,
            delimiter: ChoiceContainer,
            selected_encode_function: EncodeFunctionContainerBase,
            encode_function_list: List[EncodeFunctionContainerBase],
            data_buffer_size: int,
            *args,
            **kw):
        """Default constructor

        :param encoding: Encoding of the file to be read.
        :type encoding: ChoiceContainer
        :param delimiter: Delimiter of the file to be read.
        :type delimiter: ChoiceContainer
        :param selected_encode_function: Selected encode function.
        :type selected_encode_function: EncodeFunctionContainerBase
        :param encode_function_list: List of selectable encoding functions
        :type encode_function_list: List[EncodeFunctionContainerBase]
        :param data_buffer_size: Size of the buffer for data recovery.
        :type data_buffer_size: int
        """
        super().__init__(style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER, *args, **kw)
        self.__prev_encoding = encoding
        self.__contents_list = []
        self.__data_list = []

        self.__delimiter = delimiter
        self.__data_buffer_size = data_buffer_size

        self.__browse_btn = BrowseButton(parent=self)
        self.__browse_btn.Bind(EVT_BUTTON, lambda _: self.__OnBrowseBtnPushed())
        self.__preview_btn = PreviewButton(parent=self)
        self.__preview_btn.Bind(EVT_BUTTON, lambda _: self.__OnPreviewBtnPushed())
        self.__preview_btn.Disable()
        self.__clear_btn = ClearButton(parent=self)
        self.__clear_btn.Bind(EVT_BUTTON, lambda _: self.__OnClearBtnPushed())
        self.__clear_btn.Disable()
        control_btn_sizer = BoxSizer(HORIZONTAL)
        control_btn_sizer.Add(self.__browse_btn, 0, ALL, 10)
        control_btn_sizer.Add(self.__preview_btn, 0, ALL, 10)
        control_btn_sizer.AddStretchSpacer()
        control_btn_sizer.Add(self.__clear_btn, 0, ALL, 10)

        self.__list_ctrl = UltimateListCtrl(self, style=0, agwStyle=ULC_HRULES | ULC_REPORT | ULC_BORDER_SELECT |
                                            ULC_NO_FULL_ROW_SELECT | ULC_HAS_VARIABLE_ROW_HEIGHT)
        for n, heading in enumerate(['', 'FILE NAME', 'DATA SIZE', 'HAS BACKGROUND', 'FILE TYPE', 'PATH']):
            self.__list_ctrl.InsertColumn(n, heading, ULC_FORMAT_CENTER)

        self.__func_list_ety = FunctionListEntry(selected_function=selected_encode_function.GetValue(), function_list=encode_function_list, parent=self)
        self.__exe_btn = ExecuteButton(parent=self.__func_list_ety)
        self.__exe_btn.Bind(EVT_BUTTON, lambda _: self.__OnExecuteBtnPushed())
        self.__exe_btn.Disable()
        self.__encoding_ety = LabeledValidateEntry('Encode type', encoding, parent=self.__func_list_ety)

        self.__func_list_ety.header_sizer.AddSpacer(10)
        self.__func_list_ety.header_sizer.AddStretchSpacer()
        self.__func_list_ety.header_sizer.Add(self.__encoding_ety)
        self.__func_list_ety.header_sizer.AddSpacer(10)
        self.__func_list_ety.header_sizer.Add(self.__exe_btn)

        self.__func_list_ety.Layout()

        self.__ok_btn = OkButton(parent=self)
        self.__ok_btn.Disable()
        cancel_btn = CancelButton(parent=self)
        btn_h_sizer = BoxSizer(HORIZONTAL)
        btn_h_sizer.AddStretchSpacer(2)
        btn_h_sizer.Add(self.__ok_btn)
        btn_h_sizer.AddStretchSpacer(1)
        btn_h_sizer.Add(cancel_btn)
        btn_h_sizer.AddStretchSpacer(2)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(control_btn_sizer, 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__list_ctrl, 1, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__func_list_ety, 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(NormalLine(size=(-1, 2), parent=self), 0, EXPAND | LEFT | RIGHT, 20)
        self.Sizer.Add(btn_h_sizer, 0, EXPAND | ALL, 10)

        self.Fit()

    def GetEncoding(self) -> ChoiceContainer:
        """Get encoding.

        :rtype: ChoiceContainer
        """
        return self.__encoding_ety.GetArgumentContainer()

    def GetDelimiter(self) -> ChoiceContainer:
        """Get delimiter

        :rtype: ChoiceContainer
        """
        return self.__delimiter

    def GetSelectedEncodeFunction(self) -> EncodeFunctionContainerBase:
        """Get selected encode function

        :rtype: EncodeFunctionContainerBase
        """
        return self.__func_list_ety.GetSelectedFunction()

    def GetDataList(self) -> List[DataContainer]:
        """Get a list of DataContainer

        :rtype: List[DataContainer]
        """
        return self.__data_list

    def __GetPath(self, index):
        if index >= self.__list_ctrl.GetItemCount():
            return

        column_count = self.__list_ctrl.GetColumnCount()
        return self.__list_ctrl.GetItem(index, column_count - 1).GetText()

    def __OnBrowseBtnPushed(self):
        encode_func = self.GetSelectedEncodeFunction()
        wildcard = encode_func.SendFileTypeWildcard()

        with FileDialog(self, message=NEW_MENU_ITEM_HELP, wildcard=wildcard, style=FD_OPEN | FD_FILE_MUST_EXIST | FD_MULTIPLE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path_list = dialog.GetPaths()

        encoding = self.GetEncoding().GetValue()

        index = self.__list_ctrl.GetFirstSelected()
        item_count = self.__list_ctrl.GetItemCount()
        index = index if index != -1 else item_count
        length = len(path_list)
        for n, path in enumerate(reversed(path_list)):
            try:
                with open(path, mode='r', encoding=encoding) as f:
                    contents = f.read()

            except Exception:
                LogError(f'{basename(path)} is failed.')
                continue

            self.__contents_list.insert(index, contents)

            self.__list_ctrl.InsertStringItem(index, str(length - n + index))
            self.__list_ctrl.SetStringItem(index, 1, basename(path))
            self.__list_ctrl.SetStringItem(index, 4, GetFileExtention(path))
            self.__list_ctrl.SetStringItem(index, 5, path)

        for pos in range(index + length, item_count + length):
            self.__list_ctrl.SetStringItem(pos, 0, str(pos + 1))

        self.__data_list = [None] * len(self.__contents_list)

        if len(self.__contents_list) > 0:
            self.__preview_btn.Enable()
            self.__clear_btn.Enable()
            self.__exe_btn.Enable()

    def __OnPreviewBtnPushed(self):
        if len(self.__contents_list) == 0:
            return

        index = max(self.__list_ctrl.GetFirstSelected(), 0)
        contents = self.__contents_list[index]
        path = self.__GetPath(index)
        title = basename(path)

        dialog = DataPreviewDialog(contents, self.__delimiter, parent=self, title=title)
        dialog.Bind(EVT_CLOSE, self.__OnPreviewDialogClose)
        dialog.Show()

    def __OnPreviewDialogClose(self, event):
        event.Skip()
        dialog = event.GetEventObject()
        self.__delimiter_container = dialog.GetDelimiter()

    def __OnClearBtnPushed(self):
        selection_count = self.__list_ctrl.GetSelectedItemCount()
        if selection_count == 0:
            self.__list_ctrl.DeleteAllItems()
            self.__contents_list.clear()
            self.__data_list.clear()
        else:
            start = self.__list_ctrl.GetFirstSelected()
            end = start + selection_count
            for i in reversed(range(start, end)):
                self.__list_ctrl.DeleteItem(i)

            self.__contents_list = self.__contents_list[:start] + self.__contents_list[end:]
            self.__data_list = self.__data_list[:start] + self.__data_list[end:]

            for pos in range(start, end):
                self.__list_ctrl.SetStringItem(pos, 0, str(pos + 1))

        if len(self.__contents_list) == 0:
            self.__preview_btn.Disable()
            self.__clear_btn.Disable()
            self.__exe_btn.Disable()

        if len(self.__data_list) == 0:
            self.__ok_btn.Disable()

        self.Layout()

    def __OnExecuteBtnPushed(self):
        encode_func_container = self.GetSelectedEncodeFunction()
        for index, contents in enumerate(self.__contents_list):
            if self.__data_list[index] is not None:
                continue

            path = self.__GetPath(index)
            try:
                x, y, bg = self.__GetSpectrumParameter(contents, encode_func_container)
            except BaseException:
                LogError(f'{basename(path)} is failed.')
                continue

            spectrum = Spectrum(x, y, bg)
            data_container = DataContainer(path, self.__data_buffer_size)
            data_container.Append(spectrum, msg=path)
            self.__data_list[index] = data_container

            self.__list_ctrl.SetStringItem(index, 2, str(len(x)))
            self.__list_ctrl.SetStringItem(index, 3, 'O' if len(bg) else 'X')

        if all([data is not None for data in self.__data_list]):
            self.__ok_btn.Enable()
        else:
            self.__ok_btn.Disable()

    def __GetSpectrumParameter(self, contents, encode_func_container):
        params = encode_func_container.Execution(contents)

        x = []
        y = []
        bg = []
        for param, ret_param in zip(params, encode_func_container.SendReturnParams()):
            if ret_param == 'x':
                x = param
            elif ret_param == 'y':
                y = param
            elif ret_param == 'b':
                bg = param

        if len(x) != len(y):
            raise RuntimeError()

        if len(x) == 0:
            raise RuntimeError()

        if len(bg) != 0 or len(bg) == len(x):
            raise RuntimeError()

        return x, y, bg

    def __OnCharHook(self, event):
        event.Skip()

        if self.__encode_func_ety.HasValidArguments():
            self.__exe_btn.Enable()
        else:
            self.__exe_btn.Disable()


class ExportDialog(Dialog):
    """Dialog for outputting experimental data.
    """

    def __init__(self, project: Project, encoding: ChoiceContainer, selected_function: DecodeFunctionContainerBase, decode_function_list: List[DecodeFunctionContainerBase], *args, **kw):
        """Default constructor

        :type project: Project
        :param encoding: Encoding of the file to be read.
        :type encoding: ChoiceContainer
        :param selected_function: selected decode function
        :type selected_function: DecodeFunctionContainerBase
        :param decode_function_list: List of selectable decoding functions
        :type decode_function_list: List[DecodeFunctionContainerBase]
        """
        super().__init__(style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER, *args, **kw)
        self.__prev_encoding = encoding
        self.__project = project
        self.__dummy_project = self.__CreateDummyProject(project)

        preview_lbl = NormalText(self, label='Preview')
        self.__preview_ety = NormalEntry(self, style=TE_MULTILINE | TE_READONLY)
        self.__func_list_ety = FunctionListEntry(selected_function=selected_function, function_list=decode_function_list, parent=self)

        self.__exe_btn = ExecuteButton(parent=self.__func_list_ety)
        self.__exe_btn.Bind(EVT_BUTTON, lambda _: self.__OnExecuteBtnPushed())
        self.__encoding_ety = LabeledValidateEntry('Encode type', encoding, parent=self.__func_list_ety)

        self.__func_list_ety.Bind(EVT_CHAR_HOOK, self.__OnCharHook)
        self.__func_list_ety.header_sizer.AddSpacer(10)
        self.__func_list_ety.header_sizer.AddStretchSpacer()
        self.__func_list_ety.header_sizer.Add(self.__encoding_ety)
        self.__func_list_ety.header_sizer.AddSpacer(10)
        self.__func_list_ety.header_sizer.Add(self.__exe_btn)
        self.__func_list_ety.header_sizer.AddSpacer(10)

        self.__func_list_ety.Layout()

        ok_btn = OkButton(parent=self)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(preview_lbl, 0, LEFT, 10)
        self.Sizer.Add(self.__preview_ety, 1, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(self.__func_list_ety, 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(NormalLine(size=(-1, 2), parent=self), 0, EXPAND | LEFT | RIGHT, 20)
        self.Sizer.Add(ok_btn, 0, CENTER | ALL, 10)

        self.__UpdatePreview()
        self.Fit()

    def GetSelectedDecodeFunction(self) -> DecodeFunctionContainerBase:
        """Get selected decode function

        :rtype: DecodeFunctionContainerBase
        """
        return self.__func_list_ety.GetSelectedFunction()

    def GetEncoding(self) -> ChoiceContainer:
        """Get encoding

        :rtype: ChoiceContainer
        """
        return self.__encoding_ety.GetArgumentContainer()

    def __CreateDummyProject(self, project, data_size=3, spectrum_size=100) -> Project:
        dummy_project = deepcopy(project)
        data_list = []
        for data in project.GetDataList()[:data_size]:
            x, y = data.XY
            bg = data.BackGround

            mini_data = deepcopy(data)
            mini_data.XY = (x[:spectrum_size], y[:spectrum_size])
            mini_data.BackGround = bg[:spectrum_size]
            data_list.append(mini_data)

        dummy_project.SetDataList(data_list)

        return dummy_project

    def __UpdatePreview(self):
        func = self.GetSelectedDecodeFunction()
        project = deepcopy(self.__dummy_project)
        values = func.Execution(project)

        if not isinstance(values, (list, tuple)):
            raise TypeError()

        if len(values) == 2 and all([isinstance(value, str) for value in values]):
            contents = values[1]

        elif isinstance(values, (list, tuple)):
            if not HasValidElement(values, (list, tuple)):
                raise TypeError()

            contents = values[0][1]

        self.__preview_ety.SetValue(contents)

    def __OnExecuteBtnPushed(self):
        func = self.GetSelectedDecodeFunction()
        project = deepcopy(self.__project)

        values = func.Execution(project)

        if not isinstance(values, (list, tuple)):
            raise TypeError()

        wildcard = func.SendFileTypeWildcard()
        extension = GetExtension(wildcard)
        encoding = self.GetEncoding().GetValue()
        if len(values) == 2 and all([isinstance(value, str) for value in values]):
            file_name, contents = values
            with FileDialog(self, defaultFile=file_name + extension, wildcard=wildcard) as dialog:
                if dialog.ShowModal() == ID_CANCEL:
                    return

                path = dialog.GetPath()

            with open(path, mode='w', encoding=encoding) as f:
                f.write(contents)

        elif isinstance(values, (list, tuple)):
            if not HasValidElement(values, (list, tuple)):
                raise TypeError()

            with DirDialog(self) as dialog:
                if dialog.ShowModal() == ID_CANCEL:
                    return

                dir_path = dialog.GetPath()

            for file_name, contents in values:
                with open(join(dir_path, file_name + extension), mode='w', encoding=encoding) as f:
                    f.write(contents)

        else:
            raise TypeError()

    def __OnCharHook(self, event):
        event.Skip()

        if self.__encode_func_ety.HasValidArguments():
            self.__exe_btn.Enable()
        else:
            self.__exe_btn.Disable()


class DataPreviewDialog(Dialog):
    """Dialog for data preview.
    """

    def __init__(self, contents: str, delimiter: ChoiceContainer, *args, **kw):
        """Default constructor

        :param contents: Contents describing the experimental data
        :type contents: str
        :param delimiter: Delimiter of the file to be read.
        :type delimiter: ChoiceContainer
        """
        super().__init__(style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER, *args, **kw)
        self.__contents = contents

        self.__delimiter_ety = DelimiterEntry(delimiter, parent=self)
        self.__delimiter_ety.Bind(EVT_COMBOBOX, lambda _: self.__OnDelimiterSelected())
        self.__list_ctrl = UltimateListCtrl(self, style=0, agwStyle=ULC_HRULES | ULC_REPORT | ULC_BORDER_SELECT |
                                            ULC_NO_FULL_ROW_SELECT | ULC_HAS_VARIABLE_ROW_HEIGHT)

        delimiter = self.__delimiter_ety.GetSymbolValue()
        self.__prev_delimiter = delimiter
        self.__CreateListContents(delimiter)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__delimiter_ety, 0, ALL, 10)
        self.Sizer.Add(self.__list_ctrl, 1, EXPAND | ALL, 10)

    def GetDelimiter(self) -> ChoiceContainer:
        """Get delimiter

        :rtype: ChoiceContainer
        """
        return self.__delimiter_ety.GetArgumentContainer()

    def __OnDelimiterSelected(self):
        delimiter = self.__delimiter_ety.GetSymbolValue()
        if delimiter == self.__prev_delimiter:
            return

        self.__prev_delimiter = delimiter

        self.__list_ctrl.DeleteAllColumns()
        self.__list_ctrl.DeleteAllItems()
        self.__CreateListContents(delimiter)

    def __CreateListContents(self, delimiter):
        row_limit = 100
        col_limit = 100
        max_col = 0
        value_list = []
        for y, line in enumerate(self.__contents.split('\n')):
            if y >= row_limit:
                break

            value_list.append([])

            line = line.strip()
            if line == '':
                continue

            for x, value in enumerate(line.split(delimiter)):
                if x >= col_limit:
                    break

                value = value.strip()
                value_list[-1].append(value)

                max_col = max(x + 1, max_col)

        if max_col == 0:
            return

        self.__list_ctrl.InsertColumn(0, '')
        for x in range(max_col):
            alphabet_count = ord('Z') - ord('A') + 1
            label = chr(ord('A') + x // alphabet_count - 1) if x > alphabet_count else ''
            label += chr(ord('A') + x)
            self.__list_ctrl.InsertColumn(x + 1, chr(ord('A') + x), ULC_FORMAT_CENTER)

            if x + 1 >= col_limit:
                self.__list_ctrl.InsertColumn(x + 2, '...', ULC_FORMAT_CENTER)
                break

        for y, line in enumerate(value_list):

            self.__list_ctrl.InsertStringItem(y, str(y + 1))

            self.__list_ctrl.SetStringItem(y, 0, str(y + 1))
            for x, value in enumerate(line):
                self.__list_ctrl.SetStringItem(y, x + 1, value)

            if y + 1 >= row_limit:
                self.__list_ctrl.InsertStringItem(y + 1, ':')
                break


class ProjectMemoDialog(Dialog):
    def __init__(self, date, note, *args, **kw):
        super().__init__(style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER, *args, **kw)
        # if not isdir(dirname(path)):
        #     raise ValueError()

        # self.__path = path

        date_lbl = NormalText(self, label='Experiment date')
        self.__date_ety = DatePickerCtrl(self, dt=date)
        date_h_sizer = BoxSizer(HORIZONTAL)
        date_h_sizer.Add(date_lbl, 0, ALIGN_CENTER_VERTICAL)
        date_h_sizer.AddSpacer(10)
        date_h_sizer.Add(self.__date_ety)

        note_lbl = NormalText(self, label='Note')
        self.__note_ety = NormalEntry(self, value=note, style=TE_MULTILINE)

        self.__ok_btn = OkButton(parent=self)
        # save_btn = SaveButton(parent=self)
        # save_btn.Bind(EVT_BUTTON, self.__OnSaveBtnPushed)
        cancel_btn = CancelButton(parent=self)
        btn_h_sizer = BoxSizer(HORIZONTAL)
        btn_h_sizer.AddStretchSpacer(2)
        btn_h_sizer.Add(self.__ok_btn)
        # btn_h_sizer.Add(save_btn)
        btn_h_sizer.AddStretchSpacer(1)
        btn_h_sizer.Add(cancel_btn)
        btn_h_sizer.AddStretchSpacer(2)

        self.Sizer = BoxSizer(VERTICAL)
        # self.Sizer.AddSpacer(10)
        # self.Sizer.Add(file_h_sizer, 0, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(date_h_sizer, 0, LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(note_lbl, 0, LEFT | RIGHT, 10)
        self.Sizer.Add(self.__note_ety, 1, EXPAND | LEFT | RIGHT, 10)
        self.Sizer.AddSpacer(10)
        self.Sizer.Add(btn_h_sizer, 0, EXPAND | ALL, 10)

    # def GetPath(self):
    #     # return self.__file_ety.GetValue()
    #     return self.__path

    # def GetDirectory(self):
    #     return dirname(self.GetPath())

    # def GetFile(self):
    #     return basename(self.GetPath())

    def GetDate(self) -> datetime:
        value = self.__date_ety.GetValue()
        return datetime(value.year, value.month, value.day)

    def GetNote(self):
        return self.__note_ety.GetValue()

    # def __OnSaveBtnPushed(self, event):
    #     dirname = self.GetDirectory()
    #     file_ = self.GetFile()

    #     with FileDialog(self, defaultDir=dirname, defaultFile=file_, wildcard=SAVEFILE_WILDCARD, style=FD_SAVE) as dialog:
    #         if dialog.ShowModal() == ID_CANCEL:
    #             return

    #         path = dialog.GetPath()

    #     self.__path = path
    #     self.EndModal(event.GetId())


class RegisterDialog(Dialog):
    """Dialog for entering non-duplicate values
    """

    def __init__(self, name_list: List[str], *args, **kw):
        """Default constructor

        :param name_list: List of registered names
        :type name_list: List[str]
        """
        super().__init__(*args, **kw)
        self.__name_list = name_list

        self.__msg_lbl = NormalText(self, label='Please enter name.')
        self.__name_ety = NormalEntry(self)
        self.__name_ety.Bind(EVT_CHAR_HOOK, self.__Check)

        self.__ok_btn = OkButton(self)
        self.__cancel_btn = CancelButton(self)

        btn_h_sizer = BoxSizer(HORIZONTAL)
        btn_h_sizer.AddStretchSpacer(2)
        btn_h_sizer.Add(self.__ok_btn)
        btn_h_sizer.AddStretchSpacer(1)
        btn_h_sizer.Add(self.__cancel_btn)
        btn_h_sizer.AddStretchSpacer(2)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__msg_lbl, 0, CENTER | ALL, 10)
        self.Sizer.Add(self.__name_ety, 1, EXPAND | ALL, 10)
        self.Sizer.Add(btn_h_sizer, 0, EXPAND | ALL, 10)

        self.Fit()

    def GetName(self) -> str:
        """Get entered name.

        :rtype: str
        """
        return self.__name_ety.GetValue()

    def __Check(self, event):
        event.Skip()
        if event.IsKeyInCategory(WXK_CATEGORY_NAVIGATION):
            return

        value = self.__name_ety.GetValue()
        keycode = event.GetUnicodeKey()
        if keycode == 0:
            return

        # Convert to upper case alphabet keycode.
        if event.shiftDown and 49 <= keycode <= 57:
            keycode -= 16

        # Convert numbers to symbolic keycode. It may not work properly on non-Japanese keyboards.
        if not event.shiftDown and 65 <= keycode <= 90:
            keycode += 32

        selection = self.__name_ety.GetSelection()
        name = GetNextStr(value, keycode, selection)

        if name == '':
            msg = 'Empty name isn\'t allowed.'
            self.__ok_btn.Disable()

        elif name in self.__name_list:
            msg = 'This name is duplicated'
            self.__ok_btn.Disable()

        else:
            msg = 'Please enter name.'
            self.__ok_btn.Enable()

        self.__msg_lbl.SetLabel(msg)
        event.Skip()


class SaveCheckDialog(Dialog):
    """Dialog for confirmation of save
    """

    def __init__(self, *args, **kw):
        """Default constructor
        """
        super().__init__(*args, **kw)

        art_info = ArtProvider().GetBitmap(ART_INFORMATION)
        info_icon = StaticBitmap(self, bitmap=art_info)
        msg_lbl = NormalText(self, label='Save your changes ?')
        msg_h_sizer = BoxSizer(HORIZONTAL)
        msg_h_sizer.Add(info_icon)
        msg_h_sizer.AddSpacer(10)
        msg_h_sizer.Add(msg_lbl, 0, ALIGN_CENTER_VERTICAL)

        save_btn = SaveButton(parent=self)
        dont_save_btn = DontSaveButton(parent=self)
        cancel_btn = CancelButton(parent=self)
        btn_h_sizer = BoxSizer(HORIZONTAL)
        btn_h_sizer.AddStretchSpacer(2)
        btn_h_sizer.Add(save_btn)
        btn_h_sizer.AddStretchSpacer(1)
        btn_h_sizer.Add(dont_save_btn)
        btn_h_sizer.AddStretchSpacer(1)
        btn_h_sizer.Add(cancel_btn)
        btn_h_sizer.AddStretchSpacer(2)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(msg_h_sizer, 0, CENTER | ALL, 20)
        self.Sizer.Add(btn_h_sizer, 0, EXPAND | ALL, 10)
        self.Fit()

        self.Bind(EVT_BUTTON, self.__OnBtnPushed)

    def __OnBtnPushed(self, event):
        self.EndModal(event.GetId())


class PreferenceDialog(Dialog):
    """Dialog for setting iSATex preferences.
    """

    def __init__(self, data_buffer_size: IntContainer, *args, **kw):
        """Default constructor

        :param data_buffer_size: Buffer size for data recovery
        :type data_buffer_size: IntContainer
        """
        super().__init__(style=DEFAULT_DIALOG_STYLE | RESIZE_BORDER, *args, **kw)
        self.__data_buffer_size_ety = LabeledValidateEntry('Data buffer size', data_buffer_size, parent=self)

        self.__ok_btn = OkButton(parent=self)
        self.__cancel_btn = CancelButton(parent=self)
        btn_sizer = BoxSizer(HORIZONTAL)
        btn_sizer.AddStretchSpacer(2)
        btn_sizer.Add(self.__ok_btn, 0, ALL, 10)
        btn_sizer.AddStretchSpacer(1)
        btn_sizer.Add(self.__cancel_btn, 0, ALL, 10)
        btn_sizer.AddStretchSpacer(2)

        self.Sizer = BoxSizer(VERTICAL)
        self.Sizer.Add(self.__data_buffer_size_ety, 0, EXPAND | ALL, 10)
        self.Sizer.Add(btn_sizer, 0, EXPAND | ALL, 10)

        self.Fit()
        self.Bind(EVT_CHAR_HOOK, self.__OnCharHook)

    def GetDataBufferSizeContainer(self):
        return self.__data_buffer_size_ety.GetArgumentContainer()

    def __OnCharHook(self, event):
        event.Skip()
        if all([ety.HasValidValue() for ety in [self.__data_buffer_size_ety]]):
            self.__ok_btn.Enable()
        else:
            self.__ok_btn.Disable()


def GetNextStr(prev, keycode, selection):
    p, s = selection
    var = chr(keycode)
    if var == '' or keycode in [9, 229]:
        return prev

    if keycode == 8:
        p -= 1 if selection[0] == selection[1] else 0
        var = ''
    if keycode == 127:
        s += 1 if selection[0] == selection[1] else 0
        var = ''

    return '%s%s%s' % (prev[:p], var, prev[s:])


__all__ = [
    'NormalText',
    'NormalLine',
    'NormalEntry',
    'NormalComboBox',
    'NormalButton',
    'OkButton',
    'CancelButton',
    'SetButton',
    'ExecuteButton',
    'RegisterButton',
    'BrowseButton',
    'PreviewButton',
    'ClearButton',
    'SaveButton',
    'DontSaveButton',
    'AddButton',
    'CloseButton',
    'HelpButton',
    'Colorbar',
    'ColorSliderCtrl',
    'ColormapEntry',
    'ArgumentContainerEntryBase',
    'ValidatableEntry',
    'ValidateEntry',
    'ValidateStrEntry',
    'ValidateIterableEntryBase',
    'ValidateIterableEntry',
    'ValidateListEntry',
    'ValidateTupleEntry',
    'ValidateChoiceEntry',
    'LabeledValidateEntry',
    'DelimiterEntry',
    'FunctionArgumentEntry',
    'FunctionEntry',
    'FunctionListEntry',
    'NewDialog',
    'ExportDialog',
    'DataPreviewDialog',
    'ProjectMemoDialog',
    'RegisterDialog',
    'SaveCheckDialog',
    'PreferenceDialog',
]

if __name__ == "__main__":
    from wx import App, Frame

    from objects import (ChoiceContainer, FloatContainer,
                         FunctionContainerBase, IntContainer,
                         OptionalIntContainer)

    app = App()
    frame = Frame(None)

    class TestFunction(FunctionContainerBase):
        def __init__(self):
            int_ = IntContainer(min_=0, max_=8)
            float_ = FloatContainer(min_=0.0, max_=9)
            str_ = StrContainer('piho')
            choice = ChoiceContainer('puyo', ['puyo', 'foo', 'hoge'])
            list_ = ListArgumentContainer([int_, float_, str_])
            tuple_ = TupleArgumentContainer([int_, float_, str_, list_])
            arg_container_dict = {'int': int_, 'choice': choice, 'float': float_, 'str': str_, 'tuple': tuple_}
            # self.__arg_container_list = [tuple_]
            super().__init__(arg_container_dict)

        def Function(self):
            pass

    # ety = FunctionEntry(TestFunction(), parent=frame)
    # int_ = IntContainer(min_=0, max_=8)
    # float_ = FloatContainer(min_=0.0, max_=9)
    # str_ = StrContainer('piho')
    # choice = ChoiceContainer('puyo', ['puyo', 'foo', 'hoge'])
    # list_ = ListArgumentContainer([int_, float_, str_])
    # ety = ValidateStrEntry(str_, parent=frame)
    # ety = ValidateListEntry(list_, parent=frame)
    optional_int_ety = LabeledValidateEntry('hoge', OptionalIntContainer(None, 0, 10), parent=frame)
    frame.Show()
    app.MainLoop()
