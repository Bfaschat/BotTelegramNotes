from cx_Freeze import setup, Executable

#Cria um executavel de um arquivo .py
setup(name='Tira Print',
    version='1.0.0',
    description='Tira print da tela',
    executables= [Executable('ComandosWindows.py')])