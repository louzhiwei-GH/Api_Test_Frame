"""
    算法MD5加密
"""
# import hashlib

# def md5_encrypt(text):
#     md5 = hashlib.md5()
#     # 更新md5的数据
#     md5.update(text.encode('utf-8'))
#     # 转换数据
#     res = md5.hexdigest()
#     return res


# text = "test"
# res = md5_encrypt(text)
# print(res)


# def new_md5_encrypt(text):
#     res = hashlib.md5(text.encode('utf-8')).hexdigest()
#     return res

# res2 = new_md5_encrypt(text)
# print(res2)

"""
    对称加密算法
"""
import base64
from Crypto.Cipher import AES

class EncrypyDate:
    def __init__(self, key):
        self.key = key.encode("utf-8")
        # 校验密钥长度（16/24/32 字节）
        if len(self.key) not in (16, 24, 32):
            raise ValueError("AES密钥长度必须为16/24/32字节")
        self.length = AES.block_size
        self.aes = AES.new(self.key, AES.MODE_ECB)

    def pad(self, text):
        """
        PKCS#7 填充：使被加密数据的字节长度是 block_size 的整数倍
        支持 str 或 bytes 输入，返回 bytes
        """
        data = text.encode("utf-8") if isinstance(text, str) else text
        pad_len = self.length - (len(data) % self.length)
        if pad_len == 0:
            pad_len = self.length
        padding = bytes([pad_len]) * pad_len
        return data + padding

    def unpad(self, data: bytes) -> bytes:
        """去除 PKCS#7 填充"""
        if not data:
            raise ValueError("待去填充数据为空")
        pad_len = data[-1]
        if pad_len < 1 or pad_len > self.length:
            raise ValueError("无效的填充长度")
        return data[:-pad_len]

    def encrypt(self, text: str) -> str:
        """加密后返回 base64 字符串"""
        padded = self.pad(text)
        cipher_bytes = self.aes.encrypt(padded)
        return base64.b64encode(cipher_bytes).decode("utf-8")

    def decrypt(self, b64_text: str) -> str:
        """解密 base64 字符串，返回原始明文字符串"""
        cipher_bytes = base64.b64decode(b64_text)
        plain_padded = self.aes.decrypt(cipher_bytes)
        plain = self.unpad(plain_padded)
        return plain.decode("utf-8")


key = "1234567812345678"
eg = EncrypyDate(key)

    
