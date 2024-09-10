base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def base64_decode(encrypted_information):
    if isinstance(encrypted_information, bytes):
        encrypted_information = encrypted_information.decode('utf-8')
    encrypted_information = encrypted_information.rstrip('=')
    bit_string = ''.join(f'{base64_chars.index(c):06b}' for c in encrypted_information if c in base64_chars)
    return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8) if len(bit_string[i:i+8]) == 8)

decrypted_data = base64_decode(read_file('file1.lol'))

with open('file1.png', 'wb') as file:
    file.write(decrypted_data)
