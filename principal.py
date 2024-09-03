from extrair_dados_classe import extrair_dados_classe
import sys
import os

disciplinas = {}
alunos_turma = {}






def ler_dados(filename):

    nome_arquivo = extrair_dados_classe(filename)
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f"\n ---- LENDO DADOS DA {nome_arquivo} ----")
        arquivo.write('\n')
    # Os arquivos se encontram em uma pasta 'data' dentro do meu projeto
    file = open(f'{caminho}//{filename}')
    files = file.read()
    # Precisa fechar o arquivo depois de ler
    file.close()
    return files

def dados(data):
    linha_1 = data.split('\n')[0].split(',')
    linha_2 = data.split('\n')[1]

    CODIGO = linha_1[0].strip()
    NOME = linha_1[1].strip()
    MEDIA_MINIMA = float(linha_2.split(',')[0].strip())
    PESOS = [float(linha_2.split(',')[i].strip()) for i in range(1, 4)]

    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f'\nCODIGO: {CODIGO}\n')
        arquivo.write(f'\nNOME DA DISCIPLINA: {NOME}\n')

    return CODIGO, NOME, PESOS, MEDIA_MINIMA


def ler_dados_aluno(line):

    matricula = line.split(',')[0]
    notas = []
    for nota in line.split(',')[1:4]:
        notas.append(float(nota))
    return matricula, notas ##ENTRA NO DICT ALUNOS_TURMA

def ler_alunos(data):
    quantidade_alunos = 0
    lines = data.strip().split('\n')[2:]
    alunos = {}

    codigo, nome, pesos, media_minima = dados(data)
    for line in lines:
        if line:
            quantidade_alunos += 1
            matricula, notas = ler_dados_aluno(line)
            alunos[matricula] = notas
            media_aluno = calculo_notas(notas, pesos)

    # Contabilizar em quantas disciplinas o aluno está matriculado
            if matricula not in alunos_turma:
                info_alunos = {}
                info_alunos['MEDIAS'] = [media_aluno]
                info_alunos['DISCIPLINAS'] = [nome]
                if media_aluno >= media_minima:
                    info_alunos['APROVAÇÃO'] = [True]
                else:
                    info_alunos['APROVAÇÃO'] = [False]
                alunos_turma[matricula] = info_alunos
            else:
                alunos_turma[matricula]['MEDIAS'].append(media_aluno)
                                   # chave  #valor
                if media_aluno >= media_minima:
                    alunos_turma[matricula]['APROVAÇÃO'].append(True)
                else:
                    alunos_turma[matricula]['APROVAÇÃO'].append(False)
                alunos_turma[matricula]['DISCIPLINAS'].append(nome)

    disciplina = {}


    disciplina['NOME'] = nome
    disciplina['PESOS'] = pesos
    disciplina['MEDIA MINIMA'] = media_minima
    disciplina['QUANTIDADE DE ALUNOS'] = quantidade_alunos



    percentagem, media_turma, qtd_aprovados, alunos_com_media_maior = calculo_aprovado(alunos, pesos, media_minima, quantidade_alunos)
    porc_aprovados = percentagem
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f"\nPERCENTUAL DE APROVADOS: {porc_aprovados:.1f}%")
        arquivo.write('\n')

    # if porc_aprovados > maior_taxa:
    #     maior_taxa = porc_aprovados
    # if porc_aprovados < menor_taxa:
    #     menor_taxa = porc_aprovados

    disciplina['MEDIA TOTAL DA TURMA'] = media_turma
    disciplina['QUANTIDADE DE ALUNOS APROVADOS'] = qtd_aprovados
    disciplina['PERCENTAGEM APROVADOS'] = porc_aprovados
    disciplinas[f'{codigo}'] = disciplina

    return alunos_turma

# PARA CADA TURMA
def calculo_notas(notas, pesos):
    pesos_pesos = 0
    numerador = 0
    for nota in notas:
        for peso in pesos:
            numerador = (notas[0] * pesos[0]) + (notas[1] * pesos[1]) + (notas[2] * pesos[2])
            pesos_pesos = pesos[0] + pesos[1] + pesos[2]
            break
    media_aluno = numerador / pesos_pesos
    return media_aluno


