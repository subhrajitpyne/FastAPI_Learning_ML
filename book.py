from typing import Optional
from pydantic import BaseModel,Field #BaseModel is just like BaseClass
#Field constructor is used to validate the data

class Book(BaseModel):
    id: Optional[int]#We can make it optional as well.
    title: str = Field(min_length=3,max_length=50)
    author: str = Field(min_length=3,max_length=20)
    description: str = Field(min_length=3,max_length=50)
    rating: int = Field(ge=0,le=5)
    
    #Putting example of the schema
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "Here put book name",
                "author": "PUT AUTHOR NAME HERE",
                "description": "Mention some line to describe this book",
                "rating": "Give the rating between 0 to 5",
            }
        }
    }