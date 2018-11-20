import os,sys
BASE_DIR = os.path.abspath(__file__ + "/../../django_rulebase")
sys.path.append(BASE_DIR)
from rule import *
from rule import _in,_min,_max,_json

def django_env():
    from django.conf import settings
    filename = os.path.splitext(os.path.basename(__file__))[0]
    dierectory = os.path.abspath(__file__).replace(filename+".py", "")
    settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(dierectory, 'db.sqlite3'),
        }
        }
    )

def test_accepted():
    rule = accepted([])
    assert rule.passes('true') == True
    assert rule.passes(0) == False
    
def test_active_url():
    rule = active_url([])
    assert rule.passes('https://www.tutorialspoint.com') == True
    assert rule.passes('https://www.kavbook.ir') == False
    
def test_after():
    rule = after(['next week'])
    rule.set_values({})
    assert rule.passes('next month') == True
    assert rule.passes("2018-11-19") == False
    
def test_after_or_equal():
    rule = after_or_equal(['2 weeks ago'])
    rule.set_values({})
    assert rule.passes("2 weeks ago") == True
    assert rule.passes("3 weeks ago") == False

def test_alpha():
    rule = alpha([])
    assert rule.passes("randomtext") == True
    assert rule.passes("oh sorry __-9789") == False
    
def test_alpha_dash():
    rule = alpha_dash([])
    assert rule.passes("oaudisad99ds9") == True
    assert rule.passes("\\\\sl;d*&*&%^") == False
    
def test_alpha_num():
    rule = alpha_num([])
    assert rule.passes("Dfdsf3432") == True
    assert rule.passes('--#%#@$ HUUST BANGING on keyboard2348(*&^%$') == False
    
def test_array():
    rule = array([])
    assert rule.passes([]) == True
    assert rule.passes(set([])) == False
    
def test_before():
    rule = before(['last week'])
    rule.set_values({})
    assert rule.passes('a month ago') == True
    assert rule.passes('yesterday') == False
    
def test_before_or_equal():
    rule = before_or_equal(["today"])
    rule.set_values({})
    assert rule.passes("today") == True
    assert rule.passes("in 2 days") == False
    
def test_between():
    rule = between([3,5])
    assert rule.passes(4) == True
    assert rule.passes([4,4]) == False
    
def test_boolean():
    rule = boolean([])
    assert rule.passes(False) == True
    assert rule.passes([True]) == False
    
def test_confirmed():
    rule = confirmed([])
    rule.set_attribute("password")
    rule.set_values({'password_confirmation':"1234"})
    assert rule.passes("1234") == True
    assert rule.passes("453454") == False
    
def test_date():
    rule = date([])
    assert rule.passes("11/19/2018") == True
    assert rule.passes("2018/44/433") == False
    
def test_date_equals():
    rule = date_equals(["field"])
    rule.set_values({"field":"today"})
    assert rule.passes("today") == True
    assert rule.passes("tomorrow") == False


    
def test_date_format():
    rule = date([])
    assert rule.passes("2018/11/19") == True
    assert rule.passes("2018-11-19") == True
    assert rule.passes("19/11/2018") == True
    assert rule.passes("19-11-2018") == True
    assert rule.passes("2DEE20%30SDS") == False
    
def test_different():
    rule = different(['field'])
    rule.set_values({'field':"val"})
    assert rule.passes("val") == False
    rule.set_values({'field':["val"]})
    assert rule.passes(["val"]) == False
    rule.set_values({'field':{"se":"val"}})
    assert rule.passes({"se":"val"}) == False
    assert rule.passes({}) == True
    
def test_digits():
    rule = digits([14])
    assert rule.passes("23094827402948") == True
    assert rule.passes("230948274029481") == False
    assert rule.passes("23e48274029481") == False
    
def test_digits_between():
    rule = digits_between(['5',7])
    assert rule.passes('1458345') == True
    assert rule.passes("12120039") == False
    assert rule.passes("1039") == False

def test_distinct():
    rule = distinct([])
    assert rule.passes([1,2,3,4,5]) == True
    assert rule.passes(["3","3"]) == False
    
def test_email():
    rule = email([])
    assert rule.passes("ceo@awesome.co") == True
    assert rule.passes("super@duper-com") == False
    
def test_exists():
    django_env()
    rule = exists(["test","title"])
    assert rule.passes("some") == True
    assert rule.passes("another") == False

def test_file():
    from django.core.files.uploadedfile import InMemoryUploadedFile
    rule = file()
    assert rule.passes(InMemoryUploadedFile(*[None for i in range(7)])) == True
    assert rule.passes(dict()) == False
    
def test_filled():
    rule = filled()
    assert rule.passes("A") == True
    assert rule.passes("") == False
    
def test_gt():
    rule = gt(['field'])
    rule.set_values({"field":"value"})
    assert rule.passes("valuee") == True
    assert rule.passes("val") == False
    
def test_gte():
    rule = gte(["field"])
    rule.set_values({"field":"value"})
    assert rule.passes("12223") == True
    assert rule.passes("-") == False
    

def test_in():
    rule = _in([2,3,57,"ee"])
    assert rule.passes("ee") == True
    assert rule.passes("57") == False
    
def test_in_array():
    rule = in_array(["field"])
    rule.set_values({"field":[1,3,7,"55"]})
    assert rule.passes(7) == True
    assert rule.passes("5") == False
    
def test_integer():
    rule = integer()
    assert rule.passes(3) == True
    assert rule.passes("3") == False
    
def test_ip():
    rule = ip()
    rule.set_values({})
    rule.set_attribute("aa")
    assert rule.passes("195.168.1.22") == True
    assert rule.passes('195.256.1.22') == False
def test_ipv4():
    rule = ipv4()
    rule.set_values({})
    rule.set_attribute("")
    assert rule.passes("195.168.1.22") == True
    assert rule.passes('195.256.1.22') == False
    
def test_ipv6():
    rule = ipv6()
    rule.set_attribute("")
    rule.set_values({})
    assert rule.passes("195.168.1.22") == True
    assert rule.passes('195.256.1.22') == False
        
def test_json():
    rule = _json()
    assert rule.passes('{"field":"value"}') == True
    assert rule.passes("{'field':'value'}") == False

def test_lt():
    rule = lt(["field"])
    rule.set_values({"field":["s","11"]})
    assert rule.passes(["q"]) == True
    assert rule.passes(["swq","","qqaa"]) == False
    
def test_lte():
    rule = lte(["field"])
    rule.set_values({"field":["s","11"]})
    assert rule.passes(["q",2]) == True
    assert rule.passes(["swq","qqaa",'']) == False
    
# def test_max():
#     rule = _max()
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_mimetypes():
#     rule = mimetypes()
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_mimes():
#     rule = mimes()
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_nullable():
#     rule = nullable([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_numeric():
#     rule = numeric([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_present():
#     rule = present([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_regex():
#     rule = regex([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required():
#     rule = required([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_if():
#     rule = required_if([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_unless():
#     rule = required_unless([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_with():
#     rule = required_with([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_with_all():
#     rule = required_with_all([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_without():
#     rule = required_without([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_required_without_all():
#     rule = required_without_all([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_same():
#     rule = same([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_size():
#     rule = size([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_string():
#     rule = string([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_timezone():
#     rule = timezone([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_unique():
#     rule = unique([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_url():
#     rule = url([])
#     assert rule.passes() == True
#     assert rule.passes == False
    
# def test_uuid():
#     rule = uuid([])
#     assert rule.passes() == True
#     assert rule.passes == False
