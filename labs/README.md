### 01_chatbot_langchain

**Problema a ser resolvido:** Construir um chatbot modular usando LangChain.
**Métricas de teste:** Precisão de resposta, tempo de resposta, cobertura de intents.
**Solução:** LangChain, OpenAI, Pydantic
**Resultado esperado:** Chatbot capaz de interagir de forma contextualizada com o usuário.

---

### 02_chatbot_memoria_longa

**Problema a ser resolvido:** Adicionar memória de longo prazo ao chatbot.
**Métricas de teste:** Retenção de contexto, coerência ao longo da conversa.
**Solução:** LangChain, ChromaDB, OpenAI, Pydantic
**Resultado esperado:** Chatbot com histórico de conversa persistente.

---

### 03_rag_basico

**Problema a ser resolvido:** Implementar um pipeline RAG básico.
**Métricas de teste:** Recall de contexto, precisão de respostas contextualizadas.
**Solução:** LangChain, ChromaDB, OpenAI
**Resultado esperado:** Sistema que utiliza RAG para enriquecer respostas.

---

### 04_rag_multidocumento

**Problema a ser resolvido:** RAG sobre múltiplos documentos heterogêneos.
**Métricas de teste:** Diversidade de fontes recuperadas, precisão.
**Solução:** LangChain, ChromaDB, OpenAI
**Resultado esperado:** Respostas com base em múltiplas fontes documentais.

---

### 05_agente_multitool

**Problema a ser resolvido:** Criar agente que orquestra múltiplas ferramentas.
**Métricas de teste:** Taxa de execução correta de ferramentas, autonomia do agente.
**Solução:** LangChain, OpenAI, Ferramentas customizadas
**Resultado esperado:** Agente que utiliza diversas APIs e funções sob demanda.

---

### 06_grafo_conhecimento_neo4j

**Problema a ser resolvido:** Construir e consultar um grafo de conhecimento em Neo4j.
**Métricas de teste:** Precisão nas consultas, tempo de execução de queries.
**Solução:** Neo4j, Cypher, LangChain, networkx
**Resultado esperado:** Base de conhecimento consultável via linguagem natural.

---

### 07_roteirizacao_docker

**Problema a ser resolvido:** Automatizar a orquestração de labs com Docker Compose.
**Métricas de teste:** Facilidade de setup, tempo de deploy.
**Solução:** Docker, Docker Compose
**Resultado esperado:** Ambientes prontos e replicáveis para experimentos.

---

### 08_integra_n8n_llm

**Problema a ser resolvido:** Orquestrar fluxos de automação com n8n integrando LLMs.
**Métricas de teste:** Automação de tarefas, tempo de processamento.
**Solução:** n8n, OpenAI, Webhooks
**Resultado esperado:** Workflows de IA totalmente automatizados.

---

### 09_agente_raciocinio_causal

**Problema a ser resolvido:** Prototipar agentes capazes de inferir causas e consequências.
**Métricas de teste:** Acurácia de inferência causal, explicabilidade.
**Solução:** OpenAI, LangChain, Raciocínio Causal
**Resultado esperado:** Respostas que explicitam cadeia causal de eventos.

---

### 10_grafo_social_networkx

**Problema a ser resolvido:** Modelar redes sociais sintéticas e analisar dinâmicas.
**Métricas de teste:** Métricas de centralidade, detecção de comunidades.
**Solução:** networkx, Pydantic, visualização com matplotlib
**Resultado esperado:** Simulação e análise de redes sociais.

---

### 11_lab_embeddings

**Problema a ser resolvido:** Gerar, visualizar e comparar embeddings.
**Métricas de teste:** Similaridade, redução de dimensionalidade, clustering.
**Solução:** OpenAI, ChromaDB, t-SNE, matplotlib
**Resultado esperado:** Visualização interativa de vetores de embeddings.

---

### 12_tool_agent_benchmark

**Problema a ser resolvido:** Benchmark entre diferentes arquiteturas de agentes com ferramentas.
**Métricas de teste:** Latência, cobertura, taxa de acerto na escolha de ferramentas.
**Solução:** LangChain, OpenAI, logging customizado
**Resultado esperado:** Relatório comparativo de arquiteturas.

---

### 13_lab_rag_vs_nativo

