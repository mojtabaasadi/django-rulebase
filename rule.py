from django.core.files.uploadedfile import InMemoryUploadedFile
import re,json,datetime,pytz
import dns.resolver
from uuid import UUID
from dateparser import parse
from django.db import connection


# should find better way to parse rules and options

class Rule:
    """
    rule object for construction provide options as list Rule(options)
    """
    values = dict()
    name = "Rule"
    attribute = ""
    def __init__(self,options):
        if options is None or (not isinstance(options,str) and not isinstance(options,list)):
            raise Exception("options should be a valid")
        else:
            self.options = options.split(",") if isinstance(options,str) else options
    
    def passes(self,value):
        return False
    
    def parse_value(self,attribute,values):
        return attribute in values , values[attribute] if attribute in values else None
    
    def message(self):
        return " validation error for {attribute} because of {rule} "
    
    def set_attribute(self,attribute):
        if attribute is None or not isinstance(attribute,str) :
            raise Exception("attribute should be a valid name")
        else:
            self.attribute = attribute
    
    def set_values(self,values):
        if values is None or (not isinstance(values,dict) and not ("required" in self.name and isinstance(values,list))) :
            raise Exception("values should be a valid")
        else:
            self.values = values

    def parse_message(self,value):
        return self.message().format(**{
            'rule':self.name,
            'attribute':self.attribute,
            'options':self.options,
            'value':value
        })

class accepted(Rule):
    """
    The field under validation must be yes, on, 1, or true. This is useful for validating "Terms of Service" acceptance.
    """
    name = "accepted"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return value in ["1",1,"yes","on",True,"true"]


class active_url(Rule):
    """The field under validation must have a valid A or AAAA record according to the 
        (pythondns)[http://www.dnspython.org/examples.html] module """
    name = "active-url"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
        domain = re.search(regex,value).group(1)
        return len(dns.resolver.query(domain,'NS'))>0
        


class after(Rule):
    """The field under validation must be a value after a given date.
    The dates will be passed into (dateparser)[] parse method"""
    
    name = "after"
    def passes(self,value):
        try:
            has_val,val = self.parse_value(self.options[0],self.values)
            if not has_val:val = self.options[0]
            return parse(value) > parse(val)
        except Exception as e:
            raise e
            return False


class after_or_equal(Rule):
    """The field under validation must be a value after or equal to the given date"""

    name = "after-or-equal"
    def passes(self,value):
        try:
            return parse(value) > parse(self.values[self.options[0]])
        except Exception as e :
            raise e
            return False

class alpha(Rule):
    "The field under validation must be entirely alphabetic characters."
    name = "alpha"
    def passes(self,value):
        return value.isalpha()


class alpha_dash(Rule):
    """
        The field under validation may have alpha-numeric characters,
        as well as dashes and underscores.
    """
    name = "alpha-dash"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        value = value.replace('-','').replace("_",'')
        return value.isalnum()


class alpha_num(Rule):
    """
        The field under validation must be entirely alpha-numeric characters.
    """
    name = "alpha-num"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return value.isalnum()


class array(Rule):
    "The field under validation must be a list or tuple"
    name = "array"
    def passes(self,value):
        return isinstance(value,list) or isinstance(value,tuple)


class before(Rule):
    """The field under validation must be a value preceding the given date.
       The dates will be passed into the dateparser module. In addition, like the 'after' rule,
       the name of another field under validation may be supplied as the value of 'date'.
    """ 
    name = "before"
    def message(self):
        return "must be before {options[0]}"
    def passes(self,value):
        try:
            has_val,val = self.parse_value(self.options[0],self.values)
            if not has_val : val=self.options[0]
            return parse(value) < parse(val)
        except :
            return False


