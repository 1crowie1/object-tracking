import dvd

def main() -> None:
    video = 'videos/dvd_screen_saver.mp4'
    seconds = 300
    wall_collisions = dvd.get_collisions(video, seconds)

if __name__ == "__main__":
    main()