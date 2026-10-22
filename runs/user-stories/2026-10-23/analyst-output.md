```yaml
- id: US-01
  user: fleet technician
  title: spotting birds flagged for repairs at the start of shift
  story: >
    When I come on shift in the morning, I need to know immediately which drones came back with faults from their night runs or were flagged for work while I was away. If those birds are mixed in with healthy ones, I have no quick way to tell where my tools need to go first. I need a clear separation between machines that can fly and machines that need my hands on them before anything else moves.
  fear: >
    A damaged drone could be sent back out into the air, or I could spend half my morning driving to the wrong site while a broken bird sits waiting for help.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-02
  user: fleet technician
  title: swapping depleted batteries at outstations
  story: >
    My day involves driving between our remote landing sites to swap dead batteries for fresh ones so flights can keep moving. I need to know which sites have drones sitting drained before those birds hold up the next scheduled run. When I pull up to a site, I want certainty that the bird waiting on the ground actually needs a battery swap and is ready for me to service it.
  fear: >
    Drones will sit dead on pads across the region, blocking incoming flights and leaving me guessing which location needs fresh power first.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-03
  user: fleet technician
  title: repairing landing gear in the field
  story: >
    A lot of the birds take hard knocks on rough ground and come in with cracked or bent landing gear. I need to know which drones on the pads have mechanical gear damage so I can bring the right replacement struts out in my van. Being able to fix them right there on the pad saves having to haul the whole bird back to base.
  fear: >
    I show up at an outstation without the right replacement gear parts, forcing me to haul a drone back to the workshop for a repair I could have done on the spot.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-04
  user: fleet technician
  title: pulling damaged birds off pads for workshop bench repair
  story: >
    When a drone has serious structural or internal troubles that I cannot patch in the field, I have to take it completely out of circulation and bring it to the bench. I need to mark that bird as grounded so no dispatcher tries to assign work to it while it sits in the back of my van. Once it is cleared off the pad, other birds can use that space again without risking a collision.
  fear: >
    A dispatcher might attempt to launch a drone that is physically in the back of my van, or an incoming bird might try to land on a pad occupied by a broken machine.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-05
  user: fleet technician
  title: commissioning new charging pads at field sites
  story: >
    Setting up new charging pads is a regular part of my week as our network grows into new areas. When I finish wiring and testing a new pad, I need the whole operation to recognize that this pad exists, is safe, and can take down birds. Until that pad is officially recognized as active, no flights can plan to use it for recharging.
  fear: >
    Freshly built pads will sit completely idle and empty because the operational network does not know they exist, wasting the effort put into installing them.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-06
  user: fleet technician
  title: registering brand new birds into service
  story: >
    Management regularly brings in new birds that I have to inspect, assemble, and add to our active fleet registry. I need to confirm that every new machine is logged with its exact model, connector style, and serial number before it is cleared for its first flight. That way everyone knows what kind of hardware is out there and what jobs it can physically handle.
  fear: >
    An uninspected or wrongly cataloged bird could be sent into service with unknown hardware limits, creating severe safety risks in flight.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-07
  user: fleet technician
  title: carrying matching spare connectors for different drone models
  story: >
    We run several drone models, and their charging connectors do not all match. Before I leave the workshop in the morning, I need to know which models are currently grounded or throwing charging errors at our outstations. That tells me whether I need round pins, flat blades, or heavy-duty marine plugs in my van crates for the day.
  fear: >
    I drive all the way out to an isolated pad only to discover I brought the wrong connector style, leaving the drone stranded and doubling my travel time.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-08
  user: fleet technician
  title: finishing maintenance compliance records for regulators
  story: >
    Every single afternoon, I have to account for every wrench turn, battery swap, and pad check I performed during my shift. The aviation authorities can show up or request our logs at any moment to verify that each bird and charging pad has been inspected and maintained strictly to rule. I need every action I take during the day to stay attached to that specific bird’s lifelong service log without data getting scrambled or dropped.
  fear: >
    A software glitch could drop our maintenance history, leaving us unable to prove our birds are safe, which could lead to regulators grounding our entire operation.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-09
  user: fleet technician
  title: surviving cold-weather battery drain during critical deliveries
  story: >
    When a sudden freeze hits, our drones burn through their battery reserves far faster than usual while fighting the wind on hospital and inspection runs. When this happens, several low-battery birds begin heading for the nearest pads at the exact same moment. I need to know instantly which birds are running dangerously low on juice so I can prioritize clearing ground space for them before they fall out of the sky.
  fear: >
    Dying drones will arrive at occupied pads with no battery left to hover, leading to forced ditching or catastrophic collisions on the ground.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-10
  user: fleet technician
  title: clearing jammed charging connectors in a crisis
  story: >
    During sudden weather rushes, birds slam down onto pads and their connectors sometimes bind, jam, or weld under heavy load. When a connector jams, the drone cannot leave, and no other bird can land on that pad. I need an unmistakable notice of which specific pad has a stuck mechanism so I can rush directly to that site with my pry tools and manual release keys.
  fear: >
    A single jammed pad can cause a backup that cascades across our whole route network, leaving airborne birds with nowhere to touch down.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-11
  user: fleet technician
  title: sorting out delayed and out-of-order radio messages
  story: >
    When bad storms roll through, our radio links get patchy and messages from the birds arrive late or completely out of order. I might see a alert saying a bird has an overheated battery, followed immediately by an older message from an hour ago saying everything is normal. I need to be able to tell at a glance whether a fault report reflects what is happening right this second or what happened twenty minutes ago.
  fear: >
    I could spend hours chasing phantom faults that cleared themselves long ago, or ignore a real mechanical failure because an older all-clear message arrived late.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-12
  user: fleet technician
  title: knowing the exact pad and mechanical fault before driving out
  story: >
    When an alert sounds that a drone is in trouble, I cannot afford to guess which corner of an airfield or outstation it is sitting on. I need the exact site identifier, the specific pad number, and the exact nature of the mechanical fault before I put my van in gear. Knowing whether it is an electrical short, a snapped blade, or a dead motor tells me whether I need heavy lifting gear, high-voltage gloves, or just a screwdriver.
  fear: >
    I show up at a remote facility with the wrong toolkit and have to spend two hours driving back and forth while an urgent pad stays blocked.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-13
  user: fleet technician
  title: verifying physical connector condition with my own hands
  story: >
    Out near the saltwater port, sea spray and grime cake our metal charging contacts, and high-current arcing can burn the plastic housings. A remote sensor on a screen might claim the connection is seated, but you cannot trust a digital readout when high voltage is involved. I need to inspect the pins with my own eyes and test the latch with my hands so I know with certainty that the hardware is safe for current to flow.
  fear: >
    Trusting a false healthy status on a screen could cause an electrical fire or give a technician an electric shock when plugging in a bird.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-14
  user: fleet technician
  title: retiring aging airframes from the fleet registry
  story: >
    When management decides an airframe has reached the end of its flight life or suffered too much structural fatigue, they instruct me to retire it. I need to permanently retire that specific airframe number from our active fleet so that nobody can ever assign it to a flight queue again. Its past maintenance records must remain intact for the authorities, but the machine itself must be dead to dispatch.
  fear: >
    A worn-out, retired drone could accidentally be assigned a live customer delivery because its retirement was not fully locked across the company.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-15
  user: fleet technician
  title: preventing duplicate hardware commands during radio dropouts
  story: >
    When the radio links are sputtering in heavy rain, systems often try to send instructions over and over again to make sure they get through. If a charging pad receives duplicate lock or release commands, the mechanical actuators can chatter, jam, or blow fuses. I need the hardware at the pad to handle patchy communication cleanly without repeating mechanical cycles that ruin the equipment.
  fear: >
    Actuators and pad mechanisms will burn out from repeated cycling during communication glitches, creating massive physical repair workloads for me in the field.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-16
  user: dispatcher
  title: reviewing the day's queued jobs across different sectors
  story: >
    When I sit down at the start of my shift, I have to look across all the work queued up for the day, from standard parcel runs to urgent hospital medical deliveries. Each job comes with its own priority, delivery window, and payload characteristics. I need to see the entire pending workload in one clear overview so I can plan how our available fleet will meet those commitments throughout the day.
  fear: >
    Critical deliveries like blood or medicine will sit forgotten in the queue while low-priority retail parcels consume our best drones and pads.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-17
  user: dispatcher
  title: matching payload weight and flight distance to drone capabilities
  story: >
    Before I sign off on any flight, I have to match the weight of the cargo and the distance of the trip against the specific lift capacity and battery size of each available drone. Some birds can carry heavy parcels across short hops, while others are built for long inspection runs with lighter cameras. I need to know the true physical rating and current readiness of each machine so I do not assign a heavy box to a lightweight bird.
  fear: >
    A drone will be overloaded beyond its design limit, causing its motors to overheat and forcing an emergency landing short of the destination.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-18
  user: dispatcher
  title: keeping flight corridors clear of active airspace closures
  story: >
    The sky we fly through is constantly being carved up by temporary flight bans and emergency closures ordered by the aviation authorities. As a dispatcher, I am legally responsible for making sure none of my flights enter an active closed zone. I need to see exactly where our corridors intersect any authority closures so I can divert or delay flights before they ever cross the forbidden boundary.
  fear: >
    A drone under my legal dispatch will penetrate a prohibited airspace zone, triggering severe regulatory penalties and risking airborne collisions.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-19
  user: dispatcher
  title: keeping legal responsibility over flight plan sign-offs
  story: >
    Company policy and aviation regulations place full legal responsibility for every flight squarely on my shoulders. I cannot allow an automated computer program to choose my drones or approve my flight paths for me; I must be the one who reviews the numbers and formally signs off. I need a process that presents me with all the facts and leaves the ultimate launch decision entirely in my hands.
  fear: >
    An automated system could launch a flight on an unsafe path that I would have rejected, leaving me personally liable for the resulting incident.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-20
  user: dispatcher
  title: managing launch pad contention among multiple dispatchers
  story: >
    On a busy shift, several dispatchers are all trying to get their flights out at the same time from the same popular hub sites. We frequently run into situations where two of us try to claim the same launch pad or the same high-capacity bird at the exact same moment. I need a clear way to know which pads and drones are genuinely free so we do not step on each other's toes or promise flights that cannot leave.
  fear: >
    Two dispatchers will dispatch flights from the same pad at the same time, creating ground gridlock and missed customer delivery deadlines.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-21
  user: dispatcher
  title: handling late customer loads without grounding the fleet
  story: >
    It is very common for a customer at an industrial site or medical clinic to run behind schedule packing their cargo box. When a parcel is not ready on the pad, holding the drone on that pad ties up space and burns down the battery reserve planned for the mission. I need to be able to delay or reassign the flight easily so the pad can be cleared for other incoming traffic.
  fear: >
    A single late parcel will freeze a critical pad, causing trailing flights to stack up in the air with nowhere safe to land.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-22
  user: dispatcher
  title: compensating for sudden wind drain on battery reserves
  story: >
    When strong headwinds kick up along our flight corridors, drones consume significantly more power than standard flight calculations predict. I manually check battery reserves and weather conditions before signing off on any trip in rough conditions. I need accurate, conservative estimates of battery consumption under actual wind speeds so I do not send a bird on a run it cannot complete.
  fear: >
    A drone will exhaust its battery mid-route fighting a headwind and crash into populated terrain or water.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-23
  user: dispatcher
  title: rerouting active flights around sudden afternoon airspace closures
  story: >
    During my worst shift, an emergency airspace closure dropped out of nowhere right across our main corridor while dozens of birds were airborne. I had to scramble to push new waypoints to each drone to steer them safely around the closed block without running them into each other. I need to be able to send safe diversion paths to all affected drones immediately when a sudden closure lands.
  fear: >
    Airborne drones will plow into newly closed emergency airspace before I can steer them clear, endangering public safety and grounding our business.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-24
  user: dispatcher
  title: scrambling for emergency landing pads during widespread diversions
  story: >
    When an unexpected closure forces multiple flights to abort their routes, every bird suddenly needs a place to set down at once. On bad days, our main base only has a handful of free pads, and dispatchers end up in a frantic race to claim landing spots before power runs out. I need an instantaneous, truthful accounting of every unoccupied pad across our entire network so I can direct diverted birds to safety.
  fear: >
    Diverted drones will reach a designated recovery site only to find all pads occupied, leaving them to hover until their batteries die completely.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-25
  user: dispatcher
  title: confirming whether flight overrides were received over flaky radios
  story: >
    When the weather turns foul and radio links begin sputtering, I often have to issue manual override instructions to turn a bird around or change its altitude. Because messages drop or lag, I find myself staring at the display unable to tell if the drone actually heard me or if it is still flying blind on its old route. I need positive confirmation that my emergency override took effect on the machine before I can breathe.
  fear: >
    I assume a drone is turning around when it never got the command, letting it fly straight into severe hazards while I wait for a status update.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-26
  user: dispatcher
  title: estimating drone position when status reports arrive late or out of order
  story: >
    During bad communication dropouts, drone updates often trickle in out of chronological sequence, showing a bird five miles back after it already reported being five miles forward. In those moments, I have to manually calculate where the bird ought to be along its corridor based on its last known speed and heading. I need the system to help me distinguish old delayed reports from true fresh positions so I am not making critical safety guesses in the dark.
  fear: >
    I make avoidance decisions based on a stale report that arrived late, accidentally steering a drone into an obstacle or another aircraft.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-27
  user: dispatcher
  title: starting a shift without formal personal handoffs
  story: >
    In our dispatch room, nobody sits down to give you an individual debrief when your shift begins; you just take a desk, look at the active board, and take ownership of whatever is in the air and in the queue. I need to be able to grasp the operational state within seconds of sitting down—what is flying, what is waiting, and where the bottlenecks are. Without that instant situational clarity, I risk making decisions based on incomplete context.
  fear: >
    I inherit an ongoing flight emergency that was developing right as I sat down and fail to react in time because there was no clear summary of active hazards.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-28
  user: dispatcher
  title: preventing the system from automating route generation
  story: >
    I worry deeply that future software updates will try to automate route selection in order to speed things up. Because the law holds me personally accountable for any incident involving my flights, I cannot permit an algorithm to choose where my drones fly or which machine takes which run. I need the system to respect my authority as the human dispatcher and never bypass my direct planning choices.
  fear: >
    The system automatically routes a flight through a problematic local area without my knowledge, making me legally liable for an incident I never authorized.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-29
  user: dispatcher
  title: maintaining dispatch control during peak system load
  story: >
    When our operations reach peak hours with high flight volumes and sudden weather shifts, software tools have a habit of lagging or freezing under the pressure. I cannot afford even thirty seconds of an unresponsive screen when I have multiple drones approaching busy landing hubs at high speed. I need rock-solid stability during the most chaotic moments of our day so my dispatch commands never stall.
  fear: >
    The dispatch platform freezes during an emergency reroute, leaving me unable to issue commands while drones fly blindly toward hazards.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-30
  user: dispatcher
  title: ensuring duplicate commands are not sent across unstable links
  story: >
    When radio coverage drops in and out, pressing a command button twice out of desperation can cause duplicate commands to queue up and hit the drone back-to-back. If a bird receives conflicting or repeated commands, its autopilot can get confused or execute unwanted maneuvers. I need certainty that when I transmit an instruction, the delivery channel handles the connection cleanly and never duplicates my actions.
  fear: >
    A drone receives duplicate turn or climb orders, causing it to over-correct violently and lose control in flight.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-31
  user: airspace desk
  title: verifying corridor geometry between named sites at shift start
  story: >
    My main duty when logging on is ensuring that all established flight corridors connecting our named launch and landing sites are properly mapped and active. These corridors are the shared pathways that allow parcel, medical, and inspection drones from different companies to navigate safely. I need to verify that every corridor is correctly aligned with the current terrain and permanent airspace structures before daily operations pick up.
  fear: >
    An outdated corridor alignment could direct multiple customer fleets into unmapped obstacles or newly restricted permanent airspace.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-32
  user: airspace desk
  title: entering planned authority closures with strict active windows
  story: >
    Every day, civil aviation and public safety authorities publish scheduled airspace closures with defined start and end times for things like planned construction cranes or military drills. I need to enter these scheduled restrictions into our shared airspace map well before they take effect so everyone knows when those corridors will close. Having accurate start and finish times allows participating operators to plan their schedules smoothly around the blackout.
  fear: >
    A scheduled closure is not entered in time, causing customer drones to fly straight into a zone where heavy construction or military exercises are actively underway.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-33
  user: airspace desk
  title: posting sudden emergency closures that drop without warning
  story: >
    Police activity, bushfires, or emergency medical helicopter flights often cause the authorities to declare instant airspace bans with zero advance warning. When an emergency closure lands on my desk, I have to publish it to our shared picture immediately so all corridors passing through that zone are marked shut. Every second of delay before that closure appears on the map increases the chance of a collision with an emergency aircraft.
  fear: >
    A customer drone crosses into an active police or rescue helicopter zone because I could not post the authority's sudden restriction fast enough.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-34
  user: airspace desk
  title: amending closure boundaries when authorities shift incident zones
  story: >
    During evolving incidents like large fires or chemical spills, the authorities frequently widen the restricted boundary or push back the reopening time while flights are already up. I have to update those boundaries immediately on the shared map so the safety cushion around the hazard reflects reality. I need the updated perimeter to update across the network cleanly without dropping any existing restrictions.
  fear: >
    The authorities expand an exclusion zone, but our map continues to show the old smaller boundary, leaving drones flying through an active danger area.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-35
  user: airspace desk
  title: assessing disruption impact across customer fleets after boundary changes
  story: >
    Whenever an authority alters an active closure, I need to know how many corridors and flights across our various customer companies—like medical transport and parcel couriers—were cut off by the change. Right now, I have to do this math manually in my head by comparing company routes against the new hazard shape. I need an immediate understanding of the overall disruption scale across all customer fleets so we can gauge how severe the airspace restriction is.
  fear: >
    I underestimate the widespread disruption caused by an amended closure, leaving critical medical delivery operators blindsided by severed corridors.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-36
  user: airspace desk
  title: maintaining the shared airspace picture across server restarts
  story: >
    Every once in a while, the server our platform runs on restarts or drops offline for several minutes while drones from multiple companies are flying through our corridors. When the server comes back up, I have to verify right away that every single active closure and corridor is restored exactly as it was before the blackout. I cannot have our shared safety map wipe clean or lose authority restrictions simply because the server rebooted.
  fear: >
    A rebooted system drops active authority closures, showing clear skies where hazardous temporary bans still exist and allowing flights into forbidden zones.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-37
  user: airspace desk
  title: recovering lost authority updates after platform downtime
  story: >
    If the airspace platform goes down for five minutes during a chaotic day, the authorities might issue an amendment or a brand-new restriction while we are completely blind. The moment connection is restored, I need to confirm whether any new regulatory notices arrived during our offline window. Knowing immediately what changed while we were dark is vital before telling operators that the map is current.
  fear: >
    We resume operations after a brief outage without realizing the authorities shut down a corridor while we were offline, leading to unlawful flights.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-38
  user: airspace desk
  title: conducting direct shift handovers within the airspace desk team
  story: >
    At the end of my shift, I hand over our active airspace picture directly to the desk specialist relieving me. We do not interface with the individual customer companies or their internal dispatchers; our focus is entirely on passing between ourselves the list of active authority closures, pending extensions, and sensitive zones. I need a seamless way to transfer this operational picture so the incoming specialist has total context without missing a beat.
  fear: >
    Critical verbal notes about an imminent authority closure extension are lost between shifts, leaving the new desk operator unprepared when the zone changes.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-39
  user: airspace desk
  title: preventing unwanted dashboard bloat and automatic alerting tools
  story: >
    I am terrified that a new service will try to build heavy analytical dashboards, automated alert popups, and complex business reporting into our workspace. Our job is strictly to keep the common airspace map accurate, clear, and fast; adding unnecessary analytical fluff only creates visual clutter and slows down our core map tools. I need the service to remain lean, focused, and free of extraneous features that our desk and our customers never asked for.
  fear: >
    Our workspace becomes bogged down with cluttered dashboards and distracting alerts, making it difficult to react swiftly when authorities order an emergency closure.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-40
  user: airspace desk
  title: preventing the platform from absorbing dispatch and route planning functions
  story: >
    There is a dangerous temptation for software designers to merge customer route planning and corporate user management directly into the airspace platform. We do not steer drones, we do not pick birds, and we do not manage our customers’ flight paths; we only maintain the shared sky map. I need the platform to stay out of route planning entirely so that our airspace picture remains an independent, reliable source of truth.
  fear: >
    The airspace tool gets bogged down trying to handle individual flight routes and logins, corrupting its role as the pure, authoritative map for the sky.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-41
  user: dispatcher
  title: receiving immediate airspace updates without relying on the airspace desk's manual pace
  story: >
    When I am managing live flights carrying temperature-sensitive medical supplies, I cannot wait around while an airspace desk operator manually calculates whether my route intersects a new closure. I need closure boundaries and corridor availability to reflect in my dispatch view the second the authorities issue them. Any delay between an authority announcement and my dispatch map puts my airborne drones in direct legal and physical jeopardy.
  fear: >
    My drones continue flying into an emergency zone for several minutes because the shared map was waiting on manual cross-customer disruption calculations.
  assumption: The dispatcher assumes that airspace updates can and should appear in flight dispatch systems immediately upon issuance by authorities.
  interview_ref: dispatcher, worst day

- id: US-42
  user: airspace desk
  title: keeping flight route control strictly out of the airspace desk's mandate
  story: >
    Customer dispatchers sometimes want us to tell them where to redirect their drones when a corridor closes, but that is completely outside our responsibilities. We provide the boundaries of where aircraft can and cannot fly; how each company re-routes their specific fleet around those boundaries is their legal and operational problem. I need the system to enforce this boundary so that the airspace desk is never dragged into managing individual flights or vehicle paths.
  fear: >
    The airspace desk is held accountable for a flight diversion that failed or resulted in a crash because the system blurred the line between map authority and flight control.
  assumption: The airspace desk assumes that dispatchers must independently solve all routing problems caused by airspace closures.
  interview_ref: airspace desk, ordinary day

- id: US-43
  user: fleet technician
  title: keeping maintenance and pad status independent from customer flight schedules
  story: >
    When a pad is damaged or caked in grime, I need to take it out of service immediately, regardless of what commercial deliveries dispatchers have scheduled for that location. Dispatchers are always focused on keeping their runs moving, but my job is keeping people and equipment safe from electrical fires and hardware failures. I need to be able to lock out a pad or drone in the registry without needing approval from flight dispatchers.
  fear: >
    A dispatcher overrides or delays my maintenance grounding to push through an urgent delivery, leading to hardware destruction or a physical accident on the pad.
  assumption: The fleet technician assumes technicians possess the unilateral authority to ground any pad or drone instantly for safety reasons.
  interview_ref: fleet technician, ordinary day

- id: US-44
  user: dispatcher
  title: knowing when a pad is pulled from service before planning a landing
  story: >
    I frequently dispatch flights to remote sites based on the assumption that the destination charging pad will be operational when the bird arrives twenty minutes later. If a technician locks out or disables a pad while my flight is already halfway there, my drone is suddenly left stranded in the air with nowhere to touch down. I need upfront visibility into technician maintenance holds so I never dispatch a bird toward a pad that is about to go dark.
  fear: >
    A drone arrives at its destination with low battery only to find the technician has taken the pad apart, forcing an off-field crash landing.
  assumption: The dispatcher assumes technicians sometimes disable pads without sufficient advance warning to active flight operations.
  interview_ref: dispatcher, ordinary day
```

