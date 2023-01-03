# FixitEditor
[Fixit](https://fixit.lruihao.cn/zh-cn/)是一款基于Hugo的网站主题，FixitEditor是基于Fixit的编辑器，整合了文件头、短代码、云同步等功能，让编辑变的更简单。

## 功能简述

FixitEditor集成了

* **Fixit文件头管理**

* **一些常用的短代码**

* **本地server(Hugo)**

* **云端同步(Rsync)**

* **markdown编辑功能**（待完善）

  

## 使用FixitEditor

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

执行`python installer.py`过程中，如果出现` Permission denied`错误，就手动执行复制、重命名等操作。

## 一、使用前配置

### 1.配置网站的本地目录

1. 本地创建网站文件夹，打开cmd，示例：网站路径不要有中文字符

   ```
   C:
   cd Hugo
   hugo new site myblog
   ```

2. 新建文件夹`myblog\content\posts`，这里储存网站的所有`.md`文件。

3. [下载Fixit主题](https://github.com/hugo-fixit/FixIt/releases/)，解压并复制`Fixit`主题到网站主题文件夹`myblog\themes\`，文件夹名字修改为`Fixit`：

4. 修改两个配置文件，分别为

   * `myblog\config.toml`网站配置，[参考Fixit官网**2.3基础配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)。
   * `myblog\themes\Fixit\config.toml`，[参考Fixit官网**3.1网站配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)

### 2.安装FixitEditor

1. 下载FixitEditor，解压到任意目录，示例：`C:\FixitEditor`

2. 打开FixitEditor，修改配置文件。

3. 配置文件修改完成，即可开启使用。

### Fixit-Editor示例使用视频



## 附录 Fixit-Editor快捷键（待完善）

| 文件操作         |                                                              |
| ---------------- | ------------------------------------------------------------ |
| Ctrl+S           | 文件保存到`myblog\content\posts`文件夹                       |
| Ctrl+N           | 新建MarkDown文件（含Fixit文件头）                            |
| Ctrl+L           | 打开`myblog\content\posts`文件夹，手动选择，载入MarkDown文件 |
| **文本编辑**     |                                                              |
| Ctrl+K           | 添加超链接                                                   |
| Ctrl+B           | 文本加粗                                                     |
| Alt + '+'        | 标题升级                                                     |
| Alt + '-'        | 标题降级                                                     |
| 。。。更多快捷键 | 。。。待完善                                                 |
