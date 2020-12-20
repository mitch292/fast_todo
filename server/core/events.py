from typing import Callable
from db.events import connect_to_db, close_db_connection

def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        await connect_to_db()
    
    return start_app

def create_stop_app_handler() -> Callable:
    async def stop_app() -> None: 
        await close_db_connection()
    
    return stop_app