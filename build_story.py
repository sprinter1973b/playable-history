import json,os
from tour_data import route as tour_route
sky='<rect width="320" height="200" fill="#e9c98f"/><circle cx="260" cy="45" r="22" fill="#f6e2b0"/>'
ground='<rect y="150" width="320" height="50" fill="#8a6a45"/>'
rails='<rect y="168" width="320" height="4" fill="#3b2f2a"/><rect y="180" width="320" height="4" fill="#3b2f2a"/>'+''.join(f'<rect x="{x}" y="164" width="6" height="24" fill="#5a4030"/>' for x in range(0,320,20))
def svg(b): return f'<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{sky}{ground}{b}</svg>'
depot='<rect x="90" y="95" width="150" height="60" fill="#b5653a"/><polygon points="80,95 250,95 225,70 105,70" fill="#4a3a33"/><rect x="110" y="115" width="18" height="40" fill="#3b2f2a"/><rect x="150" y="110" width="20" height="18" fill="#f3e6c8"/><rect x="195" y="110" width="20" height="18" fill="#f3e6c8"/>'
train='<rect x="20" y="120" width="70" height="40" fill="#2b2420"/><rect x="60" y="100" width="25" height="25" fill="#2b2420"/><rect x="28" y="95" width="10" height="25" fill="#2b2420"/><circle cx="35" cy="162" r="9" fill="#555"/><circle cx="75" cy="162" r="9" fill="#555"/><circle cx="33" cy="80" r="10" fill="#ccc" opacity=".7"/>'
cotton='<rect x="200" y="125" width="40" height="30" fill="#efe8da" stroke="#8a6a45"/><rect x="245" y="125" width="40" height="30" fill="#efe8da" stroke="#8a6a45"/><rect x="222" y="97" width="40" height="28" fill="#efe8da" stroke="#8a6a45"/>'
store='<rect x="40" y="70" width="240" height="85" fill="#9c5b3b"/><rect x="40" y="62" width="240" height="14" fill="#5a3a2a"/><text x="160" y="73" font-size="10" text-anchor="middle" fill="#f3e6c8" font-family="Georgia">GENERAL MERCHANDISE · COTTON</text>'+''.join(f'<rect x="{x}" y="95" width="30" height="40" fill="#f3e6c8"/>' for x in (60,110,180,230))+'<rect x="145" y="105" width="30" height="50" fill="#3b2f2a"/>'
charter='<rect x="95" y="40" width="130" height="150" fill="#f8f1e0" stroke="#8a6a45" stroke-width="3"/><text x="160" y="70" font-size="13" text-anchor="middle" font-family="Georgia" fill="#2b2420">CHARTER</text><text x="160" y="90" font-size="10" text-anchor="middle" font-family="Georgia" fill="#2b2420">Town of Woodstock</text><text x="160" y="106" font-size="10" text-anchor="middle" font-family="Georgia" fill="#2b2420">Dec. 8, 1897</text>'+''.join(f'<rect x="110" y="{y}" width="100" height="3" fill="#c9b893"/>' for y in range(120,175,10))
mill='<rect x="0" y="140" width="320" height="22" fill="#4f7a8c"/><rect x="70" y="80" width="120" height="62" fill="#8c8c80"/><rect x="85" y="95" width="15" height="15" fill="#3b2f2a"/><rect x="120" y="95" width="15" height="15" fill="#3b2f2a"/><rect x="155" y="95" width="15" height="15" fill="#3b2f2a"/><circle cx="205" cy="125" r="22" fill="none" stroke="#5a4030" stroke-width="5"/>'
house='<rect x="90" y="85" width="140" height="70" fill="#f3e6c8" stroke="#5a4030" stroke-width="2"/><polygon points="80,88 240,88 160,45" fill="#6b4a2f"/><rect x="70" y="115" width="180" height="6" fill="#5a4030"/>'+''.join(f'<rect x="{x}" y="121" width="5" height="34" fill="#5a4030"/>' for x in (75,125,190,240))+'<rect x="150" y="125" width="20" height="30" fill="#3b2f2a"/><rect x="105" y="95" width="18" height="16" fill="#9fb8c8"/><rect x="197" y="95" width="18" height="16" fill="#9fb8c8"/>'
church='<rect x="100" y="85" width="120" height="70" fill="#f3e6c8" stroke="#5a4030" stroke-width="2"/><polygon points="92,88 228,88 160,55" fill="#6b4a2f"/><rect x="145" y="45" width="30" height="45" fill="#efe8da" stroke="#5a4030"/><polygon points="140,47 180,47 160,15" fill="#6b4a2f"/><path d="M118 135v-25a8 8 0 0116 0v25zM186 135v-25a8 8 0 0116 0v25z" fill="#c98a3b"/><rect x="150" y="120" width="20" height="35" fill="#3b2f2a"/>'
school='<rect x="40" y="90" width="240" height="65" fill="#9c5b3b"/><polygon points="30,92 290,92 160,62" fill="#4a3a33"/><rect x="148" y="40" width="24" height="26" fill="#efe8da"/><circle cx="160" cy="55" r="6" fill="#c98a3b"/>'+''.join(f'<rect x="{x}" y="105" width="20" height="24" fill="#f3e6c8"/>' for x in (60,95,200,235))+'<rect x="148" y="115" width="24" height="40" fill="#3b2f2a"/>'
bank='<rect x="80" y="60" width="160" height="95" fill="#d9b36a"/><rect x="80" y="55" width="160" height="12" fill="#a7823f"/><text x="160" y="85" font-size="14" text-anchor="middle" font-family="Georgia" fill="#3b2f2a">BANK</text><rect x="100" y="95" width="25" height="40" fill="#f3e6c8"/><rect x="195" y="95" width="25" height="40" fill="#f3e6c8"/><rect x="147" y="100" width="26" height="55" fill="#3b2f2a"/>'
I={
 "house":{"alt":"Simple drawing of a historic house with a front porch","svg":svg(house)},
 "church":{"alt":"Simple drawing of a small historic church with arched windows","svg":svg(church)},
 "school":{"alt":"Simple drawing of a brick schoolhouse with a bell cupola","svg":svg(school)},
 "bank":{"alt":"Simple drawing of a small golden-brick bank building","svg":svg(bank)},
 "book":{"alt":"Simple drawing of an open memory book","svg":svg('<rect x="70" y="60" width="90" height="100" fill="#f8f1e0" stroke="#8a6a45" stroke-width="3"/><rect x="160" y="60" width="90" height="100" fill="#f8f1e0" stroke="#8a6a45" stroke-width="3"/>'+''.join(f'<rect x="85" y="{y}" width="60" height="3" fill="#c9b893"/><rect x="175" y="{y}" width="60" height="3" fill="#c9b893"/>' for y in range(80,150,12)))},
 "cover":{"alt":"Simple drawing of a steam train arriving beside a brick depot with cotton bales","svg":svg(rails+train+depot)},
 "depot":{"alt":"Simple drawing of a small depot by the tracks with cotton bales waiting","svg":svg(rails+depot+cotton)},
 "store":{"alt":"Simple drawing of a Main Street general store selling merchandise and buying cotton","svg":svg(store)},
 "charter":{"alt":"Simple drawing of a town charter document dated December 8, 1897","svg":svg(charter)},
 "mill":{"alt":"Simple drawing of a mill building beside Little River","svg":svg(mill)},
 "warehouse":{"alt":"Simple drawing of a two-story brick cotton warehouse with a wagon of bales","svg":svg('<rect x="70" y="60" width="180" height="95" fill="#8a4a32"/><rect x="70" y="100" width="180" height="4" fill="#5a3a2a"/><rect x="100" y="70" width="16" height="24" fill="#f3e6c8"/><rect x="200" y="70" width="16" height="24" fill="#f3e6c8"/><rect x="145" y="110" width="30" height="45" fill="#3b2f2a"/><rect x="10" y="130" width="50" height="18" fill="#6b4a2f"/><circle cx="20" cy="152" r="7" fill="#444"/><circle cx="50" cy="152" r="7" fill="#444"/><rect x="15" y="112" width="18" height="18" fill="#efe8da" stroke="#8a6a45"/><rect x="36" y="112" width="18" height="18" fill="#efe8da" stroke="#8a6a45"/>')},
 "newdepot":{"alt":"Simple drawing of the 1912 depot beside the tracks","svg":svg(rails+depot)},
}
SRC=[
 {"id":"city","title":"City of Woodstock – History of Woodstock","url":"https://www.woodstockga.gov/about/history_woodstock.php"},
 {"id":"pw","title":"Preservation Woodstock – Woodstock History timeline","url":"https://www.preservationwoodstock.com/woodstock-history/"},
 {"id":"cchs","title":"Cherokee County Historical Society – Woodstock Depot (archived)","url":"https://web.archive.org/web/20140324201803/http:/www.rockbarn.org/woodstockDepot.php"},
 {"id":"nrhp","title":"National Park Service NPGallery – Woodstock Depot, NRIS 95000736","url":"https://npgallery.nps.gov/AssetDetail/NRIS/95000736"},
 {"id":"brochure","title":"Visit Woodstock GA – Historic Downtown Woodstock Walking Tour (printed brochure, Woodstock Visitors Center, 8588 Main St.)","url":"https://www.visitwoodstockga.com/"},
 {"id":"city125","title":"City of Woodstock – Celebrates 125 Years","url":"https://www.woodstockga.gov/news_detail_T15_R70.php"}]
