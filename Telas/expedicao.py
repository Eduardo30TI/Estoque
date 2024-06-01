import streamlit as st
import os
import socket as s
import DataSet.data as dt
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
from Moeda import Moeda
import plotly.graph_objects as go
from DownloadXLSX import ExcelDW
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval
import time
import pandas as pd
import plotly.graph_objects as go

var_dict=dict()

class Expedicao:

    def __init__(self) -> None:

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)

        pass


    def main(self):

        placeholder=st.empty()

        global var_dict

        with placeholder.container():

            with st.sidebar:
                
                tabela='Romaneio'
                df=dt.expedicao()

                var_dict['roteiros']=len(df[tabela]['Romaneio'].unique().tolist())

                lista=df['Picking']['Romaneio'].unique().tolist()
                df[tabela]=df[tabela].loc[~df[tabela]['Romaneio'].isin(lista)]                    
                
                btn_refresh=st.button('Atualizar',type='primary',key='btn_refresh',use_container_width=True)

                for c in ['Rota','Motorista']:

                    lista=df[tabela][c].unique().tolist()
                    filter=st.multiselect(label=c,options=lista,placeholder='Escolha as opções')

                    for j in ['Romaneio','Fila','Picking']:

                        df[j]=df[j].loc[df[j][c].isin(filter)] if len(filter)>0 else df[j]

                        pass

                    pass           

                pass

            st.title('Expedição')
            tab1,tab2,tab3,tab4=st.tabs(['Roteiro','Picking','Separação','Faturado'])            

            #roteiro
            with tab1.container():

                card1,card2,card3=st.columns(3)
                card4,card5=st.columns(2)

                var_dict['cliente']=len(df[tabela]['ID Cliente'].unique().tolist())
                var_dict['veiculos']=len(df[tabela]['Veículo'].unique().tolist())
                var_dict['nfe']=len(df[tabela]['NFe'].unique().tolist())
                var_dict['peso']=df[tabela]['Peso Bruto KG'].astype(float).sum()
                var_dict['valor']=df[tabela]['Total Venda'].astype(float).sum() 

                with card1.container():

                    st.metric(label='Entregas',value=Moeda.Numero(var_dict['cliente']))

                    pass

                with card2.container():

                    st.metric(label='Veículos',value=Moeda.Numero(var_dict['veiculos']))

                    pass

                with card3.container():

                    st.metric(label='NFe',value=Moeda.Numero(var_dict['veiculos']))

                    pass

                with card4.container():

                    st.metric(label='Tonelada',value=Moeda.FormatarMoeda(var_dict['peso']))

                    pass

                with card5.container():

                    st.metric(label='Valor R$',value=Moeda.FormatarMoeda(var_dict['valor']))

                    pass

                div1,div2=st.columns(2)

                with div1.container():

                    colunas=['Rota','NFe']
                    col_leach='Total Venda'
                    df[tabela][col_leach]=df[tabela][col_leach].astype(float)
                    temp_df=df[tabela].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    col_leach=colunas[-1]
                    del colunas[-1]
                    temp_df=temp_df.groupby(colunas,as_index=False).agg({col_leach:'count'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)

                    bar=px.bar(temp_df,x=colunas[0],y=col_leach,title=colunas[-1],text_auto=True)
                    st.plotly_chart(bar,use_container_width=True)

                    pass

                pass


                with div2.container():

                    colunas=['Motorista','NFe']
                    col_leach='Total Venda'
                    df[tabela][col_leach]=df[tabela][col_leach].astype(float)
                    temp_df=df[tabela].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    col_leach=colunas[-1]
                    del colunas[-1]
                    temp_df=temp_df.groupby(colunas,as_index=False).agg({col_leach:'count'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)
                    
                    st.dataframe(temp_df,use_container_width=True,hide_index=True)

                    pass
                
                colunas=['Data da Montagem','Romaneio','Rota','Motorista','Veículo']
                
                for c in ['Total Venda','Peso Bruto KG']:

                    df[tabela][c]=df[tabela][c].astype(float)

                    pass

                temp_df=df[tabela].groupby(colunas,as_index=False).agg({'Total Venda':'sum','Peso Bruto KG':'sum'})

                for c in ['ID Cliente','NFe']:

                    colunas=['Romaneio',c]
                    col_leach='Total Venda'
                    df[tabela][col_leach]=df[tabela][col_leach].astype(float)
                    df['temp']=df[tabela].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    col_leach=colunas[-1]
                    del colunas[-1]

                    df['temp']=df['temp'].groupby(colunas,as_index=False).agg({col_leach:'count'})

                    temp_df=temp_df.merge(df['temp'],on='Romaneio',how='inner')

                    pass
                
                col_dict={'Total Venda':'Valor','Peso Bruto KG':'Peso','ID Cliente':'Entregas','NFe':'Notas'}
                temp_df.rename(columns=col_dict,inplace=True)

                st.dataframe(temp_df,use_container_width=True,hide_index=True)

                pass            

            #picking
            with tab2.container():

                lista=df['Picking']['Romaneio'].unique().tolist()
                                                
                lista=df[tabela]['Romaneio'].loc[~df[tabela]['Romaneio'].isin(lista)].unique().tolist()
                roteiros=st.multiselect(label='Romaneio',key='text1',options=lista,placeholder='Informe o Romaneio')

                btn1,btn2,btn3,btn4=st.columns([1,1,1,4])
                
                btn_sep=btn1.button('Separador',key='btn_sep',type='primary',use_container_width=True)
                btn_cad=btn2.button('Cadastro',key='btn_cad',type='primary',use_container_width=True)

                if 'separador' in var_dict.keys():

                    st.header(f"Separador: {var_dict['separador']}")

                    btn_save=btn3.button('Salvar',key='btn_save',type='secondary',use_container_width=True)

                    if btn_save==True and len(roteiros)>0:

                        for c in df['Picking'].columns.tolist():

                            df['Picking'][c]=df['Picking'][c].astype(str)

                            pass

                        colunas=['Romaneio','Rota','Data da Montagem','Motorista']
                        temp_df=df['Romaneio'].groupby(colunas,as_index=False).agg({'Total Venda':'sum','Peso Bruto KG':'sum'})

                        temp_df=temp_df.loc[temp_df['Romaneio'].isin(roteiros)]

                        for c in ['ID Cliente','SKU']:

                            colunas=['Romaneio','Rota','Data da Montagem','Motorista',c]
                            col_leach='Total Venda'
                            df['temp']=df['Romaneio'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                            col_leach=colunas[-1]
                            df['temp']=df['temp'].groupby(colunas[0],as_index=False).agg({col_leach:'count'})

                            temp_df=temp_df.merge(df['temp'],on=colunas[0],how='inner')

                            pass
                        
                        col_dict={'Total Venda':'Valor','Peso Bruto KG':'Peso','ID Cliente':'Entrega','SKU':'Produtos'}

                        temp_df.rename(columns=col_dict,inplace=True)
                        temp_df['Separador']=var_dict['separador']
                        temp_df['Status']='EM SEPARAÇÃO'
                        temp_df['Observações']=None
                        temp_df['Data e Hora']=datetime.now().date()

                        colunas=df['Picking'].columns.tolist()

                        temp_df=temp_df[colunas]

                        for c in temp_df.columns.tolist():

                            temp_df[c]=temp_df[c].astype(str)

                            pass

                        temp_df=pd.concat([temp_df,df['Picking']],axis=0,ignore_index=True)
                        
                        dt.insert(temp_df,'Picking')
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()

                        pass                                     

                    pass

                temp_df=df[tabela].loc[df[tabela]['Romaneio'].isin(roteiros)]

                card1,card2,card3,card4=st.columns(4)
                var_dict['pedidos']=len(temp_df['Pedido'].unique().tolist())
                var_dict['clientes']=len(temp_df['ID Cliente'].unique().tolist())
                var_dict['mix']=len(temp_df['SKU'].unique().tolist())
                var_dict['total']=temp_df['Total Venda'].sum()

                with card1.container():

                    st.metric(label='Pedido(s)',value=Moeda.Numero(var_dict['pedidos']))

                    pass

                with card2.container():

                    st.metric(label='Cliente(s)',value=Moeda.Numero(var_dict['clientes']))

                    pass

                with card3.container():

                    st.metric(label='Produto(s)',value=Moeda.Numero(var_dict['mix']))

                    pass

                with card4.container():

                    st.metric(label='Valor R$',value=Moeda.FormatarMoeda(var_dict['total']))

                    pass

                div1,div2=st.columns(2)

                with div1.container():

                    colunas=['Rota']
                    col_leach='Total Venda'

                    bar=px.bar(temp_df.groupby(colunas,as_index=False).agg({col_leach:'sum'}),x=colunas[-1],y=col_leach,text_auto=True)
                    st.plotly_chart(bar,use_container_width=True)

                    pass

                with div2.container():

                    colunas=['Motorista']
                    col_leach='Total Venda'
                    df['temp']=temp_df.groupby(colunas,as_index=False).agg({col_leach:'sum'})

                    st.dataframe(df['temp'],use_container_width=True,hide_index=True)

                    colunas=['Pedido','SKU']
                    col_leach='Total Venda'
                    df['temp']=temp_df.groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    df['temp']=df['temp'].groupby(colunas[0],as_index=False).agg({col_leach:'sum',colunas[-1]:'count'})
                    
                    
                    st.dataframe(df['temp'],use_container_width=True,hide_index=True)                    

                    pass
                
                colunas=['SKU']
                col_leach='Qtde'
                temp_df[col_leach]=temp_df[col_leach].astype(float)
                df['temp']=temp_df.groupby(colunas,as_index=False).agg({col_leach:'sum'})
                                 
                df['temp']=df['Produto'].merge(df['temp'],on='SKU',how='inner')
                df['temp']['Caixa']=df['temp'].apply(lambda info: int(info['Qtde']/float(info['Fator CX'])) if float(info['Fator CX'])>0 else 0,axis=1)
                df['temp']['Unidade']=df['temp'].apply(lambda info: ((info['Qtde']/float(info['Fator CX']))-info['Caixa'])*float(info['Fator CX']) if float(info['Fator CX'])>0 else 0,axis=1)
                df['temp'].sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)

                st.dataframe(df['temp'],use_container_width=True,hide_index=True)

                pass

            #separacao
            with tab3.container():
                
                var_dict['entregas']=len(df['Picking']['Romaneio'].unique().tolist())
                var_dict['separado']=len(df['Picking'].loc[df['Picking']['Status']=='SEPARADO','Romaneio'].unique().tolist())
                var_dict['dif']=var_dict['entregas']-var_dict['roteiros']
                var_dict['perc']=round(var_dict['entregas']/var_dict['roteiros'],4)*100 if var_dict['roteiros']>0 else 0

                div1,div2,div3=st.columns([2,2,1])

                with div1.container():

                    bar=go.Figure(go.Indicator(

                        mode='gauge+number',
                        value=var_dict['perc'],
                        title={'text':'Em Separação'},
                        gauge={'axis':{'range':[0,100]}}
                    ))

                    st.plotly_chart(bar,use_container_width=True)                   

                    pass

                with div2.container():

                    var_dict['perc']=round(var_dict['separado']/var_dict['entregas'],4)*100 if var_dict['entregas']>0 else 0

                    bar=go.Figure(go.Indicator(

                        mode='gauge+number',
                        value=var_dict['perc'],
                        title={'text':'Separado'},
                        gauge={'axis':{'range':[0,100]}}
                    ))

                    st.plotly_chart(bar,use_container_width=True) 


                    pass


                with div3.container():

                    st.metric(label='Roteiros',value=Moeda.Numero(var_dict['roteiros']))
                    st.metric(label='Em Separação',value=Moeda.Numero(var_dict['entregas']))
                    st.metric(label='À Separar',value=Moeda.Numero(var_dict['dif']))
                    st.metric(label='Separado',value=Moeda.Numero(var_dict['separado']))

                    pass
                
                lista=df['Picking']['Romaneio'].unique().tolist()
                selected=st.multiselect(label='Romaneio',options=lista,key='select2',placeholder='Escolhas as opções')

                temp_df=df['Picking'].loc[df['Picking']['Romaneio'].isin(selected)] if len(selected)>0 else df['Picking']

                btn_update=st.button(label='Alterar',key='btn_update')

                if len(selected)>0:
                                        
                    if 'status' in var_dict.keys():

                        df['Picking'].loc[df['Picking']['Romaneio'].isin(selected),'Status']=var_dict['status']

                        if 'observacao' in var_dict.keys():

                            df['Picking'].loc[df['Picking']['Romaneio'].isin(selected),'Observações']=var_dict['observacao']

                            pass

                        for c in df['Picking'].columns.tolist():

                            df['Picking'][c]=df['Picking'][c].astype(str)

                            pass

                        dt.insert(df['Picking'],'Picking')

                        pass

                    pass
                
                temp_df['Faturado']='N'
                lista=df['Fila']['Romaneio'].unique().tolist()
                temp_df.loc[temp_df['Romaneio'].isin(lista),'Faturado']='S'

                on=st.toggle(label='Não Faturado',value=False)

                temp_df=temp_df.loc[temp_df['Faturado']=='N'] if on==True else temp_df

                st.dataframe(temp_df,use_container_width=True,hide_index=True)

                pass

            #faturado
            with tab4.container():

                var_dict['roteiros']=len(df['Fila']['Romaneio'].unique().tolist())
                var_dict['pedidos']=df['Fila']['Pedido'].astype(float).sum()
                var_dict['entregas']=df['Fila']['Cliente'].astype(float).sum()
                var_dict['produtos']=df['Fila']['MIX'].astype(float).sum()

                card1,card2,card3,card4=st.columns(4)

                with card1.container():

                    st.metric(label='Roteiros',value=Moeda.Numero(var_dict['roteiros']))

                    pass

                with card2.container():

                    st.metric(label='Pedidos',value=Moeda.Numero(var_dict['pedidos']))

                    pass

                with card3.container():

                    st.metric(label='Entregas',value=Moeda.Numero(var_dict['entregas']))

                    pass

                with card4.container():

                    st.metric(label='Produtos',value=Moeda.Numero(var_dict['produtos']))

                    pass

                div1,div2=st.columns(2)

                with div1.container():

                    colunas=['Rota']
                    col_leach='Cliente'
                    df['Fila'][col_leach]=df['Fila'][col_leach].astype(float)
                    temp_df=df['Fila'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)
                    bar=px.bar(temp_df,x=colunas[-1],y=col_leach,text_auto=True,title=colunas[-1])
                    st.plotly_chart(bar,use_container_width=True)

                    pass


                with div2.container():

                    colunas=['Motorista']
                    col_leach='Cliente'
                    df['Fila'][col_leach]=df['Fila'][col_leach].astype(float)
                    temp_df=df['Fila'].groupby(colunas,as_index=False).agg({col_leach:'sum'})
                    temp_df.sort_values(col_leach,ascending=False,ignore_index=True,inplace=True)


                    st.dataframe(temp_df,use_container_width=True,hide_index=True)                    

                    pass                         

                st.dataframe(df['Fila'],use_container_width=True,hide_index=True)

                pass

            style_metric_cards()

            pass

        if btn_refresh:

            st.cache_data.clear()
            st.rerun()

            pass

        if btn_sep:

            self.telaLeach()

            pass

        if btn_cad:

            self.telaCadastro()

            pass

        if btn_update:

            self.telaStatus()
            
            pass       

        pass


    @st.experimental_dialog(title='Separador')
    def telaLeach(self):

        st.markdown('----')

        df=dt.separador()

        lista=[] if len(df)<=0 else df['Separador'].unique().tolist()
        selected=st.selectbox(label='Separador',options=lista,key='select1',placeholder='Escolha o Separador')

        btn_select=st.button('Selecionar',key='btn_select',type='primary')

        if btn_select:

            var_dict['separador']=selected
            time.sleep(1)
            st.rerun()

            pass

        pass

    @st.experimental_dialog(title='Adicionar Separador')
    def telaCadastro(self):

        st.markdown('----')
      
        df=dt.separador()

        st.dataframe(df,use_container_width=True,hide_index=True)

        div1,div2=st.columns([1,3])

        global var_dict

        with div1.container():

            var_dict['id']=st.text_input(label='ID',value=len(df)+1,disabled=True)

            pass

        with div2.container():

            var_dict['nome']=st.text_input(label='Nome Completo',key='txt2').upper().strip()

            pass

        btn_save=st.button('Salvar',key='btn_save',type='primary')

        if btn_save:

            resp=self.validarCampos(var_dict)

            if resp!=None:

                mensagem=st.warning(resp)
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                cont=len(df.loc[df['Separador']==var_dict['nome']])

                if cont>0:

                    mensagem=st.warning('Separador já consta cadastrado')
                    time.sleep(2)
                    mensagem.empty()

                    pass

                else:

                    df.loc[len(df)]=[var_dict['id'],var_dict['nome']]
                    dt.insert(df,'Separador')

                    mensagem=st.success('Dados cadastrado com sucesso!')
                    time.sleep(1)
                    mensagem.empty()
                    st.rerun()

                    pass                

                pass

            pass

        pass

    @st.experimental_dialog(title='Atualizar Status')
    def telaStatus(self):

        st.markdown('----')

        global var_dict

        on=st.toggle('Observação',value=False)

        seletecd=st.selectbox(label='Status',options=['EM SEPARAÇÃO','EM ANÁLISE','SEPARADO'])
                        
        if on==True:

            var_dict['observacao']=st.text_area(label='Observação',key='text_obs').upper()

            pass

        btn=st.button(label='Selecionar',type='primary',key='select1')

        if btn:

            if seletecd!=None:

                var_dict['status']=seletecd

                mensagem=st.success('Status Ajustado')
                time.sleep(1)
                mensagem.empty()
                st.rerun()
                
                pass
            
            pass

        pass

    def validarCampos(self,campos:dict):

        temp=None

        for k,v in campos.items():

            if v=='':

                temp=f'Informe {k}'

                break

            pass

        return temp

        pass

    pass