#!/bin/bash

source ~/桌面/docling-env/bin/activate

# ===== 关键修复 =====
export HF_HUB_OFFLINE=0
export TRANSFORMERS_OFFLINE=0
export HF_DATASETS_OFFLINE=0

# ===== 清代理 =====
unset http_proxy https_proxy all_proxy
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY
unset ftp_proxy FTP_PROXY

echo "🔥 PDF2MD 工业版启动"
python convert.py
