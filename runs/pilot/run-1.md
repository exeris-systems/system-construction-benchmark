# Step 1 — Interviews

These are simulated discovery interviews based on the supplied description of the operating environment. The interviewer asks open questions and follows up when an answer is vague. The interviewees speak from the perspective of their jobs, not as software specialists.

Because no real users have been interviewed, the answers below are working hypotheses, not verified findings. Where the document does not establish a person's actual experience, the interview introduces a plausible scenario to explore and records assumptions in the resulting stories.

## Interview 1 — Fleet technician

Interview reference: fleet technician · ordinary day and worst day

Interviewer: Talk me through a normal working day, from when you arrive until you finish.

Fleet technician: I start by finding out what's happened since I left. Which drones came back, which ones are still out, which ones need charging, and whether anybody reported a fault. Then I check the charging pads and the drones that are due to go out. If a drone has been taken out of service, I need to know why before I decide what to do with it. During the day, I get new drones ready, deal with repairs, move drones onto charge, and put repaired ones back into service when I'm happy they're fit to fly.

Interviewer: You said you check what's happened since you left. How do you know the information is right?

Fleet technician: I don't always know. If the information says a drone has returned, I want to be sure it really has. A report can arrive late, or I might hear one thing from the system and something different from the person at the site. If a drone is supposed to be charging, I'll check the pad rather than trust a status that doesn't make sense.

Interviewer: What do you actually look at when you check a pad?

Fleet technician: Whether there's a drone there, whether it's connected properly, and whether it's charging. The connector matters because not every drone fits every pad. A pad can look fine but still not be doing its job. If I'm preparing a drone for service, I need confidence that it can get the charge it needs.

Interviewer: What happens when several things need your attention at once?

Fleet technician: I deal with anything that could leave someone with a drone they shouldn't use. Then I look at what else is needed to get the fleet ready. But it gets difficult when several people are asking whether particular drones are available. I don't want to tell someone a drone is ready when I'm still working on it.

Interviewer: How do you decide whether a drone is ready to go back into service after a repair?

Fleet technician: I need to know what was wrong, what was done about it, and whether the checks that matter have been completed. I don't want a fault to disappear from view just because somebody has changed the drone's status. If the same fault comes back, I need to be able to see what happened before.

Interviewer: What's the worst day you've had in the last few months?

Fleet technician: Imagine a busy day when several drones return around the same time, one needs a repair, and others are waiting for charge. At the same time, the information about a drone's return is late. People are asking for drones, but I can't tell which ones are genuinely ready. I end up checking things by hand while more work keeps arriving.

Interviewer: What makes that worse than simply having a lot of work?

Fleet technician: Not knowing what I can safely rely on. If I know three drones need repairs, I can plan around that. If I don't know whether a drone has returned, whether it's charging, or whether someone has already marked it ready, I waste time finding out. Worse, I might release a drone that isn't fit to fly.

Interviewer: What do you check manually because you don't trust the information?

Fleet technician: Whether the drone is actually at its home site, whether the pad is charging it, whether the equipment fits together, and whether the repair history matches what's been done. I also want to know whether someone else has already taken action. I don't want to do the same thing twice or undo someone else's work.

Interviewer: Why is repeating an action a concern?

Fleet technician: Because I might send a drone to charge and the instruction could go through twice. Or I might think an earlier instruction failed and try again. I need to know what really happened, not just what I tried to do. If the drone starts charging twice in the records but is physically sitting on one pad, the records are no help to me.

Interviewer: What would you be most worried about if a new service were introduced?

Fleet technician: That it would show a drone as ready when it wasn't, or show a repair as finished when it wasn't. I would also worry about losing the history when something is taken out of service and put back. I don't want someone else's decision to make a drone available without my knowing what's happened to it.

Interviewer: What if the service goes down while drones are flying?

Fleet technician: I can live with a short interruption if I know where things stand when it comes back. I don't want to find that actions I made before the interruption have vanished, or that the same action has happened twice. If I can't tell which records are current, I'll have to check everything again.

Interviewer: Suppose a drone reports a fault, then later reports that it's working again. What would you need to know?

Fleet technician: What the fault was, when it happened, whether the drone restarted, and whether it really continued working. I wouldn't assume that a later report means the original problem has gone away. I'd want to know whether anyone has checked it and whether it's still out of service.

Interviewer: What do you need to know immediately when something goes wrong?

Fleet technician: Which drone or pad is involved, where it is, what happened, and whether anyone is relying on it being available. I need to know whether it's a new problem or one we've already dealt with. If a drone is out of service, I need dispatch to stop treating it as an option.

Interviewer: Who hands work to you, and who do you hand it to?

Fleet technician: Dispatch tells me when a drone is needed and when equipment is causing a problem for the day's work. I take care of the equipment and tell dispatch when a drone is unavailable or fit to return to service. Other technicians may hand repairs to me, and I may hand a difficult repair to someone with the right experience. The important thing is that the next person knows what has been done and what still needs doing.

Interviewer: Does dispatch always agree with your view of what's urgent?

Fleet technician: Not necessarily. Dispatch wants a drone for a job that's waiting. I want to be sure the drone is safe and ready. A flight being late doesn't make a faulty drone fit to fly.

Interviewer: Is there anything else that would make your day easier?

Fleet technician: Knowing what's genuinely ready, what's being repaired, what's charging, and what still needs checking. And when a problem happens, I want the history to tell the same story as the equipment in front of me.

## Interview 2 — Dispatcher

Interview reference: dispatcher · ordinary day and worst day

Interviewer: Talk me through your working day from start to finish.

Dispatcher: I start by looking at the jobs that need to be flown, the drones we have available, and the sites we'll be using. I need to understand which deliveries are ready, which inspections have to visit a set of points, and what the day's priorities are. For each flight, I decide which drone is suitable and which corridor it should use. I sign off the flight before it leaves, and I'm responsible for that decision.