story={
"schemaVersion":1,
"meta":{"title":"The Depot at the Center of Town","museum":"Downtown Woodstock, GA","expectedSteps":5,"coverImage":"cover",
 "intro":"It is the 1890s. You are Ada Pruitt, 16, whose family farms cotton outside Woodstock. Make up to five choices and see how the railroad shaped the town you know today. About 5 minutes.",
 "characterNote":"Ada Pruitt and her family are fictional composite characters. Places, dates and events marked “True history” come from the cited sources.",
 "cta":{"label":"Learn more: walk Downtown Woodstock with History Cherokee","url":"https://www.historycherokee.org/"},
 "credits":"Story illustrations: original simple SVG drawings. Tour-stop photos and story by John B Thomas Jr, Living in Woodstock GA."},
"images":I,"sources":SRC,"start":"s1",
"route":[
 {"stop":12,"name":"Cotton Warehouse","address":"105 Towne Lake Pkwy. (formerly Church St.)","maps":"105 Towne Lake Pkwy, Woodstock, GA 30188"},
 {"stop":16,"name":"Dean's Store (today the Woodstock Visitors Center)","address":"8588 Main St.","maps":"8588 Main St, Woodstock, GA 30188"},
 {"stop":17,"name":"Woodstock Depot (1912)","address":"251 E Main St.","maps":"251 E Main St, Woodstock, GA 30188"},
 {"stop":18,"name":"Original location of J.H. Johnston Company","address":"8590/8594 Main St.","maps":"8590 Main St, Woodstock, GA 30188"},
 {"stop":25,"name":"Olde Rope Mill Park","address":"Rope Mill Rd., about 1 mile north of downtown","maps":"Olde Rope Mill Park, Woodstock, GA"}],
"scenes":{
 "s1":{"title":"Harvest at the Tracks","when":"Autumn, 1890s","image":"depot","stop":17,
  "text":["Your father's wagon creaks toward the depot with bales of cotton. Before the trains came, families here mostly grew what they needed. Now the rails run straight through the village.","Father hands you the reins. “You decide where we take this load first.”"],
  "fact":"The Marietta & North Georgia Railroad reached Woodstock in 1879 on its line from Marietta to Canton. A first depot stood on the west side of the tracks, and farmers used the line to ship cotton to mills. (Today's depot at this stop replaced that first depot in 1912.)","sources":["city","pw","cchs","brochure"],
  "choices":[{"label":"Go to the depot and ship the cotton by rail","next":"s2a"},{"label":"Stop at the big general store on Main Street","next":"s2b"}]},
 "s2a":{"title":"The Depot Agent","when":"Autumn, 1890s","image":"depot","stop":17,
  "text":["The depot agent tallies your bales, and the telegraph clicks behind him. Trains carry mail, goods and passengers to Marietta and beyond.","A man on the platform says the town may soon become an official city."],
  "fact":"The depot was the focal point for shipping cotton, rope and farm products, and for travelers heading to Canton and Marietta. It had an agent and telegraph service.","sources":["cchs"],
  "choices":[{"label":"Ask the man what becoming a city would mean","next":"s3"}]},
 "s2b":{"title":"Johnston's Store","when":"Autumn, 1890s","image":"store","stop":18,
  "text":["Main Street is lined with businesses on its west side, and cotton warehouses stand across the way. At the J.H. Johnston Company you can sell your cotton and buy supplies in the same trip.","The clerk mentions talk of a town charter."],
  "fact":"This is believed to be the first location of the J.H. Johnston Company, General Mercantile and Cotton Brokers, established in 1888. The Woodstock Masonic Lodge and the telephone exchange used the second floor, and the Bank of Woodstock began in the store before moving to its own building in 1908.","sources":["brochure","pw","city"],
  "choices":[{"label":"Ask the clerk about the charter","next":"s3"}]},
 "s3":{"title":"A Town Measured from the Depot","when":"December 1897","image":"charter","stop":17,
  "text":["News arrives: the Georgia legislature has granted Woodstock a charter. Folks gather to hear how the new town lines were drawn.","Everyone laughs when they hear where the measuring started."],
  "fact":"On December 8, 1897, the Georgia legislature chartered Woodstock. City limits ran ¾ mile north and south of the depot and ½ mile east and west of the tracks, making the depot the center of town. Nathan Fowler was the first mayor. The 1900 census counted 276 residents.","sources":["city","pw","cchs","brochure"],
  "prompt":"Years pass. Where does your future lead?",
  "choices":[{"label":"Stay in town and help with the family's cotton business","next":"s_wh"},{"label":"Look for work at the mill on Little River","next":"s4m"}]},
 "s_wh":{"title":"Weighing Day at the Warehouse","when":"Around 1905","image":"warehouse","stop":12,
  "text":["You drive the wagon up to the Johnston cotton warehouse on Church Street. A work crew wrestles each heavy bale off the wagon and onto the scale.","The clerk hands you a receipt. Down on Main Street, Dr. W.H. Dean's store is open for business. Your father asks what to do with the money."],
  "fact":"The J.H. Johnston cotton warehouse, built around 1905, is the last of several such warehouses in Woodstock. Crews moved 500-pound bales by hand into the upper floor, which opened onto Church Street. Each bale was weighed and tagged, and the owner got a receipt showing weight, date and quality. The humid basement held fertilizer, plows and other farm equipment instead. Dean's Store at 8588 Main St. was built around 1905 or earlier; Dr. W.H. Dean was the owner, and the building is now the Woodstock Visitors Center.","sources":["brochure"],
  "choices":[{"label":"Save it and watch the town grow around the depot","next":"s4"},{"label":"Buy a new plow from the warehouse basement","next":"s4"}]},
 "s4":{"title":"A New Depot","when":"1912","image":"newdepot","stop":17,
  "text":["You are grown now. Crews finish a new wooden depot beside the tracks, with a red clay tile roof, a freight room and a passenger waiting area.","Your niece asks whether to ride the train to school in Canton or Marietta."],
  "fact":"The Louisville & Nashville Railroad bought the line in 1905 and built the current depot in 1912 on the east side of the tracks, replacing the first depot, which was later torn down. It has tongue-and-groove siding and a red clay tile roof, typical North Georgia depot design with Victorian touches, and served as a “combination station” for freight and passengers. Like other L&N depots of the time, it had a separate entrance and waiting room for Black passengers under segregation.","sources":["cchs","pw","brochure"],
  "choices":[{"label":"Tell her to take the train to school","next":"e_rails"},{"label":"Tell her to stay and build something in Woodstock","next":"e_town"}]},
 "s4m":{"title":"The Mill on Little River","when":"Around 1900","image":"mill","stop":25,
  "text":["North of town, Little River drops just enough to turn a mill wheel, and the mill spins local cotton. The work is loud and long, but the pay is steady.","A foreman asks if you will train the new hands."],
  "fact":"Grist mills worked this stretch of Little River from the 1840s or earlier. The 1880 census shows the Joel T. Haley mill making cotton yarns, using the river's slight drop to power textile machinery. A series of owners and cotton businesses followed.","sources":["brochure","city"],
  "choices":[{"label":"Train the new workers","next":"e_mill"},{"label":"Return to town and the depot","next":"s4"}]}},
"endings":{
 "e_rails":{"title":"Ending: The Line to the Wider World","image":"cover","text":["Your niece rides the train to school each day, part of a generation the rails connected to wider Georgia."],
  "history":["Students rode the train from the Woodstock depot to school in Canton and Marietta. Passenger service ended on March 1, 1949, and the depot kept freight and telegraph service until the late 1950s."],"sources":["cchs"]},
 "e_town":{"title":"Ending: The Center Still Holds","image":"newdepot","text":["Your family stays and helps the little town grow around its depot."],
  "history":["The 1912 depot still stands and is on the National Register of Historic Places, the only such listing in Woodstock. Main Street was paved in 1912. Woodstock grew from about 4,500 to about 36,000 residents over three decades."],"sources":["nrhp","pw","brochure","city125"]},
 "e_mill":{"title":"Ending: Cotton into Rope","image":"mill","text":["You become one of the experienced hands at the mill, teaching others the trade as owners come and go."],
  "history":["The last cotton mill on the site, Rope Mill (1928–1949), made rope for wells, plow lines and tents. Joe Johnston and Smith Johnston Sr. were its last owners. It closed in 1949 after the U.S. Government bought the property for Lake Allatoona. Ruins of the mill and history signs are in Olde Rope Mill Park today."],"sources":["brochure","city"]}}}