class before_or_equal(Rule):
    """The field under validation must be a value preceding or equal to the given date.
         The dates will be passed into the dateparser module. In addition, like the 'after' rule,
         the name of another field under validation may be supplied as the value of 'date'.""" 
    name = "before-or-equal"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.values[self.options[0]]
    def passes(self,value):
        return parse(value) <= parse(self.cond)


class between(Rule):
    """The field under validation must have a size between the given min and max.
         Strings, numerics, arrays, and files are evaluated in the same fashion as the "size"
          rule."""
    name = "between"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.options[0],self.options[1]
    def passes(self,value):
        min,max = self.cond
        if isinstance(value,int):
            return value <= int(max) and value >= int(min)
        elif isinstance(value,InMemoryUploadedFile):
            return value.size/1000>=min and value.size/1000<=max
        elif isinstance(value.list) or isinstance(value,str):
            return len(value) >= min and len(value) <= max
        else:
            return False


class boolean(Rule):
    """
        The field under validation must be able to be cast as a boolean.
         Accepted input are true,  false, 1, 0, "1", and "0".
    """
    name = "boolean"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return isinstance(value,bool) or value in ["0",0,"1",1]


class confirmed(Rule):
    """
        The field under validation must have a matching field of foo_confirmation.
         For example, if the field under validation is password, a matching
          password_confirmation field must be present in the input.
    """
    name = "confirmed"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        try:
            return value == self.values[ self.attribute + '_confirmation']
        except :
            return False


class date(Rule):
    """
        The field under validation must be a correct according 
        to dateparser module
    """
    name = "date"
    def message(self):
        return self.__doc__.replace("The field under validation","")

    def passes(self,value):
        return isinstance(parse(value),datetime.datetime)


class date_equals(Rule):
    """
        The field under validation must be equal to the given date.
         The dates will be passed into the PHP strtotime function
    """
    name = "date-equals"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.values[self.options[0]]
    def passes(self,value):
        return parse(self.cond) == parse(value)



class different(Rule):
    "The field under validation must have a different value than field."
    name = "different"
    def passes(self,value):
        return self.values[self.options[0]] != value


class digits(Rule):
    "The field under validation must be numeric and must have an exact length of value."
    name = "digits"
    def parse_condition(self):
        self.cond = self.options['value']
    def passes(self,value):
        return (value.isdigit() or isinstance(value ,int)) and len(str(value)) == self.cond
    
class digits_between(Rule):
    "The field under validation must have a length between the given min and max."
    name = "digits-between"
    def parse_condition(self):
        self.cond = self.options['min'],self.options['max']
    def digits_between(self,value):
        return (value.isdigit() or isinstance(value ,int)) and len(str(value)) >= self.cond[0]  and len(str(value)) <= self.cond[1]



class distinct(Rule):
    "When working with arrays, the field under validation must not have any duplicate values."
    name = "distinct"
    def passes(self,value):
        return isinstance(value,list) and len(value) == len(list(set(value)))


class email(Rule):
    "The field under validation must be formatted as an e-mail address."
    name = "email"
    def passes(self,value):
        reg = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        rr = regex([reg])
        rr.set_attribute(self.attribute)
        rr.set_values(self.values)
        return rr.passes(value)

class exists(Rule):
    """
        The field under validation must exist on a given database table.
        If the 'column' option is not specified, the field name will be used.
    """
    name = "exists"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.options['table'],self.options['column']
    def passes(self,value):
        table = self.cond[0]
        column = self.cond[1] if self.cond[1] != None else 'name'
        cr = connection.cursor()
        cr.execut("select * from {} where {}={}".format(table,column,
            value if not isinstance(value,str) else "'"+value+"'"))


class file(Rule):
    "The field under validation must be a successfully uploaded file."
    name = "file"
    def passes(self,value):
        return isinstance(value,InMemoryUploadedFile)

class filled(Rule):
    "The field under validation must not be empty when it is present."
    name = "filled"
    def passes(self,value):
        return value is not None and value!=""