def calculo_aprovado(alunos, pesos, media, qtd_alunos):
    qtd_aprovados = 0
    soma_turma = 0
    alunos_com_media_maior = 0
    medias = []

    for matricula, notas in alunos.items():
        media_aluno = calculo_notas(notas, pesos)
        medias.append(media_aluno)
        soma_turma += media_aluno
        if media_aluno >= media:
            qtd_aprovados += 1

    minimo = min(medias)
    maximo = max(medias)
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f'\nMEDIA MINIMA: {minimo:.1f}')
        arquivo.write(f'\nMEDIA MAXIMA: {maximo:.1f}')
        arquivo.write(f'\nQUANTIDADE DE ALUNOS MATRICULADAS NA DISCIPLINA:{qtd_alunos}')

    percentual = (qtd_aprovados / qtd_alunos) * 100
    media_turma = soma_turma / qtd_alunos
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f'\nESSA É A MEDIA DA TURMA: {media_turma:.1f}')
    for media_aluno in medias:
        if media_aluno > media_turma:
            alunos_com_media_maior += 1
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f"\nESSA É A QUANTIDADE DE ALUNOS COM A NOTA ACIMA DA MEDIA DA TURMA: {alunos_com_media_maior}")


    return percentual, media_turma, qtd_aprovados, alunos_com_media_maior

#CALCULO MEDIA GLOBAL / ESTATISTICAS GLOBAIS

def media_global(disciplinas):

     percentual_global_turmas = 0
     media_turma_soma = 0
     cont = 0
     soma_aprovados = 0
     soma_alunos = 0


     for materias in disciplinas.values():

        media_turma_soma += materias['MEDIA TOTAL DA TURMA']
        cont += 1
        soma_aprovados += materias['QUANTIDADE DE ALUNOS APROVADOS']
        soma_alunos += materias['QUANTIDADE DE ALUNOS']

     media_global_turmas = media_turma_soma/cont
     percentual_global_turmas = (soma_aprovados / soma_alunos) * 100
     with open('RESULTADO.txt', "a") as arquivo:
         arquivo.write('\n')
         arquivo.write('\n-------ESTATISTICAS GLOBAIS--------')
         arquivo.write('\n')
         arquivo.write(f"\nMEDIA GLOBAL DAS TURMAS: {media_global_turmas:.1f}")
         arquivo.write(f"\nPERCENTUAL DE APROVAÇÃO GLOBAL: {percentual_global_turmas:.1f}%")

# b) (1.0) Quantidade de alunos matriculados em mais de 2 disciplinas do
# professor

def matriculado_mais_2_disciplinas():
    matriculado_mais_2 = 0

    for matricula in alunos_turma:
        lista_de_disciplinas = alunos_turma[matricula]['DISCIPLINAS']
        if len(lista_de_disciplinas) > 2:
            matriculado_mais_2 += 1
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f"\nQUANTIDADE DE ALUNOS MATRICULADOS EM MAIS DE 2 DISCIPLINAS: {matriculado_mais_2}")

# c) (1.0) Quantidade e percentual de alunos aprovados em TODAS as
# disciplinas que estavam matriculados

def aprovados_todas_disciplinas():
    aprovado_1 = 0
    cont = 0

    for matricula in alunos_turma:
        nao_aprovado = False
        if nao_aprovado not in alunos_turma[matricula]['APROVAÇÃO']:
            aprovado_1 += 1

    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write(f"\nQUANTIDADE DE ALUNOS APROVADOS EM TODAS AS DISCIPLINAS: {aprovado_1}")
        arquivo.write(f"\nPERCENTUAL DE ALUNOS APROVADOS EM TODAS AS DISCIPLINAS: {((aprovado_1 /len(alunos_turma)) * 100):.1f}%")


#d) (1.0) Disciplinas com a maior e a menor taxa de aprovação: Nome e taxa

