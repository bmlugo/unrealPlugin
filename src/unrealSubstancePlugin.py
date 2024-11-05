import tkinter.filedialog
from unreal import (ToolMenus, ToolMenuContext, uclass, ufunction, ToolMenuEntryScript)

import os
import sys
import importlib
import tkinter

srcPath = os.path.dirname(os.path.abspath(__file__))
if srcPath not in sys.path:
    sys.path.append(srcPath)


import UnrealUtilities
importlib.reload(UnrealUtilities)

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial()

@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy
        UnrealUtilities.UnrealUtility().ImportFromDir(importDir)

class UnrealSubstancePlugin:
    def __init__(self):
        self.submenuName="UnrealSubstancePlugin"
        self.submenuLabel="Unreal Substance Plugin"
        self.CreateMenu()

    def CreateMenu(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            ToolMenus.get().remove_menu(existing.menu_name)

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel)
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())
        ToolMenus.get().refresh_all_widgets()

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()


UnrealSubstancePlugin()
