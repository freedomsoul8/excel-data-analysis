import pandas as pd


data_file = 'data.xlsx'
result_file = ''

try:
    df = pd.read_excel(f'{data_file}')
except:
    df = pd.read_csv(f'{data_file}')

df['hour'] = pd.to_datetime(df['Timestamp'], format="%Y-%m-%d %H:%M:%S").dt.hour


timestamps = df['hour'].unique()
timestamps.tolist()

# Params
types = ['CFB','CFNA','CFNR','MTCall']
callCauses = [0,200]

data = []

for period in timestamps:
    for obj in types:
        for cause in callCauses:
            GD = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].sum(numeric_only=True)['GreetingDuration']
            RD = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].sum(numeric_only=True)['RecordDuration']
            DCR = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].nunique()['Caller']
            DCC = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].nunique()['Called']
            CC = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].count()['Called']
            CR = df[(df["Type"] == obj) & (df["CallCause"] == int(cause)) & (df["hour"] == period)].count()['Caller']
            row = [period,obj,str(cause),str(GD),str(RD),str(DCR),str(DCC),str(CC),str(CR)]
            data.append(row)


new_df = pd.DataFrame(data,columns=['Timestamp','Type','CallCause','GreetingDuration','RecordDuration','UniqueCaller','UniqueCalled','CountOfCalled','CountOfCaller'])

new_df.to_csv(f'{result_file}.csv',header=['Timestamp','Type','CallCause','GreetingDuration','RecordDuration','UniqueCaller','UniqueCalled','CountOfCalled','CountOfCaller'],sep=';',index_label=False)