def disciplina_taxa_nome(disciplinas):
    cont = 0
    maior_taxa = 0
    menor_taxa = 0
    maior_nome = ''
    menor_nome = ''

    for disciplina in disciplinas.values():
        if cont == 0:
            maior_taxa = disciplina['PERCENTAGEM APROVADOS']
            menor_taxa = disciplina['PERCENTAGEM APROVADOS']
            maior_nome = disciplina['NOME']
            menor_nome = disciplina['NOME']
        else:
            if disciplina['PERCENTAGEM APROVADOS'] > maior_taxa:
                maior_taxa = disciplina['PERCENTAGEM APROVADOS']
                maior_nome = disciplina['NOME']
            elif disciplina['PERCENTAGEM APROVADOS'] < menor_taxa:
                menor_taxa = disciplina['PERCENTAGEM APROVADOS']
                menor_nome = disciplina['NOME']
        cont += 1
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write('\n')
        arquivo.write(f'\nESSA É A MAIOR TAXA DE APROVAÇÃO: {maior_taxa:.1f}%')
        arquivo.write(f'\nESSA É O MAIOR NOME: {maior_nome}')
        arquivo.write(f'\nESSA É A MENOR TAXA DE APROVAÇÃO: {menor_taxa:.1f}%')
        arquivo.write(f'\nESSA É O MENOR NOME: {menor_nome}')


# ESTATISTICAS DE CADA ALUNO

# a) (0.5) Taxa de aprovação. Exemplo: Um aluno matriculado em 2 disciplinas
# e que foi aprovado apenas em uma teve 50% de taxa de aprovação
# b) (0.5) Disciplinas nas quais obteve a sua melhor média – nome e média
# c) (0.5) Disciplinas nas quais obteve a sua pior média – nome e média

def estatisticas_aluno(alunos_turma):
    taxa_aprovaçao = 0
    with open('RESULTADO.txt', "a") as arquivo:
        arquivo.write('\n')
        arquivo.write('\n-------ESTATISTICAS DE CADA ALUNO--------')
    for matricula in alunos_turma:
        #LISTAS
        lista_aprovados = alunos_turma[matricula]['APROVAÇÃO']
        list_medias = alunos_turma[matricula]['MEDIAS']
        lista_disciplinas = alunos_turma[matricula]['DISCIPLINAS']

        cont = 0
        for status in (lista_aprovados): #percorrer os valores
            if status == True:
                cont += 1
        taxa_aprovaçao = ((cont/len(lista_aprovados)) * 100)
        melhor_media, pior_media, pior_disciplina, melhor_disciplina = melhor_pior_media(list_medias, lista_disciplinas) #sempre retornar o PARAMETRO da variavel
        with open('RESULTADO.txt', "a") as arquivo:
            arquivo.write('\n')
            arquivo.write(f'\n-----ALUNO: {matricula}------')
            arquivo.write('\n')
            arquivo.write(f'\nESSA É A TAXA DE APROVAÇÃO DO ALUNO {matricula} NAS DISCIPLINAS EM QUE ESTA MATRICULADO: {taxa_aprovaçao:.1f}%')
            arquivo.write(f'\nESSA É A MELHOR MEDIA: {melhor_media:.1f}')
            arquivo.write(f'\nPIOR MEDIA: {pior_media:.1f}')
            arquivo.write(f'\nPIOR DISCIPLINA: {pior_disciplina}')
            arquivo.write(f'\nMELHOR DISCIPLINA: {melhor_disciplina}')

def melhor_pior_media(lista_medias, lista_disciplinas):
    melhor_media_1 = 0
    pior_media_1 = 0
    nome_melhor_materia = ''
    nome_pior_materia = ''

    for i in range(len(lista_medias)): #percorrendo as duas listas, a primeira media e a segunda nome
        if i == 0: #corresponde indice 0 da disciplina
            melhor_media_1 = lista_medias[i]
            pior_media_1 = lista_medias[i]
            nome_melhor_materia = lista_disciplinas[i]
            nome_pior_materia = lista_disciplinas[i]
        else:
            if  lista_medias[i] > melhor_media_1:
                melhor_media_1 = lista_medias[i]
                nome_melhor_materia = lista_disciplinas[i]
            elif lista_medias[i] < pior_media_1:
                pior_media_1 = lista_medias[i]
                nome_pior_materia = lista_disciplinas[i]

    return melhor_media_1, pior_media_1, nome_pior_materia, nome_melhor_materia


with open('RESULTADO.txt',"w") as arquivo:
    arquivo.write('PROCESSAMENTO_DE_NOTAS')

caminho = sys.argv[1]
arquivos = os.listdir(caminho)

for arquivo in arquivos:
    data = ler_dados(arquivo)
    alunos_turma = ler_alunos(data)
media_global(disciplinas) #tirei do for pra nao repetir e sobescrever
matriculado_mais_2_disciplinas()
aprovados_todas_disciplinas()
disciplina_taxa_nome(disciplinas)
estatisticas_aluno(alunos_turma)
