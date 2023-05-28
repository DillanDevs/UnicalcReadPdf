import re

def reader(texto):
    materias = []

    # Obtener el nombre de la materia y las notas de cada corte
    matches = re.findall(r'(\d{5}-\d\w).*?(\d+\.\d)', texto, re.DOTALL)
    for match in matches:
        codigo_materia = match[0]
        nota_primer_corte = match[1]
        nota_segundo_corte = None
        nota_tercer_corte = None

        # Buscar notas de los otros cortes
        notas_cortes = re.findall(f'{codigo_materia}.*?Nota (Segundo|Tercer) Corte (\d+\.\d)', texto, re.DOTALL)
        for nota_corte in notas_cortes:
            if nota_corte[0] == 'Segundo':
                nota_segundo_corte = nota_corte[1]
            elif nota_corte[0] == 'Tercer':
                nota_tercer_corte = nota_corte[1]

        credito = re.search(codigo_materia + r' .+? (\d+)', texto).group(1)
        
                

        materias.append({
            'nombre': re.findall(f'{codigo_materia}.*?(.*?)\d', texto)[0].strip(),
            'credito': credito[1],
            'primer_corte': nota_primer_corte,
            'segundo_corte': nota_segundo_corte,
            'tercer_corte': nota_tercer_corte
        })
    
    return materias