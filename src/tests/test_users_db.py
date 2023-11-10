from unittest.mock import patch
#
# from fastapi import APIRouter
from fastapi.testclient import TestClient

# Clases de usuarios
from src.db.models.user import User
from src.db.schemas.user import user_schema, users_schema_list
from src.db.client import db_client
from src.routers.users_db import search_user_by_field

import pytest

from src.main import app

# Object ID
from bson import ObjectId


class TestUsersEmployees:
    # Crea un cliente de prueba
    client = TestClient(app)

    def test_get_user(self):
        # Crea un usuario nuevo
        user = User(
            id="654df447ad44d3a186929960",
            username="carlos.emilio",
            name="Carlos",
            last_name="Emiliano",
            email="emilio.emilio@example.com",
            department="IoT",
            salary=40000
        )

        # Guarda el usuario en la base de datos
        db = db_client.test.employees
        _user = None
        with patch.object(db_client.test.employees, "find_one") as mock_find_one:
            # STEP 1
            # mock_find_one.return_value = search_user_by_field("email", user.email)
            # _user = search_user_by_field("email", user.email)

            # STEP 2
            mock_find_one.return_value = search_user_by_field("_id", ObjectId(user.id))
            _user = search_user_by_field("_id", ObjectId(user.id))

        # # Envía una solicitud GET para obtener el usuario
        response = self.client.get("/api/v1/users/{}".format(_user.id))
        # # Comprueba que la solicitud se haya realizado correctamente
        assert response.status_code == 200

        # Convierte la respuesta a un objeto User
        user_found = User(**response.json())

        # Comprueba que el usuario devuelto sea el mismo que el que se guardó en la base de datos
        assert user_found == _user

    # def test_get_users(self):
    #     # Creamos dos usuarios prueba
    #     users_examples = [
    #         User(
    #             username="carlos.emilio",
    #             name="Carlos",
    #             last_name="Emiliano",
    #             email="carlos.emilio@example.com",
    #             department="IoT",
    #             salary=40000
    #         ),
    #         User(
    #             username="juanito.emilio",
    #             name="Juanito",
    #             last_name="Emiliano",
    #             email="juanito.emilio@example.com",
    #             department="Marketing",
    #             salary=40000
    #         )
    #     ]
    #
    #     # Agregamos los usuarios a la DB
    #     db = db_client.test.employees
    #     with patch.object(db, "find") as mock_find:
    #         mock_find.return_value = users_schema_list(users_examples)
    #
    #     # Enviamos la soliciutd GET
    #     response = self.client.get("/api/v1/users")
    #
    #     # Comprobamos el response code
    #     assert response.status_code == 200
    #
    #     # Convertimos la lista obtenida
    #     users_found = users_schema_list(response.json())
    #
    #     # Comprobamos lo encontrado con lo enviado
    #     assert users_found == users_examples
