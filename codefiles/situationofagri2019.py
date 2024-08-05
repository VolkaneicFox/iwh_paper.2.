'''
this code develops the household level metrics for agricultural performance that is observed in the Situation of Agriculture Survey 2019

there are two visits in the survey but the data sets are only for the first visit that corresponds to the agricultural season from July-2018 to Dec-2018
'''
import numpy as np
import pandas as pd
import os
import pickle
import pyreadstat as ps
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
pd.options.mode.chained_assignment = None  # default='warn'  
def givedfdetails(df, meta):
    columndict = meta.column_names_to_labels
    columndets = meta.variable_value_labels
    df = df.rename(columns=columndict)
    return [df, columndets]
def makedata(path):
    df,meta=ps.read_sav(path)
    df,cols=givedfdetails(df,meta)
    return [df,cols]

##part1. land holdings and land use
landv1df,landv1meta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L4B5land_details_July_Dec_2018.csv")
landv1cols={'Common Primary Key for household identification':'HHID','Srl No.':'land_ownership',
            'Sector':'type','State':'state','District':'district',
            'area of land (0.00 acre)':'land_acre',
       'whether used for any agricultural production during July- December 2018':'if_used_agri_v1',
       'land used for shifting/ jhum cultivation':'jhum_land',
       'land other than the land used for shifting /jhum cultivation':'non_jhum_land',
       'only for farming of animals':'only_animal_farming',
       'both for growing of crop and farming of animals':'crops_and_animals',
       'other agricultural uses':'other_agri_uses',
       'other land not used for agriculture purpose':'other_non_agri',
       'major type of crop grown/ animal farming undertaken (code)':'farming_output_code',
       'whether any part of the land was rrigated':'if_land_irrigated',
       'area of land irrigated (0.00 acre)':'acre_irrigated',
       'source of irrigation: major source':'primary_irrigation',
       'source of irrigation: 2nd major source':'second_irrigation'}
landv1df=landv1df[list(landv1cols.keys())].rename(columns=landv1cols)

#part2. agricultural output
'''
output is measured for households with earnings from self-employment in agriculture
is more than Rs. 4000 for the last 365 days, this is collected in Visit 1 - so the period
of reference is from June 2017 since Visit 1 is canvassed from June 2018 to Dec 2018. 
This is done to only select agricultural households and the actual data on output
and sales is for the reference period July2018 to Dec2018 
'''
outputv1df,outputv1meta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L7B6output_crops_July_Dec_2018.sav")
outputv1cols={'Common Primary Key for household identification':'HHID', 'Sector':'type', 'State':'state',
'State_District':'nss_district_code2019', 'District':'district',
'Crop code':'crop_code','other disposal: sale value (Rs.)':'other_disposal_sale_Rs', 
'all disposal: quantity sold':'all_disposal_sale_kg',
'all disposal: sale value (Rs.)':'all_disposal_sale_Rs', 
'value of pre-harvest sale (Rs.)':'pre_harvest_sale_Rs', 
'value of harvested produce (Rs.)':'harvest_sale_Rs',
'value of by-products (Rs.)':'value_by_products_Rs', 
'total value (Rs.)':'total_value_Rs'}
outputv1df=outputv1df[list(outputv1cols.keys())].rename(columns=outputv1cols)
outputv1df['farming_output_code']=outputv1df['crop_code'].apply(lambda x: x[:2])

#part3. household demographics
demov1df,demov1meta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L3B4demo_other_sample_hh.sav")
democols={'Common Primary Key for household identification':'HHID', 'Sector':'type', 
          'State':'state', 'District':'district', 'State_District':'nss_district_code2019',
          'Household size':'household_size','Religion code':'religion_code',
          'Social group code':'caste_code', 'Household classification  code':'household_type2',
       'usual consumer expenditure in a month for household purposes out of purchase (A)':'usual_consumption_purchase',
       'imputed value of usual consumption in a month from home grown stock (B)':'usual_consumption_home',
       'imputed value of usual consumption in a month from wages in kind, free collection, gifts, etc (C)':'usual_consumption_gifts',
       'expenditure on purchase of household durable during last 365 days (D)':'durable_purchase_last365days',
       'usual monthly consumer expenditure E: [A+B+C+(D/12)]':'household_cons_exp_monthly',
       'value of agricultural production from self-employment activities during the last 365 days(code)':'household_type1',
       'dwelling unit code':'if_owned_house', 'type of structure':'kaccha_or_pucca',
       'whether any of the household member has bank account':'if_bank_account',
       'whether any of the household member possesses MGNREG job card':'if_mnrega_card',
       'Whether undertook any work under MGNREG during the last 365 days':'if_mnrega_work_last365days',
       'Whether any of the household member is a member of registered farmers’ organisation':'if_farmer_organisation',
       'Whether the household possesses any Kisan Credit Card':'if_kisan_credit_card',
       'Whether the household possess Soil Health Card':'if_soil_health_card',
       'whether fertilizer, etc. applied to field as per recommendations of Soil Health Card':'compliance_soil_health_card',
       'whether the household possess Animal Health Card (Nakul Swasthya Patra':'if_animal_health_card',
       'whether the household insured any crop under PM Fasal Bima Yojana during last 365 days':'if_PM_fasal_bima_last365days',
       }
demov1df=demov1df[list(democols.keys())].rename(columns=democols)

