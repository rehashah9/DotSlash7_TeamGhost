from api.main import get_profile_connections



def get_list_of_connections():
    connections = get_profile_connections()
    connection_list = []
    for connection in connections:
        if connection['connection_plugin'] == "aws":
            connection_list.append(f"{connection['name']} - (Amazon Web Services)")
    return connection_list