**Problema a ser resolvido:** Comparar respostas LLM nativas vs. RAG.
**Métricas de teste:** Satisfação do usuário, precisão de respostas.
**Solução:** OpenAI, LangChain, avaliação cega.
**Resultado esperado:** Relatório quantitativo e qualitativo.

---

### 14_agent_chain_asyncio

**Problema a ser resolvido:** Construir cadeias de agentes assíncronas.
**Métricas de teste:** Throughput, latência por tarefa.
**Solução:** asyncio, LangChain, OpenAI
**Resultado esperado:** Sistema multitarefa com resposta paralela.

---

### 15_orquestracao_multiagente

**Problema a ser resolvido:** Orquestrar agentes independentes em fluxos cooperativos.
**Métricas de teste:** Taxa de colaboração, eficiência global, conflitos.
**Solução:** LangChain, LangGraph, MCP, asyncio
**Resultado esperado:** Orquestração multiagente funcional.

---

### 16_rag_grafo

**Problema a ser resolvido:** RAG usando fontes de conhecimento em grafos (Neo4j).
**Métricas de teste:** Recuperação via grafo vs. vetorial, precisão contextual.
**Solução:** LangChain, Neo4j, Cypher
**Resultado esperado:** Respostas com evidências a partir de grafos.

---

### 17_benchmark_vectordbs

**Problema a ser resolvido:** Benchmark entre bancos vetoriais (ChromaDB, Pinecone etc).
**Métricas de teste:** Latência, recall, escalabilidade.
**Solução:** ChromaDB, outros vetoriais, scripts de teste.
**Resultado esperado:** Ranking comparativo de bases vetoriais.

---

### 18_pipelines_docker

**Problema a ser resolvido:** Padronizar deploy de pipelines IA via Docker Compose.
**Métricas de teste:** Reprodutibilidade, tempo de inicialização.
**Solução:** Docker, Compose, Makefile
**Resultado esperado:** Deploys automáticos e versionados.

---

### 19_grafana_monitoring_llm

**Problema a ser resolvido:** Monitorar desempenho de agentes com Grafana.
**Métricas de teste:** Métricas de uso, latência, falhas por endpoint.
**Solução:** Grafana, Prometheus, Docker
**Resultado esperado:** Dashboard de monitoramento em tempo real.

---

### 20_integra_langgraph_n8n

**Problema a ser resolvido:** Orquestrar fluxos multiagente em LangGraph disparados por n8n.
**Métricas de teste:** Automação ponta-a-ponta, latência total do fluxo.
**Solução:** LangGraph, n8n, webhooks
**Resultado esperado:** Workflows automatizados via agentes.

---

### 21_tool_plugins_openai

**Problema a ser resolvido:** Criar, registrar e testar ferramentas plugáveis no OpenAI Functions.
**Métricas de teste:** Facilidade de extensão, cobertura de funcionalidades.
**Solução:** OpenAI, Pydantic, FastAPI
**Resultado esperado:** Catálogo de plugins de ferramentas.

---

### 22_lab_memory_types

**Problema a ser resolvido:** Explorar tipos diferentes de memória (curta, longa, episódica, semântica).
**Métricas de teste:** Recuperação correta do tipo de memória, taxa de esquecimento.
**Solução:** LangChain, ChromaDB, Neo4j
**Resultado esperado:** Comparativo de técnicas de memória para agentes.

---

### 23_summarization_rag

**Problema a ser resolvido:** Experimentar sumarização assistida via RAG.
**Métricas de teste:** Qualidade de resumo, fidelidade ao texto original.
**Solução:** OpenAI, LangChain, ChromaDB
**Resultado esperado:** Resumos automáticos via consulta a bases.

---

### 24_pipeline_llm_schedule

**Problema a ser resolvido:** Orquestrar execuções programadas de LLMs.
**Métricas de teste:** Execução no tempo certo, confiabilidade do agendamento.
**Solução:** schedule, asyncio, LangChain
**Resultado esperado:** Execução automatizada baseada em horários.

---

### 25_notificacoes_eventos_ia

**Problema a ser resolvido:** Disparar notificações baseadas em eventos IA.
**Métricas de teste:** Taxa de entrega, latência, personalização.
**Solução:** n8n, OpenAI, webhooks
**Resultado esperado:** Sistema de alertas inteligentes.

---

### 26_agent_with_shared_utilities

