import random
import sqlite3
from datetime import date, timedelta

DATABASE = "nucleo_inclusao.db"

ESCOLAS_SELECIONADAS = [
    "EMEI ARCO ÍRIS",
    "EMEI Alfredo Castro Donaire",
    "EMEI BORBOLETINHA AZUL",
    "EMEI O MUNDO ALEGRE DA CRIANÇA",
    "EMEI REINO DA GAROTADA",
    "EMEI SABIDINHO",
    "EMEI XODÓ DA TITIA",
    "EMEI JARDIM PICERNO II",
    "EMEI JARDIM BOM RETIRO",
    "EMEI JARDIM DENADAI",
    "EMEI JARDIM LÚCIA",
    "EMEI JARDIM MARIA ANTONIA",
    "EMEI JARDIM SÃO JUDAS TADEU",
    "EMEI LASQUINHA DE GENTE",
    "EMEI PARQUE RESIDENCIAL REGINA",
    "EMEI PQ.RESIDENCIAL SALERNO",
    "EMEI PALHACINHO DENGOSO",
    "EMEI PARQUE BANDEIRANTES II",
    "EMEI PARQUE DAS NAÇÕES",
    "EMEI VISCONDE DE SABUGOSA",
    "EMEI DO CAIC ANDRÉ DE NADAI",
    "EMEI SANTO TOMAZINI",
]

ESCOLA_REGIAO = {
    "EMEI ARCO ÍRIS": "Centro / Região Central",
    "EMEI Alfredo Castro Donaire": "Nova Veneza",
    "EMEI BORBOLETINHA AZUL": "Maria Antônia / Picerno",
    "EMEI O MUNDO ALEGRE DA CRIANÇA": "Área Cura / Matão",
    "EMEI REINO DA GAROTADA": "Bom Retiro",
    "EMEI SABIDINHO": "Denadai",
    "EMEI XODÓ DA TITIA": "Bandeirantes",
    "EMEI JARDIM PICERNO II": "Maria Antônia / Picerno",
    "EMEI JARDIM BOM RETIRO": "Bom Retiro",
    "EMEI JARDIM DENADAI": "Denadai",
    "EMEI JARDIM LÚCIA": "Jardim Lúcia / São Judas",
    "EMEI JARDIM MARIA ANTONIA": "Maria Antônia / Picerno",
    "EMEI JARDIM SÃO JUDAS TADEU": "Jardim Lúcia / São Judas",
    "EMEI LASQUINHA DE GENTE": "Centro / Região Central",
    "EMEI PARQUE RESIDENCIAL REGINA": "Residencial Regina / Salerno",
    "EMEI PQ.RESIDENCIAL SALERNO": "Residencial Regina / Salerno",
    "EMEI PALHACINHO DENGOSO": "Parque Emília / Virgílio Viel",
    "EMEI PARQUE BANDEIRANTES II": "Bandeirantes",
    "EMEI PARQUE DAS NAÇÕES": "Parque Emília / Virgílio Viel",
    "EMEI VISCONDE DE SABUGOSA": "Santa Carolina / CAIC",
    "EMEI DO CAIC ANDRÉ DE NADAI": "Santa Carolina / CAIC",
    "EMEI SANTO TOMAZINI": "Cruzeiro",
}

PRIMEIROS_NOMES = [
    "Ana", "Bruno", "Carolina", "Daniel", "Eduardo", "Fernanda", "Gabriel",
    "Helena", "Isabela", "Júlia", "Kauã", "Lara", "Miguel", "Nina",
    "Otávio", "Pedro", "Rafaela", "Samuel", "Tainá", "Vitória",
    "Yasmin", "Zoe", "Mateus", "Laura", "Thiago", "Gabriela",
]

ULTIMOS_NOMES = [
    "Silva", "Souza", "Oliveira", "Costa", "Pereira", "Alves", "Rodrigues",
    "Ferreira", "Santos", "Lima", "Gomes", "Ribeiro", "Dias", "Martins",
    "Carvalho", "Melo", "Barbosa", "Rocha", "Nogueira", "Mendes",
]

RESPONSAVEIS = [
    "Mariana Souza", "Paula Oliveira", "Rafael Pereira", "Bruna Lima",
    "Carlos Santos", "Adriana Gomes", "Lucas Ferreira", "Patrícia Almeida",
    "Juliana Martins", "Ricardo Costa", "Fernanda Rocha", "Sandra Carvalho",
    "Roberta Nogueira", "Danilo Ramos", "Simone Araújo", "Luís Fernandes",
]

CARGOS = [
    "Professor(a)", "Coordenador(a)", "Pedagogo(a)", "Diretor(a)", "Orientador(a)"
]

ANOS_SERIE = [
    "1º ano", "2º ano", "3º ano", "4º ano", "5º ano", "6º ano", "7º ano", "8º ano"
]

