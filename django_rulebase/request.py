from django.http import HttpResponseBadRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import classonlymethod
from .validator import Validator
import json
def sample_request(request,valid,errors):
    if valid:
        return HttpResponse("good request")
    else:
        return HttpResponseBadRequest() 

class Request:
    view = sample_request
    validator = Validator
    def __init__(self):
        if self.view is  None and  not callable(self.view):
            raise Exception(" the request object needs view function")
        if self.validator is None and type(self.validator)!=type(Validator):
            raise Exception(" the request object needs valid validator")

    @classonlymethod
    def asView(self):
        def view_func(request):
            _json_ = 'json' in request.content_type
            if _json_:
                body = json.loads(request.body)
            else:
                body = getattr(request,request.method)
            valid = self.run_validator(self,body)
            return self.view(request,valid,self.validator.errors)
        return csrf_exempt(view_func)
    
    def run_validator(self,data):
        rules = self.rules(self) if hasattr(self,"rules") and callable(self.rules) else None
        if rules is None:
            raise Exception("{} should have 'rules' method and return dict of request rules ".format(self.__name__))
        valid = True
        if not isinstance(rules,dict):
            raise Exception("rules must be of type dict")
        if isinstance(self.validator,Validator):
            self.validator.run_validation(data)
            valid &= self.validator.valid
        else:
            validator = self.validator(rules)
            validator.run_validation(data)
            valid &= validator.valid
        return valid