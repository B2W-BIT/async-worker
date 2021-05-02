# Contributing

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:


When contributing to this repository, please first discuss the change you wish to make via issue or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Simple Process

### Install

```shell
pipenv install --pre --ignore-pipfile --dev
```

### Tests

```shell
pipenv run all-tests
```

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Submitting an Issue
Before you submit your issue search the archive, maybe your question was already answered.

If your issue appears to be a bug, and hasn't been reported, open a new issue.
Help us to maximize the effort we can spend fixing issues and adding new
features, by not reporting duplicate issues.  Providing the following information will increase the
chances of your issue being dealt with quickly:

* **Overview of the issue** - if an error is being thrown a non-minified stack trace helps
* **Motivation for or Use Case** - explain why this is a bug for you
* **async-worker Version(s)** - is it a regression?
* **Broker type and version in use** - is this a problem with RabbitMQ 3.7.7 only?
* **Reproduce the error** - provide a live example, screenshot, and/or a unambiguous set of steps. The more the better.
* **Related issues** - has a similar issue been reported before?  Reference the related issues in the description.
* **Suggest a Fix** - if you can't fix the bug yourself, perhaps you can point to what might be
  causing the problem (line of code or commit).  If you're requesting a feature, describe how the feature might work to resolve the user story.

## Submitting a Pull Request
Before you submit your pull request consider the following guidelines:

* Search [GitHub](https://github.com/b2wdigital/async-worker/pulls) for an open or closed Pull Request that relates to your submission. You don't want to duplicate effort.
* Make your changes in a new git branch

     ```shell
     git checkout -b my-fix-branch master
     ```

* Create your patch, **including appropriate test cases**.
* Follow our [Code Style](https://www.pylint.org/) with Flake8 and [PEP8](https://www.python.org/dev/peps/pep-0008/).
* Check lint
    ```shell
    pipenv run fmt-check
    ```

If you have issues, then run all lints and check consistency.

* Run lints.

    ```shell
    pipenv run fmt
    pipenv run isort-fmt
    pipenv run lint

    ```
* Run the full test suite, including `pipenv run all-tests`,
  and ensure that all tests pass.
* Commit your changes using a descriptive commit message

     ```shell
     git commit -a
     ```
  Note: the optional commit `-a` command line option will automatically "add" and "rm" edited files.

* Build your changes locally to ensure all the tests and security checks pass

    ```shell
    pipenv run all-tests
    ```

* Push your branch to GitHub:

    ```shell
    git push origin my-fix-branch
    ```

* In GitHub, send a pull request to `master`.
* If we suggest changes then:
  * Make the required updates.
  * Re-run the test suite and lints to ensure tests are still passing and code looks good.
  * Rebase your branch and force push to your GitHub repository (this will update your Pull Request):

    ```shell
    git rebase master -i
    git push -f
    ```

That's it! Thank you for your contribution!

### After your pull request is merged

After your pull request is merged, you can safely delete your branch and pull the changes
from the main (upstream) repository:

* Delete the remote branch on GitHub either through the GitHub web UI or your local shell as follows:

    ```shell
    git push origin --delete my-fix-branch
    ```

* Check out the master branch:

    ```shell
    git checkout master -f
    ```

* Delete the local branch:

    ```shell
    git branch -D my-fix-branch
    ```

## Reviewing Pull Requests

Except for critical, urgent or very small fixes, we try to leave pull requests open for most of the day or overnight if something comes in late in the day, so that multiple people have the chance to review/comment.  Anyone who reviews a pull request should leave a note to let others know that someone has looked at it.  For larger commits, we like to have a +1 from someone else on the core team and/or from other contributor(s).  Please note if you reviewed the code or tested locally -- a +1 by itself will typically be interpreted as your thinking its a good idea, but not having reviewed in detail.
