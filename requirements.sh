
#!/bin/bash
curl -L https://github.com/fullstorydev/grpcurl/releases/download/v1.9.1/grpcurl_1.9.1_linux_x86_64.tar.gz -o grpcurl.tar.gz

# Extraire
tar -xvf grpcurl.tar.gz

# Déplacer
sudo mv grpcurl /usr/local/bin/

# Donner les droits
sudo chmod +x /usr/local/bin/grpcurl


mkdir -p xray_proto
cd xray_proto

curl -O https://raw.githubusercontent.com/XTLS/Xray-core/main/app/stats/command/command.proto



#----------------------- voir quotas :: Télécharger -------------
# grpcurl -plaintext \
# -import-path . \
# -proto command.proto \
# -d '{"name":"user>>>UUID>>>traffic>>>uplink"}' \
# 127.0.0.1:10085 \
# xray.app.stats.command.StatsService/GetStats

# donc:

# grpcurl -plaintext \
# -import-path . \
# -proto command.proto \
# -d '{"name":"user>>>7b507bb0-ea88-4954-8d7e-f3c4135d8d10>>>traffic>>>uplink"}' \
# 127.0.0.1:10085 \
# xray.app.stats.command.StatsService/GetStats