"""
Bot do Telegram para Controle Automático de Gastos Parcelados
"""
import logging
import schedule
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from config import TELEGRAM_BOT_TOKEN, COMMANDS, CURRENCY_FORMAT, AUTO_UPDATE_DAY
from sheets_manager import SheetsManager
from calculator import ParcelCalculator

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados da conversa
(ADICIONAR_DESCRICAO, ADICIONAR_VALOR, ADICIONAR_PARCELA_INICIAL,
 ADICIONAR_TOTAL_PARCELAS, ADICIONAR_CARTAO,
 IMPORTAR_DADOS, RECEITA_DESCRICAO, RECEITA_VALOR) = range(8)

# Inicializar gerenciadores
sheets = SheetsManager()
calc = ParcelCalculator()


# ============ COMANDOS PRINCIPAIS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Apresentação do bot"""
    mensagem = """
🤖 *Bem-vindo ao Controle de Gastos Bot!*

Eu vou gerenciar seus gastos parcelados automaticamente! 
Nunca mais atualize parcelas manualmente! 

🎯 *Principais comandos:*

📝 `/adicionar` - Nova compra parcelada
📊 `/resumo` - Resumo financeiro do mês
📋 `/listar` - Ver gastos atuais
💰 `/receita` - Adicionar receita
🔄 `/atualizarmes` - Atualizar parcelas
📥 `/importar` - Importar dados existentes

💡 Use `/help` para ver todos os comandos

Vamos começar? Digite `/adicionar` para sua primeira compra! 🚀
    """
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Lista todos os comandos"""
    mensagem = "📚 *Comandos Disponíveis:*\n\n"
    for cmd, desc in COMMANDS.items():
        mensagem += f"/{cmd} - {desc}\n"
    
    mensagem += "\n💡 *Dica:* Use `/adicionar` para começar a controlar seus gastos!"
    await update.message.reply_text(mensagem, parse_mode='Markdown')


# ============ ADICIONAR COMPRA ============

async def adicionar_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia o processo de adicionar compra"""
    await update.message.reply_text(
        "📝 *Nova Compra Parcelada*\n\n"
        "Qual a descrição da compra?\n"
        "_Exemplo: Microfone Igreja, Fone Bluetooth, etc._",
        parse_mode='Markdown'
    )
    return ADICIONAR_DESCRICAO


async def adicionar_descricao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe a descrição"""
    context.user_data['descricao'] = update.message.text
    await update.message.reply_text(
        f"✅ Descrição: *{update.message.text}*\n\n"
        "💵 Qual o *valor TOTAL* da compra?\n"
        "_Exemplo: Se o produto custa 619.00 parcelado, digite 619.00_\n"
        "_O valor da parcela será calculado automaticamente_",
        parse_mode='Markdown'
    )
    return ADICIONAR_VALOR


async def adicionar_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o valor"""
    try:
        valor_total = float(update.message.text.replace(',', '.'))
        context.user_data['valor_total'] = valor_total
        
        await update.message.reply_text(
            f"✅ Valor Total: *{CURRENCY_FORMAT.format(valor_total)}*\n\n"
            "🔢 Qual a parcela atual?\n"
            "_Se é uma compra nova, digite 1_\n"
            "_Se já está na parcela 5, digite 5_",
            parse_mode='Markdown'
        )
        return ADICIONAR_PARCELA_INICIAL
        
    except ValueError:
        await update.message.reply_text(
            "❌ Valor inválido! Digite apenas números.\n"
            "_Exemplo: 619.00_",
            parse_mode='Markdown'
        )
        return ADICIONAR_VALOR


