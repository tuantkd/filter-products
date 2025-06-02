import time
import pyautogui


def auto_click_forever(interval_seconds=0.1, button="left", x=None, y=None):
    """
    Clicks indefinitely until the script is terminated.

    Parameters:
    - interval_seconds: float, delay between clicks in seconds.
    - button: 'left', 'right', or 'middle'.
    - x, y: optional integers for a fixed screen coordinate. If None, clicks at current mouse position.
    """
    print(
        f"Auto-clicking {button}-button every {interval_seconds:.3f}s "
        f"at position {'current mouse' if x is None else f'({x}, {y})'}."
    )
    print("Stop by closing this program window or pressing Ctrl+C in the terminal.")
    try:
        while True:
            if x is None or y is None:
                pyautogui.click(button=button)
            else:
                pyautogui.click(x=x, y=y, button=button)
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        # If you press Ctrl+C, the script will exit gracefully
        print("\nAuto-clicker terminated by user.")
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    # Example: 10 clicks per second at the current mouse position, until closed
    auto_click_forever(interval_seconds=0.1, button="left")

    # If you prefer clicking at a fixed coordinate (e.g., x=800, y=450), uncomment and adjust:
    # auto_click_forever(interval_seconds=0.1, button='left', x=800, y=450)
