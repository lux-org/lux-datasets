import lux
import pandas as pd

df = pd.read_csv("https://github.com/lux-org/lux-datasets/blob/master/data/hpi_full.csv?raw=True")
df["G10"]  = df["Country"].isin(["Belgium","Canada","France","Germany","Italy","Japan","Netherlands","United Kingdom","Switzerland","Sweden","United States of America"])
df = df[df.columns.drop(list(df.filter(regex='IneqAdj'))+["HPIRank"])]
countries = pd.read_csv("https://github.com/lux-org/lux-datasets/blob/master/data/countries.csv?raw=True")
countries["Country"]=countries["name"].apply(lambda x:x.split(",")[0])
countries.loc[countries["Country"]=='United States',"Country"] = 'United States of America'
countries["landlocked"] = countries["landlocked"].fillna("False").replace(1,"True")
countries["NumOfficialLanguages"]=countries.languages.str.count(",")+1
countries["NumBorderingCountries"]=countries.borders.str.count(",")+1
countries["NumBorderingCountries"]=countries["NumBorderingCountries"].fillna(0)
countries = countries[['Country','cca3', 'landlocked', "NumOfficialLanguages", "NumBorderingCountries",'area']]
df = df.merge(countries)
df = df.rename(index=str, columns={"SubRegion":"Region","subregion":"SubRegion"})
df["Region"] = df.Region.replace("Middle East and North Africa","Middle East")
df.area = df.area.astype(int)
df.loc[df.Country=="Russia","Country"]="Russian Federation"
df.loc[df["Country"]=="Czech Republic","Country"]="Czechia"
df.loc[df.Country=="DR Congo","Country"]="Congo, Democratic Republic of the"#not working?
df.loc[df.Country=="Bolivia","Country"]="Bolivia, Plurinational State of"
df.loc[df["Country"]=="Cote d'Ivoire","Country"]="Côte d'Ivoire"
df.to_csv("hpi_cleaned.csv",index=None)



covid = pd.read_csv("https://github.com/lux-org/lux-datasets/blob/master/data/covid-stringency.csv?raw=True")
covid = covid[covid["Day"]=="2020-03-11"]
covid= covid.rename(columns={"stringency_index":"stringency"})
covid["stringency_level"] = pd.qcut(covid["stringency"],2,labels=["Low","High"])
covid = covid.drop(columns=["stringency","Day"])
covid.to_csv("covid_cleaned.csv",index=None)