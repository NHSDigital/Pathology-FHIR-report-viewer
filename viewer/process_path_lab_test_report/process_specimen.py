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
        self.requester_specimen_id=specimen.identifier[0].value # just take first identifier
        self.laboratory_accession_id=specimen.accessionIdentifier.value
        self.specimen_type=specimen.type.coding[0].display # just take first coding
        self.collected_date=specimen.collection.collectedDateTime
        self.received_date=specimen.receivedTime
        if specimen.note is not None:
            self.notes=[x.text for x in specimen.note]
        else:
            self.notes=[]
        