import os

main_command = "export FLASK_APP=main.py && flask run --host localhost --port 8080 --reload"

# Run the main command, which is either the web app, or pytest
run_main_command = os.popen(main_command)

# Print process output in the Terminal
print(run_main_command.read())
