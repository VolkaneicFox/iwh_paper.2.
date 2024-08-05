import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
'''
The SPEI data exists for 1-month, 4-months and 12-months of temporal intensity.
Each time length has distinctive implications. Here, I will make drought summa-
ries for the districts in each time-frame. Starting from 2000 till 2019, 
(i) assign the drought categorizations and save the text files 
(ii) count the number of months of each drought category in every district
(iii) find the mean, min, max, std and median of the SPEI in each year
'''

spei_data_dir = "G://SME/Paper_2/IndiaDrought/drought_atlas/Districts/"

#step 1: assign the drought categories

def assign_spei_indicator(spei_value):
    if spei_value >= 2:
        return 'exceptional_wet'
    elif spei_value >= 1.6 and spei_value <2:
        return 'extreme_wet'
    elif spei_value >= 1.3 and spei_value < 1.6:
        return 'severe_wet'
    elif spei_value >= 0.8 and spei_value < 1.3:
        return 'moderate_wet'
    elif spei_value >= 0.5 and spei_value < 0.8:
        return 'abnormal_wet'
    elif spei_value > -0.5 and spei_value < 0.5:
        return 'normal'
    #####---#####
    elif spei_value > -0.8 and spei_value <= -0.5:
        return 'abnormal_dry' 
    elif spei_value > -1.3 and spei_value <= -0.8:
        return 'moderate_dry'
    elif spei_value > -1.6 and spei_value <= -1.3:
        return 'severe_dry'
    elif spei_value > -2 and spei_value <= -1.6:
        return 'extreme_dry'
    elif spei_value <= -2:
        return 'exceptional_dry'
    else:
        return 'unknown'

output_dir = "G://SME/Paper_2/IndiaDrought/speidata/spei_monthly_2000to2019/"

for file_name in os.listdir(spei_data_dir):
    if os.path.isfile(os.path.join(spei_data_dir, file_name)):
        district_id = file_name.split('_')[-1]
        spei_data = pd.read_csv(os.path.join(spei_data_dir, file_name), sep=' ', usecols=[0, 1, 2, 3, 4],
                                names=['Year', 'Month', 'SPEI-1Mo', 'SPEI-4Mo', 'SPEI-12Mo'], header=None)
        spei_data['SPEI-1Mo_ind'] = spei_data['SPEI-1Mo'].apply(assign_spei_indicator)
        spei_data['SPEI-4Mo_ind'] = spei_data['SPEI-4Mo'].apply(assign_spei_indicator)
        spei_data['SPEI-12Mo_ind']= spei_data['SPEI-12Mo'].apply(assign_spei_indicator)
        spei_data = spei_data[(spei_data['Year'] >= 2000)]
        output_file_path = os.path.join(output_dir, f"spei_{district_id}.txt")
        spei_data.to_csv(output_file_path, sep=',', index=False)
        
#step 2: summarising the district level drought data into three dataframes for 1, 4 and 12 months indicators
def season(mm):
    if mm>=6 and mm<=9:
        return 'summer_monsoon'
    if mm>=10 and mm<=12:
        return 'winter_monsoon'
    else:
        return 'not_monsoon'
    