**Problema a ser resolvido:** Garantir reutilização de código entre agentes via shared_utilities.
**Métricas de teste:** Redução de duplicidade, cobertura de testes.
**Solução:** Pydantic, shared_utilities
**Resultado esperado:** Modularidade máxima nos agentes.

---

### 27_lab_benchmark_langchain_vs_langgraph

**Problema a ser resolvido:** Comparar pipelines em LangChain vs. LangGraph.
**Métricas de teste:** Tempo de execução, facilidade de orquestração.
**Solução:** LangChain, LangGraph, scripts de benchmark
**Resultado esperado:** Relatório de performance e usabilidade.

---

### 28_simulacao_fluxo_rag

**Problema a ser resolvido:** Simular fluxo de consulta RAG ponta a ponta.
**Métricas de teste:** Precisão final, rastreabilidade do fluxo.
**Solução:** LangChain, OpenAI, ChromaDB
**Resultado esperado:** Simulação didática para onboarding de novos devs.

---

### 29_lab_mcp_architecture

**Problema a ser resolvido:** Implementar padrões Model-Context-Protocol.
**Métricas de teste:** Clareza de separação de funções, extensibilidade.
**Solução:** MCP, LangChain, OpenAI
**Resultado esperado:** Padrão MCP aplicado em agentes.

---

### 30_pipeline_neo4j_rag

**Problema a ser resolvido:** Recuperar e sintetizar informações de Neo4j via RAG.
**Métricas de teste:** Coerência da resposta, tempo de busca no grafo.
**Solução:** Neo4j, Cypher, LangChain
**Resultado esperado:** Consulta híbrida vetorial + grafo.

---

### 31_lab_rag_narrativas

**Problema a ser resolvido:** Geração de narrativas e storytelling com base em dados RAG.
**Métricas de teste:** Coesão do texto, criatividade, fidelidade aos dados.
**Solução:** OpenAI, LangChain, ChromaDB
**Resultado esperado:** Histórias baseadas em fatos consultados.

---

### 32_agente_autonomo_execucao_tasks

**Problema a ser resolvido:** Criar agente capaz de planejar e executar tasks autonomamente.
**Métricas de teste:** Taxa de sucesso de execução, autonomia real.
**Solução:** LangChain, asyncio, schedule, OpenAI
**Resultado esperado:** Agente proativo e autônomo funcional.

---

### 33_lab_knowledge_tracing

**Problema a ser resolvido:** Rastrear evolução de conhecimento em fluxos conversacionais.
**Métricas de teste:** Precisão do tracing, adaptabilidade do agente.
**Solução:** LangChain, Neo4j, networkx
**Resultado esperado:** Relatório de progresso de aprendizado.

---

### 34_grafo_explicabilidade

**Problema a ser resolvido:** Usar grafos para gerar explicações (XAI).
**Métricas de teste:** Clareza da explicação, rastreabilidade.
**Solução:** Neo4j, Cypher, LangChain
**Resultado esperado:** Explicações visuais baseadas em grafos.

---

### 35_lab_chatops

**Problema a ser resolvido:** Orquestrar comandos de DevOps via chat.
**Métricas de teste:** Tempo de resposta, taxa de sucesso dos comandos.
**Solução:** n8n, Docker, OpenAI
**Resultado esperado:** Operações de infra automatizadas via chat.

---

### 36_lab_lingua_natural_cypher

**Problema a ser resolvido:** Converter perguntas em linguagem natural para consultas Cypher.
**Métricas de teste:** Acurácia da conversão, cobertura de queries.
**Solução:** OpenAI, LangChain, Neo4j
**Resultado esperado:** NLP → Cypher funcional.

---

### 37_orquestrador_de_experimentos

**Problema a ser resolvido:** Orquestrar execução automatizada de múltiplos labs para experimentos.
**Métricas de teste:** Eficiência da execução em lote, logs, comparabilidade.
**Solução:** Docker Compose, Makefile, scripts Python
**Resultado esperado:** Execução e comparação automatizada de experimentos.

---

### 38_lab_simulacao_dialogos

**Problema a ser resolvido:** Simular conversas multiagente para testar raciocínio coletivo.
**Métricas de teste:** Diversidade de respostas, colaboração, criatividade.
**Solução:** LangChain, LangGraph, asyncio
**Resultado esperado:** Simulação de debates e brainstorms IA.

