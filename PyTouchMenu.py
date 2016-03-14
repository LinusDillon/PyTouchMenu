import os
import pathlib
import pygame
import argparse
import random
from subprocess import call
from pgu import gui
import wifi
import os

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


class PyTouchMenu:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    BACKGROUND_COLOUR = (0, 50, 128)

    def __init__(self):
        """Initialize"""

        self.themeDir = "Theme"
        self.backgroundDir = self.themeDir + "/Backgrounds"
        self.args = self.ParseCommandLine()
        self.menuItems = self.GetMenuItems()
        self.backgrounds = self.GetBackgrounds()
        print(self.backgrounds)

        # Initialize PyGame
        pygame.init()

        # Create the Screen
        self.screen = pygame.display.set_mode((self.args.width, self.args.height))

        # Setup background
        self.DrawBackground()

        # Create the GUI
        self.ui = gui.App(screen=self.screen, theme=gui.Theme("Theme"))
        self.table = gui.Table(valign=-1)
        self.CreateTitle()
        self.CreateItemButtons()
        self.CreateQuitButton()

    def ParseCommandLine(self):
        """Parse command line"""
        parser = argparse.ArgumentParser(
            description='Menu system for touch screens.')
        parser.add_argument('directory', action='store',
                            help='directory to scan for executable menu items')
        parser.add_argument('-t', '--title', action='store',
                            help='menu title')
        parser.add_argument('-x', '--width',
                            action='store', default=320, type=int,
                            help='width of display')
        parser.add_argument('-y', '--height',
                            action='store', default=240, type=int,
                            help='height of display')

        return parser.parse_args()

    def GetMenuItems(self):
        """Scan the menu folder for items to add to the menu"""
        d = pathlib.Path(self.args.directory)
        if not d.exists():
            raise ValueError("Directory '" + self.args.directory + "' not found.")
        if not d.is_dir():
            raise ValueError("Argument '" + self.args.directory + "' is not a directory.")
        return [f for f in d.iterdir() if f.is_file() and os.access(str(f.resolve()), os.X_OK)]

    def GetBackgrounds(self):
        """Scan the backgrounds folder for images"""
        d = pathlib.Path(self.backgroundDir)
        if not d.exists():
            raise ValueError("Directory '" + self.backgroundDir + "' not found.")
        if not d.is_dir():
            raise ValueError("Argument '" + self.backgroundDir + "' is not a directory.")
        return [f for f in d.iterdir() if f.is_file() and f.suffix == ".png"]

    def CreateQuitButton(self):
        self.ui.connect(gui.QUIT, self.ui.quit, None)
        btn = gui.Button("Exit Menu", width=self.args.width * 0.9, cls="button.quit")
        self.table.tr()
        self.table.td(btn)
        btn.connect(gui.CLICK, self.ui.quit)

    def MakeItemClick(self, item):
        def itemClick():
            call(str(item.resolve()), shell=True)
        return itemClick

    def CreateTitle(self):
        if self.args.title:
            lbl = gui.Label(self.args.title, width=self.args.width * 0.9, style={"color": (255, 255, 255)})
            self.table.tr()
            self.table.td(lbl)

    def CreateItemButtons(self):
        for item in self.menuItems:
            btn = gui.Button(item.name, width=self.args.width * 0.9)
            self.table.tr()
            self.table.td(btn)
            btn.connect(gui.CLICK, self.MakeItemClick(item))

    def GetWifiState(self):
        if not os.path.isfile("/sbin/iwlist"):
            return

    def DrawBackground(self):
        file = random.choice(self.backgrounds)
        image = pygame.image.load(str(file))
        self.screen.blit(image, (0, 0))

    def MainLoop(self):
        """This is the Main Loop"""
        self.ui.run(self.table)

if __name__ == "__main__":
    MainWindow = PyTouchMenu()
    MainWindow.MainLoop()
