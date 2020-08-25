from typing import Optional, Dict

from pydantic import BaseModel


class Payload(BaseModel):
    url: str
    headers: Optional[Dict[str, str]]
    params: Optional[Dict[str, str]]