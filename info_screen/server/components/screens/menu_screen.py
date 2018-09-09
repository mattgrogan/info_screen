from PIL import Image

from server.components.screens.screen import Screen
from server.components.layers.text_layer import TextLayer

class MenuScreen(Screen):

    def __init__(self, device):
        self.init()
        self.is_popup = False
        self.device = device

        self.setting = False

    def enter(self):
        pass

    def exit(self):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass

    def step(self):
        pass

    def handle_input(self, cmd):
        if cmd == "KEY_ENTER":
            self.setting = not self.setting

    def render(self):
        bg = Image.new("RGBA", self.device.size, "#FF0000")

        y = 0

        menu_title1 = TextLayer("Auto", size="SMALLEST")
        title_im1 = menu_title1.render()
        bg.paste(title_im1, (0, y), mask=title_im1)

        w, h = title_im1.size
        y += h + 1

        menu_title2 = TextLayer("Cycle", size="SMALLEST")
        title_im2 = menu_title2.render()
        bg.paste(title_im2, (0, y), mask=title_im2)

        w, h = title_im1.size
        y += h + 1       

        if self.setting:
            setting_text = "ON"
        else:
            setting_text = "OFF"

        menu_setting = TextLayer("is " + setting_text, size="SMALLEST")
        setting_im = menu_setting.render()
        bg.paste(setting_im, (0, y), mask=setting_im)
        
        return bg