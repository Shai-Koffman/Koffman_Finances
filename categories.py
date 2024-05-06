#! python
# -*- coding: utf-8 -*-
from enum import Enum, auto
from functools import total_ordering

@total_ordering
class Categories(Enum):
    SUPER = auto()
    ELECTRICITY = auto()
    INTERNET_AND_PHONES = auto()
    OTHER_FOOD = auto()
    RESTAURANTS_AND_HOTELS = auto()
    WATER = auto()
    ARNONA = auto()
    CAR_INSURANCE = auto()
    CAR_EXPENSES = auto()
    HEALTH_INSURANCE = auto()
    OTHER_INSURANCE = auto()
    GAS = auto()
    FUEL = auto()
    INCOME_TAX = auto()
    HEALTH_AND_MACABI = auto()
    SCHOOLS = auto()
    STARTUP = auto()
    HUGIM = auto()
    INVESTMENTS = auto()
    CASPOMAT = auto()
    CLOTHING = auto()
    PRESENTS = auto()
    INTERNET_SERVICES_AND_SHOPPING = auto()
    ABROAD_EXPENSES = auto()
    VISA_MAX = auto()
    VISA_ISRACARD = auto()
    CHECKS = auto()
    BANK_AMLOT = auto()
    HOME_RELATED = auto()
    FUN_AND_MOVIES = auto()
    MISC = auto()
    INCOMING_TRANSFERS = auto()
    SALARIES = auto()
    BANK_TRANSFERS_AND_MONEY_TRANSFERS = auto()
    UNKNOWN = auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)
    
    def to_string(self):
        return str(self)
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Categories.{self.name}"
    
    def __reduce__(self):
        return (self.__class__, (self.name,))

