import streamlit as st
import pandas as pd
from datetime import datetime

from parse_data import (
                    parse_voorlooprecord, 
                    parse_verzekerdenrecord, 
                    parse_prestatierecord, 
                    parse_commentaarrecord, 
                    parse_sluitrecord, 
                    check_parsing
)
from clean_data import (
                    merge_data,
                    clean_data
)

def display(df):
    """
    Formats the dataframe to display cleanly
    Returns df to be displayed in app
    """
    display_cols = ['BSN',
                    'Geboortedatum',
                    'Achternaam',
                    'Voorletters',
                    'Datum prestatie',
                    'Prestatiecode',
                    'Gebitselementcode',
                    'Tarief prestatie',
                    'Aantal',
                    'Declaratiebedrag',
                    'Verzekering',
                    'Machtigingsnummer'
                    ]

    df_display = (df[display_cols]
                    .sort_values(by=["Datum prestatie", "Achternaam"], ascending=[True, True])
                    .reset_index(drop=True))

    for col in df_display.columns:
        # Check if the column's dtype is datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # Convert the datetime to a string in the format dd-mm-YYYY
            df_display[col] = df_display[col].dt.strftime('%d-%m-%Y')
    
    return df_display

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
    string_data = my_upload.getvalue().decode("ISO-8859-1")  # decode bytes to string
    lines = string_data.splitlines()

    # parse data line by line per record type
    voorlooprecord = [parse_voorlooprecord(ln) for ln in lines if ln[0:2] == "01"]
    verzekerdenrecord = [parse_verzekerdenrecord(ln) for ln in lines if ln[0:2] == "02"]
    prestatierecord = [parse_prestatierecord(ln) for ln in lines if ln[0:2] == "04"]
    commentaarrecord = [parse_commentaarrecord(ln) for ln in lines if ln[0:2] == "98"]
    sluitrecord = [parse_sluitrecord(ln) for ln in lines if ln[0:2] == "99"]

    # convert to clean dfs
    df_voorlooprecord = pd.DataFrame(voorlooprecord)
    df_verzekerdenrecord = pd.DataFrame(verzekerdenrecord)
    df_prestatierecord = pd.DataFrame(prestatierecord)
    df_commentaarrecord = pd.DataFrame(commentaarrecord)
    df_sluitrecord = pd.DataFrame(sluitrecord)

    # check parsing TODO: add proper logging
    check_parsing(df_voorlooprecord, df_verzekerdenrecord, df_prestatierecord, df_commentaarrecord, df_sluitrecord)

    # clean data
    df_merged = merge_data(df_verzekerdenrecord, df_prestatierecord)
    df = clean_data(df_merged)

    ### DISPLAY RESULTS
  
    # C- en T-codes mogen niet op dezelfde behandeldatum voorkomen
    df_filter = (
            df.groupby(["BSN", "Datum prestatie"])
            .filter(
                lambda group: group["Prestatiecode"].str.contains("C").any() 
                                and group["Prestatiecode"].str.contains("T").any()))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("C|T")]
    if df_filter.shape[0] > 0:
        with st.expander("**C- en T-codes mogen niet op dezelfde behandeldatum voorkomen**", expanded=False, icon="✖️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("**C- en T-codes mogen niet op dezelfde behandeldatum voorkomen**", expanded=False, icon="✔️"):
            st.dataframe(display(df_filter))

    # A10- en H-codes mogen niet samen op dezelfde behandeldatum voorkomen
    df_filter = (
        df.groupby(["BSN", "Datum prestatie"])
        .filter(
            lambda group: group["Prestatiecode"].str.contains("A10").any() 
                            and group["Prestatiecode"].str.contains("H").any()))
    df_filter = df_filter[df_filter["Prestatiecode"].str.contains("A10|H")]
    if df_filter.shape[0] > 0:
        with st.expander("**A10- en H-codes mogen niet samen op dezelfde behandeldatum voorkomen**", expanded=False, icon="✖️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("**A10- en H-codes mogen niet samen op dezelfde behandeldatum voorkomen**", expanded=False, icon="✔️"):
            st.dataframe(display(df_filter))

    # X21 voor patiënten jonger dan 18 jaar moet machtigingsnummer hebben
    mask_filter = (
        (df["Leeftijd"] < 18)
        & (df["Prestatiecode"] == "X21")
        & (
            df["Machtigingsnummer"].isna()            # missing entirely
            | (df["Machtigingsnummer"] == "")         # empty string
            | (df["Machtigingsnummer"].str.len() < 5))) # fewer than 5 chars
    df_filter = df[mask_filter]
    if df_filter.shape[0] > 0:
        with st.expander("**X21 voor patiënten jonger dan 18 jaar moet machtigingsnummer hebben**", expanded=False, icon="✖️"):
            st.dataframe(display(df_filter))
    else:
        with st.expander("**X21 voor patiënten jonger dan 18 jaar moet machtigingsnummer hebben**", expanded=False, icon="✔️"):
            st.dataframe(display(df_filter))


else:
    st.markdown("#### Welkom bij Valident!")
    st.markdown("Upload een bestand via de linkerzijbalk om alle ongeldige declaraties te vinden.")
    st.markdown("Na het uploaden worden de gegevens gecontroleerd en krijg je een overzicht van de foutieve codecombinaties..")
    st.image("imgs/pijl.png", width=150)