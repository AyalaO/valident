import pandas as pd

def merge_data(df_verzekerdenrecord, df_prestatierecord):
    """
    Selects relevant columns and merges everything it into one dataframe.
    Returns a dataframe that contains all information to do the checks"
    """
    
    df_1 = df_verzekerdenrecord[
                        ['Identificatie detailrecord',
                         'Burgerservicenummer (bsn) verzekerde',
                         'Datum geboorte verzekerde',
                         'Naam verzekerde (01)',
                         'Voorletters verzekerde',
                         'Uzovi-nummer'
                        ]]
    
    df_2 = df_prestatierecord[
                        ['Identificatie detailrecord',
                         'Burgerservicenummer (bsn) verzekerde',
                         'Machtigingsnummer',
                         'Datum prestatie',
                         'Indicatie soort prestatierecord',
                         'Prestatiecode',
                         'Gebitselementcode',
                         'Tarief prestatie (incl. btw)',
                         'Aantal uitgevoerde prestaties',
                         'Berekend bedrag (incl. btw)',
                         'Declaratiebedrag (incl. btw)',
                        ]]
    
    df_merged = pd.merge(df_1, 
                         df_2, 
                         on='Burgerservicenummer (bsn) verzekerde', 
                         how='right'
                        )
    return df_merged



def clean_data(df):
    """
    Cleans columns, column names and column dtypes.
    Returns dataframe that has correct names and types.
    """
    
    # rename columns
    df_cleaned = df.rename(columns={
                        'Burgerservicenummer (bsn) verzekerde': 'BSN',
                        'Datum geboorte verzekerde': 'Geboortedatum',
                        'Naam verzekerde (01)': 'Achternaam',
                        'Voorletters verzekerde': 'Voorletters',
                        'Tarief prestatie (incl. btw)': 'Tarief prestatie',
                        'Aantal uitgevoerde prestaties': 'Aantal',
                        'Berekend bedrag (incl. btw)': 'Berekend bedrag',
                        'Declaratiebedrag (incl. btw)': 'Declaratiebedrag'
                    })
    
    # drop columns
    df_cleaned.drop(columns=['Identificatie detailrecord_x', 
                             'Identificatie detailrecord_y'], 
                    inplace=True)
    
    # correct types
    df_cleaned['Geboortedatum'] = pd.to_datetime(df_cleaned['Geboortedatum'], format='%Y%m%d', errors='coerce')
    df_cleaned['Datum prestatie'] = pd.to_datetime(df_cleaned['Datum prestatie'], format='%Y%m%d', errors='coerce')
    df_cleaned['Aantal'] = df_cleaned['Aantal'].astype(int)
    df_cleaned['Tarief prestatie'] = df_cleaned['Tarief prestatie'].astype(float)/100
    df_cleaned['Berekend bedrag'] = df_cleaned['Berekend bedrag'].astype(float)/100
    df_cleaned['Declaratiebedrag'] = df_cleaned['Declaratiebedrag'].astype(float)/100
    
    # add column: leeftijd tijdens behadeling
    df_cleaned["Leeftijd"] = (df_cleaned["Datum prestatie"] - df_cleaned["Geboortedatum"]).dt.days // 365
    
    # add verzekeraar naam
    df_uzovi = pd.read_csv('data/lookup_uzovi.csv', dtype={"Uzovi-nummer": str})
    df_cleaned = pd.merge(df_cleaned, df_uzovi, how='left', on='Uzovi-nummer')
    
    # order and select columns
    df_cleaned = df_cleaned[[
        'BSN', 
        'Geboortedatum', 
        'Achternaam', 
        'Voorletters', 
        'Verzekering',
        'Uzovi-nummer',
        'Machtigingsnummer', 
        'Datum prestatie', 
        'Indicatie soort prestatierecord',
        'Prestatiecode',
        'Gebitselementcode', 
        'Tarief prestatie', 
        'Aantal', 
        'Berekend bedrag',
        'Declaratiebedrag', 
        'Leeftijd'
    ]]
    
    return df_cleaned