# Categorizations - list of tuples, each tuple contains a category and a list of strings that are the names of the expenses that belong to this category
Categorizations = [
            (Categories.BANK_AMLOT, ['הפקדה','גביה/החזר מס','מכירה-אינטרנט','זיכוי הפרשי שער','הפקדת 738','מכירה-אינטרנט','עמל.ערוץ יש','עמ.העברת','דמי ניהול','עמ.יבוא']),
            (Categories.VISA_MAX,['מקס'] ),
            (Categories.VISA_ISRACARD, ['ישראכרט'] ),
            (Categories.SALARIES,['העברת משכורת','מ.חינוך-משכו-י']),
            (Categories.INCOMING_TRANSFERS,['אקסלנס ניהול-י','הפועלים-ביט','מב. הפועלים-י','מהבינלאומי ס-י','מסיטיבנק ס.-י','טריא קהילה פ-י','מפייבוקס שלי-י','משיכת חיסכון','רבית זכות','מס-הכנסה החז-י','זיכוי עמ.הישיר','קצבת ילדים-י']),
            (Categories.BANK_TRANSFERS_AND_MONEY_TRANSFERS,['העברת מט"ח 645','המרה אינטרנט','העברה תוך יומי','מכירת ני"ע','תיקון','הע. אינט700','העברה דיגי700','תש.ביבוא יש645','המרה-אינטרנט','קניה-אינטרנט','רשויות אינטרנט']),
            (Categories.WATER,['מיה','שטראוס','מים'] ),           
            (Categories.SUPER,['פירות וירקות חצי חינ','רמי לוי בשכונה סופרק','סופר הכיכר', 'סופר זול', 'מתחם 22','יוחננוף', 'אושר עד', 'שופרסל',  'עדיקה', 'מינימרקט ', 'חצי חינם','AM PM','AM:PM' ,'PM:AM', 'טיב טעם'],),
            (Categories.SCHOOLS,['י ה ת','חטיבת הביניים הראשונ','בית ספר המגן','דוארט','א.מ.ש.', 'LEAPLEARNER ', ' CBT', 'מכללת בית ברל'] ),
            (Categories.RESTAURANTS_AND_HOTELS,['CAROLINA','ריבאר','NAI  LON','דיינר מקום של בשר','קליאופטרה','NONO','אר קפה','אדום בר בע"מ','מקדונלדס','אונמי','שירותי בר בארועים', 'פורטונה פיצה', 'ארקפה ', 'פיצה ביס', 'נונומימי'
                                                , 'עידנס', 'בר אירי', 'חומוס ', 'ארומה ', 'בית רמות'
                                                , 'שיפודי הנכדים', 'טופולופומפו', 'מייזון קייזר', 'קפה מתתיהו', 'קומבה'
                                                , "ג'ירף ", 'שרון פיצה', 'זורבה', 'ארקפה ', ' לנדוור', 'דנון', 'מלון ים סוף'
                                                , 'קפה זוריק', 'גרקו', 'גלידות השרון', 'רמותה קפה אוכל ', 'בורגר ראנץ '
                                                , 'רימון דוכני ', 'אמפנדו במחנה', 'LEO BLOOMS  ', 'ארקפה  ', 'KFC ', 'מימי ', 'נקודה בלב  '
                                                , 'שגב ניהון', ' לב הפארק', 'נומי',  "ג'ונז פיצה ", 'חנדלה', 'לנדוור ', 'ברביץ', 'מיצי בשוק '
                                                , "מקדונלד'ס", 'זוזוברה', 'שושנה', 'OMAM', 'אננדה']),
            (Categories.PRESENTS,['WL *STEAM PURCHASE','XOBELZZUP','טוילנד','AMZN MKTP ', 'צעצועון ', 'פאזלבוקס', 'PAYBOX', 'BUYME', 'CHICKIES'
                                  , 'BIT', 'צומת ספרים', 'אייבורי', 'PAYBOX', ' STEAM','העברה בBIT', 'סקי פס סקי וסנובורד בע"מ'
                                  , 'כפר השעשועים', 'SMT', 'אימפריית הצעצועים','XOBYAP'] ),
            (Categories.OTHER_INSURANCE,['שירביט']),
            (Categories.CHECKS, ["שיק"]),
            (Categories.OTHER_FOOD,['רולדין','דרך היין בעמ','תותי משק טל','התות של עבודי','ליל סיס','ממלכת הקלייה - LENNY','מאפיית טלר','פרינה','משק רבינוביץ','ודיע מאנה בע"מ','ירק השדה - שטח-צמרת','אמיגו קפה','בוטיק סנטרל כפר סבא','שוק','התמרים','יובל','ROLADIN', 'מרכז הזמנו', 'סוליקה', 'WOLT', 'בוטיק סטנרל', 'בבקה ', 'עולם הממתקים', 'מאפית טלר'
                                    , 'גולדה ', 'לה פרומזרי ', 'מעדני שמיל ', 'גבינות המשק', 'חומוס כספי', 'קלית הכיכר', 'מעל המצופה'
                                    , 'מיסטר פיש', 'קפה ', 'ארטיזנל', 'רוזנר', 'לחם תושייה', 'בייקר', 'הפרטוי', "בולנז'רי ", 'אלי דלאל', 'בר המשקאות'
                                    , ' מטבח', 'מאפית', 'שמו', 'יין בעיר', 'בלילה', 'חלאתי  ', 'פפה ', 'גלידוש']),
            (Categories.INTERNET_AND_PHONES, ['טלזר 019 שירותי תקשו','SIMTLV - כרטיסי סים','HOT', 'SPIGEN', 'פרטנר', 'סלקום ', 'פלאפון']),
            (Categories.INVESTMENTS, ['מנורה מבטחים-חיים/בריאות']),
            (Categories.ELECTRICITY, ["חשמל"]),
            (Categories.MISC, ['כהן יצחק','ההחברה לאמנות ולתרבו','דמי כרטיס הנחה','ר.האוכלוסין וההגירה-','החברה לקידום החינוך והתרב','פרומרקטינג וויזרד','רעננה  BTW','2017','מגדל לוינשטיין בע"מ','חלאתי בע"מ','ברגע האחרון' ,'וולקום טכנולוגיות בעמ','פאנקי ', 'לוקר אמבין ', "יהושע בפארק ", 'קורט צבי הולנדר ', 'צורי ובניו', 'קפלה'
                               , 'סקארה', 'השואה', ' המכס', 'סיגר קלאב ', 'רשות הדואר-רכישת מוצר דאר', 'צחי ובנצי עיצוב שיער'] ),
            (Categories.ARNONA, ['עיריית הוד השרון', 'עירית הוד השרון']),
            (Categories.CAR_INSURANCE, ['כלמוביל', 'AIG', 'חובה', ' ביטוח ', 'הפניקס']),
            (Categories.CAR_EXPENSES, ['אחוזת החוף חברה חדשה','מנהרות הכרמל','דניאל פרקינג','אחוזת החוף מפעל הפיס','חניונים', 'חניה', 'רכבת', 'טעינת', 'פנגו', 'חניון', 'GETT', 'איתוראן', 'חניו', 'כביש 6', 'קאר', 'חניוני', 'הרכב','אי.וי.']),
            (Categories.HEALTH_INSURANCE, ['הראל חברה לב-י', 'הפניקס ביטוח', 'מגדל חיים', ' בריאות' ]),
            (Categories.OTHER_INSURANCE, ['הראל-ביטוח דירה',"פסגות", "מנורה ביטוח דירה"]),
            (Categories.GAS, ["סופרגז"]),
            (Categories.FUEL,['מכמורת', 'סונול', 'פז', 'דלק']),
            (Categories.INCOME_TAX, ['מס הכנסה']),
            (Categories.HEALTH_AND_MACABI, ['גוד פארם הוד השרון','בי דראגסטור ככר המוש','מכון מור','IHERB','נקודה בלב נתלי אלקובי','אופטיקה פרקש','מכבידנט', 'מכבי', 'רפואי', 'דראגסטורס', 'מדיקל', 'סופר פארם','רביע','סופר-פארם','פנופארם']),
            (Categories.STARTUP,['CURSOR','GOOGLE HEX', 'GOOGLE STORAGE', 'CHATGPT', ' MEDIUM ', 'GOOGLE DEVSISTERS ', 'TOME.APP', 'CLOUD ', 'GITHUB', 'OPENAI '
                                 , "גאדג'ט טים", 'CLOUD', 'MIDJOURNEY ', 'OPENAI', 'MICROSOFT*STORE ', 'CHATGPT', 'MICROSOFT*PC']),
            (Categories.HUGIM, ['קאנטרי', 'מחול', 'אולדרימס', 'שבט איתן', ' ספורט ', 'אנרגים', 'סטודיו']),
            
            (Categories.CASPOMAT, ["כספומט"]),
           
            (Categories.CLOTHING,['מגדלור','שלי זאנטקרן','את לבני נשים חנות אי','טופ טן','ליאת ומירב כ"ס','DREAM SPORT מתחם  -G','נייקי ישראל - סניף ח','H&M','מרגלית ילדים', 'דרים ספורט', 'קרולינה למקה ', 'S WEAR', 'דלתא', 'רנואר', 'WE SHOSE',
                                'שופרא', 'תינוקי', 'פוקס', 'אירית הראל', 'קסטרו', 'הודיס ', 'ETSY ', 'גולף', 'מקס',
                                  'מיידלה', 'זארה', 'גלי', 'אורבניקה', 'סימפוני' , 'מיננה'  ,'דקטלון']),
            
            (Categories.HOME_RELATED,['המשתלה של קרן','ללין', 'RING', 'א.א חומרי בנין', 'אור לבית', 'אייס כפר סבא', 'אלומה', 'מעבדת השרון'
                                      , 'קיי. אס.פי', 'פרחי שרונים', 'KSP', 'המרכז לבניין',  'מ.נ.מ', 'בריכות ', 'פרחים'
                                      , 'המשתלה', 'איקאה ', ' ELEGANT RADIATORS', 'איקאה', 'וולקום', 'סנט- הייר','קיי אס פי'] ),

            (Categories.INTERNET_SERVICES_AND_SHOPPING, ["KINDLE","MARKETPLACE",'PAYPAL', 'WWW.ALIEXPRES','ALIEXPRESS',"WWW.ALIEXPRESS.COM","AMAZON", "AMZN", "GOOGLE", "amzn","SPOTIFYIL","NETFLIX.COM"]),

            (Categories.FUN_AND_MOVIES, ['סינמה','סינמה סיטי-קופות','זאפה','מקס ', 'ארץ ערבה', 'סטימצקי', 'קופת כרטיסים', ' סינמה' , ' צלילה', ' פינוקים ', 'מוזיאון ישראל', 'היכל התרבות', 'PUZZLEBOX', 'מלון השרון']),
            (Categories.ABROAD_EXPENSES,  ['ADDIS','STORE','SPORT & MODE ZANGERL','שקם דיוטי','AIRBNB', 'HERCULES GREEK', 'SEA LIFE', 'TIN BUILDING', 'HULK CART', 
                                           'CHILL-N', 'BREAD ALONE', 'CICCOLATITALIAN', 'AVIS', ' SUPERCENTER ',
                                           'MIGROSS', 'PRASINI', 'ITALMARK', 'RESTAURANT ALPTRIDA', 'GEMMA PIZZERIA', 'PIGASOS', '3505 PESCHIERA',
                                           "YUKI'S BAKERY", 'DUNKIN', 'VITAEGUSTO', 'ERGON HOUSE', 'LIM*RIDE', 'UBER', 'ELDORADO', 'AMERIKA GAS STATION',
                                           'WOW', 'AVIS', 'MULBERRY', 'VANDERBILT', 'CAPTAIN CANDY', 'FYF*FROMYOUFLOWERS', 'TARGET', 'GRUPPO',
                                           'HM', 'UBER ', 'CAFE  GRAMSCI ', 'ALIEXPRESS', 'SPORT & MODE T', "ZARO'S", 'BONEYARD',
                                           'NIKEPOS_US', 'מגדל ב. כללי נסיעות לחו"ל', 'TIGER HELLAS', 'CIRCLE K ', ' IPMATIC', 'ROADHOUSE',
                                           '1ST COFFEEBIZ', 'GALLO STREET', 'O D A P ','CONAD','OLIVE GARDEN', ' HOSPITALITY', 'MTA', 'TROPICALNEWSST2527',
                                           'SENILRIA', 'SP HONEY BUG', 'TANKSTELLE', 'PASTICCERIA', 'FARMACIA DOTT', 'TST* HAMILTON PORK ',
                                           'BALTHAZAR', 'WIZZ AIR', 'PARK AUTOSILO', 'AIRALO', 'FRESHTOWN#604', 'STUBHUB', 'ERGON ', 'SHAKE SHACK',
                                           'CREMERIA ', 'TAXIS', 'BSPDV', 'KAYAK ', 'AUTOSTRADA ', 'CARIBBEAN KING', 'AGGELMAR EPE',
                                           'IPER', 'FLOCAFE ', 'קניה יזומה לארנק מט"ח', 'SCRIB HUNTER', 'DUFRITAL', 'HARD ROCK',
                                           'THGIL JS', '*YANKEE DOODLE', 'VERONA', 'IDALPE', 'BORGO MONDRAGON', 'ERGON HOUSE', 'FINGEMI',
                                           'MENCHIE 00107029   ', 'IL TORCHIO', 'ROSETTA BAKERY', 'SHAWON', 'BOX LUNCH ', "L'ARTE DEL", 'SPORTS & EMOTIONS',
                                           'LOEWS ROYAL', 'TARGET', '4035 MARKET', 'TST* MAMAN ', 'EL AL', 'CHICK-FIL-A', 'INTERSPAR',
                                           'BENACUS DI BACCOLO ', 'EATALY', 'PATATA', 'YARD HOUSE', 'רשות האוכלוסין וההגירה  ת', 'ERGON',
                                           'PRIMARK ', 'WB STUDIO', 'SQ *MY BUSINESS', 'ERGON', 'WHOLEFDS', 'DISTRIBUTORE AGIP',
                                           'זיכוי מיתרת ארנק מט"ח', 'UBER S', 'SUPERMERCATO', 'MISCUSI', 'BILLA', 'ASPIT DIREZ.', 'BOUGATSADIKO',
                                           'ALFIERI BARDOLINO', 'DUTY FREE', 'SUNRISE ', 'MEAT THE GREEK ', 'ארומה נתבג טרמינל 3',
                                           "ג'יי.אר.-היינמן טרמינל 3", 'SQ *BLANK STREET', 'THE UNDERDOG ', 'MARGATE ', 'HM IT0322',
                                           'ישראייר תעופה בע"מ-צמרת', 'COMUNE ', 'WENDYS ', 'רכישת מט"ח', 'MY STRALI',
                                             'LIDL', 'ZARA', 'PINOTSI', 'CELIO 6332', 'WORLD8.CO.IL'])
        ]

unknown_companies = []

def get_category(company: str) -> Categories:
    """
    Determines the category of a given company based on predefined categorizations.

    Args:
    - company (str): The name of the company to categorize.

    Returns:
    - Categories: The category the company belongs to. Returns Categories.OTHERS if no match is found.
    """
    if company is None:
        return Categories.UNKNOWN
    
    for category, matches in Categorizations:
    
        try:
            if any(match in company for match in matches):
                return category
        except TypeError:
            print(f"Error processing company {company}")
    #save the company name a list of unique unknown companies
    if company not in unknown_companies:
        unknown_companies.append(company)
        with open(".unknown_companies.txt", "a") as f:
            f.write(company + "\n")
            print(f"Unknown category for company {company}")

    return Categories.UNKNOWN


