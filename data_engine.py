from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
import asyncio
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, SessionLocal, ZoneSnapshot
from alerts import check_and_create_alerts
from auth import router as auth_router
from analytics import router as analytics_router
from alerts import router as alerts_router
import os

app = FastAPI(title="Event Crowd Management Engine")

# Include routers
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(alerts_router)

# Allow CORS for the dashboard (only needed for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Simulated Database
zones = {
    "Gate A": {"density": 20, "wait_time": 2, "status": "Smooth", "capacity": 500},
    "Gate B": {"density": 85, "wait_time": 15, "status": "Bottleneck", "capacity": 500},
    "Food Court": {"density": 50, "wait_time": 8, "status": "Crowded", "capacity": 1000},
    "Main Stage": {"density": 95, "wait_time": 0, "status": "Full", "capacity": 5000},
    "Restrooms North": {"density": 10, "wait_time": 1, "status": "Smooth", "capacity": 50},
    "Restrooms South": {"density": 70, "wait_time": 10, "status": "Crowded", "capacity": 50},
}

# Background task to continuously simulate live crowd movement
async def simulate_crowds():
    while True:
        await asyncio.sleep(5)  # Update every 5 seconds
        db = SessionLocal()
        try:
            for zone, data in zones.items():
                # Randomly change density by -5% to +5%
                change = random.randint(-5, 5)
                data["density"] = max(0, min(100, data["density"] + change))
                
                # Recalculate wait time based on density
                if data["density"] < 30:
                    data["status"] = "Smooth"
                    data["wait_time"] = random.randint(0, 3)
                elif data["density"] < 80:
                    data["status"] = "Crowded"
                    data["wait_time"] = random.randint(4, 12)
                else:
                    data["status"] = "Bottleneck" if "Gate" in zone or "Restroom" in zone else "Full"
                    data["wait_time"] = random.randint(13, 30) if "Restroom" in zone or "Gate" in zone else 0
                
                # Save to database for historical tracking
                snapshot = ZoneSnapshot(
                    zone_name=zone,
                    density=data["density"],
                    wait_time=data["wait_time"],
                    status=data["status"],
                    capacity=data["capacity"]
                )
                db.add(snapshot)
                
                # Check for alerts
                check_and_create_alerts(db, zone, data["density"], data["wait_time"], data["status"])
            
            db.commit()
        except Exception as e:
            print(f"Error in crowd simulation: {e}")
            db.rollback()
        finally:
            db.close()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_crowds())

@app.get("/api/zones")
def get_zones():
    return {
        "timestamp": datetime.now().isoformat(),
        "zones": zones
    }

@app.get("/api/recommendations")
def get_recommendations():
    """AI Assistant can hit this endpoint to perfectly recommend the best routing."""
    # Find the gate with the lowest wait time
    gates = {k: v for k, v in zones.items() if "Gate" in k}
    best_gate = min(gates.items(), key=lambda x: x[1]["wait_time"])
    
    # Find restrooms with the lowest wait time
    restrooms = {k: v for k, v in zones.items() if "Restroom" in k}
    best_restroom = min(restrooms.items(), key=lambda x: x[1]["wait_time"])
    
    return {
        "best_gate": {"name": best_gate[0], "wait_time": best_gate[1]["wait_time"]},
        "best_restroom": {"name": best_restroom[0], "wait_time": best_restroom[1]["wait_time"]}
    }

# Serve static files from React build (MUST be last to not override API routes)
frontend_dist = os.path.join(os.path.dirname(__file__), "dashboard", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve React SPA for all non-API routes"""
        # Serve index.html for all routes (API routes are handled by routers above)
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return {"error": "Frontend not built. Run: cd dashboard && npm run build"}

# To run: uvicorn data_engine:app --reload