Interviewer: What makes a drone suitable for a particular job?

Dispatcher: The distance, the load, the battery, and the equipment on the drone. An inspection may need a particular camera or scanner. The drone also has to be able to get to the place where the job starts. I don't want to spend time considering drones that can't do the job in the first place.

Interviewer: What do you do when you have several jobs waiting?

Dispatcher: I work out which ones are ready to go and which drones could do them. I have to consider the corridors and whether the sites can handle the take-offs and landings. Then I make the decisions and sign off the flights. It's my decision, not the system's.

Interviewer: What happens when another dispatcher is working on the same site or wants the same drone?

Dispatcher: We can get in each other's way. I might be preparing a flight with a drone I believe is available, while another dispatcher is planning something with it too. A site might also have all its landing places spoken for. If I don't know what has changed, I can make a plan that can't actually be carried out.

Interviewer: How do you know a drone is really available?

Dispatcher: I check its status, and if something doesn't add up, I ask the technician or check the latest information. A drone might have returned but need charging. It might be marked available while a repair is still in progress. Or it might be out flying, but the last report hasn't arrived yet.

Interviewer: What about a job that's waiting for its load?

Dispatcher: That's another thing I have to keep track of. A drone may be ready and the route may be suitable, but the load might not be. I don't want to treat a job as ready just because the drone is ready. The people handling the load have their own work, and their updates may arrive late.

Interviewer: What's the worst day you've had in the last few months?

Dispatcher: Picture a busy day with several flights due to leave, two dispatchers looking at the same popular drones, and a closure announced while drones are already in the air. The closure is then changed, perhaps widened or given a different end time. At the same time, a drone's last report is late, so I don't know whether it's where I expect it to be. I have to work out what I can still fly, what needs attention, and what I must not sign off.

Interviewer: What makes that situation particularly difficult?

Dispatcher: I have legal responsibility for the flight, but the information I need can be incomplete or out of date. I can't assume a drone is safely back just because an old report says so. And I can't assume that a corridor is available just because it was available when I started planning. I need to make a sound decision based on what is known now, while understanding what is still uncertain.

Interviewer: What do you check by hand because you don't trust the information?

Dispatcher: Whether the drone is actually available, whether the load is ready, whether the corridor is open, whether the site can accommodate the flight, and whether another dispatcher has already committed the drone or a take-off place. If a report looks odd, I compare it with what I know from the people on the ground.

Interviewer: You mentioned a drone that hasn't reported in. What would you do?

Dispatcher: I wouldn't treat silence as proof that the drone has stopped or landed. It might still be flying, or it might have restarted and continued. I'd need to know its last reliable position and what had happened since. I would be concerned about committing another flight on the assumption that the drone had returned.

Interviewer: What would you fear most about a new service?

Dispatcher: That it would make a decision look safer or more certain than it really is. I don't want it choosing the drone or the route for me. I want help understanding the choices, but I remain responsible for what I sign off. I also don't want a closure change or a late report to disappear behind an apparently normal status.

Interviewer: What if the service is restarted during working hours?

Dispatcher: A short interruption is manageable. What isn't manageable is not knowing whether the flight information is current when it returns. If I signed something off, I need to know whether that happened. If a drone's status changed during the interruption, I need to know what is true now, rather than be shown an old picture as if nothing happened.

Interviewer: What do you need to know right after something goes wrong?

Dispatcher: Which flight or drone is involved, its last reliable location, what the problem is, and when that information was reported. I need to know whether the corridor or site is affected, whether other flights might be affected, and whether a closure has changed since the flight was approved. I also need to know what remains unknown, because that affects the decision I make next.

Interviewer: Who hands work to you, and who do you hand it to?

Dispatcher: Customers or the people organising the work tell us what needs to be carried or inspected. The people preparing the loads tell us when they're ready. Technicians tell us whether a drone is fit to fly. I make the flight decisions, sign off, and monitor what happens. If equipment needs attention, I hand that back to the technicians; if the job can't go ahead, the people waiting for it need to know through our company's own arrangements.

Interviewer: Do technicians and dispatchers always agree about when a drone is ready?

Dispatcher: No. I might have a delivery waiting and see a drone that looks suitable. The technician might know it's still being checked or that a fault hasn't been resolved. I need their information to be clear, but I can't take the risk of assuming a drone is ready simply because I need it.

Interviewer: What would make an ordinary day easier?

Dispatcher: Knowing which drones could do the work, without the service deciding for me. Knowing whether jobs are actually ready, whether sites have room, and whether other dispatchers have already taken the options I was considering. And when something changes, I need to understand the effect on my decisions, not just see a new status.

## Interview 3 — Airspace desk

Interview reference: airspace desk · ordinary day and worst day

Interviewer: Talk me through a normal working day at the airspace desk.

Airspace desk: We maintain the shared picture of the airspace: the corridors between sites, the zones they belong to, and the closures announced by the authorities. We enter the information that applies to everyone using the service. We need to be able to distinguish planned closures from sudden ones, and we need to keep the information current when the authorities amend it.

Interviewer: What does an amendment look like in practice?

Airspace desk: A closure might cover a larger area than first announced, or its end time might change. We need to make sure the shared picture reflects the current announcement. It isn't enough to know that a closure was entered earlier. We need to know what is in force now and what has changed.

Interviewer: How do you know the information is correct?

Airspace desk: We rely on the information announced by the authorities, but we need to be careful when entering it. If something is unclear, we need to resolve that before we treat it as settled. I would also want to see what we have entered already, so we don't accidentally leave an earlier version in place.

Interviewer: What do you do when a new closure comes in while drones are flying?

Airspace desk: We enter the closure as required, but the consequences can extend beyond the desk. Several operating companies might have drones in the affected area or be preparing flights through it. The companies have their own responsibilities for their operations. We need the shared airspace information to be accurate, and we need to understand how much disruption the closure caused across the service.

