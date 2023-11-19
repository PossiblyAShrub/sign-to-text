import app.gui
import os

if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)  # Create an empty images/ dir for log files

    app.gui.main()
