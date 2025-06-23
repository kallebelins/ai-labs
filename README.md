# 🔬 Laboratório de Soluções e Estudos em Inteligência Artificial

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.10+-brightgreen.svg)

Bem-vindo ao Laboratório de IA! Este repositório serve como uma coleção centralizada de estudos, experimentos e soluções no vasto campo da Inteligência Artificial. Nossa missão é explorar e documentar implementações de IA de forma modular, isolada e altamente reprodutível.

---

## 🎯 Filosofia do Projeto

Este projeto não é uma aplicação única, mas um **monorepo que abriga múltiplos "laboratórios" independentes**. Cada laboratório é uma pasta autocontida que investiga um problema ou tecnologia específica, possuindo seu próprio:

-   Código-fonte
-   Conjunto de dados (data)
-   Dependências de bibliotecas (`requirements.txt`)
-   Testes
-   Notebooks de exploração
-   Resultados e métricas

Essa abordagem garante **isolamento total** entre os experimentos, prevenindo conflitos de dependências e tornando cada estudo 100% reprodutível por qualquer pessoa.

---

## 📂 Estrutura de Diretórios

A estrutura do repositório foi desenhada para ser intuitiva e escalável.

```sh
ai-labs/
│
├── README.md               # Este documento que você está lendo
├── LICENSE                 # Licença do projeto
│
└── labs/                   # O coração do projeto, contendo todos os laboratórios
    │
    ├── 01_chatbot_langchain/   # Exemplo de um laboratório autocontido
    │   ├── README.md           # Documentação específica deste laboratório
    │   ├── requirements.txt    # Dependências Python APENAS para este laboratório
    │   ├── src/                # Código fonte do laboratório
    │   ├── scripts/            # Scripts de execução e utilitários
    │   ├── input/              # Dados de entrada ou arquivos de teste
    │   ├── logs/               # Logs gerados durante as execuções
    │   ├── metrics/            # Relatórios e métricas
    │   └── contents/           # Outros conteúdos (imagens, artigos, etc)
    │
    ├── 02_nome_do_lab/        # Cada laboratório segue a mesma estrutura interna
    │   └── ...
    │
    └── ...                    # Demais laboratórios numerados
```

Cada laboratório é autocontido, com seu próprio ambiente virtual, dependências e organização interna. Não há uma pasta 'shared_utilities' global, mas sim laboratórios independentes, cada um com seu escopo e código isolado.

-----

## 🚀 Começando

Para começar a explorar ou contribuir com os laboratórios, siga os passos abaixo.

