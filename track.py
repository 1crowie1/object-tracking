import dvd

def main() -> None:
    """
    Main function.
    """
    video = 'videos/dvd_screen_saver.mp4'
    seconds = int(input("How long are collisions to be counted for (Seconds): "))
    visibility = int(input("How visible are the features (0-10): "))
    # count collisions in the video for the provided number of seconds
    wall_collisions = dvd.get_collisions(video, seconds, visibility)
    # display results
    print(f"There were {wall_collisions} wall collisions in {seconds} seconds of the video.")

if __name__ == "__main__":
    main()