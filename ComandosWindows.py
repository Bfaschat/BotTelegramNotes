import pyscreenshot as ImageGrab
import os, time

def screenShot():
    '''
    Tira um print da tela, e o salva na pasta temp.
    '''
    dir = 'C:\\temp\\'
    if(os.path.exists(dir) == False):
        os.mkdir(dir)

    image = ImageGrab.grab()
    image.save('{}print.jpg'.format(dir), 'jpeg')
    print('Print tirado!')


if __name__ == "__main__":
    screenShot()