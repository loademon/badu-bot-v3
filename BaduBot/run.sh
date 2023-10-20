#!/bin/bash
# ----------------- Library -----------------
pip install discord.py                       # Install discord.py library
pip install "discord.py[voice]"              # Install discord.py with voice support
pip install redis                            # Install Redis database
pip install xmltodict                        # Install xmltodict library
pip install Flask                            # Install Flask web framework
# ----------------- Library -----------------


# To start Tmux sessions using a function.
start_tmux_session() {
    tmux new-session -d -s "$1" "$2"
}


# Run Redis Server
start_tmux_session "redis_server" "redis-server"

# Run Ngrok
start_tmux_session "ngrok" "ngrok start youtube"

# Run Discord Bot
start_tmux_session "discord_bot" "python main.py"

# Run Youtube Webhook Notifier
start_tmux_session "youtube" "python youtube.py"
