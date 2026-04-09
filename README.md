# Sistema de Gestão de Estoque (SGE) com Inteligência Artificial Integrada

Este repositório contém o código-fonte do protótipo avançado de um Sistema de Gestão de Estoque (SGE). O projeto propõe um núcleo de arquitetura monolítica focado em robustez e acurácia de transações, complementado de forma inovadora com agentes de Inteligência Artificial usando a stack do LangChain/LangGraph.

---

## 🏗 Arquitetura e Modelagem de Dados

A arquitetura central foi desenhada como um backend RESTful estruturado pelos princípios do Django ORM.

### Módulos Transacionais (Core)
- **`products`**: Gerencia a entidade primária. Encapsula estado de quantidade (`quantity`), chaves relacionais, e precificação (`selling_price` como tipo monetário seguro `DecimalField`).
- **`categories` & `brands`**: Entidades de tipificação. Separadas do app de produtos para assegurar um alto grau de normalização (1NF a 3NF), permitindo crescimento modular na árvore de hierarquias de produtos.
- **`inflows` / `outflows` / `suppliers`**: Reservados para processamento transacional de inventário em dupla-camada (Entrada de Notas e Faturamento), garantindo que um produto nunca tenha seu estoque alterado por "Edição Direta", mas sim pelo log contábil de transações — uma abordagem *event-driven* em nível de dados.

O banco de dados utilizado neste estágio de protótipo é o **SQLite3**, servindo sua função de ser portátil. Todo acesso ocorre abstraído via Django ORM.

---

## 🧠 Arquitetura do Agente de Inteligência Artificial (`ai_agent`)

Como grande diferencial, o projeto adota o **LangGraph** integrado à LLM `gpt-4o-mini` da OpenAI, implementando o padrão de *Tool-calling* acionado deterministicamente.

O sistema intercepta solicitações em linguagem natural (`/api/ai/chat/`) enviadas pelos usuários ou frontends. Ao invés da LLM realizar adivinhações cegas (alucinações), ela está estritamente restrita pela topologia de um Grafo de Estado (`StateGraph`):

### Fluxo Cognitivo (Topologia de Nós)
1. **Agent Node (`call_model`)**: Infere a intenção (`intent`) baseando-se no payload do usuário pareado ao array de mensagens transientes (`history`).
2. **Conditional Edge**: Analisa os artefatos de saída do Agent. Se o raciocínio exigir recuperação de dados cruciais, ele transiciona o pipeline em *hook* para os métodos da camada ORM.
3. **Tool Node (`ToolNode`)**: Executa abstrações isoladas contra a base. O resultado da SQL ou lógica em Python é serializado de volta em um `ToolMessage` e re-injetado na janela de contexto do LLM.

### Ferramentas Integradas do Agente (`tools.py`)
- **`check_product_stock(product_name)`**: Previne alucinações de estoque acionando uma query SQL com `__iexact`. Define de forma autônoma a sub-bandeira `status` operando por Thresholds (e.g., `< 10` como crítico).
- **`list_low_stock_products(threshold)`**: Evita degradações de performance (N+1 Queries) usando o `select_related('category')`, entregando um dump formatado com todos os itens em nível crítico em uma única invocação.
- **`get_total_inventory_value()`**: Ignora complexidades in-memory no Python enviando à Engine do BD uma agregação profunda: `Product.objects.aggregate(total=Sum(F('quantity') * F('selling_price')))`, delegando ao SQL as sobrecargas de álgebra.

---

## 🛡️ Segurança e Decisões de Design

1. **Gestão de Segredos**: `SECRET_KEY`, `DEBUG` e credenciais LLM (`OPENAI_API_KEY`) foram rigorosamente injetadas por intermédio do `.env` suportado pelo pacote `python-dotenv`.
2. **Resiliência a Parsing**: O payload de entrada em `/api/ai/chat/` é severamente validado. O array dinâmico `history` passa por checagem garantindo tipagem canônica nativa para o LangChain (`role` e `content`).
3. **Ofuscação de Erros 500**: Em falhas severas de ORM ou requisição LLM, o backend ofusca o Stack-Trace do usuário utilizando instâncias próprias do `logger`, reportando ao client-side um erro genérico mapeado (Status Code 500) a fim de prevenir vazamento topológico (*Information Disclosure*).
4. **Política CORS e de Permissão**: Em conformidade com o REST Framework (`DRF`), a permissão para requests na API flutua entre `AllowAny` (para depuração em ambientes onde `DEBUG=True`) e `IsAuthenticated` por padrão.

---

## 🚀 Como fazer setup e Instanciação Local

Desenvolvedores e validadores devem garantir a presença do `python >= 3.10`.

1. **Faça o clone e configure o contexto isolado:**
   ```bash
   git clone <repo_url> SGE_Project
   cd SGE_Project
   python -m venv venv
   # Ative a venv:
   # No Windows: .\venv\Scripts\activate
   # No Linux/Mac: source venv/bin/activate
   ```

2. **Instale a árvore de exigências sistêmicas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Injete as Variáveis de Ambiente:**
   Crie um arquivo `.env` puro na raiz do diretório e insira:
   ```env
   DJANGO_SECRET_KEY=chave-super-secreta
   DJANGO_DEBUG=True
   OPENAI_API_KEY=sua-chave-openai-aqui
   ```

4. **Prepare o Banco de Relacionamentos e Polule-o:**
   ```bash
   python manage.py migrate
   python seed.py
   ```

5. **Acompanhe os Jobs:**
   ```bash
   python manage.py runserver
   ```
   > Faça uma requisição de Teste (exemplo):
   > ```bash
   > curl -X POST http://127.0.0.1:8000/api/ai/chat/ -H "Content-Type: application/json" -d "{\"message\": \"Qual o estoque do Teclado?\"}"
   > ```
