# Fixit-Editor
Fixit-Editor是基于Fixit的Post编辑器。

如果你去[Fixit官网](https://fixit.lruihao.cn/zh-cn/)，你会被它的配置内容搞的眼花缭乱。关于这一点，本人非常理解作者，因为一个项目在开发过程中，它还不成熟的时候，总是会将功能全部展现；等到项目成熟后，功能删繁就简，项目才会变得简单易用。

但是瑕不掩瑜，这些缺点仍不妨碍它成为一个好项目。因此，项目本着简单易用的初心，基于Pyqt开发了一款Fixit编辑器。

## 功能简述

Fixit-Editor集成了

* **Fixit文件头**

* **一键短代码**

* **一键本地启动**

* **一键同步到云**

* **markdown文本编辑器**

  

## 编译安装

资源文件

```
#【pyinstaller -w -i 图标ico文件的路径 主py文件 -p 打包路径】
pyinstaller -w -i fav.ico main.py -y 
python installer.py
```

如果出现` Permission denied`错误，就手动执行替代。







## 一、使用前配置

### 1.安装hugo和fixit

1. 本地创建网站文件夹，打开cmd，示例：

   ```
   G:
   cd Hugo
   hugo new site myblog(网站名字,建议英文)
   ```

   ![](https://maxwell-lx.oss-cn-beijing.aliyuncs.com/myblog/hugo%E6%96%B0%E5%BB%BA%E7%BD%91%E7%AB%99.png)

2. [下载Fixit主题](https://github.com/hugo-fixit/FixIt/releases/)，解压并复制`Fixit`主题到网站主题文件夹`myblog\themes\`，文件夹名字修改为`Fixit`：

   ![](https://maxwell-lx.oss-cn-beijing.aliyuncs.com/myblog/%E5%A4%8D%E5%88%B6%E5%88%B0Fixit.png)

3. 修改两个配置文件，分别为

   * `myblog\config.toml`网站配置，[参考Fixit官网**2.3基础配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)。
   * `myblog\themes\Fixit\config.toml`，[参考Fixit官网**3.1网站配置**](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)

4. 新建文件夹`myblog\content\posts`，这里储存网站的所有`.md`文件。

### 2.安装FixitEditor

1. 下载FixitEditor，解压到任意目录，示例：`G:\Hugo\Fixit-Editor`

2. 打开FixitEditor，修改配置文件。

3. 配置文件修改完成，即可开启使用。

### Fixit-Editor示例使用视频



## 附录 Fixit-Editor快捷键

| 文件操作     |                                                              |
| ------------ | ------------------------------------------------------------ |
| Ctrl+S       | 文件保存到`myblog\content\posts`文件夹                       |
| Ctrl+N       | 新建MarkDown文件（含Fixit文件头）                            |
| Ctrl+L       | 打开`myblog\content\posts`文件夹，手动选择，载入MarkDown文件 |
| **文本编辑** |                                                              |
|              |                                                              |
|              |                                                              |
|              |                                                              |
|              |                                                              |
|              |                                                              |
