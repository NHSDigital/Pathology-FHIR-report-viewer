from .parse_value import parse_value_entity

def process_observation(observation=None, output_strings=None, resources_by_fullUrl=None):
    
    # if observation.meta.profile[0] == "https://fhir.hl7.org.uk/StructureDefinition/UKCore-Observation-Group-Lab": # it's a "grouper"
    
    display=observation.code.coding[0].display # just use first coding
    code=observation.code.coding[0].code       # ditto
    
    if observation.hasMember is not None: # it's a "grouper"
                                          # assume that a grouper has no value  
        formatted_output=(f"{code:18} | {display:55} ")
        output_strings.append(formatted_output)
        for member_id in observation.hasMember:
            member_observation=resources_by_fullUrl[member_id.reference]
            process_observation(  # recurse
                 observation=member_observation, 
                 output_strings=output_strings, 
                 resources_by_fullUrl=resources_by_fullUrl
                 )
    else: # it's an actual individual observation
        parsed_value, reference_low, reference_high, reference_text=parse_value_entity(observation)
        formatted_output=(f"{code:18} | {display:55} | {str(parsed_value):16}")
        if reference_text!="No reference range information":
            # formatted_output=(f"{code:18} | {display:55} | {str(parsed_value):16}") 
            if (reference_low is not None) and (reference_high is not None):
                formatted_output += f" (reference: {str(reference_low):16} - {str(reference_high):16})" 
            if reference_text is not None:
                
                ############################################################################################
                # experimental way to keep reference range interpretation indented if contains line breaks #
                ############################################################################################
                temp_strings=reference_text.split('\r\n') # probably needs to cope with other forms of linebreak
                padding='\n' + len(formatted_output)*' '
                reference_text=padding.join(temp_strings)

                formatted_output += f" ({reference_text})"
        output_strings.append(formatted_output)
    return output_strings

