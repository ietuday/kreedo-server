from .serializer import*

def permission_creation(id, request_data):
    print("permission_creation called")
    permission_data = {
        "name":request_data.get('name', None),
        "content_type":id,
        "codename":request_data.get('codename',None)

    }
    print("######",permission_data)
    permission_serializer = PermissionSerializer(data=dict(permission_data))
    if permission_serializer.is_valid():
        permission_serializer.save()
        return permission_serializer.data
    else:
        print("###############",permission_serializer.errors)
        return permission_serializer.errors