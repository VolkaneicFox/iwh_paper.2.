# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:12:03 2024

@author: SME
"""

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
drought2019=pd.read_csv("G://SME/Paper_2/IndiaDrought/drought_atlas/situation_of_agri2019_drought.csv")
drought2019=drought2019[drought2019['survey_reference']=='201807-201812']

##part1. land holdings and land use
landv1df,landv1meta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L4B5land_details_July_Dec_2018.sav")
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

output2v1df,output2v1meta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L6B6output_crops_July_Dec_2018.sav")
output2v1cols={'Common Primary Key for household identification':'HHID', 'Sector':'type','State_District':'nss_district_code19',
'Srl No.':'crop_group', 'Crop code':'crop_code','Unit code':'unit',
'area of irrigated land (0.00 acre)':'irrigated_acre','quantity produced from irrigated land':'output_irrigated_acre',
'area of un-irrigated land (0.00 acre)':'unirrigated_acre',
       'quantity produced from un-irrigated land':'output_unirrigated_acre', 
'total quantity':'total_quantity','"area of land under pre-harvest sale (0.00 acre)':'preharvest_acre',
       'major disposal-to whom you sold':'major_buyer',
       'are you satisfied with the sale outcome':'sale_satistifaction',
       'major disposal: quantity sold':'major_quantity_sold', 'major disposal: sale value (Rs.)':'major_sale_Rs.',
       'other disposal: quantity sold':'other_quantity_sold'}
output2v1df=output2v1df[list(output2v1cols.keys())].rename(columns=output2v1cols)
output2v1df=output2v1df[output2v1df['crop_code'].isin(['5999','9999'])==False]
output2v1df['nss_district_code19']=output2v1df['nss_district_code19'].astype(float)

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

##cleaning and merging the nss19 codes with spei codes

landdict={'land_type':{6:'homestead',7:'homestead',8:'homestead',9:'homestead', 10:'total land',
                       1:'non-homestead',2:'non-homestead',3:'non-homestead',4:'non-homestead',5:'non-homestead'},
          'ownership':{1:'owned and possessed',6:'owned and possessed',
                       2:'leased in',3:'leased in',7:'leased in',8:'leased in',
                       4:'otherwise possessed',9:'otherwise possessed',
                       10:'total land'}}
landv1df=landv1df[landv1df['farming_output_code'].isin(['','99'])==False]
outputv1df=outputv1df[outputv1df['farming_output_code'].isin(['','99'])==False]
#from outputv1df we gather the households that report significant earnings from agriculture
agrihh=list(outputv1df['HHID'].unique())
noval=outputv1df[outputv1df['total_value_Rs'].isnull()]
outputv1df['total_value_Rs']=outputv1df['total_value_Rs'].fillna(0)
outputv1df['nss_district_code19']=outputv1df['state']+outputv1df['district']
outputv1df['nss_district_code19']=outputv1df['nss_district_code19'].astype(float)

outputmain=pd.merge(outputv1df,output2v1df,on=['HHID', 'type', 'crop_code', 'nss_district_code19'])
outputmain=outputmain.rename(columns={'harvest_sale_Rs':'harvest_value_Rs','other_disposal_sale_kg':'all_disposal_sale_kg'})
outputmain['crop_code']=outputmain['crop_code'].astype(int)
outputmain['HHID']=outputmain['HHID'].astype(int)
#modify landv1df by taking total agri output of different agri products from each household
groupcols=['HHID', 'type', 'state', 'district','if_used_agri_v1',
           'farming_output_code', 'if_land_irrigated','land_ownership']
sumcols=['land_acre', 'jhum_land', 'non_jhum_land', 'only_animal_farming',
       'crops_and_animals', 'other_agri_uses', 'other_non_agri',
       'acre_irrigated' ]
landv1df_v1=landv1df[groupcols+sumcols].groupby(groupcols).sum().reset_index()
landv1df_v1['nss_district_code19']=landv1df_v1['state']+landv1df_v1['district']
landv1df_v1['nss_district_code19']=landv1df_v1['nss_district_code19'].astype(float)
landv1df_v1['land_type']=landv1df_v1['land_ownership'].apply(lambda x:landdict['land_type'][int(x)])
landv1df_v1['land_own']=landv1df_v1['land_ownership'].apply(lambda x: landdict['ownership'][int(x)])

#part4. cost of inputs

costdf,costmeta=makedata("G://SME/paper_2/IndiaDrought/surveydata/situationofagriculture2019/V1L8B7input_expense_July_Dec_2018.sav")
costcols={'Common Primary Key for household identification':'HHID',
          'Crop code -(as in col. 2 block 6)':'crop_code',
          'Inputs-paid out expenses(Rs.)':'explicit_input_cost_Rs.'}
costdf=costdf[costcols.keys()].rename(columns=costcols)
costdf=costdf[costdf['crop_code']!='']
costdf['HHID']=costdf['HHID'].astype(int)
costdf['crop_code']=costdf['crop_code'].astype(int)
costmain=pd.merge(costdf,outputmain,on=['HHID','crop_code'])
location=drought2019[['spei_state_name','nss_district_code19','spei_district_code']].drop_duplicates()
costmain=pd.merge(costmain,location,on='nss_district_code19')
costmain=costmain.rename(columns={'spei_state_name':'state_name'})
costmain['state_name']=costmain['state_name'].apply(lambda x: x.lower().replace('&','and'))

#step1a. making the cpi data
states=list(set(costmain['state_name'].dropna()))
cpidata=pd.read_excel("G://SME/paper_2/IndiaDrought/crop_data/agri_prices/farmer_prices_monthly.xlsx",sheet_name="farmer_cpi_monthly")
cpidata['state']=cpidata['state'].replace('jamme and kashmir','jammu and kashmir')
cpidata['date']=(cpidata['year']*100)+cpidata['month']
cpidata=cpidata[(cpidata['date']>=201807)&(cpidata['date']<=201812)]
statecpi=cpidata[['state','cpi']].groupby('state').mean().reset_index()
statecpi=pd.merge(statecpi,pd.DataFrame({'state':states}),on='state',how='outer')
stategroups={'south':['andhra pradesh','karnataka','kerala','maharashtra','tamil nadu','puducherry',
                      'goa','telangana'],
             'east':['assam','bihar','odisha','west bengal'],
             'north':['haryana','himachal pradesh','jammu and kashmir','punjab','uttar pradesh',
                      'ladakh','uttarakhand','chandigarh','delhi'],
             'north-east':['manipur','meghalaya','tripura','sikkim','arunachal pradesh','nagaland',
                           'mizoram'],
             'central':['madhya pradesh','jharkhand','chhattisgarh'],
             'west':['gujarat','rajasthan']}
stategroupsr={}
for item in stategroups:
    x=stategroups[item]
    for y in x:
        stategroupsr[y]=item
stategroupsr['india']='india'  
statecpi=statecpi[statecpi['state'].isin(stategroupsr.keys())]   
statecpi['group']=statecpi['state'].apply(lambda x: stategroupsr[x])
statecpi['groupcpi']=statecpi[['group','cpi']].groupby('group').transform('mean')
statecpi['isnan']=(statecpi['cpi'].isnull()).astype(int)
statecpi['cpi']=statecpi['cpi'].fillna(0)
statecpi['general_cpi']=statecpi['cpi']+(statecpi['isnan']*statecpi['groupcpi'])
statecpi=statecpi.drop('isnan',axis=1)
statecpi=statecpi.set_index('state')
cpiindia=statecpi.loc['india','general_cpi']
statecpi['general_cpi_ix']=statecpi['general_cpi']*100/cpiindia
statecpi=statecpi.reset_index()
statecpi=statecpi.rename(columns={'state':'state_name'})

costmain1=pd.merge(costmain,statecpi[['state_name','general_cpi_ix','general_cpi']],on='state_name')
costmain1['explicit_input_cost_real']=costmain1['explicit_input_cost_Rs.']/costmain1['general_cpi'] ## does not matter if 'general_cpi' or 'general_cpi_ix'
costmain1['irrigated_acre']=costmain1['irrigated_acre'].fillna(0)
costmain1['unirrigated_acre']=costmain1['unirrigated_acre'].fillna(0)
costmain1['total_acre']=costmain1['irrigated_acre']+costmain1['unirrigated_acre']
costmain1=costmain1[costmain1['total_acre']>0.0001]
costmain1['total_yield']=costmain1['total_quantity']/costmain1['total_acre']
costmain1['yield_to_cost']=costmain1['total_yield']/costmain1['explicit_input_cost_real']
costmain1['total_quantity_to_cost']=costmain1['total_quantity']/costmain1['explicit_input_cost_real']
costmain1=costmain1.dropna(subset='explicit_input_cost_real')

costmain1['disposal_sale_real']=costmain1['all_disposal_sale_Rs']/costmain1['general_cpi_ix']
costmain1['rate_from_sale']=costmain1['all_disposal_sale_Rs']/costmain1['all_disposal_sale_kg']
costmain1['real_rate_from_sale']=costmain1['rate_from_sale']/costmain1['general_cpi_ix']
costmain1['profit_real']=costmain1['disposal_sale_real']-costmain1['explicit_input_cost_real']

costmain1=pd.merge(costmain1,drought2019[['spei_district_code','severe_dry_mo', 'extreme_dry_mo',
       'exceptional_dry_mo', 'median_spei', 'max_spei',
       'min_spei', 'std_spei','nss_district_code19']],on=['nss_district_code19','spei_district_code'])

t2m=pd.read_csv('G://SME/paper_2/IndiaDrought/speidata/sitagri2019_t2m.csv')
maindf=pd.merge(costmain1,t2m,on='spei_district_code')
mergecols=[i for i in maindf.columns if i in drought2019.columns]
maindf=pd.merge(maindf,drought2019,on=mergecols) ##32246 unique households
maindf.to_csv("G://SME/paper_2/IndiaDrought/regression_data/sitagri_spei4_cleaned.csv",index=False)

cropdict={101:'paddy',102:'jowar',103:'bajra',104:'maize',
          401:'sugarcane',606:'banana',1006:'coconut',1009:'soyabean',
          1101:'cotton',106:'wheat'}
buyersdict={1:'local_market',2:'APMC_market',3:'input_dealers',
            4:'coops',5:'govt_agency',6:'FPO', 7:'pvt_processor',
            8:'contract',9:'otherbuyers'}

maindf['profit_real_per_acre']=maindf['profit_real']/maindf['total_acre']
maindf['irrigated_acre_share']=maindf['irrigated_acre']/maindf['total_acre']
maindf['mean_t2m']=maindf['mean_t2m']-273.15
subset=maindf[maindf['crop_code'].isin(list(cropdict.keys()))]

dummy=['major_buyer','crop_code','state_name']
subset=subset[subset['major_buyer'].isna()==False]

def makedummies(colname,df,usedict=False,indict={}):
    values=df[colname].unique()
    values=list(values)
    dummycols=[]
    for v in values:
        if usedict==False:
            df[v+'_d']=df[colname].apply(lambda x: int(x==v))
            dummycols.append(str(v)+'_d')
        else:
            V=indict[v]
            df[V+'_d']=df[colname].apply(lambda x: int(x==v))
            dummycols.append(V+'_d')
    return [df,dummycols]

make=makedummies(colname='major_buyer',df=subset,usedict=True,indict=buyersdict)
subset,buyerd=make[0],make[1]
make=makedummies(colname='state_name',df=subset,usedict=False)
subset,stated=make[0],make[1]
make=makedummies(colname='crop_code',df=subset,usedict=True,indict=cropdict)
subset,cropd=make[0],make[1]
subset=subset.drop(dummy,axis=1)
buyerd.remove('otherbuyers_d')
stated.remove('bihar_d')
cropd.remove('paddy_d')

subset['mean_spei2']=subset['mean_spei']**2
subset['mean_t2m2']=subset['mean_t2m']**2
subset['mean_t2m3']=subset['mean_t2m']**3
subset['constant']=1
endog='profit_real_per_acre'
exog=['mean_spei','std_spei','mean_spei2','mean_t2m','std_t2m','mean_t2m2','irrigated_acre_share','total_yield'] #'mean_spei','std_spei','mean_spei2',
dummycols=cropd+buyerd+stated
regdf=subset[[endog]+exog+dummycols+['constant','HHID']].dropna()

import statsmodels.api as sm
regdf=regdf.drop_duplicates()
regdf=regdf.drop_duplicates(subset='HHID').drop('HHID',axis=1)
print(regdf.columns)
qtl=regdf[endog].quantile(0.95)
regdf=regdf[regdf[endog]<qtl]
y=regdf[endog]
x=regdf[exog+cropd+stated+buyerd+['constant']]
model = sm.OLS(y, x).fit(cov_type='HC3')
model.summary()
