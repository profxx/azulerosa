# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from wraps import required_params

from model.provider import ModelProvider

provider_space = Namespace("Providers Manager", description="REsource for providers")

schema = {
    "id": {"type": "numeric", "required": True, "description": "numeric string value or int"},
    "enable": {"type": "boolean", "required": True, "description": "Status of provider"},
    "type_registration": {"type": "integer", "allowed": [1, 2], "required": True, "description": "Type of provider registration. 1 : CPF, 2: CNPJ"},
    "cnpj": {"type": "string", "required": True, "check_with": "registration"},
    "state_registration": {"type": "string", "required": True, "description": "State company registration", "maxlength": 20},
    "municipal_registration": {"type": "string", "required": True, "description": "municipal company registration", "maxlength": 12},
    "fancy_name": {"type": "string", "required": True, "description": "company fancy name"},
    "company_name": {"type": "string", "required": True, "description": "Company name", "empty": False},
    "contact_name": {"type": "string", "required": True, "description": "Company contact name", "empty": True},
    "phone": {"type": "string", "required": True, "check_with": "phonecheck",  "description": "Phone Number of company"},
    "cell_phone": {"type": "string", "required": True, "check_with": "cellcheck", "description": "Cell Number of company"},
    "email": {"type": "string", "required": True, "description": "Contact email", "empty": True, "maxlength": 40},
    "site": {"type": "string", "required": True, "description": "Company site", "empty": True, "maxlength": 50},
    "zip_code": {"type": "string", "required": True, "maxlength": 8, "minlength": 8, "empty": False, "description": "Zip Code address", "regex": '[0-9]+'},
    "address": {"type": "string", "required": True, "description": "Company Address", "empty": False, "maxlength": 80},
    "number": {"type": "string", "required": True, "description": "Address number", "empty": True, "maxlength": 60},
    "complement": {"type": "string", "required": True, "description": "Address Complement", "empty": True, "maxlength": 40},
    "neighborhood": {"type": "string", "required": True, "description": "neighborhood name", "empty": False, "maxlength": 80},
    "city": {"type": "string", "required": True, "description": "Company city", "empty": False, "maxlength": 80},
    "state": {"type": "string", "required": True, "description": "Company State", "empty": False, "maxlength": 2},
    "obs": {"type": "string", "required": True, "description": "Company Observation", "empty": True}

}


@provider_space.route("")
class ProviderView(Resource):

    def get(self):
        """ List of all Provider """

        return {"data": [data.list_provider() for data in ModelProvider.query.all()]}, 200

    # @jwt_required
    @provider_space.doc(params=schema)
    @required_params(schema)
    def post(self):

        """  Create or Updated provider """       

        data = request.json

        provider = ModelProvider.find_provider(data.get("id"))

        if provider:
            return self.put()

        try:
            provider = ModelProvider(**data)
            provider.save_provider()

            return {"message": "provided created", "data": provider.json_provider()}, 201
        except Exception as err:
            print(err)
            return {"message": "Internal error"}, 500

        return {"data": data}
    
    @provider_space.hide
    @required_params(schema)
    def put(self):

        data = request.json

        provider = ModelProvider.find_provider(data.get("id"))

        if provider:

            try:

                provider.update_provider(**data)
                provider.save_provider()

                return {"message": "provider updated", "data": provider.json_provider()}, 200
            
            except:
                return {"message": "Internal Error"}, 500
        
        return {"message": "Provider not found"}, 404

@provider_space.route("/<int:id_provider>")
class ProviderGet(Resource):


    def get(self, id_provider):
        """ Get provider By id """

        provider = ModelProvider.find_provider(id_provider)

        if provider:
            return {"data": provider.json_provider()}, 200
        
        return {"message": "Provider not found"}, 404       
