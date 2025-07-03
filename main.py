import ctypes
import mmap
import time

class SPageFilePhysics(ctypes.Structure):
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("gas", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("gear", ctypes.c_int),
        ("rpm", ctypes.c_int),
        ("speedKmh", ctypes.c_float),
        ("position", ctypes.c_float * 3),  # x, y, z
    ]

shm_name = "acpmf_physics"

# Try to map shared memory
try:
    mem = mmap.mmap(-1, ctypes.sizeof(SPageFilePhysics), shm_name, access=mmap.ACCESS_READ)
except FileNotFoundError:
    print("Shared memory block not found. Make sure Assetto Corsa is running and you're on track.")
    exit()

while True:
    mem.seek(0)
    physics = SPageFilePhysics.from_buffer_copy(mem.read(ctypes.sizeof(SPageFilePhysics)))
    speed_kmh = physics.speedKmh * 3.6  # convert if needed
    
    print(f"Speed: {speed_kmh:.2f} km/h | Gear: {physics.gear} | Pos: {list(physics.position)}")

    time.sleep(0.2)
