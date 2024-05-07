from pydantic import BaseModel, UUID4, Field
from typing import Optional

class StoreData(BaseModel):
    
    provider_id: str

    '''
    Provider id must be in a string format 
    statings a persons name or reference to the data-set ownership and liability etc..

    '''
    validator_id: UUID4

    '''
    This field represents the ID of a validator and is expected to be a UUID (Universally Unique Identifier) of version 4
    that is completely different for each validators and can't be manipulated 
    '''

    wallet_id: Optional[UUID4] = Field(default=None)
    
    '''
    This field represents the ID of a wallet and is an optional UUID of version 4.
    The Optional type hint from Python's typing module means that this field can either be a UUID4 or None.
    The Field function from Pydantic allows for further customization, and here it is used to set the default value of wallet_id to None, making this field optional in a practical sense.

    '''
