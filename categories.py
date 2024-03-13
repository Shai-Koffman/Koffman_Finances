#! python
# -*- coding: utf-8 -*-
from enum import Enum, auto

class Categories(Enum):
    SUPER = auto()
    ELECTRICITY = auto()
    INTERNET_AND_PHONES = auto()
    OTHER_FOOD = auto()
    RESTOURANTS_AND_HOTELS = auto()
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
    HUGIM = auto()
    INVESTMENTS = auto()
    CASPOMAT = auto()
    CLOTHING = auto()
    PRESENTS = auto()
    AMAZON_AND_GOOGLE = auto()
    ABROAD_EXPENSES = auto()
    VISA = auto()
    CHECKS = auto()
    BANK_AMLOT = auto()
    FUN_AND_MOVIES = auto()
    OTHERS = auto()

# Categorizations - list of tuples, each tuple contains a category and a list of strings that are the names of the expenses that belong to this category
Categorizations = [
            (Categories.SUPER,
             ["םניח", " רפוס", "לסרפוש", "ףוננחוי", "ןתיב תוניי", "MP MA", "MP:MA", "יול ימר", "םעט ביט",
              "תואנועמק הגמ", "הננער קוש", "ןורשה טקרמפוטס", "לבוי זילטא"]),
              

            (Categories.ELECTRICITY, ["למשח"]),
            (Categories.INTERNET_AND_PHONES, ["TOH"]),
            (Categories.OTHER_FOOD,
             ["תייפאמ", "םחל", "ןידלור", "הפאמ", "םימחל", "וסרפסנ", "הטספ הל", "היילק", "זילטיא", "רכיכה תילק",
              "הננער תימע", "וגוט", "HSIF RM","ימימ"]),
            (Categories.RESTOURANTS_AND_HOTELS,
             ["הניל'גנא", "איצרג", "המלא", "דלישטור", "הדלוג", "והיתתמ", "היישוסה", "יצימ", "הנינמחל", "טרוגוי",
              "הלדנח", "ןשייטסיפוק", "הדנ'גל", "רוודנל", "ףר'יג", "NEHCTIK", "ONON", "םירק ילד", "למרק הפק", "הרבוזוז",
              "הני'צוק", "ALLEB AZZIP", "ןנוג יפונ", "2 בולוקוס", "beer garden", "טקידנב", "ופמופולופוט", "טאה הציפ",
              "יאתבש", "דליוו רקסוא", "המרוג הפק", "אמרכ", "הרגלא", "הדוינחמ",'546שי אוביב.שת']),
            (Categories.WATER, ["ןורשה דוה ימ", "4 ימת"]),
            (Categories.ARNONA, ["ןורשה דוה תייריע"]),
            (Categories.CAR_INSURANCE, ["סקינפה"]),
            (Categories.CAR_EXPENSES, ["תונוישר", "רטמומניד"]),
            (Categories.HEALTH_INSURANCE, ["לדגמ", "חוטיב-לארה", "חוטיב-GIA", "תואירבו םייח סקינפ"]),
            (Categories.OTHER_INSURANCE, ["תוגספ", "הריד חוטיב הרונמ"]),
            (Categories.GAS, ["זגרפוס"]),
            (Categories.FUEL,
             ["קלד", "ןולא רוד", "ןט", "לונוס", "/זפ", "קלד", "/WOLLEYזפ", "ךרבא הנוי", "סורוטומ טנירפס", "WOLLEY זפ","הכאלמה טנירפס", "/ זפ", "רוגח זפ"]),
            (Categories.INCOME_TAX, ['הסנכה סמ']),
            (Categories.HEALTH_AND_MACABI, ["יבכמ", "ינאה עיבר רד", "הילצרה םראפ-רפוס", "הידפוטרופס", "הרואל 'רד", "םראפרפוס","םראפונפ"]),
            (Categories.SCHOOLS, ["ךוניח", "ןיטילש ןג", "ןורהצ- םודיקל הרבחה", "asa","םיצוביקה רנימס"]),
            (Categories.HUGIM, ["רוד זכרמ", "הכלממה"]),
            (Categories.INVESTMENTS, ["םייח חוטיב - םיחטבמ הרונמ", "תורדתסה"]),
            (Categories.CASPOMAT, ["טמופסכ"]),
            (Categories.CLOTHING,
             ["וגנמ", "והוס", "זיירוססקא", "FLOG", "ורטסק", "סדיק-יימ", "ילענ", "סידוה", "לטילא", "הלדיימ", "יול תירש",
              "וילס", "M&H", "האדיא", "שימ§ שימ", "התלד", "הנפוא תשר טקלס", "טראוד", "סקופ","ץורע יבליב", "םירפרפ",
              "ירצומ-יקונית", "רב דנא לופ","ןונמת", "ינועבצ", "אתלד","ברימו תאיל","לגיא ןקירמא" ]),
            (Categories.PRESENTS, ["םיעושעשה רפכ", "טאריפה", "יוט", "תמוצ", "תונתמה", "ןד הרוא", "יקצמיטס", "םיעוצעצה", "גאב", "יקית", "7 אפס"]),
            (Categories.AMAZON_AND_GOOGLE, ["NOZAMA", "SU LLIB/MOC.NZMA", "ELGOOG", "SU stmp/moc.nzma", "LAPYAP"]),
            (Categories.VISA, ['י-מ"עב טרכארשי',"הזיו ימואל", "י-ב דראק ימואל", 'י-נניפ טיא סקמ']),
            (Categories.CHECKS, ["קיש"]),
            (Categories.BANK_AMLOT, ['11 שי ץורע.למע','טנרטניא תויושר','טנרטניא תויושר','31 שי ץורע.למע','טנרטניא-הינק','טנרטניא-הרמה','41 שי ץורע.למע','91 שי ץורע.למע','546ורש אובי.מע','9 שי ץורע.למע','007יגיד הרבעה','01 שי ץורע.למע','007טניא .עה','7 שי ץורע.למע','טנרטניא הרמה','546 ח"טמ תרבעה',"007טנרטניא .עה", "696הדקפה/הרבעה","21 שי ץורע.למע",'ע"ינ לוהינ ימד', '546טמ תרבעה.מע' ]),
            (Categories.FUN_AND_MOVIES, ["םיקוניפ","המניס", "גנילואב" ])
        ]

def get_category(company: str) -> Categories:
    """
    Determines the category of a given company based on predefined categorizations.

    Args:
    - company (str): The name of the company to categorize.

    Returns:
    - Categories: The category the company belongs to. Returns Categories.OTHERS if no match is found.
    """
    for category, matches in Categorizations:
        if any(match in company for match in matches):
            return category
    return Categories.OTHERS