Interviewer: How would you describe a bad day?

Airspace desk: A sudden closure comes in during a busy period, then the authority changes it again. We are trying to keep the shared picture correct while the operating companies are using it. If the service is interrupted or an update is duplicated, we could be unsure whether the latest change is reflected everywhere. We also need to understand the effect on operations without looking into one company's business.

Interviewer: Why is that boundary important?

Airspace desk: We work for the platform, not for any one operator. Each company has its own fleet, jobs, sites and clients. We don't need to know what a parcel company is delivering or which infrastructure asset another company is inspecting. We need to maintain the shared airspace picture and understand the overall disruption caused by a closure.

Interviewer: What do you check by hand because you don't trust the information?

Airspace desk: I would check the authority's announcement against the closure entered into the shared picture. I'd check whether the start and end times are correct, whether the affected area is right, and whether an amendment has replaced the earlier information rather than being treated as a separate, unrelated closure. If the system had been interrupted, I'd want to establish what was actually saved.

Interviewer: What would you be afraid a new service might get wrong?

Airspace desk: It might show an old closure as current, miss an amendment, or make a sudden closure appear to start later than it should. It could also confuse a corridor or zone, which would affect everyone relying on the shared picture. And I would worry about being shown details of a customer's business that we have no reason to see.

Interviewer: Suppose the service crashes while you are entering a closure. What would you need to know when it comes back?

Airspace desk: Whether the closure was saved, whether it was saved correctly, and whether the current picture matches the authority's announcement. I don't want to enter it again without knowing what happened the first time. That could leave duplicate or conflicting information. I'd also need to know whether other changes made around the same time are still there.

Interviewer: What do you need to know immediately after a closure has caused disruption?

Airspace desk: Which closure caused it, when it took effect, what area it covered, and how its terms changed. I need an overall picture of the effect across the operators, so we can understand the scale of disruption. But I don't need to inspect a particular company's individual jobs or commercial activity to do that.

Interviewer: How much detail about the disruption do you need?

Airspace desk: Enough to understand whether the closure affected a small part of the network or a substantial part of it, and whether an amendment changed the impact. I'd want to distinguish a flight that was already in the air from one that had not yet left, if that distinction is available. But I wouldn't want to turn this into a report about individual companies' performance.

Interviewer: Who hands work to you, and who do you hand it to?

Airspace desk: The authorities provide the closure information, and we maintain the shared picture. The operating companies rely on that picture for their own decisions. When we enter or amend a closure, we need the information to be available to them. If the information from an authority is unclear, we'd need to resolve it with the appropriate source rather than guess.

Interviewer: Do you ever need to know which operator was responsible for a particular flight?

Airspace desk: Not for the ordinary task of maintaining shared airspace information. We may need to understand the combined disruption, but that doesn't mean we should have access to the individual operator's fleet or jobs. The boundary should be clear.

Interviewer: What would make your ordinary day easier?

Airspace desk: Confidence that the shared picture reflects the latest authority information, and that amendments and sudden closures are handled correctly. I also need to know the overall disruption closures cause. And I need to do that without becoming a back door into the customers' operations.

# Step 2 — User stories

The following 45 stories are derived from the simulated interviews and the supplied operating context. They cover ordinary operations, faults, uncertainty, shared resources, airspace changes, interruptions, handovers and disagreements between roles.

The stories deliberately avoid prescribing screens, internal mechanisms or automated decisions. Each story describes a situation, a need and the consequence the user fears. Assumptions are marked explicitly rather than presented as established facts.

