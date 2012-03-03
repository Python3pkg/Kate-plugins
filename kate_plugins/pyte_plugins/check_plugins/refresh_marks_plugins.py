import kate

from PyQt4 import QtCore

from kate_settings_plugins import kate_plugins_settings


def clearMarksOfError(doc, mark_iface):
    for line in range(doc.lines()):
        if mark_iface.mark(line) == mark_iface.Error:
            mark_iface.removeMark(line, mark_iface.Error)


@kate.action(**kate_plugins_settings['refreshMarks'])
def refreshMarks(doc=None, excludes=None, exclude_all=False):
    from pyte_plugins.check_plugins.parse_plugins import parseCode
    from pyte_plugins.check_plugins.pyflakes_plugins import checkPyflakes
    from pyte_plugins.check_plugins.pep8_plugins import checkPep8
    from jste_plugins.jslint_plugins import checkJslint
    if not doc or not doc.isModified():
        excludes = excludes or []
        currentDoc = doc or kate.activeDocument()
        mark_iface = currentDoc.markInterface()
        clearMarksOfError(currentDoc, mark_iface)
        show_popup = not excludes
        if not exclude_all:
            if not 'parseCode' in excludes:
                parseCode(currentDoc, refresh=False, show_popup=show_popup)
            if not 'checkPyflakes' in excludes:
                checkPyflakes(currentDoc, refresh=False, show_popup=show_popup)
            if not 'checkPep8' in excludes:
                checkPep8(currentDoc, refresh=False, show_popup=show_popup)
            if not 'checkJslint' in excludes:
                checkJslint(currentDoc, refresh=False, show_popup=show_popup)


def createSignalCheckDocument(view, *args, **kwargs):
    doc = view.document()
    doc.modifiedChanged.connect(refreshMarks)

windowInterface = kate.application.activeMainWindow()
windowInterface.connect(windowInterface,
                QtCore.SIGNAL('viewCreated(KTextEditor::View*)'),
                createSignalCheckDocument)
