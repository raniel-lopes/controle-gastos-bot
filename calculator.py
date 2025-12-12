"""
Módulo de cálculo automático de parcelas
Calcula automaticamente qual parcela está no mês atual baseado na data de início
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from config import TIMEZONE


class ParcelCalculator:
    """Classe para calcular parcelas automaticamente"""
    
    def __init__(self, timezone=TIMEZONE):
        self.tz = pytz.timezone(timezone)
    
    def calcular_parcela_atual(self, mes_inicio, parcela_inicial, total_parcelas):
        """
        Calcula qual parcela está no mês atual
        
        Args:
            mes_inicio (str): Data de início no formato 'YYYY-MM'
            parcela_inicial (int): Número da parcela inicial (quando começou)
            total_parcelas (int): Total de parcelas
            
        Returns:
            tuple: (parcela_atual, status)
                   status pode ser: 'ativo', 'concluido', 'futuro'
        """
        try:
            # Data atual
            hoje = datetime.now(self.tz)
            mes_atual = hoje.strftime('%Y-%m')
            
            # Converter mes_inicio para datetime
            data_inicio = datetime.strptime(mes_inicio, '%Y-%m')
            
            # Calcular diferença em meses
            meses_decorridos = (hoje.year - data_inicio.year) * 12 + (hoje.month - data_inicio.month)
            
            # Calcular parcela atual
            parcela_atual = parcela_inicial + meses_decorridos
            
            # Determinar status
            if parcela_atual > total_parcelas:
                return total_parcelas, 'concluido'
            elif parcela_atual < parcela_inicial:
                return parcela_inicial, 'futuro'
            else:
                return parcela_atual, 'ativo'
                
        except Exception as e:
            print(f"Erro ao calcular parcela: {e}")
            return parcela_inicial, 'erro'
    
    def calcular_mes_inicio(self, parcela_atual, total_parcelas):
        """
        Calcula o mês de início baseado na parcela atual
        Útil para importação de dados existentes
        
        Args:
            parcela_atual (int): Parcela atual (ex: 12)
            total_parcelas (int): Total de parcelas (ex: 14)
            
        Returns:
            str: Mês de início no formato 'YYYY-MM'
        """
        try:
            hoje = datetime.now(self.tz)
            
            # Calcular quantos meses atrás começou
            meses_atras = parcela_atual - 1
            
            # Calcular data de início
            data_inicio = hoje - relativedelta(months=meses_atras)
            
            return data_inicio.strftime('%Y-%m')
            
        except Exception as e:
            print(f"Erro ao calcular mês de início: {e}")
            return datetime.now(self.tz).strftime('%Y-%m')
    
    def proximas_parcelas(self, mes_inicio, parcela_atual, total_parcelas, meses=3):
        """
        Retorna lista das próximas parcelas
        
        Args:
            mes_inicio (str): Data de início no formato 'YYYY-MM'
            parcela_atual (int): Parcela atual
            total_parcelas (int): Total de parcelas
            meses (int): Quantidade de meses para projetar
            
        Returns:
            list: Lista de dicts com {mes, parcela, status}
        """
        try:
            resultado = []
            data_inicio = datetime.strptime(mes_inicio, '%Y-%m')
            hoje = datetime.now(self.tz)
            
            for i in range(meses):
                data_projecao = hoje + relativedelta(months=i)
                meses_decorridos = (data_projecao.year - data_inicio.year) * 12 + (data_projecao.month - data_inicio.month)
                parcela = parcela_atual + meses_decorridos - ((hoje.year - data_inicio.year) * 12 + (hoje.month - data_inicio.month))
                
                if parcela <= total_parcelas:
                    resultado.append({
                        'mes': data_projecao.strftime('%Y-%m'),
                        'mes_nome': data_projecao.strftime('%B/%Y'),
                        'parcela': parcela,
                        'status': 'ativo' if parcela <= total_parcelas else 'concluido'
                    })
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao calcular próximas parcelas: {e}")
            return []
    
    def formatar_parcela(self, parcela_atual, total_parcelas):
        """
        Formata parcela no padrão visual: 12/14
        
        Args:
            parcela_atual (int): Parcela atual
            total_parcelas (int): Total de parcelas
            
        Returns:
            str: Parcela formatada (ex: "12/14")
        """
        return f"{parcela_atual}/{total_parcelas}"
    
    def atualizar_mes(self, compras_list):
        """
        Atualiza todas as parcelas para o novo mês
        
        Args:
            compras_list (list): Lista de dicts com dados das compras
            
        Returns:
            list: Lista atualizada com novos valores de parcelas
        """
        atualizadas = []
        finalizadas = []
        
        for compra in compras_list:
            parcela_atual, status = self.calcular_parcela_atual(
                compra['mes_inicio'],
                compra['parcela_inicial'],
                compra['total_parcelas']
            )
            
            compra['parcela_atual'] = parcela_atual
            compra['status'] = status
            
            if status == 'concluido':
                finalizadas.append(compra)
            else:
                atualizadas.append(compra)
        
        return {
            'atualizadas': atualizadas,
            'finalizadas': finalizadas,
            'total_atualizadas': len(atualizadas),
            'total_finalizadas': len(finalizadas)
        }


# Funções auxiliares para uso direto
def calcular_parcela_atual(mes_inicio, parcela_inicial, total_parcelas):
    """Função auxiliar para calcular parcela atual"""
    calc = ParcelCalculator()
    return calc.calcular_parcela_atual(mes_inicio, parcela_inicial, total_parcelas)


def calcular_mes_inicio(parcela_atual, total_parcelas):
    """Função auxiliar para calcular mês de início"""
    calc = ParcelCalculator()
    return calc.calcular_mes_inicio(parcela_atual, total_parcelas)


def formatar_parcela(parcela_atual, total_parcelas):
    """Função auxiliar para formatar parcela"""
    calc = ParcelCalculator()
    return calc.formatar_parcela(parcela_atual, total_parcelas)
