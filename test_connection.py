"""
Script para testar a conexão com Google Sheets
Execute: python test_connection.py
"""
import sys

def testar_configuracao():
    """Testa se todas as configurações estão corretas"""
    print("🔍 Testando configuração do bot...\n")
    
    # Testar imports
    print("📦 Testando imports...")
    try:
        import telegram
        print("  ✅ python-telegram-bot instalado")
    except ImportError:
        print("  ❌ python-telegram-bot NÃO instalado")
        print("     Execute: pip install python-telegram-bot")
        return False
    
    try:
        import gspread
        print("  ✅ gspread instalado")
    except ImportError:
        print("  ❌ gspread NÃO instalado")
        print("     Execute: pip install gspread")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv instalado")
    except ImportError:
        print("  ❌ python-dotenv NÃO instalado")
        print("     Execute: pip install python-dotenv")
        return False
    
    # Testar arquivo .env
    print("\n📄 Testando arquivo .env...")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        spreadsheet_id = os.getenv('SPREADSHEET_ID')
        
        if token:
            print(f"  ✅ TELEGRAM_BOT_TOKEN configurado")
        else:
            print("  ❌ TELEGRAM_BOT_TOKEN NÃO configurado")
            print("     Adicione no arquivo .env")
        
        if spreadsheet_id:
            print(f"  ✅ SPREADSHEET_ID configurado")
        else:
            print("  ❌ SPREADSHEET_ID NÃO configurado")
            print("     Adicione no arquivo .env")
        
        if not token or not spreadsheet_id:
            return False
            
    except FileNotFoundError:
        print("  ❌ Arquivo .env NÃO encontrado")
        print("     Copie .env.example para .env e configure")
        return False
    
    # Testar credentials.json
    print("\n🔑 Testando credentials.json...")
    import os
    if os.path.exists('credentials.json'):
        print("  ✅ credentials.json encontrado")
    else:
        print("  ❌ credentials.json NÃO encontrado")
        print("     Baixe do Google Cloud Console")
        return False
    
    # Testar conexão com Google Sheets
    print("\n📊 Testando conexão com Google Sheets...")
    try:
        from sheets_manager import SheetsManager
        sheets = SheetsManager()
        print("  ✅ Conexão com Google Sheets funcionando!")
        
        # Testar criação de abas
        print("\n📑 Verificando abas da planilha...")
        sheets.garantir_abas()
        print("  ✅ Abas verificadas/criadas com sucesso!")
        
    except Exception as e:
        print(f"  ❌ Erro ao conectar: {e}")
        return False
    
    # Testar bot do Telegram
    print("\n🤖 Testando conexão com Telegram...")
    try:
        import asyncio
        from telegram import Bot
        import os
        
        async def test_telegram_bot():
            bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
            bot_info = await bot.get_me()
            return bot_info
        
        bot_info = asyncio.run(test_telegram_bot())
        print(f"  ✅ Bot conectado: @{bot_info.username}")
    except Exception as e:
        print(f"  ❌ Erro ao conectar: {e}")
        return False
    
    return True


def main():
    """Função principal"""
    print("=" * 50)
    print("🤖 TESTE DE CONFIGURAÇÃO - CONTROLE DE GASTOS BOT")
    print("=" * 50)
    print()
    
    sucesso = testar_configuracao()
    
    print("\n" + "=" * 50)
    if sucesso:
        print("✅ TODAS AS CONFIGURAÇÕES ESTÃO CORRETAS!")
        print("\nVocê pode iniciar o bot com:")
        print("  python bot.py")
    else:
        print("❌ ALGUMAS CONFIGURAÇÕES PRECISAM DE AJUSTE")
        print("\nSiga os passos acima para corrigir.")
    print("=" * 50)
    
    return 0 if sucesso else 1


if __name__ == '__main__':
    sys.exit(main())
