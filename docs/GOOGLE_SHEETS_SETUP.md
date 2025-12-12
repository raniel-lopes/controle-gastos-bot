# 📊 Como Configurar o Google Sheets

Guia completo para configurar a integração com Google Sheets.

## 🎯 Visão Geral

O bot usa o Google Sheets para:
- Armazenar dados das compras
- Manter a planilha visual organizada
- Permitir que você veja/edite os dados diretamente no Sheets

## 📋 Pré-requisitos

- Conta Google (Gmail)
- Acesso ao Google Cloud Console

## 🔧 Passo a Passo

### 1. Criar Projeto no Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Faça login com sua conta Google
3. Clique em "Selecionar projeto" no topo
4. Clique em "Novo Projeto"
5. Digite um nome: `Controle Gastos Bot`
6. Clique em "Criar"

### 2. Ativar a API do Google Sheets

1. No menu lateral, vá em: **APIs e Serviços > Biblioteca**
2. Na barra de pesquisa, digite: `Google Sheets API`
3. Clique na API do Google Sheets
4. Clique em **"Ativar"**
5. Repita o processo para: `Google Drive API`

### 3. Criar Credenciais de Conta de Serviço

1. No menu lateral, vá em: **APIs e Serviços > Credenciais**
2. Clique em **"Criar Credenciais"**
3. Selecione **"Conta de serviço"**

4. Preencha os dados:
   - **Nome:** `bot-controle-gastos`
   - **ID:** (gerado automaticamente)
   - **Descrição:** `Bot para gerenciar gastos`
   
5. Clique em **"Criar e continuar"**

6. Em "Conceder acesso ao projeto" (opcional):
   - Pode pular clicando em **"Continuar"**

7. Em "Conceder acesso aos usuários" (opcional):
   - Pode pular clicando em **"Concluir"**

### 4. Baixar o Arquivo de Credenciais

1. Na página de Credenciais, você verá a conta de serviço criada
2. Clique no **e-mail da conta de serviço** (algo como: `bot-controle-gastos@...`)
3. Vá na aba **"Chaves"**
4. Clique em **"Adicionar chave" > "Criar nova chave"**
5. Selecione **JSON**
6. Clique em **"Criar"**

Um arquivo JSON será baixado automaticamente!

### 5. Configurar o Arquivo de Credenciais

1. Renomeie o arquivo baixado para: `credentials.json`
2. Mova o arquivo para a pasta raiz do projeto:
   ```
   controle-gastos-bot/
   ├── bot.py
   ├── credentials.json  ← Aqui!
   └── ...
   ```

**⚠️ IMPORTANTE:**
- O arquivo `credentials.json` está no `.gitignore`
- NUNCA faça commit dele no Git
- NUNCA compartilhe esse arquivo

### 6. Criar a Planilha no Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com)
2. Crie uma **Nova Planilha em Branco**
3. Dê um nome: `Controle de Gastos`
4. Copie o **ID da planilha** da URL:

Exemplo de URL:
```
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0/edit
                                        ^^^^^^^^^^^^^^^^
                                        Este é o ID!
```

### 7. Compartilhar a Planilha com o Bot

1. No arquivo `credentials.json`, procure por `"client_email"`
2. Copie o e-mail (algo como: `bot-controle-gastos@...gserviceaccount.com`)
3. Na planilha do Google Sheets, clique em **"Compartilhar"**
4. Cole o e-mail da conta de serviço
5. Dê permissão de **"Editor"**
6. **Desmarque** "Notificar pessoas"
7. Clique em **"Compartilhar"**

### 8. Configurar o .env

Abra o arquivo `.env` e adicione o ID da planilha:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
SPREADSHEET_ID=1a2b3c4d5e6f7g8h9i0
GOOGLE_SHEETS_CREDENTIALS=credentials.json
```

## ✅ Testar a Conexão

Você pode testar se está tudo certo com um script Python:

```python
# test_sheets.py
from sheets_manager import SheetsManager

sheets = SheetsManager()
print("✅ Conexão com Google Sheets funcionando!")
```

Execute:
```bash
python test_sheets.py
```

Se aparecer "✅ Conexão com Google Sheets funcionando!", está tudo certo!

## 🎨 Estrutura da Planilha

O bot criará automaticamente 3 abas:

### 1. Gastos (Visual)
A planilha bonita que você vê com seus gastos organizados por cartão.

### 2. Database (Oculta)
Dados internos do bot. Pode ocultar essa aba.

Colunas:
- ID
- Descrição
- Valor
- Parcela Inicial
- Total Parcelas
- Parcela Atual
- Mês Início
- Cartão
- Status
- Data Cadastro
- Última Atualização
- Categoria
- Observações

### 3. Receitas
Suas receitas mensais (salário, freelance, etc).

## 🔒 Segurança

**Boas práticas:**

✅ **FAÇA:**
- Mantenha `credentials.json` seguro
- Use `.gitignore` para evitar commit acidental
- Faça backup do arquivo em local seguro

❌ **NÃO FAÇA:**
- Compartilhe o `credentials.json`
- Faça commit dele no Git
- Poste em fóruns ou redes sociais

## 🆘 Problemas Comuns

### Erro: "Permission denied"
- Verifique se compartilhou a planilha com o e-mail da conta de serviço
- Confirme que a permissão é de "Editor"

### Erro: "Spreadsheet not found"
- Verifique se o ID da planilha está correto no `.env`
- Confirme que você está usando o ID, não a URL completa

### Erro: "credentials.json not found"
- Verifique se o arquivo está na pasta raiz
- Confirme que o nome está exatamente como `credentials.json`

### Erro: "API not enabled"
- Ative a Google Sheets API no Google Cloud Console
- Ative também a Google Drive API

### Planilha não atualiza
- Verifique os logs do bot
- Teste a conexão com o script de teste
- Confirme as permissões da conta de serviço

## 📚 Recursos Adicionais

- [Documentação Google Sheets API](https://developers.google.com/sheets/api)
- [Documentação gspread](https://docs.gspread.org/)
- [Google Cloud Console](https://console.cloud.google.com/)

## 🎉 Pronto!

Sua integração com Google Sheets está configurada! 

O bot criará as abas automaticamente na primeira execução.

---

⬅️ [Voltar: Telegram Setup](TELEGRAM_SETUP.md) | ➡️ [Próximo: Deploy 24/7](DEPLOY.md)
