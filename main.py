import os
import os.path
import sys
import json
import time
# pyqt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication
# 模板替换
from string import Template
# 剪贴板
import pyperclip
# ui文件
from fixiteditor_ui import Ui_MainWindow
# 弹窗窗口
from config_window import Config
# 自定义
import head_translate as headT
import util as ut
import resolver_forward as RF
import resolver_backward as RB


class InitMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(InitMainWindow, self).__init__()
        self.Config = Config()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        # 菜单栏
        self.actionnew.setShortcut("CTRL+N")
        self.actionnew.triggered.connect(self.newfile)
        self.actionload_post.setShortcut("CTRL+L")
        self.actionload_post.triggered.connect(self.loadfile)
        self.actionsave.setShortcut("CTRL+S")
        self.actionsave.triggered.connect(self.savefile)
        self.CB_isencryption.clicked.connect(self.setEncryptionMode)
        self.actionnewsite.triggered.connect(self.newsite)
        self.actionlocaledit.setShortcut("CTRL+E")
        self.actionlocaledit.triggered.connect(self.editchange_new)

        # 快捷复制
        self.PB_suojin.clicked.connect(self.suojin)
        self.PB_konghang.clicked.connect(self.konghang)
        self.PB_highlight.clicked.connect(self.highlight)
        self.PB_image.clicked.connect(self.image)
        self.PB_admonition.clicked.connect(self.admonition)
        self.PB_mermaid.clicked.connect(self.mermaid)
        self.PB_echart.clicked.connect(self.echart)
        self.PB_bilibili.clicked.connect(self.bilibili)
        self.PB_typeit.clicked.connect(self.typeit)
        self.PB_quote.clicked.connect(self.quote)
        self.PB_link.clicked.connect(self.link)
        # 服务
        self.PB_localserver.clicked.connect(self.localserver_start)
        self.PB_localservershutdown.clicked.connect(self.localserver_shutdown)
        self.PB_cloudserver.clicked.connect(self.cloudserver)
        # 打开配置窗口
        self.actionconfig.triggered.connect(self.Config.open)
        # 其他
        self.refresh_combox()

    def editchange_new(self):
        if self.actionlocaledit.isChecked():
            self.status_message("编辑器：切换到本地")
            self.resize(950, 1010)
            self.setMinimumSize(QtCore.QSize(950, 1010))
            self.setMaximumSize(QtCore.QSize(950, 1010))
            # 切换到本地编辑器，将tmp.md内容解析到本地
            self.resolver_tmp2local()
        else:
            self.status_message("编辑器：切换到外部")
            self.resize(270, 1010)
            self.setMinimumSize(QtCore.QSize(270, 1010))
            self.setMaximumSize(QtCore.QSize(270, 1010))
            # 切换到外部编辑器，将编辑内容转移到tmp.md，并保存。
            # 逆解析
            self.resolver_local2tmp()

    def newsite(self):
        filePath = QtWidgets.QFileDialog.getExistingDirectory(None, '选择文件夹', os.getcwd())
        if os.path.exists(filePath):
            disk = filePath[0] + ":"
            command = disk + " && cd " + filePath + " && " + os.getcwd() + "\\tools\\hugo.exe new site newsite && " \
                                                                           "cd .\\newsite\\content && mkdir posts && " \
                                                                           "cd .. && cd static && mkdir image"
            os.system(command)

    def newfile(self):
        value, ok = QtWidgets.QInputDialog.getText(self, "新建post", "请输入文件名:", QtWidgets.QLineEdit.Normal, "new post")
        if ok:
            self.refresh_combox()
            self.status_message("新建：新建Post")
            self.LB_postname.setText(value + ".md")
            self.LB_date.setText(ut.isodate2date_time(ut.getdate()))
            self.LE_title.setText(value)
            self.TE_abstract.setPlainText('')
            self.TE_editor.setPlainText('')
        else:
            self.status_error("新建：新建post失败")

    def loadfile(self):
        self.refresh_combox()
        config = ut.loadconfig()
        dir_path = config["sitepath"] + "\\content\\posts\\"
        if not os.path.exists(dir_path):
            self.status_error('加载：网站路径错误！')
            return 0
        fname, ok = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", dir_path, "Markdown (*.md)")
        if ok:
            with open(fname, 'r', encoding='utf-8') as f:
                fulltext = f.read()
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if "<!--more-->" in fulltext:  # 摘要分割
                fulltext_list = fulltext.split("<!--more-->\n")
                main_text = fulltext_list[1]
                # 读取
                head_dict = headT.head2json(fulltext_list[0])
                # 写入编辑器界面
                self.LB_postname.setText(fname.split('/')[-1])
                self.LB_date.setText(ut.isodate2date_time(head_dict["date"]))
                self.LB_lastmod.setText(ut.isodate2date_time(head_dict["lastmod"]))
                self.status_message("加载：Post加载成功！")
                self.LE_title.setText(head_dict["title"])
                self.LE_subtitle.setText(head_dict["subtitle"])
                self.LE_imgeurl.setText(head_dict["featuredImage"])
                if len(head_dict["password"]) > 0:
                    self.CB_isencryption.setChecked(True)
                    self.LE_password.setEnabled(True)
                    self.LE_password_tip.setEnabled(True)
                    self.LE_password.setText(head_dict["password"])
                    self.LE_password_tip.setText(head_dict["message"])
                else:
                    self.CB_isencryption.setChecked(False)
                    self.LE_password.setDisabled(True)
                    self.LE_password_tip.setDisabled(True)
                    self.LE_password.setText("")
                    self.LE_password_tip.setText("")
                # 主页显示
                if head_dict["hiddenFromHomePage"] == "false":
                    self.CB_isshowinhome.setChecked(True)
                else:
                    self.CB_isshowinhome.setChecked(False)
                # 目录
                if len(head_dict['categories']) > 0 and (head_dict["categories"][0] in config["categories"]):
                    self.CoB_category.setCurrentIndex(config["categories"].index(head_dict["categories"][0]) + 1)
                else:
                    self.CoB_category.setCurrentIndex(0)
                # 菜单
                if head_dict["menu"] not in config["menu"]:
                    self.CoB_menu.setCurrentIndex(0)
                else:
                    self.CoB_menu.setCurrentIndex(config["menu"].index(head_dict["menu"]) + 1)
                # 页面宽度样式
                page_style = ['narrow', 'normal', 'wide']
                if head_dict["pageStyle"] not in page_style:
                    self.CoB_pagewidth.setCurrentIndex(1)
                else:
                    self.CoB_pagewidth.setCurrentIndex(page_style.index(head_dict["pageStyle"]))
                # 摘要
                self.TE_abstract.setPlainText(head_dict["abstract"])
                # 正文
                self.TE_editor.setPlainText(main_text)
            else:
                self.status_error('加载：不支持的文件类型或文件头不匹配！')

    def resolver_tmp2local(self):
        with open('tmp.md', 'r', encoding='utf-8') as f:
            fulltext = f.read()
        if "****\n" in fulltext:  # tmp.md摘要分割,"****"
            fulltext_list = fulltext.split("****\n")
            self.TE_abstract.setPlainText(RF.resolver_forward(fulltext_list[0]))  # 摘要
            self.TE_editor.setPlainText(RF.resolver_forward(fulltext_list[1]))  # 正文
        else:
            self.status_error('解析：文件头不匹配！')

    def resolver_local2tmp(self):
        file = open('tmp.md', mode='w')
        abstract = RB.resolver_backward(self.url_transfer_local(self.TE_abstract.toPlainText()))
        context = RB.resolver_backward(self.url_transfer_local(self.TE_editor.toPlainText()))
        if len(abstract) == 0 or abstract[-1] != '\n':
            abstract += '\n'
        file.write(abstract + "****\n" + context)
        file.close()
        ut.gb2utf8('tmp.md')
        # 打开文件
        os.popen('start "" "tmp.md"')

    def savefile(self):
        config = ut.loadconfig()
        if len(self.LB_postname.text()) == 0:
            self.status_error('保存：当前Post为空，请加载或新建Post！')
        elif not os.path.exists(config["sitepath"] + '\\content\\posts\\'):
            self.status_error('保存：网站路径错误！')
            return
        else:
            savePath = config["sitepath"] + '\\content\\posts\\' + self.LB_postname.text()
            class_file = open(savePath, 'w')
            self.LB_lastmod.setText(ut.isodate2date_time(ut.getdate()))
            self.status_message("保存：成功！")
            head1_tmpl = open('tmpls\\head1.tmpl', 'r')
            menu_tmpl = open('tmpls\\menu.tmpl', 'r')
            head2_tmpl = open('tmpls\\head2.tmpl', 'r')
            head1_ = Template(head1_tmpl.read())
            menu_ = Template(menu_tmpl.read())
            head2_ = Template(head2_tmpl.read())
            mypost = []
            config = ut.loadconfig()
            mypost.append(head1_.substitute(
                title=self.LE_title.text(),
                subtitle=self.LE_subtitle.text(),
                license=config["license"],
                categories='["' + self.CoB_category.currentText() + '"]' if len(self.CoB_category.currentText()) > 0 else "",
                featuredImage=self.LE_imgeurl.text(),
                showinhome="false" if self.CB_isshowinhome.isChecked() else "true",
                pagestyle=self.CoB_pagewidth.currentText(),
                password=self.LE_password.text() if self.CB_isencryption.isChecked() else "",
                message=self.LE_password_tip.text(),
                author=config["author"],
                date=ut.date_time2isodate(self.LB_date.text()),
                lastmod=ut.date_time2isodate(self.LB_lastmod.text())))
            if len(self.CoB_menu.currentText()) > 0:
                mypost.append(menu_.substitute(
                    menu_flag="menu_y",
                    menu=self.CoB_menu.currentText()))
            else:
                mypost.append('#menu_n\n')
            # 摘要和正文
            if not self.actionlocaledit.isChecked():
                self.resolver_tmp2local()
            # 将摘要和正文中的本地图片，'c:\ d:\'开头的本地路径，替换成网站image文件夹  '/image/xxx.png'
            self.TE_abstract.setPlainText(self.url_transfer(self.TE_abstract.toPlainText()))
            self.TE_editor.setPlainText(self.url_transfer(self.TE_editor.toPlainText()))
            mypost.append(head2_.substitute(abstract=self.TE_abstract.toPlainText(), editor=self.TE_editor.toPlainText()))

            # 将代码写入文件
            class_file.writelines(mypost)
            class_file.close()
            # 转码
            ut.gb2utf8(savePath)

    # tmp.md 解析到 本地编辑器
    # 如果此时url为本地路径，则文件转储，同时修改图片url 为 网站url或 云url
    # 如果此时url为网站url或云url，则配置文件中设置的保存位置，调整为云url或网站url
    # 1.文件转储，将<< image >>标签中的图片url转储 目标 "网站目录\static\image\"+文件名
    # 2.修改图片url，图片一共有三个储存区域：本地，网站，图床服务器
    #   网站 "网站目录\static\image\"+文件名 修改为 "/image/"+图片名
    #   云   "网站目录\static\image\"+文件名 修改为 "http://110.110.110.110:port/"+图片名
    def url_transfer(self, ss):
        config = ut.loadconfig()
        print(config["imageserver_enable"])
        ss_list = ss.split('\n')
        for i in range(len(ss_list)):
            line = ss_list[i].replace(' ', '')
            # 图片保存在网站
            if line[0:8] == "{{<image" and not config["imageserver_enable"]:
                # 本地地址转化为网站地址，同时将文件转储到网站
                if ut.islocalpath(ut.get_in_between(line, 'src="', '"')) != False:
                    filename = ut.islocalpath(ut.get_in_between(line, 'src="', '"'))
                    abs_path = config["sitepath"] + '\\static\\image\\' + filename
                    os.popen('copy ' + ut.get_in_between(line, 'src="', '"') + " " + abs_path)
                    url = '/image/' + filename
                    ss_list[i] = '{{< image src="' + url + '" caption=' + ut.get_in_between(ss_list[i], 'caption=', ">}}") + " >}}"
                    self.status_message('图片已转储到网站 ' + filename)
                # http地址转化为网站地址，文件无变动
                if ut.ishttppath(ut.get_in_between(line, 'src="', '"')) != False:
                    filename = ut.ishttppath(ut.get_in_between(line, 'src="', '"'))
                    url = '/image/' + filename
                    ss_list[i] = '{{< image src="' + url + '" caption=' + ut.get_in_between(ss_list[i], 'caption=', ">}}") + " >}}"
                    self.status_message('图片已转储到网站 ' + filename)
            # 图片保存在云
            if line[0:8] == "{{<image" and config["imageserver_enable"]:
                # 本地地址转化为云地址，同时将文件转储到网站
                if ut.islocalpath(ut.get_in_between(line, 'src="', '"')) != False:
                    filename = ut.islocalpath(ut.get_in_between(line, 'src="', '"'))
                    abs_path = config["sitepath"] + '\\static\\image\\' + filename
                    os.popen('copy ' + ut.get_in_between(line, 'src="', '"') + " " + abs_path)
                    url = 'http://'+config["imageserver"]+'/' + filename
                    ss_list[i] = '{{< image src="' + url + '" caption=' + ut.get_in_between(ss_list[i], 'caption=', ">}}") + " >}}"
                    self.status_message('图片已转储到网站 ' + filename)
                # 网站地址转化为http地址，文件无变动
                if ut.iswebsitepath(ut.get_in_between(line, 'src="', '"')) != False:
                    filename = ut.iswebsitepath(ut.get_in_between(line, 'src="', '"'))
                    url = 'http://' + config["imageserver"] + '/' + filename
                    ss_list[i] = '{{< image src="' + url + '" caption=' + ut.get_in_between(ss_list[i], 'caption=', ">}}") + " >}}"
                    self.status_message('图片已转储到网站 ' + filename)

        return "\n".join(ss_list)

    # 本地编辑器 解析到 tmp.md
    # 修改图片url 例:"/image/"+图片名 修改为 "网站目录\static\image\"+文件名
    def url_transfer_local(self,ss):
        config = ut.loadconfig()
        ss_list = ss.split('\n')
        for i in range(len(ss_list)):
            line = ss_list[i].replace(' ', '')
            if line[0:8] == "{{<image" and ut.get_in_between(line, 'src="', '"')[0:7] == '/image/':
                filename = ut.get_in_between(line, 'src="', '"')[7:]
                abs_path = config["sitepath"] + '\\static\\image\\' + filename
                ss_list[i] = '{{< image src="' + abs_path + '" caption=' + ut.get_in_between(ss_list[i], 'caption=', ">}}") + " >}}"
                self.status_message('图片切换到本地路径 ' + filename)
        return "\n".join(ss_list)


    def refresh_combox(self):
        config = ut.loadconfig()
        self.CoB_category.clear()
        self.CoB_category.addItems(["未分类"])  # 添加空元素 未分类
        self.CoB_category.addItems(config["categories"])
        self.CoB_menu.clear()
        self.CoB_menu.addItems([""])  # 添加空元素
        self.CoB_menu.addItems(config["menu"])
        self.status_message("UI：已加载配置到UI")

    def setEncryptionMode(self):
        if self.CB_isencryption.isChecked():
            self.LE_password.setEnabled(True)
            self.LE_password_tip.setEnabled(True)
            self.CB_isshowinhome.setChecked(False)
            self.CB_isshowinhome.setDisabled(True)
        else:
            self.LE_password.setDisabled(True)
            self.LE_password_tip.setDisabled(True)
            self.CB_isshowinhome.setChecked(True)
            self.CB_isshowinhome.setDisabled(False)

    # ----------------------状态栏--------------------------#
    def status_message(self, words):
        text = "MSG:" + words + " " + ut.gettime() + '\n' + self.TE_debug.toPlainText()
        self.TE_debug.setPlainText(text)

    def status_warning(self, words):
        text = "WRN:" + words + " " + ut.gettime() + '\n' + self.TE_debug.toPlainText()
        self.TE_debug.setPlainText(text)

    def status_error(self, words):
        text = "ERR:" + words + " " + ut.gettime() + '\n' + self.TE_debug.toPlainText()
        self.TE_debug.setPlainText(text)

    # ----------------------一键复制-----------------------#
    def suojin(self):
        pyperclip.copy("&emsp;&emsp;")

    def konghang(self):
        pyperclip.copy("&nbsp;")

    def highlight(self):
        pyperclip.copy("{{< highlight html >}}\n\n{{< /highlight >}}")

    def image(self):
        pyperclip.copy('{{< image src="image_url" caption="image_caption" width=400 linked=false >}}')

    def admonition(self):
        pyperclip.copy('{{< admonition type=tip title="This is a tip" open=true >}}\n一个 **技巧** 横幅\n{{< /admonition >}}')

    def mermaid(self):
        pyperclip.copy('{{< mermaid >}}\n\n{{< /mermaid >}}')

    def echart(self):
        pyperclip.copy('{{< echarts >}}\n\n{{< /echarts >}}')

    def bilibili(self):
        pyperclip.copy('{{< bilibili BV1Sx411T7QQ >}}')

    def typeit(self):
        pyperclip.copy('{{< typeit >}}\n\n{{< /typeit >}}')

    def quote(self):
        pyperclip.copy('{{< center-quote >}}\n\n{{< /center-quote >}}')

    def link(self):
        pyperclip.copy('{{< link href="href" content="content" card=true download="">}}')

    # ----------------------server-------------------------#
    def localserver_start(self):
        self.status_message("本地服务：启动")
        config = ut.loadconfig()
        fastRender = "--disableFastRender" if self.CB_fastRender.isChecked() else ""
        command = 'cd ' + config["sitepath"] + ' && start "' + config["chrome"] + '" http://127.0.0.1:1313 && ' + os.getcwd() + "\\tools\\hugo.exe server -p 1313 " + fastRender
        # if self.CB_localserver_showcmd.isChecked():
        #     os.system(command)
        # else:
        #     os.popen(command)
        os.popen(command)

    def localserver_shutdown(self):
        self.status_message("本地服务：关闭")
        command = "taskkill /F /im  hugo.exe"
        if self.CB_localserver_showcmd.isChecked():
            os.system(command)
        else:
            os.popen(command)


    def cloudserver(self):
        self.status_message("同步到云：执行")
        config = ut.loadconfig()
        # 覆盖式创建密码文件
        f = open('rsync.passwd', 'w+')
        f.write(config["rsyncuserpasswd"])
        f.close()
        time.sleep(0.2)

        # 向云服务器同步
        if ut.isIP(config["cloudserver"]):
            sitepath_cyg = ut.winpath2cygpath(config["sitepath"])
            rsync_cmd = os.getcwd() + "\\tools\\rsync.exe -avz --port=873 --delete --progress " + sitepath_cyg + "/public  " + config["rsyncuser"] + "@" + config[
                "cloudserver"] + "::myblog/ --password-file=" + ut.winpath2cygpath(os.getcwd()) + "/rsync.passwd"
            command1 = 'cd ' + config["sitepath"] + " && " + os.getcwd() + "\\tools\\hugo.exe" + " && " + rsync_cmd
        else:
            command1 = " "

        # 向静态资源服务器同步
        if ut.isIP(config["staticserver"]):
            sitepath_cyg = ut.winpath2cygpath(config["sitepath"])
            rsync_image_cmd = os.getcwd() + "\\tools\\rsync.exe -avz --port=873 --delete --progress " + sitepath_cyg + "/static/image  " + config["rsyncuser"] + "@" + config[
                "staticserver"] + "::myblog/ --password-file=" + ut.winpath2cygpath(os.getcwd()) + "/rsync.passwd"
            command2 = 'cd ' + config["sitepath"] + " && " + rsync_image_cmd
        else:
            command2 = " "

        command = command1 + " && " + command2
        if self.CB_cloudserver_showcmd.isChecked():
            os.system(command)
        else:
            os.popen(command)

    # --------------------退出-------------------------#
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出FixitEditor', "现在退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 关闭其他子窗口
            self.Config.close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InitMainWindow()
    sys.exit(app.exec_())
