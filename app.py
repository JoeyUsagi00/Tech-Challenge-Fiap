
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

#============================================================
#DEFS
#============================================================
def classificar_entrega(dias):
    if pd.isna(dias):
        return "Não entregue"
    elif dias > 0:
        return "Atrasado"
    else:
        return "No prazo"
    satisfacao["situacao_entrega"] = (
        satisfacao["dias_atraso"]
        .apply(classificar_entrega)
    )




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
tabelas = {}

arquivos = {
    "olist_orders_dataset.csv":"olist_orders_dataset.csv",
    "olist_customers_dataset.csv":"olist_customers_dataset.csv",

    "olist_order_items_dataset.csv":"olist_order_items_dataset.csv",

    "olist_products_dataset.csv":"olist_products_dataset.csv",

    "olist_order_payments_dataset.csv":"olist_order_payments_dataset.csv",

    "olist_order_reviews_dataset.csv":"olist_order_reviews_dataset.csv",

    "olist_sellers_dataset.csv":"olist_sellers_dataset.csv",

    "olist_geolocation_dataset.csv":"olist_geolocation_dataset.csv",

    "product_category_name_translation.csv":"product_category_name_translation.csv"
}





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

# teste = st.sidebar.selectbox("Teste","Teste")
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

        # estados = customers['customer_city'].value_counts()

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
            .round(2) #Deixar o valor somente com duas casas decimais
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
# SATISFAÇÃO CLIENTES
# ============================================================

st.subheader("Satisfação Clientes")
#PERGUNTA NORTEADORA!!!!
# "As entregas estão afetando a satisfação dos clientes?"
# col_satisfacao_cliente = st.columns(1)
col_nota, col_percentual = st.columns(2)

# with col_satisfacao_cliente[0]:

with col_nota:
    with st.container(border=True):
        satisfacao = reviews.merge( #MERGE É PARA JUNTAR AS COLUNAS
            orders,
            on="order_id",
            how="inner"
        )
        satisfacao["dias atraso"] = (
            pd.to_datetime(satisfacao["order_delivered_customer_date"])
            -
            pd.to_datetime(satisfacao["order_estimated_delivery_date"])
        ).dt.days

        satisfacao["situacao_entrega"] = satisfacao["dias atraso"].apply(
            lambda x:"Atrasado" if x > 0 else "No prazo"
        )
        satisfacao["cliente_satisfeito"] = (
            satisfacao["review_score"] >= 4
        )
        percentual_satisfacao = (
            satisfacao
            .groupby("situacao_entrega")["cliente_satisfeito"]
            .mean()
            .mul(100)
            .round(2)
            .reset_index()
        )
        media_satisfacao = (
            satisfacao
            .groupby("situacao_entrega")["review_score"]
            .mean()
            .reset_index()
            .round(2)
            # .value_counts(normalize=True)
        )

        fig_satisfacao = px.bar(
            media_satisfacao,
            x="situacao_entrega",
            y="review_score",
            # y="cliente_satisfeito",
            text="review_score"
            # text="cliente_satisfeito"
        )


        fig_satisfacao.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
            textfont=dict(size=14)
        )

        fig_satisfacao.update_layout(
            title="Nota média por situação de entrega",
            xaxis_title=None,
            yaxis_title="Nota média",
            showlegend=False,
            margin=dict(
                l=10,
                r=10,
                t=60,
                b=10
            ),
            height=350
        )

        st.plotly_chart(
            fig_satisfacao,
            use_container_width=True
        )

with col_percentual:
        with st.container(border=True):
            fig_percentual = px.bar(
                percentual_satisfacao,
                x="situacao_entrega",
                y="cliente_satisfeito",
                text="cliente_satisfeito"
            )
            fig_percentual.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                textfont=dict(size=14)
            )
            fig_percentual.update_layout(
                title = "% de clientes satisfeitos",
                xaxis_title=None,
                yaxis_title="% Satisfeitos",
                showlegend=False,
                margin=dict(
                    l=10,
                    r=10,
                    t=60,
                    b=10
                ),
                height=350
            )
            st.plotly_chart(
                fig_percentual,
                use_container_width=True
            )



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
st.divider()

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

st.divider()











# ============================================================
# ACESSO LOCAL
# ============================================================


st.info(
    "🌐 Dashboard local: http://localhost:8501"
)

print("=" * 50)
print("📊 Dashboard Olist iniciado!")
print("🌐 Acesso local: http://localhost:8501")
print("=" * 50)
