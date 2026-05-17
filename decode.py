from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import PDFStream
import sys

# ⚠️ 請把下面這個檔名改成你剛剛從 CTF 網站下載下來的 PDF 檔名
pdf_filename = "你下載的PDF檔名.pdf" 

print(f"[*] 正在從 {pdf_filename} 解析 WMF 座標並提取 Flag...")

try:
    fp = open(pdf_filename, "rb")
    doc = PDFDocument(PDFParser(fp), None)
    dstring = ""
    
    # 尋找 PDF 裡面的 Stream (向量繪圖資料)
    for xref in doc.xrefs:
        for objid in xref.get_objids():
            obj = doc.getobj(objid)
            if obj is None:
                continue
            if isinstance(obj, PDFStream) and "Type" in obj.attrs:
                dstring = obj.get_data().decode("ascii")

    if not dstring:
        print("[-] 找不到圖片資料，請確認 Payload 是否正確執行。")
        sys.exit()

    # 提取座標並還原成二進位資料
    coords = [line.split(" ") for line in dstring.split("\n") if len(line.strip()) > 0]
    coords = [(int(c[1]), int(c[0])) for c in coords if c[-1] in "lm"]
    dat = [x for c in coords for x in c][::-1]

    final_data = b''
    for byte_pair in dat:
        bb = byte_pair >> 8
        ba = byte_pair & 0xFF
        final_data += bytes([ba, bb])

    # 印出 Flag (扣掉前面 2 bytes 的 AA padding)
    print("\n[🎉] 破解成功！Flag 內容為：")
    flag_content = final_data[2:].decode("ascii", errors="ignore")
    print(flag_content)

except FileNotFoundError:
    print(f"[-] 找不到檔案 {pdf_filename}，請確認檔名是否正確並放在同一資料夾。")
except Exception as e:
    print(f"[-] 發生錯誤: {e}")
