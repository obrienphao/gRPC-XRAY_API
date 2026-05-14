import grpc
from proto import command_pb2, command_pb2_grpc
from core.settings import settings
import json
import uuid
import subprocess


channel = grpc.insecure_channel(settings.XRAY_API)
stats_stub = command_pb2_grpc.StatsServiceStub(channel)

#-------------------------------------
#           X-ARAY SERVICE
#-------------------------------------

def get_stat(name: str):
    request = command_pb2.GetStatsRequest(
        name=name,
        reset=False
    )

    try:
        response = stats_stub.GetStats(request)
        return int(response.stat.value)

    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return 0
        raise


def get_user_usage(email: str)->dict:
    """
    get user usage by her email
    """
    uplink = get_stat(
        f"user>>>{email}>>>traffic>>>uplink"
    )

    downlink = get_stat(
        f"user>>>{email}>>>traffic>>>downlink"
    )

    return {
        "status": "ok",
        "uplink": uplink,
        "downlink": downlink,
        "total": uplink + downlink
    }


#----------------------------------------------
#             HELPER FUNCTION
#----------------------------------------------

def load_config(config_path: str):
    with open(config_path, "r") as f:
        return json.load(f)


def save_config(data, config_path: str):
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)


def generate_unique_uuid(existing_ids):
    while True:
        new_id = str(uuid.uuid4())

        if new_id not in existing_ids:
            return new_id


def add_client_to_xray(config_path: str, email: str):
    data = load_config(config_path)

    clients = data["inbounds"][0]["settings"]["clients"]

    for client in clients:
        if client["email"] == email:
            raise Exception("Email already exists")

    existing_ids = {client["id"] for client in clients}

    new_uuid = generate_unique_uuid(existing_ids)

    clients.append({
        "id": new_uuid,
        "level": 0,
        "email": email
    })

    save_config(data, config_path)

    subprocess.run(
        ["sudo", "systemctl", "restart", "xray"],
        check=True
    )

    return new_uuid


def list_clients(config_path: str):
    data = load_config(config_path)

    clients = data["inbounds"][0]["settings"]["clients"]

    results = []

    for client in clients:
        results.append({
            "uuid": client["id"],
            "email": client["email"],
            "level": client.get("level", 0)
        })

    return {
        "status": "ok",
        "count": len(results),
        "clients": results
    }





def restart_xray():
    subprocess.run(
        ["sudo", "systemctl", "restart", "xray"],
        check=True
    )


def delete_client_from_xray(config_path: str, email: str):
    data = load_config(config_path)

    clients = data["inbounds"][0]["settings"]["clients"]

    new_clients = [
        client for client in clients
        if client["email"] != email
    ]

    if len(new_clients) == len(clients):
        raise Exception("Client not found")

    data["inbounds"][0]["settings"]["clients"] = new_clients

    save_config(data, config_path)

    restart_xray()

    return {
        "status": "ok",
        "message": "Client deleted"
    }


def restart_client(config_path: str, email: str, uuid_value: str):
    data = load_config(config_path)

    clients = data["inbounds"][0]["settings"]["clients"]

    for client in clients:
        if client["email"] == email:
            raise Exception("Client already active")

    clients.append({
        "id": uuid_value,
        "level": 0,
        "email": email
    })

    save_config(data, config_path)

    restart_xray()

    return {
        "status": "ok",
        "message": "Client restored"
    }