async def adicionar_parcela_inicial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe a parcela inicial"""
    try:
        parcela_inicial = int(update.message.text)
        context.user_data['parcela_inicial'] = parcela_inicial
        
        await update.message.reply_text(
            f"✅ Parcela atual: *{parcela_inicial}*\n\n"
            "🎯 Qual o total de parcelas?\n"
            "_Exemplo: 12, 14, 10, etc._",
            parse_mode='Markdown'
        )
        return ADICIONAR_TOTAL_PARCELAS
        
    except ValueError:
        await update.message.reply_text(
            "❌ Número inválido! Digite apenas o número da parcela.",
            parse_mode='Markdown'
        )
        return ADICIONAR_PARCELA_INICIAL


async def adicionar_total_parcelas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o total de parcelas"""
    try:
        total_parcelas = int(update.message.text)
        context.user_data['total_parcelas'] = total_parcelas
        
        await update.message.reply_text(
            f"✅ Total: *{total_parcelas}x*\n\n"
            "💳 Qual o cartão?\n"
            "_Exemplo: Nubank, Itaú, Inter, Rico, etc._",
            parse_mode='Markdown'
        )
        return ADICIONAR_CARTAO
        
    except ValueError:
        await update.message.reply_text(
            "❌ Número inválido! Digite apenas o total de parcelas.",
            parse_mode='Markdown'
        )
        return ADICIONAR_TOTAL_PARCELAS


async def adicionar_cartao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o cartão e finaliza"""
    cartao = update.message.text
    
    # Recuperar dados
    descricao = context.user_data['descricao']
    valor_total = context.user_data['valor_total']
    parcela_inicial = context.user_data['parcela_inicial']
    total_parcelas = context.user_data['total_parcelas']
    
    # Calcular valor da parcela mensal
    valor_parcela = valor_total / total_parcelas
    
    # Adicionar na planilha
    resultado = sheets.adicionar_compra(
        descricao=descricao,
        valor_total=valor_total,
        valor_parcela=valor_parcela,
        parcela_inicial=parcela_inicial,
        total_parcelas=total_parcelas,
        cartao=cartao
    )
    
    if resultado:
        parcela_formatada = calc.formatar_parcela(
            resultado['parcela_atual'],
            resultado['total_parcelas']
        )
        
        mensagem = f"""
✅ *Compra adicionada com sucesso!*

📝 {descricao}
� Valor Total: {CURRENCY_FORMAT.format(valor_total)}
💵 Valor/mês: {CURRENCY_FORMAT.format(valor_parcela)}
📊 Parcela: {parcela_formatada}
💳 Cartão: {cartao}

A parcela será atualizada automaticamente todo mês! 🎉

Use `/resumo` para ver o total do mês.
        """
        await update.message.reply_text(mensagem, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Erro ao adicionar compra. Tente novamente.",
            parse_mode='Markdown'
        )
    
    # Limpar dados temporários
    context.user_data.clear()
    return ConversationHandler.END


# ============ LISTAR E RESUMO ============

async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista gastos do mês atual"""
    # Verificar se tem filtro de cartão
    cartao = None
    if context.args and len(context.args) > 0:
        cartao = ' '.join(context.args)
    
    compras = sheets.listar_compras(cartao=cartao, status='ativo')
    
    if not compras:
        await update.message.reply_text(
            "📭 Nenhum gasto encontrado para este mês.",
            parse_mode='Markdown'
        )
        return
    
    # Agrupar por cartão
    por_cartao = {}
    for compra in compras:
        c = compra['Cartão']
        if c not in por_cartao:
            por_cartao[c] = []
        por_cartao[c].append(compra)
    
    # Montar mensagem
    mensagem = "📊 *Gastos do Mês Atual*\n\n"
    
    for cartao_nome, lista in por_cartao.items():
        mensagem += f"💳 *{cartao_nome}*\n"
        total_cartao = 0
        
        for c in lista:
            parcela_fmt = calc.formatar_parcela(c['Parcela Atual'], c['Total Parcelas'])
            mensagem += f"  • {c['Descrição']} {parcela_fmt} - {CURRENCY_FORMAT.format(c['Valor'])}\n"
            total_cartao += c['Valor']
        
        mensagem += f"  *Subtotal:* {CURRENCY_FORMAT.format(total_cartao)}\n\n"
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra resumo financeiro completo"""
    resultado = sheets.calcular_resumo()
    
    if not resultado:
        await update.message.reply_text(
            "❌ Erro ao calcular resumo.",
            parse_mode='Markdown'
        )
        return
    
    mensagem = f"""
