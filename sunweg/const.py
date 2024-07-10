"""Sunweg API constants."""

SUNWEG_URL = "https://api.sunweg.net/v2/"
"""SunWEG API URL"""
SUNWEG_LOGIN_PATH = "login/autenticacao"
"""SunWEG API login path"""
SUNWEG_PLANT_LIST_PATH = (
    "getpaineloperacao?procurar=&integrador="
    + "&franqueado=&manutencao=&portal=&alarme=&"
    + "planos=%5B0,1,2,3,4%5D&status=%5B1,2,3,4,5%5D&"
    + "limite=100&situacao=&paginaAtual=1"
)
"""SunWEG API list plants path"""
SUNWEG_PLANT_DETAIL_PATH = "viewresumov2?agrupado=false&id="
"""SunWEG API plant details path"""
SUNWEG_INVERTER_DETAIL_PATH = "inversores/view?id="
"""SunWEG API inverter details path"""
SUNWEG_MONTH_STATS_PATH = "usinas/graficomes?"
"""SunWEG API month history path"""
