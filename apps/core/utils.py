import difflib
import json

CIVIC_ISSUES = {
    "🛣 Roads & Transport": [
        "road", "roads", "pothole", "potholes", "asphalt", "tarmac", "crack", "cracks", "broken", "damaged",
        "traffic", "jam", "signal", "red light", "crosswalk", "zebra crossing", "footpath", "sidewalk",
        "overbridge", "flyover", "bridge", "underpass", "manhole", "open manhole", "speed breaker",
        "speed hump", "lane", "highway", "expressway", "street", "avenue", "boulevard", "alley", "junction",
        "intersection", "roundabout", "median", "divider", "curb", "drainage cover", "bike lane",
        "cycle track", "bus stop", "bus stand", "railway crossing", "rail crossing", "train crossing",
        "metro station", "tram track", "auto stand", "rickshaw stand", "parking", "illegal parking",
        "encroachment", "construction debris", "dust road", "mud road", "slippery road", "oil spill",
        "congestion", "bottleneck", "blocked road", "road closed", "detour", "no entry", "wrong side",
        "one way", "no parking", "tow away", "speeding", "accident spot", "blind turn", "sharp curve",
        "signboard missing", "traffic sign", "signal light", "traffic pole", "stop sign", "yield sign",
        "danger sign", "hazard sign", "pedestrian bridge", "foot overbridge", "skywalk", "bus bay",
        "metro pillar", "pillar collapse", "bridge crack", "bridge collapse", "flyover crack", "pavement",
        "walkway", "footpath tiles", "sidewalk tiles", "uneven path", "gutter on road", "open drain road",
        "muddy patch", "road flood", "waterlogging road", "street corner", "road encroachment"
    ],

    "🗑 Garbage & Waste": [
        "garbage", "trash", "waste", "dump", "dustbin", "bin", "overflowing bin", "plastic waste",
        "food waste", "wet waste", "dry waste", "solid waste", "liquid waste", "industrial waste",
        "toxic waste", "hazardous waste", "medical waste", "biomedical waste", "e-waste", "electronic waste",
        "scrap", "debris", "construction waste", "litter", "rubbish", "filth", "junk", "refuse",
        "municipal waste", "household waste", "domestic waste", "residential garbage", "slum garbage",
        "sludge", "sewage waste", "manure", "compost", "leftovers", "kitchen waste", "vegetable waste",
        "fruit waste", "meat waste", "fish waste", "animal waste", "carcass", "dead animal", "sanitary waste",
        "diaper", "napkin", "pads", "tampons", "toilet waste", "excreta", "feces", "human waste",
        "urine bottles", "spit", "phlegm", "spittoon", "cigarette butt", "beedi butt", "gutka packet",
        "paan spit", "tobacco packet", "plastic bag", "poly bag", "polythene", "thermocol", "styrofoam",
        "styrofoam cup", "plastic bottle", "PET bottle", "glass bottle", "beer bottle", "alcohol bottle",
        "broken glass", "shards", "needle", "syringe", "blade", "razor", "hazardous item", "paint can",
        "oil can", "lubricant can", "chemical container", "detergent packet", "soap wrapper", "shampoo bottle",
        "cosmetic bottle", "tube light waste", "bulb waste", "battery waste", "cell waste", "car battery",
        "bike battery", "furniture waste", "mattress", "old sofa", "old chair", "broken cupboard"
    ],

    "💡 Streetlights & Electricity": [
        "streetlight", "street light", "lamp post", "lamp", "bulb", "tube light", "halogen", "led light",
        "led lamp", "flickering light", "blinking light", "dim light", "dark street", "no light",
        "light outage", "electric pole", "electric wire", "wiring", "loose wire", "spark", "short circuit",
        "transformer", "fuse", "switchboard", "power cut", "blackout", "brownout", "voltage drop",
        "high voltage", "low voltage", "cable cut", "underground cable", "pole broken", "pole fallen",
        "pole leaning", "street pole", "danger pole", "live wire", "shocking wire", "electric shock",
        "shock hazard", "burnt pole", "fire pole", "burnt wire", "electric fire", "lamp cover broken",
        "lamp glass broken", "pole rusted", "lamp fixture missing", "light stand", "lantern",
        "garden light", "park light", "flood light", "stadium light", "tower light", "pillar light",
        "neon light", "decorative light", "festival light", "series light", "street dark", "lane dark",
        "avenue dark", "high mast light", "mast light", "spotlight", "focus light", "security light",
        "cctv light", "emergency light", "solar lamp", "solar streetlight", "solar power pole",
        "battery backup light", "inverter light", "temporary wire", "illegal connection", "hook wire",
        "power theft", "power line sagging", "pole transformer", "pillar box", "distribution box",
        "meter box", "open meter", "power meter", "smart meter", "fused light"
    ],

    "💧 Water Supply & Drainage": [
        "water", "pipe", "pipeline", "pipe burst", "leakage", "seepage", "drip", "scarcity", "shortage",
        "no water", "contaminated water", "dirty water", "salty water", "smelly water", "chlorine water",
        "rust water", "colored water", "drain", "sewage", "gutter", "nala", "nallah", "open drain",
        "blocked drain", "choked drain", "clogged drain", "overflowing drain", "stagnant water",
        "waterlogging", "flood", "street flood", "rainwater flood", "monsoon flood", "flash flood",
        "tap", "hand pump", "borewell", "well", "tank", "overhead tank", "underground tank", "cistern",
        "sump", "bucket water", "tank water", "supply water", "drinking water", "RO water", "filtered water",
        "bottled water", "mineral water", "can water", "water packet", "hydrant", "stand post", "public tap",
        "community tap", "water kiosk", "pipeline theft", "illegal connection", "water tanker", "private tanker",
        "tank leak", "tank crack", "tank overflow", "pipe corrosion", "pipe rust", "pipe break", "pipe joint leak",
        "sewage overflow", "sewer line", "sewer choke", "sewer break", "manhole overflow", "manhole blockage",
        "storm drain", "rain drain", "storm water", "nali", "ganda nali", "nal ka pani", "jal sanchay",
        "jal pipeline", "jal leakage", "underground seepage", "groundwater depletion"
    ],

    "🌳 Parks & Environment": [
        "park", "garden", "playground", "stadium ground", "sports ground", "open ground", "open space",
        "green space", "tree", "fallen tree", "uprooted tree", "tree branch", "branch fall", "pruning needed",
        "overgrown tree", "bush", "bushes", "shrub", "hedge", "plant", "sapling", "flower bed",
        "lawn", "grass", "grass cutting", "weeds", "wild grass", "dry grass", "forest", "jungle",
        "green cover", "pollution", "air pollution", "water pollution", "noise pollution", "dust pollution",
        "smoke pollution", "vehicle smoke", "industrial smoke", "chimney smoke", "factory smoke",
        "toxic air", "CO2 emission", "carbon emission", "climate change", "heat wave", "global warming",
        "ozone hole", "deforestation", "illegal cutting", "tree cutting", "tree felling", "timber theft",
        "forest fire", "jungle fire", "grass fire", "plastic burn", "waste burn", "garbage burn",
        "burning smell", "bad odour", "smelly air", "dust storm", "sand storm", "soil erosion",
        "landslide", "mudslide", "river pollution", "lake pollution", "pond pollution", "nala pollution",
        "froth lake", "foam river", "dead fish", "aquatic death", "fish kill", "sewage in river",
        "chemical discharge", "toxic discharge", "industrial effluent", "hazardous spill", "oil spill"
    ],

    "🏥 Health & Sanitation": [
        "health", "hospital", "clinic", "dispensary", "doctor", "nurse", "medicine", "pharmacy", "chemist",
        "ambulance", "sanitation", "toilet", "public toilet", "urinal", "washroom", "latrine",
        "community toilet", "mobile toilet", "bio toilet", "septic tank", "overflowing toilet",
        "choked toilet", "dirty toilet", "filthy toilet", "stinking toilet", "open defecation",
        "open urination", "spitting", "phlegm spit", "gutka spit", "paan spit", "blood spit",
        "mosquito", "dengue", "malaria", "chikungunya", "vector", "vector borne", "mosquito breeding",
        "stagnant water mosquito", "fly nuisance", "housefly", "cockroach", "rat", "rodent",
        "pest", "pest infestation", "bedbug", "lice", "scabies", "skin infection", "water borne disease",
        "cholera", "typhoid", "dysentery", "diarrhea", "vomiting", "nausea", "food poisoning",
        "contaminated food", "spoiled food", "expired food", "milk adulteration", "food adulteration",
        "fake medicine", "counterfeit medicine", "illegal clinic", "quack doctor", "fake doctor",
        "oxygen shortage", "ventilator shortage", "covid", "flu", "viral fever", "pandemic",
        "epidemic", "outbreak", "immunization", "vaccination", "polio drop", "injection shortage",
        "sanitary pad", "napkin shortage", "hygiene issue", "waste disposal", "dirty colony",
        "unhygienic area", "filthy slum", "open garbage", "odour problem"
    ],

    "🚦 Other Civic Issues": [
        "signal", "traffic light", "cctv", "camera", "surveillance", "broken camera", "illegal hoarding",
        "poster", "banner", "flex banner", "advertisement board", "billboard", "sign board", "danger board",
        "safety board", "unsafe area", "crime spot", "snatching spot", "theft spot", "chain snatching",
        "robbery spot", "eve teasing", "molestation", "assault", "illegal building", "unauthorized construction",
        "encroachment road", "encroachment park", "hawker nuisance", "street vendor issue",
        "illegal vendor", "rickshaw nuisance", "auto nuisance", "taxi nuisance", "bike stunt", "car racing",
        "drunken driving", "drink drive", "overspeeding", "rash driving", "wrong parking", "footpath parking",
        "roadside parking", "choking road", "loudspeaker", "noise issue", "DJ noise", "religious noise",
        "fire cracker noise", "marriage procession noise", "band noise", "sound pollution",
        "unsafe wiring", "illegal connection", "illegal tapping", "wire theft", "cable theft", "pole theft",
        "iron theft", "metal theft", "manhole cover theft", "drain cover theft", "pipeline theft",
        "transformer oil theft", "public nuisance", "public drinking", "liquor bottle", "beer bottle",
        "drunk fight", "gambling", "illegal betting", "illegal hoarding", "political hoarding",
        "communal slogan", "graffiti", "wall paint", "dirty wall", "urination wall", "spit wall",
        "cow menace", "dog menace", "stray dog", "stray cow", "buffalo menace", "monkey menace",
        "pig menace", "goat menace", "bird menace", "pigeon menace", "wild animal", "snake sighting"
    ]
}


def classify_civic_issue(title: str, description: str) -> str:
    text = (title + " " + description).lower().split()
    matched_categories = set()

    for category, keywords in CIVIC_ISSUES.items():
        for word in text:
            if word in keywords:
                matched_categories.add(category)
            else:
                for keyword in keywords:
                    if difflib.SequenceMatcher(None, keyword, word).ratio() > 0.8:
                        matched_categories.add(category)

    if matched_categories:
        return 1
    return 0

# Example Run