import os

os.system("ren .\\dist\\main FixitEditor")
os.system("ren .\\dist\\FixitEditor\\main.exe FixitEditor.exe")


os.system('mkdir .\\dist\\FixitEditor\\tmpls')
os.system('mkdir .\\dist\\FixitEditor\\tools')

os.system('copy config.json .\\dist\\FixitEditor\\')
os.system('copy tools .\\dist\\FixitEditor\\tools')
os.system('copy tmp.md .\\dist\\FixitEditor\\')
os.system("copy .\\tmpls .\\dist\\FixitEditor\\tmpls")
