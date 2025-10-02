from fastapi import FastAPI, HTTPException
import asyncio  # Добавляем эту строку
import time
import random

app = FastAPI(title="Test API for Load Testing")
users_db = []

@app.get("/")
async def root():
    return {"message": "Welcome to Load Testing API", "status": "active"}

@app.get("/users")
async def get_users():
    # Заменяем time.sleep на asyncio.sleep
    delay = random.uniform(0.01, 0.05)  # Уменьшаем задержки
    await asyncio.sleep(delay)
    
    return {
        "users": users_db,
        "count": len(users_db),
        "delay_seconds": delay
    }

@app.post("/users")
async def create_user(name: str, email: str):
    user = {
        "id": len(users_db) + 1,
        "name": name,
        "email": email,
        "created_at": time.time()
    }
    users_db.append(user)
    return {"message": "User created", "user": user}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Заменяем time.sleep на asyncio.sleep
    processing_time = random.uniform(0.005, 0.02)
    await asyncio.sleep(processing_time)
    
    if user_id < 1 or user_id > len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user": users_db[user_id - 1],
        "processing_time": processing_time
    }

@app.get("/status")
async def status_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/heavy")
async def heavy_operation():
    # Уменьшаем задержку и заменяем на asyncio.sleep
    computation_time = random.uniform(0.05, 0.2)  # Было 0.1-0.5
    await asyncio.sleep(computation_time)
    
    # Оптимизируем тяжелые вычисления
    result = sum(i * i for i in range(5000))  # Было 10000
    
    return {
        "message": "Heavy computation completed",
        "computation_time": computation_time,
        "result": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)