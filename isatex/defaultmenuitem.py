from copy import deepcopy
from random import random

from matplotlib.pyplot import axis, colorbar, pcolormesh, show
from numpy import array, inf, meshgrid
from wx import (DEFAULT_DIALOG_STYLE, FD_FILE_MUST_EXIST, FD_OPEN, FD_SAVE,
                ICON_NONE, ID_CANCEL, FileDialog, LogError, MessageDialog)

from .const import (ABOUT_MENU_ITEM, DATA_MANAGER, DECODE_MANAGER,
                   ENCODE_MANAGER, EXPORT_MENU_ITEM, EXPORT_PLUGIN_MENU_ITEM,
                   FUNCTION_MANAGER, IMPORT_PLUGIN_MENU_ITEM, LAYOUT_MENU,
                   MENUBAR_MANAGER, NEW_MENU_ITEM, NEW_MENU_ITEM_HELP,
                   OPEN_MENU_ITEM, PANEL_MANAGER, PREFERENCE_MANAGER,
                   PREFERENCE_MENU_ITEM, PROJECT_MANAGER,
                   PROJECT_MEMO_MENU_ITEM, SAVE_AS_MENU_ITEM, SAVE_MENU_ITEM,
                   SAVEFILE_WILDCARD, TUTORIAL_MENU_ITEM)
from .container import CustomNormalMenuItemBase
from .control import (ExportDialog, NewDialog, PreferenceDialog,
                     ProjectMemoDialog)
from .objects import DEFAULT_PEAK, DataContainer, Spectrum


