# Maritime Performance Analysis: Variable Definitions and Domain Knowledge

This analysis focuses on modeling vessel performance using **weather-corrected (still water) data**. By removing environmental noise (wind, waves, current), the relationships between parameters strictly follow the physical laws of naval architecture.

## 1. Parameter Definitions and Variable Naming

### 1.1 Draft
* **Variable Name:** `Draft_Avg`
* **Domain Knowledge:**
    * **Definition:** The vertical distance from the keel to the waterline.
    * **Physical Impact:** Dictates the ship's displacement and **Wetted Surface Area**.
    * **Resistance Role:** Wetted surface area is the primary source of frictional resistance the ship must overcome.

### 1.2 Speed
* **Variable Name:** `Speed_STW`
* **Domain Knowledge:**
    * **Definition:** The velocity of the vessel relative to the surrounding water.
    * **Context:** In weather-corrected data, this represents performance in "ideal" calm conditions without current interference.

### 1.3 Delivered Power
* **Variable Name:** `Power_Delivered`
* **Domain Knowledge:**
    * **Definition:** The actual power reaching the propeller after transmission losses.
    * **Scope:** Ignores engine-room mechanical losses to focus purely on **hydrodynamic efficiency**.
    * **Function:** Represents the energy required to overcome total hull resistance.

### 1.4 RPM
* **Variable Name:** `Propeller_RPM`
* **Domain Knowledge:**
    * **Definition:** Revolutions Per Minute of the propeller.
    * **Role:** The kinetic input that generates thrust to balance resistance at a given speed.

---

## 2. Parameter Correlations (The Ideal Rules)
Since the data is weather-corrected, these parameters follow the standard **Propeller Law** and **Admiralty Coefficient** logic.

### 2.1 Power vs. Speed (The Cubic Law)
* **Rule:** In calm water, the power required is proportional to the **cube of the speed** ($P \propto V^3$).
* **Physics:** Water resistance increases significantly as the ship moves faster.
* **Correlation:** If speed doubles ($2x$), the power requirement increases eightfold ($2^3 = 8x$).

### 2.2 Power vs. RPM
* **Rule:** Power is proportional to **RPM cubed** ($P \propto RPM^3$).
* **Physics:** In weather-neutral conditions, the propeller follows a fixed curve where torque increases with the square of the RPM, leading to a cubic power relationship.

### 2.3 Speed vs. RPM (The Linear Link)
* **Rule:** Speed and RPM show a nearly **linear correlation**.
* **Assumption:** Valid in still water where propeller **"slip"** (the difference between theoretical and actual distance moved) remains constant.

### 2.4 The Impact of Draft
Draft acts as the **resistance baseline** for all other correlations.
* **Laden Draft (Deep):**
    * Higher resistance.
    * Requires **more Power** and **higher RPM** to achieve the same Speed compared to ballast conditions.
* **Ballast Draft (Shallow):**
    * Lower resistance.
    * Allows for **higher Speed** achieved at **lower Power** and **lower RPM**.


# Logical Validation and Anomaly Detection Rules

This module defines the logical constraints used to validate vessel performance data. These rules are based on physical laws and expected operational behaviors. Deviations from these rules indicate either data quality issues or unrecorded operational events.

## 1. Maintenance Logic (Hull & Propeller)
These rules verify the effectiveness of hull cleaning or propeller polishing and detect unrecorded maintenance events.

### 1.1 Post-Maintenance Performance
* **Rule:** After a recorded maintenance event (hull cleaning/propeller polishing), the **Power Deviation** must be lower than it was immediately before the event.
* **Reasoning:** Maintenance removes fouling (resistance). If resistance drops, the extra power required to maintain speed must also drop.

### 1.2 Natural Fouling Trend
* **Rule:** In the absence of maintenance, Power Deviation should show a consistent **upward trend** over time.
* **Reasoning:** Marine growth accumulates naturally, gradually increasing resistance.
* **Anomaly Trigger:** A sudden, unexplained drop in Power Deviation without a corresponding maintenance log indicates a data error or a missing log entry.

### 1.3 Suspected Maintenance Detection
* **Rule:** Any significant sudden drop in Power Deviation *without* a recorded maintenance event is flagged as **"Suspected Maintenance"**.

---

## 2. Physics Constraints (Hydrodynamics)
These rules enforce the immutable physical relationships between ship parameters.

### 2.1 Draft-Power Relationship
* **Rule:** At a constant speed, if **Draft increases**, **Power must increase** proportionally.
* **Reasoning:** Deeper draft means more displacement and wetted surface area, leading to higher resistance.
* **Anomaly Trigger:** An increase in draft accompanied by a decrease in power (at constant speed) is physically impossible and flags a sensor error.

### 2.2 Speed-RPM Relationship
* **Rule:** At a constant draft, **RPM** must correlate positively with **Speed**.
* **Reasoning:** To move faster, the propeller must spin faster (assuming constant pitch).
* **Anomaly Trigger:** Speed increasing while RPM decreases (or vice versa) indicates a log/sensor mismatch.

---

## 3. Data Integrity & Pattern Stability
These rules detect outliers and sensor malfunctions.

### 3.1 Speed Anomalies
* **Rule:** A sharp spike or drop in Speed *without* a corresponding change in Power or Draft is invalid.
* **Reasoning:** A ship cannot suddenly accelerate without extra power, nor decelerate significantly without dropping power or hitting resistance.

### 3.2 Consistency Check
* **Rule:** The inter-variable relationships (Draft vs. Speed vs. Power) must remain consistent over time.
* **Anomaly Trigger:** Any sudden, unexplained shift in the correlation pattern between these variables is flagged for review.





# Marine Fundamentals: Basic Terms, Concepts, and Abbreviations

## 1. Abbreviations & Acronyms
### 1.1 Vessel Metrics
* [cite_start]**DWT (Deadweight Tonnage):** The total weight a ship can safely carry (Cargo + Fuel + Water + Crew)[cite: 91, 92].
* [cite_start]**GRT (Gross Register Tonnage):** A measure of the total internal volume of the ship's enclosed spaces[cite: 102, 103].
* [cite_start]**NRT (Net Register Tonnage):** The volume of cargo spaces available for revenue-earning cargo[cite: 107, 109].
* [cite_start]**LOA (Length Overall):** Maximum length from the foremost to the aft-most point[cite: 123, 124].
* [cite_start]**LBP (Length Between Perpendiculars):** Distance between forward and aft perpendiculars, used for stability calculations[cite: 126, 127].

### 1.2 Performance & Engineering
* [cite_start]**MCR (Maximum Continuous Rating):** The maximum power the main engine can deliver continuously[cite: 393, 394].
* [cite_start]**NCR (Normal Continuous Rating):** typically 85-90% of MCR; the safe continuous operating power [cite: 397-399].
* [cite_start]**SFOC (Specific Fuel Oil Consumption):** Fuel consumed per unit of energy (g/kWh)[cite: 839].
* [cite_start]**LCV (Lower Calorific Value):** Energy content per mass of fuel (kJ/kg)[cite: 761].
* [cite_start]**STW (Speed Through Water):** Speed of the ship relative to the water[cite: 509].
* [cite_start]**SOG (Speed Over Ground):** Speed of the ship relative to the seabed (GPS speed)[cite: 522].

### 1.3 Regulatory & Commercial
* [cite_start]**IMO:** International Maritime Organization[cite: 47, 50].
* [cite_start]**SOLAS:** Safety of Life at Sea convention[cite: 50, 71].
* [cite_start]**MARPOL:** Marine Pollution convention[cite: 50, 71].
* [cite_start]**STCW:** Standards of Training, Certification, and Watchkeeping[cite: 50, 71].
* [cite_start]**PSC (Port State Control):** Inspection of foreign ships by national authorities[cite: 66, 78].
* [cite_start]**CII (Carbon Intensity Indicator):** Efficiency rating (A-E) based on CO2 per tonne-mile [cite: 980-983].
* [cite_start]**EU ETS:** European Union Emission Trading System[cite: 991].
* [cite_start]**EEOI:** Energy Efficiency Operational Indicator[cite: 1020].

---

## 2. Basic Concepts: Vessel Geometry


### 2.1 Dimensions
* [cite_start]**Breadth (Beam):** The widest point of the ship's hull[cite: 128, 129].
* [cite_start]**Depth:** Vertical distance from the keel to the main deck[cite: 131, 132].
* [cite_start]**Draft:** Vertical distance from the waterline to the bottom of the keel[cite: 135, 136].
* [cite_start]**Freeboard:** Distance from the waterline to the main deck[cite: 138, 139].
* [cite_start]**Air Draft:** Distance from the waterline to the highest point of the vessel[cite: 151, 152].

