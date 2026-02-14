WIDTH = 1000
HEIGHT = 800

# ===== PARTICLE SIZES =====
GRAVITY_STRENGTH = 120
QUARK_RADIUS = 8
NUCLEON_RADIUS = 12
ELECTRON_RADIUS = 5
ATOM_RADIUS = 20
HYDROGEN_RADIUS = 15

# ===== PARTICLE COUNTS =====
NUM_QUARKS = 10
NUM_ELECTRONS = 10

# ===== MERGE MECHANICS =====
MERGE_DISTANCE = 30
MERGE_SPEED_THRESHOLD = 12

# ===== MERGE TIMERS (in frames at 60fps) =====
# Change these to adjust how long nucleons must stick together before merging
NUCLEON_MERGE_TIMER_2 = 60   # 2-nucleon merge (proton + neutron) = ~2 seconds
NUCLEON_MERGE_TIMER_3 = 100   # 3-nucleon merge (2 protons + 1 neutron) = ~3 seconds

# ===== PHYSICS MULTIPLIERS =====
NUCLEON_ATTRACTION_MULTIPLIER = 1.75
QUARK_ATTRACTION_MULTIPLIER = 1.0
optimal_speed_quarks = 2