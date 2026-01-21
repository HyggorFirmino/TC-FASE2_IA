Tech Challenge - Fase 2 (IADT) Sistema inteligente de roteamento para distribuição de medicamentos e órgãos vitais, combinando Algoritmos Genéticos (GA) e Inteligência Artificial Generativa (LLM).
📋 Sobre o Projeto
O MedFlow AI é uma solução de logística desenvolvida para otimizar a entrega de insumos médicos em cenários críticos. O sistema não apenas encontra o caminho mais curto, mas considera variáveis complexas como prioridade de entrega (itens críticos vs. normais) e capacidade de carga dos veículos (Vehicle Routing Problem - VRP).
Além do motor matemático, o projeto integra um módulo de LLM (Large Language Model) que atua como um "Gerente de Logística Virtual", gerando relatórios de turno e respondendo dúvidas sobre a operação em linguagem natural via Chatbot.
🚀 Funcionalidades Principais
• Algoritmo Genético (GA): Utiliza conceitos de evolução (seleção, crossover e mutação) para resolver o problema do Caixeiro Viajante (TSP) adaptado.
• Gestão de Capacidade (VRP): Segmenta a rota otimizada em múltiplos veículos baseando-se no peso da carga e capacidade do caminhão.
• Sistema de Prioridades: Penaliza severamente rotas que negligenciam entregas "Críticas" em favor de entregas normais, garantindo urgência onde é necessário.
• Visualização em Tempo Real: Interface gráfica em Pygame mostrando a evolução das rotas, diferenciação de veículos por cor e status das entregas.
• Benchmark Integrado: Comparativo em tempo real entre a eficiência do Algoritmo Genético e uma abordagem aleatória (Baseline).
• Integração com IA Generativa: Geração de relatórios operacionais e Chatbot interativo para Q&A sobre a logística.
🛠️ Arquitetura e Tecnologias
O projeto foi construído em Python modularizado:
• tsp6.py: O arquivo principal. Gerencia a simulação visual (Pygame), o loop do Algoritmo Genético e a chamada para serviços de IA.
• genetic_algorithm.py: O "cérebro" matemático. Contém:
    ◦ order_crossover: Operador de cruzamento que preserva a ordem e evita duplicatas.
    ◦ mutate: Operador de mutação por troca (Swap).
    ◦ calculate_fitness_path: Função de avaliação que considera distância e penalidades de prioridade.
• benchmark_att48_2.py: Dataset base contendo coordenadas de 48 capitais (att48), adaptado com pesos de carga e níveis de prioridade.
• llm_service.py: (Módulo de integração) Conecta a solução matemática à API de IA (OpenAI/Gemini) para interpretação de dados.
• Testes Unitários: Scripts para validação de lógica (test_crossover.py, test_geometry.py, verify_penalties.py).
⚙️ Instalação e Execução
Pré-requisitos
• Python 3.8+
• Bibliotecas: pygame, matplotlib, openai (ou SDK equivalente)
pip install pygame matplotlib openai numpy
Como Rodar
1. Validar a Lógica (Opcional, mas recomendado): Execute os testes unitários para garantir que os operadores genéticos estão íntegros.
2. Iniciar a Simulação:
3. Controles da Interface:
    ◦ Acompanhe a evolução visual das linhas coloridas (cada cor é um veículo).
    ◦ Pressione G para gerar o relatório da viagem via LLM (salvo em relatorio_viagem.txt).
    ◦ Feche a janela gráfica para entrar no Modo Chatbot no terminal.
🧠 Detalhes Técnicos da Heurística
1. Representação do Genoma
Cada indivíduo é uma lista de índices representando a ordem de visita das cidades.
2. Função de Fitness e Penalidades
A pontuação de uma rota não é apenas a distância Euclidiana. O sistema aplica penalidades se:
• O caminho cruza zonas de exclusão (simulado geometricamente).
• Uma entrega normal é realizada enquanto existem entregas críticas pendentes na lista.
3. Tratamento de VRP (Vehicle Routing Problem)
Utilizamos uma abordagem de "Route-first, Cluster-second":
1. O GA encontra a melhor sequência topológica de visitas.
2. A função get_routes_with_capacity itera sobre essa sequência somando os pesos (att_48_cities_weights).
3. Quando a capacidade do veículo é atingida, o sistema força um retorno ao depósito e inicia um novo veículo (nova rota).
📊 Resultados e Performance
O sistema inclui um módulo de benchmark que compara a solução genética contra uma solução aleatória em tempo real.
• Improvement Metric: Exibido na tela como "IMPROVEMENT vs RANDOM", demonstrando a eficácia percentual da otimização.

--------------------------------------------------------------------------------
Autor: Hyggor Firmino
Curso: Pós-Graduação em Inteligência Artificial - FIAP