```
- id: US-01
  user: fleet technician
  title: Knowing what came back
  story: >
    When I start my day, I need to know which drones have actually
    returned to their home sites since I last checked. A late report
    should not make me believe a drone is still away when it has
    returned, or that it is home when it is still flying. I need to
    know what I can rely on before I start preparing equipment.
  fear: >
    I waste time searching for drones or make equipment available
    when it is still being used.
  assumption: >
    The service can receive reports about drone returns and identify
    each drone's home site.
  interview_ref: fleet technician, ordinary day

- id: US-02
  user: fleet technician
  title: Knowing what is really ready
  story: >
    When dispatch asks for a drone, I need to know whether it is
    genuinely ready to fly, not just whether somebody has marked it
    as available. A drone waiting for a repair or an important check
    must not look the same as one that is ready. I need dispatch to
    understand the difference so nobody relies on equipment that
    still needs my attention.
  fear: >
    A drone that is not fit to fly gets used because its recorded
    status looks reassuring.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-03
  user: fleet technician
  title: Finding the right charger
  story: >
    When I need to charge a drone, I need to know which of our pads
    can actually charge it. Different drones use different
    connectors, and the equipment at one of our sites cannot simply
    be borrowed from another company. I need to avoid wasting time
    moving equipment to a pad that cannot be used.
  fear: >
    A drone misses its next job while people discover too late that
    the available charging equipment does not fit.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-04
  user: fleet technician
  title: Seeing what still needs charging
  story: >
    When several drones return together, I need to know which ones
    still need charging and which ones are already charging. I also
    need to distinguish a drone that has been told to charge from
    one that is actually receiving charge. Otherwise I cannot tell
    which equipment will be ready when dispatch needs it.
  fear: >
    I promise a drone that will not have enough charge for its
    intended work.
  assumption: >
    The service can receive information about charging activity
    from the company's equipment.
  interview_ref: fleet technician, ordinary day

- id: US-05
  user: fleet technician
  title: Keeping a repair's history
  story: >
    When I take a drone out of service, I need to understand why it
    was removed and what has happened to it since. When I put it
    back into service, I need the earlier fault and repair work to
    remain part of its history. I may need that history when the
    same problem appears again or someone asks how the drone was
    looked after.
  fear: >
    Important repair work disappears from view, leaving me unable to
    explain the drone's condition or repeated faults.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-06
  user: fleet technician
  title: Bringing a new drone into the fleet
  story: >
    When we receive a new drone, I need to establish what it can do
    and which of our sites and charging pads suit it. I need its
    carrying ability, flying range, sensors and charging connector
    to be understood before dispatch relies on it. A new drone
    should not be treated like another model just because it looks
    similar.
  fear: >
    Dispatch considers a drone for work it cannot perform or sends
    it somewhere it cannot be charged.
  assumption: >
    The service is expected to hold the equipment details needed
    for day-to-day fleet operations.
  interview_ref: fleet technician, ordinary day

- id: US-07
  user: fleet technician
  title: Retiring a drone properly
  story: >
    When a drone leaves our fleet permanently, I need that to be
    clear to everyone who relies on the fleet information. Its
    earlier repairs and service history still matter, even though
    it should no longer be considered for work. I need to distinguish
    a retired drone from one that is temporarily unavailable.
  fear: >
    Dispatch chooses equipment we no longer operate, or useful
    maintenance history is lost when the drone leaves the fleet.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-08
  user: fleet technician
  title: Trusting a repair handover
  story: >
    When another technician hands me a repair, I need to know what
    failed, what they have already checked, and what remains to be
    done. If I have to repeat the work just to understand its
    history, I lose time that could be spent getting other drones
    ready. I need the next person to understand the condition of the
    equipment without guessing.
  fear: >
    A fault is missed, the same work is repeated unnecessarily, or
    an unfinished repair is mistaken for a completed one.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-09
  user: fleet technician
  title: Dealing with several returns at once
  story: >
    When several drones return while other equipment needs repairs,
    I need to understand which drones need attention and which can
    be left alone. I cannot physically check every drone at every
    moment. I need the information I receive to help me concentrate
    on the equipment that actually needs my attention.
  fear: >
    An important fault is overlooked while I spend time checking
    equipment that is already in good condition.
  assumption: >
    The service can present recent equipment reports in a way that
    helps distinguish unresolved problems from routine activity.
  interview_ref: fleet technician, worst day

- id: US-10
  user: fleet technician
  title: Knowing whether an instruction worked
  story: >
    When I ask a drone or charging pad to do something, I need to
    know whether it actually happened. If I cannot tell whether my
    first attempt got through, I need to avoid mistaking a repeated
    instruction for a successful outcome. I care about the equipment's
    real condition, not just what I tried to make it do.
  fear: >
    Equipment receives conflicting or repeated instructions, or I
    believe a task is complete when nothing has happened.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-11
  user: fleet technician
  title: Understanding a fault after a restart
  story: >
    When a drone reports a fault and later starts reporting again,
    I need to understand what happened before deciding it is fit
    for service. A fresh report does not prove that the original
    problem has gone away. I need to know whether the drone has been
    checked and whether the fault remains unresolved.
  fear: >
    A drone with a continuing fault returns to service simply
    because it has started reporting normally again.
  assumption: >
    Reports can identify a restart and provide enough history to
    distinguish it from an ordinary return to service.
  interview_ref: fleet technician, worst day

- id: US-12
  user: fleet technician
  title: Recovering after an interruption
  story: >
    When the service is interrupted during the working day, I need
    to know which equipment records and actions are still reliable
    when it becomes available again. I cannot assume that an
    instruction failed just because I did not see a response. I
    need to avoid repeating work or treating old information as
    current.
  fear: >
    I duplicate actions, lose track of equipment, or release a drone
    based on an outdated picture of its condition.
  assumption: null
  interview_ref: fleet technician, worst day

- id: US-13
  user: fleet technician
  title: Knowing what happened before a fault
  story: >
    When a drone develops a fault, I need to know its recent
    condition and the events leading up to the problem. If the
    same fault has happened before, I need to recognise that
    rather than treat it as something entirely new. This helps me
    understand the work still needed before the drone is fit to fly.
  fear: >
    A recurring problem is missed and the drone returns to service
    without the underlying issue being understood.
  assumption: >
    Relevant equipment reports and earlier repair records are
    available to the service.
  interview_ref: fleet technician, worst day

- id: US-14
  user: fleet technician
  title: Making the equipment handover clear
  story: >
    When I finish work on a drone, I need dispatch to understand
    whether it is ready, still being checked, or remains out of
    service. I need that understanding to match what I have actually
    done. Dispatch can be under pressure to start a flight, but
    that pressure must not make unfinished work look complete.
  fear: >
    Dispatch relies on a drone before I have finished the work
    needed to make it fit for service.
  assumption: null
  interview_ref: fleet technician, ordinary day

- id: US-15
  user: dispatcher
  title: Finding drones that could do the job
  story: >
    When a job comes in, I need to know which of our drones could
    reach its starting site and carry out the work. The drone must
    have the right range, carrying ability and equipment for the
    job. I want useful choices to consider, but I must make the
    decision about which drone to fly.
  fear: >
    I waste time considering unsuitable drones or rely on a choice
    that does not meet the needs of the job.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-16
  user: dispatcher
  title: Keeping the flight decision mine
  story: >
    When I prepare a flight, I need to judge the drone and corridor
    myself. I am responsible for signing off the flight, so I need
    to understand the information behind my decision. I want help
    finding out what may be possible without having a service make
    the choice for me.
  fear: >
    A flight is treated as suitable because the service made a
    choice that I am legally responsible for.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-17
  user: dispatcher
  title: Knowing whether a job is ready
  story: >
    When I have a delivery waiting, I need to know whether its load
    is actually ready to go. A suitable drone and an open corridor
    do not mean the delivery itself is ready. I need to understand
    what is holding up the job before deciding what work can go
    ahead.
  fear: >
    I prepare or release a flight for a job that cannot yet be
    carried out.
  assumption: >
    Information about load readiness is available from people or
    systems outside the service.
  interview_ref: dispatcher, ordinary day

- id: US-18
  user: dispatcher
  title: Knowing whether an inspection can be completed
  story: >
    When I plan an inspection, I need to know whether a suitable
    drone can visit the required points in the required order and
    return to where the inspection started. The drone needs the
    right sensors as well as enough range for the work. I need to
    understand whether the job is feasible before I take
    responsibility for the flight.
  fear: >
    I sign off a flight that cannot complete the inspection as
    required or return to its starting site.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-19
  user: dispatcher
  title: Avoiding a crowded site
  story: >
    When several flights are planned around the same site, I need
    to know whether there will be room for my take-off or landing.
    A drone may be suitable and a corridor may be open, but the
    site may already be committed to other flights. I need to make
    a plan that can actually be carried out alongside my colleagues'
    plans.
  fear: >
    Flights are committed to a site that cannot handle them at the
    required time.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-20
  user: dispatcher
  title: Knowing another dispatcher has the drone
  story: >
    When several of us are planning at once, I need to know whether
    another dispatcher is already relying on the drone I want to
    use. Seeing a drone as available is not enough if a colleague
    has already committed it to a flight. I need to understand what
    is genuinely available before I sign off my own decision.
  fear: >
    Two flights rely on the same drone and one cannot go ahead as
    planned.
  assumption: >
    The service is expected to represent competing plans or
    commitments before a flight departs.
  interview_ref: dispatcher, ordinary day

- id: US-21
  user: dispatcher
  title: Knowing when a flight has actually left
  story: >
    When a flight is due to depart, I need to know whether the drone
    has actually left or is still waiting at the site. I cannot
    rely on an earlier instruction as proof that the flight began.
    The difference matters when I decide what other work can be
    prepared around the same drone and site.
  fear: >
    I treat a flight as underway when it has not started, or plan
    other work around a drone that has already departed.
  assumption: >
    Departure reports can be received from sources outside the
    service.
  interview_ref: dispatcher, ordinary day

- id: US-22
  user: dispatcher
  title: Knowing when a delivery arrived
  story: >
    When a delivery is underway, I need to know whether it reached
    its destination. A drone's last report or an instruction to
    depart does not prove that the load arrived. I need to
    understand what happened to the job before I treat it as
    complete or plan the next work around it.
  fear: >
    A delivery is treated as completed even though the load has
    not arrived or its arrival is still uncertain.
  assumption: >
    The service can receive delivery progress and arrival reports.
  interview_ref: dispatcher, ordinary day

- id: US-23
  user: dispatcher
  title: Knowing whether a drone is really back
  story: >
    When a flight should have finished, I need to know whether the
    drone has actually returned. A report may arrive late, twice,
    or out of order, so I cannot assume the latest message tells
    the whole story. I need to understand the drone's situation
    before relying on it for another job.
  fear: >
    I commit a drone to new work while it is still flying or
    mistakenly treat an unfinished flight as complete.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-24
  user: dispatcher
  title: Understanding a missing report
  story: >
    When a drone stops reporting during a flight, I need to know
    what was last reliably known about its position and condition.
    Silence does not tell me whether it has landed, stopped, or
    continued flying after a restart. I need to recognise the
    uncertainty before making decisions that depend on the drone.
  fear: >
    I make a flight decision based on an assumed location or
    condition that is no longer true.
  assumption: >
    The service receives enough information to distinguish the
    time of an event from the time its report arrives.
  interview_ref: dispatcher, worst day

- id: US-25
  user: dispatcher
  title: Understanding a sudden closure
  story: >
    When the authorities announce a sudden closure, I need to
    understand whether it affects a flight I am preparing or a
    drone that is already in the air. I need to know what part of
    the shared airspace picture has changed and what remains
    uncertain. I must make my own operational decisions using the
    current information.
  fear: >
    I sign off or continue relying on a flight plan that is
    affected by a closure I have not properly understood.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-26
  user: dispatcher
  title: Keeping up with an amended closure
  story: >
    When a closure is widened or its end time changes, I need to
    understand what is different from the information I relied on
    earlier. A plan that appeared suitable before the amendment
    may no longer be suitable. I need to recognise the change
    before I make or continue relying on a flight decision.
  fear: >
    I act on the earlier version of a closure and overlook a
    change that affects the flight.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-27
  user: dispatcher
  title: Knowing what is still uncertain
  story: >
    When reports disagree, I need to know which facts are
    dependable and which remain uncertain. I cannot assume that a
    newer-arriving report describes a later event. I need enough
    context to make a responsible decision without pretending I
    know more than the available information supports.
  fear: >
    I mistake delayed or repeated information for a confirmed
    change in a drone's situation.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-28
  user: dispatcher
  title: Understanding a battery that drains faster
  story: >
    When cold or wind reduces how far a drone can fly on its
    battery, I need to understand whether it can still do the job
    I am considering. Its usual range alone may not be enough to
    judge the flight. I need to make my own decision with a
    realistic understanding of the drone's condition.
  fear: >
    I sign off a flight that the drone cannot complete safely
    with the battery available.
  assumption: >
    The service can receive sufficiently current information about
    battery condition or remaining charge.
  interview_ref: dispatcher, ordinary day

- id: US-29
  user: dispatcher
  title: Knowing what happened after a fault
  story: >
    When a drone reports a fault during a flight, I need to know
    where it was last reliably reported and what happened
    afterwards. If it restarts and continues, I need to
    distinguish that from a confirmed safe return. I need to
    understand the uncertainty before deciding what other flights
    can proceed.
  fear: >
    I assume the drone has finished its flight or is safe to reuse
    when its condition is not known.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-30
  user: dispatcher
  title: Knowing what survived an interruption
  story: >
    When the service stops during the working day, I need to know
    which flight decisions and updates still reflect what actually
    happened. I need to distinguish an action I attempted from an
    action that took effect. When the service returns, I need
    enough confidence in the information to resume my work
    without making unsafe assumptions.
  fear: >
    I rely on missing or outdated information when signing off a
    flight or deciding what can happen next.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-31
  user: dispatcher
  title: Knowing when a flight was called off
  story: >
    When I call off a flight, I need to understand whether it has
    actually been stopped from proceeding or whether the drone may
    still depart. I need to know what has happened rather than
    assume my decision reached the equipment. This matters
    especially when reports or instructions are delayed.
  fear: >
    I believe a flight has been called off while the drone
    proceeds as though it were still authorised to depart.
  assumption: >
    Calling off a flight may involve an instruction whose receipt
    cannot always be confirmed immediately.
  interview_ref: dispatcher, worst day

- id: US-32
  user: dispatcher
  title: Handing a fault back to the technician
  story: >
    When equipment prevents a flight from going ahead, I need to
    hand the problem to the technician with enough context to
    understand which drone is affected and why I cannot rely on it.
    When the technician has finished, I need to know whether the
    drone is actually fit for service. I should not have to guess
    whether a repair is complete.
  fear: >
    A drone remains unavailable without anyone understanding why,
    or returns to flight before the fault has been resolved.
  assumption: null
  interview_ref: dispatcher, ordinary day

- id: US-33
  user: airspace desk
  title: Keeping the shared airspace picture current
  story: >
    When the authorities publish new airspace information, I need
    the shared picture to reflect what they have announced. The
    operating companies rely on the same corridors, zones and
    closures, so the information must not differ simply because
    the companies run separate businesses. I need to be confident
    that everyone is relying on the current shared picture.
  fear: >
    Different operators rely on outdated or conflicting airspace
    information.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-34
  user: airspace desk
  title: Entering a planned closure correctly
  story: >
    When an authority announces a planned closure, I need to
    understand its affected area and when it starts and ends.
    Operating companies need to know when the closure applies,
    not merely that it exists. I need the shared information to
    match the announcement so that operators can make their own
    decisions.
  fear: >
    Operators plan flights using incorrect closure times or an
    incorrect understanding of the affected area.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-35
  user: airspace desk
  title: Replacing an earlier closure with an amendment
  story: >
    When an authority changes a closure's area or end time, I need
    the current picture to reflect the amendment without losing
    track of what was previously announced. I need to understand
    which terms are now in force. The companies should not have to
    guess whether an earlier version still applies.
  fear: >
    An outdated closure remains in use, or conflicting versions
    leave operators unsure which information is current.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-36
  user: airspace desk
  title: Recording a sudden closure
  story: >
    When an authority announces a closure that applies at once, I
    need its immediate effect to be represented accurately. I
    cannot treat it like an ordinary future closure if that would
    misrepresent when it takes effect. I need the shared picture
    to reflect the announcement without inventing a delay.
  fear: >
    Operators rely on an apparently open area after a closure has
    already come into force.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-37
  user: airspace desk
  title: Knowing whether a closure was saved
  story: >
    When I enter a closure and the service stops responding, I
    need to know whether the information was actually saved.
    I need to avoid entering it again blindly, because the first
    attempt may already have taken effect. Once I can continue
    working, I need confidence that the shared picture matches
    the authority's announcement.
  fear: >
    The closure is missing, entered twice, or represented by
    conflicting information.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-38
  user: airspace desk
  title: Understanding the disruption a closure caused
  story: >
    When a closure affects the network, I need to understand how
    much disruption it caused across the operating companies.
    I need to distinguish a closure's wider effect from the details
    of any one company's business. This helps me understand the
    consequences of the shared airspace change without taking
    responsibility for the operators' decisions.
  fear: >
    I cannot tell whether a closure caused substantial disruption
    or understand its overall effect on the service.
  assumption: >
    The service can determine or receive operational impact
    information at an overall level without exposing individual
    companies' commercially sensitive details.
  interview_ref: airspace desk, worst day

- id: US-39
  user: airspace desk
  title: Understanding the effect of a changing closure
  story: >
    When a closure is amended during the day, I need to understand
    whether the change made its impact greater or smaller. A wider
    area or a later end time may affect the network differently
    from the original announcement. I need to understand the
    change's consequences without turning the shared picture into
    a review of individual companies.
  fear: >
    I misunderstand the overall disruption because I cannot
    distinguish the effect of the amendment from the original
    closure.
  assumption: >
    The service can relate operational impact to the different
    versions of an authority's closure.
  interview_ref: airspace desk, worst day

- id: US-40
  user: airspace desk
  title: Respecting the boundary between companies
  story: >
    When I maintain shared airspace information, I need to see
    what is necessary to do that work without looking into each
    company's fleet, jobs or clients. The operators have separate
    business interests, even though they use the same airspace
    information. I need to understand the shared network without
    being given access to information that is not mine to see.
  fear: >
    The platform becomes a way to expose one customer's
    commercially sensitive operations to another part of the
    business.
  assumption: null
  interview_ref: airspace desk, ordinary day

- id: US-41
  user: airspace desk
  title: Knowing which information came from the authority
  story: >
    When I maintain a closure, I need to distinguish the
    authority's announcement from the information we have entered
    into the shared picture. If somebody questions the current
    closure, I need to understand what announcement it was based
    on. I should not have to rely on memory to explain why the
    shared picture says what it says.
  fear: >
    An incorrect entry goes unnoticed because nobody can establish
    which authority information it was meant to represent.
  assumption: >
    The authority's original announcements can be identified or
    referenced outside the service.
  interview_ref: airspace desk, ordinary day

- id: US-42
  user: airspace desk
  title: Knowing what changed during an interruption
  story: >
    When the service is restarted while we are working, I need
    to know whether the closure information I entered is still
    current and whether any changes were lost. I need to resume
    from a trustworthy picture rather than repeat everything I
    did before the interruption. The shared airspace information
    must not silently fall behind the authorities' announcements.
  fear: >
    Operators rely on an old airspace picture because a change
    was lost or its status is uncertain.
  assumption: null
  interview_ref: airspace desk, worst day

- id: US-43
  user: airspace desk
  title: Keeping the network understandable
  story: >
    When a corridor or zone changes, I need to understand how the
    change relates to the rest of the shared airspace picture.
    The operating companies need the network to remain consistent
    enough for them to understand where flights may be affected.
    I need to avoid creating gaps or contradictions when keeping
    the shared information current.
  fear: >
    A change leaves the network inconsistent and causes operators
    to misunderstand which corridors or areas are affected.
  assumption: >
    The service represents relationships between corridors, sites,
    zones and closures.
  interview_ref: airspace desk, ordinary day

- id: US-44
  user: dispatcher
  title: Knowing when the drone's situation has changed
  story: >
    When reports arrive late or out of order, I need to understand
    what actually happened to the drone and when it happened.
    A message arriving now may describe something that happened
    earlier, and repeated reports may describe the same event.
    I need to avoid treating the arrival of a report as proof that
    the drone has just changed state.
  fear: >
    I make an operational decision using a misleading sequence
    of events and misunderstand the drone's current situation.
  assumption: null
  interview_ref: dispatcher, worst day

- id: US-45
  user: fleet technician
  title: Keeping ownership of my company's equipment
  story: >
    When I manage our fleet, I need to know that the drones,
    charging pads, repairs and equipment records belong to our
    company. Another operator may use the same shared service,
    but that does not make our equipment available to them.
    I need to manage our equipment without accidentally changing
    another company's records or having them change ours.
  fear: >
    Equipment is treated as shared when it is privately owned,
    or one company's work interferes with another company's fleet.
  assumption: null
  interview_ref: fleet technician, ordinary day
```

