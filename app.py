from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'nucleo_inclusao_sumare_2024'  # Chave secreta para sessões
DATABASE = "nucleo_inclusao.db"

# Usuários autorizados do sistema
USUARIOS_AUTORIZADOS = {
    "ProfRodrigoDias": "Pr123456",
    "Erika_Inclusao": "Er123456",
    "Edmilson_Inclusão": "Ed123456"
}

# Perguntas do questionário de observação escolar
OBSERVACOES = [
    ("contato_visual", "Evita contato visual com frequência?"),
    ("dificuldade_interacao", "Tem dificuldade em interagir com colegas?"),
    ("prefere_sozinho", "Prefere brincar ou permanecer sozinho?"),
    ("dificuldade_regras", "Apresenta dificuldade para compreender regras sociais simples?"),
    ("resposta_chamado", "Tem dificuldade para responder quando é chamado pelo nome?"),
    ("comunicacao_oral", "Apresenta atraso ou dificuldade na comunicação oral?"),
    ("repeticao_palavras", "Repete palavras, frases ou sons com frequência?"),
    ("expressar_necessidades", "Tem dificuldade em expressar necessidades básicas?"),
    ("incômodo_sensoriais", "Demonstra incômodo intenso com barulhos, luzes, cheiros ou texturas?"),
    ("movimentos_repetitivos", "Apresenta movimentos repetitivos, como balançar as mãos ou o corpo?"),
    ("apego_rotinas", "Demonstra apego intenso a rotinas?"),
    ("irritacao_mudancas", "Fica muito irritado com mudanças inesperadas?"),
    ("interesses_restritos", "Apresenta interesses muito restritos ou repetitivos?"),
    ("crises_sem_causa", "Tem crises de choro, irritação ou agitação sem causa aparente?"),
    ("dificuldade_concentracao", "Apresenta dificuldade de concentração nas atividades?"),
    ("apoio_constante", "Necessita de apoio constante para realizar tarefas escolares?"),
    ("seletividade_alimentar", "Apresenta seletividade alimentar relatada pela família?"),
    ("dificuldade_grupo", "Apresenta dificuldade em participar de atividades em grupo?"),
    ("sensibilidade_toque", "Demonstra sensibilidade ao toque ou contato físico?"),
    ("familia_alertada", "A escola já conversou com a família sobre essas observações?")
]

OPCOES_OBSERVACAO = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]

# Lista de escolas municipais para o dropdown de cadastro.
ESCOLAS_MUNICIPAIS = [
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
    "EM CAIC ANDRÉ DE NADAI",
    "EM JOSÉ DE ANCHIETA",
    "EM DR. LEANDRO FRANCESCHINI",
    "EMEF PROF° ANALIA DE OLIVEIRA NASCIMENTO",
    "EMEF ANTONIETA CIA VIEL",
    "EMEF ANTONIO PALIOTO",
    "EMEF D. AUGUSTA RAVAGNANI BASSO",
    "EMEF PROF° ELIANA MICHIN VAUGHAN",
    "EMEF PROF° FLORA FERREIRA GOMES",
    "EMEF PROF° NEUZA DE SOUZA CAMPOS",
    "EMEF PROF° NILZA TOMAZIN",
    "EMEF RAMONA CANHETE PINTO",
    "EMEIEF OSWALDO RONCOLATO",
    "EMEI SANTO TOMAZINI",
    "EMEF Maria Aparecida de Jesus Segura",
]

# Mapeamento inicial de escolas para regiões sugeridas.
# Esta classificação regional é inicial e deve ser validada oficialmente
# pela Secretaria Municipal de Educação.
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
    "EM CAIC ANDRÉ DE NADAI": "Santa Carolina / CAIC",
    "EM JOSÉ DE ANCHIETA": "Cruzeiro",
    "EM DR. LEANDRO FRANCESCHINI": "Cruzeiro",
    "EMEF PROF° ANALIA DE OLIVEIRA NASCIMENTO": "Parque Emília / Virgílio Viel",
    "EMEF ANTONIETA CIA VIEL": "Parque Emília / Virgílio Viel",
    "EMEF ANTONIO PALIOTO": "Bandeirantes",
    "EMEF D. AUGUSTA RAVAGNANI BASSO": "Denadai",
    "EMEF PROF° ELIANA MICHIN VAUGHAN": "Rural / Assentamento",
    "EMEF PROF° FLORA FERREIRA GOMES": "Rural / Assentamento",
    "EMEF PROF° NEUZA DE SOUZA CAMPOS": "Rural / Assentamento",
    "EMEF PROF° NILZA TOMAZIN": "Rural / Assentamento",
    "EMEF RAMONA CANHETE PINTO": "Centro / Região Central",
    "EMEIEF OSWALDO RONCOLATO": "Santa Carolina / CAIC",
    "EMEI SANTO TOMAZINI": "Cruzeiro",
    "EMEF Maria Aparecida de Jesus Segura": "Parque Emília / Virgílio Viel",
}

