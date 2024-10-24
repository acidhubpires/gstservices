import geopandas as gpd
import zipfile
import tempfile
import os
from fastapi import HTTPException
from app.processing.geo_processing import process_geodata

def processar_arquivo_upload(file_content, filename):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_content)
            tmp.flush()
            tmp_filename = tmp.name

        # Verifica o tipo de arquivo baseado na extensão
        if filename.endswith(".kmz"):
            gdf = gpd.read_file(f"zip://{tmp_filename}")
        elif filename.endswith(".geojson"):
            gdf = gpd.read_file(tmp_filename)
        elif filename.endswith(".zip"):
            with zipfile.ZipFile(tmp_filename, 'r') as zip_ref:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    zip_ref.extractall(tmpdirname)
                    shp_file = None
                    for root, dirs, files in os.walk(tmpdirname):
                        for file in files:
                            if file.endswith(".shp"):
                                shp_file = os.path.join(root, file)
                                break
                    if shp_file is None:
                        raise HTTPException(status_code=400, detail="Nenhum arquivo .shp encontrado no ZIP.")
                    gdf = gpd.read_file(shp_file)
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use KMZ, GeoJSON ou ZIP.")

        if not isinstance(gdf, gpd.GeoDataFrame):
            raise HTTPException(status_code=500, detail="O arquivo fornecido não é um GeoDataFrame.")
        if 'geometry' not in gdf:
            raise HTTPException(status_code=400, detail="Nenhuma geometria encontrada no arquivo.")

        coordenadas = []
        for geom in gdf.geometry:
            if geom.is_empty:
                continue
            if geom.geom_type == "Polygon":
                coords = list(geom.exterior.coords)
            elif geom.geom_type == "MultiPolygon":
                coords = []
                for part in geom.geoms:
                    coords.extend(list(part.exterior.coords))
            else:
                coords = list(geom.coords)
            coordenadas.append(coords)

        resultados = process_geodata(coordenadas)
        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {str(e)}")
    finally:
        os.unlink(tmp_filename)
