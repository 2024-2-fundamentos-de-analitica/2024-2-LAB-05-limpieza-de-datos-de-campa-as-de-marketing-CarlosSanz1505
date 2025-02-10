"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os
    import shutil
    import glob
    import pandas as pd
    import calendar

    # Restablecer estado del directorio files antes de ejecutar
    if os.path.exists('./files/output'):
        shutil.rmtree('./files/output')
    
    # Obtener datos
    dataframes = []
    for pathname in glob.glob('./files/input/*.csv.zip'):
        dataframes.append(pd.read_csv(pathname))
    data = pd.concat(dataframes, ignore_index=True)
    print(data.columns)

    # Función auxiliar (remplazo con multiples casos)
    def replace_all(str, dic):
        for old, new in dic.items():
            str = str.replace(old, new)
        return str
    
    # Limpieza para client.csv
    job_rep = {'.': '', '-': '_'}
    data['job'] = data['job'].apply(lambda j: replace_all(j, job_rep))
    data['education'] = data['education'].apply(lambda e: pd.NA if e == 'unknown' else e.replace('.', '_'))
    data['credit_default'] = data['credit_default'].apply(lambda c: 1 if c == 'yes' else 0)
    data['mortgage'] = data['mortgage'].apply(lambda m: 1 if m == 'yes' else 0)

    # Limpieza para campaign.csv
    month_num = {month.lower(): index for index, month in enumerate(calendar.month_abbr) if month}
    data['previous_outcome'] = data['previous_outcome'].apply(lambda p: 1 if p == 'success' else 0)
    data['campaign_outcome'] = data['campaign_outcome'].apply(lambda c: 1 if c == 'yes' else 0)
    data['last_contact_date'] = '2022-' + data['month'].apply(lambda m: month_num[m]).astype(str).str.zfill(2) + '-' + data['day'].astype(str).str.zfill(2)

    # Generar archivos de salida
    os.makedirs('./files/output')
    output = {
        'client': [
            'client_id', 'age', 'job', 'marital', 'education', 
            'credit_default', 'mortgage'
        ],
        'campaign': [
            'client_id', 'number_contacts', 'contact_duration', 
            'previous_campaign_contacts', 'previous_outcome', 
            'campaign_outcome', 'last_contact_date'
        ],
        'economics': [
            'client_id', 'cons_price_idx', 'euribor_three_months'
        ]
    }
    for subset in output:
        data[output[subset]].to_csv(f'./files/output/{subset}.csv', index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()
