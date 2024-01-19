import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta

# ChatGPT Client
client = instructor.patch(OpenAI())

# keyword information
class HotelBooking(BaseModel):
    place: str
    date: date
    room_type: str
    no_of_rooms: int
    no_of_days: int

# OpenAI API
def get_response(string) -> HotelBooking:
    return client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        response_model=HotelBooking,
        messages=[
            {
                "role": "user",
                "content": f"Get Hotel Booking information for {string}",
            },
        ],
    )  

# prompt
    response = get_response("I want to order a twin at taipei at jan. 24 2024 for 3 days")
    print(response.model_dump_json(indent=2))
