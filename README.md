# 文档对比工具

自动对比两份纯文本文档，以不同颜色高亮形式输出。

增删部分分两行显示，无变化部分仅显示一行原文。

Demo： https://xlu.pythonanywhere.com/

## 使用方法

### 作为flask应用

```sh
gunicorn docdiff:app
```

或者

```sh
python docdiff.py -r
```

### 终端运行

注意：终端需支持标准的颜色转义字符串（如尝试执行`printf "\e[31mRed\e[0m\n"`）

```
usage: docdiff.py [-h] [-f FILE FILE] [-l] [-r]

options:
  -h, --help            show this help message and exit
  -f FILE FILE, --file FILE FILE
                        Input files
  -l, --line            Fast line-by-line comparison
  -r, --run-flask       Run built-in flask app in terminal
```
