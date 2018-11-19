
  

# Django Rule-base Validator
for making django validations painless


#### to use:
in app.views:
```python
from django.http import HttpResponse,HttpResponseBadRequest
from django-rulebase import Request  

def  good_request(request,is_valid,errors):
	if is_valid:return HttpResponse("good request")
	return HttpResponseBadRequest(errors['date'])
   
class  CustomeRequest(Request):
	view = good_request
	def  rules(self):
		return {
			"date":"date|required|before:tomorrow|after:yesterday"
			}
```
in app.urls
```python
from django.conf.urls import url
from .views import CustomeRequest  
urlpatterns = [
	url(r'^validate/$', CustomeRequest.asView()),
]
```  
  

# built-in rules
Below is a list of all available validation rules and their function:

rule|rule|rule
---|---|---
[Accepted](#accepted)|[Active URL](#active-url)|[After (Date)](#after)
[After Or Equal (Date)](#after_or_equal)|[Alpha](#alpha)|[Alpha Dash](#alpha_dash)
[Alpha Numeric](#alpha_num)|[Array](#array)|[Before (Date)](#before)
[Before Or Equal (Date)](#before_or_equal)|[Between](#between)|[Boolean](#boolean)
[Confirmed](#confirmed)|[Date](#date)|[Date Equals](#date_equals)
[Date Format](#date_format)|[Different](#different)|[Digits](#digits)
[Digits Between](#digits_between)|[Distinct](#distinct)|[E_Mail](#email)
[Exists (Database)](#exists)|[File](#file)|[Filled](#filled)
[Greater Than](#gt)|[Greater Than Or Equal](#gte)|[Image (File)](#image)
[In](#in)|[In Array](#in_array)|[Integer](#integer)
[IP Address](#ip)|[JSON](#json)|[Less Than](#lt)
[Less Than Or Equal](#lte)|[Max](#max)|[MIME Types](#mimetypes)
[MIME Type By File Extension](#mimes)|[Min](#min)|[Not In](#not_in)
[Not Regex](#not_regex)|[Nullable](#nullable)|[Numeric](#numeric)
[Present](#present)|[Regular Expression](#regex)|[Required](#required)
[Required If](#required_if)|[Required Unless](#required_unless)|[Required With](#required_with)
[Required With All](#required_with_all)|[Required Without](#required_without)|[Required Without All](#required_without_all)
[Same](#same)|[Size](#size)|[String](#string)
[Timezone](#timezone)|[Unique (Database)](#unique)|[URL](#url)
[UUID](#uuid)| - | -
  

### accepted

The field under validation must be yes, on, 1, or true. This is useful for validating "Terms of Service" acceptance.

### active_url

The field under validation must have a valid A or AAAA record according to the [dnspython](http://www.dnspython.org).

### after:date

The field under validation must be a value after a given date. The dates will be passed into the [dateparser](https://dateparser.readthedocs.io):

  

```python
'finish_date' : 'required|date|after:start_date'
'another_date' : 'required|date|after:tomorrow'
```

### after_or_equal:date

The field under validation must be a value after or equal to the given date. For more information, see the after rule.

### alpha

The field under validation must be entirely alphabetic characters.

### alpha_dash

The field under validation may have alpha-numeric characters, as well as dashes and underscores.

### alpha_num

The field under validation must be entirely alpha-numeric characters.

### array

The field under validation must be a list array.

### before:date

The field under validation must be a value preceding the given date. The dates will be passed into the PHP strtotime function. In addition, like the after rule, the name of another field under validation may be supplied as the value of date.

### before_or_equal:date

The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP strtotime function. In addition, like the after rule, the name of another field under validation may be supplied as the value of date.

### between:min,max

The field under validation must have a size between the given min and max. Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

### boolean

The field under validation must be able to be cast as a boolean. Accepted input are true, false, 1, 0, "1", and "0".

### confirmed

The field under validation must have a matching field of foo_confirmation. For example, if the field under validation is password, a matching password_confirmation field must be present in the input.

### date
|The field under validation must be a valid date according to the (dateparser)
[https://da](parser.readthedocs.io).

### date_equals:date

The field under validation must be equal to the given date. The dates will be passed into the PHP strtotime function.

### date_format:format

The field under validation must match the given format. You should use either date or date_format when validating a field, not both.

### different:field

The field under validation must have a different value than field.

### digits:value

The field under validation must be numeric and must have an exact length of value.

### digits_between:min,max

The field under validation must have a length between the given min and max.
  

### distinct

When working with arrays, the field under validation must not have any duplicate values.

  

'foo.*.id' : 'distinct'

  

### email

The field under validation must be formatted as an e-mail address.

### exists:table,column

The field under validation must exist on a given database table.

  

Basic Usage Of Exists Rule

'state' : 'exists:states'

If the column option is not specified, the field name will be used.

  

Specifying A Custom Column Name

'state' : 'exists:states,abbreviation'

Occasionally, you may need to specify a specific database connection to be used for the exists query. You can accomplish this by prepending the connection name to the table name using "dot" syntax:

```python

'email' : 'exists:connection.staff,email'

```

If you would like to customize the query executed by the validation rule, you may use the Rule class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the | character to delimit them:

### file

The field under validation must be a successfully uploaded file.

### filled

The field under validation must not be empty when it is present.

### gt:field

The field under validation must be greater than the given field. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

### gte:field

The field under validation must be greater than or equal to the given field. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

### image

The file under validation must be an image (jpeg, png, bmp, gif, or svg)

### in:foo,bar,...

The field under validation must be included in the given list of values. Since this rule often requires you to implode an array, the Rule::in method may be used to fluently construct the rule:

  

### in_array:anotherfield.*

The field under validation must exist in anotherfield's values.

### integer

The field under validation must be an integer.

### ip

The field under validation must be an IP address.

  

### ipv4

The field under validation must be an IPv4 address.

  

### ipv6

The field under validation must be an IPv6 address.

### json

The field under validation must be a valid JSON string.

### lt:field

The field under validation must be less than the given field. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

### lte:field

The field under validation must be less than or equal to the given field. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the size rule.

### max:value

The field under validation must be less than or equal to a maximum value. Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

### mimetypes:text/plain,...

The file under validation must match one of the given MIME types:

```python

'video' : 'mimetypes:video/avi,video/mpeg,video/quicktime'

```

To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client provided MIME type.

### mimes:foo,bar,...

The file under validation must have a MIME type corresponding to one of the listed extensions.

  

Basic Usage Of MIME Rule

```python

'photo' : 'mimes:jpeg,bmp,png'

```

Even though you only need to specify the extensions, this rule actually validates against the MIME type of the file by reading the file's contents and guessing its MIME type.

  

A full listing of MIME types and their corresponding extensions may be found at the following location: https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types

#min:value

The field under validation must have a minimum value. Strings, numerics, arrays, and files are evaluated in the same fashion as the size rule.

#not_in:foo,bar,...

The field under validation must not be included in the given list of values. The Rule::notIn method may be used to fluently construct the rule:

  

#not_regex:pattern

The field under validation must not match the given regular expression.

  

Internally, this rule uses the PHP preg_match function. The pattern specified should obey the same formatting required by preg_match and thus also include valid delimiters. For example:

```python

'email' : 'not_regex:/^.+$/i'.

```

Note: When using the regex / not_regex patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

### nullable

The field under validation may be null. This is particularly useful when validating primitive such as strings and integers that can contain null values.

### numeric

The field under validation must be numeric.

### present

The field under validation must be present in the input data but can be empty.

### regex:pattern

The field under validation must match the given regular expression.

  

Internally, this rule uses the PHP preg_match function. The pattern specified should obey the same formatting required by preg_match and thus also include valid delimiters. For example:

```python

'email' : 'regex:/^.+@.+$/i'.

```

Note: When using the regex / not_regex patterns, it may be necessary to specify rules in an array instead of using pipe delimiters, especially if the regular expression contains a pipe character.

### required

The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true:

  

The value is null.

The value is an empty string.

The value is an empty array or empty Countable object.

The value is an uploaded file with no path.

  

### required_if:anotherfield,value,...

The field under validation must be present and not empty if the anotherfield field is equal to any value.

### required_unless:anotherfield,value,...

The field under validation must be present and not empty unless the anotherfield field is equal to any value.

### required_with:foo,bar,...

The field under validation must be present and not empty only if any of the other specified fields are present.

### required_with_all:foo,bar,...

The field under validation must be present and not empty only if all of the other specified fields are present.

### required_without:foo,bar,...

The field under validation must be present and not empty only when any of the other specified fields are not present.

### required_without_all:foo,bar,...

The field under validation must be present and not empty only when all of the other specified fields are not present.

### same:field

The given field must match the field under validation.

### size:value

The field under validation must have a size matching the given value. For string data, value corresponds to the number of characters. For numeric data, value corresponds to a given integer value. For an array, size corresponds to the count of the array. For files, size corresponds to the file size in kilobytes.

### string

The field under validation must be a string. If you would like to allow the field to also be null, you should assign the nullable rule to the field.

### timezone

The field under validation must be a valid timezone identifier according to the timezone_identifiers_list PHP function.

### unique:table,column

The field under validation must be unique in a given database table. If the column option is not specified, the field name will be used.

  

Specifying A Custom Column Name:

```python

'email' : 'unique:users,email_address'

```

  

### url

The field under validation must be a valid URL.

### uuid

The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID).

## to do :

- integrate with django form 
- integrate with rest_framwork