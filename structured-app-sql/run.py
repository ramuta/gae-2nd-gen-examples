import os

# Ask user if they want to run a web app or tests
test = input("Would you like to run tests? (yes/no; default is no): ")

# Prepare the correct port number and the main command based on the user's input
if test == "yes":
    print("Preparing to run tests.")
    text_bottom = "tests"
    main_command = "pytest -p no:warnings"
    os.environ["TESTING"] = "yes"
else:
    print("Preparing to run the web app.")
    text_bottom = "web app"
    main_command = "export FLASK_APP=main.py && flask run --host localhost --port 8080 --reload"

print("Let's start our {}.".format(text_bottom))

# Run the main command, which is either the web app, or pytest
run_main_command = os.popen(main_command)

# Print process output in the Terminal
print(run_main_command.read())
