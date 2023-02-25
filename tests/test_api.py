from datetime import datetime
from unittest.mock import patch
import pytest

from requests import Response

from sunweg.api import APIHelper, SunWegApiError

from .common import INVERTER_MOCK, PLANT_MOCK

auth_success_response = Response()
auth_success_response.status_code = 200
auth_success_response._content = b'{"success":true,"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NzcyNjQzODEsImlzcyI6Imh0dHA6XC9cL2llcy5nb3YiLCJleHAiOjE2Nzc4NjkxODEsImhvc3QiOiIxOTEuMzMuMTg1LjEyOSIsImRhdGEiOnsidXN1YXJpb2lkIjo2NTQzLCJpZHBlcmZpbCI6NiwiaWRyZWxhY2lvbmFkbyI6MTAxOCwiaWRmcmFucXVlYWRvIjpudWxsLCJhbGVydGFzIjp0cnVlLCJjb250cm9sZSI6dHJ1ZSwiZnJlZSI6ZmFsc2V9fQ.907NnIUaMhVl2HVzAuzPTvVdD-huHNg932Eu2zj7-0"}'

auth_fail_response = Response()
auth_fail_response.status_code = 200
auth_fail_response._content = b'{"success":false,"message":"Error message"}'

list_plant_success_none_response = Response()
list_plant_success_none_response.status_code = 200
list_plant_success_none_response._content = (
    b'{"success":true,"capacidade":29,"usinas":[]}'
)

list_plant_success_1_response = Response()
list_plant_success_1_response.status_code = 200
list_plant_success_1_response._content = b'{"success":true,"capacidade":29,"usinas":[{"ultimaleitura":"2023-02-25 06:59:52","tempocoleta":60,"id":16925,"alarmar":1,"situacao":1,"nome":"Plant Name","endereco":"Plant Address","bairro":"Plant County","cidade":"Plant City","estado":"Plant State","datainstalacao":"2023-02-14","capacidade":"29","latitude":"-15","longitude":"-47","fuso":-3,"plano":"Free","qntdinvsem":0,"qntdinv":1,"edaytotal":"0.0000","potencia":"0.000","status":1,"eventos":[],"usinaDesligada":false,"ultimaleituraHora":"06:59","ultimaleituraData":"25\\/02\\/2023","invManut":[]}]}'

list_plant_success_2_response = Response()
list_plant_success_2_response.status_code = 200
list_plant_success_2_response._content = b'{"success":true,"capacidade":29,"usinas":[{"ultimaleitura":"2023-02-25 06:59:52","tempocoleta":60,"id":16925,"alarmar":1,"situacao":1,"nome":"Plant Name","endereco":"Plant Address","bairro":"Plant County","cidade":"Plant City","estado":"Plant State","datainstalacao":"2023-02-14","capacidade":"29","latitude":"-15","longitude":"-47","fuso":-3,"plano":"Free","qntdinvsem":0,"qntdinv":1,"edaytotal":"0.0000","potencia":"0.000","status":1,"eventos":[],"usinaDesligada":false,"ultimaleituraHora":"06:59","ultimaleituraData":"25\\/02\\/2023","invManut":[]},{"ultimaleitura":"2023-02-25 06:59:52","tempocoleta":60,"id":16925,"alarmar":1,"situacao":1,"nome":"Plant Name","endereco":"Plant Address","bairro":"Plant County","cidade":"Plant City","estado":"Plant State","datainstalacao":"2023-02-14","capacidade":"29","latitude":"-15","longitude":"-47","fuso":-3,"plano":"Free","qntdinvsem":0,"qntdinv":1,"edaytotal":"0.0000","potencia":"0.000","status":1,"eventos":[],"usinaDesligada":false,"ultimaleituraHora":"06:59","ultimaleituraData":"25\\/02\\/2023","invManut":[]}]}'

error_401_response = Response()
error_401_response.status_code = 401
error_401_response.reason = "Unauthorized"

error_500_response = Response()
error_500_response.status_code = 500
error_500_response.reason = "Internal server error"

