"""
Gerenciador de integração com Google Sheets
Mantém o visual da planilha e gerencia dados em aba oculta
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
from config import (
    GOOGLE_SHEETS_CREDENTIALS,
    SPREADSHEET_ID,
    SHEET_VISUAL,
    SHEET_DATABASE,
    SHEET_RECEITAS,
    CURRENCY_FORMAT
)
from calculator import ParcelCalculator


class SheetsManager:
    """Gerenciador da planilha do Google Sheets"""
    
    def __init__(self):
        self.calc = ParcelCalculator()
        self.client = None
        self.spreadsheet = None
        self.conectar()
    
    def conectar(self):
        """Conecta com o Google Sheets"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Importar configuração de credenciais JSON
            from config import GOOGLE_CREDENTIALS_JSON
            
            # Tentar usar credenciais da variável de ambiente primeiro
            if GOOGLE_CREDENTIALS_JSON:
                import json
                creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
                creds = ServiceAccountCredentials.from_json_keyfile_dict(
                    creds_dict, scope
                )
            else:
                # Fallback para arquivo local
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    GOOGLE_SHEETS_CREDENTIALS, scope
                )
            
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
            print("✅ Conectado ao Google Sheets")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar com Google Sheets: {e}")
            return False
    
    def garantir_abas(self):
        """Garante que as abas necessárias existam"""
        try:
            # Verificar aba visual
            try:
                self.spreadsheet.worksheet(SHEET_VISUAL)
            except:
                self.spreadsheet.add_worksheet(title=SHEET_VISUAL, rows=1000, cols=20)
            
            # Verificar aba de database
            try:
                self.spreadsheet.worksheet(SHEET_DATABASE)
            except:
                ws = self.spreadsheet.add_worksheet(title=SHEET_DATABASE, rows=1000, cols=15)
                # Adicionar cabeçalhos
                ws.update('A1:M1', [[
                    'ID', 'Descrição', 'Valor', 'Parcela Inicial', 'Total Parcelas',
                    'Parcela Atual', 'Mês Início', 'Cartão', 'Status',
                    'Data Cadastro', 'Última Atualização', 'Categoria', 'Observações'
                ]])
            
            # Verificar aba de receitas
            try:
                self.spreadsheet.worksheet(SHEET_RECEITAS)
            except:
                ws = self.spreadsheet.add_worksheet(title=SHEET_RECEITAS, rows=100, cols=10)
                ws.update('A1:E1', [['ID', 'Descrição', 'Valor', 'Data', 'Tipo']])
            
            print("✅ Abas verificadas/criadas")
            return True
        except Exception as e:
            print(f"❌ Erro ao verificar abas: {e}")
            return False
    
    def adicionar_compra(self, descricao, valor_total, valor_parcela, parcela_inicial, total_parcelas, cartao, categoria='Geral'):
        """
        Adiciona nova compra parcelada
        
        Args:
            descricao (str): Descrição da compra
            valor_total (float): Valor total da compra
            valor_parcela (float): Valor de cada parcela mensal
            parcela_inicial (int): Parcela inicial (geralmente 1)
            total_parcelas (int): Total de parcelas
            cartao (str): Nome do cartão
            categoria (str): Categoria da compra
            
        Returns:
            dict: Dados da compra adicionada
        """
        try:
            ws_db = self.spreadsheet.worksheet(SHEET_DATABASE)
            
            # Calcular mês de início baseado na parcela inicial
            mes_inicio = self.calc.calcular_mes_inicio(parcela_inicial, total_parcelas)
            
            # Calcular parcela atual
            parcela_atual, status = self.calc.calcular_parcela_atual(
                mes_inicio, parcela_inicial, total_parcelas
            )
            
            # Gerar ID único
            todas_linhas = ws_db.get_all_values()
            novo_id = len(todas_linhas)  # ID baseado no número de linhas
            
            # Data atual
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Dados da compra
            compra = {
                'id': novo_id,
                'descricao': descricao,
                'valor_total': valor_total,
                'valor_parcela': valor_parcela,
                'parcela_inicial': parcela_inicial,
                'total_parcelas': total_parcelas,
                'parcela_atual': parcela_atual,
                'mes_inicio': mes_inicio,
                'cartao': cartao,
                'status': status,
                'data_cadastro': agora,
                'ultima_atualizacao': agora,
                'categoria': categoria,
                'observacoes': ''
            }
            
            # Adicionar na planilha database (armazenar valor da parcela mensal)
            ws_db.append_row([
                novo_id, descricao, valor_parcela, parcela_inicial, total_parcelas,
                parcela_atual, mes_inicio, cartao, status,
                agora, agora, categoria, ''
            ])
            
            # Atualizar aba visual
            self.atualizar_aba_visual()
            
            print(f"✅ Compra adicionada: {descricao} - {parcela_atual}/{total_parcelas}")
            return compra
            
        except Exception as e:
            print(f"❌ Erro ao adicionar compra: {e}")
            return None
    
    def listar_compras(self, cartao=None, status='ativo'):
        """
        Lista compras filtradas
        
        Args:
            cartao (str): Nome do cartão para filtrar (None = todos)
            status (str): Status para filtrar ('ativo', 'concluido', 'todos')
            
        Returns:
            list: Lista de dicts com dados das compras
        """
        try:
            ws_db = self.spreadsheet.worksheet(SHEET_DATABASE)
            dados = ws_db.get_all_records()
            
            # Filtrar
            resultado = []
            for compra in dados:
                if cartao and compra['Cartão'].lower() != cartao.lower():
                    continue
                if status != 'todos' and compra['Status'] != status:
                    continue
                resultado.append(compra)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro ao listar compras: {e}")
            return []
    
    def atualizar_aba_visual(self):
        """
        Atualiza a aba visual mantendo o layout colorido e organizado
        """
        try:
            ws_visual = self.spreadsheet.worksheet(SHEET_VISUAL)
            ws_db = self.spreadsheet.worksheet(SHEET_DATABASE)
            
            # Buscar dados ativos
            compras = self.listar_compras(status='ativo')
            
            # Agrupar por cartão
            cartoes = {}
            for compra in compras:
                cartao = compra['Cartão']
                if cartao not in cartoes:
                    cartoes[cartao] = []
                cartoes[cartao].append(compra)
            
            # Limpar planilha visual
            ws_visual.clear()
            
            # Construir layout visual
            linha_atual = 1
            
            for cartao, lista_compras in cartoes.items():
                # Cabeçalho do cartão
                ws_visual.update(f'A{linha_atual}', [[f'═══ {cartao.upper()} ═══']])
                linha_atual += 1
                
                # Cabeçalhos de colunas
                ws_visual.update(f'A{linha_atual}:B{linha_atual}', [['Compra', 'Valor']])
                linha_atual += 1
                
                # Compras do cartão
                total_cartao = 0
                for compra in lista_compras:
                    descricao_com_parcela = f"{compra['Descrição']} {compra['Parcela Atual']}/{compra['Total Parcelas']}"
                    valor_formatado = CURRENCY_FORMAT.format(compra['Valor'])
                    
                    ws_visual.update(f'A{linha_atual}:B{linha_atual}', [
                        [descricao_com_parcela, valor_formatado]
                    ])
                    
                    total_cartao += compra['Valor']
                    linha_atual += 1
                
                # Total do cartão
                ws_visual.update(f'A{linha_atual}:B{linha_atual}', [
                    ['TOTAL', CURRENCY_FORMAT.format(total_cartao)]
                ])
                linha_atual += 2  # Espaço entre cartões
            
            print("✅ Aba visual atualizada")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar aba visual: {e}")
            return False
    
    def adicionar_receita(self, descricao, valor, tipo='Salário'):
        """Adiciona uma receita"""
        try:
            ws_receitas = self.spreadsheet.worksheet(SHEET_RECEITAS)
            
            todas_linhas = ws_receitas.get_all_values()
            novo_id = len(todas_linhas)
            agora = datetime.now().strftime('%Y-%m-%d')
            
            ws_receitas.append_row([novo_id, descricao, valor, agora, tipo])
            
            print(f"✅ Receita adicionada: {descricao} - {CURRENCY_FORMAT.format(valor)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar receita: {e}")
            return False
    
    def calcular_resumo(self):
        """
        Calcula resumo financeiro do mês atual
        
        Returns:
            dict: Resumo com receitas, despesas e saldo
        """
        try:
            # Buscar receitas
            ws_receitas = self.spreadsheet.worksheet(SHEET_RECEITAS)
            receitas_data = ws_receitas.get_all_records()
            total_receitas = sum(r['Valor'] for r in receitas_data)
            
            # Buscar despesas ativas
            compras = self.listar_compras(status='ativo')
            total_despesas = sum(c['Valor'] for c in compras)
            
            # Agrupar despesas por cartão
            por_cartao = {}
            for compra in compras:
                cartao = compra['Cartão']
                if cartao not in por_cartao:
                    por_cartao[cartao] = 0
                por_cartao[cartao] += compra['Valor']
            
            return {
                'receitas': total_receitas,
                'despesas': total_despesas,
                'saldo': total_receitas - total_despesas,
                'por_cartao': por_cartao,
                'total_compras': len(compras)
            }
            
        except Exception as e:
            print(f"❌ Erro ao calcular resumo: {e}")
            return None
    
    def atualizar_mes(self):
        """
        Atualiza todas as parcelas para o mês atual
        Deve ser executado automaticamente todo dia 1
        """
        try:
            ws_db = self.spreadsheet.worksheet(SHEET_DATABASE)
            compras = self.listar_compras(status='todos')
            
            atualizadas = 0
            finalizadas = 0
            
            for i, compra in enumerate(compras, start=2):  # Começa na linha 2 (pula cabeçalho)
                parcela_atual, status = self.calc.calcular_parcela_atual(
                    compra['Mês Início'],
                    compra['Parcela Inicial'],
                    compra['Total Parcelas']
                )
                
                # Atualizar na planilha
                ws_db.update(f'F{i}', [[parcela_atual]])  # Coluna F = Parcela Atual
                ws_db.update(f'I{i}', [[status]])  # Coluna I = Status
                ws_db.update(f'K{i}', [[datetime.now().strftime('%Y-%m-%d %H:%M:%S')]])  # Coluna K = Última Atualização
                
                if status == 'concluido':
                    finalizadas += 1
                else:
                    atualizadas += 1
            
            # Atualizar aba visual
            self.atualizar_aba_visual()
            
            resultado = {
                'atualizadas': atualizadas,
                'finalizadas': finalizadas,
                'data_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ Mês atualizado: {atualizadas} ativas, {finalizadas} finalizadas")
            return resultado
            
        except Exception as e:
            print(f"❌ Erro ao atualizar mês: {e}")
            return None
    
    def importar_dados(self, dados_lista):
        """
        Importa múltiplas compras de uma vez
        
        Args:
            dados_lista (list): Lista de dicts com dados das compras
                Formato: {'descricao', 'valor', 'parcela_atual', 'total_parcelas', 'cartao'}
        
        Returns:
            dict: Resultado da importação
        """
        try:
            sucesso = 0
            erros = 0
            
            for dados in dados_lista:
                try:
                    # Calcular mês de início baseado na parcela atual
                    mes_inicio = self.calc.calcular_mes_inicio(
                        dados['parcela_atual'],
                        dados['total_parcelas']
                    )
                    
                    # Calcular valor total e valor da parcela
                    # Se o usuário informou valor da parcela, calcular o total
                    valor_informado = dados['valor']
                    total_parcelas = dados['total_parcelas']
                    
                    # Assumir que o valor informado é o total da compra
                    valor_total = valor_informado
                    valor_parcela = valor_total / total_parcelas
                    
                    # Adicionar compra
                    resultado = self.adicionar_compra(
                        descricao=dados['descricao'],
                        valor_total=valor_total,
                        valor_parcela=valor_parcela,
                        parcela_inicial=dados['parcela_atual'],
                        total_parcelas=total_parcelas,
                        cartao=dados['cartao'],
                        categoria=dados.get('categoria', 'Geral')
                    )
                    
                    if resultado:
                        sucesso += 1
                    else:
                        erros += 1
                        
                except Exception as e:
                    print(f"❌ Erro ao importar {dados.get('descricao', 'item')}: {e}")
                    erros += 1
            
            return {
                'sucesso': sucesso,
                'erros': erros,
                'total': len(dados_lista)
            }
            
        except Exception as e:
            print(f"❌ Erro na importação: {e}")
            return None
