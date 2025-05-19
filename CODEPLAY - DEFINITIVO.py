import json
import hashlib
import getpass
import time

ARQUIVO_DADOS = "usuarios.json"

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def exibir_termos():
    print("\n[TERMO DE CONSENTIMENTO - LGPD]")
    print("O sistema Codeplay usará seus dados apenas para fins educacionais.")
    return input("Você aceita os termos? (s/n): ").lower() == 's'

def sobre_sistema():
    print("""
========== SOBRE O SISTEMA ==========
Codeplay é uma plataforma educacional voltada à inclusão digital.

Aqui, você aprenderá:
- Programação básica com Python
- Lógica computacional
- Fundamentos da LGPD e segurança digital

Este sistema foi desenvolvido como parte de um projeto acadêmico para
ajudar estudantes a aprender tecnologia de forma acessível.

Para começar, crie sua conta ou faça login.
======================================
""")
    input("Pressione ENTER para voltar ao menu.")

def criar_conta():
    dados = carregar_dados()

    if not exibir_termos():
        print("Cadastro cancelado pelo usuário.")
        return

    nome = input("Digite um nome de usuário: ").strip()
    if not nome or nome in dados:
        print("Nome inválido ou já cadastrado.")
        return

    idade = input("Informe sua idade: ").strip()
    if not idade.isdigit():
        print("A idade deve conter apenas números.")
        return

    senha = getpass.getpass("Crie uma senha segura: ")

    dados[nome] = {
        "idade": int(idade),
        "senha": gerar_hash(senha),
        "modulos": {},
        "pontuacao": {},
        "acessos": 0,
        "tempo_total": 0,
        "tempo_formatado": "0s"
    }

    salvar_dados(dados)
    print(f"Conta criada com sucesso! Bem-vindo(a) ao Codeplay, {nome}.")

def formatar_duracao(segundos):
    if segundos < 60:
        return f"{segundos:.0f}s"
    elif segundos < 3600:
        return f"{segundos / 60:.1f} min"
    else:
        return f"{segundos / 3600:.1f} h"

def acesso_usuario():
    dados = carregar_dados()
    nome = input("Usuário: ").strip()
    senha = getpass.getpass("Senha: ")

    if nome in dados and dados[nome]["senha"] == gerar_hash(senha):
        print(f"Olá, {nome}. Login realizado.")
        dados[nome]["acessos"] += 1
        dados[nome]["inicio_sessao"] = time.time()
        salvar_dados(dados)
        return nome

    print("Usuário ou senha incorretos.")
    return None

def registrar_respostas(nome, modulo, acertos):
    dados = carregar_dados()
    dados[nome]["modulos"][modulo] = "completo"
    dados[nome]["pontuacao"][modulo] = acertos
    salvar_dados(dados)

def ver_duracao_total(nome):
    dados = carregar_dados()
    tempo = dados[nome].get("tempo_formatado", "0s")
    print(f"\nTempo total no sistema: {tempo}")
    input("\nPressione ENTER para voltar.")

def aula(nome, titulo, explicacao, perguntas):
    print(f"\n=== {titulo.upper()} - Codeplay ===\n")
    print(explicacao)
    input("\nPressione ENTER para responder às perguntas.")

    pontos = 0
    for i, (pergunta, opcoes, certa) in enumerate(perguntas, 1):
        print(f"\n{i}) {pergunta}")
        for letra, texto in opcoes.items():
            print(f"   {letra}) {texto}")
        resposta = input("Resposta: ").lower()
        if resposta == certa:
            print("Correto.")
            pontos += 1
        else:
            print("Errado.")

    registrar_respostas(nome, titulo, pontos)
    input("\nPressione ENTER para continuar.")

def modulo_programacao(nome):
    texto = (
        "Neste módulo, você aprenderá conceitos básicos de programação:\n"
        "- Variáveis guardam informações (como nome ou idade).\n"
        "- Tipos de dados: int (número inteiro), float (decimal), str (texto).\n"
        "- Operadores: +, -, *, /, % (resto da divisão).\n"
    )
    quiz = [
        (
            "João quer fazer um programa para somar as idades dos seus irmãos em um projeto da escola. "
            "Qual tipo de dado ele deve usar para armazenar essas idades?",
            {"a": "str", "b": "int", "c": "bool"},
            "b"
        ),
        (
            "Larissa criou uma variável chamada 'temperatura = 37.5' em seu código. Qual o tipo dessa variável?",
            {"a": "int", "b": "float", "c": "str"},
            "b"
        ),
        (
            "Carlos está desenvolvendo um exercício no Codeplay para descobrir o resto da divisão de 15 por 4. "
            "Qual operador ele deve usar?",
            {"a": "*", "b": "/", "c": "%"},
            "c"
        )
    ]
    aula(nome, "programacao", texto, quiz)