plant_success_response = Response()
plant_success_response.status_code = 200
plant_success_response._content = b'{"success":true,"usinas":{"id":16925,"idcliente":1018,"idorg":1,"nome":"Plant Name","descricao":"","capacidade":"29.1","latitude":"-15","longitude":"-47","datainstalacao":"2023-02-14","responsavel":null,"contatotel":null,"contatoemail":null,"numero":null,"cep":"70000000","complemento":"","endereco":"Plant Address","bairro":"Plant County","cidade":"Plant City","estado":"Plant State","pais":"Plant Country","parametros":"","ultimaleitura":"2023-02-25 08:04:22","video1":"","video2":"","video3":"","plantabaixa":null,"situacao":1,"date_inc":"2023-02-14 16:57:24.276796","logoparceiro":1,"uid":null,"tempocoleta":60,"alias":"","logo":"","frasefinal":"","configpainel":"","cor":"","url":"","alarmar":1,"investimento":"118300.00","valortarifa":"0.00","fatorco2":"0.5300000","fatorarvore":"0.0136000","fatorkm":"5.3500000","idfranqueado":null,"calculapr":0,"idplano":0,"datamedidor":null,"fuso":-3,"pvanalyticsok":"0","qntdinv":1,"qntdusinas":75,"ultimafatura":null,"inversores":[{"id":21255,"idefusina":16925,"nome":"Inverter Name","descricao":"","esn":"1234ABC","parametros":"","situacao":1,"err":1,"visualiza":1,"modelo":"","tensaoca":242,"temperatura":80,"esnlogger":"","idmodbus":null,"strings":[{"id":109563,"idinversor":21255,"nome":"ST 01","nomemppt":"MPPT 01","situacao":1,"variaveltensao":"Upv1","variavelcorrente":"Ipv1"},{"id":109564,"idinversor":21255,"nome":"ST 02","nomemppt":"MPPT 01","situacao":1,"variaveltensao":"Upv2","variavelcorrente":"Ipv2"},{"id":109565,"idinversor":21255,"nome":"ST 03","nomemppt":"MPPT 02","situacao":1,"variaveltensao":"Upv3","variavelcorrente":"Ipv3"},{"id":109566,"idinversor":21255,"nome":"ST 04","nomemppt":"MPPT 02","situacao":1,"variaveltensao":"Upv4","variavelcorrente":"Ipv4"}]}],"codigo":"16925","status":1,"usinaDesligada":false,"foraDoTempo":0},"qntdusinas":75,"contatosUsina":[{"idpapel":2,"descricao":"Respons\\u00e1vel designado pelo propriet\\u00e1rio","nome":"LT Renovaveis","celular":"61981737228","email":"ltrenovaveis@gmail.com","enviarnotificacao":1,"enviarrelatorio":1},{"idpapel":3,"descricao":"Respons\\u00e1vel pela manuten\\u00e7\\u00e3o da usina","nome":"LT Renovaveis","celular":"61981737228","email":"ltrenovaveis@gmail.com","enviarnotificacao":1,"enviarrelatorio":1},{"idpapel":4,"descricao":"Integrador","nome":"","celular":"","email":"","enviarnotificacao":0,"enviarrelatorio":0}],"ultimaAtualizacao":"2023-02-25 08:04:22","AcumuladoPotencia":"0,00 kW","energiaGeradaHoje":"0,00 kWh","energiaacumulada":"23,20 kWh","energiaacumuladanumber":"23.20","taxaPerformance":1.479999999999999982236431605997495353221893310546875,"KWHporkWp":"","PerformanceRate":0,"meteo":{"Ir":"0","velVento":"0","tempAmb":"0","tempMod":"0","tsleitura":"0"},"vegLimp":{"dispositivos":[],"geral":{"nivelVeg":"-1","nivelSuj":"-1"}},"medidores":[],"analytics":false,"reles":[],"irradiancia":0,"reduz_carbono_total":"0,01","reduz_carbono_total_number":0.01229599999999999963840036087958651478402316570281982421875,"arvoresPlantadas":0,"economia":12.7869119999999991676986610400490462779998779296875,"problemas":[{"inversor":{"id":21255,"parametros":"{\\"tensaoCA\\":405,\\"tipoFase\\":\\"Trifasico\\",\\"faseTensao\\":\\"FF\\",\\"temperatura\\":80,\\"numMPPT\\":2,\\"numeroStrings\\":4,\\"potenciaInstalada\\":25}","nome":"INVERSOR01","descricao":"INVERSOR01","esn":"J63T233018RE074"},"mensagem":[{"msg":"- Tens\\u00e3o | Fase A: 11.4 V","msg2":"Tens\\u00e3o est\\u00e1 abaixo de 50% do limite (242 V) ","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":1,"tipo":2},{"msg":"- Tens\\u00e3o | Fase B: 11.7 V","msg2":"Tens\\u00e3o est\\u00e1 abaixo de 50% do limite (242 V) ","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":1,"tipo":2},{"msg":"- Tens\\u00e3o | Fase C: 10.6 V","msg2":"Tens\\u00e3o est\\u00e1 abaixo de 50% do limite (242 V) ","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":1,"tipo":2},{"msg":"- Tens\\u00e3o | Fase B: 11.7 V","msg2":"Tens\\u00e3o est\\u00e1 acima ou igual a 110% da tens\\u00e3o da Fase C (10.6 V) ","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":2,"tipo":3},{"msg":"- Pot\\u00eancia Zerada","msg2":"Pot\\u00eancia do inversor esta zerada","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":1,"tipo":8},{"msg":"- Corrente CC | String: 3","msg2":"A string 3 da Corrente CC est\\u00e1 zerada","acao":"Acionar t\\u00e9cnico de manuten\\u00e7ao para verifica\\u00e7\\u00e3o.","causas":"- Fus\\u00edvel queimado e\\/ou Conector desconectado e\\/ou Chave do inversor desligada.","status":2,"tipo":5},{"msg":"- Tens\\u00e3o CC | String: 3","msg2":"A string 3 da Tens\\u00e3o CC est\\u00e1 zerada","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":2,"tipo":5},{"msg":"- Corrente CC | String: 4","msg2":"A string 4 da Corrente CC est\\u00e1 zerada","acao":"Acionar t\\u00e9cnico de manuten\\u00e7ao para verifica\\u00e7\\u00e3o.","causas":"- Fus\\u00edvel queimado e\\/ou Conector desconectado e\\/ou Chave do inversor desligada.","status":2,"tipo":5},{"msg":"- Tens\\u00e3o CC | String: 4","msg2":"A string 4 da Tens\\u00e3o CC est\\u00e1 zerada","acao":"Entrar em contato com o gerente t\\u00e9cnico.","causas":"","status":2,"tipo":5}]}],"arquivos":[],"qtdTrackers":0}'


