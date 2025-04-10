import pandas as pandas

def clean_data(df):

    # # select relevant columns
    # df = df[['Achternaam',
    #      'Patiëntgegevens',
    #      'Geboortedatum patiënt', 
    #      'Datum', 
    #      'Tariefcode:', 
    #      'Element', 
    #      'Honorarium']]

    # # rename columns to match with mz301 as much as possible
    # df = df.rename(columns={'Geboortedatum patiënt': 'Geboortedatum',
    #                         'Patiëntgegevens': 'Patientgegevens',
    #                         'Datum': 'Datum prestatie',
    #                         'Tariefcode:': 'Prestatiecode',
    #                         'Element': 'Gebitselementcode',
    #                         'Honorarium': 'Tarief prestatie',
    #                         })


    # select relevant columns
    df = df[['PatientAchterNaam',
         'PatientInfo',
         'GeboorteDatum', 
         'Datum', 
         'code', 
         'Elementen', 
         'Honorarium']]

    # rename columns to match with mz301 as much as possible
    df = df.rename(columns={'GeboorteDatum': 'Geboortedatum',
                            'PatientInfo': 'Patientgegevens',
                            'Datum': 'Datum prestatie',
                            'code': 'Prestatiecode',
                            'Elementen': 'Gebitselementcode',
                            'Honorarium': 'Tarief prestatie',
                            'PatientAchterNaam': 'Achternaam'
                            })

    # create Leeftijd columns
    df['Leeftijd'] = (df["Datum prestatie"] - df["Geboortedatum"]).dt.days // 365

    return df