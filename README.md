# README

[TOC]

## 1. 环境

- Windows 10 x64
- Pycharm
- Python 3.9

## 2. 依赖

- PyQt5 5.15.6
- SpeechRecognition 3.8.1
- playsound 1.3.0

## 3. 运行

1. playsound包中在windows下运行时需要对该包文件进行修改，\~\\~\Lib\site-packages\playsound.py下进行如下修改：

   - 第55行左右

     ```python
         def winCommand(*command):
             bufLen = 600
             buf = c_buffer(bufLen)
             # command = ' '.join(command).encode('utf-16') 
             # 改成下面这样
             command = ' '.join(command) 
             errorCode = int(windll.winmm.mciSendStringW(command, buf, bufLen - 1, 0)) 
     ```

   - 第61行左右

     ```python
      if errorCode:
                 errorBuffer = c_buffer(bufLen)
                 windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)  # use widestring version of the function
                 exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
                                     # 注释掉下面这一行
                                     # '\n        ' + command.decode('utf-16') +
                                     '\n    ' + errorBuffer.raw.decode('utf-16').rstrip('\0'))
                 logger.error(exceptionMessage)
                 raise PlaysoundException(exceptionMessage)
     ```

   此时程序即可正确运行

2. 启动方式

   - 方式一：在 Pycharm 中打开整个项目文件，在 main.py 中点击运行
   - 方式二：在命令行进入当前目录，并输入 python main.py 运行

## 4. 功能说明

- 说 “hello” 唤醒语音助手


![](/image/image-20220427224353932.png)


- 点击屏幕显示全部指令

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220427224337776.png" style="zoom:50%;" /> 

  再次点击返回上级界面

- 启动状态界面

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220427224448546.png" style="zoom:50%;" /> 

- 说不同的指令来实现不同功能

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220427225119531.png" style="zoom:50%;" /> 

- 播放音乐

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220427230839476.png" style="zoom:50%;" /> 

- 打开记事本

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220428111813282.png" alt="image-20220428111813282" style="zoom:50%;" /> 

- 打开计算器

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220428112308057.png" alt="image-20220428112308057" style="zoom:50%;" /> 

- 打开必应

  <img src="D:\文件\前端\项目\语音交互系统\voice\program\image\image-20220428112134021.png" alt="image-20220428112134021" style="zoom:50%;" /> 

## 5.项目结构

```
--
├── main.py
├── interface.py
└── assets
	├── bg.jpg 
	├── bg.png 
	├── bg-none.png
	├── onMusic.gif 
	├── 名侦探.mp3
```

