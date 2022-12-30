import os.path
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
import json
import math
from PyQt5 import QtWidgets
from posteditor import Ui_MainWindow
import time
import head_translate as headT
import util as ut
from string import Template
import pyperclip
import os


class InitMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # super().__init__()
        super(InitMainWindow, self).__init__()
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
        self.CoB_tags.currentTextChanged.connect(self.addtags)

        # 快捷复制
        self.PB_suojin.clicked.connect(self.suojin)
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
        self.PB_localserver.clicked.connect(self.localserver)
        self.PB_cloudserver.clicked.connect(self.cloudserver)

        self.load_config()

    def newfile(self):
        value, ok = QtWidgets.QInputDialog.getText(self, "新建post", "请输入文件名:", QtWidgets.QLineEdit.Normal, "new post")
        if ok:
            self.LB_postname.setText(value + ".md")
            self.LB_status.setText("新建Post！")
            self.LB_date.setText(ut.getdate())
            self.LE_license.setText("Maxwell-lx all rights reserved.")
        else:
            self.LB_status.setText("新建Post失败！")

    def loadfile(self):
        fname, ok = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "../content/posts/", "Markdown (*.md)")
        if ok:
            with open(fname, 'r', encoding='utf-8') as f:
                fulltext = f.read()
                with open("config.json", "r", encoding='utf-8') as f:
                    config = json.load(f)
                if "<!--more-->" in fulltext:  # 摘要分割
                    fulltext_list = fulltext.split("<!--more-->\n")
                    # 读取
                    head_dict = headT.head2json(fulltext_list[0])
                    # set
                    self.LB_postname.setText(fname.split('/')[-1])
                    self.LB_date.setText(head_dict["date"])
                    self.LB_lastmod.setText(head_dict["lastmod"])
                    self.LB_status.setText("加载Post成功！")
                    self.LE_title.setText(head_dict["title"])
                    self.LE_subtitle.setText(head_dict["subtitle"])
                    self.LE_description.setText(head_dict["description"])
                    self.LE_keywords.setText(ut.list2str(head_dict["keywords"]))
                    self.LE_license.setText(head_dict["license"])
                    self.LE_imgeurl.setText(head_dict["featuredImage"])
                    self.LB_tags.setText(ut.list2str(head_dict["tags"]))
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
                    # show in home
                    if head_dict["hiddenFromHomePage"] == "false":
                        self.CB_isshowinhome.setChecked(True)
                    else:
                        self.CB_isshowinhome.setChecked(False)
                    # category
                    if len(head_dict['categories']) > 0 and (head_dict["categories"][0] in config["categories"]):
                        self.CoB_category.setCurrentIndex(config["categories"].index(head_dict["categories"][0]) + 1)
                    else:
                        self.CoB_category.setCurrentIndex(0)
                    # menu
                    if head_dict["menu"] not in config["menu"]:
                        self.CoB_menu.setCurrentIndex(0)
                    else:
                        self.CoB_menu.setCurrentIndex(config["menu"].index(head_dict["menu"]) + 1)
                    # page width, pageStyle
                    page_style = ['narrow', 'normal', 'wide']
                    if head_dict["pageStyle"] not in page_style:
                        self.CoB_pagewidth.setCurrentIndex(1)
                    else:
                        self.CoB_pagewidth.setCurrentIndex(page_style.index(head_dict["pageStyle"]))
                    self.TE_abstract.setText(head_dict["abstract"])
                    self.TE_editor.setText(fulltext_list[1])
                else:
                    self.LB_status.setText('该文档不是网站Post类型！')

    def savefile(self):
        if len(self.LB_postname.text()) == 0:
            self.LB_status.setText('当前Post为空，请加载或新建Post！')
        else:
            self.save_post()

    def load_config(self):
        with open("config.json", "r", encoding='UTF-8') as f:
            config = json.load(f)
            self.LB_author.setText(config["author"])
            self.CoB_tags.addItems(config["tags"])
            self.CoB_category.addItems(config["categories"])
            self.CoB_menu.addItems(config["menu"])
            self.LB_status.setText("已加载网站配置config.json！")
            self.LB_chrome.setText(config["chrome"])
            self.LB_cloud.setText(config['cloud'])
            self.LE_license.setText(config['license'])

    def save_post(self):
        savePath = '../content/posts/' + self.LB_postname.text()
        class_file = open(savePath, 'w')
        self.LB_lastmod.setText(ut.getdate())
        self.LB_status.setText("保存成功！")
        head1_tmpl = open('head1.tmpl', 'r')
        menu_tmpl = open('menu.tmpl', 'r')
        head2_tmpl = open('head2.tmpl', 'r')
        head1_ = Template(head1_tmpl.read())
        menu_ = Template(menu_tmpl.read())
        head2_ = Template(head2_tmpl.read())

        mypost = []
        mypost.append(head1_.substitute(
            title=self.LE_title.text(),
            subtitle=self.LE_subtitle.text(),
            description=self.LE_description.text(),
            keywords="[" + ut.addquotes4list(self.LE_keywords.text()) + "]" if len(self.LE_keywords.text()) > 0 else "",
            license=self.LE_license.text(),
            tags="[" + ut.addquotes4list(self.LB_tags.text()) + "]" if len(self.LB_tags.text()) > 0 else "",
            categories='["' + self.CoB_category.currentText() + '"]' if len(self.CoB_category.currentText()) > 0 else "",
            featuredImage=self.LE_imgeurl.text(),
            showinhome="false" if self.CB_isshowinhome.isChecked() else "true",
            pagestyle=self.CoB_pagewidth.currentText(),
            password=self.LE_password.text() if self.CB_isencryption.isChecked() else "",
            message=self.LE_password_tip.text(),
            author=self.LB_author.text(),
            date=self.LB_date.text(),
            lastmod=self.LB_lastmod.text()))
        if len(self.CoB_menu.currentText()) > 0:
            mypost.append(menu_.substitute(
                menu_flag="#menu_y",
                menu=self.CoB_menu.currentText()))
        else:
            mypost.append('\n#menu_n\n')
        mypost.append(head2_.substitute(
            abstract=self.TE_abstract.toPlainText(),
            editor=self.TE_editor.toPlainText()))

        # 将代码写入文件
        class_file.writelines(mypost)
        class_file.close()
        # 转码
        ut.gb2utf8(savePath)

    def addtags(self):
        new_tag = self.CoB_tags.currentText()
        tags = self.LB_tags.text()
        if new_tag not in tags and new_tag != "":
            if len(tags) != 0:
                tags += ","
            self.LB_tags.setText(tags + new_tag)

    def setEncryptionMode(self):
        if self.CB_isencryption.isChecked():
            self.LE_password.setEnabled(True)
            self.LE_password_tip.setEnabled(True)
        else:
            self.LE_password.setDisabled(True)
            self.LE_password_tip.setDisabled(True)

    def suojin(self):
        pyperclip.copy("&emsp;&emsp;")

    def highlight(self):
        pyperclip.copy("{{< highlight html >}}\n\n{{< /highlight >}}")

    def image(self):
        pyperclip.copy('{{< image src="/images/lighthouse.jpg" caption="Lighthouse" width=400 >}}')

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

    def localserver(self):
        os.popen('cd .. && start "' + self.LB_chrome.text() + '" http://127.0.0.1:1313 && hugo server')

    def cloudserver(self):
        os.system('cd .. && hugo && cd public && git add . && git commit -m "update post" && git push && ssh ' + self.LB_cloud.text())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出PostEditor', "现在退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InitMainWindow()
    sys.exit(app.exec_())
