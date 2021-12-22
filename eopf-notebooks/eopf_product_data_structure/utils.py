import os
import glob
import xarray as xr
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


# With this function we will be able to explore and get all variables from a given netcdf files of the product
# and put them all into an xarray dataset
def get_ds_variables(path_to_product, names=[], file_pattern="*", process_tie=False, process_coords=False, orphan=False):

    nc_files = glob.glob(os.path.join(path_to_product, f"{file_pattern}.nc"))
    
    variables = {}
    coordinates = {}
    for nc in nc_files:
        gname, _ = os.path.splitext(os.path.basename(nc))
        if len(names) == 0 or gname in names:   
            ds = xr.open_dataset(nc,decode_times=False,mask_and_scale=False)
            
            for k in ds.variables.keys():
                if "orphan" in k != orphan:
                    continue
                if 'coordinates' in gname and process_coords:
                    coordinates[k] = ds.get(k)
                elif gname.startswith('tie_') and process_tie:
                    variables[f'tie_{k}'] = ds.get(k)
                else:
                    variables[k] = ds.get(k)
    ds = xr.Dataset(data_vars=variables, coords=coordinates)
    
    return ds


def get_ds_groups(path_to_product, file_pattern="*"):

    nc_files = glob.glob(os.path.join(path_to_product, f"{file_pattern}.nc"))
    groups = {}
    for nc in nc_files:
        gname, _ = os.path.splitext(os.path.basename(nc))
        ds = get_ds_variables(path_to_product, file_pattern=gname)
        groups[gname] = ds
    return groups


def renderer(product):
    dir_path = Path(__file__).resolve().parent
    file_loader = FileSystemLoader( os.path.join(dir_path,'templates'))
    env = Environment(loader=file_loader)
    template = env.get_template('EOProductDataStructure.html')
    html = template.render({"product": product})
    return html


def create_data(dims: int):
    if dims <= 1:
        return []
    return [create_data(dims -1)]
