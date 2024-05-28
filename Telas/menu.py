import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_js_eval import streamlit_js_eval
import gspread as gc
import time
from decouple import config
import pandas as pd
import socket as s
import os
from glob import glob
import Telas as gui
import shutil

class Menu:

    def __init__(self) -> None:

        self.IP=s.gethostbyname(s.gethostname())
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)

        pass


    def main(self):

        placeholder=st.empty()

        with placeholder.container():

            with st.sidebar:

                selected=option_menu(menu_title='Menu',options=['Inventário','Sair'],menu_icon='list',icons=['box-seam-fill','box-arrow-right'])

                pass

            pass

        if selected=='Inventário':

            tela=gui.Controle()
            tela.main()

            pass

        elif selected=='Sair':

            shutil.rmtree(self.path_base)
            streamlit_js_eval(js_expressions='parent.window.location.reload()')

            pass

        pass    


    pass