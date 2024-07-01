from ._serializers import DictUISetting


def validate_ui_setting(jsonblob):
    if not jsonblob:
        return {}
    app_setting = DictUISetting.model_validate(jsonblob)
    return app_setting.root
