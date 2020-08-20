from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import re

def extracao_booleana(PATH_EXCEL_D, PATH_EXCEL_R):
    dic_regex = {}
    df_regex = pd.read_excel(PATH_EXCEL_R)
    df_dados = pd.read_excel(PATH_EXCEL_D)
    for _, row in df_regex.iterrows():
        dic_regex[row['var']] = r'{}'.format(row['regex'])
    rows_result = []
    for _, row in df_dados.iterrows():
        dic_aux = {k:0 for k in dic_regex}
        for v,reg in dic_regex.items():
            if re.search(reg,row['texto_publicacao'],re.I):
                dic_aux[v] = 1
        rows_result.append(dic_aux)
    df_res = pd.DataFrame(rows_result)
    df_res.to_excel('resultado_extração.xlsx',index=False)

def graficos_pizza(PATH_EXCEL_RES):
    df = pd.read_excel(PATH_EXCEL_RES)
    colunas_desconsiderar = ['numero_processo']
    for c in df.columns:
        if c not in colunas_desconsiderar:
            dic_valores = Counter(df[c].tolist())
            labels = list(dic_valores.keys())
            values = list(dic_valores.values())
            plt.pie(values,labels=labels,explode=[0.1 for i in range(len(values))])
            plt.savefig('variavel_{}.png'.format(c))
            plt.clf()

def relatorio_geral(PATH_EXCEL_RES):
    df = pd.read_excel(PATH_EXCEL_RES)
    colunas_desconsiderar = ['numero_processo']
    dic_var_listas = {}
    arq_relatorio = open('relatório_geral.txt','w')
    for c in df.columns:
        if c not in colunas_desconsiderar:
            dic = Counter(df[c].tolist())
            dic_var_listas[c] = dic
            arq_relatorio.write('\n\nRelatório sobre variável: {}\n'.format(c))
            for i in [0,1]:
                if i in dic:
                    arq_relatorio.write('Número de {}: {}\n'.format(i,dic[i]))
    arq_relatorio.close()

if __name__ == "__main__":
    # Arquivo excel com duas colunas: "var" (com o nome das variáveis a serem extraídas) e "regex" (com a expressão regular)
    PATH_EXCEL_REGEX = 'regex_pesquisas.xlsx'
    # Arquivo excel contendo duas colunas: "texto_publicacao" (com os textos a serem analisados) e "numero_processo" (com um identificador para os textos)
    PATH_EXCEL_DADOS = 'fonte_dados.xlsx'
    # Arquivo gerado de relatório
    PATH_RELATORIO = 'resultado_extração.xlsx'

    # Chamada da função de extração booleana
    extracao_booleana(PATH_EXCEL_DADOS, PATH_EXCEL_REGEX)
    # Gráficos de pizza para cada variável
    graficos_pizza(PATH_RELATORIO)
    # Relatório sobre as variáveis encontradas
    relatorio_geral(PATH_RELATORIO)