---

### 39_lab_pipeline_dados_n8n

**Problema a ser resolvido:** Construir pipelines de dados complexos com n8n e LLMs.
**Métricas de teste:** Capacidade de integração, tempo de processamento.
**Solução:** n8n, OpenAI, ChromaDB
**Resultado esperado:** Pipelines ETL inteligentes e automatizados.

---

### 40_lab_data_lineage_grafos

**Problema a ser resolvido:** Rastrear linhagem de dados usando grafos.
**Métricas de teste:** Completude do lineage, facilidade de auditoria.
**Solução:** Neo4j, Cypher, networkx
**Resultado esperado:** Visualização e análise de lineage.

---

### 41_lab_pipelines_async

**Problema a ser resolvido:** Construir pipelines de IA totalmente assíncronos.
**Métricas de teste:** Throughput, consumo de recursos.
**Solução:** asyncio, LangChain, OpenAI
**Resultado esperado:** Pipelines performáticos para alta concorrência.

---

### 42_lab_memoria_episodica

**Problema a ser resolvido:** Simular e avaliar memória episódica em agentes IA.
**Métricas de teste:** Recuperação de eventos, fidelidade temporal.
**Solução:** LangChain, ChromaDB, OpenAI
**Resultado esperado:** Agente que lembra experiências passadas.

---

### 43_lab_microservicos_ia

**Problema a ser resolvido:** Prototipar microserviços IA plugáveis para orquestração.
**Métricas de teste:** Facilidade de integração, escalabilidade, resiliência.
**Solução:** FastAPI, Docker, LangChain
**Resultado esperado:** Microserviços IA interconectados.

---

### 44_lab_analise_logs_agentes

**Problema a ser resolvido:** Coletar, analisar e visualizar logs de execução de agentes.
**Métricas de teste:** Detecção de falhas, insights de performance.
**Solução:** logging, Grafana, Python
**Resultado esperado:** Dashboard analítico de agentes.

---

### 45_lab_exp_rag_zero-shot

**Problema a ser resolvido:** Testar performance RAG em queries zero-shot.
**Métricas de teste:** Precisão, recall, latência.
**Solução:** OpenAI, LangChain, ChromaDB
**Resultado esperado:** Avaliação de generalização RAG.

---

### 46_lab_pipeline_documentos

**Problema a ser resolvido:** Criar pipelines automáticos de ingestão e consulta de documentos.
**Métricas de teste:** Taxa de ingestão, precisão de resposta.
**Solução:** LangChain, ChromaDB, n8n
**Resultado esperado:** Ingestão automatizada + Q&A.

---

### 47_lab_chat_com_grafos

**Problema a ser resolvido:** Chatbot com raciocínio baseado em grafos de conhecimento.
**Métricas de teste:** Relevância, profundidade das respostas.
**Solução:** Neo4j, LangChain, OpenAI
**Resultado esperado:** Conversa com base em relações de conhecimento.

---

### 48_lab_agent_explainability

**Problema a ser resolvido:** Explicabilidade em decisões e raciocínios de agentes IA.
**Métricas de teste:** Clareza, satisfação do usuário.
**Solução:** OpenAI, LangChain, visualização
**Resultado esperado:** Sistema XAI para agentes.

---

### 49_lab_finetuning_prompts

**Problema a ser resolvido:** Testar o impacto de diferentes prompts nos resultados dos LLMs.
**Métricas de teste:** Métricas de avaliação automática/humana, robustez.
**Solução:** OpenAI, LangChain, scripts de teste
**Resultado esperado:** Guia de melhores práticas de prompting.

---

### 50_lab_tracing_fluxos

**Problema a ser resolvido:** Implementar e avaliar tracing e explainability em pipelines complexos.
**Métricas de teste:** Facilidade de debugging, rastreabilidade ponta a ponta.
**Solução:** LangChain, LangGraph, logging, tracing
**Resultado esperado:** Pipelines totalmente rastreáveis e auditáveis.

---

### 51_classificacao_emails_spam

**Problema a ser resolvido:** Classificar e-mails como spam ou não usando IA.
**Métricas de teste:** Precision, recall, F1-score em conjunto de e-mails rotulados.
**Solução:** OpenAI, sklearn, Pydantic
**Resultado esperado:** API de classificação de e-mails com relatório de métricas.

