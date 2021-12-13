import os
import papermill as pm


if __name__ != "main":

    product_types = ["S3A_SL_1_RBT___", 
                    "S3A_SR_1_SRA_BS" ,
                    "S3A_OL_2_LFR___", 
                    "S3A_SY_2_VGP___", 
                    "S3A_OL_1_EFR___", 
                    "S3A_SR_1_SRA_A_", 
                    "S3A_SR_1_SRA___", 
                    "S3A_SL_2_LST___", 
                    "S3A_SR_2_LAN___", 
                    "S2B_MSIL1B", 
                    "S1A_WV_OCN__2SS", 
                    "S1A_IW_OCN__2SD", 
                    "S1A_IW_GRDH_1SD", 
                    "S2A_MSIL2A", 
                    "S2A_MSIL1C"] 

    try:
        
        for product_type in product_types:
            sat = product_type[:2].lower()
            pm.execute_notebook(
            '%s_products_data_structures.ipynb' % sat,
            'temp_notebook.ipynb',
            parameters = dict(product_type=product_type)
            )
            os.system("jupyter nbconvert --to html temp_notebook.ipynb --no-input --output-dir ./output --output  %s.html" % product_type)

    except Exception as e:
        print(e)
