===================
argus-HTMx-frontend
===================

Experimental frontend for `argus-server`_ as a django app.

Will possibly cease to exist as a separate app if the experiment is deemed
successful.

See `argus-server`_ for more about argus.

Imports `django-htmx`_. See the `documentation for django-htmx`_
for details.

Moving to argus-server repo
---------------------------
This repo is in the process of being merged into the repo at `argus-server`_.

New issues and PRs should be opened against that repo, not this one.
Existing PRs will be merged here, then moved. Existing open issues will
also be moved (eventually).

Moving issues
~~~~~~~~~~~~~

Github seems to be able to handle this just fine.

Moving PRs
~~~~~~~~~~

Procedure for existing PRs:

The code tree has been changed from ``src/argus_htmx`` to ``src/argus/htmx``
so branches should be updated accordingly. Try ``git mv`` or ``git rebase``.

If you want to move the PR to the argus-server repo you first need to move the
branch, then start a new PR with the same name at argus-server, then link back
to any discussion in this repo from the new PR. Now you can close the PR in
this repo.

First, setup the remote.

1. Add `argus-server`_ as a remote::

        git remote add argus git@github.com:Uninett/Argus.git

2. Fetch the branches on argus::

        git fetch argus

3. Checkout master::

        git switch master

Second, prep the branch.

Make sure the files are in the right tree, ``src/argus/htmx``. ``src/argus``
*in this repo* has no ``__init__.py``, this is to avoid conflicts. Do not add
one. Do ``git mv src/argus_htmx src/argus/htmx`` or ``git rebase main
mybranch`` or use a graphical client to cherrypick one by one onto main. It is
enough to just move the files. Correcting import paths and file include paths
can be done *after* the move, in the new repo, with a new commit.

This way, you can deal with file renaming conflicts once, and content change
conflicts once.

Now you're ready for the move.

1. Make a temporary branch name for the branch you want to move, at its head::

        git switch mybranch
        git switch -c fvgyhj

2. If it's only a single commit you can cherrypick it. Move the real name to
   the master then cherry-pick::

        git branch -f mybranch master
        git switch mybranch
        git cherry-pick fvgyhj

   If not, a rebase can do it for you. If you didn't do step 1 correctly there
   will be more conflicts than necessary!

   How to rebase (assumes ``mybranch`` is rebased on ``main``)::

        git rebase --onto master main mybranch

   You can now remove the temporary branch::

        git branch -d fvgyhj

3. Push the branch to the new remote::

        git switch mybranch
        git push argus

4. Make the PR in argus-server and pull the branch in your local copy of that
   repo.

5. Do any internal changes to the actual code in the new repo if you didn't do
   that as a part of the branch prep.

Done!


How to play
===========

See the docs of argus-server. The rest of this README is deprecated but kept
here until everything has been moved.

Install
-------

To make sure you do not accidentally work on an old argus-server, do the following:

1. Use/make a venv, for instance: create a new one with ``python -m venv argus-htmx``
2. Check out argus-server code
3. Install argus-server dynamically into the venv: ``pip install -e .``
4. Check out this repo
5. Install this app dynamically into the venv: ``pip install -e .``

It is now safe to remove argus-server from the venv if you feel like it.

Configure
---------

Do this in your workdir, which could be the checked out `argus-server`_ repo.

This assumes that you have a local settings file (we recommend calling it
"localsettings.py" since that is hidden by .gitignore) as a sibling of
``src/``.

At the top of this local settings file, copy the contents of
``argus.htmx.settings``. This will base the settings-file on
``argus.site.settings.backend`` and automatically use
``argus.site.utils.update_settings`` with
``argus_htmx.app_config.APP_SETTINGS`` to set/overwrite some settings and
mutate others. Note the usage of ``globals()``; due to this, inheriting from
``argus.htmx.settings`` will probably not work as expected.

While developing you will probably prefer to swap out
``argus.site.settings.backend`` with ``argus.site.settings.dev``, as the former
is almost production-ready while the latter is tuned for development and
depends on the optional dependencies you can install via ``pip install
argus-server[dev]``.

The ``argus.site.utils.update_settings`` function will add or change the settings

* INSTALLED_APPS
* LOGIN_REDIRECT_URL
* LOGIN_URL
* LOGOUT_REDIRECT_URL
* LOGOUT_URL
* MIDDLEWARE
* PUBLIC_URLS
* ROOT_URLCONF
* TEMPLATES

