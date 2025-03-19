import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Valident")

cols_display = ["Datum",
                "Achternaam",
                "Geboortedatum patiënt",
                "Tariefcode:",
                "Omschrijving", 
                "Patiëntgegevens", 
                "VolgNummer", 
                "Dossiernummer",
                "Uitgevoerd door"
               ]

def display_format(df):
    df_formatted = df[cols_display].sort_values(by=["Datum", "Achternaam"]).reset_index(drop=True)
    for col in df_formatted.select_dtypes(include=['datetime64[ns]']):
        df_formatted[col] = df_formatted[col].dt.strftime('%d-%m-%Y')
    return df_formatted

def read_data(file):
    df = pd.read_excel(file)
    return df

def find_errors_x21_age(df):
    today = pd.Timestamp.today()
    df['Age'] = df['Geboortedatum patiënt'].apply(lambda dob: (today - dob).days // 365 if pd.notnull(dob) else None)
    condition = df['Tariefcode:'].astype(str).str.contains("X21") & (df['Age'] < 18)
    return df[condition][cols_display]

def find_errors_c_t(df):
    # Step 1: Check if 'J' contains "C" or "T"
    condition_part1 = df['Tariefcode:'].astype(str).str.contains("C", na=False) | \
                        df['Tariefcode:'].astype(str).str.contains("T", na=False)
    # Step 2: Create boolean masks and compute counts per group [Achternaam, Datum]
    mask_C = df['Tariefcode:'].astype(str).str.contains("C", na=False)
    mask_T = df['Tariefcode:'].astype(str).str.contains("T", na=False)
    df['count_C_T'] = df.groupby(['Achternaam', 'Datum'])['Tariefcode:'].transform(
        lambda x: x.astype(str).str.contains("C", na=False).sum() + 
                x.astype(str).str.contains("T", na=False).sum()
    )
    # Step 3: Check if the count is greater than 1
    count_condition = df['count_C_T'] > 1
    # Step 4: Combine conditions
    final_condition = condition_part1 & count_condition
    # Step 5: Filter rows based on the condition
    return df[final_condition]

def find_errors_a10_h(df):
    # Create masks for rows where column J contains "A10" or "H"
    mask_A10 = df['Tariefcode:'].str.contains("A10", na=False)
    mask_H = df['Tariefcode:'].str.contains("H", na=False)
    # For each row, within the same group defined by columns 'A' and 'F',
    # count how many rows have "H" in column J
    count_H = df.groupby(['Achternaam', 'Datum'])['Tariefcode:'].transform(
        lambda x: x.str.contains("H", na=False).sum()
    )
    # Similarly, count how many rows in the same group have "A10" in column J
    count_A10 = df.groupby(['Achternaam', 'Datum'])['Tariefcode:'].transform(
        lambda x: x.str.contains("A10", na=False).sum()
    )
    # Replicate the Excel logic:
    condition = (mask_A10 & (count_H > 0)) | (mask_H & (count_A10 > 0))
    # Step 5: Filter rows based on the condition
    return df[condition]

def find_errors_g72(df):
    condition = df['Tariefcode:'] == 'G72'
    return df[condition]
    

# set-up sidebar layout 
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
my_upload = st.sidebar.file_uploader("", type=["xlsx"])

if my_upload is not None:
    # read and parse data
    df = read_data(my_upload)

    # set-up main page
    # TODO: if df_error is empty display ✔️, otherwise display ✖️ for expander icon
    with st.expander("**C- en T-codes mogen niet op dezelfde behandeldatum voorkomen**", expanded=False, icon="✔️"):
        st.write(display_format(find_errors_c_t(df)))

    with st.expander("**A10- en H-codes mogen niet samen op dezelfde behandeldatum voorkomen**", expanded=False, icon="✔️"):
        st.write(display_format(find_errors_a10_h(df)))

    with st.expander("**X21 mag niet gedeclareerd worden voor patiënten jonger dan 18 jaar**", expanded=False, icon="✔️"):
        st.write(display_format(find_errors_x21_age(df)))

    with st.expander("**G72 mag niet gedeclareerd worden**", expanded=False, icon="✔️"):
        st.write(display_format(find_errors_g72(df))) 
else:
    st.markdown("#### Welkom bij Valident!")
    st.markdown("Upload een Excel-bestand via de linkerzijbalk om alle ongeldige declaraties te vinden.")
    st.markdown("Na het uploaden worden de gegevens gecontroleerd en krijg je een overzicht van de foutieve codecombinaties..")
    st.image("imgs/pijl.png", width=150)
