import qrcode
url=input("Enter the URL to generate QR Code: ").strip()
file_path="D:\\OneDrive\\Desktop\\qrcode.png"
qr = qrcode.QRCode()
qr.add_data(url)
img=qr.make_image()
img.save(file_path) 
print(f"QR Code generated and saved to {file_path}")    