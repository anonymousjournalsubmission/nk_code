import os

pdfs = [f for f in os.listdir() if ('.pdf' in f and 'decrypted' not in f)]
for file in pdfs:
    with open(file, 'rb') as fp:
        decrypted_content = [byte ^ 0xa5 for byte in fp.read()]
    with open(file[:-4] + '_decrypted.pdf', 'wb') as fp:
        fp.write(bytes(decrypted_content))
        
