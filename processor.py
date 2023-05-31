import re

def eliminar_repeticiones(texto):
    # Eliminar líneas vacías y espacios en blanco adicionales
    texto = re.sub(r'\n+', '\n', texto.strip())

    # Eliminar líneas con "Unico Corte", "Primer Corte", "Segundo Corte" y "Tercer Corte"
    # y mover los decimales a las líneas anteriores
    texto = re.sub(r'(Único|Primer|Segundo|Tercer) Corte,?(\d+\.\d+)', r'\2', texto)

    # Eliminar las comas antes de las notas en las líneas siguientes
    texto = re.sub(r',Nota ', ' ', texto)

    texto = eliminar(texto)

    return texto

def eliminar(texto):
    lines = texto.split("\n")
    text_filter = []

    for line in lines:
        if line == "Único Corte" or line == "Primer Corte" or line == "Segundo Corte" or line == "Tercer Corte":
            continue
        else:
            text_filter.append(line)


    result = "\n".join(text_filter)
    return result


def combinar_lineas(text):
    lines = text.split('\n')
    merged_lines = []
    current_line = ''

    for line in lines:
        if line.strip().replace('.', '').isdigit():
            current_line += ' ' + line.strip()
        else:
            if current_line:
                merged_lines.append(current_line)
            current_line = line.strip()

    if current_line:
        merged_lines.append(current_line)

    return '\n'.join(merged_lines)

def unir_materias_divididas(texto):
    lineas = texto.split('\n')  # Dividir el texto en líneas
    resultado = []
    materia_actual = ''

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if re.match(r'^\d{5}-\d[Ll]', linea) and not re.search(r'Nota Primer Corte \d+\.\d+$', linea):
            materia_actual = lineas[i] + ' ' + lineas[i+1]
            resultado.append(materia_actual)  # Agregar materia_actual al resultado

            i += 1  # Avanzar una línea adicional para omitir la siguiente línea
        else:
            resultado.append(linea)  # Agregar la línea al resultado

        i += 1  # Avanzar a la siguiente línea

    return '\n'.join(resultado)

def formato_final(texto):
    lineas = texto.split('\n')
    nuevas_lineas = []

    patron_codigo = r'\d{5}-\d[A-Z]'
    patron_nombre = r'[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+'

    for linea in lineas:
        if re.match(patron_codigo, linea):
            indice_inicio_numero = re.search(r'\d', linea).start()
            nombre_materia = linea[indice_inicio_numero:]
            nombre_materia = re.sub(patron_nombre, r'\g<0> ', nombre_materia)
            nueva_linea = linea[:indice_inicio_numero] + nombre_materia
            nuevas_lineas.append(nueva_linea)
        else:
            nuevas_lineas.append(linea)

    nuevo_texto = '\n'.join(nuevas_lineas)
    return nuevo_texto



def reader(texto):
    materias_unica_nota = []
    materias_tres_cortes = []

    # Obtener las materias con "Nota Único Corte"
    matches_unica_nota = re.findall(r'(\d{5}-\d\w).*?Nota\s*Único\s*Corte\s*([A-F]|\s*)', texto, re.DOTALL)
    for match in matches_unica_nota:
        codigo_materia = match[0]
        unica_nota = match[1].strip() if match[1] else None

        if unica_nota == '':
            unica_nota = None

        credito_Bi = re.search(codigo_materia + r' .+? (\d+)', texto).group(1)

        materias_unica_nota.append({
            'nombre': re.findall(rf'{codigo_materia}.*?(.*?)\d', texto, re.DOTALL)[0].strip(),
            'credito': credito_Bi[1],
            'Unica_nota': unica_nota
        })

    matches_tres_notas = re.findall(r'(\d{5}-\d\w)(?!.*Nota\s+Único\s+Corte).*?Nota\s+Primer\s+Corte\s+(\d+\.\d)', texto, re.DOTALL)

    for match in matches_tres_notas:
        codigo_materia = match[0]
        nota_primer_corte = match[1]
        nota_segundo_corte = None
        nota_tercer_corte = None

        notas_cortes = re.findall(f'{codigo_materia}.*?Nota\s+Segundo\s+Corte\s+(\d+\.\d)(?:.*?Nota\s+Tercer\s+Corte\s+(\d+\.\d|\s*))?', texto, re.DOTALL)

        for nota_corte in notas_cortes:
            nota_segundo_corte = nota_corte[0]
            nota_tercer_corte = nota_corte[1].strip() if nota_corte[1] else None

        credito = re.search(codigo_materia + r' .+? (\d+)', texto).group(1)

        materias_tres_cortes.append({
            'nombre': re.findall(rf'{codigo_materia}.*?(.*?)\d', texto, re.DOTALL)[0].strip(),
            'credito': credito[1],
            'primer_corte': nota_primer_corte,
            'segundo_corte': nota_segundo_corte,
            'tercer_corte': nota_tercer_corte
        })

    # Combinar las materias con "Nota Único Corte" y las de tres cortes
    materias = materias_unica_nota + materias_tres_cortes

    return materias