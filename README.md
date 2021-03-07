# coinmarketcap-webspider

```
Collecting package metadata (current_repodata.json): ...working... done
Solving environment: ...working... failed with initial frozen solve. Retrying with flexible solve.
Collecting package metadata (repodata.json): ...working... done
Solving environment: ...working... failed with initial frozen solve. Retrying with flexible solve.


PackagesNotFoundError: The following packages are not available from current channels:

  - python-dotenv

Current channels:

  - https://repo.anaconda.com/pkgs/main/win-64
  - https://repo.anaconda.com/pkgs/main/noarch
  - https://repo.anaconda.com/pkgs/r/win-64
  - https://repo.anaconda.com/pkgs/r/noarch
  - https://repo.anaconda.com/pkgs/msys2/win-64
  - https://repo.anaconda.com/pkgs/msys2/noarch

To search for alternate channels that may provide the conda package you're
looking for, navigate to

    https://anaconda.org

and use the search bar at the top of the page.

```

```
$ anaconda search -t conda python-dotenv
Using Anaconda API: https://api.anaconda.org
Packages:
     Name                      |  Version | Package Types   | Platforms       | Builds
     ------------------------- |   ------ | --------------- | --------------- | ----------
     KC-Solutions/python-dotenv |   0.13.0 | conda           | noarch, win-64  | py_0, py36_0
                                          : Add .env support to your django/flask apps in development and deployments
     conda-forge/python-dotenv |   0.15.0 | conda           | linux-64, win-32, win-64, noarch, osx-64 | py34_0, py36_0, py27_0, pyh9f0ad1d_0, py_0, py_1, pyhd8ed1ab_0, py35_0
                                          : Get and set values in your .env file in local and production servers like Heroku does.
     nymerion/python-dotenv    |    0.6.0 | conda           | linux-64        | py35_0
     oarodriguez/python-dotenv |   0.13.0 | conda           | win-64          | py37_0, py36_0
                                          : Add .env support to your django/flask apps in development and deployments
Found 4 packages

Run 'anaconda show <USER/PACKAGE>' to get installation details

```

```
$ anaconda show  conda-forge/python-dotenv
Using Anaconda API: https://api.anaconda.org
Name:    python-dotenv
Summary: Get and set values in your .env file in local and production servers like Heroku does.
Access:  public
Package Types:  conda
Versions:
   + 0.6.0
   + 0.6.1
   + 0.8.0
   + 0.8.2
   + 0.9.1
   + 0.10.0
   + 0.10.1
   + 0.10.2
   + 0.10.3
   + 0.10.5
   + 0.12.0
   + 0.13.0
   + 0.14.0
   + 0.15.0

To install this package with conda run:
     conda install --channel https://conda.anaconda.org/conda-forge python-dotenv

```