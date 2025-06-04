# imphm-aws_ggc-daq-NIDAQ-python

基於 Python 的 National Instruments DAQ（數據採集）硬體系統。

## 概述

本專案實現了一個與 National Instruments DAQ 硬體介接的數據採集系統。它提供了讀取類比輸入信號和管理數據採集過程的功能。

## 專案結構

```
aws_ggc-daq-NIDAQ-python/
├── API/
│   └── NiDAQ.ini          # DAQ 設定檔
├── src/
│   ├── main.py           # 主應用程式入口點
│   └── nidaq_module.py   # 核心 DAQ 功能實現
├── requirements.txt      # Python 依賴項
├── recipe.yaml          # 專案配方配置
└── gdk-config.json      # GDK 配置文件
```

## 系統需求

- Python 3.x
- National Instruments DAQ 硬體
- 已安裝 NI-DAQmx 驅動程式

## 安裝步驟

1. 複製專案：
```bash
git clone https://github.com/JW-Albert/aws_ggc-daq-NIDAQ-python.git
cd aws_ggc-daq-NIDAQ-python
```

2. 安裝所需依賴：
```bash
pip install -r requirements.txt
```

## 配置

1. 在 `API/NiDAQ.ini` 中配置您的 DAQ 設定
2. 根據需要調整 `gdk-config.json` 中的參數

## 使用方法

運行主應用程式：
```bash
python src/main.py
```

## 開發

### 本地部署

進行本地部署：
```bash
./local_deploy.sh
```

移除本地部署：
```bash
./remove_local_deploy.sh
```

## 授權

[在此指定您的授權方式]

## 貢獻指南

[在此添加貢獻指南] 