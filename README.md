# 🤖 Controle de Gastos Bot

Bot do Telegram para controle automático de gastos parcelados, integrado com Google Sheets.

## 🎯 Funcionalidades

- ✅ **Cálculo Automático de Parcelas**: Nunca mais atualize parcelas manualmente!
- 📊 **Integração com Google Sheets**: Mantém seu visual colorido e organizado
- 💳 **Múltiplos Cartões**: Gerencie vários cartões em um só lugar
- 💰 **Controle de Receitas**: Saiba quanto sobra no mês
- 📈 **Resumo Financeiro**: Visualize receitas, despesas e saldo
- 🔄 **Atualização Automática**: Todo dia 1 do mês as parcelas são atualizadas
- 📥 **Importação Fácil**: Importe seus dados existentes rapidamente

## 🚀 Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Inicia o bot e mostra as opções |
| `/adicionar` | Adiciona uma nova compra parcelada |
| `/listar` | Lista gastos do mês atual |
| `/resumo` | Mostra resumo financeiro completo |
| `/receita` | Adiciona uma receita |
| `/importar` | Importa dados existentes |
| `/atualizarmes` | Atualiza parcelas manualmente |
| `/cartoes` | Lista todos os cartões cadastrados |
| `/help` | Mostra todos os comandos |

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Google Cloud (gratuita)
- Conta no Telegram

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/raniel-lopes/controle-gastos-bot.git
cd controle-gastos-bot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Bot do Telegram

Siga o guia completo em [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md)

**Resumo:**
1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Escolha um nome e username para seu bot
4. Copie o token gerado

### 4. Configure o Google Sheets

Siga o guia completo em [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md)

**Resumo:**
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a API do Google Sheets
4. Crie credenciais de conta de serviço
5. Baixe o arquivo `credentials.json`

### 5. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
SPREADSHEET_ID=id_da_sua_planilha
GOOGLE_SHEETS_CREDENTIALS=credentials.json
```

### 6. Execute o bot

```bash
python bot.py
```

## 📖 Como Usar

### Adicionar uma Compra

1. Digite `/adicionar` no chat com o bot
2. Responda as perguntas:
   - Descrição (ex: Microfone Igreja)
   - Valor da parcela (ex: 161.90)
   - Parcela atual (ex: 7)
   - Total de parcelas (ex: 10)
   - Cartão (ex: Nubank)

### Importar Dados Existentes

```
/importar

Microfone Igreja | 161.90 | 7/10 | Nubank
Smiles | 32.20 | 1/1 | Nubank
Dentista mãe | 100.00 | 6/10 | Inter
```

### Ver Resumo do Mês

```
/resumo
```

Mostra:
- Total de receitas
- Total de despesas
- Saldo do mês
- Despesas por cartão

## 🎨 Estrutura da Planilha

O bot cria 3 abas no Google Sheets:

1. **Gastos** (Visual) - A planilha bonita que você visualiza
2. **Database** (Oculta) - Dados para o bot gerenciar
3. **Receitas** - Suas receitas mensais

## 🔄 Atualização Automática

O bot atualiza as parcelas automaticamente:
- **Quando:** Todo dia 1 do mês às 00:01
- **O que faz:**
  - Incrementa o número das parcelas (7/10 → 8/10)
  - Marca compras finalizadas (10/10 → Concluído)
  - Atualiza a aba visual

Você também pode forçar a atualização com `/atualizarmes`

## 🌐 Deploy 24/7 Gratuito

Para manter o bot rodando 24/7, veja o guia:
[docs/DEPLOY.md](docs/DEPLOY.md)

Opções gratuitas:
- Railway
- Render
- PythonAnywhere
- Heroku (com limitações)

## 📂 Estrutura do Projeto

```
controle-gastos-bot/
├── bot.py                 # Bot principal do Telegram
├── sheets_manager.py      # Gerenciador do Google Sheets
├── calculator.py          # Cálculo de parcelas
├── config.py              # Configurações
├── requirements.txt       # Dependências
├── .env.example           # Exemplo de variáveis
├── .gitignore            # Arquivos ignorados
├── README.md             # Este arquivo
└── docs/                 # Documentação
    ├── INSTALACAO.md
    ├── TELEGRAM_SETUP.md
    ├── GOOGLE_SHEETS_SETUP.md
    └── DEPLOY.md
```

## 🐛 Troubleshooting

### Bot não inicia

- Verifique se o token do Telegram está correto no `.env`
- Certifique-se de que todas as dependências estão instaladas

### Erro ao conectar com Google Sheets

- Verifique se o arquivo `credentials.json` está na pasta raiz
- Confirme se o ID da planilha está correto no `.env`
- Verifique se a conta de serviço tem acesso à planilha

### Parcelas não atualizam

- Execute `/atualizarmes` manualmente
- Verifique os logs do bot
- Confirme que o bot está rodando 24/7

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar Pull Requests

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por [Raniel Lopes](https://github.com/raniel-lopes)

## 💡 Suporte

Tem dúvidas? Abra uma [issue](https://github.com/raniel-lopes/controle-gastos-bot/issues)!

---

⭐ Se este projeto te ajudou, deixe uma estrela no repositório!
