import streamlit as st
from geopy.geocoders import Nominatim
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AQICN_TOKEN = os.getenv('AQICN_TOKEN')

# Funções definidas anteriormente
def get_coordinates(address):
    geolocator = Nominatim(user_agent="air_quality_app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_air_quality(lat, lon, token):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "ok":
        return data["data"]
    else:
        return None
    
def get_level(aqi):
    if aqi <= 50:
        level = "boa"
    elif 51 <= aqi <= 100:
        level = "moderada"
    elif 101 <= aqi <= 150:
        level = "insalubre"
    else:
        level = "ruim"
    return level

def generate_call_to_action(aqi, address):

    st.write("Notamos um aumento de 30% nas queimadas na Amazônia na última semana\n")
    st.write("Em setembro de 2019, queimadas na Amazônia contribuíram para a piora da qualidade do ar em sua região.\n ")
    st.write("Se essa tendência continuar, podemos esperar uma piora na qualidade do ar nos próximos dias.\n ")
    st.write("É hora de agir! Apoie iniciativas e compartilhe informações para combater a poluição:\n")
    st.write("Lista de Ações: \n")
    st.write("1. Assinar a petição Salve a Amazônia - [Link]\n")
    st.write("2. Apoiar a ONG Amigos da Floresta - [Link] \n")
    st.write("3. Participar do webinar Impacto das Queimadas em [data] - [Link]\n")
    st.write("4. Receber notificação com links para apoiar movimentos de melhora quando as queimadas pioraren\n")
    st.write("5. Compartilhar esta mensagem com amigos e familiares")

# Interface do Streamlit
st.title("Qualidade do Ar na Sua Localidade")

address = st.text_input("Digite seu endereço ou cidade:")

if address:
    lat, lon = get_coordinates(address)
    if lat and lon:
        token = AQICN_TOKEN
        data = get_air_quality(lat, lon, token)
        if data:
            aqi = data["aqi"]
            st.write(f"### Índice de Qualidade do Ar (IQA): {aqi}")
            # Exibir informações adicionais
            if "dominentpol" in data:
                st.write(f"**Poluente dominante:** {data['dominentpol']}")
            # Gerar e exibir a chamada para ação
            level = get_level(aqi)
            st.write(f"## A qualidade do ar em {address} hoje é {level} com um IQA de {aqi} ")
            generate_call_to_action(aqi, address)
        else:
            st.error("Não foi possível obter os dados de qualidade do ar para esta localização.")
    else:
        st.error("Endereço não encontrado. Por favor, verifique e tente novamente.")