TURMAS = ["A", "B", "C", "D"]
TURNOS = ["Manhã", "Tarde", "Integral"]
NIVEIS_ATENCAO = ["Baixo", "Médio", "Alto"]
STATUS_CASO = [
    "Em atenção",
    "Acompanhamento",
    "Encaminhamento recomendado",
    "Normal",
]

OBS_PEDAGOGICAS = [
    "Tem apresentado mais dificuldades em atividades de leitura e escrita.",
    "Precisa de apoio para seguir rotinas e tarefas diárias na sala de aula.",
    "Demonstra interesse por atividades artísticas e trabalhos em grupo.",
    "Apresenta ansiedade em momentos de mudança de rotina.",
    "É muito observador e responde bem a instruções visuais.",
    "Tem dificuldade para manter atenção em atividades longas.",
    "Interage bem com colegas quando estimulado pelo professor.",
    "Apresenta comportamentos repetitivos em salas com muito movimento.",
]

SINAIS_OBSERVADOS = [
    "Evita contato visual em situações sociais.",
    "Precisa de reforço frequente para completar tarefas.",
    "Demonstra sensibilidade a barulhos e luzes fortes.",
    "Procura repetição de palavras ou gestos durante a aula.",
    "Mostra dificuldades para seguir regras coletivas.",
    "Busca apoio frequente do professor em atividades em grupo.",
    "Tem distrações frequentes em sala de aula.",
    "Apresenta alterações de humor com mudanças no cronograma.",
]