class gt(Rule):
    """
        The field under validation must be greater than the given field.
        The two fields must be of the same type. Strings, numerics, arrays,
        and files are evaluated using the same conventions as the  'size' rule.
    """

    name = "gt"
    def passes(self, value):
        try:
            if isinstance(value, int):
                return value > int(self.values[self.options[0]])
            elif isinstance(value, InMemoryUploadedFile):
                return value.size/1000 > self.values[self.options[0]]/1000
            elif isinstance(value.list) or isinstance(value, str):
                return len(value) > len(self.values[self.options[0]])
            else:
                return False
        except :
            return False

class gte(Rule):
    """
        The field under validation must be greater than or equal to the given field.
        The two fields must be of the same type.
        Strings, numerics, arrays, and files are evaluated using the same conventions as the 'size' rule.
    """
    name = "gte"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        try:
            if isinstance(value, int):
                return value >= int(self.values[self.options[0]])
            elif isinstance(value, InMemoryUploadedFile):
                return value.size/1000 >= self.values[self.options[0]]/1000
            elif isinstance(value.list) or isinstance(value, str):
                return len(value) >= len(self.values[self.options[0]])
            else:
                return False
        except Exception as e:
            raise e
            return False


class image(Rule):
    """
        The file under validation must be an image (jpeg, png, bmp, gif, or svg)
    """
    name = "image"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        for m_t in ['jpg','png','bmp','tiff','jpeg','gif','svg']:
            if m_t in value.content_type:
                return True
        return False


class _in(Rule):
    """
        The field under validation must be included in the given list of values.
        Since this rule often requires you to implode an array,
        the Rule::in method may be used to fluently construct the rule:
    """
    name = "in"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return value in self.options['values']


class in_array(Rule):
    
    """
        The field under validation must exist in anotherfield's values.
    """
    name = "in-array"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        try:
            return value in self.values[self.options[0]]
        except Exception as e:
            raise e
            return False


class integer(Rule):
    "The field under validation must be an integer."
    name = "integer"
    def passes(self,value):
        return isinstance(value,int)


class ip(Rule):
    "The field under validation must be an IP address."
    name = "ip"
    def passes(self,value):
        r = list()
        for ii in (ipv4,ipv6):
            ii([])
            ii.set_attribute(self.attribute)
            ii.set_values(self.values)
            r.append(ii.passes(value))
        return all(r)


class ipv4(Rule):
    "The field under validation must be an IPv4 address."
    name = "ipv4"
    def passes(self,value):
        reg = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        rr = regex([reg])
        rr.set_attribute(self.attribute)
        rr.set_values(self.values)
        return rr.passes(value)


class ipv6(Rule):
    "The field under validation must be an IPv6 address."
    name = "ipv6"
    def passes(self,value):
        reg = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        rr = regex([reg])
        rr.set_attribute(self.attribute)
        rr.set_values(self.values)
        return rr.passes(value)


class _json(Rule):
    "The field under validation must be a valid JSON string."
    name = "json"
    def json(self,value):
        try:
            json.loads(value)
            return True
        except Exception as e:
            raise e
            return False
   
   
class lt(Rule):
    """
        The field under validation must be less than the given field.
        The two fields must be of the same type. Strings, numerics, arrays, 
        and files are evaluated using the same conventions as the 'size' rule.
    """
    name = "lt"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        if isinstance(value,int):
            return  value < int(self.values[self.options[0]])
        elif isinstance(value,InMemoryUploadedFile):
            return value.size/1000 < self.values[self.options[0]]/1000
        elif isinstance(value.list) or isinstance(value,str):
            return len(value) < len(self.values[self.options[0]]) 
        else:
            return False
    
    
