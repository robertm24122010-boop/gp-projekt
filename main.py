import math
import random

WORLD_MIN, WORLD_MAX = -100, 100
STEP = 10
MAX_STEPS = 60


def clamp(value):
    return max(WORLD_MIN, min(WORLD_MAX, value))


def safe_int(prompt, default):
    try:
        return int(input(prompt))
    except ValueError:
        return default


def angle_to_vector(angle, step):
    rad = math.radians(angle % 360)
    return int(math.cos(rad) * step), int(math.sin(rad) * step)


def log(step, message):
    print(f"[STEP {step:02d}] {message}")


def terrain_event():
    roll = random.randint(1, 100)
    if roll < 10:
        return -25, "Pułapka terenowa"
    if roll < 20:
        return 20, "Strefa regeneracji"
    if roll < 30:
        return -10, "Trudny teren"
    return 0, ""


def random_event():
    roll = random.randint(1, 100)
    if roll < 8:
        return -20, "Burza energetyczna"
    if roll < 15:
        return 25, "Odnaleziono zasoby"
    return 0, ""


def goal_reached(x, y, gx, gy):
    return abs(x - gx) < 10 and abs(y - gy) < 10


def run_simulation(name, x, y, angle, energy, goal_x, goal_y):
    print("\n🚀 MISSION CONTROL START\n")
    print(f"MISSION: {name}")
    print(f"START: ({x}, {y})")
    print(f"GOAL: ({goal_x}, {goal_y})")
    print(f"ENERGY: {energy}")
    print("=" * 50)

    step = 0

    while step < MAX_STEPS and energy > 0:
        step += 1
        ox, oy = x, y
        dx, dy = angle_to_vector(angle, STEP)
        x = clamp(x + dx)
        y = clamp(y + dy)
        energy -= 5

        terrain_change, terrain_msg = terrain_event()
        if terrain_change:
            energy += terrain_change
            log(step, f"TERRAIN → {terrain_msg} ({terrain_change})")

        event_change, event_msg = random_event()
        if event_change:
            energy += event_change
            log(step, f"EVENT → {event_msg} ({event_change})")

        log(step, f"({ox},{oy}) → ({x},{y}) | ENERGY={energy}")

        if goal_reached(x, y, goal_x, goal_y):
            print("\n🎯 CEL OSIĄGNIĘTY")
            return "SUCCESS", x, y, step, energy

        if energy <= 0:
            print("\n☠️ ENERGIA WYCZERPANA")
            return "FAIL", x, y, step, energy

    return "INCOMPLETE", x, y, step, energy


def main():
    print("\n" + "=" * 60 + "\n")
    print("🚀 EXPEDITION SIMULATOR v1.0")
    print("=" * 60 + "\n")

    name = input("Mission name: ") or "EXP-01"
    x = safe_int("Start X: ", 0)
    y = safe_int("Start Y: ", 0)
    angle = safe_int("Angle (0-359): ", 0)
    energy = safe_int("Energy: ", 100)
    goal_x = safe_int("Goal X: ", 80)
    goal_y = safe_int("Goal Y: ", 80)

    result, x, y, steps, energy = run_simulation(name, x, y, angle, energy, goal_x, goal_y)

    print("\n" + "=" * 50)
    print("📡 FINAL REPORT")
    print("=" * 50)
    print("MISSION:", name)
    print("FINAL POSITION:", (x, y))
    print("STEPS:", steps)
    print("ENERGY LEFT:", energy)
    print("RESULT:", result)

    if input("\nRun again? (y/n): ").lower() == "y":
        main()


if __name__ == "__main__":
    main()
