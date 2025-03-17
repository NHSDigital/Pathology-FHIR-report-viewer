
from .process_observation import process_observation


def process_report_observations(
    primary_observations=None,
    resources_by_fullUrl=None,
    ):
 
    output_strings=[]

    for observation in primary_observations:
        output_strings=process_observation(
            observation=observation, 
            output_strings=output_strings, 
            resources_by_fullUrl=resources_by_fullUrl,
            )
    
    return output_strings