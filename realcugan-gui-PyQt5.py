import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
                             QHBoxLayout, QComboBox, QFileDialog, QMessageBox, QCheckBox, QGridLayout)
from PyQt5.QtGui import QFont

class RealcuganGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Realcugan GUI")
        self.resize(650, 400)  # 设置窗口大小

        # 获取屏幕的尺寸
        screen_geometry = QApplication.desktop().screenGeometry()

        # 获取屏幕宽度和高度
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 获取窗口的尺寸
        window_width = self.width()
        window_height = self.height()

        # 计算窗口位置，使其居中
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置
        self.move(x, y)

        # 设置窗口的字体为微软雅黑
        self.setFont(QFont("微软雅黑", 10))

        # 输入路径
        lbl_input = QLabel("输入路径:")
        self.input_path = QLineEdit()
        btn_file = QPushButton("选择文件")
        btn_folder = QPushButton("选择文件夹")
        btn_file.clicked.connect(self.on_select_file)
        btn_folder.clicked.connect(self.on_select_folder)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_input)
        hbox1.addWidget(self.input_path)
        hbox1.addWidget(btn_file)
        hbox1.addWidget(btn_folder)

        # 输出路径
        lbl_output = QLabel("输出路径:")
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(lbl_output)
        hbox2.addWidget(self.output_path)

        # 参数设置
        grid = QGridLayout()
        self.noise_level = QComboBox()
        self.noise_level.addItems(['-1', '0', '1', '2', '3'])
        self.noise_level.setCurrentText('-1')

        self.scale = QComboBox()
        self.scale.addItems(['1', '2', '3', '4'])
        self.scale.setCurrentText('2')

        self.tile_size = QLineEdit('400')

        self.sync_mode = QComboBox()
        self.sync_mode.addItems(['0', '1', '2', '3'])
        self.sync_mode.setCurrentText('1')

        self.gpu_id = QLineEdit()

        self.model_path = QComboBox()
        self.model_path.addItems(['models-se', 'models-pro'])
        self.model_path.setCurrentText('models-se')

        self.tta_checkbox = QCheckBox()

        # 添加鼠标提示
        self.noise_level.setToolTip("-n 降噪等级（-1/0/1/2/3，默认=-1），数值越大降噪越强，-1表示不降噪")
        self.scale.setToolTip("-s 放大倍数（1/2/3/4，默认=2），表示放大倍数，例如2表示放大2倍")
        self.tile_size.setToolTip("-t 分块大小（>=32，0=自动，默认=400），控制处理的图像块大小，值越小越省GPU内存")
        self.sync_mode.setToolTip("-c 同步间隔模式（0/1/2/3，默认=1），0=不同步，1=精确同步，2=粗略同步，3=非常粗略的同步")
        self.gpu_id.setToolTip("-g 使用的GPU编号（-1=使用CPU，默认=自动）")
        self.model_path.setToolTip("-m RealCUGAN模型路径（默认=models-se）")
        self.tta_checkbox.setToolTip("-x 启用TTA模式（不推荐启用，效果不明显且处理时间会大幅增加）")

        labels = ["降噪等级 (-1/0/1/2/3):", "放大倍数 (1/2/3/4):", "分块大小 (>=32/0=自动):",
                  "同步模式 (0/1/2/3):", "GPU编号 (-1=CPU):", "模型路径 (se/pro):", "TTA:"]
        widgets = [self.noise_level, self.scale, self.tile_size,
                   self.sync_mode, self.gpu_id, self.model_path, self.tta_checkbox]

        for i, (label, widget) in enumerate(zip(labels, widgets)):
            row = i // 2
            col = (i % 2) * 2
            grid.addWidget(QLabel(label), row, col)
            grid.addWidget(widget, row, col + 1)

        # 命令预览和按钮
        self.cmd_preview = QTextEdit()
        self.cmd_preview.setReadOnly(True)

        btn_generate = QPushButton("生成命令")
        btn_generate.clicked.connect(self.on_generate_cmd)
        btn_copy = QPushButton("复制命令")
        btn_copy.clicked.connect(self.on_copy_cmd)
        btn_run = QPushButton("运行")
        btn_run.clicked.connect(self.on_run_cmd)
        btn_reset = QPushButton("恢复默认设置")
        btn_reset.clicked.connect(self.on_reset_defaults)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(btn_generate)
        hbox3.addWidget(btn_copy)
        hbox3.addWidget(btn_run)
        hbox3.addWidget(btn_reset)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(grid)
        layout.addWidget(self.cmd_preview)
        layout.addLayout(hbox3)

        self.setLayout(layout)

    def on_select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "图像文件 (*.jpg *.png *.webp);;所有文件 (*.*)")
        if file_path:
            self.input_path.setText(file_path)
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            output_path = os.path.join(os.path.dirname(file_path), f"{file_name}_output{file_ext}")

            output_path, _ = QFileDialog.getSaveFileName(self, "选择输出文件", output_path,
                                                         "图像文件 (*.jpg *.png *.webp);;所有文件 (*.*)")
            if output_path:
                self.output_path.setText(output_path)
                self.check_overwrite(file_path, output_path)

    def on_select_folder(self):
        input_path = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if input_path:
            self.input_path.setText(input_path)
            output_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
            if output_path:
                self.output_path.setText(output_path)
                self.check_overwrite(input_path, output_path)

    def check_overwrite(self, input_path, output_path):
        if input_path == output_path:
            QMessageBox.warning(self, "警告", "输入路径和输出路径相同，原文件将被覆盖！")

    def on_generate_cmd(self):
        cmd = self.generate_command()
        self.cmd_preview.setPlainText(cmd)

    def on_copy_cmd(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.cmd_preview.toPlainText())

    def on_run_cmd(self):
        cmd = self.generate_command()
        self.cmd_preview.setPlainText(cmd)
        try:
            subprocess.run(cmd, shell=True, check=True)
            QMessageBox.information(self, "提示", "命令运行成功！")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "错误", f"运行失败: {e}")

    def on_reset_defaults(self):
        self.noise_level.setCurrentText('-1')
        self.scale.setCurrentText('2')
        self.tile_size.setText('400')
        self.sync_mode.setCurrentText('1')
        self.gpu_id.setText('')
        self.model_path.setCurrentText('models-se')
        self.tta_checkbox.setChecked(False)

    def generate_command(self):
        realcugan_path = os.path.join('realcugan-ncnn-vulkan', 'realcugan-ncnn-vulkan.exe')
        input_path = self.input_path.text()
        output_path = self.output_path.text()
        noise_level = self.noise_level.currentText()
        scale = self.scale.currentText()
        tile_size = self.tile_size.text()
        sync_mode = self.sync_mode.currentText()
        gpu_id = self.gpu_id.text()
        model_path = self.model_path.currentText()
        tta = self.tta_checkbox.isChecked()

        cmd = f'"{realcugan_path}" -v -i "{input_path}" -o "{output_path}" -n {noise_level} -s {scale} -t {tile_size} -c {sync_mode} -m {model_path}'
        if gpu_id.strip():
            cmd += f' -g {gpu_id.strip()}'
        if tta:
            cmd += ' -x'
        return cmd

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RealcuganGUI()
    gui.show()
    sys.exit(app.exec_())
