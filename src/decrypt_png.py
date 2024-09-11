base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def read_file(file_path):
    """
    Lee un archivo y devuelve su contenido en bytes.

    Args:
        file_path (str): La ruta del archivo a leer.

    Returns:
        bytes: El contenido del archivo.
    """
    with open(file_path, 'rb') as file:
        return file.read()

def base64_decode(encrypted_information):
    """
    Decodifica una cadena codificada en base64.

    Args:
        encrypted_information (str or bytes): La información codificada en base64.

    Returns:
        bytes: La información decodificada.
    """
    if isinstance(encrypted_information, bytes):
        encrypted_information = encrypted_information.decode('utf-8')
    encrypted_information = encrypted_information.rstrip('=')
    bit_string = ''.join(f'{base64_chars.index(c):06b}' for c in encrypted_information if c in base64_chars)
    return bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8) if len(bit_string[i:i+8]) == 8)

# Lee el archivo codificado en base64
decrypted_data = base64_decode(read_file('file1.lol'))

# Guarda los datos decodificados en un archivo PNG
with open('file1.png', 'wb') as file:
    file.write(decrypted_data)