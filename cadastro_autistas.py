import json
import os

# Nome do arquivo JSON onde os dados serão salvos
ARQUIVO_DADOS = "autistas.json"


def carregar_dados():
    """Carrega a lista de cadastros do arquivo JSON.

    Se o arquivo não existir ou estiver vazio, retorna uma lista vazia.
    """
    if not os.path.exists(ARQUIVO_DADOS):
        return []

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, IOError):
        return []


def salvar_dados(cadastros):
    """Salva a lista de cadastros no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(cadastros, arquivo, ensure_ascii=False, indent=4)


def cadastrar_autista(cadastros):
    """Solicita os dados do autista e adiciona à lista."""
    print("\n=== Cadastro de Autista ===")
    nome = input("Nome: ").strip()
    idade = input("Idade: ").strip()
    responsavel = input("Responsável: ").strip()
    telefone = input("Telefone: ").strip()
    escola = input("Escola: ").strip()

    if not nome:
        print("O nome é obrigatório. Cadastro cancelado.")
        return

    cadastro = {
        "nome": nome,
        "idade": idade,
        "responsavel": responsavel,
        "telefone": telefone,
        "escola": escola,
    }

    cadastros.append(cadastro)
    salvar_dados(cadastros)
    print("Cadastro realizado com sucesso!\n")


def listar_cadastros(cadastros):
    """Mostra todos os cadastros existentes."""
    print("\n=== Lista de Autistas Cadastrados ===")
    if not cadastros:
        print("Nenhum cadastro encontrado.\n")
        return

    for indice, cadastro in enumerate(cadastros, start=1):
        print(f"{indice}. Nome: {cadastro['nome']}")
        print(f"   Idade: {cadastro['idade']}")
        print(f"   Responsável: {cadastro['responsavel']}")
        print(f"   Telefone: {cadastro['telefone']}")
        print(f"   Escola: {cadastro['escola']}\n")


def buscar_por_nome(cadastros):
    """Busca cadastros pelo nome (parcial e sem diferenciar maiúsculas)."""
    termo = input("\nDigite o nome para buscar: ").strip().lower()
    if not termo:
        print("Termo de busca vazio.\n")
        return

    resultados = [cad for cad in cadastros if termo in cad["nome"].lower()]

    if not resultados:
        print("Nenhum cadastro encontrado para esse nome.\n")
        return

    print("\n=== Resultados da Busca ===")
    for indice, cadastro in enumerate(resultados, start=1):
        print(f"{indice}. Nome: {cadastro['nome']}")
        print(f"   Idade: {cadastro['idade']}")
        print(f"   Responsável: {cadastro['responsavel']}")
        print(f"   Telefone: {cadastro['telefone']}")
        print(f"   Escola: {cadastro['escola']}\n")


def escolher_cadastro(cadastros, mensagem="Escolha o número do cadastro: "):
    """Mostra os cadastros e permite escolher um pelo número."""
    if not cadastros:
        print("Nenhum cadastro disponível.\n")
        return None

    listar_cadastros(cadastros)
    escolha = input(mensagem).strip()

    if not escolha.isdigit():
        print("Entrada inválida. Digite um número.\n")
        return None

    indice = int(escolha) - 1
    if indice < 0 or indice >= len(cadastros):
        print("Número fora do intervalo.\n")
        return None

    return indice


def editar_cadastro(cadastros):
    """Edita os dados de um cadastro já existente."""
    print("\n=== Editar Cadastro ===")
    indice = escolher_cadastro(cadastros)
    if indice is None:
        return

    cadastro = cadastros[indice]
    print("Deixe em branco para manter o valor atual.")

    nome = input(f"Nome [{cadastro['nome']}]: ").strip()
    idade = input(f"Idade [{cadastro['idade']}]: ").strip()
    responsavel = input(f"Responsável [{cadastro['responsavel']}]: ").strip()
    telefone = input(f"Telefone [{cadastro['telefone']}]: ").strip()
    escola = input(f"Escola [{cadastro['escola']}]: ").strip()

    if nome:
        cadastro["nome"] = nome
    if idade:
        cadastro["idade"] = idade
    if responsavel:
        cadastro["responsavel"] = responsavel
    if telefone:
        cadastro["telefone"] = telefone
    if escola:
        cadastro["escola"] = escola

    salvar_dados(cadastros)
    print("Cadastro atualizado com sucesso!\n")


def excluir_cadastro(cadastros):
    """Remove um cadastro da lista."""
    print("\n=== Excluir Cadastro ===")
    indice = escolher_cadastro(cadastros, "Digite o número do cadastro que deseja excluir: ")
    if indice is None:
        return

    cadastro = cadastros.pop(indice)
    salvar_dados(cadastros)
    print(f"Cadastro de {cadastro['nome']} excluído com sucesso!\n")


def mostrar_menu():
    """Exibe o menu principal para o usuário."""
    print("=== Núcleo de Inclusão - Cadastro de Autistas ===")
    print("1 - Cadastrar autista")
    print("2 - Listar todos os cadastrados")
    print("3 - Buscar por nome")
    print("4 - Editar cadastro")
    print("5 - Excluir cadastro")
    print("0 - Sair")


def main():
    """Função principal que controla o fluxo do programa."""
    cadastros = carregar_dados()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_autista(cadastros)
        elif opcao == "2":
            listar_cadastros(cadastros)
        elif opcao == "3":
            buscar_por_nome(cadastros)
        elif opcao == "4":
            editar_cadastro(cadastros)
        elif opcao == "5":
            excluir_cadastro(cadastros)
        elif opcao == "0":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Digite um número entre 0 e 5.\n")


if __name__ == "__main__":
    main()
