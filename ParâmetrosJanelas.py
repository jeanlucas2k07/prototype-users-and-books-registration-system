from PIL import Image, ImageTk

class WindowParams:
    def janela_config(self):
        self.geometry("700x400")
        self.resizable(width=False, height=False)

    def parametros_janela_principal(self):
        self.geometry('1000x600')
        self.resizable(False, False)
        icon_path = "images/img_001.png"
        icon = ImageTk.PhotoImage(Image.open(icon_path))  
        self.wm_iconphoto(True, icon)