### 2.2 Floatation Mechanics
* [cite_start]**Archimedes' Principle:** An object experiences an upward buoyant force equal to the weight of the fluid it displaces[cite: 184, 185].
* [cite_start]**Displacement:** The actual weight of the ship, equal to the weight of the water displaced[cite: 216, 217].
* [cite_start]**Lightship Weight:** Weight of the empty ship structure and machinery[cite: 220].

---

## 3. Basic Concepts: Operational Terms

### 3.1 Movement & Maneuvering
* [cite_start]**Ballast:** Water added to maintain stability, control draft, and adjust trim[cite: 205, 207, 208].
* [cite_start]**Mooring:** Securing a ship to a fixed structure (berth/jetty) using ropes/wires[cite: 232].
* [cite_start]**Bunkering:** The process of loading fuel, fresh water, or lubricating oil[cite: 453, 455].
* [cite_start]**Pilotage:** Mandatory service where a local marine pilot guides the vessel through port waters[cite: 282, 283].
* [cite_start]**Towage:** Use of tugboats to assist maneuvering in tight spaces[cite: 286, 287].

### 3.2 Voyage Segments
* [cite_start]**Sea Passage:** Time when the ship is moving at sea from one port to another (BOSP to EOSP) [cite: 417-421].
* [cite_start]**Port Stay:** The period spent inside a port, including waiting, berthing, and cargo ops[cite: 426].
* [cite_start]**Laden Voyage:** Voyage leg with cargo onboard (Revenue earning)[cite: 320, 323].
* [cite_start]**Ballast Voyage:** Voyage leg with no cargo (Cost only)[cite: 327, 331].

---

## 4. Basic Concepts: Machinery & Equipment


### 4.1 Propulsion
* [cite_start]**Main Engine:** Provides propulsion power; usually a 2-stroke slow-speed engine[cite: 589, 593].
* [cite_start]**Propeller (FPP):** Fixed Pitch Propeller; blades are fixed, speed controlled by RPM[cite: 579].
* [cite_start]**Propeller (CPP):** Controllable Pitch Propeller; blade angle changes, RPM stays constant[cite: 584].
* [cite_start]**Thrusters:** Auxiliary propulsion (Bow/Stern) for lateral movement during docking[cite: 307].

### 4.2 Power & Support
* [cite_start]**Auxiliary Engine (Diesel Generator):** 4-stroke engine providing electrical power to the ship[cite: 600, 606].
* [cite_start]**Boiler:** Produces steam for heating fuel and accommodation[cite: 615, 616].
* [cite_start]**Economizer (Exhaust Gas Boiler):** Uses waste heat from the main engine to produce steam while sailing[cite: 621, 622].
* [cite_start]**Compressor:** Produces compressed air for starting the main engine[cite: 626, 627].

---

## 5. Basic Concepts: Commercial Parties

### 5.1 Roles
* [cite_start]**Shipowner:** The legal owner; provides the vessel and maintains insurance[cite: 158, 159].
* [cite_start]**Charterer:** The party hiring the ship to transport cargo[cite: 168, 169].
* [cite_start]**Ship Manager:** Company appointed to handle technical or commercial management[cite: 163, 164].

### 5.2 Status Codes
* [cite_start]**On-Hire:** Vessel is delivered to charterer; hire payments begin[cite: 248, 250].
* [cite_start]**Off-Hire:** Vessel is unavailable (breakdown/repair); hire payments stop[cite: 253, 259].
* [cite_start]**Cut and Run:** Vessel leaves port after berthing but *before* starting cargo operations[cite: 463].



# Vessel States and Operational Logic Knowledge Base

## 1. Voyage and Leg Hierarchy

### 1.1 Voyage Structure
A voyage is not a continuous unstructured movement but is divided into distinct commercial and operational segments called **legs**. [cite_start]A leg is defined as a segment of a voyage between two specific points (e.g., Port A to Port B)[cite: 338, 339].

### 1.2 Laden Voyage (Revenue Leg)
* [cite_start]**Definition:** The voyage leg where the vessel is carrying cargo[cite: 318, 320].
* [cite_start]**Commercial Status:** This is the revenue-generating phase for the shipowner (earns freight)[cite: 323].
* **Operational Characteristics:**
    * [cite_start]**Draft:** Heavier draft (ship sits lower in the water) due to cargo weight[cite: 321].
    * [cite_start]**Fuel Consumption:** Higher fuel consumption compared to ballast voyages due to increased displacement requiring more power[cite: 322].
* [cite_start]**Example:** A tanker sailing from the Middle East to India fully loaded with crude oil[cite: 324].

### 1.3 Ballast Voyage (Cost Leg)
* [cite_start]**Definition:** The voyage leg where the vessel is **not** carrying cargo and is typically returning to a port to load[cite: 325, 327].
* [cite_start]**Commercial Status:** No freight revenue is earned; this is a "cost-only" leg used to reposition the vessel[cite: 331, 337].
* **Operational Characteristics:**
    * [cite_start]**Draft:** Lighter draft (ship sits higher in the water)[cite: 329].
    * [cite_start]**Fuel Consumption:** Lower fuel consumption compared to laden voyages due to lower displacement[cite: 330].
* [cite_start]**Role of Ballast Water:** Even without cargo, the ship carries ballast water to maintain stability, submerge the propeller/rudder, and adjust trim [cite: 205-208].

---

## 2. Port Call and Activity Cycles

### 2.1 Port Call Definition
A **Port Call** is the entire period a ship spends associated with a specific port.
* [cite_start]**Start Time:** The departure timestamp of the *previous* port (when the last line was cast off)[cite: 414].
* [cite_start]**End Time:** The departure timestamp of the *current* port[cite: 415].
* [cite_start]**Scope:** This full stretch between two ports is considered one leg of the voyage[cite: 416].

### 2.2 Port Stay Phases
[cite_start]The time strictly *inside* the port (Port Stay) is divided into three precise operational stages[cite: 427]:

#### Phase 1: Inbound Port Stay
* [cite_start]**Start:** When the ship reaches **EOSP** (End of Sea Passage) outside the port[cite: 429].
* [cite_start]**End:** When the **First Line is Ashore** (ship officially ties up to the berth)[cite: 430].
* [cite_start]**Analogy:** "You're entering a parking area"[cite: 485].

#### Phase 2: Berth Time (Working Phase)
* [cite_start]**Start:** First Line Ashore (Arrival)[cite: 432].
* [cite_start]**End:** Last Line Onboard (Departure)[cite: 433].
* [cite_start]**Activities:** Cargo operations (loading/unloading), bunkering, fresh water loading, maintenance[cite: 434].
* [cite_start]**Analogy:** "Your car is parked and you're loading/unloading things"[cite: 485].

#### Phase 3: Outbound Port Stay
* [cite_start]**Start:** Last Line Onboard (when ship physically leaves the berth)[cite: 437].
* [cite_start]**End:** **BOSP** (Beginning of Sea Passage) when the ship exits port limits[cite: 438].
* [cite_start]**Analogy:** "You're leaving the parking area and heading back to the main road"[cite: 485].

---

## 3. Sea Passage Dynamics

### 3.1 Definition
[cite_start]**Sea Passage** is the period when the ship is navigating open waters between ports[cite: 418]. [cite_start]It is often referred to as being **"Underway"**[cite: 422].

### 3.2 Operational Boundaries
* **Start Point (BOSP):** Beginning Of Sea Passage. [cite_start]The moment the ship is fully clear of port limits and commences open-sea navigation[cite: 419, 420].
* **End Point (EOSP):** End Of Sea Passage. [cite_start]The moment the ship arrives near the next port[cite: 421].

### 3.3 Exclusions
[cite_start]Stoppages at sea due to weather, technical breakdowns, or charterer instructions to wait are typically **excluded** from standard Sea Passage performance calculations[cite: 423].

### 3.4 Operational Analogy
* [cite_start]**Sea Passage:** "You're driving on the highway"[cite: 485].

---

## 4. Stationary and Maneuvering States

### 4.1 Anchoring vs. Drifting
* **Anchoring:**
    * [cite_start]**Definition:** The ship drops anchor and remains in a fixed geographical area[cite: 446].
    * [cite_start]**Context:** Can occur during port stays (waiting for berth) or sea passage (breakdown/waiting)[cite: 449, 450].
    * [cite_start]**Analogy:** "Waiting in a safe spot with brakes on"[cite: 485].
* **Drifting:**
    * [cite_start]**Definition:** The ship moves slowly with currents/wind without dropping anchor[cite: 447].
    * [cite_start]**Context:** Used when anchorage is full, water is too deep, or to save fuel while waiting[cite: 442].
    * [cite_start]**Analogy:** "Waiting but slowly rolling forward"[cite: 485].