class lte(Rule):
    """
        The field under validation must be less than or equal to the given field.
        The two fields must be of the same type.
        Strings, numerics, arrays, and files are evaluated using the same
        conventions as the size rule.
    """
    name = "lte"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        try:
            if isinstance(value,int):
                return  value <= int(self.values[self.options[0]])
            elif isinstance(value,InMemoryUploadedFile):
                return value.size/1000 <= self.values[self.options[0]]/1000
            elif isinstance(value.list) or isinstance(value,str):
                return len(value) <= len(self.values[self.options[0]]) 
            else:
                return False
        except Exception as e:
            raise e
            return False
            
    
    
class _max(Rule):
    """
        The field under validation must be less than or equal to a maximum value.
        Strings, numerics, arrays, and files are evaluated
        in the same fashion as the size rule.
    """
    name = "max"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        if isinstance(value,int):
            return  value <= self.options[0]
        elif isinstance(value,InMemoryUploadedFile):
            return value.size/1000 <= self.options[0]
        elif isinstance(value.list) or isinstance(value,str):
            return len(value) <= self.options[0]
        else:
            return False


class mimetypes(Rule):
    "The file under validation must match one of the given MIME types:"
    name = "mimetypes"
    def parse_condition(self):
        self.cond = self.options
    def passes(self,value):
        return isinstance(value,InMemoryUploadedFile) and value.content_type in self.cond


class mimes(Rule):
    name = "mimes"
    def passes(self,value):
        "The file under validation must have a MIME type corresponding to one of the listed extensions."
        return value.content_type in self.options
        


class _min(Rule):
    """
        The field under validation must have a minimum value. Strings, numerics, arrays, 
        and files are evaluated in the same fashion as the size rule.
    """
    name = "min"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.options[0]
    def passes(self,value):
        if isinstance(value,int):
            return  value >= self.cond
        elif isinstance(value,InMemoryUploadedFile):
            return value.size/1000 >= self.cond 
        elif isinstance(value.list) or isinstance(value,str):
            return len(value) >= self.cond 
        else:
            return False
          


class not_in(Rule):
    """
        The field under validation must not be included in the given list of values.
        The Rule()  may be used to fluently construct the rule:
    """
    name = "not-in"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.options
    def passes(self,value):
        return value not in self.cond


class not_regex(Rule):
    "The field under validation must not match the given regular expression."
    name = "not-regex"
    def passes(self,value):
        return re.search(self.options[0],value) is None


class nullable(Rule):
    name = "nullable"
    def passes(self,value):
        """
        The field under validation may be null.
        This is particularly useful when validating primitive
        such as strings and integers that can contain null values.
        """
        return value or value == ""  or value is None or value == 0


class numeric(Rule):
    name = "numeric"
    def passes(self,value):
        "The field under validation must be numeric."
        return value.isdigit()


class present(Rule):
    name = "present"
    def passes(self,value):
        "The field under validation must be present in the input data but can be empty."
        return value or True


class regex(Rule):
    "The field under validation must match the given regular expression."
    name = "regex"
    def parse_condition(self):
        self.cond = self.options[0]
    def passes(self,value):
        return re.search(self.cond,value) is not None


class required(Rule):
    """
        The field under validation must be present in the input data and not empty.
        A field is considered "empty" if one of the following conditions are true:
        The value is null.
        The value is an empty string.
        The value is an empty array or empty Countable object.
        The value is an uploaded file with no path.
    """
    name = "required"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self):
        if isinstance(self.values,dict):
            return self.parse_value(self.attribute,self.values)[0]
        else:
            return all([self.attribute in v for v in  self.values])


class required_if(Rule):
    """
        The field under validation must be present and not empty 
        if the anotherfield field is equal to any value.
    """
    name = "required-if"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    
    
    def parse_condition(self):
        self.cond = list()
        for i in range(len(self.options)):
            if i % 2 == 0 and i+1 != len(self.options):
                self.cond.append((self.options[i],self.options[i+1])) 
    
    def passes(self):
        try:
            return sum([1 if self.parse_value(i[0],self.values)[1] == i[1] else 0 for i in self.cond]) == len(self.cond)
        except :
            return False


