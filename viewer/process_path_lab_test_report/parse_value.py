
import sys

implemented_value_types=[
    "valueQuantity",
    "valueCodeableConcept", 
    "valueRange", 
    "valueString",
]
unimplemented_value_types=[
    "valueTime", 
    "valueDateTime", 
    "valueInteger", 
    "valuePeriod", 
    "valueRatio", 
    "valueSampledData", 
    "valueBoolean",
]

class ParsedValue():
    __slots__=[
        "value",
        "unit",
        "comparator",
    ]
    
    def __init__(self,value=None, unit=None, comparator=None):
        self.value=value
        self.unit=unit
        self.comparator=comparator
    
    def __str__(self):
        value_repr_string=f"{self.value}"
        if self.unit is not None:
            value_repr_string=f"{value_repr_string} {self.unit}"
        if self.comparator is not None:
            value_repr_string=f"{self.comparator} {value_repr_string}"
        return value_repr_string



def parse_value_entity(value_entity):
    # value_entity can be 
    #      the observation object itelf 
    #      or can be a component of the observation value
    # Both of these objects have the same elements, i.e. value<type>, referenceRange, reasonAbsent, ..

    for value_type in unimplemented_value_types:
        if getattr(value_entity, value_type) is not None:
            print(f"Encountered unimplemented value type: {value_type}")
            sys.exit()

    if value_entity.valueQuantity is not None:
        parsed_value=ParsedValue(
            value=value_entity.valueQuantity.value,
            unit=value_entity.valueQuantity.unit,
            comparator=value_entity.valueQuantity.comparator
            )

    elif value_entity.valueString is not None:
        temp_value=value_entity.valueString.replace('\\n','\n')
        if temp_value.count('\n') >1: # if its a multi line output, add a preceding linebreak 
                                 # so that the code and display act like a header line
            temp_value='\n'+temp_value
        parsed_value=ParsedValue(
            value=temp_value
            )


    
    elif value_entity.valueCodeableConcept is not None:
        parsed_value=ParsedValue(
            value=value_entity.valueCodeableConcept.coding[0].display
            )

    elif value_entity.valueRange is not None:
        parsed_value=ParsedValue(
            value="ValueRange not implemented yet"
            )
    # ValueRange still to do
    # check that not more than one type still to do? or take as read
        # <valueRange>
        #   <low>
        #     <value value="10" />
        #     <unit value="x10*6/L" />
        #     <system value="http://unitsofmeasure.org" />
        #     <code value="10^6/L" />
        #   </low>
        #   <high>
        #     <value value="35" />
        #     <unit value="x10*6/L" />
        #     <system value="http://unitsofmeasure.org" />
        #     <code value="10^6/L" />
        #   </high>
        # </valueRange>
    else:
        parsed_value=ParsedValue(
            value="value type not recognised"
            )

    if value_entity.referenceRange is not None:
        if value_entity.referenceRange[0].high is not None: # NB only taking element 0 from reference range
            reference_high=ParsedValue(
                value=value_entity.referenceRange[0].high.value,
                unit=value_entity.referenceRange[0].high.unit,
                comparator=value_entity.referenceRange[0].high.comparator,
            )
        else:
            reference_high=None
        if value_entity.referenceRange[0].low is not None:
            reference_low=ParsedValue(
                value=value_entity.referenceRange[0].low.value,
                unit=value_entity.referenceRange[0].low.unit,
                comparator=value_entity.referenceRange[0].low.comparator,
            )
        else:
            reference_low=None
        reference_text=value_entity.referenceRange[0].text
    else:
        reference_low=reference_high=None
        reference_text="No reference range information"
    # print(value_entity)
    return parsed_value, reference_low, reference_high, reference_text
