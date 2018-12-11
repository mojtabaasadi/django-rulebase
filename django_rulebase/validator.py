from .rule import *
from .rule import _json,_in,_max,_min,_uuid
from django.core.handlers.wsgi import WSGIRequest
import json
from django.http import JsonResponse

builtin_rules = {
    "accepted":accepted,
    "active-url":active_url,
    "after":after,
    "after-or-equal":after_or_equal,
    "alpha":alpha,
    "alpha-dash":alpha_dash,
    "alpha-num":alpha_num,
    "array":array,
    "before":before,
    "before-or-equal":before_or_equal,
    "between":between,
    "boolean":boolean,
    "confirmed":confirmed,
    "date":date,
    "date-equals":date_equals,
    "different":different,
    "digits":digits,
    "digits-between":digits_between,
    "distinct":distinct,
    "email":email,
    "exists":exists,
    "file":file,
    "filled":filled,
    "gt":gt,
    "gte":gte,
    "image":image,
    "in":_in,
    "in-array":in_array,
    "integer":integer,
    "ip":ip,
    "ipv4":ipv4,
    "ipv6":ipv6,
    "json":_json,
    "lt":lt,
    "lte":lte,
    "max":_max,
    "mimetypes":mimetypes,
    "mimes":mimes,
    "min":_min,
    "not-in":not_in,
    "not-regex":not_regex,
    "nullable":nullable,
    "numeric":numeric,
    "present":present,
    "regex":regex,
    "required":required,
    "required-if":required_if,
    "required-unless":required_unless,
    "required-with":required_with,
    "required-with-all":required_with_all,
    "required-without":required_without,
    "required-without-all":required_without_all,
    "same":same,
    "size":size,
    "string":string,
    "timezone":timezone,
    "unique":unique,
    "url":url,
    "uuid":_uuid,
}

def parse_rule_name(rule):
    if ":" in rule:
        return rule[:rule.find(":")]
    else:
        return rule

def is_rule_valid(rule):
    valid = True
    if isinstance(rule,str):
        valid &= all([parse_rule_name(ar) in builtin_rules for ar in rule.split("|") ])
    elif isinstance(rule,list):
        valid &= all([is_rule_valid(rl) for rl in rule])
    else:
        valid &= isinstance(rule,Rule)
    if not valid: raise Exception("Seems rule '{}' is not known rule or maybe its not a valid custom rule".format(rule))
    return valid


def is_rules_valid(rules):
    valid = isinstance(rules,dict)
    for attr,rule in rules.items():
        valid &= is_rule_valid(rule)
    return valid
        
def parse_request(request):
    if "json" in request.content_type:
        data = json.loads(request.body.decode("utf-8"))
    else:
        data = dict(getattr(request,request.method))
    if len(request.FILES.keys())>0:
        for key in request.FILES.keys():
            data[key] = request.FILES[key]
    return data


class Validator:
    valid = bool(True)
    errors = None
    rules = dict()
    
    def __init__(self, rules):
        is_rules_valid(rules)
        for key in rules.keys():
            self.rules[key] = self.parse(rules[key])
                 
    def run_validation(self,values):
        valid_all = dict()
        errors = dict()
        for attribute,rules in self.rules.items():
            for rule in rules:
                valid = bool()
                rule.set_attribute(attribute)
                rule.set_values(values)
                if hasattr(rule,'parse_condition') and callable(rule.parse_condition):
                    rule.parse_condition()
                has_value,value = rule.parse_value(attribute)
                if isinstance(rule,(present,required,required_if,required_unless,required_with,required_with_all,required_without,required_without_all)):
                    valid = rule.passes()
                else:
                    if isinstance(value,list) and "*" in rule.attribute :
                        valid = all([rule.passes(v) for v in value])
                    else:
                        valid = rule.passes(value)
                message = rule.parse_message(value)
                if not valid:
                    if attribute in errors:
                        if message not in errors[attribute]:
                            errors[attribute].append(message)
                    else:
                        errors[attribute] = [rule.parse_message(value)]
                elif valid and attribute in errors and message in errors[attribute] :
                    errors[attribute].remove(message)
                    if len(errors[attribute])==0: del errors[attribute]
                self.valid &= valid
            valid_all[attribute] = valid

        if len(errors.keys())>0:
            self.errors = errors
        
        return valid_all
      
    def parse_rule(self,rule_string):
        name = parse_rule_name(rule_string)
        if ":" in rule_string:
            _end_n = rule_string.find(":")
            options = [rule_string[_end_n + 1:]]
        else :
            options = []
        return name,options
    
    def parse(self,rules):
        _rules = []
        if isinstance(rules,str):
            _rules = rules.split("|")
        elif isinstance(rules,list):
            for rule in rules:
                if isinstance(rule,str) and "|" in rule :
                    _rules += rule.split("|")
                else:
                    _rules += [ rule ]
        elif isinstance(rules,Rule):
            _rules = [rules]

        for i in range(len(_rules)):
            if isinstance(_rules[i],str):
                name,options = self.parse_rule(_rules[i])
                try:
                    _rules[i] = builtin_rules[name](*options)
                except Exception as e:
                    if "KeyError" in str(e):raise Exception("{} should be registered in this validation".format(name))
            if not isinstance(_rules[i],Rule):
                raise Exception(" {}  is not a valid rule in validation".format(str(_rules[i])))
        return _rules


def require_validation(rules):
    is_rules_valid(rules)
    def dec(func):
        def vv(*args, **kwargs):
            request = [arg for arg in args if isinstance(arg,WSGIRequest)][0]
            data = parse_request(request)
            v = Validator(rules)
            v.run_validation(data)
            if v.valid:
                return func(*args, **kwargs)
            else:
                return JsonResponse(v.errors,safe=False)
        return vv
    return dec