# Questions for the document authors

These questions should be answered before the stories are treated as agreed requirements. They target gaps, ambiguities and assumptions in the supplied description rather than proposing a design.

## A. Business boundaries and ownership

1. What exactly counts as a separate operating company within the platform, and can one organisation operate more than one fleet?
2. Can a person work for more than one operating company, or can staff ever change companies while retaining access?
3. What information is each operating company allowed to see about its own equipment, jobs, sites and flights?
4. Is any operational information about one company ever visible to another company, beyond the shared airspace picture?
5. What does the airspace desk need to know about disruption, and what information would cross the line into commercially sensitive operational data?
6. Are there circumstances in which the airspace desk must identify an affected operator, rather than see only an overall impact?
7. Who decides what information the platform company's staff are permitted to see?
8. Does the platform company itself operate drones, or does it exclusively provide the shared service?

## B. Fleet technicians and equipment

9. What information must a technician record when adding a drone, and which details come from the manufacturer?
10. Which equipment characteristics determine whether a drone is suitable for a particular delivery or inspection?
11. How is a drone's home site chosen, and can it change during ordinary operations?
12. Can a drone be temporarily assigned to a different site, and what happens to its home-site designation?
13. What exactly makes a drone available, unavailable, under repair, awaiting inspection or retired?
14. Who is allowed to change a drone's operational status, and can dispatchers override a technician's decision?
15. Can a drone have several faults or repairs in progress at the same time?
16. What maintenance and servicing history must be available when a regulator asks the operator how a drone was looked after?
17. Are repair records expected to include the person who performed the work, the checks performed, the outcome and the time of each event?
18. What happens when a technician discovers that a repair record is incomplete or incorrect?
19. Can a technician return a drone to service without completing every check, and who is authorised to make that decision?
20. How are charging pads installed, commissioned, moved, maintained and retired?
21. What does the company need to know about a pad that is powered on but cannot charge a drone?
22. How is charging readiness determined, and can the service obtain reliable information about actual battery charge?
23. What happens when a drone's battery is degraded, or its actual flying range differs from the manufacturer's stated range?
24. What happens when a drone or pad is physically present but cannot be reached through the available communications link?

