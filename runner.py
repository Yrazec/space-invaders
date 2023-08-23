"""Runner file for Space Invaders."""


from libs.space_invaders import SpaceInvaders


def main():
    """Standard main function."""

    space_invaders = SpaceInvaders(invaders_number=10)
    space_invaders.run()


if __name__ == "__main__":
    main()
