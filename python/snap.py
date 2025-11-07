from snappy import ProductIO, GPF, HashMap
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------
# 1. Abrir produto Sentinel-1 IW GRDH (.SAFE)
# -------------------------------------------------------
input_safe = r"C:\Users\11065311\Downloads\S1C_IW_GRDH_1SDV_20251105T082202_20251105T082232_004876_009A3B_4F7C.SAFE.zip"
product = ProductIO.readProduct(input_safe)

# -------------------------------------------------------
# 2. Aplicar Single Product Speckle Filter - IDAN
# -------------------------------------------------------
speckle_params = HashMap()
speckle_params.put('sourceBands', 'Intensity_VV')
speckle_params.put('filter', 'IDAN')
speckle_params.put('nLooks', 1)
speckle_params.put('adaptiveNeighSize', 50)

speckle_filtered = GPF.createProduct(
    'Speckle-Filter',
    speckle_params,
    product
)

# -------------------------------------------------------
# 3. Exportar em NETCDF4-CF
# -------------------------------------------------------
output_nc = r"/caminho/saida/s1_vv_idan50.nc"
ProductIO.writeProduct(speckle_filtered, output_nc, 'NetCDF4-CF')

# -------------------------------------------------------
# 4. Exportar banda filtrada como JPG
# -------------------------------------------------------
# Ler a banda filtrada como array
band = speckle_filtered.getBand('Intensity_VV')
w = band.getRasterWidth()
h = band.getRasterHeight()

array = np.zeros(w * h, np.float32)
band.readPixels(0, 0, w, h, array)
array = array.reshape(h, w)

# Normalização simples para visualização (log-scale opcional)
array_log = 10 * np.log10(array + 1e-8)
img_norm = (array_log - np.min(array_log)) / (np.max(array_log) - np.min(array_log))

plt.imshow(img_norm, cmap='gray')
plt.axis('off')

output_jpg = r"C:\Users\11065311\Downloads\output\s1_vv_idan50.jpg"
plt.savefig(output_jpg, dpi=300, bbox_inches='tight', pad_inches=0)

print("✅ Processamento concluído!")
print("Arquivo NETCDF salvo em:", output_nc)
print("Arquivo JPG salvo em:", output_jpg)