def test_error500() -> None:
    with patch("requests.Session.post", return_value=error_500_response):
        api = APIHelper("user@acme.com", "password")
        with pytest.raises(SunWegApiError) as e_info:
            api.authenticate()
        assert e_info.value.__str__() == "Request failed: <Response [500]>"


def test_authenticate_success() -> None:
    with patch("requests.Session.post", return_value=auth_success_response):
        api = APIHelper("user@acme.com", "password")
        assert api.authenticate() == True


def test_authenticate_failed() -> None:
    with patch("requests.Session.post", return_value=auth_fail_response):
        api = APIHelper("user@acme.com", "password")
        with pytest.raises(SunWegApiError) as e_info:
            api.authenticate()
        assert e_info.value.__str__() == "Error message"


def test_list_plants_none_success() -> None:
    with patch(
        "requests.Session.get", return_value=list_plant_success_none_response
    ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
        api = APIHelper("user@acme.com", "password")
        assert len(api.listPlants()) == 0


def test_list_plants_1_success() -> None:
    with patch(
        "requests.Session.get", return_value=list_plant_success_1_response
    ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
        api = APIHelper("user@acme.com", "password")
        assert len(api.listPlants()) == 1


def test_list_plants_2_success() -> None:
    with patch(
        "requests.Session.get", return_value=list_plant_success_2_response
    ), patch("sunweg.api.APIHelper.plant", return_value=PLANT_MOCK):
        api = APIHelper("user@acme.com", "password")
        assert len(api.listPlants()) == 2


def test_list_plants_401() -> None:
    with patch("requests.Session.post", return_value=auth_success_response), patch(
        "requests.Session.get", return_value=error_401_response
    ):
        api = APIHelper("user@acme.com", "password")
        assert len(api.listPlants()) == 0


def test_plant_success() -> None:
    with patch("requests.Session.get", return_value=plant_success_response), patch(
        "sunweg.api.APIHelper.inverter", return_value=INVERTER_MOCK
    ):
        api = APIHelper("user@acme.com", "password")
        plant = api.plant(16925)
        assert plant is not None
        assert plant.id == 16925
        assert plant.name == "Plant Name"
        assert plant.total_power == 0.0
        assert plant.last_update == datetime(2023, 2, 25, 8, 4, 22)
        assert plant.kwh_per_kwp == 0.0
        assert plant.performance_rate == 1.48
        assert plant.saving == 12.786912
        assert plant.today_energy == 0.0
        assert plant.total_carbon_saving == 0.012296
        assert plant.total_energy == 23.2
        assert plant.__str__().startswith("<class 'sunweg.plant.Plant'>")
        assert len(plant.inverters) == 1


def test_plant_401() -> None:
    with patch("requests.Session.post", return_value=auth_success_response), patch(
        "requests.Session.get", return_value=error_401_response
    ):
        api = APIHelper("user@acme.com", "password")
        assert api.plant(16925) is None
