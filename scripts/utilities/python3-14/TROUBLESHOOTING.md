# Troubleshooting: Instalação do Python 3.14 via deadsnakes PPA

## Problema 1: `add-apt-repository` trava com timeout

O comando tenta conectar ao Launchpad para validar metadados do PPA e falha:

```
TimeoutError: [Errno 110] Connection timed out
```

**Solução:** Adicionar o PPA manualmente, sem passar pelo Launchpad.

## Problema 2: `curl` retorna erro 400

O `&` no URL sem aspas faz o shell interpretar o resto como processo em background:

```bash
# Errado — o shell quebra o URL no &
curl -fsSL https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF23C...

# Correto — URL entre aspas
curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF23C..."
```

## Solução completa (Ubuntu Noble 24.04)

```bash
# 1. Importa a chave GPG
curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF23C5A6CF475977595C89F51BA6932366A755776" \
  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/deadsnakes.gpg

# 2. Adiciona o repositório
echo "deb https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu noble main" \
  | sudo tee /etc/apt/sources.list.d/deadsnakes-ppa.list

# 3. Atualiza e instala
sudo apt-get update -q
sudo apt-get install --yes python3.14 python3.14-dev python3.14-venv
```
