import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
# Структура приложения
# Думаю сделать приложение 3 страницы:
# 1. Страница с общей информацией о компании, какими-то базовыми показателями
# и графиками
# 2. Страница с ценами акций компании, их показателями
# 3. Страница с дивидендами компании, их показателями

st.title("Обзор компании Apple")
st.subheader('''Компания Apple — крупная корпорация, которая занимает \
    лидирующие позиции в сфере производства компьютерной техники, \
        гаджетов и программного обеспечения. Является одной из самых \
            "дорогих" компаний в мире.''')

st.divider()
st.header("Ключевые рыночные показатели компании")
aapl = yf.Ticker('AAPL')
col1, col2, col3 = st.columns(3)
# num_of_shares_outst - это кол-во акицй в обращении, не смог его выцепить через библиотеку, взял из открытых источников
# Это число нужно для расчета капитализации
num_of_shares_outst = 15_338_000_000
col1.metric("**Стоимость компании, млрд.**",
            f"${int((aapl.history(period='1mo').loc['2024-10-07']['Close'] * num_of_shares_outst) / 1_000_000_000)}")
col2.metric("**Выручка за 2023 г., млрд.**",
            f"${int(aapl.financials.loc['Total Revenue']['2023'] / 1_000_000_000)}")
col3.metric("**Прибыль за 2023 г., млрд.**",
            f"${int(aapl.financials.loc['Net Income']['2023'] / 1_000_000_000)}")

st.divider()
date = st.sidebar.date_input("**Укажите временной промежуток для графика цены акций**",
                             (datetime.date(2013, 1, 1), datetime.date(2024, 10, 7)), datetime.date(
                                 2013, 1, 1), datetime.date(2024, 10, 7),
                             format="YYYY.MM.DD")
st.header("График движения цены акций Apple")
aapl_df = aapl.history(period='1d', start='2013-01-01', end='2024-10-07')
# Когда выбираешь дату на виджите вылазит ошибка, пока не выберешь вторую дату
# Наверное, надо бы обработать ее исключением, но мне очень не хочется
st.line_chart(aapl_df.loc[date[0].strftime(
    "%Y-%m-%d"): date[1].strftime("%Y-%m-%d")]['Close'], x_label='Временной отрезок', y_label='Цена, $')
st.divider()
date2 = st.sidebar.date_input("**Укажите временной промежуток для графика объема торгов**",
                              (datetime.date(2013, 1, 1), datetime.date(2024, 10, 7)), datetime.date(
                                  2013, 1, 1), datetime.date(2024, 10, 7),
                              format="YYYY.MM.DD")
st.header("График объема торгов акций Apple")
st.line_chart(aapl_df.loc[date2[0].strftime(
    "%Y-%m-%d"): date2[1].strftime("%Y-%m-%d")]['Volume'], x_label='Временной отрезок', y_label='Объем, шт.')
st.divider()
