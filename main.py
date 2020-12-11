import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import subprocess

logger = logging.getLogger(__name__)


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()
        logger.info("preferences %s" % json.dumps(extension.preferences))
        item_name = subprocess.run(
            ["gnome-calculator", "-s", query], stdout=subprocess.PIPE, text=True
        ).stdout
        data = {"new_name": "%s was clicked" % item_name}
        items = [
            ExtensionResultItem(
                icon="images/icon.svg",
                name=item_name,
                description="Item description",
                on_enter=ExtensionCustomAction(data, keep_app_open=True),
            )
        ]

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name=data["new_name"],
                    on_enter=HideWindowAction(),
                )
            ]
        )


if __name__ == "__main__":
    DemoExtension().run()
