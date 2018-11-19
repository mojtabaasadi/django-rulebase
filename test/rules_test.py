import os,sys
BASE_DIR = os.path.abspath(__file__ + "/../../django_rulebase")
sys.path.append(BASE_DIR)
from rule import *

#
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
    assert rule.passes('next month') == True
    assert rule.passes("2018-11-19") == False
    
def test_after_or_equal():
    rule = after_or_equal(['2 weeks ago'])
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
    assert rule.passes('a month ago') == True
    assert rule.passes('yesterday') == False
    
def test_before_or_equal():
    rule = before_or_equal(["today"])
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

