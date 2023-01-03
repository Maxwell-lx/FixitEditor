import os
import shutil

os.rename(".\\dist\\main", ".\\dist\\FixitEditor")
os.rename(".\\dist\\FixitEditor\\main.exe", ".\\dist\FixitEditor\\FixitEditor.exe")

shutil.copy('menu.tmpl', '.\\dist\\FixitEditor\\')
shutil.copy('head1.tmpl', '.\\dist\\FixitEditor\\')
shutil.copy('head2.tmpl', '.\\dist\\FixitEditor\\')
shutil.copy('config.json', '.\\dist\\FixitEditor\\')
shutil.copy('myconfig.json', '.\\dist\\FixitEditor\\')
shutil.copy('tools', '.\\dist\\FixitEditor\\')