## C. Dispatchers and jobs

25. What information must be available before a delivery or inspection can be considered ready for planning?
26. Who creates jobs, and can a job be changed, postponed, cancelled or divided after planning has started?
27. What distinguishes a job being prepared, a flight being approved, a flight being underway and a job being completed?
28. What is the precise relationship between a job, a flight and a drone? Can one job require multiple flights, or can one flight carry out more than one job?
29. For deliveries, what does it mean for a load to be ready, collected, delivered or unsuccessfully delivered?
30. For inspections, how are the required points and their order defined, and what happens if one point cannot be visited?
31. Must an inspection always return to its starting site, even when something goes wrong during the flight?
32. How should dispatchers understand which drones could perform a job without the service selecting a drone or route for them?
33. Which factors must dispatchers consider when judging a drone's suitability beyond range, payload and sensors?
34. Who decides whether a particular corridor is suitable for a flight, and what information do they need to make that decision?
35. How are take-off and landing places at a site allocated, and what happens if several dispatchers want the same place?
36. When two dispatchers plan work using the same drone, who has priority if their plans conflict?
37. Can a dispatcher change a plan after signing off a flight, and what additional decisions are required?
38. What does calling off a flight mean at each stage: before departure, during departure, while airborne and after arrival?
39. What does the dispatcher need to know when a drone fails to report for an extended period?
40. Who is responsible for deciding what to do when a drone's position or condition cannot be established confidently?
41. What happens if a drone restarts in flight and continues its work without a person immediately noticing?
42. What is expected when actual battery consumption makes a previously feasible flight questionable?
43. What must dispatchers know about another dispatcher's commitments, and which details of that colleague's work may remain private?

