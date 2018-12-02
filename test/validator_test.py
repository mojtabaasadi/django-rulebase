from rules_test import *


def test_validation():
    rules = {
        'field1':"required|integer",
        'field2':"required-if:field1,1|integer|exists:test,id",
        'field3':"required-unless:field1,1|email",
        'field4':"required-with:field1,field2|url",
        'field5':"required-with-all:field1,field2|nullable|string",
        'field6':"required-without:field0,field18|accepted",
        'field7':"required-without-all:field19,field20|alpha-dash",
        'field8':"date|after:yesterday|before:tomorrow|after-or-equal:today|before-or-equal:now",
        'field9':"alpha-num|confirmed",
        'field9':"digits-between:3,4|digits:3|numeric",
        'field10':"gt:field2|lt:field1|gte:field2|lte:field1",
        'field11':"size:10|min:6|max:11",
        'field12':"not-regex:^[0-5]$|in:877,788,879,967",
        'field13':"regex:[0-5]{1,3}.[0-5]{1,3}.[0-5]{1,3}.[0-5]{1,3}|ip",
        "field14":"present|same:field2",
        "field15":"timezone|not-in:Asia/Riyadh,Asia/Tehran,Asia/Qatar,Asia/Muscat,Asia/Dubai",
        "field16":"array|distinct|max:5",
        "field17":"boolean|different:field6",
        "field18":"active-url",
    }
    data = {
        'field1':3,
        'field2':1,
        'field3':"ww@some.com",
        'field4':"https://www.linkedin.com/feed/",
        'field5':"",
        'field6':1,
        'field7':"required-without-allfield3_field2alpha-dash",
        'field8':"now",
        'field9':"alpha3454numconfirmed",
        'field9_confirmation':"alpha3454numconfirmed",
        'field9':"475",
        'field10':2,
        'field11':10,
        'field12':"967",
        'field13':"123.234.102.1",
        "field14":1,
        "field15":"Pacific/Truk",
        "field16":["aa",2,45,dict()],
        "field17":False,
        "field18":"https://github.com/mojtabaasadi/django-rulebase#sizevalue",
    }
    validator = Validator(rules)
    validator.run_validation(data)
    assert validator.valid == True
