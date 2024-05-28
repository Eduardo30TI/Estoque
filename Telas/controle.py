import streamlit as st
import os
import socket as s
import DataSet.data as dt
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
from Moeda import Moeda
import plotly.graph_objects as go
from DownloadXLSX import ExcelDW

class Controle:

    def __init__(self) -> None:

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)

        pass

    def main(self):

        placeholder=st.empty()

        var_dict=dict()

        with placeholder.container():

            st.title('Estoque')
            tab1,tab2,tab3=st.tabs(['Contagem','Divergência','OK'])

            dt_now=datetime.now().date()

            with st.sidebar:

                var_dict['dtinicial']=st.date_input(label='Data Inicial',value=dt_now,key='dt1')
                var_dict['dtfinal']=st.date_input(label='Data Inicial',value=dt_now,key='dt2')

                btn_refresh=st.button('Atualizar',use_container_width=True,type='primary')
                
                tabela='STK'
                df=dt.inventario()

                df[tabela]=df[tabela].loc[df[tabela]['Data e Hora'].dt.date.between(var_dict['dtinicial'],var_dict['dtfinal'])]          

                pass

            #Contagem

            codigos=df[tabela]['SKU'].unique().tolist()

            #contagem
            with tab1.container():

                var_dict['produto']=len(df['Produto'].loc[df['Produto']['Status']=='ATIVO'])
                var_dict['contagem']=len(df['STK']['SKU'].unique().tolist())
                var_dict['dif']=var_dict['contagem']-var_dict['produto']

                card1,card2,card3=st.columns(3)

                with card1.container():

                    st.metric(label='Qtde (SKU) - Ativo',value=Moeda.Numero(var_dict['produto']))

                    pass

                with card2.container():

                    st.metric(label='Itens Contados',value=Moeda.Numero(var_dict['contagem']))

                    pass

                with card3.container():

                    st.metric(label='À Contar',value=Moeda.Numero(var_dict['dif']))

                    pass

                
                df['contagem']=df['Produto'].loc[(~df['Produto']['SKU'].isin(codigos))&(df['Produto']['Status']=='ATIVO')]

                div4,div5=st.columns(2)

                with div4.container():

                    colunas=['Fabricante']
                    col_leach='SKU'
                    temp_df=df['contagem'].loc[df['contagem']['Fabricante'].str.strip()!='PADRÃO'].groupby(colunas,as_index=False).agg({col_leach:'count'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)

                    bar=px.pie(temp_df.head(),names=colunas[-1],values=col_leach,labels=True,title='Fabricante (SKU)')
                    st.plotly_chart(bar,use_container_width=True)

                    pass

                pass

                with div5.container():

                    colunas=['Linha']
                    col_leach='SKU'
                    temp_df=df['contagem'].loc[df['contagem']['Fabricante'].str.strip()!='PADRÃO'].groupby(colunas,as_index=False).agg({col_leach:'count'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)

                    bar=px.bar(temp_df.head(),x=colunas[-1],y=col_leach,text_auto=True,title='Linha (SKU)')
                    st.plotly_chart(bar,use_container_width=True)

                    pass
                
                st.dataframe(df['contagem'],use_container_width=True,hide_index=True)

                pass
            
            #divergência
            with tab2.container():

                df['divergencia']=df[tabela].loc[df[tabela]['SKU'].isin(codigos)]
                df['divergencia']['Qtde']=df['divergencia']['Qtde'].astype(int)
                df['divergencia']['Contagem']=df['divergencia']['Contagem'].astype(int)

                card1,card2,card3=st.columns(3)

                with card1.container():
                    
                    var_dict['qtde']=df['divergencia'].loc[df['divergencia']['Contagem']==1,'Qtde'].sum()

                    st.metric(label='1º Contagem',value=Moeda.Numero(var_dict['qtde']))

                    pass

                with card2.container():
                    
                    var_dict['qtde']=df['divergencia'].loc[df['divergencia']['Contagem']==2,'Qtde'].sum()

                    st.metric(label='2º Contagem',value=Moeda.Numero(var_dict['qtde']))

                    pass

                with card3.container():
                    
                    var_dict['qtde']=df['divergencia'].loc[df['divergencia']['Contagem']==3,'Qtde'].sum()

                    st.metric(label='3º Contagem',value=Moeda.Numero(var_dict['qtde']))

                    pass

                with st.container():

                    radio_selected=st.radio(label='Agrupamento',options=['Normal','Conferente','Contagem'])

                    if radio_selected=='Normal':

                        colunas=['Conferente','Rua','Bloco','Nível','Apartamento','Contagem']
                        col_leach='Qtde'
                        temp_df=df['divergencia'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                        col=colunas[-1]
                        del colunas[-1]
                        temp_df=temp_df.pivot(index=colunas,columns=col,values=col_leach).reset_index()

                        pass

                    elif radio_selected=='Conferente':

                        colunas=['Rua','Bloco','Nível','Apartamento','Conferente']
                        col_leach='Qtde'
                        temp_df=df['divergencia'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                        #temp_df['Conferente']=temp_df.apply(lambda info: str(info['Contagem'])+'-'+info['Conferente'],axis=1)
                        col=colunas[-1]
                        del colunas[-1]
                        temp_df=temp_df.pivot(index=colunas,columns=col,values=col_leach).reset_index()


                        pass

                    else:


                        colunas=['Rua','Bloco','Nível','Apartamento','Contagem']
                        col_leach='Qtde'
                        temp_df=df['divergencia'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                        #temp_df['Conferente']=temp_df.apply(lambda info: str(info['Contagem'])+'-'+info['Conferente'],axis=1)
                        col=colunas[-1]
                        del colunas[-1]
                        temp_df=temp_df.pivot(index=colunas,columns=col,values=col_leach).reset_index()

                        pass

                    st.dataframe(temp_df,use_container_width=True,hide_index=True)

                    data=ExcelDW.DownloadXLSX(temp_df)
                    st.download_button(label='Download',data=data,file_name=f'{radio_selected}.xlsx',key='dw1',type='primary')

                    pass

                with st.expander(label='Locação'):

                    colunas=['SKU','Produto','Rua','Bloco','Nível','Apartamento','Contagem']
                    col_leach='Qtde'
                    temp_df=df['divergencia'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    del colunas[-1]
                    temp_df=temp_df.pivot(index=colunas,columns='Contagem',values='Qtde').reset_index()
                    temp_df['Status']=None
                    temp_df.loc[temp_df['Status'].isnull(),'Status']='VERIFICAR'

                    for i in temp_df.index.tolist():

                        col=[l for l in temp_df.columns.tolist() if str(l).isnumeric()]

                        for c in col:

                            temp_df.loc[temp_df[c].isnull(),c]=0
                            var_max=temp_df.loc[i,col[-1]].sum()
                            var_min=temp_df.loc[i,c].sum()

                            if c!=col[-1] or var_min<=0:

                                continue


                            status='VERIFICAR' if var_max!=var_min else 'OK'
                            
                            temp_df.loc[i,'Status']=status
                            temp_df.loc[i,'Estoque Físico']=var_min

                            pass

                        pass

                    st.dataframe(temp_df.loc[temp_df['Status']=='VERIFICAR'],use_container_width=True,hide_index=True)

                    data=ExcelDW.DownloadXLSX(temp_df)
                    st.download_button(label='Download',data=data,file_name=f'Locação Divergênte.xlsx',key='dw2',type='primary')                    

                    pass
                
                pass
            
            #ok
            with tab3.container():

                card1,card2,card3,=st.columns(3)
                
                df['ok']=temp_df.loc[temp_df['Status']=='OK']

                with card1.container():

                    st.metric(label='Qtde (SKU) - Ativo',value=Moeda.Numero(var_dict['produto']))

                    pass

                with card2.container():

                    var_dict['ok']=len(df['ok']['SKU'].unique().tolist())
                    st.metric(label='Qtde (SKU) - OK',value=Moeda.Numero(var_dict['ok']))

                    pass


                with card3.container():

                    var_dict['dif']=var_dict['ok']-var_dict['produto']
                    st.metric(label='Qtde à Verificar',value=Moeda.Numero(var_dict['dif']))

                    pass                
                
                div1,div2,div3=st.columns(3)

                with st.container():

                    var_dict['perc']=round(var_dict['ok']/var_dict['produto'],4)*100 if var_dict['ok']>0 else 0

                    bar=go.Figure(go.Indicator(

                        mode='gauge+number',
                        value=var_dict['perc'],
                        title={'text':'Acuracidade de STK'},
                        gauge={'axis':{'range':[0,100]}}

                    ))

                    st.plotly_chart(bar)

                    pass
                                
                st.dataframe(df['ok'],use_container_width=True,hide_index=True)

                data=ExcelDW.DownloadXLSX(temp_df)
                st.download_button(label='Download',data=data,file_name=f'Contagem OK.xlsx',key='dw3',type='primary')                

                with st.expander('Consolidado'):

                    if len(df['ok'])>0:

                        colunas=['SKU','Produto']
                        col_leach='Estoque Físico'
                        temp_df=df['ok'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                        temp_df=temp_df.merge(df['Estoque'][['SKU','Qtde CMP']],on='SKU',how='inner')
                        temp_df['Ajustar']=temp_df.apply(lambda info: float(info[col_leach])-float(info['Qtde CMP']),axis=1)
                        temp_df=df['Produto'][['Fabricante','Linha','SKU']].merge(temp_df,on='SKU',how='inner')

                        st.dataframe(temp_df,use_container_width=True,hide_index=True)

                        data=ExcelDW.DownloadXLSX(temp_df)
                        st.download_button(label='Download',data=data,file_name=f'Acuracidade.xlsx',key='dw4',type='primary')

                        pass                  

                    pass

                pass

            style_metric_cards()
                      
            pass

        if btn_refresh:

            st.cache_data.clear()
            st.rerun()

            pass

        pass


    pass