REGIOES_ESCOLAS = [
    "Centro / Região Central",
    "Nova Veneza",
    "Maria Antônia / Picerno",
    "Área Cura / Matão",
    "Bom Retiro",
    "Denadai",
    "Bandeirantes",
    "Residencial Regina / Salerno",
    "Santa Carolina / CAIC",
    "Cruzeiro",
    "Parque Emília / Virgílio Viel",
    "Jardim Lúcia / São Judas",
    "Rural / Assentamento",
]

# Mensagem de aviso obrigatório do sistema
AVISO_IMPORTANTE = (
    "Este formulário não substitui avaliação médica, psicológica, neurológica ou multiprofissional. "
    "Ele serve apenas para registrar observações escolares e auxiliar o Núcleo de Inclusão no acompanhamento e encaminhamento."
)


def get_db_connection():
    """Abre conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela de cadastros se ela não existir."""
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
    conn.commit()
    conn.close()


def ensure_db_schema():
    """Garante que colunas extras existam no banco de dados."""
    conn = get_db_connection()
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


def get_count_group_by(column, limit=None):
    conn = get_db_connection()
    query = f"SELECT {column} AS key, COUNT(*) AS total FROM alunos GROUP BY {column} ORDER BY total DESC"
    if limit:
        query += f" LIMIT {limit}"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_recent_cadastros(limit=10):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT aluno_nome, escola_nome, data_cadastro, status_caso, nivel_atencao FROM alunos ORDER BY data_cadastro DESC, aluno_nome ASC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_dashboard_metrics():
    conn = get_db_connection()
    total_alunos = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    total_escolas = conn.execute("SELECT COUNT(DISTINCT escola_nome) FROM alunos").fetchone()[0]
    casos_atencao = conn.execute(
        "SELECT COUNT(*) FROM alunos WHERE status_caso IN (?, ?, ?)",
        ("Em atenção", "Acompanhamento", "Encaminhamento recomendado"),
    ).fetchone()[0]
    registros_recentes = conn.execute(
        "SELECT COUNT(*) FROM alunos WHERE data_cadastro >= date('now','-7 days')"
    ).fetchone()[0]
    conn.close()
    return {
        "total_alunos": total_alunos,
        "total_escolas": total_escolas,
        "casos_atencao": casos_atencao,
        "registros_recentes": registros_recentes,
    }


def calcular_pontuacao(dados):
    """Calcula a pontuação total do questionário de observações."""
    mapa_pontos = {
        "Nunca": 0,
        "Raramente": 1,
        "Às vezes": 2,
        "Frequentemente": 3,
        "Sempre": 4,
    }
    total = 0
    for campo, _ in OBSERVACOES:
        valor = dados.get(campo, "Nunca")
        total += mapa_pontos.get(valor, 0)
    return total


def classificar_pontuacao(pontuacao):
    """Classifica o resultado de acordo com a pontuação obtida."""
    if pontuacao <= 20:
        return "Baixa prioridade de acompanhamento"
    if pontuacao <= 45:
        return "Atenção e observação contínua"
    if pontuacao <= 65:
        return "Prioridade para análise do Núcleo de Inclusão"
    return "Alta prioridade para orientação e possível encaminhamento"


# Decorador para proteger rotas que requerem autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Rotas de Autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    """Página de login do sistema."""
    erro = None
    
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()
        
        # Validar credenciais
        if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha incorretos"
    
    return render_template("login.html", erro=erro)


@app.route("/logout")
def logout():
    """Faz logout do usuário."""
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route("/")
@login_required
def index():
    """Página inicial com navegação do sistema."""
    return render_template(
        "index.html",
        aviso=AVISO_IMPORTANTE,
        **get_dashboard_metrics(),
    )


@app.route("/relatorios")
@login_required
def relatorios():
    """Página de relatórios e resumo institucional."""
    metrics = get_dashboard_metrics()
    escolas_por_escola = get_count_group_by("escola_nome")
    escolas_por_regiao = get_count_group_by("unidade_regiao")
    niveis_atencao = get_count_group_by("nivel_atencao")
    turnos = get_count_group_by("turno")

    def add_width(items):
        max_total = max((item["total"] for item in items), default=1)
        return [
            {**item, "width": int(item["total"] * 100 / max_total) if max_total else 0}
            for item in items
        ]

    return render_template(
        "relatorios.html",
        aviso=AVISO_IMPORTANTE,
        data_geracao=datetime.now().strftime("%d/%m/%Y %H:%M"),
        escolas_por_escola=escolas_por_escola,
        escolas_por_regiao=escolas_por_regiao,
        niveis_atencao=niveis_atencao,
        turnos=turnos,
        escolas_top=add_width(escolas_por_escola[:6]),
        regioes_top=add_width(escolas_por_regiao[:5]),
        niveis_top=add_width(niveis_atencao),
        cadastros_recentes=get_recent_cadastros(8),
        resumo_indicadores=metrics,
        **metrics,
    )