---

### Questions for Users and Business Stakeholders

#### For Fleet Technicians & Maintenance Management
1. **Pad Lockout Protocol:** When you need to take a charging pad or drone out of service, what is the current rule or process for coordinating with flights already en route to that pad? Who has the ultimate authority if a drone with 5% battery is inbound to a pad you have just declared mechanically unsafe?
2. **Connector & Spare Management:** Exactly how many distinct connector types, charging wattages, and mechanical latching standards are currently deployed across the network? Are there plans to standardize these, or will the fleet continue to support heterogeneous hardware variants?
3. **Regulatory Records & Formats:** What exact data points and log formats do civil aviation regulators demand during an audit (e.g., technician license numbers, torque wrench calibration dates, specific battery cell telemetry, part serial swaps)?
4. **Physical Handoffs & Field Communication:** When you pull a bird from a pad and place it in your van, how do you currently record its physical location if radio links at that site are dead?
5. **Cold Weather Operations:** Do charging pads have built-in heating elements to prevent connector freezing, or is clearing ice and thermal management entirely a manual field technician task?

#### For Flight Dispatchers & Flight Operations Management
1. **Legal Responsibility and Automation Boundaries:** Regulations make the dispatcher legally responsible for flights. Where is the legal boundary regarding automated tools? Can a system suggest an optimized route or drone pairing as long as the dispatcher clicks "Approve", or is any algorithmic generation of flight paths considered unacceptable by policy or regulator standards?
2. **Pad Contention Resolution:** When two dispatchers attempt to reserve the same pad simultaneously at a high-demand hub, how is priority decided today (e.g., medical over parcel, first-come-first-served, remaining battery percentage)?
3. **Lost-Link Autopilot Behaviors:** When radio links fail completely and a drone cannot receive overrides during an airspace closure, what is the autopilot's programmed default behavior (e.g., hover in place, return to launch, land immediately on nearest terrain, or continue on old corridor)?
4. **Handover Between Shifts:** You noted that you do not perform formal handoffs between shifts. How are unresolved incidents, ongoing weather warnings, or pending maintenance issues communicated when one dispatcher steps away from the console?
5. **Battery Threshold Reserves:** What minimum reserve battery margin (in percentage or flight minutes) is legally mandated when signing off a flight under freezing or high-wind conditions?

