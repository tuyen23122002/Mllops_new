import great_expectations as ge
from great_expectations.core.batch import BatchRequest
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.exceptions import DataContextError

"""
**IMPORTANT**
This file is meant to be run as an end-2-end test command.
It is an example and might require changes to suit your data and use case.

Please refer to the `example-project` branch of the Cookiecutter-MLOps project for a complete working example –
https://dagshub.com/DagsHub/Cookiecutter-MLOps/src/example-project
"""

context = ge.data_context.DataContext()

batch_request = {
    "datasource_name": "{{fill in datasource name}}",
    "data_connector_name": "default_inferred_data_connector_name",
    "data_asset_name": "{{fill in names of files that have tests}}",  # Define the data files that should be tested
    "limit": 1000,
}

# Feel free to change the name of your suite here. Renaming this will not remove the other one.
expectation_suite_name = "{{fill in your test suite name}}"
try:
    suite = context.get_expectation_suite(expectation_suite_name=expectation_suite_name)
    print(
        f'Loaded ExpectationSuite "{suite.expectation_suite_name}" containing {len(suite.expectations)} expectations'
    )
except DataContextError:
    suite = context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name
    )
    print(f'Created ExpectationSuite "{suite.expectation_suite_name}".')

validator = context.get_validator(
    batch_request=BatchRequest(**batch_request),
    expectation_suite_name=expectation_suite_name,
)

checkpoint_config = {
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
}
checkpoint = SimpleCheckpoint(
    f"{validator.active_batch_definition.data_asset_name}_{expectation_suite_name}",
    context,
    **checkpoint_config,
)
checkpoint_result = checkpoint.run()

context.build_data_docs()

validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]
context.open_data_docs(resource_identifier=validation_result_identifier)
