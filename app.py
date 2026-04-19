from fastapi import FastAPI, HTTPException
import grpc
from proto import command_pb2, command_pb2_grpc

app = FastAPI()

XRAY_API = "127.0.0.1:10085"

#channel global (perf)
channel = grpc.insecure_channel(XRAY_API)
stub = command_pb2_grpc.StatsServiceStub(channel)


def get_stat(name: str):
    request = command_pb2.GetStatsRequest(
        name=name,
        reset=False
    )

    try:
        response = stub.GetStats(request)
        return int(response.stat.value)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return 0
        raise


def get_user_usage(email: str):
    uplink = get_stat(f"user>>>{email}>>>traffic>>>uplink")
    downlink = get_stat(f"user>>>{email}>>>traffic>>>downlink")
    return {
        "uplink": uplink,
        "downlink": downlink,
        "total": uplink + downlink
    }


# endpoint principal
@app.get("/usage/{email}")
def usage(email: str):
    try:
        return get_user_usage(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

