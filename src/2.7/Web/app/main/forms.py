from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, RadioField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
import os, json

class GenerateConfiguration(Form):
    configurations = {}

    # Get Modules Folder
    modules_folder = os.path.dirname(os.getcwd())
    modules_folder = os.path.join(modules_folder, "Modules")

    # Load configurations from these files
    for file in os.listdir(modules_folder):
        if file.endswith(".json"):
            with open(os.path.join(modules_folder, file)) as data_file:
                configurations[file] = json.load(data_file)

    for moduleName, configuration in configurations.iteritems():
        friendlyModuleName = moduleName.split("_")[0]

        # Module Enable button
        exec(friendlyModuleName + "_Enabled" + " = BooleanField('Enable " +
            friendlyModuleName +"')")

        for field in configuration["params"]:
            friendlyFieldName = field["name"].replace(" ", "_")

            # Boolean Field
            if field["fieldType"] == "BooleanField":
                exec(friendlyModuleName + "_" + friendlyFieldName + " = BooleanField('" +
                    field["name"] + "', description='" + field["description"] +
                    "')")

            # String Field
            if field["fieldType"] == "StringField":
                exec(friendlyModuleName + "_" + friendlyFieldName + " = StringField('" +
                    field["name"] + "', description='" + field["description"] +
                    "')")

            # Dropdown Field
            if field["fieldType"] == "SelectField":
                exec(friendlyModuleName + "_" + friendlyFieldName + " = SelectField('" +
                    field["name"] + "', description='" + field["description"] +
                    "', choices=" + str([tuple(choice) for choice in field["options"]]) + ")")

            # Radio Button Field
            if field["fieldType"] == "RadioField":
                exec(friendlyModuleName + "_" + friendlyFieldName + " = RadioField('" +
                    field["name"] + "', default=" + str(field["options"][0][0]) + ", description='" + field["description"] +
                    "', choices=" + str([tuple(choice) for choice in field["options"]]) + ")")

            # This will not work currently with wtf.quick_form
            # Label Field
            # if field["fieldType"] == "Label":
            #     exec(friendlyModuleName + "_" + friendlyFieldName +
            #         " = Field("label='" + field["name"] + "')")
    submit = SubmitField('Submit')