---

### 52_extracao_dados_pdf

**Problema a ser resolvido:** Extrair e estruturar dados de PDFs variados (notas fiscais, contratos, artigos).
**Métricas de teste:** Taxa de extração correta, cobertura de campos.
**Solução:** pdfplumber, OpenAI, Pydantic
**Resultado esperado:** Dados limpos em JSON a partir de PDFs reais.

---

### 53_assistente_redacao

**Problema a ser resolvido:** Auxiliar alunos na redação de textos e correção automática.
**Métricas de teste:** Nota média atribuída vs nota humana, satisfação do usuário.
**Solução:** OpenAI, LangChain
**Resultado esperado:** Plataforma de correção automatizada de redação.

---

### 54_detecta_fraudes_transacoes

**Problema a ser resolvido:** Detectar transações financeiras fraudulentas usando machine learning.
**Métricas de teste:** ROC AUC, precision, recall, taxa de falsos positivos.
**Solução:** sklearn, XGBoost, ChromaDB
**Resultado esperado:** Modelo de detecção de fraudes com painel de análise.

---

### 55_chatbot_saude_mental

**Problema a ser resolvido:** Chatbot que identifica sinais de sofrimento psicológico e orienta o usuário.
**Métricas de teste:** Detecção correta, tempo de resposta, avaliações dos usuários.
**Solução:** OpenAI, LangChain, scripts de avaliação ética
**Resultado esperado:** Assistente empático para conversas sobre saúde mental.

---

### 56_recomendacao_produtos

**Problema a ser resolvido:** Sistema de recomendação personalizado para e-commerce.
**Métricas de teste:** CTR, precisão, recall, taxa de conversão.
**Solução:** sklearn, ChromaDB, OpenAI
**Resultado esperado:** Recomendações automáticas de produtos para usuários reais.

---

### 57_sintese_voz_texto

**Problema a ser resolvido:** Transformar texto em fala realista em múltiplos idiomas.
**Métricas de teste:** Clareza, naturalidade, acurácia do idioma.
**Solução:** TTS, OpenAI, scripts Python
**Resultado esperado:** Áudio gerado a partir de qualquer texto.

---

### 58_anomalias_iot

**Problema a ser resolvido:** Detectar anomalias em dados de sensores IoT (temperatura, pressão, etc.).
**Métricas de teste:** Precisão na detecção, taxa de alarmes falsos.
**Solução:** sklearn, Pandas, OpenAI
**Resultado esperado:** Alerta automático para falhas em tempo real.

---

### 59_resumo_juridico

**Problema a ser resolvido:** Gerar resumos automáticos de decisões judiciais.
**Métricas de teste:** Sumarização, cobertura dos pontos principais, avaliação de juristas.
**Solução:** OpenAI, LangChain
**Resultado esperado:** Resumos claros e auditáveis de acórdãos.

---

### 60_traducao_documentos_multilingue

**Problema a ser resolvido:** Traduzir documentos longos entre vários idiomas automaticamente.
**Métricas de teste:** BLEU, satisfação do usuário, cobertura de idiomas.
**Solução:** OpenAI, DeepL, scripts Python
**Resultado esperado:** Documentos traduzidos com alta precisão.

---

### 61_monitoramento_reviews_online

**Problema a ser resolvido:** Monitorar menções/reviews de marcas em tempo real nas redes sociais.
**Métricas de teste:** Cobertura, tempo de detecção, análise de sentimento.
**Solução:** Twitter API, OpenAI, ChromaDB
**Resultado esperado:** Painel de menções e sentimentos de marca.

---

### 62_ocr_faturas_mensal

**Problema a ser resolvido:** Extrair dados de contas de energia/água usando OCR.
**Métricas de teste:** Precisão, recall, automação do fluxo.
**Solução:** Tesseract OCR, OpenAI, Pandas
**Resultado esperado:** Base de dados estruturada de contas mensais.

---

### 63_suporte_automatico_ia

**Problema a ser resolvido:** Automatizar respostas para um helpdesk de TI.
**Métricas de teste:** Taxa de resolução automática, NPS, tempo de resposta.
**Solução:** OpenAI, LangChain, integrações HelpDesk
**Resultado esperado:** Suporte automático para chamados comuns.

---

### 64_otimizacao_escala_funcionarios