def make_drought_details(df,drought_period,spei_code):
    years=[2000+i for i in range(20)]
    outdf=pd.DataFrame()
    for year in years:
        tempdf=pd.DataFrame()
        temp=df[df['Year']==year]
        temp['season']=temp['Month'].apply(season)
        
        summer=temp[temp['season']=='summer_monsoon']
        tempdf.loc['summer_monsoon','severe_dry_mo']=summer[summer[drought_period+'_ind']=='severe_dry'].shape[0]
        tempdf.loc['summer_monsoon','extreme_dry_mo']=summer[summer[drought_period+'_ind']=='extreme_dry'].shape[0]
        tempdf.loc['summer_monsoon','exceptional_dry_mo']=summer[summer[drought_period+'_ind']=='exceptional_dry'].shape[0]
        tempdf.loc['summer_monsoon','mean_spei']=summer[drought_period].mean()
        tempdf.loc['summer_monsoon','median_spei']=summer[drought_period].median()
        tempdf.loc['summer_monsoon','max_spei']=summer[drought_period].max()
        tempdf.loc['summer_monsoon','min_spei']=summer[drought_period].min()
        tempdf.loc['summer_monsoon','std_spei']=summer[drought_period].std()
        
        winter=temp[temp['season']=='winter_monsoon']
        tempdf.loc['winter_monsoon','severe_dry_mo']=winter[winter[drought_period+'_ind']=='severe_dry'].shape[0]
        tempdf.loc['winter_monsoon','extreme_dry_mo']=winter[winter[drought_period+'_ind']=='extreme_dry'].shape[0]
        tempdf.loc['winter_monsoon','exceptional_dry_mo']=winter[winter[drought_period+'_ind']=='exceptional_dry'].shape[0]
        tempdf.loc['winter_monsoon','mean_spei']=winter[drought_period].mean()
        tempdf.loc['winter_monsoon','median_spei']=winter[drought_period].median()
        tempdf.loc['winter_monsoon','max_spei']=winter[drought_period].max()
        tempdf.loc['winter_monsoon','min_spei']=winter[drought_period].min()
        tempdf.loc['winter_monsoon','std_spei']=winter[drought_period].std()

        tempdf.loc['allyear_monsoon','severe_dry_mo']=temp[temp[drought_period+'_ind']=='severe_dry'].shape[0]
        tempdf.loc['allyear_monsoon','extreme_dry_mo']=temp[temp[drought_period+'_ind']=='extreme_dry'].shape[0]
        tempdf.loc['allyear_monsoon','exceptional_dry_mo']=temp[temp[drought_period+'_ind']=='exceptional_dry'].shape[0]
        tempdf.loc['allyear_monsoon','mean_spei']=temp[drought_period].mean()
        tempdf.loc['allyear_monsoon','median_spei']=temp[drought_period].median()
        tempdf.loc['allyear_monsoon','max_spei']=temp[drought_period].max()
        tempdf.loc['allyear_monsoon','min_spei']=temp[drought_period].min()
        tempdf.loc['allyear_monsoon','std_spei']=temp[drought_period].std()
        
        tempdf['year']=year
        tempdf=tempdf.reset_index()
        outdf=pd.concat([outdf,tempdf],axis=0).reset_index(drop=True)
    outdf['spei_district_code']=spei_code
    return outdf

def make_drought_agri(df,drought_period,spei_code):
    periods=['201807-201906','201807-201812','201901-201906']
    #outdf=pd.DataFrame()
    df['yearmo']=((df['Year']*100)+df['Month']).astype(int)
    tempdf=pd.DataFrame() 
    for period in periods:
        p1,p2=int(period.split('-')[0]),int(period.split('-')[1])
        temp=df[(df['yearmo']>=p1)&(df['yearmo']<=p2)]
        temp['season']=temp['Month'].apply(season)
        tempdf.loc[period,'severe_dry_mo']=temp[temp[drought_period+'_ind']=='severe_dry'].shape[0]
        tempdf.loc[period,'extreme_dry_mo']=temp[temp[drought_period+'_ind']=='extreme_dry'].shape[0]
        tempdf.loc[period,'exceptional_dry_mo']=temp[temp[drought_period+'_ind']=='exceptional_dry'].shape[0]
        tempdf.loc[period,'mean_spei']=temp[drought_period].mean()
        tempdf.loc[period,'median_spei']=temp[drought_period].median()
        tempdf.loc[period,'max_spei']=temp[drought_period].max()
        tempdf.loc[period,'min_spei']=temp[drought_period].min()
        tempdf.loc[period,'std_spei']=temp[drought_period].std()
    tempdf=tempdf.reset_index()
    #outdf=pd.concat([outdf,tempdf],axis=0).reset_index(drop=True)
    tempdf['spei_district_code']=spei_code
    return tempdf

speifiles=os.listdir(output_dir)

outdfBIG1=pd.DataFrame()
for speifile in speifiles:
    speicode=speifile.split('_')[1].split('.')[0]
    speicode=int(speicode)
    indf=pd.read_csv(output_dir+speifile)
    retdf=make_drought_details(df=indf, drought_period='SPEI-1Mo', spei_code=speicode) ##'SPEI-1Mo, SPEI-4Mo, SPEI-12Mo
    outdfBIG1=pd.concat([outdfBIG1,retdf],axis=0).reset_index(drop=True)

