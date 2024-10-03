import inspect
import pathlib
from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template import engines
from django.template.context import make_context
from django.template.loader import get_template
from django.template import Template

from argus_htmx.themes.utils import get_themes
from argus_htmx import settings as argus_htmx_settings


# Copied from https://github.com/GEANT/geant-argus/pull/15 with minor modifications
class Command(BaseCommand):
    help = """\
Uses the template specified in the TAILWIND_CONFIG_TEMPLATE setting (default: tailwind/tailwind.config.js)
to dynamically build a tailwind.config.js. This file must be in an app's templates directory. The
template may contain:
 - a '{{ projectpaths }} section without square brackets that will be popuplated with auto discovered
 template dirs of installed apps
 - a '{{ daisyuithemes }}' section without square brackets that will be popuplated by the
daisyUI theme list specified in the DAISYUI_THEMES setting (default: ["dark", "light", {"argus"": {...}} ])
 - a '{{ themeoverride }}' section that will be popuplated by a dict containing tailwind theme options
 specified in TAILWIND_THEME_OVERRIDE setting (default: {})

This command also generates a `styles.css` that contains the base css file for tailwind to create
its final css file. It uses the template specified by the `TAILWIND_CSS_TEMPLATE` setting (default:
tailwind/styles.css). This file should also be in an app's templates directory

The `styles.css` template may iterate over `cssfiles` context variable that contains css
files/snippets that should be included in the final css file. Apps may define a
`tailwind_css_files` method that gives the location (as a str or pathlib.Path object) for every
css file from this app to include. (see argus_htmx.apps.HtmxFrontendConfig for an example)

Additional settings that govern the functionality of this command are:
 * TAILWIND_CONFIG_TARGET: the target location for writing the tailwind.config.js
 * TAILWIND_CSS_TARGET: override the base tailwind css file location (default: styles.css)

"""
    DEFAULT_CONFIG_TEMPLATE_PATH = "tailwind/tailwind.config.js"
    DEFAULT_CSS_TEMPLATE_PATH = "tailwind/styles.css"

    # DEFAULT_CONFIG_TARGET = "src/argus_htmx/tailwindtheme/tailwind.config.js"
    # DEFAULT_CSS_TARGET = "src/argus_htmx/tailwindtheme/styles.css"
    DEFAULT_CONFIG_TARGET = "tailwind.config.js"
    DEFAULT_CSS_TARGET = "styles.css"

    def handle(self, *args, **options):
        config_template_name = getattr(
            settings, "TAILWIND_CONFIG_TEMPLATE", self.DEFAULT_CONFIG_TEMPLATE_PATH
        )
        config_target_path = pathlib.Path(
            getattr(settings, "TAILWIND_CONFIG_TARGET", self.DEFAULT_CONFIG_TARGET)
        )
        css_template_name = getattr(
            settings, "TAILWIND_CSS_TEMPLATE", self.DEFAULT_CSS_TEMPLATE_PATH
        )
        css_target_path = pathlib.Path(
            getattr(settings, "TAILWIND_CSS_TARGET", self.DEFAULT_CSS_TARGET)
        )
        self.write_template(
            config_template_name,
            config_target_path,
            context=self.get_context(target_dir=config_target_path.parent),
            name="tailwind config",
        )
        self.write_template(
            css_template_name,
            css_target_path,
            context=self.get_context(target_dir=css_target_path.parent),
            name="tailwind base css",
        )

    def get_context(self, target_dir: pathlib.Path):
        return {
            "themeoverride": getattr(
                settings,
                "TAILWIND_THEME_OVERRIDE",
                argus_htmx_settings.TAILWIND_THEME_OVERRIDE,
            ),
            "daisyuithemes": get_themes(),
            "projectpaths": "\n".join(
                f"        '{d}/**/*.html'," for d in self.get_template_dirs()
            ),
            "cssfiles": (
                self.make_relative(p, target_dir)
                for p in sorted(self.get_css_files(), key=lambda p: p.stem)
            ),
        }

    def write_template(self, template_name, target_path, context, name):
        pathlib.Path(target_path).write_text(
            self.render_file(template_name=template_name, context=context)
        )

        self.stdout.write(f"Wrote {name} to '{target_path}'")

    @staticmethod
    def render_file(template_name: str, context):
        template = get_template(template_name)
        return template.template.render(make_context(context, autoescape=False))

    @staticmethod
    def get_template_dirs():
        for engine in engines.all():
            yield from getattr(engine, "template_dirs", [])

    @staticmethod
    def get_css_files():
        for app in apps.get_app_configs():
            if callable(css_files := getattr(app, "tailwind_css_files", None)):
                yield from (pathlib.Path(p) for p in css_files())

    @staticmethod
    def make_relative(path: pathlib.Path, base_path: pathlib.Path):
        try:
            return path.relative_to(base_path.absolute())
        except ValueError:
            return path
