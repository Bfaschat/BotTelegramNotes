import pyautogui, os

def print_tela():
    folder = 'C:\\temp\\'
    arq = '{}print.png'.format(folder)

    if(os.path.exists(folder) == False):
        os.mkdir(folder)
    elif(os.path.exists(arq) == True):
        os.remove(arq)

    pic = pyautogui.screenshot()

    pic.save(arq)
    pic.close()