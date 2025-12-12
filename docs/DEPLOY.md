# 🚀 Deploy 24/7 Gratuito

Guia para manter seu bot rodando 24 horas por dia, 7 dias por semana, de graça!

## 🎯 Por que Deploy 24/7?

Se você rodar o bot apenas no seu computador:
- ❌ Bot para quando você desliga o PC
- ❌ Atualização automática mensal não funciona
- ❌ Precisa deixar o computador ligado sempre

Com deploy na nuvem:
- ✅ Bot funciona 24/7
- ✅ Atualização automática funciona
- ✅ Acesse de qualquer lugar

## 🌐 Opções Gratuitas

### 🥇 Recomendado: Railway (Mais Fácil)

**Vantagens:**
- Deploy super fácil
- 500 horas grátis por mês (suficiente!)
- Integração direta com GitHub
- Logs em tempo real

**Desvantagens:**
- Precisa de cartão de crédito (não cobra nada)

#### Passo a Passo Railway:

1. **Crie uma conta:**
   - Acesse [railway.app](https://railway.app)
   - Faça login com GitHub

2. **Novo Projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Conecte com seu repositório `controle-gastos-bot`

3. **Configurar Variáveis de Ambiente:**
   - No painel do Railway, vá em "Variables"
   - Adicione:
     ```
     TELEGRAM_BOT_TOKEN=seu_token_aqui
     SPREADSHEET_ID=id_da_planilha
     ```

4. **Adicionar credentials.json:**
   - Copie todo o conteúdo do seu `credentials.json`
   - No Railway, crie uma variável: `GOOGLE_CREDENTIALS`
   - Cole o conteúdo JSON

5. **Criar Procfile:**
   No repositório, crie um arquivo `Procfile`:
   ```
   worker: python bot.py
   ```

6. **Atualizar config.py:**
   Adicione suporte para variável de ambiente do credentials:
   ```python
   import json
   import os
   
   # No config.py, adicione:
   if os.getenv('GOOGLE_CREDENTIALS'):
       credentials_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
       with open('credentials.json', 'w') as f:
           json.dump(credentials_dict, f)
   ```

7. **Deploy:**
   - Faça commit e push
   - Railway fará deploy automaticamente!

---

### 🥈 Render (Também Muito Bom)

**Vantagens:**
- 750 horas grátis por mês
- Não precisa cartão de crédito
- Fácil de usar

**Desvantagens:**
- Bot dorme após 15 minutos de inatividade (precisa de trick)

#### Passo a Passo Render:

1. **Crie uma conta:**
   - Acesse [render.com](https://render.com)
   - Faça login com GitHub

2. **Novo Web Service:**
   - Clique em "New +"
   - Selecione "Background Worker"
   - Conecte seu repositório

3. **Configurar:**
   - Name: `controle-gastos-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

4. **Variáveis de Ambiente:**
   Adicione as mesmas variáveis do Railway

5. **Deploy:**
   - Clique em "Create Background Worker"
   - Render fará deploy automaticamente

---

### 🥉 PythonAnywhere

**Vantagens:**
- 100% gratuito
- Muito estável
- Ótimo para Python

**Desvantagens:**
- Configuração mais manual
- Interface mais antiga

#### Passo a Passo PythonAnywhere:

1. **Criar conta:**
   - Acesse [pythonanywhere.com](https://www.pythonanywhere.com)
   - Crie conta gratuita

2. **Abrir Bash Console:**
   - Dashboard > Consoles > Bash

3. **Clonar repositório:**
   ```bash
   git clone https://github.com/seu-usuario/controle-gastos-bot.git
   cd controle-gastos-bot
   ```

4. **Instalar dependências:**
   ```bash
   pip3 install --user -r requirements.txt
   ```

5. **Configurar variáveis:**
   Crie arquivo `.env`:
   ```bash
   nano .env
   ```
   Cole suas variáveis e salve (Ctrl+O, Enter, Ctrl+X)

6. **Upload credentials.json:**
   - Use o botão "Upload a file" no Files tab
   - Faça upload do `credentials.json`

7. **Criar Task Agendada:**
   - Dashboard > Tasks
   - Adicione: `cd /home/seu_usuario/controle-gastos-bot && python3 bot.py`
   - Configure para rodar sempre

---

## 📦 Arquivos Necessários para Deploy

### Procfile
```
worker: python bot.py
```

### runtime.txt (opcional)
```
python-3.11.0
```

### requirements.txt
Já está criado! ✅

## 🔒 Segurança no Deploy

**NUNCA faça commit de:**
- ❌ `.env`
- ❌ `credentials.json`
- ❌ Tokens ou senhas

**Use variáveis de ambiente:**
- ✅ No Railway: Variables tab
- ✅ No Render: Environment variables
- ✅ No PythonAnywhere: arquivo `.env`

## 🔍 Verificar se está Funcionando

1. **Envie /start para o bot**
   - Se responder, está rodando!

2. **Verifique os logs:**
   - Railway: Logs tab
   - Render: Logs tab
   - PythonAnywhere: Error log

3. **Teste a atualização:**
   - Envie `/atualizarmes`
   - Veja se atualiza a planilha

## 🆘 Problemas Comuns

### Bot não inicia

**Verifique:**
- Variáveis de ambiente corretas
- `credentials.json` está acessível
- Logs para ver o erro exato

### Bot para depois de um tempo

**Railway:**
- Verifique se tem horas disponíveis
- Veja o uso em Dashboard

**Render:**
- Plano gratuito dorme após inatividade
- Considere upgrade ou use Railway

**PythonAnywhere:**
- Verifique se a task está rodando
- Reative se necessário

### Erro de credenciais

- Confirme que `GOOGLE_CREDENTIALS` está correto
- Verifique se o JSON está bem formatado
- Teste localmente primeiro

## 💡 Dicas Extras

### Monitorar o Bot

Adicione um comando de status:
```python
@app.command('status')
def status_command(update, context):
    update.message.reply_text("✅ Bot online e funcionando!")
```

### Logs Melhores

Configure logging no Railway/Render:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Backup Automático

Configure backup da planilha:
- Google Sheets > File > Version History
- Ou use Google Drive Backup

## 🎉 Pronto!

Seu bot está rodando 24/7 na nuvem! 🚀

Agora você pode:
- ✅ Usar o bot de qualquer lugar
- ✅ Atualização automática funciona
- ✅ Desligar seu computador tranquilo

## 📚 Recursos Adicionais

- [Documentação Railway](https://docs.railway.app/)
- [Documentação Render](https://render.com/docs)
- [Documentação PythonAnywhere](https://help.pythonanywhere.com/)

---

⬅️ [Voltar: Google Sheets Setup](GOOGLE_SHEETS_SETUP.md) | ⬅️ [Voltar ao README](../README.md)
