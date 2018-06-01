import pyscreenshot as ImageGrab
import os, time

def screenShot():
    '''
    Tira um print da tela, e o salva na pasta temp.
    '''
    try:
        dir = 'C:\\temp\\'
        if(os.path.exists(dir) == False):
            os.mkdir(dir)

        image = ImageGrab.grab()
        image.save('{}print.jpg'.format(dir), 'jpeg')
    except Exception as ex:
        print(ex)
    
    
if __name__ == "__main__":
    screenShot()