# Sistema de Triagem e Acompanhamento Inclusivo

Sistema web em Python usando Flask para cadastro e triagem de possíveis casos de alunos com sinais de TEA no Núcleo de Inclusão da Secretaria Municipal de Educação de Sumaré.

> Este formulário não substitui avaliação médica, psicológica, neurológica ou multiprofissional. Ele serve apenas para registrar observações escolares e auxiliar o Núcleo de Inclusão no acompanhamento e encaminhamento.

## Requisitos

- Python 3
- Flask

## Instalação

1. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
```

2. Ative o ambiente virtual:

No Windows:

```powershell
venv\Scripts\Activate.ps1
```

3. Instale o Flask:

```bash
pip install flask
```

## Como executar

No diretório do projeto, execute:

```bash
python app.py
```

O sistema ficará disponível em:

```
http://127.0.0.1:5000
```

## Funcionalidades

- Cadastro de escola e aluno
- Questionário de observação escolar
- Cálculo automático de pontuação
- Classificação simples de prioridade de acompanhamento
- Listar alunos cadastrados
- Buscar por nome do aluno ou nome da escola
- Visualizar, editar e excluir cadastros
- Relatório em HTML simples para impressão

## Estrutura de arquivos

- `app.py` - aplicação Flask e lógica de banco de dados
- `templates/` - páginas HTML
- `static/style.css` - estilos da interface