# Full 25-stop walking tour (replaces the 5-stop route); keep photo info from add_photos.py
old={}
if os.path.exists('stories/woodstock.json'):
    old={r['stop']:r.get('photo') for r in json.load(open('stories/woodstock.json')).get('route',[])}
story['route']=tour_route()
from chapters import C as CH
DEPOT={12:'s_wh',16:'s_wh',17:'s1',18:'s2b',25:'s4m'}
story['chapters']={}
for n,img,title,when,intro,prompt,br,keep in CH:
    p=f'c{n}_';e=p+'end'
    story['scenes'][p+'a']={"title":title,"when":when,"image":img,"stop":n,"text":intro,"prompt":prompt,
        "choices":[{"label":br[i][0],"next":p+'b'+str(i)} for i in range(2)]}
    for i,(lab,t,txt,ch) in enumerate(br):
        story['scenes'][p+'b'+str(i)]={"title":t,"when":when,"image":img,"stop":n,"text":[txt],"choices":[{"label":c,"next":e} for c in ch]}
    r=next(x for x in story['route'] if x['stop']==n)
    story['endings'][e]={"title":"Memory saved: "+keep,"image":img,"chapter":n,
        "text":[f"You add a new memory to the book you carry along the tour: {keep}."],"history":[r['blurb']],"sources":["brochure"]}
    story['chapters'][str(n)]={"title":title,"start":p+'a',"keepsake":keep,"steps":2}
    if n in DEPOT: story['chapters'][str(n)]["depotScene"]=DEPOT[n]
story['finale']={"title":"The Memory Book Is Full","image":"book","text":["You have walked all 25 stops of Historic Downtown Woodstock and saved a memory at each one, from a cotton receipt to a piece of rope from the mill on Little River.","The characters were fictional, but every building and date you met is real. Most of them are still standing, a short walk from the depot at the center of town."],"cta":{"label":"Plan a visit: Woodstock Visitors Center, 8588 Main St.","url":"https://www.visitwoodstockga.com/"}}
for r in story['route']: r['photo']=old.get(r['stop'])
json.dump(story,open('stories/woodstock.json','w'),indent=1,ensure_ascii=False)