## D. Airspace and regulatory responsibilities

44. Which authorities provide the authoritative airspace information, and how is that information received?
45. Are closures always supplied in a consistent format, or must the airspace desk interpret announcements in different forms?
46. How are the boundaries of a prohibited zone represented, and how do zones relate to the corridors and sites?
47. Can a closure affect only part of a corridor, several corridors, or a whole zone?
48. How should a planned closure, a sudden closure and an amended closure be distinguished in the operational information?
49. What happens if an authority issues an amendment that conflicts with an earlier announcement or leaves an important detail unclear?
50. How is the effective time of a sudden closure established, including when the announcement reaches the platform late?
51. When a closure changes while drones are airborne, what information is needed to understand which flights may be affected?
52. Which decisions remain exclusively the operator's responsibility under the applicable EU drone and U-space rules?
53. Which information must be available to support flight authorisation, and which party is responsible for obtaining it?
54. Is the platform expected to represent the outcome of an authority's decision, or is it also expected to support any exchange required to obtain that decision?
55. What does the airspace desk mean by measuring disruption caused by a closure?
56. Should disruption distinguish between flights cancelled, delayed, diverted, already airborne or unable to depart?
57. How should the impact of an amended closure be distinguished from the impact of the original closure?
58. What is the minimum information the airspace desk needs to understand overall disruption without inspecting individual companies' commercial operations?