class required_unless(Rule):
    """
        The field under validation must be present and not empty 
        unless the anotherfield field is equal to any value.
    """
    name = "required-unless"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    
    def parse_condition(self):
        self.cond = list()
        for i in range(len(self.options)):
            if i % 2 == 0 and i+1 != len(self.options):
                self.cond.append((self.options[i],self.options[i+1]))
    
    def passes(self):
        try:
            return not all([self.parse_value(i[0],self.values)[0] == i[1] for i in self.cond])
        except :
            return False


class required_with(Rule):
    """
        The field under validation must be present and not empty only 
        if any of the other specified fields are present.
    """
    name = "required-with"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self):
        try:
            return sum([1 if self.parse_value(i,self.values) else 0  for i in self.options]) > 0
        except :
            return False


class required_with_all(Rule):
    """The field under validation must be present and not empty {options} are present."""
    name = "required-with-all"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self):
        try:
            return sum([1 if self.parse_value(i,self.values)[0] else 0  for i in self.options]) == len(self.options)
        except :
            return False


class required_without(Rule):
    """
        The field under validation must be present and not empty
        only when any of the other specified fields are not present.
    """
    name = "required-without"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def parse_condition(self):
        self.cond = self.options
    def passes(self,value):
        try:
            return sum([1 if not self.parse_value(i)[0] else 0  for i in self.options]) > 0
        except :
            return False


class required_without_all(Rule):
    """
        The field under validation must be present and not empty only when all
        of the other specified fields are not present.
    """
    name = "required-without-all"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        try:
            return sum([1 if not self.parse_value(i,self.values)[0] else 0  for i in self.options]) == len(self.options)
        except :
            return False


class same(Rule):
    "The given field must match the field under validation."
    name = "same"
    def passes(self,value):
        o_i,o_v = self.parse_value(self.options[0],self.values)
        return o_i and value == o_v


class size(Rule):
    """
        The field under validation must have a size matching the given value.
        For string data, value corresponds to the number of characters.
        For numeric data, value corresponds to a given integer value.
        For an array, size corresponds to the count of the array. For files, 
        size corresponds to the file size in kilobytes.
    """
    name = "size"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        if isinstance(value,int):
            return  value == self.options[0]
        elif isinstance(value,InMemoryUploadedFile):
            return value.size/1000 == self.options[0] 
        elif isinstance(value.list) or isinstance(value,str):
            return len(value) == self.options[0] 
        else:
            return False



class string(Rule):
    """
        The field under validation must be a string.
        If you would like to allow the field to also be null, 
        you should assign the nullable rule to the field.
    """
    name = "string"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return isinstance(value,str)


class timezone(Rule):
    """
        The field under validation must be a valid timezone identifier 
        according to the pytz module
    """
    name = "timezone"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        return value in pytz.all_timezones


class unique(Rule):
    """
        The field under validation must be unique in a given database table. 
        If the column option is not specified, the field name will be used.
    """
    name = "unique"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        table = self.options[0]
        column = self.options[1] if self.options[1] != None else 'name'
        cr = connection.cursor()
        cr.execute("select * from {} where {}={}".format(table,column,
            value if not isinstance(value,str) else "'"+value+"'"))
        return len(cr.fetchall()) == 1


class url(Rule):
    "The field under validation must be a valid URL."
    name = "url"
    def passes(self,value):
        reg = r"^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:[/?#]\S*)?$"
        return regex(self.attribute,[reg],None).passes(value)


class uuid(Rule):
    """
        The field under validation must be a valid RFC 4122 
        (version 1, 3, 4, or 5) universally unique identifier (UUID).
    """
    name = "uuid"
    def message(self):
        return self.__doc__.replace("The field under validation","")
    def passes(self,value):
        for i in range(1,6):
            try:
                UUID(value, version=i)
                return True
            except:
                pass
        return False
