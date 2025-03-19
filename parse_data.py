import pandas as pd
from datetime import datetime

def parse_voorlooprecord(line):
    """
    Parse the given line into its respective fields according to fixed positions.
    Returns a dictionary with the parsed values. For record type 01, "Voorlooprecord"
    """
    
    # Make sure the line is at least 310 chars
    if len(line) < 310:
        raise ValueError("Line must be at least 310 characters long.")
    
    parsed = {
        "Kenmerk record": line[0:2].strip(),
        "Code externe-integratiebericht": line[2:5].strip(),
        "Versienummer berichtstandaard": line[5:7].strip(),
        "Subversienummer berichtstandaard": line[7:9].strip(),
        "Soort bericht": line[9:10].strip(),
        "Code informatiesysteem softwareleverancier": line[10:16].strip(),
        "Versieaanduiding informatiesysteem softwareleverancier": line[16:26].strip(),
        "Uzovi-nummer": line[26:30].strip(),
        "Code servicebureau": line[30:38].strip(),
        "Zorgverlenerscode": line[38:46].strip(),
        "Praktijkcode": line[46:54].strip(),
        "Instellingscode": line[54:62].strip(),
        "Identificatiecode betaling aan": line[62:64].strip(),
        "Begindatum declaratieperiode": line[64:72].strip(),
        "Einddatum declaratieperiode": line[72:80].strip(),
        "Factuurnummer declarant": line[80:92].strip(),
        "Dagtekening factuur": line[92:100].strip(),
        "Btw-identificatienummer": line[100:114].strip(),
        "Valutacode": line[114:117].strip(),
        "Reserve": line[117:310].strip(),
    }
    
    return parsed


def parse_verzekerdenrecord(line):
    """
    Parse the given line into its respective fields according to fixed positions.
    Returns a dictionary with the parsed values. For record type 02, "Verzekerdenrecord"
    """

    # Make sure the line is at least 310 chars
    if len(line) < 310:
        raise ValueError("Line must be at least 310 characters long.")

    parsed = {
        "Kenmerk record": line[0:2].strip(),
        "Identificatie detailrecord": line[2:14].strip(),
        "Burgerservicenummer (bsn) verzekerde": line[14:23].strip(),
        "Uzovi-nummer": line[23:27].strip(),
        "Verzekerdennummer (inschrijvingsnummer, relatienummer)": line[27:42].strip(),
        "Patient(identificatie)nummer": line[42:53].strip(),
        "Datum geboorte verzekerde": line[53:61].strip(),
        "Code geslacht verzekerde": line[61:62].strip(),
        "Naamcode enof naamgebruik (01)": line[62:63].strip(),
        "Naam verzekerde (01)": line[63:88].strip(),
        "Voorvoegsel verzekerde (01)": line[88:98].strip(),
        "Naamcode enof naamgebruik (02)": line[98:99].strip(),
        "Naam verzekerde (02)": line[99:124].strip(),
        "Voorvoegsel verzekerde (02)": line[124:134].strip(),
        "Voorletters verzekerde": line[134:140].strip(),
        "Naamcode enof naamgebruik (03)": line[140:141].strip(),
        "Postcode (huisadres) verzekerde": line[141:147].strip(),
        "Postcode buitenland": line[147:156].strip(),
        "Huisnummer (huisadres) verzekerde": line[156:161].strip(),
        "Huisnummertoevoeging (huisadres) verzekerde": line[161:167].strip(),
        "Code land verzekerde": line[167:169].strip(),
        "Debiteurnummer": line[169:180].strip(),
        "Indicatie client overleden": line[180:181].strip(),
        "Reserve": line[181:310].strip(),
    }

    return parsed

def parse_prestatierecord(line):
    """
    Parse the given line into its respective fields according to fixed positions.
    Returns a dictionary with the parsed values. For record type 04, "Prestatierecord"
    """

    # Make sure the line is at least 310 chars
    if len(line) < 310:
        raise ValueError("Line must be at least 310 characters long.")

    parsed = {
        "Kenmerk record": line[0:2].strip(),
        "Identificatie detailrecord": line[2:14].strip(),
        "Burgerservicenummer (bsn) verzekerde": line[14:23].strip(),
        "Uzovi-nummer": line[23:27].strip(),
        "Verzekerdenummer (inschrijvingsnummer, relatienummer)": line[27:42].strip(),
        "Machtigingsnummer": line[42:57].strip(),
        "Doorsturen toegestaan": line[57:58].strip(),
        "Datum prestatie": line[58:66].strip(),
        "Indicatie soort prestatierecord": line[66:68].strip(),
        "Indicatie bijzondere tandheelkunde": line[68:69].strip(),
        "Soort bijzondere tandheelkunde": line[69:72].strip(),
        "Aanduiding prestatiecodelijst": line[72:75].strip(),
        "Prestatiecode": line[75:81].strip(),
        "Indicatie boven enof onder tandheelkunde": line[81:82].strip(),
        "Gebitselementcode": line[82:84].strip(),
        "Vlakcode": line[84:90].strip(),
        "Aanduiding diagnosecodelijst": line[90:93].strip(),
        "Diagnosecode bijzondere tandheelkunde": line[93:97].strip(),
        "Indicatie ongeval (ongevalsgevolg)": line[97:98].strip(),
        "Zorgverlenerscode behandelaar/uitvoerder": line[98:106].strip(),
        "Specialisme behandelaar/uitvoerder": line[106:110].strip(),
        "Zorgverlenerscode voorschrijver/verwijzer": line[110:118].strip(),
        "Specialisme voorschrijver/verwijzer": line[118:122].strip(),
        "Tarief prestatie (incl. btw)": line[122:130].strip(),
        "Aantal uitgevoerde prestaties": line[130:134].strip(),
        "Berekend bedrag (incl. btw)": line[134:142].strip(),
        "Indicatie debet/credit (01)": line[142:143].strip(),
        "Bedrag vermindering bijzondere tandheelkunde": line[143:151].strip(),
        "Btw-percentage declaratiebedrag": line[151:155].strip(),
        "Declaratiebedrag (incl. btw)": line[155:163].strip(),
        "Indicatie debet/credit (02)": line[163:164].strip(),
        "Referentienummer dit prestatierecord": line[164:184].strip(),
        "Referentienummer voorgaande gerelateerde prestatierecord": line[184:204].strip(),
        "Reserve": line[204:310].strip(),
    }

    return parsed


