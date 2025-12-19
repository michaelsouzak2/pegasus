import os
import numpy as np
import tifffile as tiff
import rasterio
from rasterio.transform import xy
from netCDF4 import Dataset
from scipy.ndimage import uniform_filter
from PIL import Image

MAX_RADIUS = 50
HOMOGENEITY_THRESHOLD = 1.5
TILE = 1024


# ------------------------------------------------------------
# ENCONTRAR TIFF VV
# ------------------------------------------------------------
def encontrar_tiff_vv(safe_folder):
    measurement_dir = os.path.join(safe_folder, "measurement")
    for f in os.listdir(measurement_dir):
        if f.lower().endswith(".tiff") and "vv" in f.lower():
            return os.path.join(measurement_dir, f)
    raise FileNotFoundError("Nenhum TIFF VV encontrado.")


# ------------------------------------------------------------
# FILTRO IDAN
# ------------------------------------------------------------
def idan_filter_tile(tile, max_radius=50, threshold=1.5):
    out = np.zeros_like(tile, dtype=np.float32)
    for r in range(3, max_radius + 1, 2):
        mean_local = uniform_filter(tile, size=r)
        var_local = uniform_filter(tile**2, size=r) - mean_local**2
        mask = var_local < threshold
        out += mean_local * mask
    return out


def processar_idan_image_full(image):
    h, w = image.shape
    out = np.zeros_like(image, dtype=np.float32)

    for y in range(0, h, TILE):
        for x in range(0, w, TILE):
            y2 = min(y + TILE, h)
            x2 = min(x + TILE, w)
            tile = image[y:y2, x:x2]
            out[y:y2, x:x2] = idan_filter_tile(tile, MAX_RADIUS, HOMOGENEITY_THRESHOLD)

    return out


# ------------------------------------------------------------
# SALVAR NETCDF4_CF COM GEO
# ------------------------------------------------------------
def salvar_netcdf_cf(path, array, transform, crs):
    h, w = array.shape

    ds = Dataset(path, "w", format="NETCDF4")

    # Dimensões
    ds.createDimension("y", h)
    ds.createDimension("x", w)

    # Variáveis
    vv_var = ds.createVariable("VV_IDAN", "f4", ("y", "x"))
    vv_var.units = "DN_filtered"
    vv_var.long_name = "Sentinel-1 VV band filtered with IDAN"
    vv_var[:, :] = array

    # Coordenadas lon/lat
    lon = ds.createVariable("lon", "f8", ("y", "x"))
    lat = ds.createVariable("lat", "f8", ("y", "x"))

    # Gerar lon/lat com rasterio
    lons = np.zeros((h, w), dtype=np.float64)
    lats = np.zeros((h, w), dtype=np.float64)

    for row in range(h):
        xs, ys = xy(transform, row, np.arange(w))
        lons[row, :] = np.array(xs)
        lats[row, :] = np.array(ys)

    lon[:, :] = lons
    lat[:, :] = lats

    # CRS CF-compliant
    crs_var = ds.createVariable("crs", "i4")
    crs_var.spatial_ref = crs.wkt
    crs_var.grid_mapping_name = "transverse_mercator"

    vv_var.grid_mapping = "crs"
    lat.standard_name = "latitude"
    lon.standard_name = "longitude"

    ds.close()


# ------------------------------------------------------------
# SALVAR JPG
# ------------------------------------------------------------
def salvar_jpg_full(path, array_filtered):
    arr_db = 10 * np.log10(np.clip(array_filtered, 1e-8, None))
    p2, p98 = np.percentile(arr_db, (2, 98))
    arr_norm = np.clip((arr_db - p2) / (p98 - p2), 0, 1)
    img = (arr_norm * 255).astype(np.uint8)
    Image.fromarray(img).save(path, format="JPEG", quality=95)


# ------------------------------------------------------------
# PROCESSAMENTO PRINCIPAL
# ------------------------------------------------------------
def processar_safe(safe_folder):

    print("🔍 Procurando TIFF VV…")
    tiff_vv = encontrar_tiff_vv(safe_folder)
    print("✔ TIFF encontrado:", tiff_vv)

    # LER TIFF COM GEO USANDO RASTERIO
    with rasterio.open(tiff_vv) as src:
        vv = src.read(1).astype(np.float32)
        transform = src.transform
        crs = src.crs

    print("↳ GeoTransform:", transform)
    print("↳ CRS:", crs)

    # Aplicar filtro IDAN
    print("\n⏳ Aplicando filtro IDAN…")
    vv_idan = processar_idan_image_full(vv)

    # Exportar NETCDF3 CF
    nc_path = os.path.join(safe_folder, "VV_IDAN_CF.nc")
    salvar_netcdf_cf(nc_path, vv_idan, transform, crs)
    print("✔ NETCDF CF salvo em:", nc_path)

    # Exportar JPG
    jpg_path = os.path.join(safe_folder, "VV_IDAN.jpg")
    salvar_jpg_full(jpg_path, vv_idan)
    print("✔ JPG salvo em:", jpg_path)

    print("\n🎉 Finalizado com sucesso!\n")


if __name__ == "__main__":
    SAFE_FOLDER = r"C:\Users\11065311\git\pegasus\app\downloads\S1A_IW_GRDH_1SDV_20251128T083108_20251128T083137_062075_07C458_F0B8.SAFE"
    processar_safe(SAFE_FOLDER)
