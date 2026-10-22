# World brief — drone fleet operations

Version: 1.0
Author: contract author
Status: **signed by the contract author, 2026-10-22.** Drafted with the author's working models, which knew the requirements; every sentence that states a constraint or a need rather than a fact is declared in `brief-seeding.md`. This is the only text through which the contract author shapes the content of the user stories (decision register D-36). It describes the world the users live in. It does not describe any software.

---

## 1. The business

A platform company runs a shared service for several independent drone operating companies. Its customers today include a parcel delivery firm, an infrastructure inspection firm, and a regional hospital logistics firm. Others are expected to join.

The customer companies compete with each other or work for clients who do. Each company's fleet, jobs, sites, and problems are its own business. They accept sharing airspace information, because that information comes from the authorities and is the same for everyone.

## 2. People

**At each operating company**

- **Fleet technicians** keep drones and charging equipment in working order. They add new drones to the fleet, retire old ones, set up charging pads at the company's sites, take drones out of service for repairs and put them back, and send drones to charge.
- **Dispatchers** plan and run the flights. A dispatcher is the licensed person responsible for each flight: they decide which drone flies, along which way, and they sign off a flight before it leaves. A dispatcher can call off a flight.

**At the platform company**

- The **airspace desk** keeps the shared picture of the airspace: the network of flight corridors between sites, the zones that group them, and the closures announced by the authorities. The desk works for all customer companies and has no business looking into any one company's operations. When a closure is entered, the desk wants to know how much disruption it caused across customers.

## 3. Fleets and equipment

- A company may run a few hundred drones. The drones are of several models from different manufacturers. They differ in how much they can carry, how far they can fly on a full battery, which sensors they carry (cameras, thermal cameras, laser scanners), and which charging connector they use. Several connector types are in use and they are not interchangeable.
- Each drone has a home site. Each company has its own charging pads at its own sites, a few dozen of them. Pads are never lent to another company.
- Repairs and servicing are carried out by technicians. Regulators can ask a company to show how its drones have been looked after.

## 4. The work

- **Deliveries** carry a load from one site to another.
- **Inspections** take a drone with the right sensors to a list of points in a set order and bring it back to where the inspection started.
- Drones fly along corridors between named sites. Sites have only so many places where drones can take off and land at the same time.
- Choosing the drone and the way it flies is the dispatcher's legal responsibility. The companies' policy is that software never chooses a drone or a way for them. Dispatchers do want help finding out which of their drones could get to where a job starts.
- Several dispatchers plan at the same time, often for the same busy sites and the same popular drones.
- Before and during a flight, things happen outside the company's control: the load is ready or not, the drone reaches the points of its job, and the drone arrives. People and devices outside the company report these things.

## 5. Airspace

- The authorities define zones where flying is prohibited, and they announce closures: planned ones with a start and end time, and sudden ones that apply at once. Closures are often amended during the day, for example when an area is widened or an end time moves.
- A closure can come into force while drones of several companies are already in the air.
- The relevant rules are the EU drone operation rules (Implementing Regulation (EU) 2019/947, including geographical zones and operator responsibilities) and the EU U-space rules (Implementing Regulation (EU) 2021/664, including airspace information and flight authorisation). Personal data of staff is covered by the GDPR. None of the companies is seeking certification from the platform; they expect it to respect how these rules work in practice.

## 6. Conditions in the field

- Drones fly on their own autopilots. People on the ground supervise; nobody steers a drone with a stick through this service.
- Radio coverage is patchy, especially around ports, industrial sites, and in bad weather. Reports from drones come through relay stations. They can arrive late, out of order, more than once, or not at all.
- Drones sometimes restart in flight after a software fault and carry on.
- Batteries drain faster in cold and wind than planned.
- Nobody watches every drone at every moment; one person may be responsible for hundreds.
- The links used to give instructions to drones and to the charging equipment are unreliable too. An instruction may get through twice, and the sender often cannot tell whether the first attempt arrived.

## 7. The service itself

- The platform company is small. The service runs on a single server. It is updated and restarted during working hours, while drones are flying, and it occasionally crashes. The companies accept a few minutes of interruption.
- Each company runs its own systems, such as billing and customer updates, that need to hear about what happens to its drones and jobs.

## 8. What the companies do not want

- Management or analytical reports, exports, and dashboards beyond day-to-day operations.
- Logging in through their own corporate identity systems.
- Several languages.
- Any guarantee of meeting regulations, any compliance audit, or any data-retention or deletion features.
- Backups, high availability, or spreading the service over several servers.
- Accounts and passwords inside the service: staff accounts are issued by the platform company outside it.
- Alerts to staff by e-mail, text message, or phone; each company's own systems take care of reaching people.
- Software that plans routes or picks drones.
- Flying drones remotely through the service.
- Weather information.
- Billing or pricing of the work; companies do that in their own systems.
- Signing up new companies through the service; the platform company does that itself.
