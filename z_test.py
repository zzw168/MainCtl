from PySide6.QtWidgets import QApplication, QTextBrowser, QVBoxLayout, QWidget

app = QApplication([])

# 创建窗口和 QTextBrowser
window = QWidget()
layout = QVBoxLayout()
text_browser = QTextBrowser()
layout.addWidget(text_browser)
window.setLayout(layout)

# 设置初始文本
initial_text = "第一行\n第二行\n第三行\n第四行\n第五行\n第六行"
text_browser.setText(initial_text)

# 获取当前文本内容
text_lines = text_browser.toPlainText().splitlines()

# 修改倒数第一行内容
if len(text_lines) >= 1:
    text_lines[-1] = "这是新的倒数第一行内容"

# 将修改后的内容重新设置到 QTextBrowser
new_text = "\n".join(text_lines)
text_browser.setText(new_text)

# 显示窗口
window.show()
app.exec()
