
import sys

from .utils import format_None_to_null_string

implemented_value_types=[
    "valueQuantity",
    "valueCodeableConcept", 
    "valueRange", 
    "valueString",
    "valueRatio",
]
unimplemented_value_types=[
    "valueTime", 
    "valueDateTime", 
    "valueInteger", 
    "valuePeriod", 
    "valueSampledData", 
    "valueBoolean",
]

class ParsedValue():
    __slots__=[
        "value",
        "unit",
        "comparator",
        "value_low",
        "value_high",
        "numerator",
        "numerator_unit",
        "denominator",
        "denominator_unit",
    ]
    
    def __init__(
        self, 
        value=None, 
        unit=None, 
        comparator=None, 
        value_low=None, 
        value_high=None,
        numerator=None,
        numerator_unit=None,
        denominator=None,
        denominator_unit=None
        ):
        self.value=value
        self.unit=unit
        self.comparator=comparator
        self.value_low=value_low
        self.value_high=value_high
        self.numerator=numerator
        self.numerator_unit=numerator_unit
        self.denominator_unit=denominator_unit
        self.denominator=denominator
    
    def __str__(self):
        value_repr_string=""
        if self.value is not None:
            value_repr_string=f"{self.value}"
        if self.value_low is not None:
            value_repr_string=f"{self.value_low}-{self.value_high}"
        if self.unit is not None:
            value_repr_string=f"{value_repr_string} {self.unit}"
        if self.comparator is not None:
            value_repr_string=f"{self.comparator} {value_repr_string}"
        if self.numerator is not None:
            value_repr_string=f"{format_None_to_null_string(self.numerator)}{format_None_to_null_string(self.numerator_unit)}/{format_None_to_null_string(self.denominator)}{format_None_to_null_string(self.denominator_unit)}"
        return value_repr_string



def parse_value_entity(value_entity):
    # value_entity is an Observation resource

    for value_type in unimplemented_value_types:
        if getattr(value_entity, value_type) is not None:
            print(f"Encountered unimplemented value type: {value_type}")
            reference_text="No reference range information"
            return f"unsupported type:{value_type}", None, None, reference_text

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
            value_low=  value_entity.valueRange.low.value,
            value_high= value_entity.valueRange.high.value,
            unit= value_entity.valueRange.low.unit # assume units of high and low are same 
                                                   # only uses "unit" and not "code"  
            )
    elif value_entity.valueRatio is not None:
        parsed_value=ParsedValue(
            numerator=        value_entity.valueRatio.numerator.value,
            numerator_unit=   value_entity.valueRatio.numerator.unit, 
            denominator=      value_entity.valueRatio.denominator.value,
            denominator_unit= value_entity.valueRatio.denominator.unit,
            )
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

    return parsed_value, reference_low, reference_high, reference_text