### 4.2 Mooring
* [cite_start]**Definition:** The process of securing a ship to a fixed structure (jetty, berth, buoy) using ropes or wires[cite: 232].
* **Purpose:**
    * [cite_start]Prevents movement caused by wind, waves, tides, and currents[cite: 233].
    * [cite_start]Ensures safe alignment for cargo hoses, cranes, and gangways[cite: 234, 240, 243].

### 4.3 Tug Boat Operations
* [cite_start]**Definition:** Small, powerful vessels designed to push or pull larger ships[cite: 289].
* **Key Functions:**
    * [cite_start]**Berthing Assistance:** providing precise control in tight spaces where large ships cannot use main propulsion[cite: 292, 295].
    * [cite_start]**Escort:** Assisting tankers/LNG carriers in high-risk areas[cite: 300].
    * [cite_start]**Dead Ship Towing:** Moving vessels that have lost propulsion[cite: 298].

---

## 5. Commercial States and Transitions

### 5.1 On-Hire
* [cite_start]**Definition:** The specific moment the vessel is delivered to the charterer[cite: 249].
* [cite_start]**Financial Impact:** The charterer begins paying the daily "hire" rate from this timestamp[cite: 250].
* [cite_start]**Requirements:** Vessel must be in agreed condition; an **On-hire survey** records condition and fuel quantity[cite: 251, 252].

### 5.2 Off-Hire
* [cite_start]**Definition:** Periods when the vessel is unavailable for the charterer's use[cite: 254].
* **Triggers:**
    * [cite_start]Mechanical breakdown[cite: 255].
    * [cite_start]Dry-docking or repairs[cite: 257].
    * [cite_start]Crew strikes[cite: 258].
* [cite_start]**Financial Impact:** The charterer **does not pay** hire during these periods[cite: 259].

### 5.3 Cut and Run
* [cite_start]**Definition:** A specific scenario where a ship arrives at the berth, completes formalities, but departs **without starting** the planned cargo operation[cite: 463, 480].
* [cite_start]**"Cut":** Stop the operation before it begins[cite: 480].
* [cite_start]**"Run":** Leave the port immediately[cite: 482].
* **Causes:**
    * [cite_start]Severe port congestion or terminal equipment failure[cite: 468, 473].
    * [cite_start]Cargo not ready (shore delays)[cite: 469].
    * [cite_start]Weather restrictions (high swell/wind)[cite: 472].
    * [cite_start]Commercial cancellation by the charterer[cite: 471].
* [cite_start]**Analogy:** "Parking your car at the mall but driving away immediately because the work you came for cannot start"[cite: 485].

---

## 6. Geographical Boundaries

### 6.1 Port Limits
* [cite_start]**Definition:** The official geographical boundary of a port, including piers, jetties, and approaches under the jurisdiction of the Port Authority[cite: 263, 277].
* [cite_start]**Commercial Importance:** Vessels must usually be "within port limits" to tender the **Notice of Readiness (NOR)** unless the contract states otherwise[cite: 279].

### 6.2 Outer Port Limit (OPL)
* [cite_start]**Definition:** A designated area *outside* the official port limits[cite: 265].
* [cite_start]**Usage:** Used for anchoring, waiting for clearance, pilot boarding, or receiving supplies without officially entering the port[cite: 278].
* [cite_start]**Constraint:** Anchoring at OPL may not be valid for tendering NOR if the charter party requires the ship to be "within port limits"[cite: 280].


# Vessel Particulars, Dimensions, and Floatation Physics

## 1. Major Vessel Dimensions
These parameters define the physical envelope of the ship and are critical for determining port compatibility and navigation constraints.

### 1.1 Length Measurements
* **Length Overall (LOA):**
    * [cite_start]**Definition:** The maximum length of the ship from the foremost point of the bow to the aft-most point of the stern [cite: 123-124].
    * [cite_start]**Operational Use:** Determines berth allocation (parking space size) and canal passage fees[cite: 125].
* **Length Between Perpendiculars (LBP):**
    * [cite_start]**Definition:** The distance between the forward and aft perpendiculars, typically measured at the waterline [cite: 126-127].
    * [cite_start]**Operational Use:** Used specifically for stability calculations and hull design math, rather than docking[cite: 127].

### 1.2 Vertical Dimensions
* **Depth:**
    * [cite_start]**Definition:** The vertical distance from the keel (bottom of the ship) to the main deck [cite: 131-132].
    * [cite_start]**Significance:** Indicates the overall hull strength and internal cargo space[cite: 134].
* **Draft (or Draught):**
    * [cite_start]**Definition:** The vertical distance from the waterline to the bottom of the keel [cite: 135-136].
    * **Operational Criticality:** Determines the minimum water depth required for the ship to float. [cite_start]Crucial for entering shallow ports[cite: 137].
    * **Variable Nature:** Draft changes based on cargo load (heavier load = deeper draft) and water density.
* **Freeboard:**
    * [cite_start]**Definition:** The distance from the waterline to the main deck (the "reserve buoyancy") [cite: 138-139].
    * [cite_start]**Safety:** Directly related to Load Line regulations; a higher freeboard generally means better safety against sinking[cite: 140].
* **Air Draft:**
    * [cite_start]**Definition:** The vertical distance from the waterline to the *highest* point of the vessel (e.g., top of the mast or funnel) [cite: 151-152].
    * [cite_start]**Operational Constraint:** Determines if a ship can pass under bridges or overhead cables[cite: 150].

### 1.3 Breadth
* **Beam (Breadth):**
    * [cite_start]**Definition:** The width of the ship at its widest point [cite: 128-129].
    * [cite_start]**Impact:** A wider beam increases stability and cargo capacity but may limit access to narrow locks (e.g., Panama Canal restrictions)[cite: 130].

---

## 2. Tonnage and Capacity Definitions
*Note for RAG Context:* It is a common error to confuse "Tonnage" (Volume) with "Weight". This section clarifies the distinction.

### 2.1 Weight Metrics (Mass)
* **Deadweight (DWT):**
    * **Definition:** The total weight the ship can safely carry. [cite_start]This is the **Payload Capacity** [cite: 91-92].
    * [cite_start]**Components:** Cargo + Fuel + Fresh Water + Ballast Water + Crew + Provisions [cite: 93-99].
    * [cite_start]**Unit:** Metric Tonnes[cite: 100].
* **Displacement:**
    * **Definition:** The actual total weight of the ship and its contents at any given moment. [cite_start]It equals the weight of the water displaced by the hull [cite: 216-217].
    * [cite_start]**Formula:** $Displacement = Lightship~Weight + Deadweight$[cite: 221].

### 2.2 Volume Metrics (Space)
* **Gross Register Tonnage (GRT):**
    * [cite_start]**Definition:** A measure of the **total internal volume** of all enclosed spaces on the ship [cite: 102-103].
    * [cite_start]**Unit:** "Register Tons" (where 1 Register Ton $\approx$ 100 cubic feet)[cite: 104].
    * [cite_start]**Usage:** Used for calculating regulatory fees, port dues, and registration[cite: 105]. [cite_start]It does **not** indicate weight[cite: 106].
* **Net Register Tonnage (NRT):**
    * [cite_start]**Definition:** The volume of *only* the spaces available for carrying revenue-earning cargo[cite: 109].
    * [cite_start]**Deductions:** GRT minus engine rooms, crew spaces, and navigation bridges[cite: 114].
    * [cite_start]**Usage:** Represents the ship's commercial earning capacity[cite: 110].

---

## 3. The Science of Ship Floatation
This logic helps the AI explain *how* a 100,000-tonne steel structure stays afloat.

### 3.1 Archimedes' Principle
* [cite_start]**Rule:** Any object submerged in a fluid experiences an upward buoyant force equal to the weight of the fluid displaced by that object [cite: 184-185].
* [cite_start]**Application:** A ship floats only when the weight of the water it pushes aside (displaces) is equal to or greater than the ship's own weight [cite: 188-189].

### 3.2 The Force Balance
* [cite_start]**Gravity (Weight):** Pushes the ship *down*[cite: 194].
* [cite_start]**Buoyancy (Upthrust):** Pushes the ship *up* (reaction force from displaced water)[cite: 195].
* **Equilibrium:** When Weight = Buoyant Force, the ship floats. [cite_start]If Weight > Buoyant Force, it sinks[cite: 196].

### 3.3 Density and Shape
* **Why Steel Floats:** A solid block of steel sinks because it is denser than water. A ship is a "hollow" steel box.
* **Composition:** ~90% of the volume is air, and only ~10% is steel. [cite_start]This makes the *average density* of the ship less than water [cite: 198-201].

---

## 4. Operational Weight States

### 4.1 Lightship Weight
* [cite_start]**Definition:** The fixed weight of the empty ship itself, including the steel hull, machinery, and permanent equipment[cite: 220].
* **Analogy:** The weight of a car when it rolls off the factory line with an empty tank and no passengers.

