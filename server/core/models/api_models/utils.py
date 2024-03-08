from typing import Type

from flask_restx import fields, reqparse

from server.api import api


def reqparse_add_queryparams_doc(
        parser: reqparse.RequestParser,
        add_search_utils: bool = False,
        add_pagination: bool = True,
        query_params: list[tuple[str, Type]] = None
) -> reqparse.RequestParser:
    if add_pagination:
        parser.add_argument(
            "page",
            type=int,
            location="args"
        )
        parser.add_argument(
            "page_size",
            type=int,
            location="args"
        )

    if add_search_utils:
        parser.add_argument(
            "search_type",
            type=str,
            choices=["equals", "contains", "starts_with", "ends_with"],
            location="args"
        )
        parser.add_argument(
            "search_way",
            type=str,
            choices=["and", "or"],
            location="args"
        )

    if query_params is not None:
        for param_name, param_type in query_params:
            parser.add_argument(
                param_name,
                type=param_type,
                location="args"
            )

    return parser


base_name_model_fields = {
    "id": fields.Integer,
    "name": fields.String
}


base_name_model_fields_send = {
    "name": fields.String
}


error_model = api.model("ErrorModel", {
    "message": fields.String
})
