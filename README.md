

1. depéndance pour utilisation gRPC - Vless serveur

```sh
mkdir proto
cd proto

curl -O https://raw.githubusercontent.com/XTLS/Xray-core/main/app/stats/command/command.proto
curl -O https://raw.githubusercontent.com/XTLS/Xray-core/main/common/serial/typed_message.proto
```

2.

```sh
python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  command.proto
  ```


  # Exécution du Projet
  `uvicorn app:app --reload`