**Problema a ser resolvido:** Otimizar escalas de funcionários considerando preferências e restrições.
**Métricas de teste:** Satisfação, cobertura das demandas, número de conflitos.
**Solução:** Google OR-Tools, OpenAI, Pydantic
**Resultado esperado:** Escalas otimizadas e adaptáveis.

---

### 65_analise_sentimento_clientes

**Problema a ser resolvido:** Analisar sentimento de clientes em pesquisas NPS e SAC.
**Métricas de teste:** Acurácia na classificação de sentimento, insights gerados.
**Solução:** OpenAI, sklearn
**Resultado esperado:** Relatório de sentimentos com recomendações.

---

### 66_predicao_demanda_vendas

**Problema a ser resolvido:** Prever demanda de vendas para o próximo mês.
**Métricas de teste:** RMSE, MAPE, acurácia das previsões.
**Solução:** Prophet, sklearn, Pandas
**Resultado esperado:** Previsões automatizadas de demanda.

---

### 67_deteccao_objetos_imagens

**Problema a ser resolvido:** Detectar objetos (produtos, pessoas, placas) em imagens.
**Métricas de teste:** IoU, recall, precisão de detecção.
**Solução:** YOLOv8, OpenAI Vision, scripts Python
**Resultado esperado:** Detecção automática e visualização dos objetos.

---

### 68_assistente_financeiro_pessoal

**Problema a ser resolvido:** Automatizar organização e insights para finanças pessoais.
**Métricas de teste:** Satisfação do usuário, taxa de economia, número de insights úteis.
**Solução:** OpenAI, LangChain, Dash
**Resultado esperado:** Painel de controle e alertas financeiros inteligentes.

---

### 69_analisador_texto_plagios

**Problema a ser resolvido:** Detectar plágios e similaridades em textos acadêmicos.
**Métricas de teste:** Acurácia, recall, false positives.
**Solução:** ChromaDB, OpenAI, sklearn
**Resultado esperado:** Relatório automático de similaridade/plágio.

---

### 70_extracao_dados_websites

**Problema a ser resolvido:** Coletar e estruturar dados de diferentes sites automaticamente.
**Métricas de teste:** Cobertura, tempo de scraping, qualidade dos dados.
**Solução:** BeautifulSoup, Selenium, OpenAI
**Resultado esperado:** Base de dados de sites pronta para análise.

---

### 71_classificacao_documentos_juridicos

**Problema a ser resolvido:** Classificar automaticamente documentos jurídicos por categoria.
**Métricas de teste:** Precisão, recall, acurácia geral.
**Solução:** OpenAI, sklearn, Pydantic
**Resultado esperado:** Classificador pronto para advogados e escritórios.

---

### 72_chatbot_onboarding_rh

**Problema a ser resolvido:** Automatizar o onboarding de novos funcionários via chatbot.
**Métricas de teste:** Tempo médio de onboarding, satisfação, cobertura de informações.
**Solução:** OpenAI, LangChain, integrações RH
**Resultado esperado:** Processo de integração 100% digital e interativo.

---

### 73_sintese_ata_reuniao

**Problema a ser resolvido:** Gerar atas de reunião a partir de áudios/gravações.
**Métricas de teste:** Fidelidade, cobertura dos tópicos, precisão na transcrição.
**Solução:** OpenAI Whisper, LangChain
**Resultado esperado:** Ata automática pronta após a reunião.

---

### 74_predicao_churn_clientes

**Problema a ser resolvido:** Prever quais clientes estão prestes a cancelar serviços.
**Métricas de teste:** AUC, precisão, recall, taxa de churn real.
**Solução:** sklearn, XGBoost, Pandas
**Resultado esperado:** Alerta automático para retenção de clientes.

---

### 75_otimizacao_rotas_entrega

**Problema a ser resolvido:** Otimizar rotas de entregas urbanas para logística.
**Métricas de teste:** Distância total percorrida, tempo, custo de rota.
**Solução:** OR-Tools, networkx, OpenAI
**Resultado esperado:** Rotas otimizadas diariamente para entregadores.

---

### 76_recomendacao_conteudo_educacional

**Problema a ser resolvido:** Recomendar cursos e conteúdos para alunos baseado em performance.
**Métricas de teste:** Engajamento, precisão da recomendação, avaliações dos alunos.
**Solução:** sklearn, ChromaDB, OpenAI
**Resultado esperado:** Recomendações adaptativas em plataformas educacionais.

