# Función para calcular el inverso multiplicativo modular
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Función para cifrar con el cifrado afín para bytes
def cifrar_afin_bytes(datos, a, b):
    resultado = bytearray()  
    N = 256  # Tamaño del espacio de bytes (0-255)
    for byte in datos:
        cifrado = (a * byte + b) % N
        resultado.append(cifrado)
    return bytes(resultado)

# Función para descifrar con el cifrado afín para bytes
def descifrar_afin_bytes(datos, a, b):
    resultado = bytearray()
    N = 256  # Tamaño del espacio de bytes (0-255)
    a_inv = mod_inverse(a, N)  # Calculamos el inverso multiplicativo de 'a'
    
    if a_inv is None:
        raise ValueError(f"No existe el inverso multiplicativo para 'a={a}' y módulo {N}")

    for byte in datos:
        descifrado = (a_inv * (byte - b)) % N
        resultado.append(descifrado)
    return bytes(resultado)

# Función para resolver el sistema de ecuaciones modulares y encontrar a y b
def encontrar_a_b(x1, c1, x2, c2, N):
    delta_x = (x1 - x2) % N
    delta_c = (c1 - c2) % N
    delta_x_inv = mod_inverse(delta_x, N)
    
    if delta_x_inv is None:
        raise ValueError(f"No existe el inverso multiplicativo para delta_x={delta_x} y módulo {N}")
    
    a = (delta_c * delta_x_inv) % N
    b = (c1 - a * x1) % N
    
    return a, b

# Función para identificar el tipo de archivo basado en los bytes descifrados
def probar_firmas(datos_cifrados):
    firmas = {
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
        b'%PDF': 'PDF',
        b'\xFF\xFB': 'MP3',
        b'\xFF\xF3': 'MP3',
        b'\x49\x44\x33': 'MP3',
        b'\xFF\xF2': 'MP3',
        b'\x00\x00\x00\x20\x66\x74\x79\x70': 'MP4',
    }
    
    N = 256  # Tamaño del espacio de bytes (0-255)
    
    primeros_bytes_cifrados = datos_cifrados[:8]

    # Probar cada firma conocida
    for firma_real, tipo_archivo in firmas.items():
        longitud_firma = len(firma_real)
        
        # Probar todas las combinaciones de pares de puntos en los primeros bytes
        for i in range(longitud_firma):
            for j in range(i + 1, longitud_firma):
                # Intentamos descifrar usando los puntos i y j de la firma y del archivo cifrado
                try:
                    # Obtener valores a y b resolviendo las ecuaciones modulares
                    a, b = encontrar_a_b(firma_real[i], primeros_bytes_cifrados[i], firma_real[j], primeros_bytes_cifrados[j], N)
                    
                    # Descifrar los primeros bytes usando los valores de a y b encontrados
                    primeros_bytes_descifrados = descifrar_afin_bytes(primeros_bytes_cifrados, a, b)
                    
                    # Verificar si los primeros bytes descifrados coinciden con la firma real
                    if primeros_bytes_descifrados[:longitud_firma] == firma_real:
                        print(f"Archivo identificado como {tipo_archivo}")
                        print(f"Valores de a: {a}, b: {b}")
                        return a, b, tipo_archivo
                except ValueError:
                    # Si no se puede encontrar el inverso o hay error, continuamos con la siguiente pareja
                    continue
    
    # Si no encontramos coincidencias, devolvemos "Desconocido"
    return None, None, "Desconocido"


# Función para descifrar todo el archivo si se encuentra la firma correcta
def descifrar_archivo_completo(file_path):
    # Leer el archivo cifrado
    with open(file_path, 'rb') as f:
        datos_cifrados = f.read()
    
    # Intentar encontrar los valores de a y b y el tipo de archivo
    a, b, tipo_archivo = probar_firmas(datos_cifrados)
    
    if a is not None and b is not None:
        # Descifrar todo el archivo
        datos_descifrados = descifrar_afin_bytes(datos_cifrados, a, b)
        
        # Guardar el archivo descifrado
        output_file = f'archivo_descifrado.{tipo_archivo.lower()}'
        with open(output_file, 'wb') as f:
            f.write(datos_descifrados)
        
        print(f"Archivo descifrado guardado como: {output_file}")
    else:
        print("No se pudo identificar el archivo o descifrar los encabezados.")

# Ejemplo de uso
descifrar_archivo_completo('file3.lol')
