import streamlit as st
import pandas as pd
from datetime import datetime

from clean_data_excel import (
                    clean_data
)
from helpers import require_password

def display(df):
    """
    Formats the dataframe to display cleanly
    Returns df to be displayed in app 
    """
    display_cols = ['Geboortedatum',
                    'Achternaam',
                    #'Voorletters', # niet beschikbaar in excel
                    'Datum prestatie',
                    'Prestatiecode',
                    'Gebitselementcode',
                    'Techniek',
                    'Honorarium',
                    'Totaal Bedrag',
                    #'Aantal', # niet beschikbaar in excel
                    #'Declaratiebedrag', # # niet beschikbaar in excel
                    #'Verzekering', # niet beschikbaar in excel
                    #'Machtigingsnummer' # niet beschikbaar in excel
                    ]

    df_display = (df[display_cols]
                    .sort_values(by=["Datum prestatie", "Achternaam", "Geboortedatum"], ascending=[True, True, True])
                    .reset_index(drop=True))

    for col in df_display.columns:
        # Check if the column's dtype is datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Convert the datetime to a string in the format dd-mm-YYYY
            df_display[col] = df_display[col].dt.strftime('%d-%m-%Y')
    
    return df_display


require_password()

# set-up sidebar 
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #C8D2DA;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("imgs/logo_valident.png")
st.sidebar.write("")
st.sidebar.write("")
my_upload = st.sidebar.file_uploader("")


