
import streamlit as st
import plotly.graph_objects as go

def render_financial_gauges(indicators):
    fig = go.Figure()

    for i, (title, value) in enumerate(indicators.items()):
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            domain={'row': i // 3, 'column': i % 3},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'bgcolor': "lightgray"
            }
        ))

    fig.update_layout(
        grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
        margin=dict(t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
