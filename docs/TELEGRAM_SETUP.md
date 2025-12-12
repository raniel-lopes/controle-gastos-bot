# 📱 Como Criar um Bot no Telegram

Guia passo a passo para criar seu bot no Telegram usando o BotFather.

## 🎯 Passo a Passo

### 1. Abra o Telegram

- Abra o aplicativo do Telegram no seu celular ou computador
- Ou acesse [https://web.telegram.org](https://web.telegram.org)

### 2. Encontre o BotFather

- Na barra de pesquisa, digite: `@BotFather`
- Clique no bot oficial (tem verificação azul ✓)

![BotFather](https://core.telegram.org/file/811140184/1/zlN4goPTupk/9ff2f2f01c4bd1b013)

### 3. Crie um Novo Bot

Envie o comando:
```
/newbot
```

### 4. Escolha um Nome

O BotFather vai perguntar:
```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

Digite um nome amigável para seu bot, exemplo:
```
Meu Controle de Gastos
```

### 5. Escolha um Username

O BotFather vai pedir um username:
```
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

O username deve:
- Terminar com `bot`
- Ser único (não pode estar em uso)
- Só pode conter letras, números e underscores

Exemplo:
```
meu_controle_gastos_bot
```

### 6. Copie o Token

Se tudo der certo, você receberá uma mensagem como:
```
Done! Congratulations on your new bot. You will find it at t.me/meu_controle_gastos_bot.

You can now add a description, about section and profile picture for your bot.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**⚠️ IMPORTANTE:**
- Copie o token (a linha grande de números e letras)
- NUNCA compartilhe esse token com ninguém
- Qualquer pessoa com o token pode controlar seu bot

### 7. Configure o Token no Bot

1. Abra o arquivo `.env` na pasta do bot
2. Cole o token:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

## 🎨 Personalize Seu Bot (Opcional)

### Adicionar Foto de Perfil

```
/setuserpic
```

Escolha seu bot e envie uma imagem.

### Adicionar Descrição

```
/setdescription
```

Exemplo:
```
Bot para controle automático de gastos parcelados. Nunca mais atualize parcelas manualmente!
```

### Adicionar Sobre

```
/setabouttext
```

Exemplo:
```
Controle seus gastos de forma inteligente com atualização automática de parcelas.
```

### Configurar Comandos

Para que os comandos apareçam no menu do Telegram:

```
/setcommands
```

Escolha seu bot e cole:
```
start - Inicia o bot
adicionar - Nova compra parcelada
listar - Ver gastos do mês
resumo - Resumo financeiro
receita - Adicionar receita
importar - Importar dados existentes
atualizarmes - Atualizar parcelas
cartoes - Ver cartões cadastrados
help - Ajuda
```

## ✅ Teste seu Bot

1. Procure seu bot no Telegram pelo username escolhido
2. Clique em "Iniciar" ou envie `/start`
3. Se tudo estiver configurado, o bot vai responder!

## 🔒 Segurança

**NUNCA:**
- Compartilhe o token do bot
- Faça commit do token no Git (use `.env` e `.gitignore`)
- Poste o token em fóruns ou chats

**Se o token vazar:**
1. Volte ao BotFather
2. Envie `/mybots`
3. Escolha seu bot
4. Clique em "API Token"
5. Clique em "Revoke current token"
6. Copie o novo token e atualize o `.env`

## 🆘 Problemas Comuns

### "Username já está em uso"
- Escolha outro username único
- Tente adicionar números ou underscores

### "Bot não responde"
- Verifique se o token está correto no `.env`
- Certifique-se de que o bot Python está rodando
- Verifique se não há erros no terminal

### "Token inválido"
- Copie o token completo (sem espaços extras)
- Verifique se não há caracteres extras
- Se necessário, gere um novo token com `/token` no BotFather

## 📚 Comandos Úteis do BotFather

- `/mybots` - Ver seus bots
- `/deletebot` - Deletar um bot
- `/token` - Gerar novo token
- `/setname` - Mudar nome do bot
- `/setdescription` - Mudar descrição
- `/setuserpic` - Mudar foto de perfil
- `/setcommands` - Configurar comandos
- `/deletebot` - Excluir o bot

## 🎉 Pronto!

Seu bot está criado! Agora continue a instalação seguindo o [README.md](../README.md) principal.

---

⬅️ [Voltar para README](../README.md) | ➡️ [Próximo: Configurar Google Sheets](GOOGLE_SHEETS_SETUP.md)