### 4.2 Loaded Condition (Full Displacement)
* [cite_start]**Definition:** Lightship + Full Deadweight (Max Cargo, Fuel, etc.)[cite: 225].
* **Operational Result:** Maximum draft (deepest point in water).

### 4.3 Ballast Condition
* [cite_start]**Definition:** Lightship + Ballast Water + Minimal Consumables (No Cargo)[cite: 223].
* **Operational Result:** Minimum safe draft.

---

## 5. Ballast Operations

### 5.1 Purpose of Ballast
Ships carry ballast water (non-revenue weight) to compensate for the lack of cargo weight.
1.  [cite_start]**Stability:** Prevents the ship from becoming "top-heavy" and rolling excessively or capsizing[cite: 206].
2.  [cite_start]**Propeller Immersion:** Ensures the propeller and rudder are fully submerged to maintain steering control and propulsion efficiency[cite: 207].
3.  [cite_start]**Trim Control:** Adjusts the balance between the bow (front) and stern (back) for optimal navigation[cite: 208].

### 5.2 Risks of "No Ballast" (Lightship Condition)
If a ship sails without cargo and without ballast:
* It sits too high in the water.
* The propeller comes out of the water (racing/damage).
* Steering becomes difficult or impossible.
* [cite_start]The structure suffers stress from uneven weight distribution [cite: 211-214].



# Vessel Performance, Speed Dynamics, and Environmental Interaction

## 1. Ocean Dynamics (External Forces)
This section defines the environmental variables that act as "resistance" or "assistance" to the ship's movement. In performance analysis, these are the external factors that must be normalized to understand true vessel health.

### 1.1 Waves vs. Swell
It is critical to distinguish between locally generated waves and distant swells, as they impact hull resistance differently.

* **Wind Sea (Waves):**
    * [cite_start]**Origin:** Created by **local winds** blowing over the water surface[cite: 488].
    * [cite_start]**Characteristics:** Irregular, choppy, with varied heights and directions[cite: 489].
    * [cite_start]**Behavior:** They move with the local wind and change direction immediately as the wind changes[cite: 491].
    * [cite_start]**Energy Factor:** Energy is directly influenced by local wind strength, duration, and "fetch" (distance the wind has blown)[cite: 490].

* **Swell:**
    * [cite_start]**Origin:** Generated by powerful, distant storms (e.g., hurricanes) far away from the ship's current location[cite: 493].
    * [cite_start]**Characteristics:** Smooth, organized, long-wavelength undulations with uniform crests[cite: 494].
    * **Behavior:** Can travel thousands of miles, retaining energy from the distant storm. [cite_start]They often arrive **without any local wind** and can come from a completely different direction than the local wind[cite: 496].

### 1.2 Ocean Currents
* [cite_start]**Definition:** Continuous, directed flows of seawater, functioning like "rivers within the ocean"[cite: 498].
* **Primary Drivers:**
    * [cite_start]**Wind:** Drives surface currents and large rotating patterns called *gyres*[cite: 501].
    * [cite_start]**Coriolis Effect:** Earth's rotation deflects moving water (clockwise in N. Hemisphere, counter-clockwise in S. Hemisphere)[cite: 502].
    * [cite_start]**Thermohaline Circulation:** Density differences caused by temperature (*thermo*) and salinity (*haline*) create deep-ocean currents (the "Global Conveyor Belt")[cite: 505].
    * [cite_start]**Tides:** Lunar and solar gravity create regular currents, strongest near coasts[cite: 506].

---

## 2. Speed Terminologies (Target Parameters)
These terms define the "Reference Line" for performance. Deviations from these speeds often indicate fouling or mechanical issues.

### 2.1 Design and Contract Speeds
* **Design Speed:**
    * [cite_start]**Definition:** The theoretical speed the ship is intended to achieve under **ideal conditions** (calm water, clean hull) during the design phase [cite: 385-386].
    * [cite_start]**Use:** Basis for hull design and propulsion calculations[cite: 387].
* **Contract Speed:**
    * [cite_start]**Definition:** The speed **guaranteed** by the shipbuilder in the construction contract [cite: 389-390].
    * [cite_start]**Verification:** Must be proven during **Sea Trials** under strict conditions[cite: 391].
    * [cite_start]**Relation:** Typically slightly lower than Design Speed to allow for a safety margin[cite: 392].

### 2.2 Operational Engine Ratings
* **MCR (Maximum Continuous Rating):**
    * [cite_start]**Definition:** The **maximum power** the main engine can deliver continuously[cite: 394].
    * [cite_start]**Constraint:** Not used for regular operation; reserved for emergencies or sea trials to prove contract speed [cite: 395-396].
* **NCR (Normal Continuous Rating) / Service Speed:**
    * [cite_start]**Definition:** The safe continuous operating power, typically **85-90% of MCR**[cite: 399].
    * [cite_start]**Purpose:** Balances fuel efficiency with engine longevity[cite: 400].

### 2.3 Efficiency Modes
* **Economical Speed:**
    * [cite_start]**Definition:** A specific reduced speed (usually 2-4 knots lower than Service Speed) calculated to minimize fuel consumption per mile [cite: 401-403].
* **Slow Steaming:**
    * [cite_start]**Definition:** Deliberately operating at significantly reduced speeds (often 50-70% of full power) [cite: 404-405].
    * [cite_start]**Typical Range:** 12-16 knots for large container ships[cite: 407].
    * [cite_start]**Purpose:** Drastically reduces fuel costs and emissions[cite: 406].

---

## 3. Vessel Performance (Interaction Mechanics)
This section explains how the ship physically interacts with water and how performance is measured.

### 3.1 Speed Metrics: The "Treadmill" Concept
To evaluate performance, one must distinguish between the effort of the engine and the actual progress made.

* **Speed Through Water (STW):**
    * [cite_start]**Definition:** The speed of the ship relative to the water directly around it[cite: 511].
    * [cite_start]**Physics:** This is the speed produced purely by the propeller's thrust pushing against the water[cite: 520].
    * **Analogy:** A car running on a treadmill. [cite_start]The speedometer reads 20 km/h (Wheel Speed/STW), even if the treadmill is moving backwards [cite: 515-517].
* **Speed Over Ground (SOG):**
    * [cite_start]**Definition:** The actual speed of the ship relative to the seabed (Earth), measured by GPS[cite: 524].
    * [cite_start]**Formula:** $$SOG = STW + Current\_Effect$$[cite: 528].
    * **Scenarios:**
        * [cite_start]**Following Current:** Current pushes ship $\rightarrow$ $SOG > STW$[cite: 532].
        * [cite_start]**Opposing Current:** Current pushes back $\rightarrow$ $SOG < STW$[cite: 533].

### 3.2 Wind Interaction
* [cite_start]**Relative Wind:** The wind felt on the ship, measured by the ship's anemometer [cite: 536-537].
* [cite_start]**Formula:** $$Relative\_Wind = True\_Wind - Ship's\_Motion$$[cite: 539].
* **Analogy:** If you drive a car at 60 km/h on a calm day, you feel a 60 km/h "wind" on your face. [cite_start]This is Relative Wind created by motion[cite: 544].



### 3.3 Propeller Physics: The "Slip" Concept
A ship's propeller is like a screw, but because water is fluid, it "slips" and does not move the ship the full theoretical distance.

* [cite_start]**Definition:** The difference between the **Theoretical Speed** (Pitch $\times$ RPM) and the **Actual Speed** (STW)[cite: 550, 562].
* [cite_start]**Causes:** Water resistance, hull drag, wake flow, and fluid inefficiency [cite: 556-560].
* **Formula:**
    [cite_start]$$Slip (\%) = \frac{\text{Theoretical Speed} - \text{Actual Speed}}{\text{Theoretical Speed}} \times 100$$ [cite: 562]
* **Analogy:** A car driving on a muddy road. [cite_start]The wheels rotate (RPM), but the car moves forward less than it would on dry pavement because the tires slip in the mud [cite: 567-570].
    * **High Slip:** Indicates high resistance (fouling) or rough weather.

---

## 4. Performance Evaluation Logic (The Cycle Analogy)
How do we distinguish between "Bad Weather" and a "Bad Engine"? The manual uses a detailed bicycle analogy to explain **Performance Normalization**.

### 4.1 The Variables
* [cite_start]**The Bicycle:** Represents the Ship[cite: 797].
* [cite_start]**The Cyclist:** Represents the Engine[cite: 798].
* [cite_start]**Tyre Wear:** Represents **Hull Fouling** (Marine growth increasing resistance)[cite: 800].
* [cite_start]**Cyclist Injury:** Represents **Engine Degradation** (Lower efficiency over time)[cite: 803].
* [cite_start]**Rough Road:** Represents **Bad Weather** (Waves/Wind)[cite: 813].
* [cite_start]**Extra Load (Backpack):** Represents **Draft/Cargo Increase**[cite: 816].

