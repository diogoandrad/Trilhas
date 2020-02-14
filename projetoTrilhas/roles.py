from rolepermissions.roles import AbstractUserRole

class Estudante(AbstractUserRole):
    available_permission = {

    }


class Moderador(AbstractUserRole):
    available_permissions = {

    }

class Administrador(AbstractUserRole):
    available_permissions = {

    }