class NewMenuItem(CustomNormalMenuItemBase):
    """Menu item for loading a new project
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(NEW_MENU_ITEM, NEW_MENU_ITEM_HELP)

    def Function(self):
        """loading a new project
        """
        encoding = self.Get(ENCODE_MANAGER).GetEncoding()
        delimiter = self.Get(ENCODE_MANAGER).GetDelimiter()
        selected_function = self.Get(ENCODE_MANAGER).GetEncodeFunctionNameContainer()
        encode_function_list = self.Get(FUNCTION_MANAGER).GetEncodeFunctionList()
        data_buffer_size = self.Get(PREFERENCE_MANAGER).GetDataBufferSize()

        with NewDialog(encoding, delimiter, selected_function, encode_function_list, data_buffer_size, parent=None, title='New') as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            encoding = dialog.GetEncoding()
            delimiter = dialog.GetDelimiter()
            selected_function = dialog.GetSelectedEncodeFunction()

            data_list = dialog.GetDataList()

        self.Get(ENCODE_MANAGER).SelectEncoding(encoding)
        self.Get(ENCODE_MANAGER).SelectDelimiter(delimiter)
        self.Get(FUNCTION_MANAGER).SelectEncodeFunction(selected_function)

        if len(data_list) == 0:
            print('error?')
            return

        self.Get(PROJECT_MANAGER).NewProject(data_list)


class OpenMenuItem(CustomNormalMenuItemBase):
    """Menu item for loading an existing project
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(OPEN_MENU_ITEM, '')

    def Function(self):
        """loading an existing project
        """
        with FileDialog(None, wildcard=SAVEFILE_WILDCARD, style=FD_OPEN | FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            path = dialog.GetPath()

        self.Get(PROJECT_MANAGER).OpenProject(path)


class SaveMenuItem(CustomNormalMenuItemBase):
    """Menu item for saving a project
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(SAVE_MENU_ITEM, '')

    def Function(self):
        """saving a project
        """
        project_mgr = self.Get(PROJECT_MANAGER)
        if project_mgr.IsProjectSaved():
            return

        project = self.Get(PROJECT_MANAGER).GetProject()

        if project.GetPath() == '':
            return self.Get(MENUBAR_MANAGER).ExecuteMenuFunction(SAVE_AS_MENU_ITEM)

        self.Get(PROJECT_MANAGER).SaveProject(project)
        return True

    def OnLaunch(self):
        self.Enable(False)

    def OnProjectLoad(self, event):
        self.Enable()


class SaveAsMenuItem(CustomNormalMenuItemBase):
    """Menu item to save an unsaved project
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(SAVE_AS_MENU_ITEM, '')

    def Function(self) -> bool:
        """save an unsaved project

        :return: Whether the project has been saved or not.
        :rtype: bool
        """
        project_mgr = self.Get(PROJECT_MANAGER)
        project = project_mgr.GetProject()

        if (path := project.GetPath()) == '':
            path = project_mgr.GetDefaultProjectPath()

        dir_path = project.GetDirectory()
        file_name = project.GetFileName()

        with FileDialog(parent=None, defaultDir=dir_path, defaultFile=file_name, wildcard=SAVEFILE_WILDCARD, style=FD_SAVE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return False

            path = dialog.GetPath()

        project.SetPath(path)

        project_mgr.SaveProject(project)
        return True

    def OnLaunch(self):
        self.Enable(False)

    def OnProjectLoad(self, event):
        self.Enable()


class ExportMenuItem(CustomNormalMenuItemBase):
    """Menu item for outputting experimental data.
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(EXPORT_MENU_ITEM, '')

    def Function(self):
        """Outputting experimental data.
        """
        project = self.Get(PROJECT_MANAGER).GetProject()
        encoding = self.Get(DECODE_MANAGER).GetEncoding()
        selected_function = self.Get(FUNCTION_MANAGER).GetSelectedDecodeFunction()
        func_list = self.Get(FUNCTION_MANAGER).GetDecodeFunctionList()

        with ExportDialog(project, encoding, selected_function, func_list, parent=None, title='Export') as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            selected_function = dialog.GetSelectedDecodeFunction()

        self.Get(FUNCTION_MANAGER).SelectDecodeFunction(selected_function)

    def OnLaunch(self):
        self.Enable(False)

    def OnProjectLoad(self, event):
        self.Enable()


# class PluginImportMenuItem(CustomNormalMenuItemBase):
#     def __init__(self):
#         super().__init__(IMPORT_PLUGIN_MENU_ITEM, '')

#     def Function(self):
#         print('plugin import')


# class PluginExportMenuItem(CustomNormalMenuItemBase):
#     def __init__(self):
#         super().__init__(EXPORT_PLUGIN_MENU_ITEM, '')

#     def Function(self):
#         print('plugin export')


class ProjectMemoMenuItem(CustomNormalMenuItemBase):
    """Menu item for making notes about the project.
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(PROJECT_MEMO_MENU_ITEM, '')

    def Function(self):
        """Making notes about the project.
        """
        project = self.Get(PROJECT_MANAGER).GetProject()
        prev_date = project.GetExperimentalDate()
        prev_note = project.GetNote()

        with ProjectMemoDialog(prev_date, prev_note, parent=None) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            date = dialog.GetDate()
            note = dialog.GetNote()

        if prev_date == date and prev_note == note:
            return

        self.Get(PROJECT_MANAGER).SetProjectMemo(date, note)

    def OnLaunch(self):
        self.Enable(False)

    def OnProjectLoad(self, event):
        self.Enable()


# class FTIR_WarterContentsMappingMenuItem(CustomNormalMenuItemBase):
#     def __init__(self):
#         super().__init__('FTIR Warter Mapping', '')

#     def Function(self):
#         K = 36.37

#         data_list = self.Get(PROJECT_MANAGER).GetDataList()
#         x_list = [data.X for data in data_list]
#         y_list = [data.Y for data in data_list]

#         self.FTIR_WaterContentMapping(K, x_list, y_list, 4, 3)

#     def FTIR_WaterContentMapping(self, K, x_list, y_list, cols, rows, direction='r2d', cmap='jet', clim=(0, None)):
#         if not (len(x_list) == len(y_list) == cols * rows):
#             LogError('Map size is incorrect.')
#             return

#         warter_contents_list = []
#         for x, y in zip(x_list, y_list):
#             t = self.EstimateThickness(x, y, (1624.9, 2150.1), 1 / 0.6366)
#             if t == 0:
#                 LogError('Could not be calculated.\nThe data may not be adequate.')
#             G1 = self.EstimateThickness(x, y, (3414.9, 3653.1))
#             G2 = self.EstimateThickness(x, y, (3264.9, 3415.1))
#             G3 = self.EstimateThickness(x, y, (3264.9, 3415.1))

#             warter_contents = self.EstimateWarterContents(K, t, G1, G2, G3)
#             warter_contents_list.append(warter_contents)

#         lower_clim, upper_clim = clim
#         if lower_clim is None:
#             lower_clim = 0
#         if upper_clim is None:
#             upper_clim = max(warter_contents_list)

#         C = array(warter_contents_list).reshape([rows, cols])

#         x_grid = [i for i in range(cols + 1)]
#         y_grid = [i for i in range(rows + 1)]
#         X, Y = meshgrid(x_grid, y_grid)
#         # coordinate = array([[[x, y] for x in range(cols + 1)] for y in range(rows + 1)])
#         pcolormesh(X, Y, C, vmin=lower_clim, vmax=upper_clim, cmap=cmap)
#         colorbar()
#         axis('equal')
#         show()

#     def EstimateThickness(self, xdata, ydata, bounds=(-inf, inf,), rate=1):
#         if len(xdata) != len(ydata):
#             raise TypeError('"x" and "y" should be the same length.')

#         lower_bound, upper_bound = bounds
#         matched_index = [index for index, x in enumerate(xdata) if lower_bound < x < upper_bound]

#         clipped_xdata = array([xdata[i] for i in matched_index])
#         clipped_ydata = array([ydata[i] for i in matched_index])

#         if len(clipped_xdata) == 0:
#             return 0

#         total_area = sum([abs(y) for y in clipped_ydata])

#         upper_base = clipped_ydata[-1]
#         lower_base = clipped_ydata[0]
#         # height = clipped_xdata[-1] - clipped_xdata[0]  # 元のやつだと面積が負になる可能性がある
#         height = abs(clipped_xdata[-1] - clipped_xdata[0])
#         base_area = (upper_base + lower_base) * height / 2

#         return (total_area - base_area) * rate

#     def EstimateWarterContents(self, K, t, G1, G2, G3):
#         return 1e5 / t * 3.5 * K * ((G1 / (3780 - 3572)) + (G2 / (3780 - 3328)) + (G3 / (3780 - 3228)))


# class LayoutMenuItem(CustomNormalMenuItemBase):
#     def __init__(self):
#         super().__init__(LAYOUT_MENU_ITEM, '')

#     def Function(self):
#         mgr = self.Get(PANEL_MANAGER)
#         prev_name, _ = mgr.GetSelectedLayout()
#         name_list = mgr.GetLayoutNames()

#         with RegisterDialog(name_list, mgr, parent=None) as dialog:
#             if dialog.ShowModal() == ID_CANCEL:
#                 return

#             name = dialog.GetName()

#         mgr.RegisterCurrentLayout(name)


class AboutMenuItem(CustomNormalMenuItemBase):
    """Menu item to display about this app
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(ABOUT_MENU_ITEM, '')

    def Function(self):
        contents = 'Copyright (c) 2021 ryoTd0112'
        with MessageDialog(None, contents, caption='About', style=DEFAULT_DIALOG_STYLE | ICON_NONE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return


class TutorialMenuItem(CustomNormalMenuItemBase):
    """Menu item to tutorial.
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(TUTORIAL_MENU_ITEM, '')

    def Function(self):
        project_mgr = self.Get(PROJECT_MANAGER)
        is_success = project_mgr.AskProjectSaving()
        if not is_success:
            return

        data_buffer_size = self.Get(PREFERENCE_MANAGER).GetDataBufferSize()
        amp, ctr, wid = 1, 5, 30
        data_list = []
        peak = deepcopy(DEFAULT_PEAK)

        peak.Amp = amp
        peak.Wid = wid

        for i in range(90):
            x = array(list(range(100)))
            peak.Ctr = ctr + i
            y = [v + (random() - 0.5) * 0.05 for v in peak.Execution(x)]

            spectrum = Spectrum(x, y)
            path = f'./tutorial_data{i + 1:02}'
            data = DataContainer(path, data_buffer_size)
            data.Append(spectrum, msg=path)

            data_list.append(data)

        project_mgr.NewProject(data_list)


class PreferenceMenuItem(CustomNormalMenuItemBase):
    """Menu item for setting application preferences.
    """

    def __init__(self):
        """Default constructor
        """
        super().__init__(PREFERENCE_MENU_ITEM, '')

    def Function(self):
        """Setting application preferences.
        """
        data_buffer_size_container = self.Get(PREFERENCE_MANAGER).GetDataBufferSizeContainer()
        with PreferenceDialog(data_buffer_size_container, parent=None, title='Preference') as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return

            data_buffer_size_container = dialog.GetDataBufferSizeContainer()

        self.Get(PREFERENCE_MANAGER).SetDataBufferSize(data_buffer_size_container)


__all__ = [
    'NewMenuItem',
    'OpenMenuItem',
    'SaveMenuItem',
    'SaveAsMenuItem',
    'ExportMenuItem',
    'ProjectMemoMenuItem',
    'AboutMenuItem',
    'TutorialMenuItem',
    'PreferenceMenuItem',
]