### Pré-requisitos

  - [Git](https://git-scm.com/)
  - [Python](https://www.python.org/downloads/) (versão 3.10 ou superior)
  - Familiaridade com ambientes virtuais (`venv` ou `conda`)

### Clonando o Repositório

```bash
git clone https://github.com/kallebelins/ai-labs.git
cd laboratorio_de_ia
```

-----

## 🛠️ Fluxo de Trabalho

A interação com o projeto é feita no nível de cada laboratório individualmente.

### 1\. Trabalhando em um Laboratório Existente

Cada laboratório possui seu próprio ambiente para garantir o isolamento.

1.  **Navegue até a pasta do laboratório desejado:**

    ```bash
    cd labs/01_nome_do_lab/
    ```

2.  **Crie e ative um ambiente virtual local para este laboratório:**

    ```bash
    # Cria o ambiente na pasta .venv (que é ignorada pelo .gitignore)
    python -m venv .venv

    # Ativa o ambiente
    # No Linux/macOS:
    source .venv/bin/activate
    # No Windows:
    # .\.venv\Scripts\activate
    ```

3.  **Instale as dependências específicas do laboratório:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **(Opcional) Se o laboratório utilizar código compartilhado, instale o pacote `shared_utilities`:**

    ```bash
    pip install -e ../shared_utilities/
    ```

    O comando `-e` o instala em modo "editável", o que é ideal para desenvolvimento.

5.  **Pronto\!** Agora você pode executar os scripts, notebooks e testes contidos neste laboratório.

### 2\. Criando um Novo Laboratório

Quer iniciar um novo estudo? Siga este checklist detalhado:

1. **Crie a pasta do laboratório**
   - No diretório `labs/`, crie uma nova pasta com um nome descritivo e, preferencialmente, um prefixo numérico sequencial (ex: `03_analise_multimodal_de_videos`).
   - Exemplo:
     ```bash
     mkdir labs/03_analise_multimodal_de_videos
     cd labs/03_analise_multimodal_de_videos
     ```

2. **Crie a estrutura de subpastas**
   - Recomenda-se a seguinte estrutura mínima:
     - `src/` — Código-fonte principal do laboratório
     - `scripts/` — Scripts utilitários, de execução ou automação
     - `input/` — Dados de entrada, arquivos de teste ou exemplos
     - `logs/` — Logs gerados durante execuções
     - `metrics/` — Relatórios, métricas e resultados
     - `contents/` — Imagens, artigos, documentação extra, etc.
   - Exemplo:
     ```bash
     mkdir src scripts input logs metrics contents
     ```

3. **Crie o arquivo de dependências**
   - Crie um arquivo `requirements.txt` na raiz do laboratório, listando todas as bibliotecas necessárias para o funcionamento do seu projeto.
   - Exemplo:
     ```
     langchain
     openai
     pandas
     ```

4. **Crie a documentação do laboratório**
   - Crie um arquivo `README.md` explicando:
     - O objetivo do laboratório
     - Como configurar o ambiente e instalar dependências
     - Como executar scripts e testes
     - Quais resultados são esperados
     - Qualquer configuração especial (ex: variáveis de ambiente, chaves de API)
   - Inclua exemplos de uso e instruções para reprodutibilidade.

5. **(Opcional) Adicione arquivos de dados ou exemplos**
   - Se necessário, adicione arquivos de entrada em `input/` ou exemplos de logs em `logs/`.

6. **(Opcional) Adicione um arquivo `.gitignore**
   - Para ignorar arquivos temporários, ambientes virtuais, dados sensíveis, etc.

7. **(Opcional) Crie um ambiente virtual local**
   - Para garantir o isolamento das dependências:
     ```bash
     python -m venv .venv
     # Ative o ambiente conforme seu sistema operacional
     ```

8. **Implemente o código e scripts iniciais**
   - Comece a desenvolver seu experimento, script ou solução dentro da estrutura criada.

9. **Teste a reprodutibilidade**
   - Siga o passo a passo do seu próprio README para garantir que qualquer pessoa consiga rodar o laboratório do zero.

10. **Faça commits frequentes**
    - Versione seu progresso e documente mudanças relevantes.

Se precisar de exemplos de README ou arquivos de configuração, consulte os laboratórios já existentes no repositório!

-----

## ✨ O Pacote `shared_utilities`

Para evitar a repetição de código, funções genéricas e reutilizáveis (ex: funções de plotagem, carregamento de dados, conexão com APIs) devem ser colocadas no laboratório especial `labs/shared_utilities`. Ele funciona como uma biblioteca interna do projeto. Consulte o `README.md` dentro da pasta `shared_utilities` para mais detalhes sobre seu conteúdo e como contribuir.

-----

## 🤝 Como Contribuir

A contribuição é a força vital de um projeto de referência\! Se você deseja adicionar melhorias ou novos laboratórios, siga o fluxo padrão do GitHub:

1.  **Fork** este repositório.
2.  Crie uma nova **Branch** para sua feature (`git checkout -b feature/meu-novo-lab`).
3.  Faça o **Commit** de suas mudanças (`git commit -m 'Adiciona o laboratório X que faz Y'`).
4.  Faça o **Push** para a sua branch (`git push origin feature/meu-novo-lab`).
5.  Abra um **Pull Request** para discussão e revisão.

-----

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.
