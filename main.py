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
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import subprocess

logger = logging.getLogger(__name__)


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()
        logger.info("preferences %s" % json.dumps(extension.preferences))
        result = subprocess.run(
            ["gnome-calculator", "-s", query], stdout=subprocess.PIPE, text=True
        ).stdout
        items = [
            ExtensionResultItem(
                icon="images/icon.svg",
                name=result,
                description="Enter to copy to the clipboard\nAlt-enter to open in calculator",
                on_enter=CopyToClipboardAction(result),
                on_alt_enter=RunScriptAction("gnome-calculator -e '%s'" % query),
            )
        ]

        return RenderResultListAction(items)


if __name__ == "__main__":
    DemoExtension().run()
