import re
import random
import string

# Đọc lại nội dung tệp Lua đã tải lên
lua_file_path = "LAUCHERS_SSTR(989888089)"

with open(lua_file_path, "r", encoding="utf-8") as file:
    lua_code = file.read()

# Bước 1: Loại bỏ khoảng trắng và comment
def minify_lua(code):
    code = re.sub(r'--.*', '', code)  # Loại bỏ comment dòng (-- ...)
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)  # Loại bỏ comment khối (--[[ ... ]])
    code = "\n".join(line for line in code.splitlines() if line.strip())  # Loại bỏ dòng trống
    return code

minified_code = minify_lua(lua_code)

# Bước 2: Đổi tên biến thành tên ngẫu nhiên khó đọc
def random_var_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Tạo danh sách biến hợp lệ
tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', minified_code)
reserved_keywords = {"function", "end", "local", "if", "then", "else", "for", "while", "do", "return", "nil", "true", "false"}
var_mapping = {token: random_var_name() for token in set(tokens) if token not in reserved_keywords}

# Thay thế biến bằng tên mới
for old_var, new_var in var_mapping.items():
    minified_code = re.sub(r'\b' + old_var + r'\b', new_var, minified_code)

# Bước 3: Mã hóa chuỗi thành dạng `string.char()`
def encode_string(s):
    return '".."'.join(f'string.char({ord(c)})' for c in s)

minified_code = re.sub(r'"(.*?)"', lambda m: encode_string(m.group(1)), minified_code)

# Lưu lại mã đã obfuscate
import os

# Kiểm tra và tạo thư mục nếu chưa có
obfuscated_file_path = "obfuscated.lua"

with open(obfuscated_file_path, "w", encoding="utf-8") as file:
    file.write(minified_code)

obfuscated_file_path  # Trả về đường dẫn tệp mới
