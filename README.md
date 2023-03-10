# FixitEditor
[Fixit](https://fixit.lruihao.cn/zh-cn/)是一款基于Hugo的网站主题，FixitEditor是基于Fixit的编辑器，整合了文件头、短代码、云同步等功能，让编辑变的更简单。

## 1.功能简述

FixitEditor集成了

* **Fixit文件头管理**

* **集成常用的短代码**

* **本地server(Hugo)**

* **云端同步(Rsync)**

* **markdown编辑功能**

  

## 2.安装FixitEditor

### 1. windows上，下载解压即可用

[FixitEditor](https://github.com/Maxwell-lx/FixitEditor/releases)

如果有其他系统使用的需求，可以自行编译安装。

### 2.编译安装

编译之前，清空dist文件夹

```
#【pyinstaller -w -i 图标ico文件的路径 主py文件 -p 打包路径】
pyinstaller -w -i fav.ico main.py -y 
python installer.py
```

编译后的文件位于`.\dist\FixitEditor`,

## 3.如何使用FixitEditor

1. 下载FixitEditor，解压到任意目录，示例：`C:\FixitEditor`。

2. 打开FixitEditor，修改配置文件。

3. [下载Fixit主题](https://github.com/hugo-fixit/FixIt/releases/)，解压并复制`Fixit`主题到网站主题文件夹`myblog\themes\`，文件夹名修改为`Fixit`：

2. 修改两个配置文件，分别为

   * `myblog\config.toml`网站配置，[参考Fixit官网**2.3基础配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)。
   * `myblog\themes\Fixit\config.toml`，[参考Fixit官网**3.1网站配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)



## 4.Fixit-Editor快捷键

| 文件操作 |                                                              |
| -------- | ------------------------------------------------------------ |
| Ctrl+S   | 文件保存到`myblog\content\posts`文件夹                       |
| Ctrl+N   | 新建MarkDown文件（含Fixit文件头）                            |
| Ctrl+L   | 打开`myblog\content\posts`文件夹，手动选择，载入MarkDown文件 |
| Ctrl+E   | 本地编辑器<-->外部编辑器 切换                                |

## 5.版本兼容性

|                   | Fixit  | hugo           | rsync(cwrsync) |
| ----------------- | ------ | -------------- | -------------- |
| FixitEditor 0.1.0 | 0.2.16 | 0.105-extended | 6.2.7          |
| FixitEditor 0.2.0 | 0.2.16 | 0.105-extended | 6.2.7          |
