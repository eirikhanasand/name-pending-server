# Bedrock access

On iPad, add server address `np.hanasand.com` and port `443`.
Docker maps public UDP 443 to Geyser's internal UDP 19132. Java continues
through the existing TCP 443 router. No upstream firewall change is needed.

Geyser 2.11.3 build 1245 and Floodgate 2.2.5 build 141 are pinned alongside
ViaVersion 5.12.0 in plugins.lock.json. Downloads are checksum verified.
Update these pins when a new Bedrock client requires a newer Geyser release.

Floodgate authenticates Bedrock accounts; Java online authentication stays on.
Secure-profile enforcement is disabled because Bedrock accounts cannot provide
Java chat signatures. Floodgate keys and player data stay in the ignored data
directory. Unlinked Bedrock accounts have separate player inventories; use
Floodgate account linking to share an existing Java player identity.

Deploy from the clean source checkout:
```sh
docker exec name_pending_server rcon-cli list
# Wait until no players are online before this planned restart.
docker compose -f /home/hanasand/name_pending_server/docker-compose.yml stop minecraft
python3 bedrock/install.py /home/hanasand/name_pending_server
docker compose -f /home/hanasand/name_pending_server/docker-compose.yml up -d minecraft
docker exec name_pending_server rcon-cli "geyser version"
```

The installer backs up replaced plugins, Geyser config, and Compose in the live
deployment's backups directory. It preserves worlds and other plugins.
Keep using the clean source checkout for commits; do not push the legacy live
deployment history.

Run `python3 bedrock/check.py` from outside Inspur to verify Bedrock status and
RakNet negotiation on UDP 443. An authenticated iPad join is still required to
verify gameplay. Also check that Java still responds on TCP 443.
