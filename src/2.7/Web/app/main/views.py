from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from . import main
from .forms import GenerateConfiguration
import os, json

@main.route('/', methods=['GET', 'POST'])
def index():
    form = GenerateConfiguration()
    if form.validate_on_submit():
        # List of Modules
        modules = []

        # Get Modules Folder
        modules_folder = os.path.dirname(os.getcwd())
        modules_folder = os.path.join(modules_folder, "Modules")

        # Load names of modules into variable
        for file in os.listdir(modules_folder):
            if file.endswith(".json"):
                modules.append(file.split("_")[0])

        enabledModules = []

        # Look for Enabled Modules
        enabled = False
        for module in modules:
            exec("enabled = form." + module + "_Enabled.data")
            if enabled:
                enabledModules.append(module)

        for enabledModule in enabledModules:
            moduleOptions = {}

            # loop through form data
            for key in dir(form):
                if key.split("_")[0] == enabledModule:
                    moduleLength = len(enabledModule) + 1
                    exec("moduleOptions['" + key[moduleLength:] + "'] = form." + key + ".data")

            # Output configuration file
            jsonObject = json.dumps(moduleOptions, indent=4)

            file = open(os.path.join(modules_folder, enabledModule + "_config.json"), 'w')
            file.write(jsonObject)
            file.close()
            
    return render_template('index.html', form=form)