## E. Unreliable communications and events

59. Which outside people and devices report job progress, departures, arrivals, drone faults and charging activity?
60. What does each reported event mean, and how trustworthy is each source?
61. Do reports carry the time an event happened, the time it was recorded, or both?
62. How can the service distinguish a delayed report from a new event, and a repeated report from a second occurrence?
63. What happens if two sources provide contradictory reports about the same drone?
64. How long can communications be unavailable in the field, and what information can still be obtained during an interruption?
65. Which instructions can be sent to drones and charging pads, and what does success mean for each instruction?
66. How do staff currently establish whether an instruction was received when the sender cannot tell whether it arrived?
67. Are there instructions that must never be repeated automatically, even when their outcome is unknown?
68. What is the expected response when a drone reports a fault and later reports normal operation?
69. How can staff distinguish a drone that is safe to reuse from one that merely appears to be operating again?
70. What is the source of truth when a physical inspection contradicts the latest reported status?

## F. Service interruptions and information exchange

71. Which activities must remain possible during the accepted interruption of a few minutes?
72. What does each company need to know when the service returns after a restart or crash?
73. Which actions or decisions must remain understandable after an interruption, even if the person who made them is no longer present?
74. What does the company expect when an instruction may have been carried out but its acknowledgement was lost?
75. Which events must be shared with each company's own systems, and what information must each event contain?
76. Which company systems receive information about drones, jobs, flights, charging, faults and cancellations?
77. Do those systems expect to receive every event, or only changes to the current state?
78. How do the operating companies currently deal with missing, repeated or out-of-order information from their own systems?
79. Which information is needed to explain what happened during an incident, and how long must it remain available for ordinary operational purposes?
80. Are there operational activities that continue outside the service during its interruption, and how is the resulting information reconciled?

## G. People, handovers and working practices

81. What are the actual responsibilities and authority limits of fleet technicians, dispatchers and airspace desk staff?
82. Can several technicians work on the same drone or repair simultaneously?
83. Who is responsible for ensuring a repair handover is complete when the technician who started the work is no longer available?
84. What happens when a dispatcher and technician disagree about whether a drone is fit to fly?
85. What information must pass from the people preparing a load to the dispatcher?
86. What happens when a job's owner, load preparer, technician or dispatcher cannot be reached?
87. How many jobs, drones and sites does a dispatcher typically handle at once, and how does that vary during busy periods?
88. Which operational decisions must be made immediately, and which can wait until more reliable information arrives?
89. What do staff currently do when information is missing, and which of those workarounds are essential to keep operations going?
90. Which misunderstandings between roles cause the most delays, repeated work or unsafe assumptions?

## H. Scope and unresolved assumptions

91. Which day-to-day tasks are explicitly expected to be supported by the service, beyond the equipment, job, flight and airspace activities described?
92. Which activities are intentionally left to each company's existing systems and working practices?
93. Are there any additional user roles, such as site staff or people preparing loads, who need to interact directly with the service?
94. What does the platform company mean by accepting a few minutes of interruption, and are there specific times or circumstances in which interruptions are unacceptable?
95. What are the most important consequences of incorrect information for each role: wasted time, missed work, equipment damage, operational disruption or something else?
96. Which kinds of mistakes are recoverable, and which require immediate human attention?
97. What must staff be able to establish when a disputed event or decision is investigated later?
98. Which details in the document describe current practice, and which describe intended future policy?
99. Are there known differences between the parcel delivery, infrastructure inspection and hospital logistics companies that materially affect their day-to-day needs?
100. What evidence would the authors accept as confirmation that these stories reflect real users' needs rather than reasonable but untested assumptions?

## Analyst's closing assessment

The most important discovery theme is trustworthy operational knowledge under uncertainty. Each role needs a different kind of confidence:

- Fleet technicians need confidence that equipment status reflects its actual condition and that maintenance history remains understandable.
- Dispatchers need confidence that their decisions are based on current, appropriately qualified information while retaining responsibility for drone and route selection.
- The airspace desk needs confidence that the shared airspace picture reflects the authorities' information, while maintaining a strict boundary around each customer's business.

Several apparent requirements remain unresolved and should not be silently converted into implementation decisions: how to resolve contradictory reports, how to represent uncertain states, how to establish whether repeated instructions took effect, how to measure disruption without exposing customer operations, and how to handle competing commitments between dispatchers.

These are the areas I would prioritise in the next round of real-user interviews. The 45 stories are a discovery baseline, not yet a validated or complete requirements specification.
