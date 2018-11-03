
import os
import itertools
from PyQt5.QtWidgets import QFileDialog

def replace_default_var(string):
    string = string.replace("__HOME__", os.path.expanduser("~"))
    return string

def variablename(var):
    import itertools
    return [tpl[0] for tpl in
    itertools.ifilter(lambda x: var is x[1], globals().items())]

def from_ansi_to_html(string):
    string = str(string).replace('\n', '<br />')
    string = str(string).replace('\033[31m', '<div style="color:yellow;">')
    string = str(string).replace('\033[1m',  '<div style="font-weight: bold">')
    string = str(string).replace('\033[0m',  '</div>')
    string = str(string).replace('\033]2;',  '')
    string = str(string).replace('\a',  '')
    return string

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def select_file():
    lineEdit.setText(QFileDialog.getOpenFileName())
