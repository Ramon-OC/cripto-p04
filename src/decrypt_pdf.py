def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def brute_force_pdf(encrypted_information):
    for shift in range(256):
        decrypted_data = bytes((byte - shift) % 256 for byte in encrypted_information)
        if decrypted_data.startswith(b'%PDF'):
            return decrypted_data
    return None

decrypted_data = brute_force_pdf(read_file('file2.lol'))

with open('file2.pdf', 'wb') as file:
    file.write(decrypted_data)
