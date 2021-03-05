To run the analysis for all targets, RunAll has to be executed in cova_automatic.
The arguments are the same as for the current version of COVA.
For example to run tests for all found targets:
Main class: cova.automatic.RunAll
Arguments: -apk {APKS_PATH}/app-debug.apk -config ${SOURCE_CODE_DIR}/COVA/cova/config -platform ${SOURCE_CODE_DIR}/COVA/cova/src/test/resources/androidPlatforms
Environment: LD_LIBRARY_PATH=${SOURCE_CODE_DIR}/COVA/cova/localLibs/z3-4.8.9-x64-ubuntu-16.04/bin

Important: The version of Z3 changed, old Z3 versions do not work anymore.

The test app is in https://github.com/fynnh/COVA-activity-testapp.

The results of the evaluation of the thesis can found in this repository.

The apps of the pre-study reside in pre_study_apps.

The results of the instrument runtime can be found in results/runtime/instrument.

The COVA runtime results for different apps are in results/runtime/cova/apps.

results/runtime/cova/string_clauses contains the COVA runtime for string clauses and the apks.

Correctness results reside below results/correctness

raw_data contains the results of the analysis for the tested apps.
copy.py makes the random selection and generates tex files.

The results of the manual analysis is below manual_testing.

automatic contains the results of the automatic testing.
In each app directory, there is a check.py.
This lists the true positives and false positives of the test run.
