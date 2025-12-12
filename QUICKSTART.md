# 🚀 Guia Rápido de Instalação

Este guia resume os passos essenciais para colocar o bot para funcionar rapidamente.

## ⚡ Instalação Rápida (5 minutos)

### 1️⃣ Clone e Instale (1 min)

```bash
git clone https://github.com/raniel-lopes/controle-gastos-bot.git
cd controle-gastos-bot
pip install -r requirements.txt
```

### 2️⃣ Configure o Telegram (2 min)

1. Abra o Telegram e procure: `@BotFather`
2. Envie: `/newbot`
3. Escolha nome e username (deve terminar em `bot`)
4. Copie o token gerado

### 3️⃣ Configure o Google Sheets (2 min)

1. Acesse: [console.cloud.google.com](https://console.cloud.google.com)
2. Crie um projeto novo
3. Ative: **Google Sheets API** e **Google Drive API**
4. Crie **Conta de Serviço** em Credenciais
5. Baixe o arquivo JSON e salve como `credentials.json` na pasta do bot

6. Crie uma planilha no [Google Sheets](https://sheets.google.com)
7. Copie o ID da URL (parte entre `/d/` e `/edit`)
8. Compartilhe com o email da conta de serviço (de `credentials.json`)

### 4️⃣ Configure as Variáveis

```bash
cp .env.example .env
```

Edite `.env`:
```env
TELEGRAM_BOT_TOKEN=cole_seu_token_aqui
SPREADSHEET_ID=cole_o_id_da_planilha_aqui
```

### 5️⃣ Teste e Inicie

```bash
# Testar configuração
python test_connection.py

# Iniciar bot
python bot.py
```

## ✅ Verificação Rápida

Se tudo estiver certo, você verá:
```
✅ Conectado ao Google Sheets
✅ Abas verificadas/criadas
🤖 Bot iniciado com sucesso!
```

Agora abra o Telegram e envie `/start` para seu bot!

## 📚 Documentação Completa

Para detalhes completos, consulte:
- [README.md](README.md) - Documentação principal
- [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md) - Guia detalhado do Telegram
- [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md) - Guia detalhado do Google Sheets
- [docs/DEPLOY.md](docs/DEPLOY.md) - Como manter 24/7 online

## 🆘 Problemas?

Execute o teste de configuração:
```bash
python test_connection.py
```

Ele mostrará exatamente o que precisa ser corrigido!

## 🎯 Próximos Passos

1. **Importe seus dados:** `/importar`
2. **Adicione receitas:** `/receita`
3. **Veja o resumo:** `/resumo`
4. **Configure deploy 24/7:** Veja [docs/DEPLOY.md](docs/DEPLOY.md)

---

💡 **Dica:** Use `/help` no bot para ver todos os comandos disponíveis!
