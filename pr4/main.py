import uuid
from typing import Dict, Optional
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException, Header, Depends, status

app = FastAPI(
    title="TicketBook Web System (Testing Environment)", 
    version="1.0.0",
    description="Учебная система с намеренно заложенными дефектами для лабораторной работы"
)

# =====================================================================
# ИМИТАЦИЯ БАЗЫ ДАННЫХ
# =====================================================================
USERS_DB: Dict[str, str] = {"user@test.com": "Test1234!"}
ACTIVE_SESSIONS: Dict[str, str] = {}  # token -> email

EVENTS_DB: Dict[int, dict] = {
    1: {"name": "Концерт Скриптонита в Астане", "category": "Концерты", "date": "2026-07-15"},
    2: {"name": "Спектакль Ромео и Джульетта", "category": "Театр", "date": "2026-06-20"},
    5: {"name": "Фильм Бэтмен", "category": "Кино", "date": "2026-06-10"}
}

BOOKINGS_DB: Dict[int, dict] = {}
BOOKING_ID_COUNTER = 741

# =====================================================================
# СХЕМЫ ВАЛИДАЦИИ ДАННЫХ (Pydantic)
# =====================================================================
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BookingCreate(BaseModel):
    event_id: int

class PaymentRequest(BaseModel):
    booking_id: int
    card_token: str

# =====================================================================
# ЗАВИСИМОСТЬ ДЛЯ ПРОВЕРКИ АВТОРИЗАЦИИ
# =====================================================================
def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing or invalid token format"
        )
    
    token = authorization.split(" ")[1]
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid session token"
        )
    
    return ACTIVE_SESSIONS[token]

# =====================================================================
# МОДУЛЬ M1: AUTH (Авторизация)
# =====================================================================
@app.post("/api/auth/login", tags=["M1 Auth"])
def login(user_data: UserLogin):
    if user_data.email not in USERS_DB or USERS_DB[user_data.email] != user_data.password:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    
    # Генерация фиксированного токена для простоты тестирования (как в TC-INT-01)
    session_token = "eyJhbGciOiJIUzI1NiU...Студент_Р-23-60гб"
    ACTIVE_SESSIONS[session_token] = user_data.email
    return {"session_token": session_token, "message": "Успешный вход"}

# =====================================================================
# МОДУЛЬ M2: CATALOG (Каталог)
# =====================================================================
@app.get("/api/catalog/events", tags=["M2 Catalog"])
def get_events(category: Optional[str] = None):
    if category:
        return {k: v for k, v in EVENTS_DB.items() if v["category"].lower() == category.lower()}
    return EVENTS_DB

# =====================================================================
# МОДУЛЬ M3: BOOKING (Бронирование)
# =====================================================================
@app.post("/api/booking/create", tags=["M3 Booking"])
def create_booking(booking_data: BookingCreate, user_email: str = Depends(get_current_user)):
    global BOOKING_ID_COUNTER
    
    # ⚠ БАГ BUG-001: Намеренно убрана проверка "if booking_data.event_id not in EVENTS_DB"
    # Система создаст бронь на любой ID, даже если его нет в каталоге (например, 99999)
    
    BOOKING_ID_COUNTER += 1
    new_booking = {
        "booking_id": BOOKING_ID_COUNTER,
        "user": user_email,
        "event_id": booking_data.event_id,
        "status": "pending"
    }
    
    BOOKINGS_DB[BOOKING_ID_COUNTER] = new_booking
    return new_booking

@app.get("/api/booking/{booking_id}", tags=["M3 Booking"])
def get_booking(booking_id: int):
    if booking_id not in BOOKINGS_DB:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return BOOKINGS_DB[booking_id]

# =====================================================================
# МОДУЛЬ M4: PAYMENT (Оплата)
# =====================================================================
@app.post("/api/payment/pay", tags=["M4 Payment"])
def process_payment(payment_data: PaymentRequest):
    b_id = payment_data.booking_id
    
    if b_id not in BOOKINGS_DB:
        raise HTTPException(status_code=404, detail="Бронирование не существует")
    
    booking = BOOKINGS_DB[b_id]
    
    # ⚠ БАГ BUG-002: Намеренно закомментирована проверка на дублирование платежа:
    # if booking["status"] == "paid":
    #     raise HTTPException(status_code=409, detail="Booking already paid")
    # Из-за этого повторная оплата вернет статус success и пройдет успешно.
    
    # Эмуляция ответов платёжной системы через токен карты
    if payment_data.card_token == "tok_test_decline":
        booking["status"] = "failed"  # Обновление статуса в M3
        raise HTTPException(status_code=402, detail="payment_status: declined")
        
    if payment_data.card_token == "tok_test_valid":
        booking["status"] = "paid"  # Обновление статуса в M3
        return {
            "transaction_id": f"tx_{uuid.uuid4().hex[:6]}",
            "booking_id": b_id,
            "payment_status": "success",
            "message": "Оплата прошла успешно"
        }
    
    raise HTTPException(status_code=400, detail="Некорректный токен карты")