---

### 77_chatbot_reclamacoes_publicas

**Problema a ser resolvido:** Chatbot para receber, categorizar e priorizar reclamações do cidadão (prefeitura, órgãos públicos).
**Métricas de teste:** Tempo de resposta, taxa de resolução, priorização correta.
**Solução:** OpenAI, LangChain, Dash
**Resultado esperado:** Atendimento automático para serviços públicos.

---

### 78_detecta_fake_news

**Problema a ser resolvido:** Identificar fake news em notícias compartilhadas nas redes.
**Métricas de teste:** Precisão, recall, avaliação de especialistas.
**Solução:** OpenAI, ChromaDB, scripts Python
**Resultado esperado:** Classificador de notícias falsas/verdadeiras.

---

### 79_analise_imagem_medica

**Problema a ser resolvido:** Analisar imagens de raio-X ou tomografias para identificar anomalias.
**Métricas de teste:** Sensibilidade, especificidade, recall, precisão.
**Solução:** OpenAI Vision, PyTorch, scikit-learn
**Resultado esperado:** Detecção assistida de doenças em imagens médicas.

---

### 80_lab_analise_credito

**Problema a ser resolvido:** Prever risco de crédito para concessão de empréstimos.
**Métricas de teste:** AUC, precisão, recall.
**Solução:** sklearn, XGBoost, Pandas
**Resultado esperado:** Score de risco automático e visualização.

---

### 81_assistente_analise_curriculos

**Problema a ser resolvido:** Avaliar e ranquear currículos recebidos em processos seletivos.
**Métricas de teste:** Aderência da seleção, feedback de RH, velocidade de triagem.
**Solução:** OpenAI, ChromaDB, LangChain
**Resultado esperado:** Ranqueamento e análise automática de candidatos.

---

### 82_predicao_estoque_varejo

**Problema a ser resolvido:** Prever necessidade de estoque para minimizar rupturas e desperdício.
**Métricas de teste:** MAPE, RMSE, taxa de ruptura.
**Solução:** Prophet, sklearn, Pandas
**Resultado esperado:** Sugestão automática de reposição de estoque.

---

### 83_avaliacao_exames_linguas

**Problema a ser resolvido:** Corrigir e dar feedback automático em exames de idiomas (inglês, espanhol).
**Métricas de teste:** Concordância com avaliador humano, precisão.
**Solução:** OpenAI, LangChain
**Resultado esperado:** Correção automática e feedback personalizado.

---

### 84_categorizacao_automatica_videos

**Problema a ser resolvido:** Classificar vídeos em categorias automaticamente (esporte, notícia, educação).
**Métricas de teste:** Precisão, recall, cobertura de categorias.
**Solução:** OpenAI Vision, sklearn, scripts Python
**Resultado esperado:** Categorias sugeridas para vídeos recebidos.

---

### 85_gestor_automatizado_agenda

**Problema a ser resolvido:** Gerenciar compromissos e sugerir horários automáticos.
**Métricas de teste:** Taxa de conflitos, satisfação dos usuários, precisão nas sugestões.
**Solução:** OpenAI, LangChain, calendar API
**Resultado esperado:** Agenda pessoal inteligente.

---

### 86_deteccao_doencas_plantas

**Problema a ser resolvido:** Detectar doenças em plantas a partir de fotos de folhas.
**Métricas de teste:** Precisão, recall, cobertura de doenças detectadas.
**Solução:** OpenAI Vision, sklearn, scripts Python
**Resultado esperado:** Diagnóstico automático de lavouras.

---

### 87_avaliacao_projetos_engenharia

**Problema a ser resolvido:** Avaliar automaticamente projetos de engenharia (plantas, diagramas, orçamentos).
**Métricas de teste:** Taxa de detecção de inconsistências, satisfação dos engenheiros.
**Solução:** OpenAI, scripts Python, ChromaDB
**Resultado esperado:** Feedback automático em projetos.

---

### 88_assistente_pesquisa_cientifica

**Problema a ser resolvido:** Auxiliar pesquisadores a encontrar e resumir artigos científicos.
**Métricas de teste:** Cobertura de busca, qualidade dos resumos, tempo economizado.
**Solução:** OpenAI, LangChain, ChromaDB
**Resultado esperado:** Assistente virtual de pesquisa acadêmica.

