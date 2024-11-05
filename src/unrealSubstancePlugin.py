import tkinter.filedialog
from unreal import (ToolMenus, ToolMenuContext, uclass, ufunction, ToolMenuEntryScript) #imports tkinter for file dialog operations and Unreal Engine classes to create custom menu tools and entry scripts

#imports os for file path handling, sys for path management, importlib for module reloading, and tkinter for GUI operations
import os
import sys
import importlib
import tkinter

srcPath = os.path.dirname(os.path.abspath(__file__))
if srcPath not in sys.path:
    sys.path.append(srcPath) #adds the script's directory to the Python system path if it's not already included


import UnrealUtilities
importlib.reload(UnrealUtilities) #imports the UnrealUtilities module and reloads it so updates can be applied

@uclass() #defines a tool menu entry class for creating and finding the base material
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial() #overrides the base method and calls FindOrBuildBaseMaterial from the UnrealUtility class when selected from the menu

@uclass() #defines a tool menu entry class for loading meshes from a directory
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context) -> None: # execute method opens a file dialog to select a directory, then calls ImportFromDir from UnrealUtility to import meshes
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy
        UnrealUtilities.UnrealUtility().ImportFromDir(importDir)

class UnrealSubstancePlugin: #defines the main plugin class
    def __init__(self):
        self.submenuName="UnrealSubstancePlugin"
        self.submenuLabel="Unreal Substance Plugin"
        self.CreateMenu() #initializes the submenu name and label, then calls CreateMenu to set up the menu

    def CreateMenu(self): #retrieves the main level editor menu in Unreal Engine
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            ToolMenus.get().remove_menu(existing.menu_name) #checks if the submenu already exists and removes duplicates

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel) #creates a new submenu under the main menu
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())
        ToolMenus.get().refresh_all_widgets() #adds two custom entries that links to each's respective entry class and refreshes UI to show new entries

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript): #adds an entry script to the submenu
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()


UnrealSubstancePlugin() #instantiates the UnrealSubstancePlugin class and adds the menu entries
