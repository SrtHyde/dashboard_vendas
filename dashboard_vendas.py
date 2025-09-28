import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta
import warnings
from scipy.stats import norm
warnings.filterwarnings('ignore')

# =============================================================================
# PALETA DE CORES FEMININA - IDENTIDADE VISUAL
# =============================================================================

# Cores principais
ROSA_PRINCIPAL = '#ff9a9e'      # Rosa vibrante - cor principal do tema
ROSA_CLARO = '#fecfef'          # Rosa suave - gradientes e fundos
ROSA_PASTEL = '#ffeef8'         # Rosa pastel - fundos claros
ROSA_ESCURO = '#ff8a8e'         # Rosa escuro - hover effects

# Cores roxas
ROXO_PRINCIPAL = '#8b4a6b'      # Roxo principal - textos e títulos
ROXO_CLARO = '#6b3a4a'          # Roxo claro - textos secundários
ROXO_PASTEL = '#f8e8f5'         # Roxo pastel - fundos suaves
ROXO_ESCURO = '#e8d5e8'         # Roxo escuro - elementos de apoio
ROXO_ESCURO_2 = '#d4a5c7'       # Roxo escuro 2 - gradientes
ROXO_MEDIO = '#a5698a'          # Roxo médio - elementos intermediários
ROXO_SUAVE = '#f0d6e8'          # Roxo suave - fundos claros
ROXO_INTENSO = '#7a3d5f'        # Roxo intenso - destaques
ROXO_ESCURO_3 = '#c199b8'       # Roxo escuro 3 - variações
ROXO_CLARO_2 = '#9d6b85'        # Roxo claro 2 - textos alternativos

# Cores neutras
BRANCO = '#ffffff'              # Branco puro - fundos e contrastes
PRETO = '#000000'               # Preto - textos principais
CINZA_CLARO = '#666666'         # Cinza claro - placeholders
CINZA_MEDIO = '#cccccc'         # Cinza médio - bordas sutis

