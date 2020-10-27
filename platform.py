import wx
import abc
from formatter import ShellFormatter


class Platform(abc.ABC):

    @abc.abstractmethod
    def get_current_line(self):
        """
        get the content of the whole current line
        :return:
        """

    @abc.abstractmethod
    def get_current_length(self):
        """
        get the length of the whole current line
        :return:
        """

    @abc.abstractmethod
    def get_current_input(self, prompt):
        """
        get the user input part of the current line
        :return:
        """

    @abc.abstractmethod
    def clr_current_input(self, prompt):
        """
        clear the user input part but keep prompt part of the current line
        :return:
        """

    @abc.abstractmethod
    def connect_event_handler(self, event, handler):
        """
        bind handler to event in this GUI platform realization
        :param event:
        :param handler:
        :return:
        """

    @abc.abstractmethod
    def remap_event_string(self, event_string):
        """
        convert given event string to its event counterpart
        in this GUI realization
        :param event_string:
        :return:
        """

    @abc.abstractmethod
    def writer(self, output, formatter):
        """

        :param output:
        :param formatter:
        :return:
        """

    @abc.abstractmethod
    def configure_resources(self, conf_dict):
        """
        read settings from configurations dict
        :param conf_dict:
        :return:
        """


class ShellPlatform(Platform):

    # ---- Constructor & Initialization ----#
    def __init__(self) -> None:
        """
        Here, we just set parameters needed, the real GUI building
        job will be done at another place
        """
        self._setup_default_parameters()
        self._setup_graphical_interface()

    def _setup_default_parameters(self):
        self.fg = (0, 0, 0)
        self.bg = (255, 255, 255)
        self.title = 'Shell Session'
        self.width = 1000
        self.height = 500
        self.font = 'Consolas'
        self.size = 15

    def _setup_graphical_interface(self):
        """
        Setup graphical interface environment
        """
        self.app = wx.App()

        self.root = wx.Frame(parent=None, size=(self.width, self.height))
        self.inter = wx.TextCtrl(parent=self.root, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_CHARWRAP | wx.TE_RICH2)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.inter, 1, wx.EXPAND | wx.ALL, 0)

        # self.inter.SetCaret()
        self.inter.SetBackgroundColour(self.bg)
        self.inter.SetForegroundColour(self.fg)
        self.inter.SetFont(wx.Font(wx.FontInfo(self.size).FaceName(self.font)))
        self.root.SetSizer(self.sizer)
        self.root.SetLabel(self.title)
        self.root.Center()

    # ---- Attributes Setter & Getter ----#
    def set_attr_title(self, title):
        self.title = title

    def set_attr_width(self, width):
        self.width = width

    def set_attr_height(self, height):
        self.height = height

    def set_attr_font(self, font):
        self.font = font

    def set_attr_size(self, size):
        self.size = size

    # ---- External Interfaces ----#
    def commence_platform(self, prompt):
        """
        show platform and start main loop
        """
        self.root.Show()
        self.inter.SetDefaultStyle(ShellFormatter.attr_formatter('prompt'))
        self.inter.write(prompt)
        self.app.MainLoop()

    def get_current_line(self):
        """
        get the whole current inputting line including prompt
        """
        return self.inter.GetLineText(self.inter.GetNumberOfLines()-1)

    def get_current_length(self):
        """
        get the length of the current line including prompt
        """
        return self.inter.GetLineLength(self.inter.GetNumberOfLines()-1)

    def get_caret_position(self):
        """
        get the current caret position in current inputting line
        """
        curr_len = self.inter.GetLineLength(self.inter.GetNumberOfLines()-1)
        curr_pos = self.inter.GetInsertionPoint()
        curr_tot = self.inter.GetLastPosition()
        return curr_len-(curr_tot-curr_pos)

    def set_caret_position(self, position):
        """
        set the caret position for writing
        """
        self.inter.SetInsertionPoint(position)

    def get_current_input(self, prompt):
        """
        get the current user input string excluding prompt
        """
        line = self.inter.GetLineText(self.inter.GetNumberOfLines()-1)
        return line[len(prompt):].strip()

    def clr_current_input(self, prompt):
        """
        remove current user input string but keep prompt
        """
        final_pos = self.inter.GetLastPosition()
        curr_len = self.inter.GetLineLength(self.inter.GetNumberOfLines()-1)
        start_pos = final_pos - (curr_len-len(prompt))
        self.inter.Remove(start_pos, final_pos)

    def get_character_response(self):
        return self.inter.GetLineText(self.inter.GetNumberOfLines()-1)[-1]

    def get_column_count(self):
        return self.inter.GetSize()[0] / self.inter.GetCharWidth()

    def remap_event_string(self, event_string):
        """
        convert event string to its event counterpart in wxPython
        :param event_string:
        :return:
        """
        if event_string == "keyboard_event":
            return wx.EVT_KEY_DOWN
        elif event_string == "command_event":
            return wx.EVT_TEXT_ENTER
        elif event_string == "mouse_event":
            #return wx.EVT_LEFT_DOWN
            return wx.EVT_MOUSE_EVENTS
        elif event_string == "mouse_click_event":
            return wx.EVT_LEFT_DOWN
        elif event_string == 'mouse_wheel_event':
            return wx.EVT_MOUSEWHEEL
        elif event_string == 'mouse_dclick_event':
            return wx.EVT_LEFT_DCLICK
        elif event_string == 'mouse_motion_event':
            return wx.EVT_MOTION
        elif event_string == "character_event":
            return wx.EVT_TEXT
        else:
            raise Exception("unknown event string: %s" % event_string)

    def reader(self, prompt, classname='prompt'):
        self.inter.SetDefaultStyle(ShellFormatter.attr_formatter(classname))
        self.inter.write(prompt)
        #self.inter.SetFont(ShellFormatter.font_formatter())
        self.inter.SetDefaultStyle(ShellFormatter.attr_formatter('buffer'))

    def writer(self, output, classname='output'):
        self.inter.SetDefaultStyle(ShellFormatter.attr_formatter(classname))
        self.inter.write(output)

    def connect_event_handler(self, event_string, handler):
        if not callable(handler):
            raise Exception("%s: handler not callable" % repr(handler))

        event = self.remap_event_string(event_string)
        self.inter.Bind(event, handler)

    def disconnect_event_handler(self, event_string, handler):
        if not callable(handler):
            raise Exception("%s: handler not callable" % repr(handler))

        event = self.remap_event_string(event_string)
        self.inter.Unbind(event, handler)

    def configure_resources(self, conf_dict):
        pass