### 4.2 The Logic of Degradation
Over time, two main factors degrade performance:
1.  **Hull Fouling:** Like under-inflated or worn tires, marine growth increases resistance. [cite_start]The engine (cyclist) must work harder (burn more fuel) to maintain the same speed [cite: 825-829].
2.  **Engine Degradation:** Like an injured cyclist, the engine loses thermal efficiency. [cite_start]It consumes more fuel to produce the *same* amount of power [cite: 803-804].

### 4.3 Normalization (The "Correction" Process)
To accurately measure the health of the hull and engine, we must remove external variables.
* [cite_start]**Goal:** Compare the current performance against the **Sea Trial (Shop Test)** baseline [cite: 806-811].
* **Process:**
    * [cite_start]**Step 1:** "Negate" the power added due to rough roads (Weather Correction)[cite: 814].
    * [cite_start]**Step 2:** "Normalize" the power added due to extra load (Draft Correction)[cite: 817].
* [cite_start]**Result:** The remaining deviation is purely due to **Hull Fouling** and **Engine Degradation**[cite: 823].

### 4.4 Added Fuel Calculation Example
To quantify the cost of fouling:
1.  [cite_start]**Calculate Added Power:** $$Added\_Power = P_{delivered\_actual} - P_{sea\_trial}$$[cite: 955].
2.  [cite_start]**Calculate Added Energy:** $$Added\_Energy = Added\_Power \times Time$$[cite: 957].
3.  **Calculate Added Fuel:**
    [cite_start]$$Added\_Fuel = \frac{Added\_Energy}{LCV \text{ (Lower Calorific Value)}}$$[cite: 960].


# Advanced Performance Dependencies and Calculation Logic

## 1. The Power Transmission Chain (Loss Logic)
Understanding where power is lost is vital for distinguishing between "Engine Problems" and "Hull Problems".

### 1.1 Power Delivered vs. Effective Power
* [cite_start]**Power Delivered ($P_{del}$):** The raw power produced by the main engine at the crankshaft[cite: 831].
    * *Analogy:* Power delivered to the bicycle pedals.
* [cite_start]**Effective Power ($P_{eff}$):** The power actually available at the propeller to push the ship, *after* accounting for mechanical losses[cite: 832].
    * *Analogy:* Power at the bicycle wheels after chain/sprocket friction.
* **Transmission Loss ($L_{trans}$):** The energy lost in the gearbox, shaft, and bearings.
    * [cite_start]**Standard Value:** Typically estimated at **2%** of delivered power[cite: 952].
    * **Formula:**
      $$P_{eff} = P_{del} \times (1 - L_{trans})$$
    * [cite_start]*Example:* If the engine delivers 10,000 kW, only 9,800 kW reaches the propeller[cite: 962].

### 1.2 The Dependency
* **Inter-variable Relation:** $P_{eff}$ is directly proportional to $P_{del}$ but inversely proportional to mechanical friction (wear in bearings/shaft).
* **RAG Diagnostic Rule:** If fuel consumption is high but $P_{del}$ is normal, the issue might be downstream (shaft/propeller efficiency) rather than inside the engine cylinder.

---

## 2. The Fuel-Energy-Power Triangle
This section provides the mathematical bridge between "Physics" (Power) and "Economics" (Fuel Cost).

### 2.1 The Core Formula Chain
1.  **Energy Calculation:** Power is instantaneous; Energy is cumulative.
    * [cite_start]$$Energy~(kJ) = Power~(kW) \times Time~(seconds)$$ [cite: 957-958].
2.  **Fuel Mass Calculation:** To find how much fuel was burned to create that energy, we use the fuel's energy density (LCV).
    * **LCV (Lower Calorific Value):** The potential energy per kg of fuel (e.g., 42,700 kJ/kg).
    * **Formula:**
        [cite_start]$$Mass_{fuel} = \frac{Energy_{total}}{LCV}$$[cite: 960].

### 2.2 Variable Interdependencies
* **LCV Dependency:** If you switch to a lower quality fuel (Lower LCV), you must burn **more mass** of fuel to generate the **same energy**.
    * *Rule:* Fuel Consumption $\propto \frac{1}{LCV}$.
* **Time Dependency:** Added consumption scales linearly with voyage duration. A small efficiency loss (fouling) becomes a massive cost over a long voyage (high Time).

---

## 3. The Anatomy of "Added Consumption"
Total fuel consumption is not a single number; it is the sum of three distinct "buckets." The RAG system must be able to attribute excess fuel to the correct bucket.

### 3.1 Bucket 1: Hull & Propeller Fouling (Resistance)
* **Cause:** Marine growth (barnacles/slime) increases friction.
* **Calculation Logic:**
    * Compare **Actual Power** vs. **Sea Trial Power** (at the same speed).
    * [cite_start]$$Added~Power_{fouling} = P_{actual} - P_{seatrial}$$[cite: 955].
    * *Note:* This calculation assumes weather and draft have already been normalized.

### 3.2 Bucket 2: Engine Degradation (Efficiency)
* [cite_start]**Cause:** Wear and tear on engine components (injectors, liners) reducing thermal efficiency [cite: 802-804].
* **Calculation Logic (SFOC Shift):**
    * Calculate **Current SFOC** (Specific Fuel Oil Consumption) based on current fuel/power data.
    * Compare with **Shop Test SFOC** (Baseline) for that specific power load.
    * [cite_start]$$Added~Fuel_{engine} = (SFOC_{current} - SFOC_{shop}) \times Energy_{total}$$ [cite: 973-974].

### 3.3 Bucket 3: External Factors (To be Negated)
* **Weather:** Rough seas increase resistance (like a damaged road). [cite_start]This power demand is **negated** (subtracted) during analysis to isolate vessel health[cite: 814, 941].
* **Draft (Load):** Heavier cargo increases displacement. [cite_start]This power demand is **normalized** (adjusted via coefficients) to compare fairly with the baseline[cite: 817, 941].



---

## 4. SFOC as a Diagnostic Variable
**Specific Fuel Oil Consumption (SFOC)** is the "health check" metric for the engine itself.

### 4.1 Definition & Formula
* **Definition:** The amount of fuel (in grams) the engine burns to produce 1 kilowatt-hour (kWh) of energy.
* **Formula:**
    [cite_start]$$SFOC~(g/kWh) = \frac{\text{Fuel Flow}~(g/hr)}{\text{Power}~(kW)}$$ [cite: 968-970].

### 4.2 Diagnostic Interpretation
* **Scenario A:** $P_{del}$ is High, but SFOC is Normal.
    * *Diagnosis:* The engine is healthy (converting fuel to power efficiently), but the **Hull is Fouled** (ship needs more power to move).
* **Scenario B:** $P_{del}$ is Normal, but SFOC is High.
    * *Diagnosis:* The **Engine is Degraded** (burning more fuel to produce the same power).
* **Scenario C:** Both are High.
    * [cite_start]*Diagnosis:* Combined degradation (Tyre wear + Cyclist injury) [cite: 825-826].

---

## 5. Summary of Dependencies for RAG Retrieval

| Dependent Variable | Primary Influencers | Inverse Influencers |
| :--- | :--- | :--- |
| **Fuel Consumed** | Power, Time, Fouling, Engine Age | LCV (Fuel Quality) |
| **SOG (Speed Over Ground)** | STW, Following Current | Opposing Current, Headwind |
| **Slip %** | Hull Resistance, Weather, Fouling | Propeller Efficiency |
| **Effective Power** | Power Delivered | Transmission Loss (Gearbox friction) |


# Marine Fuel Properties, Grading, and Consumption Logic

## 1. Marine Fuel Classifications (ISO 8217:2017)
Fuel is categorized by its refining level (Residual vs. Distillate) and its viscosity.

### 1.1 Residual Marine Fuels (HFO/LFO)
Residual fuels are the "bottom of the barrel" leftovers from refining. They are viscous and require heating.
* **HFO (Heavy Fuel Oil):** High-viscosity grades used by large main engines.
    * [cite_start]**Common Grades:** RME 180, RMG 380, RMK 700[cite: 636].
    * **Operational Requirement:** Must be heated to reduce viscosity for injection.
* **LFO (Light Fuel Oil):** Lower viscosity residual grades.
    * [cite_start]**Common Grades:** RMA 10, RMB 30, RMD 80[cite: 636].