# Cores de status
VERDE = '#28a745'               # Verde - indicadores positivos
VERMELHO = '#dc3545'            # Vermelho - indicadores negativos
AZUL = '#007bff'                # Azul - links e informações
AMARELO = '#ffc107'             # Amarelo - avisos e destaques

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas - Loja de Roupas",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para identidade visual feminina
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {ROSA_PRINCIPAL} 0%, {ROSA_CLARO} 50%, {ROSA_CLARO} 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 154, 158, 0.3);
    }}
    
    .main-header h1 {{
        color: {ROXO_PRINCIPAL};
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(139, 74, 107, 0.3);
    }}
    
    .main-header p {{
        color: {ROXO_CLARO};
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {ROSA_PASTEL} 0%, {ROXO_PASTEL} 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid {ROSA_PRINCIPAL};
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.2);
        margin-bottom: 1rem;
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {ROXO_PRINCIPAL};
        margin: 0;
    }}
    
    .metric-label {{
        font-size: 1rem;
        color: {ROXO_CLARO};
        margin: 0;
        font-weight: 500;
    }}
    
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, {ROXO_ESCURO_3} 0%, {ROXO_ESCURO_3} 100%);
        color: {ROXO_PRINCIPAL};
    }}
    
    .stSelectbox > div > div {{
        background-color: {BRANCO};
        border: 2px solid {ROSA_PRINCIPAL};
        border-radius: 10px;
        color: {ROXO_PRINCIPAL};
    }}
    
    .stSelectbox > div > div > div {{
        color: {ROXO_PRINCIPAL} !important;
        font-weight: 600;
    }}
    
    .stMultiSelect > div > div {{
        background-color: {BRANCO};
        border: 2px solid {ROSA_PRINCIPAL};
        border-radius: 10px;
        color: {ROXO_PRINCIPAL};
    }}
    
    .stMultiSelect > div > div > div {{
        color: {ROXO_PRINCIPAL} !important;
        font-weight: 600;
    }}
    
    .stDateInput > div > div {{
        background-color: {BRANCO};
        border: 2px solid {ROSA_PRINCIPAL};
        border-radius: 10px;
        color: {ROXO_PRINCIPAL};
    }}
    
    .stDateInput > div > div > input {{
        color: {PRETO} !important;
        font-weight: 600;
    }}
    
    .stDateInput > div > div > input::placeholder {{
        color: {ROXO_CLARO} !important;
        opacity: 1;
        font-weight: 500;
    }}
    
    .stDateInput > div > div > input[value] {{
        color: {PRETO} !important;
        font-weight: 600;
    }}
    
    .stDateInput > div > div > div {{
        color: {PRETO} !important;
        font-weight: 600;
    }}
    
    /* =============================================================================
       REGRAS DE ALTA ESPECIFICIDADE PARA O FILTRO DE DATA NA SIDEBAR
       ============================================================================= */
    
    /* Alvo: O container do input de data DENTRO da sidebar */
    section[data-testid="stSidebar"] .stDateInput > div > div {{
        background-color: {BRANCO};
        border: 2px solid {ROSA_PRINCIPAL};
        border-radius: 10px;
    }}
    
    /* Alvo: O rótulo "Período" DENTRO da sidebar */
    section[data-testid="stSidebar"] .stDateInput label {{
        color: {ROXO_PRINCIPAL} !important;
        font-weight: 600;
    }}
    
    /* Alvo: O CAMPO DE TEXTO do input de data DENTRO da sidebar */
    section[data-testid="stSidebar"] .stDateInput input {{
        color: {PRETO} !important;
        font-weight: 600;
    }}
    
    /* Alvo: O placeholder DENTRO da sidebar */
    section[data-testid="stSidebar"] .stDateInput input::placeholder {{
        color: {CINZA_CLARO} !important;
        opacity: 1;
    }}
    
    /* Alvo: O ícone de calendário DENTRO da sidebar */
    section[data-testid="stSidebar"] .stDateInput svg {{
        fill: {ROXO_PRINCIPAL};
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {ROSA_PRINCIPAL} 0%, {ROSA_CLARO} 100%);
        color: {ROXO_PRINCIPAL};
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, {ROSA_ESCURO} 0%, {ROSA_CLARO} 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
    }}
    
    .chart-container {{
        background: {BRANCO};
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.1);
        margin-bottom: 2rem;
    }}
    
    .section-title {{
        color: {ROXO_PRINCIPAL};
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 3px solid {ROSA_PRINCIPAL};
        padding-bottom: 0.5rem;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega e processa os dados de vendas"""
    try:
        df = pd.read_csv('dados/base_vendas_sazonalidade_ajustada.csv')
        
        # Converter Data_Venda para datetime
        df['Data_Venda'] = pd.to_datetime(df['Data_Venda'])
        
        # Criar colunas derivadas
        df['Valor_Total'] = df['Quantidade'] * df['Preço_Unitário']
        df['Valor_Com_Desconto'] = df['Valor_Total'] * (1 - df['Desconto (%)'] / 100)
        df['Ano'] = df['Data_Venda'].dt.year
        df['Mês'] = df['Data_Venda'].dt.month
        df['Dia'] = df['Data_Venda'].dt.day
        df['Dia_Semana'] = df['Data_Venda'].dt.day_name()
        df['Semana'] = df['Data_Venda'].dt.isocalendar().week
        df['Trimestre'] = df['Data_Venda'].dt.quarter
        
        # Classificação de clientes por ciclo de vida (simulada)
        np.random.seed(42)
        df['Ciclo_Vida'] = np.random.choice(['Novo', 'Ativo', 'Recuperado', 'Abandonador'], 
                                          size=len(df), 
                                          p=[0.2, 0.5, 0.2, 0.1])
        
        # Faixa etária
        df['Faixa_Etaria'] = pd.cut(df['Idade'], 
                                   bins=[0, 25, 35, 45, 55, 100], 
                                   labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Cria um card de métrica personalizado"""
    delta_html = ""
    if delta is not None:
        color = "#28a745" if delta_color == "normal" else "#dc3545"
        delta_html = f'<p style="color: {color}; font-size: 0.9rem; margin: 0;">{delta}</p>'
    
    return f"""
    <div class="metric-card">
        <p class="metric-label">{title}</p>
        <p class="metric-value">{value}</p>
        {delta_html}
    </div>
    """

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>👗 Dashboard de Vendas</h1>
        <p>Análise Completa da Performance da Loja de Roupas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    if df.empty:
        st.error("Não foi possível carregar os dados. Verifique se o arquivo existe.")
        return
    
    # Sidebar com filtros
    st.sidebar.markdown("## 🎛️ Filtros")
    
    # Filtro de data
    min_date = df['Data_Venda'].min().date()
    max_date = df['Data_Venda'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['Data_Venda'].dt.date >= start_date) & 
                        (df['Data_Venda'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    # Filtros adicionais
    sexos = st.sidebar.multiselect(
        "👫 Sexo",
        options=df['Sexo'].unique(),
        default=df['Sexo'].unique()
    )
    
    categorias = st.sidebar.multiselect(
        "👕 Categorias",
        options=df['Categoria'].unique(),
        default=df['Categoria'].unique()
    )
    
    canais = st.sidebar.multiselect(
        "🏪 Canais de Venda",
        options=df['Canal_Venda'].unique(),
        default=df['Canal_Venda'].unique()
    )
    
    estados = st.sidebar.multiselect(
        "🗺️ Estados",
        options=df['Estado'].unique(),
        default=df['Estado'].unique()
    )
    
    # Aplicar filtros
    df_filtered = df_filtered[
        (df_filtered['Sexo'].isin(sexos)) &
        (df_filtered['Categoria'].isin(categorias)) &
        (df_filtered['Canal_Venda'].isin(canais)) &
        (df_filtered['Estado'].isin(estados))
    ]
    
    # KPIs principais
    st.markdown('<h2 class="section-title">📊 KPIs Principais</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        receita_total = df_filtered['Valor_Com_Desconto'].sum()
        st.markdown(create_metric_card(
            "💰 Receita Total", 
            f"R$ {receita_total:,.2f}"
        ), unsafe_allow_html=True)
    
    with col2:
        ticket_medio = df_filtered['Valor_Com_Desconto'].mean()
        st.markdown(create_metric_card(
            "🎫 Ticket Médio", 
            f"R$ {ticket_medio:,.2f}"
        ), unsafe_allow_html=True)
    
    with col3:
        total_vendas = len(df_filtered)
        st.markdown(create_metric_card(
            "🛍️ Total de Vendas", 
            f"{total_vendas:,}"
        ), unsafe_allow_html=True)
    
    with col4:
        clientes_unicos = df_filtered['Cliente'].nunique()
        st.markdown(create_metric_card(
            "👥 Clientes Únicos", 
            f"{clientes_unicos:,}"
        ), unsafe_allow_html=True)
    
    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        desconto_medio = df_filtered['Desconto (%)'].mean()
        st.markdown(create_metric_card(
            "🏷️ Desconto Médio", 
            f"{desconto_medio:.1f}%"
        ), unsafe_allow_html=True)
    
    with col6:
        avaliacao_media = df_filtered['Avaliação (1-5)'].mean()
        st.markdown(create_metric_card(
            "⭐ Avaliação Média", 
            f"{avaliacao_media:.1f}"
        ), unsafe_allow_html=True)
    
    with col7:
        produtos_unicos = df_filtered['Produto'].nunique()
        st.markdown(create_metric_card(
            "👗 Produtos Vendidos", 
            f"{produtos_unicos:,}"
        ), unsafe_allow_html=True)
    
    with col8:
        quantidade_total = df_filtered['Quantidade'].sum()
        st.markdown(create_metric_card(
            "📦 Itens Vendidos", 
            f"{quantidade_total:,}"
        ), unsafe_allow_html=True)
    
    # Gráficos de evolução temporal
    st.markdown('<h2 class="section-title">📈 Evolução Temporal</h2>', unsafe_allow_html=True)
    
    # Seleção de período para análise temporal
    periodo_analise = st.selectbox(
        "📊 Período de Análise",
        ["Diário", "Semanal", "Mensal", "Trimestral"]
    )
    
    if periodo_analise == "Diário":
        df_temporal = df_filtered.groupby('Data_Venda').agg({
            'Valor_Com_Desconto': 'sum',
            'ID_Venda': 'count',
            'Cliente': 'nunique'
        }).reset_index()
        df_temporal.columns = ['Data', 'Receita', 'Vendas', 'Clientes']
    elif periodo_analise == "Semanal":
        df_temporal = df_filtered.groupby(['Ano', 'Semana']).agg({
            'Valor_Com_Desconto': 'sum',
            'ID_Venda': 'count',
            'Cliente': 'nunique'
        }).reset_index()
        df_temporal['Data'] = df_temporal['Ano'].astype(str) + '-W' + df_temporal['Semana'].astype(str)
        df_temporal = df_temporal[['Data', 'Valor_Com_Desconto', 'ID_Venda', 'Cliente']]
        df_temporal.columns = ['Data', 'Receita', 'Vendas', 'Clientes']
    elif periodo_analise == "Mensal":
        df_temporal = df_filtered.groupby(['Ano', 'Mês']).agg({
            'Valor_Com_Desconto': 'sum',
            'ID_Venda': 'count',
            'Cliente': 'nunique'
        }).reset_index()
        df_temporal['Data'] = df_temporal['Ano'].astype(str) + '-' + df_temporal['Mês'].astype(str).str.zfill(2)
        df_temporal = df_temporal[['Data', 'Valor_Com_Desconto', 'ID_Venda', 'Cliente']]
        df_temporal.columns = ['Data', 'Receita', 'Vendas', 'Clientes']
    else:  # Trimestral
        df_temporal = df_filtered.groupby(['Ano', 'Trimestre']).agg({
            'Valor_Com_Desconto': 'sum',
            'ID_Venda': 'count',
            'Cliente': 'nunique'
        }).reset_index()
        df_temporal['Data'] = df_temporal['Ano'].astype(str) + '-Q' + df_temporal['Trimestre'].astype(str)
        df_temporal = df_temporal[['Data', 'Valor_Com_Desconto', 'ID_Venda', 'Cliente']]
        df_temporal.columns = ['Data', 'Receita', 'Vendas', 'Clientes']
    
    # Gráfico de evolução da receita
    col1, col2 = st.columns(2)
    
    with col1:
        fig_receita = px.line(
            df_temporal, 
            x='Data', 
            y='Receita',
            title=f'💰 Evolução da Receita - {periodo_analise}',
            color_discrete_sequence=[ROSA_PRINCIPAL]
        )
        fig_receita.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO
        )
        st.plotly_chart(fig_receita, use_container_width=True)
    
    with col2:
        fig_vendas = px.line(
            df_temporal, 
            x='Data', 
            y='Vendas',
            title=f'🛍️ Evolução do Número de Vendas - {periodo_analise}',
            color_discrete_sequence=[ROSA_CLARO]
        )
        fig_vendas.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO
        )
        st.plotly_chart(fig_vendas, use_container_width=True)
    
    # Análise de clientes
    st.markdown('<h2 class="section-title">👥 Análise de Clientes</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por ciclo de vida - Gráfico de barras
        ciclo_vida_counts = df_filtered['Ciclo_Vida'].value_counts()
        fig_ciclo = px.bar(
            x=ciclo_vida_counts.index,
            y=ciclo_vida_counts.values,
            title='🔄 Distribuição por Ciclo de Vida',
            color_discrete_sequence=[ROSA_PRINCIPAL, ROXO_MEDIO, ROXO_ESCURO_2, ROXO_SUAVE]
        )
        fig_ciclo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO,
            xaxis_title="Ciclo de Vida",
            yaxis_title="Número de Clientes"
        )
        st.plotly_chart(fig_ciclo, use_container_width=True)
    
    with col2:
        # Distribuição por sexo - Gráfico de pizza com porcentagens
        sexo_counts = df_filtered['Sexo'].value_counts()
        sexo_percent = (sexo_counts / sexo_counts.sum() * 100).round(1)
        
        fig_sexo = px.pie(
            values=sexo_counts.values,
            names=sexo_counts.index,
            title='👫 Distribuição por Sexo',
            color_discrete_sequence=[ROSA_PRINCIPAL, ROXO_MEDIO]
        )
        fig_sexo.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=14
        )
        fig_sexo.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO
        )
        st.plotly_chart(fig_sexo, use_container_width=True)
    
    # Pirâmide etária por sexo
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">📊 Pirâmide Etária por Sexo</h3>', unsafe_allow_html=True)
    
    # Criar dados para pirâmide etária
    piramide_data = df_filtered.groupby(['Sexo', 'Faixa_Etaria']).size().reset_index(name='Quantidade')
    
    # Separar por sexo
    masculino = piramide_data[piramide_data['Sexo'] == 'M'].copy()
    feminino = piramide_data[piramide_data['Sexo'] == 'F'].copy()
    
    # Inverter valores do masculino para criar efeito pirâmide
    masculino['Quantidade'] = -masculino['Quantidade']
    
    # Criar gráfico de barras horizontais
    fig_piramide = go.Figure()
    
    # Adicionar barra masculina
    fig_piramide.add_trace(go.Bar(
        y=masculino['Faixa_Etaria'],
        x=masculino['Quantidade'],
        name='Masculino',
        orientation='h',
        marker_color=ROXO_MEDIO,
        text=[abs(x) for x in masculino['Quantidade']],
        textposition='inside',
        hovertemplate='<b>Masculino</b><br>Faixa Etária: %{y}<br>Quantidade: %{text}<extra></extra>'
    ))
    
    # Adicionar barra feminina
    fig_piramide.add_trace(go.Bar(
        y=feminino['Faixa_Etaria'],
        x=feminino['Quantidade'],
        name='Feminino',
        orientation='h',
        marker_color=ROSA_PRINCIPAL,
        text=feminino['Quantidade'],
        textposition='inside',
        hovertemplate='<b>Feminino</b><br>Faixa Etária: %{y}<br>Quantidade: %{text}<extra></extra>'
    ))
    
    fig_piramide.update_layout(
        title='📊 Pirâmide Etária por Sexo',
        xaxis_title='Quantidade de Clientes',
        yaxis_title='Faixa Etária',
        barmode='relative',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=ROXO_PRINCIPAL,
        font_color=ROXO_CLARO,
        height=400,
        xaxis=dict(
            tickformat='.0f',
            showgrid=True,
            gridcolor='rgba(139, 74, 107, 0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(139, 74, 107, 0.2)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_piramide, use_container_width=True)
    
    # Distribuição de Idades com PDF
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">📈 Distribuição de Idades (PDF)</h3>', unsafe_allow_html=True)
    
    # Criar dados para o gráfico de distribuição
    idades = df_filtered['Idade'].values
    
    # Calcular estatísticas da distribuição normal
    mu, sigma = norm.fit(idades)
    
    # Criar histograma
    fig_distribuicao = go.Figure()
    
    # Adicionar histograma
    fig_distribuicao.add_trace(go.Histogram(
        x=idades,
        nbinsx=15,
        name='Frequência (Histograma)',
        marker_color=ROSA_CLARO,
        marker_line_color=ROXO_PRINCIPAL,
        marker_line_width=1,
        opacity=0.6,
        yaxis='y'
    ))
    
    # Criar curva KDE
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(idades)
    x_kde = np.linspace(idades.min(), idades.max(), 100)
    y_kde = kde(x_kde)
    
    # Adicionar curva KDE
    fig_distribuicao.add_trace(go.Scatter(
        x=x_kde,
        y=y_kde,
        mode='lines',
        name='KDE - Densidade Observada',
        line=dict(color=ROXO_INTENSO, width=3),
        yaxis='y2'
    ))
    
    # Criar curva normal ajustada
    x_norm = np.linspace(idades.min(), idades.max(), 100)
    y_norm = norm.pdf(x_norm, mu, sigma)
    
    # Adicionar curva normal
    fig_distribuicao.add_trace(go.Scatter(
        x=x_norm,
        y=y_norm,
        mode='lines',
        name='PDF - Distribuição Normal Ajustada',
        line=dict(color=ROXO_PRINCIPAL, width=3, dash='dash'),
        yaxis='y2'
    ))
    
    # Configurar layout
    fig_distribuicao.update_layout(
        title='📈 Distribuição de Idades (PDF)',
        xaxis_title='Idade',
        yaxis=dict(
            title='Frequência',
            side='left',
            showgrid=True,
            gridcolor='rgba(139, 74, 107, 0.2)'
        ),
        yaxis2=dict(
            title='Densidade de Probabilidade',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=ROXO_PRINCIPAL,
        font_color=ROXO_CLARO,
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(139, 74, 107, 0.2)'
        )
    )
    
    # Adicionar anotação com estatísticas
    fig_distribuicao.add_annotation(
        x=0.02,
        y=0.98,
        xref='paper',
        yref='paper',
        text=f'μ = {mu:.1f}<br>σ = {sigma:.1f}',
        showarrow=False,
        font=dict(color=ROXO_PRINCIPAL, size=12),
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor=ROXO_PRINCIPAL,
        borderwidth=1
    )
    
    st.plotly_chart(fig_distribuicao, use_container_width=True)
    
    # Segmentação de Clientes por Valor e Frequência
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">🏆 Segmentação de Clientes por Valor e Frequência</h3>', unsafe_allow_html=True)
    
    # Agrupar dados por cliente
    analise_clientes = df_filtered.groupby('Cliente').agg(
        Frequencia=('ID_Venda', 'count'),
        Valor_Total_Gasto=('Valor_Com_Desconto', 'sum')
    ).reset_index()

    fig_clientes = px.scatter(
        analise_clientes,
        x='Frequencia',
        y='Valor_Total_Gasto',
        size='Valor_Total_Gasto', # Tamanho da bolha representa o valor
        hover_name='Cliente',
        title='🏆 Segmentação de Clientes por Valor e Frequência',
        labels={'Frequencia': 'Número de Compras', 'Valor_Total_Gasto': 'Receita Total Gerada (R$)'}
    )
    
    # Aplicar o tema personalizado ao gráfico
    fig_clientes.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=ROXO_PRINCIPAL,
        font_color=ROXO_CLARO,
        xaxis_title="Número de Compras",
        yaxis_title="Receita Total Gerada (R$)"
    )
    
    st.plotly_chart(fig_clientes, use_container_width=True)
    
    # Análise de Avaliação e NPS
    st.markdown('<h2 class="section-title">⭐ Análise de Avaliação e NPS</h2>', unsafe_allow_html=True)
    
    # Calcular NPS
    def calculate_nps(avaliacoes):
        """Calcula o Net Promoter Score"""
        promotores = len(avaliacoes[avaliacoes >= 4])  # 4 e 5 estrelas
        detratores = len(avaliacoes[avaliacoes <= 2])  # 1 e 2 estrelas
        total = len(avaliacoes)
        
        if total == 0:
            return 0
        
        nps = ((promotores - detratores) / total) * 100
        return nps
    
    # NPS atual
    nps_atual = calculate_nps(df_filtered['Avaliação (1-5)'])
    
    # Distribuição das avaliações
    avaliacao_counts = df_filtered['Avaliação (1-5)'].value_counts().sort_index()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # NPS Score
        nps_color = VERDE if nps_atual >= 0 else VERMELHO if nps_atual < -50 else AMARELO
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p class="metric-label">📊 NPS Score</p>
            <p class="metric-value" style="color: {nps_color};">{nps_atual:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Avaliação Média
        avaliacao_media = df_filtered['Avaliação (1-5)'].mean()
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p class="metric-label">⭐ Avaliação Média</p>
            <p class="metric-value">{avaliacao_media:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Total de Avaliações
        total_avaliacoes = len(df_filtered)
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p class="metric-label">📝 Total de Avaliações</p>
            <p class="metric-value">{total_avaliacoes:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos de avaliação
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição das avaliações
        fig_avaliacoes = px.bar(
            x=avaliacao_counts.index,
            y=avaliacao_counts.values,
            title='📊 Distribuição das Avaliações',
            color=avaliacao_counts.values,
            color_continuous_scale=[ROXO_SUAVE, ROXO_MEDIO, ROXO_INTENSO, ROXO_PRINCIPAL]
        )
        fig_avaliacoes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO,
            xaxis_title="Avaliação (Estrelas)",
            yaxis_title="Quantidade",
            showlegend=False
        )
        fig_avaliacoes.update_traces(
            text=avaliacao_counts.values,
            textposition='outside',
            textfont_size=12
        )
        st.plotly_chart(fig_avaliacoes, use_container_width=True)
    
    with col2:
        # Classificação NPS
        promotores = len(df_filtered[df_filtered['Avaliação (1-5)'] >= 4])
        neutros = len(df_filtered[(df_filtered['Avaliação (1-5)'] == 3)])
        detratores = len(df_filtered[df_filtered['Avaliação (1-5)'] <= 2])
        
        nps_data = pd.DataFrame({
            'Categoria': ['Promotores', 'Neutros', 'Detratores'],
            'Quantidade': [promotores, neutros, detratores],
            'Cor': [VERDE, AMARELO, VERMELHO]
        })
        
        fig_nps = px.pie(
            values=nps_data['Quantidade'],
            names=nps_data['Categoria'],
            title='🎯 Classificação NPS',
            color_discrete_sequence=[VERDE, AMARELO, VERMELHO]
        )
        fig_nps.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        fig_nps.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO
        )
        st.plotly_chart(fig_nps, use_container_width=True)
    
    # Evolução temporal das avaliações
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">📈 Evolução Temporal das Avaliações</h3>', unsafe_allow_html=True)
    
    # Filtro específico para evolução temporal das avaliações
    col_filtro1, col_filtro2 = st.columns([1, 3])
    
    with col_filtro1:
        periodo_avaliacao = st.selectbox(
            "📊 Período de Análise",
            ["Diário", "Semanal", "Mensal", "Trimestral"],
            index=2  # Mensal como padrão
        )
    
    with col_filtro2:
        st.markdown(f"<p style='color: {ROXO_CLARO}; font-size: 0.9rem; margin-top: 0.5rem;'>Selecione o período para análise da evolução das avaliações e NPS</p>", unsafe_allow_html=True)
    
    # Calcular NPS por período
    if periodo_avaliacao == "Diário":
        df_temporal_avaliacao = df_filtered.groupby('Data_Venda').agg({
            'Avaliação (1-5)': ['mean', 'count']
        }).reset_index()
        df_temporal_avaliacao.columns = ['Data', 'Avaliacao_Media', 'Total_Avaliacoes']
        df_temporal_avaliacao['NPS'] = df_filtered.groupby('Data_Venda')['Avaliação (1-5)'].apply(calculate_nps).values
    elif periodo_avaliacao == "Semanal":
        df_temporal_avaliacao = df_filtered.groupby(['Ano', 'Semana']).agg({
            'Avaliação (1-5)': ['mean', 'count']
        }).reset_index()
        df_temporal_avaliacao.columns = ['Ano', 'Semana', 'Avaliacao_Media', 'Total_Avaliacoes']
        df_temporal_avaliacao['Data'] = df_temporal_avaliacao['Ano'].astype(str) + '-W' + df_temporal_avaliacao['Semana'].astype(str)
        df_temporal_avaliacao['NPS'] = df_filtered.groupby(['Ano', 'Semana'])['Avaliação (1-5)'].apply(calculate_nps).values
        df_temporal_avaliacao = df_temporal_avaliacao[['Data', 'Avaliacao_Media', 'Total_Avaliacoes', 'NPS']]
    elif periodo_avaliacao == "Mensal":
        df_temporal_avaliacao = df_filtered.groupby(['Ano', 'Mês']).agg({
            'Avaliação (1-5)': ['mean', 'count']
        }).reset_index()
        df_temporal_avaliacao.columns = ['Ano', 'Mês', 'Avaliacao_Media', 'Total_Avaliacoes']
        df_temporal_avaliacao['Data'] = df_temporal_avaliacao['Ano'].astype(str) + '-' + df_temporal_avaliacao['Mês'].astype(str).str.zfill(2)
        df_temporal_avaliacao['NPS'] = df_filtered.groupby(['Ano', 'Mês'])['Avaliação (1-5)'].apply(calculate_nps).values
        df_temporal_avaliacao = df_temporal_avaliacao[['Data', 'Avaliacao_Media', 'Total_Avaliacoes', 'NPS']]
    else:  # Trimestral
        df_temporal_avaliacao = df_filtered.groupby(['Ano', 'Trimestre']).agg({
            'Avaliação (1-5)': ['mean', 'count']
        }).reset_index()
        df_temporal_avaliacao.columns = ['Ano', 'Trimestre', 'Avaliacao_Media', 'Total_Avaliacoes']
        df_temporal_avaliacao['Data'] = df_temporal_avaliacao['Ano'].astype(str) + '-Q' + df_temporal_avaliacao['Trimestre'].astype(str)
        df_temporal_avaliacao['NPS'] = df_filtered.groupby(['Ano', 'Trimestre'])['Avaliação (1-5)'].apply(calculate_nps).values
        df_temporal_avaliacao = df_temporal_avaliacao[['Data', 'Avaliacao_Media', 'Total_Avaliacoes', 'NPS']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolução da avaliação média
        fig_avaliacao_evol = px.line(
            df_temporal_avaliacao,
            x='Data',
            y='Avaliacao_Media',
            title=f'⭐ Evolução da Avaliação Média - {periodo_avaliacao}',
            color_discrete_sequence=[ROSA_PRINCIPAL]
        )
        fig_avaliacao_evol.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO,
            xaxis_title="Período",
            yaxis_title="Avaliação Média"
        )
        st.plotly_chart(fig_avaliacao_evol, use_container_width=True)
    
    with col2:
        # Evolução do NPS
        fig_nps_evol = px.line(
            df_temporal_avaliacao,
            x='Data',
            y='NPS',
            title=f'📊 Evolução do NPS - {periodo_avaliacao}',
            color_discrete_sequence=[ROXO_INTENSO]
        )
        fig_nps_evol.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO,
            xaxis_title="Período",
            yaxis_title="NPS Score"
        )
        # Adicionar linha de referência NPS = 0
        fig_nps_evol.add_hline(y=0, line_dash="dash", line_color="gray", 
                              annotation_text="NPS = 0", annotation_position="bottom right")
        st.plotly_chart(fig_nps_evol, use_container_width=True)
    
    # Análise de produtos
    st.markdown('<h2 class="section-title">👗 Análise de Produtos</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 produtos por receita
        top_produtos = df_filtered.groupby('Produto')['Valor_Com_Desconto'].sum().nlargest(10)
        fig_produtos = px.bar(
            x=top_produtos.values,
            y=top_produtos.index,
            orientation='h',
            title='🏆 Top 10 Produtos por Receita',
            color_discrete_sequence=['#ff9a9e']
        )
        fig_produtos.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='#8b4a6b',
            font_color='#6b3a4a',
            xaxis_title="Receita (R$)",
            yaxis_title="Produto"
        )
        st.plotly_chart(fig_produtos, use_container_width=True)
    
    with col2:
        # Treemap de receita por categoria
        categoria_receita = df_filtered.groupby('Categoria')['Valor_Com_Desconto'].sum().reset_index()
        categoria_receita.columns = ['Categoria', 'Receita']
        
        fig_treemap = px.treemap(
            categoria_receita,
            path=['Categoria'],
            values='Receita',
            title='📊 Receita por Categoria (Treemap)',
            color='Receita',
            color_continuous_scale=[ROXO_SUAVE, ROXO_ESCURO, ROXO_MEDIO, ROXO_INTENSO, ROXO_PRINCIPAL]
        )
        fig_treemap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color=ROXO_PRINCIPAL,
            font_color=ROXO_CLARO
        )
        st.plotly_chart(fig_treemap, use_container_width=True)
    
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">🎨 Heatmap: Quantidade Vendida por Cor vs Tamanho</h3>', unsafe_allow_html=True)

    # 1. ORDENAÇÃO LÓGICA DOS TAMANHOS
    # Define a ordem correta para os tamanhos
    tamanhos_ordem = ['P', 'M', 'G', 'GG']
    df_filtered['Tamanho'] = pd.Categorical(df_filtered['Tamanho'], categories=tamanhos_ordem, ordered=True)
    
    # Criar pivot table para o heatmap
    heatmap_pivot = pd.pivot_table(
        df_filtered,
        values='Quantidade',
        index='Cor',
        columns='Tamanho',
        aggfunc='sum',
        fill_value=0
    ).sort_index() # Ordena as cores alfabeticamente no eixo Y
    
    # 2. NOVA ESCALA DE CORES
    # Cria um gradiente que vai do rosa pastel ao roxo intenso
    colorscale_custom = [ROSA_PASTEL, ROSA_PRINCIPAL, ROXO_INTENSO]
    
    # Criar o heatmap
    fig_heatmap = px.imshow(
        heatmap_pivot,
        text_auto=True,  # Deixa o Plotly gerenciar os valores e a cor do texto
        aspect="auto",   # Ajusta o aspecto para preencher o container
        color_continuous_scale=colorscale_custom,
        labels=dict(x="Tamanho", y="Cor", color="Quantidade")
    )
    
    # 3. LAYOUT ATUALIZADO
    fig_heatmap.update_layout(
        title_text='🔥 Quantidade Vendida: Cor vs Tamanho',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=ROXO_PRINCIPAL,
        font_color=ROXO_CLARO,
        xaxis_title="Tamanho",
        yaxis_title="Cor",
        coloraxis_colorbar=dict(
            title="Quantidade",
            title_font_color=ROXO_PRINCIPAL,
            tickfont_color=ROXO_CLARO
        )
    )
    
    # Atualiza o hovertemplate para uma melhor experiência
    fig_heatmap.update_traces(
        hovertemplate="<b>Cor:</b> %{y}<br><b>Tamanho:</b> %{x}<br><b>Quantidade:</b> %{z}<extra></extra>"
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Análise de efetividade dos descontos
    st.markdown(f'<h3 style="color: {ROXO_PRINCIPAL}; font-size: 1.4rem; margin: 1.5rem 0 1rem 0;">💸 Análise de Efetividade dos Descontos</h3>', unsafe_allow_html=True)
    
    fig_desconto = px.scatter(
        df_filtered,
        x='Desconto (%)',
        y='Quantidade',
        color='Categoria', # Opcional: para ver o comportamento por categoria
        title='💸 Análise de Efetividade dos Descontos',
        labels={'Desconto (%)': 'Desconto Aplicado (%)', 'Quantidade': 'Itens Vendidos na Transação'},
        trendline='ols' # Adiciona uma linha de tendência para visualizar a correlação
    )
    
    # Aplicar o tema personalizado ao gráfico
    fig_desconto.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color=ROXO_PRINCIPAL,
        font_color=ROXO_CLARO,
        xaxis_title="Desconto Aplicado (%)",
        yaxis_title="Itens Vendidos na Transação"
    )
    
    st.plotly_chart(fig_desconto, use_container_width=True)
    
    # Análise geográfica
    st.markdown('<h2 class="section-title">🗺️ Análise Geográfica</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top estados por receita
        estado_receita = df_filtered.groupby('Estado')['Valor_Com_Desconto'].sum().nlargest(10)
        fig_estados = px.bar(
            x=estado_receita.index,
            y=estado_receita.values,
            title='🏆 Top 10 Estados por Receita',
            color_discrete_sequence=['#ff9a9e']
        )
        fig_estados.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='#8b4a6b',
            font_color='#6b3a4a',
            xaxis_title="Estado",
            yaxis_title="Receita (R$)"
        )
        st.plotly_chart(fig_estados, use_container_width=True)
    
    with col2:
        # Distribuição por canal de venda
        canal_receita = df_filtered.groupby('Canal_Venda')['Valor_Com_Desconto'].sum()
        fig_canal = px.pie(
            values=canal_receita.values,
            names=canal_receita.index,
            title='🏪 Receita por Canal de Venda',
            color_discrete_sequence=['#ff9a9e', '#fecfef']
        )
        fig_canal.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='#8b4a6b',
            font_color='#6b3a4a'
        )
        st.plotly_chart(fig_canal, use_container_width=True)
    
    # Análise de performance por vendedor
    st.markdown('<h2 class="section-title">👨‍💼 Performance dos Vendedores</h2>', unsafe_allow_html=True)
    
    vendedor_stats = df_filtered.groupby('Vendedor').agg({
        'Valor_Com_Desconto': 'sum',
        'ID_Venda': 'count',
        'Cliente': 'nunique',
        'Avaliação (1-5)': 'mean'
    }).round(2)
    vendedor_stats.columns = ['Receita Total', 'Número de Vendas', 'Clientes Únicos', 'Avaliação Média']
    vendedor_stats['Ticket Médio'] = (vendedor_stats['Receita Total'] / vendedor_stats['Número de Vendas']).round(2)
    
    st.dataframe(
        vendedor_stats.sort_values('Receita Total', ascending=False),
        use_container_width=True
    )
    
    # Análise de sazonalidade
    st.markdown('<h2 class="section-title">📅 Análise de Sazonalidade</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Vendas por dia da semana
        dia_semana_receita = df_filtered.groupby('Dia_Semana')['Valor_Com_Desconto'].sum()
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dia_semana_receita = dia_semana_receita.reindex(dias_ordem)
        
        fig_dia = px.bar(
            x=dia_semana_receita.index,
            y=dia_semana_receita.values,
            title='📊 Receita por Dia da Semana',
            color_discrete_sequence=['#ff9a9e']
        )
        fig_dia.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='#8b4a6b',
            font_color='#6b3a4a',
            xaxis_title="Dia da Semana",
            yaxis_title="Receita (R$)"
        )
        st.plotly_chart(fig_dia, use_container_width=True)
    
    with col2:
        # Vendas por mês
        mes_receita = df_filtered.groupby('Mês')['Valor_Com_Desconto'].sum()
        fig_mes = px.bar(
            x=mes_receita.index,
            y=mes_receita.values,
            title='📅 Receita por Mês',
            color_discrete_sequence=['#fecfef']
        )
        fig_mes.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='#8b4a6b',
            font_color='#6b3a4a',
            xaxis_title="Mês",
            yaxis_title="Receita (R$)"
        )
        st.plotly_chart(fig_mes, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8b4a6b; padding: 2rem;">
        <p style="font-size: 1.1rem; margin: 0;">💖 Dashboard desenvolvido com amor para análise de vendas</p>
        <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0;">Powered by Streamlit & Plotly</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
