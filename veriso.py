# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VeriSO
                                 A QGIS plugin
 Verification application module for Interlis data.
                              -------------------
        begin                : 2014-07-28
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Stefan Ziegler
        email                : edi.gonzales@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import resources_rc

from veriso_dialog import VeriSODialog
import os.path


class VeriSO:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'VeriSO_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = VeriSODialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&VeriSO')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'VeriSO')
        self.toolbar.setObjectName(u'VeriSO')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VeriSO', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        icon_path = ':/plugins/veriso/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'VeriSO'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # main toolbar
        self.toolBar = self.iface.addToolBar("VeriSO")
        self.toolBar.setObjectName("VeriSO.Main.ToolBar")
        self.toolBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))        

        # projects
        self.menuBarProjects = QMenuBar()
        self.menuBarProjects.setObjectName("VeriSO.Main.ProjectsMenuBar")                
        self.menuBarProjects.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
        self.menuProjects = QMenu()
        self.menuProjects.setTitle(self.tr("Projects"))
        self.menuBarProjects.addMenu(self.menuProjects)

        # files
        self.menuBarFile= QMenuBar()
        self.menuBarFile.setObjectName("VeriSO.Main.FileMenuBar")        
        self.menuBarFile.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.menuFile = QMenu()
        self.menuFile.setTitle(self.tr("File"))

        self.import_project = QAction(self.tr("Import project"), self.iface.mainWindow())
        self.import_project.triggered.connect(self.doImportProject)
        self.delete_project = QAction(self.tr("Delete project"), self.iface.mainWindow())    
        self.delete_project.triggered.connect(self.doDeleteProject)
        self.menuFile.addActions([self.import_project, self.delete_project])
        self.menuBarFile.addMenu(self.menuFile) 
        
        # settings
        self.menuBarSettings = QMenuBar()
        self.menuBarSettings.setObjectName("VeriSO.Main.SettingsMenuBar")
        self.menuBarSettings.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))        
        self.menuSettings = QMenu()
        self.menuSettings.setTitle(self.tr("Settings"))
        
        self.options = QAction(self.tr("Options"), self.iface.mainWindow())
        self.options.triggered.connect(self.doOptions)
        self.menuSettings.addActions([self.options])
        self.menuBarSettings.addMenu(self.menuSettings)        
        
        
        
        # add menus to toolbar
        self.toolBar.addWidget(self.menuBarProjects) 
        self.toolBar.addWidget(self.menuBarFile)
        self.toolBar.addWidget(self.menuBarSettings)
        
    def doImportProject(self):
        print "import"       
        from base.file.doImportProject import ImportProjectDialog
        self.import_dlg = ImportProjectDialog(self.iface.mainWindow())
        ret = self.import_dlg.initGui()
        print ret
        if ret:
            self.import_dlg.show()
        
        
    def doDeleteProject(self):
        print "delete"
        
        
    def doOptions(self):
        print "fooo"
        from base.settings.doOptions import OptionsDialog
        self.options_dlg = OptionsDialog(self.iface.mainWindow())
        self.options_dlg.initGui()
        self.options_dlg.show()
        self.options_dlg.projectsDatabaseHasChanged.connect(self.doLoadProjectsDatabase)
        
    def doLoadProjectsDatabase(self):
        print "dodooododododo"
#        from base.projects.doLoadProjectsDatabase import LoadProjectsDatabase
#        d = LoadProjectsDatabase(self.iface.messageBar())
#        projects = d.read()
#        
#        if projects != None:
#            groupedProjects = {}
#            for project in projects:
#                moduleName = project["appmodulename"]
#                try:
#                    moduleList = groupedProjects[moduleName]
#                except KeyError:
#                    moduleList = []
#                
#                moduleList.append(project)
#                groupedProjects[moduleName] = moduleList
#            
#            self.menuProjects.clear()
#            for key in sorted(groupedProjects.iterkeys()):
#                modules = groupedProjects[key]
#                groupMenu = self.menuProjects.addMenu(QCoreApplication.translate("Qcadastre", unicode(key)))
#                sortedProjectsList = sorted(modules, key=lambda k: k['displayname']) 
#                for project in sortedProjectsList:
#                    action = QAction(QCoreApplication.translate("QGeoApp", unicode(project["displayname"])), self.iface.mainWindow())
#                    groupMenu.addAction(action)
#                    QObject.connect(action, SIGNAL( "triggered()"), lambda activeProject=project: self.doLoadProject(activeProject))


    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&VeriSO'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
