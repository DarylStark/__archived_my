# New version

As soon as you're ready to release a new version, with a new versionnumber, you have to do a few steps. Usually, the versionnumber increases when a specific milestone is reached or when a new feature is added. The rules for version numers are;

-   The major is almost never increased
-   The minor is increased when a big new feature is added
-   The release is increased when small bugfixes are added but no new features

To increase the versionnumber, do the following steps;

-   Merge the `development` branch with the `main` branch
-   Make sure all changes are in the main branch
-   Run the unit tests, only proceed when they are all succeeded
-   In case of the Web UI: compile _and_ install the new files
-   Open the file `/tools/deploy-to-gae.py` and update the versionnumber for the services
-   Git commmit the code with the versionnumber in the commit message: `Version 1.0.0`
-   Create a Git tag for the new version: `git tag -a v1.0.0`
-   Push the new version to GitHub with the tags: `git push --tags`
-   Upload the new version to Google App Engine
-   Remove the old version from Google App Engine