def parse_commentaarrecord(line):
    """
    Parse the given line into its respective fields according to fixed positions.
    Returns a dictionary with the parsed values. For record type 98, "Commentaarrecord"
    """
    
    # Make sure the line is at least 310 chars
    if len(line) < 310:
        raise ValueError("Line must be at least 310 characters long.")
    
    parsed = {
        "Kenmerk record": line[0:2].strip(),
        "Identificatie detailrecord": line[2:14].strip(),
        "Regelnummer vrije tekst": line[14:18].strip(),
        "Vrije tekst": line[18:158].strip(),
        "Reserve": line[158:310].strip(),
    }
    
    return parsed


def parse_sluitrecord(line):
    """
    Parse the given line into its respective fields according to fixed positions.
    Returns a dictionary with the parsed values. For record type 99, "Sluitrecord"
    """
    
    # Make sure the line is at least 310 chars
    if len(line) < 310:
        raise ValueError("Line must be at least 310 characters long.")
    
    parsed = {
        "Kenmerk record": line[0:2].strip(),
        "Aantal verzekerdenrecords": line[2:8].strip(),
        "Aantal debiteurrecords": line[8:14].strip(),
        "Aantal prestatierecords": line[14:20].strip(),
        "Aantal commentaarrecords": line[20:26].strip(),
        "Totaal aantal detailrecords": line[26:33].strip(),
        "Totaal declaratiebedrag": line[33:44].strip(),
        "Indicatie debet enof credit": line[44:45].strip(),
        "Reserve": line[45:310].strip(),
    }
    
    return parsed


def convert_date(date_string):
    date_object = datetime.strptime(date_string, '%Y%m%d').date()
    return date_object


def check_parsing(df_voorlooprecord, df_verzekerdenrecord, df_prestatierecord, df_commentaarrecord, df_sluitrecord):
    
    ### Print start and end date
    print(f"Begindatum declaratieperiode: {convert_date(df_voorlooprecord['Begindatum declaratieperiode'][0]).strftime('%d-%m-%Y')}")
    print(f"Einddatum declaratieperiode: {convert_date(df_voorlooprecord['Einddatum declaratieperiode'][0]).strftime('%d-%m-%Y')}")
    print(f"-------------------------------")
    
    ### Check if files are aligned
    # Aantal verzekerdenrecords
    verzekerdend = df_sluitrecord['Aantal verzekerdenrecords'].astype(int).iloc[0]
    if verzekerdend == df_verzekerdenrecord.shape[0]:
        print(f"Aantal verzekerdenrecords is {verzekerdend}")
    else:
        print(f"Aantal verzekerdenrecords is {df_verzekerdenrecord.shape[0]}, zou volgens sluitrecords {verzekerdend} moeten zijn.")
    
    # Aantal debiteurrecords Is dit "03"?
  
    # Aantal prestatierecords
    prestaties = df_sluitrecord['Aantal prestatierecords'].astype(int).iloc[0]
    if prestaties == df_prestatierecord.shape[0]:
        print(f"Aantal prestatierecords is {prestaties}")
    else:
        print(f"Aantal prestatierecords is {df_prestatierecord.shape[0]}, zou volgens sluitrecords {prestaties} moeten zijn.")
    
    # Aantal commentaarrecords
    commentaren = df_sluitrecord['Aantal commentaarrecords'].astype(int).iloc[0]
    if commentaren == df_commentaarrecord.shape[0]:
        print(f"Aantal commentaarrecords is {commentaren}")
    else:
        print(f"Commentaarrecords is {df_commentaarrecord.shape[0]}, zou volgens sluitrecords {commentaren} moeten zijn.")
    
    # Totaal declaratierecords
    totaal = df_sluitrecord['Totaal aantal detailrecords'].astype(int).iloc[0]
    totaal_summed = (df_voorlooprecord.shape[0] +
               df_verzekerdenrecord.shape[0] * 2 +
               df_prestatierecord.shape[0] + 
               df_commentaarrecord.shape[0] + 
               df_sluitrecord.shape[0]
               - 2 # don't count voorlop- & sluitrecord
               )
    if totaal == totaal_summed:
        print(f"Totaal aantal detailrecords is {totaal}")
    else:
        print(f"Totaal aantal detailrecords is {totaal_summed}, zou volgens sluitrecords {totaal} moeten zijn")
    
    