outdfBIG1=outdfBIG1.rename(columns={'index':'season'})
outdfBIG1.to_csv("D://Paper_2/IndiaDrought/drought_atlas/spei1Mo_districts.csv",index=False)

outdfBIG4=pd.DataFrame()
for speifile in speifiles:
    speicode=speifile.split('_')[1].split('.')[0]
    speicode=int(speicode)
    indf=pd.read_csv(output_dir+speifile)
    #retdf=make_drought_details(df=indf, drought_period='SPEI-4Mo', spei_code=speicode)
    retdf=make_drought_agri(df=indf, drought_period='SPEI-4Mo', spei_code=speicode) ##'SPEI-1Mo, SPEI-4Mo, SPEI-12Mo
    outdfBIG4=pd.concat([outdfBIG4,retdf],axis=0).reset_index(drop=True)

#outdfBIG4=outdfBIG4.rename(columns={'index':'season'})
outdfBIG4=outdfBIG4.rename(columns={'index':'survey_reference'})
#outdfBIG4.to_csv("G://SME/paper_2/IndiaDrought/speidata/spei14Mo_districts.csv",index=False)
#outdfBIG4.to_csv("G://SME/Paper_2/IndiaDrought/drought_atlas/situation_of_agri2019_drought.csv",index=False)

outdfBIG12=pd.DataFrame()
for speifile in speifiles:
    speicode=speifile.split('_')[1].split('.')[0]
    speicode=int(speicode)
    indf=pd.read_csv(output_dir+speifile)
    retdf=make_drought_details(df=indf, drought_period='SPEI-12Mo', spei_code=speicode) ##'SPEI-1Mo, SPEI-4Mo, SPEI-12Mo
    outdfBIG12=pd.concat([outdfBIG12,retdf],axis=0).reset_index(drop=True)

outdfBIG12=outdfBIG12.rename(columns={'index':'season'})
outdfBIG12.to_csv("D://Paper_2/IndiaDrought/drought_atlas/spei112Mo_districts.csv",index=False)


outdfBIG12=pd.DataFrame()
for speifile in speifiles:
    speicode=speifile.split('_')[1].split('.')[0]
    speicode=int(speicode)
    indf=pd.read_csv(output_dir+speifile)
    retdf=make_drought_agri(df=indf, drought_period='SPEI-12Mo', spei_code=speicode) ##'SPEI-1Mo, SPEI-4Mo, SPEI-12Mo
    outdfBIG12=pd.concat([outdfBIG12,retdf],axis=0).reset_index(drop=True)

outdfBIG12=outdfBIG12.rename(columns={'index':'survey_reference'})
outdfBIG12.to_csv("G://SME/paper_2/IndiaDrought/drought_atlas/spei12Mo_sit_agri2019.csv",index=False)


## step 2a. combining with state and district names
outdfBIG4=pd.read_csv("G://SME/paper_2/IndiaDrought/speidata/spei14Mo_districts.csv")
outdfBIG4 = outdfBIG4[outdfBIG4['year']>=2010]
outdfBIG4['severe_drought'] = outdfBIG4['severe_dry_mo'] > 0
outdfBIG4['extreme_drought'] = outdfBIG4['extreme_dry_mo'] > 0
outdfBIG4['exceptional_drought'] = outdfBIG4['exceptional_dry_mo'] > 0
speigeo=pd.read_csv("G://SME/paper_2/IndiaDrought/speidata/nss2019_to_spei_directory.csv")
#speigeo['nss_district_code19']=(speigeo['nss_state_code']*100)+(speigeo['nss_district_code'])
#speigeo=speigeo.sort_values(by=['nss_state_name','district_name'])
speigeo = speigeo.drop(index=401)
outdfBIG4=pd.merge(outdfBIG4,speigeo,on='spei_district_code')
outdfBIG4=outdfBIG4.sort_values(by=['nss_state_name','district_name'])
outdfBIG4.to_csv("G://SME/Paper_2/IndiaDrought/drought_atlas/situation_of_agri2019_drought.csv",index=False)
outdfBIG4.to_csv("G://SME/paper_2/IndiaDrought/speidata/spei14Mo_districts.csv",index=False)
