import pandas as pd
import csv

source_file_full_path = ".\\source\\NewYearHonoursList2019.csv"
output_file_full_path = ".\\output\\NewYearHonoursList2019_x.csv"

df = pd.read_csv(source_file_full_path,encoding='iso-8859-1',skiprows=1)

# Suffixes we wanna identify
suffixes = [
    "KG","LG","KT","LT","GCB","KCB","DCB","CB","GCMG","KCMG","DCMG","CMG","DSO","GCVO",
    "KCVO","DCVO","CVO","LVO","MVO","OM","ISO","GBE","KBE","DBE","CBE","OBE","MBE","CH",
    "VC","GC","KP","GCSI","GCIE","VA","CI","KCSI","KCIE","CSI","CIE","ISM","MVO","MBE",
    "IOM","CGC","RRC","DSC","MC","DFC","AFC","ARRC","OBI","DCM","CGM","GM","IDSM","DSM",
    "MM","DFM","AFM","SGM","IOM","CPM","QGM","RVM","BEM","KPM","KPFSM","QPM","QFSM","QAM",
    "QVRM","MSM","ERD","VD","TD","UD","ED","RD","VRD","AE","QV","MNM","PC","ADC","ADC(P)",
    "QHP","QHS","QHDS","QHNS","QHC","SCJ","J","LJ","P","DP","LC","CJ","MR","C","QS","SL",
    "KC","QC","JP","DL","MP","MSP","AM","MLA","MHK","SHK","MLC","MEP","FRS","FBA","FRSE",
    "AC","FRS","FRENG","ONZ"]

# Prefixes we wanna identify
prefixes = [
    "Hon","Rt","Professor","Prof","Dr","Councillor","Colonel","Reverend","Brig","Baroness",
    "Lady","Sheriff","Imam","Archbishop","Very","Rev","The","Lord","Mr","Lt","Mrs","Ms",
    "Major","Capt","Captain","Miss","Sir","Commander","Doctor","Dame","His","Honour",
    "Bishop","Mufti","Col","(Retd)","(rtd)","Baron","Sister","Chief","Superintendent"
]

# Word search function
def word_finder(x,list_type):
  df_words = set(x.split(' '))
  extract_words =  set(list_type).intersection(df_words)
  return ' '.join(extract_words)

# Lose any redundant commas
df['New_name'] = df['Name'].str.replace(',', '')

# Fix any weird spacings between hyphenated words
df['New_name'] = df['New_name'].str.replace(' - ', '-')

# Suffix calcs
df['Suffix_temp'] = df.New_name.apply(word_finder,args=(suffixes,))
df['Suffix_len'] = df['Suffix_temp'].str.len()
df['New_len'] = df['New_name'].str.len() - df['Suffix_temp'].str.len()

# Get suffixes
df['Suffix'] = df.apply(lambda x: x['New_name'][x['New_len']:],axis=1)

# Remove suffixes
df['New_name'] = df.apply(lambda x: x['New_name'][:x['New_len']],axis=1)

# Get prefixes
df['Prefix_temp'] = df.New_name.apply(word_finder,args=(prefixes,))
df['Prefix_len'] = df['Prefix_temp'].str.len()
df['Prefix'] = df.apply(lambda x: x['New_name'][:x['Prefix_len']],axis=1)

# Remove prefixes
df['New_name'] = df.apply(lambda x: x['New_name'][x['Prefix_len']:],axis=1)

# Get alternative names (names in brackets)
df['Alt_name'] = df['New_name'].str.extract('.*\((.*)\).*')
df['Alt_name'] = df['Alt_name'].fillna('')

# Remove names in brackets
df['New_name'] = df['New_name'].str.replace(r"\(.*\)","")
df['New_name'] = df['New_name'].str.strip()

# Get LastNames
df['LastName'] = df['New_name'].str.extract("([- A-Z'É]+$)")

# Remove LastNames
df['Len'] = df['New_name'].str.len() - df['LastName'].str.len()
df['New_name'] = df.apply(lambda x: x['New_name'][:x['Len']],axis=1)

#Get first name
df2 = pd.DataFrame(df['New_name'].str.split(None,1).tolist(),columns="FirstName MiddleNames".split())

# Create a new data frame containing all the relevant fields
df3 = pd.DataFrame()

df3['Prefix'] = df['Prefix']
df3['FirstName'] = df2['FirstName']
df3['MiddleNames'] = df2['MiddleNames'].str.strip()
df3['LastName'] = df['LastName'].str.strip()
df3['Suffix'] = df['Suffix']
df3['AKA'] = df['Alt_name']
df3['OriginalName'] = df['Name'].str.strip()
df3['Order'] = df['Order']
df3['Level'] = df['Level']
df3['Award'] = df['Award']
df3['Citation'] = df['Citation']
df3['County'] = df['County']

# output
df3.to_csv(output_file_full_path, index=None, header=True, quoting=csv.QUOTE_NONNUMERIC, encoding='iso-8859-1')
