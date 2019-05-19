from google.cloud import bigquery
import json

# Perform a query and return the results as a list of tuples
def query_tumor_metadata(metadata_path, sql_query):
    metadata=[]
    client = bigquery.Client()
    query_job = client.query(sql_query)

    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()

    # Now create a json file that the sort and later stages will use
    jdata=[]
    for i,row in df.iterrows():
        data = dict(
            file_name=row.svsFileName,
            file_id=row.file_gdc_id,
            cases=[dict(
                samples=[dict(
                    sample_type=row.sample_type_name)],
                diagnoses=[dict(
                    tumor_stage=row.clinical_stage)],
                project=dict(
                    project_id=row.project_short_name)
            )]
            )
        jdata.append(data)

    with open(metadata_path, 'w') as md:
        json.dump(jdata, md)

# Perform a query and return the results as a list of tuples
def query_mutation_metadata(images_metadata_path, mutations_metadata_path, hugo_symbols_path, sql_query):
    client = bigquery.Client()
    query_job = client.query(sql_query)

    results = query_job.result()  # Waits for job to complete.
    df = results.to_dataframe()

    # Now create a json file that the sort and later stages will use
    jdata = []
    mutations_data=[]
    symbols = []
    for i,row in df.iterrows():
        images_data = dict(
            file_name=row.svsFilename,
            file_id=row.file_gdc_id
            )
        if not images_data in jdata:
            jdata.append(images_data)
        
        line = "{} {}".format(row.sample_barcode[0:12], row.Hugo_Symbol)
        if line not in mutations_data:
            mutations_data.append(line)
        
        symbol = row.Hugo_Symbol
        if symbol not in symbols and not symbol == "WT":
            symbols.append(symbol)
        
    with open(images_metadata_path, 'w') as md:
        json.dump(jdata, md)
    with open(mutations_metadata_path, 'w') as md:
        for line in mutations_data:
            md.write(line+'\n')
    symbols.sort()
    with open(hugo_symbols_path, 'w') as md:
        for line in symbols:
            md.write(line+'\n')


