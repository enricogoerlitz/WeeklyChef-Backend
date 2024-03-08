from dataclasses import dataclass

from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
    create_access_token,
    create_refresh_token
)


jwt_manager = JWTManager()


@dataclass(frozen=True)
class JsonWebTokenDTO:
    access_token: str
    refresh_token: str

    @staticmethod
    def create(obj: dict) -> 'JsonWebTokenDTO':
        """
        Creates an JsonWebTokenDTO from the given object.

        Args:
            obj (dict): any dictinory as object

        Returns:
            JsonWebTokenDTO: created JsonWebTokenDTO
        """
        access_token = create_access_token(identity=obj)
        refresh_token = create_refresh_token(identity=obj)

        return JsonWebTokenDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }


def add_user_id_to_data(data: dict, fieldname: str) -> dict:
    jwt_identity = get_jwt_identity()
    data[fieldname] = jwt_identity.get("id")
    return data
