import json
# pyqt
from PyQt5 import QtWidgets
# ui文件
from config_ui import Ui_Config
# 自定义
import util as ut


class Config(QtWidgets.QMainWindow, Ui_Config):
    def __init__(self):
        super(Config, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.PB_saveconfig.clicked.connect(self.save_config)
        self.PB_loadconfig.clicked.connect(self.load_config)

    def open(self):
        self.show()
        # 打开窗口同时加载config.json
        config = ut.loadconfig()
        self.write_config2ui(config)

    def save_config(self):
        config_dict = {}
        config_dict["sitepath"] = self.LE_sitepath.text().strip()
        config_dict["chrome"] = self.LE_chrome.text().strip()

        config_dict["cloudserver"] = self.LE_cloudserver.text().strip()
        config_dict["rsyncuser"] = self.LE_rsyncuser.text().strip()
        config_dict["rsyncuserpasswd"] = self.LE_rsyncuserpasswd.text().strip()

        config_dict["author"] = self.LE_author.text().strip()
        config_dict["categories"] = self.LE_categories.text().split(',')
        config_dict["menu"] = self.LE_menu.text().split(',')
        config_dict["license"] = self.LE_license.text().strip()
        # 写入config.json
        config_json = json.dumps(config_dict, indent=4, ensure_ascii=False)
        with open('config.json', 'w', encoding='utf-8') as json_file:
            json_file.write(config_json)
        # 关闭弹窗
        self.close()

    def load_config(self):
        fname, ok = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", filter="json (*.json)")
        if ok:
            with open(fname, 'r', encoding='utf-8') as f:
                userconfig = json.load(f)
                self.write_config2ui(userconfig)

    def write_config2ui(self, config):
        self.LE_sitepath.setText(config["sitepath"])
        self.LE_chrome.setText(config["chrome"])
        self.LE_cloudserver.setText(config["cloudserver"])
        self.LE_rsyncuser.setText(config["rsyncuser"])
        self.LE_rsyncuserpasswd.setText(config["rsyncuserpasswd"])

        self.LE_author.setText(config["author"])
        self.LE_categories.setText(ut.list2str(config["categories"]))
        self.LE_menu.setText(ut.list2str(config["menu"]))

        self.LE_license.setText(config["license"])