#### For the Airspace Desk Team & Airspace Authority Liaisons
1. **Authority Communication Channels:** How do the aviation authorities transmit planned and sudden closures to your desk today (e.g., phone call, digital NOTAM feed, specialized government terminal, email)?
2. **Disruption Assessment Needs:** You mentioned needing to understand how much disruption a closure causes across customers, but you do not want dashboards or reports. Exactly what information do you need in that moment, and what action do you take once you know the disruption level?
3. **Customer Segregation:** Are customer fleets (hospital vs. parcel delivery) permitted to see each other's corridors and flight density on the shared map, or must each customer's active paths remain completely private and isolated from competitors?
4. **Server Recovery & Data Resynchronization:** When the airspace desk platform drops offline, is there an external secondary authority feed that records closures during the outage, or must the operator manually reconcile closures with the authorities upon reconnecting?
5. **Mandate Boundaries:** What is the exact organizational and contractual relationship between the airspace desk and the customer drone companies? Does the airspace desk have the authority to unilaterally forbid a launch, or does it strictly publish boundary data that customer dispatchers are obligated to obey?

#### For Platform Business Leadership & Product Owners
1. **Multi-Tenancy and Architecture:** Is this platform intended to be a multi-tenant common infrastructure shared across independent third-party drone operators (competing logistics firms, hospitals, regional operators), or is it an internal platform for one parent organization?
2. **Liability and Compliance:** If an airspace closure update is delayed or dropped due to network instability and a drone violates restricted airspace, where does the legal liability lie—with the software platform, the airspace desk, the operating company, or the individual licensed dispatcher?
3. **Connectivity Infrastructure:** Are there plans to upgrade the field communications infrastructure (e.g., multi-carrier satellite links, private cellular networks), or must the software platform assume that cellular and radio links will remain flaky and out-of-order indefinitely?
4. **Service Level Agreements (SLAs):** What are the business uptime and latency requirements for transmitting sudden emergency airspace closures to airborne vehicles?
5. **Scope Management:** Given the strong disagreement between the airspace desk (demanding a lean, map-only service without alerts or dashboards) and dispatchers/technicians (requiring detailed hardware statuses, conflict resolution, and regulatory records), will these user groups interact with completely distinct specialized applications built on a common core, or is a single unified application envisioned?
