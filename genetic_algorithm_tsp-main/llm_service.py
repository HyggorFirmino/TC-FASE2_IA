import os
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configure sua API KEY aqui ou garanta que esteja nas variáveis de ambiente
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def gerar_relatorio_motorista(rota_ordenada, dados_veiculos):
    if not GROQ_API_KEY:
        return "Erro: Chave de API da Groq (GROQ_API_KEY) não encontrada. Configure a variável de ambiente."

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""
        Atue como um Gerente de Logística Hospitalar experiente.
        
        CONTEXTO:
        Foi gerada uma rota otimizada para entrega de suprimentos/medicamentos.
        
        DADOS DA ROTA:
        Rota Ordenada (Índices das Cidades): {rota_ordenada}
        
        DADOS DOS VEÍCULOS/VIAGENS:
        {dados_veiculos}
        
        TAREFAS:
        1. Crie instruções claras e passo-a-passo para os motoristas, dividindo por viagem se houver mais de uma.
        2. Destaque explicitamente quaisquer entregas em Cidades CRÍTICAS (prioridade alta), instruindo atenção redobrada.
        3. Analise se a rota parece lógica e eficiente considerando o retorno ao depósito.
        
        Responda em formato de relatório profissional.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Erro ao gerar relatório com Groq: {str(e)}"

def enviar_pergunta_chat(contexto, pergunta):
    if not GROQ_API_KEY:
        return "Erro: Chave de API da Groq não configurada."
        
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        system_prompt = f"""
        Você é um assistente especialista em logística hospitalar.
        Você tem acesso ao seguinte Relatório de Viagem/Otimização gerado por um Algoritmo Genético:
        
        === INÍCIO DO CONTEXTO ===
        {contexto}
        === FIM DO CONTEXTO ===
        
        Use APENAS essas informações para responder às dúvidas do usuário. Se a informação não estiver no contexto, diga que não sabe.
        Seja direto e prestativo.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Erro no chat: {str(e)}"