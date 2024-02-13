import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# ページ毎に異なる変数を保持するためのsession_stateを初期化
if 'page_num' not in st.session_state:
    st.session_state.page_num = 'page1'

# ページ毎に異なるデータを保持するためのsession_stateを初期化
if 'input_data' not in st.session_state:
    st.session_state.input_data = pd.DataFrame(columns=['Year', 'Month','Day','カテゴリ', '金額','累計','メモ'])

#ページ毎に異なるデータを保持するためのsession_stateを初期化
if 'input_data2' not in st.session_state:
    st.session_state.input_data2 = pd.DataFrame(columns=['Month','Day','カテゴリ', '金額','累計','メモ'])


# ページ毎に異なるデータを保持するためのsession_stateを初期化
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = pd.DataFrame(columns=['Day','累計'])

# ページ毎に異なるデータを保持するためのsession_stateを初期化
if 'sum' not in st.session_state:
    st.session_state.sum = 0

# データフレームの初期化
# columns=['日付', 'カテゴリ', '金額','メモ']
# df = pd.DataFrame(columns=columns)
# category={'Year':[], 'Month':[],'Day':[],'カテゴリ':[], '金額':[],'メモ':[]}
# category={'Year':["2023","2024","2024","2024"], 'Month':["12","1","1","2"], 'Day':["30","4","10","15"], 'カテゴリ':["自炊費","自炊費","自炊費","自炊費"], '金額':["1000","1400","2100","10000"],'メモ':["","","",""]}
# df = pd.DataFrame(category)
            

# サイドバーにページ選択のセレクトボックスを作成
page = st.sidebar.selectbox('MENU', ['収支入力', '月々収支', '年間収支'])


# 選択されたページに応じてコンテンツを表示
if page == '収支入力':
    st.title('収支入力')

    tab1, tab2= st.tabs(["入力FORM", "DATA"])

    with tab1:
        with st.form("収支入力FORM", clear_on_submit=False):
            
            # 収入または支出の入力フォーム
            today=pd.to_datetime('today')

            year_month_day=st.date_input('年月日', today)
            year=year_month_day.year
            month=year_month_day.month
            day=year_month_day.day

            # st.write('year_month_day:', year)
            # st.write('year_month_day:', month)
            # st.write('year_month_day:', day)

            category = st.selectbox('カテゴリを選択', ['収入', '自炊費','外食費','娯楽費','生活用品','購入品'])
            amount = st.number_input('金額', min_value=0, step=1)
            

            memo = st.text_area('memo')
            submitted = st.form_submit_button("データ入力")

            # 入力されたデータをデータフレームに追加
            if submitted:
                # newdata=[[pd.to_datetime(date),category,amount,memo]]
                # #new_data=pd.DataFrame({'日付': pd.to_datetime(date), 'カテゴリ': category, '金額': amount,'メモ':memo})
                # new_data=pd.DataFrame(data=newdata,columns=columns)
                # #df = df.append(new_data)
                # #df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                # df = pd.concat([df, new_data], ignore_index=True)

                new_data={'Year':year,'Month':month,'Day':day, 'カテゴリ':category, '金額':amount,'メモ':memo}
            
                st.session_state.input_data = pd.concat([st.session_state.input_data,pd.DataFrame([new_data])], ignore_index=True)
                # st.session_state.input_data['累計'] = st.session_state.input_data['金額'].cumsum()
                st.session_state.input_data = st.session_state.input_data.reset_index(drop=True)
                
                # df = pd.concat([df,pd.DataFrame([new_data])], ignore_index=True)
                # df = df.reset_index(drop=True)

    with tab2:
        # データフレームを表示
        st.checkbox("Use container width", value=True, key="use_container_width")
        st.subheader('購入ログ')

        options_list = [f'{i}' for i in range(1, 13)]

        specified_column = 'Year'
        selected_value=st.selectbox(f'Select a value for {specified_column}:', st.session_state.input_data[specified_column].unique())
        specified_data = selected_value
        filtered_data = st.session_state.input_data[st.session_state.input_data[specified_column] == specified_data]

        specified_column1 = 'Month'
        selected_value1=st.selectbox(f'Select a value for {specified_column1}:', options_list)
        specified_data1 = int(selected_value1)
        filtered_data1 = filtered_data[filtered_data[specified_column1] == specified_data1]

        # st.session_state.input_data['累計'] = filtered_data['金額'].cumsum()
        # st.dataframe(df, use_container_width=st.session_state.use_container_width,hide_index=True)
        st.data_editor(filtered_data1, use_container_width=st.session_state.use_container_width,hide_index=True)
        
        st.session_state.sum=filtered_data1['金額'].sum()
        st.write('累計金額:',st.session_state.sum)

