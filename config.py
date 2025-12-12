"""
Configurações do bot de controle de gastos
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Configurações do Google Sheets
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# Configurações gerais
TIMEZONE = os.getenv('TIMEZONE', 'America/Sao_Paulo')
AUTO_UPDATE_DAY = int(os.getenv('AUTO_UPDATE_DAY', 1))

# Nomes das abas da planilha
SHEET_VISUAL = 'Gastos'  # Aba visual que o usuário vê
SHEET_DATABASE = 'Database'  # Aba oculta com dados do bot
SHEET_RECEITAS = 'Receitas'  # Aba de receitas

# Formato de moeda
CURRENCY_FORMAT = 'R$ {:.2f}'

# Comandos do bot
COMMANDS = {
    'start': 'Inicia o bot e mostra as opções',
    'adicionar': 'Adiciona uma nova compra parcelada',
    'importar': 'Importa dados existentes',
    'listar': 'Lista gastos do mês atual',
    'resumo': 'Mostra resumo financeiro do mês',
    'receita': 'Adiciona uma receita',
    'atualizarmes': 'Atualiza parcelas para o próximo mês',
    'editar': 'Edita uma compra existente',
    'remover': 'Remove uma compra',
    'cartoes': 'Lista todos os cartões',
    'proximo': 'Mostra gastos do próximo mês',
    'help': 'Mostra todos os comandos disponíveis'
}
