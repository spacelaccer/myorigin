import os
from shell import ShellSession


shell = ShellSession()

# load config file
shell.configure_configuration_resources()
# check directories
shell.configure_directory_structure()

# shell.configure_platform_resources()
# shell.configure_parser_resources()
# shell.configure_output_resources()
# shell.configure_recorder_resources()
# shell.configure_completer_resources()

# load all available commands
shell.connect_command_collection()
# shell.connect_handler_collection()
# add event handlers
shell.add_event_handler("command_event", shell.command_event_handler)
shell.add_event_handler("keyboard_event", shell.keyboard_event_handler)
shell.add_event_handler("mouse_click_event", shell.click_event_handler)
shell.add_event_handler("mouse_wheel_event", shell.wheel_event_handler)
shell.add_event_handler("mouse_dclick_event", shell.dclick_event_handler)
#shell.add_event_handler("mouse_motion_event", shell.motion_event_handler)
# start running
shell.commence_running()

