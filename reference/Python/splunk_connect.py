import splunklib.client as client
import splunklib.results as results
import sys

try:
    import pandas as pd
except ImportError:
    pass


def splunk_connect(instance, username, password):
    try:
        # Create a Service instance and log in 
        if instance == 'dev':
            HOST = '10.169.193.61'
        elif instance == 'cert':
            HOST = "cdc4c-loganalysis-splunk-searchheaddatastream.route53.lexis.com"
        elif instance == 'prod':
            HOST = "prod-splunk-gui.route53.lexis.com"
        else:
            print(f'Instance {instance} type not recognized.')
            return None

        service = client.connect(
            host=HOST,
            port=8089,
            scheme='https',
            username=username,
            password=password, )
        return service
    except Exception as error:
        print(error)


def splunk_search(service, query, **kwargs):
    job = service.jobs.create(query, **kwargs)
    
    if 'pandas' not in sys.modules.keys():
        result_stream = job.results(output_mode='json')
    
        json_results = json.loads(result_stream.read())
        return json_results, job
    else:
        rr = results.ResultsReader(job.preview())
        row=0
        resultsdf = pd.DataFrame()
        for res in rr:
            if isinstance(res,list):
                result = pd.DataFrame(index=[row], data=res)
            elif isinstance(res, results.Message):
                print(f'Message: {res}')
                return None, None
            else:
                result = pd.DataFrame(index=[row], data=[res])
            resultsdf = resultsdf.append(result, sort=True)
            row+=1
        return resultsdf, job