### 1.2 Distillate Marine Fuels (MGO/MDO)
Distillates are cleaner, lighter fuels similar to diesel used in cars.
* **MGO (Marine Gas Oil):** Pure distillate, low viscosity.
    * [cite_start]**Grades:** DMA, DMZ[cite: 641].
    * [cite_start]**Viscosity Range:** 2.0–6.0 cSt at 40°C[cite: 641].
* **MDO (Marine Diesel Oil):** A blend of distillates with a small amount of residual fuel.
    * [cite_start]**Grade:** DMB[cite: 641].
    * [cite_start]**Viscosity Range:** 2.0–11.0 cSt at 40°C[cite: 641].

### 1.3 Emergency Fuel
* [cite_start]**DMX:** A special distillate grade with a lower flash point ($\ge 43^\circ$C) reserved specifically for emergency equipment like lifeboat engines and emergency generators[cite: 641, 758].

---

## 2. Critical Fuel Properties (The Variables)
These chemical properties determine *how* the fuel must be handled and *how much* energy it provides.

### 2.1 Sulfur Content
* **Why it matters:** Directly impacts compliance with **MARPOL Annex VI** and emission regulations. [cite_start]High sulfur causes acid rain and engine corrosion [cite: 735-736].
* **Operational Impact:**
    * [cite_start]Ships in **Emission Control Areas (ECAs)** must use fuel with $\le 0.10\%$ sulfur[cite: 740].
    * [cite_start]Global cap is $\le 0.50\%$ sulfur[cite: 651].
    * [cite_start]Ships using high-sulfur fuel must have "Scrubbers" (exhaust cleaning systems) installed[cite: 740].

### 2.2 Density
* **Why it matters:** Determines the **Mass-to-Volume ratio**. [cite_start]Fuel is bought by mass (metric tons) but measured by volume (liters/cubic meters)[cite: 743].
* **Operational Impact:**
    * [cite_start]Higher density means more energy per liter but makes the fuel harder to pump[cite: 744].
    * Crucial for setting **Purifiers** (centrifuges) that separate water/sludge from fuel. [cite_start]Incorrect density settings cause fuel loss or engine damage[cite: 747].

### 2.3 Viscosity
* [cite_start]**Why it matters:** Determines flow resistance and how well the fuel "atomizes" (sprays) inside the engine cylinder[cite: 750].
* **Constraints:**
    * [cite_start]**Too High:** Poor atomization leading to incomplete combustion and soot[cite: 751].
    * [cite_start]**Too Low:** Risk of leakage in fuel pumps and injectors[cite: 752].
* [cite_start]**Operational Impact:** Residual fuels (HFO) must be heated to a specific temperature to reach the correct viscosity before entering the engine[cite: 754].

### 2.4 Flash Point
* [cite_start]**Why it matters:** A safety parameter defining the minimum temperature at which fuel vapors can ignite[cite: 757].
* [cite_start]**Regulatory Limit:** Marine fuels must have a flash point $\ge 60^\circ$C (except DMX) to ensure safe storage in hot engine rooms[cite: 758].

### 2.5 Lower Calorific Value (LCV)
* [cite_start]**Why it matters:** Indicates the "Energy Density" of the fuel (Energy content per kg)[cite: 763].
* **Operational Impact:**
    * [cite_start]Used as the denominator in all fuel efficiency calculations[cite: 769].
    * [cite_start]**Correlation:** Higher LCV = More energy output per ton = Better commercial efficiency[cite: 766].
    * *Note:* Gas fuels (LNG) generally have higher LCV than liquid fuels.

---

## 3. Alternative Fuels (Decarbonization)

As the industry shifts away from fossil fuels, these alternatives are becoming critical for RAG knowledge bases handling "Green Shipping" queries.

### 3.1 Gas-Based Fuels
* **LNG (Liquefied Natural Gas):**
    * [cite_start]**Pros:** Reduces $CO_2$ by 20-30%; eliminates SOx and Particulate Matter (PM) [cite: 670-671].
    * [cite_start]**Cons:** Requires cryogenic storage (-162°C) and specialized bunkering infrastructure[cite: 672].
    * [cite_start]**Engine:** Commonly used in Dual-Fuel engines[cite: 790].
* **LPG (Liquefied Petroleum Gas):**
    * [cite_start]**Pros:** Low SOx/NOx; easier to store than LNG [cite: 674-675].
    * [cite_start]**Cons:** Still emits $CO_2$ (fossil-based)[cite: 676].

### 3.2 Alcohol and Ammonia
* **Methanol:**
    * [cite_start]**Pros:** Liquid at ambient temperature (easy handling); reduces SOx/NOx/PM [cite: 678-680].
    * [cite_start]**Cons:** Toxic and has a low flash point (safety risk)[cite: 682].
* **Ammonia:**
    * [cite_start]**Pros:** **Zero carbon emissions** at combustion[cite: 691].
    * [cite_start]**Cons:** Highly toxic and corrosive; requires special handling; lower energy density than oil [cite: 692-693].

### 3.3 Biofuels
* [cite_start]**FAME (Fatty Acid Methyl Esters):** Biodiesel from veg oils/animal fats; common in blends [cite: 711-714].
* [cite_start]**HVO (Hydrotreated Vegetable Oil):** Renewable diesel; a high-quality "drop-in" replacement for conventional diesel [cite: 715-718].
* [cite_start]**Impact:** Can achieve 80-90% lifecycle $CO_2$ reduction[cite: 687].

---

## 4. Fuel Consumption Calculation Logic
This section details how to convert "Power" into "Fuel Mass" to determine performance loss.

### 4.1 The Core Formula (Power to Mass)
To calculate how much extra fuel is burned due to inefficiencies (like fouling):
[cite_start]$$Added~Fuel (\Delta F) = \frac{Added~Energy (\Delta E)}{LCV}$$ [cite: 960]

### 4.2 Step-by-Step Calculation Flow
1.  **Calculate Added Power ($\Delta P$):**
    * Subtract the **Sea Trial Power** (Baseline) from the **Actual Power** (Current).
    * [cite_start]$\Delta P = P_{actual} - P_{trial}$[cite: 955].
2.  **Calculate Added Energy ($\Delta E$):**
    * Multiply Added Power by the duration (Time).
    * [cite_start]$\Delta E = \Delta P \times Time$[cite: 957].
    * *Unit Note:* If Power is kW and Time is Hours, Energy is kWh. [cite_start]Convert to kJ if LCV is in kJ/kg ($1~kWh = 3600~kJ$)[cite: 958].
3.  **Calculate Fuel Mass:**
    * Divide Energy by the Fuel's LCV.
    * [cite_start]$Mass_{fuel} = \frac{\Delta E}{LCV}$[cite: 960].

### 4.3 SFOC Calculation (Engine Health Check)
**Specific Fuel Oil Consumption (SFOC)** measures engine efficiency independent of the hull.
* **Formula:**
    [cite_start]$$SFOC~(g/kWh) = \frac{Fuel~Consumption~(g/hr)}{Power~(kW)}$$ [cite: 968-970].
* **Logic:**
    * [cite_start]If calculated SFOC > Shop Test SFOC, the **engine** is degrading [cite: 971-972].
    * [cite_start]The difference determines "Added Fuel due to Engine Degradation" [cite: 973-974].

### 4.4 Example Data Points
* [cite_start]**Transmission Loss:** Typically **2%** of delivered power is lost between engine and propeller[cite: 952].
* [cite_start]**Typical LCV:** ~42,700 kJ/kg for standard marine fuel[cite: 950].
* [cite_start]**Baseline Comparison:** Always compare *Effective Power* (at propeller) to ensure apples-to-apples comparison between sea trials and daily operations [cite: 961-962].


# Advanced Fuel Dependencies and Operational Relations

## 1. Physical Property Dependencies (Cause & Effect)
Understanding how fuel properties dictate operational requirements is critical for avoiding machinery failure.

### 1.1 The Viscosity-Temperature-Combustion Chain
* **The Relationship:** Viscosity is inversely proportional to temperature.
* **Operational Logic:**
    * **Residual Fuels (HFO):** Have high natural viscosity (e.g., 380 cSt). [cite_start]They must be **heated** to reduce viscosity to the required level for injection[cite: 754].
    * **Combustion Dependency:**
        * [cite_start]**Too High Viscosity:** Causes poor "atomization" (spray pattern) in the cylinder $\rightarrow$ leads to incomplete combustion and soot deposits [cite: 750-751].
        * [cite_start]**Too Low Viscosity:** Causes leakage in fuel pumps and injectors due to lack of lubrication film[cite: 752].
* **RAG Diagnostic Rule:** If "Incomplete Combustion" alarms trigger, check if **Fuel Heating** is sufficient for the specific grade (RMG/RMK) in use.