def modulo_logica(nome):
    texto = (
        "A lógica computacional nos ajuda a criar regras para tomar decisões no código.\n"
        "- AND: só é verdadeiro se ambas as partes forem verdadeiras.\n"
        "- OR: é verdadeiro se ao menos uma parte for.\n"
        "- NOT: inverte o valor lógico.\n"
        "Exemplo: if idade >= 18 and idade <= 30:"
    )
    quiz = [
        (
            "Em um exercício no Codeplay, Amanda quer que o programa verifique se a idade do aluno está entre 15 e 25 anos. "
            "Qual condição lógica ela deve usar?",
            {
                "a": "idade >= 15 or idade <= 25",
                "b": "idade < 15 and idade > 25",
                "c": "idade >= 15 and idade <= 25"
            },
            "c"
        ),
        (
            "Durante uma aula, o instrutor do Codeplay escreveu: if not False:. "
            "O que o Python irá considerar como resultado lógico dessa condição?",
            {"a": "Verdadeiro", "b": "Falso", "c": "Erro"},
            "a"
        ),
        (
            "Em um projeto do Codeplay, Bruno quer permitir acesso a alunos com menos de 12 anos "
            "ou mais de 60. Qual operador lógico ele deve usar?",
            {"a": "and", "b": "not", "c": "or"},
            "c"
        )
    ]
    aula(nome, "logica", texto, quiz)

def modulo_lgpd(nome):
    texto = (
        "A LGPD é a Lei Geral de Proteção de Dados, que protege informações pessoais.\n"
        "- Dados como nome, CPF e e-mail devem ser protegidos.\n"
        "- Nunca clique em links suspeitos.\n"
        "- Use senhas fortes e únicas.\n"
    )
    quiz = [
        (
            "Em uma atividade do Codeplay, Luana criou um formulário pedindo nome completo, e-mail e CPF. "
            "Esses dados são considerados:",
            {"a": "Públicos", "b": "Pessoais", "c": "Financeiros"},
            "b"
        ),
        (
            "Carlos recebeu uma mensagem oferecendo um curso grátis e pedindo para confirmar seus dados bancários. "
            "Qual seria a melhor atitude a tomar?",
            {
                "a": "Clicar no link para ver do que se trata",
                "b": "Ignorar ou denunciar como phishing",
                "c": "Responder com seus dados por precaução"
            },
            "b"
        ),
        (
            "No Codeplay, Pedro aprendeu a criar senhas mais seguras. Qual das opções abaixo é uma boa prática?",
            {
                "a": "Usar a mesma senha em todos os sites",
                "b": "Compartilhar a senha com alguém de confiança",
                "c": "Criar senhas fortes e diferentes para cada site"
            },
            "c"
        )
    ]
    aula(nome, "lgpd", texto, quiz)

def painel_interativo(nome):
    while True:
        print("\n--- ÁREA DO ALUNO ---")
        print("1. Ver progresso")
        print("2. LGPD")
        print("3. Programação")
        print("4. Lógica")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            ver_duracao_total(nome)
        elif escolha == "2":
            modulo_lgpd(nome)
        elif escolha == "3":
            modulo_programacao(nome)
        elif escolha == "4":
            modulo_logica(nome)
        elif escolha == "5":
            dados = carregar_dados()
            fim = time.time()
            inicio = dados[nome].get("inicio_sessao", fim)
            tempo_gasto = int(fim - inicio)
            dados[nome]["tempo_total"] += tempo_gasto
            dados[nome]["tempo_formatado"] = formatar_duracao(dados[nome]["tempo_total"])
            dados[nome].pop("inicio_sessao", None)
            salvar_dados(dados)
            print(f"Sessão encerrada. Duração: {formatar_duracao(tempo_gasto)}")
            break
        else:
            print("Opção inválida.")

def iniciar_sistema():
    print("=================================")
    print("         BEM-VINDO AO CODEPLAY")
    print(" Plataforma de Inclusão Digital")
    print("=================================")

    while True:
        print("\n1. Sobre o sistema\n2. Criar conta\n3. Entrar\n4. Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            sobre_sistema()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            user = acesso_usuario()
            if user:
                painel_interativo(user)
        elif opcao == "4":
            print("Encerrando o sistema. Até a próxima!")
            break
        else:
            print("Opção inválida.")

# Início da execução
iniciar_sistema()