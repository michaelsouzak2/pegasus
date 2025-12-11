import os
import numpy as np
from snappy import ProductIO, GPF
from PIL import Image

# -------------------------------------------
# CONFIGURAÇÃO INICIAL
# -------------------------------------------
safe_path = r"C:\Users\11065311\git\pegasus\app\downloads\S1A_IW_GRDH_1SDV_20251128T083108_20251128T083137_062075_07C458_F0B8.SAFE"    # caminho da pasta .SAFE
output_jpg = r"C:\Users\11065311\git\pegasus\app\downloads\S1A_IW_GRDH_1SDV_20251128T083108_20251128T083137_062075_07C458_F0B8.SAFE\intensity_VV.jpg"   # saída

# -------------------------------------------
# 1. CARREGAR O PRODUTO
# -------------------------------------------
print("Carregando produto...")
product = ProductIO.readProduct(safe_path)

# -------------------------------------------
# 2. APLICAR CALIBRAÇÃO (necessário para gerar intensity_VV)
# -------------------------------------------
print("Calibrando a banda VV...")
parameters = {
    'outputSigmaBand': False,
    'outputGammaBand': False,
    'outputBetaBand': True,     # cria intensidade (beta0)
    'selectedPolarisations': 'VV'
}

calibrated
