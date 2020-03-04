# Lexibot

Lexibot is a bot to monitor a set of lexibank datasets. 

It is designed to run over a directory containing datasets that have been cloned there.

Lexibot will loop over each dataset in the directory doing these steps:

        # check
        invalids = self.validate()
        warnings = self.lexibank_checks()
        differences = self.compare_cldf()
        
        if invalids or differences or warnings:
            self.notify(invalids, differences, warnings)



1. update from git `Lexibot.update_repository()`
    - git fetch remote origin
    - sets `dirty` flag if there are any changes to repository

2. install a new virtual env for this dataset `Lexibot.install_virtualenv()`

3. Make CLDF with `Lexibot.make_cldf()`:
    - if the `dirty` flag is set

...and then check the dataset in the following ways:

4. Validate CLDF with `Lexibot.validate()`:
    - store errors

5. Run `check` commands with `Lexibot.run_lexibank_checks()`:
    - store errors

6. Compare for differences between the stored CLDF dataset and the new rebuilt one with `Lexibot.compare_cldf()`:
    - if no differences, quit
    
7. Notify people somehow


## Usage:


```shell
# install some datasets
mkdir datasets
git clone https://github.com/lexibank/birchallchapacuran datasets/birchallchapacuran
git clone https://github.com/lexibank/kitchensemitic datasets/kitchensemitic

# list datasets
lexibot list datasets

# run bot
lexibot run datasets
```