OPCOES_OBSERVACAO = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola_nome TEXT,
            unidade_regiao TEXT,
            responsavel_preenc TEXT,
            cargo_funcao TEXT,
            telefone_email TEXT,
            aluno_nome TEXT,
            data_nascimento TEXT,
            idade TEXT,
            ano_serie TEXT,
            turma TEXT,
            turno TEXT,
            responsavel_familiar TEXT,
            telefone_responsavel TEXT,
            laudo TEXT,
            aee TEXT,
            acompanhamento_externo TEXT,
            contato_visual TEXT,
            dificuldade_interacao TEXT,
            prefere_sozinho TEXT,
            dificuldade_regras TEXT,
            resposta_chamado TEXT,
            comunicacao_oral TEXT,
            repeticao_palavras TEXT,
            expressar_necessidades TEXT,
            incômodo_sensoriais TEXT,
            movimentos_repetitivos TEXT,
            apego_rotinas TEXT,
            irritacao_mudancas TEXT,
            interesses_restritos TEXT,
            crises_sem_causa TEXT,
            dificuldade_concentracao TEXT,
            apoio_constante TEXT,
            seletividade_alimentar TEXT,
            dificuldade_grupo TEXT,
            sensibilidade_toque TEXT,
            familia_alertada TEXT,
            data_cadastro TEXT,
            status_caso TEXT,
            nivel_atencao TEXT,
            sinais_observados TEXT,
            observacoes_pedagogicas TEXT
        )
        """
    )
    existing = [row["name"] for row in conn.execute("PRAGMA table_info(alunos)")]
    extra_columns = [
        ("data_cadastro", "TEXT"),
        ("status_caso", "TEXT"),
        ("nivel_atencao", "TEXT"),
        ("sinais_observados", "TEXT"),
        ("observacoes_pedagogicas", "TEXT"),
    ]
    for column_name, column_type in extra_columns:
        if column_name not in existing:
            conn.execute(f"ALTER TABLE alunos ADD COLUMN {column_name} {column_type}")
    conn.commit()
    conn.close()


def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")


def random_phone():
    prefix = random.choice(["19", "11", "21"])
    number = random.randint(900000000, 999999999)
    return f"({prefix}) 9{str(number)[1:5]}-{str(number)[5:]}"


def random_aluno_nome():
    return f"{random.choice(PRIMEIROS_NOMES)} {random.choice(ULTIMOS_NOMES)} {random.choice(ULTIMOS_NOMES)}"


def random_data_nascimento():
    start = date.today() - timedelta(days=12 * 365)
    end = date.today() - timedelta(days=8 * 365)
    delta = (end - start).days
    na = start + timedelta(days=random.randint(0, delta))
    return na


def generate_records(count):
    escolas = ESCOLAS_SELECIONADAS.copy()
    assigned_schools = escolas + [random.choice(escolas) for _ in range(count - len(escolas))]
    random.shuffle(assigned_schools)

    statuses = ["Em atenção"] * 18 + ["Acompanhamento"] * 12 + ["Encaminhamento recomendado"] * 6 + ["Normal"] * 14
    random.shuffle(statuses)

    records = []
    for index in range(count):
        escola = assigned_schools[index]
        regiao = ESCOLA_REGIAO.get(escola, "Centro / Região Central")
        data_nasc = random_data_nascimento()
        idade = date.today().year - data_nasc.year
        data_cadastro = date.today() - timedelta(days=random.choice([0, 1]) if index < 2 else random.randint(8, 35))
        status_caso = statuses[index]
        nivel_atencao = (
            "Alto" if status_caso in ["Em atenção", "Encaminhamento recomendado"] else "Médio"
            if status_caso == "Acompanhamento"
            else "Baixo"
        )
        records.append({
            "escola_nome": escola,
            "unidade_regiao": regiao,
            "responsavel_preenc": random.choice(RESPONSAVEIS),
            "cargo_funcao": random.choice(CARGOS),
            "telefone_email": random_phone(),
            "aluno_nome": random_aluno_nome(),
            "data_nascimento": format_date(data_nasc),
            "idade": str(idade),
            "ano_serie": random.choice(ANOS_SERIE),
            "turma": f"{random.choice(TURMAS)}",
            "turno": random.choice(TURNOS),
            "responsavel_familiar": random.choice(RESPONSAVEIS),
            "telefone_responsavel": random_phone(),
            "laudo": random.choice(["Sim", "Não", "Em avaliação"]),
            "aee": random.choice(["Sim", "Não"]),
            "acompanhamento_externo": random.choice(["Sim", "Não", "Não informado"]),
            "contato_visual": random.choice(OPCOES_OBSERVACAO),
            "dificuldade_interacao": random.choice(OPCOES_OBSERVACAO),
            "prefere_sozinho": random.choice(OPCOES_OBSERVACAO),
            "dificuldade_regras": random.choice(OPCOES_OBSERVACAO),
            "resposta_chamado": random.choice(OPCOES_OBSERVACAO),
            "comunicacao_oral": random.choice(OPCOES_OBSERVACAO),
            "repeticao_palavras": random.choice(OPCOES_OBSERVACAO),
            "expressar_necessidades": random.choice(OPCOES_OBSERVACAO),
            "incômodo_sensoriais": random.choice(OPCOES_OBSERVACAO),
            "movimentos_repetitivos": random.choice(OPCOES_OBSERVACAO),
            "apego_rotinas": random.choice(OPCOES_OBSERVACAO),
            "irritacao_mudancas": random.choice(OPCOES_OBSERVACAO),
            "interesses_restritos": random.choice(OPCOES_OBSERVACAO),
            "crises_sem_causa": random.choice(OPCOES_OBSERVACAO),
            "dificuldade_concentracao": random.choice(OPCOES_OBSERVACAO),
            "apoio_constante": random.choice(OPCOES_OBSERVACAO),
            "seletividade_alimentar": random.choice(OPCOES_OBSERVACAO),
            "dificuldade_grupo": random.choice(OPCOES_OBSERVACAO),
            "sensibilidade_toque": random.choice(OPCOES_OBSERVACAO),
            "familia_alertada": random.choice(["Sim", "Não"]),
            "data_cadastro": format_date(data_cadastro),
            "status_caso": status_caso,
            "nivel_atencao": nivel_atencao,
            "sinais_observados": random.choice(SINAIS_OBSERVADOS),
            "observacoes_pedagogicas": random.choice(OBS_PEDAGOGICAS),
        })
    return records


def insert_records(records):
    conn = get_db_connection()
    campos = [
        "escola_nome", "unidade_regiao", "responsavel_preenc", "cargo_funcao",
        "telefone_email", "aluno_nome", "data_nascimento", "idade", "ano_serie",
        "turma", "turno", "responsavel_familiar", "telefone_responsavel",
        "laudo", "aee", "acompanhamento_externo", "contato_visual",
        "dificuldade_interacao", "prefere_sozinho", "dificuldade_regras",
        "resposta_chamado", "comunicacao_oral", "repeticao_palavras",
        "expressar_necessidades", "incômodo_sensoriais", "movimentos_repetitivos",
        "apego_rotinas", "irritacao_mudancas", "interesses_restritos",
        "crises_sem_causa", "dificuldade_concentracao", "apoio_constante",
        "seletividade_alimentar", "dificuldade_grupo", "sensibilidade_toque",
        "familia_alertada", "data_cadastro", "status_caso", "nivel_atencao",
        "sinais_observados", "observacoes_pedagogicas",
    ]
    placeholders = ",".join("?" for _ in campos)
    values = [tuple(record[field] for field in campos) for record in records]
    conn.executemany(
        f"INSERT INTO alunos ({','.join(campos)}) VALUES ({placeholders})",
        values,
    )
    conn.commit()
    conn.close()


def main():
    random.seed(42)
    ensure_schema()
    conn = get_db_connection()
    current_count = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    conn.close()
    if current_count >= 50:
        print(f"O banco já contém {current_count} registros. Nenhuma ação foi necessária.")
        return
    to_insert = 50 - current_count
    records = generate_records(to_insert)
    insert_records(records)
    print(f"Foram inseridos {to_insert} registros fictícios no banco {DATABASE}.")
    print("Métricas esperadas após a inserção:")
    print("- Alunos cadastrados: 50")
    print("- Escolas participantes: 22")
    print("- Casos em atenção: 36")
    print("- Registros recentes: 2")


if __name__ == "__main__":
    main()
