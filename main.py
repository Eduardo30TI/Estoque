import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import time
import socket as s
import os
from glob import glob
import DataSet.data
import Telas as gui
import DataSet.data as dt

icon_path=os.path.join(os.getcwd(),'Icones','*.*')
icon=glob(icon_path)

if len(icon)>0:

    with open(icon[-1],'rb') as file:

        st.set_page_config(page_title='Controle STK',layout='wide',page_icon=file.read())

        pass

    pass

else:

    st.set_page_config(page_title='Controle STK',layout='wide')

    pass

class Login:

    def __init__(self) -> None:

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)

        self.img_path=os.path.join(os.getcwd(),'Imagens','*.*')
        self.img=glob(self.img_path)

        pass


    def main(self):

        temp_path=os.path.join(self.path_base,'log.txt')
        arq=glob(temp_path)

        if len(arq)<=0:

            self.log()

            pass

        else:

            tela=gui.Menu()
            tela.main()
            
            pass

        pass


    def log(self):

        placeholder=st.empty()

        var_dict=dict()

        with placeholder.container():

            div1,div2,div3=st.columns([1,2,1])

            with div2.container():

                img1,img2,img3=st.columns(3)

                with img2.container():

                    if len(self.img)>0:

                        with open(self.img[-1],'rb') as file:
                            
                            st.image(file.read(),width=250)

                            pass

                        pass

                    pass

                st.title('Login')
                st.markdown('----')

                var_dict['email']=st.text_input('E-mail',key='email').upper()
                var_dict['senha']=st.text_input('Senha',type='password',key='senha').upper()

                btn_log=st.button('Conectar',use_container_width=True,key='btn_log',type='primary')

                pass

            pass

        if btn_log:

            resp=self.validarCampos(var_dict)

            if resp!=None:

                mensagem=div2.warning(resp)
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                df=dt.usuario()

                cont=len(df.loc[(df['ID Usuário'].str.strip()==var_dict['senha'])&(df['E-mail Usuário'].str.strip()==var_dict['email'])])

                if cont>0:
                    
                    temp_path=os.path.join(self.path_base,'log.txt')

                    with open(temp_path,'w') as file:

                        file.write(var_dict['email'])

                        pass

                    mensagem=div2.success('Seja bem vindo')
                    time.sleep(1)
                    mensagem.empty()
                    placeholder.empty()
                    streamlit_js_eval(js_expressions='parent.window.location.reload()')

                    pass


                else:


                    mensagem=div2.warning('Usuário não encontrado!')
                    time.sleep(1)
                    mensagem.empty()

                    pass

                pass

            pass

        pass


    def validarCampos(self,campos:dict):

        temp_dict={0:None}

        for k,v in campos.items():

            if v=='':

                temp_dict[0]=f'Informe {k}'

                break

            pass

        return temp_dict[0]

        pass

    pass


app=Login()
app.main()