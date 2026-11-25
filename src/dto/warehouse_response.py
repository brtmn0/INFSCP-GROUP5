from pydantic import BaseModel, Field


class WarehouseResponse(BaseModel):
    id: int = Field(description="Warehouse id", examples=[1])
    code: str = Field(description="Unique warehouse code", examples=["WH-001"])
    name: str = Field(description="Warehouse name", examples=["Warehouse Rotterdam"])
    address: str = Field(description="Warehouse address", examples=["Wijnhaven 107"])
    city: str = Field(description="Warehouse city", examples=["Rotterdam"])
    zip_code: str = Field(description="Warehouse zip code", examples=["213CE"])
    province: str = Field(description="Warehouse province", examples=["Zuid-Holland"])
    country: str = Field(description="Warehouse country", examples=["Netherlands"])
    contact_name: str = Field(description="Warehouse contact name", examples=["John Doe"])
    contact_phone: str = Field(description="Warehouse contact phone", examples=["+31 612345678"])
    contact_email: str = Field(description="Warehouse contact email", examples=["john.doe@example.com"])
