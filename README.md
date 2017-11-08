# Standard Container Integration Format (SCI-F) Apps

Hi there! This is the base for SCI-F apps. We just finished developing the nuts
and bolts, and will have instructions for contributing soon.

[![CircleCI](https://circleci.com/gh/containers-ftw/apps.svg?style=svg)](https://circleci.com/gh/containers-ftw/apps)

![robot](assets/img/app/robots/robot18.png)


## Contribute an App

**1. Prepare your Fork**
First, fork the repo, and clone it:

```
git clone git@github.com:<username>/apps.git
cd apps
```

Take a look at the folder `_apps`. This is a directory of markdown files, where each directory (and level) corresponds with a category, and each file is associated with one app. Basically, all you need to do is contribute a markdown file! Let's say we have a workflow app, and we want to add it to a new category, "flow." First let's make the folder.


```
# $PWD is apps
mkdir _apps/workflow
```

**2. Name your App**
Let's now copy the template there to work with. The name of the file will correspond with your app name. If put inside a folder, the folder must also be represented in the file name. Remember that the name is important - it will be the name of the markdown file (without the `.md` extension). For example, to name my app `workflow-internal-serial` under the folder `workflow` I would do:

```
cp _templates/appname-template.md _apps/workflow/workflow-internal-serial.md
```

Here I am anticipating that "workflow" is likely to be a general category that others might want to make apps for, so I'm creating it's own folder. Also remember that the app namespace must be unique, and so names should be very specific. I wouldn't want to give a general name like `workflow-run.md` because it is too general. There are likely going to be many workflows. So given a file name, the corresponding app name maps like this:

```
_apps/workflow/workflow-internal-serial.md --> workflow-internal-serial
```

**3. Customize the File**
Next, you should edit the file that you just copied with your app. Let's take a look:

      ---
      title:  "App Name"
      date:   YYYY-MM-DD HH:MM:SS
      author: Vanessa Sochat
      tags: 
      - scif
      - singularity
      files:
       - app-file.sh
       - SingularityApp.appname
      ---

      ```yaml
      %apprun appname
          exec $SINGULARITY_APPROOT/app-file.sh
      %appfiles appname
          app-file.sh
      ```

Notice that we have two sections - the top header has metadata, and the bottom is whatever sections you would include in a Singularity Recipe file. You can easily copy paste your container code at the bottom in the `yaml` section, and the only change you might need to make is renaming the app to the one that corresponds with the folder, e.g.:

```
%apprun appname  --> %apprun workflow-internal-serial
```

Now let's look at the metadata in the header:

 - **title** is a human readable title. Make sure it remains in quotes
 - **date** should correspond to the date that you created or are adding the app.
 - **author** is your alias
 - **tags** are important - they help to make your app searchable. This should be a yaml list of single terms
 - **files** are not required, but if you have them, you should create a folder named equivalently to your app (eg, `workflow-internal-serial` in the same folder as the markdown file, and add the files here. They will be provided if someone downloads your app. 

Finally, if you want to provide an isolated recipe for your app (perhaps as a suggested use case) you can add the recipe to a folder named corresponding to your app. Following the current example:

```
mkdir _apps/workflow/workflow-internal-serial
touch _apps/workflow/workflow-internal-serial/SingularityApp.workflow-internal-serial
```

**4. Preview and Submit**
You can preview locally with `bundle exec jekyll serve`. You can also test locally with `python -m unittest tests.test_recipes`. You should then commit changes to your branch, push to Github, and submit a pull request (PR) to the main branch. The same tests will be run, and when the PR is merged, will be live on the site.

That's it! The robots appreciate your contribution!

## Helpful Jekyll Tips

The tag to distinguish except from post is `<!--more-->`. If you want to define
a custom one in a post:

```
excerpt_separator: <!--readmore-->
```