# set-up main page
if my_upload is not None:
    # read data
    df = pd.read_excel(my_upload)

    # clean data
    df = clean_data(df)

    ### DISPLAY RESULTS #############################################

    ### code combinaties ############################################
    st.write('**Code combinaties**')

    # C- en T-codes mogen niet op dezelfde behandeldatum voorkomen
    df_filter = (
            df.groupby(["Patientgegevens", "Datum prestatie"])
            .filter(
                lambda group: group["Prestatiecode"].str.contains("C").any() 
                                and group["Prestatiecode"].str.contains("T").any()))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("C|T")]
    if df_filter.shape[0] > 0:
        with st.expander("C- en T-codes mogen niet op dezelfde behandeldatum voorkomen", expanded=False, icon="🔴"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("C- en T-codes mogen niet op dezelfde behandeldatum voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # A10- en H-codes mogen niet op dezelfde behandeldatum voorkomen
    df_filter = (
        df.groupby(["Patientgegevens", "Datum prestatie", "Gebitselementcode"])
        .filter(
            lambda group: group["Prestatiecode"].str.contains("A10").any() 
                            and group["Prestatiecode"].str.contains("H").any()))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("A10|H")]
    if df_filter.shape[0] > 0:
        with st.expander("A10- en H-codes mogen niet op dezelfde behandeldatum en element voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("A10- en H-codes mogen niet op dezelfde behandeldatum en element voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # E02 en C001, C002 of C003 mogen niet op dezelfde behandeldatum voorkomen
    df_filter = (
    df.groupby(["Patientgegevens", "Datum prestatie"])
      .filter(
          lambda group: group["Prestatiecode"].eq("E02").any()
                         and group["Prestatiecode"].isin(["C001", "C002", "C003"]).any()
      ))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("E02|C001|C002|C003")]
    if df_filter.shape[0] > 0:
        with st.expander("E02 en C001, C002 of C003 mogen niet op dezelfde behandeldatum voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("E02 en C001, C002 of C003 mogen niet op dezelfde behandeldatum voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))
    
    # G72 mag niet gedeclareerd worden
    df_filter = df[df['Prestatiecode']=='G72']
    if df_filter.shape[0] > 0:
        with st.expander("G72 mag niet gedeclareerd worden", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("G72 mag niet gedeclareerd worden", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # # J049 vereist machtigingsnummer en voorloopcode 002
    # mask_filter = (
    # (df["Prestatiecode"] == "J049")
    # &
    # (
    #     df["Geboortedatum"].isna()  # no birthdate
    #     # OR Machigingsnummer is invalid:
    #     | df["Machtigingsnummer"].isna()            # missing
    #     | (df["Machtigingsnummer"] == "")           # empty
    #     | (df["Machtigingsnummer"].str.len() < 5)   # fewer than 5 chars
    # ))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("J049 vereist machtigingsnummer en voorloopcode 002", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("J049 vereist machtigingsnummer en voorloopcode 002", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # V30 mag maximaal 1 keer op dezelfde behandeldatum voorkomen
    mask_filter = (
    (df["Prestatiecode"] == "V30")
    & (
        df.groupby(["Patientgegevens", "Datum prestatie"])["Prestatiecode"]
          .transform(lambda s: (s == "V30").sum()) > 1
    ))
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("V30 mag maximaal 1 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("V30 mag maximaal 1 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # V35 mag maximaal 1 keer op dezelfde behandeldatum en element voorkomen
    mask_filter = (
    (df["Prestatiecode"] == "V35")
    & (
        df.groupby(["Patientgegevens", "Datum prestatie", "Gebitselementcode"])["Prestatiecode"]
          .transform(lambda s: (s == "V35").sum()) > 1
    ))
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("V35 mag maximaal 1 keer op dezelfde behandeldatum en element voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("V35 mag maximaal 1 keer op dezelfde behandeldatum en element voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))
    
    # P045 mag maximaal 1 keer op dezelfde behandeldatum en element voorkomen
    mask_filter = (
    (df["Prestatiecode"] == "P045")
    & (
        df.groupby(["Patientgegevens", "Datum prestatie", "Gebitselementcode"])["Prestatiecode"]
          .transform(lambda s: (s == "P045").sum()) > 1
    ))
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("P045 mag maximaal 1 keer op dezelfde behandeldatum en element voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("P045 mag maximaal 1 keer op dezelfde behandeldatum en elementvoorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))
    
    # P045 vereist vermelding van elementnummer
    mask_filter = (
    (df["Prestatiecode"] == "P045")
    & (
        df["Gebitselementcode"].isna()            # missing (NaN)
        | (df["Gebitselementcode"] == "")         # empty string
        # | (df["Gebitselementcode"].str.len() != 2)  # length not equal to 2
    ))

    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("P045 vereist vermelding van elementnummer", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("P045 vereist vermelding van elementnummer", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))
    
    # P045 mag maximal 8x voorkomen voor oner- of bovenkaak op zelfde datum
    mask_filter = (
    # 1) >8 P045→Bovenkaak
    (df
     .groupby(["Patientgegevens","Datum prestatie"])["Gebitselementcode"]
     .transform(lambda s: (
         (df.loc[s.index, "Prestatiecode"] == "P045")
         & (s == "Bovenkaak")
     ).sum())
     > 8)

    |  # 2) >8 P045→Onderkaak
    (df
     .groupby(["Patientgegevens","Datum prestatie"])["Gebitselementcode"]
     .transform(lambda s: (
         (df.loc[s.index, "Prestatiecode"] == "P045")
         & (s == "Onderkaak")
     ).sum())
     > 8)

    |  # 3) >8 P045→prefix “1” or “2”
    (df
     .groupby(["Patientgegevens","Datum prestatie"])["Gebitselementcode"]
     .transform(lambda s: (
         (df.loc[s.index, "Prestatiecode"] == "P045")
         & s.astype(str).str[0].isin(["1", "2"])
     ).sum())
     > 8)

    |  # 4) >8 P045→prefix “3” or “4”
    (df
     .groupby(["Patientgegevens","Datum prestatie"])["Gebitselementcode"]
     .transform(lambda s: (
         (df.loc[s.index, "Prestatiecode"] == "P045")
         & s.astype(str).str[0].isin(["3", "4"])
     ).sum())
     > 8)
    )

    df_filter = df[(df["Prestatiecode"] == "P045") & mask_filter]

    if df_filter.shape[0] > 0:
        with st.expander("P045 mag maximal 8x voorkomen voor onder- of bovenkaak op zelfde datum", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("P045 mag maximal 8x voorkomen voor onder- of bovenkaak op zelfde datum", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # C022 mag maximaal 4 keer op dezelfde behandeldatum voorkomen
    mask_filter = (
    (df["Prestatiecode"] == "C022")
    & (
        df.groupby(["Patientgegevens", "Datum prestatie"])["Prestatiecode"]
          .transform(lambda s: (s == "C022").sum()) > 4
    ))
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("C022 mag maximaal 4 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("C022 mag maximaal 4 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # J042 en J043 mag niet op dezelfde behandeldatum voorkomen met R-codes
    df_filter = (
        df.groupby(["Patientgegevens", "Datum prestatie"])
        .filter(
            lambda group: (group["Prestatiecode"].isin(["J042", "J043"]).any()
            and group["Prestatiecode"].str.contains("R", na=False).any())
        )
    )
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("J042|J043|R", na=False)]
    if df_filter.shape[0] > 0:
        with st.expander("J042 en J043 mag niet op dezelfde behandeldatum voorkomen met R-codes", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("J042 en J043 mag niet op dezelfde behandeldatum voorkomen met R-codes", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))

    # J042 en J043 mag niet op dezelfde behandeldatum voorkomen met J040 of J041
    df_filter = (
    df.groupby(["Patientgegevens", "Datum prestatie"])
      .filter(
          lambda group: (group["Prestatiecode"].isin(["J042", "J043"]).any()
           and group["Prestatiecode"].isin(["J040", "J041"]).any()
      )))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("J042|J043|J040|J041")]
    if df_filter.shape[0] > 0:
        with st.expander("J042 en J043 mag niet op dezelfde behandeldatum voorkomen met J040 of J041", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("J042 en J043 mag niet op dezelfde behandeldatum voorkomen met J040 of J041", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))        
        
    # T102 mag maximaal 1 keer op dezelfde behandeldatum voorkomen
    mask_filter = (
    (df["Prestatiecode"] == "T102")
    & (
        df.groupby(["Patientgegevens", "Datum prestatie"])["Prestatiecode"]
          .transform(lambda s: (s == "T102").sum()) > 1
    ))
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("T102 mag maximaal 1 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("T102 mag maximaal 1 keer op dezelfde behandeldatum voorkomen", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))


    # ### onder 18 jaar #########################################################
    # st.write('**Onder 18 jaar**')

    # # X21 voor patiënten jonger dan 18 jaar vereist machtigingsnummer
    # mask_filter = (
    #     (df["Leeftijd"] < 18)
    #     & (df["Prestatiecode"] == "X21")
    #     & (
    #         df["Machtigingsnummer"].isna()            # missing entirely
    #         | (df["Machtigingsnummer"] == "")         # empty string
    #         | (df["Machtigingsnummer"].str.len() < 5))) # fewer than 5 chars
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("X21 voor patiënten jonger dan 18 jaar vereist machtigingsnummer", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("X21 voor patiënten jonger dan 18 jaar vereist machtigingsnummer", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # G-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ
    # mask_filter = (
    # (df["Prestatiecode"] == "G") 
    # & (df["Leeftijd"] < 18) 
    # & (df["Verzekering"].str.contains("VGZ", na=False))
    # & (
    #     df["Machtigingsnummer"].isna()               # missing 
    #     | (df["Machtigingsnummer"] == "")            # empty string
    #     | (df["Machtigingsnummer"].str.len() < 5)    # fewer than 5 characters
    # ))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("G-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("G-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # T-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ
    # mask_filter = (
    # (df["Prestatiecode"] == "T") 
    # & (df["Leeftijd"] < 18) 
    # & (df["Verzekering"].str.contains("VGZ", na=False))
    # & (
    #     df["Machtigingsnummer"].isna()               # missing 
    #     | (df["Machtigingsnummer"] == "")            # empty string
    #     | (df["Machtigingsnummer"].str.len() < 5)    # fewer than 5 characters
    # ))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("T-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("T-codes voor patiënten jonger dan 18 jaar vereist machtigingsnummer bij VGZ", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))


    # ### minimale techniek kosten ############################################
    # st.write('**Minimale techniek kosten**')

    # # R24 minimale techniekkosten van 250 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "R24") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 250))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("R24 minimale techniekkosten van 250 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("R24 minimale techniekkosten van 250 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # R34 minimale techniekkosten van 525 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "R34") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 525))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("R34 minimale techniekkosten van 525 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("R34 minimale techniekkosten van 525 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))

    # # F471A minimale techniekkosten van 400 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "F471A") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 400))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("F471A minimale techniekkosten van 400 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("F471A minimale techniekkosten van 400 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))

    # # F461A minimale techniekkosten van 400 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "F461A") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 400))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("F461A minimale techniekkosten van 400 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("F461A minimale techniekkosten van 400 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))

    # # F813A minimale techniekkosten van 25 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "F813A") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 25))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("F813A minimale techniekkosten van 25 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("F813A minimale techniekkosten van 25 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # G69 minimale techniekkosten van 130 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "G69") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] < 130))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("G69 minimale techniekkosten van 130 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("G69 minimale techniekkosten van 130 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))

    # ### maximale techniek kosten ############################################
    # st.write('**Maximale techniek kosten**')

    # # P023 maximale techniekkosten van 325 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "P023") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 325))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("P023 maximale techniekkosten van 325 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("P023 maximale techniekkosten van 325 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # P020 maximale techniekkosten van 380 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "P020") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 380))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("P020 maximale techniekkosten van 380 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("P020 maximale techniekkosten van 380 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # P022 maximale techniekkosten van 705 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "P022") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 705))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("P022 maximale techniekkosten van 705 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("P022 maximale techniekkosten van 705 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # P068 maximale techniekkosten van 76 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "P068") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 76))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("P068 maximale techniekkosten van 76 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("P068 maximale techniekkosten van 76 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # P062 maximale techniekkosten van 109 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "P062") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 109))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("P062 maximale techniekkosten van 109 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("P062 maximale techniekkosten van 109 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # J100 maximale techniekkosten van 217 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "J100") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 217))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("J100 maximale techniekkosten van 217 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("J100 maximale techniekkosten van 217 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # J101 maximale techniekkosten van 217 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "J101") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 217))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("J101 maximale techniekkosten van 217 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("J101 maximale techniekkosten van 217 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
    
    # # J104 maximale techniekkosten van 93 euro
    # mask_filter = (
    # (df["Prestatiecode"] == "J104") &
    # (df["Indicatie soort prestatierecord"] == "02") & # Techniekkosten aangegeven met "02"
    # (df["Tarief prestatie"] > 93))
    # df_filter = df[mask_filter]
    # if df_filter.shape[0] > 0:
    #     with st.expander("J104 maximale techniekkosten van 93 euro", expanded=False, icon="🔴️"):
    #         st.dataframe(display(df_filter))
    # else:
    #     with st.expander("J104 maximale techniekkosten van 93 euro", expanded=False, icon="✅"):
    #         st.dataframe(display(df_filter))
  
    ### overige checks ############################################
    st.write('**Overige Checks**')
    # Negatieve bedragen
    df_filter = df[(df['Totaal Bedrag']<0) | 
                   (df['Techniek']<0) | 
                   (df['Honorarium']<0) ]
    if df_filter.shape[0] > 0:
        with st.expander("Negatief bedrag", expanded=False, icon="🔴️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("Negatief bedrag", expanded=False, icon="✅"):
            st.dataframe(display(df_filter))


else:
    st.markdown("#### Welkom bij Valident!")
    st.markdown("Upload een bestand via de linkerzijbalk om alle ongeldige declaraties te vinden.")
    st.markdown("Na het uploaden worden de gegevens gecontroleerd en krijg je een overzicht van de foutieve codecombinaties..")
    st.image("imgs/pijl.png", width=150)