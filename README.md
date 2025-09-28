# 👗 Dashboard de Vendas - Loja de Roupas

Um dashboard interativo e elegante desenvolvido em Streamlit para análise completa de vendas de uma loja de roupas, com identidade visual feminina e moderna.

## ✨ Características

### 🎨 Design Feminino
- Paleta de cores em tons de rosa e roxo
- Gradientes suaves e elegantes
- Ícones temáticos de moda
- Interface intuitiva e moderna

### 📊 KPIs Principais
- **Receita Total**: Valor total das vendas
- **Ticket Médio**: Valor médio por venda
- **Total de Vendas**: Número de transações
- **Clientes Únicos**: Quantidade de clientes distintos
- **Desconto Médio**: Percentual médio de desconto aplicado
- **Avaliação Média**: Satisfação dos clientes
- **Produtos Vendidos**: Diversidade de produtos
- **Itens Vendidos**: Quantidade total de peças

### 📈 Análises Disponíveis
- **Evolução Temporal**: Diária, semanal, mensal e trimestral
- **Análise de Clientes**: Ciclo de vida e faixa etária
- **Análise de Produtos**: Top produtos e categorias
- **Análise Geográfica**: Performance por estado
- **Performance dos Vendedores**: Ranking e métricas
- **Sazonalidade**: Padrões por dia da semana e mês

### 🎛️ Filtros Interativos
- **Período**: Seleção de data personalizada
- **Categorias**: Filtro por tipo de produto
- **Canais de Venda**: Online vs Loja Física
- **Estados**: Análise geográfica específica

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
git clone <url-do-repositorio>
cd visualizacao_dados
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o dashboard**
```bash
streamlit run dashboard_vendas.py
```

4. **Acesse no navegador**
   - O dashboard será aberto automaticamente em `http://localhost:8501`
   - Caso não abra automaticamente, acesse manualmente

## 📁 Estrutura do Projeto

```
visualizacao_dados/
├── dashboard_vendas.py          # Dashboard principal
├── requirements.txt             # Dependências do projeto
├── README.md                   # Este arquivo
├── dados/
│   └── base_vendas_sazonalidade_ajustada.csv  # Dados de vendas
└── Etapa_3_Bianca,_Lorena_e_Beatriz.ipynb     # Notebook de análise
```

## 📊 Dados Utilizados

O dashboard utiliza o arquivo `base_vendas_sazonalidade_ajustada.csv` que contém:
- Informações de vendas (ID, data, valor, quantidade)
- Dados do cliente (nome, sexo, idade, localização)
- Detalhes do produto (nome, categoria, tamanho, cor)
- Informações de venda (vendedor, canal, desconto, avaliação)

## 🎯 Funcionalidades Principais

### 1. **KPIs em Tempo Real**
- Métricas atualizadas conforme os filtros aplicados
- Cards visuais com destaque para valores importantes

### 2. **Análise Temporal Flexível**
- Visualização diária, semanal, mensal ou trimestral
- Gráficos de linha para acompanhar tendências

### 3. **Segmentação de Clientes**
- Classificação por ciclo de vida (Novo, Ativo, Recuperado, Abandonador)
- Análise por faixa etária
- Distribuição geográfica

### 4. **Performance de Produtos**
- Ranking dos produtos mais vendidos
- Análise por categoria
- Identificação de tendências

### 5. **Análise de Vendedores**
- Ranking por receita gerada
- Métricas de performance individual
- Avaliação média dos clientes

## 🎨 Personalização Visual

O dashboard utiliza uma paleta de cores feminina:
- **Rosa Principal**: `#ff9a9e`
- **Rosa Claro**: `#fecfef`
- **Roxo**: `#8b4a6b`
- **Roxo Claro**: `#6b3a4a`
- **Fundo**: Gradientes suaves em tons pastel

## 📱 Responsividade

O dashboard é totalmente responsivo e funciona bem em:
- 💻 Desktop
- 📱 Tablet
- 📱 Smartphone

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Criação de gráficos interativos
- **NumPy**: Computação numérica
- **Python**: Linguagem de programação

## 📈 Próximas Funcionalidades

- [ ] Exportação de relatórios em PDF
- [ ] Alertas automáticos para metas
- [ ] Comparação com períodos anteriores
- [ ] Análise de previsão de vendas
- [ ] Integração com APIs externas

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato através dos canais disponíveis.

---

💖 **Desenvolvido com amor para análise de vendas de moda**