### 1.2 The Density-Mass-Purification Chain
* **The Relationship:** Density affects the separation of impurities and the calculation of energy.
* **Mass vs. Volume:**
    * Fuel is purchased by **Weight** (Metric Tonnes) but measured onboard by **Volume** (Cubic Meters).
    * [cite_start]**Relation:** $$Mass = Volume \times Density$$[cite: 743].
    * [cite_start]**Energy Impact:** Higher density fuels contain more energy per *liter* but are harder to pump[cite: 744].
* **Purifier Dependency:**
    * Centrifugal purifiers remove water and sludge based on density difference.
    * **Constraint:** If the fuel density is too close to water ($1.0~kg/L$), purification fails. [cite_start]The "Gravity Disc" or electronic settings must strictly match the specific fuel density[cite: 747].

### 1.3 The Sulfur-Emissions-Equipment Chain
* [cite_start]**Regulatory Trigger:** **IMO 2020** limits global sulfur to 0.50%, and **ECAs** (Emission Control Areas) limit it to 0.10%[cite: 651].
* **Equipment Dependency:**
    * [cite_start]**High Sulfur Fuel (HSFO):** Can *only* be used if the ship has a **Scrubber** (Exhaust Gas Cleaning System) installed[cite: 740].
    * **Low Sulfur Fuel (VLSFO/MGO):** Must be used if no scrubber exists.
* [cite_start]**Damage Relation:** High sulfur combustion creates sulfuric acid, leading to **cold corrosion** in engines and acid rain environmentally[cite: 736].

---

## 2. Dual-Fuel Engine Dependencies
This section defines the logic for modern engines that switch between gas and liquid modes.

### 2.1 The Primary-Secondary Fuel Relation
* [cite_start]**Definition:** Dual-fuel engines are designed to run on two specific types of fuel simultaneously or alternatively[cite: 786].
* **Operational Modes:**
    1.  **Gas Mode (Primary):** The engine runs on LNG, LPG, or Methanol.
    2.  [cite_start]**Pilot Fuel (Ignition):** Even in gas mode, a small amount of **Liquid Fuel (MDO)** is injected to ignite the gas (since gas does not self-ignite easily by compression)[cite: 788].
    3.  [cite_start]**Backup Mode:** If the gas system fails, the engine automatically switches to 100% liquid fuel[cite: 788].
* **RAG Context:** When calculating "Total Fuel Consumption" for a dual-fuel ship, the system must sum **Gas Consumption + Pilot Fuel Consumption**.

---

## 3. Advanced Consumption Mathematics (Attribution Logic)
This is the core logic for distinguishing **Hull Fouling** from **Engine Degradation**. The manual uses a specific subtraction method to isolate these variables.

### 3.1 Step 1: Calculating "Added Power" (The Hull Factor)
* **Concept:** Determine how much *extra* power is needed solely to overcome external resistance (fouling).
* **Formula:**
  $$Added~Power (\Delta P) = P_{Actual} - P_{SeaTrial}$$
  [cite_start]*(Note: Comparisons must be made at the same speed)*[cite: 955].
* **Energy Conversion:**
  [cite_start]$$Added~Energy = \Delta P \times Time$$[cite: 957].
* **Fuel Cost of Fouling:**
  [cite_start]$$Added~Fuel_{Hull} = \frac{Added~Energy}{LCV}$$[cite: 960].

### 3.2 Step 2: Calculating "Effective Power" (Transmission Loss)
* **Concept:** Power measured at the engine is not what reaches the propeller.
* **Relation:**
  $$P_{Effective} = (P_{Delivered} - Added~Power) \times (1 - Loss_{Trans})$$
* [cite_start]**Standard Loss:** Typically **2%** (0.02) for gearbox/shaft friction[cite: 962].

### 3.3 Step 3: Calculating "Engine Degradation" (The SFOC Factor)
* **Concept:** If the engine burns more fuel per kWh than it did when new, the *engine itself* is degraded.
* **SFOC Formula:**
  [cite_start]$$SFOC_{Current}~(g/kWh) = \frac{Fuel~Flow~(g/hr)}{P_{Effective}~(kW)}$$ [cite: 968-970].
* **Degradation Calculation:**
  [cite_start]$$Added~Fuel_{Engine} = (SFOC_{Current} - SFOC_{ShopTest}) \times Effective~Energy$$ [cite: 973-974].

### 3.4 The Total Consumption Equation
For a complete performance report, the total fuel consumed is the sum of three components:
$$Total~Fuel = Fuel_{Baseline} + Fuel_{HullFouling} + Fuel_{EngineDegradation}$$
[cite_start]*[cite: 975-978]*

---

## 4. Energy Density (LCV) Relations
* **The Efficiency Dependency:** Fuel efficiency is not just about the engine; it is about the fuel's chemistry.
* **Relation:**
  $$Consumption \propto \frac{1}{LCV}$$
* **Implication:**
    * If you switch from **MGO** (LCV ~42,700 kJ/kg) to **LNG** (Higher LCV), you burn less mass for the same power.
    * [cite_start]If you use a **Biofuel blend** with lower LCV, your consumption (in metric tonnes) will **increase** to maintain the same speed [cite: 764-766].



# Commercial Engagement and Regulatory Frameworks

## 1. Regulatory Governance Structure
Ships operate in international waters, so they are governed by a hierarchy of global and national bodies rather than a single government.

### 1.1 International Maritime Organization (IMO)
* [cite_start]**Role:** The UN specialized agency that sets global standards for safety, security, and environmental performance[cite: 47, 50].
* [cite_start]**Jurisdiction:** Global scope; its conventions (rules) are adopted by member countries[cite: 50].
* **Key Conventions:**
    * **SOLAS:** Safety of Life at Sea (Construction, Fire Safety, Life-saving).
    * **MARPOL:** Marine Pollution (Emissions, Sewage, Oil).
    * [cite_start]**STCW:** Standards of Training, Certification, and Watchkeeping for Seafarers[cite: 50, 71].
* [cite_start]**Analogy:** Comparable to an international body setting vehicle safety standards, but enforced by individual nations[cite: 49].

### 1.2 The "Tripartite" Enforcement System

* **Flag State (The "Registry"):**
    * **Definition:** The country where the ship is registered (e.g., Panama, Liberia).
    * **Role:** Has primary legal jurisdiction over the ship anywhere in the world. [cite_start]Issues statutory certificates and ensures IMO rule implementation [cite: 64-65, 74].
    * [cite_start]**Analogy:** Like the "RTO" (Regional Transport Office) where your car is registered[cite: 65].
* **Port State Control (PSC) (The "Police"):**
    * **Definition:** Inspectors from the country *visiting* the ship (e.g., US Coast Guard inspecting a Greek ship in New York).
    * **Role:** Verifies compliance with international rules. [cite_start]Can **detain** unsafe ships until defects are fixed [cite: 66-67, 80-82].
    * [cite_start]**Analogy:** Like traffic police in another state checking your out-of-state car[cite: 67].
* **Classification Society (The "Tech Auditors"):**
    * [cite_start]**Definition:** Independent technical organizations (e.g., DNV, ABS, LR) authorized by the Flag State[cite: 61, 87].
    * [cite_start]**Role:** Sets technical rules for design/construction and surveys the ship to issue the **Class Certificate** [cite: 62, 88-89].
    * [cite_start]**Analogy:** Like ARAI/ICAT certification bodies ensuring a car model meets technical safety norms[cite: 61, 63].

---

## 2. Commercial Engagement Models (Chartering)
This section defines *who* pays for the ship's time and fuel.

### 2.1 The Parties Involved
* [cite_start]**Shipowner:** The legal owner who provides the vessel, ensures compliance, and maintains insurance (Hull & Machinery, P&I) [cite: 158-162].
* [cite_start]**Ship Manager:** Appointed by the owner to handle technical (maintenance/crew) or commercial (bookings) operations [cite: 163-166].
* [cite_start]**Charterer:** The entity that hires the ship to transport cargo [cite: 168-169].

### 2.2 Types of Charter Contracts
* **Voyage Charter:**
    * [cite_start]**Definition:** The ship is hired for a single specific trip (Voyage A to B)[cite: 171].
    * **Responsibility:** Owner pays for fuel and port dues; Charterer pays "Freight" for the cargo.
* **Time Charter:**
    * [cite_start]**Definition:** The ship is hired for a specific period (e.g., 6 months)[cite: 173].
    * **Responsibility:** Charterer directs the ship's schedule and **pays for fuel** and port charges. Owner provides crew and maintenance.
    * **RAG Context:** In Time Charters, "Fuel Efficiency" is the Charterer's main concern.
* **Bareboat Charter:**
    * [cite_start]**Definition:** The charterer leases the entire ship for a long term and takes full control, including hiring their own crew[cite: 174].

