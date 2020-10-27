import os
import wx
import shutil
import configparser
import callback
from parser import ShellParser
from recorder import ShellRecorder
from platform import ShellPlatform
from formatter import ShellFormatter


class ShellSession:

    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.config = {
            'conf':   'resources.conf',
            'prompt': '>> ',
            'db': 'database',
            'cal': 'calibrates',
            'lin': 'linearfits',
            'der': 'derivative',
            'lab': 'laboratory',
        }

        self.engine = 'wxpython'
        self.events = ['keyboard_event',
                       'command_event',
                       'character_event',
                       'mouse_event',
                       'mouse_click_event',
                       'mouse_wheel_event',
                       'mouse_dclick_event',
                       'mouse_motion_event']

        self.event_handlers = {}
        self.kbhit_accelers = {}

        self.parser = ShellParser()
        self.platform = ShellPlatform()
        self.recorder = ShellRecorder()
        # self.completer = ShellCompleter()
        # self.formatter = ShellFormatter()

    def configure_configuration_resources(self):
        """
        read settings from resource file for shell
        """
        path = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(path, self.config['conf'])
        if not os.path.exists(file):
            print("config not exists")
            return
        if not os.path.isfile(file):
            print("config not regular file")
            return

        parser = configparser.ConfigParser()
        parser.read(file)
        for section in parser.sections():
            if section == 'Booleans':
                for option in parser.options('Booleans'):
                    self.config.update({option: parser.getboolean('Booleans', option)})
            elif section == 'Integers':
                for option in parser.options('Integers'):
                    self.config.update({option: parser.getint('Integers', option)})
            elif section == 'Floats':
                for option in parser.options('Floats'):
                    self.config.update({option: parser.getfloat('Floats', option)})
            # now, we should process style rules for displaying text
            elif section == 'STYLES':
                for option in parser.options('STYLES'):
                    ShellFormatter.add_style_rule(option, parser.get('STYLES', option))

                print(ShellFormatter.rules)
            elif section == "PATH":
                for option in parser.options('PATH'):
                    self.config.update({option: parser.get('PATH', option).split(':')})
            else:
                self.config.update(parser.items(section))

        #print(self.config['sources'])
        #print(self.config['dests'])
        if not self.config['prompt'].endswith(' '):
            self.config['prompt'] += ' '

    @staticmethod
    def check_directory(path, dir):
        dest = os.path.join(path, dir)
        if not os.path.exists(dest):
            print("make directory: %s" % dest)
            os.mkdir(dest)
            return
        if not os.path.isdir(dest):
            print("make directory: %s" % dest)

    def configure_directory_structure(self):
        """
        check directories into which we need to store files
        :return:
        """
        self.check_directory(self.root, self.config['db'])
        self.check_directory(self.root, self.config['cal'])
        self.check_directory(self.root, self.config['lin'])
        self.check_directory(self.root, self.config['der'])
        self.check_directory(self.root, self.config['lab'])

    def add_event_handler(self, event, handler):
        """
        add event handler to shell
        :param event:
        :param handler:
        :return:
        """
        if not isinstance(event, str):
            raise Exception("event should be string")
        if event not in self.events:
            raise Exception("%s: event not supported" % event)
        self.event_handlers.update({event: handler})
        self.platform.connect_event_handler(event, handler)

    def del_event_handler(self, event):
        """
        remove event handler from shell
        :param event:
        :return:
        """
        if not isinstance(event, str):
            raise Exception("event should be string")
        if event not in self.events:
            raise Exception("%s event not supported" % event)
        if event not in self.event_handlers:
            return
        handler = self.event_handlers.pop(event)
        self.platform.disconnect_event_handler(event, handler)

    def add_kbhit_acceler(self, keystroke, acceler):
        """
        add keyboard hit accelerator to shell
        :param keystroke: 'ctrl-U', 'ctrl-alt-U' etc.
        :param acceler:
        :return:
        """
        self.kbhit_accelers.update({keystroke: acceler})

    def keyboard_event_handler(self, event):
        """
        handler for keyboard input event
        :param event:
        :return:
        """
        if event.GetModifiers() == wx.MOD_CONTROL:
            if event.GetKeyCode() == ord('U'):
                print("ctrl-u hit")
        elif event.GetModifiers() == wx.MOD_CONTROL|wx.MOD_SHIFT:
            if event.GetKeyCode() == ord('U'):
                print("ctrl-U hit")

        keycode = event.GetKeyCode()

        if keycode == wx.WXK_BACK or keycode == wx.WXK_LEFT:
            if self.platform.get_caret_position() > len(self.config['prompt']):
                event.Skip()
        elif keycode == wx.WXK_TAB:
            print("tab hit")
        elif keycode == wx.WXK_UP:
            if not self.recorder.empty():
                if not self.recorder.status():
                    self.recorder.append(self.platform.get_current_input(self.config['prompt']))
                self.platform.clr_current_input(self.config['prompt'])
                self.platform.writer(self.recorder.prev())
        elif keycode == wx.WXK_DOWN:
            if not self.recorder.empty():
                self.platform.clr_current_input(self.config['prompt'])
                self.platform.writer(self.recorder.next())
        elif keycode == wx.WXK_ESCAPE:
            self.recorder.rewind()
        elif keycode == wx.WXK_CAPITAL:
            #self.platform.writer(chr(keycode), 'command')
            print("caps lock")
        else:
            #print("%c" % chr(event.GetUnicodeKey()))
            event.Skip()

    def command_event_handler(self, event):
        """
        handler for command entering event
        :param event:
        :return:
        """
        curr_line = self.platform.get_current_line()
        curr_comm = curr_line[len(self.config['prompt']):].strip()

        # rewind recorder
        if self.recorder.status():
            self.recorder.rewind()
        # if command not empty, it should be added to recorder
        if curr_comm:
            self.recorder.commit(curr_comm)
        # start processing
        self.platform.writer('\n')
        self.parser.parse(self, self.platform, curr_comm)
        #self.platform.writer('\n')
        self.platform.reader(self.config['prompt'])
        # self.platform.writer(self.config['prompt'])

    def click_event_handler(self, event):
        print("click event")

    def wheel_event_handler(self, event):
        print("wheel event")

    def dclick_event_handler(self, event):
        print("double click event")

    def motion_event_handler(self, event):
        print("motion event")

    def character_event_handler(self, event):
        """
        handler for reading interactive character response
        :param event:
        :return:
        """
        self.character = self.platform.get_character_response()
        print("character: %c" % self.character)
        self.del_event_handler("character_event")

    def get_character_response(self):
        return self.character

    def connect_command_collection(self):
        """
        add all needed commands from here to shell
        :return:
        """
        self.parser.append_element('list-dest', 'listdest', 'listdes', 'listdet', callback=callback.list_dest, description="list dest path")
        self.parser.append_element('list-source', 'listsrc', callback=callback.list_source, description='list source path')
        self.parser.append_element('list-calibrates', 'listcal', prototype={'src': 'str'}, callback=callback.list_calibrates, description='list calibrates files')
        self.parser.append_element('list-linearfits', 'listlin', prototype={'src': 'str'}, callback=callback.list_linearfits, description='list linearfits files')
        self.parser.append_element('list-derivative', 'listder', prototype={'src': 'str'}, callback=callback.list_derivative, description='list derivative files')
        self.parser.append_element('make-calibrates', 'makecal', prototype={'src': 'str', 'dest': 'str'}, callback=callback.make_calibrates, description='make calibrates files')
        self.parser.append_element('make-linearfits', 'makelin', prototype={'src': 'str', 'dest': 'str'}, callback=callback.make_linearfits, description='make linearfits files')
        self.parser.append_element('make-derivative', 'makeder', callback=callback.make_derivative, description='make derivative files')

    def commence_running(self):
        """
        commence shell running since here
        :return:
        """
        self.platform.commence_platform(self.config['prompt'])
