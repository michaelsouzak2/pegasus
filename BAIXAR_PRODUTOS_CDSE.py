# from .\python import query, download
from python import query, download
import datetime
from os.path import join

CREDENTIALS = {
    "username": '',
    "password": ''
}

footprint = 'POLYGON((-50.757842619956556 1.713089604452307,-50.04394891222159 0.214167613589467,-49.187276462939614 -0.42833223483449956,-47.0455953397347 -0.8566405321680151,-44.90391421652978 -1.9271495375252385,-42.33389686868388 -3.424648812498191,-39.478322037743986 -3.3533842936203513,-37.764977139180054 -4.706396924967933,-36.12302161138961 -5.204253132623734,-35.266349162107645 -6.482557661346959,-35.337738532881154 -8.323128266355198,-36.40857909448361 -9.873883686334636,-37.764977139180054 -11.067271191165005,-38.19331336382104 -12.32556981839386,-39.2641539254235 -12.604395868464152,-39.2641539254235 -14.68550277851709,-39.62110077929098 -17.42936143052296,-40.04943700393197 -19.3935633268578,-40.834720082440434 -20.66787838652985,-41.69139253172241 -21.931591422224443,-42.47667561023087 -22.658163091948353,-43.54751617183334 -22.987163891966844,-44.83252484575628 -23.052868400618053,-46.26031226122623 -23.642758322510915,-47.830878418243174 -25.008789717549362,-49.11588709216612 -25.97536172719073,-48.401993384431144 -26.87039081626623,-48.473382755204646 -27.69519941061025,-50.472285136862574 -29.76089039297331,-51.828683181559015 -30.563288563610506,-52.54257688929399 -31.66341527464389,-53.25647059702896 -32.32939253519518,-53.827585563216935 -33.0503647078067,-51.25756821537103 -33.76548196998729,-40.834720082440434 -26.231792061421544,-33.48161489277022 -20.13258590671309,-32.12521684807377 -12.255816684950346,-29.697978241774862 -6.4116197635661365,-32.26799558962076 -3.210839783382781,-38.978596442329504 0.0713893523019209,-46.9028165981877 1.9271495375252243,-50.757842619956556 1.713089604452307,-50.757842619956556 1.713089604452307))'
output_dir = r"produtos"
atraso = 1


#Buscando por produtos, isso retorna um dicionário.
results = query.query(
    'Sentinel1',
    start_date = datetime.date.today() - datetime.timedelta(days=atraso),
    end_date = datetime.date.today(),
    geometry=footprint,
)

#Extraindo titulos e ids dos dicionario retornado pela pesquisa.
todos_titulos, todos_ids, todos_tamanhos = [], [], []
for item, info in results.items():
    todos_ids.append(info['id'])
    todos_titulos.append(info['properties']['title'][:-5]) #O trecho '.SAFE' é removido.
    todos_tamanhos.append(info['properties']['services']['download']['size'])
    
todos_produtos = list(zip(todos_titulos, todos_ids, todos_tamanhos))

#Filtrando resultados com base na polarização IW e tipo SLC.
indicadores, produtos = ['S1A_IW_GRDH_', 'S1C_IW_GRDH_'], []
for p in todos_produtos:
    trecho, titulo = p[0][0:12], p[0]
    if((trecho in indicadores) and len(titulo) == 67):
        produtos.append(p)
        
print(f"NÚMERO DE PRODUTOS ENCONTRADOS: {len(produtos)}")

quantidade = 1  # Ou a quantidade desejada de itens a serem baixados

for i in range(quantidade):
    gb_formatado = "{:.1f}".format(produtos[i][2]/2**30)
    print(f'BAIXANDO {produtos[i][0]} COM {gb_formatado} GiB')
    download.download(produtos[i][1], outfile=join(output_dir, produtos[i][0] + ".zip"), **CREDENTIALS, total_size=produtos[i][2])