---

### 89_analise_video_aulas

**Problema a ser resolvido:** Analisar videoaulas e gerar resumos, tópicos-chave e perguntas.
**Métricas de teste:** Cobertura, qualidade dos resumos, relevância das perguntas.
**Solução:** OpenAI, Whisper, LangChain
**Resultado esperado:** Resumos automáticos e quizzes de videoaulas.

---

### 90_classificacao_transacoes_blockchain

**Problema a ser resolvido:** Classificar transações blockchain como suspeitas ou normais.
**Métricas de teste:** Acurácia, recall, taxa de detecção de fraude.
**Solução:** sklearn, OpenAI, scripts Python
**Resultado esperado:** Alerta para transações atípicas em tempo real.

---

### 91_analise_riscos_projetos

**Problema a ser resolvido:** Avaliar riscos em projetos (TI, engenharia, pesquisa).
**Métricas de teste:** Taxa de acerto das previsões, satisfação dos gestores.
**Solução:** OpenAI, LangChain, scripts Python
**Resultado esperado:** Relatório de riscos automatizado.

---

### 92_assistente_regulamentos_instituicao

**Problema a ser resolvido:** Responder dúvidas sobre regulamentos internos de empresas/universidades.
**Métricas de teste:** Cobertura de respostas corretas, satisfação dos colaboradores.
**Solução:** OpenAI, LangChain, ChromaDB
**Resultado esperado:** Assistente institucional de regulação e compliance.

---

### 93_predicao_acidentes_trabalho

**Problema a ser resolvido:** Prever risco de acidentes de trabalho em diferentes setores.
**Métricas de teste:** Recall, precisão, taxa de acerto em histórico.
**Solução:** sklearn, Pandas, OpenAI
**Resultado esperado:** Alertas e plano preventivo automatizado.

---

### 94_detecta_lavagem_dinheiro

**Problema a ser resolvido:** Detectar padrões de lavagem de dinheiro em transações financeiras.
**Métricas de teste:** Precisão, recall, avaliação de especialistas.
**Solução:** sklearn, OpenAI, Pandas
**Resultado esperado:** Detecção e alerta automático para bancos e fintechs.

---

### 95_analise_documentos_midiaticos

**Problema a ser resolvido:** Analisar grandes volumes de notícias e identificar tendências.
**Métricas de teste:** Cobertura, precisão das tendências detectadas.
**Solução:** OpenAI, ChromaDB, scripts Python
**Resultado esperado:** Relatórios automáticos para mídia.

---

### 96_automatizacao_resumos_projetos

**Problema a ser resolvido:** Gerar resumos automáticos de relatórios de projeto.
**Métricas de teste:** Fidelidade, cobertura, clareza dos resumos.
**Solução:** OpenAI, LangChain
**Resultado esperado:** Resumo automático para gestores e clientes.

---

### 97_analise_energia_predios

**Problema a ser resolvido:** Analisar consumo de energia em prédios e sugerir otimizações.
**Métricas de teste:** Economia de energia, precisão das sugestões.
**Solução:** Pandas, sklearn, OpenAI
**Resultado esperado:** Relatório de economia energética.

---

### 98_lab_roteirizacao_turismo

**Problema a ser resolvido:** Criar roteiros turísticos personalizados com IA.
**Métricas de teste:** Satisfação do usuário, adequação das sugestões.
**Solução:** OpenAI, LangChain, integrações APIs turismo
**Resultado esperado:** Roteiro automático e personalizado para cada viajante.

---

### 99_avaliacao_qualidade_software

**Problema a ser resolvido:** Avaliar qualidade de código-fonte e sugerir melhorias.
**Métricas de teste:** Cobertura de testes, número de sugestões aceitas.
**Solução:** SonarQube, OpenAI, scripts Python
**Resultado esperado:** Relatório automatizado de qualidade de software.

---

### 100_lab_prospecao_clientes

**Problema a ser resolvido:** Automatizar prospecção de clientes via análise de dados abertos (LinkedIn, redes).
**Métricas de teste:** Leads gerados, conversão, tempo de qualificação.
**Solução:** Selenium, OpenAI, ChromaDB
**Resultado esperado:** Lista qualificada de potenciais clientes.

---
