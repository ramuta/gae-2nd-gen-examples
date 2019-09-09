import os
import time
import atexit

# Datastore emulator instance
run_datastore = None


# Exit handler to stop the emulator
def exit_handler():
    """
    Needed to stop the emulator
    :return: None
    """
    if run_datastore:
        run_datastore.close()
        print("Datastore emulator stopped.")
    print("Exiting the script")


# register the Exit handler
atexit.register(exit_handler)

# Ask user if they want to run a web app or tests
test = input("Would you like to run tests? (yes/no; default is no): ")

# Prepare the correct port number and the main command based on the user's input
if test == "yes":
    print("Preparing to run tests.")
    emulator_port = "8002"
    main_command = "pytest -p no:warnings"
else:
    print("Preparing to run the web app.")
    emulator_port = "8001"
    main_command = "python main.py"

# Run datastore emulator
emulator_command = 'gcloud beta emulators datastore start --no-legacy --data-dir=. --project test --host-port "localhost:{}"'.format(emulator_port)
run_datastore = os.popen(emulator_command)

# 10 seconds wait for the Emulator to start
# TODO: replace with checking the localhost:port response which should be "Ok"
time.sleep(10)

# Run the main command, which is either the web app, or pytest
run_main_command = os.popen(main_command)

# Print process output in the Terminal
print(run_main_command.read())
