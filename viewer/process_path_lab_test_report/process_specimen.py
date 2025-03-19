class SpecimenData():
    __slots__=[
        "requester_specimen_id",
        "laboratory_accession_id",
        "specimen_type",
        "collected_date",
        "received_date",
        "notes",
        ]

    def __init__ (self, specimen=None):
        if specimen.identifier is not None:
            self.requester_specimen_id=specimen.identifier[0].value # just take first identifier
        else:
            self.requester_specimen_id=""

        if specimen.accessionIdentifier is not None:
            self.laboratory_accession_id=specimen.accessionIdentifier.value
        else:
            self.laboratory_accession_id=""

        if (specimen.type is not None) and (specimen.type.coding is not None):
            self.specimen_type=specimen.type.coding[0].display # just take first coding
        else:
            self.specimen_type=""
        
        if specimen.collection is not None:
            self.collected_date=specimen.collection.collectedDateTime
        else:
            self.collected_date=""
            
        self.received_date=specimen.receivedTime
        
        if specimen.note is not None:
            self.notes=[x.text for x in specimen.note]
        else:
            self.notes=[]
        