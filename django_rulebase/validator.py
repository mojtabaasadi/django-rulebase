from .rule import *
from .rule import _json,_in,_max,_min

class Validator:
    rules = {
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
        "uuid":uuid,
    }
    valid = bool(True)
    errors = dict()

    def run_validation(self,attribute,rules,values):
        rules = self.parse(rules)
        for rule in rules:
            valid = bool()
            rule.set_attribute(attribute)
            rule.set_values(values)
            if hasattr(rule,'parse_condition') and callable(rule.parse_condition):
                rule.parse_condition()
            has_value,value = self.parse_value(attribute,values)
            if "." in attribute:
                rule.parse_value = self.parse_value
                has_value,value = self.parse_value(attribute,values)
            if isinstance(rule,(required,required_if,required_unless,required_with,required_with_all,required_without,required_without_all)):
                rule.parse_value = self.parse_value
                has_value,value = self.parse_value(attribute,values)
                valid = rule.passes() and has_value
            else:
                has_value,value = rule.parse_value(attribute,values)
                if isinstance(value,list):
                    valid = all([rule.passes(v) for v in value])
                else:
                    valid = rule.passes(value)
            message = rule.parse_message(value)
            if not valid:
                if attribute in self.errors:
                    if message not in self.errors[attribute]:
                        self.errors[attribute].append(message)
                else:
                    self.errors[attribute] = [rule.parse_message(value)]
            elif valid and attribute in self.errors and message in self.errors[attribute] :
                self.errors[attribute].remove(message)
                if len(self.errors[attribute])==0: del self.errors[attribute]
            self.valid &= valid    
    
    def parse_value(self,attribute,values):
        " should parse value and collect value or values"
        if "." in attribute:
            _val = values
            childs = attribute.split(".")
            try:
                for ch_i in range(len(childs)):
                    if childs[ch_i]!="*" :
                        if isinstance(_val,dict) and childs[ch_i] in _val:
                            _val = _val[childs[ch_i]]
                        elif isinstance(_val,list):
                            _val = [v[childs[ch_i]] for v in _val]
                return True,_val
            except Exception as e:
                if "KeyError" in str(e): return  False,None
        else :
            if attribute in values:
                return True,values[attribute]
            else:
                return False,None
    
    def parse_rule(self,rule_string):
        if ":" in rule_string:
            _end_n = rule_string.find(":")
            name = rule_string[:_end_n] 
            options = rule_string[_end_n+1:].split(",")
        else :
            name = rule_string
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
        for i in range(len(_rules)):
            if isinstance(_rules[i],str):
                name,options = self.parse_rule(_rules[i])
                try:
                    _rules[i] = self.rules[name](options)
                except Exception as e:
                    if "KeyError" in str(e):raise Exception("{} should be reggitered in this validation".format(name))
            if not isinstance(_rules[i],Rule):
                raise Exception(" {}  is not a valid rule in validation".format(str(_rules[i])))
        return _rules
                    
    def  register_rule(self,name,rule):
        if not isinstance(rule,Rule):
            raise Exception(" rule must be instance of Rule")
        if rule.name in self.rules:
            raise Exception("rule {} already registered".format(rule.name))
        self.rules[rule.name] = rule