See ``argus_htmx.appconfig._app_settings`` for what is being set. The
management command ``printsettings`` (which depends on the app
``django-extensions``, a ``dev``-dependency) will print out the complete
settings used.

Customizing
-----------

If you add more pages and endpoints you will have to write your own root
urls.py and set ROOT_URLCONF appropriately.

If you have some other apps you want installed and configured, you could either
add the necessary settings to your ``localsettings.py`` or use the extra-apps
machinery. The later is especially useful during the development phase when you
haven't settled on which apps to use yet.

With extra-apps machinery
~~~~~~~~~~~~~~~~~~~~~~~~~

You make a JSON-file which is read into your settings via one of two
environment variables.

In order to add apps and settings that *extend* ``argus-server`` and this
``app`` you use the environment variable ``ARGUS_EXTRA_APPS``::

    export ARGUS_EXTRA_APPS=`cat extra.json`

If you want to *override* existing apps the environment variable to use is
``ARGUS_OVERRIDING_APPS``::

    export ARGUS_OVERRIDING_APPS=`cat overriding.json`

Have a look at the contents of ``argus_htmx.appconfig._app_settings`` for an
example of what you can set this way.

You can merge your urlpatterns with the apps' urlpatterns via the
``argus.site.utils.get_urlpatterns`` function, see ``argus.htmx.urls`` for an
example.

Optional authentication backend settings
----------------------------------------

If using ``django.contrib.auth.backends.RemoteUserBackend`` (which depends on
the middleware ``django.contrib.auth.middleware.RemoteUserMiddleware``) there's
an optional setting ``ARGUS_REMOTE_USER_METHOD_NAME`` to choose what to show on
the button.

If using ``social_core.backends.open_id_connect.OpenIdConnectAuth`` there's an
optional setting ``ARGUS_OIDC_METHOD_NAME`` to choose what to show on the
button.

Both can be set via environment variables.

Update
======

On every new version, reinstall the dependencies since there might be new ones.

Themes and styling
==================

To try out daisyUI themes use the context processor
``argus_htmx.context_processor.theme_via_session`` instead of
``argus_htmx.context_processor.theme_via_GET``.

Default included themes are: `light`, `dark` and `argus`.

This project supports Tailwind CSS utility classes and daisyUI components for styling.
Below is an overview of the stack, installation and build instructions, and configuration details for themes and styles.

Overview
--------
* Tailwind CSS: A utility-first CSS framework for rapidly building custom user interfaces.
* daisyUI: A component library for Tailwind CSS that provides a set of ready-to-use components as well as color themes.

Installation and build instructions
-----------------------------------
Recommended but open for tweaks and adaptations steps:

1. Get Tailwind standalone CLI bundled with daisyUI from
   https://github.com/dobicinaitis/tailwind-cli-extra

   Most linux::

        $ curl -sL https://github.com/dobicinaitis/tailwind-cli-extra/releases/latest/download/tailwindcss-extra-linux-x64 -o /tmp/tailwindcss
        $ chmod +x /tmp/tailwindcss

   For other OSes see
   https://github.com/dobicinaitis/tailwind-cli-extra/releases/latest/ and
   update the bit after ``download/`` accordingly.

   Optionally you can compile tailwind+daisyUI standalone cli bundle yourself as described here:
   https://github.com/tailwindlabs/tailwindcss/discussions/12294#discussioncomment-8268378.
2. (Linux/OsX) Move the tailwindcss file to your $PATH, for instance to ``~/bin/`` or ``.local/bin``.
3. Go to the repo directory (parent of ``src/``)
4. Build main stylesheet file using ``tailwindcss`` executable from step 1 and
   pointing to the included config file:

   Manually::

        tailwindcss -c src/argus_htmx/tailwindtheme/tailwind.config.js -i src/argus_htmx/tailwindtheme/styles.css --output src/argus_htmx/static/styles.css

   Running with the ``--watch`` flag for automatic update on change seems
   error-prone so we've made it very easy to run the command, with ``make`` or ``tox``::

        make tailwind
        tox -e tailwind

   Either will rebuild the styles for you.


Customization
-------------

How to customize the look:

* Override Argus' Tailwind CSS theme defaults and/or choose which daisyUI
  color themes to include. You can do so by updating the default
  ``TAILWIND_THEME_OVERRIDE`` and ``DAISYUI_THEMES`` values respectively
  before running a ``tailwind_config`` management command:

  Via environment variables, for example::

    TAILWIND_THEME_OVERRIDE = '
      {
        "borderWidth": {
          "DEFAULT": "1px"
        },
        "extend": {
          "borderRadius": {
            "4xl": "2rem"
          }
        }
      }
    '
    DAISYUI_THEMES = '
      [
        "light",
        "dark",
        "cyberpunk",
        "dim",
        "autumn",
        { "mytheme": {
            "primary": "#009eb6",
            "primary-content": "#00090c",
            "secondary": "#00ac00",
            "secondary-content": "#000b00",
            "accent": "#ff0000",
            "accent-content": "#160000",
            "neutral": "#262c0e",
            "neutral-content": "#cfd1ca",
            "base-100": "#292129",
            "base-200": "#221b22",
            "base-300": "#1c161c",
            "base-content": "#d0cdd0",
            "info": "#00feff",
            "info-content": "#001616",
            "success": "#b1ea50",
            "success-content": "#0c1302",
            "warning": "#d86d00",
            "warning-content": "#110400",
            "error": "#ff6280",
            "error-content": "#160306"
            }
        }
      ]
    '

  Or by providing corresponding values in your local settings that star-imports from an `argus-server`_ settings file::

        TAILWIND_THEME_OVERRIDE = {...}
        DAISYUI_THEMES = [...]

  Some links that may be relevant for the customization values mentioned above:
    * `daisyUI themes`_
    * `list of daisyUI color names`_
    * `Tailwind CSS theme customization`_

* Override the default main stylesheet path by setting
  ``ARGUS_STYLESHEET_PATH`` in the environment. The path is under
  ``STATIC_URL``. This depends on the context processor
  ``argus_htmx.context_processors.path_to_stylesheet``.
* Include additional styles/stylesheets using the ``head`` block in your templates.
* Generate a Tailwind config file by running the ``tailwind_config`` management
  command. By default the generated file will be based on
  ``src/argus_htmx/tailwindtheme/tailwind.config.template.js`` and expected
  values will be injected with reasonable defaults.

UI Settings
===========

Incident table column customization
-----------------------------------
You can customize which columns are shown in the incidents listing table by overriding the
``INCIDENT_TABLE_COLUMNS`` setting. This setting takes a list of ``str`` or
``argus_htmx.incidents.customization.IncidentTableColumn`` instances. when given a ``str``, this
key must be available in the ``argus_htmx.incidents.customization.BUILTIN_COLUMNS`` dictionary. For
example::

    from argus_htmx.incidents.customization import BUILTIN_COLUMNS, IncidentTableColumn

    INCIDENT_TABLE_COLUMNS = [
        "id",
        "start_time",
        BUILTIN_COLUMNS["description"], # equivalent to just "description"
        IncidentTableColumn( # a new column definition
            name="name",
            label="Custom"
            cell_template="/path/to/template.html"
            context={
                "additional": "value"
            }
        ),

    ]

For inbuilt support for other types of columns see the howtos in `the local docs <docs/howtos/>`_.


.. _django-htmx: https://github.com/adamchainz/django-htmx
.. _argus-server: https://github.com/Uninett/Argus
.. _documentation for django-htmx: https://django-htmx.readthedocs.io/en/latest/
.. _daisyUI themes: https://daisyui.com/docs/themes/
.. _list of daisyUI color names: https://daisyui.com/docs/colors/#-2
.. _tailwind-cli-extra: https://github.com/dobicinaitis/tailwind-cli-extra
.. _Tailwind CSS theme customization: https://tailwindcss.com/docs/theme

Custom widget
-------------

Argus supports showing an extra widget next to the menubar in the incidents listing. This box can
take the width of 1/3 of the window. You can add the widget by creating a context processor that
injects an ``incidents_extra_widget`` variable that points to an html template::

    def extra_widget(request):
        return {
            "incidents_extra_widget": "path/to/_extra_widget.html",
        }

*note* Don't forget to include the context processor in your settings

You could then create ``path/to/_extra_widget.html`` as following::

    <div id="service-status" class="border border-primary rounded-2xl h-full p-2">
      My custom widget
    </div>


Page size
---------

By default, incidents are shown with a page size of ``10`` (ie. 10 rows at a time), and the user can
select a different page size from ``[10, 20, 50, 100]``. It possible to override these settings by
setting the ``ARGUS_INCIDENTS_DEFAULT_PAGE_SIZE`` and ``ARGUS_INCIDENTS_PAGE_SIZES`` setting
respectively.
