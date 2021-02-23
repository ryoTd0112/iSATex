from abc import ABCMeta, abstractmethod
from util import RestrictedList, Singleton


class iSATexObject:
    """The base class for all iSATex objects, mainly used to distinguish which objects should be managed by the manager.
    """
    pass


class StorableObject(iSATexObject, metaclass=ABCMeta):
    """Inheriting from this class allows the application to save the state.
    """
    @abstractmethod
    def SendSaveData(self):
        """
            The application will store the value returned by this method.
            Return the value needed to restore the current state of the class.
            The only allowed types are Str, Int, Float, List, and Dict, Storable Object.

        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()

    @abstractmethod
    def ReceiveSaveData(self, save_data):
        """This method receives the value returned by "SendSaveData" as an argument. Restore the previous state.

        :param save_data: value of returned by "SendSaveData"
        :type save_data: [type]
        :raises NotImplementedError: Error sent if the method is not overridden.
        """
        raise NotImplementedError()


class CommunicableObjectBase(iSATexObject):
    """
    By inheriting from this class, it is possible to communicate with the following managers.
    MenubarManager,
    PanelManager,
    FunctionManager,
    EncodeManager,
    DecodeManager,
    ProjectManager,
    PeakManager,
    DataManager,
    SpectrumManager,
    MappingManager,
    ColorManager,
    PreferenceManager,

    Please refer to the documentation of each manager for details.
    """
    _core_mgr = None

    def Get(self, key, default=None):
        """Get manager by specifying the following keys.

        :param key: Key to specify
        :type key: Str
        :param default: Return value if the value corresponding to the specified key is not found., defaults to None
        :type default: Any, optional
        :return: The value corresponding to the specified key.
        :rtype: Any
        """
        return CommunicableObjectBase._core_mgr.Get(key, default)

    def SendEvent(self, event):
        """Send an event.

        :param event: An event containing information to be sent.
        :type event: iSATexEvent
        """
        CommunicableObjectBase._core_mgr.SendEvent(event)


class SettingStorableObjectBase(Singleton, iSATexObject):
    """Inherit this class when you want iSATex to save non-default settings until after the application is launched.
    """
    def RequireSetting(self) -> tuple:
        """The return value is used as the key to save the settings. The setting is stored as a dictionary, so it must be a unique value. This method is intended to be overridden.

        :return: name of the settings
        :rtype: tuple
        """
        # for override
        return tuple()

    def SendSetting(self) -> dict:
        """Save the return value to the configuration file. The key of the dictionary returned by this method should be consistent with the key specified in "RequireSetting". This method is intended to be overridden.

        :return: Settings to be saved
        :rtype: dict
        """
        # for override
        return dict()

    def ReceiveSetting(self, setting: dict):
        """The saved configuration will be passed as an argument. The key of the dictionary returned by this method should be consistent with the key specified in "RequireSetting". This method is intended to be overridden.

        :param setting: saved setting
        :type setting: dict
        """
        # for override
        pass


class RestrictedStorableListBase(RestrictedList, StorableObject):
    def __init__(self, ElementClass, *args, **kwargs):
        super().__init__(ElementClass, *args, **kwargs)
        super(RestrictedList, self).__init__()

    def SendSaveData(self):
        return [element for element in self]

    def ReceiveSaveData(self, save_data):
        self.clear()
        self.extend(save_data)


class ChameleonWidgetBase(iSATexObject):
    @classmethod
    def SetStyle(cls):
        pass


__all__ = [
    'iSATexObject',
    'StorableObject',
    'CommunicableObjectBase',
    'SettingStorableObjectBase',
    'RestrictedStorableListBase',
    'ChameleonWidgetBase',
]