@app.route("/novo", methods=["GET", "POST"])
@login_required
def novo_cadastro():
    """Tela de cadastro de novo aluno e escola."""
    if request.method == "POST":
        dados = request.form.to_dict()
        conn = get_db_connection()
        campos = [campo for campo, _ in OBSERVACOES] + [
            "escola_nome", "unidade_regiao", "responsavel_preenc", "cargo_funcao",
            "telefone_email", "aluno_nome", "data_nascimento", "idade", "ano_serie",
            "turma", "turno", "responsavel_familiar", "telefone_responsavel",
            "laudo", "aee", "acompanhamento_externo"
        ]
        valores = [dados.get(campo, "") for campo in campos]
        placeholders = ",".join("?" for _ in campos)
        conn.execute(
            f"INSERT INTO alunos ({','.join(campos)}) VALUES ({placeholders})",
            valores,
        )
        conn.commit()
        aluno_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return redirect(url_for("detalhes", aluno_id=aluno_id))

    return render_template(
        "cadastro.html",
        titulo="Novo Cadastro",
        aluno={},
        observacoes=OBSERVACOES,
        opcoes=OPCOES_OBSERVACAO,
        aviso=AVISO_IMPORTANTE,
        escolas_municipais=ESCOLAS_MUNICIPAIS,
        regioes=REGIOES_ESCOLAS,
        escola_regiao=ESCOLA_REGIAO,
    )


@app.route("/alunos", methods=["GET", "POST"])
@login_required
def alunos():
    """Lista todos os alunos cadastrados com suporte a busca integrada."""
    termo = request.values.get("q", "").strip()
    cadastros = []
    mensagem = ""

    if termo:
        termo_sql = f"%{termo}%"
        conn = get_db_connection()
        cadastros = conn.execute(
            "SELECT * FROM alunos WHERE aluno_nome LIKE ? OR escola_nome LIKE ? OR turma LIKE ? ORDER BY aluno_nome",
            (termo_sql, termo_sql, termo_sql),
        ).fetchall()
        conn.close()
        mensagem = f"Resultados da busca para '{termo}' ({len(cadastros)} encontrado{'s' if len(cadastros) != 1 else ''})"
    else:
        conn = get_db_connection()
        cadastros = conn.execute("SELECT * FROM alunos ORDER BY aluno_nome").fetchall()
        conn.close()
        mensagem = "Lista completa de alunos cadastrados"

    return render_template(
        "listar.html",
        cadastros=cadastros,
        aviso=AVISO_IMPORTANTE,
        mensagem=mensagem,
        termo=termo,
    )


@app.route("/detalhes/<int:aluno_id>")
@login_required
def detalhes(aluno_id):
    """Mostra detalhes e resultado da triagem para um aluno."""
    conn = get_db_connection()
    aluno = conn.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,)).fetchone()
    conn.close()

    if aluno is None:
        return redirect(url_for("alunos"))

    dados = dict(aluno)
    pontuacao = calcular_pontuacao(dados)
    classificacao = classificar_pontuacao(pontuacao)

    return render_template(
        "detalhes.html",
        aluno=dados,
        pontuacao=pontuacao,
        classificacao=classificacao,
        observacoes=OBSERVACOES,
        aviso=AVISO_IMPORTANTE,
    )


@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
@login_required
def editar(aluno_id):
    """Editar os dados de um cadastro existente."""
    conn = get_db_connection()
    aluno = conn.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,)).fetchone()

    if aluno is None:
        conn.close()
        return redirect(url_for("alunos"))

    if request.method == "POST":
        dados = request.form.to_dict()
        campos = [campo for campo, _ in OBSERVACOES] + [
            "escola_nome", "unidade_regiao", "responsavel_preenc", "cargo_funcao",
            "telefone_email", "aluno_nome", "data_nascimento", "idade", "ano_serie",
            "turma", "turno", "responsavel_familiar", "telefone_responsavel",
            "laudo", "aee", "acompanhamento_externo"
        ]
        simbolos = ",".join(f"{campo} = ?" for campo in campos)
        valores = [dados.get(campo, "") for campo in campos] + [aluno_id]
        conn.execute(
            f"UPDATE alunos SET {simbolos} WHERE id = ?",
            valores,
        )
        conn.commit()
        conn.close()
        return redirect(url_for("detalhes", aluno_id=aluno_id))

    conn.close()
    return render_template(
        "cadastro.html",
        titulo="Editar Cadastro",
        aluno=dict(aluno),
        observacoes=OBSERVACOES,
        opcoes=OPCOES_OBSERVACAO,
        aviso=AVISO_IMPORTANTE,
        escolas_municipais=ESCOLAS_MUNICIPAIS,
        regioes=REGIOES_ESCOLAS,
        escola_regiao=ESCOLA_REGIAO,
    )


@app.route("/excluir/<int:aluno_id>", methods=["POST"])
@login_required
def excluir(aluno_id):
    """Exclui um cadastro do banco de dados."""
    conn = get_db_connection()
    conn.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("alunos"))


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    else:
        ensure_db_schema()
    app.run(debug=True)
