
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Dashboard Olist",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Vendas - Olist")
st.write("Análise dos pedidos, clientes e categorias de produtos.")


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

PASTA_DADOS = Path(__file__).parent / "archive"

orders = pd.read_csv(
    PASTA_DADOS / "olist_orders_dataset.csv"
)

customers = pd.read_csv(
    PASTA_DADOS / "olist_customers_dataset.csv"
)

products = pd.read_csv(
    PASTA_DADOS / "olist_products_dataset.csv"
)

items = pd.read_csv(
    PASTA_DADOS / "olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    PASTA_DADOS / "olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    PASTA_DADOS / "olist_order_reviews_dataset.csv"
)

sellers = pd.read_csv(
    PASTA_DADOS / "olist_sellers_dataset.csv"
)


# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================

orders["order_status"] = orders["order_status"].replace({
    "delivered": "entregue",
    "shipped": "enviado",
    "canceled": "cancelado",
    "unavailable": "indisponivel",
    "invoiced": "faturado",
    "processing": "processando",
    "created": "criado",
    "approved": "aprovado"
})

payments["payment_type"] = payments["payment_type"].replace({
    "credit_card": "cartão de crédito",
    "debit_card": "cartão de débito",
    "not_defined": "não definido"
})


# ============================================================
# INDICADORES
# ============================================================

total_pedidos = len(orders)

total_clientes = customers["customer_unique_id"].nunique()

total_produtos = products["product_id"].nunique()

total_vendedores = sellers["seller_id"].nunique()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total de pedidos",
        f"{total_pedidos:,}".replace(",", ".")
    )

with col2:
    st.metric(
        "Total de clientes",
        f"{total_clientes:,}".replace(",", ".")
    )

with col3:
    st.metric(
        "Total de produtos",
        f"{total_produtos:,}".replace(",", ".")
    )

with col4:
    st.metric(
        "Total de vendedores",
        f"{total_vendedores:,}".replace(",", ".")
    )


st.divider()


# ============================================================
# PRIMEIRA LINHA DE GRÁFICOS
# ============================================================

col_pedidos, col_clientes, col_produtos, col_pagamentos = st.columns(4)


# ============================================================
# PEDIDOS
# ============================================================

with col_pedidos:

    with st.container(border=True):

        st.markdown("### 📊 Pedidos")

        proporcao = (
            orders["order_status"]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
            .reset_index()
            .sort_index(ascending=False)
        )

        proporcao.columns = [
            "order_status",
            "percentual"
        ]

        fig_proporcao = px.bar(
            proporcao,
            x="percentual",
            y="order_status",
            text="percentual"
        )
        fig_proporcao.update_xaxes(
            range=[0,105]
        )

        fig_proporcao.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            cliponaxis=False
        )

        fig_proporcao.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            margin=dict(
                l=5,
                r=35,
                t=10,
                b=5
            ),
            height=250
        )

        st.plotly_chart(
            fig_proporcao,
            use_container_width=True
        )


# ============================================================
# CLIENTES
# ============================================================

with col_clientes:

    with st.container(border=True):

        st.markdown("### 👥 Clientes")

        proporcao_clientes = (
            customers
            .drop_duplicates("customer_unique_id")
            ["customer_state"]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
            .head(5)
            .reset_index()
        )

        proporcao_clientes.columns = [
            "customer_state",
            "percentual"
        ]

        fig_clientes = px.bar(
            proporcao_clientes,
            x="customer_state",
            y="percentual",
            text="percentual"
        )

        fig_clientes.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            cliponaxis=False
        )

        fig_clientes.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            margin=dict(
                l=5,
                r=5,
                t=10,
                b=5
            ),
            height=250
        )

        st.plotly_chart(
            fig_clientes,
            use_container_width=True
        )


# ============================================================
# PRODUTOS
# ============================================================

with col_produtos:

    with st.container(border=True):

        st.markdown("### 🛍️ Produtos")

        top_produtos = (
            products["product_category_name"]
            .value_counts(normalize=True)
            .mul(100)
            .dropna()
            .head(5)
            .sort_values()
            .reset_index()
        )

        top_produtos.columns = [
            "categoria",
            "quantidade"
        ]

        fig_produtos = px.bar(
            top_produtos,
            x="categoria",
            y="quantidade",
            text="quantidade",
            #orientation="h"
        )

        fig_produtos.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig_produtos.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            margin=dict(
                l=5,
                r=5,
                t=10,
                b=5
            ),
            height=250
        )

        st.plotly_chart(
            fig_produtos,
            use_container_width=True
        )


# ============================================================
# PAGAMENTOS
# ============================================================

with col_pagamentos:

    with st.container(border=True):

        st.markdown("### 💳 Pagamentos")

        pagamentos = (
            payments["payment_type"]
            .value_counts(normalize=True)
            .mul(100)
            .round(2)
            .reset_index()
        )

        pagamentos.columns = [
            "tipo",
            "percentual"
        ]

        fig_pagamentos = px.bar(
            pagamentos,
            x="tipo",
            y="percentual",
            text="percentual"
        )

        fig_pagamentos.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        fig_pagamentos.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            margin=dict(
                l=5,
                r=5,
                t=10,
                b=5
            ),
            height=250
        )

        st.plotly_chart(
            fig_pagamentos,
            use_container_width=True
        )


# ============================================================
# SEPARAÇÃO
# ============================================================

st.divider()


# ============================================================
# CATEGORIAS DE PRODUTOS
# ============================================================

categorias = (
    products["product_category_name"]
    .dropna()
    .value_counts()
    .reset_index()
)

categorias.columns = [
    "quantidade",
    "categoria"
    
]


# ============================================================
# TOP 10 CATEGORIAS
# ============================================================

st.subheader("🏆 Top 10 categorias de produtos")

top_10 = (
    categorias
    .sort_values(
        "quantidade",
        ascending=False
    )
    .head(10)
    .sort_values(
        "quantidade",
        ascending=True
    )
)

fig_categorias = px.bar(
    top_10,
    x="categoria",
    y="quantidade",
    text="categoria",
)

fig_categorias.update_traces(
    textposition="outside",
    texttemplate="%{text}%",

)

fig_categorias.update_layout(
    xaxis_title="Quantidade",
    yaxis_title=None,
    showlegend=False,
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    ),
    height=400
)

st.plotly_chart(
    fig_categorias,
    use_container_width=True
)


# ============================================================
# 10 CATEGORIAS COM MENOR QUANTIDADE
# ============================================================

st.subheader("📉 10 categorias com menor quantidade")

menores_10 = (
    categorias
    .sort_values(
        "quantidade",
        ascending=True
    )
    .head(10)
    .sort_values(
        "quantidade",
        ascending=True
    )
)

fig_menores = px.bar(
    menores_10,
    x="quantidade",
    y="categoria",
    text="quantidade",
    orientation="h"
)

fig_menores.update_traces(
    textposition="outside"
)

fig_menores.update_layout(
    xaxis_title="Quantidade",
    yaxis_title=None,
    showlegend=False,
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    ),
    height=400
)

st.plotly_chart(
    fig_menores,
    use_container_width=True
)


# ============================================================
# ACESSO LOCAL
# ============================================================

st.divider()

st.info(
    "🌐 Dashboard local: http://localhost:8501"
)

print("=" * 50)
print("📊 Dashboard Olist iniciado!")
print("🌐 Acesso local: http://localhost:8501")
print("=" * 50)
