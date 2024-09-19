### [English](README.md) / [Русский](README_RU.md) / 中文

**Alex(GoD) tool for .trans**

这是一个简单的 GUI 应用程序，用于从/向 .trans 文件（通常用于游戏本地化）提取和添加字符串。

![image](https://github.com/user-attachments/assets/19307c0f-eb01-4acf-9a19-0187676bad35) ![image](https://github.com/user-attachments/assets/a0c52db5-e283-4bcb-a3fd-21087fb0d6c0)
![image](https://github.com/user-attachments/assets/bdeb6b7e-a67f-462d-826d-e8356ff56e21)

**功能：**

* 从 .trans 文件的选定列中提取字符串。
* 将字符串从文本文件添加到 .trans 文件的选定列。
* 以表格格式预览 .trans 文件的内容。
* 选择要从 .trans 文件中提取的特定文件。
* 深色主题，改善视觉体验。

**如何使用：**

1. 使用“浏览”按钮选择 .trans 文件。
2. 使用单选按钮选择要从中提取字符串的列。
3. 单击“提取字符串”将字符串提取到名为“output_strings.txt”的文本文件中。
4. 要添加字符串，请选择输出文本文件和要添加到的列。
5. 单击“添加字符串”将字符串添加到 .trans 文件（将创建一个带有“_modified”后缀的新文件）。
A. 使用“预览”按钮查看 .trans 文件的内容。
B. 使用“选择文件”按钮选择要从中提取字符串的特定文件。

**要求：**

* Python 3
* Tkinter
* ttkthemes

**安装：**

1. 安装所需的软件包：
   ```
   pip install tkinter ttkthemes
   ```
2. 下载脚本。
3. 运行脚本：
   ```
   python TransExtractor.py
   ```
