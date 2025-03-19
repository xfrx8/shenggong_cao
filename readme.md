

## 功能

- **手动输入数据**：在网页上输入浓度与电压数据，进行线性回归计算，生成标准曲线图。
- **CSV 文件上传**：上传 CSV 文件（要求包含 `concentration` 和 `voltage` 列），自动解析数据、计算回归并生成图表。
- **预测功能**：根据回归参数计算给定电压对应的浓度值。

## 项目结构

```
.
├── app.py                # Flask 后端应用，包含所有路由及数据处理、绘图代码
├── templates/
│   └── index.html        # 前端 HTML 模板文件，提供用户交互界面
└── README.md             # 本说明文件
```


安装依赖的命令（推荐使用虚拟环境）：

```bash
pip install flask flask_cors numpy matplotlib scipy pandas pywebview
```

## 运行程序

1. **准备模板文件**  
   确保将前端 HTML 文件放在 `templates` 文件夹内，文件名为 `index.html`。

2. **启动 Flask 应用**  
   在项目根目录下运行：

   ```bash
   python app.py
   ```

   运行后，浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 即可看到交互页面。


## 打包为 exe

为了将整个应用打包成独立的可执行文件（exe），你可以使用 [PyInstaller](https://www.pyinstaller.org/) 工具。安装 PyInstaller：

```bash
pip install pyinstaller
```

在项目根目录下执行以下命令打包（注意 Windows 下使用分号分隔源与目标路径；其他系统请使用冒号 `:`）：

```bash
pyinstaller --onefile --windowed --add-data "templates;templates" app.py
```

打包完成后，可执行文件会生成在 `dist` 文件夹内。运行该 exe 文件，即可启动应用，无需安装 Python 环境。

## 注意事项

- **模板文件包含**  
  打包时请确保 `templates` 文件夹被包含进 exe 文件中，否则运行时 Flask 无法找到前端页面。

- **代码调试**  
  如果出现依赖问题或图像生成异常，可先在本地 Python 环境中调试，确保所有功能正常后再进行打包。

---

以上就是本项目的基本说明。希望这个项目能帮助你理解如何使用 Flask 构建 Web 应用、利用纯 Python 实现数据处理与绘图，并最终打包成独立的 exe 文件。
