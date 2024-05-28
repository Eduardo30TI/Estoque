import streamlit as st
from streamlit_option_menu import option_menu
import gspread as gc
import time
from decouple import config
import pandas as pd
import socket as s
import os
from glob import glob
import Telas as gui

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

                selected=option_menu(menu_title='Menu',options=['Inventário'],menu_icon='list',icons=['box-seam-fill'])

                pass

            pass

        if selected=='Inventário':

            tela=gui.Controle()
            tela.main()

            pass

        pass    


    pass