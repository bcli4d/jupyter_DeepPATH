from google.cloud import bigquery
import json

# Perform a query and return the results as a list of tuples
def query_bq(metadata_path, sql_query):
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

