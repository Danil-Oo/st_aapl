import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import numpy as np
import datetime
from functools import reduce

st.title('Доходность акций Apple')

aapl = yf.Ticker('AAPL')
aapl_df = aapl.history(period='1d', start='2013-01-01', end='2024-10-07')
# Добавляю колонку с расчетом логарифмической доходности по каждому дню,
# так ее можно суммировать и найти годовую, арифметическую суммировать нельзя
aapl_df['ln_profitab'] = np.log(aapl_df['Close'] / aapl_df['Close'].shift(1))
aapl_df = aapl_df.reset_index()
aapl_df['Date'] = pd.to_datetime(aapl_df['Date'])
years = [i for i in range(2013, 2024)]
aapl_profitability_by_year = []
for j in years:
    aapl_profitability_by_year \
        .append((aapl_df[aapl_df['Date'].dt.year == j]['ln_profitab'].sum())
                * 100)

aapl_profitab_df = pd.DataFrame({'Годы': years,
                                 'Акции Apple, %': aapl_profitability_by_year,
                                 'Ставка ФРС США, %': [0.11, 0.09, 0.13,
                                                       0.39, 1, 1.83,
                                                       2.16, 0.37, 0.08,
                                                       4.1, 5.33]})

select_bar = st.sidebar.multiselect(
    "**Показать на графике:**", ['Акции Apple, %', 'Ставка ФРС США, %'],
    ['Акции Apple, %', 'Ставка ФРС США, %'])
st.header("Сравнение доходности акций Apple со ставкой ФРС США")
st.bar_chart(data=aapl_profitab_df, x='Годы',
             y=select_bar)
st.write('**Ставка ФРС США - это процент, по которому банки предоставляют \
    друг другу краткосрочные кредиты. То есть уровень ставки олицетворяет \
        "стоимость денег" для всей экономики. Аналог ключевой ставки в РФ, \
            который используется для сравнения доходности альтернативных \
                вложений.*')
st.divider()

income_num = st.sidebar.slider('**Выберите сумму в долларах**', 1000,
                               100_000, 20_000, 2000)
percent_list = [1 + (z/100) for z in aapl_profitability_by_year]
percent_list.insert(0, income_num)
revenue_of_investor = reduce(lambda x, y: x * y, percent_list)
st.subheader(f"Если бы в 2013 году вы вложили в акции Apple ${income_num}, \
    то к концу 2023 года вы бы заработали: ")

st.metric(' ', f"${round(revenue_of_investor, 2)}")
st.divider()
st.title('Дивиденды')

dividends_aapl = aapl_df[aapl_df['Dividends']
                         != 0][['Date', 'Dividends', 'Close']]
aapl_dividends_per_year = []
for n in years:
    aapl_dividends_per_year \
        .append(dividends_aapl[dividends_aapl['Date']
                               .dt.year == n]['Dividends'].sum())

aapl_divs_df = pd.DataFrame({'Годы': years,
                             'Дивиденды за год, $': aapl_dividends_per_year})

st.header("Суммарный объем дивидендов на одну акцию Apple")
st.bar_chart(data=aapl_divs_df, x='Годы',
             y='Дивиденды за год, $')
st.divider()

dividends_aapl['Div_profitab'] = round(
    dividends_aapl['Dividends'] / dividends_aapl['Close'] * 100, 2)

dividends_aapl = dividends_aapl.set_index('Date')

st.header("График дивидендной доходности компании Apple")
st.line_chart(dividends_aapl['Div_profitab'],
              y_label='Дивидендная доходность, %')
st.divider()