📊 *Resumo Financeiro - {datetime.now().strftime('%B/%Y')}*

💰 *Receitas:* {CURRENCY_FORMAT.format(resultado['receitas'])}
💳 *Despesas:* {CURRENCY_FORMAT.format(resultado['despesas'])}
━━━━━━━━━━━━━━━━
{'✅' if resultado['saldo'] >= 0 else '⚠️'} *Saldo:* {CURRENCY_FORMAT.format(resultado['saldo'])}

📋 *Despesas por Cartão:*
    """
    
    for cartao, valor in resultado['por_cartao'].items():
        mensagem += f"\n💳 {cartao}: {CURRENCY_FORMAT.format(valor)}"
    
    mensagem += f"\n\n📦 Total de {resultado['total_compras']} compras ativas"
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')


# ============ RECEITAS ============

async def receita_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia adicionar receita"""
    await update.message.reply_text(
        "💰 *Nova Receita*\n\n"
        "Qual a descrição?\n"
        "_Exemplo: Salário, Freelance, Rendimentos, etc._",
        parse_mode='Markdown'
    )
    return RECEITA_DESCRICAO


async def receita_descricao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe descrição da receita"""
    context.user_data['receita_descricao'] = update.message.text
    await update.message.reply_text(
        f"✅ Descrição: *{update.message.text}*\n\n"
        "💵 Qual o valor?\n"
        "_Exemplo: 4300.00_",
        parse_mode='Markdown'
    )
    return RECEITA_VALOR


async def receita_valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe valor e finaliza"""
    try:
        valor = float(update.message.text.replace(',', '.'))
        descricao = context.user_data['receita_descricao']
        
        resultado = sheets.adicionar_receita(descricao, valor)
        
        if resultado:
            await update.message.reply_text(
                f"✅ *Receita adicionada!*\n\n"
                f"💰 {descricao}: {CURRENCY_FORMAT.format(valor)}\n\n"
                f"Use `/resumo` para ver o saldo atualizado.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "❌ Erro ao adicionar receita.",
                parse_mode='Markdown'
            )
        
        context.user_data.clear()
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "❌ Valor inválido! Digite apenas números.",
            parse_mode='Markdown'
        )
        return RECEITA_VALOR


# ============ IMPORTAR DADOS ============

async def importar_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia importação de dados"""
    mensagem = """
📥 *Importar Dados Existentes*

Envie seus gastos no formato:
`DESCRIÇÃO | VALOR | PARCELA_ATUAL/TOTAL | CARTÃO`

*Exemplos:*
```
Microfone Igreja | 161.90 | 7/10 | Nubank
Smiles | 32.20 | 1/1 | Nubank
Dentista mãe | 100.00 | 6/10 | Inter
```

Pode enviar múltiplas linhas de uma vez!
Digite /cancelar para sair.
    """
    await update.message.reply_text(mensagem, parse_mode='Markdown')
    return IMPORTAR_DADOS


async def importar_dados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa dados importados"""
    try:
        linhas = update.message.text.strip().split('\n')
        dados_lista = []
        
        for linha in linhas:
            partes = [p.strip() for p in linha.split('|')]
            if len(partes) != 4:
                continue
            
            descricao = partes[0]
            valor_parcela = float(partes[1].replace(',', '.'))
            parcelas = partes[2].split('/')
            parcela_atual = int(parcelas[0])
            total_parcelas = int(parcelas[1])
            cartao = partes[3]
            
            dados_lista.append({
                'descricao': descricao,
                'valor_parcela': valor_parcela,
                'parcela_atual': parcela_atual,
                'total_parcelas': total_parcelas,
                'cartao': cartao
            })
        
        if not dados_lista:
            await update.message.reply_text(
                "❌ Nenhum dado válido encontrado. Verifique o formato.",
                parse_mode='Markdown'
            )
            return IMPORTAR_DADOS
        
        # Importar
        resultado = sheets.importar_dados(dados_lista)
        
        if resultado:
            mensagem = f"""
✅ *Importação Concluída!*

📊 Sucesso: {resultado['sucesso']}
❌ Erros: {resultado['erros']}
📦 Total: {resultado['total']}

Use `/listar` para ver os dados importados!
            """
            await update.message.reply_text(mensagem, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Erro na importação.",
                parse_mode='Markdown'
            )
        
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Erro ao processar dados: {str(e)}\n\n"
            "Verifique o formato e tente novamente.",
            parse_mode='Markdown'
        )
        return IMPORTAR_DADOS


