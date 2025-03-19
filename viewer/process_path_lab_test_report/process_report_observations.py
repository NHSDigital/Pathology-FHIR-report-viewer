
import traceback

from .process_observation import process_observation

def process_report_observations(
    primary_observations=None,
    resources_by_fullUrl=None,
    ):
 
    output_strings=[]

    for observation in primary_observations:
        
        try:
            output_strings=process_observation(
                observation=observation, 
                output_strings=output_strings, 
                resources_by_fullUrl=resources_by_fullUrl,
                )
        except Exception as exception:
            output_strings.append("==============================")
            output_strings.append("Error processing observation, stack trace:")
            output_strings.append("".join(traceback.format_exception(exception)))
            output_strings.append("==============================")
            
    
    return output_strings