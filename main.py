import os
import os.path
import sys
import json
# pyqt
import time

from PyQt5 import QtWidgets
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
        self.CB_isencryption.stateChanged.connect(self.setEncryptionMode)
        self.actionnewsite.triggered.connect(self.newsite)

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
        # 启动
        self.PB_localserver.clicked.connect(self.localserver_start)
        self.PB_cloudserver.clicked.connect(self.cloudserver)
        # 打开配置窗口
        self.actionconfig.triggered.connect(self.Config.open)
        # 其他
        self.refresh_combox()

    def newsite(self):
        filePath = QtWidgets.QFileDialog.getExistingDirectory(None, '选择文件夹', os.getcwd())
        ok = os.path.exists(filePath)
        if ok:
            disk = filePath[0]+":"
            command = disk + " && cd "+ filePath +" && "+ os.getcwd() + "\\tools\\hugo.exe new site newsite && cd .\\newsite\\content && mkdir posts"
            os.system(command)

    def newfile(self):
        value, ok = QtWidgets.QInputDialog.getText(self, "新建post", "请输入文件名:", QtWidgets.QLineEdit.Normal, "new post")
        if ok:
            self.refresh_combox()
            self.status_message("新建Post")
            self.LB_postname.setText(value + ".md")
            self.LB_date.setText(ut.getdate())
            self.LE_title.setText(value)
        else:
            self.status_error("新建post失败")

    def loadfile(self):
        self.refresh_combox()
        config = ut.loadconfig()
        dir_path = config["sitepath"] + "\\content\\posts\\"
        if not os.path.exists(dir_path):
            self.status_error('不存在此路径：content\\posts\\')
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
                self.LB_date.setText(head_dict["date"])
                self.LB_lastmod.setText(head_dict["lastmod"])
                self.status_message("加载Post成功！")
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
                self.status_error('不支持的文件类型，或文件头不匹配！')

    def savefile(self):
        config = ut.loadconfig()
        if len(self.LB_postname.text()) == 0:
            self.status_error('当前Post为空，请加载或新建Post！')
        else:
            savePath = config["sitepath"] + '\\content\\posts\\' + self.LB_postname.text()
            class_file = open(savePath, 'w')
            self.LB_lastmod.setText(ut.getdate())
            self.status_message("保存成功！")
            head1_tmpl = open('head1.tmpl', 'r')
            menu_tmpl = open('menu.tmpl', 'r')
            head2_tmpl = open('head2.tmpl', 'r')
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
                date=self.LB_date.text(),
                lastmod=self.LB_lastmod.text()))
            if len(self.CoB_menu.currentText()) > 0:
                mypost.append(menu_.substitute(
                    menu_flag="menu_y",
                    menu=self.CoB_menu.currentText()))
            else:
                mypost.append('#menu_n\n')
            mypost.append(head2_.substitute(
                abstract=self.TE_abstract.toPlainText(),
                editor=self.TE_editor.toPlainText()))

            # 将代码写入文件
            class_file.writelines(mypost)
            class_file.close()
            # 转码
            ut.gb2utf8(savePath)

    def refresh_combox(self):
        config = ut.loadconfig()
        self.CoB_category.clear()
        self.CoB_category.addItems([""])  # 添加空元素
        self.CoB_category.addItems(config["categories"])
        self.CoB_menu.clear()
        self.CoB_menu.addItems([""])  # 添加空元素
        self.CoB_menu.addItems(config["menu"])
        self.status_message("已加载配置")

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
        self.LB_status.setText(words + " " + ut.gettime())
        self.LB_status.setStyleSheet("color:rgb(0, 0, 0)")

    def status_warning(self, words):
        self.LB_status.setText(words + " " + ut.gettime())
        self.LB_status.setStyleSheet("color:rgb(255, 255, 0)")

    def status_error(self, words):
        self.LB_status.setText(words + " " + ut.gettime())
        self.LB_status.setStyleSheet("color:rgb(255, 0, 0)")

    # ----------------------一键复制-----------------------#
    def suojin(self):
        pyperclip.copy("&emsp;&emsp;")

    def konghang(self):
        pyperclip.copy("&nbsp;")

    def highlight(self):
        pyperclip.copy("{{< highlight html >}}\n\n{{< /highlight >}}")

    def image(self):
        pyperclip.copy('{{< image src="/images/lighthouse.jpg" caption="Lighthouse" width=400 linked=false >}}')

    def admonition(self):
        pyperclip.copy('{{< admonition type=tip title="This is a tip" open=false >}}\n一个 **技巧** 横幅\n{{< /admonition >}}')

    def mermaid(self):
        pyperclip.copy('''
        {{< mermaid >}}
        gantt
        dateFormat  YYYY-MM-DD
        title Adding GANTT diagram to mermaid
        
        section A section
        Completed task            :done,    des1, 2014-01-06,2014-01-08
          Active task               :active,  des2, 2014-01-09, 3d
          Future task               :         des3, after des2, 5d
          Future task2              :         des4, after des3, 5d
          {{< /mermaid >}}')
        ''')

    def echart(self):
        pyperclip.copy('{{< echarts >}}\njson\n{{< /echarts >}}')

    def bilibili(self):
        pyperclip.copy('{{< bilibili BV1Sx411T7QQ >}}')

    def typeit(self):
        pyperclip.copy('{{< typeit >}}\n这一个带有基于 [TypeIt](https://typeitjs.com/) 的 **打字动画** 的 *段落* ...\n{{< /typeit >}}')

    def quote(self):
        pyperclip.copy('''
        {{ <center-quote>}}
        **hello** *world*
        this is a center - quote shortcode example.
        {{ </center-quote>}}
        ''')

    def link(self):
        pyperclip.copy('{{< link href="https://github.com/hugo-fixit/FixIt" content="FixIt Theme" title="source of FixIt Theme" card=true download="/mainsitehead.md">}}')

    # ----------------------server-------------------------#
    def localserver_start(self):
        self.status_message("启动本地服务")
        config = ut.loadconfig()
        fastRender = "--disableFastRender" if self.CB_fastRender.isChecked() else ""
        command = 'cd ' + config["sitepath"] + ' && start "' + config["chrome"] + '" http://127.0.0.1:1313 && ' + os.getcwd() + "\\tools\\hugo.exe server -p 1313 " + fastRender
        if self.CB_localserver_showcmd.isChecked():
            os.system(command)
        else:
            os.popen(command)

    def cloudserver(self):
        self.status_message("同步到云")
        config = ut.loadconfig()
        # 覆盖式创建密码文件
        f = open('rsync.passwd', 'w+')
        f.write(config["rsyncuserpasswd"])
        f.close()
        time.sleep(0.2)
        # 向云服务器同步
        sitepath_cyg = ut.winpath2cygpath(config["sitepath"])
        rsync_cmd = os.getcwd() + "\\tools\\rsync.exe -avz --port=873 --delete --progress " + sitepath_cyg + "/public  " + config["rsyncuser"] + "@" + config[
            "cloudserver"] + "::myblog/ --password-file=" + ut.winpath2cygpath(os.getcwd()) + "/rsync.passwd"
        command = 'cd ' + config["sitepath"] + " && " + os.getcwd() + "\\tools\\hugo.exe" + " && " + rsync_cmd
        if self.CB_cloudserver_showcmd.isChecked():
            os.system(command)
        else:
            os.popen(command)

    # --------------------退出-------------------------#
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出Fixit-Editor', "现在退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 关闭其他子窗口
            self.Config.close()
            event.accept()
        else:
            event.ignore()


# -----------------------其他------------------------#
# def addItemIfNotEqual(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InitMainWindow()
    sys.exit(app.exec_())
