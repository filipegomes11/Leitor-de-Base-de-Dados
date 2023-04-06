import pandas as pd
import numpy as np
# Módulo para referenciar tipagens
from typing import List, Any, Tuple
import os

if (os.system("pip install multipledispatch") == 0):
    print("------------------------------------------------")
    print("   multipledispatch instalado com sucesso!")
    print("------------------------------------------------")
else:
    print("------------------------------------------------\n")
    print("Não foi possível instalar o multipledispatch.")
    print("\n------------------------------------------------")

# Módulo externo para criar sobrecargas de funções
from multipledispatch import dispatch

class ExtratorDeProbabilidades:
    # Letra a
    def __init__(self, path: str) -> None:
        # Seta o path como um atributo da classe; não será usado1

        self.path = path
        try:
            # Cria o dataframe a partir do path passado
            self.df = pd.read_csv(path, sep=',', encoding="iso-8859-1")

        except:
            self.df = pd.DataFrame({})
            print("------------------------------------------------")
            print("    Ocorreu um erro ao carregar o arquivo.")
            print("------------------------------------------------")
            os.system("pause")
            os.system("cls")
            
    
    # Letra b
    def carregar_colunas(self, lista_colunas: List[str], quantidade: int) -> pd.DataFrame:
        try:
            # Tenta carregar as colunas baseado no limite que o usuário desejar;
            return self.df[lista_colunas][:quantidade]
        except:
            print("------------------------------------------------")
            print("    Ocoreu um erro ao carregar as colunas")
            print("------------------------------------------------")
            os.system("pause")
            os.system("cls")
    # Letra c
    def descarregar_colunas(self) -> None:
        self.df = pd.DataFrame({})
    
    # Letra d
    def probabilidade_apriori(self, caracteristica: str, valor: Any) -> float or None:
        try:
            # Filtra o dataframe pela coluna desejada da tabela e calcula o tamanho
            num_espec = len(self.df[self.df[caracteristica] == valor])
            # Retorna o tamanho do tabela filtrada dividido pela tabela total
            return num_espec/len(self.df)
        except:
            print("------------------------------------------------")
            print("  Ocorreu um erro ao calcular a porcentagem.")
            print("------------------------------------------------")
            os.system("cls")

    # Letra e
    @dispatch(str, tuple) # Decorator usado para utilizar a sobrecarga; como definido na questão, a função deve possuir mesmo nome
    def probabilidade_apriori_intervalo(self, caracteristica: str, intervalo: Tuple[int, int]) -> float or None:
        try:

            inicio, fim = intervalo
            num_espec = len(self.df[caracteristica][inicio:fim])
            return num_espec / len(self.df[caracteristica])

        except:
            print("------------------------------------------------")
            print("  Ocorreu um erro ao calcular a porcentagem.")
            print("------------------------------------------------")
            os.system("pause")
            os.system("cls")
    
    # Letra f
    def probabilidade_condicional(self, cond_a: Tuple[str, str], cond_b: Tuple[str, str]) -> float or None:
        try:
            # Recebe duas colunas e valores a serem filtrados
            carac_a, val_a = cond_a
            carac_b, val_b = cond_b
            # Cria duas condições que serão utilizadas para gerar o filtro no dataframe
            filter_a = self.df[carac_a] == val_a
            filter_b = self.df[carac_b] == val_b
            # Retorna o tamanho das duas condições a e b aplicadas no dataframe dividido pelo tamanho do dataframe aplicado à condição b
            return len(self.df[filter_a & filter_b])/len(self.df[filter_b])
        except:
            print("------------------------------------------------")
            print("  Ocorreu um erro ao calcular a porcentagem.")
            print("------------------------------------------------")
            os.system("pause")
            os.system("cls")
    
    # Letra g
    @dispatch(tuple, tuple)
    def probabilidade_apriori_intervalo(self, a: Tuple[str, str], b: Tuple[str, Tuple[int, int]]):
        try:
            carac, valor = a
            _, (inicio, fim) = b
            
            try:
                qtd_filtro = (self.df[carac][inicio:fim] == valor).value_counts()[True]
            except KeyError:
                qtd_filtro = 0

            qtd_total = len(self.df[carac] == valor)
            return qtd_filtro/qtd_total

        except ZeroDivisionError:
            return 0

    # Desafios
    def desafio_a(self, a: Tuple[str, str], b: Tuple[str, str], column=str, percentage: float = 0.9):
        try:
            carac_a, valor_a = a
            carac_b, valor_b = b
            modelos = self.df[(self.df[carac_a] == valor_a) & (self.df[carac_b] < valor_b)][column].value_counts(normalize=True) > percentage
            # Cria um conjunto que irá guardar o valor dos carros
            carros = set()
            # Itera sobre os valores verdade da tabela criada pelo filtro, junto aos índices, que nesse caso
            for modelo, valor in zip(modelos.index, modelos):
                # Caso o valor seja true, adiciona o modelo do carro no conjunto
                if valor == True: carros.add(modelo)
            # Retorna o conjunto de carros caso exista pelo menos um, caso contrário retorna "{}"
            return carros if carros else "{}"
        except:
            print("Ocorreu um erro ao resolver o desafio.")

    def desafio_b(self, a: Tuple[str, str], b: Tuple[str, str], pct: float):
        try:
            # Gera um dataframe com os filtros passados
            carac_a, valor_a = a
            carac_b, valor_b = b
            valores = self.df[(self.df[carac_a] == valor_a) & (self.df[carac_b] == valor_b)]
            # Caso o índice seja maior que 2, iremos receber o primeiro e último índice
            if len(valores.index) >= 2:
                # Retorna o primeiro e o último índice, representando os limites
                val = len(valores.index)
                for i in range(val):
                    if (i/val) > pct: break
                return (valores.index[0], valores.index[i])
            # Caso haja apenas um valor, não faz sentido querer enviar um range, pois qualquer range contendo o valor
            # satisfaz a condição; nesse caso enviamos apenas o índice do valor que satisfaz a condição
            elif len(valores.index) == 1:
                return {valores.index[0]}
            else:
                # Caso não exista, retorna None
                return None
        except:
            print("Ocorreu um erro ao resolver o desafio.")

    def menu(self):
        print(" __________________________________________________") 
        print("|1 - Carregar Arquivo                              |")
        print("|2 - Mostrar DataFrame                             |")
        print("|3 - Carregar Colunas                              |")
        print("|4 - Probabilidade à Priori                        |")
        print("|5 - Probabilidade à Priori - Intervalo            |")
        print("|6 - Probabilidade Condicional                     |")
        print("|7 - Probabilidade à Priori - Intervalo (Tipo 2)   |")
        print("|8 - Desafio                                       |")
        print("|9 - Descarregar Arquivo                           |")
        print("|10- Créditos                                      |")
        print("|0 - Sair                                          |")
        print("|__________________________________________________|") 
        print()
        

        opt = int(input("Insira o número relativo à operação desejada: "))
        if (opt == 1):
         
            filename = input("\nInsira o filename: ")
            self.__init__(filename)
            print("<<<------------------------------------------>>>")
            print("     BASE DE DADOS CARREGADA COM SUCESSO!")
            print("<<<------------------------------------------>>>")
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 2):
            os.system("cls")
            print(self.df)
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 3):
            print("------------------------------------------------")
            colunas = input("Insira o nome das colunas que deseja verificar, separadas por espaço: ").split()
            lim = int(input("Insira a quantidade de elementos desejada: "))
            print(self.carregar_colunas(colunas, lim))
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 4):
            print("------------------------------------------------")
            carac = input("Insira a coluna: ")
            val = input("Insira o valor")
            print(self.probabilidade_apriori(carac, val))
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 5):
            print("------------------------------------------------")
            carac = input("Insira a coluna desejada: ")
            inf = input("Insira o limite inferior: ")
            sup = input("Insira o limite superior: ")
            print(self.probabilidade_apriori_intervalo(carac, (inf, sup)))
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 6):
            print("------------------------------------------------")
            cond_a, valor_a = input("Insira a coluna e o valor seguidos por espaço: ").split()
            cond_b, valor_b = input("Insira a segunda coluna e o valor seguidos por espaço: ").split()
            print(self.probabilidade_condicional((cond_a, valor_a), (cond_b, valor_b)))
            os.system("pause")
            os.system("cls")
            return True

        elif (opt == 7):
            print("------------------------------------------------")
            os.system("cls")
            cond, valor = input("Insira a coluna e o valor seguidos por espaço: ").split()
            inf = input("Insira o limite inferior: ")
            sup = input("Insira o limite superior: ")
            print(self.probabilidade_apriori_intervalo((cond, valor), (cond, (inf, sup))))
            os.system("pause")
            os.system("cls")
            return True
            
            print(self.desafio_a((cond_a, valor_a), (cond_b, valor_b), col, pct))

        elif (opt == 8):
            print("------------------------------------------------")
            cond_a, valor_a = input("Insira a coluna e o valor seguidos por espaço: ").split()
            cond_b, valor_b = input("Insira a segunda coluna e o valor seguidos por espaço: ").split()
            pct = float(input("Insira a porcentagem entre 0 e 1: "))
            print(self.desafio_b((cond_a, valor_a), (cond_b, valor_b), pct))
            os.system("pause")
            os.system("cls")        
        
        elif (opt == 9):
            os.system("cls")        
            self.descarregar_colunas()
            print("------------------------------------------------")
            print("     Dataframe limpo com sucesso!")
            print("------------------------------------------------")    
            os.system("pause")
            os.system("cls")
            return True
        
        elif (opt == 10):
            os.system("cls")
            print("  ______________________________________________ ")
            print(" |                                              |")
            print(" |     2º Projeto de IP - PYTHON                |")
            print(" | Prof. Dr. Luis Filipe Alves Pereira          |")
            print(" |----------------------------------------------|")
            print(" |                                              |")
            print(" |  Aluno1: Claudierio Baltazar Barra Nova      |")
            print(" |  Aluno2: Filipe Alencar Andrade Amorim Gomes |")
            print(" |______________________________________________|\n")
            os.system("pause")
            os.system("cls")

        elif (opt == 0):
            print("\n------------------------------------------------")
            print("     O programa foi encerrado com sucesso.")
            print("------------------------------------------------\n")
            os.system("pause")
            os.system("cls")            
            return

"""### Testes com o csv vehicles-light"""

t = ExtratorDeProbabilidades('vehicles-light.csv')
t.probabilidade_apriori(caracteristica='region', valor='birmingham')

t.probabilidade_apriori_intervalo('region', (1, 10))

t.probabilidade_condicional(cond_a=('region', 'birmingham'), cond_b=('transmission', 'other'))

t.probabilidade_apriori_intervalo(("transmission", "manual"), ("transmission", (29, 150)))

"""### Main Loop"""

while t.menu() != None:
    continue