### 2.3 Commercial Milestones
* **On-Hire:**
    * The exact moment the ship is delivered to the charterer.
    * Charterer begins paying daily hire.
    * [cite_start]Requires an **On-Hire Survey** to record condition and fuel quantity [cite: 248-252].
* **Off-Hire:**
    * The ship is unavailable due to breakdown, repairs, or strikes.
    * Charterer **stops paying** daily hire.
    * [cite_start]**Off-Hire Clauses** define how deductions are calculated [cite: 253-260].

---

## 3. Commercial & Environmental Regulations (Decarbonization)
These regulations have direct financial implications for ship operations and are essential for modern performance software.

### 3.1 Carbon Intensity Indicator (CII)
* **Definition:** A rating system (A to E) measuring the operational efficiency of a ship.
* [cite_start]**Metric:** $CO_2$ emitted per tonne-mile of cargo moved[cite: 981, 983].
* **Analogy:** Like a "Fuel Efficiency Rating" (Mileage) for cars. [cite_start]A gas-guzzler gets a poor rating [cite: 984-986].
* [cite_start]**Impact:** Poor data quality (wrong distance/fuel) leads to a bad grade, which restricts the ship's ability to trade[cite: 989, 1041].

### 3.2 EU Emissions Trading System (EU ETS)
* [cite_start]**Definition:** A "Cap and Trade" system where ships must pay for their carbon emissions on voyages to/from/within the EU [cite: 991-992].
* [cite_start]**Mechanism:** More fuel burned $\rightarrow$ More $CO_2$ $\rightarrow$ Higher financial cost[cite: 993].
* **Impact:** Accurate reporting is financially critical. [cite_start]40-70% of EU voyages fall under this rule [cite: 996-997].

### 3.3 FuelEU Maritime
* [cite_start]**Definition:** Upcoming regulation focusing on the **Greenhouse Gas (GHG) Intensity** of the energy used [cite: 1007-1008].
* **Goal:** Forces the adoption of cleaner fuels (biofuels, blends) over time.
* [cite_start]**Penalty:** Ships are penalized if their average GHG intensity exceeds the limit [cite: 1012-1015].

### 3.4 Energy Efficiency Operational Indicator (EEOI)
* [cite_start]**Definition:** A voluntary monitoring tool measuring fuel per cargo tonne-mile[cite: 1021].
* [cite_start]**Usage:** Tracks real-world efficiency variations due to hull fouling, weather, or operational decisions [cite: 1032-1037].

---

## 4. Why Data Accuracy Matters (Developer Context)
The manual explicitly links software data quality to financial risk.

* **The "Garbage In, Garbage Out" Risk:**
    * Incorrect Fuel Logs + Wrong Distance = Incorrect $CO_2$ Values.
    * [cite_start]**Result:** Wrong CII Grades, EU ETS Fines, and Contract Penalties [cite: 1039-1043].
* **Car Analogy:**
    * If you calculate car mileage using a broken odometer and a guessed fuel amount, your efficiency calculation is meaningless. [cite_start]Ships face the same issue, but the financial penalties are in the millions [cite: 1044-1049].

# Future Technologies and Decarbonization Pathways

## 1. The Fuel Transition Hierarchy
The industry categorizes fuels based on their carbon footprint and technological maturity. This hierarchy defines the roadmap to zero emissions.

### 1.1 Conventional Marine Fuels (The Baseline)
* [cite_start]**Types:** HFO (Heavy Fuel Oil), MDO (Marine Diesel Oil), MGO (Marine Gas Oil) [cite: 772-775].
* **Status:** Fossil-based, high carbon, fully established infrastructure.

### 1.2 Low-Carbon Fuels (Transitional)
* [cite_start]**Types:** Natural Gas (LNG), Fossil-based Methanol [cite: 776-777].
* **Role:** Immediate reduction in emissions (SOx, NOx, Partial CO2) but still fossil-derived.

### 1.3 Carbon-Neutral Fuels
* [cite_start]**Types:** Biodiesel, Bio-methanol, Biogas [cite: 778-779].
* **Role:** "Drop-in" or compatible fuels derived from organic matter where the CO2 absorbed during growth roughly equals the CO2 emitted during combustion.

### 1.4 Zero-Carbon Fuels (The Goal)
* [cite_start]**Types:** Electricity, Green Hydrogen, Green Ammonia [cite: 780-783].
* **Role:** Fuels that release **zero CO2** at the point of combustion (or usage).

---

## 2. Alternative Fuel Chemistries

Each fuel type presents specific engineering challenges regarding storage, toxicity, and energy density.

### 2.1 LNG (Liquefied Natural Gas)
* **Definition:** Natural gas cooled to liquid state for transport.
* **Advantages:**
    * [cite_start]Lowers CO2 emissions by **20-30%**[cite: 670].
    * [cite_start]Drastically cuts SOx, NOx, and Particulate Matter (PM)[cite: 671].
* **Challenges:**
    * [cite_start]Requires **cryogenic storage** (very low temperatures) and specialized bunkering infrastructure[cite: 672].
    * [cite_start]Commonly used in **Dual-Fuel Engines**[cite: 790].

### 2.2 LPG (Liquefied Petroleum Gas)
* **Advantages:** Low SOx and NOx emissions; [cite_start]**easier storage** than LNG (less extreme temperature/pressure requirements) [cite: 674-675].
* [cite_start]**Challenges:** It is still a fossil fuel and emits CO2[cite: 676].

### 2.3 Methanol
* **Advantages:**
    * [cite_start]**Liquid at ambient temperature**, making bunkering and storage much simpler than LNG/Hydrogen[cite: 678].
    * [cite_start]Significantly reduces SOx, NOx, and PM[cite: 679].
* **Challenges:**
    * **Toxic** to humans.
    * [cite_start]**Low Flash Point**, creating safety/fire risks[cite: 682].

### 2.4 Ammonia ($NH_3$)
* [cite_start]**Advantages:** **Zero carbon emissions** during combustion[cite: 691].
* **Challenges:**
    * [cite_start]**Highly Toxic** and corrosive; a leak can be fatal to the crew[cite: 692].
    * [cite_start]Lower energy density requires larger storage tanks[cite: 693].
    * Requires special handling protocols.

### 2.5 Hydrogen ($H_2$)
* [cite_start]**Advantages:** **Zero CO2** emissions when used in fuel cells or combustion[cite: 695].
* **Challenges:**
    * [cite_start]Requires **cryogenic** or **high-pressure** storage[cite: 697].
    * [cite_start]Infrastructure is currently very limited[cite: 697].

---

## 3. Biofuels (Drop-In Solutions)
Biofuels are critical because they often do not require engine modifications.

### 3.1 FAME (Fatty Acid Methyl Esters)
* [cite_start]**Source:** Produced from vegetable oils or animal fats[cite: 713].
* [cite_start]**Usage:** Common in **Biodiesel blends** (e.g., B20, B30)[cite: 714].
* **Operational Note:** First-generation biodiesel; requires careful handling to prevent microbial growth or filter clogging.

### 3.2 HVO (Hydrotreated Vegetable Oil)
* [cite_start]**Source:** Renewable diesel made by hydrogen-treating plant oils[cite: 716].
* [cite_start]**Advantage:** A high-quality **"Drop-in" replacement** for conventional diesel[cite: 718]. It mimics the chemical properties of diesel almost perfectly, unlike FAME.

### 3.3 Lifecycle Impact
* [cite_start]**Potential:** Can achieve up to **80-90% reduction** in lifecycle CO2 emissions[cite: 687].
* [cite_start]**Challenge:** Sustainability of the feedstock (raw material) supply[cite: 688].

---

## 4. Non-Fuel Technologies
Decarbonization also involves mechanical assistance to reduce fuel demand.

### 4.1 Wind-Assisted Propulsion

* [cite_start]**Technologies:** Rotor sails (Flettner rotors), Kites, Rigid Wing sails[cite: 703].
* **Efficiency Gains:**
    * [cite_start]**Retrofit:** 5-20% fuel savings[cite: 704].
    * [cite_start]**New Builds:** Up to 50% potential savings[cite: 704].

### 4.2 Battery-Electric & Hybrid Systems
* [cite_start]**Use Case:** Ideal for **short voyages** (ferries) and **port operations**[cite: 706].
* [cite_start]**Advantage:** **Zero emissions** during operation (silent and clean)[cite: 707].
* [cite_start]**Limitation:** Limited range due to battery weight and capacity[cite: 708].

### 4.3 Synthetic e-Fuels
* [cite_start]**Definition:** Fuels created using renewable electricity (Power-to-X), such as e-Methanol, e-Ammonia, or e-Diesel[cite: 698].
* [cite_start]**Potential:** Theoretically **Carbon-Neutral** if the electricity used is green[cite: 699].
* [cite_start]**Barrier:** High production cost and limited current availability[cite: 700].

