import os
from pathlib import Path
from tqdm import tqdm

# ===== 工业稳定环境锁死 =====
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

# 干掉代理（你刚刚报错的根源）
for k in ["http_proxy","https_proxy","all_proxy",
          "HTTP_PROXY","HTTPS_PROXY","ALL_PROXY",
          "ftp_proxy","FTP_PROXY"]:
    os.environ.pop(k, None)

pdf_dir = Path("./input")
out_dir = Path("./output")
out_dir.mkdir(exist_ok=True)

pdf_files = list(pdf_dir.rglob("*.pdf"))
print(f"📄 PDF数量: {len(pdf_files)}")

# ===== 尝试 docling =====
USE_DOCLING = True
try:
    from docling.document_converter import DocumentConverter
    converter = DocumentConverter()
except Exception:
    USE_DOCLING = False
    import fitz

def convert_docling(pdf):
    result = converter.convert(str(pdf))
    return result.document.export_to_markdown()

def convert_pymupdf(pdf):
    doc = fitz.open(pdf)
    return "\n".join(page.get_text() for page in doc)

for pdf in tqdm(pdf_files):
    try:
        if USE_DOCLING:
            md = convert_docling(pdf)
        else:
            md = convert_pymupdf(pdf)

        out_file = out_dir / f"{pdf.stem}.md"
        out_file.write_text(md, encoding="utf-8")

        print("OK:", pdf.name)

    except Exception as e:
        print("FAIL:", pdf.name, e)

print("✅ 全部完成")
