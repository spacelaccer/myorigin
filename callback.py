import os
import re
import shutil


def list_source(shell, platform, parser, *args, **kwargs):
    """
    list all source directories for any possible file operations
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    index = 0
    for source in shell.config['sources']:
        index += 1
        platform.writer("source path %s: " % str(index), "command")
        platform.writer("%s\n" % source, "output")


def list_dest(shell, platform, parser, *args, **kwargs):
    """
    list all destination directories for any possible file operations
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    index = 0
    for dest in shell.config['dests']:
        index += 1
        platform.writer("dest path %s: " % str(index), "output")
        platform.writer("%s\n" % dest, "output")


def list_calibrates(shell, platform, parser, *args, **kwargs):
    """
    list all calibrates files under the given source path
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    if 'src' not in kwargs:
        if shell.config['sources']:
            source = shell.config['sources'][0]
        else:
            platform.writer("no source path given\n", "error")
            return
    else:
        source = kwargs['src']
        if not os.path.exists(source):
            platform.writer("%s: source path not exists\n" % source, "error")
            return

    calibrates = []
    max_chars = 0
    for filename in os.listdir(source):
        if filename.endswith(".pCal") or filename.endswith(".fCal"):
            calibrates.append(filename)
            if len(filename) > max_chars:
                max_chars = len(filename)

    if not calibrates:
        platform.writer('%s: no calibrates found\n' % source)
        return
    columns = int((platform.get_column_count() - 1) / (max_chars + 2))  # separated by 2 spaces, start with 1 space
    column = 0
    for filename in calibrates:
        column += 1
        if column == 1:
            platform.writer(' ')
        platform.writer("%s  " % filename, "output")
        if column == columns:
            platform.writer('\n')
            column = 0
    if column != columns and column != 0:
        platform.writer('\n')


def list_linearfits(shell, platform, parser, *args, **kwargs):
    """
    list all linearfits files under the given source path
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    if 'src' not in kwargs:
        if shell.config['sources']:
            source = shell.config['sources'][0]
        else:
            platform.writer("no source path given\n", "error")
            return
    else:
        source = kwargs['src']
        if not os.path.exists(source):
            platform.writer("%s: source path not exists\n" % source, "error")
            return

    linearfits = []
    pattern = r'ZCF-301B\s+ST\d{3,5}\w{4,}-?\w{0,3}[.]xls$'
    for filename in os.listdir(source):
        if re.match(pattern, filename):
            linearfits.append(filename)

    if not linearfits:
        platform.writer("%s: no linearfits found\n" % source)
        return
    for filename in linearfits:
        platform.writer("%s\n" % filename, "output")


def list_derivative(shell, platform, parser, *args, **kwargs):
    """
    list all derivative files under the given source path
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    if 'src' not in kwargs:
        if shell.config['sources']:
            source = shell.config['sources'][0]
        else:
            platform.writer("no source path given\n", "error")
            return
    else:
        source = kwargs['src']
        if not os.path.exists(source):
            platform.writer("%s: source path not exists\n" % source, "error")
            return

    derivatives = []
    pattern = r'ZCF-301B\s+ST\d{3,5}\(\d{4}[.]\d{2}[.]\d{2}\)-?\w{0,3}$'
    for filename in os.listdir(source):
        derivative = os.path.join(source, filename)
        if os.path.isdir(derivative):
            platform.writer("directory found: %s\n" % derivative, "error")
        if os.path.isdir(derivative) and re.search(pattern, filename):
            derivatives.append(derivative)

    if not derivatives:
        platform.writer("%s: no derivative found\n" % source, "output")
        return
    for filename in derivatives:
        platform.writer("derivative found: %s\n" % filename, "output")


def make_calibrates(shell, platform, parser, *args, **kwargs):
    """
    copy wanted calibrates to  'laboratory directory'
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    print("args: %s" % repr(args))
    print("kwargs: %s" % repr(kwargs))

    if 'src' not in kwargs:
        if shell.config['sources']:
            source = shell.config['sources'][0]
        else:
            platform.writer("no source given\n", "error")
            return
    else:
        source = kwargs['src']
        if not os.path.exists(source):
            platform.writer("%s: source do not exist\n" % source, "error")
            return

    dest = os.path.join(shell.root, shell.config['lab'])
    if not os.path.exists(dest):
        platform.writer("%s: dest not exist\n" % dest, "error")

    calibrates = []
    for filename in os.listdir(source):
        for arg in args:
            if re.match(arg+"[.][pf]Cal", filename):
                print(filename)
                calibrates.append(os.path.join(source, filename))

    if not calibrates:
        platform.writer("%s: no calibrates found\n" % source, "error")
    for filename in calibrates:
        platform.writer("Making lab calibrate: %s\n" % filename)
        shutil.copy(filename, dest)

def make_linearfits(shell, platform, parser, *args, **kwargs):
    """
    copy linearfits to laboratory directory
    """
    print("args: %s" % repr(args))
    print("kwargs: %s" % repr(kwargs))

    if 'src' not in kwargs:
        if shell.config['sources']:
            source = shell.config['sources'][0]
        else:
            platform.writer("no source given\n", "error")
            return
    else:
        source = kwargs['src']
        if not os.path.exists(source):
            platform.writer("%s: source do not exist\n" % source, "error")

    dest = os.path.join(shell.root, shell.config['lab'])
    if not os.path.exists(dest):
        platform.writer("%s: dest not exist\n" % dest, "error")

    linearfits = []
    pattern = r'^ZCF-301B\s+ST\d{4,5}\w{4,}-?\w{0,3}[.]xls$'
    for filename in os.listdir(source):
        for arg in args:
            if re.match(pattern, filename) and re.search(arg, filename):
                print(filename)
                linearfits.append(os.path.join(source, filename))

    if not linearfits:
        platform.writer("%s: no linearfits found\n" % source, "error")
    for filename in linearfits:
        platform.writer("Making lab linearfit: %s\n" % filename)
        #shutil.copy(filename, dest)

def make_derivative(shell, platform, parser, *args, **kwargs):
    """
    create derivative by files present
    :param shell:
    :param platform:
    :param parser:
    :param args:
    :param kwargs:
    :return:
    """
    print("args: %s" % repr(args))
    print("kwargs: %s" % repr(kwargs))

    path = os.path.join(shell.root, shell.config['lab'])
    if not os.path.exists(path):
        platform.writer("%s: directory not exists\n" % path, "error")
        return

    pres_calibrates = []
    flow_calibrates = []
    flow_linearfits = []
    file_derivative = []

    pres_pattern = r'^(?P<number>\d{4,5})[.]pCal$'
    flow_pattern = r'^(?P<number>\d{4,5})[.]fCal$'
    lfit_pattern = r'^ZCF-301B\s+ST\d{4,5}\w{4,}-?\w{0,3}[.]xls$'
    derv_pattern = r'ZCF-301B\s+ST\d{3,5}\(\d{4}[.]\d{2}[.]\d{2}\)-?\w{0,3}$'

    for filename in os.listdir(path):
        if filename.endswith("Cal"):
            if re.match(pres_pattern, filename):  # pressure calibrates
                pres_calibrates.append(filename)
            elif re.match(flow_pattern, filename): # flow calibrates
                flow_calibrates.append(filename)
            else:
                continue
        elif filename.startswith("ZCF-301B"):
            if re.match(lfit_pattern, filename):  # linearfits
                flow_linearfits.append(filename)
            elif re.match(derv_pattern, filename):  # derivative
                file_derivative.append(filename)
            else:
                continue
        else:
            continue
