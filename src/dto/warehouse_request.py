from pydantic import BaseModel, Field


class WarehouseRequest(BaseModel):
    code: str = Field(description="Unique warehouse code", min_length=1, examples=["WH-001"])
    name: str = Field(description="Warehouse name", min_length=1, examples=["Warehouse Rotterdam"])
    address: str = Field(description="Warehouse address", min_length=1, examples=["Wijnhaven 107"])
    city: str = Field(description="Warehouse city", min_length=1, examples=["Rotterdam"])
    zip_code: str = Field(description="Warehouse zip code", min_length=1, examples=["213CE"])
    province: str = Field(description="Warehouse province", min_length=1, examples=["Zuid-Holland"])
    country: str = Field(description="Warehouse country", min_length=1, examples=["Netherlands"])
    contact_name: str = Field(description="Warehouse contact name", min_length=1, examples=["John Doe"])
    contact_phone: str = Field(description="Warehouse contact phone", min_length=1, examples=["+31 612345678"])
    contact_email: str = Field(description="Warehouse contact email", min_length=1, examples=["john.doe@example.com"])
