def extrair_dados_classe(filename):
    split = filename.split('.csv')[0].split('_')
    return str.capitalize(split[0] + " " + split[1])