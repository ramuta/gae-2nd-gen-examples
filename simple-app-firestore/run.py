import os
import time
import atexit

# Firestore emulator instance
run_firestore = None


# Exit handler to stop the emulator
def exit_handler():
    if run_firestore:
        run_firestore.close()
        print("Firestore emulator stopped.")
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
    main_command = "export FLASK_APP=main.py && flask run --host localhost --port 8080 --reload"

# Run firestore emulator
emulator_command = 'gcloud beta emulators firestore start --project test --host-port "localhost:{}"'.format(emulator_port)
run_firestore = os.popen(emulator_command)

# 10 seconds wait for the Emulator to start
# TODO: replace with checking the localhost:port response which should be "Ok"
time.sleep(10)

# Run the main command, which is either the web app, or pytest
run_main_command = os.popen(main_command)

# Print process output in the Terminal
print(run_main_command.read())