# ============ ATUALIZAÇÃO MENSAL ============

async def atualizar_mes_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando manual para atualizar mês"""
    await update.message.reply_text("🔄 Atualizando parcelas...", parse_mode='Markdown')
    
    resultado = sheets.atualizar_mes()
    
    if resultado:
        mensagem = f"""
✅ *Mês Atualizado!*

📊 Compras atualizadas: {resultado['atualizadas']}
✔️ Compras finalizadas: {resultado['finalizadas']}
📅 Data: {resultado['data_atualizacao']}

As parcelas foram atualizadas automaticamente! 🎉
        """
        await update.message.reply_text(mensagem, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Erro ao atualizar mês.",
            parse_mode='Markdown'
        )


def atualizar_mes_automatico():
    """Função para atualização automática agendada"""
    logger.info("Executando atualização automática mensal...")
    resultado = sheets.atualizar_mes()
    if resultado:
        logger.info(f"✅ Atualização concluída: {resultado}")
    else:
        logger.error("❌ Erro na atualização automática")


# ============ OUTROS COMANDOS ============

async def cartoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todos os cartões"""
    compras = sheets.listar_compras(status='ativo')
    cartoes_unicos = set(c['Cartão'] for c in compras)
    
    mensagem = "💳 *Cartões Cadastrados:*\n\n"
    for cartao in sorted(cartoes_unicos):
        mensagem += f"• {cartao}\n"
    
    mensagem += f"\n📦 Total: {len(cartoes_unicos)} cartões"
    await update.message.reply_text(mensagem, parse_mode='Markdown')


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela operação atual"""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Operação cancelada!",
        parse_mode='Markdown'
    )
    return ConversationHandler.END


# ============ MAIN ============

def main():
    """Função principal"""
    # Verificar configuração
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN não configurado!")
        return
    
    # Garantir abas na planilha
    sheets.garantir_abas()
    
    # Criar aplicação
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers de comandos simples
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("listar", listar))
    app.add_handler(CommandHandler("resumo", resumo))
    app.add_handler(CommandHandler("cartoes", cartoes))
    app.add_handler(CommandHandler("atualizarmes", atualizar_mes_comando))
    
    # Conversação: Adicionar compra
    conv_adicionar = ConversationHandler(
        entry_points=[CommandHandler("adicionar", adicionar_start)],
        states={
            ADICIONAR_DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_descricao)],
            ADICIONAR_VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_valor)],
            ADICIONAR_PARCELA_INICIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_parcela_inicial)],
            ADICIONAR_TOTAL_PARCELAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_total_parcelas)],
            ADICIONAR_CARTAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, adicionar_cartao)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )
    app.add_handler(conv_adicionar)
    
    # Conversação: Adicionar receita
    conv_receita = ConversationHandler(
        entry_points=[CommandHandler("receita", receita_start)],
        states={
            RECEITA_DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receita_descricao)],
            RECEITA_VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receita_valor)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )
    app.add_handler(conv_receita)
    
    # Conversação: Importar dados
    conv_importar = ConversationHandler(
        entry_points=[CommandHandler("importar", importar_start)],
        states={
            IMPORTAR_DADOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, importar_dados)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )
    app.add_handler(conv_importar)
    
    # Agendar atualização automática (todo dia 1 às 00:01)
    schedule.every().day.at("00:01").do(atualizar_mes_automatico)
    
    logger.info("🤖 Bot iniciado com sucesso!")
    
    # Iniciar bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
