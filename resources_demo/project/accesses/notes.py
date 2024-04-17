from .dtos import AccessContext


class AccessPolicy:
    def __init__(self, resource, actions, conditions):
        self.resource = resource
        self.actions: list[str] = actions
        self.conditions = conditions

    def allows(self, user, context: AccessContext):
        for condition in self.conditions:
            # тут базовая проверка на разрешённые поля по пользователю
            if not condition(user, context):
                return False
        return True


# Define policies
policies = [
    AccessPolicy(resource='file', action='read', conditions=[is_admin]),
    AccessPolicy(resource='file', action='write', conditions=[is_owner, during_business_hours]),
    # настройка политик для админа
    AccessPolicy(resource='nodes', action='write', conditions=[is_owner, during_business_hours]),

    # настройка политик для пользователя
    AccessPolicy(resource='nodes',
                 actions='read',
                 conditions=[is_owner, is_reading_available_fields]),
    AccessPolicy()
]


# Simulate access request
def request_access(user, action, resource):
    context = {'resource_owner_id': 2}  # Example context
    
    for policy in policies:
        if policy.resource == resource and action in policy.actions:
            if policy.allows(user, context):
                return True
    return False

# Example users
admin_user = {'id': 1, 'role': 'admin'}
regular_user = {'id': 2, 'role': 'user'}

# Test the access control
print(request_access(admin_user, 'read', 'file'))  # Should be True
print(request_access(regular_user, 'write', 'file'))  # Should be True during business hours if user is the owner
print(request_access(regular_user, 'read', 'file'))  # Should be False since no policy allows it
