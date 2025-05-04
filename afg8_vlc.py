import vlc

vlc_instance = vlc.Instance("--no-xlib")
player = vlc_instance.media.player_new()

player.set_media(vlc_instance.media_new("example.mp4"))

player.play()

input("Beliebige Taste zum Beenden")

player.stop()
