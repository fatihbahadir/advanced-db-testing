from core.application import App

def run():
    App().start()

def screen_test():

    from modules.screen.screen import Screen
    
    screen = Screen(
        app=None,
        geometry= "400x400",
        title="Form"
        )

    screen.start()

if __name__ == "__main__":
    run()