elif page == '月々収支':
    st.title('月々収支')

    options_list = [f'{i}' for i in range(1, 13)]

    specified_column2 = 'Year'
    selected_value2=st.selectbox(f'Select a value for {specified_column2}:', st.session_state.input_data[specified_column2].unique())
    specified_data2 = selected_value2
    filtered_data2 = st.session_state.input_data[st.session_state.input_data[specified_column2] == specified_data2]
    # st.session_state.input_data2 = st.session_state.input_data[st.session_state.input_data[specified_column2] == specified_data2]
    # st.write('filtered_data2')
    # st.write(filtered_data2)
    # st.write(st.session_state.input_data2)

    specified_column3 = 'Month'
    selected_value3=st.selectbox(f'Select a value for {specified_column3}:', options_list)
    specified_data3 = int(selected_value3)
    filtered_data3 = filtered_data2[filtered_data2[specified_column3] == specified_data3]
    # filtered_data3 = st.session_state.input_data2[st.session_state.input_data2[specified_column3] == specified_data3]
    # st.write('filtered_data3')
    # st.write(filtered_data3)

    # st.write()
    filtered_data3['累計']= filtered_data3['金額'].cumsum()
    # st.write('filtered_data3[累計]')
    # st.write(filtered_data3['累計'])

    st.session_state.graph_data = filtered_data3[['Day', '累計']]
    st.session_state.graph_data = st.session_state.graph_data.reset_index(drop=True)
    # st.write('st.session_state.graph_data')
    # st.write(st.session_state.graph_data)
    # st.line_chart(st.session_state.input_data('Day')['累計'])
    st.bar_chart(st.session_state.graph_data.set_index('Day'),use_container_width=True)
    # matplotlibで棒グラフを描画
    # fig, ax = plt.subplots()
    # ax.bar(st.session_state.input_data['Day'], st.session_state.input_data['累計'])
    # st.pyplot(fig)



else:
    st.title('年間収支')
    # specified_column4 = 'Year'
    # selected_value4=st.selectbox(f'Select a value for {specified_column4}:', st.session_state.input_data[specified_column4].unique())
    # specified_data4 = int(selected_value4)
    # filtered_data4 = st.session_state.input_data[st.session_state.input_data[specified_column4] == specified_data4]

    specified_column4 = 'Year'
    selected_value4=st.selectbox(f'Select a value for {specified_column4}:', st.session_state.input_data[specified_column4].unique())
    specified_data4 = selected_value4
    filtered_data4 = st.session_state.input_data[st.session_state.input_data[specified_column4] == specified_data4]

    # 各カテゴリごとに合計を計算
    result_df = st.session_state.input_data.groupby('Year')['金額'].sum().reset_index()
    st.bar_chart(result_df.set_index('Year'),use_container_width=True)


# # 月ごとの支出の可視化
# st.subheader('月ごとの支出合計')
# monthly_expenses = df[df['カテゴリ'] == '支出'].groupby(df['日付'].dt.month)['金額'].sum()
# fig_monthly_expenses, ax_monthly_expenses = plt.subplots()
# monthly_expenses.plot(kind='bar', ax=ax_monthly_expenses)
# st.pyplot(fig_monthly_expenses)

# # 支出の割合を円グラフで表示
# st.subheader('支出の割合')
# expense_category_totals = df[df['カテゴリ'] == '支出'].groupby('カテゴリ')['金額'].sum()
# fig_expense_pie, ax_expense_pie = plt.subplots()
# ax_expense_pie.pie(expense_category_totals, labels=expense_category_totals.index, autopct='%1.1f%%', startangle=90)
# ax_expense_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# st.pyplot(fig_expense_pie)

# # 収入と支出の合計を表示
# st.subheader('収支の合計')
# income_total = df[df['カテゴリ'] == '収入']['金額'].sum()
# expense_total = df[df['カテゴリ'] == '支出']['金額'].sum()
# st.write(f'収入合計: {income_total} 円')
# st.write(f'支出合計: {expense_total} 円')
# st.write(f'収支差: {income_total - expense_total} 円')
